#!/usr/bin/env python

######################################################################
#
# The ntuple files should come from the TTEff code
#
# Author: Matti Kortelainen
#
######################################################################

import os
import math
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import plotTauEfficiency as tauEfficiency

style90_23 = styles.Style(ROOT.kOpenCircle, ROOT.kRed+1)
style90_32 = styles.Style(ROOT.kFullCircle, ROOT.kRed+1)
style160_23 = styles.Style(ROOT.kOpenSquare, ROOT.kBlue-4)
style160_32 = styles.Style(ROOT.kFullSquare, ROOT.kBlue-4)
style5 = styles.StyleCompound([styles.Style(33, ROOT.kMagenta-2), styles.StyleMarker(markerSize=2)])
style6 = styles.StyleCompound([styles.Style(34, ROOT.kOrange-2), styles.StyleMarker(markerSize=2)])

# base = "/mnt/flustre/mkortela/TTEffNtuples/tteffAnalysis_TTToHplusBWB_M-%s_7TeV-pythia6-tauola_Fall11_E7TeV_Ave%s_50ns_v2_v442p9_V00_09_08_v3/tteffAnalysis-hltpftautight-hpspftau.root"
# files_09_08_v3 = [
#     (base % (90, 23), "M=90, PU=23", style90_23),
#     (base % (90, 32), "M=90, PU=32", style90_32),
#     (base % (160, 23), "M=160, PU=23", style160_23),
#     (base % (160, 32), "M=160, PU=32", style160_32),
#     ]

# base = "/mnt/flustre/mkortela/TTEffNtuples/tteffAnalysis_TTToHplusBWB_M-%s_7TeV-pythia6-tauola_Fall11_E7TeV_Ave%s_50ns_v2_v442p9_V00_09_11/tteffAnalysis-hltpftautight-hpspftau.root"
# files_09_11 = [
#     (base % (90, 32), "M=90, PU=32", style90_32)
# ]

#base = "/mnt/flustre/mkortela/TTEffNtuples/tteffAnalysis_TTToHplusBWB_M-%s_7TeV-pythia6-tauola_Fall11_E7TeV_Ave%s_50ns_v2_v443_V00_09_13_v2/tteffAnalysis-hltpftaumedium-hpspftau.root"
#files_09_13_v2 = [
#    (base % (90, 32), "M=90, PU=32", style90_32)
#]

pickEvents=""
#pickEvents="picked_"
base = "/mnt/flustre/mkortela/TTEffNtuples/tteffAnalysis_TTToHplusBWB_M-%s_7TeV-pythia6-tauola_Fall11_E7TeV_Ave%s_50ns_v2_v443_V00_09_16/"+pickEvents+"tteffAnalysis-hltpftaumedium-hpspftau.root"
dict_09_16 = {
    "M90_PU32" : (base % (90, 32), "M=90, PU=32", style90_32),
    "M160_PU32": (base % (160, 32), "M=160, PU=32", style160_32),
    "M90_PU23" : (base % (90, 23), "M=90, PU=23", style90_23),
    "M160_PU23": (base % (160, 23), "M=160, PU=23", style160_23),
}

base = "/mnt/flustre/mkortela/TTEffNtuples/tteffAnalysis_TTToHplusBWB_M-%s_7TeV-pythia6-tauola_Fall11_E7TeV_Ave%s_50ns_v2_v443_V00_09_16_noVertex/"+pickEvents+"tteffAnalysis-hltpftaumedium-hpspftau.root"
dict_09_16_noPV = {
    "M90_PU32" : (base % (90, 32), "M=90, PU=32", style90_32),
    "M160_PU32": (base % (160, 32), "M=160, PU=32", style160_32),
    "M90_PU23" : (base % (90, 23), "M=90, PU=23", style90_23),
    "M160_PU23": (base % (160, 23), "M=160, PU=23", style160_23),
}
base = "/mnt/flustre/mkortela/TTEffNtuples/tteffAnalysis_TTToHplusBWB_M-%s_7TeV-pythia6-tauola_Fall11_E7TeV_Ave%s_50ns_v2_v443_V00_09_16_vertexSelector/"+pickEvents+"tteffAnalysis-hltpftaumedium-hpspftau.root"
dict_09_16_vertexSelector = {
    "M90_PU32" : (base % (90, 32), "M=90, PU=32", style90_32),
    "M160_PU32": (base % (160, 32), "M=160, PU=32", style160_32),
    "M90_PU23" : (base % (90, 23), "M=90, PU=23", style90_23),
    "M160_PU23": (base % (160, 23), "M=160, PU=23", style160_23),
}

base = "/mnt/flustre/mkortela/TTEffNtuples/tteffAnalysis_TTToHplusBWB_M-%s_7TeV-pythia6-tauola_Fall11_E7TeV_Ave%s_50ns_v2_v443_V00_09_17_noVertex/"+pickEvents+"tteffAnalysis-hltpftaumedium-hpspftau.root"
dict_09_17_noPV = {
    "M90_PU32" : (base % (90, 32), "M=90, PU=32", style90_32),
    "M160_PU32": (base % (160, 32), "M=160, PU=32", style160_32),
    "M90_PU23" : (base % (90, 23), "M=90, PU=23", style90_23),
    "M160_PU23": (base % (160, 23), "M=160, PU=23", style160_23),
}
base = "/mnt/flustre/mkortela/TTEffNtuples/tteffAnalysis_TTToHplusBWB_M-%s_7TeV-pythia6-tauola_Fall11_E7TeV_Ave%s_50ns_v2_v443_V00_09_17_noVertex/"+pickEvents+"tteffAnalysis-hltpftau-hpspftau.root"
dict_09_17_loose = {
    "M90_PU32" : (base % (90, 32), "M=90, PU=32", style90_32),
    "M160_PU32": (base % (160, 32), "M=160, PU=32", style160_32),
    "M90_PU23" : (base % (90, 23), "M=90, PU=23", style90_23),
    "M160_PU23": (base % (160, 23), "M=160, PU=23", style160_23),
}

def make_09_18(version="", iso=""):
    base = "/mnt/flustre/mkortela/TTEffNtuples/tteffAnalysis_TTToHplusBWB_M-%d_7TeV-pythia6-tauola_Fall11_E7TeV_Ave%d_50ns_v2_v443_V00_09_18%s/"+pickEvents+"tteffAnalysis-hltpftau%s-hpspftau.root"
    return {
        "M90_PU32" : (base % (90, 32, version, iso), "M=90, PU=32", style90_32),
        "M160_PU32": (base % (160, 32, version, iso), "M=160, PU=32", style160_32),
        "M90_PU23" : (base % (90, 23, version, iso), "M=90, PU=23", style90_23),
        "M160_PU23": (base % (160, 23, version, iso), "M=160, PU=23", style160_23),
        }

dc_loose = make_09_18()
dc_loose_noPV = make_09_18(version="_noVertex")
dc_loose_vertexSelector = make_09_18(version="_vertexSelector")
dc_medium = make_09_18(iso="medium")
dc_medium_noPV = make_09_18(version="_noVertex", iso="medium")
dc_medium_vertexSelector = make_09_18(version="_vertexSelector", iso="medium")

files_medium = [
    dc_medium_noPV["M90_PU23"],
    dc_medium_noPV["M160_PU23"],
    dc_medium_noPV["M90_PU32"],
    dc_medium_noPV["M160_PU32"],
]
files_loose = [
    dc_loose_noPV["M90_PU23"],
    dc_loose_noPV["M160_PU23"],
    dc_loose_noPV["M90_PU32"],
    dc_loose_noPV["M160_PU32"],
]

#outputDir = "triggerDevelopmentPlots"
#outputDir = "triggerDevelopmentPlotsLooseCombined"
outputDir = "triggerDevelopmentPlotsMediumCombined"
#outputDir = "triggerDevelopmentPlotsTightCombined"

offlineSelectionNoPt = And(
    "abs(PFTauEta) < 2.1",
    "PFTauLeadChargedHadrCandPt > 20",
    "PFTauProng == 1",
    "PFTau_decayModeFinding > 0.5",
    "PFTau_againstElectronMedium > 0.5 && PFTau_againstMuonTight > 0.5",
#    "PFTau_byTightIsolation"
#    "PFTau_byLooseCombinedIsolationDeltaBetaCorr"
    "PFTau_byMediumCombinedIsolationDeltaBetaCorr"
#    "PFTau_byTightCombinedIsolationDeltaBetaCorr"
)
offlineSelection = And(
    offlineSelectionNoPt,
    "PFTauPt > 20",
)
offlineSelection40 = And(
    offlineSelectionNoPt,
    "PFTauPt > 40",
)

offlineEventSelection = And(
    "Sum$(%s) >= 1" % offlineSelection40,
    "Sum$(PFJetPt > 30) >= 3+Sum$(%s && PFTauJetMinDR < 0.5)" % offlineSelection40
)

l1Selection = "PFTau_matchedL1 >= 0"
#l1Selection = "PFTau_matchedL1 >= 0 && L1JetEt[PFTau_matchedL1] > 52"
#l1Selection = "hasMatchedL1Jet"
#l1Selection = "hasMatchedL1Jet && L1JetEt > 52"

l2Selection_template = And("hasMatchedL2Jet", "L2JetEt>%d")

l25Selection_reco = "hasMatchedL25Tau"
l25Selection_pt_template = "L25TauPt>%d"
#l25Selection_trackFound = "L25TauLeadChargedHadrCandExists"
l25Selection_trackFound = "L25Tau_TrackFinding"
l25Selection_trackPt_template = "L25TauLeadChargedHadrCandPt>%d"
l25Selection_trackPt = "L25Tau_TrackPt20"
l25Selection_template = And(
    l25Selection_reco,
    l25Selection_pt_template,
    l25Selection_trackFound,
    l25Selection_trackPt
)

#l3SelectionIso = And("primaryVertexIsValid", "L25TauIsoChargedHadrCandPtMax < 1.0")
l3SelectionIso = "L25Tau_LooseIso"
#l3SelectionProng = "L25Tau
l3SelectionProng = "L25TauProng <= 4"
l3Selection = And(l3SelectionIso, l3SelectionProng)

l1MetSelection_template = "L1MET>%d"
l2MetSelection_template = "HLTMET_ET>%d"
l2MhtSelection_template = "HLTMHT_ET>%d"

#ptbins = [20, 30, 40, 50, 60, 80, 100, 120, 140, 160]
ptbins = [20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100, 120, 140, 160]
hnumpt = ROOT.TH1F("hnumpt", "hnumpt", len(ptbins)-1, array.array("d", ptbins))
npubins = [0, 10, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35, 40]
hnumpv = ROOT.TH1F("hnumpv", "hnumpv", len(npubins)-1, array.array("d", npubins))
#metbins = [0, 25, 50, 75, 100, 125, 150, 175, 225]
#metbins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200]
metbins = [0, 10, 20, 35, 50, 65, 80, 95, 110, 125, 140, 160, 180, 200]
hnummet = ROOT.TH1F("hnummet", "hnummet", len(metbins)-1, array.array("d", metbins))

xlabel_pt = "#tau-jet p_{T} (GeV/c)"
xlabel_npv = "Good reco vertices"
xlabel_met = "Uncorrected PF E_{T}^{miss}"

def isoToMedium(selection, mediumIsolation):
    if mediumIsolation:
        return selection.replace("LooseIso", "MediumIso")
    else:
        return selection


def main():
    style = tdrstyle.TDRStyle()

    histograms.createLegend.moveDefaults(dx=-0.2, dy=-0.4, dh=-0.15)

    if len(pickEvents) > 0:
        doPlots(35, 35, 20, 40, 75)
    #doPlots(30, 35, 20, 40, 75)
    #doPlots(20, 35, 20, 40, 75)
    #doPlots(25, 35, 10, 40, 75)

    doPlots(25, 35, 20, 40, 70, l25Prongs=4)
    doPlots(25, 35, 20, 40, 70, l25Prongs=4, mediumIsolation=True)

    if len(pickEvents) > 0:
        doPlots(25, 35, 20, 40, 75, l25Prongs=4)
        doPlots(25, 35, 20, 40, 70)
        doPlots(25, 35, 20, 40, 70, l25Prongs=4)
        doPlots(25, 35, 20, 40, 70, l25Prongs=3)
        doPlots(25, 35, 20, 40, 70, l25Prongs=2)

        doPlots(25, 35, 20, 40, 70, useMHT=True)
        doPlots(25, 35, 20, 40, 75, useMHT=True)
    else:
        doPlots2("M90_PU32")
        doPlots2("M160_PU32")
        doPlots2("M90_PU23")
        doPlots2("M160_PU23")

def doPlots(l2JetPt, l25TauPt, l25TrackPt, l1Met, hltMet, useMHT=False, l25Prongs=None, mediumIsolation=False):
    # offlineSelectionOther = And(
    #     "PFMET_ET > 50",
    #     "Sum$(PFJetPt > 30) >= (3+Sum$(%s && PFTauJetMinDR < 0.5))" % offlineSelection
    # )

    isoName = "Loose"
    if mediumIsolation:
        isoName = "Medium"
    

    trigger = "HLT_L2Jet%d_%sIsoPFTau%d_Trk%d" % (l2JetPt, isoName, l25TauPt, l25TrackPt)
    if l25Prongs != None:
        trigger += "_Prong%d" % l25Prongs
    triggerMet = "L1_ETM%d_%s_MET%d" % (l1Met, trigger, hltMet)
    if useMHT:
        triggerMet = triggerMet.replace("MET", "PFMHT")

    l2Selection = l2Selection_template % l2JetPt

    l25Selection_pt = l25Selection_pt_template % l25TauPt
    l25Selection  = l25Selection_template % l25TauPt

    l3SelectionProngs = ""
    if l25Prongs != None:
        l3SelectionProngs = "L25TauProng <= %d" % l25Prongs

    l1MetSelection = l1MetSelection_template % l1Met
    l2MetSelection = l2MetSelection_template % hltMet
    if useMHT:
        l2MetSelection = l2MhtSelection_template % hltMet

    if mediumIsolation:
        plotter = Plotter([(tauEfficiency.EfficiencyCalculator([f]), l, p) for f, l, p in files_medium], outputDir)
#        plotter_noPV = Plotter([(tauEfficiency.EfficiencyCalculator([f]), l, p) for f, l, p in files_noPV], outputDir)
#        plotter_vertexSelector= Plotter([(tauEfficiency.EfficiencyCalculator([f]), l, p) for f, l, p in files_vertexSelector], outputDir)
    else:
        plotter = Plotter([(tauEfficiency.EfficiencyCalculator([f]), l, p) for f, l, p in files_loose], outputDir)
    
    def dopTau(refvar, refname, xlabel, selection, opts={}, **kwargs):
        prefix = trigger+"_"+refname

        # L1 reco
        denom = selection
        num = And(denom, l1Selection)
        plotter.plotEfficiency(prefix+"_Tau1_L1Eff", refvar, num, denom, xlabel=xlabel, ylabel="L1 jet reco eff", opts=opts, **kwargs)

        # L2 jet
        denom = num
        num = And(denom, l2Selection)
        plotter.plotEfficiency(prefix+"_Tau1_L20Eff", refvar, num, denom, xlabel=xlabel, ylabel="L2 jet eff", opts=opts, **kwargs)
    
        # L25 tau
        denom = num
        num = And(denom, l25Selection_reco)
        plotter.plotEfficiency(prefix+"_Tau1_L25Eff_1Reco", refvar, num, denom, xlabel=xlabel, ylabel="L2.5 tau reco eff", opts=opts, **kwargs)

        #opts_ = {"ymin": 0.5, "ymax": 1.05}
        #opts_.update(opts)
        denom = num
        num = And(denom, l25Selection_trackFound)
        plotter.plotEfficiency(prefix+"_Tau1_L25Eff_2TrackFound", refvar, num, denom, xlabel=xlabel, ylabel="L2.5 track finding eff", opts=opts, **kwargs)

        denom = num
        num = And(denom, l25Selection_pt)
        plotter.plotEfficiency(prefix+"_Tau1_L25Eff_3Pt", refvar, num, denom, xlabel=xlabel, ylabel="L2.5 tau pt cut eff", opts=opts, **kwargs)

        denom = num
        num = And(denom, l25Selection_trackPt)
        plotter.plotEfficiency(prefix+"_Tau1_L25Eff_3TrackPt", refvar, num, denom, xlabel=xlabel, ylabel="L2.5 track pt cut eff", opts=opts, **kwargs)

        # L3 eff
        opts_ = {}
        #opts_ = {"ymin": 0.5, "ymax": 1.05}
        opts_.update(opts)
        denom = num
        num = And(denom, isoToMedium(l3SelectionIso, mediumIsolation))
        plotter.plotEfficiency(prefix+"_Tau1_L3Eff_1Isolation", refvar, num, denom, xlabel=xlabel, ylabel="L3 tau isolation eff", opts=opts_, **kwargs)

        denom = num
        num = And(denom, l3SelectionProng)
        plotter.plotEfficiency(prefix+"_Tau1_L3Eff_2Prong", refvar, num, denom, xlabel=xlabel, ylabel="L3 tau prong eff", opts=opts_, **kwargs)

        # HLT eff
        denom = selection
        num = And(denom, l2Selection, l25Selection, isoToMedium(l3Selection, mediumIsolation))
        plotter.plotEfficiency(prefix+"_Tau2_HLTEff", refvar, num, denom, xlabel=xlabel, ylabel="HLT tau eff", opts=opts, **kwargs)

        # L1+HLT eff
        denom = selection
        num = And(denom, l1Selection, l2Selection, l25Selection, isoToMedium(l3Selection, mediumIsolation))
        plotter.plotEfficiency(prefix+"_Tau3_L1HLTEff", refvar, num, denom, xlabel=xlabel, ylabel="L1+HLT tau eff", opts=opts, **kwargs)

    def dopMet(refvar, refname, xlabel, selection, opts={}, **kwargs):
        prefix = trigger+"_"+refname

        # L1
        denom = selection
        num = And(denom, l1MetSelection)
        moveLegend = {}
        if refname == "NPV":
            moveLegend = {"dx": -0.1, "dy": -0.2}
        plotter.plotEfficiency(prefix+"_Met1_L1Eff", refvar, num, denom, xlabel=xlabel, ylabel="L1_ETM eff", opts=opts, moveLegend=moveLegend, **kwargs)

        # L2
        denom = num
        num = And(denom, l2MetSelection)
        if refname == "NPV":
            moveLegend={"dx": -0.1, "dy": -0.2}
        plotter.plotEfficiency(prefix+"_Met1_L2Eff", refvar, num, denom, xlabel=xlabel, ylabel="L2 MET eff", opts=opts, moveLegend=moveLegend, **kwargs)

        # L1+HLT eff
        denom = selection
        num = And(denom, l1MetSelection, l2MetSelection)
        if refname == "NPV":
            {"dx": -0.1, "dy": 0.4}
        plotter.plotEfficiency(prefix+"_Met2_L1HLTEff", refvar, num, denom, xlabel=xlabel, ylabel="L1+HLT MET eff", opts=opts, moveLegend=moveLegend, **kwargs)


    if len(pickEvents) != 0:
        print triggerMet
        for p in [plotter,
#                  plotter_noPV, plotter_vertexSelector
                  ]:
            p.printEfficiency("Sum$(%s)>=1" % And(offlineSelection, l1Selection, l2Selection, l25Selection, l3Selection, l3SelectionProngs, l1MetSelection, l2MetSelection),
                              "Sum$(%s)>=1" % offlineSelection)

#    dopTau("PFTauPt>>hnumpt", "PFTauPt", xlabel_pt, offlineSelection, opts={"xmin": 0}, cutLine=[40])
#    dopTau("numGoodOfflinePV>>hnumpv", "NPV", xlabel_npv, And("PFTauPt>40", offlineSelection))

#    dopMet("PFMET_ET>>hnummet", "PFMET", xlabel_met, offlineEventSelection, opts={"xmin": 0}, cutLine=[50])
#    dopMet("numGoodOfflinePV>>hnumpv", "NPV", xlabel_npv, And("PFMET_ET>50", offlineEventSelection))


def doPlots2(sample):
    inputFile = dc_loose_noPV[sample][0]
    plotter = Plotter2(tauEfficiency.EfficiencyCalculator([inputFile]), outputDir)

    # L2 jet ET threshold
    denom = And(offlineSelection, l1Selection)
    plotter.plotEfficiency(sample+"L2JetEt_PFTauPt", "PFTauPt>>hnumpt", [
            (And(denom, l2Selection_template%20), denom, "L2 jet E_{T} > 20", style90_32),
            (And(denom, l2Selection_template%25), denom, "L2 jet E_{T} > 25", style160_32),
            (And(denom, l2Selection_template%35), denom, "L2 jet E_{T} > 35", style5),
            ],
                           xlabel=xlabel_pt, ylabel="L2 jet eff",
                           opts={"xmin": 0, "ymin": 0.5, "ymax": 1.05}, cutLine=[40])

    
    # Global vs. regional clusterization
    # plotterGlob = Plotter([
    #         (tauEfficiency.EfficiencyCalculator([inputFile.replace("hltpftaumedium", "hltpftaumediuml2global")]), "Global clusterization (L2 eff)", style90_32),
    #         (tauEfficiency.EfficiencyCalculator([inputFile]), "Regional clusterization (L1+L2 eff)", style160_32),
    #         ], outputDir)

    # plotterGlob.plotEfficiency2(sample+"L2JetClusterization_PFTauPt", "PFTauPt>>hnumpt",
    #                             [And(offlineSelection, l2Selection_template%25), 
    #                              And(offlineSelection, l1Selection, l2Selection_template%25)
    #                              ],
    #                             [offlineSelection, offlineSelection],
    #                             xlabel=xlabel_pt, ylabel="(L1+)L2 jet eff", opts={"xmin": 0, "ymin": 0.5, "ymax": 1.05}, cutLine=[40], moveLegend={"dx": -0.15})


    # Prongs
    denom = And(offlineSelection, l1Selection, l2Selection_template%25, l25Selection_template%35, l3SelectionIso)
    denom = denom.replace("&&PFTauProng == 1", "")
#    print denom
    plotter.plotDistribution(sample+"NProngs", "L25TauProng>>tmp(6,0,6)", [
        (And(denom, "PFTauProng == 1"), "HPS 1 prong", style90_32),
        (And(denom, "PFTauProng == 3"), "HPS 3 prong", style160_32),
#        (And(denom, "PFTauProng != 1 && PFTauProng != 3"), "HPS other", style5),
        ],
                             xlabel="Number of L2.5 PFTau signal tracks", ylabel="MC events")

    plotter.plotEfficiency(sample+"NProngs_PFTauPt", "PFTauPt>>hnumpt", [
        (And(denom, "L25TauProng <= 3"), denom, "L2.5 prong #leq 3", style90_32),
        (And(denom, "L25TauProng <= 4"), denom, "L2.5 prong #leq 4", style160_32),
        ],
                           xlabel=xlabel_pt, ylabel="Prong eff", opts={"xmin": 0, "ymin": 0.8, "ymax": 1.05}, cutLine=[40])

    denom = And(denom, "PFTauPt>40")
    plotter.plotEfficiency(sample+"NProngs_NPV", "numGoodOfflinePV>>hnumpv", [
        (And(denom, "L25TauProng <= 2"), denom, "L2.5 prong #leq 2", style5),
        (And(denom, "L25TauProng <= 3"), denom, "L2.5 prong #leq 3", style90_32),
        (And(denom, "L25TauProng <= 4"), denom, "L2.5 prong #leq 4", style160_32),
        ],
                           xlabel=xlabel_npv, ylabel="Prong eff", opts={"xmin": 0, "ymin": 0.7, "ymax": 1.05})

    denom = And(denom, "PFTauProng == 1")
    plotter.plotEfficiency(sample+"NProngs_Prong1_PFTauPt", "PFTauPt>>hnumpt", [
        (And(denom, "L25TauProng <= 2"), denom, "L2.5 prong #leq 2", style5),
        (And(denom, "L25TauProng <= 3"), denom, "L2.5 prong #leq 3", style90_32),
        (And(denom, "L25TauProng <= 4"), denom, "L2.5 prong #leq 4", style160_32),
        ],
                           xlabel=xlabel_pt, ylabel="Prong eff", opts={"xmin": 0, "ymin": 0.7, "ymax": 1.05}, cutLine=[40])

    denom = And(denom)
    plotter.plotEfficiency(sample+"NProngs_Prong1_NPV", "numGoodOfflinePV>>hnumpv", [
        (And(denom, "L25TauProng <= 2"), denom, "L2.5 prong #leq 2", style5),
        (And(denom, "L25TauProng <= 3"), denom, "L2.5 prong #leq 3", style90_32),
        (And(denom, "L25TauProng <= 4"), denom, "L2.5 prong #leq 4", style160_32),
        ],
                           xlabel=xlabel_npv, ylabel="Prong eff", opts={"xmin": 0, "ymin": 0.7, "ymax": 1.05})

    # Leading track pT
    denom = And(offlineSelection, l1Selection, l2Selection_template%25, l25Selection_reco, l25Selection_pt_template%35, l25Selection_trackFound, l3Selection)
    plotter.plotEfficiency(sample+"LeadTrackPt_PFTauPt", "PFTauPt>>hnumpt", [
        (And(denom, l25Selection_trackPt_template%10), denom, "L2.5 leading track p_{T} < 10", style90_32),
        (And(denom, l25Selection_trackPt_template%15), denom, "L2.5 leading track p_{T} < 15", style160_32),
        (And(denom, l25Selection_trackPt_template%20), denom, "L2.5 leading track p_{T} < 20", style5),
        ],
                           xlabel=xlabel_pt, ylabel="Prong eff", opts={"xmin": 0, "ymin": 0.8, "ymax": 1.05}, cutLine=[40])
    plotter.plotEfficiency(sample+"LeadTrackPt_NPV", "numGoodOfflinePV>>hnumpt", [
        (And(denom, l25Selection_trackPt_template%10), denom, "L2.5 leading track p_{T} < 10", style90_32),
        (And(denom, l25Selection_trackPt_template%15), denom, "L2.5 leading track p_{T} < 15", style160_32),
        (And(denom, l25Selection_trackPt_template%20), denom, "L2.5 leading track p_{T} < 20", style5),
        ],
                           xlabel=xlabel_npv, ylabel="Leading track pT eff", opts={"xmin": 0, "ymin": 0.8, "ymax": 1.05}, cutLine=[40])


    # Vertex tests
    # denom = And(offlineSelection, l1Selection, l2Selection_template%25, l25Selection_reco, "PFTauPt>40")
    # num = And(denom, l25Selection_trackFound)
    # plotterVertex = Plotter([
    #         (tauEfficiency.EfficiencyCalculator([dc_loose[sample][0]]), "Default", style90_32),
    #         (tauEfficiency.EfficiencyCalculator([dc_loose_noPV[sample][0]]), "Without vertex requirement", style160_32),
    #         (tauEfficiency.EfficiencyCalculator([dc_loose_vertexSelector[sample][0]]), "Vertex by lead. track", style5)
    #         ], outputDir)
    # plotterVertex.plotEfficiency2(sample+"L25TauLeadingTrackFinding_NPV", "numGoodOfflinePV>>hnumpv",
    #                               [num, num, And(num, "L25Tau_VertexSelection")],
    #                               [denom, denom, denom],
    #                               xlabel=xlabel_npv, ylabel="L2.5 track finding eff", opts={"ymin": 0.8, "ymax": 1.05})


    # Isolation
    # denom = And(offlineSelection, l1Selection, l2Selection_template%25, l25Selection_template%35, "PFTauPt>40")
    # plotter.plotEfficiency(sample+"L3Isolation_NPV", "numGoodOfflinePV>>hnumpv", [
    #         (And(denom, l3SelectionIso), denom, "L3 MediumIsolation", style90_32),
    #         (And(denom, "primaryVertexIsValid && L25TauIsoChargedHadrCandPtMax < 1.0"), denom, "L3 iso ch p_{T} > 1.0", style160_32),
    #         (And(denom, "primaryVertexIsValid && L25TauIsoChargedHadrCandPtMax < 1.5"), denom, "L3 iso ch p_{T} > 1.5", style5),
    #         (And(denom, "primaryVertexIsValid && L25TauIsoChargedHadrCandPtMax < 2.0"), denom, "L3 iso ch p_{T} > 2.0", style6),
    #         ],
    #                        xlabel=xlabel_npv, ylabel="L3 isolation eff", opts={"xmin": 0, "ymin": 0.5, "ymax": 1.05})

    # plotterIsolation = Plotter([
    #         (tauEfficiency.EfficiencyCalculator([dc_medium_noPV[sample][0]]), "L3 MediumIsolation", style90_32),
    #         (tauEfficiency.EfficiencyCalculator([dc_loose_noPV[sample][0]]), "L3 LooseIsolation", style160_32),
    #         ], outputDir)
    # plotterIsolation.plotEfficiency2(sample+"L3Isolation2_NPV", "numGoodOfflinePV>>hnumpv",
    #         [And(denom, "L25Tau_MediumIso"), And(denom, "L25Tau_LooseIso")],
    #         [denom, denom],
    #         xlabel=xlabel_npv, ylabel="L3 isolation eff", opts={"ymin": 0.6, "ymax": 1.05})

    # denom = And(offlineSelection, "L25TauProng <= 4", "PFTauPt>40")
    # numMedium = And(denom, l1Selection, l2Selection_template%25, l25Selection_template%35)
    # numLoose = And(numMedium, "L25Tau_LooseIso")
    # numMedium = And(numMedium, "L25Tau_MediumIso")
    # plotterIsolation.plotEfficiency2(sample+"Full_NPV", "numGoodOfflinePV>>hnumpv",
    #                                  [numMedium, numLoose],
    #                                  [denom, denom],
    #                                  xlabel=xlabel_npv, ylabel="L1+HLT eff", opts={"ymin": 0.5, "ymax": 1.05})



    # L1_ETM threshold
    denom = offlineEventSelection
    denom = denom.replace("PFTauPt", "PFTauProng <= 4 && PFTauPt")  
    plotter.plotEfficiency(sample+"L1ETM_PFMET", "PFMET_ET>>hnummet", [
            (And("L1MET>30", denom), denom, "L1_ETM30", style90_32),
            (And("L1MET>36", denom), denom, "L1_ETM36", style160_32),
            (And("L1MET>40", denom), denom, "L1_ETM40", style5),
            ],
                           xlabel=xlabel_met, ylabel="L1_ETM eff",
                           cutLine=[50]
                           )

    denom2 = And(offlineEventSelection, "PFMET_ET>50")
    plotter.plotEfficiency(sample+"L1ETM_NPV", "numGoodOfflinePV>>hnumpv", [
            (And("L1MET>30", denom2), denom2, "L1_ETM30", style90_32),
            (And("L1MET>36", denom2), denom2, "L1_ETM36", style160_32),
            (And("L1MET>40", denom2), denom2, "L1_ETM40", style5),
            ],
                           xlabel=xlabel_npv, ylabel="L1_ETM eff",
                           )

    # plotter.plotEfficiency(sample+"L1ETM_HLTMET", "HLTMET_ET>>hnummet", [
    #         (And("L1MET>30", denom), denom, "L1_ETM30", style90_32),
    #         (And("L1MET>36", denom), denom, "L1_ETM36", style160_32),
    #         (And("L1MET>40", denom), denom, "L1_ETM40", style5),
    #         ],
    #                        xlabel="HLT E_{T}^{miss} (GeV)", ylabel="L1_ETM eff",
    #                        )

    # plotter.plotEfficiency(sample+"L1ETM_HLTPFHMT", "HLTMHT_ET>>hnummet", [
    #         (And("L1MET>30", denom), denom, "L1_ETM30", style90_32),
    #         (And("L1MET>36", denom), denom, "L1_ETM36", style160_32),
    #         (And("L1MET>40", denom), denom, "L1_ETM40", style5),
    #         ],
    #                        xlabel="HLT PFMHT (GeV)", ylabel="L1_ETM eff",
    #                        )
                           
    # MET threshold
    plotter.plotEfficiency(sample+"L1ETM_MET_PFMHT_PFMET", "PFMET_ET>>hnummet",[
            (And(denom, "L1MET>40 && HLTMET_ET>60"), denom, "L1_ETM40 & MET > 60", style90_32),
            (And(denom, "L1MET>40 && HLTMET_ET>70"), denom, "L1_ETM40 & MET > 70", style160_32),
            (And(denom, "L1MET>40 && HLTMHT_ET>60"), denom, "L1_ETM40 & PFMHT > 60", style5),
            (And(denom, "L1MET>40 && HLTMHT_ET>70"), denom, "L1_ETM40 & PFMHT > 70", style6),
            ],
                           xlabel=xlabel_met, ylabel="MET/PFMHT eff",
                           cutLine=[50], moveLegend={"dy": -0.1}
                           )
    plotter.plotEfficiency(sample+"L1ETM_MET_PFMHT1_NPV", "numGoodOfflinePV>>hnumpv",[
            (And(denom2, "L1MET>40 && HLTMET_ET>60"), denom2, "L1_ETM40 & MET > 60", style90_32),
            (And(denom2, "L1MET>40 && HLTMET_ET>70"), denom2, "L1_ETM40 & MET > 70", style160_32),
            (And(denom2, "L1MET>40 && HLTMHT_ET>60"), denom2, "L1_ETM40 & PFMHT > 60", style5),
            (And(denom2, "L1MET>40 && HLTMHT_ET>70"), denom2, "L1_ETM40 & PFMHT > 70", style6),
            ],
                           xlabel=xlabel_npv, ylabel="MET/PFMHT eff",
                           moveLegend={"dy": -0.1}
                           )

    plotter.plotEfficiency(sample+"L1ETM_MET_PFMHT2_PFMET", "PFMET_ET>>hnummet",[
            (And(denom, "L1MET>30 && HLTMET_ET>70"), denom, "L1_ETM30 & MET > 70", style90_32),
            (And(denom, "L1MET>36 && HLTMET_ET>70"), denom, "L1_ETM36 & MET > 70", style160_32),
            (And(denom, "L1MET>40 && HLTMET_ET>70"), denom, "L1_ETM40 & MET > 70", style5),
            ],
                           xlabel=xlabel_met, ylabel="MET/PFMHT eff",
                           cutLine=[50], moveLegend={"dy": -0.1}
                           )
    plotter.plotEfficiency(sample+"L1ETM_MET_PFMHT2_NPV", "numGoodOfflinePV>>hnumpv",[
            (And(denom2, "L1MET>30 && HLTMET_ET>70"), denom2, "L1_ETM30 & MET > 70", style90_32),
            (And(denom2, "L1MET>36 && HLTMET_ET>70"), denom2, "L1_ETM36 & MET > 70", style160_32),
            (And(denom2, "L1MET>40 && HLTMET_ET>70"), denom2, "L1_ETM40 & MET > 70", style5),
            ],
                           xlabel=xlabel_npv, ylabel="MET/PFMHT eff",
                           moveLegend={"dy": -0.1}
                           )

    plotter.plotEfficiency(sample+"L1ETM_METPFMHT_PFMET", "PFMET_ET>>hnummet",[
            (And(denom, "L1MET>40 && HLTMET_ET>20 && HLTMHT_ET > 60"), denom, "L1_ETM40 & MET20 & PFMHT60", style90_32),
            (And(denom, "L1MET>40 && HLTMET_ET>30 && HLTMHT_ET > 60"), denom, "L1_ETM40 & MET30 & PFMHT60", style160_32),
            (And(denom, "L1MET>40 && HLTMET_ET>40 && HLTMHT_ET > 60"), denom, "L1_ETM40 & MET40 & PFMHT60", style5),
            (And(denom, "L1MET>40 && HLTMET_ET>70"), denom, "L1_ETM40 & MET70 (ref)", style6),
            ],
                           xlabel=xlabel_met, ylabel="MET/PFMHT eff",
                           cutLine=[50], moveLegend={"dy": -0.1}
                           )

    denom = And(denom, "L1MET>40")
    plotter.plotEfficiency(sample+"MET_PFMHT_PFMET", "PFMET_ET>>hnummet",[
            (And(denom, "HLTMET_ET>60"), denom, "MET > 60", style90_32),
            (And(denom, "HLTMET_ET>70"), denom, "MET > 70", style160_32),
            (And(denom, "HLTMHT_ET>60"), denom, "PFMHT > 60", style5),
            (And(denom, "HLTMHT_ET>70"), denom, "PFMHT > 70", style6),
            ],
                           xlabel=xlabel_met, ylabel="MET/PFMHT eff",
                           cutLine=[50]
                           )


class Plotter:
    def __init__(self, inputList, plotDir):
        self.inputList = inputList
        self.plotDir = plotDir

        if not os.path.exists(plotDir):
            os.mkdir(plotDir)

    def plotEfficiency(self, name, varexp, numerator, denominator, opts={}, **kwargs):
        effs = []
        for i, (calc, legendLabel, plotStyle) in enumerate(self.inputList):
            den = calc.getRootHisto(varexp, denominator)
            num = calc.getRootHisto(varexp, numerator)

            eff = ROOT.TGraphAsymmErrors(num, den)
            plotStyle.apply(eff)
            gr = histograms.HistoGraph(eff, "Eff%d", "p", "EP")
            gr.setLegendLabel(legendLabel)

            effs.append(gr)
            
        p = plots.PlotBase(effs, saveFormats=[".png"])

        opts_ = {"ymin": 0, "ymax": 1.1}
        opts_.update(opts)

        drawPlot(p, os.path.join(self.plotDir, name), opts=opts_, **kwargs)

    def plotEfficiency2(self, name, varexp, numerators, denominators, opts={}, **kwargs):
        effs = []
        for i, (calc, legendLabel, plotStyle) in enumerate(self.inputList):
            den = calc.getRootHisto(varexp, denominators[i])
            num = calc.getRootHisto(varexp, numerators[i])

            eff = ROOT.TGraphAsymmErrors(num, den)
            plotStyle.apply(eff)
            gr = histograms.HistoGraph(eff, "Eff%d", "p", "EP")
            gr.setLegendLabel(legendLabel)

            effs.append(gr)
            
        p = plots.PlotBase(effs, saveFormats=[".png"])

        opts_ = {"ymin": 0, "ymax": 1.1}
        opts_.update(opts)

        drawPlot(p, os.path.join(self.plotDir, name), opts=opts_, **kwargs)

    def printEfficiency(self, numerator, denominator):
        for calc, legendLabel, plotStyle in self.inputList:
            den = float(calc.getEntries(denominator))
            num = float(calc.getEntries(numerator))
            
            nden = dataset.Count(den, math.sqrt(den))
            nnum = dataset.Count(num, math.sqrt(num))
            nnum.divide(nden)

            print "%s: %.2f +- %.2f %%  (%.0f/%.0f)" % (legendLabel, nnum.value()*100, nnum.uncertainty()*100, num, den)

class Plotter2:
    def __init__(self, calc, plotDir):
        self.calc = calc
        self.plotDir = plotDir
        if not os.path.exists(plotDir):
            os.mkdir(plotDir)

    def plotEfficiency(self, name, varexp, definitions, opts={}, **kwargs):
        effs = []
        for i, (numerator, denominator, legendLabel, plotStyle) in enumerate(definitions):
            den = self.calc.getRootHisto(varexp, denominator)
            num = self.calc.getRootHisto(varexp, numerator)

            eff = ROOT.TGraphAsymmErrors(num, den)
            plotStyle.apply(eff)
            gr = histograms.HistoGraph(eff, "Eff%d", "p", "EP")
            gr.setLegendLabel(legendLabel)

            effs.append(gr)

        p = plots.PlotBase(effs, saveFormats=[".png"])
        opts_ = {"ymin": 0, "ymaxa": 1.1}
        opts_.update(opts)

        drawPlot(p, os.path.join(self.plotDir, name), opts=opts_, **kwargs)

    def plotDistribution(self, name, varexp, selections, **kwargs):
        histos = []
        for i, (selection, legendLabel, plotStyle) in enumerate(selections):
            h = self.calc.getRootHisto(varexp, selection)
            st = styles.StyleFill(plotStyle)
            st.apply(h)
            h = histograms.Histo(h, "Eff%d", legendStyle="f")
            h.setIsDataMC(False, True)
            h.setLegendLabel(legendLabel)
            histos.append(h)

        p = plots.PlotBase(histos, saveFormats=[".png"])
        names = [h.getName() for h in histos]
        #names.reverse()
        p.histoMgr.stackHistograms("Eff", names)
        drawPlot(p, os.path.join(self.plotDir, name), **kwargs)


def drawPlot(p, name, xlabel=None, ylabel=None, opts={}, moveLegend={}, cutLine=None):
    p.createFrame(name, opts=opts)
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
    if xlabel != None:
        p.frame.GetXaxis().SetTitle(xlabel)
    if ylabel != None:
        p.frame.GetYaxis().SetTitle(ylabel)

    if cutLine != None:
        lst = cutLine
        if not isinstance(lst, list):
            lst = [lst]
        for line in lst:
            p.addCutBoxAndLine(line, box=False, line=True)

    p.draw()
    p.save()


if __name__ == "__main__":
    main()
