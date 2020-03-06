#!/bin/bash

# Check to see if argument 1 is a directory
datahome="/daqdata"

if [ -d "$1" ]; then
    datahome="$1"
fi

# List "physics" file types
# Eliminate lariat_physics_*.dat from list
#for file in $(ls $datahome/lariat_r??????_sr????.root $datahome/lariat_physics_*.dat $datahome/lariat_pedestal_*.root); do
#for file in $(ls $datahome/sbnd_r??????_sr????.root $datahome/sbnd_r??????_sr???.root $datahome/sbnd_r??????_sr??.root $datahome/sbnd_r??????_sr?.root); do

for file in $(ls $datahome/sbnd_r??????_*.root $datahome/digits_sbnd_r??????_*.root); do
#
#  add raw pedestal files to list
#    complete files have a .dat.complete extensions
    fileBase=${file%'.root'}
#    fileBase1=${file%'.root'}
#    fileBase=${fileBase1%'.dat'}

    # Does either *.complete or *.complete.error file already exist?
    #  If not, check to see if closed and make .complete file
    if [ ! -f $fileBase.complete -a ! -f $fileBase.complete.error ]; then

#
#  3/2/16 removed requirement for checking if file is closed
#    Insert sleep command instead
#        # Check if data file is closed
#	if [[ !`lsof $file` ]]; then
#            echo File $file ready for archiving, creating .complete file
#            touch $fileBase.complete
#       fi
	sleep 2s
	touch $fileBase.complete
    fi
done


