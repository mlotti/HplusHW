#! /usr/bin/env python

# -----------------------------------------------------------------------------------
# What this script does:
#   Produce tau fake rate curves as function of fake tau pT for selected datasets
# -----------------------------------------------------------------------------------

import sys
import shutil
import ROOT
ROOT.gROOT.SetBatch(True)

import os
from optparse import OptionParser
from math import sqrt

#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.analysisModuleSelector import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset

def createPlot(b, myLuminosity, mydir, name):
    c = ROOT.TCanvas()
    b.Draw("colz")
    myFormats = ["png","C","eps"]
    for f in myFormats:
        c.Print("%s/%s.%s"%(mydir, name, f))

def getAgreementPlot(hData, bkgList, zRange):
    for j in range(1,hData.GetNbinsY()+1):
        for i in range(1,hData.GetNbinsX()+1):
            mySum = 0.0
            for b in bkgList:
                mySum += b.GetBinContent(i,j)
            if mySum > 0.0:
                hData.SetBinContent(i,j,hData.GetBinContent(i,j) / mySum)
            else:
                hData.SetBinContent(i,j,-10.0)
    hData.SetMinimum(1.0-zRange)
    hData.SetMaximum(1.0+zRange)

def main(opts,mySignalDsetMgr,myEmbDsetMgr,myQCDDsetMgr,mySuffix):
    def getHisto(dset, name, lumi):
        d = dset.getDatasetRootHisto(name)
        if d.isMC():
            d.normalizeToLuminosity(lumi)
        return d.getHistogram()
    
    # Make directory for output
    
    if os.path.exists(mySuffix):
        if os.path.exists("%s_old"%mySuffix):
            shutil.rmtree("%s_old"%mySuffix)
        os.rename(mySuffix, "%s_old"%mySuffix)
    os.mkdir(mySuffix)

        # Get luminosity
    myLuminosity = 0.0
    myDataDatasets = mySignalDsetMgr.getDataDatasets()
    for d in myDataDatasets:
        myLuminosity += d.getLuminosity()

    # Merge datasets
    plots.mergeRenameReorderForDataMC(mySignalDsetMgr)
    mergeEWK = True
    myAvailableDatasetNames = ["Data", "TTToHplusBWB_M120"]
    if mergeEWK:
        mySignalDsetMgr.merge("EWK", [
                              "TTJets",
                              "WJets",
                              "DYJetsToLL",
                              "SingleTop", 
                              "Diboson"
                              ])
        myAvailableDatasetNames.extend(["EWK"])
    else:
        myAvailableDatasetNames.extend(["TTJets"])

    prefix = "ForDataDrivenCtrlPlots"
    prefixFakes = "ForDataDrivenCtrlPlotsEWKFakeTaus"

    myPlotNames = ["ImprovedDeltaPhiCuts2DCollinearMinimum",
                   "ImprovedDeltaPhiCuts2DBackToBackMinimum",
                   "ImprovedDeltaPhiCuts2DMinimum"]
    for i in range (1,5):
        myPlotNames.append("ImprovedDeltaPhiCuts2DJet%dCollinear"%i)
        myPlotNames.append("ImprovedDeltaPhiCuts2DJet%dBackToBack"%i)
        myPlotNames.append("ImprovedDeltaPhiCuts2DJet%d"%i)
     
    for item in myPlotNames: 
        print item
        # data
        hData = getHisto(mySignalDsetMgr.getDataset("Data"), "%s/%s"%(prefix,item), myLuminosity)
        # signal
        h120 = getHisto(mySignalDsetMgr.getDataset("TTToHplusBWB_M120"), "%s/%s"%(prefix,item), myLuminosity)
        h160 = getHisto(mySignalDsetMgr.getDataset("TTToHplusBWB_M160"), "%s/%s"%(prefix,item), myLuminosity)
        h300 = getHisto(mySignalDsetMgr.getDataset("HplusTB_M300"), "%s/%s"%(prefix,item), myLuminosity)
        h600 = getHisto(mySignalDsetMgr.getDataset("HplusTB_M600"), "%s/%s"%(prefix,item), myLuminosity)
        # EWK
        hEmb = getHisto(myEmbDsetMgr.getDataset("Data"), "%s/%s"%(prefix,item), myLuminosity)
        # QCD
        hQCD = getHisto(myQCDDsetMgr.getDataset("QCDinvertedmt"), "%s/%s"%(prefix,item), myLuminosity)
        # EWK fakes
        hFakes = getHisto(mySignalDsetMgr.getDataset("EWK"), "%s/%s"%(prefixFakes,item), myLuminosity)
        # MC EWK genuine tau
        hGenuineTau = getHisto(mySignalDsetMgr.getDataset("EWK"), "%s/%s"%(prefix,item), myLuminosity)
        hGenuineTau.Add(hFakes, -1.0)
        # MC EWK
        hMCEWK = getHisto(mySignalDsetMgr.getDataset("EWK"), "%s/%s"%(prefix,item), myLuminosity)
        # Create sum histogram
        myRange = 1.0
        getAgreementPlot(hData, [hEmb,hQCD,hFakes], myRange)
        hDataAgreementEWKMC = getHisto(mySignalDsetMgr.getDataset("Data"), "%s/%s"%(prefix,item), myLuminosity)
        getAgreementPlot(hDataAgreementEWKMC, [hMCEWK,hQCD], myRange)
        # Create plots
        createPlot(hData, myLuminosity, mySuffix, item+"_data_dataDriven")
        createPlot(hDataAgreementEWKMC, myLuminosity, mySuffix, item+"_data_EWKMC")
        if not opts.dataonly:
            createPlot(hEmb, myLuminosity, mySuffix, item+"_emb")
            createPlot(hQCD, myLuminosity, mySuffix, item+"_qcd")
            createPlot(hFakes, myLuminosity, mySuffix, item+"_fakes")
            createPlot(hGenuineTau, myLuminosity, mySuffix, item+"_genuinetau")
            createPlot(h120, myLuminosity, mySuffix, item+"_hp120")
            createPlot(h160, myLuminosity, mySuffix, item+"_hp160")
            createPlot(h300, myLuminosity, mySuffix, item+"_hp300")
            createPlot(h600, myLuminosity, mySuffix, item+"_hp600")

if __name__ == "__main__":
    style = tdrstyle.TDRStyle()
    style.tdrStyle.SetPadRightMargin(0.15)
        
    myModuleSelector = AnalysisModuleSelector() # Object for selecting data eras, search modes, and optimization modes
    parser = OptionParser(usage="Usage: %prog [options]")
    myModuleSelector.addParserOptions(parser)
    parser.add_option("-d", dest="dirs", action="append", help="name of sample directory inside multicrab dir (multiple directories can be specified with multiple -d arguments)")
    parser.add_option("--signaldir", dest="signalDir", action="store", help="signal Multicrab directory")
    parser.add_option("--embdir", dest="embDir", action="store", help="embedding pseudo-Multicrab directory")
    parser.add_option("--qcddir", dest="qcdDir", action="store", help="QCD pseudo-Multicrab directory")
    parser.add_option("--dataonly", dest="dataonly", action="store_true", default=False, help="Do only data agreemement plots")
    (opts, args) = parser.parse_args()

    # Get dataset manager creator and handle different era/searchMode/optimizationMode combinations
    signalDsetCreator = dataset.readFromMulticrabCfg(directory=opts.signalDir)
    embDsetCreator = dataset.readFromMulticrabCfg(directory=opts.embDir)
    qcdDsetCreator = dataset.readFromMulticrabCfg(directory=opts.qcdDir)
    myModuleSelector.setPrimarySource("Signal analysis", signalDsetCreator)
    myModuleSelector.addOtherSource("Embedding", embDsetCreator)
    myModuleSelector.addOtherSource("QCD", qcdDsetCreator)
    myModuleSelector.doSelect(opts)

    # Arguments are ok, proceed to run
    myChosenModuleCount = len(myModuleSelector.getSelectedEras())*len(myModuleSelector.getSelectedSearchModes())*len(myModuleSelector.getSelectedOptimizationModes())
    print "Will run over %d modules (%d eras x %d searchModes x %d optimizationModes)"%(myChosenModuleCount,len(myModuleSelector.getSelectedEras()),len(myModuleSelector.getSelectedSearchModes()),len(myModuleSelector.getSelectedOptimizationModes()))
    myCount = 1
    for era in myModuleSelector.getSelectedEras():
        for searchMode in myModuleSelector.getSelectedSearchModes():
            for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                print "%sProcessing module %d/%d: era=%s searchMode=%s optimizationMode=%s%s"%(HighlightStyle(), myCount, myChosenModuleCount, era, searchMode, optimizationMode, NormalStyle())
                mySuffix = "_%s_%s_%s"%(era,searchMode,optimizationMode)
                # Create dataset managers
                myMgrs = []
                myEmbDsetMgr = embDsetCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
                myMgrs.append(myEmbDsetMgr)
                mySignalDsetMgr = signalDsetCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
                myMgrs.append(mySignalDsetMgr)
                myQCDDsetMgr = qcdDsetCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
                myMgrs.append(myQCDDsetMgr)
                for m in myMgrs:
                    m.updateNAllEventsToPUWeighted()
                    #m.loadLuminosities()
                mySignalDsetMgr.loadLuminosities()
                main(opts,mySignalDsetMgr,myEmbDsetMgr,myQCDDsetMgr,mySuffix)
                myCount += 1
    print "\n%sPlotting done.%s"%(HighlightStyle(),NormalStyle())

