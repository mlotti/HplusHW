#!/usr/bin/env python

import os
import sys
import math
import subprocess
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def main(opts):
    taskDirs = multicrab.getTaskDirectories(opts)
    multicrab.checkCrabInPath()

    for task in taskDirs:
        if not os.path.exists(task):
            print "%s: Task directory missing" % task
            continue

        jobsList = []
        if opts.getoutput is None:
            jobs = multicrab.crabStatusToJobs(task, printCrab=False)
            for key in jobs.keys():
                if "Done" in key:
                    jobsList.extend([j.id for j in jobs[key]])
        else:
            jobsList.extend(multicrab.prettyToJobList(opts.getoutput))
        if len(jobsList) == 0:
            print "%s: no jobs to retrieve" % task
            continue

        # Getoutput loop
        maxJobs = len(jobsList)
        if opts.jobs > 0:
            maxJobs = opts.jobs

        for i in xrange(0, int(math.ceil(float(len(jobsList))/maxJobs))):
            jobsToGet = jobsList[i*maxJobs:(i+1)*maxJobs]
            jobsStr = ",".join([str(j) for j in jobsToGet])
            command = ["crab", "-c", task, "-getoutput", jobsStr]
            print "Getting %d jobs from task %s" % (len(jobsToGet), task)
            print "Command", " ".join(command)
            ret = subprocess.call(command)
            if ret != 0:
                print "Command '%s' failed with exit code %s" % (" ".join(command), ret)
                if not opts.allowFails:
                    return 1

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    multicrab.addOptions(parser)
    parser.add_option("--jobs", dest="jobs", type="int", default=-1,
                      help="Number of jobs whose output is retrieved in one crab call (default: -1, retrieve all)")
    parser.add_option("--getoutput", dest="getoutput", type="string", default=None,
                      help="Get the output of these jobs only (default is to get output of all jobs). This also prevents the call to 'crab -status'.")
    parser.add_option("--allowFails", dest="allowFails", default=False, action="store_true",
                      help="Continue getoutput even if crab -getoutput fails for any reason")

    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)

    sys.exit(main(opts))
