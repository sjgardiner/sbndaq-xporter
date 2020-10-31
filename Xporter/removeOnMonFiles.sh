#!/bin/bash

find /data/onmon_files -name '*.root' -type f -mtime +0.25 -delete
