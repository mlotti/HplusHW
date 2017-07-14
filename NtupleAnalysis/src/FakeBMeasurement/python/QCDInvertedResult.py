'''
Description: 
Calculates QCD Inverted shapes with the appropriate normalization
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
import ROOT


#================================================================================================
# Function Definition
#================================================================================================
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return


def Verbose(msg, printHeader=True, verbose=False):
    if not verbose:
        return
    Print(msg, printHeader)
    return

#================================================================================================
# Class Definition
#================================================================================================
class QCDInvertedShape:
    '''
    Class for calculating the QCD factorised results
    Shape has to be a dataDrivenQCDCount object
    '''
    def __init__(self, shape, moduleInfoString, normFactors, optionPrintPurityByBins=True, optionDoNQCDByBinHistograms=False, optionUseInclusiveNorm=False, verbose=False): #alex
        self._resultCountObject = None # ExtendedCount object which contains the result
        self._resultShape       = None # TH1F which contains the final shape histogram for NQCD
        self._resultShapeEWK    = None # TH1F which contains the final shape histogram for EWK MC
        self._resultShapePurity = None # TH1F which contains the final shape histogram for QCD purity
        self._histogramsList    = [] # List of TH1F histograms
        self._optionUseInclusiveNorm = optionUseInclusiveNorm        
        self._doCalculate(shape, moduleInfoString, normFactors, optionPrintPurityByBins, optionDoNQCDByBinHistograms)
        self._verbose = verbose
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
        # Calculate final shape in signal region (shape * w_QCD)
        nSplitBins = shape.getNumberOfPhaseSpaceSplitBins()

        # Initialize result containers
        self._resultShape = aux.Clone(shape.getDataDrivenQCDHistoForSplittedBin(0))
        self._resultShape.Reset()
        self._resultShape.SetTitle("NQCDFinal_Total_%s"%moduleInfoString)
        self._resultShape.SetName("NQCDFinal_Total_%s"%moduleInfoString)

        # EWK
        self._resultShapeEWK = aux.Clone(shape.getDataDrivenQCDHistoForSplittedBin(0))
        self._resultShapeEWK.Reset()
        self._resultShapeEWK.SetTitle("NQCDFinal_EWK_%s"%moduleInfoString)
        self._resultShapeEWK.SetName("NQCDFinal_EWK_%s"%moduleInfoString)

        # Purity
        self._resultShapePurity = aux.Clone(shape.getDataDrivenQCDHistoForSplittedBin(0))
        self._resultShapePurity.Reset()
        self._resultShapePurity.SetTitle("NQCDFinal_Purity_%s"%moduleInfoString)
        self._resultShapePurity.SetName("NQCDFinal_Purity_%s"%moduleInfoString)

        self._histogramsList = []
        myUncertaintyLabels  = ["statData", "statEWK"]
        self._resultCountObject = extendedCount.ExtendedCount(0.0, [0.0, 0.0], myUncertaintyLabels)

        if optionDoNQCDByBinHistograms:
            for i in range(0, nSplitBins):
                hBin = aux.Clone(self._resultShape)
                hBin.SetTitle("NQCDFinal_%s_%s"%(shape.getPhaseSpaceBinFileFriendlyTitle(i).replace(" ",""), moduleInfoString))
                hBin.SetName("NQCDFinal_%s_%s"%(shape.getPhaseSpaceBinFileFriendlyTitle(i).replace(" ",""), moduleInfoString))
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

        Print("Calculate results separately for each phase-space bin and then combine", True)
        # For-loop: All bins 
        for i in range(0, nSplitBins):

            Verbose("Get data-driven QCD, data, and MC EWK shape histogram for the phase-space bin", True)
            h     = shape.getDataDrivenQCDHistoForSplittedBin(i)
            hData = shape.getDataHistoForSplittedBin(i)
            hEwk  = shape.getEwkHistoForSplittedBin(i)
            
            Verbose("Get normalization factor", True)
            wQCDLabel = shape.getPhaseSpaceBinFileFriendlyTitle(i)
            if self._optionUseInclusiveNorm:
                wQCDLabel = "Inclusive"
            wQCD = 0.0
            
            if not wQCDLabel in normFactors.keys():
                msg = "No normalization factors available for bin '%s' when accessing histogram %s! Ignoring this bin..." % (wQCDLabel,shape.getHistoName())
                Print(ShellStyles.WarningLabel() + msg, True)
            else:
                wQCD = normFactors[wQCDLabel]
            Verbose("The QCD weight is wQCD = %s (label=%s)" % (wQCD, wQCDLabel), True)

            # Construct info table (debugging)
            table  = []
            align  = "{:>10} {:>15} {:>15} {:>15} {:^3} {:>10} {:^3} {:>10}"
            header = align.format("Shape Bin", "Bin Content", "NormFactor", "QCD", "+/-", "Data Stat.", "+/-", "EWK Stat.")
            hLine  = "="*100
            table.append("{:^100}".format(shape.getHistoName()))
            table.append(hLine)
            table.append(header)
            table.append(hLine)
            
            # For-Loop: All bins in the shape histogram
            binSum = 0.0
            nBins  = h.GetNbinsX()
            for j in range(1, nBins+1):

                # Initialise values
                myResult         = 0.0
                myStatDataUncert = 0.0
                myStatEwkUncert  = 0.0

                # Ignore zero bins
                if abs(h.GetBinContent(j)) > 0.00001:
                    Verbose("Calculating the result")
                    binContent = h.GetBinContent(j)
                    binSum    += binContent
                    myResult   = binContent * wQCD

                    Verbose("Calculate abs. stat. uncert. for data and for MC EWK (Do not calculate here MC EWK syst.)", True)
                    myStatDataUncert = hData.GetBinError(j) * wQCD
                    myStatEwkUncert  = hEwk.GetBinError(j)  * wQCD
                    table.append(align.format(j, "%0.1f" % binContent, wQCD, "%.1f" % myResult, "+/-", "%.1f" % myStatDataUncert, "+/-", "%.1f" % myStatEwkUncert))

                # Get count object
                myCountObject = extendedCount.ExtendedCount(myResult, [myStatDataUncert, myStatEwkUncert], myUncertaintyLabels)
                self._resultCountObject.add(myCountObject)

                if optionDoNQCDByBinHistograms:
                    self._histogramsList[i].SetBinContent(j, myCountObject.value())
                    self._histogramsList[i].SetBinError(j, myCountObject.statUncertainty())

                self._resultShape.SetBinContent(j, self._resultShape.GetBinContent(j) + myCountObject.value())
                self._resultShape.SetBinError(j, self._resultShape.GetBinError(j) + myCountObject.statUncertainty()**2) # Sum squared

                Verbose("Sum items for purity calculation", True)
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
        if 0:
            print "NQCD Integral(%s) = %s "% ( shape.getHistoName(), self._resultCountObject.getResultStringFull("%.1f"))
        qcdResults = self._resultCountObject.getResultAndStatErrorsDict()
        table.append(align.format("%s-%.0f" % (1, nBins), "%.1f" % binSum, wQCD, "%.1f" % qcdResults["value"], "+/-", "%.1f" % qcdResults["statData"], "+/-", "%.1f" % qcdResults["statEWK"]))
        table.append(hLine)
        for i, line in enumerate(table):
            Verbose(line, i==0)

        if optionPrintPurityByBins:
            Verbose("Printing Shape Purity bin-by-bin.", True)
            self.PrintPurityByBins(nBins, shape, myShapeDataSum, myShapeDataSumUncert, myShapeEwkSum, myShapeEwkSumUncert)
        return

    def PrintPurityByBins(self, nBins, shape, shapeDataSum, shapeDataSumUncert, shapeEwkSum, shapeEwkSumUncert):

        # Construct info table (debugging)
        table = []
        align  = "{:>8} {:>12} {:>10} {:^3} {:<10}"
        header = align.format("Shape Bin", "Range", "Purity", "+/-", "Uncertainty")
        hLine  = "="*50
        table.append("{:^50}".format(shape.getHistoName()))
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
            self._resultShapePurity.SetBinContent(j, myPurity)
            self._resultShapePurity.SetBinError(j, myPurityUncert)            
        
            # Bin-range or overflow bin?
            if j < self._resultShape.GetNbinsX():
                bin = "%.1f - %.1f" % (self._resultShape.GetXaxis().GetBinLowEdge(j), self._resultShape.GetXaxis().GetBinUpEdge(j) )
            else:
                bin = "> %.1f"   % (self._resultShape.GetXaxis().GetBinLowEdge(j) )
            table.append(align.format(j, bin, "%.3f" % myPurity, "+/-", "%.3f" % myPurityUncert))
        table.append(hLine)

        #FIXME: shape.getDataDrivenQCDHistoForSplittedBin(0).GetBinWidth(1) =  Njets_Data_0dataDriven
        # something is wrong here? is that why the binwidth, binLowEdge, etc.. of purity are all 0?
        # Print purity as function of final shape bins
        for i, line in enumerate(table):
            Print (line, i==0)
        return
        
    ## Calculates the result for 2D histograms
    def _doCalculate2D(self, nSplitBins, shape, normFactors, optionPrintPurityByBins, optionDoNQCDByBinHistograms, myUncertaintyLabels):
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
                print ShellStyles.WarningLabel()+"No normalization factors available for bin '%s' when accessing histogram %s! Ignoring this bin..."%(wQCDLabel,shape.getHistoName())
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
    

class QCDInvertedResultManager:
    '''
    Manager class for obtaining all the required information to be saved to a pseudo-multicrab
    '''
    def __init__(self,
                 dataPath,
                 ewkPath,
                 dsetMgr,
                 luminosity,
                 moduleInfoString,
                 normFactors,
                 optionCalculateQCDNormalizationSyst=True,
                 normDataSrc = None,
                 normEWKSrc  = None,
                 optionUseInclusiveNorm=False,
                 verbose=False):
        self._shapePlots = []
        self._shapePlotLabels = []
        self._QCDNormalizationSystPlots = []
        self._QCDNormalizationSystPlotLabels = []
        self._moduleInfoString = moduleInfoString
        self._useInclusiveNorm = optionUseInclusiveNorm
        if len(normFactors.keys()) == 1 and normFactors.keys()[0] == "Inclusive":
            self._useInclusiveNorm = True
        self._verbose = verbose

        msg = "Obtaining final shape from data path \"%s\"" % (dataPath) 
        Verbose(ShellStyles.HighlightStyle() + msg + ShellStyles.NormalStyle(), self._verbose)

        # Determine list of plots to consider
        myObjects = dsetMgr.getDataset("Data").getDirectoryContent(dataPath)
        
        # Ignore unwanted histograms and those designed for HToTauNu
        keywordList = ["BackToBackAngularCuts", "CollinearAngularCuts", "DeltaPhiTauMet", "MET", "SelectedMu", "SelectedTau", "shapeTransverseMass"]
        ignoreList  = []
        for k in keywordList:
            ignoreList.extend(filter(lambda name: k in name, myObjects))

        msg = "Ignoring a total of %s unwanted histograms and/or those designed for HToTauNu" % (len(ignoreList))
        Print(ShellStyles.HighlightStyle() + msg + ShellStyles.NormalStyle(), True)

        # Update myObjects list with filtered results
        myObjects = list(x for x in myObjects if x not in ignoreList)

        # For-Loop: All  plots to consider
        for i, plotName in enumerate(myObjects, 1):

            msg = "Histogram %d/%d: %s" % (i, len(myObjects), os.path.join(dataPath, plotName) )
            Print(ShellStyles.HighlightAltStyle() + msg + ShellStyles.NormalStyle(), True)

            # Ensure that histograms exist
            dataOk = self._sanityChecks(dsetMgr, dataPath, plotName) 
            ewkOk  = self._sanityChecks(dsetMgr, ewkPath, plotName)

            # Obtain shape plots (the returned object is not owned)
            myShapeHisto = self._obtainShapeHistograms(i, dataPath, ewkPath, dsetMgr, plotName, luminosity, normFactors)

            # Obtain plots for systematics coming from met shape difference for control plots
            if optionCalculateQCDNormalizationSyst:
                if isinstance(myShapeHisto, ROOT.TH2):
                    print ShellStyles.WarningLabel()+"Skipping met shape uncertainty because histogram has more than 1 dimensions!"
                else:
                    self._obtainQCDNormalizationSystHistograms(myShapeHisto, dsetMgr, plotName, luminosity, normDataSrc, normEWKSrc)
            print "1"*100
        return

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
            Print(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), True)
        else:
            (myRootObject, myRootObjectName) = dsetMgr.getDataset("EWK").getFirstRootHisto("%s/%s" % (dirName,plotName) )
            if isinstance(myRootObject, ROOT.TH2):
                msg ="Skipping '%s', because it is not a TH1 object" % (plotName)
                Print(ShellStyles.WarningLabel() + msg + ShellStyles.NormalStyle(), True)
                myStatus = False
            myRootObject.Delete()
        return myStatus
    
    def _obtainShapeHistograms(self, i, dataPath, ewkPath, dsetMgr, plotName, luminosity, normFactors):
        
        # Get the shape
        myShape    = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr,"Data", "EWK", plotName, dataPath, ewkPath, luminosity)
        moduleInfo = self._moduleInfoString + "_" + plotName
        myPlot     = QCDInvertedShape(myShape, moduleInfo, normFactors, optionUseInclusiveNorm=self._useInclusiveNorm)

        myShape.delete()
        myPlotHisto = aux.Clone(myPlot.getResultShape(), "ctrlPlotShapeInManager")
        myPlot.delete()
        myPlotHisto.SetName(plotName+"%d"%i)
        myPlotHisto.SetTitle(plotName)
        self._shapePlots.append(myPlotHisto)
        self._shapePlotLabels.append(plotName)

        # MC EWK and purity
        myPlotMCEWKHisto = aux.Clone(myPlot.getResultMCEWK(), "ctrlPlotMCEWKInManager")
        myPlotMCEWKHisto.SetName(plotName+"%d_MCEWK"%i)
        myPlotMCEWKHisto.SetTitle(plotName+"_MCEWK")
        self._shapePlots.append(myPlotMCEWKHisto)
        self._shapePlotLabels.append(myPlotMCEWKHisto.GetTitle())
        myPlotPurityHisto = aux.Clone(myPlot.getResultPurity(), "ctrlPlotPurityInManager")
        myPlotPurityHisto.SetName(plotName+"%d_Purity"%i)
        myPlotPurityHisto.SetTitle(plotName+"_Purity")
        self._shapePlots.append(myPlotPurityHisto)
        self._shapePlotLabels.append(myPlotPurityHisto.GetTitle())
        return myPlotHisto

    def _obtainQCDNormalizationSystHistograms(self, shapeHisto, dsetMgr, plotName, luminosity, normDataSrc, normEWKSrc):
        msg = "...Obtaining region transition systematics"
        Print(ShellStyles.HighlightStyle() + msg + ShellStyles.NormalStyle(), True)
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
