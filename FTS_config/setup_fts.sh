#
# Generic setup script for FTS
#
#    You may need to set the explicit version of FTS
#    $SAM_CP_CONFIG_DIR should point to the directory
#    where the sam_cp.cfg file resides.
#

source /home/nfs/icarusraw/ups/setups
setup ifdhc v2_5_4
setup sam_cp v9_0_8
setup encp -q stken:x86_64
setup ifdhc_config v2_4_5

export SAM_CP_CONFIG_DIR=$PWD
export X509_USER_PROXY=/opt/icarusraw/icarusraw.Raw.proxy

source ~icarusraw/FTS/bin/activate

#export X509_CERT_DIR=
