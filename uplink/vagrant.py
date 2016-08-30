"""Uplink prototype vagrant integration support."""

from jinja2 import Environment, PackageLoader


BOX_MAP = {
    'debian:jessie': 'debian/contrib-jessie64',
}


def generate_vagrantfile(conf):
    """Generate a vagrantfile from configuration.

    Returns vagrantfile as a string.
    """
    env = Environment(loader=PackageLoader('uplink', 'templates'))
    tmpl = env.get_template('vagrantfile.tmpl')
    vagrant_data = {'vms': []}
    for name, container in conf.data['containers'].items():
        vm = {}
        vm['name'] = name
        vm['hostname'] = name + '.local'
        vm['ip'] = container['network']['ip']
        vm['box'] = BOX_MAP[container['from']]
        vm['shell_provision'] = container['commands']
        vagrant_data['vms'].append(vm)
    return tmpl.render(config_name=conf.filename, **vagrant_data)
