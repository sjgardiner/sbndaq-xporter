#!/bin/bash

find /daq/log/* -type f -mtime +90 -exec rm -f {} \;
find /daq/log/metrics/* -type f -mtime +14 -exec rm -f {} \;
find /daq/log/fts_logs/* -type f -mtime +14 -exec rm -f {} \;
rm /daq/log/grafana/graphite/exception.log
rm /daq/log/grafana/carbon/listener.log
#find /data/onmon_files -name '*.root' -type f -mtime 0.25 -delete
