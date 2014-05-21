## \package SplittedHistoReader
#
# Purpose: Read histograms splitted by n axes in phase space
#
# Indexing starts always from zero
#
# Author: Lauri A. Wendland

import ROOT

class SplittedHistoReader:
    def __init__(self, dsetMgr, dsetLabel):
        self._binLabels = [] # Contains the label of the nth dimension
        self._binCount = []  # Contains the bin count for the nth dimension
        self._decypherBinInfo(dsetMgr, dsetLabel)

    ## Obtain splitted bin information
    def _decypherBinInfo(self, dsetMgr, dsetLabel):
        # Obtain histogram containing the split information
        mySplittedBinInfoHistoName = "SplittedBinInfo"
        dsetRootHisto = None
        try:
            dsetRootHisto = dsetMgr.getDataset(dsetLabel).getDatasetRootHisto(mySplittedBinInfoHistoName)
        except Exception, e:
            raise Exception (ShellStyles.ErrorLabel()+"Cannot find histogram '%s'!\n  Message = %s!"%(mySplittedBinInfoHistoName, str(e)))
        splittedBinInfoHisto = dsetRootHisto.getHistogram()
        ROOT.SetOwnership(splittedBinInfoHisto, True)
        # Copy splitting information with proper normalisation (to account for a merge)
        myNormalizer = splittedBinInfoHisto.GetBinContent(1)
        for i in range(2, splittedBinInfoHisto.GetNbinsX()+1):
            if splittedBinInfoHisto.GetBinContent(i) > 1:
                self._binLabels.append(splittedBinInfoHisto.GetXaxis().GetBinLabel(i))
                self._binCount.append(int(splittedBinInfoHisto.GetBinContent(i) / myNormalizer))
        splittedBinInfoHisto.Delete()

    ## Returns the maximum bin number
    def getMaxBinNumber(self):
        myProduct = 1
        for x in self._binCount:
            myProduct *= x
        return int(myProduct)

    ## Returns the splitted bin labels (returns an empty list if no splitting was done)
    def getBinLabels(self):
        return self._binLabels

    ## Returns the splitted bin sizes (returns an empty list if no splitting was done)
    def getBinSizes(self):
        return self._binCount

    ## Returns a list of histograms
    def getSplittedBinHistograms(self, dsetMgr, dsetlabel, histoName, luminosity):
        # Check the format
        if self._splittingDoneWithMultipleHistograms(dsetMgr, dsetlabel, histoName):
            # Found multiple bins, get histograms
            return self._getSplittedHistogramsFromMultipleSources(dsetMgr, dsetlabel, histoName, luminosity)
        else:
            # Assume that a single histogram contains the information
            return self._getSplittedHistogramsFromSingleSource(dsetMgr, dsetlabel, histoName, luminosity)

    ## Returns true if the splitting is done with multiple histograms
    def _splittingDoneWithMultipleHistograms(self, dsetMgr, dsetlabel, histoName):
        myNameList = histoName.split("/")
        myMultipleFileName = histoName+"/"+myNameList[len(myNameList)-1]+"0"
        myMultipleFilesStatus = dsetMgr.getDataset(dsetlabel).hasRootHisto(histoName)
        return myMultipleFilesStatus

    ## Returns a list of histograms (one per split bin, in the same order)
    # I.e. vector<WrappedTHn*> -> list of THn's (THn = TH1, TH2, ...)
    def _getSplittedHistogramsFromMultipleSources(self, dsetMgr, dsetlabel, histoName, luminosity):
        myHistoList = []
        myNameList = histoName.split("/")
        myMultipleFileNameStem = histoName+"/"+myNameList[len(myNameList)-1]
        for i in range(0, self.getMaxBinNumber()):
            myDsetRootHisto = dsetMgr.getDataset(dsetlabel).getDatasetRootHisto(myMultipleFileNameStem+str(i))
            if dsetMgr.getDataset(dsetlabel).isMC():
                myDsetRootHisto.normalizeToLuminosity(luminosity)
            h = myDsetRootHisto.getHistogram()
            ROOT.SetOwnership(h, True)
            myHistoList.append(h)
        return myHistoList

    ## Deconstructs a 2D histogram into a list of histograms (one per split bin, in the same order)
    # I.e. WrappedUnfoldedFactorisationHisto (= TH2 with factorisation bin on y-axis) -> list of TH1's
    # Limitation: can only use 1D shapes
    def _getSplittedHistogramsFromSingleSource(self, dsetMgr, dsetlabel, histoName, luminosity):
        myHistoList = []
        myNameList = histoName.split("/")
        myNameStem = myNameList[len(myNameList)-1]
        myDsetRootHisto = dsetMgr.getDataset(dsetlabel).getDatasetRootHisto(histoName)
        if dsetMgr.getDataset(dsetlabel).isMC():
            myDsetRootHisto.normalizeToLuminosity(luminosity)
        myHisto = myDsetRootHisto.getHistogram()
        for i in range(0, self.getMaxBinNumber()):
            myName = myNameStem+"_"+dsetlabel+"_"+str(i)
            h = ROOT.TH1F(myName, myHisto.GetYaxis().GetBinLabel(i+1), myHisto.GetXaxis().GetNbins(), myHisto.GetXaxis().GetXmin(), myHisto.GetXaxis().GetXmin())
            h.Sumw2()
            for j in range(0, myHisto.GetXaxis().GetNbins()+2):
                h.SetBinContent(j, myHisto.GetBinContent(j, i+1))
                h.SetBinError(j, myHisto.GetBinError(j, i+1))
            ROOT.SetOwnership(h, True)
            myHistoList.append(h)
        return myHistoList # do the histograms disappear from memory???
