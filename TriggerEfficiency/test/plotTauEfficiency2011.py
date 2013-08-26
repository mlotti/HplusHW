#!/usr/bin/env python

######################################################################
#
# The ntuple files should come from the TTEff code
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
from math import sqrt

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
"""
class PythonWriter:
    class Parameters:
        def __init__(self, name, label,runrange,lumi,eff):
            self.name     = name
            self.label    = label
            self.runrange = runrange
            self.lumi     = lumi
            self.eff      = eff
        def Print(self):
            print "check Parameters",self.name,self.label,self.runrange,self.lumi

    def __init__(self):
        self.ranges = []
        self.mcs    = []
        self.namedSelection = []
        self.bins   = []

    def addParameters(self,name,path,label,runrange,lumi,eff):
        print "check addParameters",name,path,label,runrange,lumi 
        labelFound = False
        for r in self.ranges:
            if r.name == name and r.label == label and r.runrange == runrange:
                labelFound = True
        if not labelFound:
            self.ranges.append(self.Parameters(name,label,runrange,lumi,eff))
            self.dumpParameters(path,label,runrange,lumi,eff)
        print "check self.ranges size",len(self.ranges)
        for r in self.ranges:
            r.Print()

    def addMCParameters(self,name,label,eff):
        #print "check addMCParameters",name,label
        labelFound = False
        for mc in self.mcs:
            if mc.label == label and mc.name == name:
                labelFound = True
        if not labelFound:
            self.mcs.append(self.Parameters(name,label,"","",eff))

    def SaveOfflineSelection(self,selection):
        found = False
        for n in self.namedSelection:
            if n == selection:
                found = True
        if not found:
            self.namedSelection.append(selection)

    def dumpParameters(self,path,label,runrange,lumi,eff):

        fName = os.path.join(path,"dataParameters.py")
        fOUT = open(fName,"w")

        self.writeParameters(fOUT,label,runrange,lumi,eff)

    def write(self,fName):
        fOUT = open(fName,"w")
        self.timeStamp(fOUT)

        for r in self.ranges:
            self.findBins(r.eff)

        fOUT.write("import FWCore.ParameterSet.Config as cms\n\n")

        fOUT.write("def triggerBin(pt, efficiency, uncertainty):\n")
        fOUT.write("    return cms.PSet(\n")
        fOUT.write("        pt = cms.double(pt),\n")
        fOUT.write("        efficiency = cms.double(efficiency),\n")
        fOUT.write("        uncertainty = cms.double(uncertainty)\n")
        fOUT.write("    )\n\n")

        print "check self.namedSelection",self.namedSelection

        for ns in self.namedSelection:
            name      = ns[0]
            selection = ns[1]

            fOUT.write("\ntauLegEfficiency_"+name+" = cms.untracked.PSet(\n")

            fOUT.write("    # The selected triggers for the efficiency. If one trigger is\n")
            fOUT.write("    # given, the parametrization of it is used as it is (i.e.\n")
            fOUT.write("    # luminosity below is ignored). If multiple triggers are given,\n")
            fOUT.write("    # their parametrizations are used weighted by the luminosities\n")
            fOUT.write("    # given below.\n")
            fOUT.write("    # selectTriggers = cms.VPSet(\n")
            fOUT.write("    #     cms.PSet(\n")
            fOUT.write("    #         trigger = cms.string(\"HLT_IsoPFTau35_Trk20_EPS\"),\n")
            fOUT.write("    #         luminosity = cms.double(0)\n")
            fOUT.write("    #     ),\n")
            fOUT.write("    # ),\n")
            fOUT.write("    # The parameters of the trigger efficiency parametrizations,\n")
            fOUT.write("    # looked dynamically from TriggerEfficiency_cff.py\n\n")

            fOUT.write("    # Offline selection: "+selection+"\n\n")

            fOUT.write("    dataParameters = cms.PSet(\n")
            for r in self.ranges:
                if r.name == name:
                    self.writeParameters(fOUT,r.label,r.runrange,r.lumi,r.eff)
            fOUT.write("    ),\n")

            fOUT.write("    mcParameters = cms.PSet(\n")
            for mc in self.mcs:
                #print "check write mc",mc.name,name
                if mc.name == name:
                    self.writeMCParameters(fOUT,mc.label,mc.eff)
            fOUT.write("    ),\n")

            fOUT.write("    dataSelect = cms.vstring(),\n")
            fOUT.write("    mcSelect = cms.string(\""+self.mcs[0].label+"\"),\n")
            fOUT.write("    mode = cms.untracked.string(\"disabled\") # dataEfficiency, scaleFactor, disabled\n")
            fOUT.write(")\n")

    def writeParameters(self,fOUT,label,runrange,lumi,eff):
        runrange_re = re.compile("(?P<firstRun>(\d+))-(?P<lastRun>(\d+))")
        match = runrange_re.search(runrange)
        if not match:
            print "Run range not valid",runrange
            sys.exit()

        fOUT.write("        # "+label+"\n")
        fOUT.write("        runs_"+match.group("firstRun")+"_"+match.group("lastRun")+" = cms.PSet(\n")
        fOUT.write("            firstRun = cms.uint32("+match.group("firstRun")+"),\n")
        fOUT.write("            lastRun = cms.uint32("+match.group("lastRun")+"),\n")
        fOUT.write("            luminosity = cms.double(%s), # 1/pb\n"%lumi)
        self.writeBins(fOUT,label,eff)
        fOUT.write("        ),\n")

    def writeMCParameters(self,fOUT,label,eff):
        fOUT.write("        "+label+" = cms.PSet(\n")
        self.writeBins(fOUT,label,eff,ihisto=1)
        fOUT.write("        ),\n")

    def writeBins(self,fOUT,label,eff,ihisto=0):
        fOUT.write("            bins = cms.VPSet(\n")
        nbins = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetN()
        for i in range(nbins):
            binLowEdge = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetX()[i]
            binLowEdge-= eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorX(i)
            efficiency = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetY()[i]
            error      = max(eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYhigh(i),eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYlow(i))
#            efficiency = eff.ratios[0].getRootGraph().GetY()[i]
#            error = max(eff.ratios[0].getRootGraph().GetErrorYhigh(i),eff.ratios[0].getRootGraph().GetErrorYlow(i))
            fOUT.write("                triggerBin("+str(binLowEdge)+", "+str(efficiency)+", "+str(error)+"),\n")
        #print "check writeBins",nbins,len(self.bins)
        if nbins < len(self.bins):
            for i in range(nbins,len(self.bins)):
                #print self.bins[i],efficiency,error
                fOUT.write("                triggerBin("+str(self.bins[i])+", "+str(efficiency)+", "+str(error)+"), # duplicated bin\n")
        fOUT.write("            ),\n")

    def findBins(self,eff):
        nbins = eff.histoMgr.getHistos()[0].getRootHisto().GetN()
        for i in range(nbins):
            binLowEdge = eff.histoMgr.getHistos()[0].getRootHisto().GetX()[i]
            binLowEdge-= eff.histoMgr.getHistos()[0].getRootHisto().GetErrorX(i)
            if binLowEdge not in self.bins:
                self.bins.append(binLowEdge)

    def timeStamp(self,fOUT):
        import datetime
        time = datetime.datetime.now().ctime()
        fOUT.write("# Generated on "+time+"\n")
        fOUT.write("# by HiggsAnalysis/TriggerEfficiency/test/plotTauEfficiency.py\n\n")

    def sysError(self):
        ihisto = 0
        ranges = self.removeDuplicateRunRanges(self.ranges)
        lumiSum = 0
        effSum = []
        for i in range(ranges[0].eff.histoMgr.getHistos()[ihisto].getRootHisto().GetN()):
            effSum.append(0)

        for r in ranges:
            lumiSum += r.lumi
            print "RunRange",r.runrange
            print "    Lumi",r.lumi
            eff = r.eff
            for i in range(eff.histoMgr.getHistos()[ihisto].getRootHisto().GetN()):
                binLowEdge = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetX()[i]
                binLowEdge-= eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorX(i)
                efficiency = eff.histoMgr.getHistos()[ihisto].getRootHisto().GetY()[i]
                error      = max(eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYhigh(i),eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorYlow(i))
                effSum[i]+= r.lumi*r.lumi*error*error
                print "    ",binLowEdge,efficiency,error

        print
        print "Summed lumi",lumiSum
        print "Summed uncertainty"
        for i in range(len(effSum)):
            binLowEdge = ranges[0].eff.histoMgr.getHistos()[ihisto].getRootHisto().GetX()[i]
            binLowEdge-= ranges[0].eff.histoMgr.getHistos()[ihisto].getRootHisto().GetErrorX(i)
            print "    ",binLowEdge,sqrt(effSum[i])/lumiSum

    def removeDuplicateRunRanges(self,ranges):
        returnRanges = []
        runMin = 999999999
        runMax = 0
        runrange_re = re.compile("(?P<firstRun>(\d+))-(?P<lastRun>(\d+))")
        for r in ranges:
            match = runrange_re.search(r.runrange)
            if match:
                firstRun = match.group("firstRun")
                lastRun = match.group("lastRun")
                if not(firstRun < runMax and firstRun > runMin) and not(lastRun > runMin and lastRun < runMax):
                    if firstRun < runMin:
                        runMin = firstRun
                    if lastRun > runMax:
                        runMax = lastRun
                    returnRanges.append(r)
        return returnRanges
"""

pythonWriter = PythonWriter()

def main():
    style = tdrstyle.TDRStyle()

    histograms.createLegend.moveDefaults(dh=-0.18)

    puWeights = []
    puWeights.append("pileupWeight_2011AB.C")
    puWeights.append("pileupWeight_2011A.C")
    puWeights.append("pileupWeight_2011B.C")
    puWeights.append("pileupWeight_2011A_RR1.C")
    puWeights.append("pileupWeight_2011A_RR2.C")
    puWeights.append("pileupWeight_2011A_RR3.C")
    puWeights.append("pileupWeight_Unweighted.C")

    puWeightPath = "src/HiggsAnalysis/TriggerEfficiency/test"

#    macroPath = os.path.join(os.environ["CMSSW_BASE"], puWeightPath, puWeights[0]+"+")
#    macroPath = os.path.join(os.environ["CMSSW_BASE"], "src/HiggsAnalysis/TriggerEfficiency/test/pileupWeight2011AB.C+")
#    macroPath = os.path.join(os.environ["CMSSW_BASE"], "src/HiggsAnalysis/TriggerEfficiency/test/pileupWeight_test.C+")
#    macroPath = macroPath.replace("../src/","")
#    ROOT.gROOT.LoadMacro(macroPath)

    highPurity = True

    ### Offline selection definition (H+)
    offlineSelectionHPlusBase = "PFTauPt > 20 && abs(PFTauEta) < 2.1"
    offlineSelectionHPlusBase += "&& 1/PFTauInvPt > 20"
    offlineSelectionHPlusBase += "&& PFTauProng == 1"
    offlineSelectionHPlusBase += "&& againstMuonTight > 0.5"
    offlineSelectionHPlusBase += "&& MuonTauInvMass < 80"

    offlineSelectionMediumMedium = offlineSelectionHPlusBase
    offlineSelectionMediumMedium+= "&& againstElectronMedium > 0.5"
    offlineSelectionMediumMedium+= "&& byMediumCombinedIsolationDeltaBetaCorr > 0.5"

    offlineSelectionMediumMVA = offlineSelectionHPlusBase
    offlineSelectionMediumMVA+= "&& againstElectronMVA > 0.5"
    offlineSelectionMediumMVA+= "&& byMediumCombinedIsolationDeltaBetaCorr > 0.5"

    offlineSelectionLooseMedium = offlineSelectionHPlusBase
    offlineSelectionLooseMedium+= "&& againstElectronMedium > 0.5"
    offlineSelectionLooseMedium+= "&& byLooseCombinedIsolationDeltaBetaCorr > 0.5"

    offlineSelectionLooseMVA = offlineSelectionHPlusBase
    offlineSelectionLooseMVA+= "&& againstElectronMVA > 0.5"
    offlineSelectionLooseMVA+= "&& byLooseCombinedIsolationDeltaBetaCorr > 0.5"

    #### 2011 W(taunu)H(bb) analysis Segala, Zenz, Narain                                                                                          
    offlineSelectionWtaunuHbb = "PFTauPt > 20 && abs(PFTauEta) < 2.1"
    offlineSelectionWtaunuHbb += "&& 1/PFTauInvPt > 20"
    offlineSelectionWtaunuHbb += "&& againstElectronLoose > 0.5 && againstMuonTight > 0.5"
    offlineSelectionWtaunuHbb += "&& decayModeFinding > 0.5"
    offlineSelectionWtaunuHbb += "&& byLooseCombinedIsolationDeltaBetaCorr > 0.5"

    #### 
    offlineSelections = []
    offlineSelections.append(namedselection("byMediumCombinedIsolationDeltaBetaCorr_againstElectronMedium",offlineSelectionMediumMedium))
    offlineSelections.append(namedselection("byMediumCombinedIsolationDeltaBetaCorr_againstElectronMVA",offlineSelectionMediumMVA))
    offlineSelections.append(namedselection("byLooseCombinedIsolationDeltaBetaCorr_againstElectronMVA",offlineSelectionLooseMVA))
    offlineSelections.append(namedselection("byLooseCombinedIsolationDeltaBetaCorr_againstElectronMedium",offlineSelectionLooseMedium))
#    offlineSelections.append(namedselection("WtaunuHbb",offlineSelectionWtaunuHbb))

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

                doPlots(1,highPurity=highPurity,selection=selection,pyScenario=pyScenario)
                doPlots(2,highPurity=highPurity,selection=selection,pyScenario=pyScenario)
                doPlots(3,highPurity=highPurity,selection=selection,pyScenario=pyScenario)
                doPlots(4,highPurity=highPurity,selection=selection,pyScenario=pyScenario) #2011B
#    doPlots(5,highPurity=highPurity)
#    doPlots(6,highPurity=highPurity) #2011A
#    doPlots(7,highPurity=highPurity) #2011A+B

    pythonWriter.write("tauLegTriggerEfficiency_cff.py")
    pythonWriter.sysError()

def namedselection(name,selection):
    namedSelection = []
    namedSelection.append(name)
    namedSelection.append(selection)
    return namedSelection

def doPlots(runrange, selection, dataVsMc=True, highPurity=True, dataMcSameTrigger=False, pyScenario="Unweighted"):

    ### Offline selection definition
    selectionName    = selection[0]
    offlineSelection = selection[1]
    """
    offlineSelection = "PFTauPt > 20 && abs(PFTauEta) < 2.1"
    offlineSelection += "&& 1/PFTauInvPt > 20"
    offlineSelection += "&& PFTauProng == 1"
#    offlineSelection += "&& againstElectronMedium > 0.5 && againstMuonTight > 0.5"
    offlineSelection += "&& againstElectronMVA > 0.5 && againstMuonTight > 0.5"
#    offlineSelection += "&& byTightIsolation > 0.5"
#    offlineSelection += "&& byVLooseCombinedIsolationDeltaBetaCorr > 0.5"
#    offlineSelection += "&& byLooseCombinedIsolationDeltaBetaCorr > 0.5"
    offlineSelection += "&& byMediumCombinedIsolationDeltaBetaCorr > 0.5"
    offlineSelection += "&& MuonTauInvMass < 80"
    
    #### 2011 W(taunu)H(bb) analysis Segala, Zenz, Narain                                                         
    offlineSelection = "PFTauPt > 20 && abs(PFTauEta) < 2.1"
    offlineSelection += "&& 1/PFTauInvPt > 20"
    offlineSelection += "&& againstElectronLoose > 0.5 && againstMuonTight > 0.5"
    offlineSelection += "&& decayModeFinding > 0.5"
    offlineSelection += "&& byLooseCombinedIsolationDeltaBetaCorr > 0.5"
    """
####    pythonWriter.SaveOfflineSelection(selection)

    offlineTauPt40 = "PFTauPt > 40"

####    offlineTauPt40 = "PFTauPt > 41 && PFTauPt < 50"

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
        runsText = "170722-173198"
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
        runs = "run >= 175832 && run <= 180252"
        runsText = "175832-180252"
#        offlineTriggerData = "HLT_IsoMu20_v9 && MuonPt > 20"
####        offlineTriggerData = "(HLT_IsoMu15_L1ETM20_v3 || HLT_IsoMu15_L1ETM20_v4 || HLT_IsoMu15_v14 || HLT_IsoMu15_v17 || HLT_IsoMu15_v18) && MuonPt > 15"
        offlineTriggerData = "(HLT_IsoMu15_L1ETM20_v3 || HLT_IsoMu15_L1ETM20_v4) && MuonPt > 15"
    elif runrange == 5: # Run2011B-Tau-PromptSkim-v1 (179959-180252) 
        lumi = 2762
        label = ""
        runs = "run >= 179959 && run <= 180252"
        runsText = "179959-180252"
        offlineTriggerData = "HLT_IsoMu15_L1ETM20_v3 && MuonPt > 15"

    elif runrange == 6: # Whole A-part
        lumi = 2332.834
        label = "Dummy"
        runs = "run >= 160404 && run <= 173692"
        runsText = "160404-173692"
        offlineTriggerData = "(((HLT_IsoMu17_v5 || HLT_IsoMu17_v6 || HLT_IsoMu17_v8) && MuonPt > 17)"
        offlineTriggerData += "|| ((HLT_IsoMu17_v9 || HLT_IsoMu17_v11) && MuonPt > 17)"
        offlineTriggerData += "|| (HLT_IsoMu17_v13 && MuonPt > 17)"
        offlineTriggerData += "|| (HLT_IsoMu20_v9 && MuonPt > 20))"

    elif runrange == 7: # Whole 2011 data
        lumi = 5094.834
        label = "Dummy"
        runs = "run >= 160404 && run <= 180252"
        runsText = "160404-180252"
        offlineTriggerData = "(((HLT_IsoMu17_v5 || HLT_IsoMu17_v6 || HLT_IsoMu17_v8) && MuonPt > 17)"
        offlineTriggerData += "|| ((HLT_IsoMu17_v9 || HLT_IsoMu17_v11) && MuonPt > 17)"
        offlineTriggerData += "|| (HLT_IsoMu17_v13 && MuonPt > 17)"
        offlineTriggerData += "|| (HLT_IsoMu20_v9 && MuonPt > 20)"
        offlineTriggerData += "|| (HLT_IsoMu15_L1ETM20_v3 && MuonPt > 15))"

    else:
        raise Exception("Invalid run range %d" % runrange)

    offlineTriggerData = "(%s) && %s" % (offlineTriggerData, runs)
#    offlineTriggerMc = "HLT_IsoMu17_v5 && MuonPt > 17"
    offlineTriggerMc = "HLT_IsoMu17_v14 && MuonPt > 17"

    muMetMt = "sqrt( 2 * MuonPt * MET * (1-cos(MuonPhi-METphi)) )"
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
#    l1TriggerName2 = l1TriggerName1
#    hltTriggerName2 = hltTriggerName1
    l1TriggerName2 = "Jet52_Central"
    hltTriggerName2 = "MediumIsoPFTau35_Trk20"

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


    print "Offline selection for 1 (data/highPurity)", offlineSelection1
    print "Offline selection for 2 (MC/lowPurity)", offlineSelection2


    ### Create efficiency calculator
    if dataVsMc:
        files1 = getFilesData(runrange, highPurity)
        files2 = getFilesMc(highPurity)
        legend1 = "Data"
#        legend2 = "MC Z#rightarrow#tau#tau"
        legend2 = "Z/#gamma* #rightarrow #tau#tau\nsimulation"
    else:
        files1 = getFilesData(runrange, True)
        files2 = getFilesData(runrange, False)
        legend1 = "Data high purity"
        legend2 = "Data low purity"
    #print "check files",files1,files2
    ### Prepare for plotting
    plotDir = ""
    if dataVsMc:
        if highPurity:
            plotDir += "HighPur"
        else:
            plotDir += "LowPur"
        
        if not dataMcSameTrigger:
            plotDir += "McFall11"
    else:
        plotDir += "LowVsHighPur"

    plotDir += "RunRange%d" % runrange
    
    plotter = Plotter(EfficiencyCalculator(files1), EfficiencyCalculator(files2), plotDir, lumi)
    plotter.setLegends(legend1, legend2)
    plotter.setTriggers(dataVsMc, l1TriggerName1, hltTriggerName1, l1TriggerName2, hltTriggerName2, runsText)

    ptbins = [20, 30, 40, 50, 60, 80,
              150
              ]
    etabins = [-2.1, -1.05, 0, 1.05, 2.1]
    vtxbins = [0,5,10,15,20]

    prefix = "Data2011_"

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
    plotter.plotDistribution(prefix+"N_Vertices", "numGoodOfflinePV>>foo3(20,0,20)", sel1, sel2, mcWeight, xlabel="Number of good vertices")

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

    print "        denom1 =",denom1
    print "        denom2 =",denom2
    print "        num1   =",num1
    print "        num2   =",num2
    

    if runrange == 6:
        denom1 = And(offlineSelection,"(( (((HLT_IsoMu17_v5 || HLT_IsoMu17_v6 || HLT_IsoMu17_v8) && MuonPt > 17)|| ((HLT_IsoMu17_v9 || HLT_IsoMu17_v11) && MuonPt > 17)) && run >= 160404 && run <= 167913 ) || ((HLT_IsoMu17_v13 && MuonPt > 17) && run >= 170722 && run <= 173198) || ((HLT_IsoMu20_v9 && MuonPt > 20) && run >= 173236 && run <= 173692) ) ")
        denom2 = And(offlineSelection,"(HLT_IsoMu17_v14 && MuonPt > 17)")
        num1   = And(offlineSelection,"(((((HLT_IsoMu17_v5 || HLT_IsoMu17_v6 || HLT_IsoMu17_v8) && MuonPt > 17)|| ((HLT_IsoMu17_v9 || HLT_IsoMu17_v11) && MuonPt > 17)) && run >= 160404 && run <= 167913 && ((L1TauVeto==0 && L1IsolationRegions_2GeV>=7 && L1JetEt>52) || (!(L1TauVeto==0 && L1IsolationRegions_2GeV>=7) && L1JetEt > 68)) && hasMatchedL1Jet&&hasMatchedL2Jet == 1 && L2JetEt > 35&&l25Et > 35 && foundTracksInJet && l25Pt > 20&&primaryVertexIsValid && l25TrkIsoPtMax < 1.0 && l25EcalIsoEtMax < 1.5) || ((HLT_IsoMu17_v13 && MuonPt > 17) && run >= 170722 && run <= 173198 && hasMatchedL1Jet&&hasMatchedL2Jet == 1 && L2JetEt > 35&&l25Et > 35 && foundTracksInJet && l25Pt > 20&&primaryVertexIsValid && l25TrkIsoPtMax < 1.0 && l25EcalIsoEtMax < 1.5) || ((HLT_IsoMu20_v9 && MuonPt > 20) && run >= 173236 && run <= 173692 && L1JetEt > 52 && hasMatchedL1Jet&&hasMatchedL2Jet == 1 && L2JetEt > 35&&l25Et > 35 && foundTracksInJet && l25Pt > 20&&primaryVertexIsValid && l25TrkIsoPtMax < 1.0) )")
        num2   = And(offlineSelection,"HLT_IsoMu17_v14 && MuonPt > 17&&L1JetEt > 52 && hasMatchedL1Jet&&hasMatchedL2Jet == 1 && L2JetEt > 35&&l25Et > 35 && foundTracksInJet && l25Pt > 20&&primaryVertexIsValid && l25TrkIsoPtMax < 1.0")

#    if runrange == 7:
#        denom1 = And(offlineSelection,"((HLT_IsoMu15_L1ETM20_v3 && MuonPt > 15) && run >= 175860 && run <= 180252)")
#        denom2 = And(offlineSelection,"(HLT_IsoMu17_v14 && MuonPt > 17)")
#        num1   = And(offlineSelection,"( (HLT_IsoMu15_L1ETM20_v3 && MuonPt > 15) && run >= 175860 && run <= 180252&&#L1JetEt > 52 && hasMatchedL1Jet&&hasMatchedL2Jet == 1 && L2JetEt > 35&&l25Et > 35 && foundTracksInJet && l25Pt > 20&#&primaryVertexIsValid && l25TrkIsoPtMax < 1.0)")
#        num2   = And(offlineSelection,"HLT_IsoMu17_v14 && MuonPt > 17&&L1JetEt > 52 && hasMatchedL1Jet&&hasMatchedL2#Jet == 1 && L2JetEt > 35&&l25Et > 35 && foundTracksInJet && l25Pt > 20&&primaryVertexIsValid && l25TrkIsoPtMax < 1.0#")


    if runrange == 7:
        denom1 = And(offlineSelection,"(( (((HLT_IsoMu17_v5 || HLT_IsoMu17_v6 || HLT_IsoMu17_v8) && MuonPt > 17)|| ((HLT_IsoMu17_v9 || HLT_IsoMu17_v11) && MuonPt > 17)) && run >= 160404 && run <= 167913 ) || ((HLT_IsoMu17_v13 && MuonPt > 17) && run >= 170722 && run <= 173198) || ((HLT_IsoMu20_v9 && MuonPt > 20) && run >= 173236 && run <= 173692) || ((HLT_IsoMu15_L1ETM20_v3 && MuonPt > 15) && run >= 175860 && run <= 180252)) ")
        denom2 = And(offlineSelection,"(HLT_IsoMu17_v14 && MuonPt > 17)")
        num1   = And(offlineSelection,"(((((HLT_IsoMu17_v5 || HLT_IsoMu17_v6 || HLT_IsoMu17_v8) && MuonPt > 17)|| ((HLT_IsoMu17_v9 || HLT_IsoMu17_v11) && MuonPt > 17)) && run >= 160404 && run <= 167913 && ((L1TauVeto==0 && L1IsolationRegions_2GeV>=7 && L1JetEt>52) || (!(L1TauVeto==0 && L1IsolationRegions_2GeV>=7) && L1JetEt > 68)) && hasMatchedL1Jet&&hasMatchedL2Jet == 1 && L2JetEt > 35&&l25Et > 35 && foundTracksInJet && l25Pt > 20&&primaryVertexIsValid && l25TrkIsoPtMax < 1.0 && l25EcalIsoEtMax < 1.5) || ((HLT_IsoMu17_v13 && MuonPt > 17) && run >= 170722 && run <= 173198 && hasMatchedL1Jet&&hasMatchedL2Jet == 1 && L2JetEt > 35&&l25Et > 35 && foundTracksInJet && l25Pt > 20&&primaryVertexIsValid && l25TrkIsoPtMax < 1.0 && l25EcalIsoEtMax < 1.5) || ((HLT_IsoMu20_v9 && MuonPt > 20) && run >= 173236 && run <= 173692 && L1JetEt > 52 && hasMatchedL1Jet&&hasMatchedL2Jet == 1 && L2JetEt > 35&&l25Et > 35 && foundTracksInJet && l25Pt > 20&&primaryVertexIsValid && l25TrkIsoPtMax < 1.0) || ((HLT_IsoMu15_L1ETM20_v3 && MuonPt > 15) && run >= 175860 && run <= 180252&&L1JetEt \
> 52 && hasMatchedL1Jet&&hasMatchedL2Jet == 1 && L2JetEt > 35&&l25Et > 35 && foundTracksInJet && l25Pt > 20&&primaryVertexIsValid && l25TrkIsoPtMax < 1.0))")
        num2   = And(offlineSelection,"HLT_IsoMu17_v14 && MuonPt > 17&&L1JetEt > 52 && hasMatchedL1Jet&&hasMatchedL2Jet == 1 && L2JetEt > 35&&l25Et > 35 && foundTracksInJet && l25Pt > 20&&primaryVertexIsValid && l25TrkIsoPtMax < 1.0")

    efficiency = plotter.plotEfficiency(prefix+"Tau3_L1HLT_PFTauPt", "PFTauPt>>hnumpt", num1, denom1, num2, denom2, mcWeight, opts=optspt, xlabel=xlabel, ylabel="Level-1 + HLT tau efficiency", fit=True, fitMin=20., fitMax=150., drawText=True, printResults=True)

    denom1pt = And(denom1, offlineTauPt40)
    denom2pt = And(denom2, offlineTauPt40)
    num1pt = And(num1, offlineTauPt40)
    num2pt = And(num2, offlineTauPt40)
    plotter.plotEfficiency(prefix+"Tau4_L1HLT_PFTauEta", "PFTauEta>>heta(4, -2.1, 2.1)", num1pt, denom1pt, num2pt, denom2pt, mcWeight, xlabel="#tau-jet #eta")
    plotter.plotEfficiency(prefix+"Tau4_L1HLT_PFTauPhi", "PFTauPhi>>heta(4, -3.1416, 3.1416)", num1pt, denom1pt, num2pt, denom2pt, mcWeight, xlabel="#tau-jet #phi")
    plotter.plotEfficiency(prefix+"Tau4_L1HLT_NVtx", "numGoodOfflinePV>>hnumvtx", num1pt, denom1pt, num2pt, denom2pt, mcWeight, opts=optspt, xlabel="Number of good vertices", ylabel="Level-1 + HLT tau efficiency", fit=False, drawText=True, printResults=False)    

    print "\nPlotDir",plotDir
    """
    for i in range(len(vtxbins)-1):
        binlow = vtxbins[i]
        binhigh = vtxbins[i+1]
        vtxSelection = "numGoodOfflinePV > %s"%binlow
        vtxSelection+= " && numGoodOfflinePV <= %s"%binhigh

        label = "vtx"+str(binlow)+"-"+str(binhigh)
        denom1vtx = And(denom1, vtxSelection)
        denom2vtx = And(denom2, vtxSelection)
        num1vtx = And(num1, vtxSelection)
        num2vtx = And(num2, vtxSelection)

        plotter.plotEfficiency(prefix+"Tau3_L1HLT_PFTauPt_"+label, "PFTauPt>>hnumpt", num1vtx, denom1vtx, num2vtx, denom2vtx, mcWeight, opts=optspt, xlabel=xlabel, ylabel="Level-1 + HLT tau efficiency", fit=False, fitMin=20., fitMax=150., drawText=True, printResults=False)

        print "Plotting vtx range",vtxSelection

    """
    #dumpParameters(plotDir,label,runsText,lumi,efficiency)
    pythonWriter.addParameters(selectionName,plotDir,label,runsText,lumi,efficiency)
    pythonWriter.addMCParameters(selectionName,"Fall11_PU_"+pyScenario,efficiency)


def getFilesData(runrange, highPurity):
    tmp = ""
    if highPurity:
        tmp = "-highpurity"
    if runrange < 3:
        return [os.path.join(DATAPATH,"tteffAnalysis_SingleMuRun2011A_Tau_08Nov2011_v6_RAW_RECO_TTEffSkim_v444_V00_10_12_v1/tteffAnalysis-hltpftautight-hpspftau"+tmp+".root")]
    if runrange == 3:
        return [os.path.join(DATAPATH,"tteffAnalysis_SingleMuRun2011A_Tau_08Nov2011_v6_RAW_RECO_TTEffSkim_v444_V00_10_12_v1/tteffAnalysis-hltpftautight-hpspftau"+tmp+".root")]
    if runrange == 4:
#        return [os.path.join(DATAPATH,"tteffAnalysis_SingleMuRun2011B_Tau_PromptSkim_v1_v444_V00_10_01_v2/tteffAnalysis-hltpftau-hpspftau"+tmp+".root")]
        return [os.path.join(DATAPATH,"tteffAnalysis_MET_Run2011B_v1_RAW_v444_V00_10_12_v1/tteffAnalysis-hltpftautight-hpspftau"+tmp+".root")]
    if runrange > 4:
        return [os.path.join(DATAPATH,"tteffAnalysis_SingleMuRun2011A_Tau_08Nov2011_v6_RAW_RECO_TTEffSkim_v444_V00_10_12_v1/tteffAnalysis-hltpftautight-hpspftau"+tmp+".root"),os.path.join(DATAPATH,"tteffAnalysis_MET_Run2011B_v1_RAW_v444_V00_10_12_v1/tteffAnalysis-hltpftautight-hpspftau"+tmp+".root")]
    return [
        # 160431_167913
        ["files/tteffAnalysis_SingleMu_Run2011A_Tau_May10ReReco_v1_v428_1_V00_09_07/tteffAnalysis-hltpftautight-hpspftau"+tmp+".root",
         "files/tteffAnalysis_SingleMu_Run2011A_Tau_PromptSkim_v4_v428_1_V00_09_07/tteffAnalysis-hltpftautight-hpspftau"+tmp+".root",
         ],
        # 170722_173198, Aug05 is missing!
        ["files/tteffAnalysis_SingleMu_Run2011A_Tau_PromptSkim_v6_v428_1_V00_09_07/tteffAnalysis-hltpftautight-hpspftau"+tmp+".root"],
        # 173236_173692_v428
        ["files/tteffAnalysis_SingleMu_Run2011A_Tau_PromptSkim_v6_v428_1_V00_09_07/tteffAnalysis-hltpftautight-hpspftau"+tmp+".root"]
        ][runrange-1]
    

def getFilesMc(highPurity):
    tmp = ""
    if highPurity:
        tmp += "-highpurity"
    return [os.path.join(DATAPATH,"tteffAnalysis_DYToTauTau_M_20_CT10_TuneZ2_7TeV_powheg_pythia_tauola_Fall11_PU_S6_START42_V14B_v1_RAW__v444_V00_10_01_v3/tteffAnalysis-hltpftau-hpspftau"+tmp+".root")]
#    return [os.path.join(DATAPATH,"tteffAnalysis_DYToTauTau_M_20_TuneZ2_7TeV_pythia6_tauola_Fall11_PU_S6_START42_V14B_v1_v444_V00_10_01_v3/tteffAnalysis-hltpftau-hpspftau"+tmp+".root")]
#files/tteffAnalysis_DYtoTauTau_M-20_TuneP0_7TeV-pythia6-tauola_Summer11-PU_S4_START42_V11-v2_v428_1_V00_09_07/tteffAnalysis-hltpftautight-hpspftau"+tmp+".root"]


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
                    histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy
                else:
                    histograms.addText(x, y, "Data (runs %s)"%self.runs, size); y -= dy
                    histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy
                    y -= 0.01
                    histograms.addText(x, y, "MC", size, color=mcColor); y -= dy
                    histograms.addText(x, y, "L1:  %s" % self.l1TriggerName2, size, color=mcColor); y -= dy
                    histograms.addText(x, y, "HLT: %s" % self.hltTriggerName2, size, color=mcColor); y -= dy
            else:
                histograms.addText(x, y, "Data (runs %s)"%self.runs, size); y -= dy
                histograms.addText(x, y, "L1:  %s" % self.l1TriggerName1, size); y -= dy
                histograms.addText(x, y, "HLT: %s" % self.hltTriggerName1, size); y -= dy

        if printResults:
            ratioweighted = 0
            weight = 0
            ratio = p.ratios[0]
            print
            for bin in xrange(1, n1.GetNbinsX()+1):
                i = bin-1
                print "Bin low edge %.0f" % n1.GetBinLowEdge(bin)
                print "   1: efficiency %.7f +- %.7f" % (eff1.GetY()[i], max(eff1.GetErrorYhigh(i), eff1.GetErrorYlow(i))), "Entries num",n1.GetBinContent(bin),"denom",d1.GetBinContent(bin)
                print "   2: efficiency %.7f +- %.7f" % (eff2.GetY()[i], max(eff2.GetErrorYhigh(i), eff2.GetErrorYlow(i))), "Entries num",n2.GetBinContent(bin),"denom",d2.GetBinContent(bin)
                print "   ratio:        %.7f +- %.7f" % (ratio.getRootGraph().GetY()[i], max(ratio.getRootGraph().GetErrorYhigh(i), ratio.getRootGraph().GetErrorYlow(i)))
                if n1.GetBinLowEdge(bin) >= 40:
                    weight += n1.GetBinContent(bin)
                    ratioweighted += n1.GetBinContent(bin)*max(eff1.GetErrorYhigh(i), eff1.GetErrorYlow(i))
            print
            print "Weighted uncert PFTau > 40:", ratioweighted/weight
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
