#! /usr/bin/env python

import os
import sys
from optparse import OptionParser

import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
#import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
from HiggsAnalysis.NtupleAnalysis.tools.ShellStyles import *

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

def getDatacardList():
    myDict = {}
    dirs = os.listdir(".")
    for d in dirs:
        if os.path.isdir(d) and d.startswith("datacards_"):
            # Find opt info
            mySplit = d.split("_")
            myOptIndex = -1
            myQCDIndex = -1
            for i in range(0, len(mySplit)):
                if myOptIndex >= 0:
                    if mySplit[i] == "QCDfact" or mySplit[i] == "QCDinv":
                        myQCDIndex = i
                if mySplit[i].startswith("opt") or mySplit[i].startswith("Opt"):
                    myOptIndex = i
            sOpt = "Nominal"
            if myOptIndex >= 0 and myQCDIndex >= 0:
                sOpt = "_".join(map(str,mySplit[myOptIndex:myQCDIndex]))
            # Store
            if not sOpt in myDict.keys():
                myDict[sOpt] = []
            myDict[sOpt].append(d)
    # sort
    for d in myDict.keys():
        myDict[d].sort()
    return myDict

def getColumns(mydir):
    myDict = {}
    myList = os.listdir(mydir)
    myList.sort()
    myFile = None
    for d in myList:
        if d.startswith("lands_datacard_") or d.startswith("combine_datacard_") and d.endswith(".txt"):
            # Read file contents
            f = open("%s/%s"%(mydir,d))
            lines = f.readlines()
            f.close()
            # Obtain headers
            myFoundStatus = False
            for l in lines:
                if not myFoundStatus and l.startswith("process"):
                    myFoundStatus = True
                    mySplit = l.replace("\n","").split(" ")
                    for i in mySplit:
                        if i != "" and i != "process":
                            myDict[i] = d
    return myDict

def printColumnDict(mydict):
    print "\nOptions for datacard column are:"
    mykeys = mydict.keys()
    mykeys.sort()
    for k in mykeys:
        print "  ",k

def getMainHistogram(filename, column):
    f = ROOT.TFile(filename.replace("datacard_","histograms_").replace(".txt",".root"),"r")
    if f == None:
        sys.exit()
    h = f.Get(column).Clone()
    h.SetDirectory(None)
    f.Close()
    if h == None:
        raise Exception("Error: cannot find histogram '%s' in file %s!"%(column, filename))
    hunc = dataset.RootHistoWithUncertainties(h)
    hunc.makeFlowBinsVisible()
    
    return hunc

def addUncertainties(filename, column, h):
    def _decypher(line):
        myList = []
        s = line.split(" ")
        for i in s:
            if i != "":
                myList.append(i.replace("\n",""))
        return myList

    # Read file contents
    f = open(filename)
    lines = f.readlines()
    f.close()
    # Obtain process index
    index = None
    myRateFoundStatus = False
    myShapeUncertList = []
    for l in lines:
        llist = _decypher(l)
        if myRateFoundStatus:
            if len(llist) > 1:
                mySystName = llist[0]
                myValue = llist[index+1]
                if llist[1].startswith("shape") and myValue == "1" and not "stat_binByBin" in llist[0]:
                    # add shape uncertainty
                    myShapeUncertList.append(mySystName)
                elif not "stat_binByBin" in llist[0] and myValue != "1" and myValue != "0" and myValue != "-":
                    # add normalization uncertainty
                    if "/" in myValue:
                        mySplit = myValue.split("/")
                        h.addNormalizationUncertaintyRelative(mySystName, float(mySplit[1])-1.0, float(mySplit[0])-1.0)
                        #raise Exception()
                    else:
                        h.addNormalizationUncertaintyRelative(mySystName, float(myValue)-1.0)

        else:
            if llist[0] == "process":
                for i in range(0,len(llist)):
                    if column == llist[i]:
                        index = i
            if llist[0] == "rate":
                myRateFoundStatus = True
    # Add shape uncertainties from list
    f = ROOT.TFile(filename.replace("datacard_","histograms_").replace(".txt",".root"),"r")
    for item in myShapeUncertList:
        hup = f.Get("%s_%sUp"%(column,item)).Clone()
        hdown = f.Get("%s_%sDown"%(column,item)).Clone()
        hup.SetDirectory(None)
        hdown.SetDirectory(None)
        h.addShapeUncertaintyFromVariation(item, hup, hdown)
    f.Close()

def getLuminosity(filename):
    # Read file contents
    f = open(filename)
    lines = f.readlines()
    f.close()
    for l in lines:
        mySplit = lines[0].split(" ")
        if mySplit[0] == "Description:":
            for i in range(0,len(mySplit)):
                if mySplit[i].startswith("luminosity="):
                    return float(mySplit[i].replace("luminosity=",""))
    return -1.0

if __name__ == "__main__":
    myStyle = tdrstyle.TDRStyle()
    myStyle.setOptStat(False)

    parser = OptionParser(usage="Usage: %prog [options]",add_help_option=False,conflict_handler="resolve")
    parser.add_option("-h", "--help", dest="helpStatus", action="store_true", default=False, help="Show this help message and exit")
    parser.add_option("-l", dest="list", action="store_true", default=False, help="List available datacards in this directory")
    parser.add_option("--refDir", dest="refDir", action="store", help="Reference datacard directory")
    parser.add_option("--testDir", dest="testDir", action="store", help="Test datacard directory to compare against reference")
    parser.add_option("--refColumn", dest="refColumn", action="store", help="Reference datacard column")
    parser.add_option("--testColumn", dest="testColumn", action="store", help="Test datacard column to compare against reference")

    (opts, args) = parser.parse_args()

    if opts.list:
        print "Available datacard directories:"
        myList = getDatacardList()
        myKeys = myList.keys()
        myKeys.sort()
        for d in myKeys:
            print "scenario %s%s%s:"%(HighlightStyle(), d, NormalStyle())
            for i in myList[d]:
                print "  ",i
            print ""
        sys.exit()

    # Check arguments
    myStatus = True
    if opts.refDir == None or opts.testDir == None:
        print "Error: Make sure you provide reference and test directories with --refDir and --testDir arguments!"
        myStatus = False
    if opts.refColumn == None and myStatus:
        print "Error: Make sure you provide reference column with --refColumn argument!"
        printColumnDict(getColumns(opts.refDir))
        myStatus = False
    if opts.testColumn == None and myStatus:
        print "Error: Make sure you provide reference column with --testColumn argument!"
        printColumnDict(getColumns(opts.testDir))
        myStatus = False

    if not myStatus or opts.helpStatus:
        print ""
        parser.print_help()
        sys.exit()

    # Check columns
    myRefColumnDict = getColumns(opts.refDir)
    if opts.refColumn not in myRefColumnDict.keys():
        print "Error: reference column '%s' not found!"%opts.refColumn
        printColumnDict(getColumns(opts.refDir))
        sys.exit()
    myTestColumnDict = getColumns(opts.testDir)
    if opts.testColumn not in myTestColumnDict.keys():
        print "Error: test column '%s' not found!"%opts.testColumn
        printColumnDict(getColumns(opts.testDir))
        sys.exit()

    # Get ref histogram
    refFile = "%s/%s"%(opts.refDir, myRefColumnDict[opts.refColumn])
    href = getMainHistogram(refFile, opts.refColumn)
    href.getRootHisto().SetLineColor(ROOT.kBlack)
    addUncertainties(refFile, opts.refColumn, href)
    refHistoName = "ref: %s %.1f"%(opts.refColumn, href.getRootHisto().Integral())
    refHistoName = refHistoName.replace("ref: EWK_Tau", "EWK+tt with #tau_{h} (data)")
    refHisto = histograms.Histo(href, refHistoName, drawStyle="HIST", legendStyle="l")
    refLumi = getLuminosity(refFile)
    # Get test histogram
    testFile = "%s/%s"%(opts.testDir, myTestColumnDict[opts.testColumn])
    htest = getMainHistogram(testFile, opts.testColumn)
    htest.getRootHisto().SetLineColor(ROOT.kRed)
    addUncertainties(testFile, opts.testColumn, htest)
    testHistoName = "ref: %s %.1f"%(opts.testColumn, htest.getRootHisto().Integral())
    testHistoName = testHistoName.replace("ref: MC_EWKTau", "EWK+tt with #tau_{h} (MC)")
    testHisto = histograms.Histo(htest, testHistoName, drawStyle="HIST", legendStyle="l")
    testLumi = getLuminosity(testFile)
    # Check lumi
    myLumiStatus = True
    if abs(testLumi-refLumi)/refLumi > 0.001:
        myLumiStatus = False
        print WarningLabel()+"Luminosities are different! ref lumi = %f pb-1, test lumi = %f pb-1"%(refLumi, testLumi)
    # Make plot
    plot = plots.ComparisonPlot(refHisto, testHisto)
    plot.setLuminosity(refLumi)
    plot.histoMgr.forEachHisto(lambda h: h.getRootHisto().SetLineWidth(3))
    myPlotName = "comparisonPlot_%s_%s"%(opts.refColumn, opts.testColumn)
    myParams = {}
    myParams["ylabel"] = "Events/#Deltam_{T}"
    myParams["xlabel"] = "Transverse mass / GeV"
    myParams["log"] = False
    myParams["opts2"] = {"ymin": 0.0, "ymax":2.0}
    myParams["opts"] = {"ymin": 0.0}
    myParams["ratio"] = True
    myParams["ratioType"] = "errorScale"
    myParams["ratioYlabel"] = "Ratio"
    myParams["divideByBinWidth"] = True,
    #myParams["cmsText"] = myCMSText
    myParams["addLuminosityText"] = myLumiStatus
#    myParams["stackMCHistograms"] = True
    #myParams["addMCUncertainty"] = True
    myParams["moveLegend"] = {"dx": -0.3}
    myParams["ratioType"] = "errorScale"
    myParams["ratioCreateLegend"] = True
    myParams["ratioMoveLegend"] = {"dx": -0.03, "dy": -0.38}
    plots.drawPlot(plot, myPlotName, **myParams)
    print "Generated plot for",myPlotName
