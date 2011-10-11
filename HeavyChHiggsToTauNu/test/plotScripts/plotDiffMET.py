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
#    mT = plots.DataMCPlot(datasets, td.clone(varexp="sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))>>dist(400, 0, 400)"))
    
#    met = plots.DataMCPlot(datasets, td.clone(varexp="met_p4.Et()>>dist(400, 0, 400)"))
    metBase = plots.DataMCPlot(datasets, analysis+"/MET_BaseLineTauIdBtag")
    metInver = plots.DataMCPlot(datasets, analysis+"/MET_InvertedTauIdBtag")  
    # Rebin before subtracting
    metBase.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    metInver.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(10))
    
    metInverted_data = metInver.histoMgr.getHisto("Data").getRootHisto().Clone(analysis+"/MET_InvertedTauIdBtag")
    print "print inverted met"
    print metInverted_data.GetEntries()

    # Create the data-EWK histogram and draw it
    diffBase = dataEwkDiff(metBase, "MET_base_data-ewk")
    diffInverted = dataEwkDiff(metInver,"MET_inverted_data-ewk")

    # Draw the MET distribution
    transverseMass(metBase,"MET_base")
    transverseMass(metInver,"MET_inverted")

  
    # Set the styles
    dataset._normalizeToOne(diffBase)
    dataset._normalizeToOne(diffInverted)
    plot = plots.ComparisonPlot(
        histograms.Histo(diffBase, "Baseline"),
        histograms.Histo(diffInverted, "Inverted"))


    
    st1 = styles.getDataStyle().clone()
    st2 = st1.clone()
    st2.append(styles.StyleLine(lineColor=ROOT.kRed))
    plot.histoMgr.forHisto("Baseline", st1)
    plot.histoMgr.forHisto("Inverted", st2)
    

    plot.createFrame("METbaseVSinverted-ewk", opts={"xmax": 400, "ymin":1e-5, "ymaxfactor": 1.5},
                     createRatio=True, opts2={"ymin": -5 , "ymax": 6 }, # bounds of the ratio plot
                     )

    plot.getPad().SetLogy(True)    
    plot.setLegend(histograms.createLegend(0.7, 0.68, 0.9, 0.93))
    plot.frame.GetXaxis().SetTitle("MET (GeV)")
    plot.frame.GetYaxis().SetTitle("Data - EWK")
 
# Draw the plot
    plot.draw()
    plot.save()




   
def dataEwkDiff(mT,name):
    # Get the normalized TH1 histograms
    # Clone the data one, because we subtract the EWK from it
    data = mT.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    ewk = mT.histoMgr.getHisto("EWK").getRootHisto()

    # Subtract ewk from data
    data.Add(ewk, -1)

    return data

def plotDataEwkDiff(mT, name):
    data = dataEwkDiff(mT, name)

    # Draw the subtracted plot
    plot = plots.PlotBase()
    plot.histoMgr.appendHisto(histograms.Histo(data, "Data-EWK"))
    plot.createFrame(name, opts={"ymin": 1e-1, "ymaxfactor": 10})
    plot.frame.GetXaxis().SetTitle("MET (GeV)")
    plot.frame.GetYaxis().SetTitle("Data - EWK")
    # Set Y axis to logarithmic
    plot.getPad().SetLogy(True)
    plot.draw()
    # Add the various texts to 
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
#    plot.addLuminosityText()
    plot.save()

def transverseMass(plot,name):
    plot.histoMgr.forHisto("EWK", styles.StyleFill(styles.ttStyle))
    plot.stackMCHistograms()
    plot.setLegend(histograms.createLegend(0.7, 0.68, 0.9, 0.93))
    plot.createFrame(name, opts={"ymin": 1e-1, "ymaxfactor": 10})
    # Set Y axis to logarithmic
    plot.getPad().SetLogy(True)
    plot.frame.GetXaxis().SetTitle("MET (GeV)")
    plot.frame.GetYaxis().SetTitle("Events / %.0f GeV" % plot.binWidth())
    plot.draw()
    # Add the various texts to 
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    plot.addLuminosityText()
    plot.save()
    

if __name__ == "__main__":
    main()
