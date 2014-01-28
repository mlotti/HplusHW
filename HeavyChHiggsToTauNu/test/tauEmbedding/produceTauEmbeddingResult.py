#!/usr/bin/env python

######################################################################
#
# Produce a ROOT file with the histograms/counters from tau embedding
# as correctly normalized etc.
#
# The input is a multicrab directory produced with
# * signalAnalysis_cfg.py with "doPat=1 tauEmbeddingInput=1" command line arguments
#
# Author: Matti Kortelainen
#
######################################################################


import os
import sys
import math
import time
import json
import array
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.git as git
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics as systematics


def processDirectory(dset, srcDirName, dstDir, scaleBy):
    # Get directories, recurse to them
    dirs = dset.getDirectoryContent(srcDirName, lambda o: isinstance(o, ROOT.TDirectory))
    dirs = filter(lambda n: n != "configInfo", dirs)

    for d in dirs:
        newDir = dstDir.mkdir(d)
        processDirectory(dset, os.path.join(srcDirName, d), newDir, scaleBy)

    # Then process histograms
    histos = dset.getDirectoryContent(srcDirName, lambda o: isinstance(o, ROOT.TH1))
    dstDir.cd()
    shouldScale = True
    if srcDirName == "counters":
        # Don't touch unweighted counters
        shouldScale = False
    for hname in histos:
        drh = dset.getDatasetRootHisto(os.path.join(srcDirName, hname))
        hnew = drh.getHistogram() # TH1
        hnew.SetName(hname)
        hnew.SetDirectory(dstDir)
        if shouldScale and hname not in "SplittedBinInfo":
            tauEmbedding.scaleTauBRNormalization(hnew)
            if scaleBy is not None:
                hnew.Scale(scaleBy)
        hnew.Write()
#        ROOT.gDirectory.Delete(hname)
        hnew.Delete()

def main(output, dset, dstPostfix="", scaleBy=None):
    start = time.time()

    # Create analysis directory
    tmp = dset
    if not hasattr(tmp, "getSearchMode"):
        tmp = dset.datasets[0]
    analysisDirName = "signalAnalysis"+tmp.getSearchMode()+tmp.getDataEra()+tmp.getOptimizationMode()+tmp.getSystematicVariation()+dstPostfix
    analysisDir = output.mkdir(analysisDirName)

    # Create config info directory
    configInfoDir = analysisDir.mkdir("configInfo")
    configInfoDir.cd()
    nbins = 2
    configInfoHist = ROOT.TH1F("configinfo", "configinfo", nbins, 0, nbins)
    configInfoHist.SetDirectory(configInfoDir)
    configInfoHist.GetXaxis().SetBinLabel(1, "control")
    configInfoHist.SetBinContent(1, 1)
    if dset.isData():
        configInfoHist.GetXaxis().SetBinLabel(2, "luminosity")
        configInfoHist.SetBinContent(2, dset.getLuminosity())
    if dset.isMC():
        configInfoHist.GetXaxis().SetBinLabel(2, "crossSection")
        configInfoHist.SetBinContent(2, dset.getCrossSection())
    configInfoHist.Write()
    configInfoHist.Delete()

    # Process histograms
    processDirectory(dset, "", analysisDir, scaleBy)

    stop = time.time()
    print "Processed in %f.2 s" % (stop-start)

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] multicrab-dir")
    parser.add_option("--analysisName", dest="analysisName", type="string", default=None,
                      help="Specify analysisName explicitly (by default the longest one is selected")
    parser.add_option("--allEras", dest="allEras", action="store_true", default=False,
                      help="Process all data eras (default is to process the longest one)")
    parser.add_option("--list", dest="listAnalyses", action="store_true", default=False,
                      help="List available analysis name information, and quit.")
    parser.add_option("--mc", dest="mcs", action="append", type="string", default=[],
                      help="Process also these MC samples. If any of them is '*', all available MC's are used")
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Expected exactly one multicrab directory, got %d" % len(args))

    createArgs = {"directory": args[0], "includeOnlyTasks": "SingleMu"}
    datasetCreator = dataset.readFromMulticrabCfg(**createArgs)
    datasetCreatorMC = None
    if len(opts.mcs) > 0:
        if "*" in opts.mcs:
            del createArgs["includeOnlyTasks"]
            createArgs["excludeTasks"] = "SingleMu"
        else:
            createArgs["includeOnlyTasks"] = "|".join(opts.mcs)
        datasetCreatorMC = dataset.readFromMulticrabCfg(**createArgs)
    if opts.listAnalyses:
        datasetCreator.printAnalyses()
        sys.exit(0)
    analysisName = opts.analysisName
    if analysisName is None:
        analysisName = ""
        for a in datasetCreator.getAnalyses():
            if len(a) > len(analysisName):
                analysisName = a
        if len(analysisName) == 0:
            raise Exception("Did not find analysis name")

    # Deduce eras
    if datasetCreatorMC is not None:
        eras = datasetCreatorMC.getDataEras()
    else:
        eras = datasetCreator.getDataEras()
        letters = {}
        for e in eras:
            letters[e[-1]] = 1
        keys = letters.keys()
        keys.sort()
        tmp = eras[0]
        for k in keys[1:]:
            tmp += k
            eras.append(tmp)
        if not opts.allEras:
            tmp = eras[0]
            for e in eras[1:]:
                if len(e) > len(tmp):
                    tmp = e
            eras = [tmp]

    # Create pseudo multicrab directory
    taskDir = multicrab.createTaskDir("embedding")

    f = open(os.path.join(taskDir, "codeVersion.txt"), "w")
    f.write(git.getCommitId()+"\n")
    f.close()
    f = open(os.path.join(taskDir, "codeStatus.txt"), "w")
    f.write(git.getStatus()+"\n")
    f.close()
    f = open(os.path.join(taskDir, "codeDiff.txt"), "w")
    f.write(git.getDiff()+"\n")
    f.close()
    # A bit of a kludgy way to indicate for datacard generator that this directory is from embedding (this can be obsolete way)
    f = open(os.path.join(taskDir, "multicrab.cfg"), "w")
    f.write("[Data]\n")
    f.write("dummy = embedded\n\n")
    if datasetCreatorMC is not None:
        for mc in datasetCreatorMC.getDatasetNames():
            f.write("[%s]\n"%mc)
            f.write("dummy = embedded\n\n")
    f.close()
    f = open(os.path.join(taskDir, "inputInfo.txt"), "w")
    f.write("Embedded directory: %s\n" % args[0])

    configInfoAdded = {}

    dcs = [datasetCreator]
    if datasetCreatorMC is not None:
        dcs.append(datasetCreatorMC)

    for dc in dcs:
        for searchMode in dc.getSearchModes():
            for era in eras:
                for optMode in dc.getOptimizationModes():
                    for systVar in [None]+dc.getSystematicVariations():
                        f.write("Analysis %s, searchMode %s, dataEra %s, optimizationMode %s, systematicVariation %s\n" % (analysisName, searchMode, era, optMode, systVar))
                        dsetMgr = dc.createDatasetManager(analysisName=analysisName, searchMode=searchMode,
                                                          dataEra=era, optimizationMode=optMode,
                                                          systematicVariation=systVar,
                                                          enableSystematicVariationForData=True)

                        if len(dsetMgr.getDataDatasets()) > 0:
                            dsetMgr.loadLuminosities()
                            dsetMgr.mergeData()
                        for dset in dsetMgr.getAllDatasets():
                            print "Dataset", dset.getName()
                            resdir = os.path.join(taskDir, dset.getName(), "res")
                            if not os.path.exists(resdir):
                                os.makedirs(resdir)

                            # Open and close result file in order to prevent
                            # per-analysis time blowing up (because of ROOT)
                            if not dset.getName() in configInfoAdded:
                                dv = "pseudo"
                                if dset.isMC():
                                    dv = dset.getDataVersion()
                                resultFile = ROOT.TFile.Open(os.path.join(resdir, "histograms-%s.root"%dset.getName()), "RECREATE")
                                aux.addConfigInfo(resultFile, dset, addLuminosity=False, dataVersion=dv, additionalText={"analysisName": analysisName})
                                configInfoAdded[dset.getName()] = True
                            else:
                                resultFile = ROOT.TFile.Open(os.path.join(resdir, "histograms-%s.root"%dset.getName()), "UPDATE")

                            main(resultFile, dset)
                            if systVar is None and "SystVarGenuineTau" not in dc.getSystematicVariations():
                                unc = systematics.getTauIDUncertainty(isGenuineTau=True)
                                main(resultFile, dset, dstPostfix="SystVarGenuineTauPlus", scaleBy=(1+unc.getUncertaintyUp()))
                                main(resultFile, dset, dstPostfix="SystVarGenuineTauMinus", scaleBy=(1-unc.getUncertaintyDown()))

                            resultFile.Close()
#                        break
#                    break
#                break

    f.close()
    print "Created", taskDir
