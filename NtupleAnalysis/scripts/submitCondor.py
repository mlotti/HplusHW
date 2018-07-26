#!/usr/bin/env python
'''
DESCRIPTION:
Submit multible jobs to condor


USAGE:
submitCondor.py [options]


EXAMPLE:
submitCondor.py --topMass 400 --bdt 0p40


LAST USED:
submitCondor.py --topMass 500 --bdt 0p40 


'''

#================================================================================================ 
# Modules here
#================================================================================================ 
import subprocess
from subprocess import Popen, PIPE
import os
import sys
import datetime
from optparse import OptionParser 

import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles


#================================================================================================ 
# Variable definition
#================================================================================================ 
ss = ShellStyles.SuccessStyle()
ns = ShellStyles.NormalStyle()
ts = ShellStyles.NoteStyle()
hs = ShellStyles.HighlightAltStyle()
es = ShellStyles.ErrorStyle()

#================================================================================================ 
# Function Definitions
#================================================================================================ 
def Verbose(msg, printHeader=False):
    if not VERBOSE:
        return
    if printHeader:
        print "=== submitCondor.py:"

    if msg !="":
        print "\t", msg
    return

def GetFName():
    fName = __file__.split("/")[-1]
    fName = fName.replace(".pyc", ".py")
    return fName

def Print(msg, printHeader=True):
    fName = GetFName()
    if printHeader:
        print "=== ", fName
    if msg !="":
        print "\t", msg
    return

def PrintFlushed(msg, printHeader=True):
    '''
    Useful when printing progress in a loop
    '''
    msg = "\r\t" + msg
    if printHeader:
        print "=== ", GetFName()
    sys.stdout.write(msg)
    sys.stdout.flush()
    return     

def CheckForValidProxy():
    process = Popen(['voms-proxy-info'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = process.communicate()
    if len(err) > 0:
        raise Exception(es + err + ns)
        # err  = err.replace("\n", "")
        # err += " Continuing anyway (not needed)"
        # Print(es + err + ns, True)
    else:
        lines = output.splitlines()
        for l in lines:
            if "timeleft" not in l:
                continue
            time  = l.split(": ")[-1]
            hours = int(time.split(":")[0])
            mins  = int(time.split(":")[1])
            secs  = int(time.split(":")[2])

            # Determine the time remaining in seconds
            dt = hours*60*60 + mins*60 + secs

            # Require at least 60 seconds of valid proxy
            if dt < 60:
                raise Exception(es + "No valid CMS VO proxy found!" + ns)
            else:
                Print(ss + "Valid CMS VO proxy found!" + ns, True)
    return


def main(opts):

    Verbose("Check that a CMS VO proxy exists (voms-proxy-init)", True)
    CheckForValidProxy()


    Verbose("Create directory %s" % (opts.dirName), True)
    if os.path.isdir(opts.dirName):
        Print("Directory %s already exists! EXIT" % (es + opts.dirName + ns), True)
        sys.exit()
    else:
        Print("Creating directory %s" % (ss + opts.dirName + ns), True)
        os.mkdir(opts.dirName)
    os.system("cp %s %s/." % ("runSystOnCondor.csh", opts.dirName) )
    os.chdir(opts.dirName)

    # Settings
    analyses  = ["Hplus2tbAnalysis", "FakeBMeasurement"]
    nSyst     = len(opts.systVarsList)
    groupDict = {}
    jdlList   = []
    groupDict["Hplus2tbAnalysis"] = map(chr, range(65, 91))
    groupDict["FakeBMeasurement"] = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

    Verbose("Creating the jdl files", True)
    # For-loop: All analyses
    for i, analysis in enumerate(analyses, 1):
        groups  = groupDict[analysis]
        nGroups = len(groups)

        # For-loop: All systematics
        for j, syst in enumerate(opts.systVarsList, 1):
            
            # For-loop: All groups
            for k, group in enumerate(groups, 1):
                baseName = "%s_Group%s_Syst%s" % (analysis, group, syst)
                # fileName = "%s_Cluster$(Cluster)_Process$(Process)" % (baseName) #original
                fileName = baseName
                jdl = "run_%s.jdl" % (baseName)
                
                msg = "Creating %s (%d/%d)" % (jdl, j*k, nGroups*nSyst)
                if "FakeB" in analysis:
                    PrintFlushed(ts + msg + ns, i*j*k==1)
                else:
                    PrintFlushed(hs + msg + ns, i*j*k==1)
                f = open(jdl, "w")    
                f.write("universe = vanilla\n")
                f.write("Executable = runSystOnCondor.csh\n")
                f.write("Should_Transfer_Files = YES\n")
                f.write("WhenToTransferOutput = ON_EXIT\n")
                f.write("Transfer_Input_Files = runSystOnCondor.csh, %s/HiggsAnalysis.tgz, %s/%s.tgz\n" % (opts.codePath, opts.mcrabPath, opts.mcrab) )
                f.write("Output = output_%s.txt\n" % (fileName) )
                f.write("Error  = error_%s.txt\n"  % (fileName) )
                f.write("Log    = log_%s.txt\n"    % (fileName) )
                f.write("x509userproxy = /tmp/x509up_u52142\n")
                f.write("Arguments = %s NewTopAndBugFixAndSF_TopMassLE%s_BDT%s_Group%s_Syst%s %s %s\n" % (analysis, opts.topMass, opts.BDT, group, syst, group, syst) )
                f.write("Queue 1\n")
                f.close()
                jdlList.append(jdl)
        print
        
    Verbose("Submitting the jobs", True)
    for i, jdl in enumerate(jdlList, 1):
        cmd = "condor_submit %s" %  (jdl)
        #PrintFlushed(hs + cmd + ns, i==1)
        os.system(cmd)

    Print("Total of %s%d jobs submitted%s" % (ss, len(jdlList), ns), True)
    return

if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html
 
    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''

    # Default settings
    VERBOSE   = False
    SYSTVARS  = None
    CODEPATH  = "/uscms_data/d3/aattikis/workspace/cmssw/CMSSW_8_0_30/src"
    MCRABPATH = "/uscms_data/d3/aattikis/workspace/multicrab"
    MCRAB     = "multicrab_Hplus2tbAnalysis_v8030_20180508T0644"
    DIRNAME   = None

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=True, conflict_handler="resolve")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("--systVars", dest="systVars", default = SYSTVARS,
                      help="List of comma-separated (NO SPACE!) systematic variations to  perform. Overwrites the default list of systematics [default: %s]" % SYSTVARS)

    parser.add_option("--codePath", dest="codePath", default = CODEPATH,
                      help="Full path to HiggsAnalysis code tarball to be ran on [default: %s]" % CODEPATH)

    parser.add_option("--mcrabPath", dest="mcrabPath", default = MCRABPATH,
                      help="Full path to multicrab Ntuples to be ran on [default: %s]" % MCRABPATH)

    parser.add_option("--mcrab", dest="mcrab", action="store", default = MCRAB,
                      help="Path to the multicrab directory for input [default: %s]" % (MCRAB) )

    parser.add_option("-d", "--dirName", dest="dirName", action="store",
                      help="Name of directory to be created where all the output will be stored [default: %s]" % (DIRNAME) )

    parser.add_option("--topMass", dest="topMass", action="store", default=None,
                      help="Top mass cut used in analuysis [default: %s]" % (None) )

    parser.add_option("--bdt", dest="BDT", action="store", default=None,
                      help="BDT cut used in analuysis [default: %s]" % (None) )

    (opts, parseArgs) = parser.parse_args()

    if opts.topMass == None:
        Print("Please provide a top mass cut value (--topMass 500)", True)

    if opts.BDT == None:
        Print("Please provide a BDT cut value (--bdt 0p40)", True)

    # Define output dir name
    date = datetime.date.today().strftime('%d%b%Y')    #date = datetime.date.today().strftime('%d-%b-%Y')
    if opts.dirName == None:
        opts.dirName = "TopMassLE%s_BDT%s_AbsEta0p8_1p4_2p0_Pt_60_90_160_300_Stat_%s" % (opts.topMass, opts.BDT, date)
    else:
        opts.dirName += "_%s" % (date)

    # Overwrite default systematics
    opts.systVarsList = []
    if opts.systVars != None:
        opts.doSystematics = True
        opts.systVarsList = opts.systVars.split(",")
    else:
        opts.systVarsList = ["JES", "JER", "BTagSF", "TopPt", "PUWeight",  "TopTagSF"]

    # Call the main function
    main(opts)
