#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedding MC
# within the signal analysis. The corresponding python job
# configuration is signalAnalysis_cfg.py with "doPat=1
# tauEmbeddingInput=1" command line arguments.
#
# Authors: Ritva Kinnunen, Matti Kortelainen
#
######################################################################

import math, array, os

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import plotTauEmbeddingSignalAnalysis as tauEmbedding

# Configuration
#analysis = "signalAnalysisRtau0"
#analysis = "signalAnalysisRtau70"
#analysis = "signalAnalysisRtau80"

#postfix = ""
#postfix = "CaloMet60"
postfix = "CaloMet60TEff"

analysis = "signalAnalysis"+postfix
analysisNoRtau = "signalAnalysisRtau0MET70"+postfix
#analysis = analysisNoRtau
counters = analysis+"Counters"

#normalize = True
normalize = False

#era = "EPS"
#era = "Run2011A-EPS"
era = "Run2011A"

countersWeighted = counters
#countersWeighted = counters+"/weighted"
if normalize:
    countersWeighted = counters+"/weighted"


# main function
def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)

    if era == "EPS":
        datasets.remove([
            "SingleMu_Mu_170722-172619_Aug05",
            "SingleMu_Mu_172620-173198_Prompt",
            "SingleMu_Mu_173236-173692_Prompt",
        ])
    elif era == "Run2011A-EPS":
        datasets.remove([
            "SingleMu_Mu_160431-163261_May10",
            "SingleMu_Mu_163270-163869_May10",
            "SingleMu_Mu_165088-166150_Prompt",
            "SingleMu_Mu_166161-166164_Prompt",
            "SingleMu_Mu_166346-166346_Prompt",
            "SingleMu_Mu_166374-167043_Prompt",
            "SingleMu_Mu_167078-167913_Prompt",

            #"SingleMu_Mu_170722-172619_Aug05",
            #"SingleMu_Mu_172620-173198_Prompt",
            #"SingleMu_Mu_173236-173692_Prompt",

            ])
    elif era == "Run2011A":
        pass
    else:
        raise Exception("Unsupported era "+era)
    datasets.updateNAllEventsToPUWeighted()
    datasets.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasets)
    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.04)
    datasets.remove(["QCD_Pt20_MuEnriched"])
    histograms.createLegend.moveDefaults(dh=-0.05)

    def createPlot(name):
        name2 = name
        if isinstance(name, basestring):
            name2 = analysis+"/"+name
        return plots.DataMCPlot(datasets, name2)

    weight = "weightPileup"
    weightBTagging = weight+"*weightBTagging"
    #weight = ""
    #weightBTagging = weight
    if normalize:
        weight = "weightPileup*weightTrigger"
        weightBTagging = weight+"*weightBTagging"
    treeDraw = dataset.TreeDraw(analysis+"/tree", weight=weight)

    tauEmbedding.normalize=False
    drawPlot = tauEmbedding.drawPlot

    caloMetCut = "(tecalomet_p4.Et() > 60)"
    caloMetNoHFCut = "(tecalometNoHF_p4.Et() > 60)"
    metCut = "(met_p4.Et() > 50)"
    bTaggingCut = "passedBTagging"
    #deltaPhi160Cut = "abs(tau_p4.Phi() - met_p4.Phi())*57.3 <= 160"
    deltaPhi160Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 160)"
    deltaPhi130Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 130)"
    deltaPhi90Cut = "(acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 <= 90)"


    mt = "sqrt(2 * tau_p4.Pt() * met_p4.Et() * (1-cos(tau_p4.Phi()-met_p4.Phi())))"
    mtOriginal = "sqrt(2 * temuon_p4.Pt() * temet_p4.Et() * (1-cos(temuon_p4.Phi()-temet_p4.Phi())))"
    #mtCut = " (0 <= %s)" % mt
    mtCut = "(80 < %s && %s < 120)" % (mt, mt)
    #mtCut = "(60 < tau_p4.Pt() && tau_p4.Pt() < 80)"

    td = treeDraw.clone(selection="&&".join([metCut, bTaggingCut, mtCut]))
    drawPlot(createPlot(td.clone(varexp="met_p4.Pt() >>tmp(40,0,400)")),
             "met", "Raw PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="goodPrimaryVertices_n >>tmp(20,0,20)")),
             "vertices_n", "Number of good primary vertices", ylabel="Events", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="tau_p4.Pt() >>tmp(25,0,250)")),
             "tauPt", "#tau-jet p_{T} (GeV/c)", ylabel="Events / %.0f GeV/c", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="tau_p4.Eta() >>tmp(25, -2.5, 2.5)")),
             "tauEta", "#tau-jet #eta (GeV/c)", ylabel="Events / %.1f", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="tau_p4.Phi() >>tmp(32, -3.2, 3.2)")),
             "tauPhi", "#tau-jet #phi (rad)", ylabel="Events / %.1f", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="acos( (tau_p4.Px()*met_p4.Px()+tau_p4.Py()*met_p4.Py())/(tau_p4.Pt()*met_p4.Et()) )*57.3 >> tmp(18,0,180)")),
             "deltaPhi", "#Delta#phi(#tau jet, E_{T}^{miss}) (^{#circ})", ylabel="Events / %.0f^#{circ}", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="%s >>tmp(20,0,200)"%mt)),
             "mt", "m_{T}(#tau jet, E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})

    drawPlot(createPlot(td.clone(varexp="temuon_p4.Pt() >>tmp(25,0,250)")),
             "muonPt", "Muon p_{T} (GeV/c)", ylabel="Events / %.0f GeV/c", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="temet_p4.Pt() >>tmp(40,0,400)")),
             "metOriginal", "Original E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="acos( (temuon_p4.Px()*temet_p4.Px()+temuon_p4.Py()*temet_p4.Py())/(temuon_p4.Pt()*temet_p4.Et()) )*57.3 >> tmp(18,0,180)")),
             "deltaPhiOriginal", "#Delta#phi(#mu, E_{T,orig}^{miss}) (^{#circ})", ylabel="Events / %.0f^#{circ}", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="%s >>tmp(20,0,200)"%mtOriginal)),
             "mtOriginal", "m_{T}(#mu, E_{T,orig}^{miss} (GeV)", ylabel="Events / %.0f GeV", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    

    print td.selection

    beamHaloEvents = [
        (167676, 191, 175029501),
        (167281, 131, 169702989),
        (171178, 585, 622286805),
        (171578, 353, 342125646),
        (171876, 116, 164854215),
        (170854, 109, 112747742),
        (172822, 2241, 2818902364),
        (172822, 697, 946580712),
        (172868, 462, 625761643),
        (172791, 182, 223810661),
        (173692, 745, 1067744681),
        ]

    td = treeDraw.clone(selection="||".join(["(run==%d && lumi==%d && event==%d)" % eventId for eventId in beamHaloEvents]))
    drawPlot(createPlot(td.clone(varexp="tau_p4.Pt() >>tmp(25,0,250)")),
             "beamHalo_tauPt", "#tau-jet p_{T} (GeV/c)", ylabel="Events / %.0f GeV/c", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="met_p4.Pt() >>tmp(40,0,400)")),
             "beamHalo_met", "Raw PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="%s >>tmp(20,0,200)"%mt)),
             "beamHalo_mt", "m_{T}(#tau jet, E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV", addMCUncertainty=True, ratio=False, opts2={"ymin":0, "ymax": 2})
    



# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
