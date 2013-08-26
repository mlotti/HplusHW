#!/usr/bin/env python

######################################################################
#
# The ntuple files should come from the TTEff2 code
#
# Needs ROOT >= 5.30 (for TEfficiency)
#
# Author: Matti Kortelainen
# Modified 18052012/S.Lehti
# Modified 20062012/S.Lehti
#
######################################################################

import os
import array
import re
import sys

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or

DATAPATH = "/home/slehti/public/Trigger/TriggerEfficiency/data"

from PythonWriter import PythonWriter

pythonWriter = PythonWriter()

def main():
    style = tdrstyle.TDRStyle()

    histograms.createLegend.moveDefaults(dh=-0.2)

    puWeights = []
    puWeights.append("pileupWeight_2012ABC.C")
    puWeights.append("pileupWeight_2012AB.C")
    puWeights.append("pileupWeight_2012A.C")
    puWeights.append("pileupWeight_2012B.C")
    puWeights.append("pileupWeight_2012C.C")
    puWeights.append("pileupWeight_Unweighted.C")

    puWeightPath = "src/HiggsAnalysis/TriggerEfficiency/test"

    highPurity = True
####    highPurity = False

    ### Offline selection definition
    """
    offlineSelection = "PFTauPt > 20 && abs(PFTauEta) < 2.1"
    offlineSelection += "&& PFTauLeadChargedHadrCandPt > 20"
    offlineSelection += "&& PFTauProng == 1"
#    offlineSelection += "&& PFTau_againstElectronMedium > 0.5 && PFTau_againstMuonTight > 0.5"
    offlineSelection += "&& PFTau_againstElectronMVA > 0.5 && PFTau_againstMuonTight > 0.5"
#    offlineSelection += "&& byTightIsolation > 0.5"
#    offlineSelection += "&& byVLooseCombinedIsolationDeltaBetaCorr > 0.5"
#    offlineSelection += "&& byLooseCombinedIsolationDeltaBetaCorr > 0.5"
    offlineSelection += "&& PFTau_byMediumCombinedIsolationDeltaBetaCorr > 0.5"
    offlineSelection += "&& MuonTauInvMass < 80"
    """
    ### Offline selection definition (H+)                                                                         
    offlineSelectionHPlusBase = "PFTauPt > 20 && abs(PFTauEta) < 2.1"
    offlineSelectionHPlusBase += "&& PFTauLeadChargedHadrCandPt > 20"
    offlineSelectionHPlusBase += "&& PFTauProng == 1"
    offlineSelectionHPlusBase += "&& PFTau_againstMuonTight > 0.5"
    offlineSelectionHPlusBase += "&& MuonTauInvMass < 80"

    offlineSelectionMediumMedium = offlineSelectionHPlusBase
    offlineSelectionMediumMedium+= "&& PFTau_againstElectronMedium > 0.5"
    offlineSelectionMediumMedium+= "&& PFTau_byMediumCombinedIsolationDeltaBetaCorr > 0.5"

    offlineSelectionMediumMVA = offlineSelectionHPlusBase
    offlineSelectionMediumMVA+= "&& PFTau_againstElectronMVA > 0.5"
    offlineSelectionMediumMVA+= "&& PFTau_byMediumCombinedIsolationDeltaBetaCorr > 0.5"

    offlineSelectionLooseMedium = offlineSelectionHPlusBase
    offlineSelectionLooseMedium+= "&& PFTau_againstElectronMedium > 0.5"
    offlineSelectionLooseMedium+= "&& PFTau_byLooseCombinedIsolationDeltaBetaCorr > 0.5"

    offlineSelectionLooseMVA = offlineSelectionHPlusBase
    offlineSelectionLooseMVA+= "&& PFTau_againstElectronMVA > 0.5"
    offlineSelectionLooseMVA+= "&& PFTau_byLooseCombinedIsolationDeltaBetaCorr > 0.5"

    #### W(taunu)H(bb) analysis Segala, Zenz, Narain

    offlineSelectionWtaunuHbb = "PFTauPt > 20 && abs(PFTauEta) < 2.1"
    offlineSelectionWtaunuHbb += "&& PFTauLeadChargedHadrCandPt > 20"
    offlineSelectionWtaunuHbb += "&& PFTau_againstElectronLoose > 0.5 && PFTau_againstMuonTight > 0.5"
    offlineSelectionWtaunuHbb += "&& PFTau_byLooseCombinedIsolationDeltaBetaCorr > 0.5"
    offlineSelectionWtaunuHbb += "&& PFTau_decayModeFinding > 0.5"


    offlineSelections = []
    offlineSelections.append(namedselection("byMediumCombinedIsolationDeltaBetaCorr_againstElectronMedium",offlineSelectionMediumMedium))
    offlineSelections.append(namedselection("byMediumCombinedIsolationDeltaBetaCorr_againstElectronMVA",offlineSelectionMediumMVA))
    offlineSelections.append(namedselection("byLooseCombinedIsolationDeltaBetaCorr_againstElectronMVA",offlineSelectionLooseMVA))
    offlineSelections.append(namedselection("byLooseCombinedIsolationDeltaBetaCorr_againstElectronMedium",offlineSelectionLooseMedium))

    pu_re = re.compile("pileupWeight_(?P<scenario>(\S+))\.C")
    for puWeight in puWeights:
        pyScenario = pu_re.search(puWeight)
        match = pu_re.search(puWeight)
        if match:
            pyScenario = match.group("scenario")

            if pyScenario != "Unweighted":
                ROOT.gROOT.Clear()
                ROOT.gROOT.Reset()
                macroPath = os.path.join(os.environ["CMSSW_BASE"], puWeightPath, puWeight+"+")
                macroPath = macroPath.replace("../src/","")
                macroPath = macroPath.replace("HiggsAnalysis/TriggerEfficiency/test/../../../","")

                ROOT.gROOT.LoadMacro(macroPath)

            for selection in offlineSelections:

                pythonWriter.SaveOfflineSelection(selection)

                doPlots(6,highPurity=highPurity,selection=selection,pyScenario=pyScenario)
                doPlots(7,highPurity=highPurity,selection=selection,pyScenario=pyScenario)
                doPlots(8,highPurity=highPurity,selection=selection,pyScenario=pyScenario)
                doPlots(10,highPurity=highPurity,selection=selection,pyScenario=pyScenario)
                doPlots(11,highPurity=highPurity,selection=selection,pyScenario=pyScenario)

    pythonWriter.write("tauLegTriggerEfficiency2012_cff.py")
#    pythonWriter.sysError()

def namedselection(name,selection):
    namedSelection = []
    namedSelection.append(name)
    namedSelection.append(selection)
    return namedSelection

def doPlots(runrange, selection, dataVsMc=True, highPurity=True, dataMcSameTrigger=False, pyScenario="Unweighted"):

    selectionName    = selection[0]
    offlineSelection = selection[1]

    if runrange < 6:
        histograms.energyText = "7 TeV"
    if runrange >= 6:
        histograms.energyText = "8 TeV"

    offlineTauPt40 = "PFTauPt > 41"
#    offlineTauPt40 = "PFTauPt > 40 && PFTauPt < 50"


    if runrange == 1: # May10+Prompt-v4 (160431-167913)
        lumi = 1197
        label = "L1_SingleTauJet52 OR L1_SingleJet68 + HLT_IsoPFTau35_Trk20_MET45 (Run2011A)"
        #l1Trigger = "(L1_SingleTauJet52 || L1_SingleJet68)"
        #hltTrigger = "(run >= 160341 && run <= 165633 && (HLT_IsoPFTau35_Trk20_MET45_v1 || HLT_IsoPFTau35_Trk20_MET45_v2 || HLT_IsoPFTau35_Trk20_MET45_v4 || HLT_IsoPFTau35_Trk20_MET45_v6))"
        #hltTrigger += "|| (run >= 165970 && run <= 167913 && (HLT_IsoPFTau35_Trk20_MET60_v2 || HLT_IsoPFTau35_Trk20_MET60_v3 || HLT_IsoPFTau35_Trk20_MET60_v4)"
        runs = "run >= 160404 && run <= 167913"
        runsText = "160404-167913"
        offlineTriggerData = "((HLT_IsoMu17_v5 || HLT_IsoMu17_v6 || HLT_IsoMu17_v8) && MuonPt > 17)" # runs 160404-165633, unprescaled
        offlineTriggerData += "|| ((HLT_IsoMu17_v9 || HLT_IsoMu17_v11) && MuonPt > 17)"              # runs 165970-167913, PRESCALED
    elif runrange == 2: # Prompt-v6 (172620-173198), Aug05 (170722-172619) is missing!
        lumi = 870.119
        label = "L1_Jet52_Central + HLT_IsoPFTau35_Trk20_MET60 (Run2011A)"
        runs = "run >= 170722 && run <= 173198"
        runsText = "170826-173198"
        offlineTriggerData = "HLT_IsoMu17_v13 && MuonPt > 17"# runs 17022-172619, PRESCALED
    elif runrange == 3: # Prompt-v6 (173236-173692)
        lumi = 265.715
        label = "L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011A)"
        runs = "run >= 173236 && run <= 173692";
        runsText = "173236-173692"
        offlineTriggerData = "HLT_IsoMu20_v9 && MuonPt > 20"
    elif runrange == 4: # Run2011B-Tau-PromptSkim-v1 (175860-179889)
        lumi = 2762
        label = "L1_Jet52_Central + HLT_MediumIsoPFTau35_Trk20_MET60 (Run2011B)"
####        runs = "run >= 175860 && run <= 179889"
####        runsText = "175860-179889"
#### Merged runrange5 with runrange4 to approximate runrange5 efficiency with runrange4 efficiency.
#### The error should be small. Reason: too low statistics for an efficiency estimate for runrange5.
#### 20.6.2012/S.Lehti
        runs = "run >= 175860 && run <= 180252"
        runsText = "175860-180252"
#        offlineTriggerData = "HLT_IsoMu20_v9 && MuonPt > 20"
        offlineTriggerData = "HLT_IsoMu15_L1ETM20_v3 && MuonPt > 15"
    elif runrange == 5: # Run2011B-Tau-PromptSkim-v1 (179959-180252) 
        lumi = 2762
        runs = "run >= 179959 && run <= 180252"
        runsText = "179959-180252"
        offlineTriggerData = "HLT_IsoMu15_L1ETM20_v3 && MuonPt > 15"

    elif runrange == 6: #Run2012A 
        lumi = 697
        label = "Run2012A"
        runs = "run >= 190456 && run <= 193621" #FIXME the runMax
        runsText = "190456-193621"
        offlineTriggerData = "(HLT_IsoMu15_eta2p1_L1ETM20_v3 > 0.5 || HLT_IsoMu15_eta2p1_L1ETM20_v4 > 0.5) && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v3 > 0.5 && MuonPt > 15"

    elif runrange == 7: #Run2012B
        lumi = 4428
        label = "Run2012B"
        runs = "run >= 193834 && run <= 196531" #FIXME the runMin
        runsText = "193834-196531"
        offlineTriggerData = "HLT_IsoMu15_eta2p1_L1ETM20_v5 && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v3 && MuonPt > 15"

    elif runrange == 8: #Run2012C up to tau trigger bug fix at 202807, missing part 202807-203742 corresponds to 281.134 pb-1
        lumi = 6610
        label = "Run2012C"
        runs = "run >= 198022 && run <= 202585"
        runsText = "198022-202585"  
        offlineTriggerData = "(HLT_IsoMu15_eta2p1_L1ETM20_v6 > 0.5 || HLT_IsoMu15_eta2p1_L1ETM20_v7 > 0.5) && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v3 && MuonPt > 15"

    elif runrange == 9: #Run2012D
        lumi = 0 
        label = "Run2012D"
        runs = "run >= 198022 && run <= 203742"
        runsText = "198022-203742"
        offlineTriggerData = ""
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v3 && MuonPt > 15"


    elif runrange == 10: #Run2012A+B
        lumi = 5126
        label = "Run2012A+B"
        runs = "run >= 190456 && run <= 196531"
        runsText = "190456-196531"
        offlineTriggerData = "(HLT_IsoMu15_eta2p1_L1ETM20_v3 || HLT_IsoMu15_eta2p1_L1ETM20_v4 || HLT_IsoMu15_eta2p1_L1ETM20_v5) && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v3 && MuonPt > 15"

    elif runrange == 11: #Run2012A+B+C up to tau trigger bug fix at 202807
        lumi = 11736
        label = "Run2012A+B+C"
        runs = "run >= 190456 && run <= 202585"
        runsText = "190456-202585"
        offlineTriggerData = "(HLT_IsoMu15_eta2p1_L1ETM20_v3 || HLT_IsoMu15_eta2p1_L1ETM20_v4 || HLT_IsoMu15_eta2p1_L1ETM20_v5 || HLT_IsoMu15_eta2p1_L1ETM20_v6 || HLT_IsoMu15_eta2p1_L1ETM20_v7) && MuonPt > 15"
        offlineTriggerMc   = "HLT_IsoMu15_eta2p1_L1ETM20_v3 && MuonPt > 15"

    else:
        raise Exception("Invalid run range %d" % runrange)

    offlineTriggerData = "(%s) && %s" % (offlineTriggerData, runs)
#    offlineTriggerMc = "HLT_IsoMu17_v5 && MuonPt > 17"
#    offlineTriggerMc = "HLT_IsoMu17_v14 && MuonPt > 17"

    muMetMt = "sqrt( 2 * MuonPt * PFMET_ET * (1-cos(MuonPhi-PFMET_phi)) )"
    muMetMtCut = muMetMt+" < 40"
    if dataVsMc and highPurity:
        offlineSelection += "&& "+muMetMtCut
    if not dataVsMc:
        offlineSelection += "&& "+offlineTriggerData

    # if dataVsMc, 1=data, 2=MC
    # if not, 1=highPurity, 2=lowPurity
    offlineSelection1 = offlineSelection
    offlineSelection2 = offlineSelection


    # Trigger in 1 and 2 are the same if dataMcSameTrigger is true, or dataVsMc is false
    sameTrigger12 = (dataVsMc and dataMcSameTrigger) or not dataVsMc

    if dataVsMc:
        offlineSelection1 += "&& "+offlineTriggerData
        offlineSelection2 += "&& "+offlineTriggerMc
    else:
        offlineSelection1 += "&& "+muMetMtCut

    ### Trigger selectiondefinitions
    # Default is for run range 1
    l1TriggerName1 = "SingleTauJet52 OR SingleJet68"
    hltTriggerName1 = "IsoPFTau35_Trk20"
    l1TriggerName2 = l1TriggerName1
    hltTriggerName2 = hltTriggerName1

    # L1
    l1TauEt = 52
    l1CenEt = 68
    l1SelectionJetReco = "hasMatchedL1Jet"
    #l1SelectionTauVeto = "L1TauVeto == 0 && hasMatchedL1Jet"
    #l1SelectionIsolation = "L1IsolationRegions_2GeV>=7 && L1TauVeto == 0 && hasMatchedL1Jet"
    #l1SelectionTau = "L1IsolationRegions_2GeV>=7 && L1TauVeto == 0 && hasMatchedL1Jet"
    #l1SelectionCen = "!(L1IsolationRegions_2GeV>=7 && L1TauVeto == 0) && hasMatchedL1Jet"
    #l1Selection1 = "((L1TauVeto==0 && L1IsolationRegions_2GeV>=7 && L1JetEt>52) || (!(L1TauVeto==0 && L1IsolationRegions_2GeV>=7) && L1JetEt > 68)) && hasMatchedL1Jet"
    l1SelectionTauVeto = "L1TauVeto == 0"
    l1SelectionIsolation = "L1IsolationRegions_2GeV>=7"
    l1SelectionTau = And(l1SelectionJetReco, l1SelectionTauVeto, l1SelectionIsolation)
    l1SelectionCen = And(l1SelectionJetReco, Not(And(l1SelectionTauVeto, l1SelectionIsolation)))
    l1Selection1 = "((L1TauVeto==0 && L1IsolationRegions_2GeV>=7 && L1JetEt>52) || (!(L1TauVeto==0 && L1IsolationRegions_2GeV>=7) && L1JetEt > 68)) && hasMatchedL1Jet"
#    l1Selection2 = l1Selection1
    l1Selection2 = "L1JetEt > 52 && hasMatchedL1Jet" # Fall11 MC
    
    if runrange >= 2:
        l1TriggerName1 = "Jet52_Central"
        l1CenEta = 52
        l1Selection1 = "L1JetEt > 52 && hasMatchedL1Jet"

    if sameTrigger12:
        l1Selection2 = l1Selection1
        l1TriggerName2 = l1TriggerName1
    
    # L2 and 2.5
    l2Selection = "hasMatchedL2Jet == 1 && L2JetEt > 35"
    l25Selection = "l25Et > 35 && foundTracksInJet && l25Pt > 20"

    # L3
    l3Selection1 = "primaryVertexIsValid && l25TrkIsoPtMax < 1.0 && l25EcalIsoEtMax < 1.5"
#    l3Selection2 = l3Selection1
    l3Selection2 = "primaryVertexIsValid && l25TrkIsoPtMax < 1.0"
    if runrange >= 3:
        hltTriggerName1 = " MediumIsoPFTau35_Trk20"
        l3Selection1 = "primaryVertexIsValid && l25TrkIsoPtMax < 1.0"
        if sameTrigger12:
            l3Selection2 = l1Selection1
            hltTriggerName2 = hltTriggerName1

    if runrange >= 6:
        l1TriggerName1  = ""
        hltTriggerName1 = "LooseIsoPFTau35_Trk20_Prong1"
        l1TriggerName2  = ""
        hltTriggerName2 = "LooseIsoPFTau35_Trk20_Prong1"


    print "Offline selection for 1 (data/highPurity)", offlineSelection1
    print "Offline selection for 2 (MC/lowPurity)", offlineSelection2


    ### Create efficiency calculator
    if dataVsMc:
        files1 = getFilesData(runrange, highPurity)
        files2 = getFilesMc(runrange, highPurity)
        legend1 = "Data"
        legend2 = "MC Z#rightarrow#tau#tau M_400to800"
    else:
        files1 = getFilesData(runrange, True)
        files2 = getFilesData(runrange, False)
        legend1 = "Data high purity"
        legend2 = "Data low purity"

    ### Prepare for plotting
    plotDir = ""
    if dataVsMc:
        if highPurity:
            plotDir += "HighPur"
        else:
            plotDir += "LowPur"
        
        if not dataMcSameTrigger:
            if runrange < 6:
                plotDir += "McFall11"
            if runrange >= 6:
                plotDir += "McSummer12"
    else:
        plotDir += "LowVsHighPur"


    plotDir += "RunRange%d" % runrange
    
    plotter = Plotter(EfficiencyCalculator(files1), EfficiencyCalculator(files2), plotDir, lumi)
    plotter.setLegends(legend1, legend2)
    plotter.setTriggers(dataVsMc, l1TriggerName1, hltTriggerName1, l1TriggerName2, hltTriggerName2, runsText)

#    ptbins = [20, 30, 40, 50, 60, 80, 150]
    ptbins = [20, 30, 40, 50, 60, 80, 100, 150, 200, 300, 400, 500]
    etabins = [-2.1, -1.05, 0, 1.05, 2.1]
    vtxbins = [0,5,10,15,20,25,30,35]

    if runrange < 6:
        prefix = "Data2011_"
    if runrange == 6:
        prefix = "Data2012A_"
    if runrange == 7:
        prefix = "Data2012B_"
    if runrange == 8:
        prefix = "Data2012C_"
    if runrange == 9:
        prefix = "Data2012D_"
    if runrange == 10:
        prefix = "Data2012AB_"
    if runrange == 11:
        prefix = "Data2012ABC_"
    if runrange == 11:
        prefix = "Data2012ABCD_"

    mcWeight = None
    if dataVsMc and pyScenario != "Unweighted":
        mcWeight = "pileupWeight_"+pyScenario+"(MCNPU)"
    print
    print "MC weight",pyScenario
    print

    # Distributions
    ROOT.gStyle.SetErrorX(0.5)
    sel1 = offlineSelection1+"&&"+offlineTauPt40
    sel2 = offlineSelection2+"&&"+offlineTauPt40
    plotter.plotDistribution(prefix+"MuonTauVisMass", "MuonTauInvMass>>foo1(9,0,180)", sel1, sel2, mcWeight, xlabel="m(#mu, #tau) (GeV/c^{2}")
    plotter.plotDistribution(prefix+"MuonMetTransverseMass", muMetMt+">>foo2(10,0,100)", sel1, sel2, mcWeight, xlabel="m_{T}(#mu, E_{T}^{miss}) (GeV/c^{2})")
    plotter.plotDistribution(prefix+"N_Vertices", "numGoodOfflinePV>>foo3(35,0,35)", sel1, sel2, mcWeight, xlabel="Number of good vertices")

    if runrange < 6:
        sel1 = offlineSelection1+"&&"+l1SelectionJetReco
        sel2 = offlineSelection2+"&&"+l1SelectionJetReco
####    plotter.plotDistribution(prefix+"L1JetEt", "L1JetEt>>foo4(40,0,160)", sel1, sel2, mcWeight, xlabel="L1 jet E_{T} (GeV)")
####    plotter.plotDistribution(prefix+"L1TauJetEt", "L1JetEt>>foo4(40,0,160)", sel1+"&&hasMatchedL1TauJet", sel2+"&&hasMatchedL1TauJet", mcWeight, xlabel="L1 jet E_{T} (GeV)")
####    plotter.plotDistribution(prefix+"L1CenJetEt", "L1JetEt>>foo4(40,0,160)", sel1+"&&hasMatchedL1CenJet", sel2+"&&hasMatchedL1CenJet", mcWeight, xlabel="L1 jet E_{T} (GeV)")

    # Efficiencies
    hnumpt = ROOT.TH1F("hnumpt", "hnumpt", len(ptbins)-1, array.array("d", ptbins))
    hnumvtx = ROOT.TH1F("hnumvtx", "hnumvtx", len(vtxbins)-1, array.array("d", vtxbins))

    #hnumpt.Sumw2()
    optspt = {"xmin": 0}
    xlabel = "#tau-jet p_{T} (GeV/c)"

    # Level-1
    denom1 = offlineSelection1
    denom2 = offlineSelection2
    if runrange < 6:
        num1 = denom1+"&&"+l1SelectionJetReco
        num2 = denom2+"&&"+l1SelectionJetReco
####    plotter.plotEfficiency(prefix+"Tau1_L1Eff_1JetReco_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="L1 jet reco efficiency", moveLegend={"dy": -0.2})

        denom1 = num1
        denom2 = num2
        num1 = denom1+"&&"+l1SelectionTauVeto
        num2 = denom2+"&&"+l1SelectionTauVeto
####    plotter.plotEfficiency(prefix+"Tau1_L1Eff_2TauVeto_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="L1 tau veto efficiency", moveLegend={"dy": -0.2})

        denom1 = num1
        denom2 = num2
        num1 = denom1+"&&"+l1SelectionIsolation
        num2 = denom2+"&&"+l1SelectionIsolation
####    plotter.plotEfficiency(prefix+"Tau1_L1Eff_3TauIsolation_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="L1 tau isolation efficiency", moveLegend={"dy": -0.2})

        denom1 = offlineSelection1
        denom2 = offlineSelection2
        num1 = denom1+"&&"+l1SelectionTau
        num2 = denom2+"&&"+l1SelectionTau
####    plotter.plotEfficiency(prefix+"Tau1_L1Eff_4TauJet_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="L1 tau jet efficiency", moveLegend={"dy": -0.2})

        num1 = denom1+"&&"+l1SelectionCen
        num2 = denom2+"&&"+l1SelectionCen
####    plotter.plotEfficiency(prefix+"Tau1_L1Eff_5CenJet_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="L1 central jet efficiency")

        denom1 = offlineSelection1+"&&"+l1SelectionJetReco
        denom2 = offlineSelection2+"&&"+l1SelectionJetReco
        num1 = denom1+"&&"+l1Selection1
        num2 = denom2+"&&"+l1Selection2
####    plotter.plotEfficiency(prefix+"Tau1_L1Eff_6TauCenEtThreshold_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="L1 jet E_{T} threshold efficiency")

        denom1 = offlineSelection1
        denom2 = offlineSelection2
        num1 = denom1+"&&"+l1Selection1
        num2 = denom2+"&&"+l1Selection2
####    plotter.plotEfficiency(prefix+"Tau2_L1Eff_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="Level-1 tau efficiency")
    
    # HLT
        denom1 = num1
        denom2 = num2
        num1 = denom1+"&&"+l2Selection
        num2 = denom2+"&&"+l2Selection
        print "########################################"
        print num2
        print denom2
####    plotter.plotEfficiency(prefix+"Tau2_L20Eff_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="Level-2 tau efficiency")
    #plotter.plotEfficiency(prefix+"Tau2_L20Eff_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, opts=optspt, xlabel=xlabel, ylabel="Level-2 tau efficiency")
        print "========================================"

        denom1 = num1
        denom2 = num2
        num1 = denom1+"&&"+l25Selection
        num2 = denom2+"&&"+l25Selection
####    plotter.plotEfficiency(prefix+"Tau2_L25Eff_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="Level-2.5 tau efficiency", moveLegend={"dy": -0.4})

        denom1 = num1
        denom2 = num2
        num1 = denom1+"&&"+l3Selection1
        num2 = denom2+"&&"+l3Selection2
####    plotter.plotEfficiency(prefix+"Tau2_L3Eff_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="Level-3 tau efficiency", moveLegend={"dy": -0.4})

        denom1 = And(offlineSelection1, l1Selection1)
        denom2 = And(offlineSelection2, l1Selection2)
        num1 = And(denom1, l2Selection, l25Selection, l3Selection1)
        num2 = And(denom2, l2Selection, l25Selection, l3Selection2)
####    plotter.plotEfficiency(prefix+"Tau3_HLT_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="HLT tau efficiency")

        denom1 = offlineSelection1
        denom2 = offlineSelection2
        num1 = And(denom1, l1Selection1, l2Selection, l25Selection, l3Selection1)
        num2 = And(denom2, l1Selection2, l2Selection, l25Selection, l3Selection2)
        efficiency = plotter.plotEfficiency(prefix+"Tau3_L1HLT_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="Level-1 + HLT tau efficiency", fit=True, fitMin=20., fitMax=150., drawText=True, printResults=True)

        denom1 = And(denom1, offlineTauPt40)
        denom2 = And(denom2, offlineTauPt40)
        num1 = And(num1, offlineTauPt40)
        num2 = And(num2, offlineTauPt40)
        plotter.plotEfficiency(prefix+"Tau4_L1HLT_PFTauEta", "PFTauEta>>heta(4, -2.1, 2.1)", num1, denom1, num2, denom2, mcWeight, xlabel="#tau-jet #eta")
        plotter.plotEfficiency(prefix+"Tau4_L1HLT_PFTauPhi", "PFTauPhi>>heta(4, -3.1416, 3.1416)", num1, denom1, num2, denom2, mcWeight, xlabel="#tau-jet #phi")

    if runrange == 6:
        denom1 = offlineSelection1
        denom2 = offlineSelection2
        num1 = And(denom1,"(HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 > 0.5 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v3 > 0.5 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4 > 0.5) && PFTau_matchedHLTObject")
        num2 = And(denom2,"HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 > 0.5 && PFTau_matchedHLTObject")
        efficiency = plotter.plotEfficiency(prefix+"Tau3_L1HLT_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="Level-1 + HLT tau efficiency", fit=True, fitMin=20., fitMax=150., drawText=True, printResults=True)

    if runrange == 7:
        denom1 = offlineSelection1
        denom2 = offlineSelection2
        num1 = And(denom1,"HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 && PFTau_matchedHLTObject")
        num2 = And(denom2,"HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 && PFTau_matchedHLTObject")
        efficiency = plotter.plotEfficiency(prefix+"Tau3_L1HLT_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="Level-1 + HLT tau efficiency", fit=True, fitMin=20., fitMax=150., drawText=True, printResults=True)

    if runrange == 8:
        denom1 = offlineSelection1
        denom2 = offlineSelection2
        num1 = And(denom1,"(HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v7 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v8 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v9) && PFTau_matchedHLTObject")
        num2 = And(denom2,"HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 && PFTau_matchedHLTObject")

    if runrange == 9:
        denom1 = offlineSelection1
        denom2 = offlineSelection2
        num1 = And(denom1,"(HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v3 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v7) && PFTau_matchedHLTObject")
        num2 = And(denom2,"HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 && PFTau_matchedHLTObject")


    if runrange == 10:
        denom1 = offlineSelection1
        denom2 = offlineSelection2
        num1 = And(denom1,"(HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v3 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6) && PFTau_matchedHLTObject")
        num2 = And(denom2,"HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 && PFTau_matchedHLTObject")

    if runrange == 11:
        denom1 = offlineSelection1
        denom2 = offlineSelection2
        num1 = And(denom1,"(HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v3 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v4 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v6 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v7 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v8 || HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v9) && PFTau_matchedHLTObject")
        num2 = And(denom2,"HLT_IsoMu15_eta2p1_LooseIsoPFTau35_Trk20_Prong1_L1ETM20_v2 && PFTau_matchedHLTObject")

    efficiency = plotter.plotEfficiency(prefix+"Tau3_L1HLT_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="Level-1 + HLT tau efficiency", fit=True, fitMin=20., fitMax=150., drawText=True, printResults=True)

    denom1pt = And(denom1, offlineTauPt40)
    denom2pt = And(denom2, offlineTauPt40)
    num1pt = And(num1, offlineTauPt40)
    num2pt = And(num2, offlineTauPt40)

    effVsNvtx = plotter.plotEfficiency(prefix+"Tau4_L1HLT_NVtx", "numGoodOfflinePV>>hnumvtx", num1pt, denom1pt, num2pt, denom2pt, mcWeight, opts=optspt, xlabel="Number of good vertices", ylabel="Level-1 + HLT tau efficiency", fit=False, drawText=True, printResults=True)    

    #dumpParameters(plotDir,label,runsText,lumi,efficiency)
    pythonWriter.addParameters(selectionName,plotDir,label,runsText,lumi,efficiency)
    if runrange < 6:
        pythonWriter.addMCParameters(selectionName,"Fall11_PU_"+pyScenario,efficiency)
    else:
        pythonWriter.addMCParameters(selectionName,"Summer12_PU_"+pyScenario,efficiency)

    print "\nPlotDir",plotDir

def getFilesData(runrange, highPurity):
    tmp = ""
    if highPurity:
        tmp = "-highpurity"

    data2012A = os.path.join(DATAPATH,"tteffAnalysis2_TauPlusX_Run2012A_v1_RAW_TTEffSkim_v534_V00_11_03_v2/tteffAnalysis-hltpftau-hpspftau"+tmp+".root")
    data2012B = os.path.join(DATAPATH,"tteffAnalysis2_TauPlusX_Run2012B_13Jul2012_v1_AOD_TTEffSkim_v534_V00_11_03_v2/tteffAnalysis-hltpftau-hpspftau"+tmp+".root")
    data2012C = os.path.join(DATAPATH,"tteffAnalysis2_TauPlusX_Run2012C_v1_AOD_TTEffSkim_v534_V00_11_03_v2/tteffAnalysis-hltpftau-hpspftau"+tmp+".root")
    data2012D = os.path.join(DATAPATH,"tteffAnalysis2_TauPlusX_Run2012D_v1_AOD_TTEffSkim_v534_V00_11_03_v2/tteffAnalysis-hltpftau-hpspftau"+tmp+".root")

    returnData = []

    if runrange == 6:
        returnData.append(data2012A)
    if runrange == 7:
        returnData.append(data2012B)
    if runrange == 8:
        returnData.append(data2012C)
    if runrange == 9:
        returnData.append(data2012D)
    if runrange == 10:
        returnData.append(data2012A)
        returnData.append(data2012B)
    if runrange == 11:
        returnData.append(data2012A)
        returnData.append(data2012B)
        returnData.append(data2012C)
    if runrange == 12:
        returnData.append(data2012A)
        returnData.append(data2012B)
        returnData.append(data2012C)
        returnData.append(data2012D)

    print
    print "Datafiles:",returnData
    return returnData
    

def getFilesMc(runRange,highPurity):
    tmp = ""
    if highPurity:
        tmp += "-highpurity"

    mcSummer12_DYToTauTau_M_20 = os.path.join(DATAPATH,"tteffAnalysis2_DYToTauTau_M_20_TuneZ2star_8TeV_pythia6_tauola_Summer12_PU_S8_START52_V9_v1_AODSIM_v526hltp2_V00_11_02_v1/tteffAnalysis-hltpftau-hpspftau"+tmp+".root")
    mcSummer12_DYToTauTau_M_20_400to800 = os.path.join(DATAPATH,"tteffAnalysis2_DYToTauTau_M_400to800_TuneZ2Star_8TeV_pythia6_tauola_Summer12_PU_S7_START52_V9_v1_AODSIM_v526hltp2_V00_11_02_v2/tteffAnalysis-hltpftau-hpspftau"+tmp+".root")

    returnMC = []
    if runRange >= 6:
        returnMC.append(mcSummer12_DYToTauTau_M_20)
        returnMC.append(mcSummer12_DYToTauTau_M_20_400to800)

    print
    print "MC files:",returnMC
    return returnMC


class EfficiencyCalculator:
    def __init__(self, files):
        self.chain = ROOT.TChain("TTEffTree")
        for f in files:
            self.chain.Add(f)

    def getRootHisto(self, varexp, selection, weight=None):
        if weight != None:
            selection = "%s*(%s)" % (weight, selection)
        self.chain.Draw(varexp, selection, "goff e")
        h = self.chain.GetHistogram().Clone()
        h.SetDirectory(0)
        return h

    def getEntries(self, selection):
        return self.chain.GetEntries(selection)

class Plotter:
    def __init__(self, calc1, calc2, plotDir, lumi):
        self.calc1 = calc1
        self.calc2 = calc2
        self.plotDir = plotDir
        self.lumi = lumi

        if not os.path.exists(plotDir):
            os.mkdir(plotDir)

    def setLegends(self, legend1, legend2):
        self.legend1 = legend1
        self.legend2 = legend2

    def setTriggers(self, dataVsMc, l1TriggerName1, hltTriggerName1, l1TriggerName2, hltTriggerName2, runs):
        self.dataVsMc = dataVsMc
        self.l1TriggerName1 = l1TriggerName1
        self.hltTriggerName1 = hltTriggerName1
        self.l1TriggerName2 = l1TriggerName2
        self.hltTriggerName2 = hltTriggerName2
        self.runs = runs

        if not dataVsMc:
            if l1TriggerName1 != l1TriggerName2:
                raise Exception("If dataVsMc is False, l1TriggerName1 and 2 should be same ('%s' != '%s')" % (l1TriggerName1, l1TriggerName2))
            if hltTriggerName1 != hltTriggerName2:
                raise Exception("If dataVsMc is False, hltTriggerName1 and 2 should be same ('%s' != '%s')" % (hltTriggerName1, hltTriggerName2))

    def plotDistribution(self, name, varexp, selection1, selection2=None, weight2=None, xlabel=None, opts={}):
        if selection2 == None:
            selection2 = selection1

        h1 = self.calc1.getRootHisto(varexp, selection1)
        h2 = self.calc2.getRootHisto(varexp, selection2, weight2)

        h1.SetName("histo1")
        h2.SetName("histo2")

        dataset._normalizeToOne(h1)
        dataset._normalizeToOne(h2)

        h1.SetLineWidth(2)

        h2.SetLineColor(ROOT.kRed)
        h2.SetLineWidth(2)

        err1 = h1.Clone("err1")
        err1.SetMarkerSize(0)
        err1.SetFillColor(ROOT.kGray)

        err2 = h2.Clone("err2")
        err2.SetMarkerSize(0)
        err2.SetFillColor(ROOT.kRed-9)

        p = plots.ComparisonPlot(h1, h2)
        #p.prependPlotObject(err1, "E2")
        p.prependPlotObject(err2, "E2")

        p.histoMgr.setHistoDrawStyle("histo1", "EP")
        if hasattr(self, "legend1"):
            p.histoMgr.setHistoLegendLabelMany({"histo1": self.legend1, "histo2": self.legend2})

        self._common(name, p, xlabel, "Arbitrary units")
        histograms.addText(0.62, 0.77, "Normalized to unit area", size=17)
        p.save()

    def plotEfficiency(self, name, varexp, num1, denom1, num2, denom2, weight2=None, xlabel=None, ylabel=None, opts={}, opts2={}, fit=False, fitMin=None, fitMax=None, moveLegend={}, drawText=False, printResults=False):
        print "num",num1
        print "den",denom1

        n1 = self.calc1.getRootHisto(varexp, num1)
        d1 = self.calc1.getRootHisto(varexp, denom1)

        n2 = self.calc2.getRootHisto(varexp, num2, weight2)
        d2 = self.calc2.getRootHisto(varexp, denom2, weight2)

        eff1 = ROOT.TGraphAsymmErrors(n1, d1)
        eff2 = ROOT.TGraphAsymmErrors(n2, d2)

        x = ROOT.Double(0)
        y = ROOT.Double(0)

        styles.dataStyle.apply(eff1)
        styles.mcStyle.apply(eff2)
        eff1.SetMarkerSize(1)
        eff2.SetMarkerSize(1.5)

        p = plots.ComparisonPlot(histograms.HistoGraph(eff1, "eff1", "p", "P"),
                                 histograms.HistoGraph(eff2, "eff2", "p", "P")) 
        if hasattr(self, "legend1"):
            p.histoMgr.setHistoLegendLabelMany({"eff1": self.legend1, "eff2": self.legend2})

        opts_ = {"ymin": 0, "ymax": 1.1}
        opts_.update(opts)

        opts2_ = {"ymin": 0.5, "ymax": 1.5}
        opts2_.update(opts2)

        moveLegend_ = {"dx": -0.55}
        moveLegend_.update(moveLegend)

        if fit:
            (fit1, res1) = self._fit("eff1", eff1, fitMin, fitMax)
            (fit2, res2) = self._fit("eff2", eff2, fitMin, fitMax)

            p.prependPlotObject(fit2)
            p.prependPlotObject(fit1)

        self._common(name, p, xlabel, ylabel, ratio=True, opts=opts_, opts2=opts2_, moveLegend=moveLegend_)
        if drawText and hasattr(self, "l1TriggerName1"):
            x = 0.45
            y = 0.35
            size = 17
            dy = 0.035
            mcColor = eff2.GetMarkerColor()
            if self.dataVsMc:
                if self.l1TriggerName1 == self.l1TriggerName2 and self.hltTriggerName1 == self.hltTriggerName2:
                    histograms.addText(x, y, "Data (runs %s) and MC"%self.runs, size); y -= dy
                    if len(self.l1TriggerName1) > 0:
                        histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy
                else:
                    histograms.addText(x, y, "Data (runs %s)"%self.runs, size); y -= dy
                    if len(self.l1TriggerName1) > 0:
                        histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy
                    y -= 0.01
                    histograms.addText(x, y, "MC", size, color=mcColor); y -= dy
                    if len(self.l1TriggerName2) > 0:
                        histograms.addText(x, y, "L1:  %s" % self.l1TriggerName2, size, color=mcColor); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName2, size, color=mcColor); y -= dy
            else:
                histograms.addText(x, y, "Data (runs %s)"%self.runs, size); y -= dy
                if len(self.l1TriggerName2) > 0:
                    histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy

        if printResults:
            ratio = p.ratios[0]
            print
            for bin in xrange(1, n1.GetNbinsX()+1):
                i = bin-1
                print "Bin low edge %.0f" % n1.GetBinLowEdge(bin)
                print "   1: efficiency %.7f +- %.7f" % (eff1.GetY()[i], max(eff1.GetErrorYhigh(i), eff1.GetErrorYlow(i))), "Entries num",n1.GetBinContent(bin),"denom",d1.GetBinContent(bin)
                print "   2: efficiency %.7f +- %.7f" % (eff2.GetY()[i], max(eff2.GetErrorYhigh(i), eff2.GetErrorYlow(i))), "Entries num",n2.GetBinContent(bin),"denom",d2.GetBinContent(bin)
                print "   ratio:        %.7f +- %.7f" % (ratio.getRootGraph().GetY()[i], max(ratio.getRootGraph().GetErrorYhigh(i), ratio.getRootGraph().GetErrorYlow(i)))
            print

        p.getFrame2().GetYaxis().SetTitle("Ratio")
        p.save()
        return p

    def _fit(self, name, graph, min, max, xpos=0):
        function = ROOT.TF1("fit"+name, "0.5*[0]*(1+TMath::Erf( (sqrt(x)-sqrt([1]))/(sqrt(2)*[2]) ))", min, max);
        function.SetParameters(1., 40., 1.);
        function.SetParLimits(0, 0.0, 1.0);
        fitResult = graph.Fit(function, "NRSE+EX0");
        print "Fit status", fitResult.Status()
        #fitResult.Print("V");
        #fitResult.GetCovarianceMatrix().Print();
        function.SetLineColor(graph.GetMarkerColor());
        function.SetLineWidth(2);
        # function.Draw("same")
        # ROOT.gPadUpdate();
        # stat = graph.FindObject("stats");
        # stat.SetX1NDC(stat.GetX1NDC()+xpos);
        # stat.SetX2NDC(stat.GetX2NDC()+xpos);
        # stat.SetTextColor(graph.GetMarkerColor());
        # stat.SetLineColor(graph.GetMarkerColor());
        return (function, fitResult)


    def _common(self, name, plot, xlabel=None, ylabel=None, ratio=False, opts={}, opts2={}, moveLegend={}):
        plot.createFrame(os.path.join(self.plotDir, name), createRatio=ratio, opts=opts, opts2=opts2)
        if hasattr(self, "legend1"):
            plot.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

        if xlabel != None:
            plot.frame.GetXaxis().SetTitle(xlabel)
        if ylabel != None:
            plot.frame.GetYaxis().SetTitle(ylabel)

        plot.draw()
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        histograms.addLuminosityText(None, None, self.lumi)



if __name__ == "__main__":
    main()
