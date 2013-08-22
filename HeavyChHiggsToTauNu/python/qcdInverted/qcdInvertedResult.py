# Description: Calculates QCD Inverted shapes with the appropriate normalization
# Makes also the shape histograms in phase space bins and the final shape
# Note: Systematic uncertainties need to be treated separately (since they should be taken from variation modules)
#
# Authors: LAW

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.dataDrivenQCDCount import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.extendedCount import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShapeHistoModifier import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.errorPropagation import *

## Class for calculating the QCD factorised results
# Shape has to be a dataDrivenQCDCount object
class QCDInvertedShape:
    def __init__(self, shape, histoSpecs, moduleInfoString, normFactors, optionPrintPurityByBins=False):
        self._resultCountObject = None # ExtendedCount object which contains the result
        self._resultShape = None # TH1F which contains the final shape histogram
        self._histogramsList = [] # List of TH1F histograms
        self._doCalculate(shape, histoSpecs, moduleInfoString, normFactors, optionPrintPurityByBins)
        #self._doCalculateOldStyle(shape, histoSpecs, moduleInfoString, normFactors, optionPrintPurityByBins)

    ## Returns the ExtendedCountObject with the result
    def getResultCountObject(self):
        return self._resultCountObject

    ## Returns the final shape histogram
    def getResultShape(self):
        return self._resultShape

    ## Returns the list of shape histograms (one for each split phase space bin)
    def getNQCDHistograms(self):
        return self._histogramsList

    ## Calculates the result
    def _doCalculate(self, shape, histoSpecs, moduleInfoString, normFactors, optionPrintPurityByBins):
        # Calculate final shape in signal region (shape * w_QCD)
        nSplitBins = shape.getNumberOfPhaseSpaceSplitBins()
        myModifier = ShapeHistoModifier(histoSpecs)
        # Initialize result containers
        self._resultShape = myModifier.createEmptyShapeHistogram("%s_%s"%(shape.getFileFriendlyHistoName(),moduleInfoString))
        self._histogramsList = []
        myUncertaintyLabels = ["statData", "statEWK"]
        self._resultCountObject = ExtendedCount(0.0, [0.0, 0.0], myUncertaintyLabels)
        for i in range(0, nSplitBins):
            hBin = myModifier.createEmptyShapeHistogram("%s_%s_%s"%(shape.getFileFriendlyHistoName(),moduleInfoString,shape.getPhaseSpaceBinFileFriendlyTitle(i).replace(" ","")))
            self._histogramsList.append(hBin)
        # Intialize counters for purity calculation in final shape binning
        myShapeDataSum = []
        myShapeDataSumUncert = []
        myShapeEwkSum = []
        myShapeEwkSumUncert = []
        for j in range(1,self._resultShape.GetNbinsX()+1):
            myShapeDataSum.append(0.0)
            myShapeDataSumUncert.append(0.0)
            myShapeEwkSum.append(0.0)
            myShapeEwkSumUncert.append(0.0)
        myMinIndex = 0
        if not shape.getPhaseSpaceBinFileFriendlyTitle(0) in normFactors.keys():
            myMinIndex = 1
        # Calculate results separately for each phase space bin and then combine
        for i in range(myMinIndex, nSplitBins):
            # Get data-driven QCD, data, and MC EWK shape histogram for the phase space bin
            h = shape.getDataDrivenQCDHistoForSplittedBin(i, histoSpecs)
            hData = shape.getDataHistoForSplittedBin(i, histoSpecs)
            hEwk = shape.getEwkHistoForSplittedBin(i, histoSpecs)
            # Get normalization factor
            if not shape.getPhaseSpaceBinFileFriendlyTitle(i) in normFactors.keys():
                raise Exception(ErrorLabel()+"No normalization factors available for bin '%s' when accessing histogram %s!"%(shape.getPhaseSpaceBinFileFriendlyTitle(i),shape.getHistoName()))
            wQCD = normFactors[shape.getPhaseSpaceBinFileFriendlyTitle(i)]
            # Loop over bins in the shape histogram
            for j in range(1,h.GetNbinsX()+1):
                myResult = 0.0
                myStatDataUncert = 0.0
                myStatEwkUncert = 0.0
                if abs(h.GetBinContent(j)) > 0.00001: # Ignore zero bins
                    # Calculate result
                    myResult = h.GetBinContent(j) * wQCD
                    # Calculate abs. stat. uncert. for data and for MC EWK
                    myStatDataUncert = hData.GetBinError(j) * wQCD
                    myStatEwkUncert = hEwk.GetBinError(j) * wQCD
                    #errorPropagationForProduct(hLeg1.GetBinContent(j), hLeg1Data.GetBinError(j), myEffObject.value(), myEffObject.uncertainty("statData"))
                    # Do not calculate here MC EWK syst.
                myCountObject = ExtendedCount(myResult, [myStatDataUncert, myStatEwkUncert], myUncertaintyLabels)
                self._resultCountObject.add(myCountObject)
                self._histogramsList[i].SetBinContent(j, myCountObject.value())
                self._histogramsList[i].SetBinError(j, myCountObject.statUncertainty())
                self._resultShape.SetBinContent(j, self._resultShape.GetBinContent(j) + myCountObject.value())
                self._resultShape.SetBinError(j, self._resultShape.GetBinError(j) + myCountObject.statUncertainty()**2) # Sum squared
                # Sum items for purity calculation
                myShapeDataSum[j-1] += hData.GetBinContent(j)*wQCD
                myShapeDataSumUncert[j-1] += (hData.GetBinError(j)*wQCD)**2
                myShapeEwkSum[j-1] += hEwk.GetBinContent(j)*wQCD
                myShapeEwkSumUncert[j-1] += (hEwk.GetBinError(j)*wQCD)**2
        # Take square root of uncertainties
        myModifier.finaliseShape(dest=self._resultShape)
        # Print result
        print "Integral(%s) = %s "%(shape.getHistoName(), self._resultCountObject.getResultStringFull("%.1f"))
        # Print purity as function of final shape bins
        if optionPrintPurityByBins:
            print "Purity of shape %s"%shape.getHistoName()
            print "shapeBin purity purityUncert"
            for j in range (1,h.GetNbinsX()+1):
                myPurity = 0.0
                myPurityUncert = 0.0
                if abs(myShapeDataSum[j-1]) > 0.000001:
                    myPurity = 1.0 - myShapeEwkSum[j-1] / myShapeDataSum[j-1]
                    myPurityUncert = errorPropagationForDivision(myShapeEwkSum[j-1], myShapeEwkSumUncert[j-1], myShapeDataSum[j-1], myShapeDataSumUncert[j-1])
                # Print purity info of final shape
                myString = ""
                if j < h.GetNbinsX():
                    myString = "%d..%d"%(h.GetXaxis().GetBinLowEdge(j),h.GetXaxis().GetBinUpEdge(j))
                else:
                    myString = ">%d"%(h.GetXaxis().GetBinLowEdge(j))
                myString += " %.3f %.3f"%(myPurity, myPurityUncert)
                print myString

    ## Calculates the result
    def _doCalculateOldStyle(self, shape, histoSpecs, moduleInfoString, normFactors, optionPrintPurityByBins):
        # Calculate final shape in signal region (shape * w_QCD)
        nSplitBins = shape.getNumberOfPhaseSpaceSplitBins()
        myModifier = ShapeHistoModifier(histoSpecs)
        # Initialize result containers
        self._resultShape = myModifier.createEmptyShapeHistogram("%s_%s"%(shape.getFileFriendlyHistoName(),moduleInfoString))
        self._histogramsList = []
        myUncertaintyLabels = ["statData", "statEWK"]
        self._resultCountObject = ExtendedCount(0.0, [0.0, 0.0], myUncertaintyLabels)
        for i in range(0, nSplitBins):
            hBin = myModifier.createEmptyShapeHistogram("%s_%s_%s"%(shape.getFileFriendlyHistoName(),moduleInfoString,shape.getPhaseSpaceBinFileFriendlyTitle(i).replace(" ","")))
            self._histogramsList.append(hBin)
        # Intialize counters for purity calculation in final shape binning
        myShapeDataSum = []
        myShapeDataSumUncert = []
        myShapeEwkSum = []
        myShapeEwkSumUncert = []
        for j in range(1,self._resultShape.GetNbinsX()+1):
            myShapeDataSum.append(0.0)
            myShapeDataSumUncert.append(0.0)
            myShapeEwkSum.append(0.0)
            myShapeEwkSumUncert.append(0.0)
        myMinIndex = 0
        if not shape.getPhaseSpaceBinFileFriendlyTitle(0) in normFactors.keys():
            myMinIndex = 1
        # Calculate results separately for each phase space bin and then combine
        for i in range(myMinIndex, nSplitBins):
            # Get data-driven QCD, data, and MC EWK shape histogram for the phase space bin
            h = shape.getDataDrivenQCDHistoForSplittedBin(i, histoSpecs)
            hData = shape.getDataHistoForSplittedBin(i, histoSpecs)
            hEwk = shape.getEwkHistoForSplittedBin(i, histoSpecs)
            # Get normalization factor
            if not shape.getPhaseSpaceBinFileFriendlyTitle(i) in normFactors.keys():
                raise Exception(ErrorLabel()+"No normalization factors available for bin '%s' when accessing histogram %s!"%(shape.getPhaseSpaceBinFileFriendlyTitle(i),shape.getHistoName()))
            wQCD = normFactors[shape.getPhaseSpaceBinFileFriendlyTitle(i)]
            wEWK = normFactors[shape.getPhaseSpaceBinFileFriendlyTitle(i)+"EWK"]
            # Loop over bins in the shape histogram
            for j in range(1,h.GetNbinsX()+1):
                myResult = 0.0
                myStatDataUncert = 0.0
                myStatEwkUncert = 0.0
                if abs(h.GetBinContent(j)) > 0.00001: # Ignore zero bins
                    # Calculate result
                    myResult = hData.GetBinContent(j) * wQCD - hEwk.GetBinContent(j) * wEWK
                    # Calculate abs. stat. uncert. for data and for MC EWK
                    myStatDataUncert = hData.GetBinError(j) * wQCD
                    myStatEwkUncert = hEwk.GetBinError(j) * wEWK
                    #errorPropagationForProduct(hLeg1.GetBinContent(j), hLeg1Data.GetBinError(j), myEffObject.value(), myEffObject.uncertainty("statData"))
                    # Do not calculate here MC EWK syst.
                myCountObject = ExtendedCount(myResult, [myStatDataUncert, myStatEwkUncert], myUncertaintyLabels)
                self._resultCountObject.add(myCountObject)
                self._histogramsList[i].SetBinContent(j, myCountObject.value())
                self._histogramsList[i].SetBinError(j, myCountObject.statUncertainty())
                self._resultShape.SetBinContent(j, self._resultShape.GetBinContent(j) + myCountObject.value())
                self._resultShape.SetBinError(j, self._resultShape.GetBinError(j) + myCountObject.statUncertainty()**2) # Sum squared
                # Sum items for purity calculation
                myShapeDataSum[j-1] += hData.GetBinContent(j)*wQCD
                myShapeDataSumUncert[j-1] += (hData.GetBinError(j)*wQCD)**2
                myShapeEwkSum[j-1] += hEwk.GetBinContent(j)*wEWK
                myShapeEwkSumUncert[j-1] += (hEwk.GetBinError(j)*wEWK)**2
        # Take square root of uncertainties
        myModifier.finaliseShape(dest=self._resultShape)
        # Print result
        print "Integral(%s) = %s "%(shape.getHistoName(), self._resultCountObject.getResultStringFull("%.1f"))
        # Print purity as function of final shape bins
        if optionPrintPurityByBins:
            print "Purity of shape %s"%shape.getHistoName()
            print "shapeBin purity purityUncert"
            for j in range (1,h.GetNbinsX()+1):
                myPurity = 0.0
                myPurityUncert = 0.0
                if abs(myShapeDataSum[j-1]) > 0.000001:
                    myPurity = 1.0 - myShapeEwkSum[j-1] / myShapeDataSum[j-1]
                    myPurityUncert = errorPropagationForDivision(myShapeEwkSum[j-1], myShapeEwkSumUncert[j-1], myShapeDataSum[j-1], myShapeDataSumUncert[j-1])
                # Print purity info of final shape
                myString = ""
                if j < h.GetNbinsX():
                    myString = "%d..%d"%(h.GetXaxis().GetBinLowEdge(j),h.GetXaxis().GetBinUpEdge(j))
                else:
                    myString = ">%d"%(h.GetXaxis().GetBinLowEdge(j))
                myString += " %.3f %.3f"%(myPurity, myPurityUncert)
                print myString
