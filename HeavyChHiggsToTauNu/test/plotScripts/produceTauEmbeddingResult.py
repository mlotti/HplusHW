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

dirEmbs = tauEmbedding.dirEmbs
dirSig = tauEmbedding.dirSig

def main():
    datasetsEmb = tauEmbedding.DatasetsMany(dirEmbs, analysisEmb+"Counters", normalizeMCByLuminosity=False)
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")
    datasetsEmb.forEach(lambda d: d.mergeData())
    datasetsEmb.setLumiFromData()

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

class EventCounterDYCorrection:
    def __init__(self, datasetsDYCorrection, counters=None, **kwargs):
        self.datasetsDYCorrection = datasetsDYCorrection

        countersSig = counters
        if countersSig != None:
            countersSig = datasetsDYCorrection._replaceSigName(countersSig)

        self.eventCounterEmb = tauEmbedding.EventCounterMany(datasetsDYCorrection.datasetsEmb, counters=counters, **kwargs)
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
