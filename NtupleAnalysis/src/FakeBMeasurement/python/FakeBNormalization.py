
'''
Description:
This package contains the tools for calculating 
the normalization factors from FakeBMeasurementAnalysis

Instructions for using, call the following methods:
1) create manager (each algorithm has it's own manager inheriting from a base class)
2) create templates (createTemplate()) and add fit functions to them (template::setFitter)
3) loop over bins and start by calling resetBinResults()
4) for each bin, add histogram to templates (template::setHistogram)
5) for each bin, plot templates (plotTemplates())
6) for each bin, calculate norm.coefficients (calculateNormalizationCoefficients())
7) for each bin, calculate combined norm.coefficient (calculateCombinedNormalization())
'''
#================================================================================================ 
# Imports
#================================================================================================ 
import ROOT
ROOT.gROOT.SetBatch(True)
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.fitHelper as fitHelper
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
from HiggsAnalysis.NtupleAnalysis.tools.OrderedDict import OrderedDict
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.errorPropagation as errorPropagation
import os
import shutil
import array
import sys
import datetime

#================================================================================================ 
# Global Function Definitions
#================================================================================================ 
def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def createLegend(xMin=0.62, yMin=0.79, xMax=0.92, yMax=0.92):
    l = ROOT.TLegend(xMin, yMin, xMax, yMax)
    l.SetFillStyle(-1)
    l.SetBorderSize(0)
    return l

#================================================================================================ 
# Class Definitions
#================================================================================================ 
class FakeBNormalizationManager:
    '''
    Base class for QCD measurement normalization from which specialized algorithm classes inherit
    '''
    def __init__(self, binLabels, resultDirName, moduleInfoString, verbose=False):
        self._verbose      = verbose
        self._templates    = {}
        self._binLabels    = binLabels
        self._sources      = {}
        self._commentLines = []
        self._BinLabelMap  = {}
        self._TF           = {} # Transfer Factor (TF)
        self._TF_Error     = {}
        self._TF_Up        = {}
        self._TF_Down      = {}
        self._dqmKeys      = OrderedDict()
        self._myPath       = os.path.join(resultDirName, "normalisationPlots")
        if not isinstance(binLabels, list):
            raise Exception("Error: binLabels needs to be a list of strings")
        self.Verbose("__init__")

        # No optimisation mode
        if moduleInfoString == "":
            moduleInfoString = "Default" 
        
        if not os.path.exists(self._myPath):
            self.Print("Creating new directory %s" % (self._myPath), True )
            os.mkdir(self._myPath)
        self._plotDirName = os.path.join(resultDirName, "normalisationPlots", moduleInfoString)

        # If already exists, Delete an entire directory tree
        if os.path.exists(self._plotDirName):
            msg = "Removing directory tree %s" % (self._plotDirName)
            self.Verbose(ShellStyles.NoteStyle() + msg + ShellStyles.NormalStyle(), True)
            shutil.rmtree(self._plotDirName)
        msg = "Creating directory %s" % (self._plotDirName)
        self.Verbose(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), False)
        os.mkdir(self._plotDirName)
        return

    def Print(self, msg, printHeader=False):
        fName = __file__.split("/")[-1]
        if printHeader==True:
            print "=== ", fName + ": class " + self.__class__.__name__
            print "\t", msg
        else:
            print "\t", msg
            return
        
    def Verbose(self, msg, printHeader=True, verbose=False):
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return

    def GetQCDNormalization(self, binLabel):
        if binLabel in self._TF.keys():
            return self._TF[binLabel]
        else:
            raise Exception("Error: _TF dictionary has no key \"%s\"! "% (binLabel) )

    def GetTransferFactor(self, binLabel):
        return self.GetQCDNormalization(binLabel)


    def GetQCDNormalizationError(self, binLabel):
        if binLabel in self._TF_Error.keys():
            return self._TF_Error[binLabel]
        else:
            raise Exception("Error: _TF dictionary has no key \"%s\"! "% (binLabel) )
    
    def CalculateTransferFactor(self, binLabel, hFakeB_Baseline, hFakeB_Inverted, verbose=False):
        '''
        Calculates the combined normalization and, if specified, 
        varies it up or down by factor (1+variation)
 
        TF = Transfer Factor
        SR = Signal Region
        CR = Control Region
        VR = Verification Region
        '''
        self.verbose = verbose

        # Obtain counts for QCD and EWK fakes
        lines = []

        # NOTES: Add EWKGenuineB TF, Add Data TF, add QCD TF, Add EWK TF, add MCONLY TFs
        nSR_Error = ROOT.Double(0.0)
        nCR_Error = ROOT.Double(0.0)
        # nTotalError = ROOT.TMath.Sqrt(nSRerror**2 + nCRError**2)
        
        nSR = hFakeB_Baseline.IntegralAndError(1, hFakeB_Baseline.GetNbinsX()+1, nSR_Error)
        nCR = hFakeB_Inverted.IntegralAndError(1, hFakeB_Inverted.GetNbinsX()+1, nCR_Error)
        # nTotal = nSR + nCR

        # Calculate Transfer Factor (TF) from Control Region (R) to Signal Region (SR): R = N_CR1/ N_CR2
        TF       = None
        TF_Up    = None
        TF_Down  = None
        TF_Error = None

        if 1: ## nTotal > 0.0:
            TF = nSR / nCR
            TF_Error = errorPropagation.errorPropagationForDivision(nSR, nSR_Error, nCR, nCR_Error)
            TF_Up = TF + TF_Error
            if TF_Up > 1.0:
                TF_Up = 1.0
            TF_Down = TF - TF_Error
            if TF_Down < 0.0:
                TF_Down = 0.0
        lines.append("TF (bin=%s) = N_CR1 / N_CR2 = %f / %f =  %f +- %f" % (binLabel, nSR, nCR, TF, TF_Error) )

        # Calculate the combined normalization factor (f_fakes = w*f_QCD + (1-w)*f_EWKfakes)
        fakeRate      = None
        fakeRateError = None
        fakeRateUp    = None
        fakeRateDown  = None
        if TF != None:
            #     fakeRate = w*self._TF[binLabel] + (1.0-w)*self._ewkNormalization[binLabel]
            #     fakeRateUp = wUp*self._TF[binLabel] + (1.0-wUp)*self._ewkNormalization[binLabel]
            #     fakeRateDown = wDown*self._TF[binLabel] + (1.0-wDown)*self._ewkNormalization[binLabel]
            #     fakeRateErrorPart1 = errorPropagation.errorPropagationForProduct(w, wError, self._TF[binLabel], self._TFError[binLabel])
            #     fakeRateErrorPart2 = errorPropagation.errorPropagationForProduct(w, wError, self._ewkNormalization[binLabel], self._ewkNormalizationError[binLabel])
            #     fakeRateError = ROOT.TMath.Sqrt(fakeRateErrorPart1**2 + fakeRateErrorPart2**2)
            
            # Replace bin label with histo title (has exact binning info)
            self._BinLabelMap[binLabel] = hFakeB_Inverted.GetTitle()
            self._TF[binLabel   ]       = TF
            self._TF_Error[binLabel]    = TF_Error
            self._TF_Up[binLabel]       = TF_Up
            self._TF_Down[binLabel]     = TF_Down
        # self._combinedFakesNormalizationError[binLabel] = fakeRateError
        # self._combinedFakesNormalizationUp[binLabel] = fakeRateUp
        # self._combinedFakesNormalizationDown[binLabel] = fakeRateDown

        # Store all information for later used (write to file)
        self._commentLines.extend(lines)

        # Print output and store comments
        if 0:
            for i, line in enumerate(lines, 1):
                Print(line, i==1)
        return
        
    def writeNormFactorFile(self, filename, opts):
        '''
        Save the fit results for QCD and EWK.

        The results will are stored in a python file starting with name:
        "QCDInvertedNormalizationFactors_" + moduleInfoString

        The script also summarizes warnings and errors encountered:
        - Green means deviation from normal is 0-3 %,
        - Yellow means deviation of 3-10 %, and
        - Red means deviation of >10 % (i.e. something is clearly wrong).
        
        If necessary, do adjustments to stabilize the fits to get rid of the errors/warnings. 
        The first things to work with are:
        a) Make sure enough events are in the histograms used
        b) Adjust fit parameters and/or fit functions and re-fit results
        
        Move on only once you are pleased with the normalisation coefficients
        '''
        s = ""
        s += "# Generated on %s\n"% datetime.datetime.now().ctime()
        s += "# by %s\n" % os.path.basename(sys.argv[0])
        s += "\n"
        s += "import sys\n"
        s += "\n"
        s += "def QCDInvertedNormalizationSafetyCheck(era, searchMode, optimizationMode):\n"
        s += "    validForEra        = \"%s\"\n" % opts.dataEra
        s += "    validForSearchMode = \"%s\"\n" % opts.searchMode
        s += "    validForOptMode    = \"%s\"\n" % opts.optMode
        s += "    if not era == validForEra:\n"
        s += "        raise Exception(\"Error: inconsistent era, normalisation factors valid for\",validForEra,\"but trying to use with\",era)\n"
        s += "    if not searchMode == validForSearchMode:\n"
        s += "        raise Exception(\"Error: inconsistent search mode, normalisation factors valid for\",validForSearchMode,\"but trying to use with\",searchMode)\n"
        s += "    if not optimizationMode == validForOptMode:\n"
        s += "        raise Exception(\"Error: inconsistent optimization mode, normalisation factors valid for\",validForOptMode,\"but trying to use with\",optimizationMode)\n"
        s += "    return"
        s += "\n"

        s += "QCDNormalization = {\n"
        for k in self._TF:
            if 0:
                print "key = %s, value = %s" % (k, self._TF[k])
            s += '    "%s": %f,\n'%(k, self._TF[k])
        s += "}\n"

        s += "QCDNormalizationError = {\n"
        for k in self._TF_Error:
            s += '    "%s": %f,\n'%(k, self._TF_Error[k])
        s += "}\n"

        s += "QCDNormalizationErrorUp = {\n"
        for k in self._TF_Up:
            s += '    "%s": %f,\n'%(k, self._TF_Up[k])
        s += "}\n"

        s += "QCDNormalizationErrorDown = {\n"
        for k in self._TF_Down:
            s += '    "%s": %f,\n'%(k, self._TF_Down[k])
        s += "}\n"

        self.Verbose("Writing results in file %s" % filename, True)
        fOUT = open(filename,"w")
        fOUT.write(s)
        fOUT.write("'''\n")
        for l in self._commentLines:
            fOUT.write(l + "\n")
        fOUT.write("'''\n")
        fOUT.close()

        msg = "Results written in file %s" % (ShellStyles.SuccessStyle()  + filename + ShellStyles.NormalStyle())
        self.Print(msg, True)

        # Create the transfer factors plot (for each bin of FakeB measurement)
        self._generateCoefficientPlot() 
        # self._generateDQMplot()
        return

    def _generateCoefficientPlot(self):
        '''
        This probably is needed in the case the measurement is done in
        bins of a correlated quantity (e.g. pT in the case of inverted tau isolation
        '''
        def makeGraph(markerStyle, color, binList, valueDict, upDict, downDict):
            g = ROOT.TGraphAsymmErrors(len(binList))
            for i in range(len(binList)):
                g.SetPoint(i, i+0.5, valueDict[binList[i]])
                g.SetPointEYhigh(i, upDict[binList[i]])
                g.SetPointEYlow(i, downDict[binList[i]])
            g.SetMarkerSize(1.2)
            g.SetMarkerStyle(markerStyle)
            g.SetLineColor(color)
            g.SetLineWidth(3)
            g.SetMarkerColor(color)
            return g
        # Obtain bin list in right order
        keyList = []
        keys = self._TF.keys()
        keys.sort()
#        for k in keys:
#            if "lt" in k:
#                keyList.append(k)
#        for k in keys:
#            if "eq" in k:
#                keyList.append(k)
#        for k in keys:
#            if "gt" in k:
#                keyList.append(k)

        # For-loop: All Fake-b measurement bins
        for k in keys:        
            keyList.append(k)
            #if "Inclusive" in keys:
            #    keyList.append("Inclusive")
            
            
        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(False)
        style.setGridX(True)
        style.setGridY(True)

        # Create graphs
        gFakeB  = makeGraph(ROOT.kFullCircle, ROOT.kRed, keyList, self._TF, self._TF_Error, self._TF_Error)

        # Make plot
        hFrame = ROOT.TH1F("frame","frame", len(keyList), 0, len(keyList))
        # Change bin labels to text
        for i, binLabel in enumerate(keyList, 1):
            # for i in range(len(keyList)):
            binLabelText = self.getFormattedBinLabelString(binLabel)
            #hFrame.GetXaxis().SetBinLabel(i+1, binLabelText)
            hFrame.GetXaxis().SetBinLabel(i, binLabelText)

        # Set min and max ?
        hFrame.GetYaxis().SetTitle("transfer factors (R_{i})")
        # hFrame.GetXaxis().SetTitle("Fake-b bin")
        
        # Customise axes
        hFrame.SetMinimum(0.6e-1)
        hFrame.SetMaximum(5e0)
        if len(self._BinLabelMap) > 12:
            lSize = 8
        elif len(self._BinLabelMap) > 8:
            lSize = 12
        else:
            lSize = 16
        hFrame.GetXaxis().SetLabelSize(lSize) # 20
        hFrame.GetXaxis().LabelsOption("d")
        # Label Style options
        # "a" sort by alphabetic order 
        # ">" sort by decreasing values 
        # "<" sort by increasing values 
        # "h" draw labels horizonthal 
        # "v" draw labels vertical
        # "u" draw labels up (end of label right adjusted)
        # "d" draw labels down (start of label left adjusted)

        # Create canvas
        c = ROOT.TCanvas()
        c.SetLogy(True)
        c.SetGridx()
        c.SetGridy()

        hFrame.Draw()
        gFakeB.Draw("p same")
        histograms.addStandardTexts(cmsTextPosition="outframe")
        
        # Create the legend & draw it
        l = ROOT.TLegend(0.65, 0.80, 0.90, 0.90)
        l.SetFillStyle(-1)
        l.SetBorderSize(0)
        # l.AddEntry(gFakeB, "Fake-#it{b} #pm Stat.", "LP")
        l.AddEntry(gFakeB, "Value #pm Stat.", "LP")
        l.SetTextSize(0.035)
        l.Draw()

        # Store ROOT ignore level to normal before changing it
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning

        # Save the plot
        for item in ["png", "C", "pdf"]:
            c.Print(self._plotDirName + "/QCDNormalisationCoefficients.%s" % item)

        # Reset the ROOT ignore level to normal
        ROOT.gErrorIgnoreLevel = backup

        # Inform user
        msg = "Transfer-factors written in %s " % (ShellStyles.SuccessStyle() + self._plotDirName + ShellStyles.NormalStyle())
        self.Print(msg, False)
        return

    def getFormattedBinLabelString(self, binLabel):
        '''
        Dirty trick to get what I want
        '''
        if binLabel not in self._BinLabelMap:
            # for k in self._BinLabelMap:
            #     print k
            raise Exception("Got unexpected bin label \"%s\"!" % binLabel)
        newLabel = self._BinLabelMap[binLabel]
        newLabel = newLabel.replace("abs(", "|")
        newLabel = newLabel.replace(")", "|")
        newLabel = newLabel.replace("..", "-")
        newLabel = newLabel.replace(":", ",")
        newLabel = newLabel.replace("TetrajetBjet", "") #"b^{ldg} ")
        newLabel = newLabel.replace("Pt", "p_{T} ")
        newLabel = newLabel.replace("Eta", "#eta ")
        if "inclusive" in binLabel.lower():
            newLabel = "Inclusive"
        return newLabel

    def _generateDQMplot(self):
        '''
        Create a DQM style plot
        '''
        # Check the uncertainties on the normalization factors
        for k in self._dqmKeys.keys():
            self._addDqmEntry(k, "norm.coeff.uncert::QCD" , self._TFError[k], 0.03, 0.10)
            self._addDqmEntry(k, "norm.coeff.uncert::fake", self._ewkNormalizationError[k], 0.03, 0.10)
            value = abs(self._combinedFakesNormalizationUp[k]-self._combinedFakesNormalization[k])
            value = max(value, abs(self._combinedFakesNormalizationDown[k]-self._combinedFakesNormalizationUp[k]))
            self._addDqmEntry(k, "norm.coeff.uncert::combined", value, 0.03, 0.10)
        # Construct the DQM histogram
        h = ROOT.TH2F("QCD DQM", "QCD DQM",
                      len(self._dqmKeys[self._dqmKeys.keys()[0]].keys()), 0, len(self._dqmKeys[self._dqmKeys.keys()[0]].keys()),
                      len(self._dqmKeys.keys()), 0, len(self._dqmKeys.keys()))
        h.GetXaxis().SetLabelSize(15)
        h.GetYaxis().SetLabelSize(15)
        h.SetMinimum(0)
        h.SetMaximum(3)
        #h.GetXaxis().LabelsOption("v")
        nWarnings = 0
        nErrors = 0
        for i in range(h.GetNbinsX()):
            for j in range(h.GetNbinsY()):
                ykey = self._dqmKeys.keys()[j]
                xkey = self._dqmKeys[ykey].keys()[i]
                h.SetBinContent(i+1, j+1, self._dqmKeys[ykey][xkey])
                h.GetYaxis().SetBinLabel(j+1, ykey)
                h.GetXaxis().SetBinLabel(i+1, xkey)
                if self._dqmKeys[ykey][xkey] > 2:
                    nErrors += 1
                elif self._dqmKeys[ykey][xkey] > 1:
                    nWarnings += 1
        palette = array.array("i", [ROOT.kGreen+1, ROOT.kYellow, ROOT.kRed])
        ROOT.gStyle.SetPalette(3, palette)
        c = ROOT.TCanvas()
        c.SetBottomMargin(0.2)
        c.SetLeftMargin(0.2)
        c.SetRightMargin(0.2)
        h.Draw("colz")
        
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning
        for item in ["png", "C", "pdf"]:
            c.Print(self._plotDirName+"/QCDNormalisationDQM.%s"%item)
        ROOT.gErrorIgnoreLevel = backup
        ROOT.gStyle.SetPalette(1)
        print "Obtained %d warnings and %d errors for the normalization"%(nWarnings, nErrors)
        if nWarnings > 0 or nErrors > 0:
            print "Please have a look at %s/QCDNormalisationDQM.png to see the origin of the warning(s) and error(s)"%self._plotDirName
        return

    def _addDqmEntry(self, binLabel, name, value, okTolerance, warnTolerance):
        if not binLabel in self._dqmKeys.keys():
            self._dqmKeys[binLabel] = OrderedDict()
        result = 2.5
        if abs(value) < okTolerance:
            result = 0.5
        elif abs(value) < warnTolerance:
            result = 1.5
        self._dqmKeys[binLabel][name] = result
        return

    def _getSanityCheckTextForFractions(self, dataTemplate, binLabel, saveToComments=False):
        '''
        Helper method to be called from parent class when calculating norm.coefficients
        
        NOTE: Should one divide the fractions with dataTemplate.getFittedParameters()[0] ? 
              Right now not because the correction is so small.
        '''
        self.Verbose("_getSanityCheckTextForFractions()", True)
        
        # Get variables
        label         = "QCD"
        fraction      = dataTemplate.getFittedParameters()[1]
        fractionError = dataTemplate.getFittedParameterErrors()[1]
        nBaseline     = self._templates["%s_Baseline" % label].getNeventsFromHisto(False)
        nCalculated   = fraction * dataTemplate.getNeventsFromHisto(False)

        if nCalculated > 0:
            ratio = nBaseline / nCalculated
        else:
            ratio = 0
        lines = []
        lines.append("Fitted %s fraction: %f +- %f" % (label, fraction, fractionError))
        lines.append("Sanity check: ratio = %.3f: baseline = %.1f vs. fitted = %.1f" % (ratio, nBaseline, nCalculated))

        # Store all information for later used (write to file)
        if saveToComments:
            self._commentLines.extend(lines)
        return lines

    def _checkOverallNormalization(self, template, binLabel, saveToComments=False):
        '''
        Helper method to be called from parent class when calculating norm.coefficients
        '''
        self.Verbose("_checkOverallNormalization()")
        
        # Calculatotions
        value = template.getFittedParameters()[0]
        error = template.getFittedParameterErrors()[0]

        # Definitions
        lines = []
        lines.append("The fitted overall normalization factor for purity is: (should be 1.0)")
        lines.append("NormFactor = %f +/- %f" % (value, error))

        self._addDqmEntry(binLabel, "OverallNormalization(par0)", value-1.0, 0.03, 0.10)

        # Store all information for later used (write to file)
        if saveToComments:
            self._commentLines.extend(lines)
        return lines
    
    ## Helper method to be called from parent class when calculating norm.coefficients
    def _getResultOutput(self, binLabel):
        lines = []
        lines.append("   Normalization factor (QCD): %f +- %f"%(self._TF[binLabel], self._TFError[binLabel]))
        lines.append("   Normalization factor (EWK fake taus): %f +- %f"%(self._ewkNormalization[binLabel], self._ewkNormalizationError[binLabel]))
        lines.append("   Combined norm. factor: %f +- %f"%(self._combinedFakesNormalization[binLabel], self._combinedFakesNormalizationError[binLabel]))

        # Store all information for later used (write to file)
        self._commentLines.extend(lines)
        return lines
