#! /usr/bin/env python

import sys
import ROOT
ROOT.gROOT.SetBatch(True)

import os
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.TopPtWeightSchemes as topPtWeightSchemes

# We don't need (or actaually can not create) full dataset.Dataset object
class DatasetWrapper:
    def __init__(self, name, rootFile, baseDirectory):
        self.name = name
        self.rootFile = rootFile
        self.baseDirectory = baseDirectory

    def getRootFile(self):
        return self.rootFile

    def getTree(self, treeName):
        return self.rootFile.Get(treeName)

    def createRootChain(self, treeName):
        return (self.getTree(treeName), treeName)

    def getName(self):
        return self.name

    def getBaseDirectory(self):
        return self.baseDirectory

    def isMC(self):
        return True

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

    hweight = hdata.Clone()
    hweight.Divide(hmc)

    hweightUp = hdataup.Clone()
    hweightUp.Divide(hmc)

    hweightDown = hdatadown.Clone()
    hweightDown.Divide(hmc)

    ntupleCache = dataset.NtupleCache("pileupNtuple/tree", "PileupWeightSelector",
                                      selectorArgs=[hweight, hweightUp, hweightDown],
                                      )

    topPtNames = ROOT.std.vector("string")()
    topPtFormulasAllHadr = ROOT.std.vector("string")()
    topPtFormulasSemiLep = ROOT.std.vector("string")()
    topPtFormulasDiLep = ROOT.std.vector("string")()
    print topPtNames
    for name, scheme in topPtWeightSchemes.schemes.iteritems():
        topPtNames.push_back(name)
        topPtFormulasAllHadr.push_back(scheme.allhadronic)
        topPtFormulasSemiLep.push_back(scheme.leptonjets)
        topPtFormulasDiLep.push_back(scheme.dilepton)

    ntupleCacheTTJets = dataset.NtupleCache("pileupNtuple/tree", "PileupWeightSelector",
                                            selectorArgs=[hweight, hweightUp, hweightDown, topPtNames, topPtFormulasAllHadr, topPtFormulasSemiLep, topPtFormulasDiLep],
                                            cacheFileName="histogramCacheTTJets.root"
                                            )


    # loop over datasets
    myoutput = ""
    for multicrabDir in opts.multicrabdir:
        crabDirs = multicrab.getTaskDirectories(None, os.path.join(multicrabDir, "multicrab.cfg"))
        for crabDir in crabDirs:
            taskName = os.path.split(crabDir)[1]
            rootFile = ROOT.TFile.Open(os.path.join(crabDir, "res", "histograms-%s.root"%taskName))
            if rootFile.IsZombie():
                sys.exit()

            # Create Dataset wrapper
            dset = DatasetWrapper(taskName, rootFile, multicrabDir)

            # Get tree for non-weighted number of events
            mytree = dset.getTree("pileupNtuple/tree")
            if mytree == 0:
                raise Exception("Did not find 'pileupNtuple/tree' from %s" % rootFile.GetName())
            nevents = mytree.GetEntries()

            nc = ntupleCache
            topPtWeighting = opts.doTopPt and "TTJets" in taskName
            if topPtWeighting:
                nc = ntupleCacheTTJets

            # Process tree
            nc.process(dset)

            # Get results
            def getResult(histo):
                return nc.getRootHisto(dset, histo, None).GetBinContent(1)
            nevt = getResult("events")
            nevtup = getResult("eventsUp")
            nevtdown = getResult("eventsDown")

            rootFile.Close()
            # Write output line
            if topPtWeighting:
                taskPrefix = "        "+'"'+taskName+'"'+": WeightedAllEventsTopPt("
                myline = taskPrefix+"unweighted = WeightedAllEvents(unweighted=%d, "%nevents+"weighted=%f, "%nevt+"up=%f, "%nevtup+"down=%f),\n"%nevtdown
                for name in topPtWeightSchemes.schemes.iterkeys():
                    def construct(prefix, histoPostfix, postfix):
                        top_nevt = getResult("events_topPt%s_%s"%(histoPostfix, name))
                        top_nevtup = getResult("eventsUp_topPt%s_%s"%(histoPostfix, name))
                        top_nevtdown = getResult("eventsDown_topPt%s_%s"%(histoPostfix, name))
                        return prefix + "=WeightedAllEvents(unweighted=%d, weighted=%f, up=%f, down=%f)" % (nevents, top_nevt, top_nevtup, top_nevtdown) + postfix + "\n"

                    firstPrefix = " "*len(taskPrefix) + name + " = WeightedAllEventsTopPt.Weighted("
                    myline += construct(firstPrefix+"weighted", "", ",")
                    myline += construct(" "*len(firstPrefix)+"up", "Up", ",")
                    myline += construct(" "*len(firstPrefix)+"down", "Down", "),")
                myline += " "*len(taskPrefix)+"),\n"
            else:
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
    print "Copy the above fragment to python/tools/pileupReweightedAllEvents.py and replace 'myera' with appropriate label, e.g. 2011A\n"
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
    parser.add_option("--noTopPt", dest="doTopPt", action="store_false", default=True,
                      help="Do not do top pT reweighting for TTJets")
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
