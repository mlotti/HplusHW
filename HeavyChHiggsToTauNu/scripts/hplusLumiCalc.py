#!/usr/bin/env python

import os
import re
import sys
import glob
import subprocess
import json
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

# lumiCalc.py usage taken from
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/LumiCalc

def isMCTask(taskdir):
    path = os.path.join(taskdir, "share", "crab.cfg")
    if not os.path.exists(path):
        print "crab.cfg at %s doesn't exist, assuming task is MC" % path
        return True

    f = open(path)
    mc = False
    for line in f:
        if "pycfg_params" in line:
            if "crossSection" in line:
                mc = True
            break
    f.close()
    return mc

def main(opts, args):
    if opts.report:
        multicrab.checkCrabInPath()

    crabdirs = multicrab.getTaskDirectories(opts)

    cell = "\|\s+(?P<%s>\S+)\s+"

    lumi_re = re.compile((cell % "deliveredls")+
                         (cell % "delivered")+
                         (cell % "selectedls")+
                         (cell % "recorded")+"\|")
    #lumi_re = re.compile("\|\s(?P<recorded>\S+)\s")

    data = {}
    if not opts.truncate and os.path.exists(opts.output):
        f = open(opts.output, "r")
        data = json.load(f)
        f.close()
    
    for d in crabdirs:
        if isMCTask(d):
            print "  Ignoring task directory '%s', it looks like MC" % d
            continue

        if opts.report:
            cmd = ["crab", "-report", "-c", d]
            if opts.verbose:
                print " ".join(cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = p.communicate()[0]
            ret = p.returncode
            if ret != 0:
                print "Call to 'crab -report -d %s' failed with return value %d" % (d, ret)
                print output
                return 1
            if opts.verbose:
                print output
    
        jsonfile = os.path.join(d, "res", "lumiSummary.json")
        #print
        #print "================================================================================"
        #print "Dataset %s:" % d
        cmd = ["lumiCalc.py", "-i", jsonfile, "--with-correction", "--nowarning", "overview", "-b", "stable"]
        #cmd = ["lumiCalc2.py", "-i", jsonfile, "--nowarning", "overview", "-b", "stable"]
        #cmd = ["lumiCalc.py", "-c", "frontier://LumiCalc/CMS_LUMI_PROD", "-r", "132440", "--nowarning", "overview"]
        #ret = subprocess.call(cmd)
        if opts.verbose:
            print " ".join(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.communicate()[0]
        ret = p.returncode
        if ret != 0:
            print "Call to lumiCalc.py failed with return value %d with command" % ret
            print " ".join(cmd)
            print output
            return 1
        if opts.verbose:
            print output

        lines = output.split("\n")
        lines.reverse()
        lumi = -1.0
        for line in lines:
            m = lumi_re.search(line)
            if m:
                lumi = float(m.group("recorded"))/1e6 # ub^-1 -> pb^-1, lumiCalc.py returns ub^-1
                #lumi = float(m.group("recorded")) # lumiCalc2.py returns pb^-1
                break

        print "Task %s recorded luminosity %f pb^-1" % (d, lumi)
        data[d] = lumi

        # Save the json file after each data task in case of future errors
        f = open(opts.output, "wb")
        json.dump(data, f, sort_keys=True, indent=2)
        f.close()

    f = open(opts.output, "wb")
    json.dump(data, f, sort_keys=True, indent=2)
    f.close()

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    parser.add_option("--output", "-o", dest="output", type="string", default="lumi.json",
                      help="Output file to write the dataset integrated luminosities")
    parser.add_option("--truncate", dest="truncate", default=False, action="store_true",
                      help="Truncate the output file before writing")
    parser.add_option("--noreport", dest="report", action="store_false", default=True,
                      help="Do not run 'crab -report', i.e. you guarantee that the lumiSummary.json contains already all jobs.")
    parser.add_option("--verbose", dest="verbose", action="store_true", default=False,
                      help="Print outputs of the commands which are executed")
    
    (opts, args) = parser.parse_args()

    sys.exit(main(opts, args))
