#! /usr/bin/env python

# This is the swiss pocket knife for running Lands/Combine on large array of datacards
# Author: Lauri Wendland

import os
import sys
import select
import pty
import subprocess
import json
from optparse import OptionParser

import HiggsAnalysis.LimitCalc.CommonLimitTools as commonLimitTools

class Result:
    def __init__(self, opts, basedir):
        self._opts = opts
        self._basedir = basedir
        self._allRetrieved = False
        self._limitCalculated = False
        self._output = ""
        self._findJobDir(basedir)
        if self._jobDir == None:
            if self._opts.printonly:
                print "Error: need to create and submit jobs first! Skipping ..."
            else:
                self._createAndSubmit()
        else:
            # Check if limits have already been calculated
            if os.path.exists("%s/%s/limits.json"%(self._basedir,self._jobDir)):
                print "Limit already calculated, skipping ..."
                self._limitCalculated = True
            else:
                self._createAndSubmit()
                #if not self._opts.printonly and not self._opts.lhcTypeAsymptotic:
                #    self._getOutput()

    def _findJobDir(self, basedir):
        self._jobDir = None
        for dirname, dirnames, filenames in os.walk(basedir):
            for subdirname in dirnames:
                if "LandSMultiCrab" in subdirname or "CombineMultiCrab" or "CombineResults" in subdirname:
                    self._jobDir = subdirname

    def _createAndSubmit(self):
        # Go to base directory
        os.chdir(self._basedir)
        # Create jobs
        myPath = os.path.join(os.getenv("HIGGSANALYSIS_BASE"), "NtupleAnalysis/src/LimitCalc/work")
        if not os.path.exists(myPath):
            raise Exception("Error: Could not find directory '%s'!"%myPath)
        myCommand = os.path.join(myPath, "generateMultiCrabTaujets.py")
        if self._opts.combination:
            myCommand = os.path.join(myPath, "generateMultiCrabCombination.py")
        if self._opts.brlimit:
            myCommand += " --brlimit"
        else:
            myCommand += " --sigmabrlimit"       
#        if self._opts.sigmabrlimit:
#            myCommand += " --sigmabrlimit"
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
#        print "Creating jobs with:",myCommand
        os.system(myCommand)
        if myGridStatus:
            # asymptotic jobs are run on the fly
            # Change to job directory
            self._findJobDir(".")
            if self._jobDir == None:
                raise Exception("Error: Could not find 'LandSMultiCrab' or 'CombineMultiCrab' in a sub directory name under the base directory '%s'!"%self._basedir)
            os.chdir(self._jobDir)
            # Submit jobs
            print "Submitting jobs"
            proc = subprocess.Popen(["multicrab","-submit all"], stdout=subprocess.PIPE)
            (out, err) = proc.communicate()
            print out
        # Change directory back
        s = self._backToTopLevel()
        if len(s) > 1:
            os.chdir(s)
        #print "current dir =",os.getcwd()

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
        print "\n"+self._basedir
        if not self._limitCalculated:
            print "Results not yet retrieved"
            return
        myFile = open("%s/%s/limits.json"%(self._basedir,self._jobDir),"r")
        myResults = json.load(myFile)
        masspoints = myResults["masspoints"]
        myKeys = ["median","-2sigma","-1sigma","+1sigma","+2sigma"]
        line = "mass  obs.      "
        for item in myKeys:
            line += "%9s "%item
        print line+"   Rel. errors in same order"
        for k in sorted(masspoints.keys()):
            line = "%4d "%int(k)
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
            print line
        myFile.close()

    def getBaseDir(self):
        return self._basedir

if __name__ == "__main__":
    parser = commonLimitTools.createOptionParser(lepDefault=None, lhcDefault=False, lhcasyDefault=True, fullOptions=False)
    parser.add_option("--printonly", dest="printonly", action="store_true", default=False, help="Print only the ready results")
    parser.add_option("--combination", dest="combination", action="store_true", default=False, help="Run combination instead of only taunu fully hadr.")
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
    myResults = []
    dir_counter = 1
    for d in myDirs:
        print "\n\033[93mLimitOMatic: Considering directory %s (directory %d/%d)\033[00m"%(d,dir_counter,len(myDirs))
        myResults.append(Result(opts,d))
        print "\033[92mLimitOMatic: Directory %s (directory %d/%d) processed!\033[00m"%(d,dir_counter,len(myDirs))
        dir_counter+=1       

    # Summary of results
#    print "The results stored in the following directories:""
#    for r in myResults:
#        print(r.getBaseDir())

#    for r in myResults:
#        r.printResults()

    # Manual submitting of merge
    s = ""
    for r in myResults:
        s += r._output
    if s != "":
        print "\nRun the following to merge the root files (then rerun this script to see the summary of results)"
        print s
