# Description: Calculates the systematics for the MET shape difference for data-driven QCD measurements
#
# Authors: LAW

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from math import sqrt
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.dataDrivenQCDCount import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShapeHistoModifier import *

#from HiggsAnalysis.HeavyChHiggsToTauNu.tools.extendedCount import *

## Calculates the systematics for the MET shape difference for data-driven QCD measurements
class SystematicsForMetShapeDifference:
    ## Constructor
    # signalRegion and ctrlRegion are of type dataDrivenQCDCount, they are the shape histograms at the tested stage
    # finalShape is the final shape histogram (needs to be already properly normalised)
    # histoSpecs is a dictionary (see python/tools/ShapeHistoModifier.py for it's defition)
    # moduleInfoString is a string that is unique to the analysis module
    def __init__(self, signalRegion, ctrlRegion, finalShape, histoSpecs, moduleInfoString):
        self._signalRegionHistograms = []
        self._ctrlRegionHistograms = []
        self._hCombinedSignalRegion = None
        self._hCombinedCtrlRegion = None
        self._systUpHistogram = None
        self._systDownHistogram = None
        # Calculate
        self._calculate(signalRegion, ctrlRegion, finalShape, histoSpecs, moduleInfoString)

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

    def _calculate(self, signalRegion, ctrlRegion, finalShape, histoSpecs, moduleInfoString):
        def normaliseToUnity(h):
            # Normalise area to unity since we only care about the shape
            myIntegral = abs(h.Integral(1, h.GetNbinsX()+2))
            if myIntegral > 0.0:
                h.Scale(1.0 / myIntegral)

        nSplitBins = signalRegion.getNumberOfPhaseSpaceSplitBins()
        myModifier = None
        if histoSpecs == None:
            myModifier = ShapeHistoModifier(histoSpecs,finalShape)
        else:
            myModifier = ShapeHistoModifier(histoSpecs)
        # Initialize histograms
        self._hCombinedSignalRegion = myModifier.createEmptyShapeHistogram("QCDSystSignalRegion_Total_%s"%(moduleInfoString))
        self._hCombinedCtrlRegion = myModifier.createEmptyShapeHistogram("QCDSystCtrlRegion_Total_%s"%(moduleInfoString))
        for i in range(0, nSplitBins):
            self._signalRegionHistograms.append(myModifier.createEmptyShapeHistogram("QCDSystSignalRegion_%s_%s"%(signalRegion.getPhaseSpaceBinFileFriendlyTitle(i), moduleInfoString)))
            self._ctrlRegionHistograms.append(myModifier.createEmptyShapeHistogram("QCDSystCtrlRegion_%s_%s"%(signalRegion.getPhaseSpaceBinFileFriendlyTitle(i), moduleInfoString)))
        self._systUpHistogram = myModifier.createEmptyShapeHistogram("QCDSystUp_%s"%(moduleInfoString))
        self._systDownHistogram = myModifier.createEmptyShapeHistogram("QCDSystDown_%s"%(moduleInfoString))
        # Loop over phase space bins to sum histograms
        for i in range(0, nSplitBins):
            # Get data-driven QCD shapes for MET
            hSignalRegion = signalRegion.getDataDrivenQCDHistoForSplittedBin(i, histoSpecs)
            hCtrlRegion = ctrlRegion.getDataDrivenQCDHistoForSplittedBin(i, histoSpecs)
            # Add to output histograms
            myModifier.addShape(source=hSignalRegion, dest=self._hCombinedSignalRegion)
            myModifier.addShape(source=hCtrlRegion, dest=self._hCombinedCtrlRegion)
            myModifier.addShape(source=hSignalRegion, dest=self._signalRegionHistograms[i])
            myModifier.addShape(source=hCtrlRegion, dest=self._ctrlRegionHistograms[i])
            # Finalize individual histograms (important to do before calculation, because then overflow bin is already merged)
            myModifier.finaliseShape(dest=self._signalRegionHistograms[i])
            myModifier.finaliseShape(dest=self._ctrlRegionHistograms[i])
            normaliseToUnity(self._signalRegionHistograms[i])
            normaliseToUnity(self._ctrlRegionHistograms[i])
            # Loop over histogram bins to calculate uncertainty for each bin
            # For each bin, uncertainty is sqrt(sum_k(sigma_k*N_k)) / sum_k(N_k)
        # Finalize combined histograms
        myModifier.finaliseShape(dest=self._hCombinedSignalRegion)
        myModifier.finaliseShape(dest=self._hCombinedCtrlRegion)
        normaliseToUnity(self._hCombinedSignalRegion)
        normaliseToUnity(self._hCombinedCtrlRegion)
        # Fill up and down variation histogram (bin-by-bin)
        if finalShape == None:
            return
        mySumUp = 0.0
        mySumDown = 0.0
        for i in range(1, self._systUpHistogram.GetNbinsX()+1):
            myRatio = 1.0
            myRatioSigma = 0.0 # Absolute uncertainty
            if abs(self._hCombinedSignalRegion.GetBinContent(i)) > 0.00001 and abs(self._hCombinedCtrlRegion.GetBinContent(i)) > 0.00001:
                # Allow ratio to fluctuate also to negative side (it may happen for small numbers of the final shape)
                myRatio = self._hCombinedSignalRegion.GetBinContent(i) / self._hCombinedCtrlRegion.GetBinContent(i)
                a = (self._hCombinedSignalRegion.GetBinError(i) / self._hCombinedSignalRegion.GetBinContent(i))**2
                b = (self._hCombinedCtrlRegion.GetBinError(i) / self._hCombinedCtrlRegion.GetBinContent(i))**2
                myRatioSigma = sqrt(a**2 + b**2)*abs(myRatio) # abs needed to keep sigma positive
            #print i, (myRatio+myRatioSigma)*finalShape.GetBinContent(i), (myRatio-myRatioSigma)*finalShape.GetBinContent(i), finalShape.GetBinContent(i)
            self._systUpHistogram.SetBinContent(i, (myRatio+myRatioSigma)*finalShape.GetBinContent(i))
            self._systDownHistogram.SetBinContent(i, (myRatio-myRatioSigma)*finalShape.GetBinContent(i))
            # Do not bother to calculate overall uncertainty with the approach above as it will cancel almost completely out!
            # I.e. Take the bin-by-bin uncertainty instead 
            # To get a feeling a conservative (overestimated) total uncertainty is calculated here (uncertainty weighted by Nevents of the final shape)
            mySumUp += (myRatio+myRatioSigma)**2
            mySumDown += (myRatio-myRatioSigma)**2
        mySigmaUp = sqrt(mySumUp) / finalShape.Integral()
        mySigmaDown = sqrt(mySumDown) / finalShape.Integral()
        print "Conservative estimate for syst. uncertainty from met shape difference: up: %.1f %% down: %.1f %%"%(mySigmaUp*100.0,mySigmaDown*100.0)