#!/usr/bin/env python

import subprocess
import shutil
import StringIO
import time
import sys
import os
import re
from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

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

    if opts.byHost:
        global status_format
        status_format = status_format.replace("18s", "40s")

    if opts.save:
        out = open(opts.saveFile, "w")

    for task in taskDirs:
        if not os.path.exists(task):
            if opts.showMissing:
                print >>sys.stderr, "%s: Task directory missing" % task
            continue

        try:
            jobs = multicrab.crabStatusToJobs(task, opts.printCrab)
        except Exception:
            if not opts.allowFails:
                raise
            print "%s: crab -status failed" % task
            continue

        jobSummaries = {}
        njobs = 0
        for key, item in jobs.iteritems():
            hosts = {}
            for job in item:
                if job.host != None:
                    aux.addToDictList(hosts, job.host, job)
            if opts.byHost:
                for host, joblist in hosts.iteritems():
                    jobSummaries[key+" "+host] = JobSummary(joblist, [host])
            else:
                jobSummaries[key] = JobSummary(item, hosts)
            l = len(item)
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

        if opts.save:
            out.write(line)
            out.write("\n")
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
                aux.addToDictList(failedJobs, jobCode, "%s/res/CMSSW_%d.stdout" % (task, jobId))

    summary = StringIO.StringIO()
    
    summary.write("----------------------------------------\n")
    print "Summary for %d task(s), total %d job(s):" % (len(taskDirs), allJobs)
    for s in order_done:
        if s in stats:
            summary.write(status_format % (s+":", stats[s]))
            summary.write("\n")
            del stats[s]
    b = []
    for s in order_run:
        if s in stats:
            b.append(status_format % (s+":", stats[s]))
            del stats[s]
    keys = stats.keys()
    keys.sort()
    for key in keys:
        summary.write(status_format % (key+":", stats[key]))
        summary.write("\n")
    for line in b:
        summary.write(line)
        summary.write("\n")


    summary.write("----------------------------------------\n")
    if len(resubmitJobs) == 0:
        summary.write("No failed/aborted jobs to resubmit\n")
    else:
        summary.write("Following jobs failed/aborted, and can be resubmitted\n\n")
        for task in taskDirs:
            if task in resubmitJobs:
                summary.write("crab -c %s -resubmit %s\n" % (task, resubmitJobs[task]))
        summary.write("\n")

    if opts.failedLogs:
        summary.write("----------------------------------------\n")
        summary.write("Log files of failed jobs\n")
        keys = failedJobs.keys()
        keys.sort()
        for code in keys:
            summary.write("\nJob exit code %d:\n" % code)
            summary.write("\n".join(failedJobs[code]))
            summary.write("\n")

    if opts.save:
        out.write(summary.getvalue())
        out.close()
    print summary.getvalue()

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
    parser.add_option("-l", "--long", dest="long", action="store_true", default=False,
                      help="Shorthand for '--showJobs --showHosts")
    parser.add_option("--byHost", dest="byHost", action="store_true", default=False,
                      help="With --showHosts/-l, categorize jobs by host also")
    parser.add_option("--save", dest="save", action="store_true", default=False,
                      help="Save the output to a file, specified by --saveFile") 
    parser.add_option("--saveFile", dest="saveFile", default="status.txt",
                      help="File where the output is saved with --save (default: 'status.txt')")
    parser.add_option("--printCrab", dest="printCrab", action="store_true", default=False,
                      help="Print CRAB output")
    parser.add_option("--allowFails", dest="allowFails", default=False, action="store_true",
                      help="Continue submissions even if crab -status fails for any reason")
    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)

    opts.resubmit = opts.resubmit.lower()
    if opts.resubmit not in ["all", "aborted", "done"]:
        codes = opts.resubmit.split(",")
        opts.resubmit = [int(c) for c in codes]

    if opts.long:
        opts.showHosts = True
        opts.showJobs = True

    sys.exit(main(opts))
