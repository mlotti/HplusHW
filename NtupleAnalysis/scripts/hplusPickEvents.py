#!/usr/bin/env python

import sys
import os
import re

import ROOT

def usage():
    print
    print "### Usage:   ",os.path.basename(sys.argv[0])," <rootfile> <pickEvents.txt>"
    print
    sys.exit()

def main():

    if len(sys.argv) < 3:
        usage()

    root_re = re.compile("(?P<filename>[^/]*\.root)")
    pick_re = re.compile("(?P<filename>pick\S*\.txt)")

    rootFile = ""
    pickFile = ""
    for argv in sys.argv:
        match = root_re.search(argv)
        if match:
            rootFile = argv
        match = pick_re.search(argv)
        if match:
            pickFile = argv

    #print rootFile,pickFile

    newFile = os.path.basename(rootFile.replace(".root","_PickEvents.root"))

    fIN = ROOT.TFile.Open(rootFile)
    fOUT = ROOT.TFile.Open(newFile,"RECREATE")

    commit = None
    generated = None

    commit_re = re.compile("Commit")
    gen_re = re.compile("Generated")
    fIN.cd()
    keys = fIN.GetListOfKeys()
    for i in range(fIN.GetNkeys()):
        objName = keys.At(i).GetName()
        match = commit_re.search(objName)
        if match:
            commit = objName
        match = gen_re.search(objName)
        if match:
            generated = objName


    fOUT.cd()
    tcommit = ROOT.TNamed("","")
    tcommit.Write(commit)

    dv_re = re.compile("")
    dataversion = None
    configInfoDir = fOUT.mkdir("configInfo")
    if fIN.cd("configInfo"):
        subdir = ROOT.gDirectory
        keys = subdir.GetListOfKeys()
        for i in range(len(keys)):
            fIN.cd("configInfo")
            objName = keys.At(i).GetName()
            #print objName
            obj = subdir.Get(objName)
            fOUT.cd("configInfo")
            obj.Write()

    fIN.cd()
    tree = fIN.Get("Events")
    fOUT.cd()
    pickTree = tree.CloneTree(0)
    rle_re = re.compile("(?P<run>\d+):(?P<lumi>\d+):(?P<event>\d+)")
    fPick = open(pickFile)
    fSelection = ""
    for i,line in enumerate(fPick):
        match = rle_re.search(line)
        if match:
            run = match.group("run")
            lumi = match.group("lumi")
            event = match.group("event")
            selection = "(run == %s && lumi == %s && event == %s)"%(run,lumi,event)
            if len(fSelection) == 0:
                fSelection += selection
            else:
                fSelection += "||"+selection 
            if i > 0 and i%50 == 0:
                sys.stdout.write("Processing %ith event          "%i)
                sys.stdout.flush()
                restart_line()
                fIN.cd()
                tmptree = tree.CopyTree(fSelection)
                treelist = ROOT.TList()
                treelist.Add(tmptree)
                fOUT.cd()
                pickTree.Merge(treelist)
                fSelection = ""
    fIN.cd()
    tmptree = tree.CopyTree(fSelection)
    treelist = ROOT.TList()
    treelist.Add(tmptree)
    fOUT.cd()
    print "Processed all events         "
    pickTree.Merge(treelist)

    pickTree.Write()

    fgen = ROOT.TNamed("","")
    fgen.Write(generated.replace('\n',''))

    orig = str(os.path.abspath(rootFile))
    orig = orig.replace('/','.')
    if orig[0] == '.':
        orig = orig[1:]
    pick = "Orig. file: "+orig
    fpick = ROOT.TNamed("","")
    fpick.Write(pick)

    fOUT.ls()
    print "Picked Events, entries",pickTree.GetEntries()
    fOUT.Close()
    fIN.Close()

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

if __name__ == "__main__":
    main()
