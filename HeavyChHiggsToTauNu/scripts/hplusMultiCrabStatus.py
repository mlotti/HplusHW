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

status_format = "%-18s %4d"

class JobSummary:
    def __init__(self, jobs, hosts):
        self.jobs = [job.id for job in jobs]
        self.hosts = hosts

def formatSummaries(opts, line, key, summary):
    #sum = " %s %d: %s" % (key, len(summary.jobs), multicrab.prettyJobnums(summary.jobs))
    if opts.showHosts or opts.showJobs:
        line += "\n  "+status_format % (key+":", len(summary.jobs))
        if opts.showJobs and len(summary.jobs) > 0:
            line += ": "+multicrab.prettyJobnums(summary.jobs)
        if opts.showHosts and len(summary.hosts) > 0:
            line += " (%s)" % ", ".join(summary.hosts)
    else:
        line += " %s %d" % (key, len(summary.jobs))+","
    return line

def main(opts):
    taskDirs = multicrab.getTaskDirectories(opts)
    multicrab.checkCrabInPath()

    resubmitJobs = {}
    failedJobs = {}
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
            jobSummaries[key] = JobSummary(item, hosts)
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
        failed = []
        for key, joblist in jobs.iteritems():
            for job in joblist:
                if job.failed(opts.resubmit):
                    failed.append( (job.id, job.jobExitCode) )
        if len(failed) > 0:
            failed.sort()
            pretty = multicrab.prettyJobnums([x[0] for x in failed])
            resubmitJobs[task] = pretty
            for jobId, jobCode in failed:
                multicrab._addToDictList(failedJobs, jobCode, "%s/res/CMSSW_%d.stdout" % (task, jobId))
    
    print "----------------------------------------"
    print "Summary for %d task(s), total %d job(s):" % (len(taskDirs), allJobs)
    for s in order_done:
        if s in stats:
            print status_format % (s+":", stats[s])
            del stats[s]
    b = []
    for s in order_run:
        if s in stats:
            b.append(status_format % (s+":", stats[s]))
            del stats[s]
    keys = stats.keys()
    keys.sort()
    for key in keys:
        print status_format % (key+":", stats[key])
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

    if opts.failedLogs:
        print "----------------------------------------"
        print "Log files of failed jobs"
        keys = failedJobs.keys()
        keys.sort()
        for code in keys:
            print
            print "Job exit code %d:" % code
            print "\n".join(failedJobs[code])

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    multicrab.addOptions(parser)
    parser.add_option("--resubmit", dest="resubmit", default="all", 
                      help="Provide the resubmit list for these jobs ('all', 'aborted', 'done', comma separated list of exit codes; default 'all'")
    parser.add_option("--failedLogs", dest="failedLogs", action="store_true", default=False,
                      help="Show the list of log files of failed jobs")
    parser.add_option("--showMissing", dest="showMissing", action="store_true", default=False,
                      help="Show also the missing task directories")
    parser.add_option("--showHosts", dest="showHosts", action="store_true", default=False,
                      help="Show summary of hosts where the jobs are running")
    parser.add_option("--showJobs", dest="showJobs", action="store_true", default=False,
                      help="Show job numbers for each status type")
    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)

    opts.resubmit = opts.resubmit.lower()
    if opts.resubmit not in ["all", "aborted", "done"]:
        codes = opts.resubmit.split(",")
        opts.resubmit = [int(c) for c in codes]

    sys.exit(main(opts))
