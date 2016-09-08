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
