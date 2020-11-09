 #!/bin/bash

echo "------------------------------------ start.sh ----------------------------------------------"
/usr/bin/python3 /home/stankovic/Remote-Controlled-Home-Lights/the_home_gateway.py > /home/stankovic/Remote-Controlled-Home-Lights/the_home_gateway.log 2>&1
echo "DONE"
