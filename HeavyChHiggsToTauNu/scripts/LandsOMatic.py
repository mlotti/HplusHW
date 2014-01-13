#! /usr/bin/env python

# This is the swiss pocket knife for running Lands on large array of datacards
# Author: Lauri Wendland

import os
import sys
import select
import pty
import subprocess
import json
from optparse import OptionParser


class Result:
    def __init__(self, opts, basedir):
        print basedir
        self._opts = opts
        self._basedir = basedir
        self._allRetrieved = False
        self._limitCalculated = False
        self._output = ""
        self._findJobDir()
        print self._jobDir
        if self._jobDir == None:
            if self._opts.printOnly:
                raise Exception("Error: need to create and submit jobs first!")
            self._createAndSubmit()
        else:
            # Check if limits have already been calculated
            if os.path.exists("%s/%s/limits.json"%(self._basedir,self._jobDir)):
                print "Limit already calculated"
                self._limitCalculated = True
            else:
                if not self._opts.printonly:
                    self._getOutput()

    def _findJobDir(self):
        self._jobDir = None
        for dirname, dirnames, filenames in os.walk(self._basedir):
            for subdirname in dirnames:
                if "LandSMultiCrab" in subdirname:
                    self._jobDir = subdirname
        if self._jobDir == None:
            raise Exception("Error: Could not find 'LandSMultiCrab' in a sub directory name under the base directory '%s'!"%self._basedir)

    def _createAndSubmit(self):
        # Go to base directory
        os.chdir(self._basedir)
        # Find brlimit directory
        s = ""
        i = 0
        while not os.path.exists("./%sbrlimit"%(s)) and i < 5:
            s += "../"
        if i == 5:
            raise Exception("Error: Could not find test/brlimit directory!")
        # Create jobs
        myCommand = "%sbrlimit/generateMultiCrabTaujets.py --lhc --create"%(s)
        if self._opts.brlimit:
            myCommand += " --brlimit"
        if self._opts.sigmabrlimit:
            myCommand += " --sigmabrlimit"
        print "Creating jobs with:",myCommand
        os.system(myCommand)
        # Change to job directory
        self._findJobDir()
        os.chdir(self._jobDir)
        # Submit jobs
        print "Submitting jobs"
        proc = subprocess.Popen(["multicrab","-submit all"], stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        print out
        # Change directory back
        os.chdir(self._backToTopLevel())

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
        for i in range(0,len(mySplit)):
            s += "../"
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
        line = "mass  "
        for item in myKeys:
            line += "%9s "%item
        print line+"   Rel. errors in same order"
        for k in sorted(masspoints.keys()):
            line = "%4d "%int(k)
            for item in myKeys:
                line += " %9.5f"%(float(masspoints[k]["expected"][item]))
            for item in myKeys:
                a = float(masspoints[k]["expected"]["%s_error"%item])
                b = float(masspoints[k]["expected"][item])
                r = 0.0
                if b > 0:
                    r = a/b
                line += " %9.4f"%(r)
            print line
        myFile.close()

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-h", "--help", dest="helpStatus", action="store_true", default=False, help="Show this help message and exit")
    parser.add_option("--brlimit", dest="brlimit", action="store_true", default=False, help="Calculate limit on Br(t->bH+)")
    parser.add_option("--sigmabrlimit", dest="sigmabrlimit", action="store_true", default=False, help="Calculate limit on sigma(H+)xBr(t->bH+)")
    parser.add_option("--printonly", dest="printonly", action="store_true", default=False, help="Print only the ready results")
    (opts, args) = parser.parse_args()
    if opts.helpStatus:
        parser.print_help()
        sys.exit()

    # Check options
    if opts.brlimit == opts.sigmabrlimit and not opts.printonly:
        if opts.brlimit:
            raise Exception("Error: Please enable only --brlimit or --sigmabrlimit !")
        else:
            raise Exception("Error: Please enable --brlimit or --sigmabrlimit !")

    # Obtain directory list
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
    for d in myDirs:
        myResults.append(Result(opts,d))

    # Summary of results
    print "\nSummary of results"
    for r in myResults:
        r.printResults()

    # Manual submitting of merge
    s = ""
    for r in myResults:
        s += r._output
    if s != "":
        print "\nRun the following to merge the root files (then rerun this script to see the summary of results)"
        print s