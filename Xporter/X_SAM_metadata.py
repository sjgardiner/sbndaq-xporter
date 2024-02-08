#import modules
#
import os
import sys
import time
import safe
from runperiod import runperiod
import SAMUtilities
import json
import re
from datetime import datetime
import random
import time

import offline_run_history
import ROOT
from ROOT import TFile,TTree
#
# Begin SAM metadata function
#
def SAM_metadata(filename, projectvers, projectname, detectorname):
    "Subroutine to write out SAM information"
    
    metadata = {}

    #get filesize
    metadata["file_size"] = os.stat(filename).st_size 
    
    #get file name
    fname = filename.split("/")[-1]
    metadata["file_name"] = fname 

    #file type
    metadata["file_type"] = "data" 

    #file format is artroot
    metadata["file_format"] = "artroot" 
    
    #file tier is rawdata
    metadata["data_tier"] = "raw"

    #
    if(detectorname=="sbn_nd"):
        metadata["sbn_dm.detector"] = "sbn_nd"  
    elif(detectorname=="sbn_fd"):
        metadata["sbn_dm.detector"] = "sbn_fd"

    #file stream [beam trigger]
    stream = "commissioning"
    for part in fname.split("_"):
        if(part.find("fstrm")==0):
            stream = part[5:].lower()
            break
    print("data_stream = '%s'"%stream)
    metadata["data_stream"] = stream  

    #get run number from file name
    run_num = 0
    for part in fname.split("_"):
        if (part.find("run")==0): 
            run_num = int(part[3:])
            break
    print("RunNum = %d" % run_num)

    metadata["runs"] = [ [ run_num , "physics"] ] 

    #checksum
    checksum = SAMUtilities.adler32_crc(filename)
    checksumstr = "enstore:%s" % checksum

    print("Checksum = %s" % checksumstr)


    #time
    gmt = time.gmtime(os.stat(filename).st_mtime)
    time_tuple =time.struct_time(gmt) #strftime("%d-%b-%Y %H:%M:%S",gmt)
    
    metadata["sbn_dm.file_year"] = time_tuple[0] 
    metadata["sbn_dm.file_month"] = time_tuple[1] 
    metadata["sbn_dm.file_day"] = time_tuple[2] 

    #print "Creation time:", timestr

    
    metadata["checksum"] = [ checksumstr ]  
    
    if(detectorname=="sbn_nd"):
        try:
            print("SBND database is not up yet and therefore, currently we are defining projectname, projectversion, configuration, project stage variables manually. Once the SBND database is up and running, then these variables will be retrieved from the SBND database directly as done for ICARUS.")
            metadata["sbnd_project.version"]="v0_07_01"
            metadata["sbnd_project.name"]="sbnd_daq_v0_07_01"
            metadata["configuration.name"] ="standard"
            metadata["sbnd_project.stage"] = "daq"
            metadata["sbn_dm.beam_type"] = "none"
            metadata["sbn.experiment"] = "sbnd"

            # Implementation of random floats for SBND metadata
            # 8 Feb 2024, S. Gardiner
            #
            # First get a random number on [0, 1) using the current run number
            # as a seed. This ensures that all files with the same run number
            # have the same value in the SAM metadata.
            random.seed( run_num )
            sbnd_random_run = random.random()
            metadata["sbnd.random_run"] = sbnd_random_run

            # Now ensure a unique seed using the system time and the file name
            # together
            seconds_since_epoch = time.time()
            file_hash = hash( fname )
            my_unique_seed = seconds_since_epoch + file_hash
            random.seed( my_unique_seed )
            sbnd_random = random.random()
            metadata["sbnd.random"] = sbnd_random

        except:
            print("Failed to connect to database.")

    #ICARUS specific fields for bookkeping 
    elif(detectorname=="sbn_fd"):
        try:
            result=offline_run_history.RunHistoryiReader().read(run_num)
            dictionary={**result[1]}

            if len(dictionary)==0:
                print("...pending run records failed. trying run records")
                result = offline_run_history.RunHistoryiReader(ucondb_uri='https://dbdata0vm.fnal.gov:9443/icarus_on_ucon_prod/app/data/run_records/configuration/key=%d').read(run_num)
                dictionary={**result[1]}

            version = dictionary.get('projectversion')

            metadata["icarus_project.version"] = version.rsplit()[0] #"raw_%s" % projectvers  

            metadata["icarus_project.name"] = "icarus_daq_%s" % version.rsplit()[0] #projectname

            metadata["configuration.name"] = dictionary.get('configuration')

            s = dictionary.get('configuration').lower()

        except Exception as e:
            print('X_SAM_Metadata.py exception: '+ str(e))
            print(datetime.now().strftime("%T"), "Failed to connect to RunHistoryReader")

            metadata["icarus_project.stage"] = "daq" #runperiod(int(run_num)) 

       
            # beam options
            beambnb = "bnb"
            beamnumi = "numi"
            laser = "laser"
            zerobias = "zerobias"
            bnbnumi = "common"

            if ((beambnb in s and s.find(beamnumi) == -1) or stream=='bnb' or stream=='bnbmajority' or stream=='bnbminbias'):
                beam = "BNB"
            elif ((beamnumi in s and s.find(beambnb) == -1) or stream=='numi' or stream=='numimajority' or stream=='numiminbias'):
                beam = "NUMI"
            elif ( zerobias or laser) in s:
                beam = "none"
            elif ('offbeam' in stream):
                beam = "none"
            elif (bnbnumi) in s:
                beam = "mixed"
            else:
                beam = "unknown"

            metadata["sbn_dm.beam_type"] = beam


    #for event count:
    fFile = TFile(filename,"READ")
    fTree= fFile.Get("Events")
    nEvents = fTree.GetEntries()
    print("number of event in the root file %d" % nEvents)

    metadata["sbn_dm.event_count"] = nEvents

    # components list
    #s = dictionary.get('components').replace('[','').replace(']','')
    #metadata["icarus.components"] = s.split(', ')


    return json.dumps(metadata)


#comment out the rest for now

 
#    run_num = filename.split("_")
#
#    period = filename.rfind(".")
#    if (period < 0):
#        print "No suffix"
#        return False
#    suffix = filename[period+1:len(filename)]
#    if (suffix == "root"):
#        fileformat = "artroot"
#    else:
#        print "Unknown suffix:", suffix
#        return False
#    #
#    # get checksum
#    #   remove checksum calculation from .json file
#    checksum = SAMUtilities.adler32_crc(filename)
#    #    print "Checksum:", checksum
#    #
#    # get modified time
#    #
#    timestr = SAMUtilities.timestring(os.stat(filename).st_mtime)
#    #    print "Creation time:", timestr
#    #
#    # open SAM metadata file for writing
#    #
#    jj=filename.rfind("/")
#    if(jj<0):
#        jj=0
#    dropbox = dropboxdir+filename[jj:]+".json"
#    #    print dropbox
#    sf = open(dropbox,"w")
#    #    print "SAM file is open"
#    #
#    # Write pyton headers for SAM
#    #
#    sf.write('{\n')
#    #
#    # Write SAM metadata
#    #
#    sf.write('\t"file_name" : "'+filename[jj:]+'",\n')
#    sf.write('\t"file_size" : '+str(filesize)+',\n')
#    sf.write('\t"file_type" : "data",\n')
#    sf.write('\t"file_format" : "'+fileformat+'",\n')
#    sf.write('\t"data_tier" : "raw",\n')
#    sf.write('\t"group" : "lariat",\n')
#    sf.write('\t"checksum": [ "enstore:'+checksum+'" ],\n')
#    sf.write('\t"event_count" : 1,\n')
#    sf.write('\t"first_event" : '+safe.subrun+',\n')
#    sf.write('\t"last_event" : '+safe.subrun+',\n')
#    sf.write('\t"start_time" : "'+timestr+'",\n')
#    sf.write('\t"end_time" : "'+timestr+'",\n')
#    #
#    #Experiment specific fields
#    #
#    #
#    # fcl table not included
#    # project table not included
#    # filter table not included
#    #
#    #run number strut
#    #
#    sf.write('\t'+'"runs" : [ ['+safe.run+', '+safe.subrun+', "'+'physics'+'" ] ],\n' )
#    #
#    # run period
#    #
#    sf.write('\t"run.period" : "'+runperiod(int(safe.run))+'"\n')
#    #
#    # Write SAM footer data
#    #
#
#    sf.write("}\n")
#    sf.close()
#
#    #    print("SAM footer data written and file closed")
#    return True
