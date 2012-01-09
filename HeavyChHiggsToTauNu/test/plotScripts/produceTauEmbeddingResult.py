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
import plotTauEmbeddingSignalAnalysis as tauEmbedding

#analysisEmb = "signalAnalysis"
#analysisSig = "signalAnalysis"
analysisEmb = "signalAnalysisCaloMet60TEff"
analysisSig = "signalAnalysisGenuineTau"

output = "histograms-ewk.root"

dirEmbs = [
    "multicrab_signalAnalysis_v13_3_Run2011A_120104_150358",
    "multicrab_signalAnalysis_Met50_v13_2_seedTest1_Run2011A_111219_213247",
    "multicrab_signalAnalysis_v13_2_seedTest2_Run2011A_111220_000831",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest3_Run2011A_120108_112224",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest4_Run2011A_120108_144749",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest5_Run2011A_120108_151542",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest6_Run2011A_120109_085259",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest7_Run2011A_120109_090954",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest8_Run2011A_120109_092254",
    "multicrab_signalAnalysis_Met50_systematics_v13_3_seedTest9_Run2011A_120109_093600",
    ]

#    dirSig = "../../multicrab_compareEmbedding_Run2011A_111201_143238
dirSig = "../multicrab_compareEmbedding_Run2011A_111219_185818"

def main():
    datasetsEmb = DatasetsMany(dirEmbs, analysisEmb+"Counters")
    datasetsSig = dataset.getDatasetsFromMulticrabCfg(cfgfile=dirSig+"/multicrab.cfg", counters=analysisSig+"Counters")
    datasetsEmb.forEach(plots.mergeRenameReorderForDataMC)
    datasetsEmb.setLumiFromData()
    plots.mergeRenameReorderForDataMC(datasetsSig)

    nonDyMc = ["QCD_Pt20_MuEnriched", "WJets", "TTJets", "SingleTop", "Diboson"]
    datasetsEmb.remove(nonDyMc)
    datasetsSig.remove(nonDyMc)

    tauEmbedding.normalize=True
    tauEmbedding.era = "Run2011A"

    of = ROOT.TFile.Open(output, "RECREATE")

    addConfigInfo(of, datasetsEmb, dirEmbs, dirSig)

    adder = RootHistoAdder(datasetsEmb, datasetsSig)
    counters = "Counters/weighted"
    def addHistos(name):
        adder.addRootHistos(of, name, analysisEmb, analysisSig)
        adder.addRootHistos(of, name+counters, analysisEmb+counters, analysisSig+counters, isCounter=True)

    addHistos("signalAnalysis")
    adder.embeddingOnly()
    addHistos("signalAnalysisEmbedding")
    adder.dyCorrectionOnly()
    addHistos("signalAnalysisDYCorrection")

    # aeh, for counters we need something else

    of.Close()


def addConfigInfo(of, datasetsEmb, dirEmbs, dirSig):
    d = of.mkdir("configInfo")
    d.cd()

    # configinfo histogram
    configinfo = ROOT.TH1F("configinfo", "configinfo", 3, 0, 3)
    axis = configinfo.GetXaxis()

    def setValue(bin, name, value):
        axis.SetBinLabel(bin, name)
        configinfo.SetBinContent(bin, value)

    setValue(1, "control", 1)
    setValue(2, "isData", 1)
    setValue(3, "luminosity", datasetsEmb.getLumi())

    configinfo.Write()

    # dataVersion
    firstData = datasetsEmb.getDatasetFromFirst("Data")
    if isinstance(firstData, dataset.DatasetMerged):
        firstData = firstData.datasets[0]

    dataVersion = ROOT.TNamed("dataVersion", firstData.dataVersion)
    dataVersion.Write()

    # codeVersion
    codeVersion = ROOT.TNamed("codeVersion", git.getCommitId())
    codeVersion.Write()

    # Input information
    for i, d in enumerate(dirEmbs):
        tmp = ROOT.TNamed("directoryEmbedded_%d"%i, d)
        tmp.Write()
    tmp = ROOT.TNamed("directorySignal", dirSig)
    tmp.Write()
    tmp = ROOT.TNamed("analysisEmbedded", analysisEmb)
    tmp.Write()
    tmp = ROOT.TNamed("analysisSignal", analysisSig)
    tmp.Write()

    of.cd()

class RootHistoAdder:
    def __init__(self, datasetsEmb, datasetsSig):
        self.datasetsEmb = datasetsEmb
        self.datasetsSig = datasetsSig
        self.dySig = datasetsSig.getDataset("DYJetsToLL")

        self.includeEmbedding = True
        self.includeDY = True

    def fullResult(self):
        self.includeEmbedding = True
        self.includeDY = True

    def embeddingOnly(self):
        self.includeEmbedding = True
        self.includeDY = False

    def dyCorrectionOnly(self):
        self.includeEmbedding = False
        self.includeDY = True
        

    def addRootHistos(self, of, dstName, srcEmbName, srcSigName, isCounter=False):
        split = dstName.split("/")
        thisDir = of
        for s in split:
            thisDir = thisDir.mkdir(s)

        subdirectories = self.dySig.getDirectoryContent(srcSigName, lambda x: isinstance(x, ROOT.TDirectory))
        histograms = self.dySig.getDirectoryContent(srcSigName, lambda x: isinstance(x, ROOT.TH1) and not isinstance(x, ROOT.TH2))

        #print subdirectories
        #print histograms

        thisDir.cd()
        for hname in histograms:
            self.writeRootHisto(thisDir, hname, srcEmbName+"/"+hname, srcSigName+"/"+hname, isCounter)

        for dirname in subdirectories:
            self.addRootHistos(thisDir, dirname, srcEmbName+"/"+dirname, srcSigName+"/"+dirname, isCounter)

        of.cd()

    def writeRootHisto(self, directory, dstName, srcEmbName, srcSigName, isCounter):
        if not self.datasetsEmb.hasHistogram("Data", srcEmbName):
            return
    
        # Get properly normalized embedded data, embedded DY and normal DY histograms
        (embDataHisto, tmp) = self.datasetsEmb.getHistogram("Data", srcEmbName)
        (embDyHisto, tmp) = self.datasetsEmb.getHistogram("DYJetsToLL", srcEmbName)
        sigDyHisto = self.dySig.getDatasetRootHisto(srcSigName) # DatasetRootHisto
        sigDyHisto.normalizeToLuminosity(self.datasetsEmb.getLumi())
        sigDyHisto = sigDyHisto.getHistogram() # ROOT.TH1
    
        histo = None
        if isCounter:
            embDataCounter = counter.HistoCounter("EmbData", embDataHisto)
            embDyCounter = counter.HistoCounter("EmbDy", embDyHisto)
            sigDyCounter = counter.HistoCounter("SigDy", sigDyHisto)

            table = counter.CounterTable()
            table.appendColumn(embDataCounter)
            table.appendColumn(embDyCounter)
            table.appendColumn(sigDyCounter)

            nrows = table.getNrows()
            ncolumns = table.getNcolumns()
            removeRows = []

            for irow in xrange(0, nrows):
                allFull = True
                for icol in xrange(0, ncolumns):
                    if table.getCount(irow, icol) == None:
                        allFull = False
                        break
                if not allFull:
                    removeRows.append(irow-len(removeRows)) # hack to take into account the change in indices when removing a row
            for irow in removeRows:
                table.removeRow(index=irow)

            if table.getNrows() == 0:
                return

            column = None
            if self.includeEmbedding:
                column = table.getColumn(name="EmbData")
            if self.includeDY:
                embDyColumn = table.getColumn(name="EmbDy")
                sigDyColumn = table.getColumn(name="SigDy")
                dyCorrection = counter.subtractColumn("Correction", sigDyColumn, embDyColumn)

                if column == None:
                    column = dyCorrection
                else:
                    column = counter.sumColumn("Corrected", [column, dyCorrection])
            histo = dataset._counterToHisto(dstName, column.getPairList())
                
        else:
            if self.includeEmbedding:
                histo = embDataHisto
            if self.includeDY:
                # DY: normal-embedded
                sigDyHisto.Add(embDyHisto, -1)
    
                if histo == None:
                    histo = sigDyHisto
                else:
                    # data(Embedded) + DY(normal-embeded)
                    histo.Add(sigDyHisto)
        
        histo.SetName(dstName)
        histo.SetDirectory(directory)
        histo.Write()
    
        print "%s/%s" % (directory.GetPath(), dstName)

    

class DatasetsMany:
    def __init__(self, dirs, counters):
        self.datasetManagers = []
        for d in dirs:
            datasets = dataset.getDatasetsFromMulticrabCfg(cfgfile=d+"/multicrab.cfg", counters=counters)
            datasets.loadLuminosities()
            self.datasetManagers.append(datasets)

    def forEach(self, function):
        for dm in self.datasetManagers:
            function(dm)

    # Compatibility with dataset.DatasetManager
    def remove(self, *args, **kwargs):
        self.forEach(lambda d: d.remove(*args, **kwargs))

    # End of compatibility methods
    def getDatasetFromFirst(self, name):
        return self.datasetManagers[0].getDataset(name)

    def setLumiFromData(self):
        self.lumi = self.getDatasetFromFirst("Data").getLuminosity()

    def getLumi(self):
        return self.lumi

    def getHistogram(self, datasetName, name):
        histos = self.getHistograms(datasetName, name)

        histo = histos[0]
        histo_low = histo.Clone(histo.GetName()+"_low")
        histo_high = histo.Clone(histo.GetName()+"_high")
        for h in histos[1:]:
            for bin in xrange(0, histo.GetNbinsX()+2):
                histo.SetBinContent(bin, histo.GetBinContent(bin)+h.GetBinContent(bin))
                histo.SetBinError(bin, histo.GetBinError(bin)+h.GetBinError(bin))

                histo_low.SetBinContent(bin, min(histo_low.GetBinContent(bin), h.GetBinContent(bin)))
                histo_high.SetBinContent(bin, max(histo_high.GetBinContent(bin), h.GetBinContent(bin)))

        for bin in xrange(0, histo.GetNbinsX()+2):
            histo.SetBinContent(bin, histo.GetBinContent(bin)/len(histos))
            histo.SetBinError(bin, histo.GetBinError(bin)/len(histos))

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
            if h.isMC():
                h.normalizeToLuminosity(self.lumi)
            h = histograms.HistoWithDataset(ds, h.getHistogram(), "dummy") # only needed for scaleNormalization()
            tauEmbedding.scaleNormalization(h)
            h = h.getRootHisto()
            h.SetName("Trial %d"%(i+1))
            histos.append(h)

        return histos # list of individual histograms

if __name__ == "__main__":
    main()
