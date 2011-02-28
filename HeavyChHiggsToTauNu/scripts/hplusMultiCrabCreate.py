#!/usr/bin/env python

import subprocess
import shutil
import os
import sys
import ConfigParser
from optparse import OptionParser
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab

def main(opts):
    mc_conf_file = opts.cfgfile
    crab_conf_file = None
    py_conf_file = None
    json_files = []

    if not os.path.exists(mc_conf_file):
        print "Multicrab configuration file %s doesn't exist!" % mc_conf_file
        return 1

    mc_parser = ConfigParser.ConfigParser()
    mc_parser.read(mc_conf_file)
    crab_conf_file = mc_parser.get("MULTICRAB", "cfg")
    try:
        py_conf_file = mc_parser.get("COMMON", "CMSSW.pset")
    except ConfigParser.NoOptionError:
        pass
    for s in mc_parser.sections():
        try:
            json_files.append(mc_parser.get(s, "CMSSW.lumi_mask"))
        except ConfigParser.NoOptionError:
            pass

    crab_parser = ConfigParser.ConfigParser()
    crab_parser.read(crab_conf_file)
    if py_conf_file == None:
        py_conf_file = crab_parser.get("CMSSW", "pset")
    try:
        json_files.append(crab_parser.get("CMSSW", "lumi_mask"))
    except ConfigParser.NoOptionError:
        pass

    # Unique list of json files
    keys = {}
    for f in json_files:
        keys[f] = 1
    json_files = keys.keys()   

    if crab_conf_file == None:
        print "Did not find crab configuration file"
        return 1
    if py_conf_file == None:
        print "Did not find CMSSW python configuration file"
        return 1

    # Check crab environment
    multicrab.checkCrabInPath()
    dirname = multicrab.createTaskDir()

    shutil.copy(mc_conf_file, os.path.join(dirname, "multicrab.cfg"))
    flist = [crab_conf_file, py_conf_file]
    if len(json_files) > 0:
        flist.extend(json_files)
    for f in flist:
        shutil.copy(f, dirname)

    print "Copied %s to %s" % (", ".join(flist), dirname)
    print "Creating multicrab task"
    print
    print "############################################################"
    print

    os.chdir(dirname)
    subprocess.call(["multicrab", "-create"])

    print
    print "############################################################"
    print
    print "Created multicrab task to subdirectory "+dirname
    print
    print "Jobs can be submitted by e.g. 'cd %s; multicrab -submit" % dirname
    print
   
    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--cfg", dest="cfgfile", type="string", default="multicrab.cfg",
                      help="Multicrab configuration file (default: 'multicrab.cfg')")
    (opts, args) = parser.parse_args()

    sys.exit(main(opts))
