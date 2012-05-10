#!/usr/bin/env python

import sys
import subprocess

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

def main():
    args = sys.argv[1:]

    # Merge the LandS root files
    print "Merging job ROOT files"
    command = ["hplusMergeHistograms.py", "-i", "split\S+_limits_tree\S*\.root"]+args
    ret = subprocess.call(command)
    if ret != 0:
        raise Exception("hplusMergeHistograms failed with exit code %d, command was\n%s" %(ret, " ".join(command)))

    # Run LandS to do obtain the results
    print "Running LandS for merged expected results"
    result = lands.ParseLandsOutput(".")
    result.print2()
    result.saveJson()

    return 0


if __name__ == "__main__":
    sys.exit(main())
