#!/usr/bin/env python

import os
import sys
import subprocess

def getFiles(dataset):
    p = subprocess.Popen(["dbs", "search", "--query", "find file where dataset = %s"%dataset], stdout=subprocess.PIPE)
    output = p.communicate()[0]
    ret = []
    for line in output.split("\n"):
        if "/store/" in line:
            ret.append(line)
    return ret

def getLumis(name):
    p = subprocess.Popen(["dbs", "search", "--query", "find lumi where file = %s"%name], stdout=subprocess.PIPE)
    output = p.communicate()[0]
    ret = []
    for line in output.split("\n"):
        try:
            ret.append(int(line))
        except ValueError:
            pass
    return ret

if __name__ == "__main__":
    dset = sys.argv[1]

    files = getFiles(dset)
    lumiMap = {}
    for f in files:
        lumis = getLumis(f)
        f = os.path.basename(f)
        for l in lumis:
            if l in lumiMap:
                lumiMap[l].append(f)
            else:
                lumiMap[l] = [f]

    fine = True
    for lumi, files in lumiMap.iteritems():
        if len(files) > 1:
            print "Lumi %d, files %s" % (lumi, ", ".join(files))
            fine = False
    if fine:
        print "Dataset is fine"

#files = getFiles("/TTToHplusBWB_M-150_7TeV-pythia6-tauola/Spring11-PU_S1_START311_V1G1-v1/AODSIM")
#print getLumis(files[0])
