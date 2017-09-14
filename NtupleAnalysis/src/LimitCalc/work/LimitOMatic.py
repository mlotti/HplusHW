#! /usr/bin/env python
'''
DESCRIPTION:
This is the swiss pocket knife for running Lands/Combine on large array of datacards


INSTRUCTIONS:


USAGE:
./LimitOMatic.py --sigmabrlimit --lhcasy --dir <datacard_dir> [opts]



Example:
./LimitOMatic.py --sigmabrlimit --lhcasy --dir datacards_combine_170904_144807_Hplus2tb_13TeV_LdgTetrajetMass_Run2016_80to1000_nominal_example3__MC_FakeAndGenuineTauNotSeparated/ --verbose


Last Used:
./LimitOMatic.py --sigmabrlimit --lhcasy --dir datacards_combine_170904_144807_Hplus2tb_13TeV_LdgTetrajetMass_Run2016_80to1000_nominal_example3__MC_FakeAndGenuineTauNotSeparated/ --verbose

'''
#================================================================================================ 
# Imports
#================================================================================================ 
import os
import sys
import select
import pty
import subprocess
import json
from optparse import OptionParser
import re

import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.LimitCalc.CommonLimitTools as commonLimitTools

#================================================================================================ 
# Class Definition
#================================================================================================ 
def Verbose(msg, printHeader=False):
    #if not opts.verbose:
    if opts.verbose <= 2:
        return
    
    if printHeader:
        print "=== LimitOMatic.py:"
        
    if msg !="":
        print "\t", msg
    return

def Print(msg, printHeader=False):
    if printHeader:
        print "=== LimitOMatic.py:"
        
    if msg !="":
        print "\t", msg
    return

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]


#================================================================================================ 
# Class Definition
#================================================================================================ 
class Result:
    def __init__(self, opts, basedir):
        self._opts            = opts
        self._basedir         = basedir
        self._allRetrieved    = False
        self._limitCalculated = False
        self._output          = ""
        self._findJobDir(basedir)
        if self._jobDir == None:
            if self._opts.printonly:
                msg =  "Need to create and submit jobs first! Skipping ..."
                Print(ShellStyles.ErrorLabel()  + msg, True)
            else:
                msg = "Creating and submitting " + basedir
                Verbose(msg, True)
                self._createAndSubmit()
        else:
            msg = "Check if limits have already been calculated ..."
            Verbose(msg, True)

            lumiPath = "%s/%s/limits.json" % (self._basedir, self._jobDir) 
            if os.path.exists(lumiPath):
                msg = "File \"%s\" already exists!\n\tThe limit has already been calculated.\n\tSkipping ..." % (lumiPath)
                Print(ShellStyles.NoteStyle()  + msg + ShellStyles.NormalStyle(), True)
                self._limitCalculated = True
            else:
                msg = "Creating and submitting " + basedir
                Verbose(msg, True)
                self._createAndSubmit()
                #if not self._opts.printonly and not self._opts.lhcTypeAsymptotic:
                #    self._getOutput()
        return

    def _findJobDir(self, basedir):
        self._jobDir = None

        counter = 0
        # For-loop: All sub-directories & files inside basedir
        for dirname, dirnames, filenames in os.walk(basedir):
            nSubDirs = len(dirnames)
            nFiles   = len(filenames)
            msg      = "Found %s sub-directories and %s files under %s" % (nSubDirs, nFiles, dirname)
            Verbose(msg, counter==0)

            # For-loop: All directories inside basedir            
            for subdirname in dirnames:
                if "LandSMultiCrab" in subdirname or "CombineMultiCrab" or "CombineResults" in subdirname:
                    self._jobDir = subdirname
                else:
                    pass
            counter += 1
        return

    def _createAndSubmit(self):
        # Go to base directory
        os.chdir(self._basedir)

        # Create jobs
        myPath = os.path.join(os.getenv("HIGGSANALYSIS_BASE"), "NtupleAnalysis/src/LimitCalc/work")
        if not os.path.exists(myPath):
            raise Exception("Error: Could not find directory '%s'!" % myPath)

        myCommand = os.path.join(myPath, "generateMultiCrabTaujets.py")
        if self._opts.combination:
            myCommand = os.path.join(myPath, "generateMultiCrabCombination.py")

        if self._opts.brlimit:
            myCommand += " --brlimit"
        else:
            myCommand += " --sigmabrlimit"

        myGridStatus = True
        if hasattr(self._opts, "lepType") and self._opts.lepType:
            myCommand += " --lep"
            raise Exception("The LEP type CLs is no longer supported. Please use --lhcasy (asymptotic LHC-type CLs.")

        if hasattr(self._opts, "lhcType") and self._opts.lhcType:
            myCommand += " --lhc"
            raise Exception("The LHC type CLs is no longer supported. Please use --lhcasy (asymptotic LHC-type CLs.")

        if hasattr(self._opts, "lhcTypeAsymptotic") and self._opts.lhcTypeAsymptotic:
            myCommand += " --lhcasy"
            myGridStatus = False

        if myGridStatus:
            myCommand += " --create"

        if not self._opts.nomlfit:
            myCommand += " --mlfit"

        if self._opts.significance:
            myCommand += " --significance"

        if self._opts.unblinded:
            myCommand += " --final"

        #msg = "Creating jobs with command:\n\t%s" % myCommand
        msg =  myCommand
        Verbose(ShellStyles.HighlightAltStyle() + msg + ShellStyles.NormalStyle() , True)
        os.system(myCommand)

        # asymptotic jobs are run on the fly
        if myGridStatus:
            
            # Change to job directory
            self._findJobDir(".")
            if self._jobDir == None:
                raise Exception("Error: Could not find 'LandSMultiCrab' or 'CombineMultiCrab' in a sub directory name under the base directory '%s'!"%self._basedir)
            os.chdir(self._jobDir)

            # Submit jobs
            msg = "Submitting multicrab jobs" 
            Verbose(msg, True)
            proc = subprocess.Popen(["multicrab", "-submit all"], stdout=subprocess.PIPE)
            (out, err) = proc.communicate()
            print out

        # Change directory back
        s = self._backToTopLevel()
        if len(s) > 1:
            os.chdir(s)
        # print "current dir =",os.getcwd()
        return

    def _getOutput(self):
        # Go to job directory
        os.chdir("%s/%s"%(self._basedir,self._jobDir))
        # Get output
        print "Checking output and status"
        proc = subprocess.Popen(["multicrab","-status -get"], stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        # Check status
        myStatus = True
        while myStatus:
            print "Calling for hplusMultiCrabStatus.py to check status of jobs ..."
            proc = subprocess.Popen(["hplusMultiCrabStatus.py"], stdout=subprocess.PIPE)
            (out, err) = proc.communicate()
            # Handle output
            myLines = out.split("\n")
            myStatusSummary = []
            myResubmitCommands = []
            myStatusStarted = False
            myResubmitStarted = False
            for line in myLines:
                if myStatusStarted:
                    if not "------" in line:
                        myStatusSummary.append(line)
                if myResubmitStarted:
                    if "crab" in line:
                        myResubmitCommands.append(line)
                # Update status
                if "-------" in line:
                    if not myStatusStarted:
                        myStatusStarted = True
                    elif not myResubmitStarted:
                        myStatusStarted = False
                        myResubmitStarted = True
            # Update status
            for line in myStatusSummary:
                print line
            if len(myStatusSummary) == 1:
                if "Retrieved:" in myStatusSummary[0]:
                    self._allRetrieved = True
            # Resubmit
            for line in myResubmitCommands:
                print "resubmitting"
                os.system(line)
            # Fetch results
            myDoneStatus = False
            for line in myStatusSummary:
                if "Done" in line:
                    myDoneStatus = True
            if myDoneStatus:
                print "Fetching output"
                proc = subprocess.Popen(["multicrab","-status -get"], stdout=subprocess.PIPE)
                (out, err) = proc.communicate()
            else:
                myStatus = False
        # Obtain results
        if self._allRetrieved:
            # Commented the subprocess merging, because it started to hang frequently
            print "Merging results"
            #proc = subprocess.Popen(["landsMergeHistograms.py","--delete"],stdout=subprocess.PIPE)
            #(out, err) = proc.communicate()
            os.system("landsMergeHistograms.py --delete")
            self._limitCalculated = True
            #self._output += "cd %s/%s\n"%(self._basedir,self._jobDir)
            #self._output += "landsMergeHistograms.py --delete\n"
            #self._output += "cd %s\n"%self._backToTopLevel()

        # Change directory back
        os.chdir(self._backToTopLevel())

    def _backToTopLevel(self):
        mySplit = self._basedir.split("/")
        s = ""
        for i in range(0,len(mySplit)-1):
            s += "../"
        if s == "":
            s = "."
        return s 

    def _runSubProcess(self, inputList):
        s = ""
        master, slave = pty.openpty()
        proc = subprocess.Popen(inputList,stdout=slave,stderr=slave,close_fds=True)
        while proc.poll() is None: # do not use communicate() because it can block
            proc.check_output()
            (out,err) = proc.communicate()
        return out

    def printResults(self):
        '''
        Print the results for all mass points:
        mass,  observed median, -2sigma, -1sigma, +1sigma, +2sigma, Rel. errors in same order
        '''
        msg = "{:^120}".format(self._basedir)
        Print(msg)
        if not self._limitCalculated:
            Verbose("Results not yet retrieved. Return", True)
            return

        # Open json file to read the results
        filePath   = "%s/%s/limits.json" % (self._basedir,self._jobDir)
        fileMode   = "r"
        myFile     = open(filePath, fileMode)
        myResults  = json.load(myFile)
        masspoints = myResults["masspoints"]
        myKeys     = ["median","-2sigma","-1sigma","+1sigma","+2sigma"]
        line       = "mass  obs.      "
        
        # Print columns names
        hLine = "="*120
        Print(hLine)
        for item in myKeys:
            line += "%9s " % item
        line += "   Rel. errors in same order"
        Print(line)
        Print(hLine)

        # For-loop: From small to high mass values
        for i, k in enumerate(sorted(masspoints.keys(), key=natural_keys), 1):
            line = "%4d " % int(k)
            if self._opts.unblinded:
                line += " %9.5f"%float(masspoints[k]["observed"])
            else:
                line += " (blinded) "
            for item in myKeys:
                line += " %9.5f"%(float(masspoints[k]["expected"][item]))
            for item in myKeys:
                if "%s_error"%item in masspoints[k]["expected"]:
                    a = float(masspoints[k]["expected"]["%s_error"%item])
                    b = float(masspoints[k]["expected"][item])
                    r = 0.0
                    if b > 0:
                        r = a/b
                    line += " %9.4f"%(r)
                else:
                    line += "      n.a."
            Print(line, False)

        # Close json file
        myFile.close()
        Print(hLine)
        print
        return


    def getBaseDir(self):
        return self._basedir


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
    
    # Default Values
    VERBOSE     = 0 #-1 to 4
    PRINTONLY   = False
    COMBINATION = False
    parser = commonLimitTools.createOptionParser(lepDefault=None, lhcDefault=False, lhcasyDefault=True, fullOptions=False)

    parser.add_option("--printonly", dest="printonly", action="store_true", default=PRINTONLY, 
                      help="Print only the ready results [default = %s]" % PRINTONLY)

    parser.add_option("--combination", dest="combination", action="store_true", default=COMBINATION, 
                      help="Run combination instead of only taunu fully hadr.")

    parser.add_option("-v", "--verbose", dest="verbose", default = VERBOSE,
                      help="Enable verbosity (for debugging) 0-4 (-1 = very quiet; 0 = quiet, 1 = verbose, 2+ = debug) [default = %s]" % VERBOSE)

    opts = commonLimitTools.parseOptionParser(parser)

    # Obtain directory list
    myDirs = opts.dirs[:]
    if len(myDirs) == 0 or (len(myDirs) == 1 and myDirs[0] == "."):
        myDirs = []
        for dirname, dirnames, filenames in os.walk('.'):
            for subdirname in dirnames:
                #if "LandSMultiCrab" in subdirname:
                if "datacards_" in subdirname:
                    myDirs.append(os.path.join(dirname, subdirname))
        if len(myDirs) == 0:
            raise Exception("Error: Could not find any sub directories starting with 'datacards_' below this directory!")
    myDirs.sort()
    myResults   = []
    dir_counter = 1

    # For-loop: All datacard directories
    for counter, d in enumerate(myDirs, 1):
        msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Directory", "%i" % counter, "/", "%i:" % len(myDirs), "%s" % d)
        Print(ShellStyles.HighlightAltStyle()  + msg + ShellStyles.NormalStyle(), counter==1)
        myResults.append(Result(opts, d))

        # Inform user of success
        msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Directory", "%i" % counter, "/", "%i:" % len(myDirs), "Success")
        Print(ShellStyles.SuccessStyle()  + msg + ShellStyles.NormalStyle(), True)

    Verbose("The results are stored in the following directories:", counter==1)
    for i, r in enumerate(myResults, 1):
        msg = str(i) + ") " + r.getBaseDir()
        Verbose(msg, False)

    Print("Printing results for all directories:", True)
    for r in myResults:
        r.printResults()

    # Manual submitting of merge
    s = ""
    for r in myResults:
       s += r._output

    if s != "":
        msg = "Run the following to merge the root files (then rerun this script to see the summary of results)"
        Print(msg, True)
        print s
