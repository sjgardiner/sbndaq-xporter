 #  Usage: python Xporter.py <data directory> <dropbox directory>
#
# program to:
#       1)  Check to see if there are new files and if there are:
#       2) update run configuration database
#       3) create the SAM metadata file
#       4) move the data file to the dropbox
#
# import modules
import sys
import os
import time
import shutil
import psycopg2 # Get database functions
import dbvariables # get conn and cur
import X_SAM_metadata
import X_xml_db_fill
import filelock
import safe
import subprocess
#
# Get directory of Xporter.py
#
Xporterdir = os.path.dirname(os.path.abspath(__file__))
#
# check to see if the data directory and the dropbox directory exist
#
if (len(sys.argv) != 3 and not (len(sys.argv) == 4 and (sys.argv[3] == "prod" or sys.argv[3] == "dev"))):
    print 'Command: python Xporter.py <data directory> <dropbox directory> <"dev"/"prod">'
    sys.exit(1)
try:
    dropboxdir=sys.argv[2]
    os.chdir(dropboxdir)
    if (dropboxdir[len(dropboxdir)-1] != "/"): dropboxdir=dropboxdir+"/"
except:
    print "Dropbox directory: ", dropboxdir, "not found - please restart program"
    sys.exit(1)
#
# connect to database
# 
develop = True
if (len(sys.argv) == 4 and sys.argv[3]=="prod"):
    develop=False
if (develop):
# development version
    dbvariables.conn = psycopg2.connect(database="lariat_dev", user="randy", host="ifdbdev", port="5441")
    dbvariables.cur=dbvariables.conn.cursor()
#production version
else:
    ntry = 0
    nodbconnection = True
    while nodbconnection:
        try:
            dbvariables.conn = psycopg2.connect(database="lariat_prd", user="lariatdataxport", password="lariatdataxport_321", host="ifdbprod2", port="5443")
            dbvariables.cur=dbvariables.conn.cursor()
            nodbconnection = False
        except:
            ntry +=1
            if (ntry % 5 == 1): print "Failed to make lariat_prd connection for",ntry,"times... sleep for 5 minutes"
            time.sleep(300)
try:
    os.chdir(sys.argv[1])
    datadir=sys.argv[1]
    if (datadir[len(datadir)-1] != '/'): datadir = datadir+'/'
except:
    print "Data directory: ", datadir, "not found - please restart program"
    sys.exit(1)
#
#  check for file lock
#
lock = filelock.FileLock(datadir+"XporterInProgress")
try: 
    lock.acquire(timeout=5)
except filelock.Timeout as err:
    exit(0)
#
# Run file.Complete.py to check for new files
#
fnull = open("/dev/null","w")
subprocess.call([Xporterdir+"/findComplete.sh",datadir])
#
# Begin data loop 
#
switch = True
count = 0
fextension = ".complete"
while switch:

    goodrun = True

#
# Check for finish files
#
    dirlist=os.listdir(datadir)
    for filename in dirlist:
        if (filename[len(filename)-len(fextension):] == fextension and filename != "lariat_r-_sr-.complete"):
            findex=filename.rfind(fextension)
#
# found a finish file
#
            print time.ctime(time.time()),": Found finish file:",filename
            filenameshort=filename[0:findex]
#
# Get run and subrun number
#
            safe.run = "0"
            safe.subrun = "0"
            safe.type = 0
#
# .root files
#
            if (filenameshort[:6] == "sbnd_r" or filenameshort[:13] == "digits_sbnd_r"):
                ll = len(filenameshort)
                kk = filenameshort.rfind("_")
                if (kk > 0):
                    #There is a _dl1 some of the bloody time in the name now for some reason so find the next _
                    #if (filenameshort[kk+1:] == "dl1"):
                    #    ii = filenameshort[:kk].rfind("_")
                    if (filenameshort[:kk].isdigit() and filenameshort[filenameshort[:kk].rfind("_")+1] != "r"):
                        ii = kk 
                    elif (filenameshort[kk+1:kk+3] == "sr"):
                        ii = kk+2
                    #If there is a load of rubbish afterwards lets igore this until we get to just a number. 
                    else:
                        while not (filenameshort[kk+1:ll].isdigit() and filenameshort[filenameshort[:kk].rfind("_")+1] == "r" or kk == 0):
                            ll = kk 
                            kk = filenameshort[:kk].rfind("_")
                        ii = kk 
                    if (ii > 0):
                        #No sr in front now so i've changed the where it starts. 
                        safe.subrun = filenameshort[ii+1:ll]
                        while (safe.subrun[0] == "0"):
                            safe.subrun = safe.subrun[1:]
                        if not (safe.subrun.isdigit()):
                            print "Sub run is not a number or is not of the assumed form" 
                            goodrun = False
                        jj = filenameshort[:ii].rfind("_")
                        if(filenameshort[jj+1:jj+3] == "sr"):
                            ii = jj 
                            jj = filenameshort[:jj].rfind("_")
                        if (jj>0):
                            safe.run = filenameshort[jj+2:ii]
                            while (safe.run[0] == "0"):
                                safe.run = safe.run[1:]
#
#  print out decoding of run and subrun
#
            #if (safe.run != "0" and safe.subrun != "0"):
            #    print "Found run:subrun",safe.run+":"+safe.subrun
            nf = 0
#
# Look for other files that go with .complete file
#
            for filename2 in dirlist:
#
# check for .root files
#
                if (filename2 ==  filenameshort+".root"):
                    datafile = filename2
                    nf+=1
#
# Check for data file
#
            if (nf == 0):
                print "No data file found for run:",safe.run,"Subrun:",safe.subrun
                #            else:
                #                print "Found data file:", datafile
#
# Check for configuration file
#
#
#  Check that all files are present
# 
            if (nf!= 0):
                print "Found data file for "+safe.run+":"+safe.subrun+" - begin processing"
#
#  Do database entry
#
                if (goodrun or filenameshort[:13] != "digits_sbnd_r"):
#                   print "Configfile:", configfile
                    xx =  X_xml_db_fill.fill_db(str(os.path.getctime(datadir+datafile)))
                    goodrun = goodrun and xx
# make SAM .json file
#
                if (goodrun):
                    xx= X_SAM_metadata.SAM_metadata(dropboxdir,datafile)
                    goodrun = goodrun and xx
                if (goodrun):
# no errors - move files
#
#  move data file to dropbox and delete finish file and time file
#
                    os.rename(datafile,dropboxdir+datafile)
# for real move remove the previous comment  and comment out the following line
#                    shutil.copy(datafile,dropboxdir+datafile)
                    print "Moved file",datafile,"to SAM dropbox"
#                    os.remove(filename)
#  Until we are confident things are working, move finish file to backup directory.
                    os.rename(filename, datadir+"backup/"+filename)
                    print "(Re)moved:", filename
            if (nf == 0 or not goodrun):
#
#  Error .. rename finish file to .complete.error
#
                print "Error while processing:",filename,"-no files (re)moved"
                os.rename(filename,filename+".error")
#  -- program is now set up to run as a cron job
#
#  go to sleep for 70 seconds
#
# --> debug    print "Current time:",time.ctime()
# to make program continuously look remove the comment before the next line
#    time.sleep(70)
# --> debug    print "Finished sleep:",time.ctime()
# and comment out the following line  
    switch=False
#
# release lock
#
lock.release()


