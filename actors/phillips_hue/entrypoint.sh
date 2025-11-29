#!/bin/sh
python3 -u /scripts/controller_api.py &
python3 -u /scripts/phillips_hue.py &
wait