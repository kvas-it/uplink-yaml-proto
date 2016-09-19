"""Uplink prototype command line interface."""

import logging

import click

from . import core

log = logging.getLogger(__name__)


@click.group()
@click.option('--backend', '-b', default='vagrant', show_default=True,
              envvar='UPLINK_BACKEND', help='Virtualisation backend')
@click.option('--uplinkfile', '-u', default='uplink.yaml', show_default=True,
              type=click.File('r'), envvar='UPLINKFILE',
              help='Configuration file.')
@click.option('--uplink-dir', default='.uplink', show_default=True,
              envvar='UPLINK_DIR', help='Directory for keeping uplink state.')
@click.option('--debug', '-d', is_flag=True, default=False,
              help='Show debugging information.')
@click.option('--verbose', '-v', is_flag=True, default=False,
              help='Show additional information.')
@click.pass_context
def cli(ctx, **options):
    if options['verbose']:
        logging.basicConfig(level=logging.INFO)
    if options['debug']:
        logging.basicConfig(level=logging.DEBUG)
    ctx.obj = core.Uplink(**options)


@cli.command()
@click.pass_obj
def status(uplink):
    """Display current status."""
    uplink.backend.get_container_states()


@cli.command()
@click.pass_obj
@click.argument('task')
def run(uplink, task):
    """Run a task."""
    uplink.run_task(task)


@cli.command()
@click.pass_obj
@click.argument('container')
def create(uplink, container):
    """Create one container."""
    uplink.create_container(container)


@cli.command()
@click.pass_obj
@click.argument('container')
def delete(uplink, container):
    """Delete one container."""
    uplink.delete_container(container)


@cli.command('delete-all')
@click.pass_obj
def delete_all(uplink):
    """Delete all containers."""
    uplink.delete_all_containers()
