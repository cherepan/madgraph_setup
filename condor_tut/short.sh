#!/bin/bash
# short.sh: a short discovery job
printf "Start time: "; /bin/date
printf "Job is running on node: "; /bin/hostname
printf "Job running as user: "; /usr/bin/id
printf "Job is running in directory: "; /bin/pwd
echo "$ncpu"
echo "$nEv"
echo "$seed"
printf $nEv,$seed,$ncpu,'\n'
echo "\n Working hard..."
sleep 3
echo "Science complete!"
