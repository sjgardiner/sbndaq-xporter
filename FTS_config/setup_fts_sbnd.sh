#
# Generic setup script for FTS
#
#    You may need to set the explicit version of FTS
#    $SAM_CP_CONFIG_DIR should point to the directory
#    where the sam_cp.cfg file resides.
#

source /daq/software/products/setup
#source ${HOME}/fts_stuff/my_local_products/setups
#setup sam_cp v9_0_8
#setup encp -q stken:x86_64
#setup ifdhc v2_6_1 -q e20:p392:prof
#setup ifdhc_config v2_6_1b

ups active

export SAM_CP_CONFIG_DIR=$PWD
export X509_USER_PROXY=/opt/sbndraw/sbndraw.Raw.proxy

source ${HOME}/fts_stuff/fts_env/bin/activate

export FTS_RUN_DIR=${HOME}/fts_stuff/fts_run/$(hostname)
export FTS_LOG_DIR=/daq/log/fts_logs/$(hostname)
mkdir -p $FTS_RUN_DIR
mkdir -p $FTS_LOG_DIR

export FTS_CONFIG_FILE=$PWD/sbnd-evb_fts_config.ini
cp $FTS_CONFIG_FILE $FTS_RUN_DIR/

#export X509_CERT_DIR=
