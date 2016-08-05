#!/usr/bin/env python

import yaml
import sys


data = yaml.load(sys.stdin)
print yaml.dump(data, default_flow_style=False)
