#!/bin/sh
#
# Demo script for Redmine configuration.
#
# This should be run with a virtualenv that has uplink installed
# (note that Uplink prototype requires Python 3):
#
# 	$ pyvenv venv                # create virtualenv
# 	$ . venv/bin/activate        # activate it
# 	(venv)$ ./demo-1.sh          # run this demo script
#
# If one of the commands fails, we need to interrupt the whole thing. After
# that we would need to delete the half-created containers and redo it.
set -ex

export UPLINK_UPLINKFILE=redmine-2.yaml

# Delete the leftovers from previous runs.
uplink delete-all

# Create the containers.
uplink create application
uplink create database

# Initialise the database and Redmine config.
uplink run init

# Start Redmine (on http://10.8.10.8:3000/).
uplink run start
