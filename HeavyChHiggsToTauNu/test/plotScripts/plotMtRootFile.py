#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

analysis = "signalAnalysis"
counters = analysis+"Counters"
outputFile = "lands.root"

def main():
    # Create all datasets from a multicrab task
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)

    # Read integrated luminosities of data datasets from lumi.json
    datasets.loadLuminosities()

    # Default merging nad ordering of data and MC datasets
    # All data datasets to "Data"
    # All QCD datasets to "QCD"
    # All single top datasets to "SingleTop"
    # WW, WZ, ZZ to "Diboson"
    plots.mergeRenameReorderForDataMC(datasets)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    #xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.2, br_Htaunu=1)

    # LandS assumes ttbar cross section  for both HW and HH
    # LandS expects that HW and HH are normalized to top cross section

    xsect.setHplusCrossSectionsToTop(datasets)

    # Create data-MC comparison plot to get the proper normalization
    # easily
    mt = plots.DataMCPlot(datasets, analysis+"/transverseMassBeforeFakeMet")

    # Rebin to have the agreed 10 GeV binning
    mt.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))

    # Create the output ROOT file
    f = ROOT.TFile.Open(outputFile, "RECREATE")
    
    # Add the histograms of the wanted datasets to the tree
    for datasetName, outputName in [("Data", "data"),
                                    ("TTToHplusBWB_M120", "hw"),
                                    ("TTToHplusBHminusB_M120", "hh")]:
        th1 = mt.histoMgr.getHisto(datasetName).getRootHisto().Clone("mt_"+outputName)
        th1.SetDirectory(f)
        th1.Write()

    # Write and close the file
    f.Close()

    print
    print "Wrote transverse mass histograms to %s for LandS" % outputFile

if __name__ == "__main__":
    main()
