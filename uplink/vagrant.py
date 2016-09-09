"""Uplink prototype vagrant backend."""

import collections
import os
import subprocess

from jinja2 import Environment, PackageLoader


BOX_MAP = {
    'debian:jessie': 'debian/contrib-jessie64',
}


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
        cmd = ['vagrant'] + list(args)
        subprocess.check_call(cmd, cwd=self.rootdir)

    def get_container_states(self):
        """Return the states of the containers."""
        self._run_vagrant('status')

    def create_container(self, container_name):
        """Create one container."""
        self._run_vagrant('up', container_name)

    def delete_all_containers(self):
        """Delete all containers."""
        self._run_vagrant('destroy', '-f')

    def delete_container(self, container_name):
        """Delete one container."""
        self._run_vagrant('destroy', '-f', container_name)

    def run_task(self, task_name):
        """Run one task."""
        for step in self.uplink.tasks[task_name]:
            if isinstance(step, dict):
                for container_name, commands in step.items():
                    script_name = self._write_shell_script(commands)
                    self._run_vagrant(
                        'ssh', container_name, '--', 'sudo', '-E', '-H',
                        '/bin/sh', '/vagrant/' + script_name
                    )
            else:
                self.run_task(step)
