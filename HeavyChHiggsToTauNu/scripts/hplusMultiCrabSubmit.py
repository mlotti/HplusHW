#!/usr/bin/env python

import subprocess
import shutil
import time
import sys
import os
import re
from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def main(opts):
    taskDirs = multicrab.getTaskDirectories(opts)
    multicrab.checkCrabInPath()

    allJobs = []
    for task in taskDirs:
        if not os.path.exists(task):
            print "%s: Task directory missing" % task
            continue

        jobs = multicrab.crabStatusToJobs(task)
        if not "Created" in jobs:
            print "%s: no 'Created' jobs to submit" % task
            continue
        allJobs.extend(jobs["Created"])

    maxJobs = len(allJobs)
    if opts.maxJobs >= 0 and int(opts.maxJobs) < int(maxJobs):
        maxJobs = opts.maxJobs

    njobsSubmitted = 0
    while njobsSubmitted < maxJobs:
        njobsToSubmit = min(opts.jobs, maxJobs-njobsSubmitted, len(allJobs))
        njobsSubmitted += njobsToSubmit    
        jobsToSubmit = {}
        for n in xrange(0, njobsToSubmit):
            job = allJobs.pop(0)
            multicrab._addToDictList(jobsToSubmit, job.task, job.id)

        for task, jobs in jobsToSubmit.iteritems():
            pretty = multicrab.prettyJobnums(jobs)
            command = ["crab", "-c", task, "-submit", pretty]
            print "Submitting %d jobs from task %s" % (len(jobs), task)
            print "Command", " ".join(command)
            if not opts.test:
                ret = subprocess.call(command)
                if ret != 0:
                    raise Exception("Command '%s' failed with exit code %d" % (" ".join(command), ret))
        if njobsSumitted < maxJobs:
            print "Submitted, sleeping %f seconds" % opts.sleep
            time.sleep(opts.sleep)
        else:
            print "Submitted"

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    parser.add_option("--jobs", dest="jobs", type="int", default=50, 
                      help="Number of jobs to submit at a time (default: 50)")
    parser.add_option("--maxJobs", dest="maxJobs", type="int", default=-1,
                      help="Maximum number of jobs to submit (default: -1, i.e. all)")
    parser.add_option("--sleep", dest="sleep", type="float", default=900.0,
                      help="Number of seconds to sleep between submissions (default: 900 s= 15 min)")
    parser.add_option("--test", dest="test", default=False, action="store_true",
                      help="Test only, do not submit anything")
    (opts, args) = parser.parse_args()

    sys.exit(main(opts))

