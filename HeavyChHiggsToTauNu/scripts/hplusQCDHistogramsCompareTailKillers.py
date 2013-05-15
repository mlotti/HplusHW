#!/usr/bin/env python

######################################################################
# All imported modules
######################################################################
# System modules
import sys
import math
import array
import re
import os
# ROOT modules
import ROOT
from ROOT import gStyle
# HPlus modules
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
# Script-specific modules
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.QCDHistoHelper as HistoHelper

######################################################################
# User options
######################################################################
bBatchMode      = True
sDataEra        = "Run2011A" #"Run2011A" #"Run2011B" #"Run2011AB"
sLegStyle       = "P"
sDrawStyle      = "P" # "AP" "EP" "HIST9"

######################################################################
# Global definitions
######################################################################
myRootFilePath  = "info/QCDMeasurementFactorisedInfo.root" 
myQCDschemes    = ["TauPt", "TauEta", "Nvtx", "Full"]
myErrorTypes    = ["StatAndSyst", "StatOnly"]
myValidDataEras = ["Run2011A", "Run2011B", "Run2011AB"]
myTailKillers   = ["ZeroPlus", "LoosePlus", "MediumPlus", "TightPlus"]

yMinRatio     = 0.0
yMaxRatio     = 2.0
yMaxFactor    = 1.5
yMinLog       = 1E-01
yMinLogNorm   = 1E-04
yMaxFactorLog = 5

ROOT.gROOT.SetBatch(bBatchMode)

######################################################################
# Function declarations
######################################################################
def main():
    
    ##################
    # Purity plots 
    ##################
    PurityStdSelList = HistoHelper.GetPurityHistoNames(sMyLeg="StandardSelections")
    doHistosCompare(PurityStdSelList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Purity_StdSel", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)
    
    PurityLeg1List = HistoHelper.GetPurityHistoNames(sMyLeg="Leg1")
    doHistosCompare(PurityLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Purity_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    PurityLeg2List = HistoHelper.GetPurityHistoNames(sMyLeg="Leg2")
    doHistosCompare(PurityLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Purity_Leg2", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)


    ##################    
    # Efficiency plots 
    ##################
    EfficiencyLeg1List = HistoHelper.GetEfficiencyHistoNames(sMyLeg="leg1")
    doHistosCompare(EfficiencyLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Efficiency_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    EfficiencyLeg2List = HistoHelper.GetEfficiencyHistoNames(sMyLeg="leg2")
    doHistosCompare(EfficiencyLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Efficiency_Leg2", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)


    ##################
    # mT shapes 
    ##################
    MtShapesStdSelList = HistoHelper.GetMtShapeHistoNames(sMyLeg="StandardSelections")
    doHistosCompare(MtShapesStdSelList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShapes_StdSel", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)
    
    MtShapesLeg1List = HistoHelper.GetMtShapeHistoNames(sMyLeg="Leg1")
    doHistosCompare(MtShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShapes_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    MtShapesLeg2List = HistoHelper.GetMtShapeHistoNames(sMyLeg="Leg2")
    doHistosCompare(MtShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShapes_Leg2", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    #binList = [1] #[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #bin 0 = underflow, bin 10 = overflow
    #for index in binList:
        #MtBinShapesLeg1List   = HistoHelper.GetMtBinShapeHistoNames(lBinList = [index], sMyLeg="Leg1")
        #doHistosCompare(MtBinShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "ClosureTest_Mt_Bin" + str(index), bNormalizeToOne = True, bRatio=False, bInvertRatio=False)


    ##################
    # MET shapes 
    ##################
    MetShapesStdSelList = HistoHelper.GetMetShapeHistoNames(sMyLeg="")
    doHistosCompare(MetShapesStdSelList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MetShapes_StdSel", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)
    
    #MetShapesLeg1List = HistoHelper.GetMetShapeHistoNames(sMyLeg="AfterLeg1")
    #doHistosCompare(MetShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MetShapes_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    MetShapesLeg2List = HistoHelper.GetMetShapeHistoNames(sMyLeg="AfterLeg2")
    doHistosCompare(MetShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MetShapes_Leg2", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    #binList = [1] #[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #bin 0 = underflow, bin 10 = overflow
    #for index in binList:
        #MetBinShapesLeg1List   = HistoHelper.GetMetBinShapeHistoNames(lBinList = [index], sMyLeg="Leg1")
        #doHistosCompare(MetBinShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "ClosureTest_Met_Bin" + str(index), bNormalizeToOne = True, bRatio=False, bInvertRatio=False)

    ##################
    # Full mass shapes 
    ##################
    MassShapeLeg1List = HistoHelper.GetMassShapeHistoNames(sMyLeg="Leg1")
    doHistosCompare(MassShapeLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MassShapes_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)


    ##################
    # QCD Event Yields
    ##################
    NqcdList = HistoHelper.GetNQcdHistoNames()
    doHistosCompare(NqcdList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "NQcd", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)
    #getNqcdNumbers()

    
    ##################
    # Number of events
    ##################
    NEvtsStdSelList = HistoHelper.GetNEventsHistoNames(sMyLeg="StandardSelections")
    doHistosCompare(NEvtsStdSelList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "NEvts_StdSel", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    NEvtsLeg1List = HistoHelper.GetNEventsHistoNames(sMyLeg="Leg1")
    doHistosCompare(NEvtsLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "NEvts_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    NEvtsLeg2List = HistoHelper.GetNEventsHistoNames(sMyLeg="Leg2")
    doHistosCompare(NEvtsLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "NEvts_Leg2", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)


    ##################
    # Number jets 
    ##################
    NjetsList  = HistoHelper.GetCtrlNjetsHistoNames()
    doHistosCompare(NjetsList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Njets", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

        
    ##################
    # Number b-jets
    ##################
    NbjetsList  = HistoHelper.GetCtrlNbjetsHistoNames()
    doHistosCompare(NbjetsList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Nbjets", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)


    return

######################################################################
def getNqcdNumbers():
    myDirsDict = getTailKillerDirs()

    print "*** sDataEra = ", sDataEra
    for tailKiller in myTailKillers:
        dirName  = myDirsDict[tailKiller]
        filePath =  dirName + "/info/EventYieldSummary_m120.txt"
        myFile = open(filePath, "r")

        if tailKiller == "ZeroPlus":
            tailKiller = r"\DeltaPhi_{\text{Zero+}}"
        elif tailKiller == "LoosePlus":
            tailKiller = r"\DeltaPhi_{\text{Loose+}}"
        elif tailKiller == "MediumPlus":
            tailKiller = r"\DeltaPhi_{\text{Medium+}}"
        elif tailKiller == "TightPlus":
            tailKiller = r"\DeltaPhi_{\text{Tight+}}"
        else:
            print "*** ERROR! Unexpected Tail-Killer scenario name."
            sys.exit()
            
        for line in myFile.readlines():
            if "Multijets" not in line:
                continue
            else:
                #print tailKiller + " : " + line.strip().replace("+-", "$\pm$").replace("(stat.)", "").replace("(syst.)", "").replace("Multijets:", "\NQcd = ") + "\\"
                print line.strip().replace("+-", "$\pm$").replace("(stat.)", "").replace("(syst.)", "").replace("Multijets:", r"N$^{\text{QCD}}_{%s}$ = " % (tailKiller)) + r"\\"
                print r"\vspace{0.2cm}"
    return

######################################################################
def getDataEra():

    cwd = os.getcwd()
    myDataEra = None
    
    # Check all valid data-eras
    for era in myValidDataEras:
        if "_" + era + "_" in cwd:
            myDataEra = era
        else:
            continue

    if myDataEra == None:
        print "*** ERROR: Invalid data-era selected. Please select one of the following:\n    %s" %(myValidDataEras)
        sys.exit()
    else:
        return myDataEra

######################################################################
def getLumi(myDataEra):

    # Check if user-defined data-era is allowed
    if myDataEra == "Run2011A":
        myLumi            = 2311.191 #(pb)
    elif myDataEra == "Run2011B":
        myLumi            = 2739 #(pb)
    elif myDataEra == "Run2011AB":
        myLumi            = 5050.191 #(pb)
    else:
        print "*** ERROR: Invalid data-era selected. Please select one of the following:\n    %s" %(myValidDataEras)
        sys.exit()

    return myLumi

######################################################################
def checkUserOptions(QCDscheme, ErrorType):
    
    if QCDscheme not in myQCDschemes:
        print "*** ERROR: Invalid QCD factorisation scheme selected. Please select one of the following:\n    %s" %(myQCDschemes)
        sys.exit()
        
    if ErrorType not in myErrorTypes:
        print "*** ERROR: Invalid Error-Type selected. Please select one of the following:\n    %s" %(myFactorisationSchemes)
        sys.exit()
    
    return

######################################################################
def getRootFile(myPath):

    if os.path.exists(myPath):
        print "*** Opening ROOT file:\n    \"%s\"" % (myPath)
        f = ROOT.TFile.Open(myPath)
        return f
    else:
        print "*** ERROR: The path \"%s\" defined for the ROOT file is invalid. Please check the path name." % (myPath)
        sys.exit()

######################################################################
def getHisto(rootFile, pathName):
    
    histo = rootFile.Get(pathName)
    if not isinstance(histo, ROOT.TH1):
        print "*** ERROR: Histogram \"%s\" is not a ROOT.TH1 instance. Check that its path is correct." %(pathName)
        sys.exit()
    else:
        return histo

######################################################################
def getTailKillerDirs():
    
    myDirsDict = {}
    for tailKiller in myTailKillers:
        for dirName in os.walk('.').next()[1]: 
            if ("_" + sDataEra  + "_") not in dirName:
                continue
            else:
                if tailKiller in dirName:
                    myDirsDict[tailKiller] = dirName
                    #print "*** tailKiller = %s , dirName = %s" % (tailKiller, dirName)
                else:
                    continue

    if len(myDirsDict) < 1:
        print "*** ERROR: No valid Tail-Killer directory was found in the current working directory. Check that the Tail-Killer scenarios are valid. %s" % (myTailKillers)
        sys.exit()
    else:
        return myDirsDict

######################################################################
def doHistosCompare(HistoList, myPath, QCDscheme, ErrorType, mySaveName, bNormalizeToOne, bRatio, bInvertRatio):
                
    # Check the current working directory name for a valid data-era
    myDataEra = sDataEra

    # Get the integrated luminosity of the data-era (only used for addind lumi text)
    myLumi = getLumi(myDataEra)

    # Check that the user-defined options are valid
    checkUserOptions(QCDscheme, ErrorType)

    # Get the relevant Tail-Killer directories to be read
    myDirsDict = getTailKillerDirs()

    counter = 0
    #for tailKiller in myDirsDict.keys(): #this is not used as it screws-up the ordering (dictionaries have no order)
    for tailKiller in myTailKillers:
        dirName = myDirsDict[tailKiller]
        
        print "\n*** Processing Tail-Killer scenario \"%s\"" % (tailKiller)
        rootFile = getRootFile(dirName + "/" + myPath)

        # Plot all histograms defined in the HistoList    
        print "*** There are \"%s\" histogram(s) in the plotting queue (QCDscheme = \"%s\"):" % (len(HistoList), QCDscheme)
        for h in HistoList:
            folderName = "Contraction_" + QCDscheme
            histoName  = h.name.replace("*QcdScheme*", QCDscheme).replace("*ErrorType*", ErrorType)
            # Temporary quick-fix to naming difference
            if "Shape_" in histoName:
                histoName = histoName.replace("StatAndSyst", "fullUncert").replace("StatOnly", "statUncert") 
            pathName   = folderName + "/" + histoName
            histo      = getHisto(rootFile, pathName)
            
            if mySaveName == None:
                saveName = myDataEra + "_" + histoName
                saveName = saveName.replace("/", "__")
            else:
                saveName = myDataEra + "_" + mySaveName
            saveName = saveName.replace("Leg1", "MetLeg").replace("Leg2", "TauLeg").replace("leg1", "MetLeg").replace("leg2", "TauLeg")
            xLabel   = h.xLabel
            yLabel   = h.yLabel
            xMin     = h.xMin
            xMax     = h.xMax
            logX     = h.bLogX
            yMin     = h.yMin
            yMax     = h.yMax
            logY     = h.bLogY
            legendLabel = tailKiller # = h.legendLabel

            # Create and draw the plots
            if counter == 0:
                p = createPlot(histo, myLumi, legendLabel)
                h = histograms.Histo(setHistoStyle(histo, counter), legendLabel, sLegStyle, sDrawStyle)
            else:
                h = histograms.Histo(setHistoStyle(histo, counter), legendLabel, sLegStyle, sDrawStyle)
                histograms.Histo(h, histoName, sLegStyle, sDrawStyle)
                p.histoMgr.appendHisto(h)
                                    
            # Increment counter
            counter = counter + 1
            binValue = h.getRootHisto().GetBinContent(2)
            saveFile = open("efficiencies.txt", "a")
            saveFile.write( "%s: , %s: , %s: , {%s}\n" % (sDataEra, tailKiller, mySaveName, binValue) )

    if bNormalizeToOne == True:
        p.histoMgr.forEachHisto(lambda h: dataset._normalizeToOne(h.getRootHisto()))
        yMinLog == yMinLogNorm
        saveName = saveName + "_normalizedToOne"
                    
    # Customise the plot
    if yMin == None or yMax == None:
        drawPlot = plots.PlotDrawer(log=logY, addLuminosityText=True, ratio=bRatio, ratioInvert=bInvertRatio, ratioYlabel="Ratio", opts={"ymaxfactor": yMaxFactor}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymin": yMinLog, "ymaxfactor": yMaxFactorLog})
    else:
        drawPlot = plots.PlotDrawer(log=logY, addLuminosityText=True, ratio=bRatio, ratioInvert=bInvertRatio, ratioYlabel="Ratio", opts={"ymin": yMin, "ymax": yMax}, opts2={"ymin": yMinRatio, "ymax": yMaxRatio}, optsLog={"ymin": yMin, "ymax": yMax})

    # Save the plots
    drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, customizeBeforeDraw=setLabelOption)
    print "*** Saved \"%s\"" % (saveName)

    return 

######################################################################
def setLabelOption(p):
   
    # See: http://root.cern.ch/root/htmldoc/TAxis.html#TAxis:LabelsOption
    if p.getFrame().GetXaxis().GetLabels() == None:
        return
    else:
        p.getFrame().GetXaxis().LabelsOption("u") #"h", "v" "d" "u"
        p.getFrame().GetXaxis().SetLabelSize(14.5) #"h", "v" "d" "u"
        
    return

######################################################################    
def setHistoStyle(histo, counter):

    # Since the list of supported styles/colours contains 12 entries, if counter goes out of scope it
    if counter > 11:
        counter = 0
        
    myColours = [ROOT.kRed+1, ROOT.kAzure+1, ROOT.kOrange+1, ROOT.kViolet+1, ROOT.kMagenta+1, ROOT.kGreen+3, 
                 ROOT.kRed-7, ROOT.kOrange-7, ROOT.kGreen-5, ROOT.kAzure-7,  ROOT.kViolet-7, ROOT.kMagenta-7]
    
    myMarkerStyles = [ROOT.kFullCircle, ROOT.kFullSquare, ROOT.kFullTriangleUp, ROOT.kFullTriangleDown, ROOT.kStar, ROOT.kPlus, ROOT.kCircle, 
                      ROOT.kOpenCircle, ROOT.kOpenSquare, ROOT.kOpenTriangleUp, ROOT.kOpenCross, ROOT.kDot]

    myLineStyles = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2]

    histo.SetMarkerColor(myColours[counter])
    histo.SetMarkerColor(myColours[counter])
    histo.SetMarkerStyle(myMarkerStyles[counter])
    histo.SetMarkerSize(1.2)

    histo.SetLineColor(myColours[counter])
    histo.SetLineStyle(myLineStyles[counter]);
    histo.SetLineWidth(2);

    histo.SetFillStyle(3001)
    histo.SetFillColor(myColours[counter])
    
    return histo

######################################################################
def createPlot(histo, myLumi, legendLabel, **kwargs):

    style = tdrstyle.TDRStyle()

    if isinstance(histo, ROOT.TH1):
        args = {"legendStyle": sLegStyle, "drawStyle": sDrawStyle}
        args.update(kwargs)
        histo.GetZaxis().SetTitle("")
        #p = plots.PlotBase([histograms.Histo(histo, legendLabel, **args)])
        p = plots.ComparisonManyPlot(histograms.Histo(histo, legendLabel, **args), [])
        p.setLuminosity(myLumi)
        return p
    else:
        print "*** ERROR: Histogram \"%s\" is not a valid instance of a ROOT.TH1" % (histo)
        sys.exit()

######################################################################
if __name__ == "__main__":

    # Call the main function
    main()

    # Keep session alive (otherwise canvases close automatically)
    if not bBatchMode:
        raw_input("*** DONE! Press \"ENTER\" key exit session: ")

######################################################################
