"""Uplink prototype vagrant backend."""

import collections
import os
import subprocess

from jinja2 import Environment, PackageLoader


BOX_MAP = {
    'debian:jessie': 'debian/contrib-jessie64',
}


VagrantMessage = collections.namedtuple(
    'VagrantMessage',
    ['timestamp', 'target', 'type', 'data']
)


class VagrantBackend(object):
    """Vagrant container management backend."""

    def __init__(self, uplink):
        self.uplink = uplink
        self.rootdir = os.path.join(uplink.rootdir, 'vagrant')
        if not os.path.isdir(self.rootdir):
            os.mkdir(self.rootdir)
        self._write_vagrantfile()

    def _write_vagrantfile(self):
        """Generate vagrantfile."""
        env = Environment(loader=PackageLoader('uplink', 'templates'))
        tmpl = env.get_template('vagrantfile.tmpl')
        params = {'vms': []}
        for name, container in self.uplink.containers.items():
            vm = {}
            vm['name'] = name
            vm['hostname'] = name + '.local'
            vm['ip'] = container['network']['ip']
            vm['box'] = BOX_MAP[container['from']]
            vm['shell_provision'] = container['commands']
            params['vms'].append(vm)
        with open(os.path.join(self.rootdir, 'Vagrantfile'), 'w') as file:
            file.write(tmpl.render(**params))

    def _write_shell_script(self, commands):
        env = Environment(loader=PackageLoader('uplink', 'templates'))
        tmpl = env.get_template('shellscript.tmpl')
        with open(os.path.join(self.rootdir, 'script.sh'), 'w') as file:
            file.write(tmpl.render(commands=commands))
        return 'script.sh'

    def _run_vagrant(self, *args):
        # TODO: Yield the lines instead of returning them all at once.
        cmd = ['vagrant', '--machine-readable'] + list(args)
        output = subprocess.check_output(cmd, cwd=self.rootdir)
        lines = str(output, 'utf-8').split('\n')[:-1]
        for line in lines:
            try:
                yield VagrantMessage(*line.split(',', 3))
            except TypeError:
                yield line

    def get_container_states(self):
        """Return the states of the containers."""
        states = {}
        for msg in self._run_vagrant('status'):
            if msg.type == 'state':
                states[msg.target] = msg.data
        return states

    def create_container(self, container_name):
        """Create one container."""
        for msg in self._run_vagrant('up', container_name):
            print(msg)

    def delete_all_containers(self):
        """Delete all containers."""
        for msg in self._run_vagrant('destroy', '-f'):
            if msg.type == 'ui':
                print(msg.data)

    def delete_container(self, container_name):
        """Delete one container."""
        for msg in self._run_vagrant('destroy', '-f', container_name):
            if msg.type == 'ui':
                print(msg.data)

    def run_task(self, task_name):
        """Run one task."""
        for step in self.uplink.tasks[task_name]:
            if isinstance(step, dict):
                for container_name, commands in step.items():
                    script_name = self._write_shell_script(commands)
                    result = self._run_vagrant(
                        'ssh', container_name, '--', 'sudo', '-E', '-H',
                        '/bin/sh', '/vagrant/' + script_name
                    )
                    for msg in result:
                        print(msg)
            else:
                self.run_task(step)
