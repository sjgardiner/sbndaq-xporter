import subprocess
import json
import glob
import os

root_file_list = glob.glob("/data/fts_dropbox/*.root")

addr_lead_str="https://fndca3b.fnal.gov:3880/api/v1/namespace/pnfs/fnal.gov/usr/icarus/archive/sbn/sbn_fd/data/raw/ext/raw_sbndaq_v0_04_03/DataXportTesting_03Feb2020/Run0/00/00"

for f in root_file_list:
    r1 = f.split("_")[3][3:][:2]
    r2 = f.split("_")[3][3:][2:]
    addr = "%s/%s/%s/%s?locality=true"%(addr_lead_str,r1,r2,f.split("/")[-1])
    p = subprocess.Popen(['curl','-k','-X','GET','%s'%addr],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    curl_out = json.loads(stdout)

    if not "fileLocality" in curl_out:
        print("FILE %s not declared?"%f)
        continue

    if "NONE" in curl_out["fileLocality"]:
        print("FILE %s no locality?"%f)
        continue

    if "NEARLINE" in curl_out["fileLocality"] :
        print("FILE %s ON TAPE!"%f)
        json_file = f.split(".")[0]+".json"
        print("Delete files %s and %s"%(f,json_file))
        os.system("rm -f %s"%f)
        os.system("rm -f %s"%json_file)


print("Done")
