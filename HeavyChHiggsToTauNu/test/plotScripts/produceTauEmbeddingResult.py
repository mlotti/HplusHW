#!/usr/bin/env python

######################################################################
#
# Produce a ROOT file with the histograms/counters from tau embedding
# as correctly normalized etc.
#
# The input is a set of multicrab directories produced with
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1" command line arguments
# and one multicrab directory with
# * signalAnalysis_cfg.py with "doTauEmbeddingLikePreselection=True" in the config file
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
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

#analysisEmb = "signalAnalysis"
#analysisSig = "signalAnalysis"
analysisEmb = "signalAnalysisCaloMet60TEff"
analysisSig = "signalAnalysisGenuineTau"

#analysisEmb = analysisEmb+"JESPlus03eta02METPlus00"
#analysisEmb = analysisEmb+"JESMinus03eta02METPlus00"

output = "histograms-ewk.root"

dirEmbs_120109 = [
#    "multicrab_signalAnalysis_v13_3_Run2011A_120104_150358",
#    "multicrab_signalAnalysis_Met50_v13_2_seedTest1_Run2011A_111219_213247",
#    "multicrab_signalAnalysis_v13_2_seedTest2_Run2011A_111220_000831",

    "multicrab_signalAnalysis_Met50_systematics_v13_3_Run2011A_120109_140527",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest1_Run2011A_120109_141906",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest2_Run2011A_120109_143132",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest3_Run2011A_120108_112224",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest4_Run2011A_120108_144749",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest5_Run2011A_120108_151542",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest6_Run2011A_120109_085259",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest7_Run2011A_120109_090954",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest8_Run2011A_120109_092254",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest9_Run2011A_120109_093600",
    ]
dirEmbs_120118 = [
    "multicrab_signalAnalysis_Met50_systematics_v13_3_Run2011A_120118_140348",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest1_Run2011A_120118_160858",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest2_Run2011A_120118_163209",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest3_Run2011A_120118_165326",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest4_Run2011A_120118_171624",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest5_Run2011A_120118_174036",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest6_Run2011A_120118_180507",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest7_Run2011A_120118_182839",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest8_Run2011A_120118_185055",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest9_Run2011A_120118_191252",
    ]

dirEmbs_120126 = [
    "multicrab_signalAnalysis_Met50_systematics_v13_3_Run2011A_120126_100639",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest1_Run2011A_120126_103205",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest2_Run2011A_120126_105224",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest3_Run2011A_120126_111220",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest4_Run2011A_120126_113344",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest5_Run2011A_120126_115504",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest6_Run2011A_120126_190657",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest7_Run2011A_120126_123557",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest8_Run2011A_120126_125610",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest9_Run2011A_120126_131446",
]
dirEmbs_120131 = [
    "multicrab_signalAnalysis_Met50_systematics_v13_3_Run2011A_120131_123142",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest1_Run2011A_120131_133727",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest2_Run2011A_120131_135817",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest3_Run2011A_120131_141821",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest4_Run2011A_120131_143855",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest5_Run2011A_120131_145907",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest6_Run2011A_120131_152041",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest7_Run2011A_120131_154149",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest8_Run2011A_120131_160339",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest9_Run2011A_120131_162422",
]

#dirEmbs = dirEmbs_120109
#dirEmbs = dirEmbs_120118
#dirEmbs = dirEmbs_120126
dirEmbs = dirEmbs_120131

#    dirSig = "../../multicrab_compareEmbedding_Run2011A_111201_143238
#dirSig = "../multicrab_compareEmbedding_Run2011A_111219_185818"
#dirSig = "../multicrab_compareEmbedding_Run2011A_120116_154158" # for 120109
dirSig = "../multicrab_compareEmbedding_Run2011A_120118_122555" # for 120118, 120126, 120131

uncertaintyByAverage = False

def main():
    datasetsEmb = DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=False)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")
    datasetsEmb.forEach(lambda d: d.mergeData())
    datasetsEmb.setLumiFromData()

#    nonDyMc = ["QCD_Pt20_MuEnriched", "WJets", "TTJets", "SingleTop", "Diboson"]
#    datasetsEmb.remove(nonDyMc)
#    datasetsSig.remove(nonDyMc)

    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"


    taskDir = multicrab.createTaskDir("embedded")

    f = open(os.path.join(taskDir, "codeVersion.txt"), "w")
    f.write(git.getCommitId()+"\n")
    f.close()
    f = open(os.path.join(taskDir, "codeStatus.txt"), "w")
    f.write(git.getStatus()+"\n")
    f.close()
    f = open(os.path.join(taskDir, "codeDiff.txt"), "w")
    f.write(git.getDiff()+"\n")
    f.close()
    f = open(os.path.join(taskDir, "inputInfo.txt"), "w")
    f.write("Embedded directories:\n%s\n\nNormal directory:\n%s\n" % ("\n".join(dirEmbs), dirSig))
    f.write("\nEmbedded analysis: %s\nNormal analysis: %s\n" % (analysisEmb, analysisSig))
    f.close()

    operate = lambda dn: operateDataset(taskDir, datasetsEmb, datasetsSig, dn)

    operate("Data")
    operate("DYJetsToLL_M50_TuneZ2_Summer11")
    operate("WW_TuneZ2_Summer11")

    # of = ROOT.TFile.Open(output, "RECREATE")

    # addConfigInfo(of, datasetsEmb, dirEmbs, dirSig)

    # adder = RootHistoAdder(datasetsEmb, datasetsSig)
    # counters = "Counters/weighted"
    # def addHistos(name):
    #     adder.addRootHistos(of, name, analysisEmb, analysisSig)
    #     adder.addRootHistos(of, name+counters, analysisEmb+counters, analysisSig+counters, isCounter=True)

    # addHistos("signalAnalysis")
    # adder.embeddingOnly()
    # addHistos("signalAnalysisEmbedding")
    # adder.dyCorrectionOnly()
    # addHistos("signalAnalysisDYCorrection")

    # of.Close()

def operateDataset(taskDir, datasetsEmb, datasetsSig, datasetName):
    directory = os.path.join(taskDir, datasetName, "res")
    os.makedirs(directory)
    of = ROOT.TFile.Open(os.path.join(directory, "histograms-%s.root" % datasetName), "RECREATE")

    addConfigInfo(of, datasetsEmb.getDatasetFromFirst(datasetName))

    of.cd()

    counters = "Counters/weighted"
    if datasetName == "Data":
        adder = RootHistoAdder(datasetsEmb, datasetName)
        def addDataHistos(mainDir="signalAnalysis", subDir="", **kwargs):
            adder.addRootHistos(of, mainDir+subDir, analysisEmb+subDir, **kwargs)
        def addDataCounters(mainDir="signalAnalysis", subDir="", **kwargs):
            addDataHistos(mainDir, subDir=subDir+counters, isCounter=True, **kwargs)

        def addJESData(case):
            addDataHistos(subDir=case, only=["transverseMass", "transverseMassAfterDeltaPhi160", "transverseMassAfterDeltaPhi130"])
            addDataCounters(subDir=case)

        addDataHistos()
        addDataCounters()

        # tau ES uncertainty by variation
        addJESData("JESPlus03eta02METPlus00")
        addJESData("JESPlus03eta02METMinus00")
        addJESData("JESMinus03eta02METPlus00")
        addJESData("JESMinus03eta02METMinus00")

    else:
        adder = RootHistoAdderResidual(datasetsEmb, datasetsSig, datasetName)
        def addMcHistos(mainDir="signalAnalysis", subDir="", **kwargs):
            adder.addRootHistos(of, mainDir+subDir, analysisEmb+subDir, analysisSig+subDir, **kwargs)
        def addMcCounters(mainDir="signalAnalysis", subDir="", **kwargs):
            addMcHistos(mainDir, subDir=subDir+counters, isCounter=True, **kwargs)

        ## Normal results
        addMcHistos()
        addMcCounters()

        ## Systematics

        # Trigger
        # Uncertainties in normal and embedded have independent nature, square sum
        # Store counters and ScaleFactorUncertainties from both embedded and normal
        adder.setEmbeddedOnly(True)
        addMcHistos(mainDir="signalAnalysisEmbedded", only="ScaleFactorUncertainties")
        addMcCounters(mainDir="signalAnalysisEmbedded")
        adder.setEmbeddedOnly(False)
        adder.setNormalOnly(True)
        addMcHistos(mainDir="signalAnalysisNormal", only="ScaleFactorUncertainties")
        addMcCounters(mainDir="signalAnalysisNormal")
        adder.setNormalOnly(False)
        

        # JES
        # Uncertainties are in same direction in both => for each variated case produce residual counts
        def addJES(case):
            addMcHistos(subDir=case, only=["transverseMass", "transverseMassAfterDeltaPhi160", "transverseMassAfterDeltaPhi130"])
            addMcCounters(subDir=case)
        addJES("JESPlus03eta02METPlus10")
        addJES("JESPlus03eta02METMinus10")
        addJES("JESMinus03eta02METPlus10")
        addJES("JESMinus03eta02METMinus10")

        # Lepton veto
        # Pick the values only from normal (already done for trigger)

        # btag (mistag)
        # Pick the values only from normal
        # In addition of counters, need a few histograms (already done for trigger)

        # PU
        # Same story as for JES
        addMcCounters(subDir="PUWeightPlus")
        addMcCounters(subDir="PUWeightMinus")

    of.Close()


def addConfigInfo(of, dataset):
    d = of.mkdir("configInfo")
    d.cd()

    # configinfo histogram
    configinfo = ROOT.TH1F("configinfo", "configinfo", 3, 0, 3)
    axis = configinfo.GetXaxis()

    def setValue(bin, name, value):
        axis.SetBinLabel(bin, name)
        configinfo.SetBinContent(bin, value)

    setValue(1, "control", 1)
    if dataset.isData():
        setValue(2, "luminosity", dataset.getLuminosity())
        setValue(3, "isData", 1)
    elif dataset.isMC():
        setValue(2, "crossSection", dataset.getCrossSection())
        setValue(3, "isData", 0)

    configinfo.Write()
    configinfo.Delete()

    # dataVersion
    ds = dataset
    if dataset.isData():
        ds = dataset.datasets[0]

    dataVersion = ROOT.TNamed("dataVersion", ds.dataVersion)
    dataVersion.Write()
    dataVersion.Delete()

    # codeVersion
    codeVersion = ROOT.TNamed("codeVersion", git.getCommitId())
    codeVersion.Write()
    codeVersion.Delete()

    of.cd()

class RootHistoAdder:
    def __init__(self, datasetsEmb, datasetName):
        self.datasetsEmb = datasetsEmb
        self.datasetName = datasetName

    def addRootHistos(self, of, dstName, srcEmbName, isCounter=False, only=None):
        split = dstName.split("/")
        thisDir = of
        for s in split:
            thisDir = thisDir.mkdir(s)

        arbitraryDataset = self.datasetsEmb.getDatasetFromFirst(self.datasetName)

        subdirectories = arbitraryDataset.getDirectoryContent(srcEmbName, lambda x: isinstance(x, ROOT.TDirectory))
        histograms = arbitraryDataset.getDirectoryContent(srcEmbName, lambda x: isinstance(x, ROOT.TH1) and not isinstance(x, ROOT.TH2))
        
        if only != None:
            func = lambda n: n in only
            subdirectories = filter(func, subdirectories)
            histograms = filter(func, histograms)

        thisDir.cd()
        for hname in histograms:
            self.writeRootHisto(thisDir, hname, srcEmbName+"/"+hname, isCounter)

        for dirname in subdirectories:
            self.addRootHistos(thisDir, dirname, srcEmbName+"/"+dirname, isCounter)

        of.cd()

    def writeRootHisto(self, directory, dstName, srcEmbName, isCounter):
        if not self.datasetsEmb.hasHistogram(self.datasetName, srcEmbName):
            return
    
        # Get properly normalized embedded data
        (embDataHisto, tmp) = self.datasetsEmb.getHistogram(self.datasetName, srcEmbName)

        histo = None
        if isCounter:
            embDataCounter = counter.HistoCounter("EmbData", embDataHisto)
            table = counter.CounterTable()
            table.appendColumn(embDataCounter)
            column = table.getColumn(name="EmbData")
            histo = dataset._counterToHisto(dstName, column.getPairList())
        else:
            histo = embDataHisto
        
        histo.SetName(dstName)
        histo.SetDirectory(directory)
        histo.Write()
    
        histo.Delete() # could this help???

        print "%s/%s" % (directory.GetPath(), dstName)

class RootHistoAdderResidual:
    def __init__(self, datasetsEmb, datasetsSig, datasetName):
        self.datasetsEmb = datasetsEmb
        self.datasetSig = datasetsSig.getDataset(datasetName)
        self.datasetName = datasetName

        self.normalOnly = False
        self.embeddedOnly = False

    def setNormalOnly(self, value):
        self.normalOnly = value

    def setEmbeddedOnly(self, value):
        self.embeddedOnly = value

    def addRootHistos(self, of, dstName, srcEmbName, srcSigName, isCounter=False, only=None):
        split = dstName.split("/")
        thisDir = of
        for s in split:
            thisDir = thisDir.mkdir(s)

        arbitraryDataset = self.datasetsEmb.getDatasetFromFirst(self.datasetName)

        subdirectories = arbitraryDataset.getDirectoryContent(srcEmbName, lambda x: isinstance(x, ROOT.TDirectory))
        histograms = arbitraryDataset.getDirectoryContent(srcEmbName, lambda x: isinstance(x, ROOT.TH1) and not isinstance(x, ROOT.TH2))
        if only != None:
            func = lambda n: n in only
            subdirectories = filter(func, subdirectories)
            histograms = filter(func, histograms)

        thisDir.cd()
        for hname in histograms:
            self.writeRootHisto(thisDir, hname, srcEmbName+"/"+hname, srcSigName+"/"+hname, isCounter)

        for dirname in subdirectories:
            self.addRootHistos(thisDir, dirname, srcEmbName+"/"+dirname, srcSigName+"/"+dirname, isCounter)

        of.cd()

    def writeRootHisto(self, directory, dstName, srcEmbName, srcSigName, isCounter):
        if not self.datasetsEmb.hasHistogram(self.datasetName, srcEmbName) or not self.datasetSig.hasRootHisto(srcSigName):
            return

        histo = None
        # Get properly normalized embedded and normal MC
        (embMcHisto, tmp) = self.datasetsEmb.getHistogram(self.datasetName, srcEmbName)
        sigMcHisto = self.datasetSig.getDatasetRootHisto(srcSigName).getHistogram() # ROOT.TH1

        #print embMcHisto, sigMcHisto

        if self.normalOnly:
            histo = sigMcHisto
        elif self.embeddedOnly:
            histo = embMcHisto
        else:
        
            if isCounter:
                embMcCounter = counter.HistoCounter("EmbMc", embMcHisto)
                sigMcCounter = counter.HistoCounter("SigMc", sigMcHisto)
    
                table = counter.CounterTable()
                table.appendColumn(embMcCounter)
                table.appendColumn(sigMcCounter)
    
                table.removeNonFullRows()
                if table.getNrows() == 0:
                    return
    
                embMcColumn = table.getColumn(name="EmbMc")
                sigMcColumn = table.getColumn(name="SigMc")
                residual = counter.subtractColumn("Correction", sigMcColumn, embMcColumn)
                histo = dataset._counterToHisto(dstName, residual.getPairList())
            else:
                # Residual MC: normal-embedded
                sigMcHisto.Add(embMcHisto, -1)
                histo = sigMcHisto
        
        histo.SetName(dstName)
        histo.SetDirectory(directory)
        histo.Write()
    
        histo.Delete() # could this help???

        print "%s/%s" % (directory.GetPath(), dstName)


class DatasetsMany:
    def __init__(self, dirs, counters, normalizeMCByLuminosity=False):
        self.datasetManagers = []
        for d in dirs:
            datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=d+"/multicrab.cfg", counters=counters)
            datasets.loadLuminosities()
            tauEmbedding.updateAllEventsToWeighted(datasets)
            self.datasetManagers.append(datasets)

        self.normalizeMCByLuminosity=normalizeMCByLuminosity

    def forEach(self, function):
        for dm in self.datasetManagers:
            function(dm)

    # Compatibility with dataset.DatasetManager
    def remove(self, *args, **kwargs):
        self.forEach(lambda d: d.remove(*args, **kwargs))

    def getAllDatasetNames(self):
        return self.datasetManagers[0].getAllDatasetNames()

    def close(self):
        self.forEach(lambda d: d.close())

    # End of compatibility methods
    def getDatasetFromFirst(self, name):
        return self.datasetManagers[0].getDataset(name)

    def setLumiFromData(self):
        self.lumi = self.getDatasetFromFirst("Data").getLuminosity()

    def getLuminosity(self):
        return self.lumi

    def getHistogram(self, datasetName, name, rebin=1):
        histos = self.getHistograms(datasetName, name)

        # Averaging is done here
        histo = histos[0]
        histo_low = histo.Clone(histo.GetName()+"_low")
        histo_high = histo.Clone(histo.GetName()+"_high")
        for h in histos[1:]:
            for bin in xrange(0, histo.GetNbinsX()+2):
                histo.SetBinContent(bin, histo.GetBinContent(bin)+h.GetBinContent(bin))
                if uncertaintyByAverage:
                    histo.SetBinError(bin, histo.GetBinError(bin)+h.GetBinError(bin))
                else:
                    histo.SetBinError(bin, math.sqrt(histo.GetBinError(bin)**2+h.GetBinError(bin)**2))

                histo_low.SetBinContent(bin, min(histo_low.GetBinContent(bin), h.GetBinContent(bin)))
                histo_high.SetBinContent(bin, max(histo_high.GetBinContent(bin), h.GetBinContent(bin)))

        for bin in xrange(0, histo.GetNbinsX()+2):
            histo.SetBinContent(bin, histo.GetBinContent(bin)/len(histos))
            if uncertaintyByAverage:
                histo.SetBinError(bin, histo.GetBinError(bin)/len(histos))
            else:
                histo.SetBinError(bin, histo.GetBinError(bin)/len(histos))

        if rebin > 1:
            histo.Rebin(rebin)
            histo_low.Rebin(rebin)
            histo_high.Rebin(rebin)

        binCenters = []
        values = []
        errLow = []
        errHigh = []
        for bin in xrange(1, histo.GetNbinsX()+1):
            binCenters.append(histo.GetXaxis().GetBinCenter(bin))
            values.append(histo.GetBinContent(bin))
            errLow.append(histo.GetBinContent(bin) - histo_low.GetBinContent(bin))
            errHigh.append(histo_high.GetBinContent(bin) - histo.GetBinContent(bin))

        gr = ROOT.TGraphAsymmErrors(len(binCenters),
                                    array.array("d", binCenters), array.array("d", values),
                                    array.array("d", [0]*len(binCenters)), array.array("d", [0]*len(binCenters)),
                                    array.array("d", errLow), array.array("d", errHigh))

        histo.SetName("Average")

        return (histo, gr) # Average histogram, min/max graph

    def hasHistogram(self, datasetName, name):
        has = True
        for dm in self.datasetManagers:
            has = has and dm.getDataset(datasetName).hasRootHisto(name)
        return has

    def getHistograms(self, datasetName, name):
        histos = []
        for i, dm in enumerate(self.datasetManagers):
            ds = dm.getDataset(datasetName)
            h = ds.getDatasetRootHisto(name)
            if h.isMC() and self.normalizeMCByLuminosity:
                h.normalizeToLuminosity(self.lumi)
            h = histograms.HistoWithDataset(ds, h.getHistogram(), "dummy") # only needed for scaleNormalization()
            tauEmbedding.scaleNormalization(h)
            h = h.getRootHisto()
            h.SetName("Trial %d"%(i+1))
            histos.append(h)

        return histos # list of individual histograms

    def getCounter(self, datasetName, name):
        (embDataHisto, tmp) = self.getHistogram(datasetName, name)
        return counter.HistoCounter(datasetName, embDataHisto)

class DatasetsResidual:
    def __init__(self, datasetsEmb, datasetsSig, analysisEmb, analysisSig, residualNames, totalNames=[]):
        self.datasetsEmb = datasetsEmb
        self.datasetsSig = datasetsSig

        # For an ugly hack
        self.analysisEmb = analysisEmb
        self.analysisSig = analysisSig

        self.residualNames = residualNames
        self.totalNames = totalNames
        for name in totalNames:
            if name in residualNames:
                raise Exception("residualNames and totalNames must be disjoint (dataset '%s' was given in both)")

    def _replaceSigName(self, name):
        if isinstance(name, basestring):
            return name.replace(self.analysisEmb, analysisSig)
        else:
            return name.clone(tree=lambda name: name.replace(self.analysisEmb, self.analysisSig))

    def forEach(self, function):
        self.datasetsEmb.forEach(function)
        function(self.datasetsSig)

    # Compatibility with dataset.DatasetManager
    def remove(self, *args, **kwargs):
        self.forEach(lambda d: d.remove(*args, **kwargs))

    def getAllDatasetNames(self):
        return self.datasetsEmb.getAllDatasetNames()

    def close(self):
        self.forEach(self, lambda d: d.close())

    # End of compatibility methods
    
    def getLuminosity(self):
        return self.datasetsEmb.getLuminosity()

    def hasHistogram(self, datasetName, name):
        return self.datasetsEmb.hasHistogram(datasetName, name) and self.datasetsSig.getDataset(datasetName).hasHistogram(name)

    def getHistogram(self, datasetName, name, rebin=1):
        if datasetName in self.totalNames:
            #print "Creating sum for "+datasetName
            (histo, tmp) = self.datasetsEmb.getHistogram(datasetName, name, rebin)
            for res in self.residualNames:
                #print "From residual of "+res
                (h, tmp) = self.getHistogram(res, name, rebin)
                histo.Add(h)
            return (histo, None)
        elif not datasetName in self.residualNames:
            return self.datasetsEmb.getHistogram(datasetName, name)

        #print "Calculating residual of "+datasetName

        # Ugly hack
        sigName = self._replaceSigName(name)

        # Get properly normalized embedded data, embedded DY and normal DY histograms
        (embHisto, tmp) = self.datasetsEmb.getHistogram(datasetName, name)
        sigHisto = self.datasetsSig.getDataset(datasetName).getDatasetRootHisto(sigName) # DatasetRootHisto
        sigHisto.normalizeToLuminosity(self.datasetsEmb.getLuminosity())
        sigHisto = sigHisto.getHistogram() # ROOT.TH1

        # residual = normal-embedded
        sigHisto.Add(embHisto, -1)

        sigHisto.SetName(embHisto.GetName()+"Residual")
        if rebin > 1:
            sigHisto.Rebin(rebin)

        return (sigHisto, None)

    def getCounter(self, datasetName, name):
        if not datasetName in self.residualNames:
            return self.datasetsEmb.getCounter(datasetName, name)

        # Ugly hack
        sigName = name
        if isinstance(sigName, basestring):
            sigName = sigName.replace(self.analysisEmb, self.analysisSig)
        else:
            sigName = sigName.clone(tree=sigName.tree.replace(self.analysisEmb, self.analysisSig))

        # Get properly normalized embedded data, embedded DY and normal DY histograms
        (embHisto, tmp) = self.datasetsEmb.getHistogram(datasetName, name)
        sigHisto = self.datasetsSig.getDataset(datasetName).getDatasetRootHisto(sigName) # DatasetRootHisto
        sigHisto.normalizeToLuminosity(self.datasetsEmb.getLuminosity())
        sigHisto = sigHisto.getHistogram() # ROOT.TH1

        table = counter.CounterTable()
        table.appendColumn(counter.HistoCounter("Embedded", embHisto))
        table.appendColumn(counter.HistoCounter("Normal", sigHisto))
        table.removeNonFullRows()

        embColumn = table.getColumn(name="Embedded")
        sigColumn = table.getColumn(name="Normal")
        residual = counter.subtractColumn(datasetName+" residual", sigColumn, embColumn)
        return residual


class DatasetsDYCorrection:
    def __init__(self, datasetsEmb, datasetsSig, analysisEmb, analysisSig):
        self.datasetsEmb = datasetsEmb
        self.datasetsSig = datasetsSig

        # For an ugly hack
        self.analysisEmb = analysisEmb
        self.analysisSig = analysisSig

    def _replaceSigName(self, name):
        if isinstance(name, basestring):
            return name.replace(self.analysisEmb, analysisSig)
        else:
            return name.clone(tree=lambda name: name.replace(self.analysisEmb, self.analysisSig))

    def forEach(self, function):
        self.datasetsEmb.forEach(function)
        function(self.datasetsSig)

    # Compatibility with dataset.DatasetManager
    def remove(self, *args, **kwargs):
        self.forEach(lambda d: d.remove(*args, **kwargs))

    def getAllDatasetNames(self):
        return self.datasetsEmb.getAllDatasetNames()

    def forEach(self, function):
        self.datasetsEmb.forEach(function)
        function(self.datasetsSig)

    # End of compatibility methods
    
    def getLuminosity(self):
        return self.datasetsEmb.getLuminosity()

    def hasHistogram(self, datasetName, name):
        return self.datasetsEmb.hasHistogram(datasetName, name) and self.datasetsSig.getDataset(datasetName).hasHistogram(name)


    def getHistogram(self, datasetName, name, rebin=1):
        if not datasetName in ["Data", "EWKMC", "DYJetsToLL"]:
            return self.datasetsEmb.getHistogram(datasetName, name)

        # Ugly hack
        sigName = self._replaceSigName(name)

        # Get properly normalized embedded data, embedded DY and normal DY histograms
        (embDataHisto, tmp) = self.datasetsEmb.getHistogram(datasetName, name)
        (embDyHisto, tmp) = self.datasetsEmb.getHistogram("DYJetsToLL", name)
        sigDyHisto = self.datasetsSig.getDataset("DYJetsToLL").getDatasetRootHisto(sigName) # DatasetRootHisto
        sigDyHisto.normalizeToLuminosity(self.datasetsEmb.getLuminosity())
        sigDyHisto = sigDyHisto.getHistogram() # ROOT.TH1


        histo = embDataHisto
        # DY: normal-embedded
        sigDyHisto.Add(embDyHisto, -1)

        # data(Embedded) + DY(normal-embeded)
        histo.Add(sigDyHisto)
        
        histo.SetName(histo.GetName()+"DYCorrected")

        if rebin > 1:
            histo.Rebin(rebin)

        return (histo, None)

    def getCounter(self, datasetName, name):
        if not datasetName in ["Data", "EWKMC", "DYJetsToLL"]:
            (embDataHisto, tmp) = self.datasetsEmb.getHistogram(datasetName, name)
            return counter.HistoCounter(datasetName, embDataHisto)

        # Ugly hack
        sigName = name
        if isinstance(sigName, basestring):
            sigName = sigName.replace(self.analysisEmb, self.analysisSig)
        else:
            sigName = sigName.clone(tree=sigName.tree.replace(self.analysisEmb, self.analysisSig))

        # Get properly normalized embedded data, embedded DY and normal DY histograms
        (embDataHisto, tmp) = self.datasetsEmb.getHistogram(datasetName, name)
        (embDyHisto, tmp) = self.datasetsEmb.getHistogram("DYJetsToLL", name)
        sigDyHisto = self.datasetsSig.getDataset("DYJetsToLL").getDatasetRootHisto(sigName) # DatasetRootHisto
        sigDyHisto.normalizeToLuminosity(self.datasetsEmb.getLuminosity())
        sigDyHisto = sigDyHisto.getHistogram() # ROOT.TH1

        embDataCounter = counter.HistoCounter("EmbData", embDataHisto)
        embDyCounter = counter.HistoCounter("EmbDy", embDyHisto)
        sigDyCounter = counter.HistoCounter("SigDy", sigDyHisto)

        table = counter.CounterTable()
        table.appendColumn(embDataCounter)
        table.appendColumn(embDyCounter)
        table.appendColumn(sigDyCounter)

        table.removeNonFullRows()

        column = table.getColumn(name="EmbData")
        embDyColumn = table.getColumn(name="EmbDy")
        sigDyColumn = table.getColumn(name="SigDy")
        dyCorrection = counter.subtractColumn("Correction", sigDyColumn, embDyColumn)
        column = counter.sumColumn(datasetName, [column, dyCorrection])

        return column


class EventCounterMany:
    def __init__(self, datasetsMany, scaleNormalization=True, *args, **kwargs):
        self.eventCounters = []
        for dsMgr in datasetsMany.datasetManagers:
            ec = counter.EventCounter(dsMgr, *args, **kwargs)
            ec.normalizeMCToLuminosity(datasetsMany.getLuminosity())
            if scaleNormalization:
                tauEmbedding.scaleNormalization(ec)
            self.eventCounters.append(ec)

    def removeColumns(self, datasetNames):
        for ec in self.eventCounters:
            ec.removeColumns(datasetNames)

    def mainCounterAppendRow(self, *args, **kwargs):
        for ec in self.eventCounters:
            ec.getMainCounter().appendRow(*args, **kwargs)

    def subCounterAppendRow(self, name, *args, **kwargs):
        for ec in self.eventCounters:
            ec.getSubCounter(name).appendRow(*args, **kwargs)

    def getMainCounterTable(self):
        return counter.meanTable([ec.getMainCounterTable() for ec in self.eventCounters], uncertaintyByAverage)

    def getSubCounterTable(self, name):
        return counter.meanTable([ec.getSubCounterTable(name) for ec in self.eventCounters], uncertaintyByAverage)

    def getMainCounterTableFit(self):
        return counter.meanTableFit([ec.getMainCounterTable() for ec in self.eventCounters])

    def getSubCounterTableFit(self, name):
        return counter.meanTableFit([ec.getSubCounterTable(name) for ec in self.eventCounters])

    def getNormalizationString(self):
        return self.eventCounters[0].getNormalizationString()

class EventCounterResidual:
    def __init__(self, datasetsResidual, counters=None, **kwargs):
        self.datasetsResidual = datasetsResidual
        self.residualNames = datasetsResidual.residualNames

        countersSig = counters
        if countersSig != None:
            countersSig = datasetsResidual._replaceSigName(countersSig)

        self.eventCounterEmb = EventCounterMany(datasetsResidual.datasetsEmb, counters=counters, **kwargs)
        self.eventCounterSig = counter.EventCounter(datasetsResidual.datasetsSig, counters=countersSig, **kwargs)
        self.eventCounterSig.normalizeMCToLuminosity(datasetsResidual.datasetsEmb.getLuminosity())

    def mainCounterAppendRow(self, rowName, treeDraw):
        treeDrawSig = self.datasetsDYCorrection._replaceSigName(treeDraw)
        self.eventCounterEmb.mainCounterAppendRow(rowName, treeDraw)
        self.eventCounterSig.getMainCounter().appendRow(rowName, treeDrawSig)

    def subCounterAppendRow(self, name, rowName, treeDraw):
        treeDrawSig = self.datasetsDYCorrection._replaceSigName(treeDraw)
        self.eventCounterEmb.subCounterAppendRow(name, rowName, treeDraw)
        self.eventCounterSig.getSubCounter(name).appendRow(rowName, treeDrawSig)

    def _calculateResidual(self, table, sigTable):
        columnNames = table.getColumnNames()
        for name in columnNames:
            if name in self.residualNames:
                i = columnNames.index(name)
                col = table.getColumn(index=i)
                table.removeColumn(i)
                col = counter.subtractColumn(name+" residual", sigTable.getColumn(name=name), col)
                table.insertColumn(i, col)
        return table

    def getMainCounterTable(self):
        table = self.eventCounterEmb.getMainCounterTable()
        sigTable = self.eventCounterSig.getMainCounterTable()
        
        table = self._calculateResidual(table, sigTable)
        return table

    def getSubCounterTable(self, name):
        table = self.eventCounterEmb.getSubCounterTable(name)
        sigTable = self.eventCounterSig.getSubCounterTable(name)
        
        table = self._calculateResidual(table, sigTable)
        return table
    
    

class EventCounterDYCorrection:
    def __init__(self, datasetsDYCorrection, counters=None, **kwargs):
        self.datasetsDYCorrection = datasetsDYCorrection

        countersSig = counters
        if countersSig != None:
            countersSig = datasetsDYCorrection._replaceSigName(countersSig)

        self.eventCounterEmb = EventCounterMany(datasetsDYCorrection.datasetsEmb, counters=counters, **kwargs)
        self.eventCounterSig = counter.EventCounter(datasetsDYCorrection.datasetsSig, counters=countersSig, **kwargs)
        self.eventCounterSig.normalizeMCToLuminosity(datasetsDYCorrection.datasetsEmb.getLuminosity())

    def mainCounterAppendRow(self, rowName, treeDraw):
        treeDrawSig = self.datasetsDYCorrection._replaceSigName(treeDraw)
        self.eventCounterEmb.mainCounterAppendRow(rowName, treeDraw)
        self.eventCounterSig.getMainCounter().appendRow(rowName, treeDrawSig)

    def subCounterAppendRow(self, name, rowName, treeDraw):
        treeDrawSig = self.datasetsDYCorrection._replaceSigName(treeDraw)
        self.eventCounterEmb.subCounterAppendRow(name, rowName, treeDraw)
        self.eventCounterSig.getSubCounter(name).appendRow(rowName, treeDrawSig)

    def _correctColumn(self, table, name, correction):
        columnNames = table.getColumnNames()
        i = columnNames.index(name)
        col = table.getColumn(index=i)
        table.removeColumn(i)
        col = counter.sumColumn(name, [col, correction])
        table.insertColumn(i, col)

    def getMainCounterTable(self):
        table = self.eventCounterEmb.getMainCounterTable()
        sigTable = self.eventCounterSig.getMainCounterTable()
        
        sigDyColumn = sigTable.getColumn(name="DYJetsToLL")
        embDyColumn = table.getColumn(name="DYJetsToLL")
        dyCorrection = counter.subtractColumn("Correction", sigDyColumn, embDyColumn)

        if "Data" in table.getColumnNames():
            self._correctColumn(table, "Data", dyCorrection)
        self._correctColumn(table, "DYJetsToLL", dyCorrection)

        return table

    def getSubCounterTable(self, name):
        table = self.eventCounterEmb.getSubCounterTable(name)
        sigTable = self.eventCounterSig.getSubCounterTable(name)
        
        sigDyColumn = sigTable.getColumn(name="DYJetsToLL")
        embDyColumn = table.getColumn(name="DYJetsToLL")
        dyCorrection = counter.subtractColumn("Correction", sigDyColumn, embDyColumn)

        if "Data" in table.getColumnNames():
            self._correctColumn(table, "Data", dyCorrection)
        self._correctColumn(table, "DYJetsToLL", dyCorrection)

        return table
            

if __name__ == "__main__":
    main()
