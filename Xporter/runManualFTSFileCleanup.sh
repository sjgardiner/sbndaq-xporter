#!/bin/bash

timestamp=`date +%Y_%m_%d_%H_%M`
logfile="/daq/log/fts_logs/`hostname`/FileCleanup_`hostname`_${timestamp}.log"

python /home/nfs/icarus/FileTransfer/sbndaq-xporter/Xporter/ManualFTSFileCleanup.py >> ${logfile} 2>&1

exit 0
