#! /usr/bin/env python

import sys
import ROOT
ROOT.gROOT.SetBatch(True)

import os
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab


def getEventWeight(hmc, hdata, nvtx):
    # Get bin index
    mybin = hmc.GetXaxis().FindBin(nvtx)
    mydatabin = hdata.GetXaxis().FindBin(nvtx)
    if mybin != mydatabin:
        print "Error: data and mc pileup histograms have different binning!"
        sys.exit()
    # Calculate data/MC
    return hdata.GetBinContent(mybin) / hmc.GetBinContent(mybin)

def main(opts):
    # open PU histograms
    fmc = ROOT.TFile.Open(opts.mcPU)
    if fmc.IsZombie():
        sys.exit()
    hmcoriginal = fmc.Get("pileup")
    hmc = hmcoriginal.Clone("hmc")
    hmc.Scale(1.0 / hmc.Integral())
    fdata = ROOT.TFile.Open(opts.dataPU)
    if fdata.IsZombie():
        sys.exit()
    hdataoriginal = fdata.Get("pileup")
    hdata = hdataoriginal.Clone("hdata")
    hdata.Scale(1.0 / hdata.Integral())
    fdataup = ROOT.TFile.Open(opts.dataPU.replace(".root","up.root"))
    if fdataup.IsZombie():
        sys.exit()
    hdatauporiginal = fdataup.Get("pileup")
    hdataup = hdatauporiginal.Clone("hdataup")
    hdataup.Scale(1.0 / hdataup.Integral())
    fdatadown = ROOT.TFile.Open(opts.dataPU.replace(".root","down.root"))
    if fdatadown.IsZombie():
        sys.exit()
    hdatadownoriginal = fdatadown.Get("pileup")
    hdatadown = hdatadownoriginal.Clone("hdatadown")
    hdatadown.Scale(1.0 / hdatadown.Integral())

    # loop over datasets
    myoutput = ""
    for multicrabDir in opts.multicrabdir:
        crabDirs = multicrab.getTaskDirectories(None, os.path.join(multicrabDir, "multicrab.cfg"))
        for crabDir in crabDirs:
            taskName = os.path.split(crabDir)[1]
            rootFile = ROOT.TFile.Open(os.path.join(crabDir, "res", "histograms-%s.root"%taskName))
            if rootFile.IsZombie():
                sys.exit()
            # Get tree
            mytree = rootFile.Get("pileupNtuple/tree")
            if mytree == 0:
                sys.exit()
            nevents = mytree.GetEntries()
            print "Processing", taskName, "nevents =",nevents,"..."
            # Set branch adress in tree
            myleaf = mytree.GetLeaf("TrueNumInteractions")
            if myleaf == 0:
                sys.exit()
            # Loop over tree
            nevt = 0.0
            nevtup = 0.0
            nevtdown = 0.0
            for i in range(1,nevents+1):
                if i % 200 == 0:
                    mybar = "\r["
                    for j in range(0, int(float(i) / float(nevents) * 40.0)):
                        mybar += "."
                    for j in range(int(float(i) / float(nevents) * 40.0),40):
                        mybar += " "
                    sys.stdout.write(mybar+"]")
                mytree.GetEntry(i)
                nevt += getEventWeight(hmc, hdata, myleaf.GetValue())
                nevtup += getEventWeight(hmc, hdataup, myleaf.GetValue())
                nevtdown += getEventWeight(hmc, hdatadown, myleaf.GetValue())
                #print nevt, nevtup, nevtdown
            rootFile.Close()
            sys.stdout.write(" Done\n")
            # Write output line
            myline = "        "+'"'+taskName+'"'+": WeightedAllEvents(unweighted=%d, "%nevents+"weighted=%f, "%nevt+"up=%f, "%nevtup+"down=%f),\n"%nevtdown
            #print "\n"+myline
            myoutput += myline
    myresult = "_weightedAllEvents = {\n"
    myresult += "    "+'"'+"myera"+'"'+": {\n"
    myresult += myoutput
    myresult += "    },\n"
    myresult += "}\n\n"
    print ""
    print myresult
    print "Copy the above fragment to python/tools/dataset.py and replace 'myera' with appropriate label, e.g. 2011A\n"
    print "Result was obtained with PU histograms:"
    print "  data:",opts.dataPU
    print "  dataup:",opts.dataPU.replace(".root","up.root")
    print "  datadown:",opts.dataPU.replace(".root","down.root")
    print "  MC:",opts.mcPU
    print ""

#    print "PU weights written to", myoutput

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    #multicrab.addOptions(parser)
    #dataset.addOptions(parser)
    #parser.add_option("-h", "--help", action="help")
    parser.add_option("--dataPU", dest="dataPU", action="store", type="string", help="root file containing PU spectrum for data")
    #parser.add_option("--dataPUup", dest="dataPUup", action="store", type="string", help="root file containing PU spectrum with up variation for data")
    #parser.add_option("--dataPUdown", dest="dataPUdown", action="store", type="string", help="root file containing PU spectrum with down variation for data")
    parser.add_option("--mcPU", dest="mcPU", action="store", type="string", help="root file containing PU spectrum for MC")
    parser.add_option("-o", "--output", dest="outname", action="store", type="string", default="outPU_cfi.py", help="name for output cfi.py fragment")
    parser.add_option("--mdir", dest="multicrabdir", action="append", help="name of multicrab dir (multiple directories can be specified with multiple --mdir arguments)")
    (opts, args) = parser.parse_args()
    
    # Check that proper arguments were given
    mystatus = True
    if opts.dataPU == None:
        print "Missing source for PU spectrum of data!\n"
        mystatus = False
    if opts.mcPU == None:
        print "Missing source for PU spectrum of MC!\n"
        mystatus = False
    if opts.multicrabdir == None:
        print "Missing source for multicrab directories!\n"
        mystatus = False
    if not mystatus:
        parser.print_help()
        sys.exit()

    # Arguments are ok, proceed to run
    main(opts)
    
    #sys.exit(main(opts))
