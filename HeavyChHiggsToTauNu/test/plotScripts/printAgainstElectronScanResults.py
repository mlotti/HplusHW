#!/usr/bin/env python

import sys
import os
import ROOT

def main(argv):
    myDirectory = "tautest_againstElectron_LooseIso"
    #myDirectory = "tautest_againstElectron_MediumIso"
    myDatasets = ["TTToHplusBWB_M80_Fall11",
                  "TTToHplusBWB_M120_Fall11",
                  "TTToHplusBWB_M160_Fall11",
                  "HplusTB_M200_Fall11",
                  "HplusTB_M300_Fall11",
                  "TTJets_TuneZ2_Fall11"]

    myCounterPrefix = "signalAnalysis"
    myLabels = ["AgainstElectronLoose",
                "AgainstElectronMedium",
                "AgainstElectronTight",
                "AgainstElectronMVA"]
    myCNames = [["tau w. scale", "trigger scale factor", myCounterPrefix+"#lbl#Counters/counter"],
                ["genuine taus", "Tau is genuine", myCounterPrefix+"#lbl#Counters/counter"],
                ["dphi<160 all", "deltaPhiTauMET<160", myCounterPrefix+"#lbl#Counters/counter"],
                ["dphi<160 fake taus", "nonQCDType2:deltaphi160", myCounterPrefix+"#lbl#Counters/counter"],
                ["dphi<160 e->tau", ":deltaphi160", myCounterPrefix+"#lbl#Counters/e->tau"],
                ["dphi<160 e->tau, tau outside", ":deltaphi160", myCounterPrefix+"#lbl#Counters/e->tau with tau outside acceptance"],
                ["dphi<160 mu->tau", ":deltaphi160", myCounterPrefix+"#lbl#Counters/mu->tau"],
                ["dphi<160 mu->tau, tau outside", ":deltaphi160", myCounterPrefix+"#lbl#Counters/mu->tau with tau outside acceptance"],
                ["dphi<160 jet->tau", ":deltaphi160", myCounterPrefix+"#lbl#Counters/jet->tau"],
                ["dphi<160 jet->tau, tau outside", ":deltaphi160", myCounterPrefix+"#lbl#Counters/jet->tau with tau outside acceptance"]]

    print "Directory", myDirectory,"\n"
    for label in myLabels:
        print label
        table = []
        # make title of table
        row = ["Counters"]
        for dset in myDatasets:
            row.append(";"+dset+";;")
        table.append(row)
        # loop over table rows
        for c in myCNames:
            row = [c[0]]
            for dset in myDatasets:
                # open root file
                myFilename = myDirectory + "/" + dset + "/res/histograms-" + dset + ".root"
                f = ROOT.TFile.Open(myFilename)
                if f == 0:
                    print "Cannot open", myFilename
                    sys.exit()
                # obtain histogram
                histoname = c[2].replace("#lbl#",label)
                h = f.Get(histoname)
                #print "Getting histogram",histoname,h
                if h == 0:
                    print "Cannot open histogram ", histoname, " in file ", myFilename, endl
                    sys.exit()
                for b in range(1, h.GetNbinsX()+1):
                    if h.GetXaxis().GetBinLabel(b) == c[1]:
                        row.append(";"+str(h.GetBinContent(b))+";+-;"+str(h.GetBinError(b)))
            table.append(row)
        # print table
        for row in table:
            output = "{0:32}".format(row[0])
            i = 1
            for dset in myDatasets:
                output += " {0:27}".format(row[i])
                i += 1
            print output
        print "\n"

main(sys.argv[1:])
