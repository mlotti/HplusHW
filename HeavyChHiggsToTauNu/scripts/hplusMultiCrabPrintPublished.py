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

#        self.events = None
        self.jobs = None
        self.time = None
        self.size = None
        self.dbsPath = None
        self.jobs_published = None
        self.jobs_failed = None
        self.jobs_still_to_publish = None

def addInputPublishToTasks(tasks):
    for key, task in tasks.iteritems():
        cfgparser = ConfigParser.ConfigParser()
        cfgparser.read(os.path.join(task.directory, "share", "crab.cfg"))
        task.inputDataset = cfgparser.get("CMSSW", "datasetpath").split("/")[1]
        task.publishName = cfgparser.get("USER", "publish_data_name")
        #print task.inputDataset, task.publishName

#log_re = re.compile("total events: (?P<events>\d+) in dataset: (?P<dbs>/\S+)")
log_re = re.compile("Publishing block (?P<dbs>/[^#]+)#")
summary_re = re.compile("published (?P<published>\d+), failed (?P<failed>\d+), still_to_publish (?P<still>\d+)")
def parseLog(logFile, tasks):
    dbsPath = None
    f = open(logFile)
    for line in f:
        # Infer DBS path
        m = log_re.search(line)
        if m:
            tmp = m.group("dbs")
            if dbsPath is None:
                dbsPath = tmp
            elif dbsPath != tmp:
                raise Exception("Internal error: dbsPath '%s' tmp '%s'" % (dbsPath, tmp))
            continue
        # After summary line, find the corresponding task
        m = summary_re.search(line)
        if m:
            if dbsPath is None:
                raise Exception("Did not find DBS path before summary, line '%s' of file %s" % (line, logFile))
            found = False
            for key, task in tasks.iteritems():
                if task.inputDataset in dbsPath and task.publishName in dbsPath:
#                    task.events = m.group("events")
                    task.jobs_published = int(m.group("published"))
                    task.jobs_failed = int(m.group("failed"))
                    task.jobs_still_to_publish = int(m.group("still"))
                    task.dbsPath = dbsPath
                    found = True
                    break
            if not found:
                print "Did not find crab task matching to published %s" % dbsPath
            dbsPath = None

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
    addInputPublishToTasks(tasks)
    #print

    # Read publish.log files produced by hplusMultiCrabPublish.py
    publishLogs = glob.glob("publish_*.log")
    if len(publishLogs) == 0:
        print "Did not find any publish_*.log files, are you sure you've run hplusMultiCrabPublish?"
        return 1
    publishLogs.sort()
    for logFile in publishLogs:
        parseLog(logFile, tasks)

    #print

    # Check if publication is complete
    taskNames = tasks.keys()
    taskNames.sort()
    for name in taskNames:
        task = tasks[name]
        still = task.jobs_still_to_publish
        if still is not None and still > 0:
            print "%s publication not complete (published %d, failed %d, still_to_publish %d)" % (name, task.jobs_published, task.jobs_failed, still)
            del tasks[name]

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

        npublished = task.jobs_published
        if npublished is not None and npublished != task.jobs:
            print "%s publication nto complete (published %d of %d jobs)" % (npublished, task.jobs)

    # Print out
#    print
#    for key, task in tasks.iteritems():
#        print "# %s events, %d jobs" % (task.events, task.jobs)
        print "# %d jobs" % (task.jobs)
        print "# %s" % task.time
        print "# %s" % task.size
        print '"%s": TaskDef("%s", dbs="phys03"),' % (key, task.dbsPath)

    return 0
    


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    multicrab.addOptions(parser)
    parser.add_option("--sizeFile", dest="sizeFile", default="pattuple.root",
                      help="For --size, specify the output file name (default: 'pattuple.root')")
    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)

    sys.exit(main(opts))
