#!/bin/bash

timestamp=`date +%Y_%m_%d`
now=`date "+%Y-%m-%d %T"`
logfile="/daq/log/fts_logs/`hostname`/xporter_`hostname`_${timestamp}.log"
logfile_attempt="/daq/log/fts_logs/`hostname`/attempt_xporter_`hostname`_${timestamp}.log"

file_lock="/tmp/xporter_`hostname`.lock"

if [ -f $file_lock ]; then
    echo "$now : Xport in progress! Do not run" >> ${logfile_attempt} 2>&1
    exit 0
fi

echo "$now : Xport Starting! Obtaining lock file $file_lock now!" >> ${logfile_attempt} 2>&1

touch $file_lock

#echo $logfile

#echo $timestamp >> ${logfile} 2>&1

source /daq/software/products/setup
setup root v6_22_06a -q e20:p383b:prof

(( $(pip3 freeze |grep requests |wc -l) )) ||  { echo "requests is missing; installing requests..."; pip3 install --user requests; }

#python3 /home/nfs/icarus/FileTransfer/sbndaq-xporter/Xporter/Xporter.py /data/daq /data/fts_dropbox none >> ${logfile} 2>&1
python3 -u /home/nfs/icarus/FileTransfer/sbndaq-xporter/Xporter/Xporter.py /data/daq /data/fts_dropbox none sbndaq_v0_04_03 DataXportTesting_03Feb2020 >> ${logfile} 2>&1
#python3 /home/nfs/icarus/FileTransfer/sbndaq-xporter/Xporter/Xporter.py /data/daq /data/fts_dropbox none sbndaq_v0_04_03 DataXportTesting_03Feb2020 


#echo "done?"

echo "$now : Xport Finished! Releasing lock file $file_lock now!" >> ${logfile_attempt} 2>&1

rm $file_lock

exit 0
