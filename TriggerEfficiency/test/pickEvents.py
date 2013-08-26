#!/usr/bin/env python

import sys
import os
import re
import ROOT

root_re = re.compile("(?P<rootfile>([^/]*))\.root")
event_re = re.compile("(?P<run>(\d+)):(?P<lumi>(\d+)):(?P<event>(\d+))")

def usage():
    print "\n"
    print "### Usage:   pickEvents.py <root file> -pick <pick events file>\n"
    print "\n"
    sys.exit()

def main():

    if len(sys.argv) == 1:
        usage()

    rootfiles = []
    pickeventsfile = ""

    iarg = 1
    while iarg < len(sys.argv):
        if sys.argv[iarg] == "-pick" and iarg < len(sys.argv)-1 :
            pickeventsfile = sys.argv[iarg+1]
            iarg += 1
        match = root_re.search(sys.argv[iarg])
        if match:
            rootfiles.append(sys.argv[iarg])
        iarg += 1

    if pickeventsfile == "":
        usage()

    events = getEvents(pickeventsfile)

    for file in rootfiles:
        pick(file,events)


def getEvents(filename):
    events = []
    fIN = open(filename,'r')
    for line in fIN:
        events.append(line.replace("\n", ""))
    return events

def pick(filename,events):

    fIN = ROOT.TFile.Open(filename)

    fName = "picked.root"
    namebody = filename
    match = root_re.search(filename)
    if match:
        namebody = match.group("rootfile")
        fName = filename.replace(namebody,"picked_"+namebody)

    fOUT = ROOT.TFile.Open(fName,'RECREATE')

    intree = fIN.Get("TTEffTree") 

    leaves = intree.GetListOfLeaves()
    class PyListOfLeaves(dict) :
        pass

    pyl = PyListOfLeaves()
    for i in range(0,leaves.GetEntries() ) :
        leaf = leaves.At(i)
        name = leaf.GetName()
        # add dynamically attribute to my class 
        pyl.__setattr__(name,leaf)

#    for i in range(0,intree.GetEntries()):
#	intree.GetEntry(i)
#        print "rootfile: ",str(int(pyl.run.GetValue())) + ":" + str(int(pyl.lumi.GetValue())) + ":" + str(int(pyl.event.GetValue()))

    tree = intree.CloneTree(0)

    for event in events:
	match = event_re.search(event)
	if match:
	    #print match.group("run"),match.group("lumi"),match.group("event")
	
    	    selection = "run == " + match.group("run") + " && lumi == " + match.group("lumi") + " && event == " + match.group("event")
            picktree = intree.CopyTree(selection)
	    treelist = ROOT.TList()
	    treelist.Add(picktree)
	    tree.Merge(treelist)

            treelist.Delete()
            del treelist

    print namebody," saving",tree.GetEntries(),"events"
    tree.AutoSave()
    fIN.Close()
    fOUT.Close()


if __name__ == "__main__":
    main()
