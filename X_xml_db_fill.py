import sys

#import psycopg2 # Get database functions 

import dbvariables # get variable names
import safe
#
#
# function to fill db from xml file
#
def fill_db(timestr):
#
# Already connected to database in main program
# dbvariables.conn = database connection
# dbvariables.cur = cursor
#
#
# database file name:
#
    dbtableXML = "sbnd_xml_database"
#
# make a new database table
#
#
#the following line is for testing only!
#dbvariables.cur.execute("TRUNCATE TABLE "+dbtableXML+";")
    goodrun = True
    psqlcmd = "INSERT INTO "+dbtableXML+"(runnumber, subrun, runs\
tarttimesec) VALUES ("+safe.run+", "+safe.subrun+", "+timestr+");"
#    print psqlcmd
    dbvariables.cur.execute(psqlcmd)
    dbvariables.conn.commit()
    return goodrun 

