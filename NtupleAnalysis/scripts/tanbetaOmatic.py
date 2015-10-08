#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

def getCrabDir(taskDir):
    mysublist = os.listdir(taskDir)
    for subl in mysublist:
        if subl.startswith("crab_0_"):
            return subl
    return None

def isResultRetrieved(taskDir, crabDir):
    myreslist = os.listdir(os.path.join(taskDir,crabDir,"res"))
    for resl in myreslist:
        if resl.startswith("output_") and resl.endswith(".tgz"):
            return True
    return False

def isResultExtracted(taskDir):
    mysublist = os.listdir(taskDir)
    for subl in mysublist:
        if subl.startswith("higgsCombine") and subl.endswith(".root"):
             return True
    return False

def checkTaskdirStatuses():
    print "Checking task dir statuses ..."
    nall = 0
    nsub = 0
    nrun = 0
    nout = 0
    ndone = 0
    unfinishedjobs = []

    mylist = os.listdir(".")
    for l in mylist:
        if l.startswith("CombineMultiCrab_"):
            nall += 1
            mysublist = os.listdir(l)
            myCrabDir = getCrabDir(l)
            if myCrabDir == None:
                if isResultExtracted(l):
                    continue
                print "Submitting %s"%l
                os.system("cd %s ; crab -create -submit all ; cd .."%l)
                nsub += 1
                continue
            # crab task created
            myResultRetrievedStatus = isResultRetrieved(l, myCrabDir)
            if not myResultRetrievedStatus:
                print "Checking status %s"%l
                os.system("cd %s ; crab -status -get ; cd .."%l)
                if not isResultRetrieved(l, myCrabDir):
                    unfinishedjobs.append(l)
                    nrun += 1
                    continue
            # Result has been retrieved
            myResultExtractedStatus = isResultExtracted(l)
            if not myResultExtractedStatus:
                print "Extracting result %s"%l
                os.system("cd %s ; tar xfz crab_0*/res/output*tgz ; cd .."%l)
                if not isResultExtracted(l):
                    nout += 1
                    continue
            # Results exist
            ndone += 1
            # Clean up
            if myCrabDir != None:
                myPath = os.path.join(l,myCrabDir,"share")
                if os.path.exists(myPath):
                    os.system("rm -r %s"%myPath)
                myPath = os.path.join(l, "combine")
                if os.path.exists(myPath):
                    os.system("rm -r %s"%myPath)

    if len(unfinishedjobs) > 0:
        print "\nPotentially troublesome tasks:"
        for l in unfinishedjobs:
            print "  %s"%l
    print "\nTan beta run status:"
    print "              Tasks:",nall
    print "     Task submitted:",nsub
    print "   Queueing/Running:",nrun
    print "Raw output obtained:",nout
    print "               Done:",ndone
    if ndone != nall:
        print "\nRerun this script again to advance the status until all tasks are done"
    else:
        print "\nAll jobs done"
        return True
    return False

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--create", dest="createGridTasks", action="store_true", default=False, help="Create grid tasks")
    parser.add_option("--scen", dest="scenarios", action="append", default=[], help="MSSM scenarios")
    parser.add_option("-t", "--tanbeta", dest="tanbeta", action="append", default=[], help="tanbeta values (will scan only these)")
    parser.add_option("-m", "--mass", dest="massPoints", action="append", default=[], help="mass values (will scan only these)")
    parser.add_option("--tanbetarangemin", dest="tanbetarangemin", action="append", default=[], help="tanbeta values minimum range")
    parser.add_option("--tanbetarangemax", dest="tanbetarangemax", action="append", default=[], help="tanbeta values maximum range")
    parser.add_option("--export", dest="export", action="store_true", default=False, help="Export results when they are done")
    (opts, args) = parser.parse_args()

    if opts.createGridTasks:
        myCommand = os.environ["CMSSW_BASE"]+"/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/brlimit/doTanBetaScan.py"
        myCommand += " --lhcasy --final --sigmabrlimit"
        myCommand += " --creategridjobs --gridmassive"
        for s in opts.scenarios:
            myCommand += " --scen %s"%s
        for s in opts.tanbeta:
            myCommand += " -t %s"%s
        for s in opts.massPoints:
            myCommand += " -m %s"%s
        if len(opts.tanbetarangemin) > 0 and len(opts.tanbetarangemax) > 0:
            myCommand += " --tanbetarangemin %s --tanbetarangemax %s"%(opts.tanbetarangemin, opts.tanbetarangemax)
        print "Creating crab task directories with command:\n%s"%myCommand
        #os.system(myCommand)

    if checkTaskdirStatuses():
        if opts.export:
            print "Making package of results ..."
            os.system("tar cfz tanbeta_results.tgz CombineMultiCrab_lhcasy* *WG.root")
            print "Results have been exported"
        print "All results have been retrieved."
        print "To do plots, run brlimit/tanbetaReadResults.py"

