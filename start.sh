 #!/bin/bash

echo "------------------------------------ start.sh ----------------------------------------------"
/usr/bin/python3 sonoff-switches.py > /home/pi/Remote-Controlled-Home-Lights/sonoff.log 2>&1
echo "DONE"
