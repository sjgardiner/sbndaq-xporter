import subprocess
import json
import glob
import os

root_file_list = glob.glob("/data/fts_dropbox/*.root")
json_file_list = glob.glob("/data/fts_dropbox/*.json")

#FTS output string formatted as below
#${sbn_dm.detector}/${file_type}/${data_tier}/${data_stream}/${icarus_project.version}/${icarus_project.name}/${icarus_project.stage}/${run_number[8/2]}


addr_lead_str="https://fndca3b.fnal.gov:3880/api/v1/namespace/pnfs/fnal.gov/usr/icarus/archive/sbn"

for fname in json_file_list:
    #print(fname)
    metadata = {}
    with open(fname) as f:
        try:
            metadata = json.load(f)
        except:
            print('Failed to load file %s'%fname)
    if len(metadata)==0:
        continue
    run_number = int(metadata["runs"][0][0])
    append_str = "%s/%s/%s/%s/%s/%s/%s/%02d/%02d/%02d/%02d"%(metadata["sbn_dm.detector"],
                                                                 metadata["file_type"],
                                                                 metadata["data_tier"],
                                                                 metadata["data_stream"],
                                                                 metadata["icarus_project.version"],
                                                                 metadata["icarus_project.name"],
                                                                 metadata["icarus_project.stage"],
                                                                 run_number/100/100/100,
                                                                 run_number/100/100,
                                                                 run_number/100,
                                                                 run_number%100)
                                                             
    #print(append_str)
    root_fname=fname[:-5]
    #print(root_fname)

    addr = "%s/%s/%s?locality=true"%(addr_lead_str,append_str,root_fname.split("/")[-1])
    #print(addr)

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

    if "NONE" in curl_out["fileLocality"]:
        print("FILE %s no locality?"%root_fname)
        continue

    if "NEARLINE" in curl_out["fileLocality"] :
        print("FILE %s ON TAPE!"%root_fname)
        print("Delete files %s and %s"%(fname,root_fname))
        os.system("rm -f %s"%root_fname)
        os.system("rm -f %s"%fname)


print("Done")
