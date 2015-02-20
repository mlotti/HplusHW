#!/usr/bin/env python

import os, re
import sys
import glob
import json
import array
import shutil
import subprocess
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

def main():
    f = open("configuration.json")
    config = json.load(f)
    f.close()

    masspoints = config["masspoints"]

    probs = array.array("d", [0.5, 0.84, 0.16, 0.975, 0.025])
    quants = array.array("d", [0, 0, 0, 0, 0])

    result = {}

    for mass in masspoints:
        f = ROOT.TFile.Open("Injected_m{MASS}/res/histograms-Injected_m{MASS}.root".format(MASS=mass))
#        f.ls()
        tree = f.Get("limit")
#        print tree
        th = ROOT.TH1F("tmp", "tmp", 2000, 0, 0.2)
        tree.Draw("limit >>tmp", "quantileExpected==-1", "goff")

        th.GetQuantiles(5, quants, probs)

        f.Close()

        result[mass] = {
            "expected": {
                "median": "%.6f" % quants[0],
                "+1sigma": "%.6f" % quants[1],
                "-1sigma": "%.6f" % quants[2],
                "+2sigma": "%.6f" % quants[3],
                "-2sigma": "%.6f" % quants[4]
            },
            "mass": mass,
            "observed": "0"
        }

    f = open("limits.json")
    content = json.load(f)
    f.close()

    content["masspoints"] = result

    f = open("limits.json", "w")
    json.dump(content, f, sort_keys=True, indent=2)
    f.close()        


if __name__ == "__main__":
#    parser = OptionParser(usage="Usage: %prog [options]")
#    (opts, args) = parser.parse_args()
#    sys.exit(main(opts, args))
    sys.exit(main())
