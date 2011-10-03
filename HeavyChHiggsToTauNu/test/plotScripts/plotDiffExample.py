#!/usr/bin/env python

###########################################################################
#
# This script is only intended as an example, please do NOT modify it.
# For example, start from scratch and look here for help, or make a
# copy of it and modify the copy (including removing all unnecessary
# code).
#
###########################################################################

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

analysis = "signalAnalysis"
counters = analysis+"Counters"

def main():
    # Create all datasets from a multicrab task
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)

    # Read integrated luminosities of data datasets from lumi.json
    datasets.loadLuminosities()

    # Include only 120 mass bin of HW and HH datasets
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))

    # Default merging nad ordering of data and MC datasets
    # All data datasets to "Data"
    # All QCD datasets to "QCD"
    # All single top datasets to "SingleTop"
    # WW, WZ, ZZ to "Diboson"
    plots.mergeRenameReorderForDataMC(datasets)

    # Set BR(t->H) to 0.2, keep BR(H->tau) in 1
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Merge WH and HH datasets to one (for each mass bin)
    # TTToHplusBWB_MXXX and TTToHplusBHminusB_MXXX to "TTToHplus_MXXX"
    plots.mergeWHandHH(datasets)

    # Merge EWK datasets
    datasets.merge("EWK", [
            "WJets",
            "TTJets",
            "DYJetsToLL",
            "SingleTop",
            "Diboson"
            ])

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Create the normalized plot of transverse mass
    # Read the histogram from the file
    #mT = plots.DataMCPlot(datasets, analysis+"/transverseMass")

    # Create the histogram from the tree (and see the selections explicitly)
    td = dataset.TreeDraw(analysis+"/tree", weight="weightPileup*weightTrigger*weightPrescale",
                             selection="met_p4.Et() > 70 && Max$(jets_btag) > 1.7")
    mT = plots.DataMCPlot(datasets, td.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))>>dist(400, 0, 400)"))

    # Rebin before subtracting
    mT.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(20))

    # Create the data-EWK histogram and draw it
    dataEwkDiff(mT)

    # Draw the mT distribution
    transverseMass(mT)

def dataEwkDiff(mT):
    # Get the normalized TH1 histograms
    # Clone the data one, because we subtract the EWK from it
    data = mT.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    ewk = mT.histoMgr.getHisto("EWK").getRootHisto()

    # Subtract ewk from data
    data.Add(ewk, -1)

    # Draw the subtracted plot
    plot = plots.PlotBase()
    plot.histoMgr.appendHisto(histograms.Histo(data, "Data-EWK"))
    plot.createFrame("transverseMass_data-ewk")
    plot.frame.GetXaxis().SetTitle("m_{T}(#tau, MET) (GeV)")
    plot.frame.GetYaxis().SetTitle("Data - EWK")
    plot.draw()
    plot.save()

def transverseMass(plot):
    plot.histoMgr.forHisto("EWK", styles.StyleFill(styles.ttStyle))
    plot.stackMCHistograms()
    plot.setLegend(histograms.createLegend(0.7, 0.68, 0.9, 0.93))
    plot.createFrame("transverseMass")
    plot.frame.GetXaxis().SetTitle("m_{T}(#tau, MET) (GeV)")
    plot.frame.GetYaxis().SetTitle("Events / %.0f GeV" % plot.binWidth())
    plot.draw()
    plot.save()
    

if __name__ == "__main__":
    main()
