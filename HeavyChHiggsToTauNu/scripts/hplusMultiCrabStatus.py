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

class JobSummary:
    def __init__(self, njobs, hosts):
        self.njobs = njobs
        self.hosts = hosts

def formatSummaries(opts, line, key, summary):
    sum = " %s %d" % (key, summary.njobs)
    if opts.showHosts:
        line += "\n "+sum
        if len(summary.hosts) > 0:
            line += " (%s)" % ",".join(summary.hosts)
    else:
        line += sum+","
    return line

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

        jobSummaries = {}
        njobs = 0
        for key, item in jobs.iteritems():
            hosts = {}
            for job in item:
                if job.host != None:
                    hosts[job.host] = 1
            l = len(item)
            jobSummaries[key] = JobSummary(l, hosts)
            njobs += l
            allJobs += l
            if key in stats:
                stats[key] += l
            else:
                stats[key] = l

        # First the succesfully done
        line = "%s (%d jobs):" % (task, njobs)
        for s in order_done:
            if s in jobSummaries:
                line = formatSummaries(opts, line, s, jobSummaries[s])
                del jobSummaries[s]

        # Then the aborted-submitted to the end of the line
        line_end = ""
        for s in order_run:
            if s in jobSummaries:
                line_end = formatSummaries(opts, line_end, s, jobSummaries[s])
                del jobSummaries[s]

        # Then the failed ones to the middle
        keys = jobSummaries.keys()
        keys.sort()
        for key in keys:
            line = formatSummaries(opts, line, key, jobSummaries[key])
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
        for task in taskDirs:
            if task in resubmitJobs:
                print "crab -c %s -resubmit %s" % (task, resubmitJobs[task])
        print
    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    parser.add_option("--status", dest="status", default="all", 
                      help="Provide the resubmit list for these jobs ('all', 'Aborted', comma separated list of exit codes; default 'all'")
    parser.add_option("--showMissing", dest="showMissing", action="store_true", default=False,
                      help="Show also the missing task directories")
    parser.add_option("--showHosts", dest="showHosts", action="store_true", default=False,
                      help="Show summary of hosts where the jobs are running")
    (opts, args) = parser.parse_args()

    opts.status = opts.status.lower()
    if opts.status not in ["all", "aborted"]:
        codes = opts.status.split(",")
        opts.status = [int(c) for c in codes]

    sys.exit(main(opts))
