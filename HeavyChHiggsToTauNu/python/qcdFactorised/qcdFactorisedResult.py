from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.dataDrivenQCDCount import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.extendedCount import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShapeHistoModifier import *

## Class for calculating the QCD factorised results
class QCDFactorisedResult:
    def __init__(self, basicShape, leg1Shape, leg2Shape, histoSpecs, moduleInfoString):
        self._resultCountObject = None # ExtendedCount object which contains the result
        self._resultShape = None # TH1F which contains the final shape histogram
        self._nQCDHistogramsList = [] # List of TH1F histograms
        self._doCalculate(basicShape, leg1Shape, leg2Shape, histoSpecs, moduleInfoString)

    ## Returns the ExtendedCountObject with the result
    def getResultCountObject(self):
        return self._resultCountObject

    ## Returns the final shape histogram
    def getResultShape(self):
        return self._resultShape

    ## Returns the list of shape histograms (one for each split phase space bin)
    def getNQCDHistograms(self):
        return self._nQCDHistogramsList

    ## Calculates the result
    def _doCalculate(self, basicShape, leg1Shape, leg2Shape, histoSpecs, moduleInfoString):
        # Calculate final shape in signal region (leg1 * leg2 / basic)
        # Note that the calculation of the result is exactly the same for both the ABCD method and the traditional method
        nSplitBins = basicShape.getNumberOfPhaseSpaceSplitBins()
        myModifier = ShapeHistoModifier(histoSpecs)
        # Initialize result containers
        self._resultShape = myModifier.createEmptyShapeHistogram("NQCD_Total_%s"%moduleInfoString)
        self._nQCDHistogramsList = []
        myUncertaintyLabels = ["statData", "statEWK"]
        self._resultCountObject = ExtendedCount(0.0, [0.0, 0.0], myUncertaintyLabels)
        for i in range(0, nSplitBins):
            hBin = myModifier.createEmptyShapeHistogram("NQCD_%s_%s"%(basicShape.getPhaseSpaceBinFileFriendlyTitle(i).replace(" ",""), moduleInfoString))
            self._nQCDHistogramsList.append(hBin)
        # Calculate results separately for each phase space bin and combine
        for i in range(0, nSplitBins):
            # Get data-driven QCD shape histogram for the phase space bin
            hBasic = basicShape.getDataDrivenQCDHistoForSplittedBin(i, histoSpecs)
            hLeg1 = leg1Shape.getDataDrivenQCDHistoForSplittedBin(i, histoSpecs)
            hLeg2 = leg2Shape.getDataDrivenQCDHistoForSplittedBin(i, histoSpecs)
            # Get data shape histograms for the phase space bin
            hBasicData = basicShape.getDataHistoForSplittedBin(i, histoSpecs)
            hLeg1Data = leg1Shape.getDataHistoForSplittedBin(i, histoSpecs)
            hLeg2Data = leg2Shape.getDataHistoForSplittedBin(i, histoSpecs)
            # Get MC EWK shape histograms for the phase space bin
            hBasicEwk = basicShape.getEwkHistoForSplittedBin(i, histoSpecs)
            hLeg1Ewk = leg1Shape.getEwkHistoForSplittedBin(i, histoSpecs)
            hLeg2Ewk = leg2Shape.getEwkHistoForSplittedBin(i, histoSpecs)

            # Loop over bins in the shape histogram
            for j in range(1,hBasic.GetNbinsX()+1):
                myResult = 0.0
                myStatDataUncertSquared = 0.0
                myStatEwkUncertSquared = 0.0
                if abs(hBasic.GetBinContent(j)) > 0.00001: # Ignore zero bins
                    # Calculate result
                    myResult = abs(hLeg1.GetBinContent(j) * hLeg2.GetBinContent(j) / hBasic.GetBinContent(j))
                    # Treat negative numbers
                    if hLeg1.GetBinContent(j) < 0.0 or hLeg2.GetBinContent(j) < 0.0 or hBasic.GetBinContent(j) < 0.0:
                        myResult = -myResult;
                    # Calculate abs. stat. uncert. for data
                    if hBasicData.GetBinContent(j) > 0.0:
                        myStatDataUncertSquared += 1.0 / hBasicData.GetBinContent(j) # Delta N / N = sqrt(N) / N
                    if hLeg1Data.GetBinContent(j) > 0.0:
                        myStatDataUncertSquared += 1.0 / hLeg1Data.GetBinContent(j) # Delta N / N
                    if hLeg2Data.GetBinContent(j) > 0.0:
                        myStatDataUncertSquared += 1.0 / hLeg2Data.GetBinContent(j) # Delta N / N
                    myStatDataUncertSquared *= myResult**2
                    # Calculate abs. stat. uncert. for MC EWK
                    if hBasicEwk.GetBinContent(j) > 0.0:
                        myStatEwkUncertSquared += (hBasicEwk.GetBinError(j) / hBasicEwk.GetBinContent(j))**2 # Delta N / N
                    if hLeg1Ewk.GetBinContent(j) > 0.0:
                        myStatEwkUncertSquared += (hLeg1Ewk.GetBinError(j) / hLeg1Ewk.GetBinContent(j))**2 # Delta N / N
                    if hLeg2Ewk.GetBinContent(j) > 0.0:
                        myStatEwkUncertSquared += (hLeg2Ewk.GetBinError(j) / hLeg2Ewk.GetBinContent(j))**2 # Delta N / N
                    myStatEwkUncertSquared *= myResult**2
                    # Do not calculate here MC EWK syst.
                myCountObject = ExtendedCount(myResult, [sqrt(myStatDataUncertSquared), sqrt(myStatEwkUncertSquared)], myUncertaintyLabels)
                self._resultCountObject.add(myCountObject)
                self._nQCDHistogramsList[i].SetBinContent(j, myCountObject.value())
                self._nQCDHistogramsList[i].SetBinError(j, myCountObject.statUncertainty())
                self._resultShape.SetBinContent(j, self._resultShape.GetBinContent(j) + myCountObject.value())
                self._resultShape.SetBinError(j, self._resultShape.GetBinError(j) + myCountObject.statUncertainty()**2) # Sum squared
        # Take square root of uncertainties
        myModifier.finaliseShape(dest=self._resultShape)
        # Print result
        print "NQCD = %s "%(self._resultCountObject.getResultStringFull("%.1f"))



