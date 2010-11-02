#!/usr/bin/env python

import subprocess
import shutil
import os
import sys
import time
import ConfigParser

def main():
    mc_conf_file = "multicrab.cfg"
    crab_conf_file = None
    py_conf_file = None

    mc_parser = ConfigParser.ConfigParser()
    mc_parser.read(mc_conf_file)
    crab_conf_file = mc_parser.get("MULTICRAB", "cfg")

    crab_parser = ConfigParser.ConfigParser()
    crab_parser.read(crab_conf_file)
    py_conf_file = crab_parser.get("CMSSW", "pset")

    if crab_conf_file == None:
        print "Did not find crab configuration file"
        return 1
    if py_conf_file == None:
        print "Did not find CMSSW python configuration file"
        return 1

    dirname = "multicrab_" + time.strftime("%y%m%d_%H%M%S")
    os.mkdir(dirname)

    flist = [mc_conf_file, crab_conf_file, py_conf_file]

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

    print
    print "############################################################"
    print 
    print "hplusCrabCreate.py will soon be removed, use"
    print
    print "     hplusMultiCrabCreate.py"
    print
    print "instead."
    print
    print "############################################################"
    print
  
    return 0

if __name__ == "__main__":
    sys.exit(main())
