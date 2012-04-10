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
    datasets.updateNAllEventsToPUWeighted()

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
    met5060 = plots.DataMCPlot(datasets, analysis+"/QCD_MET_AfterJetsBtagging5060")
    met6070 = plots.DataMCPlot(datasets, analysis+"/QCD_MET_AfterJetsBtagging6070")
    met7080 = plots.DataMCPlot(datasets, analysis+"/QCD_MET_AfterJetsBtagging7080")
    met80100 = plots.DataMCPlot(datasets, analysis+"/QCD_MET_AfterJetsBtagging80100")
    met100120 = plots.DataMCPlot(datasets, analysis+"/QCD_MET_AfterJetsBtagging100120")
    met120150 = plots.DataMCPlot(datasets, analysis+"/QCD_MET_AfterJetsBtagging120150")
    met150 = plots.DataMCPlot(datasets, analysis+"/QCD_MET_AfterJetsBtagging150")
    
    # Rebin before subtracting
    met5060.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    met6070.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    met7080.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    met80100.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    met100120.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1)) 
    met120150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
    met150.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(1))
       
    
    data5060 = met5060.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    data6070 = met6070.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    data7080 = met7080.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    data80100 = met80100.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    data100120 = met100120.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    data120150 = met120150.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    data150 = met150.histoMgr.getHisto("Data").getRootHisto().Clone("Data")
    
    # Create the data-EWK histogram and draw it
#    diffBase = dataEwkDiff(metBase, "MET_base_data-ewk")
#    diffInverted = dataEwkDiff(metInver,"MET_inverted_data-ewk")

    # Draw the MET distribution
#    transverseMass(metBase,"MET_base")
#    transverseMass(metInver,"MET_inverted")


    # Set the styles
#    dataset._normalizeToOne(diffBase)
#    dataset._normalizeToOne(diffInverted)
    plot = plots.PlotBase()
    plot.histoMgr.appendHisto(histograms.Histo(data5060, "50 < p_{T}^{#tau jet} < 60 GeV"))
    plot.histoMgr.appendHisto(histograms.Histo(data6070, "60 < p_{T}^{#tau jet} < 70 GeV"))
    plot.histoMgr.appendHisto(histograms.Histo(data7080, "70 < p_{T}^{#tau jet} < 80 GeV"))
    plot.histoMgr.appendHisto(histograms.Histo(data80100, "80 < p_{T}^{#tau jet} < 100 GeV"))
    plot.histoMgr.appendHisto(histograms.Histo(data100120, "100 < p_{T}^{#tau jet} < 120 GeV"))
    plot.histoMgr.appendHisto(histograms.Histo(data120150, "120 < p_{T}^{#tau jet} < 150 GeV"))
    plot.histoMgr.appendHisto(histograms.Histo(data150, "p_{T}^{#tau jet} > 150 GeV")) 
    
    st1 = styles.getDataStyle().clone()
    st2 = st1.clone()
    st2.append(styles.StyleLine(lineColor=ROOT.kRed))
    st3 = st1.clone()
    st3.append(styles.StyleLine(lineColor=ROOT.kBlue))
    st4 = st1.clone()
    st4.append(styles.StyleLine(lineColor=ROOT.kGreen))
    st5 = st1.clone()
    st5.append(styles.StyleLine(lineColor=ROOT.kMagenta, lineStyle=2))
    st6 = st1.clone()
    st6.append(styles.StyleLine(lineColor=ROOT.kPink, lineStyle=8)) # lineWidth=6))
    st7 = st1.clone()
    st7.append(styles.StyleLine(lineColor=ROOT.kBlue-2, lineStyle=3))
    
    plot.histoMgr.forHisto("50 < p_{T}^{#tau jet} < 60 GeV", st1)
    plot.histoMgr.forHisto("60 < p_{T}^{#tau jet} < 70 GeV", st2)
    plot.histoMgr.forHisto("70 < p_{T}^{#tau jet} < 80 GeV", st3)
    plot.histoMgr.forHisto("80 < p_{T}^{#tau jet} < 100 GeV", st4)
    plot.histoMgr.forHisto("100 < p_{T}^{#tau jet} < 120 GeV", st5)
    plot.histoMgr.forHisto("120 < p_{T}^{#tau jet} < 150 GeV", st6)
    plot.histoMgr.forHisto("p_{T}^{#tau jet} > 150 GeV", st7)  

    plot.createFrame("METinBins", opts={"xmax": 200, "ymin":1e-1, "ymaxfactor": 1.5},
#                     createRatio=True, opts2={"ymin": -5 , "ymax": 6 }, # bounds of the ratio plot
                     )

    plot.getPad().SetLogy(True)    
    plot.setLegend(histograms.createLegend(0.6, 0.68, 0.8, 0.93))
    plot.frame.GetXaxis().SetTitle("MET (GeV)")
    plot.frame.GetYaxis().SetTitle("Data")
 
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
