#!/bin/csh -f
################################################################
# C Shell Programming:
# http://www-cs.canisius.edu/ONLINESTUFF/UNIX/shellprogramming.html
#
# Desctiption:
# "Jobs" are submitted from the LXPLUS cluster.
# A "job" consists of a script, typically located inside AFS (the AFS filesystem is visible to the batch nodes).
# After submission the jobs typically queues until the scheduler decides that its turn has come.
# The job has its own local "pool" directory on the worker node where it can read and write local files. 
# The pool directory is deleted at the end of the job.
# Large data files needed for the job should be copied to the local pool directory (e.g. by Castor) in or accessed remotely (e.g. by EOS).
# Data files written locally by the job should be copied out to CERN storage (typically EOS or Castor).
# The results of the job run (STDOUT/STDERR) and job completion status are sent back to the user.
# 
# Return Codes:
# http://information-technology.web.cern.ch/services/fe/lxbatch/howto/how-interpet-batch-job-return-codes
#
# Useful Links:
# http://information-technology.web.cern.ch/book/cern-batch-service-user-guide/getting-started-batch-system/batch-concepts-and-cern-batch-system
# https://twiki.cern.ch/twiki/bin/view/Main/BatchJobs
# https://twiki.cern.ch/twiki/bin/view/Main/UsingLxBatch
# http://information-technology.web.cern.ch/services/batch
# http://information-technology.web.cern.ch/book/cern-batch-service-user-guide/getting-started-batch-system/using-batch-system
################################################################


################################################################
# Definitions
################################################################
echo "=== lxbatch.csh: Defininig VARIABLES"
set INITIAL=`echo $USER | cut -c1-1`
set POOL_DIR=$cwd # or `pwd`
set POOL_BASE=`basename $POOL_DIR` #or basename `pwd`
set PY_FILE=runAnalysis.py
set LOG_FILE=log.txt
set ENV_FILE=setup.csh
set SAVE_DIR=/afs/cern.ch/work/$INITIAL/$USER/lxbatch/LSFJOB_$POOL_BASE
set MCRAB_DIR=/afs/cern.ch/user/$INITIAL/$USER/workspace/multicrab/multicrab_Hplus2tbAnalysis_v8014_20160818T1956/
set ANALYSIS=Kinematics
set CMSSW=8_0_14
set HOME_DIR=/afs/cern.ch/user/$INITIAL/$USER
set CMSSW_DIR=$HOME_DIR/scratch0/CMSSW_$CMSSW
set HIGGS_DIR=$CMSSW_DIR/src/HiggsAnalysis
set HIGGS=`basename $HIGGS_DIR`
set WORK_DIR=$HIGGS/NtupleAnalysis/src/$ANALYSIS/work
set NEVENTS=-1


################################################################
# Place first timestamp on log file
################################################################
date >> $LOG_FILE


################################################################
# Copy HiggsAnalysis to $POOL_DIR (takes some time!)
################################################################
echo "=== lxbatch.csh: Copying {$HIGGS_DIR} to {$POOL_DIR}"
cp -r $HIGGS_DIR . 
#rsync --partial --progress -r $HIGGS_DIR .
date
echo "=== lxbatch.csh: Copied {$HIGGS_DIR} to {$POOL_DIR}"
ls -lt
echo


################################################################
# Setup the environment
################################################################
#>> $LOG_FILE
echo "=== lxbatch.csh: Changing directory to {$POOL_DIR/$HIGGS}."
cd $POOL_DIR/$HIGGS
ls -lt

echo
echo "=== lxbatch.csh: Setting up the environment by sourcing the script {$ENV_FILE}"
source $ENV_FILE
echo


################################################################
# Gather info (debugging purposed)
################################################################
echo "=== lxbatch.csh: g++ version is"
g++ -v

echo
echo "=== lxbatch.csh: ROOTSYS is"
echo $ROOTSYS

echo
echo "=== lxbatch.csh: python is"
python --version

echo
echo "=== lxbatch.csh: HOSTNAME is"
hostname
echo


################################################################
# Run the code
################################################################
#>> $LOG_FILE
echo "=== lxbatch.csh: Changing directory to {$WORK_DIR}"
cd $POOL_DIR/$WORK_DIR
ls -lt

echo "=== lxbatch.csh: Copying the library files to ${WORK_DIR}"
cp $POOL_DIR/$HIGGS/NtupleAnalysis/obj/Framework/src/FrameworkDict_rdict.pcm .
#cp $POOL_DIR/$HIGGS/NtupleAnalysis/lib/libHPlusAnalysis.so . 
ls -lt

echo "=== lxbatch.csh: Running the python file {$PY_FILE}"
./$PY_FILE -m $MCRAB_DIR -n $NEVENTS  >> $LOG_FILE


################################################################
# Place final timestamp on log file
################################################################
date >> $LOG_FILE


################################################################
# Copy output dir (and log.txt) to save dir
################################################################
#>> $LOG_FILE
echo
echo "=== lxbatch.csh: Copying output to {$SAVE_DIR}"
mkdir $SAVE_DIR
cp $LOG_FILE $SAVE_DIR/.
cp -r {$ANALYSIS}_* $SAVE_DIR/.
