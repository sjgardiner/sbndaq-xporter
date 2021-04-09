#!/bin/bash

crontab_file=$1

for server in icarus-evb01 icarus-evb02 icarus-evb03 icarus-evb04 icarus-evb05 icarus-evb06
do
    echo "Executing: ssh ${server} crontab ~icarus/FileTransfer/sbndaq-xporter/Xporter/${crontab_file}"
    ssh $server "crontab ~icarus/FileTransfer/sbndaq-xporter/Xporter/${crontab_file}"
done

