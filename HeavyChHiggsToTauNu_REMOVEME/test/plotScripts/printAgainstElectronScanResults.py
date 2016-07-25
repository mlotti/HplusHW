#!/usr/bin/env python


# -----------------------------------------------------------------------------------
# What this script does:
#   Prints tau fake rate and efficiencies
# Use case:
#   Choose tau working points for against electron, against muon, and isolation discriminators
# -----------------------------------------------------------------------------------

import sys
import ROOT
ROOT.gROOT.SetBatch(True)

import os
from optparse import OptionParser
from math import sqrt,pow

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle

class Result:
    def __init__(self, dsetTitle, variationTitle):
        self._dsetTitle = dsetTitle
        self._variationTitle = variationTitle
        self._taus = 0.0
        self._efakes = 0.0
        self._mufakes = 0.0
        self._jetfakes = 0.0
        #self._genuineTauAcceptance = 0.0
        self._eventYield = 0.0
        self._genuineTauEventYield = 0.0
        self._tausErr = 0.0
        self._efakesErr = 0.0
        self._mufakesErr = 0.0
        self._jetfakesErr = 0.0
        #self._genuineTauAcceptanceErr = 0.0
        self._eventYieldErr = 0.0
        self._genuineTauEventYieldErr = 0.0

    def printAll(self,prefix=None):
        myPrefix = ""
        if prefix != None:
            myPrefix = prefix+" , "
        print myPrefix+"Nall,",self._eventYield,",",self._eventYieldErr,",Ntau,",self._genuineTauEventYield,",",self._genuineTauEventYieldErr,",tauRatio,",self._taus,",",self._tausErr,",etauRatio,",self._efakes,",",self._efakesErr,",mutauRatio,",self._mufakes,",",self._mufakesErr,",jettauRatio,",self._jetfakes,",",self._jetfakesErr

    def setValueForData(self, h):
        self._eventYield = h.GetBinContent(1)
        self._eventYieldErr = h.GetBinError(1)


    def setValueForMC(self, h):
        Nall = h.GetBinContent(1)
        Ntau = h.GetBinContent(2)+h.GetBinContent(3)
        Netau = h.GetBinContent(4)
        Nmutau = h.GetBinContent(5)
        Njettau = h.GetBinContent(6)
        if Nall > 0:
            self._taus = Ntau / Nall;
            if Ntau > 0:
                self._tausErr = self._taus*sqrt(pow(sqrt(pow(h.GetBinError(2),2)+pow(h.GetBinError(3),2))/Ntau,2)+pow(h.GetBinError(1)/Nall,2))
            self._efakes = Netau / Nall;
            if Netau > 0:
                self._efakesErr = self._efakes*sqrt(pow(h.GetBinError(4)/Netau,2)+pow(h.GetBinError(1)/Nall,2))
            self._mufakes = Nmutau / Nall;
            if Nmutau > 0:
                self._mufakesErr = self._mufakes*sqrt(pow(h.GetBinError(5)/Nmutau,2)+pow(h.GetBinError(1)/Nall,2))
            self._jetfakes = Njettau / Nall;
            if Njettau > 0:
                self._jetfakesErr = self._jetfakes*sqrt(pow(h.GetBinError(6)/Njettau,2)+pow(h.GetBinError(1)/Nall,2))
        self._eventYield = Nall
        self._eventYieldErr = h.GetBinError(1)
        self._genuineTauEventYield = Ntau
        self._genuineTauEventYieldErr = sqrt(pow(h.GetBinError(2),2)+pow(h.GetBinError(3),2))
        Ncheck = Ntau + Netau + Nmutau + Njettau
        if Nall > 0:
            if Ncheck/Nall < 0.0001:
                print "Error: Constituents do not sum up to All events! (%s,%s)"%(self._dsetTitle,self._variationTitle)
                self.printAll()
                for i in range (1,h.GetNbinsX()+1):
                    print h.GetXaxis().GetBinLabel(i),",",h.GetBinContent(i)
                sys.exit()

    def belongsToDataset(self, dsetTitle):
        return self._dsetTitle == dsetTitle

    def belongsToVariation(self, variationTitle):
        return self._variationTitle == variationTitle

def getModules(rootFile,opts,myFilters):
    mylist = []
    myEra = opts.era[0][0].upper()+opts.era[0][1:]
    myRunType = opts.runType[0][0].upper()+opts.runType[0][1:]
    for i in range(0, rootFile.GetNkeys()):
        myKey = rootFile.GetListOfKeys().At(i)
        if myKey.IsFolder():
            # Ignore systematics directories
            myTitle = myKey.GetTitle()
            if not "Plus" in myTitle and not "Minus" in myTitle and not "configInfo" in myTitle and not "PUWeightProducer" in myTitle:
                if myEra in myTitle and myRunType in myTitle:
                    # Apply filters
                    myStatus = True
                    for f in myFilters:
                        if f not in myTitle:
                            myStatus = False
                    if myStatus or len(myTitle) < 35:
                        mylist.append(myTitle)
    return mylist

def main(opts):
    tdrstyle.TDRStyle()

    myDatasets = ["TTToHplusBWB_M80_Fall11",
                  "TTToHplusBWB_M120_Fall11",
                  "TTToHplusBWB_M160_Fall11",
                  "HplusTB_M180_Fall11",
                  "HplusTB_M220_Fall11",
                  "HplusTB_M300_Fall11",
                  "TTJets_TuneZ2_Fall11",
                  "Tau_160431-167913_2011A_Nov08",
                  "Tau_170722-173198_2011A_Nov08",
                  "Tau_173236-173692_2011A_Nov08",
                  "Tau_175832-180252_2011B_Nov19"]
    myFilters = ["AgainstElectronVTightMVA3",
                 "AgainstMuonTight2"]
    myFilters = []
    myHistonameData = "CommonPlots/AtEveryStep/Selected/nVertices"
    myHistoname = "CommonPlots/AtEveryStep/Selected/tau_fakeStatus"
    myHistoname = "CommonPlots/AtEveryStep/JetSelection/tau_fakeStatus"

    myModuleList = []
    myResults = []
    Ndset = 0
    for dset in myDatasets:
        Ndset += 1
        print "Dataset: %d/%d: %s"%(Ndset,len(myDatasets),dset)
        # Open root file
        myfilename = "%s/res/histograms-%s.root"%(dset,dset)
        myRootFile = ROOT.TFile.Open(myfilename)
        if myRootFile == None:
            print "Error: Could not open root file '%s'!"%myfilename
            sys.exit()
        # Fine modules
        if len(myModuleList) == 0:
            myModuleList = getModules(myRootFile,opts,myFilters)
        # Loop over modules
        Nmodule = 0
        for module in myModuleList:
            Nmodule += 1
            myResult = Result(dset,module)
            if dset[0:4] == "Tau_":
                # Get histogram
                myEra = opts.era[0][0].upper()+opts.era[0][1:]
                myRunType = opts.runType[0][0].upper()+opts.runType[0][1:]
                myTmpName = module.replace(myEra,"")
                h = myRootFile.Get("%s/%s"%(myTmpName,myHistoname))
                if h == None:
                    print "Error: could not open histogram '%s/%s' in file '%s'!"%(myTmpName,myHistoname,myfilename)
                    sys.exit()
                myResult.setValueForData(h)
            else:
                # Get histogram
                h = myRootFile.Get("%s/%s"%(module,myHistoname))
                if h == None:
                    print "Error: could not open histogram '%s/%s' in file '%s'!"%(module,myHistoname,myfilename)
                    sys.exit()
                # Get results
                myResult.setValueForMC(h)
            myResults.append(myResult)
        myRootFile.Close()
    # Results have been read, now print output
    print "\nResults for step",myHistoname
    for dset in myDatasets:
        print "Dataset:"+dset
        for module in myModuleList:
            for r in myResults:
                if r.belongsToDataset(dset) and r.belongsToVariation(module):
                    r.printAll(module)

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    #parser.add_option("-d", dest="dirs", action="append", help="name of sample directory inside multicrab dir (multiple directories can be specified with multiple -d arguments)")
    parser.add_option("-e", dest="era", action="append", help="name of era")
    parser.add_option("-t", dest="runType", action="append", help="type of run (light / heavy)")
    (opts, args) = parser.parse_args()

    # Check that proper arguments were given
    mystatus = True
    #if opts.dirs == None:
        #print "Missing source for sample directories!\n"
        #mystatus = False
    if opts.era == None:
        print "Missing specification for era!\n"
        mystatus = False
    if opts.runType == None:
        print "Missing run type specification! (light or heavy)"
        mystatus = False
    if not mystatus:
        parser.print_help()
        sys.exit()

    # Arguments are ok, proceed to run
    main(opts)

