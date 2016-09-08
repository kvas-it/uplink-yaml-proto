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

    def _run_vagrant(self, *args):
        cmd = ['vagrant', '--machine-readable'] + list(args)
        output = subprocess.check_output(cmd, cwd=self.rootdir)
        lines = str(output, 'utf-8').split('\n')
        return [VagrantMessage(*l.split(',', 3)) for l in lines if l]

    def get_container_states(self):
        """Return the states of the containers."""
        states = {}
        for msg in self._run_vagrant('status'):
            if msg.type == 'state':
                states[msg.target] = msg.data
        return states
