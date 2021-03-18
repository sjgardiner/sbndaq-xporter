#!/bin/bash

find /data/daq -name 'RootDAQOut*.root' -type f -mtime +2 -exec rm -f {} +
