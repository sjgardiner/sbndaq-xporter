#!/bin/bash

for server in icarus-evb01 icarus-evb02 icarus-evb03 icarus-evb04 icarus-evb05 icarus-evb06
do
    echo "Executing: rm /tmp/xporter*.lock"
    ssh $server "rm /tmp/xporter*.lock"
    echo "Executing: rm /data/daq/XporterInProgress*"
    ssh $server "rm /data/daq/XporterInProgress*"
done

