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
        self._NEvtsCR1       = {}
        self._NEvtsCR1_Error = {}
        self._NEvtsCR2       = {}
        self._NEvtsCR2_Error = {}
        self._NEvtsCR3       = {}
        self._NEvtsCR3_Error = {}
        self._NEvtsCR4       = {}
        self._NEvtsCR4_Error = {}
        self._TF           = {} # Transfer Factor (TF)
        self._TF_Error     = {}
        self._TF_Up        = {}
        self._TF_Down      = {}
        self._TF_Up2x      = {}
        self._TF_Down2x    = {}
        self._TF_Up3x      = {}
        self._TF_Down3x    = {}
        self._dqmKeys      = OrderedDict()
        self._myPath       = os.path.join(resultDirName, "normalisationPlots")
        self._BinLabelMap  = {}
        self._FakeBNormalization       = {} # for the time being same as TF
        self._FakeBNormalizationError  = {} # for the time being same as TF_Error
        self._FakeBNormalizationUp     = {} # for the time being same as TF_Up
        self._FakeBNormalizationUp2x   = {} 
        self._FakeBNormalizationUp3x   = {} 
        self._FakeBNormalizationDown   = {} # for the time being same as TF_Down
        self._FakeBNormalizationDown2x = {} 
        self._FakeBNormalizationDown3x = {} 

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
           # print "=== ", fName + ": class " + self.__class__.__name__
            print "=== ", fName
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
    
    def CalculateTransferFactor(self, binLabel, hFakeB_CR1, hFakeB_CR2, hFakeB_CR3, hFakeB_CR4, verbose=False):
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
        nCR1_Error = ROOT.Double(0.0)
        nCR2_Error = ROOT.Double(0.0)
        nCR3_Error = ROOT.Double(0.0)
        nCR4_Error = ROOT.Double(0.0)
        
        # Get Events in all CRs and their associated errors
        nCR1 = hFakeB_CR1.IntegralAndError(1, hFakeB_CR1.GetNbinsX()+1, nCR1_Error)
        nCR2 = hFakeB_CR2.IntegralAndError(1, hFakeB_CR2.GetNbinsX()+1, nCR2_Error)
        nCR3 = hFakeB_CR3.IntegralAndError(1, hFakeB_CR3.GetNbinsX()+1, nCR3_Error)
        nCR4 = hFakeB_CR4.IntegralAndError(1, hFakeB_CR4.GetNbinsX()+1, nCR4_Error)

        # Calculate Transfer Factor (TF) from Control Region (R) to Signal Region (SR): R = N_CR1/ N_CR2
        TF        = None
        TF_Up     = None
        TF_Up2x   = None
        TF_Up3x   = None
        TF_Down   = None
        TF_Down2x = None
        TF_Down3x = None
        TF_Error  = None
        TF        = (nCR1 / nCR2)
        TF_Error  = errorPropagation.errorPropagationForDivision(nCR1, nCR1_Error, nCR2, nCR2_Error)

        # Up variations
        TF_Up    = TF + TF_Error
        TF_Up2x  = TF + 2*TF_Error
        TF_Up3x  = TF + 3*TF_Error
        if TF_Up > 1.0:
            Print("Forcing TF_Up (=%.3f) to be equal to 1!" % ( TF_Up), i==1) # added  23 Oct 2018
            TF_Up = 1.0
        if TF_Up2x > 1.0:
            Print("Forcing TF_Up2x (=%.3f) to be equal to 1!" % ( TF_Up2x), i==1) # added  23 Oct 2018
            TF_Up2x = 1.0
        if TF_Up3x > 1.0:
            Print("Forcing TF_Up3x (=%.3f) to be equal to 1!" % ( TF_Up3x), i==1) # added  23 Oct 2018
            TF_Up3x = 1.0

        # Down variations
        TF_Down   = TF - TF_Error
        TF_Down2x = TF - 2*TF_Error
        TF_Down3x = TF - 3*TF_Error
        if TF_Down < 0.0:
            Print("Forcing TF_Down   (=%.3f) to be equal to 0" % (TF_Down), i==1) # added  23 Oct 2018
            TF_Down = 0.0
        if TF_Down2x < 0.0:
            Print("Forcing TF_Down2x (=%.3f) to be equal to 0" % (TF_Down2x), i==1) # added  23 Oct 2018
            TF_Down2x = 0.0
        if TF_Down3x < 0.0:
            Print("Forcing TF_Down3x (=%.3f) to be equal to 0" % (TF_Down3x), i==1) # added  23 Oct 2018
            TF_Down3x = 0.0

        lines.append("TF (bin=%s) = N_CR1 / N_CR2 = %f / %f =  %f +- %f" % (binLabel, nCR1, nCR2, TF, TF_Error) )

        # Calculate the transfer factors (R_{i}) where i is index of bin the Fake-b measurement is made in (pT and/or eta of ldg b-jet)
        if TF != None:
            # Replace bin label with histo title (has exact binning info)
            self._BinLabelMap[binLabel] = self.getNiceBinLabel(hFakeB_CR2.GetTitle())
            self._NEvtsCR1[binLabel]       = nCR1
            self._NEvtsCR1_Error[binLabel] = nCR1_Error
            self._NEvtsCR2[binLabel]       = nCR2
            self._NEvtsCR2_Error[binLabel] = nCR2_Error
            self._NEvtsCR3[binLabel]       = nCR3
            self._NEvtsCR3_Error[binLabel] = nCR3_Error
            self._NEvtsCR4[binLabel]       = nCR4
            self._NEvtsCR4_Error[binLabel] = nCR4_Error
            self._TF[binLabel   ]       = TF
            self._TF_Error[binLabel]    = TF_Error
            self._TF_Up[binLabel]       = TF_Up
            self._TF_Up2x[binLabel]     = TF_Up2x
            self._TF_Up3x[binLabel]     = TF_Up3x
            self._TF_Down[binLabel]     = TF_Down 
            self._TF_Down2x[binLabel]   = TF_Down2x 
            self._TF_Down3x[binLabel]   = TF_Down3x 
            self._FakeBNormalization[binLabel]       = TF         # TF
            self._FakeBNormalizationError[binLabel]  = TF_Error   # Error(TF)
            self._FakeBNormalizationUp[binLabel]     = TF_Up      # TF + Error
            self._FakeBNormalizationUp2x[binLabel]   = TF_Up2x    # TF + 2*Error
            self._FakeBNormalizationUp3x[binLabel]   = TF_Up3x    # TF + 3*Error
            self._FakeBNormalizationDown[binLabel]   = TF_Down    # TF - Error
            self._FakeBNormalizationDown2x[binLabel] = TF_Down2x  # TF - 2*Error
            self._FakeBNormalizationDown3x[binLabel] = TF_Down3x  # TF - 3*Error

        # Store all information for later used (write to file)
        self._commentLines.extend(lines)

        # Print output and store comments
        if 0:
            for i, line in enumerate(lines, 1):
                Print(line, i==1)
        return

    def getNiceBinLabel(self, binLabel):
        newLabel = binLabel.replace("abs", "")
        if 1:
            newLabel = newLabel.replace("TetrajetBjet", " ")
            newLabel = newLabel.replace("TetrajetBJet", " ")
        else: #more room
            newLabel = newLabel.replace("TetrajetBjet", "b-jet ")
            newLabel = newLabel.replace("TetrajetBJet", "b-jet ")
        newLabel = newLabel.replace("_", " ")
        newLabel = newLabel.replace("(", "|")
        newLabel = newLabel.replace(")", "|")
        newLabel = newLabel.replace("Eta", "#eta")
        newLabel = newLabel.replace("..", "-")
        newLabel = newLabel.replace("CRtwo", "")
        return newLabel

    def writeTransferFactorsToFile(self, filename, opts):
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
        s += "def FakeBNormalisationSafetyCheck(era, searchMode, optimizationMode):\n"
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
        s += "\n"

        # First write the transfer factor (for each Fake-b measurement bin)
        s += "FakeBNormalisation_Value = {\n"
        for binLabel in self._TF:            
            s += '    "%s": %f,\n' % (binLabel, self._TF[binLabel])
        s += "}\n"
        s += "\n"

        # Then write the transfer factor error (for each Fake-b measurement bin)
        s += "FakeBNormalisation_Error = {\n"
        for binLabel in self._TF_Error:
            s += '    "%s": %f,\n' % (binLabel, self._TF_Error[binLabel])
        s += "}\n"
        s += "\n"

        # Then write the transfer factors + error (for each Fake-b measurement bin)
        s += "FakeBNormalisation_ErrorUp = {\n"
        for binLabel in self._TF_Up:
            s += '    "%s": %f,\n' % (binLabel, self._TF_Up[binLabel]) 
        s += "}\n"
        s += "\n"

        # Then write the transfer factors + 2*error (for each Fake-b measurement bin)
        s += "FakeBNormalisation_ErrorUp2x = {\n"
        for binLabel in self._TF_Up2x:
            s += '    "%s": %f,\n' % (binLabel, self._TF_Up2x[binLabel])
        s += "}\n"
        s += "\n"

        # Then write the transfer factors + 3*error (for each Fake-b measurement bin)
        s += "FakeBNormalisation_ErrorUp3x = {\n"
        for binLabel in self._TF_Up3x:
            s += '    "%s": %f,\n' % (binLabel, self._TF_Up3x[binLabel])
        s += "}\n"
        s += "\n"

        # Then write the transfer factors - error (for each Fake-b measurement bin)
        s += "FakeBNormalisation_ErrorDown = {\n"
        for binLabel in self._TF_Down:
            s += '    "%s": %f,\n' % (binLabel, self._TF_Down[binLabel])
        s += "}\n"
        s += "\n"

        # Then write the transfer factors - 2*error (for each Fake-b measurement bin)
        s += "FakeBNormalisation_ErrorDown2x = {\n"
        for binLabel in self._TF_Down2x:
            s += '    "%s": %f,\n' % (binLabel, self._TF_Down2x[binLabel])
        s += "}\n"
        s += "\n"

        # Then write the transfer factors - 3*error (for each Fake-b measurement bin)
        s += "FakeBNormalisation_ErrorDown3x = {\n"
        for binLabel in self._TF_Down3x:
            s += '    "%s": %f,\n' % (binLabel, self._TF_Down3x[binLabel])
        s += "}\n"
        s += "\n"

        # Then write bin label map
        s += "BinLabelMap = {\n"
        for binLabel in self._BinLabelMap:
            s += '    "%s": \"%s\",\n' % (binLabel, self._BinLabelMap[binLabel])
        s += "}\n"
        s += "\n"
            
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
        self._generateTransferFactorsPlot() 
        self._generateDQMPlot()
        return

    def _generateTransferFactorsPlot(self):
        '''
        The resulting plot will contain the transfer factors (y-axis) for a given measurement bin (x-axis)
        This is needed in the case the Fake-b measurement is done in
        bins of a correlated quantity (e.g. eta of leading b-jet in Fake-b for HToTB, and tau-pT in the 
        case of inverted tau isolatio for HToTau)
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
        style.setGridX(False)
        style.setGridY(False)
        style.setOptStat(False)

        # Create graphs
        gFakeB = makeGraph(ROOT.kFullCircle, ROOT.kAzure, keyList, self._TF, self._TF_Error, self._TF_Error)

        # Make plot
        hFrame = ROOT.TH1F("frame","frame", len(keyList), 0, len(keyList))

        # Change bin labels to text
        for i, binLabel in enumerate(keyList, 1):
            binLabelText = self.getFormattedBinLabelString(binLabel)
            hFrame.GetXaxis().SetBinLabel(i, binLabelText)

        # Set axes names
        hFrame.GetYaxis().SetTitle("transfer factor") #R_{i}
        # hFrame.GetXaxis().SetTitle("Fake-b bin")
        
        # Customise axes
        logy = False
        if logy:
            hFrame.SetMinimum(0.6e-1)
            hFrame.SetMaximum(2e0)
        else:
            hFrame.SetMinimum(0.0)
            hFrame.SetMaximum(1.0)
            
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
        c.SetLogy(logy)
        c.SetGridx(False)
        c.SetGridy(False)

        hFrame.Draw()
        gFakeB.Draw("p same")
        histograms.addStandardTexts(cmsTextPosition="outframe")
        
        # Create the legend & draw it
        l = ROOT.TLegend(0.65, 0.80, 0.90, 0.90)
        l.SetFillStyle(-1)
        l.SetBorderSize(0)
        l.AddEntry(gFakeB, "Value #pm stat.", "LP") # "Fake-#it{b} #pm Stat.", "LP"
        l.SetTextSize(0.035)
        if 0:
            l.Draw()

        # Store ROOT ignore level to normal before changing it
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning

        # Save the plot
        for item in ["png", "C", "pdf"]:
            c.Print(self._plotDirName + "/FakeBNormalisationCoefficients.%s" % item)

        # Reset the ROOT ignore level to normal
        ROOT.gErrorIgnoreLevel = backup

        # Inform user
        msg = "Plot saved under %s" % (ShellStyles.SuccessStyle() + self._plotDirName + "/" + ShellStyles.NormalStyle())
        self.Print(msg, True)
        return

    def getFormattedBinLabelString(self, binLabel):
        '''
        Dirty trick to get what I want
        '''
        if binLabel not in self._BinLabelMap:
            raise Exception("Got unexpected bin label \"%s\"!" % binLabel)
        newLabel = self._BinLabelMap[binLabel]
        newLabel = newLabel.replace("abs(", "|")
        newLabel = newLabel.replace(")", "|")
        newLabel = newLabel.replace("..", "-")
        newLabel = newLabel.replace(":", ",")
        newLabel = newLabel.replace("TetrajetBJet", "") #"b^{ldg} ")
        newLabel = newLabel.replace("Pt", "p_{T} ")
        newLabel = newLabel.replace("Eta", "#eta ")
        if "inclusive" in binLabel.lower():
            newLabel = "Inclusive"
        return newLabel

    def _generateDQMPlot(self):
        '''
        Create a Data Quality Monitor (DQM) style plot
        to easily check the error for each transfer factor
        and whether it is within an acceptable relative error
        '''
        # Define error warning/tolerance on relative errors
        okay  = 1.0/(len(self._BinLabelMap.keys()))
        warn  = 0.5*okay
        NEvts = []
        # Check the uncertainties on the normalization factors
        for k in self._BinLabelMap:
            relErrorUp   = abs(self._TF_Up[k])/(self._TF[k])
            relErrorDown = abs(self._TF_Down[k])/(self._TF[k])
            relError     = self._TF_Error[k]/self._TF[k]
            if 0: 
                print "bin = %s , relErrorUp = %s, relErrorDown = %s " % (k, relErrorUp, relErrorDown)

            # Add DQM entries
            NCR1 = 0
            NCR2 = 0
            NCR3 = 0
            NCR4 = 0
            for j in self._NEvtsCR1:
                NCR1 += self._NEvtsCR1[j]
                NEvts.append(self._NEvtsCR1[j])
            for j in self._NEvtsCR2:
                NCR2 += self._NEvtsCR2[j]
                NEvts.append(self._NEvtsCR2[j])                
            for j in self._NEvtsCR3:
                NCR3 += self._NEvtsCR3[j]
                NEvts.append(self._NEvtsCR3[j])
            for j in self._NEvtsCR4:
                NCR4 += self._NEvtsCR4[j]
                NEvts.append(self._NEvtsCR4[j])                

            if 0:
                print "NCR1[%s] = %0.1f, NCR2[%s] = %0.1f, k = %s" % (k, self._NEvtsCR1[k], k, self._NEvtsCR2[k], k)
                print "NCR1 = %s, NCR2 = %s, k = %s" % (NCR1, NCR2, k)
                print "error/NCR1[%s] = %0.2f, error/NCR2[%s] = %0.2f" % (k, self._NEvtsCR1_Error[k]/self._NEvtsCR1[k], k, self._NEvtsCR2_Error[k]/self._NEvtsCR2[k])
            
            # Add DQM plot entries
            self._addDqmEntry(self._BinLabelMap[k], "N_{CR1}", self._NEvtsCR1[k], NCR1*okay, NCR1*warn)
            self._addDqmEntry(self._BinLabelMap[k], "N_{CR2}", self._NEvtsCR2[k], NCR2*okay, NCR2*warn)
            self._addDqmEntry(self._BinLabelMap[k], "N_{CR3}", self._NEvtsCR3[k], NCR3*okay, NCR3*warn)
            self._addDqmEntry(self._BinLabelMap[k], "N_{CR4}", self._NEvtsCR4[k], NCR4*okay, NCR4*warn)
            # self._addDqmEntry(self._BinLabelMap[k], "#frac{#sigma_{CR1}}{N_{CR1}}", self._NEvtsCR1_Error[k]/NCR1, 0.05, 0.15)
            # self._addDqmEntry(self._BinLabelMap[k], "#frac{#sigma_{CR2}}{N_{CR2}}", self._NEvtsCR2_Error[k]/NCR2, 0.05, 0.15)
            
        # Construct the DQM histogram
        nBinsX = len(self._dqmKeys[self._dqmKeys.keys()[0]].keys())
        nBinsY = len(self._dqmKeys.keys())
        h = ROOT.TH2F("FakeB DQM", "FakeB DQM", nBinsX, 0, nBinsX, nBinsY, 0, nBinsY)

        # Customise axes
        h.GetXaxis().SetLabelSize(15)
        h.GetYaxis().SetLabelSize(10)

        # Set Min and Max of z-axis
        if 0: # red, yellow, green for DQM 
            h.SetMinimum(0)
            h.SetMaximum(3)
        else: # pure entries instead of red, yellow, green
            h.SetMinimum(min(NEvts)*0.25)
            h.SetMaximum(round(max(NCR1, NCR2, NCR3, NCR4)))
            h.SetContour(10)
            #h.SetContour(3)
        if 0:
            h.GetXaxis().LabelsOption("v")
            h.GetYaxis().LabelsOption("v")
            
        nWarnings = 0
        nErrors   = 0
        # For-loop: All x-axis bins
        for i in range(h.GetNbinsX()):
            # For-loop: All y-axis bins
            for j in range(h.GetNbinsY()):
                ykey = self._dqmKeys.keys()[j]
                xkey = self._dqmKeys[ykey].keys()[i]

                # Set the bin content
                h.SetBinContent(i+1, j+1, self._dqmKeys[ykey][xkey])
                h.GetXaxis().SetBinLabel(i+1, xkey)
                h.GetYaxis().SetBinLabel(j+1, ykey)
                if self._dqmKeys[ykey][xkey] > 2:
                    nErrors += 1
                elif self._dqmKeys[ykey][xkey] > 1:
                    nWarnings += 1

        # Apply TDR style
        style = tdrstyle.TDRStyle()
        style.setOptStat(False)
        style.setGridX(False)
        style.setGridY(False)
        style.setWide(True, 0.15)
        
        # Set the colour styling (red, yellow, green)
        if 0:
            palette = array.array("i", [ROOT.kGreen+1, ROOT.kYellow, ROOT.kRed])
            ROOT.gStyle.SetPalette(3, palette)
        else:
            # https://root.cern.ch/doc/master/classTColor.html
            ROOT.gStyle.SetPalette(ROOT.kLightTemperature)
            # ROOT.gStyle.SetPalette(ROOT.kColorPrintableOnGrey)
            #tdrstyle.setRainBowPalette()
            #tdrstyle.setDeepSeaPalette()

        # Create canvas        
        c = ROOT.TCanvas()
        c.SetLogx(False)
        c.SetLogy(False)
        c.SetLogz(True)
        c.SetGridx()
        c.SetGridy()
        h.Draw("COLZ") #"COLZ TEXT"


        # Add CMS text and text with colour keys
        histograms.addStandardTexts(cmsTextPosition="outframe") 
        if 0:
            histograms.addText(0.55, 0.80, "green < %.0f %%" % (okay*100), size=20)
            histograms.addText(0.55, 0.84, "yellow < %.0f %%" % (warn*100), size=20)
            histograms.addText(0.55, 0.88, "red > %.0f %%" % (warn*100), size=20)

        # Save the canvas to a file
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kWarning
        plotName = os.path.join(self._plotDirName, "FakeBNormalisationDQM")
        # For-loop: Save formats
        for ext in ["png", "C", "pdf"]:
            saveName ="%s.%s" % (plotName, ext)
            c.Print(saveName)
        ROOT.gErrorIgnoreLevel = backup
        ROOT.gStyle.SetPalette(1)

        msg = "Obtained %d warnings and %d errors for the normalisation" % (nWarnings, nErrors)
        self.Verbose(msg)
        if nWarnings > 0:
            msg = "DQM has %d warnings and %d errors! Please have a look at %s.png." % (nWarnings, nErrors, os.path.basename(plotName))
            self.Verbose(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle(), True)

        #if nWarnings > 0 or nErrors > 0:
        if nErrors > 0:
            msg = "DQM has %d warnings and %d errors! Please have a look at %s.png." % (nWarnings, nErrors, os.path.basename(plotName))
            self.Verbose(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle(), True)
        return

    def _addDqmEntry(self, binLabel, name, value, okTolerance, warnTolerance):
        # Define colour codes
        red    = 2.5
        yellow = 1.5 
        green  = 0.5

        if not binLabel in self._dqmKeys.keys():
            self._dqmKeys[binLabel] = OrderedDict()
        result = red

        if abs(value) > okTolerance:
            result = green
        elif abs(value) > warnTolerance:
            result = yellow
        else:
            pass

        #self._dqmKeys[binLabel][name] = result
        self._dqmKeys[binLabel][name] = value
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
        lines.append("Transfer Factor (bin=%s): %f +- %f" % (binLabel, self._TF[binLabel], self._TFError[binLabel]) )
        lines.append("Normalisation (bin=%s)  : %f +- %f" % (binLabel, self._FakeBNormalization[binLabel], self._FakeBNormalizationError[binLabel]))

        # Store all information for later used (write to file)
        self._commentLines.extend(lines)
        return lines
