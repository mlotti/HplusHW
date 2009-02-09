#!/bin/sh

#@$-r   CMSSW_m2t    # request name
#@$-lf  1500mb       # output file size limit
#@$-eo               # join stderr and stdout
#@$-me               # send mail upon termination
#@$-s /bin/bash      # shell

#$ -N CMSSW_m2t
#$ -q lhc
#$ -S /bin/bash
#$ -o $JOB_NAME.$JOB_ID.stdout
#$ -V
#$ -cwd
#$ -m be
#$ -j y
#$ -l h_rt=06:00:00
#$ -notify

if [ "x$#" != "x3" ]; then
    echo "Usage: bsub analysis.sh.job <inputfile> <outputdir> <outputfile>"
    exit
fi

CONFIGFILE=offlineAnalysis_cfg.py
INPUTFILE=$1
OUTPUTDIR=$2
OUTPUTFILE=$3
BATCH=lxplus
ANALYSISOUTPUT=analysis.root

if [ "x$SGE_O_HOST" = "xsepeli" ]; then
    BATCH=sepeli

    ulimit -s 10240 # limit to stack to 10M
    export SCRAM_ARCH="slc4_ia32_gcc345"
    export BUILD_ARCH="slc4_amd64"
    export VO_CMS_SW_DIR="/home/opt/cms/cmssw"
    source $VO_CMS_SW_DIR/cmsset_default.sh

    LS_SUBCWD=$(pwd)

    export X509_USER_PROXY=$WRKDIR/x509up_u19683
    if [ ! -e $X509_USER_PROXY ]; then
        echo "Proxy file doesn't exist at $X509_USER_PROXY"
        exit
    fi

    WORKDIR=$TMPDIR
fi


echo "Setting runtime"
cd $LS_SUBCWD
eval $(scramv1 runtime -sh)

#env

cd $WORKDIR
echo "Working directory is $WORKDIR"

export MYINPUTFILES=$INPUTFILE
export MYMAXEVENTS=-1

echo "Running CMSSW"
cmsRun $LS_SUBCWD/$CONFIGFILE

OUTPUT=$OUTPUTDIR/$OUTPUTFILE

if [ -e $ANALYSISOUTPUT ]; then
    if [ "x$BATCH" = "xlxplus" ]; then
        echo "Copying $ANALYSISOUTPUT to CASTOR as $OUTPUT"
        rfcp $ANALYSISOUTPUT $OUTPUT
    elif [ "x$BATCH" = "xsepeli" ]; then
        echo "Copying $ANALYSISOUTPUT to madhatter as $OUTPUT"
        dccp -A $ANALYSISOUTPUT $OUTPUT
    fi
fi

if [ "x$BATCH" = "xsepeli" ]; then
    cp $LS_SUBCWD/${JOB_NAME}.${JOB_ID}.stdout $LS_SUBCWD/${JOB_NAME}.${JOB_ID}.stdout.stored
fi
