#!/usr/bin/env python

import sys
import os
import tarfile
from optparse import OptionParser
from datetime import date, time, datetime

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter

class HistogramInput:
    def __init__(self, histoNameList, binWidth, logStatus=True):
        # can be a list (for backward compatibility)
        if isinstance(histoNameList,list):
            self._histoNameList = histoNameList
        else:
            self._histoNameList = [histoNameList]
        self._binWidth = binWidth
        self._logStatus = logStatus

        self._mcNormalization={}

    def setMCNormalization(self, **kwargs):
        self._mcNormalization.update(**kwargs)

    def getHistoNameList(self):
        return self._histoNameList

    def getBinWidth(self):
        return self._binWidth

    def getLogStatus(self):
        return self._logStatus

    def getHistogram(self, dset, isRef):
        hname = None
        for name in self._histoNameList:
            mySplit = name.split("/")
            if dset.hasRootHisto("%s/%sInclusive"%(name,mySplit[len(mySplit)-1])):
                hname = "%s/%sInclusive"%(name,mySplit[len(mySplit)-1])
            else:
                if dset.hasRootHisto(name):
                    hname = name
        if hname == None:
            if isRef:
                print "Warning: could not open histogram '%s' in reference file %s!"%(', '.join(map(str, self._histoNameList)),dset.getName())
                return ("_".join(map(str,self._histoNameList)),None)
            else:
                print "Warning: could not open histogram '%s' in test file %s!"%(', '.join(map(str, self._histoNameList)),dset.getName())
                return ("_".join(map(str,self._histoNameList)),None)
        roothisto = dset.getDatasetRootHisto(hname)
        #roothisto.normalizeToOne()
        if dset.isMC():
            if "normalizeToLumi" in self._mcNormalization:
                roothisto.normalizeToLuminosity(self._mcNormalization["normalizeToLumi"])
            elif isinstance(dset, dataset.DatasetMerged):
                roothisto.normalizeToLuminosity(1)
        hnew = roothisto.getHistogram()
        # Rebin
        binwidth = hnew.GetXaxis().GetBinWidth(1)
        if self._binWidth > binwidth:
            hnew.Rebin(int(self._binWidth / binwidth))
        myName = "New"
        if isRef:
            myName = "Reference"
        binwidth = hnew.GetXaxis().GetBinWidth(1)
        h = ROOT.TH1F("h_"+myName,"h_"+myName, hnew.GetNbinsX()+2, hnew.GetXaxis().GetXmin() - binwidth, hnew.GetXaxis().GetXmax() + binwidth)
        # Copy bin contents
        for i in range (1, hnew.GetNbinsX()+1):
            h.SetBinContent(i+1, hnew.GetBinContent(i))
            h.SetBinError(i+1, hnew.GetBinError(i))
            if hnew.GetXaxis().GetBinLabel(i) <> "":
                h.GetXaxis().SetBinLabel(i+1, hnew.GetXaxis().GetBinLabel(i))
        # Set under/overflow bins
        h.SetBinContent(1, hnew.GetBinContent(0))
        h.SetBinError(1, hnew.GetBinError(0))
        h.SetBinContent(h.GetNbinsX(), hnew.GetBinContent(hnew.GetNbinsX()+1))
        h.SetBinError(h.GetNbinsX(), hnew.GetBinError(hnew.GetNbinsX()+1))
        # Set attributes
        h.SetEntries(hnew.GetEntries())
        h.SetTitle(hnew.GetTitle())
        h.SetXTitle(hnew.GetXaxis().GetTitle())
        h.SetYTitle(hnew.GetYaxis().GetTitle())
        h.SetStats(1)
        h.SetName(myName)
        # Set style
        if isRef:
            h.SetFillStyle(1001)
            h.SetFillColor(ROOT.kBlue-6)
            h.SetLineColor(ROOT.kBlue-6)
            #statbox.SetTextColor(ROOT.kBlue-6)
        else:
            h.SetMarkerColor(ROOT.kBlack)
            h.SetLineColor(ROOT.kBlack)
            h.SetMarkerStyle(20)
            h.SetMarkerSize(1.0)
            #statbox.SetTextColor(ROOT.kBlack)
        return (hname,h)

# Groups histograms and counters around a theme; a separate page is created for each group
class ValidateGroup:
    def __init__(self, groupName):
        self._groupName = groupName
        self._output = ""
        self._myDifference = 0.0
        self._counters = [] # list of count names (strings), main counters = "main"
        self._readCounterCount = 0
        self._histograms = [] # list of HistogramInputs
        self._yellowWarnings = []
        self._redWarnings = []

        self._mcNormalization = {}

    def addCounter(self, counterName):
        self._counters.append(counterName)

    def addHistogram(self, histoName, binWidth, logStatus):
        self._histograms.append(HistogramInput(histoName, binWidth, logStatus))

    def setMCNormalization(self, **kwargs):
        self._mcNormalization.update(kwargs)
        for h in self._histograms:
            h.setMCNormalization(**kwargs)

    def getName(self):
        return self._groupName

    def getOutput(self):
        return self._output

    def getDifference(self):
        return self._myDifference

    def getItemCount(self):
        return len(self._counters)+len(self._histograms)

    def getReadCounterCount(self):
        return self._readCounterCount

    def getReadHistogramCount(self):
        return len(self._histograms)

    def getRedWarnings(self):
        return self._redWarnings

    def getYellowWarnings(self):
        return self._yellowWarnings

    def doValidate(self, mydir, refDataset, testDataset):
        if not os.path.exists(mydir):
            os.mkdir(mydir)
        #myOutput = "<br><a href=#maintop>Back to datasets</a>\n"
        # validate counters
        self._myDifference = 0.0
        myOutput = "<a name=mytop></a>"
        #print "Generating validation counters"
        self._readCounterCount = 0

        mcNormalization = ""
        if refDataset.isMC() or testDataset.isMC():
            if "normalizeToLumi" in self._mcNormalization:
                mcNormalization = "MC is normalized to %s fb<sup>-1</sup><br>\n" % histograms.formatLuminosityInFb(self._mcNormalization["normalizeToLumi"])

        if len(self._counters) > 0:
            myOutput += "<h1>Counters for validation:</h1><br>\n%s" % mcNormalization
            myOutput += self._doValidateCounters(refDataset, testDataset)
            myOutput += '<a href="#mytop">Back to top</a><br>\n'
        # validate histograms
        #print "Generating validation histograms"
        if len(self._histograms) > 0:
            myOutput += "<h1>Histograms for validation:</h1><br>\n"
            myOutput += "Note: the underflow (overflow) bin is shown as the first (last) bin in the histogram<br>\n"
            myOutput += "Color legend: blue histogram = reference, red points = dataset to be validated<br>\n"
            myOutput += "Difference is defined as sum_i (abs(new_i / ref_i - 1.0)), where sum goes over the histogram bins<br>%s<br>\n" % mcNormalization
            myOutput += self._doValidateHistograms(mydir, refDataset, testDataset)
            myOutput += '<a href="#mytop">Back to top</a><br>\n'
        # make html
        self._output = myOutput
        #makehtml(mydir,"index.html",myOutput+myCounterOutput+myHistoOutput)
        #print "Histograms done for dataset",refDataset.getName()
        #print "Legend: blue histogram = reference, red points = dataset to be validated\n"

    ### Counter based validation methods ------------------------------------------------

    def _doValidateCounters(self, refDataset, testDataset):
        myOutput = ""
        # Get event counters
        refEventCounter = counter.EventCounter(refDataset)
        testEventCounter = counter.EventCounter(testDataset)
        if isinstance(refDataset, dataset.DatasetMerged) or isinstance(testDataset, dataset.DatasetMerged):
            refEventCounter.normalizeMCToLuminosity(self._mcNormalization["normalizeToLumi"])
            testEventCounter.normalizeMCToLuminosity(self._mcNormalization["normalizeToLumi"])
        mcNormalization = ""
        for ds, ec in [(refDataset, refEventCounter), (testDataset, testEventCounter)]:
            if ds.isMC():
                if "normalizeToLumi" in self._mcNormalization:
                    ec.normalizeMCToLuminosity(self._mcNormalization["normalizeToLumi"])

        # Get sub counter names
        refSubCounterNames = refEventCounter.getSubCounterNames()
        testSubCounterNames = testEventCounter.getSubCounterNames()
        # Loop over requested counter names
        for counterName in self._counters:
            #print ".. analyzing counter",counterName
            if counterName == "main":
                myOutput += "<br>\n<b>Main counters</b><br>\n<br>\n"
                refCounter = refEventCounter.getMainCounter().getTable()
                testCounter = testEventCounter.getMainCounter().getTable()
                myOutput += self._validateCounterValues(refCounter,testCounter)
            else:
                myOutput += "<br>\n<b>Subcounters: %s</b><br>\n<br>\n"%(counterName)
                itemFoundStatus = False
                for item in refSubCounterNames:
                    if item == counterName:
                        itemFoundStatus = True
                        refCounter = refEventCounter.getSubCounterTable(item)
                        if item in testSubCounterNames:
                            testCounter = testEventCounter.getSubCounterTable(item)
                            myOutput += self._validateCounterValues(refCounter, testCounter)
                        else:
                            myOutput += self._validateCounterValues(refCounter, None)
                # If item was not found in reference dataset, then look only at test dataset
                if not itemFoundStatus:
                    for item in testSubCounterNames:
                        if item == counterName:
                            itemFoundStatus = True
                            testCounter = testEventCounter.getSubCounterTable(item)
                            myOutput += self._validateCounterValues(None, testCounter)
                # Report items that were not found
                if not itemFoundStatus:
                    print "      counter %s not found!"%counterName
                    print "      Full counter list: main, %s"%(", ".join(map(str,refSubCounterNames)))
                    myOutput += "<b>Not found! Check name.</b><br>\n"
            if "#b00000" in myOutput:
                self._redWarnings = "Mismatch in counter group <b>%s</b><br>\n"%counterName
            elif "#b0b000" in myOutput:
                self._yellowWarnings = "Minor mismatch in counter group <b>%s</b><br>\n"%counterName
        return myOutput

    def _validateCounterValues(self, refCounter, testCounter):
        # Make table in output
        myOutput = "<table>\n"
        myOutput += "<tr><td><b>Counter</b></td>"
        myOutput += "<td><b>New counts</b></td><td><b>Ref. counts</b></td><td><b>New/Ref.</b></td>"
        myOutput += "<td><b>New eff.</b></td><td><b>Ref. eff.</b></td><td><b>New/Ref.</b></td>"
        myOutput += "</tr>\n"
        oldrow = ""
        # This handles nonexisting rows correctly
        table = counter.CounterTable()
        if refCounter is not None:
            c = refCounter.getColumn(index=0)
            c.setName("Ref")
            table.appendColumn(c)
        if testCounter is not None:
            c = testCounter.getColumn(index=0)
            c.setName("Test")
            table.appendColumn(c)

        for row in table.getRowNames():
            myOutput += self._testCounterValues(oldrow, row, refCounter, testCounter)
            oldrow = row
        self._readCounterCount += table.getNrows()
        myOutput += "</table>\n"
        return myOutput

    def _testCounterValues(self, oldrow, row, refCounter, testCounter):
        # obtain event counts
        value1 = self._findValue(row,refCounter)
        value2 = self._findValue(row,testCounter)
        myOutput = "<tr>\n"
        myOutput += "<td><b>"+row+"</b></td>"
        if value2 >= 0:
            myOutput += "<td align=center>"+str(value2)+"</td>"
        else:
            myOutput += "<td align=center>-</td>"
        if value1 >= 0:
            myOutput += "<td align=center>"+str(value1)+"</td>"
        else:
            myOutput += "<td align=center>-</td>"
        if value1 == value2 and value1 > 0:
            myOutput += "<td bgcolor=#00b000>&nbsp;</td>"
        else:
            myratio = -1;
            if value1 > 0:
                myratio = float(value2) / float(value1)
                self._myDifference += abs(myratio-1.0)
            myOutput += self._getCounterAgreementColor(myratio)
        # obtain efficiencies
        oldvalue1 = 0
        oldvalue2 = 0
        eff1 = 0
        eff2 = 0
        if not oldrow == "":
            oldvalue1 = self._findValue(oldrow,refCounter)
            oldvalue2 = self._findValue(oldrow,testCounter)
        if oldvalue1 > 0:
            eff1 = float(value1) / float(oldvalue1)
        if oldvalue2 > 0:
            eff2 = float(value2) / float(oldvalue2)
        myratio = -1.0;
        if eff1 > 0:
            myratio = eff2 / eff1
        if eff2 > 0:
            myOutput += "<td align=center>%1.5f</td>" % eff2
        else:
            myOutput += "<td align=center>-</td>"
        if eff1 > 0:
            myOutput += "<td align=center>%1.5f</td>" % eff1
        else:
            myOutput += "<td align=center>-</td>"
        myOutput += self._getCounterAgreementColor(myratio)

        myOutput += "</tr>\n"
        return myOutput

    def _findValue(self, row, counter):
        if counter == None:
            return -1
        for i in xrange(counter.getNrows()):
            if row == counter.rowNames[i]:
                return int(counter.getCount(i,0).value())
        #print "Counter value not found"
        return -1

    def _getCounterAgreementColor(self, ratio):
        myOutput = ""
        if abs(ratio+1) < 0.0001:
            myOutput += "<td align=center bgcolor=#00b000>-</td>"
        elif abs(ratio-1) < 0.0001:
            myOutput += "<td bgcolor=#00b000>&nbsp</td>"
        elif abs(ratio-1) < 0.01:
            myOutput += "<td align=center bgcolor=#00b000>%1.5f</td>" % ratio
        elif abs(ratio-1) < 0.03:
            myOutput += "<td align=center bgcolor=#b0b000>%1.5f</td>" % ratio
        else:
            myOutput += "<td align=center bgcolor=#b00000>%1.5f</td>" % ratio
        return myOutput

    ### Histogram based validation methods ------------------------------------------------

    def _doValidateHistograms(self, mydir, refDataset, testDataset):
        mycolumns = 2
        myscale = 200.0 / float(mycolumns)
        myOutput = ""
        # histograms
        myindexcount = 0
        mycount = 0
        myOutput += "<table>\n"
        for h in self._histograms:
            # Obtain histograms
            #print "Obtaining histogram histogram %s"% ', '.join(map(str, h.getHistoNameList()))
            (hrefname, hRef) = h.getHistogram(refDataset, True)
            (htestname, hTest) = h.getHistogram(testDataset, False)
            if hRef == None or hTest == None:
                continue
            # Histograms exist
            myindexcount += 1
            if mycount == 0:
                myOutput += "<tr>\n"
            mycount += 1
            myOutput += "<td>"
            # construct output name
            myname = hrefname.replace("/", "_")
            # make canvas
            mydifference = self._makePlot(mydir, myname, hRef, hTest, h.getLogStatus())
            self._myDifference += abs(mydifference)
            # Make output
            myOutput += "<hr><h3>%s</h3><br>\n"%(myname)
            myOutput += "<br><img"
            #myOutput += " width=%f%%" % myscale
            #myOutput += " height=%f%%" % myscale
            myOutput += " src=%s.png alt=%s><br>"%(myname,myname)
            myOutput += "\n<br>src = %s"%(", ".join(map(str, h.getHistoNameList())))
            myOutput += "<br>bin width = "+str(h.getBinWidth())
            myOutput += "<br>Difference = %1.3f\n" % mydifference
            myOutput += "</td>\n"
            # close cell (and if necessary also row) in table
            if mycount == mycolumns:
                myOutput += "</tr>\n"
                mycount = 0
        # close if necessary row in table
        if mycount > 0:
            myOutput += "</tr>\n"
        myOutput += "</table>\n"
        return myOutput

    def _makePlot(self, mydir, histoName, hRef, hTest, logStatus):
        # Create canvas
        canvas = ROOT.TCanvas(histoName, histoName, 600, 500)
        canvas.cd()
        self._setCanvasDefinitions(canvas)
        # Make frame and set its extrema
        myframe = hRef.Clone("hclone")
        myframe.SetBinContent(1,0)
        myframe.SetStats(0)
        myframe.SetXTitle("")
        myframe.GetXaxis().SetLabelSize(0)
        myframe.SetTitleSize(0.06, "Y")
        myframe.SetLabelSize(0.05, "Y")
        myframe.GetYaxis().SetTitleOffset(0.75)
        self._setFrameExtrema(myframe,hRef,hTest,logStatus)
        # Make agreement histograms
        hdiff = hTest.Clone("hdiffclone")
        hdiff.SetStats(0)
        hdiff.Divide(hRef)
        hdiffWarn = hdiff.Clone("hdiffwarn")
        hdiffWarn.SetLineColor(ROOT.kOrange)
        hdiffWarn.SetFillColor(ROOT.kOrange)
        hdiffWarn.SetMarkerColor(ROOT.kOrange)
        hdiffError = hdiff.Clone("hdifferror")
        hdiffError.SetLineColor(ROOT.kRed+1)
        hdiffError.SetFillColor(ROOT.kRed+1)
        hdiffError.SetMarkerColor(ROOT.kRed+1)
        for i in range(1, hdiff.GetNbinsX()+1):
            if hdiff.GetBinContent(i) > 0 and abs(hdiff.GetBinContent(i) - 1) > 0.03:
                hdiffError.SetBinContent(i, hdiff.GetBinContent(i))
                hdiffError.SetBinError(i, hdiff.GetBinError(i))
                hdiff.SetBinContent(i, -100)
                hdiffWarn.SetBinContent(i, -100)
            elif hdiff.GetBinContent(i) > 0 and abs(hdiff.GetBinContent(i) - 1) > 0.01:
                hdiffWarn.SetBinContent(i, hdiff.GetBinContent(i))
                hdiffWarn.SetBinError(i, hdiff.GetBinError(i))
                hdiff.SetBinContent(i, -100)
        # Line at zero
        hdiffLine = hRef.Clone("hdifflineclone")
        hdiffLine.SetLineColor(ROOT.kGray)
        for i in range(1, hdiff.GetNbinsX()+1):
            hdiffLine.SetBinContent(i,1)
            hdiffLine.SetBinError(i,0)
        hdiffLine.SetLineWidth(1)
        hdiffLine.SetFillStyle(0)
        hdiffLine.SetMaximum(2)
        hdiffLine.SetMinimum(0)
        hdiffLine.SetTitle("")
        hdiffLine.SetStats(0)
        hdiffLine.SetTitleSize(0.05 / 0.3 * 0.7, "XYZ")
        hdiffLine.SetLabelSize(0.05 / 0.3 * 0.7, "XYZ")
        hdiffLine.SetNdivisions(505, "Y")
        hdiffLine.GetXaxis().SetTitleOffset(1.1)
        hdiffLine.GetYaxis().SetTitleOffset(0.4)
        hdiffLine.SetXTitle(hRef.GetXaxis().GetTitle())
        hdiffLine.SetYTitle("New/Ref.")
        # Analyse agreement
        mydifference = self._analyseHistoDiff(canvas, hRef, hTest)
        # Plot pad
        canvas.cd(1)
        if logStatus == "log":
            canvas.GetPad(1).SetLogy()
        myframe.Draw()
        hRef.Draw("histo sames")
        hTest.Draw("e1 sames")
        canvas.GetPad(1).RedrawAxis()
        # Modify stat boxes
        canvas.GetPad(1).Update()
        hRef.FindObject("stats").SetLineColor(ROOT.kBlue-6)
        hRef.FindObject("stats").SetTextColor(ROOT.kBlue-6)
        hRef.FindObject("stats").Draw()
        hTest.FindObject("stats").SetY1NDC(0.615)
        hTest.FindObject("stats").SetY2NDC(0.775)
        hTest.FindObject("stats").Draw()
        canvas.GetPad(1).Modified()
        #canvas.GetPad(1).Update()
        # Difference pad
        canvas.cd(2)
        hdiffLine.Draw()
        hdiffError.Draw("e same")
        hdiffWarn.Draw("e same")
        hdiff.Draw("e same")
        canvas.GetPad(2).RedrawAxis()
        canvas.GetPad(2).Modified()
        # Save plot
        canvas.Modified()
        canvas.Print(mydir+"/"+histoName+".png")
        canvas.Close()
        # Return difference
        return mydifference

    def _analyseHistoDiff(self, canvas, hRef, hTest):
        canvas.GetPad(1).SetFrameFillColor(4000)
        canvas.GetPad(2).SetFrameFillColor(4000)
        diff = 0.0
        if not hRef.GetNbinsX() == hTest.GetNbinsX():
            canvas.GetPad(1).SetFillColor(ROOT.kOrange)
            canvas.GetPad(2).SetFillColor(ROOT.kOrange)
        else:
            # same number of bins in histograms
            zerocount = 0
            for i in range(1, hRef.GetNbinsX()):
                if hRef.GetBinContent(i) > 0:
                    diff += abs(hTest.GetBinContent(i) / hRef.GetBinContent(i) - 1.0)
                elif hTest.GetBinContent(i) > 0:
                    zerocount = zerocount + 1
            if (diff > 0.03 or zerocount > 3):
                canvas.GetPad(1).SetFillColor(ROOT.kRed+1)
                canvas.GetPad(2).SetFillColor(ROOT.kRed+1)
            elif (diff > 0.01 or zerocount > 1):
                canvas.GetPad(1).SetFillColor(ROOT.kOrange)
                canvas.GetPad(2).SetFillColor(ROOT.kOrange)
        return diff

    def _setCanvasDefinitions(self, canvas):
        canvas.Range(0,0,1,1)
        canvas.SetFrameFillColor(ROOT.TColor.GetColor("#fdffff"))
        canvas.SetFrameFillStyle(1001)
        canvas.Divide(2,1)
        canvas.GetPad(1).SetPad(0,0.3,1.,1.)
        canvas.GetPad(2).SetPad(0,0.0,1.,0.3)
        # agreement pad
        pad = canvas.GetPad(2)
        #pad.SetFillStyle(4000);
        pad.SetBorderMode(0);
        pad.SetBorderSize(2);
        pad.SetTickx(1);
        pad.SetTicky(1);
        pad.SetLeftMargin(0.10);
        pad.SetRightMargin(0.05);
        pad.SetTopMargin(0);
        pad.SetBottomMargin(0.34);
        # plot pad
        myplotpad = canvas.GetPad(1)
        myplotpad = canvas.GetPad(1)
        myplotpad.SetTickx(1)
        myplotpad.SetTicky(1)
        myplotpad.SetLeftMargin(0.10)
        myplotpad.SetRightMargin(0.05)
        myplotpad.SetTopMargin(0.065)
        myplotpad.SetBottomMargin(0.0)

    def _setFrameExtrema(self, myframe, h1, h2, logstatus):
        # obtain and set x range
        xmin = h1.GetXaxis().GetXmin()
        if h2.GetXaxis().GetXmin() > h1.GetXaxis().GetXmin():
            xmin = h2.GetXaxis().GetXmin()
        xmax = h1.GetXaxis().GetXmax()
        if h2.GetXaxis().GetXmax() > h1.GetXaxis().GetXmax():
            xmax = h2.GetXaxis().GetXmax()
        myframe.GetXaxis().Set(1, xmin, xmax)
        # obtain and set minimum y value
        ymin = 0.0
        if logstatus == "log":
            ymin = 1.5
            for i in range(1, h1.GetNbinsX()):
                if h1.GetBinContent(i) > 0 and h1.GetBinContent(i) < ymin:
                    ymin = h1.GetBinContent(i)
            for i in range(1, h2.GetNbinsX()):
                if h2.GetBinContent(i) > 0 and h2.GetBinContent(i) < ymin:
                    ymin = h2.GetBinContent(i)
            if ymin > 1:
                ymin = 1.5
        myscalefactor = 1.1
        if logstatus == "log":
            myscalefactor = 1.5
            myframe.SetMinimum(ymin / myscalefactor)
        else:
            myframe.SetMinimum(ymin)
        # obtain and set maximum y value
        ymax = h1.GetMaximum()
        if h2.GetMaximum() > h1.GetMaximum():
            ymax = h2.GetMaximum()
        myframe.SetMaximum(ymax*myscalefactor)

# Class for containing frame information
class NavigationPanel:
    def __init__(self, timeStamp):
        self._timestamp = timeStamp
        self._era = None
        self._searchMode = None
        self._variation = None
        self._dataset = None
        self._datasetTest = None
        self._colorPanelHeader = '"#000060"'
        self._colorPanelFontHeader = '"#f0f0f0"'
        self._colorPanelContent = '"#6666cc"' #a0a0a0
        self._colorInfoContent = '"#d0d0d0"'
        self._colorPanelFontContent = '"#000000"'
        self._colorPanelMajorDifference = '"#b00000"'
        self._colorPanelOkDifference = '"#00b000"'

    def setTimestamp(self, t):
        self._timestamp = t

    def setModule(self, era, searchMode, variation):
        self._era = era
        self._searchMode = searchMode
        self._variation = variation

    def setDataset(self, dataset, datasetTest=None):
        self._dataset = dataset
        self._datasetTest = datasetTest

    def makehtml(self, groups, groupOutput, mydir, myname):
        # Table
        myOutput = "<table border=0 cellpadding=4>\n"
        myOutput += '<tr valign="top">\n'
        myOutput += '<td bgcolor=%s>\n'%self._colorPanelContent
        myOutput += self._generatePanel(groups)
        myOutput += "</td>\n"
        myOutput += '<td bgcolor=%s>\n'%self._colorInfoContent
        myOutput += groupOutput
        myOutput += "</td>\n"
        myOutput += "</tr>\n"
        myOutput += "</table>\n"
        makehtml(mydir,myname,myOutput)

    def _generatePanel(self, groups):
        myOutput = "<table border=0 cellpadding=2>\n"
        # Title
        myOutput += self._generatePanelHeaderCell("")
        myOutput += self._generatePanelHeaderCell("<h2>H+ Validation Suite</h2>")
        myOutput += self._generatePanelHeaderCell("")
        # Link
        myOutput += self._generatePanelContentCell('<a href="../../index.html">Select dataset/module</a>')
        # Header
        myOutput += self._generatePanelHeaderCell("Time stamp")
        myOutput += self._generatePanelContentCell(self._timestamp)
        myOutput += self._generatePanelHeaderCell("Dataset")
        if self._dataset == self._datasetTest:
            myOutput += self._generatePanelContentCell(self._dataset)
        else:
            myOutput += self._generatePanelContentCell("%s vs. <br/> %s" % (self._dataset, self._datasetTest))
        myOutput += self._generatePanelHeaderCell("Data Era")
        myOutput += self._generatePanelContentCell(self._era)
        myOutput += self._generatePanelHeaderCell("Search Mode")
        myOutput += self._generatePanelContentCell(self._searchMode)
        myOutput += self._generatePanelHeaderCell("Variation")
        myOutput += self._generatePanelContentCell(self._variation)
        # Groups
        myOutput += self._generatePanelHeaderCell("Selection groups")
        for g in groups:
            myOutput += '<tr>'
            if g.getDifference() > 0.03:
                myOutput += '<td bgcolor=%s>'%self._colorPanelMajorDifference
            else:
                myOutput += '<td bgcolor=%s>'%self._colorPanelOkDifference
            myOutput += '<b><a href="%s.html">%s</a></b></td>'%(g.getName().replace(" ","_"),g.getName())
            #myOutput += 'Delta=%.2f</td></tr>\n'%(g.getDifference())
            myOutput += '</tr>\n'
        # End of table
        myOutput += self._generatePanelContentCell("&nbsp;")
        myOutput += "</table>\n"
        return myOutput

    def _generatePanelHeaderCell(self, title):
        myOutput = '<tr><td bgcolor=%s><font color=%s>'%(self._colorPanelHeader,self._colorPanelFontHeader)
        myOutput += "<b>%s</b>"%title
        myOutput += "</font></td></tr>\n"
        return myOutput

    def _generatePanelContentCell(self, entry):
        myOutput = '<tr><td bgcolor=%s><font color=%s>'%(self._colorPanelContent,self._colorPanelFontContent)
        if entry == None:
            myOutput += "<b>(None)</b>"
        else:
            myOutput += "<b>%s</b>"%(entry)
        myOutput += "</font></td></tr>\n"
        return myOutput

def addCommonPlotsAtEveryStep(commonPlotGroups,commonPlotItem,binWidth,options):
    myGroup = ValidateGroup("CommonPlots_everystep_%s"%commonPlotItem)
    for group in commonPlotGroups:
        myGroup.addHistogram("CommonPlots/AtEveryStep/%s/%s"%(group,commonPlotItem), binWidth, options)
    return myGroup

def createValidateHistograms():
    # entry syntax: histogram_name_with_path, bin_width, linear/log
    myGroups = []

    myGroup = ValidateGroup("Main counters")
    myGroup.addCounter("main")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("MET filters")
    myGroup.addCounter("METFilters")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Primary vertices")
    myGroup.addHistogram("Vertices/verticesBeforeWeight", 1, "log")
    myGroup.addHistogram("Vertices/verticesAfterWeight", 1, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Trigger matched tau collection")
    myGroup.addCounter("Trigger")
    myGroup.addCounter("Trigger debug")
    myGroup.addHistogram(["tauID/N_TriggerMatchedTaus","TauSelection/N_TriggerMatchedTaus"], 1, "log")
    myGroup.addHistogram(["tauID/N_TriggerMatchedSeparateTaus","TauSelection/N_TriggerMatchedSeparateTaus"], 1, "log")
    myGroup.addHistogram(["tauID/HPSDecayMode","TauSelection/TauCand_DecayModeFinding"], 1, "log")
    myGroup.addHistogram(["tauID/TauSelection_all_tau_candidates_N","TauSelection/TauSelection_all_tau_candidates_N"], 1, "log")
    myGroup.addHistogram(["tauID/TauSelection_all_tau_candidates_pt","TauSelection/TauSelection_all_tau_candidates_pt"], 5, "log")
    myGroup.addHistogram(["tauID/TauSelection_all_tau_candidates_eta","TauSelection/TauSelection_all_tau_candidates_eta"], 0.1, "log")
    myGroup.addHistogram(["tauID/TauSelection_all_tau_candidates_phi","TauSelection/TauSelection_all_tau_candidates_phi"], 3.14159265 / 36, "log")
    myGroup.addHistogram(["tauID/TauSelection_all_tau_candidates_MC_purity","TauSelection/TauSelection_all_tau_candidates_MC_purity"], 1, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Tau candidate selection")
    myGroup.addHistogram(["tauID/TauCand_JetPt","TauSelection/TauCand_JetPt"], 5, "log")
    myGroup.addHistogram(["tauID/TauCand_JetEta","TauSelection/TauCand_JetEta"], 0.1, "log")
    myGroup.addHistogram(["tauID/TauCand_LdgTrackPtCut","TauSelection/TauCand_LdgTrackPtCut"], 5, "log")
    myGroup.addHistogram(["tauID/TauSelection_cleaned_tau_candidates_N","TauSelection/TauSelection_cleaned_tau_candidates_N"], 1, "log")
    myGroup.addHistogram(["tauID/TauSelection_cleaned_tau_candidates_pt","TauSelection/TauSelection_cleaned_tau_candidates_pt"], 5, "log")
    myGroup.addHistogram(["tauID/TauSelection_cleaned_tau_candidates_eta","TauSelection/TauSelection_cleaned_tau_candidates_eta"], 0.1, "log")
    myGroup.addHistogram(["tauID/TauSelection_cleaned_tau_candidates_phi","TauSelection/TauSelection_cleaned_tau_candidates_phi"], 3.14159265 / 36, "log")
    myGroup.addHistogram(["tauID/TauSelection_cleaned_tau_candidates_MC_purity","TauSelection/TauSelection_cleaned_tau_candidates_MC_purity"], 1, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Tau ID")
    myGroup.addCounter("TauIDPassedJets::TauSelection_HPS")
    myGroup.addCounter("TauIDPassedEvt::TauSelection_HPS")
    myGroup.addHistogram(["tauID/IsolationPFChargedHadrCandsPtSum","TauSelection/IsolationPFChargedHadrCandsPtSum"], 1, "log")
    myGroup.addHistogram(["tauID/IsolationPFGammaCandEtSum","TauSelection/IsolationPFGammaCandEtSum"], 1, "log")
    myGroup.addHistogram(["tauID/TauID_OneProngNumberCut","TauSelection/TauID_NProngsCut"], 1, "log")
    myGroup.addHistogram(["tauID/TauID_RtauCut","TauSelection/TauID_RtauCut"], 0.05, "log")
    myGroup.addHistogram(["tauID/TauSelection_selected_taus_N","TauSelection/TauSelection_selected_taus_N"], 1, "log")
    myGroup.addHistogram(["tauID/TauSelection_selected_taus_pt","TauSelection/TauSelection_selected_taus_pt"], 5, "log")
    myGroup.addHistogram(["tauID/TauSelection_selected_taus_eta","TauSelection/TauSelection_selected_taus_eta"], 0.1, "log")
    myGroup.addHistogram(["tauID/TauSelection_selected_taus_phi","TauSelection/TauSelection_selected_taus_phi"], 3.14159265 / 36, "log")
    myGroup.addHistogram(["tauID/TauSelection_selected_taus_MC_purity","TauSelection/TauSelection_selected_taus_MC_purity"], 1, "log")
    myGroup.addHistogram(["FakeTauIdentifier/TauMatchType","FakeTauIdentifier_TauID/TauMatchType"], 1, "log")
    myGroup.addHistogram(["FakeTauIdentifier/TauOrigin","FakeTauIdentifier_TauID/TauOrigin"], 1, "log")
    myGroup.addHistogram(["FakeTauIdentifier/MuOrigin","FakeTauIdentifier_TauID/MuOrigin"], 1, "log")
    myGroup.addHistogram(["FakeTauIdentifier/ElectronOrigin","FakeTauIdentifier_TauID/ElectronOrigin"], 1, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Tau after tau ID")
    myGroup.addHistogram("SelectedTau/SelectedTau_pT_AfterTauID", 5, "log")
    myGroup.addHistogram("SelectedTau/SelectedTau_eta_AfterTauID", 0.1, "log")
    myGroup.addHistogram("SelectedTau/SelectedTau_phi_AfterTauID", 3.14159265 / 36, "log")
    myGroup.addHistogram("SelectedTau/SelectedTau_Rtau_AfterTauID", 0.05, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Tau after all cuts")
    myGroup.addHistogram("SelectedTau/SelectedTau_pT_AfterCuts", 10, "log")
    myGroup.addHistogram("SelectedTau/SelectedTau_eta_AfterCuts", 0.2, "log")
    myGroup.addHistogram("SelectedTau/SelectedTau_Rtau_AfterCuts", 0.05, "log")
    #            myGroup.addHistogram("SelectedTau/NonQCDTypeII_SelectedTau_pT_AfterCuts","SelectedTau/NonQCDTypeII_SelectedTau_pT_AfterCuts"], 10, "log")
    #            myGroup.addHistogram("SelectedTau/NonQCDTypeII_SelectedTau_eta_AfterCuts","SelectedTau/NonQCDTypeII_SelectedTau_eta_AfterCuts"], 0.2, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Veto tau selection")
    myGroup.addCounter("VetoTauSelection")
    myGroup.addCounter("TauIDPassedJets::TauVeto_HPS")
    myGroup.addCounter("TauIDPassedEvt::TauVeto_HPS")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Electrons")
    myGroup.addCounter("ElectronSelection")
    myGroup.addHistogram("ElectronSelection/ElectronPt_all", 5, "log")
    myGroup.addHistogram("ElectronSelection/ElectronEta_all", 0.1, "log")
    myGroup.addHistogram("ElectronSelection/ElectronPt_veto", 5, "log")
    myGroup.addHistogram("ElectronSelection/ElectronEta_veto", 0.1, "log")
    myGroup.addHistogram("ElectronSelection/NumberOfVetoElectrons", 1, "log")
    myGroup.addHistogram("ElectronSelection/ElectronPt_medium", 5, "log")
    myGroup.addHistogram("ElectronSelection/ElectronEta_medium", 0.1, "log")
    myGroup.addHistogram("ElectronSelection/NumberOfMediumElectrons", 1, "log")
    myGroup.addHistogram("ElectronSelection/ElectronPt_tight", 5, "log")
    myGroup.addHistogram("ElectronSelection/ElectronEta_tight", 0.1, "log")
    myGroup.addHistogram("ElectronSelection/NumberOfTightElectrons", 1, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Muons")
    myGroup.addCounter("MuonSelection")
    myGroup.addHistogram("MuonSelection/LooseMuonPt", 5, "log")
    myGroup.addHistogram("MuonSelection/LooseMuonEta", 0.1, "log")
    myGroup.addHistogram("MuonSelection/NumberOfLooseMuons", 1, "log")
    myGroup.addHistogram("MuonSelection/TightMuonPt", 5, "log")
    myGroup.addHistogram("MuonSelection/TightMuonEta", 0.1, "log")
    myGroup.addHistogram("MuonSelection/NumberOfTightMuons", 1, "log")
    myGroup.addHistogram("MuonSelection/MuonTransverseImpactParameter", 0.02, "log")
    myGroup.addHistogram("MuonSelection/MuonDeltaIPz", 1, "log")
    myGroup.addHistogram("MuonSelection/MuonRelIsol", 0.1, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("All jets")
    myGroup.addCounter("Jet main")
    myGroup.addCounter("Jet selection")
    myGroup.addHistogram("JetSelection/jet_pt", 10, "log")
    myGroup.addHistogram("JetSelection/jet_pt_central", 5, "log")
    myGroup.addHistogram("JetSelection/jet_eta", 0.2, "log")
    myGroup.addHistogram("JetSelection/jet_phi", 3.14159265 / 36, "log")
    myGroup.addHistogram("JetSelection/jetEMFraction", 0.05, "log")
    myGroup.addHistogram("JetSelection/firstJet_pt", 10, "log")
    myGroup.addHistogram("JetSelection/firstJet_eta", 0.2, "log")
    myGroup.addHistogram("JetSelection/firstJet_phi", 3.14159265 / 36, "log")
    myGroup.addHistogram("JetSelection/secondJet_pt", 10, "log")
    myGroup.addHistogram("JetSelection/secondJet_eta", 0.2, "log")
    myGroup.addHistogram("JetSelection/secondJet_phi", 3.14159265 / 36, "log")
    myGroup.addHistogram("JetSelection/thirdJet_pt", 10, "log")
    myGroup.addHistogram("JetSelection/thirdJet_eta", 0.2, "log")
    myGroup.addHistogram("JetSelection/thirdJet_phi", 3.14159265 / 36, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Selected jets")
    myGroup.addHistogram("JetSelection/NumberOfSelectedJets", 1, "log")
    myGroup.addHistogram("JetSelection/SelectedJets/jet_pt", 5, "log")
    myGroup.addHistogram("JetSelection/SelectedJets/jet_eta", 0.2, "log")
    myGroup.addHistogram("JetSelection/SelectedJets/jet_phi", 3.14159265 / 36, "log")
    myGroup.addHistogram("JetSelection/SelectedJets/jet_NeutralEmEnergyFraction", 0.05, "log")
    myGroup.addHistogram("JetSelection/SelectedJets/jet_NeutralHadronEnergyFraction", 0.05, "log")
    myGroup.addHistogram("JetSelection/SelectedJets/jet_NeutralHadronMultiplicity", 1, "log")
    myGroup.addHistogram("JetSelection/SelectedJets/jet_PhotonEnergyFraction", 0.05, "log")
    myGroup.addHistogram("JetSelection/SelectedJets/jet_PhotonMultiplicity", 1, "log")
    myGroup.addHistogram("JetSelection/SelectedJets/jet_ChargedHadronEnergyFraction", 0.05, "log")
    myGroup.addHistogram("JetSelection/SelectedJets/jet_ChargedMultiplicity", 1, "log")
    myGroup.addHistogram("JetSelection/SelectedJets/jet_PartonFlavour", 1, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Excluded jets, i.e. jets with DeltaR(jet, tau) < 0.5")
    myGroup.addHistogram("JetSelection/ExcludedJets/jet_pt", 10, "log")
    myGroup.addHistogram("JetSelection/ExcludedJets/jet_eta", 0.2, "log")
    myGroup.addHistogram("JetSelection/ExcludedJets/jet_phi", 3.14159265 / 36, "log")
    myGroup.addHistogram("JetSelection/ExcludedJets/jet_NeutralEmEnergyFraction", 0.05, "log")
    myGroup.addHistogram("JetSelection/ExcludedJets/jet_NeutralHadronEnergyFraction", 0.05, "log")
    myGroup.addHistogram("JetSelection/ExcludedJets/jet_NeutralHadronMultiplicity", 1, "log")
    myGroup.addHistogram("JetSelection/ExcludedJets/jet_PhotonEnergyFraction", 0.05, "log")
    myGroup.addHistogram("JetSelection/ExcludedJets/jet_PhotonMultiplicity", 1, "log")
    myGroup.addHistogram("JetSelection/ExcludedJets/jet_ChargedHadronEnergyFraction", 0.05, "log")
    myGroup.addHistogram("JetSelection/ExcludedJets/jet_ChargedMultiplicity", 1, "log")
    myGroup.addHistogram("JetSelection/ExcludedJets/jet_PartonFlavour", 1, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("MET")
    myGroup.addHistogram("MET/met", 20, "log")
    myGroup.addHistogram("MET/metSignif", 5, "log")
    myGroup.addHistogram("MET/metSumEt", 20, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("b-jet tagging")
    myGroup.addCounter("b-tagging")
    myGroup.addHistogram("Btagging/NumberOfBtaggedJets", 1, "log")
    myGroup.addHistogram("Btagging/jet_bdiscriminator", 0.1, "log")
    myGroup.addHistogram("Btagging/bjet_pt", 10, "log")
    myGroup.addHistogram("Btagging/bjet_eta", 0.2, "log")
    myGroup.addHistogram("Btagging/bjet1_pt", 20, "log")
    myGroup.addHistogram("Btagging/bjet1_eta", 0.2, "log")
    myGroup.addHistogram("Btagging/bjet2_pt", 20, "log")
    myGroup.addHistogram("Btagging/bjet2_eta", 0.2, "log")
    myGroup.addHistogram("Btagging/MCMatchForPassedJets", 1, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("QCD tail killer")
    myGroup.addCounter("QCDTailKiller")
    myGroup.addHistogram("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet1", 10, "log")
    myGroup.addHistogram("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet2", 10, "log")
    myGroup.addHistogram("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet3", 10, "log")
    myGroup.addHistogram("QCDTailKiller/BackToBackSystem/CircleCut_BackToBackJet4", 10, "log")
    myGroup.addHistogram("QCDTailKiller/CollinearSystem/CircleCut_CollinearJet1", 10, "log")
    myGroup.addHistogram("QCDTailKiller/CollinearSystem/CircleCut_CollinearJet2", 10, "log")
    myGroup.addHistogram("QCDTailKiller/CollinearSystem/CircleCut_CollinearJet3", 10, "log")
    myGroup.addHistogram("QCDTailKiller/CollinearSystem/CircleCut_CollinearJet4", 10, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Transverse and invariant mass")
    #myGroup.addCounter("FullHiggsMassCalculator")
    #myGroup.addHistogram("deltaPhi", 10, "linear")
    myGroup.addHistogram(["shapeTransverseMass",], 20, "linear")
    myGroup.addHistogram(["shapeEWKFakeTausTransverseMass"], 20, "linear")
    myGroup.addHistogram(["shapeInvariantMass",], 10, "linear")
    myGroup.addHistogram(["shapeEWKFakeTausInvariantMass"], 10, "linear")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("TopSelection (TopChi)")
    myGroup.addCounter("top")
    myGroup.addHistogram("TopChiSelection/PtTop", 10, "log")
    myGroup.addHistogram("TopChiSelection/TopMass", 10, "log")
    myGroup.addHistogram("TopChiSelection/WMass", 5, "log")
    myGroup.addHistogram("TopChiSelection/Chi2Min", 0.2, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("Fake taus")
    myGroup.addCounter("e->tau")
    myGroup.addCounter("mu->tau")
    myGroup.addCounter("jet->tau")
    myGroup.addCounter("tau->tau")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("ForDataDrivenCtrlPlots")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/SelectedTau_pT_AfterStandardSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/SelectedTau_eta_AfterStandardSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/SelectedTau_phi_AfterStandardSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/SelectedTau_Rtau_AfterStandardSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/SelectedTau_DecayMode_AfterStandardSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/Njets_AfterStandardSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/JetPt_AfterStandardSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/JetEta_AfterStandardSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsCollinearMinimum", 20, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/MET", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/METPhi", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/NBjets", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/BJetPt", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/BJetEta", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsBackToBackMinimum", 20, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/TopMass", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/WMass", 10, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("ForDataDrivenCtrlPlotsEWKFakeTaus")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/SelectedTau_pT_AfterStandardSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/SelectedTau_eta_AfterStandardSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/SelectedTau_phi_AfterStandardSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/SelectedTau_Rtau_AfterStandardSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/SelectedTau_DecayMode_AfterStandardSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/Njets_AfterStandardSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/JetPt_AfterStandardSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/JetEta_AfterStandardSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/ImprovedDeltaPhiCutsCollinearMinimum", 20, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/MET", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/METPhi", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/NBjets", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/BJetPt", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/BJetEta", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/ImprovedDeltaPhiCutsBackToBackMinimum", 20, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/TopMass", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/WMass", 10, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("ControlPlotsAfterMtSelections")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/SelectedTau_pT_AfterMtSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/SelectedTau_eta_AfterMtSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/SelectedTau_phi_AfterMtSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/SelectedTau_Rtau_AfterMtSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/SelectedTau_DecayMode_AfterMtSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/Njets_AfterMtSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/JetPt_AfterMtSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/JetEta_AfterMtSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsCollinearMinimum_AfterMtSelections", 20, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/MET_AfterMtSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/METPhi_AfterMtSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/NBjets_AfterMtSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/BJetPt_AfterMtSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/BJetEta_AfterMtSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/ImprovedDeltaPhiCutsBackToBackMinimum_AfterMtSelections", 20, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/TopMass_AfterMtSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlots/WMass_AfterMtSelections", 10, "log")
    myGroups.append(myGroup)
  
    myGroup = ValidateGroup("ControlPlotsAfterMtSelectionsEWKFakeTaus")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/SelectedTau_pT_AfterMtSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/SelectedTau_eta_AfterMtSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/SelectedTau_phi_AfterMtSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/SelectedTau_Rtau_AfterMtSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/SelectedTau_DecayMode_AfterMtSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/Njets_AfterMtSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/JetPt_AfterMtSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/JetEta_AfterMtSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/ImprovedDeltaPhiCutsCollinearMinimum_AfterMtSelections", 20, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/MET_AfterMtSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/METPhi_AfterMtSelections", 0.1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/NBjets_AfterMtSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/BJetPt_AfterMtSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/BJetEta_AfterMtSelections", 1, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/ImprovedDeltaPhiCutsBackToBackMinimum_AfterMtSelections", 20, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/TopMass_AfterMtSelections", 10, "log")
    myGroup.addHistogram("ForDataDrivenCtrlPlotsEWKFakeTaus/WMass_AfterMtSelections", 10, "log")
    myGroups.append(myGroup)
    
    myGroup = ValidateGroup("QCDInverted_Baseline_Norm")
    myGroup.addHistogram("baseline/METBaselineTauIdAfterCollinearCuts", 10, "log")
    myGroup.addHistogram("baseline/METBaselineTauIdAfterCollinearCutsPlusBtag", 10, "log")
    myGroup.addHistogram("baseline/MTBaselineTauIdAfterCollinearCuts", 10, "log")
    myGroup.addHistogram("baseline/MTBaselineTauIdFinalReversedBtag", 10, "log")
    myGroup.addHistogram("baseline/MTBaselineTauIdFinalReversedBacktoBackDeltaPhi", 10, "log")
    myGroup.addHistogram("baseline/INVMASSBaselineTauIdAfterCollinearCuts", 10, "log")
    myGroup.addHistogram("baseline/INVMASSBaselineTauIdFinalReversedBtag", 10, "log")
    myGroup.addHistogram("baseline/INVMASSBaselineTauIdFinalReversedBacktoBackDeltaPhi", 10, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("QCDInverted_Inverted_Norm")
    myGroup.addHistogram("Inverted/METInvertedTauIdAfterCollinearCuts", 10, "log")
    myGroup.addHistogram("Inverted/METInvertedTauIdAfterCollinearCutsPlusBtag", 10, "log")
    myGroup.addHistogram("Inverted/MTInvertedTauIdAfterCollinearCuts", 10, "log")
    myGroup.addHistogram("Inverted/MTInvertedTauIdFinalReversedBtag", 10, "log")
    myGroup.addHistogram("Inverted/MTInvertedTauIdFinalReversedBacktoBackDeltaPhi", 10, "log")
    myGroup.addHistogram("Inverted/INVMASSInvertedTauIdAfterCollinearCuts", 10, "log")
    myGroup.addHistogram("Inverted/INVMASSInvertedTauIdFinalReversedBtag", 10, "log")
    myGroup.addHistogram("Inverted/INVMASSInvertedTauIdFinalReversedBacktoBackDeltaPhi", 10, "log")
    myGroups.append(myGroup)

    # Add common plots
    myCommonPlots = ["VertexSelection","TauSelection","TauWeight","ElectronVeto","MuonVeto","JetSelection","MET","BTagging","Selected"]
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "nVertices", 1, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "tau_fakeStatus", 1, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "tau_pT", 10, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "tau_eta", 1, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "tau_phi", 0.0873, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "tau_Rtau", 0.1, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "electrons_N", 1, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "muons_N", 1, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "jets_N", 1, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "jets_N_allIdentified", 1, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "MET_Raw", 10, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "MET_MET", 10, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "MET_phi", 0.0873, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "bjets_N", 1, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "DeltaPhi_TauMET", 10, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "hDeltaR_TauMETJet1MET", 10, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "hDeltaR_TauMETJet2MET", 10, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "hDeltaR_TauMETJet3MET", 10, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "hDeltaR_TauMETJet4MET", 10, "log"))
    myGroups.append(addCommonPlotsAtEveryStep(myCommonPlots, "transverseMass", 20, "linear"))

    myGroup = ValidateGroup("EvtTopology")
    myGroup.addCounter("EvtTopology")
    myGroup.addHistogram("EvtTopology/alphaT", 0.1, "log")
    myGroup.addHistogram("EvtTopology/sphericity", 0.05, "log")
    myGroup.addHistogram("EvtTopology/aplanarity", 0.05, "log")
    myGroups.append(myGroup)

    myGroup = ValidateGroup("MCinfo for selected events")
    myGroup.addCounter("MCinfo for selected events")
    myGroups.append(myGroup)
    return myGroups

def makehtml(mydir, myFilename, myOutput):
    myhtmlheader = "<html>\n<head>\n<title>ValidationResults</title>\n</head>\n<body bgcolor=#6666cc>\n"
    myhtmlfooter = "</body>\n</html>\n"
    myfile = open("%s/%s.html"%(mydir,myFilename.replace(".html","").replace(" ","_")),"w")
    myfile.write(myhtmlheader)
    myfile.write(myOutput)
    myfile.write(myhtmlfooter)
    myfile.close()

def main(opts,timeStamp,refDsetCreator,testDsetCreator,myValidateGroups,era,searchMode,analysisVariation,myBaseDir,myModuleDir):
    myTotalCount = 0.0
    for g in myValidateGroups:
        myTotalCount += g.getItemCount()
    # Create output directory
    if not os.path.exists(myBaseDir+"/"+myModuleDir):
        os.mkdir(myBaseDir+"/"+myModuleDir)
    # Create Navigation panel
    myPanel = NavigationPanel(timeStamp)
    myPanel.setModule(era,searchMode,analysisVariation)
    # Message to screen
    print "\nValidating era = %s, searchMode = %s, analysisVariation = %s\n"%(era,searchMode,analysisVariation)
    # Construct output
    #myOutput = "<h1>Validation of datasets</h1><br>\n"
    #myOutput = "<hr><br>\n"
    #myOutput = "Era = %s<br>\n"%era
    #myOutput += "SearchMode = %s<br>\n"%searchMode
    #if analysisVariation != None:
        #myOutput += "AnalysisVariation = no variation (default taken)<br>\n"
    #else:
        #myOutput += "AnalysisVariation = %s<br>\n"%analysisVariation
    #myOutput = "<hr><br>\n"
    # Obtain dataset managers (using default value for analysisName)
    #refDatasetMgr = refDsetCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=analysisVariation,analysisName="signalAnalysisMIdEffTrgEffMetEffTEff")
    refDatasetMgr = refDsetCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=analysisVariation)
    testDatasetMgr = testDsetCreator.createDatasetManager(dataEra=era,searchMode=searchMode,optimizationMode=analysisVariation)
    # Normalisation
    refDatasetMgr.updateNAllEventsToPUWeighted()
    testDatasetMgr.updateNAllEventsToPUWeighted()
    # Find common dataset names
    commonDatasetNames = None
    if opts.mergeRefDataset != None or opts.mergeTestDataset != None:
        # Merge datasets
        refName = "mergedRef_%s"%("_".join(map(str,opts.mergeRefDataset)))
        testName = "mergedTest_%s"%("_".join(map(str,opts.mergeTestDataset)))
        commonDatasetNames = [(refName, testName)]
        print "Merging: %s -> ref."%", ".join(map(str,opts.mergeRefDataset))
        refDatasetMgr.merge(refName, opts.mergeRefDataset)
        print "Merging: %s -> test"%", ".join(map(str,opts.mergeTestDataset))
        testDatasetMgr.merge(testName, opts.mergeTestDataset)
    elif opts.testDir is None:
        commonDatasetNames = compareLists(refDatasetMgr.getAllDatasetNames(),testDatasetMgr.getAllDatasetNames(),opts.dirs)
        commonDatasetNames = [(x, x) for x in commonDatasetNames]
    else:
        commonDatasetNames = [(opts.dirs[0], opts.testDir)]
    # Loop over common dataset names
    #myOutput += "Following dataset names found in both reference and test multicrab directories<br>\n"
    myOutput = "      <ul>\n"
    myItemCount = 0.0
    for refDsetName, testDsetName in commonDatasetNames:
        myReadCounterItemsCount = 0
        myReadHistogramsCount = 0
        print "  Dataset: %s"%refDsetName
        myPanel.setDataset(refDsetName, testDsetName)
        name = refDsetName
        if refDsetName != testDsetName:
            name = "%s vs. %s" % (refDsetName, testDsetName)
        myOutput += '        <li><b><a href="%s.html">%s</a></b>'%(myModuleDir+"/"+refDsetName+"/"+myValidateGroups[0].getName().replace(" ","_"),name)
        myGroupCount = 0
        for g in myValidateGroups:
            myGroupCount += 1
            print "  ... validating group %d/%d: %s"%(myGroupCount, len(myValidateGroups), g.getName())
            # Create output and histograms and cache difference for panel
            #if not (myItemCount % 20):
                #print "  ... validating histograms/counters %.2f"%(myItemCount/myTotalCount*100.0)
            g.doValidate(myBaseDir+"/"+myModuleDir+"/"+refDsetName, refDatasetMgr.getDataset(refDsetName), testDatasetMgr.getDataset(testDsetName))
            myReadCounterItemsCount += g.getReadCounterCount()
            myReadHistogramsCount += g.getReadHistogramCount()
        # Create html subpages with panel
        for g in myValidateGroups:
            myPanel.makehtml(myValidateGroups,g.getOutput(),myBaseDir+"/"+myModuleDir+"/"+refDsetName,g.getName())
        myItemCount += 1.0
        myOutput += " (subcounters=%d, histograms=%d)</li>\n"%(myReadCounterItemsCount,myReadHistogramsCount)
    myOutput += "      </ul>\n"
    # Save output
    # Do not call close here, call it only once for dataset creators
    return myOutput

def compareLists(refList, testList, optList):
    selectList = []
    if optList == None:
        optList = refList
    for optItem in optList:
        if optItem in refList and optItem in testList:
            selectList.append(optItem)
    #print "ref=",refList
    #print "test=",testList
    #print "sel=",selectList
    return selectList

if __name__ == "__main__":
    ROOT.gROOT.SetBatch() # no flashing canvases

    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--ref", dest="reference", action="store", default=None, help="reference multicrab directory")
    parser.add_option("--refFile", dest="referenceFile", default=None, help="Reference file (give either this or --ref")
    parser.add_option("--oldref", dest="oldreference", action="store_true", help="use this flag if the reference is using signalAnalysisCounters")
    parser.add_option("--test", dest="test", action="store", help="multicrab directory to be tested/validated")
    parser.add_option("--testFile", dest="testFile", default=None, help="Test file (give either this or --test")
    parser.add_option("-d", dest="dirs", action="append", help="name of sample directory inside multicrab dir (multiple directories can be specified with multiple -d arguments)")
    parser.add_option("--testDir", dest="testDir", default=None, help="Name of the sample directory in test multicrab dir")
    parser.add_option("--mergeRefDataset", dest="mergeRefDataset", action="append", help="name of tasks inside multicrab dir to be merged as the ref dataset (multiple directories can be specified with multiple -d arguments)")
    parser.add_option("--mergeTestDataset", dest="mergeTestDataset", action="append", help="name of tasks inside multicrab dir to be merged as the test dataset (multiple directories can be specified with multiple -d arguments)")
    parser.add_option("-v", dest="variation", action="append", help="name of variation")
    parser.add_option("-e", dest="era", action="append", help="name of era")
    parser.add_option("-m", dest="searchMode", action="append", help="name of search mode")
    parser.add_option("--normalizeToLumi", dest="normalizeToLumi", type="float", default=None, help="If set, normalize MC to this luminosity (default is to not to normalize)")
    (opts, args) = parser.parse_args()

    # Check that proper arguments were given
    mystatus = True
    if opts.reference is None and opts.referenceFile is None:
        print "Error: Missing reference multicrab directory!"
        mystatus = False
    if opts.test is None and opts.testFile is None:
        print "Error: Missing multicrab directory for testing/validation!"
        mystatus = False
    if opts.dirs == None and not (opts.mergeRefDataset != None and opts.mergeTestDataset != None):
        print "(optional) Missing source for sample directories (use -d if desired) will use all sample directories"
        #mystatus = False
    if opts.era == None:
        print "(optional) Missing specification for era (use -e if desired) - will use all available eras"
        #mystatus = False
    if opts.searchMode == None:
        print "(optional) Missing specification for searchMode (use -m if desired) - will use all available searchModes"
        #mystatus = False
    if opts.variation== None:
        print "(optional) Missing specification for analysis variation (use -v if desired) - will use all available variations"
        #mystatus = False
    if opts.testDir is not None and (opts.dirs is None or len(opts.dirs) != 1):
        print "Error: with --testDir exactly one -d is allowed (got %d)" % (len(opts.dirs))
        myStatus = False
    if opts.mergeRefDataset != None and opts.mergeTestDataset == None:
        print "Error: --mergeRefDataset has been used, please define also --mergeTestDataset !"
        myStatus = False
    if opts.mergeRefDataset == None and opts.mergeTestDataset != None:
        print "Error: --mergeTestDataset has been used, please define also --mergeRefDataset !"
        myStatus = False
    if not mystatus:
        parser.print_help()
        sys.exit()

    # Create dataset creators to see what's inside
    kwargs = {}
    if opts.dirs is not None:
        kwargs["includeOnlyTasks"] = opts.dirs[:]
    if opts.reference is not None:
        refDsetCreator = dataset.readFromMulticrabCfg(directory=opts.reference, **kwargs)
    else:
        refDsetCreator = dataset.readFromRootFiles([("File", opts.referenceFile)])
    if opts.testDir is not None:
        kwargs["includeOnlyTasks"] = [opts.testDir]
    if opts.test is not None:
        testDsetCreator = dataset.readFromMulticrabCfg(directory=opts.test, **kwargs)
    else:
        testDsetCreator = dataset.readFromRootFiles([("File", opts.testFile)])
    myEraList = compareLists(refDsetCreator.getDataEras(), testDsetCreator.getDataEras(), opts.era)
    mySearchModeList = compareLists(refDsetCreator.getSearchModes(), testDsetCreator.getSearchModes(), opts.searchMode)
    myVariationList = compareLists(refDsetCreator.getOptimizationModes(), testDsetCreator.getOptimizationModes(), opts.variation)
    if len(myVariationList) == 0:
        myVariationList.append(None)
    # Create ValidateGroups
    myValidateGroups = createValidateHistograms()
    if opts.normalizeToLumi is not None:
        for vg in myValidateGroups:
            vg.setMCNormalization(normalizeToLumi=opts.normalizeToLumi)

    # Create output directory
    myTimeStamp = datetime.now().strftime("%y%m%d_%H%M%S")
    myDir = "validation_"+myTimeStamp
    if not os.path.exists(myDir):
        os.mkdir(myDir)

    myMainFile = "<h1>Choose dataset:</h1><br>\n"
    # Arguments are ok, proceed to run
    myMainFile += "<ul>\n"
    for e in myEraList:
        # Format era properly
        myMainFile += "  <li><b>Era =</b> %s</li>\n"%e
        myMainFile += "  <ul>\n"
        for m in mySearchModeList:
            myMainFile += "    <li><b>SearchMode =</b> %s</li>\n"%m
            myMainFile += "    <ul>\n"
            if myVariationList[0] == None:
                myHtmlRef="%s_%s_defaultAnalysis"%(e,m)
                myMainFile += '      <li>Nominal analysis</li>\n'
                myMainFile += main(opts,myTimeStamp,refDsetCreator,testDsetCreator,myValidateGroups,e,m,None,myDir,myHtmlRef)
            else:
                for v in myVariationList:
                    myHtmlRef="%s_%s_%s"%(e,m,v)
                    myMainFile += '      <li><b>Variation =</b> %s</li>\n'%(v)
                    myMainFile += main(opts,myTimeStamp,refDsetCreator,testDsetCreator,myValidateGroups,e,m,v,myDir,myHtmlRef)
            myMainFile += "    </ul>\n"
        myMainFile += "  </ul>\n"
    myMainFile += "</ul>\n"
    myMainFile += "If not all eras / searchModes / variations are seen in the above list, then some of them do not exist in the reference or test multicrab directory.<br>\n"
    myMainFile += "<hr>Created by script scripts/validate.py<br>\n"
    # Make html page for choosing run
    myPanel = NavigationPanel(myTimeStamp)
    myPanel.makehtml([],myMainFile,myDir,"index.html")
    # Make tar package
    print "\nMaking tar package '%s.tgz' for exporting/archiving ..."%myDir
    tar = tarfile.open("%s.tgz"%myDir, mode="w:gz")
    tar.add(myDir)
    tar.close()
    # Final output
    print "\nDone."
    print "To browse, type:"
    print "firefox %s/index.html"%myDir
    print "\n(garbage collection might take some time before you can use the shell again ...)\n"
    #vie datasetcreator -> main

