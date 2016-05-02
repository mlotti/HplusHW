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
echo "=== setup.csh"

if ( $?HIGGSANALYSIS_BASE ) then
    echo "Standalone environment already loaded"
    exit
endif

echo "\n===Determining LOCATION variable"
# Detect CMSSW
set LOCATION=""
if ( $?CMSSW_BASE ) then
    set LOCATION="CMSSW"
endif

# Detect lxplus and jade
if ( $LOCATION == "" ) then
    if (`hostname` =~ "lxplus"* ) then
        set LOCATION="lxplus"
    else if (`hostname` =~ "jade"* ) then
	set LOCATION="jade"
    else if (`hostname` =~ "Mac"* ) then
	set LOCATION="mac"
    endif
endif
echo "LOCATION is $LOCATION"

setenv HIGGSANALYSIS_BASE $PWD
echo "HIGGSANALYSIS_BASE is $HIGGSANALYSIS_BASE"

if ( $LOCATION == "lxplus" ) then
    echo "\n=== Sourcing lxplus environments for gcc 4.8 and ROOT 6.04.00"
    source /afs/cern.ch/sw/lcg/contrib/gcc/4.8/x86_64-slc6-gcc48-opt/setup.csh
    setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/6.04.00/x86_64-slc6-gcc48-opt/root
    setenv LD_LIBRARY_PATH "${ROOTSYS}/lib:${LD_LIBRARY_PATH}"
    setenv PATH "${ROOTSYS}/bin:${PATH}"
    if ($?PYTHONPATH) then
        setenv PYTHONPATH "$ROOTSYS/lib:$PYTHONPATH"
    else
        setenv PYTHONPATH "$ROOTSYS/lib"
    endif 
endif


set LD_LIBRARY_PATH_APPEND=""
if ( $LOCATION == "jade" ) then
    # Hand-picked from CMSSW_7_4_0_pre6 slc6_amd64_gcc491
    # To update
    # - create a developer area (cmsrel)
    # - source the environment (cmsenv)
    # - look the new paths with 'scram tool list' and 'scram tool info'

    echo "\n=== Sourcing jade environments"

    # scram tool info gcc-cxxcompiler
    set GCC_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms

    # scram tool info root_interface
    # setenv ROOTSYS /cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/5.34.22-cms2
    setenv ROOTSYS /cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/6.02.00-cms4

    # scram tool info xrootd
    set XROOTD_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/xrootd/4.0.4

    # scram tool info xz
    set XZ_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/xz/5.0.3__5.1.2alpha-cms

    # scram tool info python
    set PYTHON_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python/2.7.6-cms

    set LD_LIBRARY_PATH_APPEND=$ROOTSYS/lib:$GCC_BASE/lib64:$GCC_BASE/lib:$XROOTD_BASE/lib:$XZ_BASE/lib:$PYTHON_BASE/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libjpg/8b-cms/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libpng/1.6.16/lib

    setenv PATH $ROOTSYS/bin:$GCC_BASE/bin:$XROOTD_BASE/bin:$PATH

    if ($?PYTHONPATH) then
	setenv PYTHONPATH "$ROOTSYS/lib:$PYTHONPATH"
    else
	setenv PYTHONPATH "$ROOTSYS/lib"
    endif
endif


echo "\n=== Appending to LD_LIBRARY_PATH"
set LD_LIBRARY_PATH_APPEND="$HIGGSANALYSIS_BASE/NtupleAnalysis/lib:${LD_LIBRARY_PATH_APPEND}"
if ( ! $?LD_LIBRARY_PATH ) then
    setenv LD_LIBRARY_PATH "${LD_LIBRARY_PATH_APPEND}"
else
    setenv LD_LIBRARY_PATH "${LD_LIBRARY_PATH_APPEND}:${LD_LIBRARY_PATH}"
endif

echo "\n=== Creating symbolic links and hidden directories for $LOCATION"
set PATHPREFIX=.python
echo "PATHPREFIX is $PATHPREFIX"

if ( $LOCATION == "CMSSW" ) then    
    if ( ! $?CMSSW_BASE || ! -e $CMSSW_BASE/python/HiggsAnalysis/NtupleAnalysis ) then
        ln -s $HIGGSANALYSIS_BASE/NtupleAnalysis/python $CMSSW_BASE/python/HiggsAnalysis/NtupleAnalysis
    endif

else
    if ( ! -e $PATHPREFIX/HiggsAnalysis ) then
	echo "\n=== Creating $PATHPREFIX directory under `pwd`. Creating __init__.py"
        mkdir -p $PATHPREFIX/HiggsAnalysis
        touch $PATHPREFIX/HiggsAnalysis/__init__.py
    endif

    echo "\n=== Loop over directories under NtupleAnalysis/ and HeavyChHiggsToTauNu/"
    foreach DIR ( NtupleAnalysis HeavyChHiggsToTauNu )
	#echo "DIR=$DIR"

	set LINK_NAME=$PATHPREFIX/HiggsAnalysis/$DIR
	set TARGET=$HIGGSANALYSIS_BASE/$DIR/python
	set PYINIT=$LINK_NAME/__init__.py

	# If $PATHPREFIX/HiggsAnalysis/$DIR does not exist
        if ( ! -e $PATHPREFIX/HiggsAnalysis/$DIR ) then

            echo "Linking $TARGET with $LINK_NAME"
	    ln -s $TARGET $LINK_NAME

	    echo "Creating $PYINIT"
            touch $PYINIT
	    
            foreach d ( $PATHPREFIX/HiggsAnalysis/$DIR/* )
                if ( -d $d ) then
		    echo "Creating $d/__init__.py"
                    touch $d/__init__.py
                endif
            end
        endif
    end


    echo "\n=== Loop over directories under NtupleAnalysis/src"
    foreach DIR ( `ls NtupleAnalysis/src` )
	#echo "DIR=$DIR"

	# NOTE: Remove last "/" from directory name. The "/" at the end causes the linking to FAIL for some shells
	set DIR=`echo $DIR | sed 's/\(.*\)\//\1 /'`
	echo "-->DIR=$DIR"

	set LINK_NAME=$PATHPREFIX/HiggsAnalysis/$DIR
	set TARGET=$HIGGSANALYSIS_BASE/NtupleAnalysis/src/$DIR/python
	set PYINIT=$LINK_NAME/__init__.py

	# If $LINK_NAME does not exist and $TARGET exists
        if ( ! -e $LINK_NAME && -e $HIGGSANALYSIS_BASE/NtupleAnalysis/src/$DIR/python ) then

            echo "Linking $TARGET with $LINK_NAME"
            ln -s $TARGET $LINK_NAME

            echo "Creating $PYINIT"
            touch $PYINIT

            foreach d ( $PATHPREFIX/HiggsAnalysis/$DIR/* )
                if ( -d $d ) then
		    echo "Creating $d/__init__.py"
                    touch $d/__init__.py
                endif
            end
        endif
    end

    echo "Setting PYTHONPATH"
    if ( -z PYTHONPATH ) then
        setenv PYTHONPATH '${PWD}/$PATHPREFIX' #NOTE: Double quotes will NOT WORK for some shells!!!
        echo "PYTHONPATH is $PYTHONPATH"
    else
        setenv PYTHONPATH '${PWD}/$PATHPREFIX:${PYTHONPATH}'  #NOTE: Double quotes will NOT WORK for some shells!!!
        echo "PYTHONPATH is $PYTHONPATH"
    endif

endif

echo "\n=== Setting PATH variable"
setenv PATH "${HIGGSANALYSIS_BASE}/HeavyChHiggsToTauNu/scripts:${HIGGSANALYSIS_BASE}/NtupleAnalysis/scripts:${PATH}"

echo "\n=== Install externals (if necessary)"
sh +x installexternals.sh
