'''
Description: 
Calculates QCD/FakeB data-driven shapes with the appropriate normalization
Makes also the shape histograms in phase space bins and the final shape

Note:
Systematic uncertainties need to be treated separately (since they should be taken from variation modules)
'''
#================================================================================================
# Imports
#================================================================================================
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.extendedCount as extendedCount
import HiggsAnalysis.NtupleAnalysis.tools.errorPropagation as errorPropagation
import HiggsAnalysis.QCDMeasurement.systematicsForMetShapeDifference as metSyst
import HiggsAnalysis.FakeBMeasurement.dataDrivenQCDCount as dataDrivenQCDCount
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import math
import os
import sys
import copy
import ROOT

#================================================================================================
# Function Definition
#================================================================================================
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1].replace("pyc", "py")
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def IsTH1(h, raiseExcept=False):
    if not isinstance(h, ROOT.TH1):
        msg = "Expected object of type ROOT.TH1, got \"%s\" instead" % (type(h))
        if raiseExcept:
            raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())
        return False
    else:
        return True

def GetDecimalFormat(value):
    if value == 0.0:
        decFormat = "%.0f" % value
    elif abs(value) >= 1.0:
        decFormat = "%.0f" % value
    elif abs(value) >= 0.1:
        decFormat = "%.1f" % value
    elif abs(value) >= 0.01:
        decFormat = "%.2f" % value
    elif abs(value) >= 0.001:
        decFormat = "%.3f" % value
    else:
        decFormat = "%.4f" % value
    return decFormat

def GetTH1BinWidthString(myTH1, iBin):
    IsTH1(myTH1, raiseExcept=True)
     
    width = myTH1.GetBinWidth(iBin)
    return GetDecimalFormat(width)# + str(width)

def GetTH1BinRangeString(myTH1, iBin):
    IsTH1(myTH1, raiseExcept=True)

    lowEdge   = myTH1.GetXaxis().GetBinLowEdge(iBin)
    upEdge    = myTH1.GetXaxis().GetBinUpEdge(iBin)
    rangeStr  = GetDecimalFormat(lowEdge)
    rangeStr += " -> "
    rangeStr += GetDecimalFormat(upEdge)
    return rangeStr

def PrintTH1Info(myTH1):
    '''
    Generic histogram prints detailed tabled
    with the properties of a ROOT.TH1 instance object
    '''
    if not IsTH1(myTH1):
        return

    # Constuct the table
    table   = []
    align  = "{:>5} {:>10} {:^20} {:>15} {:^3} {:<10} {:>15} {:^3} {:<10}"
    header = align.format("Bin", "Bin Width", "Bin Range", "Bin Content", "+/-", "Error", "Cum. Integral", "+/-", "Error")
    hLine  = "="*100

    # Create table
    table.append("{:^100}".format(myTH1.GetName()))    
    table.append(hLine)
    table.append(header)
    table.append(hLine)

    # For-loop: All bins
    h = myTH1
    for j in range(0, myTH1.GetNbinsX()+1):
        binWidth      = GetTH1BinWidthString(myTH1, j)
        #binRange      = "%.1f -> %.1f" % (h.GetXaxis().GetBinLowEdge(j), h.GetXaxis().GetBinUpEdge(j) )
        binRange      = GetTH1BinRangeString(myTH1, j)
        binContent    = "%.2f" % h.GetBinContent(j)
        binError      = "%.2f" % h.GetBinError(j)
        integralError = ROOT.Double(0.0)
        integral      = h.IntegralAndError(0, j, integralError, "")
        table.append(align.format(j, binWidth, binRange, binContent, "+/-", binError,"%.1f" % integral, "+/-", "%.1f" % integralError))
    table.append(hLine)
    table.append("")

    for l in table:
        Print(l, False)
    return
        
#================================================================================================
# Class Definition
#================================================================================================
class QCDInvertedShape:
    '''
    Class for calculating the QCD factorised results

    Shape has to be a dataDrivenQCDCount object
    '''
    def __init__(self, shape, moduleInfoString, normFactors, optionPrintPurityByBins=True, optionDoNQCDByBinHistograms=False, optionUseInclusiveNorm=False, verbose=False):
        self._verbose = verbose
        self._shape   = shape
        self._moduleInfoString  = moduleInfoString
        self._resultCountObject = None # ExtendedCount object which contains the result
        self._resultShape       = None # TH1F which contains the final shape histogram for NQCD
        self._resultShapeEWK    = None # TH1F which contains the final shape histogram for EWK MC
        self._resultShapePurity = None # TH1F which contains the final shape histogram for QCD purity
        self._histogramsList    = []   # List of TH1F histograms
        self._optionUseInclusiveNorm      = optionUseInclusiveNorm        
        self._optionPrintPurityByBins     = optionPrintPurityByBins
        self._optionDoNQCDByBinHistograms = optionDoNQCDByBinHistograms
        self._doCalculate(shape, moduleInfoString, normFactors, optionPrintPurityByBins, optionDoNQCDByBinHistograms)
        return

    def PrintSettings(self, printHistos, verbose):
        '''
        Mostly for debugging purposes
        '''
        info   = []
        align  = "{:<30} {:<70} {:<50}"
        header = align.format("Variable", "Value", "Comment")
        hLine  = "="*150
        info.append("{:^150}".format(self._shape.getHistoName()))
        info.append(hLine)
        info.append(header)
        info.append(hLine)
        info.append(align.format("resultShape"                , self._resultShape.GetName()      , "Name of final shape TH1F for NQCD"))
        info.append(align.format("resultShapeEWK"             , self._resultShapeEWK.GetName()   , "Name of final shape TH1F for EWK MC"))
        info.append(align.format("resultShapePurity"          , self._resultShapePurity.GetName(), "Name of final shape TH1F for QCD purity"))
        info.append(align.format("histogramsList"             , len(self._histogramsList)        , "Length of list of TH1F histograms"))
        info.append(align.format("moduleInfoString"           , self._moduleInfoString           , "Era, Mode, Optimization Mode, and Plot Name"))
        info.append(align.format("verbose"                    , self._verbose                    , "Flag for increased verbosity (Debugging)"))
        info.append(align.format("optionUseInclusiveNorm"     , self._optionUseInclusiveNorm     , "Flag for use of inclusive normalisation"))
        info.append(align.format("optionPrintPurityByBins"    , self._optionPrintPurityByBins    , "Flag for printing QCD purity for given histo (bin-by-bin)"))
        info.append(align.format("optionDoNQCDByBinHistograms", self._optionDoNQCDByBinHistograms, "Flag for doing QCD events bin-by-bin"))
        info.append(hLine)
        info.append("")

        if verbose:
            for i, line in enumerate(info):
                self.Print(line, i==0)

        if printHistos:
            PrintTH1Info(self._resultShape)
            PrintTH1Info(self._resultShapeEWK)
            PrintTH1Info(self._resultShapePurity)
        return

    def Print(self, msg, printHeader=False):
        fName = __file__.split("/")[-1].replace("pyc", "py")
        if printHeader==True:
            print "=== ", fName
            print "\t", msg
        else:
            print "\t", msg
        return

    def Verbose(self, msg, printHeader=True):
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return

    def delete(self):
        self._resultShape.Delete()
        for h in self._histogramsList:
            h.Delete()
        self._histogramsList = None
        return

    def getResultCountObject(self):
        '''
        Returns the ExtendedCountObject with the result
        '''
        return self._resultCountObject

    def getResultShape(self):
        '''
        Returns the final shape histogram
        '''
        return self._resultShape

    def getResultMCEWK(self):
        '''
        Returns the MC EWK contribution to final shape histogram
        '''
        return self._resultShapeEWK

    def getResultPurity(self):
        '''
        Returns the final shape purity histogram
        '''
        return self._resultShapePurity

    def getNQCDHistograms(self):
        '''
        Returns the list of shape histograms (one for each split phase space bin)
        '''
        return self._histogramsList

    def _doCalculate(self, shape, moduleInfoString, normFactors, optionPrintPurityByBins, optionDoNQCDByBinHistograms):
        '''
        Calculates the result
        '''
        self.Verbose("Calculate final shape in signal region (shape * w_QCD) & initialize result containers", True)
        nSplitBins = shape.getNumberOfPhaseSpaceSplitBins()
        self.Verbose("The phase-space of shape %s is split into %i bin(s)" % (shape.getDataDrivenQCDHistoForSplittedBin(0).GetName(), nSplitBins), True)

        self.Verbose("Create Data-Driven Shape", True)
        self._resultShape = aux.Clone(shape.getDataDrivenQCDHistoForSplittedBin(0))
        self._resultShape.Reset()
        self._resultShape.SetTitle("FakeB_Total_%s"%moduleInfoString)
        self._resultShape.SetName("FakeB_Total_%s"%moduleInfoString)

        self.Verbose("Create EWK shape", True)
        self._resultShapeEWK = aux.Clone(shape.getDataDrivenQCDHistoForSplittedBin(0))
        self._resultShapeEWK.Reset()
        self._resultShapeEWK.SetTitle("FakeB_EWK_%s"%moduleInfoString)
        self._resultShapeEWK.SetName("FakeB_EWK_%s"%moduleInfoString)

        self.Verbose("Create Purity shape", True)
        self._resultShapePurity = aux.Clone(shape.getDataDrivenQCDHistoForSplittedBin(0))
        self._resultShapePurity.Reset()
        self._resultShapePurity.SetTitle("FakeB_Purity_%s"%moduleInfoString)
        self._resultShapePurity.SetName("FakeB_Purity_%s"%moduleInfoString)

        self._histogramsList = []
        myUncertaintyLabels  = ["statData", "statEWK"]
        self._resultCountObject = extendedCount.ExtendedCount(0.0, [0.0, 0.0], myUncertaintyLabels)

        if optionDoNQCDByBinHistograms:
            for i in range(0, nSplitBins):
                hBin = aux.Clone(self._resultShape)
                hBin.SetTitle("FakeB_%s_%s"%(shape.getPhaseSpaceBinFileFriendlyTitle(i).replace(" ",""), moduleInfoString))
                hBin.SetName("FakeB_%s_%s"%(shape.getPhaseSpaceBinFileFriendlyTitle(i).replace(" ",""), moduleInfoString))
                self._histogramsList.append(hBin)

        if isinstance(self._resultShape, ROOT.TH2):
            self._doCalculate2D(nSplitBins, shape, normFactors, optionPrintPurityByBins, optionDoNQCDByBinHistograms, myUncertaintyLabels)
            return

        # Intialize counters for purity calculation in final shape binning
        myShapeDataSum       = []
        myShapeDataSumUncert = []
        myShapeEwkSum        = []
        myShapeEwkSumUncert  = []

        # For-loop: All Bins
        for j in range(1,self._resultShape.GetNbinsX()+1):
            myShapeDataSum.append(0.0)
            myShapeDataSumUncert.append(0.0)
            myShapeEwkSum.append(0.0)
            myShapeEwkSumUncert.append(0.0)

        self.Verbose("Calculate results separately for each phase-space bin and then combine", True)
        # For-loop: All measurement bins (e.g. tau pT bins for HToTauNu)
        for i in range(0, nSplitBins):
            # N.B: The \"Inclusive\" value is in the zeroth bin

            self.Verbose("Get data-driven QCD, data, and MC EWK shape histogram for the phase-space bin #%i" % (i), True)
            h     = shape.getDataDrivenQCDHistoForSplittedBin(i)
            hData = shape.getDataHistoForSplittedBin(i)
            hEwk  = shape.getEwkHistoForSplittedBin(i)
            
            self.Verbose("Get normalization factor", True)
            wQCDLabel = shape.getPhaseSpaceBinFileFriendlyTitle(i)
            if self._optionUseInclusiveNorm:
                wQCDLabel = "Inclusive"
            wQCD = 0.0
            
            if not wQCDLabel in normFactors.keys():
                msg = "No normalization factors available for bin '%s' when accessing histogram %s! Ignoring this bin..." % (wQCDLabel,shape.getHistoName())
                self.Print(ShellStyles.WarningLabel() + msg, True)
            else:
                wQCD = normFactors[wQCDLabel]                
            msg = "Weighting bin \"%i\" (label=\"%s\")  with normFactor \"%s\"" % (i, wQCDLabel, wQCD)
            self.Verbose(ShellStyles.NoteLabel() + msg, True)

            # Construct info table (debugging)
            table  = []
            align  = "{:>6} {:^10} {:^15} {:>10} {:>10} {:>10} {:^3} {:^12} {:^3} {:^12}"
            header = align.format("Bin", "Width", "Range", "Content", "NormFactor", "FakeB", "+/-", "Stat. Data", "+/-", "Stat. EWK")
            hLine  = "="*100
            table.append("{:^100}".format(shape.getHistoName()))
            table.append(hLine)
            table.append(header)
            table.append(hLine)

            binSum    = 0.0
            nBins     = h.GetNbinsX()
            binWidth  = hData.GetBinWidth(0)
            xMin      = hData.GetXaxis().GetBinCenter(0)
            xMax      = hData.GetXaxis().GetBinCenter(nBins+1)

            # For-Loop (nested): All bins in the shape histogram 
            for j in range(1, nBins+1):

                # Initialise values
                myResult         = 0.0
                myStatDataUncert = 0.0
                myStatEwkUncert  = 0.0

                # Ignore zero bins
                if abs(h.GetBinContent(j)) > 0.00001:
                    # self.Verbose("Bin %i: Calculating the result" % (j) , j==0)
                    binContent = h.GetBinContent(j)
                    binRange   = "%.1f -> %.1f" % (h.GetXaxis().GetBinLowEdge(j), h.GetXaxis().GetBinUpEdge(j) )
                    binWidth   = GetTH1BinWidthString(h, j)
                    binSum    += binContent
                    myResult   = binContent * wQCD #apply  normalisation factor (transfer from CR to SR))
                    self.Verbose("Bin %i: BinContent = %.3f x %.3f = %.3f" % (j, binContent, wQCD, myResult), False)

                    # self.Verbose("Calculate abs. stat. uncert. for data and for MC EWK (Do not calculate here MC EWK syst.)", True)
                    myStatDataUncert = hData.GetBinError(j) * wQCD
                    myStatEwkUncert  = hEwk.GetBinError(j)  * wQCD
                    table.append(align.format(j, binWidth, binRange, "%0.1f" % binContent, wQCD, "%.1f" % myResult, "+/-", "%.1f" % myStatDataUncert, "+/-", "%.1f" % myStatEwkUncert))

                # Get count object
                myCountObject = extendedCount.ExtendedCount(myResult, [myStatDataUncert, myStatEwkUncert], myUncertaintyLabels)
                self._resultCountObject.add(myCountObject)

                if optionDoNQCDByBinHistograms:
                    self.Verbose("Setting bin content \"%i\"" % (j), True)
                    self._histogramsList[i].SetBinContent(j, myCountObject.value())
                    self._histogramsList[i].SetBinError(j, myCountObject.statUncertainty())

                binContent = self._resultShape.GetBinContent(j) + myCountObject.value()
                binError   = self._resultShape.GetBinError(j) + myCountObject.statUncertainty()**2
                self.Verbose("Setting bin %i to content %0.1f +/- %0.1f" % (j, binContent, binError), j==0)
                self._resultShape.SetBinContent(j, binContent)
                self._resultShape.SetBinError(j, binError) # Sum squared (take sqrt outside loop on final squared sum)
                
                self.Verbose("Sum items for purity calculation", True)
                myShapeDataSum[j-1]       += hData.GetBinContent(j)*wQCD
                myShapeDataSumUncert[j-1] += (hData.GetBinError(j)*wQCD)**2
                myShapeEwkSum[j-1]        += hEwk.GetBinContent(j)*wQCD
                myShapeEwkSumUncert[j-1]  += (hEwk.GetBinError(j)*wQCD)**2

            # Delete the shape histograms
            h.Delete()
            hData.Delete()
            hEwk.Delete()

        # For-loop: All shape bins
        for j in range(1,self._resultShape.GetNbinsX()+1):
            # Take square root of uncertainties
            self._resultShape.SetBinError(j, math.sqrt(self._resultShape.GetBinError(j)))

        # Print detailed results in a formatted table
        qcdResults = self._resultCountObject.getResultAndStatErrorsDict()
        bins       = "%0.f-%.0f" % (1, nBins)
        binRange   = "%.1f -> %.1f" % (xMin, xMax)
        binSum     = "%.1f" % binSum
        nQCD       = "%.1f" % qcdResults["value"]
        dataStat   = "%.1f" % qcdResults["statData"]
        ewkStat    = "%.1f" % qcdResults["statEWK"]
        table.append(align.format(bins, binWidth, binRange, binSum, wQCD, nQCD, "+/-", dataStat, "+/-", ewkStat))
        table.append(hLine)
        # For-loop: All lines in table
        for i, line in enumerate(table):
            if i == len(table)-2:
                self.Verbose(ShellStyles.TestPassedStyle()+line+ShellStyles.NormalStyle(), i==1)
            else:
                self.Verbose(line, i==0)

        if optionPrintPurityByBins:
            self.Verbose("Printing Shape Purity bin-by-bin.", True)
            self.PrintPurityByBins(nBins, shape, myShapeDataSum, myShapeDataSumUncert, myShapeEwkSum, myShapeEwkSumUncert)
        return

    def PrintPurityByBins(self, nBins, shape, shapeDataSum, shapeDataSumUncert, shapeEwkSum, shapeEwkSumUncert):
        # Construct info table (debugging)
        table = []
        align  = "{:>6} {:^20} {:>10} {:^3} {:<10}"
        header = align.format("Bin", "Range", "Purity", "+/-", "Uncertainty")
        hLine  = "="*70
        table.append("{:^70}".format(shape.getHistoName()))
        table.append(hLine)
        table.append(header)
        table.append(hLine)
        
        # For-loop: All shape bins
        for j in range (1, nBins+1):
            
            # Declare variables
            myPurity       = 0.0
            myPurityUncert = 0.0
            ewkSum         = shapeEwkSum[j-1]
            ewkSumUncert   = math.sqrt(shapeEwkSumUncert[j-1])
            dataSum        = shapeDataSum[j-1]
            dataSumUncert  = math.sqrt(shapeDataSumUncert[j-1])

            # Ignore zero bins
            if abs(dataSum) > 0.000001:
                myPurity       = 1.0 - ewkSum / dataSum
                myPurityUncert = errorPropagation.errorPropagationForDivision(ewkSum, ewkSumUncert, dataSum, dataSumUncert)
                
            # Store MC EWK content
            self._resultShapeEWK.SetBinContent(j, ewkSum)
            self._resultShapeEWK.SetBinError(j, ewkSumUncert)

            # Store Purity content
            self._resultShapePurity.SetBinContent(j, myPurity)
            self._resultShapePurity.SetBinError(j, myPurityUncert)
            
            # Bin-range or overflow bin?
            if j < self._resultShape.GetNbinsX():
                binRange = "%.1f -> %.1f" % (self._resultShape.GetXaxis().GetBinLowEdge(j), self._resultShape.GetXaxis().GetBinUpEdge(j) )                
            else:
                binRange = "> %.1f"   % (self._resultShape.GetXaxis().GetBinLowEdge(j) )
            table.append(align.format(j, binRange, "%.3f" % myPurity, "+/-", "%.3f" % myPurityUncert))
        table.append(hLine)

        #FIXME: shape.getDataDrivenQCDHistoForSplittedBin(0).GetBinWidth(1) =  Njets_Data_0dataDriven
        # something is wrong here? is that why the binwidth, binLowEdge, etc.. of purity are all 0?
        # Print purity as function of final shape bins
        for i, line in enumerate(table):
            self.Verbose(line, i==0)
        return
        
    def _doCalculate2D(self, nSplitBins, shape, normFactors, optionPrintPurityByBins, optionDoNQCDByBinHistograms, myUncertaintyLabels):
        '''
        Calculates the result for 2D histograms
        '''
        # Intialize counters for purity calculation in final shape binning
        myShapeDataSum = []
        myShapeDataSumUncert = []
        myShapeEwkSum = []
        myShapeEwkSumUncert = []
        myList = []
        for k in range(1,self._resultShape.GetNbinsY()+1):
            myList.append(0.0)
        for j in range(1,self._resultShape.GetNbinsX()+1):
            myShapeDataSum.append(myList[:])
            myShapeDataSumUncert.append(myList[:])
            myShapeEwkSum.append(myList[:])
            myShapeEwkSumUncert.append(myList[:])
        # Calculate results separately for each phase space bin and then combine
        for i in range(0, nSplitBins):
            # Get data-driven QCD, data, and MC EWK shape histogram for the phase space bin
            h = shape.getDataDrivenQCDHistoForSplittedBin(i)
            hData = shape.getDataHistoForSplittedBin(i)
            hEwk = shape.getEwkHistoForSplittedBin(i)
            # Get normalization factor
            wQCDLabel = shape.getPhaseSpaceBinFileFriendlyTitle(i)
            if self._optionUseInclusiveNorm:
                wQCDLabel = "Inclusive"
            wQCD = 0.0
            if not wQCDLabel in normFactors.keys():
                msg = "No normalization factors available for bin '%s' when accessing histogram %s! Ignoring this bin..." % (wQCDLabel, shape.getHistoName())
                print ShellStyles.WarningLabel() + msg
            else:
                wQCD = normFactors[wQCDLabel]
            # Loop over bins in the shape histogram
            for j in range(1,h.GetNbinsX()+1):
                for k in range(1,h.GetNbinsY()+1):
                    myResult = 0.0
                    myStatDataUncert = 0.0
                    myStatEwkUncert = 0.0
                    if abs(h.GetBinContent(j,k)) > 0.00001: # Ignore zero bins
                        # Calculate result
                        myResult = h.GetBinContent(j,k) * wQCD
                        # Calculate abs. stat. uncert. for data and for MC EWK
                        myStatDataUncert = hData.GetBinError(j,k) * wQCD
                        myStatEwkUncert = hEwk.GetBinError(j,k) * wQCD
                        #errorPropagation.errorPropagationForProduct(hLeg1.GetBinContent(j), hLeg1Data.GetBinError(j), myEffObject.value(), myEffObject.uncertainty("statData"))
                        # Do not calculate here MC EWK syst.
                    myCountObject = extendedCount.ExtendedCount(myResult, [myStatDataUncert, myStatEwkUncert], myUncertaintyLabels)
                    self._resultCountObject.add(myCountObject)
                    if optionDoNQCDByBinHistograms:
                        self._histogramsList[i].SetBinContent(j, k, myCountObject.value())
                        self._histogramsList[i].SetBinError(j, k, myCountObject.statUncertainty())
                    self._resultShape.SetBinContent(j, k, self._resultShape.GetBinContent(j, k) + myCountObject.value())
                    self._resultShape.SetBinError(j, k, self._resultShape.GetBinError(j, k) + myCountObject.statUncertainty()**2) # Sum squared
                    # Sum items for purity calculation
                    myShapeDataSum[j-1][k-1] += hData.GetBinContent(j,k)*wQCD
                    myShapeDataSumUncert[j-1][k-1] += (hData.GetBinError(j,k)*wQCD)**2
                    myShapeEwkSum[j-1][k-1] += hEwk.GetBinContent(j,k)*wQCD
                    myShapeEwkSumUncert[j-1][k-1] += (hEwk.GetBinError(j,k)*wQCD)**2
            h.Delete()
            hData.Delete()
            hEwk.Delete()
        # Take square root of uncertainties
        for j in range(1,self._resultShape.GetNbinsX()+1):
            for k in range(1,self._resultShape.GetNbinsY()+1):
                self._resultShape.SetBinError(j, k, math.sqrt(self._resultShape.GetBinError(j, k)))

        # Print result
        print "NQCD Integral(%s) = %s "%(shape.getHistoName(), self._resultCountObject.getResultStringFull("%.1f"))

        # Print purity as function of final shape bins
        if optionPrintPurityByBins:
            print "Purity of shape %s"%shape.getHistoName()
            print "shapeBin purity purityUncert"
        for j in range (1,self._resultShape.GetNbinsX()+1):
            for k in range(1,self._resultShape.GetNbinsY()+1):
                myPurity = 0.0
                myPurityUncert = 0.0
                if abs(myShapeDataSum[j-1][k-1]) > 0.000001:
                    myPurity = 1.0 - myShapeEwkSum[j-1][k-1] / myShapeDataSum[j-1][k-1]
                    myPurityUncert = errorPropagation.errorPropagationForDivision(myShapeEwkSum[j-1][k-1], math.sqrt(myShapeEwkSumUncert[j-1][k-1]), myShapeDataSum[j-1][k-1], math.sqrt(myShapeDataSumUncert[j-1][k-1]))
                # Store MC EWK content
                self._resultShapeEWK.SetBinContent(j, k, myShapeEwkSum[j-1][k-1])
                self._resultShapeEWK.SetBinError(j, k, math.sqrt(myShapeEwkSumUncert[j-1][k-1]))
                self._resultShapePurity.SetBinContent(j, k, myPurity)
                self._resultShapePurity.SetBinError(j, k, myPurityUncert)
                # Print purity info of final shape
                if optionPrintPurityByBins:
                    myString = ""
                    if j < self._resultShape.GetNbinsX():
                        myString = "%d..%d, "%(self._resultShape.GetXaxis().GetBinLowEdge(j),self._resultShape.GetXaxis().GetBinUpEdge(j))
                    else:
                        myString = ">%d, "%(self._resultShape.GetXaxis().GetBinLowEdge(j))
                    if k < self._resultShape.GetNbinsY():
                        myString = "%d..%d"%(self._resultShape.GetYaxis().GetBinLowEdge(k),self._resultShape.GetYaxis().GetBinUpEdge(k))
                    else:
                        myString = ">%d"%(self._resultShape.GetYaxis().GetBinLowEdge(k))
                    myString += " %.3f %.3f"%(myPurity, myPurityUncert)
                    print myString
        return
    

#================================================================================================
# Function Definition
#================================================================================================
class QCDInvertedResultManager:
    '''
    Manager class for obtaining all the required information to be saved to a pseudo-multicrab
    '''
    def __init__(self, dataPath, ewkPath, dsetMgr, luminosity, moduleInfoString, normFactors,
                 optionCalculateQCDNormalizationSyst=True, normDataSrc=None, normEWKSrc=None,
                 optionUseInclusiveNorm=False, keyList=[], verbose=False):
        self._verbose = verbose
        self._shapePlots = []
        self._shapePlotLabels = []
        self._QCDNormalizationSystPlots = []
        self._QCDNormalizationSystPlotLabels = []
        self._moduleInfoString = moduleInfoString
        self._useInclusiveNorm = optionUseInclusiveNorm
        if len(normFactors.keys()) == 1 and normFactors.keys()[0] == "Inclusive":
            self._useInclusiveNorm = True
        self._histoPathsData= self._GetHistoPaths(dsetMgr, "Data", dataPath, keyList)
        if ewkPath == dataPath:
            self._histoPathsEWK = self._histoPathsData
        else:
            self._histoPathsEWK  = self._GetHistoPaths(dsetMgr, "EWK" , ewkPath , keyList)
        
        # Sanity chech:
        if len(self._histoPathsEWK) != len(self._histoPathsData):
            msg = "List of histograms for EWK does not match in size that of Data"
            raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())

        # For-Loop: All plots to consider
        for i, plotName in enumerate(self._histoPathsData, 1):

            # For testing ..
            #if "Njets" not in plotName:
            #    continue  

            # Inform user of progress
            msg = "{:<9} {:>3} {:<1} {:<3} {:<50}".format("Histogram", "%i" % i, "/", "%s:" % (len(self._histoPathsData)), os.path.join(dataPath, plotName) )
            self.Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), i==1)

            # Ensure that histograms exist && pass other sanity checks
            dataOk = self._sanityChecks(dsetMgr, dataPath, plotName) 
            ewkOk  = self._sanityChecks(dsetMgr, ewkPath , plotName)

            if dataOk*ewkOk == False:
                self.Print(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle(), i==1)
                continue
            
            self.Verbose("Obtaining shape plots (the returned object is not owned)", True)
            myShapeHisto = self._obtainShapeHistograms(i, dataPath, ewkPath, dsetMgr, plotName, luminosity, normFactors)
            
            # Obtain plots for systematics coming from shape difference for control plots # fixme: Systematics
            if optionCalculateQCDNormalizationSyst:
                if isinstance(myShapeHisto, ROOT.TH2):
                    msg = "Skipping met shape uncertainty because histogram has more than 1 dimensions!"
                    self.Print(ShellStyles.WarningLabel() + msg, True)
                else:
                    self._obtainQCDNormalizationSystHistograms(myShapeHisto, dsetMgr, plotName, luminosity, normDataSrc, normEWKSrc)
            
        msg = "Obtaining final shape from data path %s" % (ShellStyles.NoteStyle() + dataPath + ShellStyles.NormalStyle())
        self.Verbose(msg, True)
        return

    def Print(self, msg, printHeader=False):
        fName = __file__.split("/")[-1].replace("pyc", "py")
        if printHeader==True:
            print "=== ", fName
            print "\t", msg
        else:
            print "\t", msg
        return

    def Verbose(self, msg, printHeader=True):
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return

    def _GetHistoPaths(self, dsetMgr, dataset, folderPath, keyList):
        '''
        Determine list of histograms to consider (full paths)
        The keyList contains strings that if ALL 2are contained in 
        a histogram name the histogram will be added to the list of
        objects to be returned.
        '''
        # Get all objects inside the ROOT file under specific directory 
        msg = "Obtaining all ROOT file contents for dataset %s from folder %s" % (dataset, ShellStyles.NoteStyle() + folderPath + ShellStyles.NormalStyle())
        self.Verbose(msg, True)
        allObjects  = dsetMgr.getDataset(dataset).getDirectoryContent(folderPath)
        keepObjects = []
        skipObjects = []

        # Remove anything which does not contain any string from the keyList
        for o in allObjects:
            if all(k in o for k in keyList):
                keepObjects.append(o)
            elif any(k in o for k in keyList):
                pass
            else:
                skipObjects.append(o)

        # Count histograms in lists
        nAll  = len(allObjects)
        nKeep = len(keepObjects)
        nSkip = len(skipObjects)

        if nKeep == 0:
            msg = "Did not find any compatible object under dir %s. Check the \"keyList\" provided" % (folderPath)
            raise Exception(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())

        # Now remove anything which does not contain any string from the keyList
        msg = "Skipping %i histograms for dataset %s. Did not match all keys %s" % (nSkip, dataset, ", ".join(keyList) )
        self.Verbose(ShellStyles.NoteStyle() + msg + ShellStyles.NormalStyle(), True)
        for hName in skipObjects:
            self.Verbose(os.path.join(folderPath, hName), False)

        # Now remove anything which does not contain any string from the keyList
        msg = "Found %i histograms for dataset %s. Matched all keys %s" % (nKeep, dataset, ", ".join(keyList) )
        self.Verbose(ShellStyles.NoteStyle() + msg + ShellStyles.NormalStyle(), True)
        for hName in keepObjects:
            self.Verbose(os.path.join(folderPath, hName), False)
        return keepObjects

    def _sanityChecks(self, dsetMgr, dirName, plotName):
        '''
        Check existence of histograms
        '''
        # Definitions
        myStatus      = True
        myFoundStatus = True
        
        # For-loop: All EWK datasets
        for d in dsetMgr.getDataset("EWK").datasets:
            if not d.hasRootHisto("%s/%s" % (dirName,plotName) ):
                myFoundStatus = False

        # If something is wrong
        if not myFoundStatus:
            myStatus = False
            msg = "Skipping '%s', because it does not exist for all EWK datasets (you probably forgot to set histo level to Vital when producing the multicrab)!" % (plotName)
            self.Print(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), True)
        else:
            (myRootObject, myRootObjectName) = dsetMgr.getDataset("EWK").getFirstRootHisto("%s/%s" % (dirName,plotName) )
            if isinstance(myRootObject, ROOT.TH2): 
                msg ="Skipping '%s', because it is not a TH1 object" % (plotName)
                self.Verbose(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), True)
                myStatus = False
            myRootObject.Delete()
        return myStatus
    
    def PrintShapeInputSummary(self, dataPath, ewkPath, dsetMgr, plotName, luminosity, normFactors):
        # Inform user of input (debugging purposes)
        lines = []
        align = "{:<20} {:<60}"
        hLine = "="*80
        lines.append(hLine)
        lines.append(align.format("Variable", "Value"))
        lines.append(hLine)
        lines.append(align.format("Data Histo", os.path.join(dataPath, plotName) ))
        lines.append(align.format("EWK Histo" , os.path.join(ewkPath , plotName) ))
        lines.append(align.format("Luminosity", luminosity))
        lines.append(align.format("NormFactor", normFactors))
        lines.append(hLine)
        for l in lines:
            self.Print(l, False)
        # dsetMgr.PrintInfo()
        return

    def PrintShapePuritySummary(self, myShape):
        # Inform user of Purity (debugging purposes)
        lines = []
        align = "{:>10} {:>8} {:^3} {:<10} {:^3} {:<15}"
        hLine = "="*55
        lines.append(hLine)
        lines.append(align.format("", "Purity", "+/-", "Uncertainty", "+/-", "Syst. Uncertainty"))
        lines.append(hLine)
        lines.append(align.format("central", "%.2f" % myShape.getIntegratedPurity().value(), "+/-", "%.3f" % myShape.getIntegratedPurity().uncertainty(), "+/-", "%.3f" % myShape.getIntegratedPurity().systUncertainty() ) )
        lines.append(align.format("minimum", "%.2f" % myShape.getMinimumPurity().value()   , "+/-", "%.3f" % myShape.getMinimumPurity().uncertainty()   , "+/-", "%.3f" % myShape.getMinimumPurity().systUncertainty() ) )
        lines.append(hLine)
        for l in lines:
            self.Print(l, False)
        return

    def _obtainShapeHistograms(self, i, dataPath, ewkPath, dsetMgr, plotName, luminosity, normFactors):
        self.Verbose("_obtainShapeHistograms()", True)

        if self._verbose:
            self.PrintShapeInputSummary(dataPath, ewkPath, dsetMgr, plotName, luminosity, normFactors)

        self.Verbose("Obtain the (pre-normFactor) shape %s as \"DataDrivenQCDShape\" type object" % (plotName), True) 
        myShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr, "Data", "EWK", plotName, dataPath, ewkPath, luminosity, self._useInclusiveNorm, self._verbose)
        
        if self._verbose:
            msg = "Printing TH1s (before NormFactors) of \"Data\", \"Data-Driven QCD\", \"EWK\",  and \"Bin-by\Bin Purity\" and \"Integrated Purity\""
            self.Print(msg, True)
            PrintTH1Info(myShape.getIntegratedDataHisto())
            PrintTH1Info(myShape.getIntegratedDataDrivenQCDHisto()) #Data-EWK. NormFactor not applied
            PrintTH1Info(myShape.getIntegratedEwkHisto())
            PrintTH1Info(myShape.getPurityHisto())  # Splitted-bin (disabled for Inclusive mode)
            PrintTH1Info(myShape.getIntegratedPurityForShapeHisto())        
            self.PrintShapePuritySummary(myShape)
        
        self.Verbose("Obtain the (post-normFactor) shape %s as \"QCDInvertedShape\" type object (Takes \"DataDrivenQCDShape\" type object as argument)" % (plotName), True)
        moduleInfo = self._moduleInfoString + "_" + plotName
        myPlot= QCDInvertedShape(myShape, moduleInfo, normFactors, optionUseInclusiveNorm=self._useInclusiveNorm)        
        myPlot.PrintSettings(printHistos=self._verbose, verbose=self._verbose)

        # Define histogram name as will be written in the ROOT file
        self.Verbose("%sDefining the name of histogram objects, as they will appear in the ROOT file%s" % (ShellStyles.WarningStyle(), ShellStyles.NormalStyle()), True)
        hName  = plotName + "%d" %i
        hTitle = plotName.replace("CRSelections", "AllSelections").replace("Baseline_", "").replace("Inverted_", "")#FIXME - alex-iro
        #hTitle = plotName

        # DataDriven
        myShape.delete()
        myPlotHisto = aux.Clone(myPlot.getResultShape(), "ctrlPlotShapeInManager")
        myPlot.delete()
        myPlotHisto.SetName(hName)
        myPlotHisto.SetTitle(hTitle)
        self._shapePlots.append(myPlotHisto)
        self._shapePlotLabels.append(myPlotHisto.GetTitle())# this is the name the object will have in the ROOT file

        # MC EWK
        hName  = plotName + "%d_MCEWK" %i
        myPlotMCEWKHisto = aux.Clone(myPlot.getResultMCEWK(), "ctrlPlotMCEWKInManager")
        myPlotMCEWKHisto.SetName(hName) 
        myPlotMCEWKHisto.SetTitle(hTitle + "_MCEWK")
        self._shapePlots.append(myPlotMCEWKHisto)
        self._shapePlotLabels.append(myPlotMCEWKHisto.GetTitle())# this is the name the object will have in the ROOT file

        # Purity
        hName  = plotName + "%d_Purity" %i
        myPlotPurityHisto = aux.Clone(myPlot.getResultPurity(), "ctrlPlotPurityInManager")
        myPlotPurityHisto.SetName(hName)
        myPlotPurityHisto.SetTitle(hTitle + "_Purity")
        self._shapePlots.append(myPlotPurityHisto)
        self._shapePlotLabels.append(myPlotPurityHisto.GetTitle())# this is the name the object will have in the ROOT file
        return myPlotHisto

    def _obtainQCDNormalizationSystHistograms(self, shapeHisto, dsetMgr, plotName, luminosity, normDataSrc, normEWKSrc):
        msg = "Obtaining region transition systematics"
        self.Print(ShellStyles.HighlightStyle() + msg + ShellStyles.NormalStyle(), True)

        myPlotSignalRegionShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr=dsetMgr,
                                                                        dsetLabelData="Data",
                                                                        dsetLabelEwk="EWK",
                                                                        histoName=plotName,
                                                                        dataPath=normDataSrc+"QCDNormalizationSignal",
                                                                        ewkPath=normEWKSrc+"QCDNormalizationSignal",
                                                                        luminosity=luminosity)

        myPlotControlRegionShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr=dsetMgr,
                                                                         dsetLabelData="Data",
                                                                         dsetLabelEwk="EWK",
                                                                         histoName=plotName,
                                                                         dataPath=normDataSrc+"QCDNormalizationControl",
                                                                         ewkPath=normEWKSrc+"QCDNormalizationControl",
                                                                         luminosity=luminosity)

        myPlotRegionTransitionSyst = metSyst.SystematicsForMetShapeDifference(myPlotSignalRegionShape, 
                                                                              myPlotControlRegionShape, 
                                                                              shapeHisto, 
                                                                              moduleInfoString=self._moduleInfoString,
                                                                              quietMode=True)
        myPlotSignalRegionShape.delete()
        myPlotControlRegionShape.delete()
        # Store up and down variations
        #hUp = aux.Clone(myPlotRegionTransitionSyst.getUpHistogram(), "QCDfactMgrSystQCDSystUp%d"%i)
        #hUp.SetTitle(plotName+"systQCDUp")
        #self._QCDNormalizationSystPlots.append(hUp)
        #self._QCDNormalizationSystPlotLabels.append(hUp.GetTitle())
        #hDown = aux.Clone(myPlotRegionTransitionSyst.getDownHistogram(), "QCDfactMgrSystQCDSystDown%d"%i)
        #hDown.SetTitle(plotName+"systQCDDown")
        #self._QCDNormalizationSystPlots.append(hDown)
        #self._QCDNormalizationSystPlotLabels.append(hDown.GetTitle())
        # Store source histograms
        hNum = aux.Clone(myPlotRegionTransitionSyst.getCombinedSignalRegionHistogram(), "QCDfactMgrSystQCDSystNumerator")
        hNum.SetTitle(plotName+"systQCDNumerator")
        self._QCDNormalizationSystPlots.append(hNum)
        self._QCDNormalizationSystPlotLabels.append(hNum.GetTitle())
        hDenom = aux.Clone(myPlotRegionTransitionSyst.getCombinedCtrlRegionHistogram(), "QCDfactMgrSystQCDSystDenominator")
        hDenom.SetTitle(plotName+"systQCDDenominator")
        self._QCDNormalizationSystPlots.append(hDenom)
        self._QCDNormalizationSystPlotLabels.append(hDenom.GetTitle())
        # Free memory
        myPlotRegionTransitionSyst.delete()

    ## Delete the histograms
    def delete(self):
        def delList(l):
            for h in l:
                if h != None:
                    h.Delete()
            l = None
        delList(self._shapePlots)
        delList(self._QCDNormalizationSystPlots)
        self._shapePlots = None
        self._shapePlotLabels = None
        self._QCDNormalizationSystPlots = None
        self._QCDNormalizationSystPlotLabels = None

    def getShapePlots(self):
        return self._shapePlots
    
    def getShapePlotLabels(self):
        return self._shapePlotLabels
      
    def getQCDNormalizationSystPlots(self):
        return self._QCDNormalizationSystPlots
    
    def getQCDNormalizationSystPlotLabels(self):
        return self._QCDNormalizationSystPlotLabels
