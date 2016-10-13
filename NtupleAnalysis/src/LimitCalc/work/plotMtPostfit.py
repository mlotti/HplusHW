#!/usr/bin/env python

import os
import sys
from optparse import OptionParser
import getpass
import socket
    
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
    
import ROOT


analysis = "SignalAnalysis"
formats = [".pdf",".png"]

def usage():
    print
    print "### Usage:   ",os.path.basename(sys.argv[0])," <pseudomulticrabdir>"
    print
    sys.exit()

def divideByBinWidth(histolist):
    returnlist = []

    for h in histolist:
        histo = h.getRootHisto().Clone()
        print "Histogram",histo.GetName()
        for ibin in range(1,histo.GetNbinsX()+1):
            print "bin low",histo.GetXaxis().GetBinLowEdge(ibin)
            print "bin width",histo.GetXaxis().GetBinWidth(ibin)
            print "bin value",histo.GetBinContent(ibin)
            newValue = histo.GetBinContent(ibin)/histo.GetXaxis().GetBinWidth(ibin)
            print "bin error",histo.GetBinError(ibin)
            newError = histo.GetBinError(ibin)/histo.GetXaxis().GetBinWidth(ibin)
            print "bin value, new",newValue
            print "bin error, new",newError

            histo.SetBinContent(ibin,newValue)
            histo.SetBinError(ibin,newError)
            h.setRootHisto(histo)
#        sys.exit(0)
        returnlist.append(h)

    return returnlist

def main():

    if len(sys.argv) < 2 and not os.path.isdir(sys.argv[1]):
        usage()

    multicrabdir = sys.argv[1]

    signalAnalysisDir = ""
    QCDAnalysisDir    = os.path.join(multicrabdir,"pseudoMulticrab_QCDMeasurement")

    candDirs = execute("ls %s"%multicrabdir)
    for d in candDirs:
        if "SignalAnalysis_" in d:
            signalAnalysisDir = os.path.join(multicrabdir,d)

    print "Using",signalAnalysisDir
    print "     ",QCDAnalysisDir

    style    = tdrstyle.TDRStyle()
    ROOT.gROOT.SetBatch(True)
    datasets    = dataset.getDatasetsFromMulticrabDirs([signalAnalysisDir], analysisName=analysis)

    datasetsQCD = dataset.getDatasetsFromMulticrabDirs([QCDAnalysisDir], analysisName="signalAnalysis")
    datasets.extend(datasetsQCD)

    plots.mergeRenameReorderForDataMC(datasets)
    luminosity = datasets.getDataset("Data").getLuminosity()

    # Semi-ugly hack for approval homework, remember improve for the next round
    totalErrorFile = ROOT.TFile("outputLight.root")
    #totalErrorFile = ROOT.TFile("outputHeavy.root")
    ## Remove superfluous shape variation uncertainties                                                                  
    totalErrorHistoUp = totalErrorFile.Get("total_background")
    rebin = [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,700,800]
    import array
    #totalErrorHistoUp.Sumw2()
    totalErrorHistoUp = totalErrorHistoUp.Rebin(len(rebin)-1,"foo",array.array("d",rebin))
    totalErrorHistoDown = totalErrorHistoUp.Clone("foo2")
    for i in xrange(1, totalErrorHistoUp.GetNbinsX()+1):
        #print i, totalErrorHistoUp.GetBinContent(i), totalErrorHistoUp.GetBinError(i)
        totalErrorHistoUp.SetBinContent(i, totalErrorHistoUp.GetBinError(i))
        totalErrorHistoDown.SetBinContent(i, -totalErrorHistoDown.GetBinError(i))
        #print i, totalErrorHistoUp.GetBinContent(i), totalErrorHistoDown.GetBinContent(i)
    # semi-ugly hack continues below in QCD

    myStackList = []
    h_data = datasets.getDataset("Data").getDatasetRootHisto("ForDataDrivenCtrlPlots/shapeTransverseMass_POSTFIT").getHistogram()
    myRHWU = dataset.RootHistoWithUncertainties(h_data)
    myRHWU.makeFlowBinsVisible()
    myHisto = histograms.Histo(myRHWU, "Data")
    myHisto.setIsDataMC(isData=True, isMC=False)
    myStackList.insert(0, myHisto)

    h_FakeTau = datasets.getDataset("QCDMeasurementMT").getDatasetRootHisto("ForDataDrivenCtrlPlots/shapeTransverseMass_POSTFIT").getHistogram()
    myRHWU = dataset.RootHistoWithUncertainties(h_FakeTau)
    # semi-ugly hack continues
    htemp=myRHWU.getRootHisto()
    myRHWU.addAbsoluteShapeUncertainty("toterr", totalErrorHistoUp, totalErrorHistoDown)
    #myRHWU.addShapeUncertaintyFromVariation("toterr", totalErrorHistoUp, totalErrorHistoDown)
    # semi-ugly hack ends
    myRHWU.makeFlowBinsVisible()
    myHisto = histograms.Histo(myRHWU, "QCDdata")
    myHisto.setIsDataMC(isData=False, isMC=True)
    myStackList.insert(1, myHisto)

    expectedList = []
    expectedList.append("TT")
    expectedList.append("WJets")
    expectedList.append("SingleTop")
    expectedList.append("DYJetsToLL")
    expectedList.append("Diboson")

    for i in range(0,len(expectedList)):
        drh = datasets.getDataset(expectedList[i]).getDatasetRootHisto("ForDataDrivenCtrlPlots/shapeTransverseMass_POSTFIT")
        h_bgr = drh.getHistogram()
        myRHWU = dataset.RootHistoWithUncertainties(h_bgr)
#        myRHWU.addShapeUncertaintyRelative("syst", th1Plus=self._expectedListSystUp[i], th1Minus=self._expectedListSystDown[i])
        myRHWU.makeFlowBinsVisible()
        myHisto = histograms.Histo(myRHWU, expectedList[i])
        myHisto.setIsDataMC(isData=False, isMC=True)
        myStackList.append(myHisto)

    #myStackList = divideByBinWidth(myStackList)

    # no, ugly hack continues here
    histograms.uncertaintyMode.set(histograms.Uncertainty.SystOnly)
    plots._legendLabels["MCSystError"] = "Bkg. stat.#oplus syst. unc."
    plots._legendLabels["BackgroundSystError"] = "Bkg. stat.#oplus syst. unc."
    # and stops again here
    myStackPlot = plots.DataMCPlot2(myStackList)
    myStackPlot.setLuminosity(luminosity)
    myStackPlot.setDefaultStyles()
    myParams = {}   
    myParams["ylabel"] = "Events / bin"
    myParams["ratioYlabel"] = "Data/Bkg."
    myParams["xlabel"] = "m_{T} (GeV)" 

    myParams["log"] = True
    myParams["ratio"] = True
    myParams["cmsTextPosition"] = "outframe"
    myParams["opts"] = {"ymin": 0.0001, "ymax": 3000.0}
    myParams["opts2"] = {"ymin": 0., "ymax":1.99}
    myParams["moveLegend"] = {"dx": -0.15, "dy": 0., "dh":0.05} # for data-driven
    myParams["ratioMoveLegend"] = {"dx": -0.51, "dy": 0.03}
    myParams["stackMCHistograms"] = True
    myParams["divideByBinWidth"] = True
    myParams["addMCUncertainty"] = True
    myParams["ratioType"] = "errorScale"
    myParams["ratioCreateLegend"] = True
    myParams["ratioMoveLegend"] = dict(dy=-0.45, dh=-0.1, dx=-0.5)
    plots.drawPlot(myStackPlot, "TransVerseMassPOSTFIT", **myParams)



def execute(cmd):
    f = os.popen4(cmd)[1]
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
    f.close()
    return ret

if __name__ == "__main__":
    main()
