#!/usr/bin/env python

import os
import sys
import subprocess

sPrefix = "srm://madhatter.csc.fi:8443"
sStartPath = "/pnfs/csc.fi/data/cms/store/user/%s"%os.getenv("USER")

def removeItems(path):
    cmd = "arcls"
    proc = subprocess.Popen([cmd, sPrefix+path], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    lines = out.split("\n")
    for l in lines:
        if l.endswith("log.tar.gz") or l.endswith(".root"):
            # Remove
            print "Removing", os.path.join(path,l)
            os.system("arcrm %s"%(sPrefix+os.path.join(path,l)))
        elif l != "":
            # Assume this is a directory
            print "Entering directory", os.path.join(path,l)
            removeItems(os.path.join(path,l))
            print "Removing directory", os.path.join(path,l)
            os.system("arcrm %s"%(sPrefix+os.path.join(path,l)))

if __name__ == "__main__":
    removeItems(sStartPath)

