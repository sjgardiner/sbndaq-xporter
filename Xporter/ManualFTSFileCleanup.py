import subprocess
import json
import glob
import os
from datetime import datetime

import sys

root_file_list = glob.glob("/data/sbndraw/fts_dropbox/*.root")
json_file_list = glob.glob("/data/sbndraw/fts_dropbox/*.json")
json_file_list.sort(key=lambda x: os.path.getmtime(x))

if not root_file_list:
    print('No files found. Are you running this program from the event builder machine?')
nfile = len(json_file_list)

#FTS output string formatted as below
#${sbn_dm.detector}/${file_type}/${data_tier}/${data_stream}/${icarus_project.version}/${icarus_project.name}/${icarus_project.stage}/${run_number[8/2]}

MATCH_STRING = "NEARLINE"
if (len(sys.argv) > 1):
    MATCH_STRING = sys.argv[1]

now = datetime.now()
print(f'Remove files containing {MATCH_STRING} in curl output.')
print(f'Found {nfile} metadata files in dropbox area')


addr_lead_str="https://fndca3b.fnal.gov:3880/api/v1/namespace/pnfs/fnal.gov/usr/sbnd/archive/sbn"

for i, fname in enumerate(json_file_list):
    metadata = {}
    if i % 100 == 0:
        print(f' checking file {i}/{nfile}')
    with open(fname) as f:
        try:
            metadata = json.load(f)
        except:
            print('Failed to load file %s'%fname)
    if len(metadata)==0:
        continue
    run_number = int(metadata["runs"][0][0])
    # print(fname)
    append_str = "%s/%s/%s/%s/%s/%s/%s/%02d/%02d/%02d/%02d"%(metadata["sbn_dm.detector"],
                                                                 metadata["file_type"],
                                                                 metadata["data_tier"],
                                                                 metadata["data_stream"],
                                                                 metadata["sbnd_project.version"],
                                                                 metadata["sbnd_project.name"],
                                                                 metadata["sbnd_project.stage"],
                                                                 run_number//100//100//100%100,
                                                                 run_number//100//100%100,
                                                                 run_number//100%100,
                                                                 run_number%100)
                                                             
    #print(append_str)
    root_fname=fname[:-5]
    #print(root_fname)

    addr = "%s/%s/%s?locality=true"%(addr_lead_str,append_str,root_fname.split("/")[-1])
    print(addr)

    p = subprocess.Popen(['curl','-k','-X','GET','%s'%addr],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    curl_out = {}
    try:
        curl_out = json.loads(stdout)
    except:
        print("Failed to load JSON.")
        print(stderr)

    if not "fileLocality" in curl_out:
        print("FILE %s not declared?"%root_fname)
        continue

    ts = datetime.fromtimestamp(curl_out['creationTime'] / 1e3)
    elapsed_days = (now - ts).days
    print(f'Got file ({elapsed_days:.1f} days old)')
    print(curl_out)

    if "NONE" in curl_out["fileLocality"]:
        print("FILE %s no locality?"%root_fname)
        continue

    if MATCH_STRING in curl_out["fileLocality"] :
        #print("FILE %s ON TAPE!"%root_fname)
        #print("FILE:", root_fname, "STATUS:", curl_out["fileLocality"], "MATCHES THE REQUIRED PATTERN:", MATCH_STRING, "!")
        print(ts)
        if elapsed_days > 7:
            print("Delete files %s and %s (%.1f days old)"%(fname,root_fname,elapsed_days))
            os.system("rm -f %s"%root_fname)
            os.system("rm -f %s"%fname)
    else:
        print("File not on tape yet, not deleting!")

print("Done")
