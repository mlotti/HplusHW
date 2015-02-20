# Package for making plots of QCD inverted measurement
# Author: Lauri Wendland

import ROOT
import sys,os,shutil
from optparse import OptionParser
from time import sleep
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gStyle.SetPalette(1)
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.systematicsForMetShapeDifference import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles as ShellStyles
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.dataDrivenQCDCount import *
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdInverted.qcdInvertedResult import *


class QCDInvertedPlotBase:
    def __init__(self, opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors):
        self._opts = opts
        self._dsetMgr = dsetMgr
        self._moduleInfoString = moduleInfoString
        self._myDir = myDir
        self._luminosity = luminosity
        self._normFactors = normFactors

    def _drawPlot(self, plot):
        plot.setLuminosity(self._luminosity)
        if "2012" in self._moduleInfoString:
            plot.setEnergy("8")
        else:
            plot.setEnergy("7")
        plot.addStandardTexts()
        plot.draw()
        plot.save()

class QCDInvertedPlot(QCDInvertedPlotBase):
    def __init__(self, opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors):
        QCDInvertedPlotBase.__init__(self, opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors)

    def getIntegratedHistogram(self, histoName, histoSpecs, optionPrintPurityByBins=False):
        myRebinList = None
        if "variableBinSizeLowEdges" in histoSpecs.keys() and len(histoSpecs["variableBinSizeLowEdges"]) > 0:
            myRebinList = histoSpecs["variableBinSizeLowEdges"][:]
        myShape = DataDrivenQCDShape(self._dsetMgr, "Data", "EWK", histoName, self._luminosity, rebinList=myRebinList)
        return myShape.getIntegratedDataDrivenQCDHisto(histoSpecs)

    def getFinalHistogram(self, histoName, histoSpecs, optionPrintPurityByBins=False):
        myRebinList = None
        if "variableBinSizeLowEdges" in histoSpecs.keys() and len(histoSpecs["variableBinSizeLowEdges"]) > 0:
            myRebinList = histoSpecs["variableBinSizeLowEdges"][:]
        myShape = DataDrivenQCDShape(self._dsetMgr, "Data", "EWK", histoName, self._luminosity, rebinList=myRebinList)
        myShapeResult = QCDInvertedShape(myShape, self._moduleInfoString, self._normFactors, optionPrintPurityByBins)
        return myShapeResult.getResultShape()

    def makeFinalPlot(self, histoName, outName, histoSpecs, plotOptions, optionPrintPurityByBins=False):
        # Check if plot exists
        if not self._dsetMgr.getDataset("Data").hasRootHisto(histoName):
            print "Could not find histogram or directory '%s' in the multicrab root files (perhaps you did not run on Informative level), skipping it ..."%histoName
            return
        h = self.getFinalHistogram(histoName, histoSpecs, optionPrintPurityByBins)
        plot = plots.PlotBase([histograms.Histo(h,"shape", drawStyle="E")])
        plot.createFrame("%s/%s_%s"%(self._myDir,outName,self._moduleInfoString), opts=plotOptions)
        plot.frame.GetXaxis().SetTitle(histoSpecs["xtitle"])
        plot.frame.GetYaxis().SetTitle(histoSpecs["ytitle"])
        styles.dataStyle(plot.histoMgr.getHisto("shape"))
        self._drawPlot(plot)

    def makeIntegratedPlot(self, histoName, outName, histoSpecs, plotOptions, optionPrintPurityByBins=False):
        h = self.getIntegratedHistogram(histoName, histoSpecs, optionPrintPurityByBins)
        plot = plots.PlotBase([histograms.Histo(h, "shape", drawStyle="E")])
        plot.createFrame("%s/%s_%s"%(self._myDir,outName,self._moduleInfoString), opts=plotOptions)
        plot.frame.GetXaxis().SetTitle(histoSpecs["xtitle"])
        plot.frame.GetYaxis().SetTitle(histoSpecs["ytitle"])
        styles.dataStyle(plot.histoMgr.getHisto("shape"))
        self._drawPlot(plot)

class QCDInvertedSystematics(QCDInvertedPlotBase):
    def __init__(self, systName, opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors, histoSpecs):
        QCDInvertedPlotBase.__init__(self, opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors)
        # Input quantities
        self._systName = systName
        self._myRebinList = None
        if "variableBinSizeLowEdges" in histoSpecs.keys() and len(histoSpecs["variableBinSizeLowEdges"]) > 0:
            self._myRebinList = histoSpecs["variableBinSizeLowEdges"][:]
        self._hFinalShape = None
        # Output quantities
        self._hSystematicsUp = None
        self._hSystematicsDown = None
        self._myCtrlRegion = None
        self._mySignalRegion = None
        self._mySystObject = None
        self._histoSpecs = histoSpecs

    ## Cache final result to speed up code
    def setFinalShapeHistogram(self, h):
        self._hFinalShape = h

    def getUpHistogram(self):
        if len(self._hSystematicsUp) == 0:
            self.doSystematicsForMetShapeDifference()
        return self._hSystematicsUp

    def getDownHistogram(self):
        if len(self._hSystematicsDown) == 0:
            self.doSystematicsForMetShapeDifference()
        return self._hSystematicsDown

    def _obtainFinalShapeHistogram(self, histoName):
        if histoName == None:
            raise Exception(ShellStyles.ErrorLabel()+"You forgot to give final shape histo name or to cache the final shape histogram!")
        print ShellStyles.WarningLabel()+"Final shape histo was not cached to QCDInvertedSystematics. Obtaining final shape from '%s'."%histoName
        # Obtain final result
        myFinalShape = DataDrivenQCDShape(self._dsetMgr, "Data", "EWK", histoName, self._luminosity, rebinList=self._myRebinList)
        myFinalShapeResult = QCDInvertedShape(myFinalShape, self._moduleInfoString, self._normFactors, optionPrintPurityByBins=False)
        self._hFinalShape = myFinalShapeResult.getResultShape().Clone()

    ## Do systematics coming from met shape difference
    def doSystematicsForMetShapeDifference(self, histoNamePrefix, histoNameSuffix, finalShapeHisto=None):
        # Set here the names of the histograms you want to access
        myCtrlRegionName = "Inverted/%sInvertedTauId%s"%(histoNamePrefix, histoNameSuffix)
        mySignalRegionName = "baseline/%sBaselineTauId%s"%(histoNamePrefix, histoNameSuffix)
        # Check if histograms exist
        if not self._dsetMgr.getDataset("Data").hasRootHisto(finalShapeHisto):
            print "Could not find histogram or directory '%s', skipping ..."%finalShapeHisto
            return
        if not self._dsetMgr.getDataset("Data").hasRootHisto(myCtrlRegionName):
            print "Could not find histogram or directory '%s', skipping ..."%myCtrlRegionName
            return
        if not self._dsetMgr.getDataset("Data").hasRootHisto(mySignalRegionName):
            print "Could not find histogram or directory '%s', skipping ..."%mySignalRegionName
            return
        # Obtain final shape histo, if it is not cached
        if self._hFinalShape == None:
            if finalShapeHisto != None:
                self._obtainFinalShapeHistogram(finalShapeHisto)
        # Obtain QCD shapes
        self._myCtrlRegion = DataDrivenQCDShape(self._dsetMgr, "Data", "EWK", myCtrlRegionName, self._luminosity, rebinList=self._myRebinList)
        self._mySignalRegion = DataDrivenQCDShape(self._dsetMgr, "Data", "EWK", mySignalRegionName, self._luminosity, rebinList=self._myRebinList)
        # Calculate uncertainty
        self._mySystObject = SystematicsForMetShapeDifference(self._mySignalRegion, self._myCtrlRegion, self._hFinalShape, self._moduleInfoString, optionDoBinByBinHistograms=True)
        self._hSystematicsUp = self._mySystObject.getUpHistogram().Clone()
        self._hSystematicsDown = self._mySystObject.getDownHistogram().Clone()
        print "Evaluated MET shape systematics"

    ## Make nice plots
    def doSystematicsPlots(self):
        if self._mySystObject == None:
            return
        # Make sure results have been obtained
        if self._hSystematicsUp == None:
            self.doSystematicsForMetShapeDifference()
        # Create output directory
        if os.path.exists("%s/Systematics_%s"%(self._myDir, self._systName)):
            shutils.rmtree("%s/Systematics_%s"%(self._myDir, self._systName))
        os.mkdir("%s/Systematics_%s"%(self._myDir, self._systName))
        # Make plot for systematics (phase-space bins integrated)
        if self._hFinalShape != None:
            self._hFinalShape.SetLineColor(ROOT.kBlack)
            self._hSystematicsUp.SetLineColor(ROOT.kBlue)
            self._hSystematicsDown.SetLineColor(ROOT.kRed)
            myYmax = 15
            if "2012" in self._moduleInfoString:
                myYmax = 30
            plot = plots.ComparisonManyPlot(histograms.Histo(self._hFinalShape, "Nominal", drawStyle="E"),
                [histograms.Histo(self._hSystematicsUp, "Up", drawStyle="E"), histograms.Histo(self._hSystematicsDown, "Down", drawStyle="E")])
            plot.createFrame("%s/Systematics_%s/QCDInvertedShapeWithMetSyst_final_%s"%(self._myDir, self._systName, self._moduleInfoString), createRatio=True, opts2={"ymin": 0, "ymax": 2}, opts={"addMCUncertainty": True, "ymin": -5, "ymax": myYmax})
            plot.frame.GetXaxis().SetTitle(self._histoSpecs["xtitle"])
            plot.frame.GetYaxis().SetTitle(self._histoSpecs["ytitle"])
            plot.setLegend(histograms.createLegend(0.59, 0.70, 0.87, 0.90))
            plot.legend.SetFillColor(0)
            plot.legend.SetFillStyle(1001)
            styles.mcStyle(plot.histoMgr.getHisto("Up"))
            #plot.histoMgr.getHisto("Up").getRootHisto().SetMarkerSize(0)
            styles.mcStyle2(plot.histoMgr.getHisto("Down"))
            styles.dataStyle(plot.histoMgr.getHisto("Nominal"))
            self._drawPlot(plot)

        # Make plots for systematics (for each phase-space bin separately)
        nSplitBins = self._myCtrlRegion.getNumberOfPhaseSpaceSplitBins()
        myCtrlHistograms = self._mySystObject.getHistogramsForCtrlRegion()
        mySignalHistograms = self._mySystObject.getHistogramsForSignalRegion()
        myMinIndex = 0
        if myCtrlHistograms[0] == None:
            myMinIndex = 1 # Skip empty first bin
        for i in range(myMinIndex, nSplitBins):
            plot = plots.ComparisonPlot(histograms.Histo(mySignalHistograms[i].Clone(), "Signal region", drawStyle="E"),
                                        histograms.Histo(myCtrlHistograms[i].Clone(), "Ctrl. region", drawStyle="E"))
            plot.createFrame("%s/Systematics_%s/QCDInvertedShapeWithMetSyst_%s_%s"%(self._myDir, self._systName, self._myCtrlRegion.getPhaseSpaceBinFileFriendlyTitle(i), self._moduleInfoString), createRatio=True, opts2={"ymin": 0, "ymax": 2}, opts={"addMCUncertainty": True, "ymin": -0.05, "ymax": 0.3})
            plot.frame.GetXaxis().SetTitle(self._histoSpecs["xtitle"])
            plot.frame.GetYaxis().SetTitle("Arb. units. (Normalised to 1)")
            styles.mcStyle(plot.histoMgr.getHisto("Ctrl. region"))
            styles.dataStyle(plot.histoMgr.getHisto("Signal region"))
            plot.setLegend(histograms.createLegend(0.59, 0.77, 0.87, 0.90))
            plot.legend.SetFillColor(0)
            plot.legend.SetFillStyle(1001)
            #plot.histoMgr.getHisto("Up").getRootHisto().SetMarkerSize(0)
            self._drawPlot(plot)
            print "Saved MET shape systematics plot for bin %s"%self._myCtrlRegion.getPhaseSpaceBinFileFriendlyTitle(i)

class QCDInvertedBridgeToDatacard(QCDInvertedPlot):
    def __init__(self, opts, dsetMgr, moduleInfoString, myDir, luminosity, normFactors):
        self._directoryNames = []
        self._histograms = []
        # Obtain directory names and histograms
        self._makeDataDrivenHistogram()

    # Sniff automatically data-driven control plot names and final shape names
    def _makeDataDrivenHistogram(self):
        myObjects = self._dsetMgr.getDataset("Data").getDirectoryContent(".")
        for item in myObjects:
            if "shape" in myObjects:
                append(item)
        self._directoryNames.extend(self._dsetMgr.getDataset("Data").getDirectoryContent("ForDataDrivenCtrlPlots"))
        # Obtain histograms
        for item in self._directoryNames:
            self._histograms.append(self.getFinalHistogram(item, None, optionPrintPurityByBins=False))
        print "Data-driven control plots obtained"

    def _makePseudoMulticrabDirectory(self, rootFile):
        # Make module directory
        mySplit = self._moduleInfoString.split("_")
        myEra = mySplit[0]
        mySearchMode = mySplit[1]
        myVariation = mySplit[2]
        if len(mySplit) > 2:
            raise Exception(ShellStyles.ErrorLabel()+"Assert len(moduleInfoString.split('_') == 3 failed! (mod = %s)"%self._moduleInfoString)
        myModuleDir = "signalAnalysisInvertedTau%s%s%s"%(mySearchMode, myEra, myVariation)
        rootFile.cd("/")
        rootFile.mkdir(myModuleDir)
        rootFile.cd(myModuleDir)
        # Loop over directory names
        for i in range(0, len(self._directoryNames)):
            # Handle final shapes
            if "shape" in self._directoryNames[i]:
                # Write shape histogram
                self._histograms[i].Clone(self._directoryNames[i]).Write()
            else:
                # Create first directory
                mySplit = self._directoryNames[i].split("/")
                mySubDir = mySplit[0]
                myHistoName = mySplit[1]
                if len(mySplit) > 1:
                    raise Exception(ShellStyles.ErrorLabel()+"Assert len(directoryNames.split('/') == 2 failed! (mod = %s)"%self._directoryNames[i])
                rootFile.mkdir(mySubDir)
                rootFile.cd(mySubDir)
                self._histograms[i].Clone(myHistoName).Write()
                rootFile.cd(myModuleDir)
        rootFile.Write()
        print "Written module %s to the pseudo-multicrab output"%self._moduleInfoString

