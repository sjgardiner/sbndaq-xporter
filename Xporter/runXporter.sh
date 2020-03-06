#!/bin/bash

timestamp=`date +%Y_%m_%d`
logfile="xporter_`hostname`_${timestamp}.log"

file_lock="/tmp/xporter_`hostname`.lock"

if [ -f $file_lock ]; then
    echo "Xport in progress! Do not run"
    exit 0
fi

touch $file_lock

#echo $logfile
#echo $timestamp

python /home/nfs/icarus/FileTransfer/sbndaq-xporter/Xporter/Xporter.py /data/daq /data/test_dropbox3 none sbndaq_v0_04_03 DataXportTesting_03Feb2020 >> /home/nfs/icarus/FileTransfer/Xporter_logs/${logfile} 2>&1

rm $file_lock
