#!/usr/bin/env python

import os
import re
import sys
import glob
import gzip

from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import hplusFileSize as fileSize
import hplusMultiCrabStatus as multicrabStatus

class TimeAnalysis:
    def __init__(self):
        self.exe_re = re.compile("ExeTime=(?P<time>\d+)")
        self.user_re = re.compile("CrabUserCpuTime=(?P<time>\d+(\.\d+)?)")
        self.sys_re = re.compile("CrabSysCpuTime=(?P<time>\d+(\.\d+)?)")
        self.stageout_re = re.compile("CrabStageoutTime=(?P<time>\d+(\.\d+)?)")

    def reset(self):
        self.exe_times = []
        self.user_times = []
        self.sys_times = []
        self.stageout_times = []

    def analyse(self, line):
        m = self.exe_re.search(line)
        if m:
            self.exe_times.append(float(m.group("time")))
            return True
        m = self.user_re.search(line)
        if m:
            self.user_times.append(float(m.group("time")))
            return True
        m = self.sys_re.search(line)
        if m:
            self.sys_times.append(float(m.group("time")))
            return True
        m = self.stageout_re.search(line)
        if m:
            self.stageout_times.append(float(m.group("time")))
            return True

        return False

    def _times(self, name, lst):
        if len(lst) > 0:
            return "%s mean %.1f, min %.1f, max %.1f" % (name, sum(lst)/len(lst), min(lst), max(lst))
        else:
            return "%s empty" % name

    def userTime(self):
        return self._times("User", self.user_times)

    def result(self, prefix=""):
        pref = prefix+" "
        ret = pref+"Time analysis:\n"
        pref += " "
        ret += pref+self._times("Exe", self.exe_times) + "\n"
        ret += pref+self.userTime() + "\n"
        ret += pref+self._times("Sys", self.sys_times) + "\n"
        ret += pref+self._times("Stageout", self.stageout_times)
        return ret

class SizeAnalysis:
    def __init__(self, filename):
        self.file_re = re.compile("(?P<size>\d+)\s+\S+\s+\d+\s+\d+:\d+\s+%s$"%filename)
        #self.file_re = re.compile("\d+:\d+\s+%s$"%filename)

    def reset(self):
        self.sizes = []

    def analyse(self, line):
        m = self.file_re.search(line)
        if m:
            self.sizes.append(int(m.group("size")))
            return True

        return False

    def size(self):
        if len(self.sizes) == 0:
            s_mean = 0
        else:
            s_mean = float(sum(self.sizes))/len(self.sizes)
        s_min = float(min(self.sizes))
        s_max = float(max(self.sizes))
        return "Mean %s, min %s, max %s" % (fileSize.pretty(s_mean), fileSize.pretty(s_min), fileSize.pretty(s_max))

    def result(self, prefix=""):
        ret = prefix+"Size analysis:\n"
        ret += prefix+" "+self.size()
        return ret

class HostAnalysis:
    def __init__(self):
        self.host_re = re.compile("Job submitted on host (?P<host>\S+)")

    def reset(self):
        self.hosts = {}

    def analyse(self, line):
        m = self.host_re.search(line)
        if m:
            self.hosts[m.group("host")] = self.hosts.get(m.group("host"), 0)+1
            return True
        return False

    def result(self, prefix=""):
        pref = prefix+" "
        ret = pref+"Host analysis:"
        pref += " "
        keys = self.hosts.keys()
        keys.sort()
        for k in keys:
            ret += "\n%s%s: %d" % (pref, k, self.hosts[k])
        return ret

#                         mon+day     time+timezone       pid
watchdog_re = re.compile("\S+\s+\d+\s+\d+:\d+:\d+\s+\S+\s+\S+\s+(?P<rss>\d+)\s+(?P<vsize>\d+)\s+(?P<disk>\d+)\s+(?P<cpu>\d+)\s+(?P<wall>\d+)")

class WatchdogAnalysis:
    def __init__(self):
        pass

    def reset(self):
        self.rss = []
        self.vsize = []
        self.disk = []
        self.cpu = []
        self.wall = []
        self.prevMatch = None
        self.watchdogOn = False

    def analyse(self, line):
        if "WATCHDOG LOG ENDED" in line:
            def _app(lst, name, div=1024):
                lst.append(float(self.prevMatch.group(name))/div)
            _app(self.rss, "rss")
            _app(self.vsize, "vsize")
            _app(self.disk, "disk", div=1)
            _app(self.cpu, "cpu", div=1)
            _app(self.wall, "wall", div=1)
            self.watchdogOn = False
            return True
        if not self.watchdogOn:
            self.watchdogOn = "LINES OF WATCHDOG LOG" in line
            return False

        m = watchdog_re.search(line)
        if m:
            self.prevMatch = m
        return False

    def _mems(self, name, lst):
        return "%s mean %.1f, min %.1f, max %.1f" % (name, sum(lst)/len(lst), min(lst), max(lst))

    def result(self, prefix=""):
        pref = prefix+" "
        ret = pref+"Watchod resource analysis:"
        pref += " "
        ret += "\n"+pref+self._mems("RSS (MB)", self.rss)
        ret += "\n"+pref+self._mems("VSIZE (MB)", self.vsize)
        ret += "\n"+pref+self._mems("Disk (MB)", self.disk)
        ret += "\n"+pref+self._mems("CPU (s)", self.cpu)
        ret += "\n"+pref+self._mems("Wall (s)", self.wall)
        return ret

class MemoryAnalysis:
    def __init__(self):
        pass

    def reset(self):
        self.rss = []
        self.vsize = []
        self.disk = []

    def analyse(self, line):
        m = watchdog_re.search(line)
        if m:
            def _app(lst, name, div=1024):
                lst.append(float(m.group(name))/div)
            _app(self.rss, "rss")
            _app(self.vsize, "vsize")
            _app(self.disk, "disk", div=1)
            return True
        return False

    def _mems(self, name, lst):
        return "%s mean %.1f, min %.1f, max %.1f" % (name, sum(lst)/len(lst), min(lst), max(lst))

    def result(self, prefix=""):
        pref = prefix+" "
        ret = pref+"Memory analysis (%d jobs):\n" % len(self.rss)
        pref += " "
        ret += pref+self._mems("RSS (MB)", self.rss) + "\n"
        ret += pref+self._mems("VSIZE (MB)", self.vsize) + "\n"
        ret += pref+self._mems("Disk (MB)", self.disk)
        return ret

def analyseFiles(files, analyses, reverse=False, breakWhenFirstFound=False):
    for a in analyses:
        a.reset()

    for name in files:
        if ".gz" in name:
            f = gzip.open(name, "rb")
        else:
            f = open(name)

        if reverse:
            content = f.readlines()
            content.reverse()
        else:
            content = f

        for line in content:
            found = False
            for a in analyses:
                found = a.analyse(line)
                if found:
                    break
            if found and breakWhenFirstFound:
                break
        f.close()

def analyseTask(files, wfiles, analyses, watchdogAnalyses, prefix=""):
    if len(files) == 0:
        return

    if len(analyses) > 0:
        analyseFiles(files, analyses)
    if len(wfiles) > 0:
        analyseFiles(wfiles, watchdogAnalyses, reverse=True, breakWhenFirstFound=True)

    for a in analyses+watchdogAnalyses:
        print a.result(prefix)

def excludeInclude(files, include, exclude=None):
    if exclude is None and include is None:
        return files
    if exclude is not None:
        jobNums = multicrab.prettyToJobList(exclude)
    else:
        jobNums = multicrab.prettyToJobList(include)
    ret = []
    for name in files:
        found = False
        for num in jobNums:
            if "_%d." % num in name:
                found = True
                break
        if ((found and include is not None) or
            (not found and exclude is not None)):
            ret.append(name)
    return ret

def main(opts):
    taskDirs = multicrab.getTaskDirectories(opts)

    analyses = []
    watchdogAnalyses = []
    if opts.time:
        analyses.append(TimeAnalysis())
    if opts.size:
        analyses.append(SizeAnalysis(opts.sizeFile))
    if opts.memory:
        watchdogAnalyses.append(MemoryAnalysis())
    if opts.host:
        analyses.append(HostAnalysis())
    if opts.watchdog:
        analyses.append(WatchdogAnalysis())

    if len(analyses)+len(watchdogAnalyses) == 0:
        return 1

    for task in taskDirs:
        files = glob.glob(os.path.join(task, "res", "CMSSW_*.stdout"))
        files = excludeInclude(files, opts.include, opts.exclude)
        wfiles = []
        if len(watchdogAnalyses) > 0:
            wfiles = glob.glob(os.path.join(task, "res", "Watchdog_*.log.gz"))
            wfiles = excludeInclude(wfiles, opts.include, opts.exclude)

        if opts.byStatus:
            try:
                jobs = multicrab.crabStatusToJobs(task, opts.printCrab)
            except Exception:
                if not opts.allowFails:
                    raise
                print "%s: crab -status failed" % task
                continue
            print "Task %s" % task
            # Ignore running jobs
            for status in multicrabStatus.order_run:
                if status in jobs:
                    del jobs[status]
            stats = jobs.keys()
            stats.sort()
            for status in stats:
                ids = ",".join(["%d"%j.id for j in jobs[status]])
                f = excludeInclude(files, ids)
                wf = excludeInclude(wfiles, ids)
                print " %s, %d jobs" % (status, len(files))
                analyseTask(f, wf, analyses, watchdogAnalyses, prefix=" ")
        else:
            print "Task %s, %d jobs" % (task, len(files))
            analyseTask(files, wfiles, analyses, watchdogAnalyses)

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] [crab task dirs]\n\nCRAB task directories can be given either as the last arguments, or with -d.")
    parser.add_option("--time", dest="time", action="store_true", default=False,
                      help="Analyse real and CPU time")
    parser.add_option("--size", dest="size", action="store_true", default=False,
                      help="Analyse output file size (see also --sizeFile)")
    parser.add_option("--sizeFile", dest="sizeFile", default="pattuple.root",
                      help="For --size, specify the output file name (default: 'pattuple.root')")
    parser.add_option("--memory", dest="memory", action="store_true", default=False,
                      help="Analyse memory usage")
    parser.add_option("--host", dest="host", action="store_true", default=False,
                      help="Analyse host names where jobs were run")
    parser.add_option("--watchdog", dest="watchdog", action="store_true", default=False,
                      help="Analyse resource usage from watchdog output (from CMSSW.stdout)")
    parser.add_option("--exclude", dest="exclude", type="string", default=None,
                      help="Exclude these jobs from the analysis (clashes with --include)")
    parser.add_option("--include", dest="include", type="string", default=None,
                      help="Include only these jobs from the analysis (clashes with --exclude)")
    parser.add_option("--byStatus", dest="byStatus", action="store_true", default=False,
                      help="Show results by status type")
    parser.add_option("--printCrab", dest="printCrab", action="store_true", default=False,
                      help="Print CRAB output (relevant for --byStatus)")
    parser.add_option("--allowFails", dest="allowFails", default=False, action="store_true",
                      help="Continue submissions even if crab -status fails for any reason (relevant for --byStatus)")
    multicrab.addOptions(parser)
    (opts, args) = parser.parse_args()
    if opts.exclude is not None and opts.include is not None:
        parser.error("You may not specify both --exclude and --include")
    if (opts.exclude is not None or opts.include is not None) and opts.byStatus:
        parser.error("--byStatus conflicts with --exclude and --include")
    opts.dirs.extend(args)

    sys.exit(main(opts))
