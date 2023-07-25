#!/bin/bash

timestamp=`date +%Y_%m_%d_%H_%M`
logfile="/daq/log/fts_logs/`hostname`/FileCleanup_`hostname`_${timestamp}.log"

python3 /home/nfs/icarus/FileTransfer/sbndaq-xporter/Xporter/ManualFTSFileCleanup.py >> ${logfile} 2>&1

#Run with argument 'ONLINE' in order to remove files once they are on dCache, but not confirmed on tape.
#python3 /home/nfs/icarus/FileTransfer/sbndaq-xporter/Xporter/ManualFTSFileCleanup.py ONLINE >> ${logfile} 2>&1

exit 0
