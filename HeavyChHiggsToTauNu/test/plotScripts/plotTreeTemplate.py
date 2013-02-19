#!/usr/bin/env python

######################################################################
#
# This plot script is for analysing the muon selection part of the EWK
# background measurement. The corresponding python job configuration
# is tauEmbedding/muonAnalysis_cfg.py.
#
# The development script is plotMuonAnalysis
#
# Author: Matti Kortelainen
#
######################################################################

import sys
import array

import ROOT
ROOT.gROOT.SetBatch(False) #True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

# Selections (per-event cut)
JetSelection = "jets_p4@.size() >= 3"
MetCut = "met_p4.Pt() > 40"
Mt = "TMath::Sqrt(2*tau_p4.Et()*met_p4.Et()*( 1.0 - ( tau_p4.X()*met_p4.px() + tau_p4.Y()*met_p4.py())/( tau_p4.Et()*met_p4.Et() )))"
MtCut = Mt + "> 150"
Btag = "passedBTagging"
BtagCut = Btag + " >= 1.0"
TauIso = "tau_id_byTightIsolation"
TauIsoCut = TauIso + " >= 1.0"
DeltaPhi = "TMath::ACos(( tau_p4.X()*met_p4.px() + tau_p4.Y()*met_p4.py())/( tau_p4.Et()*met_p4.Et() ))*(180/TMath::Pi())"
DeltaPhiCut = DeltaPhi + "< 160"

# Declarations
treeDraw = dataset.TreeDraw("tree", weight="weightPileup*weightTrigger*weightPrescale")

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(directory="/Volumes/disk/attikis/HIG-12-037/TreeAnalysis_v44_4_130113_105229/", dataEra="Run2011A")
    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()

    print "\n*** Available datasets: %s" % (datasets.getAllDatasetNames())
    datasets.merge("EWK", ["TTJets_TuneZ2_Fall11", "WJets_TuneZ2_Fall11", "DYJetsToLL_M50_TuneZ2_Fall11", "T_t-channel_TuneZ2_Fall11", "Tbar_t-channel_TuneZ2_Fall11", "T_tW-channel_TuneZ2_Fall11", "Tbar_tW-channel_TuneZ2_Fall11", "T_s-channel_TuneZ2_Fall11", "Tbar_s-channel_TuneZ2_Fall11", "WW_TuneZ2_Fall11", "WZ_TuneZ2_Fall11", "ZZ_TuneZ2_Fall11"])
    #datasets.merge("EWK", ["T_s-channel_TuneZ2_Fall11", "Tbar_s-channel_TuneZ2_Fall11", "WW_TuneZ2_Fall11", "WZ_TuneZ2_Fall11", "ZZ_TuneZ2_Fall11"])

    plots.mergeRenameReorderForDataMC(datasets)
    
    # Print basic info
    print "\n*** Int.Lumi",datasets.getDataset("Data").getLuminosity()
    print "*** norm=",datasets.getDataset("TTToHplusBWB_M120").getNormFactor()
    
    # Remove signals other than M120
    datasets.remove(filter(lambda name: "TTToHplus" in name and not "M120" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    datasets.remove(filter(lambda name: "HplusTB" in name, datasets.getAllDatasetNames()))
    
    # Remove data (MC only analysis)
    #datasets.remove(datasets.getDataDatasetNames())

    # Setup style
    styleGenerator = styles.generator(fill=True)
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.04)

    # Merge signals into one histo
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    doPlots(datasets)
    raw_input("*** Press \"Enter\" to exit pyROOT: ")
    
def doPlots(datasets):
    def createPlot(name, **kwargs):
        return plots.DataMCPlot(datasets, name, **kwargs)
    
    #drawPlot = plots.PlotDrawer(stackMCHistograms=True, addMCUncertainty=True, log=True, ratio=True, addLuminosityText=True, ratioYlabel="Ratio", optsLog={"ymin": 1e-1}, opts2={"ymin": 0, "ymax": 2})
    drawPlot = plots.PlotDrawer(stackMCHistograms=True, addMCUncertainty=True, log=True, ratio=False, addLuminosityText=True, ratioYlabel="Ratio", optsLog={"ymin": 1e-1}, opts2={"ymin": 0, "ymax": 2})
    
    # myTreeDraw = treeDraw.clone(selection=And(MetCut, MtCut, BtagCut))
    myTreeDraw = treeDraw.clone(selection=And(MetCut, BtagCut, DeltaPhiCut))
    histograms.cmsTextMode = histograms.CMSMode.PRELIMINARY
    
    print "*** NOTE: What about btag scale factor?\n"
    sphericity = myTreeDraw.clone(varexp="sphericity >> sphericity(20, 0.0, 1.0)")
    drawPlot(createPlot(sphericity), "sphericity", "sphericity", ylabel="Events / %.1f ", cutBox={"cutValue":0.0, "greaterThan":True})

    aplanarity = myTreeDraw.clone(varexp="aplanarity >> aplanarity(20, 0.0, 0.5)")
    drawPlot(createPlot(aplanarity), "aplanarity", "aplanarity", ylabel="Events / %.1f ", cutBox={"cutValue":0.0, "greaterThan":True})

    planarity = myTreeDraw.clone(varexp="planarity >> planarity(20, 0.0, 0.5)")
    drawPlot(createPlot(planarity), "planarity", "planarity", ylabel="Events / %.1f ", cutBox={"cutValue":0.0, "greaterThan":True})
    
    circularity = myTreeDraw.clone(varexp="circularity >> circularity(20, 0.0, 1.0)")
    drawPlot(createPlot(circularity), "circularity", "circularity", ylabel="Events / %.1f ", cutBox={"cutValue":0.0, "greaterThan":True})

    mT = myTreeDraw.clone(varexp="%s >> circularity(30, 0.0, 600.0)" % (Mt))
    drawPlot(createPlot(mT), "mT", "m_{T} [GeV/c^{2}]", ylabel="Events / %.0f ", cutBox={"cutValue":80.0, "greaterThan":True})
    
if __name__ == "__main__":
    main()
