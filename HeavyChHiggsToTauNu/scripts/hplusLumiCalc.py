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

# Convert luminosity to pb^-1
def convertLumi(lumi, unit):
    if unit == "ub":
        return lumi/1e6
    elif unit == "nb":
        return lumi/1e3
    elif unit == "pb":
        return lumi
    elif unit == "fb":
        return lumi*1e3
    else:
        raise Exception("Unsupported luminosity unit %s"%unit)

def main(opts, args):
    if opts.report:
        multicrab.checkCrabInPath()

    cell = "\|\s+(?P<%s>\S+)\s+"

    lumi_re = re.compile((cell % "deliveredls")+
                         (cell % "delivered")+
                         (cell % "selectedls")+
                         (cell % "recorded")+"\|")
    #lumi_re = re.compile("\|\s(?P<recorded>\S+)\s")
    unit_re = re.compile("Recorded\(/(?P<unit>.*)\)")

    if not opts.truncate and os.path.exists(opts.output):
        f = open(opts.output, "r")
        data = json.load(f)
        f.close()
    
    files = []
    # only if no explicit files, or some directories explicitly given
    if len(opts.files) == 0 or len(opts.dirs) > 0:
        crabdirs = multicrab.getTaskDirectories(opts)
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
        
            files.append((d, os.path.join(d, "res", "lumiSummary.json")))
    files.extend([(None, f) for f in opts.files])
    
    data = {}
    for task, jsonfile in files:
        #print
        #print "================================================================================"
        #print "Dataset %s:" % d
        if opts.lumicalc == "lumiCalc1":
            cmd = ["lumiCalc.py", "-i", jsonfile, "--with-correction", "--nowarning", "overview", "-b", "stable"]
        if opts.lumicalc == "lumiCalc2":
            cmd = ["lumiCalc2.py", "-i", jsonfile, "--nowarning", "overview", "-b", "stable"]
        if opts.lumicalc == "pixelLumiCalc":
            cmd = ["pixelLumiCalc.py", "-i", jsonfile, "--nowarning", "overview"]
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
        unit = None
        for line in lines:
            m = unit_re.search(line)
            if m:
                unit = m.group("unit")
                break

            m = lumi_re.search(line)
            if m:
                lumi = float(m.group("recorded")) # lumiCalc2.py returns pb^-1
#                if opts.lumicalc1:
#                    lumi = lumi/1e6 # ub^-1 -> pb^-1, lumiCalc.py returns ub^-1
                continue

        if unit == None:
            raise Exception("Didn't find unit information from lumiCalc output, command was %s" % " ".join(cmd))
        lumi = convertLumi(lumi, unit)

        if task == None:
            print "File %s recorded luminosity %f pb^-1" % (jsonfile, lumi)
        else:
            print "Task %s recorded luminosity %f pb^-1" % (task, lumi)
            data[task] = lumi

        # Save the json file after each data task in case of future errors
        if len(data) > 0:
            f = open(opts.output, "wb")
            json.dump(data, f, sort_keys=True, indent=2)
            f.close()

    if len(data) > 0:
        f = open(opts.output, "wb")
        json.dump(data, f, sort_keys=True, indent=2)
        f.close()

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    multicrab.addOptions(parser)
    parser.add_option("-f", dest="files", type="string", action="append", default=[],
                      help="JSON files to calculate the luminosity for (this or -d is required)")
    parser.add_option("--output", "-o", dest="output", type="string", default="lumi.json",
                      help="Output file to write the dataset integrated luminosities")
    parser.add_option("--truncate", dest="truncate", default=False, action="store_true",
                      help="Truncate the output file before writing")
    parser.add_option("--noreport", dest="report", action="store_false", default=True,
                      help="Do not run 'crab -report', i.e. you guarantee that the lumiSummary.json contains already all jobs.")
    parser.add_option("--verbose", dest="verbose", action="store_true", default=False,
                      help="Print outputs of the commands which are executed")
    parser.add_option("--lumiCalc1", dest="lumicalc", action="store_const", const="lumiCalc1",
                      help="Use lumiCalc.py instead of lumiCalc2.py (default is to use pixelLumiCalc.py")
    parser.add_option("--lumiCalc2", dest="lumicalc", action="store_const", const="lumiCalc2",
                      help="Use lumiCalc2.py (default is to use pixelLumiCalc.py)")
    parser.add_option("--pixelLumiCalc", dest="lumicalc", action="store_const", const="pixelLumiCalc",
                      help="Use pixelLumiCalc.py instead of lumiCalc2.py (default)")
    
    (opts, args) = parser.parse_args()
    if opts.lumicalc == None:
        opts.lumicalc = "pixelLumiCalc"
    print "Calculating luminosity with %s" % opts.lumicalc

    sys.exit(main(opts, args))
