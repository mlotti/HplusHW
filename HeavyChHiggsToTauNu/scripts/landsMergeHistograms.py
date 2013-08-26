#!/usr/bin/env python

import os
import sys
import json
import subprocess
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux

def main(opts, args):
    # Merge the LandS root files
    f = open("configuration.json")
    config = json.load(f)
    f.close()

    # forward parameters
    if opts.delete:
        args.append("--delete")
    if len(opts.filter) > 0:
        args.extend(["--filter", opts.filter])
    for d in opts.dirs:
        args.extend(["-d", d])

    if config["clsType"] == "LEP":
        command = ["hplusMergeHistograms.py", "-i", "split\S+_limits_tree\S*\.root"]+args
    elif config["clsType"] == "LHC":
        command = ["hplusMergeHistograms.py", "-i", "split\S+_m2lnQ\S*\.root"]+args
    else:
        raise Exception("Unsupported clsType '%s' in configuration.json" % config["clsType"])
    if not opts.skipMerge:
        print "Merging job ROOT files"
        ret = subprocess.call(command)
        if ret != 0:
            raise Exception("hplusMergeHistograms failed with exit code %d, command was\n%s" %(ret, " ".join(command)))

    # Run LandS to do obtain the results
    print "Running LandS for merged expected results"
    result = lands.ParseLandsOutput(".", opts.unblinded)
    #result.print2(opts.unblinded)
    result.saveJson()

    # Plot the BR limit
    limitArgs = ""
    if opts.unblinded:
        limitArgs += " --unblinded"
    script = os.path.join(aux.higgsAnalysisPath(), "HeavyChHiggsToTauNu", "test", "brlimit", "plotBRLimit.py")
    ret = subprocess.call([script,limitArgs])
    if ret != 0:
        raise Exception("plotBRLimit.py failed with exit code %d, command was\n%s" % (ret, script))

    # Final printout
    print "The BR limits (above) are saved in limits.json file, and to limitsBr.* plot."
    print "Before trusting the results, plase check"
    print " - limitsBrRelativeUncertainty.* plot to see if you have enough MC toy experiments"
    print "   (the relative toy MC statistical uncertainty should be less than ~2-3 %, according to Mingshui)"
    print " - plot_m*.gif plots to see if the BR range covers all limits"
    print "   (the CLs=0.05 should be interpolated, not extrapolated)"
    print "For more information, please see https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsChToTauNuFullyHadronicLimits"

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] -- [options to hplusMergeHistograms]")
    multicrab.addOptions(parser)
    parser.add_option("--skipMerge", dest="skipMerge", default=False, action="store_true",
                      help="Don't run hplusMergeHistograms (i.e. run only LandS for the merged output)")
    parser.add_option("--delete", dest="delete", default=False, action="store_true",
                      help="Delete the source files to save disk space (default is to keep the files)")
    parser.add_option("--unblinded", dest="unblinded", default=False, action="store_true",
                      help="Draw observation to limit plots")

    (opts, args) = parser.parse_args()

    sys.exit(main(opts, args))
