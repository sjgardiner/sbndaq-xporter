#
# Various functions to make SAM files
#
#
# Script to calculate Adler-32 checksum
#
import sys
from zlib import adler32
import time

def adler32_crc(filename):
    "Calculate checksum for file filename)"

    BLOCKSIZE = 1024*1024
    crc = 0
    with open(filename,"rb") as f:
        while True:
            data = f.read(BLOCKSIZE)
            if not data:
                break
            crc = adler32(data,crc)
    #crc=int(crc)
    if crc < 0:
        crc = ( crc & 0x7FFFFFFF) | 0x80000000
    return str(crc)
#
# End of checksum routine 
#
# 
# Routine to make properly formatted date
#
def timestring(tt):
    " Output a time string that is to SAM's liking"
    gmt = time.gmtime(tt)
    timestr =time.strftime("%d-%b-%Y %H:%M:%S",gmt)
    return timestr
#
# end of routine
#
 
