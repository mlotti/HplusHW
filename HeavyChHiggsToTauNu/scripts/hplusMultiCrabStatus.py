#!/usr/bin/env python

import subprocess
import shutil
import time
import sys
import os
import re
from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

status_re = re.compile("(?P<id>\d+)\s+(?P<end>\S)\s+(?P<status>\S+\s+(\(.*?\))?)\s+(?P<action>\S+)\s+(?P<execode>\S+)?\s+(?P<jobcode>\S+)?\s+(?P<host>\S+)?")

order_done = ["Retrieved", "Done"]
order_run = ["Running", "Scheduled", "Ready", "Submitted", "Created"]

def intIfNotNone(n):
    if n == None:
        return n
    return int(n)

class CrabJob:
    def __init__(self, task, match):
        self.task = task
        self.id = int(match.group("id"))
        self.end = match.group("end")
        self.status = match.group("status")
        self.origStatus = self.status[:]
        self.action = match.group("action")
        self.exeExitCode = intIfNotNone(match.group("execode"))
        self.jobExitCode = intIfNotNone(match.group("jobcode"))
        self.host = match.group("host")

        # Let's not care the difference of 'Done (success)' and 'Done
        # (failed)' at this level
        if "Done" in self.status:
            self.status = "Done"

        failed = True
        if self.jobExitCode != None and self.jobExitCode != 0:
            self.status += " (%d)" % self.jobExitCode
        elif self.exeExitCode != None and self.exeExitCode != 0:
            self.status += " (exe %d)" % self.jobExitCode

    def stdoutFile(self):
        return os.path.join(self.task, "res", "CMSSW_%d.stdout"%self.id)

    def failed(self, filter):
        if (filter == "all" or filter == "aborted") and self.origStatus == "Aborted":
            return True
        if self.origStatus != "Retrieved":
            return False
        if self.exeExitCode == 0 and self.jobExitCode == 0:
            return False

        if filter == "all":
            return True
        if filter == "aborted":
            return False
        if self.jobExitCode in filter:
            return True
        return False

def statusOutput(task):
    command = ["crab", "-status", "-c", task]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    if p.returncode != 0:
        raise Exception("Command '%s' failed with exit code %d, output:\n%s" % (" ".join(command), p.returncode, output))
    return output

def addToDictList(d, name, item):
    if name in d:
        d[name].append(item)
    else:
        d[name] = [item]

def outputToJobs(task, output):
    jobs = {}
    for line in output.split("\n"):
        m = status_re.search(line)
        if m:
            job = CrabJob(task, m)
            addToDictList(jobs, job.status, job)
    return jobs

def main(opts):
    taskDirs = multicrab.getTaskDirectories(opts)
    multicrab.checkCrabInPath()

    resubmitJobs = {}
    stats = {}
    allJobs = 0

    for task in taskDirs:
        if not os.path.exists(task):
            print "%s: Task directory missing" % task
            continue
        
        output = statusOutput(task)
        jobs = outputToJobs(task, output)

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
                if job.failed(opts.filter):
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
    parser.add_option("--filter", dest="filter", default="all", 
                      help="Provide the resubmit list for these jobs ('all', 'Aborted', comma separated list of exit codes; default 'all'")
    (opts, args) = parser.parse_args()

    opts.filter = opts.filter.lower()
    if opts.filter not in ["all", "aborted"]:
        codes = opts.filter.split(",")
        opts.filter = [int(c) for c in codes]

    sys.exit(main(opts))
