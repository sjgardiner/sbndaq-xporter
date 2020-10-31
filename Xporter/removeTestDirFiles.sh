#!/bin/bash

find /data/test_daq -name '*.root' -type f -mtime +0.25 -delete
