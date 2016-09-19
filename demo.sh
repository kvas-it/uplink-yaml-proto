#!/bin/sh
# Demo script for Redmine configuration.

if [ ! -d venv ]; then
  pyvenv venv
fi

. venv/bin/activate
pip install -r requirements.txt

export UPLINKFILE=redmine.yaml

# Delete the leftovers from previous runs.
uplink delete-all

# Create the containers.
uplink create application
uplink create database

# Initialise the database and Redmine config.
uplink run init

# Start Redmine (on http://10.8.10.8:3000/).
uplink run start

echo http://10.8.10.8:3000/
