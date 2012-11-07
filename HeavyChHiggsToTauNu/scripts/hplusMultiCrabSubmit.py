#!/usr/bin/env python

import subprocess
import shutil
import time
import sys
import os
import re
from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrabWorkflowsTools as multicrabWorkflowsTools

def isInRange(opts, j):
    if opts.firstJob >= 0 and j.id < opts.firstJob:
        return False
    if opts.lastJob >= 0 and j.id > opts.lastJob:
        return False
    return True

def main(opts):
    taskDirs = multicrab.getTaskDirectories(opts)
    multicrab.checkCrabInPath()

    resubmitMode = (len(opts.resubmit) > 0)
    resubmitIdListMode = (opts.resubmit not in ["failed", "aborted"])

    if resubmitMode and resubmitIdListMode and len(taskDirs) != 1:
        print "Option '--resubmit job_id_list' can be used with only one task, trying to use with %d tasks" % len(taskDirs)
        return 1

    if resubmitMode and resubmitIdListMode:
        resubmitJobList = multicrab.prettyToJobList(opts.resubmit)

    # Obtain all jobs to be (re)submitted
    allJobs = []
    for task in taskDirs:
        if not os.path.exists(task):
            print "%s: Task directory missing" % task
            continue

        jobs = multicrab.crabStatusToJobs(task, printCrab=False)
        if not resubmitMode: # normal submission
            if not "Created" in jobs:
                print "%s: no 'Created' jobs to submit" % task
                continue
            allJobs.extend(filter(lambda j: isInRange(opts, j), jobs["Created"]))
        elif not resubmitIdListMode: # resubmit all failed jobs
            status = "all"
            if opts.resubmit == "aborted":
                status = "aborted"
            for joblist in jobs.itervalues():
                for job in joblist:
                    if job.failed(status):
                        allJobs.append(job)
        else: # resubmit explicit list of jobs
            for joblist in jobs.itervalues():
                for job in joblist:
                    if job.id in resubmitJobList:
                        allJobs.append(job)
                        resubmitJobList.remove(job.id)

    # Set the number of maximum jobs to submit
    maxJobs = len(allJobs)
    if opts.maxJobs >= 0 and int(opts.maxJobs) < int(maxJobs):
        maxJobs = opts.maxJobs

    submitCommand = "-submit"
    if len(opts.resubmit) > 0:
        submitCommand = "-resubmit"

    sites = []
    siteSubmitIndex = 0
    if len(opts.toSites) > 0:
        sites = opts.toSites.split(",")

    # Submission loop
    njobsSubmitted = 0
    while njobsSubmitted < maxJobs:
        # Construct list of jobs per task to submit
        njobsToSubmit = min(opts.jobs, maxJobs-njobsSubmitted, len(allJobs))
        njobsSubmitted += njobsToSubmit    
        jobsToSubmit = {}
        for n in xrange(0, njobsToSubmit):
            job = allJobs.pop(0)
            multicrabWorkflowsTools._addToDictList(jobsToSubmit, job.task, job.id)

        # If explicit list of sites to submit was given, get the site to submit this time
        crabOptions = []
        if len(sites) > 0:
            site = sites[siteSubmitIndex]
            siteSubmitIndex = (siteSubmitIndex+1) % len(sites)
            crabOptions.append("-GRID.se_black_list= -GRID.se_white_list="+site)

        # Actual submission
        for task, jobs in jobsToSubmit.iteritems():
            pretty = multicrab.prettyJobnums(jobs)
            command = ["crab", "-c", task, submitCommand, pretty] + opts.crabArgs.split(" ") + crabOptions
            print "Submitting %d jobs from task %s" % (len(jobs), task)
            print "Command", " ".join(command)
            if not opts.test:
                ret = subprocess.call(command)
                if ret != 0:
                    message = "Command '%s' failed with exit code %d" % (" ".join(command), ret)
                    if opts.allowFails:
                        print message
                    else:
                        raise Exception()

        # Sleep between submissions
        if njobsSubmitted < maxJobs:
            print "Submitted, sleeping %f seconds" % opts.sleep
            time.sleep(opts.sleep)
        else:
            print "Submitted"

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    multicrab.addOptions(parser)
    parser.add_option("--jobs", dest="jobs", type="int", default=50, 
                      help="Number of jobs to submit at a time (default: 50)")
    parser.add_option("--maxJobs", dest="maxJobs", type="int", default=-1,
                      help="Maximum number of jobs to submit (default: -1, i.e. all)")
    parser.add_option("--firstJob", dest="firstJob", type="int", default=-1,
                      help="First job to submit (default: -1, i.e. first which exists)")
    parser.add_option("--lastJob", dest="lastJob", type="int", default=-1,
                      help="Last job to submit (default: -1, i.e. last which exists)")
    parser.add_option("--resubmit", dest="resubmit", type="string", default="",
                      help="Resubmit jobs. Can be list of job IDs, or 'failed'/'aborted' for (all failed)/aborted jobs (conflicts with --firstJob and --lastJob, and with explicit job ID list can be used with only one task).")
    parser.add_option("--sleep", dest="sleep", type="float", default=900.0,
                      help="Number of seconds to sleep between submissions (default: 900 s= 15 min)")
    parser.add_option("--test", dest="test", default=False, action="store_true",
                      help="Test only, do not submit anything")
    parser.add_option("--allowFails", dest="allowFails", default=False, action="store_true",
                      help="Continue submissions even if crab -submit fails for any reason")
    parser.add_option("--crabArgs", dest="crabArgs", default="",
                      help="String of options to pass to CRAB")
    parser.add_option("--toSites", dest="toSites", default="",
                      help="Comma separated list of sites to submit jobs. Jobs are submitted in a round-robin way to these sites. (conflicts with -GRID.(se|ce)_(white|black)_list in --crabArgs)")
    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)

    if len(opts.resubmit) > 0 and (opts.firstJob != -1 or opts.lastJob != -1):
        print "--resubmit conflicts with --firstJob and --lastJob"
        print opts.firstJob, opts.lastJob
        sys.exit(1)

    if len(opts.toSites) > 0:
        tmp = opts.crabArgs.lower()
        if "-grid.se" in tmp or "-grid.ce" in tmp:
            print "--toSites conflicts with '-GRID.(se|ce)_(white|black)_list' in --crabArgs"
            sys.exit(1)

    sys.exit(main(opts))

