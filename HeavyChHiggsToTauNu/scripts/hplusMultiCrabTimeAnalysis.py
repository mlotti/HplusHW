#!/usr/bin/env python

import os
import re
import sys
import glob

from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab


def times(name, lst):
    return "  %s mean %.1f, min %.1f, max %.1f" % (name, sum(lst)/len(lst), min(lst), max(lst))

def main(opts):
    taskDirs = multicrab.getTaskDirectories(opts)

    exe_re = re.compile("ExeTime=(?P<time>\d+)")
    user_re = re.compile("CrabUserCpuTime=(?P<time>\d+(\.\d+)?)")
    sys_re = re.compile("CrabSysCpuTime=(?P<time>\d+(\.\d+)?)")

    for task in taskDirs:
        files = glob.glob(os.path.join(task, "res", "CMSSW_*.stdout"))

        if len(files) == 0:
            continue

        exe_times = []
        user_times = []
        sys_times = []
        for name in files:
            f = open(name)
            for line in f:
                m = exe_re.search(line)
                if m:
                    exe_times.append(float(m.group("time")))
                    continue
                m = user_re.search(line)
                if m:
                    user_times.append(float(m.group("time")))
                    continue
                m = sys_re.search(line)
                if m:
                    sys_times.append(float(m.group("time")))
            f.close()
        print "Task", task
        print times("Exe", exe_times)
        print times("User", user_times)
        print times("Sys", sys_times)


if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    (opts, args) = parser.parse_args()

    sys.exit(main(opts))
