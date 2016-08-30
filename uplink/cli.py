"""Uplink prototype command line interface."""

import click
import logging

from . import config
from . import vagrant


log = logging.getLogger(__name__)


@click.group()
@click.option('--config-file', '-c', default='uplink.yaml', show_default=True,
              type=click.File('r'), help='Configuration file.')
@click.option('--debug', '-d', is_flag=True, default=False,
              help='Show debugging information.')
@click.option('--verbose', '-v', is_flag=True, default=False,
              help='Show additional information.')
@click.pass_context
def cli(ctx, **kw):
    ctx.obj = kw
    if kw['verbose']:
        logging.basicConfig(level=logging.INFO)
    if kw['debug']:
        logging.basicConfig(level=logging.DEBUG)


@cli.command()
@click.option('--output-file', '-o', type=click.File('w'), show_default=True,
              default='Vagrantfile', help='Output file')
@click.pass_context
def vagrantfile(ctx, output_file):
    """Generate a Vagrantfile for the project.

    The generated Vagrantfile will include all containers defined by the
    conifguration file.
    """
    conf = config.load_yaml(ctx.obj['config_file'])
    vagrantfile = vagrant.generate_vagrantfile(conf)
    output_file.write(vagrantfile)
