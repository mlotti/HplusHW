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
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

# These are per-muon cuts
muonKinematics = "(muons_p4.Pt() > 40 && abs(muons_p4.Eta()) < 2.1)"
muondB = "(abs(muons_f_dB) < 0.02)"
muonIsolation = "((muons_f_tauTightIc04ChargedIso + muons_f_tauTightIc04GammaIso) == 0)"
muonSelection = "(%s && %s && %s)" % (muonKinematics, muondB, muonIsolation)
muonSelectionNoIso = "(%s && %s)" % (muonKinematics, muondB)

# Construct muon veto, first the muons accepted as veto muons
muonVeto = "muons_p4.Pt() > 15 && abs(muons_p4.Eta()) < 2.5 && abs(muons_f_dB) < 0.02 && (muons_f_trackIso+muons_f_caloIso)/muons_p4.Pt() <= 0.15"
# then exclude the selected muon (this will work only after the 'one selected muon' requirement)
muonVetoNoIso = muonVeto + " && !"+muonSelectionNoIso
muonVeto += " && !"+muonSelection
# then make it a sum cut
muonVeto = "Sum$(%s) == 0" % muonVeto
muonVetoNoIso = "Sum$(%s) == 0" % muonVetoNoIso

electronVeto = "ElectronVetoPassed"

# Jet selection as per-event cut
#jetSelection = "(jets_p4.Pt() > 30 && abs(jets_p4.Eta()) < 2.4 && jets_looseId)"
# Jet cleaning
#jetSelection += ""
# Construct per-event cut
#jetSelection = "Sum$(%s) >= 3" % jetSelection
jetSelection = "jets_p4@.size() >= (3+Sum$(%s && muons_jetMinDR < 0.1))" % muonSelection
jetSelectionNoIso = "jets_p4@.size() >= (3+Sum$(%s && muons_jetMinDR < 0.1))" % muonSelectionNoIso

metcut = "pfMet_p4.Pt() > 40"

btagging = "Sum$(jets_f_tche > 1.7 && sqrt((jets_p4.Phi()-muons_p4.Phi())^2+(jets_p4.Eta()-muons_p4.Eta())^2) > 0.5) >= 1"

analysis = "muonNtuple"

#era = "EPS"
#era = "Run2011A-EPS"
era = "Run2011A"

weight = {"EPS": "pileupWeightEPS",
          "Run2011A-EPS": "weightPileup_Run2011AnoEPS",
          "Run2011A": "weightPileup_Run2011A",
          }[era]
#weight = ""

treeDraw = dataset.TreeDraw(analysis+"/tree", weight=weight)

def main():
    counters = analysis+"Counters"
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.updateNAllEventsToPUWeighted()

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
            ])
    elif era == "Run2011A":
        pass

    datasets.loadLuminosities()

    plots.mergeRenameReorderForDataMC(datasets)
    
    styleGenerator = styles.generator(fill=True)

    style = tdrstyle.TDRStyle()
    plots._legendLabels["QCD_Pt20_MuEnriched"] = "QCD"
    histograms.createLegend.moveDefaults(dx=-0.02)

    doPlots(datasets)
    printCounters(datasets)

def doPlots(datasets):
    def createPlot(name, **kwargs):
        return plots.DataMCPlot(datasets, name, **kwargs)
    drawPlot = plots.PlotDrawer(stackMCHistograms=True, addMCUncertainty=True, log=True, ratio=True, addLuminosityText=True,
                                optsLog={"ymin": 1e-1}, opts2={"ymin": 0, "ymax": 2})

    selections = [
        ("Full_", And(muonSelection, muonVeto, electronVeto, jetSelection)),
        ("FullNoIso_", And(muonSelectionNoIso, muonVetoNoIso, electronVeto, jetSelectionNoIso)),
#        ("Analysis_", "&&".join([muonSelection, muonVeto, electronVeto, jetSelection, metcut, btagging])),
        ]

    for name, selection in selections:
        tdMuon = treeDraw.clone(selection=selection)


        td = tdMuon.clone(varexp="muons_p4.Pt() >>tmp(40,0,400)")
        drawPlot(createPlot(td), name+"muon_pt_log", "Muon p_{T} (GeV/c)", ylabel="Events / %.0f GeV/c", cutBox={"cutValue":40, "greaterThan":True})

        td = tdMuon.clone(varexp="pfMet_p4.Pt() >>tmp(40,0,400)")
        drawPlot(createPlot(td), name+"met_log", "E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV")

        td = tdMuon.clone(varexp="sqrt(2 * muons_p4.Pt() * pfMet_p4.Et() * (1-cos(muons_p4.Phi()-pfMet_p4.Phi()))) >>tmp(40,0,400)")
        drawPlot(createPlot(td), name+"mt_log", "m_{T}(#mu, E_{T}^{miss}) (GeV/c^{2})", ylabel="Events / %.0f GeV/c^{2}")

def printCounters(datasets):
    print "============================================================"
    print "Dataset info: "
    datasets.printInfo()

    eventCounter = counter.EventCounter(datasets)
    selection = "Sum$(%s) >= 1" % muonKinematics
    selection = "Sum$(%s && %s) >= 1" % (muonKinematics, muondB)
    selection = "Sum$(%s && %s && %s) >= 1" % (muonKinematics, muondB, muonIsolation)
    selection = "Sum$(%s && %s && %s) == 1" % (muonKinematics, muondB, muonIsolation)
    selection += "&&" +muonVeto
    selection += "&&" +electronVeto
    selection += "&&" +jetSelection
    eventCounter.getMainCounter().appendRow("Selected control sample", treeDraw.clone(selection=selection))

    eventCounter.normalizeMCByLuminosity()

    table = eventCounter.getMainCounterTable()
    mcDatasets = filter(lambda n: n != "Data", table.getColumnNames())
    table.insertColumn(1, counter.sumColumn("MCSum", [table.getColumn(name=name) for name in mcDatasets]))

    table.keepOnlyRows("Selected control sample")
    # reorder columns
    qcd = table.getColumn(name="QCD_Pt20_MuEnriched")
    table.removeColumn(table.getColumnNames().index("QCD_Pt20_MuEnriched"))
    table.insertColumn(5, qcd)

    table.transpose()

    # result = counter.CounterTable()
    # def addRow(name, value):
    #     result.appendRow(counter.CounterRow(name, ["Number of events"], [value]))
    # for name in ["Data", "MCSum", "WJets", "TTJets", "DYJetsToLL", "QCD_Pt20_MuEnriched", "SingleTop", "Diboson"]:
    #     addRow(name, table.getColumn(name=name).getCount(0))

    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.1f'))
    print table.format(cellFormat)


if __name__ == "__main__":
    main()
