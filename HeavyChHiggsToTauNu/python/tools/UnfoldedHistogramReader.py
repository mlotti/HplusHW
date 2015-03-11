## \package UnfoldedHistogramReader
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
# Indexing starts always from zero; for accessing root items, one is added to the internal indexing
#
# Author: Lauri A. Wendland

import os
import sys
import ROOT

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import Count
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles as ShellStyles
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

    ## Returns the Nbins list (dimension is the number of factorisation axes) of the factorisation bins
    def getNbinsList(self):
        return self._binCount

    ## Returns the number of the factorisation bins
    def getUnfoldedBinCount(self):
        return self._unfoldedBinCount

    ## Returns labels of the factorisation axes (dimension is the number of factorisation axes=
    def getBinLabelList(self):
        return self._binLabels

    ## Returns the factorisation bin labels including the ranges (dimension: N(factorisation axes) * N(bins))
    def getFactorisationFullBinLabels(self):
        return self._factorisationFullBinLabels

    ## Returns the factorisation bin labels without the ranges (dimension: N(factorisation axes) * N(bins))
    def getFactorisationCaptions(self):
        return self._factorisationCaptions

    ## Returns the factorisation bin ranges without the labels (dimension: N(factorisation axes) * N(bins))
    def getFactorisationRanges(self):
        return self._factorisationRanges

    ## Decomposes the unfolded bin into the different axes of factorisation, returns a list of indices
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

    ## Returns a list of count objects (one for each shape bin) for the factorisation bin [x,y,...]
    # Note: under- and overflow bin included only, if more than one bins exist (assume one bin histogram to be a count histogram)
    def getShapeForBin(self, factorisationBinIndexList, h):
        self._initialize(h)
        # Check that binning dimension is correct
        if len(self._binCount) != len(factorisationBinIndexList):
            raise Exception("Error in UnfoldedHistogramReader::getEventCountForBin(): You asked for %d dimensions, but the histogram has %d dimensions (the dimension needs to be the same)!"%(len(factorisationBinIndexList), len(self._binCount)))
        myResult = []
        myMin = 0
        myMax = h.GetNbinsX()
        if h.GetNbinsX() != 1:
            # Include under- and overflow bin
            myMin -= 1
            myMax += 1
        myUnfoldedBin = self._convertBinIndexListToUnfoldedIndex(factorisationBinIndexList)+1
        for i in range(myMin,myMax):
            myValue = h.GetBinContent(i+1, myUnfoldedBin)
            myUncertainty = h.GetBinError(i+1, myUnfoldedBin)
            myResult.append(Count(myValue, myUncertainty))
        return myResult

    ## Returns a list of Count objects for the unfolded factorisation bin
    # Note: under- and overflow bin included only, if more than one bins exist (assume one bin histogram to be a count histogram)
    def getShapeByUnfoldedBin(self, unfoldedBinIndex, h):
        self._initialize(h)
        myResult = []
        myMin = 0
        myMax = h.GetNbinsX()
        if h.GetNbinsX() != 1:
            # Include under- and overflow bin
            myMin -= 1
            myMax += 1
        for i in range(myMin,myMax):
            myValue = h.GetBinContent(i+1, unfoldedBinIndex+1)
            myUncertainty = h.GetBinError(i+1, unfoldedBinIndex+1)
            myResult.append(Count(myValue, myUncertainty))
        return myResult

    ## Returns a list of the Count objects for a factorisation bin by contracting the other factorisation dimensions (i.e. reduce the factorisation dimensions to just the one specified)
    # Note: under- and overflow bin included only, if more than one bins exist (assume one bin histogram to be a count histogram)
    def getContractedShapeForBin(self, factorisationAxisToKeep, factorisationBin, h):
        self._initialize(h)
        myResult = []
        myMin = 0
        myMax = h.GetNbinsX()
        if h.GetNbinsX() != 1:
            # Include under- and overflow bin
            myMin -= 1
            myMax += 1
        for i in range(myMin,myMax):
            myValue = self._contractionRecursionForBin([], factorisationAxisToKeep, factorisationBin, h, i)
            myUncertainty = sqrt(self._contractionRecursionUncertaintyForBin([], factorisationAxisToKeep, factorisationBin, h, i))
            myResult.append(Count(myValue, myUncertainty))
        return myResult

    # Prints info about factorisation axes and ranges
    def printFactorisationDefinitions(self):
        print "Factorisation settings:"
        for i in range(0,len(self._binLabels)):
            print "  variable: %s, binning={%s}"%(self._binLabels[i], '; '.join(map(str, self._factorisationRanges[i])))

    ## Do the summing by recursion for a given shape bin at a time
    def _contractionRecursionForBin(self, binIndexList, factorisationAxisToKeep, factorisationBin, h, shapeBin):
        #print "recursion",binIndexList
        if len(binIndexList) == len(self._binCount):
            # On final axis, return value
            if len(binIndexList) != factorisationAxisToKeep:
                #print "value=",h.GetBinContent(shapeBin, self._convertBinIndexListToUnfoldedIndex(binIndexList))
                return h.GetBinContent(shapeBin+1, self._convertBinIndexListToUnfoldedIndex(binIndexList)+1)
            else:
                if binIndexList[len(binIndexList)] == factorisationBin:
                    #print "value=",h.GetBinContent(shapeBin, self._convertBinIndexListToUnfoldedIndex(binIndexList))
                    return h.GetBinContent(shapeBin+1, self._convertBinIndexListToUnfoldedIndex(binIndexList)+1)
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

    ## Helper method to do the actual recursion
    def _contractionRecursionUncertaintyForBin(self, binIndexList, factorisationAxisToKeep, factorisationBin, h, shapeBin):
        #print "recursion",binIndexList
        if len(binIndexList) == len(self._binCount):
            # On final axis, return value
            if len(binIndexList) != factorisationAxisToKeep:
                return h.GetBinError(shapeBin+1, self._convertBinIndexListToUnfoldedIndex(binIndexList)+1)**2
            else:
                if binIndexList[len(binIndexList+1)] == factorisationBin:
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

    ## Decompose factorisation bin labels and nbins information from histogram title
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
                    print ShellStyles.WarningLabel()+"UnfoldedHistogramReader::_initialize(): tried naive bug fix for last factorisation bin dimension (guessed dimension: %s, histo: %s)"%(myList[i*2+1][0],myList[i*2+1][1:])
                    self._binCount.append(int(myList[i*2+1][0]))
                else:
                    raise Exception(ShellStyles.ErrorLabel()+"UnfoldedHistogramReader: failed to decompose histogram title (it should contain the bin label and nbins information for n bins separated with '%s'\nHistogram title was: %s"%(self._separator, myTitle))
            myOutput += "%s nbins=%d "%(self._binLabels[i], self._binCount[i])
        if self._debugStatus:
            print "UnfoldedHistogramReader: Histogram binning determined as : %s"%myOutput
        if len(self._binLabels) == 0:
            raise Exception(ShellStyles.ErrorLabel()+"UnfoldedHistogramReader: failed to decompose histogram title (it should contain the bin label and nbins information for n bins separated with '%s'\nHistogram title was: %s"%(self._separator, myTitle))
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

    ## Converts the N dimensional index to 1-dimensional unfolded one
    def _convertBinIndexListToUnfoldedIndex(self, factorisationBinIndexList):
        # y = x1 + x2*Nx1 + x3*Nx1*Nx2 + ...
        mySum = 0
        for i in range(0,len(self._binCount)):
            myProduct = 1
            for j in range(0,i):
                myProduct *= self._binCount[j]
            mySum += factorisationBinIndexList[i]*myProduct
        return mySum

## Method containing the validation tests for this package
def validateUnfoldedHistogramReader():
    def check(a,b):
        if abs(a-b) < 0.00001:
            return TestPassedStyle()+"PASSED"+ShellStyles.NormalStyle()
        else:
            print ErrorStyle()+"FAILED (%f != %f)"%(a,b)+ShellStyles.NormalStyle()
            raise Exception("Error: validation test failed!")
    print ShellStyles.HighlightStyle()+"validate: UnfoldedHistogramReader\n"+ShellStyles.NormalStyle()
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
    print "validate: UnfoldedHistogramReader::getShapeForBin(): ",check(r.getShapeForBin([3,1,2],h)[2],32*3)
    print "validate: UnfoldedHistogramReader::getShapeUncertaintyForBin(): ",check(r.getShapeUncertaintyForBin([3,1,2],h)[2],sqrt(32*3))
    # Test contracted event counts
    print "validate: UnfoldedHistogramReader::getContractedEventCountForBin(): ",check(r.getContractedEventCountForBin(0,0,h),276)
    print "validate: UnfoldedHistogramReader::getContractedEventCountUncertaintyForBin(): ",check(r.getContractedEventCountUncertaintyForBin(0,0,h),sqrt(276))
    print "validate: UnfoldedHistogramReader::getContractedShapeCountForBin() test1: ",check(r.getContractedShapeForBin(2,1,h)[0],222)
    print "validate: UnfoldedHistogramReader::getContractedShapeCountUncertaintForBin() test1: ",check(r.getContractedShapeUncertaintyForBin(2,1,h)[0],sqrt(222))
    print "validate: UnfoldedHistogramReader::getContractedShapeCountForBin() test2: ",check(r.getContractedShapeForBin(2,1,h)[3],888)
    print "validate: UnfoldedHistogramReader::getContractedShapeCountUncertaintForBin() test2: ",check(r.getContractedShapeUncertaintyForBin(2,1,h)[3],sqrt(888))
