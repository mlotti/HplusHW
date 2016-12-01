#!/usr/bin/env python

# Script meant for reducing the data size to a fraction.
# Needed for checking how the analysis is affected if the trigger rate
# is dropped to 0.9, 0.8 or 0.5 of the gathered integrated lumi
# 01122016/S.Lehti

import sys
import os
import re
import random
import ROOT

def usage():
    print
    print "### Usage:   ",os.path.basename(sys.argv[0])," <multicrabdir> <fraction to be kept>"
    print "### Example: ",os.path.basename(sys.argv[0])," multicrab_SignalAnalysis 0.8"
    print
    sys.exit()

def copy(what,into):
    print "Copying",os.path.basename(what)
#    if os.path.exists(os.path.join(into,what)):
#        return
    if os.path.isfile(what):
        command = "cp %s %s"%(what,into)
    else:
        dirname = os.path.basename(what)
        if not os.path.exists(os.path.join(into,dirname)):
            os.mkdir(os.path.join(into,dirname))
            os.mkdir(os.path.join(into,dirname,"results"))
        command = "cp %s %s"%(os.path.join(what,"results","histo*.root"),os.path.join(into,dirname,"results"))
                 
    os.system(command)

def isdatadir(dIN):
    data_re = re.compile("_Run201\d\S_")
    match = data_re.search(os.path.basename(dIN))
    if match:
        return True
    return False

def reduce(dIN,subdir,dOUT,fraction):
    print "Copying",os.path.basename(subdir)
    if not os.path.exists(os.path.join(dOUT,subdir)):
        os.mkdir(os.path.join(dOUT,subdir))
        os.mkdir(os.path.join(dOUT,subdir,"results"))
    files = execute("ls %s"%os.path.join(dIN,subdir,"results","histo*.root"))
    for fIN in files:
        fOUT = os.path.join(dOUT,subdir,"results",os.path.basename(fIN))
        copyfile(fIN,fOUT,fraction)

def copyfile(fnameIN,fnameOUT,fraction):

    fIN = ROOT.TFile.Open(fnameIN,"R")
    fOUT = ROOT.TFile.Open(fnameOUT,"RECREATE")

    fIN.cd()
    keys = fIN.GetListOfKeys()
    for i in range(len(keys)):
        if keys.At(i):
            keyName = keys.At(i).GetName()
            dir = fIN.GetDirectory(keyName)
            fOUT.cd()

            if keyName == "Events":
                treeIN = fIN.Get(keyName)
                treeOUT = treeIN.CloneTree(0)

                for i in range(treeIN.GetEntries()):
                    if random.random() > fraction:
                        continue
                    treeIN.GetEntry(i)
                    treeOUT.Fill()
                    
                #print "check Events",treeIN.GetEntries(),treeOUT.GetEntries()
                continue

            if dir:
                fOUT.mkdir(keyName)
                fOUT.cd(keyName)
                subKeys = dir.GetListOfKeys()
                for skey in subKeys:
                    tobj = fIN.Get(os.path.join(keyName,skey.GetName()))
                    tobj.Write()
                continue
                
            keys.At(i).Write()

    fOUT.Close()
    fIN.Close()
    
def execute(cmd):
    f = os.popen4(cmd)[1]
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
    f.close()
    return ret

def main():
    
    if len(sys.argv) < 3:
        usage()

    multicrabdir = ""
    fraction = 1.0

    for arg in sys.argv[1:]:
        if os.path.exists(arg) and os.path.isdir(arg):
            multicrabdir = arg
        else:
            fraction = float(arg)

    if multicrabdir[len(multicrabdir)-1:] == "/":
        multicrabdir = multicrabdir[:len(multicrabdir)-1]
    newmulticrabdir = multicrabdir + "_LUMI%s"%fraction
    print "Making new multicrab dir",newmulticrabdir,"with %s of luminosity"%fraction

    if not os.path.exists(newmulticrabdir):
        os.mkdir(newmulticrabdir)
    copy(os.path.join(multicrabdir,"lumi.json"),newmulticrabdir)

    ls = execute("ls %s"%multicrabdir)
    subdirs = []
    for a in ls:
        if os.path.isdir(os.path.join(multicrabdir,a)):
            subdirs.append(a)
    for d in subdirs:
        if isdatadir(d):
            reduce(multicrabdir,d,newmulticrabdir,fraction)
        else:
            copy(os.path.join(multicrabdir,d),newmulticrabdir)
            

    
if __name__ == "__main__":
    main()
