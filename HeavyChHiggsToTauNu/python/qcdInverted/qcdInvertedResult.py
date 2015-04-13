# Description: Calculates QCD Inverted shapes with the appropriate normalization
# Makes also the shape histograms in phase space bins and the final shape
# Note: Systematic uncertainties need to be treated separately (since they should be taken from variation modules)
#
# Authors: LAW

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles as ShellStyles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.extendedCount as extendedCount
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.errorPropagation as errorPropagation
import HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.systematicsForMetShapeDifference as systematicsForMetShapeDifference
import HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.dataDrivenQCDCount as dataDrivenQCDCount
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.systematics as systematics
import math
import ROOT

## Class for calculating the QCD factorised results
# Shape has to be a dataDrivenQCDCount object
class QCDInvertedShape:
    def __init__(self, shape, moduleInfoString, normFactors, optionPrintPurityByBins=False, optionDoNQCDByBinHistograms=False):
        self._resultCountObject = None # ExtendedCount object which contains the result
        self._resultShape = None # TH1F which contains the final shape histogram for NQCD
        self._resultShapeEWK = None # TH1F which contains the final shape histogram for EWK MC
        self._resultShapePurity = None # TH1F which contains the final shape histogram for QCD purity
        self._histogramsList = [] # List of TH1F histograms
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
        for i in range(0, nSplitBins):
            # Get data-driven QCD, data, and MC EWK shape histogram for the phase space bin
            h = shape.getDataDrivenQCDHistoForSplittedBin(i)
            hData = shape.getDataHistoForSplittedBin(i)
            hEwk = shape.getEwkHistoForSplittedBin(i)
            # Get normalization factor
            if not shape.getPhaseSpaceBinFileFriendlyTitle(i) in normFactors.keys():
                raise Exception(ShellStyles.ErrorLabel()+"No normalization factors available for bin '%s' when accessing histogram %s!"%(shape.getPhaseSpaceBinFileFriendlyTitle(i),shape.getHistoName()))
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
            if not shape.getPhaseSpaceBinFileFriendlyTitle(i) in normFactors.keys():
                raise Exception(ShellStyles.ErrorLabel()+"No normalization factors available for bin '%s' when accessing histogram %s!"%(shape.getPhaseSpaceBinFileFriendlyTitle(i),shape.getHistoName()))
            wQCD = normFactors[shape.getPhaseSpaceBinFileFriendlyTitle(i)]
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

class QCDInvertedControlPlot: # OBSOLETE
    def __init__(self, shape, moduleInfoString, normFactors, title=""):
        self._resultShape = None # TH1F which contains the final shape histogram
        self._normFactors = normFactors
        self._title = title
        if title == "":
            title = "NQCDCtrl_Total_%s"%moduleInfoString
        self._doCalculate(shape, moduleInfoString)

    def delete(self):
        self._resultShape.Delete()
        self._normFactors = None

    ## Returns the final shape histogram
    def getResultShape(self):
        return self._resultShape

    ## Calculates the result
    def _doCalculate(self, shape, moduleInfoString):
        # Calculate final shape in signal region (shape * w_QCD)
        nSplitBins = shape.getNumberOfPhaseSpaceSplitBins()
        # Initialize result containers
        self._resultShape = aux.Clone(shape.getDataDrivenQCDHistoForSplittedBin(0))
        self._resultShape.Reset()
        self._resultShape.SetTitle(self._title+"tmp")
        self._resultShape.SetName(self._title+"tmp")
        ROOT.SetOwnership(self._resultShape, True)
        myUncertaintyLabels = ["statData", "statEWK"]
        self._resultCountObject = extendedCount.ExtendedCount(0.0, [0.0, 0.0], myUncertaintyLabels)
        # Calculate results separately for each phase space bin and then combine
        for i in range(0, nSplitBins):
            # Get data-driven QCD, data, and MC EWK shape histogram for the phase space bin
            h = shape.getDataDrivenQCDHistoForSplittedBin(i)
            # Get normalization factor
            if not shape.getPhaseSpaceBinFileFriendlyTitle(i) in self._normFactors.keys():
                raise Exception(ShellStyles.ErrorLabel()+"No normalization factors available for bin '%s' when accessing histogram %s!"%(shape.getPhaseSpaceBinFileFriendlyTitle(i),shape.getHistoName()))
            wQCD = self._normFactors[shape.getPhaseSpaceBinFileFriendlyTitle(i)]
            # Loop over bins in the shape histogram
            for j in range(1,h.GetNbinsX()+1):
                myResult = 0.0
                myResultStatUncert = 0.0
                if abs(h.GetBinContent(j)) > 0.00001: # Ignore zero bins
                    # Calculate result
                    myResult = h.GetBinContent(j) * wQCD
                    myResultStatUncert = h.GetBinError(j) * wQCD
                    # Do not calculate here MC EWK syst.
                self._resultShape.SetBinContent(j, self._resultShape.GetBinContent(j) + myResult)
                self._resultShape.SetBinError(j, self._resultShape.GetBinError(j) + myResultStatUncert**2) # Sum squared
            h.Delete()
        # Take square root of uncertainties
        for j in range(1,self._resultShape.GetNbinsX()+1):
            self._resultShape.SetBinError(j, math.sqrt(self._resultShape.GetBinError(j)))
        # Print result
        print "Control plot integral(%s) = %s "%(self._title, self._resultShape.Integral())

class QCDInvertedResultManager:
    def __init__(self, shapeString, normalizationPoint, dsetMgr, luminosity, moduleInfoString, normFactors, dataDrivenFakeTaus=False, shapeOnly=False, displayPurityBreakdown=False, noRebin=False):
        print ShellStyles.HighlightStyle()+"...Obtaining final shape"+ShellStyles.NormalStyle()
        # Obtain QCD shapes
        myRebinList = None
        if not noRebin:
            myRebinList = systematics.getBinningForPlot(shapeString)

        myShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr, "Data", "EWK", shapeString, luminosity, myRebinList,dataDrivenFakeTaus=dataDrivenFakeTaus)
        # Calculate final shape in signal region (leg1 * leg2 / basic)
        myResult = QCDInvertedShape(myShape, moduleInfoString, normFactors, optionPrintPurityByBins=displayPurityBreakdown)
        myShape.delete()
        self._hShape = aux.Clone(myResult.getResultShape())
        self._hShape.SetName(self._hShape.GetName()+"finalShapeInManager")
        self._hShapeMCEWK = aux.Clone(myResult.getResultMCEWK())
        self._hShapeMCEWK.SetName(self._hShape.GetName()+"finalShapeInManager")
        self._hShapePurity = aux.Clone(myResult.getResultPurity())
        self._hShapePurity.SetName(self._hShape.GetName()+"finalShapeInManager")
        myResult.delete()
        if not shapeOnly:
            print ShellStyles.HighlightStyle()+"...Obtaining region transition systematics"+ShellStyles.NormalStyle()
            # Do systematics coming from met shape difference
            histoNamePrefix = "MT"
            if shapeString == "shapeInvariantMass":
                histoNamePrefix = "INVMASS"
            myCtrlRegionName = "Inverted/%sInvertedTauId%s"%(histoNamePrefix, normalizationPoint)
            mySignalRegionName = "baseline/%sBaselineTauId%s"%(histoNamePrefix, normalizationPoint)
            myCtrlRegionShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr, "Data", "EWK", myCtrlRegionName, luminosity, myRebinList) #dataDrivenFakeTaus=dataDrivenFakeTaus
            mySignalRegionShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr, "Data", "EWK", mySignalRegionName, luminosity, myRebinList) #dataDrivenFakeTaus=dataDrivenFakeTaus
            myRegionTransitionSyst = systematicsForMetShapeDifference.SystematicsForMetShapeDifference(mySignalRegionShape, myCtrlRegionShape, self._hShape, moduleInfoString=moduleInfoString)
            self._hRegionSystUp = aux.Clone(myRegionTransitionSyst.getUpHistogram(), "QCDinvMgrQCDSystUp")
            self._hRegionSystDown = aux.Clone(myRegionTransitionSyst.getDownHistogram(), "QCDinvMgrQCDSystDown")
            self._hRegionSystNumerator = aux.Clone(myRegionTransitionSyst.getCombinedSignalRegionHistogram(), "QCDinvMgrQCDSystNumerator")
            self._hRegionSystDenominator = aux.Clone(myRegionTransitionSyst.getCombinedCtrlRegionHistogram(), "QCDinvMgrQCDSystDenominator")
            myRegionTransitionSyst.delete()
            # Obtain data-driven control plots
            self._hCtrlPlotLabels = []
            self._hCtrlPlotLabelsForQCDSyst = []
            self._hCtrlPlots = []
            self._hRegionSystUpCtrlPlots = []
            self._hRegionSystDownCtrlPlots = []
            self._hRegionSystNumenatorCtrlPlots = []
            self._hRegionSystDenominatorCtrlPlots = []
            myObjects = dsetMgr.getDataset("Data").getDirectoryContent("ForDataDrivenCtrlPlots")
            i = 0
            for item in myObjects:
                myStatus = True
                i += 1
                print ShellStyles.HighlightStyle()+"...Obtaining ctrl plot %d/%d: %s%s"%(i,len(myObjects),item,ShellStyles.NormalStyle())
                myEWKFoundStatus = True
                for d in dsetMgr.getDataset("EWK").datasets:
                    if not d.hasRootHisto("%s/%s"%("ForDataDrivenCtrlPlots",item)):
                        myEWKFoundStatus = False
                if not myEWKFoundStatus:
                    myStatus = False
                    if isinstance(self._hShape, ROOT.TH2):
                        print ShellStyles.WarningLabel()+"Skipping uncertainties because histogram has more than 1 dimensions!"
                    else:
                        print ShellStyles.WarningLabel()+"Skipping '%s', because it does not exist for all EWK datasets (you probably forgot to set histo level to Vital when producing the multicrab)!"%(item)+ShellStyles.NormalStyle()
                else:
                    (myRootObject, myRootObjectName) = dsetMgr.getDataset("EWK").getFirstRootHisto("%s/%s"%("ForDataDrivenCtrlPlots",item))
                    if isinstance(myRootObject, ROOT.TH2):
                        print ShellStyles.WarningLabel()+"Skipping '%s', because it is not a TH1 object!"%(item)+ShellStyles.NormalStyle()
                        myStatus = False
                if myStatus:
                    myRebinList = None # Do rebinning in datacard generator
                    myCtrlShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr, "Data", "EWK", "ForDataDrivenCtrlPlots/%s"%item, luminosity, rebinList=myRebinList,dataDrivenFakeTaus=dataDrivenFakeTaus)
                    myCtrlPlot = QCDInvertedShape(myCtrlShape, moduleInfoString+"_"+item, normFactors)
                    myCtrlShape.delete()
                    self._hCtrlPlotLabels.append(item)
                    myCtrlPlotHisto = aux.Clone(myCtrlPlot.getResultShape(), "ctrlPlotShapeInManager")
                    myCtrlPlotHisto.SetName(item+"%d"%i)
                    myCtrlPlotHisto.SetTitle(item)
                    self._hCtrlPlots.append(myCtrlPlotHisto)
                    # MC EWK and purity
                    self._hCtrlPlotLabels.append(item+"_MCEWK")
                    myCtrlPlotMCEWKHisto = aux.Clone(myCtrlPlot.getResultMCEWK(), "ctrlPlotMCEWKInManager")
                    myCtrlPlotMCEWKHisto.SetName(item+"%d_MCEWK"%i)
                    myCtrlPlotMCEWKHisto.SetTitle(item+"_MCEWK")
                    self._hCtrlPlots.append(myCtrlPlotMCEWKHisto)
                    self._hCtrlPlotLabels.append(item+"_Purity")
                    myCtrlPlotPurityHisto = aux.Clone(myCtrlPlot.getResultPurity(), "ctrlPlotPurityInManager")
                    myCtrlPlotPurityHisto.SetName(item+"%d_Purity"%i)
                    myCtrlPlotPurityHisto.SetTitle(item+"_Purity")
                    self._hCtrlPlots.append(myCtrlPlotPurityHisto)
                    # Add labels
                    if not isinstance(myCtrlPlotHisto, ROOT.TH2):
                        self._hCtrlPlotLabelsForQCDSyst.append(item)
                    myCtrlPlot.delete()
                    # Do systematics coming from met shape difference for control plots
                    if isinstance(myCtrlPlotHisto, ROOT.TH2):
                        print ShellStyles.WarningLabel()+"Skipping met shape uncertainty because histogram has more than 1 dimensions!"
                    else:
                        myCtrlPlotSignalRegionShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr, "Data", "EWK", "%s/%s"%("ForDataDrivenCtrlPlotsQCDNormalizationSignal",item), luminosity, rebinList=myRebinList) #dataDrivenFakeTaus=dataDrivenFakeTaus
                        myCtrlPlotControlRegionShape = dataDrivenQCDCount.DataDrivenQCDShape(dsetMgr, "Data", "EWK", "%s/%s"%("ForDataDrivenCtrlPlotsQCDNormalizationControl",item), luminosity, rebinList=myRebinList) #dataDrivenFakeTaus=dataDrivenFakeTaus
                        myCtrlPlotRegionTransitionSyst = systematicsForMetShapeDifference.SystematicsForMetShapeDifference(myCtrlPlotSignalRegionShape, myCtrlPlotControlRegionShape, myCtrlPlotHisto, moduleInfoString=moduleInfoString, quietMode=True)
                        myCtrlPlotSignalRegionShape.delete()
                        myCtrlPlotControlRegionShape.delete()
                        # Up variation
                        hUp = aux.Clone(myCtrlPlotRegionTransitionSyst.getUpHistogram(), "QCDfactMgrSystQCDSystUp%d"%i)
                        hUp.SetTitle(item+"systQCDUp")
                        self._hRegionSystUpCtrlPlots.append(hUp)
                        # Down variation
                        hDown = aux.Clone(myCtrlPlotRegionTransitionSyst.getDownHistogram(), "QCDfactMgrSystQCDSystDown%d"%i)
                        hDown.SetTitle(item+"systQCDDown")
                        self._hRegionSystDownCtrlPlots.append(hDown)
                        # Source histograms
                        hNum = aux.Clone(myCtrlPlotRegionTransitionSyst.getCombinedSignalRegionHistogram(), "QCDfactMgrSystQCDSystNumerator%d"%i)
                        hNum.SetTitle(item+"systQCDNumerator")
                        self._hRegionSystNumenatorCtrlPlots.append(hNum)
                        hDenom = aux.Clone(myCtrlPlotRegionTransitionSyst.getCombinedCtrlRegionHistogram(), "QCDfactMgrSystQCDSystDenominator%d"%i)
                        hDenom.SetTitle(item+"systQCDDenominator")
                        self._hRegionSystDenominatorCtrlPlots.append(hDenom)
                        # Free memory
                        myCtrlPlotRegionTransitionSyst.delete()
                        #print "\n***** memdebug %d\n"%i
                        #if i <= 2:
                        #    ROOT.gDirectory.GetList().ls()
                myRootObject.Delete()
        myCtrlRegionShape.delete()
        mySignalRegionShape.delete()

    ## Delete the histograms
    def delete(self):
        def delList(l):
            for h in l:
                h.Delete()
            l = None
        self._hShape.Delete()
        self._hShapeMCEWK.Delete()
        self._hShapePurity.Delete()
        self._hRegionSystUp.Delete()
        self._hRegionSystDown.Delete()
        self._hRegionSystDenominator.Delete()
        self._hRegionSystNumerator.Delete()
        self._hCtrlPlotLabels = None
        delList(self._hCtrlPlots)
        delList(self._hRegionSystUpCtrlPlots)
        delList(self._hRegionSystDownCtrlPlots)
        delList(self._hRegionSystNumenatorCtrlPlots)
        delList(self._hRegionSystDenominatorCtrlPlots)

    def getShape(self):
        return self._hShape

    def getShapeMCEWK(self):
        return self._hShapeMCEWK

    def getShapePurity(self):
        return self._hShapePurity

    def geRegionSystUp(self):
        return self._hRegionSystUp

    def geRegionSystDown(self):
        return self._hRegionSystDown

    def getRegionSystNumerator(self):
        return self._hRegionSystNumerator

    def getRegionSystDenominator(self):
        return self._hRegionSystDenominator

    def getControlPlotLabels(self):
        return self._hCtrlPlotLabels

    def getControlPlotLabelsForQCDSyst(self):
        return self._hCtrlPlotLabelsForQCDSyst

    def getControlPlots(self):
        return self._hCtrlPlots

    def getRegionSystUpCtrlPlots(self):
        return self._hRegionSystUpCtrlPlots

    def getRegionSystDownCtrlPlots(self):
        return self._hRegionSystDownCtrlPlots

    def getRegionSystNumeratorCtrlPlots(self):
        return self._hRegionSystNumenatorCtrlPlots

    def getRegionSystDenominatorCtrlPlots(self):
        return self._hRegionSystDenominatorCtrlPlots
