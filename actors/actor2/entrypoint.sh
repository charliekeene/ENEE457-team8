#!/bin/sh
python3 -u /scripts/actor_scripts/controller_api.py &
python3 -u /scripts/actor_scripts/actor2.py &
wait