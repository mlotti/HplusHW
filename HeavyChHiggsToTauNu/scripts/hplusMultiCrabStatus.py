#!/usr/bin/env python

import subprocess
import shutil
import time
import sys
import os
import re
from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

order_done = ["Retrieved", "Done"]
order_run = ["Running", "Scheduled", "Ready", "Submitted", "Created"]

def main(opts):
    taskDirs = multicrab.getTaskDirectories(opts)
    multicrab.checkCrabInPath()

    resubmitJobs = {}
    stats = {}
    allJobs = 0

    for task in taskDirs:
        if not os.path.exists(task):
            if opts.showMissing:
                print "%s: Task directory missing" % task
            continue
        
        jobs = multicrab.crabStatusToJobs(task)

        lens = {}
        njobs = 0
        for key, item in jobs.iteritems():
            l = len(item)
            lens[key] = l
            njobs += l
            allJobs += l
            if key in stats:
                stats[key] += l
            else:
                stats[key] = l

        # First the succesfully done
        line = "%s (%d jobs):" % (task, njobs)
        for s in order_done:
            if s in lens:
                line += " %s %d," %(s, lens[s])
                del lens[s]

        # Then the aborted-submitted to the end of the line
        line_end = ""
        for s in order_run:
            if s in lens:
                line_end += " %s %d,"%(s, lens[s])
                del lens[s]

        # Then the failed ones to the middle
        keys = lens.keys()
        keys.sort()
        for key in keys:
            line += " %s %d," % (key, lens[key])
        line += line_end
        if line[-1] == ",":
            line = line[0:-1]
        
        print line

        # Infer the jobs to be resubmitted
        resubmit = []
        for key, joblist in jobs.iteritems():
            for job in joblist:
                if job.failed(opts.status):
                    resubmit.append(job.id)
        if len(resubmit) > 0:
            resubmit.sort()
            pretty = multicrab.prettyJobnums(resubmit)
            resubmitJobs[task] = pretty
    
    print "----------------------------------------"
    print "Summary for %d task(s), total %d job(s):" % (len(taskDirs), allJobs)
    for s in order_done:
        if s in stats:
            print "%s: %d" % (s, stats[s])
            del stats[s]
    b = []
    for s in order_run:
        if s in stats:
            b.append("%s: %d" % (s, stats[s]))
            del stats[s]
    keys = stats.keys()
    keys.sort()
    for key in keys:
        print "%s: %d" % (key, stats[key])
    for line in b:
        print line


    print "----------------------------------------"
    if len(resubmitJobs) == 0:
        print "No failed/aborted jobs to resubmit"
    else:
        print "Following jobs failed/aborted, and can be resubmitted"
        print
        for task, jobs in resubmitJobs.iteritems():
            print "crab -c %s -resubmit %s" % (task, jobs)
        print
    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    parser.add_option("--status", dest="status", default="all", 
                      help="Provide the resubmit list for these jobs ('all', 'Aborted', comma separated list of exit codes; default 'all'")
    parser.add_option("--showMissing", dest="showMissing", action="store_true", default=False,
                      help="Show also the missing task directories")
    (opts, args) = parser.parse_args()

    opts.status = opts.status.lower()
    if opts.status not in ["all", "aborted"]:
        codes = opts.status.split(",")
        opts.status = [int(c) for c in codes]

    sys.exit(main(opts))
