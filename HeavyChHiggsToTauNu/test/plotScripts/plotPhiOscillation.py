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

def myfitfunc(x, par):
    return par[0]*x[0]+par[1]

def myMCfitfuncX(x, par):
    return -0.020039*x[0]+par[0]

def myMCfitfuncY(x, par):
    return -0.119791*x[0]+par[0]

def getHistogram(rootfile,histoname):
    h = rootfile.Get(histoname)
    if h == None:
        raise Exception ("Error: histogram '%s' not found!"%histoname)
    return h;

def produceCurve(h, histoNamePrefix):
    hOut = ROOT.TH1F("hout%s"%histoNamePrefix,"hout%s"%histoNamePrefix,h.GetNbinsX(),h.GetXaxis().GetXmin(),h.GetXaxis().GetXmax())
    htmp = ROOT.TH1F("tmp","tmp",h.GetNbinsY(),h.GetYaxis().GetXmin(),h.GetYaxis().GetXmax())
    for i in range(1,h.GetNbinsX()+1):
        htmp.Clear()
        mySum = 0.0
        myErrorSum = 0.0
        for j in range(0,h.GetNbinsY()+2):
            htmp.SetBinContent(j, h.GetBinContent(i,j))
            htmp.SetBinError(j, h.GetBinError(i,j))
            mySum += h.GetBinContent(i,j)
            myErrorSum += h.GetBinError(i,j)**2
        if myErrorSum > 0:
            if sqrt(myErrorSum) / mySum < 0.15:
                hOut.SetBinContent(i, htmp.GetMean(1))
                hOut.SetBinError(i, htmp.GetMeanError(1))
    return hOut

def producePlotX(myCounter, mydir, h, axisLabel, dsetName, title, maxbins):
    producePlot(myCounter, mydir, h, axisLabel, dsetName, title, maxbins, isX=True, isY=False)

def producePlotY(myCounter, mydir, h, axisLabel, dsetName, title, maxbins):
    producePlot(myCounter, mydir, h, axisLabel, dsetName, title, maxbins, isX=False, isY=True)

def producePlot(myCounter, mydir, h, axisLabel, dsetName, title, maxbins, isX=False, isY=False):
    myRebinFactor = 1

    # Find fit minimum and maximum
    myMin = 9999
    myMax = 0
    for i in range(1,h.GetNbinsX()+1):
        a = h.GetBinContent(i)
        if abs(a) > 0.000001:
            if i < myMin:
                myMin = i-1
            if i > myMax:
                myMax = i
    # Obtain canvas
    c = ROOT.TCanvas()
    # Do fit
    fit = None
    if isX:
        fit = ROOT.TF1("fit",myMCfitfuncX,myMin,myMax,1)
        fit.SetParNames ("Offset")
    if isY:
        fit = ROOT.TF1("fit",myMCfitfuncY,myMin,myMax,1)
        fit.SetParNames ("Offset")
    if fit == None:
        fit = ROOT.TF1("fit",myfitfunc,myMin,myMax,2)
        fit.SetParNames ("Slope","Offset")
    fit.SetLineWidth(2)

    hFrame = ROOT.TH1F("frame","frame",2,0,maxbins)
    hFrame.SetMinimum(-100)
    hFrame.SetMaximum(100)
    hFrame.SetXTitle("N_{vertices}")
    hFrame.SetYTitle(axisLabel)
    #c.SetLogy()
    #hFrame.FindObject("stats").SetLineColor(ROOT.kBlue-6)
                #h1.FindObject("stats").SetTextColor(ROOT.kBlue-6)
                #h1.FindObject("stats").Draw()
    h.SetLineColor(ROOT.kBlack)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetMarkerSize(0.6)
    h.SetMarkerStyle(20)
    h.Rebin(myRebinFactor)
    h.Scale(1.0/float(myRebinFactor))

    #myRebinFactor = 5
    #h2 = h.Clone(h.GetName()+"2")
    #h2.Rebin(myRebinFactor)
    #h2.Scale(1.0/float(myRebinFactor))
    #h2.SetLineColor(ROOT.kBlue-6)
    #h2.SetMarkerColor(ROOT.kBlue-6)
    #fit2 = ROOT.TF1("fit2",myfitfunc,5/myRebinFactor,35/myRebinFactor,2)
    #fit2.SetParNames ("Slope","Offset")
    #fit2.SetLineWidth(2)
    #fit2.SetLineStyle(2)
    #fit2.SetLineColor(ROOT.kBlue-6)

    # Do ugly hack to force creation of fit stats object and make a clone of it (since drawing the frame destroys the stats object)
    # If the fit -command is called after the frame has been drawn, the axis labels on the frame diasppear :)
    h.Fit("fit","","",myMin,myMax)
    ROOT.gPad.Update()
    statsObject = h.FindObject("stats")
    stats = None
    if statsObject != None:
        stats = statsObject.Clone()
    #h2.Fit("fit2")
    #ROOT.gPad.Update()
    #stats2 = h2.FindObject("stats").Clone()
    #stats2.SetTextColor(ROOT.kBlue-6)
    #stats2.SetY1NDC(0.795)
    #stats2.SetY2NDC(0.895)

    hFrame.Draw()
    h.Draw("SAME E")
    #h2.Draw("SAME E")
    if stats != None:
        stats.Draw()
    #stats2.Draw()

    #h.FindObject("stats").Draw()
    chi2 = -1
    if fit.GetNDF() > 0:
        chi2 = fit.GetChisquare()/fit.GetNDF()
    print "Fit for %s: params: chi2/ndf %f slope %f +- %f constant %f +- %f"%(title,chi2,fit.GetParameter(0),fit.GetParError(0),fit.GetParameter(1),fit.GetParError(1))
    # FIXME : add here saving of the parameters into a config file
    # Legend
    leg = ROOT.TLegend(0.2, 0.82, 0.7, 0.88, "", "brNDC")
    leg.SetBorderSize(0)
    leg.SetTextFont(63)
    leg.SetTextSize(18)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.AddEntry(h, dsetName, "lp")
    leg.Draw()

    # Info string
    myInfo = mydir.split("_")
    tex = ROOT.TLatex(0.2,0.87,myInfo[1]) # era
    tex.SetNDC()
    tex.SetTextFont(43)
    tex.SetTextSize(27)
    tex.SetLineWidth(2)
    tex.Draw()

    myFormats = ["png","C","eps"]
    for f in myFormats:
        c.Print("%s/phiOscillation_%s_%02d_%s.%s"%(mydir, dsetName, myCounter, title, f))

def main(opts,signalDsetCreator,era,searchMode,optimizationMode):
    # Make directory for output
    mySuffix = "phiOscillation_%s_%s_%s"%(era,searchMode,optimizationMode)
    if os.path.exists(mySuffix):
        if os.path.exists("%s_old"%mySuffix):
            shutil.rmtree("%s_old"%mySuffix)
        os.rename(mySuffix, "%s_old"%mySuffix)
    os.mkdir(mySuffix)
    # Create dataset manager
    myDsetMgr = signalDsetCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=optimizationMode)
    myDsetMgr.updateNAllEventsToPUWeighted()
    myDsetMgr.loadLuminosities()

    style = tdrstyle.TDRStyle()
    # Get luminosity
    myLuminosity = 0.0
    myDataDatasets = myDsetMgr.getDataDatasets()
    for d in myDataDatasets:
        myLuminosity += d.getLuminosity()

    # Merge datasets
    plots.mergeRenameReorderForDataMC(myDsetMgr)
    mergeEWK = not True
    
    myAvailableDatasetNames = ["Data", "TTToHplusBWB_M120"]
    if mergeEWK:
        myDsetMgr.merge("EWK", [
                      "TTJets",
                      "WJets",
                      "DYJetsToLL",
                      "SingleTop", 
                      "Diboson"
                      ])
        myAvailableDatasetNames.extend(["EWK"])
    else:
        myAvailableDatasetNames.extend(["TTJets", "WJets"])

    # loop over datasets
    myList = []
    if opts.dirs == None:
        myList.extend(myAvailableDatasetNames)
    else:
        if len(opts.dirs) > 0:
            myList.extend(opts.dirs)
        else:
            myList.extend(myAvailableDatasetNames)
    for d in myList:
        print HighlightStyle()+d+NormalStyle()
        doPlots(d, myDsetMgr.getDataset(d), opts, mySuffix, myLuminosity)

def doPlots(dsetName, dset, opts, mySuffix, luminosity):
    maxbins = 60
    myPlotNames = ["METPhiOscillationCorrectionAfterTaus/NverticesVsMET",
                   "METPhiOscillationCorrectionAfterLeptonVeto/NverticesVsMET",
                   "METPhiOscillationCorrectionAfterNjets/NverticesVsMET",
                   "METPhiOscillationCorrectionAfterMETSF/NverticesVsMET",
                   "METPhiOscillationCorrectionAfterCollinearCuts/NverticesVsMET",
                   "METPhiOscillationCorrectionAfterBjets/NverticesVsMET",
                   "METPhiOscillationCorrectionAfterMET/NverticesVsMET",
                   "METPhiOscillationCorrectionAfterBjetsEWKFakeTaus/NverticesVsMET",
                   "METPhiOscillationCorrectionAfterMETEWKFakeTaus/NverticesVsMET",
                   "METPhiOscillationCorrectionAfterAllSelections/NverticesVsMET"]
    myCounter = 0
    for n in myPlotNames:
        myCounter += 1
        hDX = dset.getDatasetRootHisto(n+"X")
        hDY = dset.getDatasetRootHisto(n+"Y")
        if hDX.isMC():
            hDX.normalizeToLuminosity(luminosity)
            hDY.normalizeToLuminosity(luminosity)
        hX = produceCurve(hDX.getHistogram(), n+dsetName+"X")
        hY = produceCurve(hDY.getHistogram(), n+dsetName+"Y")
        # We have the histograms and names, lets make the plot
        myName = n.replace("/","_")
        if hDX.isMC() and False:
            producePlotX(myCounter, mySuffix, hX, "Average MET_{x}, GeV", dsetName, "%s_X"%myName, maxbins)
            producePlotY(myCounter, mySuffix, hY, "Average MET_{y}, GeV", dsetName, "%s_Y"%myName, maxbins)
        else:
            producePlot(myCounter, mySuffix, hX, "Average MET_{x}, GeV", dsetName, "%s_X"%myName, maxbins)
            producePlot(myCounter, mySuffix, hY, "Average MET_{y}, GeV", dsetName, "%s_Y"%myName, maxbins)
        # Plots before and after correction
        hPhiAfter = dset.getDatasetRootHisto(n.replace("NverticesVsMET","METPhiCorrected"))
        hPhiBefore = dset.getDatasetRootHisto(n.replace("NverticesVsMET","METPhiUncorrected"))

if __name__ == "__main__":
    myModuleSelector = AnalysisModuleSelector() # Object for selecting data eras, search modes, and optimization modes
    parser = OptionParser(usage="Usage: %prog [options]")
    myModuleSelector.addParserOptions(parser)
    parser.add_option("-d", dest="dirs", action="append", help="name of sample directory inside multicrab dir (multiple directories can be specified with multiple -d arguments)")
    parser.add_option("--mdir", dest="multicrabDir", action="store", help="Multicrab directory")
    (opts, args) = parser.parse_args()

    # Get dataset manager creator and handle different era/searchMode/optimizationMode combinations
    myPath = "."
    if opts.multicrabDir != None:
        myPath = opts.multicrabDir
    signalDsetCreator = dataset.readFromMulticrabCfg(directory=myPath)
    myModuleSelector.setPrimarySource("Signal analysis", signalDsetCreator)
    myModuleSelector.doSelect(opts)

    # Arguments are ok, proceed to run
    myChosenModuleCount = len(myModuleSelector.getSelectedEras())*len(myModuleSelector.getSelectedSearchModes())*len(myModuleSelector.getSelectedOptimizationModes())
    print "Will run over %d modules (%d eras x %d searchModes x %d optimizationModes)"%(myChosenModuleCount,len(myModuleSelector.getSelectedEras()),len(myModuleSelector.getSelectedSearchModes()),len(myModuleSelector.getSelectedOptimizationModes()))
    myCount = 1
    for era in myModuleSelector.getSelectedEras():
        for searchMode in myModuleSelector.getSelectedSearchModes():
            for optimizationMode in myModuleSelector.getSelectedOptimizationModes():
                print "%sProcessing module %d/%d: era=%s searchMode=%s optimizationMode=%s%s"%(HighlightStyle(), myCount, myChosenModuleCount, era, searchMode, optimizationMode, NormalStyle())
                main(opts,signalDsetCreator,era,searchMode,optimizationMode)
                myCount += 1
    print "\n%sPlotting done.%s"%(HighlightStyle(),NormalStyle())

