#!/usr/bin/env python

import sys
import json
import subprocess

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

def main():
    args = sys.argv[1:]

    # Merge the LandS root files
    print "Merging job ROOT files"
    f = open("configuration.json")
    config = json.load(f)
    f.close()
    if config["clsType"] == "LEP":
        command = ["hplusMergeHistograms.py", "-i", "split\S+_limits_tree\S*\.root"]+args
    elif config["clsType"] == "LHC":
        command = ["hplusMergeHistograms.py", "-i", "split\S+_m2lnQ\S*\.root"]+args
    else:
        raise Exception("Unsupported clsType '%s' in configuration.json" % config["clsType"])
    if not "--skipMerge" in args:
        ret = subprocess.call(command)
        if ret != 0:
            raise Exception("hplusMergeHistograms failed with exit code %d, command was\n%s" %(ret, " ".join(command)))

    if "-h" in args or "--help" in args:
        return 0

    # Run LandS to do obtain the results
    print "Running LandS for merged expected results"
    result = lands.ParseLandsOutput(".")
    result.print2()
    result.saveJson()

    return 0

if __name__ == "__main__":
    sys.exit(main())
