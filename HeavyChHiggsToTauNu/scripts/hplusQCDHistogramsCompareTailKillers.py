#!/usr/bin/env python

######################################################################
# All imported modules
######################################################################
# System modules
import sys
# ROOT modules
import ROOT
from ROOT import gStyle
# HPlus modules
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
# Script-specific modules
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.QCDHistoHelper as Helper

######################################################################
# User options and global definitions
######################################################################
myValidDataEras = ["Run2011A", "Run2011B", "Run2011AB"]
myTailKillers   = ["ZeroPlus", "LoosePlus", "MediumPlus", "TightPlus"]
bBatchMode      = True
bAddLumiText    = True
myDataEra       = "Run2011AB"
sLegStyle       = "P"
sDrawStyle      = "EP"
yMinRatio       = 0.0
yMaxRatio       = 2.0
yMaxFactor      = 1.5
yMinLog         = 1E-01
yMinLogNorm     = 1E-04
yMaxFactorLog   = 5

myRootFilePath  = "info/QCDMeasurementFactorisedInfo.root" 
ROOT.gROOT.SetBatch(bBatchMode)

######################################################################
# Function declarations
######################################################################
def main():
    
    ##################
    # Purity plots 
    ##################
    PurityStdSelList = Helper.GetPurityHistoNames(sMyLeg="StandardSelections")
    doHistosCompare(PurityStdSelList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Purity_StdSel", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)
    
    PurityLeg1List = Helper.GetPurityHistoNames(sMyLeg="Leg1")
    doHistosCompare(PurityLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Purity_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)
    
    PurityLeg2List = Helper.GetPurityHistoNames(sMyLeg="Leg2") #should be the same for all Tail-Killers
    doHistosCompare(PurityLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Purity_Leg2", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)


    ##################    
    # Efficiency plots 
    ##################
    EfficiencyLeg1List = Helper.GetEfficiencyHistoNames(sMyLeg="leg1") 
    doHistosCompare(EfficiencyLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Efficiency_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    #EfficiencyLeg2List = Helper.GetEfficiencyHistoNames(sMyLeg="leg2") #should be the same for all Tail-Killers
    #doHistosCompare(EfficiencyLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Efficiency_Leg2", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)


    ##################
    # mT shapes 
    ##################
    #MtShapesStdSelList = Helper.GetMtShapeHistoNames(sMyLeg="StandardSelections") #should be the same for all Tail-Killers
    #doHistosCompare(MtShapesStdSelList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShapes_StdSel", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)
    
    MtShapesLeg1List = Helper.GetMtShapeHistoNames(sMyLeg="Leg1")
    doHistosCompare(MtShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShapes_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    #MtShapesLeg2List = Helper.GetMtShapeHistoNames(sMyLeg="Leg2") #should be the same for all Tail-Killers
    #doHistosCompare(MtShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MtShapes_Leg2", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    #binList = [1] #[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #bin 0 = underflow, bin 10 = overflow
    #for index in binList:
        #MtBinShapesLeg1List   = Helper.GetMtBinShapeHistoNames(lBinList = [index], sMyLeg="Leg1")
        #doHistosCompare(MtBinShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "ClosureTest_Mt_Bin" + str(index), bNormalizeToOne = True, bRatio=False, bInvertRatio=False)


    ##################
    # MET shapes 
    ##################
    #MetShapesStdSelList = Helper.GetMetShapeHistoNames(sMyLeg="") #should be the same for all Tail-Killers
    #doHistosCompare(MetShapesStdSelList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MetShapes_StdSel", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)
    
    MetShapesLeg1List = Helper.GetMetShapeHistoNames(sMyLeg="AfterLeg1")
    doHistosCompare(MetShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MetShapes_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    #MetShapesLeg2List = Helper.GetMetShapeHistoNames(sMyLeg="AfterLeg2") #should be the same for all Tail-Killers
    #doHistosCompare(MetShapesLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MetShapes_Leg2", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    #binList = [1] #[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] #bin 0 = underflow, bin 10 = overflow
    #for index in binList:
        #MetBinShapesLeg1List   = Helper.GetMetBinShapeHistoNames(lBinList = [index], sMyLeg="Leg1")
        #doHistosCompare(MetBinShapesLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "ClosureTest_Met_Bin" + str(index), bNormalizeToOne = True, bRatio=False, bInvertRatio=False)

    ##################
    # Full mass shapes 
    ##################
    MassShapeLeg1List = Helper.GetMassShapeHistoNames(sMyLeg="Leg1")
    doHistosCompare(MassShapeLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "MassShapes_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)


    ##################
    # QCD Event Yields
    ##################
    NqcdList = Helper.GetNQcdHistoNames()
    doHistosCompare(NqcdList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "NQcd", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    
    ##################
    # Number of events
    ##################
    #NEvtsStdSelList = Helper.GetNEventsHistoNames(sMyLeg="StandardSelections") #should be the same for all Tail-Killers
    #doHistosCompare(NEvtsStdSelList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "NEvts_StdSel", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    NEvtsLeg1List = Helper.GetNEventsHistoNames(sMyLeg="Leg1")
    doHistosCompare(NEvtsLeg1List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "NEvts_Leg1", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

    #NEvtsLeg2List = Helper.GetNEventsHistoNames(sMyLeg="Leg2") 
    #doHistosCompare(NEvtsLeg2List, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "NEvts_Leg2", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)


    ##################
    # Number jets 
    ##################
    #NjetsList  = Helper.GetCtrlNjetsHistoNames() #should be the same for all Tail-Killers
    #doHistosCompare(NjetsList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Njets", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)

        
    ##################
    # Number b-jets
    ##################
    #NbjetsList  = Helper.GetCtrlNbjetsHistoNames() #should be the same for all Tail-Killers
    #doHistosCompare(NbjetsList, myRootFilePath, QCDscheme = "TauPt", ErrorType = "StatAndSyst", mySaveName = "Nbjets", bNormalizeToOne = False, bRatio=False, bInvertRatio=False)


    ##################
    # LaTeX Tables
    ##################
    getNqcdTable(fileName = "NQcd_Event_Yields.tex")

    return

######################################################################
def getNqcdTable(fileName):

    myDirsDict = Helper.getTailKillerDir(myTailKillers, myDataEra)
    outFile = open(fileName, "w")
    
    # Create the LaTeX table
    outFile.write(r"\renewcommand{\arraystretch}{1.2}" + "\n")
    outFile.write(r"\begin{table}[ht]" + "\n")
    outFile.write(r"\centering" + "\n")
    outFile.write(r"\label{tab:Purities:%s}" % (myDataEra) + "\n")
    outFile.write(r"\begin{tabular}{l c  c c c c}" + "\n")
    outFile.write(r"\\" + "\n")
    outFile.write(r"\hline" + "\n")
    outFile.write(r"Tail-Killer & Events &  & Stat. &  & Syst. \\" + "\n")
    outFile.write(r"\hline" + "\n")

    for tailKiller in myTailKillers:
        dirName  = myDirsDict[tailKiller]
        filePath =  dirName + "/info/EventYieldSummary_m120.txt"
        myFile = open(filePath, "r")
        
        for line in myFile.readlines():
            if "Multijets" not in line:
                continue
            else:
                line = line.strip().replace("+-", "$\pm$").replace("(stat.)", "").replace("(syst.)", "").replace("Multijets:", (tailKiller))
                for entry in line.split()[:-1]:
                    outFile.write(entry + r" & ")
                    
                outFile.write(line.split()[len(line.split())-1] + r" \\ " + "\n")

    # Close-up the table
    outFile.write(r"\hline" + "\n")
    outFile.write(r"\end{tabular}" + "\n")
    outFile.write(r"\end{table}" + "\n")
    outFile.write(r"\renewcommand{\arraystretch}{1.0}" + "\n")
    outFile.close()
    print "\n*** Saved LaTeX table in \"%s\"\n" % (fileName)

    return

######################################################################
def doHistosCompare(HistoList, myPath, QCDscheme, ErrorType, mySaveName, bNormalizeToOne, bRatio, bInvertRatio):
                
    # Get the integrated luminosity of the data-era (only used for addind lumi text)
    myLumi = Helper.getLumi(myDataEra)

    # Check that the user-defined options are valid
    Helper.checkUserOptions(QCDscheme, ErrorType)

    # Get the relevant Tail-Killer directories to be read
    myDirsDict = Helper.getTailKillerDir(myTailKillers, myDataEra)

    counter = 0
    #for tailKiller in myDirsDict.keys(): #this is not used as it screws-up the ordering (dictionaries have no order)
    for tailKiller in myTailKillers:

        dirName = myDirsDict[tailKiller]
        rootFile = Helper.getRootFile(dirName + "/" + myPath)

        # Plot all histograms defined in the HistoList    
        print "*** There are \"%s\" histogram(s) in the plotting queue (QCDscheme = \"%s\" , Tail-Killer = \"%s\"):" % (len(HistoList), QCDscheme, tailKiller)
        for h in HistoList:

            pathName, histoName  = Helper.getHistoNameAndPath(QCDscheme, ErrorType, h)
            histo                = Helper.getHisto(rootFile, pathName)
            saveName             = Helper.getFullSaveName(myDataEra, None, bNormalizeToOne, mySaveName)

            # Get histogram attributes as defined in QCDHistoHelper.py
            xLabel       = h.xLabel
            yLabel       = h.yLabel
            xMin         = h.xMin
            xMax         = h.xMax
            logX         = h.bLogX
            yMin         = h.yMin
            yMax         = h.yMax
            logY         = h.bLogY
            legendLabel  = tailKiller
            legendHeader = h.legendHeader
            
            # Create and draw the plots
            if counter == 0:
                print "    Creating  \"%s\" (%s)" % (histoName, tailKiller)
                p = Helper.createPlot(histo, myLumi, legendLabel, sLegStyle, sDrawStyle)
                h = histograms.Histo(Helper.setHistoStyle(histo, counter), legendLabel, sLegStyle, sDrawStyle)
            else:
                h = histograms.Histo(Helper.setHistoStyle(histo, counter), legendLabel, sLegStyle, sDrawStyle)
                histograms.Histo(h, histoName, sLegStyle, sDrawStyle)
                print "    Appending  \"%s\" (%s)" % (histoName, tailKiller)
                p.histoMgr.appendHisto(h)
                                    
            # Increment counter
            counter = counter + 1
            binValue = h.getRootHisto().GetBinContent(2)

    if bNormalizeToOne == True:
        p.histoMgr.forEachHisto(lambda h: dataset._normalizeToOne(h.getRootHisto()))
        yMinLog == yMinLogNorm

    # Customize the plots
    drawPlot = Helper.customizePlot(logY, bAddLumiText, bRatio, bInvertRatio, "Ratio", yMin, yMax, yMaxFactor, yMinRatio, yMaxRatio, yMinLog, yMaxFactorLog)

    # Save the plots
    drawPlot(p, saveName, xlabel=xLabel, ylabel=yLabel, customizeBeforeDraw=Helper.setLabelOption)
    print "*** Saved canvas as \"%s\"\n" % (saveName)

    return 

######################################################################
if __name__ == "__main__":

    main()

    if not bBatchMode:
        raw_input("*** DONE! Press \"ENTER\" key exit session: ")

######################################################################
