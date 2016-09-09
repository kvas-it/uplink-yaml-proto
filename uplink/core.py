"""Uplink core."""

import os

from . import uplinkfile, vagrant


class UplinkError(Exception):
    """Errors specific to uplink."""


class Uplink(object):
    """Uplink engine."""

    def __init__(self, **options):
        """Read the uplinkfile and initialise uplink."""
        if options['backend'] != 'vagrant':
            raise UplinkError('Only vagrant backend is supported.')
        self.options = options
        self.uplinkfile = uplinkfile.load(options['uplinkfile'])
        self.rootdir = os.path.join(os.getcwd(), self.options['uplink_dir'])
        if not os.path.isdir(self.rootdir):
            os.mkdir(self.rootdir)
        self.backend = vagrant.VagrantBackend(self)

    @property
    def containers(self):
        return self.uplinkfile.data.get('containers', {})

    @property
    def tasks(self):
        return self.uplinkfile.data.get('tasks', {})

    def run_task(self, task_name):
        if task_name not in self.tasks:
            raise UplinkError('Invalid task name: ' + task_name)
        return self.backend.run_task(task_name)

    def create_container(self, container_name):
        if container_name not in self.containers:
            raise UplinkError('Invalid container name: ' + container_name)
        return self.backend.create_container(container_name)

    def delete_all_containers(self):
        return self.backend.delete_all_containers()

    def delete_container(self, container_name):
        if container_name not in self.containers:
            raise UplinkError('Invalid container name: ' + container_name)
        return self.backend.delete_container(container_name)
