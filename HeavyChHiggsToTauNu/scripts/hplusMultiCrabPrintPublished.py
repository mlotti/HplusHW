#!/usr/bin/env python

import os
import re
import sys
import glob

from optparse import OptionParser
import ConfigParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.OrderedDict as OrderedDict
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import hplusMultiCrabAnalysis as multicrabAnalysis

class Task:
    def __init__(self, directory):
        self.directory = directory

        self.inputDataset = None
        self.publishName = None

        self.events = None
        self.jobs = None
        self.time = None
        self.size = None
        self.dbsPath = None

def main(opts):
    taskDirs = multicrab.getTaskDirectories(opts)

    # Find task directories
    tasks = OrderedDict.OrderedDict()
    for d in taskDirs:
        if os.path.exists(d):
            tasks[d] = Task(d)
        elif os.path.exists(d+"_published"):
            print "%s: using directory %s_published" % (d, d)
            tasks[d] = Task(d+"_published")
        else:
            print "%s: directory not found, skipping" % d

    print

    # Find publish name from crab.cfg's
    for key, task in tasks.iteritems():
        cfgparser = ConfigParser.ConfigParser()
        cfgparser.read(os.path.join(task.directory, "share", "crab.cfg"))
        task.inputDataset = cfgparser.get("CMSSW", "datasetpath").split("/")[1]
        task.publishName = cfgparser.get("USER", "publish_data_name")
        #print task.inputDataset, task.publishName
    #print

    # Read publish.log files produced by hplusMultiCrabPublish.py
    publishLogs = glob.glob("publish_*.log")
    if len(publishLogs) == 0:
        print "Did not find any publish_*.log files, are you sure you've run hplusMultiCrabPublish?"
        return 1
    log_re = re.compile("total events: (?P<events>\d+) in dataset: (?P<dbs>/\S+)")
    for logFile in publishLogs:
        f = open(logFile)
        for line in f:
            m = log_re.search(line)
            if m:
                dbsPath = m.group("dbs")
                found = False
                for key, task in tasks.iteritems():
                    if task.inputDataset in dbsPath and task.publishName in dbsPath:
                        task.events = m.group("events")
                        task.dbsPath = dbsPath
                        found = True
                if not found:
                    print "Did not find crab task matching to published %s" % dbsPath
    #print

    # Read time and size information
    timeAnalysis = multicrabAnalysis.TimeAnalysis()
    sizeAnalysis = multicrabAnalysis.SizeAnalysis(opts.sizeFile)
    analyses = [timeAnalysis, sizeAnalysis]
    print
    for key, task in tasks.iteritems():
        # For this we don't care if the jobs succeeded or not
        outFiles = glob.glob(os.path.join(task.directory, "res", "CMSSW_*.stdout"))
        if len(outFiles) == 0:
            print "%s: 0 CMSSW_*.stdout files, something is badly wrong!" % key
            sys.exit(1)

        multicrabAnalysis.analyseFiles(outFiles, analyses)
        task.jobs = len(outFiles)
        task.time = timeAnalysis.userTime()
        task.size = sizeAnalysis.size()

    # Print out
#    print
#    for key, task in tasks.iteritems():
        print "# %s events, %d jobs" % (task.events, task.jobs)
        print "# %s" % task.time
        print "# %s" % task.size
        print '"%s": TaskDef("%s"),' % (key, task.dbsPath)

    return 0
    


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    multicrab.addOptions(parser)
    parser.add_option("--sizeFile", dest="sizeFile", default="pattuple.root",
                      help="For --size, specify the output file name (default: 'pattuple.root')")
    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)

    sys.exit(main(opts))
