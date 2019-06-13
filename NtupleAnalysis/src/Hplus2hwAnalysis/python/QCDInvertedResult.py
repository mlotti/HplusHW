# Description: Calculates QCD Inverted shapes with the appropriate normalization
# Makes also the shape histograms in phase space bins and the final shape
# Note: Systematic uncertainties need to be treated separately (since they should be taken from variation modules)
#
# Authors: LAW

import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.extendedCount as extendedCount
import HiggsAnalysis.NtupleAnalysis.tools.errorPropagation as errorPropagation
import HiggsAnalysis.Hplus2hwAnalysis.systematicsForMetShapeDifference as metSyst
import HiggsAnalysis.Hplus2hwAnalysis.dataDrivenQCDCount as dataDrivenQCDCount
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import math
import os
import ROOT

## Class for calculating the QCD factorised results
# Shape has to be a dataDrivenQCDCount object
class QCDInvertedShape:
    def __init__(self, shape, moduleInfoString, normFactors, optionPrintPurityByBins=False, optionDoNQCDByBinHistograms=False, optionUseInclusiveNorm=False):
        self._resultCountObject = None # ExtendedCount object which contains the result
        self._resultShape = None # TH1F which contains the final shape histogram for NQCD
        self._resultShapeEWK = None # TH1F which contains the final shape histogram for EWK MC
        self._resultShapePurity = None # TH1F which contains the final shape histogram for QCD purity
        self._histogramsList = [] # List of TH1F histograms
        self._optionUseInclusiveNorm = optionUseInclusiveNorm
        self._doCalculate(shape, moduleInfoString, normFactors, optionPrintPurityByBins, optionDoNQCDByBinHistograms)

    def delete(self):
        self._resultShape.Delete()
        for h in self._histogramsList:
            h.Delete()
        self._histogramsList = None

    ## Returns the ExtendedCountObject with the result
    def getResultCountObject(self):
        return self._resultCountObject

    ## Returns the final shape histogram
    def getResultShape(self):
        return self._resultShape

    ## Returns the MC EWK contribution to final shape histogram
    def getResultMCEWK(self):
        return self._resultShapeEWK

    ## Returns the final shape purity histogram
    def getResultPurity(self):
        return self._resultShapePurity

    ## Returns the list of shape histograms (one for each split phase space bin)
    def getNQCDHistograms(self):
        return self._histogramsList

    ## Calculates the result
    def _doCalculate(self, shape, moduleInfoString, normFactors, optionPrintPurityByBins, optionDoNQCDByBinHistograms):
        # Calculate final shape in signal region (shape * w_QCD)
        nSplitBins = shape.getNumberOfPhaseSpaceSplitBins()
        # Initialize result containers
        self._resultShape = aux.Clone(shape.getDataDrivenQCDHistoForSplittedBin(0))
        self._resultShape.Reset()
        self._resultShape.SetTitle("NQCDFinal_Total_%s"%moduleInfoString)
        self._resultShape.SetName("NQCDFinal_Total_%s"%moduleInfoString)
        self._resultShapeEWK = aux.Clone(shape.getDataDrivenQCDHistoForSplittedBin(0))
        self._resultShapeEWK.Reset()
        self._resultShapeEWK.SetTitle("NQCDFinal_EWK_%s"%moduleInfoString)
        self._resultShapeEWK.SetName("NQCDFinal_EWK_%s"%moduleInfoString)
        self._resultShapePurity = aux.Clone(shape.getDataDrivenQCDHistoForSplittedBin(0))
        self._resultShapePurity.Reset()
        self._resultShapePurity.SetTitle("NQCDFinal_Purity_%s"%moduleInfoString)
        self._resultShapePurity.SetName("NQCDFinal_Purity_%s"%moduleInfoString)
        self._histogramsList = []
        myUncertaintyLabels = ["statData", "statEWK"]
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
        myShapeDataSum = []
        myShapeDataSumUncert = []
        myShapeEwkSum = []
        myShapeEwkSumUncert = []
        for j in range(1,self._resultShape.GetNbinsX()+1):
            myShapeDataSum.append(0.0)
            myShapeDataSumUncert.append(0.0)
            myShapeEwkSum.append(0.0)
            myShapeEwkSumUncert.append(0.0)
        # Calculate results separately for each phase space bin and then combine
#        print "nSplitted bins: ", nSplitBins
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
#            print "DEBUG: in splitted bin: ", i, " weight: ", wQCD
            for j in range(1,h.GetNbinsX()+1):
                myResult = 0.0
                myStatDataUncert = 0.0
                myStatEwkUncert = 0.0
                if abs(h.GetBinContent(j)) > 0.00001: # Ignore zero bins
                    # Calculate result
                    myResult = h.GetBinContent(j) * wQCD
                    # Calculate abs. stat. uncert. for data and for MC EWK
                    myStatDataUncert = hData.GetBinError(j) * wQCD
                    myStatEwkUncert = 0 #hEwk.GetBinError(j) * wQCD
                    #errorPropagation.errorPropagationForProduct(hLeg1.GetBinContent(j), hLeg1Data.GetBinError(j), myEffObject.value(), myEffObject.uncertainty("statData"))
                    # Do not calculate here MC EWK syst.
                myCountObject = extendedCount.ExtendedCount(myResult, [myStatDataUncert, myStatEwkUncert], myUncertaintyLabels)
                self._resultCountObject.add(myCountObject)
                if optionDoNQCDByBinHistograms:
                    self._histogramsList[i].SetBinContent(j, myCountObject.value())
                    self._histogramsList[i].SetBinError(j, myCountObject.statUncertainty())
                self._resultShape.SetBinContent(j, self._resultShape.GetBinContent(j) + myCountObject.value())
                self._resultShape.SetBinError(j, self._resultShape.GetBinError(j) + myCountObject.statUncertainty()**2) # Sum squared

                # Sum items for purity calculation
                myShapeDataSum[j-1] += hData.GetBinContent(j)*wQCD
                myShapeDataSumUncert[j-1] += (hData.GetBinError(j)*wQCD)**2
                myShapeEwkSum[j-1] += hEwk.GetBinContent(j)*wQCD
                myShapeEwkSumUncert[j-1] += (hEwk.GetBinError(j)*wQCD)**2
            h.Delete()
            hData.Delete()
            hEwk.Delete()
        # Take square root of uncertainties
        for j in range(1,self._resultShape.GetNbinsX()+1):
            self._resultShape.SetBinError(j, math.sqrt(self._resultShape.GetBinError(j)))
        # Print result
        print "NQCD Integral(%s) = %s "%(shape.getHistoName(), self._resultCountObject.getResultStringFull("%.1f"))
        # Print purity as function of final shape bins
        if optionPrintPurityByBins:
            print "Purity of shape %s"%shape.getHistoName()
            print "shapeBin purity purityUncert"
        for j in range (1,self._resultShape.GetNbinsX()+1):
            myPurity = 0.0
            myPurityUncert = 0.0
            if abs(myShapeDataSum[j-1]) > 0.000001:
                myPurity = 1.0 - myShapeEwkSum[j-1] / myShapeDataSum[j-1]
                myPurityUncert = errorPropagation.errorPropagationForDivision(myShapeEwkSum[j-1], math.sqrt(myShapeEwkSumUncert[j-1]), myShapeDataSum[j-1], math.sqrt(myShapeDataSumUncert[j-1]))
            # Store MC EWK content
            self._resultShapeEWK.SetBinContent(j, myShapeEwkSum[j-1])
            self._resultShapeEWK.SetBinError(j, math.sqrt(myShapeEwkSumUncert[j-1]))
            self._resultShapePurity.SetBinContent(j, myPurity)
            self._resultShapePurity.SetBinError(j, myPurityUncert)
            # Print purity info of final shape
            if optionPrintPurityByBins:
                myString = ""
                if j < self._resultShape.GetNbinsX():
                    myString = "%d..%d"%(self._resultShape.GetXaxis().GetBinLowEdge(j),self._resultShape.GetXaxis().GetBinUpEdge(j))
                else:
                    myString = ">%d"%(self._resultShape.GetXaxis().GetBinLowEdge(j))
                myString += " %.3f %.3f"%(myPurity, myPurityUncert)
                print myString

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

#class QCDInvertedControlPlot: # OBSOLETE
    #def __init__(self, shape, moduleInfoString, normFactors, title=""):
        #self._resultShape = None # TH1F which contains the final shape histogram
        #self._normFactors = normFactors
        #self._title = title
        #if title == "":
            #title = "NQCDCtrl_Total_%s"%moduleInfoString
        #self._doCalculate(shape, moduleInfoString)

    #def delete(self):
        #self._resultShape.Delete()
        #self._normFactors = None

    ### Returns the final shape histogram
    #def getResultShape(self):
        #return self._resultShape

    ### Calculates the result
    #def _doCalculate(self, shape, moduleInfoString):
        ## Calculate final shape in signal region (shape * w_QCD)
        #nSplitBins = shape.getNumberOfPhaseSpaceSplitBins()
        ## Initialize result containers
        #self._resultShape = aux.Clone(shape.getDataDrivenQCDHistoForSplittedBin(0))
        #self._resultShape.Reset()
        #self._resultShape.SetTitle(self._title+"tmp")
        #self._resultShape.SetName(self._title+"tmp")
        #ROOT.SetOwnership(self._resultShape, True)
        #myUncertaintyLabels = ["statData", "statEWK"]
        #self._resultCountObject = extendedCount.ExtendedCount(0.0, [0.0, 0.0], myUncertaintyLabels)
        ## Calculate results separately for each phase space bin and then combine
        #for i in range(0, nSplitBins):
            ## Get data-driven QCD, data, and MC EWK shape histogram for the phase space bin
            #h = shape.getDataDrivenQCDHistoForSplittedBin(i)
            ## Get normalization factor
            #if not shape.getPhaseSpaceBinFileFriendlyTitle(i) in self._normFactors.keys():
                #raise Exception(ShellStyles.ErrorLabel()+"No normalization factors available for bin '%s' when accessing histogram %s!"%(shape.getPhaseSpaceBinFileFriendlyTitle(i),shape.getHistoName()))
            #wQCD = self._normFactors[shape.getPhaseSpaceBinFileFriendlyTitle(i)]
            ## Loop over bins in the shape histogram
            #for j in range(1,h.GetNbinsX()+1):
                #myResult = 0.0
                #myResultStatUncert = 0.0
                #if abs(h.GetBinContent(j)) > 0.00001: # Ignore zero bins
                    ## Calculate result
                    #myResult = h.GetBinContent(j) * wQCD
                    #myResultStatUncert = h.GetBinError(j) * wQCD
                    ## Do not calculate here MC EWK syst.
                #self._resultShape.SetBinContent(j, self._resultShape.GetBinContent(j) + myResult)
                #self._resultShape.SetBinError(j, self._resultShape.GetBinError(j) + myResultStatUncert**2) # Sum squared
            #h.Delete()
        ## Take square root of uncertainties
        #for j in range(1,self._resultShape.GetNbinsX()+1):
            #self._resultShape.SetBinError(j, math.sqrt(self._resultShape.GetBinError(j)))
        ## Print result
        #print "Control plot integral(%s) = %s "%(self._title, self._resultShape.Integral())

## Manager class for obtaining all the required information to be saved to a pseudo-multicrab
class QCDInvertedResultManager:
    def __init__(self,
                 dataPath,
                 ewkPath,
                 dsetMgr,
                 luminosity,
                 moduleInfoString,
                 normFactors,
                 #dataDrivenFakeTaus=False,
                 #shapeOnly=False,
                 #displayPurityBreakdown=False,
                 #optionUseInclusiveNorm=False,
                 optionCalculateQCDNormalizationSyst=True,
                 normDataSrc=None,
                 normEWKSrc=None,
                 optionUseInclusiveNorm=False):
        self._shapePlots = []
        self._shapePlotLabels = []
        self._QCDNormalizationSystPlots = []
        self._QCDNormalizationSystPlotLabels = []
        self._moduleInfoString = moduleInfoString

        self._useInclusiveNorm = optionUseInclusiveNorm
        if len(normFactors.keys()) == 1 and normFactors.keys()[0] == "Inclusive":
            self._useInclusiveNorm = True

        print ShellStyles.HighlightStyle()+"...Obtaining final shape"+ShellStyles.NormalStyle()
        # Determine list of plots to consider
        myObjects = dsetMgr.getDataset("Data").getDirectoryContent(dataPath)
        # Loop over plots to consider
        i = 0
        for plotName in myObjects:
            i += 1
            print ShellStyles.HighlightStyle()+"...Obtaining ctrl plot %d/%d: %s%s"%(i,len(myObjects),plotName,ShellStyles.NormalStyle())
            # Check that histograms exist
            mySkipStatus = self._sanityChecks(dsetMgr, dataPath, plotName) and self._sanityChecks(dsetMgr, ewkPath, plotName)
            if not mySkipStatus:
                continue
            # Obtain shape plots (the returned object is not owned)

#	    print "DEBUG: ewkPath: ", ewkPath

            myShapeHisto = self._obtainShapeHistograms(i, dataPath, ewkPath, dsetMgr, plotName, luminosity, normFactors)
            # Obtain plots for systematics coming from met shape difference for control plots
            if optionCalculateQCDNormalizationSyst:
                if isinstance(myShapeHisto, ROOT.TH2):
                    print ShellStyles.WarningLabel()+"Skipping met shape uncertainty because histogram has more than 1 dimensions!"
                else:
                    self._obtainQCDNormalizationSystHistograms(myShapeHisto, dsetMgr, plotName, luminosity, normDataSrc, normEWKSrc)

    ## Check existence of histograms
    def _sanityChecks(self, dsetMgr, dirName, plotName):
        myStatus = True
        myFoundStatus = True
        for d in dsetMgr.getDataset("EWK").datasets:
            if not d.hasRootHisto("%s/%s"%(dirName,plotName)):
                myFoundStatus = False
        if not myFoundStatus:
            myStatus = False
            print ShellStyles.WarningLabel()+"Skipping '%s', because it does not exist for all EWK datasets (you probably forgot to set histo level to Vital when producing the multicrab)!"%(plotName)+ShellStyles.NormalStyle()
        else:
            (myRootObject, myRootObjectName) = dsetMgr.getDataset("EWK").getFirstRootHisto("%s/%s"%(dirName,plotName))
            if isinstance(myRootObject, ROOT.TH2):
                print ShellStyles.WarningLabel()+"Skipping '%s', because it is not a TH1 object!"%(plotName)+ShellStyles.NormalStyle()
                myStatus = False
            myRootObject.Delete()
        return myStatus
    
    def _obtainShapeHistograms(self, i, dataPath, ewkPath, dsetMgr, plotName, luminosity, normFactors):
        myShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr=dsetMgr,
                                                        dsetLabelData="Data",
                                                        dsetLabelEwk="EWK",
                                                        histoName=plotName,
                                                        dataPath=dataPath,
                                                        ewkPath=ewkPath,
                                                        luminosity=luminosity)
        myPlot = QCDInvertedShape(myShape,
                                  self._moduleInfoString+"_"+plotName,
                                  normFactors,
                                  optionUseInclusiveNorm=self._useInclusiveNorm)
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
        print ShellStyles.HighlightStyle()+"...Obtaining region transition systematics"+ShellStyles.NormalStyle()
        myPlotSignalRegionShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr=dsetMgr,
                                                                        dsetLabelData="Data",
                                                                        dsetLabelEwk="EWK",
                                                                        histoName=plotName,
                                                                        dataPath=normDataSrc+"", #"QCDNormalizationSignal",
                                                                        ewkPath=normEWKSrc+"", #"QCDNormalizationSignal",
                                                                        luminosity=luminosity)
        myPlotControlRegionShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr=dsetMgr,
                                                                         dsetLabelData="Data",
                                                                         dsetLabelEwk="EWK",
                                                                         histoName=plotName,
                                                                         dataPath=normDataSrc+"", #"QCDNormalizationControl",
                                                                         ewkPath=normEWKSrc+"", #"QCDNormalizationControl",
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
