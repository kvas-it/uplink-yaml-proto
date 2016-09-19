"""Uplink prototype project config (uplinkfile) handling."""

import logging
import string
import sys

import yaml


log = logging.getLogger(__name__)


class Uplinkfile(object):
    """Description of the project for uplink system."""

    def __init__(self, filename, data):
        self.filename = filename
        self.variables = data['variables']
        self.containers = self._expand_vars(data['containers'] or {})
        self.tasks = self._expand_vars(data['tasks'] or {})

    def _expand_vars(self, value):
        if isinstance(value, list):
            return [self._expand_vars(i) for i in value]
        if isinstance(value, dict):
            return {k: self._expand_vars(v) for k, v in value.items()}
        if isinstance(value, str) and '$' in value:
            return string.Template(value).substitute(self.variables)
        return value


def load(file):
    """Load uplinkfile from an open yaml file."""
    log.debug('Loading uplinkfile from ' + file.name)
    try:
        data = yaml.load(file)
        return Uplinkfile(file.name, data)
    except yaml.error.YAMLError as err:
        sys.exit(err)
