#!/usr/bin/env python

from __future__ import print_function

import argparse
import code
import pprint
import sys
import yaml


parser = argparse.ArgumentParser(description='Load and dump a yaml file')
parser.add_argument('input', type=argparse.FileType('r'), nargs='?',
                    default='-', help='Input file')
parser.add_argument('-i', '--interactive', action='store_true',
                    help='Start interactive session after loading the data')
parser.add_argument('-p', '--print', action='store_true',
                    help='Dump the loaded data structure as Python')
parser.add_argument('-y', '--yaml', action='store_true',
                    help='Dump the loaded data as YAML')
args = parser.parse_args()

try:
    data = yaml.load(args.input)
except yaml.error.YAMLError as err:
    sys.exit(err)

if getattr(args, 'print'):
    pprint.pprint(data)
if args.yaml:
    print(yaml.dump(data, default_flow_style=False))
if args.interactive:
    code.interact(local={'data': data})
