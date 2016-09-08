"""Uplink prototype project config (uplinkfile) handling."""

import logging
import sys
import yaml


log = logging.getLogger(__name__)


class Uplinkfile(object):
    """Description of the project for uplink system."""

    def __init__(self, filename, data):
        self.filename = filename
        self.data = data


def load(file):
    """Load uplinkfile from an open yaml file."""
    log.debug('Loading uplinkfile from ' + file.name)
    try:
        data = yaml.load(file)
        return Uplinkfile(file.name, data)
    except yaml.error.YAMLError as err:
        sys.exit(err)
