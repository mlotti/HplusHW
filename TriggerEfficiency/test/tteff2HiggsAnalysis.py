#!/usr/bin/env python

import sys
import re
import os

import ROOT
ROOT.gROOT.SetBatch(True)

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux import execute

def usage():
    print
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>"
    print
    sys.exit()


def main():
    if len(sys.argv) < 2:
        usage()


    path = sys.argv[1]
    if not os.path.exists(os.path.join(path,"multicrab.cfg")):
        print "multicrab.cfg not found"
        usage()

    files = getFiles(path)
    for fIN in files:
        modify(fIN)

def getFiles(path):
    files = []
    taskdirs = execute("ls "+path)
    for taskdir in taskdirs:
        subdir = os.path.join(path,taskdir,"res")
        if os.path.isdir(subdir):
            histogramfiles = execute("ls "+os.path.join(subdir,"histograms-*.root"))
            for filename in histogramfiles:
                #filename = os.path.join(subdir,"res","histograms-"+taskdir+".root")
                if os.path.exists(filename):
                    files.append(filename)
    return files

def getDataVersion(filename):
    logfile = os.path.dirname(filename).replace("/res","/log/crab.log")
    dv_re = re.compile("dataVersion=(?P<dataVersion>\S+?):")
    if os.path.exists(logfile):
        fLOG = open(logfile)
        for line in fLOG:
            match = dv_re.search(line)
            if match:
                return match.group("dataVersion")
    print "WARNING, dataversion not found"
    return "dummy"

def modify(filename):

    newName = filename.replace(".","_new.")
    origName = filename.replace(".root",".root_orig")

    fIN = ROOT.TFile.Open(filename)

    if not fIN.FindKey("analysis") == None:
        print "File",filename,"already processed, doing nothing.."
        return

    fOUT = ROOT.TFile.Open(newName,"RECREATE")
    fOUT.cd()
    anadir = fOUT.mkdir("analysis")
    anadir.cd()

    counterdir = anadir.mkdir("counters")
    counterdir.cd()
    counter = ROOT.TH1D("counter","counter",1,0,1)
    counter.Write()

    infodir = fOUT.mkdir("configInfo")
    infodir.cd()
    configinfo = ROOT.TH1D("configinfo","configinfo",1,0,1)
    configinfo.SetBinContent(1,1)
    configinfo.GetXaxis().SetBinLabel(1,"control")
    configinfo.Write()

#    vname = "53XmcS6"
#    data_re = re.compile("^histograms-Tau_")
#
#    match = data_re.search(os.path.basename(filename))
#    if match:
#        vname = "53Xdata"
    vname = getDataVersion(filename)

    dataversion = ROOT.TNamed("dataVersion",vname)
    dataversion.Write()

    anadir.cd()
    tree = fIN.Get("TTEffTree").CloneTree()
    print "modifying",filename," entries",tree.GetEntries()
    if not tree:
        print "Error: cannot find the tree!"
        sys.exit()

#    fOUT = ROOT.TFile.Open(newName,"RECREATE")
#    fOUT.cd()
#    anadir = fOUT.mkdir("analysis")
#    anadir.cd()
    tree.Write("",ROOT.TObject.kWriteDelete)
#    fOUT.WriteTObject(tree)


    fOUT.Close()
    fIN.Close()

    os.system("mv "+filename+" "+origName)
    os.system("mv "+newName+" "+filename)

if __name__ == "__main__":
    main()
