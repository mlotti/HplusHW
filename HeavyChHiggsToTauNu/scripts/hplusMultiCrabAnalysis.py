#!/usr/bin/env python

import os
import re
import sys
import glob
import gzip

from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import hplusFileSize as fileSize

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
        return "%s mean %.1f, min %.1f, max %.1f" % (name, sum(lst)/len(lst), min(lst), max(lst))

    def userTime(self):
        return self._times("User", self.user_times)

    def result(self):
        ret = " Time analysis:\n"
        ret += "  "+self._times("Exe", self.exe_times) + "\n"
        ret += "  "+self.userTime() + "\n"
        ret += "  "+self._times("Sys", self.sys_times) + "\n"
        ret += "  "+self._times("Stageout", self.stageout_times)
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

    def result(self):
        ret = " Size analysis:\n"
        ret += "  "+self.size()
        return ret

class MemoryAnalysis:
    def __init__(self):
        #                         mon+day     time+timezone       pid
        self.mem_re = re.compile("\S+\s+\d+\s+\d+:\d+:\d+\s+\S+\s+\S+\s+(?P<rss>\d+)\s+(?P<vsize>\d+)\s+(?P<disk>\d+)")

    def reset(self):
        self.rss = []
        self.vsize = []
        self.disk = []

    def analyse(self, line):
        m = self.mem_re.search(line)
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

    def result(self):
        ret = " Memory analysis (%d jobs):\n" % len(self.rss)
        ret += "  "+self._mems("RSS (MB)", self.rss) + "\n"
        ret += "  "+self._mems("VSIZE (MB)", self.vsize) + "\n"
        ret += "  "+self._mems("Disk (MB)", self.disk)
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

    if len(analyses)+len(watchdogAnalyses) == 0:
        return 1

    def excludeInclude(files):
        if opts.exclude is None and opts.include is None:
            return files
        if opts.exclude is not None:
            jobNums = multicrab.prettyToJobList(opts.exclude)
        else:
            jobNums = multicrab.prettyToJobList(opts.include)
        ret = []
        for name in files:
            found = False
            for num in jobNums:
                if "_%d." % num in name:
                    found = True
                    break
            if ((found and opts.include is not None) or
                (not found and opts.exclude is not None)):
                ret.append(name)
        return ret

    for task in taskDirs:
        files = glob.glob(os.path.join(task, "res", "CMSSW_*.stdout"))
        files = excludeInclude(files)

        if len(files) == 0:
            continue

        if len(analyses) > 0:
            analyseFiles(files, analyses)
        if len(watchdogAnalyses) > 0:
            wfiles = glob.glob(os.path.join(task, "res", "Watchdog_*.log.gz"))
            wfiles = excludeInclude(wfiles)
            if len(wfiles) > 0:
                analyseFiles(wfiles, watchdogAnalyses, reverse=True, breakWhenFirstFound=True)

        print "Task %s, %d jobs" % (task, len(files))
        for a in analyses+watchdogAnalyses:
            print a.result()

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
    parser.add_option("--exclude", dest="exclude", type="string", default=None,
                      help="Exclude these jobs from the analysis (clashes with --include)")
    parser.add_option("--include", dest="include", type="string", default=None,
                      help="Include only these jobs from the analysis (clashes with --exclude)")
    multicrab.addOptions(parser)
    (opts, args) = parser.parse_args()
    if opts.exclude is not None and opts.include is not None:
        parser.error("You may not specify both --exclude and --include")
    opts.dirs.extend(args)

    sys.exit(main(opts))
