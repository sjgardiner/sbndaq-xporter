#!/bin/bash

find /daq/log/* -type f -mtime +90 -exec rm -f {} \;
#find /data/onmon_files -name '*.root' -type f -mtime 0.25 -delete
