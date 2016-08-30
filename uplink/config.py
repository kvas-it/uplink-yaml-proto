"""Uplink prototype configuration handling."""

import logging
import sys
import yaml


log = logging.getLogger(__name__)


class Config(object):
    """Uplink configuration."""

    def __init__(self, filename, data):
        self.filename = filename
        self.data = data


def load_yaml(file):
    """Load configuration from an open yaml file."""
    log.debug('Loading configuration from ' + file.name)
    try:
        data = yaml.load(file)
        return Config(file.name, data)
    except yaml.error.YAMLError as err:
        sys.exit(err)
