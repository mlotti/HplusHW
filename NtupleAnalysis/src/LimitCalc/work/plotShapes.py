#!/usr/bin/env python
'''
DESCRIPTION:


USAGE:
cd <datacard>
./plotShapes.py [opts]
                      

EXAMPLES:
../plotShapes.py --dirName shapeSyst


LAST USED:
../plotShapes.py --dirName shapeSyst --xmax 3000 --logy --h2tb

'''

#================================================================================================
# Imports
#================================================================================================
import sys
import os
from optparse import OptionParser
import math
import array

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.systematics as systematics
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.LimitCalc.DatacardReader as DatacardReader
import HiggsAnalysis.LimitCalc.CommonLimitTools as limitTools
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles

# Height settings for the all-in-one ratio plot
_cHeaderHeight = 40
_cBodyHeight   = 180
_cFooterHeight = 70

#================================================================================================
# Class definitions
#================================================================================================
class RatioPlotContainer:
    def __init__(self, datasetName, verbose=False):
        self._verbose  = verbose
        self._dsetName = datasetName
        self._ratioPlotList = []
        self._systNameList  = []
        return

    def _GetName(self):
        return __file__.split("/")[-1].replace(".pyc", ".py")

    def Print(self, msg, printHeader=False):
        fName = self._GetName()
        if printHeader==True:
            print "=== ", fName
            print "\t", msg
        else:
            print "\t", msg
        return

    def PrintFlushed(self, msg, printHeader=True):
        '''
        Useful when printing progress in a loop
        '''
        msg = "\r\t" + msg + " "*20
        if printHeader:
            print "=== ", self._GetFName()
            sys.stdout.write(msg)
        sys.stdout.flush()
        return

    def Verbose(self, msg, printHeader=True, verbose=False):
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return

    def addRatioPlot(self, ratioPlot, systName):
        self._ratioPlotList.append(ratioPlot)
        self._systNameList.append(systName)
        return

    def drawIndividually(self):
        for i in range(0,len(self._systNameList)):
            myPlotName = "shapeSystRatioOnlyIndividual_%s_syst_%s"%(self._dsetName,self._systNameList[i])
            plot = self._ratioPlotList[i]
            backup = ROOT.gErrorIgnoreLevel
            ROOT.gErrorIgnoreLevel = ROOT.kError
            c = ROOT.TCanvas("","",600,240)
            ROOT.gErrorIgnoreLevel = backup
            c.SetLeftMargin(0.12)
            c.SetBottomMargin(0.3)
            plot.getFrame2().GetXaxis().SetTitleOffset(.85)
            plot.getFrame2().GetYaxis().SetLabelSize(26)
            plot.getFrame2().GetYaxis().SetTitleOffset(.36)
            plot.getFrame2().Draw() # Clone needed because otherwise plot.getFrame2() becomes None after Draw()
            plot.ratioHistoMgr.draw()
            plot.ratioLine.Draw("L")
            c.RedrawAxis()
            tb = histograms.PlotText(x=0.18, y=0.82, text=self._systNameList[i], size=30)
            tb.Draw()
            backup = ROOT.gErrorIgnoreLevel
            ROOT.gErrorIgnoreLevel = ROOT.kError
            for suffix in [".png",".C",".eps"]:
                c.Print("%s/%s%s" % (opts.dirName, myPlotName, suffix))
            ROOT.gErrorIgnoreLevel = backup
        return

    def drawAllInOne(self, myAllShapeNuisances, luminosity):
        myMaxSize = len(myAllShapeNuisances)
        # Create pads
        canvasHeight = _cHeaderHeight + _cBodyHeight * myMaxSize + _cFooterHeight
        c = ROOT.TCanvas("","",600,canvasHeight)
        c.Divide(1,myMaxSize)
        myHeightBefore = canvasHeight
        myHeightAfter = canvasHeight
        for i in range(0,myMaxSize):
            myHeightBefore = myHeightAfter
            p = c.cd(i+1)
            myTopMargin = 0.0
            myBottomMargin = 0.0
            if i == 0:
                # Top histogram with header
                myHeightAfter -= _cHeaderHeight + _cBodyHeight
                myTopMargin = float(_cHeaderHeight) / float(_cHeaderHeight+_cBodyHeight)
            elif i == myMaxSize-1:
                # Bottom histogram with x axis label and title
                myHeightAfter -= _cFooterHeight + _cBodyHeight
                myBottomMargin = float(_cFooterHeight) / float(_cFooterHeight+_cBodyHeight)
            else:
                # Middle histogram, only body
                myHeightAfter -= _cBodyHeight
            (xlow, ylow, xup, yup) = [ROOT.Double(x) for x in [0.0]*4]
            p.GetPadPar(xlow, ylow, xup, yup)
            p.SetPad(xlow, float(myHeightAfter)/float(canvasHeight), xup, float(myHeightBefore)/float(canvasHeight))
            p.SetBorderMode(0)
            p.SetFillStyle(4000)
            p.SetTopMargin(myTopMargin)
            p.SetBottomMargin(myBottomMargin)

        # Draw plots
        if len(self._ratioPlotList) == 0:
            self.Verbose("No ratioplots in list. Cannot draw all-in-one plot!", False)
            return

        o = self._ratioPlotList[0].getFrame2()
        myEmptyPlot = aux.Clone(o) # Keep the clone if it is needed to draw the x axis

        # For-loop: All nuisances
        for i in range(0, myMaxSize):
            p = c.cd(i+1)

            # Find plot
            myPlotIndex = None
            for j in range(0,len(self._systNameList)):
                if myAllShapeNuisances[i] == self._systNameList[j]:
                    myPlotIndex = j
            plot = None
            if myPlotIndex != None:
                plot = self._ratioPlotList[myPlotIndex].getFrame2()
            else:
                if i == myMaxSize-1:
                    plot = myEmptyPlot # Use this to draw the x axis
                else:
                    plot = self._ratioPlotList[0].getFrame2() # Only the empty frame matters

            # Draw plot
            if i == myMaxSize-1:
                # Bottom histogram
                plot.GetXaxis().SetTitleOffset(0.6*myMaxSize+0.6) # 6.6/10, 3.6/5
            else:
                plot.GetXaxis().SetTitleSize(0)
                plot.GetXaxis().SetLabelSize(0)
            plot.GetYaxis().SetLabelSize(26)
            plot.GetYaxis().SetTitleOffset(0.34*myMaxSize+0.1) # 3.5/10, 1.8/5
            plot.SetMinimum(0.601) # 0.001
            plot.SetMaximum(1.399) # 1.999

            # Plot frame for every nuisance
            plot.Draw()

            # Plot content only if affected
            if myPlotIndex != None:
                self._ratioPlotList[myPlotIndex].ratioHistoMgr.draw()
            self._ratioPlotList[0].ratioLine.Draw("L")
            p.RedrawAxis()

            # Labels for shape nuisance and dataset
            myHeight = 0.82
            if i == 0:
                myHeight = myHeight*float(_cBodyHeight) / float(_cHeaderHeight+_cBodyHeight)
            elif i == myMaxSize-1:
                myHeight = (myHeight*float(_cBodyHeight)+float(_cFooterHeight)) / float(_cFooterHeight +_cBodyHeight)
            histograms.addText(x=0.18, y=myHeight, text=myAllShapeNuisances[i], size=30)

            myHeight = 0.08
            if i == 0:
                myHeight = myHeight*float(_cBodyHeight) / float(_cHeaderHeight+_cBodyHeight)
            elif i == myMaxSize-1:
                myHeight = (myHeight*float(_cBodyHeight)+float(_cFooterHeight)) / float(_cFooterHeight +_cBodyHeight)
            histograms.addText(x=0.93, y=myHeight, text=self._dsetName, size=30, align="right")

            # Header labels
            if i == 0:
                histograms.addStandardTexts(lumi=luminosity, cmsTextPosition="outframe")

            # Labels for non-existing nuisances
            if myPlotIndex == None:
                myHeight = 0.44
                if i == 0:
                    myHeight = myHeight*float(_cBodyHeight) / float(_cHeaderHeight+_cBodyHeight)
                elif i == myMaxSize-1:
                    myHeight = (myHeight*float(_cBodyHeight)+float(_cFooterHeight)) / float(_cFooterHeight +_cBodyHeight)
                histograms.addText(x=0.555, y=myHeight, text="Not affected", size=30, align="center")

        # Save plot
        plotName = "shapeSystRatioOnlyAll_%s" % (self._dsetName)
        saveName = os.path.join(opts.dirName, plotName)
        backup   = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kError        
        # For-loop: All formats to save
        for i, ext in enumerate([".png",".C",".eps"], 1):
            fName = saveName + ext
            c.Print(fName)
            msg = "Created file %s" % (ShellStyles.SuccessStyle() + fName + ShellStyles.NormalStyle())
            self.Verbose(msg, i==1)
        ROOT.gErrorIgnoreLevel = backup
        return

#================================================================================================
# Class definitions
#================================================================================================
class DatasetContainer:
    def __init__(self, column, label, nuisances, cardReader, verbose=False):
        self._verbose = verbose
        self._name    = column
        self._label   = label
        self._uncertaintyShapes = nuisances
        self._cardReader = cardReader
        return

    def _GetName(self):
        return __file__.split("/")[-1].replace(".pyc", ".py")

    def GetName(self):
        return self._name

    def Print(self, msg, printHeader=False):
        fName = self._GetName()
        if printHeader==True:
            print "=== ", fName
            print "\t", msg
        else:
            print "\t", msg
        return

    def PrintFlushed(self, msg, printHeader=True):
        '''
        Useful when printing progress in a loop
        '''
        msg = "\r\t" + msg + " "*20
        if printHeader:
            print "=== ", self._GetFName()
            sys.stdout.write(msg)
        sys.stdout.flush()
        return

    def Verbose(self, msg, printHeader=True, verbose=False):
        if not self._verbose:
            return
        self.Print(msg, printHeader)
        return

    def debug(self):
        print "name =",self._name
        print "uncertainties = %s"%(", ".join(map(str, self._uncertaintyShapes)))

    def doPlot(self, opts, myAllShapeNuisances, f, mass, luminosity, signalTable, rebinList=None):
        def rebin(h, rebinList):
            if rebinList == None or h == None:
                return h
            myArray = array.array("d",rebinList)
            hnew = h.Rebin(len(rebinList)-1,h.GetTitle(),myArray)
            h.Delete()
            return hnew
        
        self.Verbose("Doing plots for dataset \"%s\"" % (self._name), False)
        hNominal = f.Get(self._cardReader.getHistoNameForColumn(self._name))
        hNominal = rebin(hNominal, rebinList)
        hNominal.SetFillStyle(0)
        hNominalFine = f.Get(self._cardReader.getHistoNameForColumn(self._name)+"_fineBinning")
        hNominalFine = rebin(hNominalFine, rebinList)
        hNominalHisto = histograms.Histo(hNominal, self._name, drawStyle="HIST")
        # Determine label
        mySignalLabels = ["HH","HW","Hp"]
        mySignalStatus = False
        for l in mySignalLabels:
            if l in self._name:
                mySignalStatus = True
        myMCLabels = ["HH","HW","Hp","MC"]
        myMCStatus = False
        
        for mclab in myMCLabels:
            if mclab in self._name:
                myMCStatus = True
        histograms.cmsTextMode = histograms.CMSMode.PRELIMINARY
        if myMCStatus:
            histograms.cmsTextMode = histograms.CMSMode.SIMULATION_PRELIMINARY
        x = 0.6
        size = 20
        myRatioContainer = RatioPlotContainer(self._label)
    
        # For-loop: All uncertainties
        for i, uncName in enumerate(self._uncertaintyShapes, 1):
            myShortName = uncName
            self.Verbose("{:>3} {:^1} {:<3} {:<1} {:<40}".format(i, "/", len(self._uncertaintyShapes), ":", myShortName), i==1)

            #msg = "{:<10} {:<15} {:<20}".format("m = %s GeV"  % (mass), "Shape %s (%d/%d) " % (uncName, len(self._uncertaintyShapes)))
            msg = "{:>5} {:>2} {:^1} {:>3} {:<20}".format("Shape", i, "/", str(len(self._uncertaintyShapes))+":", uncName)
            #PrintFlushed(msg, False)
            Print(msg, False)

            myLongName = self._cardReader.getHistoNameForNuisance(self._name, uncName)

            hup = f.Get("%sUp"%(myLongName))
            hup = rebin(hup, rebinList)
            hup.SetFillStyle(0)
            up     = dataset.RootHistoWithUncertainties(hup)
            upFine = f.Get("%sUp_fineBinning"%(myLongName))
            upFine = rebin(upFine, rebinList)
            nom    = dataset.RootHistoWithUncertainties(hNominal.Clone())
            nom.makeFlowBinsVisible()

            hdown = f.Get("%sDown"%(myLongName))
            hdown = rebin(hdown, rebinList)
            hdown.SetFillStyle(0)
            down     = dataset.RootHistoWithUncertainties(hdown)
            downFine = f.Get("%sDown_fineBinning"%(myLongName))
            downFine = rebin(downFine, rebinList)

            up.getRootHisto().SetLineColor(ROOT.kRed)
            nom.getRootHisto().SetLineColor(ROOT.kBlack)
            down.getRootHisto().SetLineColor(ROOT.kBlue)

            upHisto   = histograms.Histo(up, "Up %.1f"%_integral(up.getRootHisto()), drawStyle="HIST", legendStyle="l")
            downHisto = histograms.Histo(down, "Down %.1f"%_integral(down.getRootHisto()), drawStyle="HIST", legendStyle="l")
            nomHisto  = histograms.Histo(nom, "Nominal %.1f"%_integral(nom.getRootHisto()), drawStyle="HIST", legendStyle="l")

            # Add fit uncert. as stat uncert.
            for i in range(0,9):
                tailFitUp = f.Get("%s_TailFit_par%dUp"%(myLongName,i))
                tailFitDown = f.Get("%s_TailFit_par%dDown"%(myLongName,i))
                if tailFitUp != None and tailFitDown != None:
                    nom.addShapeUncertaintyFromVariation("%s_TailFit_par%d"%(self._name,i),tailFitUp,tailFitDown)
                    tailFitUp.Delete()
                    tailFitDown.Delete()
            tailfitNames = filter(lambda n: "_TailFit_" in n, nom.getShapeUncertaintyNames())
            nom.setShapeUncertaintiesAsStatistical(tailfitNames)

            # Do plot
            plot = plots.ComparisonManyPlot(nomHisto, [upHisto, downHisto])
            plot.setLuminosity(luminosity)
            plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
            myPlotName = "%s/shapeSyst_%s_syst%s" % (opts.dirName, self._label, uncName.replace("Up",""))

            # Define plot settings
            myParams = {}
            myParams["ylabel"] = "Events"
            myParams["log"]    = opts.logy
            myParams["opts"]   = {"xmin": opts.xmin, "xmax": opts.xmax, "ymin": 0.0}
            myParams["opts2"]  = {"ymin": 0.60, "ymax": 1.40}
            myParams["ratio"]  = True
            myParams["ratioType"]   = "errorScale"
            myParams["ratioYlabel"] = "Var./Nom."
            myParams["addLuminosityText"]   = True
            myParams["customizeBeforeDraw"] = customizeMarker
            myParams["addMCUncertainty"]    = True
            myParams["ratioErrorOptions"]   = {"numeratorStatSyst": False}
            if opts.logy:
                myParams["opts"]["ymin"] = 1e0
            if opts.light:
                myParams["opts"] = {"ymin": 0.0, "xmax":500.0}
            
            # Draw the plot
            plots.drawPlot(plot, myPlotName, **myParams)
            myRatioContainer.addRatioPlot(plot, myShortName)

            # Analyse up and down variation
            if mySignalStatus and upFine != None and downFine != None:
                a = abs(upFine.Integral()/hNominalFine.Integral() - 1.0)
                b = abs(1.0 - downFine.Integral()/hNominalFine.Integral())
                r = a

                if b > a:
                    r = b

                if uncName in signalTable.keys():
                    if r < signalTable[uncName]["min"]:
                        signalTable[uncName]["min"] = r
                    if r > signalTable[uncName]["max"]:
                        signalTable[uncName]["max"] = r
                else:
                    signalTable[uncName] = {}
                    signalTable[uncName]["min"] = r
                    signalTable[uncName]["max"] = r
            
        # Create plots with only the ratio plot
        if opts.individual:
            myRatioContainer.drawIndividually()
        else:
            myRatioContainer.drawAllInOne(myAllShapeNuisances, luminosity)

#================================================================================================
# Function definitions
#================================================================================================
def customizeMarker(p):
    for h in p.ratioHistoMgr.getHistos():
        if h.getName() == "BackgroundStatError":
            continue

        h.setDrawStyle("P")
        th1 = h.getRootHisto()
        th1.SetMarkerSize(2)
        th1.SetMarkerStyle(34) # or 2?
        th1.SetMarkerColor(th1.GetLineColor())
        #th1.SetLineWidth(0)
        # I have no idea why "P" above is not enough...
        #for i in xrange(1, th1.GetNbinsX()+1):
        #    th1.SetBinError(i, 0)
        # th1 is no longer a th1 but instead a TGraphAsymmErrors object
        for i in xrange(0, th1.GetN()):
            th1.SetPointEYhigh(i, 0)
            th1.SetPointEYlow(i, 0)

def doPlot(opts,mass,nameList,allShapeNuisances,luminosity,myDatacardPattern,rootFilePattern,signalTable):
    fName = rootFilePattern % mass
    f = ROOT.TFile.Open(fName)

    content = f.GetListOfKeys()
    # Suppress the warning message of missing dictionary for some iterator
    backup = ROOT.gErrorIgnoreLevel
    ROOT.gErrorIgnoreLevel = ROOT.kError
    diriter = content.MakeIterator()
    ROOT.gErrorIgnoreLevel = backup

    # Find the datacard and nuisance names
    myCardReader = DatacardReader.DataCardReader(".", mass, myDatacardPattern, rootFilePattern)
    myDatasetNames = myCardReader.getDatasetNames()
    # Find the name stem and the name of the uncertainties
    datasets = []
    shapes = []
    for d in myDatasetNames:
        myLabel = d
        myStatus = not d in nameList
        if d == myDatasetNames[0]:
            myStatus = True
            if not str(mass) in d:
                myLabel = "%sm%d"%(d,mass)
        
        myShapeNuisanceNames = myCardReader.getShapeNuisanceNames(d)
        myFilteredShapeNuisances = []
        for n in myShapeNuisanceNames:
            if not "statBin" in n and not n.endswith("_statUp") and not n.endswith("_statDown"):
                myFilteredShapeNuisances.append(n)
        if myStatus:
            myDataset = DatasetContainer(column=d, label=myLabel, nuisances=myFilteredShapeNuisances, cardReader=myCardReader, verbose=opts.verbose)
            datasets.append(myDataset)
            nameList.append(d)
        for n in myFilteredShapeNuisances:
            if not n in shapes:
                shapes.append(n)

    rebinList = None
    if opts.h2tb:
        rebinList = systematics._dataDrivenCtrlPlotBinning["LdgTetrajetMass_AfterAllSelections"] 

    ## Do the actual plots
    for i, d in enumerate(datasets, 1):
        if opts.verbose:
            d.debug()
        msg = "{:>10}, {:<20}".format("m = %d GeV" % (mass), d.GetName())
        if i < len(datasets):
            Print(ShellStyles.HighlightAltStyle() + msg + ShellStyles.NormalStyle(), False)
        else:
            Print(ShellStyles.SuccessStyle() + msg + ShellStyles.NormalStyle(), False)
        
        d.doPlot(opts, shapes, f, mass, luminosity, signalTable, rebinList)
    Verbose("Closing ROOT file %s" % (fName), True)
    f.Close()

def _integral(h):
    # return h.Integral(0, h.GetNbinsX()+1)
    return h.Integral()

def PrintFlushed(msg, printHeader=True):
    '''
    Useful when printing progress in a loop
    '''
    msg = "\r\t" + msg + " "*20
    if printHeader:
        print "=== ",  __file__.split("/")[-1]
    sys.stdout.write(msg)
    sys.stdout.flush()
    return

def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def Verbose(msg, printHeader=True, verbose=False):
    if not opts.verbose:
        return
    aux.Print(msg, printHeader)
    return

def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setGridX(opts.gridx)
    style.setGridY(opts.gridy)
    style.setLogX(opts.logx)
    style.setLogY(opts.logy)

    # Create legend and set style
    histograms.createLegend.moveDefaults(dx=-0.1, dh=-0.15)
    histograms.uncertaintyMode.set(histograms.Uncertainty.StatOnly)
    styles.ratioLineStyle.append(styles.StyleLine(lineColor=13))

    # Define some variables
    nameList          = []
    allShapeNuisances = []
    signalTable       = {}
    myDatacardPattern = ""
    myRootfilePattern = ""

    # Find out the mass points
    if opts.cardPattern == None:
        mySettings = limitTools.GeneralSettings(".",[])
        myDatacardPattern = mySettings.getDatacardPattern(limitTools.LimitProcessType.TAUJETS)
        myRootfilePattern = mySettings.getRootfilePattern(limitTools.LimitProcessType.TAUJETS)
    else:
        myDatacardPattern = opts.cardPattern.replace("MMM","M%s").replace("MM","%s")
        myRootfilePattern = opts.rootfilePattern.replace("MMM","M%s").replace("MM","%s")

    # Get mass points to consider
    massPoints = DatacardReader.getMassPointsForDatacardPattern(".", myDatacardPattern)
    Print("The following masses will be considered: %s" % (ShellStyles.HighlightAltStyle() + ", ".join(massPoints) + ShellStyles.NormalStyle() ), True)

    # For-loop: All mass points
    for i, m in enumerate(massPoints, 1):
        # Obtain luminosity from the datacard
        myLuminosity = float(limitTools.readLuminosityFromDatacard(".", myDatacardPattern % m ) )

        # Do the plots
        doPlot(opts, int(m), nameList, allShapeNuisances, myLuminosity, myDatacardPattern, myRootfilePattern, signalTable)

    # Print signal table
    Print("Max contracted uncertainty for signal:", True)    
    table = []
    align = "{:>15} {:>15} {:>15}"
    hLine = "="*50
    table.append(hLine)
    table.append(align.format("Systematic", "Minimum", "Maximum"))
    table.append(hLine)
    # For-loop: All signal    
    for i, k in enumerate(signalTable.keys(), 1):
        # Print("Key = %s" % (k), False)
        minVal = "%.3f" % (signalTable[k]["min"])
        maxVal = "%.3f" % (signalTable[k]["max"])
        msg    = align.format(k, minVal, maxVal)
        table.append(msg)
    table.append(hLine)
    for row in table:
        Print(row, False)

    msg = "All results under directory %s" % (ShellStyles.SuccessStyle() + opts.dirName + ShellStyles.NormalStyle())
    Print(msg, True)

    return

#================================================================================================
# Main
#================================================================================================
if __name__ == "__main__":
    '''
    https://docs.python.org/3/library/argparse.html
    
    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''
    # Default settings
    GRIDX       = False
    GRIDY       = False
    LOGX        = False   
    LOGY        = False   
    HELP        = False
    LIGHT       = False
    HTOTB       = False
    VERBOSE     = False
    XMIN        = 0.0
    XMAX        = 1000.0
    DIRNAME     = "shapeSyst"
    INDIVIDUAL  = False
    CARDPATTERN = None
    ROOTPATTERN = None
    HToTB       = False

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")

    parser.add_option("-h", "--help", dest="helpStatus", action="store_true", default=HELP, 
                      help="Show this help message and exit [default: %s]" % (HELP))

    parser.add_option("--individual", dest="individual", action="store_true", default=INDIVIDUAL, 
                      help="Generates individual plots for shape ratios instead of one large plot [defalt: %s]" % (INDIVIDUAL) )

    parser.add_option("--cardpattern", dest="cardPattern", action="store", default=CARDPATTERN, 
                      help="Pattern of datacard with MM denoting mass value [default: %s]" % (CARDPATTERN) )

    parser.add_option("--rootfilepattern", dest="rootfilePattern", action="store", default=ROOTPATTERN, 
                      help="Pattern of root file with MM denoting mass value [default: %s]" % (ROOTPATTERN))

    parser.add_option("--gridx", dest="gridx", default=GRIDX, action="store_true",
                      help="Enable the grid for the x-axis [default: %s]" % (GRIDX) )
    
    parser.add_option("--gridy", dest="gridy", default=GRIDY, action="store_true",
                      help="Enable the grid for the y-axis [default: %s]" % (GRIDY) )
    
    parser.add_option("--logy", dest="logy",  default=LOGY, action="store_true",
                      help="Set the y-axis to logarithmic scale [default: %s]" % (LOGY) )

    parser.add_option("--logx", dest="logx", action="store_true", default=LOGX, 
                      help="Plot x-axis (mT or invariant mass) as logarithmic [default: %s]" % (LOGX) )

    parser.add_option("--light", dest="light", action="store_true", default=LIGHT, 
                      help="Plot x-axis (mT) only up to 500 GeV (good for light H+ analysis) [default: %s]" % (LIGHT) )

    parser.add_option("--dirName", dest="dirName",  default=DIRNAME, 
                      help="The directory name under which to store the results [default: %s]" % (DIRNAME) )

    parser.add_option("--xmin", dest="xmin",  default=XMIN, type=float,
                      help="The minimum value for the x-axis [default: %s]" % (XMIN) )

    parser.add_option("--xmax", dest="xmax",  default=XMAX, type=float,
                      help="The maximum value for the x-axis [default: %s]" % (XMAX) )

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",  default=VERBOSE,
                      help="Enable verbosity (for debugging) [default: %s]" % (VERBOSE) )

    parser.add_option("--h2tb", dest="h2tb", action="store_true", default=HToTB,
                      help="Flag to indicate that settings should reflect h2tb analysis [default: %s]" % (HToTB) )

    (opts, args) = parser.parse_args()

    if opts.helpStatus:
        parser.print_help()
        sys.exit()

    # Create directory for plots
    if not os.path.exists(opts.dirName):
        os.mkdir(opts.dirName)

    main(opts)
