## \package ControlPlotMaker
# Classes for making control plots (surprise, surprise ...)

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardColumn import DatacardColumn
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
#from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShapeHistoModifier import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import Count,RootHistoWithUncertainties

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles

from math import pow,sqrt,log10
import os
import sys
import ROOT

##
class ControlPlotMaker:
    ## Constructor
    def __init__(self, opts, config, dirname, luminosity, observation, datasetGroups):
        plots._legendLabels["MCStatError"] = "Bkg. stat."
        plots._legendLabels["MCStatSystError"] = "Bkg. stat.#oplussyst."
        if config.ControlPlots == None:
            return
        myStyle = tdrstyle.TDRStyle()
        myStyle.setOptStat(False)

        self._opts = opts
        self._config = config
        self._dirname = dirname
        self._luminosity = luminosity
        self._observation = observation
        self._datasetGroups = datasetGroups

        #myEvaluator = SignalAreaEvaluator()

        # Make control plots
        print "\n"+HighlightStyle()+"Generating control plots"+NormalStyle()
        # Loop over mass points
        for m in self._config.MassPoints:
            print "... mass = %d GeV"%m
            # Initialize flow plot
            selectionFlow = SelectionFlowPlotMaker(self._config, m)
            myBlindingCount = 0
            for i in range(0,len(self._config.ControlPlots)):
                myCtrlPlot = self._config.ControlPlots[i]
                myMassSuffix = "_M%d"%m
                # Initialize histograms
                hSignal = None
                hQCD = None
                hEmbedded = None
                hEWKfake = None
                hData = None
                # Loop over dataset columns to find histograms
                myStackList = []
                for c in self._datasetGroups:
                    if c.isActiveForMass(m,self._config) and not c.typeIsEmptyColumn():
                        h = c.getControlPlotByIndex(i).Clone()
                        if c.typeIsSignal():
                            # Scale light H+ signal
                            if m < 179:
                                if c.getLabel()[:2] == "HH":
                                    h.Scale(self._config.OptionBr**2)
                                elif c.getLabel()[:2] == "HW":
                                    h.Scale(2.0*self._config.OptionBr*(1.0-self._config.OptionBr))
                            if hSignal == None:
                                hSignal = h.Clone()
                            else:
                                hSignal.Add(h)
                        elif c.typeIsQCD():
                            if hQCD == None:
                                hQCD = h.Clone()
                            else:
                                hQCD.Add(h)
                        elif c.typeIsEWK():
                            if self._config.OptionReplaceEmbeddingByMC:# or False: # FIXME
                                myHisto = histograms.Histo(h,c._datasetMgrColumn)
                                myHisto.setIsDataMC(isData=False, isMC=True)
                                myStackList.append(myHisto)
                            else:
                                if hEmbedded == None:
                                    hEmbedded = h.Clone()
                                else:
                                    hEmbedded.Add(h)
                        elif c.typeIsEWKfake():
                            if hEWKfake == None:
                                hEWKfake = h.Clone()
                            else:
                                hEWKfake.Add(h)
                if hQCD != None:
                    myHisto = histograms.Histo(hQCD,"QCD")
                    myHisto.setIsDataMC(isData=False, isMC=True)
                    myStackList = [myHisto]+myStackList
                if hEmbedded != None:
                    myHisto = histograms.Histo(hEmbedded,"Embedding")
                    myHisto.setIsDataMC(isData=False, isMC=True)
                    myStackList.append(myHisto)
                if hEWKfake != None:
                    myHisto = histograms.Histo(hEWKfake,"EWKfakes")
                    myHisto.setIsDataMC(isData=False, isMC=True)
                    myStackList.append(myHisto)
                hData = observation.getControlPlotByIndex(i).Clone()
                # Apply blinding
                if len(myCtrlPlot.blindedRange) > 0:
                    self._applyBlinding(hData,myCtrlPlot.blindedRange)
                myHisto = histograms.Histo(hData,"Data")
                myHisto.setIsDataMC(isData=True, isMC=False)
                myStackList.insert(0, myHisto)
                # Add signal
                mySignalLabel = "TTToHplus_M%d"%m
                if m > 179:
                    mySignalLabel = "HplusTB_M%d"%m
                myHisto = histograms.Histo(hSignal,mySignalLabel)
                myHisto.setIsDataMC(isData=False, isMC=True)
                myStackList.insert(1, myHisto)
                # Add data to selection flow plot
                if len(myCtrlPlot.blindedRange) > 0:
                    selectionFlow.addColumn(myCtrlPlot.flowPlotCaption,None,myStackList[1:])
                else:
                    selectionFlow.addColumn(myCtrlPlot.flowPlotCaption,hData,myStackList[1:])
                # Make plot
                myStackPlot = plots.DataMCPlot2(myStackList)
                myStackPlot.setLuminosity(self._luminosity)
                myStackPlot.setDefaultStyles()
                myParams = myCtrlPlot.details.copy()
                # Tweak paramaters
                if myParams["unit"] != "":
                    myParams["xlabel"] = "%s, %s"%(myParams["xlabel"],myParams["unit"])
                myMinWidth = 10000.0
                myMaxWidth = 0.0
                for j in range(1,hData.getRootHisto().GetNbinsX()+1):
                    w = hData.getRootHisto().GetBinWidth(j)
                    if w < myMinWidth:
                        myMinWidth = w
                    if w > myMaxWidth:
                        myMaxWidth = w
                myWidthSuffix = "%d-%d"%(myMinWidth,myMaxWidth)
                if abs(myMinWidth-myMaxWidth) < 0.0001:
                    myWidthSuffix = "%d"%(myMinWidth)
                if not (myParams["unit"] == "" and myWidthSuffix == "1"):
                    myParams["ylabel"] = "%s / %s %s"%(myParams["ylabel"],myWidthSuffix,myParams["unit"])
                myParams["ratio"] = True
                myParams["ratioType"] = "errorScale"
                myParams["ratioYlabel"] = "Data/#Sigma Exp."
                myParams["stackMCHistograms"] = True
                myParams["addMCUncertainty"] = True
                myParams["addLuminosityText"] = True
                # Remove non-dientified keywords
                del myParams["unit"]
                # Do plotting
                plots.drawPlot(myStackPlot, "%s/DataDrivenCtrlPlot_M%d_%02d_%s"%(self._dirname,m,i,myCtrlPlot.title), **myParams)

            # Do selection flow plot
            selectionFlow.makePlot(self._dirname,m,len(self._config.ControlPlots),self._luminosity)
        #myEvaluator.save(dirname)
        print "Control plots done"



    def _applyBlinding(self,myObject,blindedRange = []):
        myHisto = myObject.getRootHisto()
        for i in range (1, myHisto.GetNbinsX()+1):
            # Blind if any edge of the current bin is inside the blinded range or if bin spans over the blinded range
            if ((myHisto.GetXaxis().GetBinLowEdge(i) >= blindedRange[0] and myHisto.GetXaxis().GetBinLowEdge(i) <= blindedRange[1]) or
                (myHisto.GetXaxis().GetBinUpEdge(i) >= blindedRange[0] and myHisto.GetXaxis().GetBinUpEdge(i) <= blindedRange[1]) or 
                (myHisto.GetXaxis().GetBinLowEdge(i) <= blindedRange[0] and myHisto.GetXaxis().GetBinUpEdge(i) >= blindedRange[1])):
                myHisto.SetBinContent(i, -1.0)
                myHisto.SetBinError(i, 0.0)

class SignalAreaEvaluator:
    def __init__(self):
        self._output = ""

    def addEntry(self,mass,title,evaluationRange,hSignal,hQCD,hEmbedded,hEWKfake):
        # Obtain event counts
        mySignal = self._evaluate(evaluationRange,hSignal)
        myQCD = self._evaluate(evaluationRange,hQCD)
        myEmbedded = self._evaluate(evaluationRange,hEmbedded)
        myEWKfake = self._evaluate(evaluationRange,hEWKfake)
        # Produce output
        myOutput = "%s, mass=%d, range=%d-%d\n"%(title,mass,evaluationRange[0],evaluationRange[1])
        myOutput += "  signal: %f +- %f\n"%(mySignal.value(),mySignal.uncertainty())
        myOutput += "  QCD: %f +- %f\n"%(myQCD.value(),myQCD.uncertainty())
        myOutput += "  EWKtau: %f +- %f\n"%(myEmbedded.value(),myEmbedded.uncertainty())
        myOutput += "  EWKfake: %f +- %f\n"%(myEWKfake.value(),myEWKfake.uncertainty())
        myExpected = Count(0.0, 0.0)
        myExpected.add(myQCD)
        myExpected.add(myEmbedded)
        myExpected.add(myEWKfake)
        myOutput += "  Total expected: %f +- %f\n"%(myExpected.value(),myExpected.uncertainty())
        mySignal.divide(myExpected)
        myOutput += "  signal/expected: %f +- %f\n"%(mySignal.value(),mySignal.uncertainty())
        myOutput += "\n"
        self._output += myOutput

    def save(self,dirname):
        myFilename = dirname+"/signalAreaEvaluation.txt"
        myFile = open(myFilename, "w")
        myFile.write(self._output)
        myFile.close()
        print HighlightStyle()+"Signal area evaluation written to: "+NormalStyle()+myFilename
        self._output = ""

    def _evaluate(self,evaluationRange,h):
        myResult = 0.0
        myError = 0.0
        for i in range(1,h.GetNbinsX()+1):
            if (h.GetXaxis().GetBinLowEdge(i) >= evaluationRange[0] and
                h.GetXaxis().GetBinUpEdge(i) <= evaluationRange[1]):
                myResult += h.GetBinContent(i)
                myError += pow(h.GetBinError(i),2)
        return Count(myResult,sqrt(myError))

class SelectionFlowPlotMaker:
    def __init__(self, config, mass):
        self._config = config
        self._mass = mass
        # Calculate number of bins
        myBinList = []
        for c in self._config.ControlPlots:
            if c.flowPlotCaption != "" and c.flowPlotCaption != "final":
                myBinList.append(c.flowPlotCaption)
        myBinCount = len(myBinList)
        # Make an empty frame
        myPlotName = "SelectionFlow_%d"%mass
        self._hFrame = ROOT.TH1F(myPlotName,myPlotName,myBinCount,0,myBinCount)
        for i in range(0,myBinCount):
            self._hFrame.GetXaxis().SetBinLabel(i+1, myBinList[i])
        # Make empty histograms for HH, HW, QCD, EWKtau, EWKfake, datacard
        self._expectedList = []
        self._expectedLabelList = []
        self._expectedListSystUp = []
        self._expectedListSystDown = []
        self._data = None
        # Initialise column pointer
        self._myCurrentColumn = 0

    def addColumn(self,label,data,expectedList):
        if label == "":
            return
        # Create histograms if necessary
        if self._data == None:
            self._createHistograms(data,expectedList)
        # Add expected
        for i in range(0,len(expectedList)):
            myRate = expectedList[i].getRootHistoWithUncertainties().getRate()
            self._expectedList[i].SetBinContent(self._myCurrentColumn, myRate)
            self._expectedList[i].SetBinError(self._myCurrentColumn, expectedList[i].getRootHistoWithUncertainties().getRateStatUncertainty())
            uncertUp = 0.0
            uncertDown = 0.0
            if myRate > 0.0:
                (uncertUp,uncertDown) = expectedList[i].getRootHistoWithUncertainties().getRateSystUncertainty()
                self._expectedListSystUp[i].SetBinContent(self._myCurrentColumn, uncertUp/myRate)
                self._expectedListSystDown[i].SetBinContent(self._myCurrentColumn, uncertDown/myRate)
        # Add data
        if data != None:
            self._data.SetBinContent(self._myCurrentColumn, data.getRate())
            self._data.SetBinError(self._myCurrentColumn, data.getRateStatUncertainty())
        else:
            self._data.SetBinContent(self._myCurrentColumn, -1)
        self._myCurrentColumn += 1

    def _createHistograms(self,data,expectedList):
        for e in expectedList:
            self._expectedList.append(self._hFrame.Clone())
            self._expectedListSystUp.append(self._hFrame.Clone())
            self._expectedListSystDown.append(self._hFrame.Clone())
            self._expectedLabelList.append(e.name)
        self._data = self._hFrame.Clone()

    def makePlot(self, dirname, m, index, luminosity):
        myStackList = []
        # expected
        for i in range(0,len(self._expectedList)):
            myRHWU = RootHistoWithUncertainties(self._expectedList[i])
            myRHWU.addShapeUncertaintyRelative("syst", self._expectedListSystUp[i], self._expectedListSystUp[i])
            myHisto = histograms.Histo(myRHWU, self._expectedLabelList[i])
            myHisto.setIsDataMC(isData=False, isMC=True)
            myStackList.append(myHisto)
        # data
        myRHWU = RootHistoWithUncertainties(self._data)
        myHisto = histograms.Histo(myRHWU, "Data")
        myHisto.setIsDataMC(isData=True, isMC=False)
        myStackList.insert(0, myHisto)
        # Make plot
        myStackPlot = plots.DataMCPlot2(myStackList)
        myStackPlot.setLuminosity(luminosity)
        myStackPlot.setDefaultStyles()
        myParams = {}
        myParams["ylabel"] = "Events"
        myParams["log"] = True
        myParams["optsLog"] = {"ymin": 0.5}
        myParams["opts2"] = {"ymin": 0.8, "ymax":1.2}
        myParams["ratio"] = True
        myParams["ratioType"] = "errorScale"
        myParams["ratioYlabel"] = "Data/#Sigma Exp."
        myParams["stackMCHistograms"] = True
        myParams["addMCUncertainty"] = True
        myParams["addLuminosityText"] = True
        plots.drawPlot(myStackPlot, "%s/DataDrivenCtrlPlot_M%d_%02d_SelectionFlow"%(dirname,m,index), **myParams)

