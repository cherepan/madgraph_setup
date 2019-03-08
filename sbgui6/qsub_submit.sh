#! /bin/bash     
echo 'Starting Job'       
export workdir=$(pwd)     
export HOME=$(pwd)     
cd /home-pbs/vcherepa/MG/madgraph_setup/sbgui6
/home-pbs/vcherepa/MG/madgraph_setup/sbgui6/short.sh 5 7 8 
echo 'Completed Job'    
