#!/bin/sh
python3 -u /scripts/actor_scripts/controller_api.py &
python3 -u /scripts/actor_scripts/amazon_alexa.py &
wait