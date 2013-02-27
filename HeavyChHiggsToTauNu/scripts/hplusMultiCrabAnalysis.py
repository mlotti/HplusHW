#!/usr/bin/env python

import os
import re
import sys
import glob

from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import hplusFileSize as fileSize

class TimeAnalysis:
    def __init__(self):
        self.exe_re = re.compile("ExeTime=(?P<time>\d+)")
        self.user_re = re.compile("CrabUserCpuTime=(?P<time>\d+(\.\d+)?)")
        self.sys_re = re.compile("CrabSysCpuTime=(?P<time>\d+(\.\d+)?)")

    def reset(self):
        self.exe_times = []
        self.user_times = []
        self.sys_times = []

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

        return False

    def _times(self, name, lst):
        return "%s mean %.1f, min %.1f, max %.1f" % (name, sum(lst)/len(lst), min(lst), max(lst))

    def userTime(self):
        return self._times("User", self.user_times)

    def result(self):
        ret = " Time analysis:\n"
        ret += "  "+self._times("Exe", self.exe_times) + "\n"
        ret += "  "+self.userTime() + "\n"
        ret += "  "+self._times("Sys", self.sys_times)
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
        s_mean = float(sum(self.sizes))/len(self.sizes)
        s_min = float(min(self.sizes))
        s_max = float(max(self.sizes))
        return "Mean %s, min %s, max %s" % (fileSize.pretty(s_mean), fileSize.pretty(s_min), fileSize.pretty(s_max))

    def result(self):
        ret = " Size analysis:\n"
        ret += "  "+self.size()
        return ret

def analyseFiles(files, analyses):
    for a in analyses:
        a.reset()

    for name in files:
        f = open(name)
        for line in f:
            found = False
            for a in analyses:
                found = a.analyse(line)
                if found:
                    break
            if found:
                continue
        f.close()


def main(opts):
    taskDirs = multicrab.getTaskDirectories(opts)

    analyses = []
    if opts.time:
        analyses.append(TimeAnalysis())
    if opts.size:
        analyses.append(SizeAnalysis(opts.sizeFile))

    if len(analyses) == 0:
        return 1

    for task in taskDirs:
        files = glob.glob(os.path.join(task, "res", "CMSSW_*.stdout"))

        if len(files) == 0:
            continue

        analyseFiles(files, analyses)

        print "Task %s, %d jobs" % (task, len(files))
        for a in analyses:
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
    multicrab.addOptions(parser)
    (opts, args) = parser.parse_args()
    opts.dirs.extend(args)

    sys.exit(main(opts))
