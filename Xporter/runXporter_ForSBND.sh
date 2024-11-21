#!/bin/bash

timestamp=`date +%Y_%m_%d`
now=`date "+%Y-%m-%d %T"`
#logfile="/daq/log/fts_logs/`hostname`/xporter_`hostname`_${timestamp}.log"
#logfile_attempt="/daq/log/fts_logs/`hostname`/attempt_xporter_`hostname`_${timestamp}.log"

logfile="/daq/log/fts_logs/xporter.log"  
logfile_attempt="/daq/log/fts_logs/attempt_xporter.log" 

# clear big logs
logsize=$(du -b "$logfile" | cut -f 1)
if ((logsize>100000000)); then
	rm "$logfile"
	rm "$logfile_attempt"
fi

file_lock="/tmp/xporter_`hostname`.lock"

if [ -f $file_lock ]; then
    echo "$now : Xport in progress! Do not run" 2>&1 | tee -a ${logfile_attempt}
    exit 0
fi

echo "$now : Xport Starting! Obtaining lock file $file_lock now!" 2>&1 | tee -a ${logfile_attempt}

touch $file_lock

echo $timestamp >> ${logfile} 2>&1

source /daq/software/products/setup
setup root v6_26_06 -q e26:p3913:prof

my_urllib3_version=$(pip3 freeze | grep urllib3 | sed -e 's/urllib3==//')
if [ "${my_urllib3_version}" != "1.25.6" ]; then
  # Install downgraded version of urllib3 to avoid versioning problems with
  # OpenSSL
  pip3 install --user urllib3==1.25.6
fi

(( $(pip3 freeze |grep requests |wc -l) )) ||  { echo "requests is missing; installing requests..."; pip3 install --user requests; }

python3 -u /home/nfs/sbndraw/fts_stuff/sbndaq-xporter/Xporter/Xporter.py /data/sbndraw/fts_data /data/sbndraw/fts_dropbox sbn_nd 2>&1 | tee -a ${logfile}

echo "$now : Xport Finished! Releasing lock file $file_lock now!" 2>&1 | tee -a ${logfile_attempt}

rm $file_lock
