'''
DESCRIPTION:
 Calculates the systematics for the data-driven FakeB measurements

INSTRUCTIONS:
import this file in LimitCalc/python/Extractor.py

'''
#================================================================================================
# Imports
#================================================================================================
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
from math import sqrt
import array
from HiggsAnalysis.QCDMeasurement.dataDrivenQCDCount import *
import HiggsAnalysis.NtupleAnalysis.tools.histogramsExtras as histogramsExtras
from HiggsAnalysis.NtupleAnalysis.tools.errorPropagation import errorPropagationForDivision
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import ROOT

#================================================================================================
# Imports
#================================================================================================
class SystematicsForMetShapeDifference:
    '''
    Calculates the systematics for the data-driven FakeB measurement
    '''
    def __init__(self, signalRegion, ctrlRegion, finalShape, moduleInfoString, quietMode=False, optionDoBinByBinHistograms=False):
        '''
        Constructor
        signalRegion and ctrlRegion are of type dataDrivenQCDCount, they are the shape histograms at the tested stage
        finalShape is the final shape histogram (needs to be already properly normalised)
         moduleInfoString is a string that is unique to the analysis module    
        '''
        self._signalRegionHistograms = []
        self._ctrlRegionHistograms   = []
        self._hCombinedSignalRegion  = None
        self._hCombinedCtrlRegion    = None
        self._systUpHistogram        = None
        self._systDownHistogram      = None
        self._calculate(signalRegion, ctrlRegion, finalShape, moduleInfoString, quietMode, optionDoBinByBinHistograms)
        return

    def Print(self, msg, printHeader=False):
        fName = __file__.split("/")[-1].replace("pyc", "py")
        if printHeader==True:
            print "===", fName
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
        '''
        Delete the histograms
        '''
        for h in self._signalRegionHistograms:
            h.Delete()
        for h in self._ctrlRegionHistograms:
            h.Delete()
        self._hCombinedSignalRegion.Delete()
        self._hCombinedCtrlRegion.Delete()
        self._systUpHistogram.Delete()
        self._systDownHistogram.Delete()
        return

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
            '''
            Normalise area to unity since we only care about the shape
            '''
            myIntegral = abs(h.Integral(1, h.GetNbinsX()+2))
            if myIntegral > 0.0:
                h.Scale(1.0 / myIntegral)
            return

        nSplitBins = signalRegion.getNumberOfPhaseSpaceSplitBins()
        # Initialize histograms
        self._hCombinedSignalRegion = aux.Clone(finalShape)
        self._hCombinedSignalRegion.Reset()
        self._hCombinedSignalRegion.SetTitle("QCDSystSignalRegion_Total_%s" % (moduleInfoString) )
        self._hCombinedSignalRegion.SetName("QCDSystSignalRegion_Total_%s"  % (moduleInfoString) )
        self._hCombinedCtrlRegion = aux.Clone(finalShape)
        self._hCombinedCtrlRegion.Reset()
        self._hCombinedCtrlRegion.SetTitle("QCDSystCtrlRegion_Total_%s" % (moduleInfoString) )
        self._hCombinedCtrlRegion.SetName("QCDSystCtrlRegion_Total_%s"  % (moduleInfoString) )
        if optionDoBinByBinHistograms:
            for i in range(0, nSplitBins):
                h = aux.Clone(self._hCombinedSignalRegion)
                h.SetTitle("QCDSystSignalRegion_%s_%s" % (signalRegion.getPhaseSpaceBinFileFriendlyTitle(i), moduleInfoString) )
                h.SetName("QCDSystSignalRegion_%s_%s"  % (signalRegion.getPhaseSpaceBinFileFriendlyTitle(i), moduleInfoString) )
                self._signalRegionHistograms.append(h)
                h = aux.Clone(self._hCombinedSignalRegion)
                h.SetTitle("QCDSystCtrlRegion_%s_%s" % (signalRegion.getPhaseSpaceBinFileFriendlyTitle(i), moduleInfoString) )
                h.SetName("QCDSystCtrlRegion_%s_%s"  % (signalRegion.getPhaseSpaceBinFileFriendlyTitle(i), moduleInfoString) ) 
                self._ctrlRegionHistograms.append(h)
        self._systUpHistogram = aux.Clone(self._hCombinedSignalRegion)
        self._systUpHistogram.SetTitle("QCDSystUp_%s" % (moduleInfoString) )
        self._systUpHistogram.SetName("QCDSystUp_%s"  % (moduleInfoString) )
        self._systDownHistogram = aux.Clone(self._hCombinedSignalRegion)
        self._systDownHistogram.SetTitle("QCDSystDown_%s" % (moduleInfoString) )
        self._systDownHistogram.SetName("QCDSystDown_%s"  % (moduleInfoString) )

        # For-loop: Phase-space bins to sum histograms
        for i in range(0, nSplitBins):
            # Get data-driven FakeB shapes for invariant mass
            hSignalRegion = signalRegion.getDataDrivenQCDHistoForSplittedBin(i)
            print "hSignaRegion.GetName() = ", hSignaRegion.GetName()
            hCtrlRegion    = ctrlRegion.getDataDrivenQCDHistoForSplittedBin(i)
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
        return

class SystematicsForTransferFactor:
    def __init__(self, verbose=False):
        self._verbose = verbose
        return

    def Print(self, msg, printHeader=False):
        fName = __file__.split("/")[-1].replace("pyc", "py")
        if printHeader==True:
            print "===", fName
            print "\t", msg
        else:
            print "\t", msg
        return

    def Verbose(self, msg, printHeader=True):
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return

    def createSystHistograms(self, hRate, hSystUp, hSystDown, hSystUpFromVar, hSystDownFromVar, quietMode=True):
        '''
        Uses the histogram "hSystUpFromVar" and "hSystDownFromVar" to account the systematic uncertainties 
        related to the Transfer Factors (TF) from the Control (or Verification) 
        Region (VR) to the Signal Region (SR). This sys. uncertainty should have both a Rate + Shape impact
        on final invariant mass distribution. 

        The two aforementioned histograms correspond to the invariant massdistrubutions
        ("ForDataDrivenCtrlPlots/LdgTetrajetMass_AfterAllSelections") obtained by using applying
        the transfer factors (TF) of the FakeB measurement to shapes from the VR. Instead of the nominal TF 
        however, the TF+TF_Error and TF-TF_Error are used instead, where TF_Error is the statistical error of
        the TF, calculated by using error propagation:
        TF = CR1/CR2
        TF_Error = ErrorPropagationForDivision(TF) = sqrt((sigmaA/b)**2 + (a/(b**2)*sigmaB)**2)
        where:
        A = Integral of CR1 histogram  (from ROOT)
        sigmaA = Integral Error for CR1 histogram (from ROOT)
        These histograms should be already in place (and correctly normalised) for the FakeB pseudodataset, 
        after running the ./makePseudoMulticrab.py -m <FakeB-dir> script.

        The error is symmetric and it is basically defined as:
        hSystUp   = Rate + 1sigma
        hSystDown = Rate - 1sigma
        where the rate is obtained from the filled histogram provided ("hRate")
        and sigma is the TF_Error as discussed above (error propagation on the division of CR1 and CR2)

        In this function we don't need to calculate the error propagation. The function assumes that the histograms provided
        already have the final variations in place (i.e. up = rate+error, down = rate-error)
        ''' 
        # Get the (clean) histogram name 
        fullName  = hRate.GetName()
        cleanName = fullName.replace("_cloned", "")
        cleanName = cleanName.replace("_FakeBMeasurementTrijetMass", "")
        rebinX    = systematics.getBinningForPlot(cleanName)

        self.Verbose("Make sure this histogram has the same binning as the final data-driven plot", True)
        if rebinX != None:
            self.Verbose("Rebinning histogram \"%s\" (\"%s\")" % (cleanName, fullName), True)
            hRate        = hRate.Rebin(len(rebinX)-1, hRate.GetName(), array.array("d", rebinX))
            hSystUpFromVar   = hSystUpFromVar.Rebin(len(rebinX)-1, hSystUpFromVar.GetName(), array.array("d", rebinX))
            hSystDownFromVar = hSystDownFromVar.Rebin(len(rebinX)-1, hSystDownFromVar.GetName(), array.array("d", rebinX))
            #hSystUp      = hSystUp.Rebin(len(rebinX)-1, hSystUp.GetName(), array.array("d", rebinX))     #don't !
            #hSystDown    = hSystDown.Rebin(len(rebinX)-1, hSystDown.GetName(), array.array("d", rebinX)) #don't !

        # Constuct a summary table
        table   = []
        align  = "{:>7} {:>15} {:>10} {:>12} {:>12} {:>12} {:>10}"
        header = align.format("Bin #", "Bin Centre", "Rate (Nom)", "Rate (Up)", "Rate (Down)", "% Up", "% Down")
        hLine  = "="*85
        table.append( "{:^85}".format(cleanName))
        table.append(hLine)
        table.append(header)
        table.append(hLine)

        # For-loop: All histogram bins for given data-driven control plot
        nBinsX = hRate.GetNbinsX()
        for i in range(1, nBinsX+1):
            self.Verbose("Calculating systematic for bin \"%d\" in histogram \"%s\"" % (i, hRate.GetName()), i==1)

            # Calculate the systematics 
            rateNominal      = hRate.GetBinContent(i)
            rateSystUp       = hSystUpFromVar.GetBinContent(i)
            rateSystDown     = hSystDownFromVar.GetBinContent(i)
            binCentre        = hRate.GetBinCenter(i)

            # Calculate percentage difference wrt nominal
            if rateNominal > 0.0:
                rateSystUpPerc   = (rateSystUp-rateNominal)/(rateNominal)*100
                rateSystDownPerc = (rateSystDown-rateNominal)/(rateNominal)*100
            else:
                rateSystUpPerc   = 0
                rateSystDownPerc = 0
                
            # Fill summary table for given bin
            row = align.format(i, binCentre, "%.1f" % rateNominal, "%.1f" % rateSystUp, "%.1f" % rateSystDown, "%.1f" % rateSystUpPerc, "%.1f" % rateSystDownPerc)
            table.append(row)
            self.Verbose(ShellStyles.ErrorStyle() + row + ShellStyles.NormalStyle(), i==1)

            # Fill the up/down systematics histograms
            self.Verbose("Setting the systematics values in the histograms SystUp and SystDown", False)
            hSystUp.SetBinContent(i, rateSystUp)
            hSystDown.SetBinContent(i, rateSystDown)

        # Append total uncertainty info
        table.extend(self.GetTotalUncertainyTable(hRate, hSystUpFromVar, hSystDownFromVar, hLine, align))
        
        # Print summary table
        if  quietMode == False or self._verbose == True:
            for i, row in enumerate(table, 1):
                self.Print(row, i==1)
        return

    def GetTotalUncertainyTable(self, hRate, hSystUp, hSystDown, hLine, align):
        table = []

        # Calculate total uncertainty
        rateNominalSum  = hRate.Integral()
        rateSystUpSum   = hSystUp.Integral()
        rateSystDownSum = hSystDown.Integral()
        signalUncert   = 0.0
        ctrlUncert     = 0.0
        ratio          = 1.0
        ratioSigma     = 0.0
        nBinsX          = hRate.GetNbinsX()

        # For-loop: All bins in histo (up)
        for i in range(1, nBinsX+1):
            signalUncert += hSystUp.GetBinError(i)**2
            ctrlUncert   += hSystDown.GetBinError(i)**2

        # Sanity check
        if rateSystUpSum > 0.0 and rateSystDownSum > 0.0:
            # Calculate ratio and its error with error propagation
            ratio = rateSystUpSum / rateSystDownSum
            # Calculate ratio error with error propagation
            ratioSigma = errorPropagationForDivision(rateSystUpSum, sqrt(signalUncert), rateSystDownSum, sqrt(ctrlUncert) )

        # Calculate % errors up/down
        table.append(hLine)
        sigmaUp   = (ratio + ratioSigma - 1.0)*100
        sigmaDown = (ratio - ratioSigma - 1.0)*100
        rangeX    = "%s to %s" % (hRate.GetBinCenter(1), hRate.GetBinCenter(nBinsX))
        rangeBins = "1 to %d" % (nBinsX)    
        table.append( align.format(rangeBins, rangeX, "%.1f" % rateNominalSum, "%.1f" % rateSystUpSum, "%.1f" % rateSystDownSum, "%.1f" % (sigmaUp), "%.1f" % (sigmaDown)) )
        evtYield  = "{:^85}".format("Events +/- stat. +/- syst. = %.1f +/- %.1f +/- %.1f" % (rateNominalSum, abs(rateNominalSum-rateSystUpSum), abs(rateNominalSum-rateSystDownSum)))
        table.append( ShellStyles.HighlightAltStyle() + evtYield + ShellStyles.NormalStyle() )
        table.append(hLine)
        return table
