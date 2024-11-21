#!/bin/bash

for server in sbnd-evb01 sbnd-evb02 sbnd-evb03 sbnd-evb04 sbnd-evb05 sbnd-evb06 sbnd-evb07
do
    ssh sbndraw@$server 'cd /home/nfs/sbndraw/fts_stuff/sbndaq-xporter/FTS_config; source setup_fts_sbnd.sh; stop_fts; start_fts'
done

