#!/usr/bin/env python

# UnfoldedHistogramReader
#
# Purpose: Provide tools for reading information out of unfolded histograms (factorisation or binned information)
#
# Remarks:
#   - Binning information is assumed to be stored in the histogram title separated with a semicolon (for example: 'taupt:5:taueta:3:titleofhistogram')
#   - Histogram object is assumed to be TH2
#   - Information in histogram object is stored with following convention:
#     . x-axis contains information for the factorisation bin (just one bin for event counts; n bins for a shape)
#     . y-axis is the unfolded bin number (i.e. factorisation bin)
#     . Unfolding of binning is done with formula: y = x1 + x2*Nx1 + x3*Nx1*Nx2 ... (Nx is the number of bins including under- and overflow for given dimension)
#
# Author: Lauri A. Wendland

import os
import sys
import ROOT

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from math import sqrt

class UnfoldedHistogramReader:
    def __init__(self, debugStatus = False):
        self._binLabels = []  # Each cell contains the label of the nth dimension
        self._binCount = []   # Each cell contains the nbins count of the nth dimension
        self._unfoldedBinCount = None
        self._separator = ":" # Setting for decomposing bin information from histogram title
        self._debugStatus = debugStatus
        self._factorisationFullBinLabels = []
        self._factorisationCaptions = []
        self._factorisationRanges = []

    def getNbinsList(self):
        return self._binCount

    def getUnfoldedBinCount(self):
        return self._unfoldedBinCount

    def getBinLabelList(self):
        return self._binLabels

    def getFactorisationFullBinLabels(self):
        return self._factorisationFullBinLabels

    def getFactorisationCaptions(self):
        return self._factorisationCaptions

    def getFactorisationRanges(self):
        return self._factorisationRanges

    # Decomposes the unfolded bin into the different axes of factorisation, returns a list of indices
    def decomposeUnfoldedbin(self, unfoldedBinIndex):
        myIndexList = []
        for i in range(0,len(self._binCount)):
            myIndexList.append(None)
        myValue = unfoldedBinIndex
        for i in range(0,len(self._binCount)):
            myReversedIndex = len(self._binCount)-i-1
            myProduct = 1
            for j in range(0,myReversedIndex):
                myProduct *= self._binCount[j]
            #print i, myReversedIndex, myProduct
            myIndexList[myReversedIndex] = int(myValue / myProduct)
            myValue -= myIndexList[myReversedIndex] * myProduct
        #print myIndexList
        return myIndexList

    # Returns the event count of the factorisation bin [x,y,...]
    def getEventCountForBin(self, factorisationBinIndexList, h):
        self._initialize(h)
        # Check that binning dimension is correct
        if len(self._binCount) != len(factorisationBinIndexList):
            raise Exception("Error in UnfoldedHistogramReader::getEventCountForBin(): You asked for %d dimensions, but the histogram has %d dimensions (the dimension needs to be the same)!"%(len(factorisationBinIndexList), len(self._binCount)))
        return h.GetBinContent(1, self._convertBinIndexListToUnfoldedIndex(factorisationBinIndexList)+1)

    # Returns the event count (stat.) uncertainty of the factorisation bin [x,y,...]
    def getEventCountUncertaintyForBin(self, factorisationBinIndexList, h):
        self._initialize(h)
        # Check that binning dimension is correct
        if len(self._binCount) != len(factorisationBinIndexList):
            raise Exception("Error in UnfoldedHistogramReader::getEventCountForBin(): You asked for %d dimensions, but the histogram has %d dimensions (the dimension needs to be the same)!"%(len(factorisationBinIndexList), len(self._binCount)))
        return h.GetBinError(1, self._convertBinIndexListToUnfoldedIndex(factorisationBinIndexList)+1)

    # Returns the event count in a bin of a shape for the factorisation bin [x,y,...]
    def getShapeCountForBin(self, factorisationBinIndexList, h, shapeBin):
        self._initialize(h)
        # Check that binning dimension is correct
        if len(self._binCount) != len(factorisationBinIndexList):
            raise Exception("Error in UnfoldedHistogramReader::getEventCountForBin(): You asked for %d dimensions, but the histogram has %d dimensions (the dimension needs to be the same)!"%(len(factorisationBinIndexList), len(self._binCount)))
        return h.GetBinContent(shapeBin, self._convertBinIndexListToUnfoldedIndex(factorisationBinIndexList)+1)

    # Returns the event count (stat.) uncertainty in a bin of a shape for the factorisation bin [x,y,...]
    def getShapeCountUncertaintyForBin(self, factorisationBinIndexList, h, shapeBin):
        self._initialize(h)
        # Check that binning dimension is correct
        if len(self._binCount) != len(factorisationBinIndexList):
            raise Exception("Error in UnfoldedHistogramReader::getEventCountForBin(): You asked for %d dimensions, but the histogram has %d dimensions (the dimension needs to be the same)!"%(len(factorisationBinIndexList), len(self._binCount)))
        return h.GetBinError(shapeBin, self._convertBinIndexListToUnfoldedIndex(factorisationBinIndexList)+1)

    # Returns the event count of the unfolded factorisation bin
    def getEventCountForUnfoldedBin(self, unfoldedBinIndex, h):
        self._initialize(h)
        return h.GetBinContent(1, unfoldedBinIndex+1)

    # Returns the event count (stat.) uncertainty of the unfolded factorisation bin
    def getEventCountUncertaintyForUnfoldedBin(self, unfoldedBinIndex, h):
        self._initialize(h)
        return h.GetBinError(1, unfoldedBinIndex+1)

    # Returns the event count in a bin of a shape for the unfolded factorisation bin
    def getShapeCountForUnfoldedBin(self, unfoldedBinIndex, h, shapeBin):
        self._initialize(h)
        return h.GetBinContent(shapeBin, unfoldedBinIndex+1)

    # Returns the event count (stat.) uncertainty in a bin of a shape for the unfolded factorisation bin
    def getShapeCountUncertaintyForUnfoldedBin(self, unfoldedBinIndex, h, shapeBin):
        self._initialize(h)
        return h.GetBinError(shapeBin, unfoldedBinIndex+1)

    # Returns the event count for a factorisation bin by contracting the other factorisation dimensions (i.e. reduce the factorisation dimensions to just the one specified)
    def getContractedEventCountForBin(self, factorisationAxisToKeep, factorisationBin, h):
        self._initialize(h)
        return self._contractionRecursionForBin([], factorisationAxisToKeep, factorisationBin, h, 1)

    # Returns the event count (stat.) uncertainty for a factorisation bin by contracting the other factorisation dimensions (i.e. reduce the factorisation dimensions to just the one specified)
    def getContractedEventCountUncertaintyForBin(self, factorisationAxisToKeep, factorisationBin, h):
        self._initialize(h)
        return sqrt(self._contractionRecursionUncertaintyForBin([], factorisationAxisToKeep, factorisationBin, h, 1))

    # Returns the event count for a factorisation bin by contracting the other factorisation dimensions (i.e. reduce the factorisation dimensions to just the one specified)
    def getContractedShapeCountForBin(self, factorisationAxisToKeep, factorisationBin, h, shapeBin):
        self._initialize(h)
        return self._contractionRecursionForBin([], factorisationAxisToKeep, factorisationBin, h, shapeBin)

    # Returns the event count (stat.) uncertainty for a factorisation bin by contracting the other factorisation dimensions (i.e. reduce the factorisation dimensions to just the one specified)
    def getContractedShapeCountUncertaintyForBin(self, factorisationAxisToKeep, factorisationBin, h, shapeBin):
        self._initialize(h)
        return sqrt(self._contractionRecursionUncertaintyForBin([], factorisationAxisToKeep, factorisationBin, h, shapeBin))

    # Prints info about factorisation axes and ranges
    def printFactorisationDefinitions(self):
        print "Factorisation settings:"
        for i in range(0,len(self._binLabels)):
            print "  variable: %s, binning={%s}"%(self._binLabels[i], '; '.join(map(str, self._factorisationRanges[i])))

    def _contractionRecursionForBin(self, binIndexList, factorisationAxisToKeep, factorisationBin, h, shapeBin):
        #print "recursion",binIndexList
        if len(binIndexList) == len(self._binCount):
            # On final axis, return value
            if len(binIndexList) != factorisationAxisToKeep:
                #print "value=",h.GetBinContent(shapeBin, self._convertBinIndexListToUnfoldedIndex(binIndexList))
                return h.GetBinContent(shapeBin, self._convertBinIndexListToUnfoldedIndex(binIndexList)+1)
            else:
                if binIndexList[len(binIndexList)] == factorisationBin:
                    #print "value=",h.GetBinContent(shapeBin, self._convertBinIndexListToUnfoldedIndex(binIndexList))
                    return h.GetBinContent(shapeBin, self._convertBinIndexListToUnfoldedIndex(binIndexList)+1)
                else:
                    #print "value=0"
                    return 0.0
        else:
            # Not last axis, i.e. need to investigate next dimension
            mySum = 0.0
            if len(binIndexList) != factorisationAxisToKeep:
                #print "not on axis"
                # Not on desired axis, loop over all cells
                for i in range(0,self._binCount[len(binIndexList)]):
                    myBinIndexList = []
                    myBinIndexList.extend(binIndexList)
                    myBinIndexList.append(i)
                    mySum += self._contractionRecursionForBin(myBinIndexList, factorisationAxisToKeep, factorisationBin, h, shapeBin)
            else:
                #print "axis",factorisationAxisToKeep
                # On desired axis, take only the chosen value
                myBinIndexList = []
                myBinIndexList.extend(binIndexList)
                myBinIndexList.append(factorisationBin)
                mySum += self._contractionRecursionForBin(myBinIndexList, factorisationAxisToKeep, factorisationBin, h, shapeBin)
            return mySum

    def _contractionRecursionUncertaintyForBin(self, binIndexList, factorisationAxisToKeep, factorisationBin, h, shapeBin):
        #print "recursion",binIndexList
        if len(binIndexList) == len(self._binCount):
            # On final axis, return value
            if len(binIndexList) != factorisationAxisToKeep:
                return h.GetBinError(shapeBin, self._convertBinIndexListToUnfoldedIndex(binIndexList)+1)**2
            else:
                if binIndexList[len(binIndexList)] == factorisationBin:
                    return h.GetBinError(shapeBin, self._convertBinIndexListToUnfoldedIndex(binIndexList)+1)**2
                else:
                    return 0.0
        else:
            # Not last axis, i.e. need to investigate next dimension
            mySum = 0.0
            if len(binIndexList) != factorisationAxisToKeep:
                # Not on desired axis, loop over all cells
                for i in range(0,self._binCount[len(binIndexList)]):
                    myBinIndexList = []
                    myBinIndexList.extend(binIndexList)
                    myBinIndexList.append(i)
                    mySum += self._contractionRecursionUncertaintyForBin(myBinIndexList, factorisationAxisToKeep, factorisationBin, h, shapeBin)
            else:
                # On desired axis, take only the chosen value
                myBinIndexList = []
                myBinIndexList.extend(binIndexList)
                myBinIndexList.append(factorisationBin)
                mySum += self._contractionRecursionUncertaintyForBin(myBinIndexList, factorisationAxisToKeep, factorisationBin, h, shapeBin)
            return mySum

    # Decompose factorisation bin labels and nbins information from histogram title
    def _initialize(self, h):
        if len(self._binLabels) > 0:
            return
        myTitle = h.GetTitle()
        myList = myTitle.split(self._separator)
        myFactorisationBins = int(len(myList) / 2) # allows for the title of the histogram to be placed after the last separator
        myOutput = ""
        for i in range(0,myFactorisationBins):
            self._binLabels.append(myList[i*2])
            if myList[i*2+1].isdigit():
                self._binCount.append(int(myList[i*2+1]))
            else:
                # try a bug fix by taking first character only
                if myList[i*2+1][0].isdigit():
                    print WarningLabel()+"UnfoldedHistogramReader::_initialize(): tried naive bug fix for last factorisation bin dimension (guessed dimension: %s, histo: %s)"%(myList[i*2+1][0],myList[i*2+1][1:])
                    self._binCount.append(int(myList[i*2+1][0]))
                else:
                    raise Exception(ErrorLabel()+"UnfoldedHistogramReader: failed to decompose histogram title (it should contain the bin label and nbins information for n bins separated with '%s'\nHistogram title was: %s"%(self._separator, myTitle))
            myOutput += "%s nbins=%d "%(self._binLabels[i], self._binCount[i])
        if self._debugStatus:
            print "UnfoldedHistogramReader: Histogram binning determined as : %s"%myOutput
        if len(self._binLabels) == 0:
            raise Exception(ErrorLabel()+"UnfoldedHistogramReader: failed to decompose histogram title (it should contain the bin label and nbins information for n bins separated with '%s'\nHistogram title was: %s"%(self._separator, myTitle))
        self._unfoldedBinCount = h.GetNbinsY()
        # Loop over y axis to find axis values
        myBinCaptions = []
        myBinRanges = []
        for i in range(1,h.GetNbinsY()+1):
            mySplitBin = h.GetYaxis().GetBinLabel(i).split("/")
            # Obtain bin captions
            if len(self._factorisationCaptions) == 0:
                for s in mySplitBin:
                    myCaption = ""
                    if "=" in s:
                        myCaption = s.split("=")[0]
                    elif ">" in s:
                        myCaption = s.split(">")[0]
                    elif "<" in s:
                        myCaption = s.split("<")[0]
                    self._factorisationFullBinLabels.append([])
                    self._factorisationCaptions.append(myCaption)
                    self._factorisationRanges.append([])
            # Obtain range information
            for k in range (0,len(mySplitBin)):
                if not mySplitBin[k] in self._factorisationFullBinLabels[k]:
                    self._factorisationFullBinLabels[k].append(mySplitBin[k])
                # Remove label and equal signs
                s = mySplitBin[k].replace(self._factorisationCaptions[k],"").replace("=","")
                if not s in self._factorisationRanges[k]:
                    self._factorisationRanges[k].append(s)

    def _convertBinIndexListToUnfoldedIndex(self, factorisationBinIndexList):
        # y = x1 + x2*Nx1 + x3*Nx1*Nx2 + ...
        mySum = 0
        for i in range(0,len(self._binCount)):
            myProduct = 1
            for j in range(0,i):
                myProduct *= self._binCount[j]
            mySum += factorisationBinIndexList[i]*myProduct
        return mySum

def validate():
    def check(a,b):
        if abs(a-b) < 0.00001:
            return TestPassedStyle()+"PASSED"+NormalStyle()
        else:
            print ErrorStyle()+"FAILED (%f != %f)"%(a,b)+NormalStyle()
            raise Exception("Error: validation test failed!")
    print HighlightStyle()+"validate: UnfoldedHistogramReader\n"+NormalStyle()
    print "Creating dummy histogram for testing..."
    # Create histogram with factorisation dimensions 4 x 3 x 4
    h = ROOT.TH2F("testHisto","AxisA:4:AxisB:3:AxisC:4:testHisto",10,0.,10.,48,0.,48.)
    h.Sumw2()
    # Fill known information to the histogram
    myValue = 1
    # Loop over bins
    for k in range(0,4):
        for j in range(0,3):
            for i in range(0,4):
                # Loop over shape
                idx = (i)+(j)*4+(k)*4*3
                for b in range(0,10):
                    for a in range(0,myValue*(b+1)):
                        h.Fill(b,idx)
                #print myValue,i,j,k,idx,"test",h.GetBinContent(1,idx+1)
                myValue += 1
    # Then make some tests
    r = UnfoldedHistogramReader(debugStatus=True)
    # Test binning specs
    r._initialize(h)
    print "validate: UnfoldedHistogramReader::_initialize():",check(len(r.getNbinsList()),3)
    # Test bin unfolding
    print "validate: UnfoldedHistogramReader::_convertBinIndexListToUnfoldedIndex():",check(r._convertBinIndexListToUnfoldedIndex([1,2,3]),45)
    print "validate: UnfoldedHistogramReader::decomposeUnfoldedbin1(): ", check(r.decomposeUnfoldedbin(45)[0],1)
    print "validate: UnfoldedHistogramReader::decomposeUnfoldedbin2(): ", check(r.decomposeUnfoldedbin(45)[1],2)
    print "validate: UnfoldedHistogramReader::decomposeUnfoldedbin3(): ", check(r.decomposeUnfoldedbin(45)[2],3)
    # Test event counts
    print "validate: UnfoldedHistogramReader::getEventCountForBin(): ",check(r.getEventCountForBin([1,2,3],h),46)
    print "validate: UnfoldedHistogramReader::getEventCountUncertaintyForBin(): ",check(r.getEventCountUncertaintyForBin([1,2,3],h),sqrt(46))
    # Test shape counts
    print "validate: UnfoldedHistogramReader::getShapeCountForBin(): ",check(r.getShapeCountForBin([3,1,2],h,3),32*3)
    print "validate: UnfoldedHistogramReader::getShapeCountUncertaintyForBin(): ",check(r.getShapeCountUncertaintyForBin([3,1,2],h,3),sqrt(32*3))
    # Test contracted event counts
    print "validate: UnfoldedHistogramReader::getContractedEventCountForBin(): ",check(r.getContractedEventCountForBin(0,0,h),276)
    print "validate: UnfoldedHistogramReader::getContractedEventCountUncertaintyForBin(): ",check(r.getContractedEventCountUncertaintyForBin(0,0,h),sqrt(276))
    print "validate: UnfoldedHistogramReader::getContractedShapeCountForBin() test1: ",check(r.getContractedShapeCountForBin(2,1,h,1),222)
    print "validate: UnfoldedHistogramReader::getContractedShapeCountUncertaintForBin() test1: ",check(r.getContractedShapeCountUncertaintyForBin(2,1,h,1),sqrt(222))
    print "validate: UnfoldedHistogramReader::getContractedShapeCountForBin() test2: ",check(r.getContractedShapeCountForBin(2,1,h,4),888)
    print "validate: UnfoldedHistogramReader::getContractedShapeCountUncertaintForBin() test2: ",check(r.getContractedShapeCountUncertaintyForBin(2,1,h,4),sqrt(888))
