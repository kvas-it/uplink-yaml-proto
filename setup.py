"""Uplink prototype."""

from setuptools import setup

setup(
    name='uplink',
    version='0.1.0',
    description='Uplink prototype',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    packages=['uplink'],
    install_requires=['pyyaml', 'click', 'jinja2'],
    extras_require={
        'test': ['pytest'],
    },
    package_data={
        'uplink': ['templates/vagrantfile.tmpl'],
    },
    entry_points={
        'console_scripts': [
            'uplink=uplink.cli:cli',
        ],
    },
)
