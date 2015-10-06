# Description: Calculates the systematics for the MET shape difference for data-driven QCD measurements
#
# Authors: LAW

import NtupleAnalysis.toolsShellStyles as ShellStyles
from math import sqrt
from QCDMeasurement.dataDrivenQCDCount import *
import NtupleAnalysis.toolshistogramsExtras as histogramsExtras
from NtupleAnalysis.toolserrorPropagation import errorPropagationForDivision
import NtupleAnalysis.toolsaux as aux
#from NtupleAnalysis.toolsextendedCount import *
import ROOT

## Calculates the systematics for the MET shape difference for data-driven QCD measurements
class SystematicsForMetShapeDifference:
    ## Constructor
    # signalRegion and ctrlRegion are of type dataDrivenQCDCount, they are the shape histograms at the tested stage
    # finalShape is the final shape histogram (needs to be already properly normalised)
    # moduleInfoString is a string that is unique to the analysis module
    def __init__(self, signalRegion, ctrlRegion, finalShape, moduleInfoString, quietMode=False, optionDoBinByBinHistograms=False):
        self._signalRegionHistograms = []
        self._ctrlRegionHistograms = []
        self._hCombinedSignalRegion = None
        self._hCombinedCtrlRegion = None
        self._systUpHistogram = None
        self._systDownHistogram = None
        # Calculate
        self._calculate(signalRegion, ctrlRegion, finalShape, moduleInfoString, quietMode, optionDoBinByBinHistograms)

    ## Delete the histograms
    def delete(self):
        for h in self._signalRegionHistograms:
            h.Delete()
        for h in self._ctrlRegionHistograms:
            h.Delete()
        self._hCombinedSignalRegion.Delete()
        self._hCombinedCtrlRegion.Delete()
        self._systUpHistogram.Delete()
        self._systDownHistogram.Delete()

    def getHistogramsForSignalRegion(self):
        return self._signalRegionHistograms

    def getHistogramsForCtrlRegion(self):
        return self._ctrlRegionHistograms

    def getCombinedSignalRegionHistogram(self):
        return self._hCombinedSignalRegion

    def getCombinedCtrlRegionHistogram(self):
        return self._hCombinedCtrlRegion

    def getUpHistogram(self):
        return self._systUpHistogram

    def getDownHistogram(self):
        return self._systDownHistogram

    def _calculate(self, signalRegion, ctrlRegion, finalShape, moduleInfoString, quietMode, optionDoBinByBinHistograms):
        def normaliseToUnity(h):
            # Normalise area to unity since we only care about the shape
            myIntegral = abs(h.Integral(1, h.GetNbinsX()+2))
            if myIntegral > 0.0:
                h.Scale(1.0 / myIntegral)

        nSplitBins = signalRegion.getNumberOfPhaseSpaceSplitBins()
        # Initialize histograms
        self._hCombinedSignalRegion = aux.Clone(finalShape)
        self._hCombinedSignalRegion.Reset()
        self._hCombinedSignalRegion.SetTitle("QCDSystSignalRegion_Total_%s"%(moduleInfoString))
        self._hCombinedSignalRegion.SetName("QCDSystSignalRegion_Total_%s"%(moduleInfoString))
        self._hCombinedCtrlRegion = aux.Clone(finalShape)
        self._hCombinedCtrlRegion.Reset()
        self._hCombinedCtrlRegion.SetTitle("QCDSystCtrlRegion_Total_%s"%(moduleInfoString))
        self._hCombinedCtrlRegion.SetName("QCDSystCtrlRegion_Total_%s"%(moduleInfoString))
        if optionDoBinByBinHistograms:
            for i in range(0, nSplitBins):
                h = aux.Clone(self._hCombinedSignalRegion)
                h.SetTitle("QCDSystSignalRegion_%s_%s"%(signalRegion.getPhaseSpaceBinFileFriendlyTitle(i), moduleInfoString))
                h.SetName("QCDSystSignalRegion_%s_%s"%(signalRegion.getPhaseSpaceBinFileFriendlyTitle(i), moduleInfoString))
                self._signalRegionHistograms.append(h)
                h = aux.Clone(self._hCombinedSignalRegion)
                h.SetTitle("QCDSystCtrlRegion_%s_%s"%(signalRegion.getPhaseSpaceBinFileFriendlyTitle(i), moduleInfoString))
                h.SetName("QCDSystCtrlRegion_%s_%s"%(signalRegion.getPhaseSpaceBinFileFriendlyTitle(i), moduleInfoString))
                self._ctrlRegionHistograms.append(h)
        self._systUpHistogram = aux.Clone(self._hCombinedSignalRegion)
        self._systUpHistogram.SetTitle("QCDSystUp_%s"%(moduleInfoString))
        self._systUpHistogram.SetName("QCDSystUp_%s"%(moduleInfoString))
        self._systDownHistogram = aux.Clone(self._hCombinedSignalRegion)
        self._systDownHistogram.SetTitle("QCDSystDown_%s"%(moduleInfoString))
        self._systDownHistogram.SetName("QCDSystDown_%s"%(moduleInfoString))
        # Loop over phase space bins to sum histograms
        for i in range(0, nSplitBins):
            # Get data-driven QCD shapes for MET
            hSignalRegion = signalRegion.getDataDrivenQCDHistoForSplittedBin(i)
            hCtrlRegion = ctrlRegion.getDataDrivenQCDHistoForSplittedBin(i)
            if optionDoBinByBinHistograms:
                # Add to output histograms
                self._signalRegionHistograms[i].Add(hSignalRegion)
                self._ctrlRegionHistograms[i].Add(hCtrlRegion)
                histogramsExtras.makeFlowBinsVisible(self._signalRegionHistograms[i])
                histogramsExtras.makeFlowBinsVisible(self._ctrlRegionHistograms[i])
                normaliseToUnity(self._signalRegionHistograms[i])
                normaliseToUnity(self._ctrlRegionHistograms[i])
            # Add to total histograms
            self._hCombinedSignalRegion.Add(hSignalRegion)
            self._hCombinedCtrlRegion.Add(hCtrlRegion)
        # Finalize combined histograms
        histogramsExtras.makeFlowBinsVisible(self._hCombinedSignalRegion)
        histogramsExtras.makeFlowBinsVisible(self._hCombinedCtrlRegion)
        normaliseToUnity(self._hCombinedSignalRegion)
        normaliseToUnity(self._hCombinedCtrlRegion)
        # Fill up and down variation histogram (bin-by-bin)
        if finalShape == None:
            return
        createSystHistograms(finalShape, self._systUpHistogram, self._systDownHistogram, self._hCombinedSignalRegion, self._hCombinedCtrlRegion, quietMode)

def createSystHistograms(hRate, hSystUp, hSystDown, hNumerator, hDenominator, quietMode=True):
    for i in range(1, hRate.GetNbinsX()+1):
        myRatio = 1.0
        myRatioSigma = 0.2 # Relative uncertainty default value
        if abs(hNumerator.GetBinContent(i)) > 0.00001 and abs(hDenominator.GetBinContent(i)) > 0.00001:
            # Allow ratio to fluctuate also to negative side (it may happen for small numbers of the final shape)
            myRatio = hNumerator.GetBinContent(i) / hDenominator.GetBinContent(i)
            myRatioSigma = errorPropagationForDivision(hNumerator.GetBinContent(i), hNumerator.GetBinError(i), hDenominator.GetBinContent(i), hDenominator.GetBinError(i))
            if myRatioSigma > 1.0:
                myRatioSigma = 1.0
            #if myRatio < 0.0:
            #    myRatioSigma *= -1.0 # this would take a potential cross-over into account, but it is discouraged
            # because merging bins could lead to potential cancellations and underestimation of syst. uncertainty
        #print i, (myRatio+myRatioSigma)*hRate.GetBinContent(i), (myRatio-myRatioSigma)*hRate.GetBinContent(i), hRate.GetBinContent(i)
        hSystUp.SetBinContent(i, (1.0+myRatioSigma)*hRate.GetBinContent(i))
        hSystDown.SetBinContent(i, (1.0-myRatioSigma)*hRate.GetBinContent(i))
    # Calculate total uncertainty
    if not quietMode:
        mySignalIntegral = hNumerator.Integral()
        myCtrlIntegral = hDenominator.Integral()
        mySignalUncert = 0.0
        myCtrlUncert = 0.0
        for i in range(1, hSystUp.GetNbinsX()+1):
            mySignalUncert += hNumerator.GetBinError(i)**2
            myCtrlUncert += hDenominator.GetBinError(i)**2
        myRatio = 1.0
        myRatioSigma = 0.0
        if mySignalIntegral > 0.0 and myCtrlIntegral > 0.0:
            myRatio = mySignalIntegral / myCtrlIntegral
            myRatioSigma = errorPropagationForDivision(mySignalIntegral,sqrt(mySignalUncert),myCtrlIntegral,sqrt(myCtrlUncert))
        mySigmaUp = myRatio + myRatioSigma - 1.0
        mySigmaDown = myRatio - myRatioSigma - 1.0
        print "Estimate for syst. uncertainty of non-isol.->isol. shape difference: up: %.1f %% down: %.1f %%"%(mySigmaUp*100.0,mySigmaDown*100.0)
