#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedding MC
# within the tau ID. The corresponding python job
# configuration is embeddingAnalysis_cfg.py
#
# Author: Matti Kortelainen
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


analysis = "tauNtuple"
counters = analysis+"Counters"

#era = "EPS"
#era = "Run2011A-EPS"
era = "Run2011A"

# expressions
decayModeExp = "(taus_decayMode<=2)*taus_decayMode + (taus_decayMode==10)*3 +(taus_decayMode > 2 && taus_decayMode != 10)*4>>tmp(5,0,5)"
rtauExp = "(taus_leadPFChargedHadrCand_p4.P() / taus_p4.P() -1e-10)"

# tau candidate selection
decayModeFinding = "taus_decayMode >= 0" # replace with discriminator after re-running ntuples
tauPtCut = "(taus_p4.Pt() > 40)"
tauEtaCut = "(abs(taus_p4.Eta()) < 2.1)"
tauLeadPt = "(taus_leadPFChargedHadrCand_p4.Pt() > 20)"
ecalFiducial = "(!( abs(taus_p4.Eta()) < 0.18 || (0.423 < abs(taus_p4.Eta()) && abs(taus_p4.Eta()) < 0.461)"
ecalFiducial += " || (0.770 < abs(taus_p4.Eta()) && abs(taus_p4.Eta()) < 0.806)"
ecalFiducial += " || (1.127 < abs(taus_p4.Eta()) && abs(taus_p4.Eta()) < 1.163)"
ecalFiducial += " || (1.460 < abs(taus_p4.Eta()) && abs(taus_p4.Eta()) < 1.558)" # gap
ecalFiducial += "))"
electronRejection = "(taus_f_againstElectronMedium > 0.5)"
muonRejection = "(taus_f_againstMuonTight > 0.5)"

# tau ID
tightIsolation = "(taus_f_byTightIsolation > 0.5)"
oneProng = "(taus_signalPFChargedHadrCands_n == 1)"
rtau = "(%s > 0.7)" % rtauExp

tauCandidateSelection = "("+ "&&".join([decayModeFinding, tightIsolation, tauPtCut, tauEtaCut, tauLeadPt, ecalFiducial, electronRejection, muonRejection]) + ")"
tauID = "("+ "&&".join([tightIsolation, oneProng, rtau]) +")"

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
    datasets.loadLuminosities()
    plots.mergeRenameReorderForDataMC(datasets)

    # Remove signal
    datasets.remove(filter(lambda name: "TTToHplus" in name, datasets.getAllDatasetNames()))

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    histograms.createLegend.moveDefaults(dx=-0.04)
    plots._legendLabels["QCD_Pt20_MuEnriched"] = "QCD"
    #datasets.remove(["QCD_Pt20_MuEnriched"])
    #histograms.createLegend.moveDefaults(dh=-0.05)

    def createPlot(name):
        name2 = name
        if isinstance(name, basestring):
            name2 = analysis+"/"+name
        return plots.DataMCPlot(datasets, name2)

    weight = "weightPileup_Run2011A"
    if era == "EPS":
        weight = "pileupWeightEPS"
    elif era == "Run2011A-EPS":
        weight = "pileupWeight_Run2011AnoEPS"
    treeDraw = dataset.TreeDraw(analysis+"/tree", weight=weight)

    tauEmbedding.normalize=True
    tauEmbedding.era=era
    drawPlot = tauEmbedding.drawPlot

    if datasets.hasDataset("QCD_Pt20_MuEnriched"):
        datasets.remove(["QCD_Pt20_MuEnriched"])
        histograms.createLegend.moveDefaults(dh=-0.05)

    # Decay mode finding
    td=treeDraw.clone(selection="&&".join([decayModeFinding, tightIsolation]))
    postfix = "_1AfterDecayModeFindingIsolation"
    drawPlot(createPlot(td.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)")),
             "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", cutLine=40)
    drawPlot(createPlot(td.clone(varexp="taus_decayMode>>tmp(16,0,16)")),
             "tauDecayMode"+postfix+"_check", "", opts={"nbins":16}, opts2={"ymin":0.9, "ymax":1.4}, function=decayModeCheckCustomize)

    # Pt
    td=treeDraw.clone(selection="&&".join([decayModeFinding, tightIsolation, tauPtCut]))
    postfix = "_2AfterPtCut"
    drawPlot(createPlot(td.clone(varexp="taus_p4.Eta()>>tmp(25,-2.5,2.5")),
             "tauEta"+postfix, "#tau-jet candidate #eta", ylabel="Events / %.1f", opts={"ymin": 1e-1}, moveLegend={"dx": -0.2, "dy": -0.49}, cutLine=[-2.1, 2.1])
    drawPlot(createPlot(td.clone(varexp="taus_p4.Phi()>>tmp(32,-3.2,3.2")),
             "tauPhi"+postfix, "#tau-jet candidate #phi (rad)", ylabel="Events / %.1f", opts={"ymin": 1e-1}, moveLegend={"dx": -0.2, "dy": -0.45})
    drawPlot(createPlot(td.clone(varexp=decayModeExp)),
             "tauDecayMode"+postfix+"", "", opts={"ymin": 1, "ymaxfactor": 20, "nbins":5}, opts2={"ymin":0.9, "ymax":1.4}, moveLegend={"dy": 0.02, "dh": -0.02}, function=decayModeCustomize)

    # Eta
    td=treeDraw.clone(selection="&&".join([decayModeFinding, tightIsolation, tauPtCut, tauEtaCut]))
    postfix = "_3AfterEtaCut"
    drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.Pt()>>tmp(25,0,250)")),
             "tauLeadingTrackPt"+postfix, "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts2={"ymin":0, "ymax": 2}, cutLine=20)

    # Tau candidate selection
    td=treeDraw.clone(selection=tauCandidateSelection)
    postfix = "_4AfterTauCandidateSelection"
    drawPlot(createPlot(td.clone(varexp=decayModeExp)),
             "tauDecayMode"+postfix+"", "", opts={"ymin": 1e-2, "ymaxfactor": 20, "nbins":5}, opts2={"ymin":0, "ymax":2}, moveLegend={"dy": 0.02, "dh": -0.02}, function=decayModeCustomize)

    # Isolation + one prong
    td = treeDraw.clone(selection="&&".join([tauCandidateSelection, tightIsolation, oneProng]))
    postfix = "_5AfterOneProng"
    drawPlot(createPlot(td.clone(varexp="taus_p4.Pt()>>tmp(25,0,250)")),
             "tauPt"+postfix, "#tau-jet candidate p_{T} (GeV/c)", opts2={"ymin": 0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="taus_p4.P()>>tmp(25,0,250)")),
             "tauP"+postfix, "#tau-jet candidate p (GeV/c)", opts2={"ymin": 0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.Pt()>>tmp(25,0,250)")),
             "tauLeadingTrackPt"+postfix, "#tau-jet ldg. charged particle p_{T} (GeV/c)", opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp="taus_leadPFChargedHadrCand_p4.P()>>tmp(25,0,250)")),
             "tauLeadingTrackP"+postfix, "#tau-jet ldg. charged particle p (GeV/c)", opts2={"ymin":0, "ymax": 2})
    drawPlot(createPlot(td.clone(varexp=rtauExp+">>tmp(22, 0, 1.1)")),
             "rtau"+postfix, "R_{#tau} = p^{ldg. charged particle}/p^{#tau jet}", ylabel="Events / %.1f", opts={"ymin": 5e-2, "ymaxfactor": 20}, moveLegend={"dx":-0.48}, cutLine=0.7)

    # Full id
    td = treeDraw.clone(selection="&&".join([tauCandidateSelection, tauID]))
    postfix = "_6AfterTauID"
    drawPlot(createPlot(td.clone(varexp=decayModeExp)),
             "tauDecayMode"+postfix+"", "", opts={"ymin": 1e-2, "ymaxfactor": 20, "nbins":5}, opts2={"ymin":0, "ymax":3}, moveLegend={"dy": 0.02, "dh": -0.02}, function=decayModeCustomize)


def decayModeCheckCustomize(h):
    n = 16
    if hasattr(h, "getFrame1"):
        h.getFrame1().GetXaxis().SetNdivisions(n)
        h.getFrame1().GetXaxis().SetNdivisions(n)
    else:
        h.getFrame().GetXaxis().SetNdivisions(n)

    xaxis = h.getFrame().GetXaxis()
    xaxis.SetBinLabel(1, "#pi^{#pm}")
    xaxis.SetBinLabel(2, "#pi^{#pm}#pi^{0}")
    xaxis.SetBinLabel(3, "#pi^{#pm}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(4, "#pi^{#pm}#pi^{0}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(5, "#pi^{#pm} N#pi^{0}")
    xaxis.SetBinLabel(6, "#pi^{+}#pi^{-}")
    xaxis.SetBinLabel(7, "#pi^{+}#pi^{-}#pi^{0}")
    xaxis.SetBinLabel(8, "#pi^{+}#pi^{-}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(9, "#pi^{+}#pi^{-}#pi^{0}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(10, "#pi^{+}#pi^{-} N#pi^{0}")
    xaxis.SetBinLabel(11, "#pi^{+}#pi^{-}#pi^{#pm}")
    xaxis.SetBinLabel(12, "#pi^{+}#pi^{-}#pi^{#pm}#pi^{0}")
    xaxis.SetBinLabel(13, "#pi^{+}#pi^{-}#pi^{#pm}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(14, "#pi^{+}#pi^{-}#pi^{#pm}#pi^{0}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(15, "#pi^{+}#pi^{-}#pi^{#pm} N#pi^{0}")
    xaxis.SetBinLabel(16, "Other")


def decayModeCustomize(h):
    n = 5
    if hasattr(h, "getFrame1"):
        h.getFrame1().GetXaxis().SetNdivisions(n)
        h.getFrame1().GetXaxis().SetNdivisions(n)
    else:
        h.getFrame().GetXaxis().SetNdivisions(n)

    xaxis = h.getFrame().GetXaxis()
    xaxis.SetBinLabel(1, "#pi^{#pm}")
    xaxis.SetBinLabel(2, "#pi^{#pm}#pi^{0}")
    xaxis.SetBinLabel(3, "#pi^{#pm}#pi^{0}#pi^{0}")
    xaxis.SetBinLabel(4, "#pi^{+}#pi^{-}#pi^{#pm}")
    xaxis.SetBinLabel(5, "Other")



if __name__ == "__main__":
    main()
