#================================================================================================
# Script for setting up standalone environment (i.e. without CMSSW
# release area) for accessing the python libraries and scripts.
#
# Usage:
# cd HiggsAnalysis
# source setup.csh
#
# Note:
# tested so far LOCATION="" and LOCATION="jade"
#================================================================================================
if ( $?HIGGSANALYSIS_BASE ) then
    echo "Standalone environment already loaded"
    exit
endif

set LOCATION=""
if ( $?CMSSW_BASE ) then
    set LOCATION="CMSSW"
    echo "\n=== LOCATION is $LOCATION. Known problems with Python when 'cmsenv' is set (Perhaps PYTHONPATH?. Press any key to continue: "
    set proceed=$<
    echo "Continuing ..."
endif

# Detect LXPLUS or MAC OS X (Darwin)
if ( $LOCATION == "" ) then
    if (`hostname` =~ "lxplus"* ) then
        set LOCATION="lxplus"
    else if (`hostname` =~ "Mac"* ) then
	set LOCATION="mac"
    else if (`hostname` =~ *".cern.ch" ) then #Example: p06109780e53561.cern.ch
	set LOCATION="lxbatch"
     else if (`hostname` =~ *".fnal.gov" ) then #Example: cmslpc35.fnal.gov
        set LOCATION="lpc"
    endif
endif


# Set the HiggsAnalysis base directory
setenv HIGGSANALYSIS_BASE $PWD


set LD_LIBRARY_PATH_APPEND=""
if ( $LOCATION == "lxplus" || $LOCATION == "lxbatch" || $LOCATION == "lpc" ) then
    echo "\n=== Sourcing $LOCATION environments (Hand-picked from CMSSW_8_0_24)"
    echo "To update:"
    echo "1) create a developer area (cmsrel):"
    echo "cmsrel CMSWW_X_Y_Z"
    echo "2) source the CMSSW environment (cmsenv):"
    echo "cd  CMSWW_X_Y_Z/src/"
    echo "cmssev"
    echo "3) Look the new paths with 'scram tool list' and 'scram tool info'"
    echo "[See setup.csh for more details]"


    ### scram tool info gcc-cxxcompiler (Look for GCC_CXXCOMPILER_BASE)
    set GCC_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/gcc/4.9.3   # CMSSW_7_6_5
    #set GCC_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/gcc/5.3.0   # CMSSW_8_0_24

    ### scram tool info root_interface (Look for ROOT_INTERFACE_BASE)
    # setenv ROOTSYS /cvmfs/cms.cern.ch/slc6_amd64_gcc493/lcg/root/6.02.12-kpegke4   # CMSSW_7_6_5
    setenv ROOTSYS /cvmfs/cms.cern.ch/slc6_amd64_gcc493/lcg/root/6.06.00
    #setenv ROOTSYS /cvmfs/cms.cern.ch/slc6_amd64_gcc530/lcg/root/6.06.00-ikhhed5   # CMSSW_8_0_24

    ### scram tool info xrootd (Look for XROOTD_BASE)
    set XROOTD_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/xrootd/4.0.4-kpegke2   # CMSSW_7_6_5
    #set XROOTD_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/xrootd/4.4.1           # CMSSW_8_0_24

    ### scram tool info xz (Look for XZ_BASE)den th
    set XZ_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/xz/5.2.1    # CMSSW_7_6_5
    #set XZ_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/xz/5.2.1    # CMSSW_8_0_24

    ### scram tool info python (Look for PYTHON_BASE)
    set PYTHON_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/python/2.7.6-kpegke     # CMSSW_7_6_5
    #set PYTHON_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/python/2.7.11-giojec2   # CMSSW_8_0_24

    ### Set the run-time shared library loader (ld.so) an extra set of directories to look for when searching for shared libraries.
    #set LD_LIBRARY_PATH_APPEND=$ROOTSYS/lib:$GCC_BASE/lib64:$GCC_BASE/lib:$XROOTD_BASE/lib:$XZ_BASE/lib:$PYTHON_BASE/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libjpg/8b-cms/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libpng/1.6.16/lib
    #set LD_LIBRARY_PATH_APPEND=$ROOTSYS/lib:$GCC_BASw/lib64:$GCC_BASE/lib:$XROOTD_BASE/lib:$XZ_BASE/lib:$PYTHON_BASE/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/libjpg/8b-cms/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/libpng/1.6.16/lib:/uscms/home/${USER}/.local/lib/gcc493
    set LD_LIBRARY_PATH_APPEND=$ROOTSYS/lib:$GCC_BASE/lib64:$GCC_BASE/lib:$XROOTD_BASE/lib:$XZ_BASE/lib:$PYTHON_BASE/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/libjpg/8b-cms/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/libpng/1.6.16/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc493/cms/cmssw/CMSSW_7_6_5/external/slc6_amd64_gcc493/lib/
    #set LD_LIBRARY_PATH_APPEND=$ROOTSYS/lib:$GCC_BASE/lib64:$GCC_BASE/lib:$XROOTD_BASE/lib:$XZ_BASE/lib:$PYTHON_BASE/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_25/external/slc6_amd64_gcc530/lib/

    ### Set the PATH (crucial update on 7 Feb 2017)
    setenv PATH $PYTHON_BASE/bin:/$ROOTSYS/bin:$GCC_BASE/bin:$XROOTD_BASE/bin:$PATH

    if ($?PYTHONPATH) then
	setenv PYTHONPATH "$ROOTSYS/lib:$PYTHONPATH"
    else
	setenv PYTHONPATH "$ROOTSYS/lib"
    endif
endif


# echo "\n=== Appending to LD_LIBRARY_PATH"
set LD_LIBRARY_PATH_APPEND="$HIGGSANALYSIS_BASE/NtupleAnalysis/lib:${LD_LIBRARY_PATH_APPEND}"
if ( ! $?LD_LIBRARY_PATH ) then
    setenv LD_LIBRARY_PATH "${LD_LIBRARY_PATH_APPEND}"
else
    setenv LD_LIBRARY_PATH "${LD_LIBRARY_PATH_APPEND}:${LD_LIBRARY_PATH}"
endif

# echo "\n=== Creating symbolic links and hidden directories for $LOCATION"
set PATHPREFIX=.python

if ( $LOCATION == "CMSSW" ) then    
    if ( ! $?CMSSW_BASE || ! -e $CMSSW_BASE/python/HiggsAnalysis/NtupleAnalysis ) then
        ln -s $HIGGSANALYSIS_BASE/NtupleAnalysis/python $CMSSW_BASE/python/HiggsAnalysis/NtupleAnalysis
    endif

else
    if ( ! -e $PATHPREFIX/HiggsAnalysis ) then
	# echo "\n=== Creating $PATHPREFIX directory under `pwd`. Creating __init__.py"
        mkdir -p $PATHPREFIX/HiggsAnalysis
        touch $PATHPREFIX/HiggsAnalysis/__init__.py
    endif

    # echo "\n=== Loop over directories under NtupleAnalysis/ and HeavyChHiggsToTauNu/"
    foreach DIR ( NtupleAnalysis )
	# echo "DIR=$DIR"

	set LINK_NAME=$PATHPREFIX/HiggsAnalysis/$DIR
	set TARGET=$HIGGSANALYSIS_BASE/$DIR/python
	set PYINIT=$LINK_NAME/__init__.py

	# If $PATHPREFIX/HiggsAnalysis/$DIR does not exist
        if ( ! -e $PATHPREFIX/HiggsAnalysis/$DIR ) then

            # echo "Linking $TARGET with $LINK_NAME"
	    ln -s $TARGET $LINK_NAME

	    # echo "Creating $PYINIT"
            touch $PYINIT
	    
            foreach d ( $PATHPREFIX/HiggsAnalysis/$DIR/* )
                if ( -d $d ) then
		    # echo "Creating $d/__init__.py"
                    touch $d/__init__.py
                endif
            end
        endif
    end


    echo "\n=== Loop over directories under NtupleAnalysis/src"
    foreach DIR ( `ls NtupleAnalysis/src` )
	# echo "DIR=$DIR"

	# NOTE: Remove last "/" from directory name. The "/" at the end causes the linking to FAIL for some shells
	set DIR=`echo $DIR | sed 's/\(.*\)\//\1 /'`
	set LINK_NAME=$PATHPREFIX/HiggsAnalysis/$DIR
	set TARGET=$HIGGSANALYSIS_BASE/NtupleAnalysis/src/$DIR/python
	set PYINIT=$LINK_NAME/__init__.py

	# If $LINK_NAME does not exist and $TARGET exists
        if ( ! -e $LINK_NAME && -e $HIGGSANALYSIS_BASE/NtupleAnalysis/src/$DIR/python ) then

            # echo "Linking $TARGET with $LINK_NAME"
            ln -s $TARGET $LINK_NAME

            # echo "Creating $PYINIT"
            touch $PYINIT

            foreach d ( $PATHPREFIX/HiggsAnalysis/$DIR/* )
                if ( -d $d ) then
		    # echo "Creating $d/__init__.py"
                    touch $d/__init__.py
                endif
            end
        endif
    end

    # Set PYTHONPATH
    if ( -z PYTHONPATH ) then
        setenv PYTHONPATH ${PWD}/${PATHPREFIX} #NOTE: Double quotes will NOT WORK for some shells!!!
        echo "PYTHONPATH is $PYTHONPATH"
    else
        setenv PYTHONPATH ${PWD}/${PATHPREFIX}:${PYTHONPATH}  #NOTE: Double quotes will NOT WORK for some shells!!!
        echo "PYTHONPATH is $PYTHONPATH"
    endif

endif


#echo "\n=== Setting PATH variable"
#setenv PATH "${HIGGSANALYSIS_BASE}/HeavyChHiggsToTauNu/scripts:${HIGGSANALYSIS_BASE}/NtupleAnalysis/scripts:${PATH}"
setenv PATH "${HIGGSANALYSIS_BASE}/NtupleAnalysis/scripts:${PATH}"

#echo "\n=== Install externals (if necessary)"
sh +x installexternals.sh

echo "\n=== The environment variables set are:"
echo "LOCATION is $LOCATION"
echo "HIGGSANALYSIS_BASE is $HIGGSANALYSIS_BASE"
echo "PATHPREFIX is $PATHPREFIX"
echo "ROOTSYS is $ROOTSYS"
echo "LD_LIBRARY_PATH is $LD_LIBRARY_PATH"
echo "PYTHONPATH is $PYTHONPATH"
echo "PATH is $PATH"
