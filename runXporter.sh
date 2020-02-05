#!/bin/bash

timestamp=`date +%Y_%m_%d`
logfile="xporter_`hostname`_${timestamp}.log"

#echo $logfile
#echo $timestamp

python /home/nfs/icarus/FileTransfer/sbndaq-xporter/Xporter.py /data/daq /data/test_dropbox3 none sbndaq_v0_04_03 DataXportTesting_03Feb2020 >> /home/nfs/icarus/FileTransfer/Xporter_logs/${logfile} 2>&1

