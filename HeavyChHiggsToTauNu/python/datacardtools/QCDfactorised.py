## \package QCDfactorised
# Classes for extracting and calculating multijet background with factorised approach

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.Extractor import ExtractorMode,ExtractorBase
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardColumn import ExtractorResult,DatacardColumn
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.MulticrabPathFinder import MulticrabDirectoryDataType
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import Count
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.ShapeHistoModifier import *
from math import pow,sqrt
import os
import sys
import ROOT

## Extracts data-MC EWK counts from a given point in the analysis
class QCDEventCount():
    def __init__(self,
                 histoPrefix,
                 histoName,
                 dsetMgr,
                 dsetMgrDataColumn,
                 dsetMgrMCEWKColumn,
                 luminosity,
                 assumedMCEWKSystUncertainty):
        self._histoname = histoName
        self._assumedMCEWKSystUncertainty = assumedMCEWKSystUncertainty
        # Obtain histograms
        datasetRootHistoData = dsetMgr.getDataset(dsetMgrDataColumn).getDatasetRootHisto(histoPrefix+"/"+histoName)
        datasetRootHistoMCEWK = dsetMgr.getDataset(dsetMgrMCEWKColumn).getDatasetRootHisto(histoPrefix+"/"+histoName)
        datasetRootHistoMCEWK.normalizeToLuminosity(luminosity)
        self._hData = datasetRootHistoData.getHistogram()
        self._hMC = datasetRootHistoMCEWK.getHistogram()
        self._messages = []
        self._messagesFromQCDCount = False

    def clean(self):
        if self._hData != None:
            self._hData.IsA().Destructor(self._hData)
        if self._hMC != None:
            self._hMC.IsA().Destructor(self._hMC)
        self._messages = []

    def getMessages(self):
        return self._messages

    def is1D(self):
        return (isinstance(self._hData,ROOT.TH1F) or isinstance(self._hData,ROOT.TH1D)) and not is2D()

    def is2D(self):
        return (isinstance(self._hData,ROOT.TH2F) or isinstance(self._hData,ROOT.TH2D)) and not is3D()

    def is3D(self):
        return isinstance(self._hData,ROOT.TH3F) or isinstance(self._hData,ROOT.TH3D)

    def getNbinsX(self):
        return self._hData.GetNbinsX()

    def getNbinsY(self):
        return self._hData.GetNbinsY()

    def getNbinsZ(self):
        return self._hData.GetNbinsZ()

    def getTotalDimension(self):
        return self.getNbinsX()*self.getNbinsY()*self.getNbinsZ()

    def getClonedHisto(self, name):
        return self._hData.Clone(name)

    def getBinLabel(self,axis,idx):
        if axis == "X":
            return self._hData.GetXaxis().GetBinLabel(idx)
        elif axis == "Y":
            return self._hData.GetYaxis().GetBinLabel(idx)
        elif axis == "Z":
            return self._hData.GetZaxis().GetBinLabel(idx)
        raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" getBinLabel only supports axes X, Y, or Z!")

    ## Returns number of events for data
    def getDataCount(self,idx,idy=-1,idz=-1):
        if self.is3D():
            return self._hData.GetBinContent(idx,idy,idz)
        elif self.is2D():
            return self._hData.GetBinContent(idx,idy)
        elif self.is1D():
            return self._hData.GetBinContent(idx)
        else:
            Exception(ErrorStyle()+"QCD factorised / factorisation data has more than 3 dimensions!"+NormalStyle())

    def getContracted1DDataCount(self,idx,axis="X"):
        myCount = 0.0
        if self.is3D():
            if axis == "X":
                for j in range(1,self.getNbinsY()+1):
                    for k in range(1,self.getNbinsZ()+1):
                        myCount += self._hData.GetBinContent(idx,j,k)
            elif axis == "Y":
                for i in range(1,self.getNbinsX()+1):
                    for k in range(1,self.getNbinsZ()+1):
                        myCount += self._hData.GetBinContent(i,idx,k)
            elif axis == "Z":
                for i in range(1,self.getNbinsX()+1):
                    for j in range(1,self.getNbinsY()+1):
                        myCount += self._hData.GetBinContent(i,j,idx)
            else:
              raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" valid options for axis are X, Y, and Z (you tried '"+axis+"')")
        elif self.is2D():
            if axis == "X":
                for j in range(1,self.getNbinsY()+1):
                    myCount += self._hData.GetBinContent(idx,j)
            elif axis == "Y":
                for i in range(1,self.getNbinsX()+1):
                    myCount += self._hData.GetBinContent(i,idx)
            else:
              raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" valid options for axis are X, Y, and Z (you tried '"+axis+"')")
        elif self.is1D():
            myCount += self._hData.GetBinContent(idx)
        return myCount

    ## Returns number of events for MC
    def getMCCount(self,idx,idy=-1,idz=-1):
        if self.is3D():
            return self._hMC.GetBinContent(idx,idy,idz)
        elif self.is2D():
            return self._hMC.GetBinContent(idx,idy)
        elif self.is1D():
            return self._hMC.GetBinContent(idx)
        else:
            Exception(ErrorStyle()+"QCD factorised / factorisation data has more than 3 dimensions!"+NormalStyle())

    def getContracted1DMCCount(self,idx,axis="X"):
        myCount = 0.0
        if self.is3D():
            if axis == "X":
                for j in range(1,self.getNbinsY()+1):
                    for k in range(1,self.getNbinsZ()+1):
                        myCount += self._hMC.GetBinContent(idx,j,k)
            elif axis == "Y":
                for i in range(1,self.getNbinsX()+1):
                    for k in range(1,self.getNbinsZ()+1):
                        myCount += self._hMC.GetBinContent(i,idx,k)
            elif axis == "Z":
                for i in range(1,self.getNbinsX()+1):
                    for j in range(1,self.getNbinsY()+1):
                        myCount += self._hMC.GetBinContent(i,j,idx)
            else:
              raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" valid options for axis are X, Y, and Z (you tried '"+axis+"')")
        elif self.is2D():
            if axis == "X":
                for j in range(1,self.getNbinsY()+1):
                    myCount += self._hMC.GetBinContent(idx,j)
            elif axis == "Y":
                for i in range(1,self.getNbinsX()+1):
                    myCount += self._hMC.GetBinContent(i,idx)
            else:
              raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" valid options for axis are X, Y, and Z (you tried '"+axis+"')")
        elif self.is1D():
            myCount += self._hMC.GetBinContent(idx)
        return myCount

    ## Returns stat. error (data only)
    def getDataError(self,idx,idy=-1,idz=-1):
        if self.is3D():
            return self._hData.GetBinError(idx,idy,idz)
        elif self.is2D():
            return self._hData.GetBinError(idx,idy)
        elif self.is1D():
            return self._hData.GetBinError(idx)
        else:
            Exception(ErrorStyle()+"QCD factorised / factorisation data has more than 3 dimensions!"+NormalStyle())

    def getContracted1DDataError(self,idx,axis="X"):
        myUncert = 0.0
        if self.is3D():
            if axis == "X":
                for j in range(1,self.getNbinsY()+1):
                    for k in range(1,self.getNbinsZ()+1):
                        myUncert += (self._hData.GetBinError(idx,j,k))**2
            elif axis == "Y":
                for i in range(1,self.getNbinsX()+1):
                    for k in range(1,self.getNbinsZ()+1):
                        myUncert += (self._hData.GetBinError(i,idx,k))**2
            elif axis == "Z":
                for i in range(1,self.getNbinsX()+1):
                    for j in range(1,self.getNbinsY()+1):
                        myUncert += (self._hData.GetBinError(i,j,idx))**2
            else:
              raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" valid options for axis are X, Y, and Z (you tried '"+axis+"')")
        elif self.is2D():
            if axis == "X":
                for j in range(1,self.getNbinsY()+1):
                    myUncert += (self._hData.GetBinError(idx,j))**2
            elif axis == "Y":
                for i in range(1,self.getNbinsX()+1):
                    myUncert += (self._hData.GetBinError(i,idx))**2
            else:
              raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" valid options for axis are X, Y, and Z (you tried '"+axis+"')")
        elif self.is1D():
            myUncert += (self._hData.GetBinError(idx))**2
        return sqrt(myUncert)

    ## Returns stat. error (MC only)
    def getMCStatError(self,idx,idy=-1,idz=-1):
        if self.is3D():
            return self._hMC.GetBinError(idx,idy,idz)
        elif self.is2D():
            return self._hMC.GetBinError(idx,idy)
        elif self.is1D():
            return self._hMC.GetBinError(idx)
        else:
            Exception(ErrorStyle()+"QCD factorised / factorisation data has more than 3 dimensions!"+NormalStyle())

    def getContracted1DMCStatError(self,idx,axis="X"):
        myUncert = 0.0
        if self.is3D():
            if axis == "X":
                for j in range(1,self.getNbinsY()+1):
                    for k in range(1,self.getNbinsZ()+1):
                        myUncert += (self._hMC.GetBinError(idx,j,k))**2
            elif axis == "Y":
                for i in range(1,self.getNbinsX()+1):
                    for k in range(1,self.getNbinsZ()+1):
                        myUncert += (self._hMC.GetBinError(i,idx,k))**2
            elif axis == "Z":
                for i in range(1,self.getNbinsX()+1):
                    for j in range(1,self.getNbinsY()+1):
                        myUncert += (self._hMC.GetBinError(i,j,idx))**2
            else:
              raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" valid options for axis are X, Y, and Z (you tried '"+axis+"')")
        elif self.is2D():
            if axis == "X":
                for j in range(1,self.getNbinsY()+1):
                    myUncert += (self._hMC.GetBinError(idx,j))**2
            elif axis == "Y":
                for i in range(1,self.getNbinsX()+1):
                    myUncert += (self._hMC.GetBinError(i,idx))**2
            else:
              raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" valid options for axis are X, Y, and Z (you tried '"+axis+"')")
        elif self.is1D():
            myUncert += (self._hMC.GetBinError(idx))**2
        return sqrt(myUncert)

    ## Returns syst. error (MC only)
    def getMCSystError(self,idx,idy=-1,idz=-1):
        if self.is3D():
            return self._hMC.GetBinContent(idx,idy,idz) * self._assumedMCEWKSystUncertainty
        elif self.is2D():
            return self._hMC.GetBinContent(idx,idy) * self._assumedMCEWKSystUncertainty
        elif self.is1D():
            return self._hMC.GetBinContent(idx) * self._assumedMCEWKSystUncertainty
        else:
            Exception(ErrorStyle()+"QCD factorised / factorisation data has more than 3 dimensions!"+NormalStyle())

    def getContracted1DMCSystError(self,idx,axis="X"):
        return self.getContracted1DMCCount(idx,axis) * self._assumedMCEWKSystUncertainty

    ## Returns stat.+syst. uncertainty
    def getTotalError(self,idx,idy=-1,idz=-1):
        myDataError = self.getDataError(idx,idy,idz)
        myMCStatError = self.getMCStatError(idx,idy,idz)
        myMCSystError = self.getMCSystError(idx,idy,idz)
        myResultError = sqrt(pow(myDataError,2) + pow(myMCStatError,2) + pow(myMCSystError,2))
        return myResultError

    ## Returns Count object for data-MC (uncertainty = stat.+syst. uncertainty)
    def getQCDCount(self,idx,idy=-1,idz=-1):
        # Obtain value and its uncertainty
        myData = self.getDataCount(idx,idy,idz)
        myMC = self.getMCCount(idx,idy,idz)
        myResultError = sqrt(pow(self.getDataError(idx,idy,idz),2)+pow(self.getMCStatError(idx,idy,idz),2))
        myResult = myData - myMC
        # Obtain uncertainty # Check negative result
        if myResult < 0:
            myMsg = WarningStyle()+"Warning:"+NormalStyle()+" QCD factorised: negative count (setting to zero) for %s bin (%s=%s"%(self._histoname, self._hData.GetXaxis().GetTitle(), self._hData.GetXaxis().GetBinLabel(idx))
            if (idy>-1):
                myMsg += "; %s=%s"%(self._hData.GetYaxis().GetTitle(), self._hData.GetYaxis().GetBinLabel(idy))
            if (idz>-1):
                myMsg += "; %s=%s"%(self._hData.GetZaxis().GetTitle(), self._hData.GetZaxis().GetBinLabel(idz))
            myMsg += ") (data=%f, MC=%f, result=%f)"%(myData, myMC, myResult)
            self._messages.append(myMsg)
            myResult = 0.0
            #myResultError = 0.0 do not set it to zero, but instead keep it as it is to be more realistic!
        self._messagesFromQCDCount = True
        # Return result 
        return Count(myResult,myResultError)

    ## Returns the count object for data-MC for a bin on first variation parameter, other parameters are contracted (i.e. summed)
    ## (uncertainty = stat.+syst. uncertainty)
    def getContracted1DQCDCount(self,idx,axis="X"):
        # Obtain value and its uncertainty
        myData = self.getContracted1DDataCount(idx,axis)
        myMC = self.getContracted1DMCCount(idx,axis)
        myResult = myData - myMC
        myResultError = sqrt(pow(self.getContracted1DDataError(idx,axis),2)+
                             pow(self.getContracted1DMCStatError(idx,axis),2))
        # Obtain uncertainty # Check negative result
        if myResult < 0:
            myResult = 0.0
            #myResultError = 0.0 do not set it to zero, but instead keep it as it is to be more realistic!
        # Return result
        return Count(myResult,myResultError)

    ## Getter for purity of 1-dimensional factorisation
    # Returns Count object for (data-MC)/data
    def getPurity(self,idx,idy=-1,idz=-1):
        myData = self.getDataCount(idx,idy,idz)
        myDataError = self.getDataError(idx,idy,idz)
        myMC = self.getMCCount(idx,idy,idz)
        myMCError = self.getMCStatError(idx,idy,idz)
        myQCD = myData - myMC
        myQCDError = sqrt(pow(myDataError,2)+pow(myMCError,2))
        if myData > 0 and myQCD > 0:
          myResult = myQCD / myData
          myResultError = myResult*sqrt(pow(myQCDError/myQCD,2)+pow(myDataError/myData,2))
        else:
          myResult = 0.0
          myResultError = 0.0
        return Count(myResult,myResultError)

    def getContracted1DPurity(self,idx,axis="X"):
        myData = self.getContracted1DDataCount(idx,"X")
        myDataError = self.getContracted1DDataError(idx,"X")
        myMC = self.getContracted1DMCCount(idx,"X")
        myMCError = self.getContracted1DMCStatError(idx,"X")
        myQCD = myData - myMC
        myQCDError = sqrt(pow(myDataError,2)+pow(myMCError,2))
        if myData > 0 and myQCD > 0:
          myResult = myQCD / myData
          myResultError = myResult*sqrt(pow(myQCDError/myQCD,2)+pow(myDataError/myData,2))
        else:
          myResult = 0.0
          myResultError = 0.0
        return Count(myResult,myResultError)

    ## Returns a purity histogram
    def getPurityHistogram(self):
        hlist = []
        if self.is3D():
            myName = "purity_"+self._histoname.replace("/","_")+"_Total"
            hTot = ROOT.TH2F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY(),self._hData.GetNbinsX()*self._hData.GetNbinsZ(),0,self._hData.GetNbinsX()*self._hData.GetNbinsZ())
            myName = "purity_"+self._histoname.replace("/","_")+"_contractedX"
            hContractedX = ROOT.TH1F(myName,myName,self._hData.GetNbinsX(),0,self._hData.GetNbinsX())
            for i in range(1,self._hData.GetNbinsX()+1):
                # Fill contracted histogram
                myContractedPurity = self.getContracted1DPurity(i,"X")
                hContractedX.SetBinContent(i, myContractedPurity.value())
                hContractedX.SetBinError(i, myContractedPurity.uncertainty())
                hContractedX.GetXaxis().SetBinLabel(i,self._hData.GetXaxis().GetBinLabel(i))
                hContractedX.SetYTitle("Purity")
                # Generate one 2D histo for each x bin
                myName = "purity_"+self._histoname.replace("/","_")+"_bin_%d"%(i)
                h = ROOT.TH2F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY(),self._hData.GetNbinsZ(),0,self._hData.GetNbinsZ())
                h.SetZTitle("Purity")
                for j in range(1, self._hData.GetNbinsY()+1):
                    h.GetXaxis().SetBinLabel(j,self._hData.GetYaxis().GetBinLabel(j))
                    hTot.GetXaxis().SetBinLabel(j,self._hData.GetYaxis().GetBinLabel(j))
                for k in range(1, self._hData.GetNbinsZ()+1):
                    h.GetYaxis().SetBinLabel(k,self._hData.GetZaxis().GetBinLabel(k))
                    hTot.GetYaxis().SetBinLabel(k+(i-1)*self._hData.GetNbinsZ(), "("+self._hData.GetXaxis().GetBinLabel(i)+"; "+self._hData.GetZaxis().GetBinLabel(k)+")")
                # Calculate and fill purity
                for j in range(1,self._hData.GetNbinsY()+1):
                    for k in range(1,self._hData.GetNbinsZ()+1):
                        myPurity = self.getPurity(i,j,k)
                        #print "Debug: QCD factorised: Purity in %f bin %d,%d,%d"%(myPurity.value(),i,j,k)
                        h.SetBinContent(j, k, myPurity.value())
                        h.SetBinError(j, k, myPurity.uncertainty())
                        hTot.SetBinContent(j, k+(i-1)*self._hData.GetNbinsZ(), myPurity.value())
                        hTot.SetBinError(j, k+(i-1)*self._hData.GetNbinsZ(), myPurity.uncertainty())
                        if myPurity.value() > 0.0 and myPurity.value() < 0.5:
                            print WarningStyle()+"Warning: QCD factorised: Purity in %s bin %d,%d,%d is low (%f +- %f)!"%(self._histoname,i,j,k,myPurity.value(),myPurity.uncertainty())+NormalStyle()
                hlist.append(h)
            hlist.append(hTot)
            hlist.append(hContractedX)
        elif self.is2D():
            h = self._hData.Clone("purity_"+self._histoname.replace("/","_"))
            h.Reset()
            h.SetZTitle("Purity")
            for i in range(1,h.GetNbinsX()+1):
                for j in range(1,h.GetNbinsY()+1):
                    myPurity = self.getPurity(i,j)
                    h.SetBinContent(i, j, myPurity.value())
                    h.SetBinError(i, j, myPurity.uncertainty())
                    if myPurity.value() > 0.0 and myPurity.value() < 0.5:
                        print WarningStyle()+"Warning: QCD factorised: Purity in %s bin %d,%d is low (%f +- %f)!"%(self._histoname,i,j,myPurity.value(),myPurity.uncertainty())+NormalStyle()
            hlist.append(h)
        elif self.is1D():
            h = self._hData.Clone("purity_"+self._histoname.replace("/","_"))
            h.Reset()
            h.SetYTitle("Purity")
            for i in range(1,h.GetNbinsX()+1):
                myPurity = self.getPurity(i)
                h.SetBinContent(i, myPurity.value())
                h.SetBinError(i, myPurity.uncertainty())
                if myPurity.value() > 0.0 and myPurity.value() < 0.5:
                    print WarningStyle()+"Warning: QCD factorised: Purity in %s bin %d is low (%f +- %f)!"%(self._histoname,i,myPurity.value(),myPurity.uncertainty())+NormalStyle()
            hlist.append(h)
        else:
            raise Exception(ErrorStyle()+"QCD factorised / factorisation data has more than 3 dimensions!"+NormalStyle())
        return hlist

    ## Returns histogram(s) for number of events
    def getEventCountHistograms(self):
        hlist = []
        if self.is1D():
            h = self._hData.Clone("QCDeventCount_"+self._histoname.replace("/","_"))
            h.Reset()
            h.SetYTitle("NQCD")
            for i in range(1,h.GetNbinsX()+1):
                myData = self.getDataCount(i)
                myMC = self.getMCCount(i)
                myResultError = sqrt(pow(self.getDataError(i),2)+pow(self.getMCStatError(i),2))
                myResult = myData - myMC
                h.SetBinContent(i, myResult)
                h.SetBinError(i, myResultError)
            hlist.append(h)
        elif self.is2D():
            h = self._hData.Clone("QCDeventCount_"+self._histoname.replace("/","_"))
            h.Reset()
            h.SetZTitle("NQCD")
            for i in range(1,h.GetNbinsX()+1):
                for j in range(1,h.GetNbinsY()+1):
                    myData = self.getDataCount(i,j)
                    myMC = self.getMCCount(i,j)
                    myResultError = sqrt(pow(self.getDataError(i,j),2)+pow(self.getMCStatError(i,j),2))
                    myResult = myData - myMC
                    h.SetBinContent(i, j, myResult)
                    h.SetBinError(i, j, myResultError)
            hlist.append(h)
        elif self.is3D():
            myName = "QCDeventCount_"+self._histoname.replace("/","_")+"_Total"
            hTot = ROOT.TH2F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY(),self._hData.GetNbinsX()*self._hData.GetNbinsZ(),0,self._hData.GetNbinsX()*self._hData.GetNbinsZ())
            for i in range(1,self._hData.GetNbinsX()+1):
                # Generate one 2D histo for each x bin
                myName = "QCDeventCount_"+self._histoname.replace("/","_")+"_bin_%d"%(i)
                h = ROOT.TH2F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY(),self._hData.GetNbinsZ(),0,self._hData.GetNbinsZ())
                h.SetZTitle("NQCD")
                for j in range(1, self._hData.GetNbinsY()+1):
                    h.GetXaxis().SetBinLabel(j,self._hData.GetYaxis().GetBinLabel(j))
                    hTot.GetXaxis().SetBinLabel(j,self._hData.GetYaxis().GetBinLabel(j))
                for k in range(1, self._hData.GetNbinsZ()+1):
                    h.GetYaxis().SetBinLabel(k,self._hData.GetZaxis().GetBinLabel(k))
                    hTot.GetYaxis().SetBinLabel(k+(i-1)*self._hData.GetNbinsZ(), "("+self._hData.GetXaxis().GetBinLabel(i)+"; "+self._hData.GetZaxis().GetBinLabel(k)+")")
                # Calculate and fill result
                for j in range(1,self._hData.GetNbinsY()+1):
                    for k in range(1,self._hData.GetNbinsZ()+1):
                        myData = self.getDataCount(i,j,k)
                        myMC = self.getMCCount(i,j,k)
                        myResultError = sqrt(pow(self.getDataError(i,j,k),2)+pow(self.getMCStatError(i,j,k),2))
                        myResult = myData - myMC
                        h.SetBinContent(j, k, myResult)
                        h.SetBinError(j, k, myResultError)
                        hTot.SetBinContent(j, k+(i-1)*self._hData.GetNbinsZ(), myResult)
                        hTot.SetBinError(j, k+(i-1)*self._hData.GetNbinsZ(), myResultError)
                hlist.append(h)
            hlist.append(hTot)
        else:
            raise Exception(ErrorStyle()+"QCD factorised / factorisation data has more than 3 dimensions!"+NormalStyle())
        return hlist


    ## Returns histogram(s) for checking the impact of negative QCD counts
    def getNegativeEventCountHistograms(self):
        hlist = []
        mySum = 0.0
        if self.is1D():
            h = self._hData.Clone("QCDeventCountNegativeImpact_"+self._histoname.replace("/","_"))
            h.Reset()
            h.SetYTitle("NQCD")
            for i in range(1,h.GetNbinsX()+1):
                myData = self.getDataCount(i)
                myMC = self.getMCCount(i)
                myResultError = sqrt(pow(self.getDataError(i),2)+pow(self.getMCStatError(i),2))
                myResult = myData - myMC
                if myResult < 0: # Fill only negative values and relate them to the total nQCD
                    h.SetBinContent(i, myResult)
                    h.SetBinError(i, myResultError)
                else:
                    mySum += myResult
            hlist.append(h)
        elif self.is2D():
            h = self._hData.Clone("QCDeventCountNegativeImpact_"+self._histoname.replace("/","_"))
            h.Reset()
            h.SetZTitle("NQCD")
            for i in range(1,h.GetNbinsX()+1):
                for j in range(1,h.GetNbinsY()+1):
                    myData = self.getDataCount(i,j)
                    myMC = self.getMCCount(i,j)
                    myResultError = sqrt(pow(self.getDataError(i,j),2)+pow(self.getMCStatError(i,j),2))
                    myResult = myData - myMC
                    if myResult < 0: # Fill only negative values and relate them to the total nQCD
                        h.SetBinContent(i, j, myResult)
                        h.SetBinError(i, j, myResultError)
                    else:
                        mySum += myResult
            hlist.append(h)
        elif self.is3D():
            myName = "QCDeventCountNegativeImpact_"+self._histoname.replace("/","_")+"_Total"
            hTot = ROOT.TH2F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY(),self._hData.GetNbinsX()*self._hData.GetNbinsZ(),0,self._hData.GetNbinsX()*self._hData.GetNbinsZ())
            for i in range(1,self._hData.GetNbinsX()+1):
                # Generate one 2D histo for each x bin
                myName = "QCDeventCountNegativeImpact_"+self._histoname.replace("/","_")+"_bin_%d"%(i)
                h = ROOT.TH2F(myName,myName,self._hData.GetNbinsY(),0,self._hData.GetNbinsY(),self._hData.GetNbinsZ(),0,self._hData.GetNbinsZ())
                h.SetZTitle("NQCD")
                for j in range(1, self._hData.GetNbinsY()+1):
                    h.GetXaxis().SetBinLabel(j,self._hData.GetYaxis().GetBinLabel(j))
                    hTot.GetXaxis().SetBinLabel(j,self._hData.GetYaxis().GetBinLabel(j))
                for k in range(1, self._hData.GetNbinsZ()+1):
                    h.GetYaxis().SetBinLabel(k,self._hData.GetZaxis().GetBinLabel(k))
                    hTot.GetYaxis().SetBinLabel(k+(i-1)*self._hData.GetNbinsZ(), "("+self._hData.GetXaxis().GetBinLabel(i)+"; "+self._hData.GetZaxis().GetBinLabel(k)+")")
                # Calculate and fill result
                for j in range(1,self._hData.GetNbinsY()+1):
                    for k in range(1,self._hData.GetNbinsZ()+1):
                        myData = self.getDataCount(i,j,k)
                        myMC = self.getMCCount(i,j,k)
                        myResultError = sqrt(pow(self.getDataError(i,j,k),2)+pow(self.getMCStatError(i,j,k),2))
                        myResult = myData - myMC
                        if myResult < 0: # Fill only negative values and relate them to the total nQCD
                            h.SetBinContent(j, k, myResult)
                            h.SetBinError(j, k, myResultError)
                            hTot.SetBinContent(j, k+(i-1)*self._hData.GetNbinsZ(), myResult)
                            hTot.SetBinError(j, k+(i-1)*self._hData.GetNbinsZ(), myResultError)
                        else:
                            mySum += myResult
                hlist.append(h)
            hlist.append(hTot)
        else:
            raise Exception(ErrorStyle()+"QCD factorised / factorisation data has more than 3 dimensions!"+NormalStyle())
        if mySum > 0:
            for histo in hlist:
                histo.Scale(1.0/mySum)
        return hlist

## Helper class for calculating the result from three points of counting in the analysis
class QCDfactorisedCalculator():
    def __init__(self, basicCounts, leg1Counts, leg2Counts, doHistograms=False):
        # NQCD with full parameter space
        self._NQCD = 0.0
        self._dataUncertainty = 0.0
        self._MCStatUncertainty = 0.0
        self._MCSystUncertainty = 0.0

        # NQCD with only first parameter (others contracted)
        self._contractedNQCD = {}
        self._contractedDataUncertainty = {}
        self._contractedMCStatUncertainty = {}
        self._contractedMCSystUncertainty = {}

        self._basicCount = basicCounts
        self._leg1Counts = leg1Counts
        self._leg2Counts = leg2Counts

        self._yieldTable = ""
        self._compactYieldTable = ""

        # Count NQCD
        self._nQCDHistograms = []
        self._count(basicCounts, leg1Counts, leg2Counts, doHistograms)
        # Count NQCD by doing first contraction to one axis
        self._contractedCount(basicCounts, leg1Counts, leg2Counts, "X", doHistograms)
        if basicCounts.is2D() or basicCounts.is3D():
            self._contractedCount(basicCounts, leg1Counts, leg2Counts, "Y", doHistograms)
        if basicCounts.is3D():
            self._contractedCount(basicCounts, leg1Counts, leg2Counts, "Z", doHistograms)

        # Make yield tables
        if doHistograms:
            self._yieldTable = self._createYieldTable()
            self._compactYieldTable = self._createCompactYieldTable()

    def clean(self):
        self._basicCount.clean()
        self._leg1Counts.clean()
        self._leg2Counts.clean()

    def getCompactYieldTable(self):
        return self._compactYieldTable

    def getYieldTable(self):
        return self._yieldTable

    def getNQCD(self):
        return self._NQCD

    def getContractedNQCD(self,axis):
        return self._contractedNQCD[axis]

    def getNQCDHistograms(self):
        return self._nQCDHistograms

    def getDataUncertainty(self):
        return self._dataUncertainty / self._NQCD

    def getMCStatUncertainty(self):
        return self._MCStatUncertainty / self._NQCD

    def getMCSystUncertainty(self):
        return self._MCSystUncertainty / self._NQCD

    def getStatUncertainty(self):
        return sqrt(pow(self._dataUncertainty,2)+pow(self._MCStatUncertainty,2)) / self._NQCD

    def getSystUncertainty(self):
        return self.getMCSystUncertainty()

    def getContractedStatUncertainty(self,axis):
        return sqrt(pow(self._contractedDataUncertainty[axis],2)+pow(self._contractedMCStatUncertainty[axis],2)) / self._contractedNQCD[axis]

    def getContractedSystUncertainty(self,axis):
        return self._contractedMCSystUncertainty[axis] / self._contractedNQCD[axis]

    def getTotalUncertainty(self):
        return sqrt(pow(self._dataUncertainty,2)+pow(self._MCStatUncertainty,2)+pow(self._getMCSystUncertainty,2)) / self._NQCD

    def getLeg1Efficiency(self,idx,idy=-1,idz=-1):
        return self._getEfficiency(self._leg1Counts, self._basicCount,idx,idy,idz)

    def getLeg2Efficiency(self,idx,idy=-1,idz=-1):
        return self._getEfficiency(self._leg2Counts, self._basicCount,idx,idy,idz)

    def _getEfficiency(self,nominator,denominator,idx,idy=-1,idz=-1):
        myValue = -1.0
        myError = 0.0
        nominatorCount = nominator.getQCDCount(idx,idy,idz)
        denominatorCount = denominator.getQCDCount(idx,idy,idz)
        if denominatorCount.value() > 0 and nominatorCount.value() > 0:
            myValue = nominatorCount.value() / denominatorCount.value()
            myError = myValue*sqrt(pow(nominatorCount.uncertainty()/nominatorCount.value(),2)+pow(denominatorCount.uncertainty()/denominatorCount.value(),2))
            #print "1D eff: nom=%f, denom=%f, value=%f +- %f:"%(nominatorCount.value(),denominatorCount.value(),myValue,myError)
        return Count(myValue,myError)

    def getContracted1DLeg1Efficiency(self,idx,axis):
        return self._getContracted1DEfficiency(self._leg1Counts,self._basicCount,idx,axis)

    def getContracted1DLeg2Efficiency(self,idx,axis):
        return self._getContracted1DEfficiency(self._leg2Counts,self._basicCount,idx,axis)

    ## Returns the efficiency for a bin on first variation parameter, other parameters are contracted (i.e. summed)
    def _getContracted1DEfficiency(self,nominator,denominator,idx,axis):
        myValue = -1.0
        myError = 0.0
        nominatorCount = nominator.getContracted1DQCDCount(idx,axis)
        denominatorCount = denominator.getContracted1DQCDCount(idx,axis)
        if denominatorCount.value() > 0 and nominatorCount.value() > 0:
            myValue = nominatorCount.value() / denominatorCount.value()
            myError = myValue*sqrt(pow(nominatorCount.uncertainty()/nominatorCount.value(),2)+pow(denominatorCount.uncertainty()/denominatorCount.value(),2))
            #print "1D eff: nom=%f, denom=%f, value=%f +- %f:"%(nominatorCount.value(),denominatorCount.value(),myValue,myError)
        return Count(myValue,myError)

    def getLeg1EfficiencyHistogram(self):
        return self._createEfficiencyHistogram(self._leg1Counts, self._basicCount, "leg1")

    def getLeg2EfficiencyHistogram(self):
        return self._createEfficiencyHistogram(self._leg2Counts, self._basicCount, "leg2")

    def _createEfficiencyHistogram(self, nominator, denominator, suffix=""):
        # Create histogram
        hlist = []
        if nominator.is1D():
            h = nominator.getClonedHisto("QCDfactEff_"+suffix)
            h.Reset()
            h.SetYTitle("Efficiency")
            for i in range(1, h.GetNbinsX()+1):
                myEfficiency = self._getEfficiency(nominator,denominator,i)
                if myEfficiency.value() > 0:
                    h.SetBinContent(i, myEfficiency.value())
                    h.SetBinError(i, myEfficiency.uncertainty())
            hlist.append(h)
        elif nominator.is2D():
            h = nominator.getClonedHisto("QCDfactEff_"+suffix)
            h.Reset()
            h.SetZTitle("Efficiency")
            for i in range(1, h.GetNbinsX()+1):
                for j in range(1, h.GetNbinsY()+1):
                    myEfficiency = self._getEfficiency(nominator,denominator,i,j)
                    if myEfficiency.value() > 0:
                        h.SetBinContent(i, j, myEfficiency.value())
                        h.SetBinError(i, j, myEfficiency.uncertainty())
            hlist.append(h)
        elif nominator.is3D():
            myName = "QCDfactEff_"+suffix+"_Total"
            hTot = ROOT.TH2F(myName,myName,nominator.getNbinsY(),0,nominator.getNbinsY(),nominator.getNbinsX()*nominator.getNbinsZ(),0,nominator.getNbinsX()*nominator.getNbinsZ())
            for i in range(1, nominator.getNbinsX()+1):
                # Generate one 2D histo for each x bin
                myName = "QCDfactEff_"+suffix+"_bin_%d"%(i)
                h = ROOT.TH2F(myName,myName,nominator.getNbinsY(),0,nominator.getNbinsY(),nominator.getNbinsZ(),0,nominator.getNbinsZ())
                h.SetZTitle("Efficiency")
                for j in range(1, nominator.getNbinsY()+1):
                    h.GetXaxis().SetBinLabel(j,nominator.getBinLabel("Y",j))
                    hTot.GetXaxis().SetBinLabel(j,nominator.getBinLabel("Y",j))
                for k in range(1, nominator.getNbinsZ()+1):
                    h.GetYaxis().SetBinLabel(k,nominator.getBinLabel("Z",k))
                    hTot.GetYaxis().SetBinLabel(k+(i-1)*nominator.getNbinsZ(),"("+nominator.getBinLabel("X",i)+"; "+nominator.getBinLabel("Z",k))
                # Calculate and fill efficiency
                for j in range(1, nominator.getNbinsY()+1):
                    for k in range(1, nominator.getNbinsZ()+1):
                        myEfficiency = self._getEfficiency(nominator,denominator,i,j,k)
                        if myEfficiency.value() > 0:
                            h.SetBinContent(j, k, myEfficiency.value())
                            h.SetBinError(j, k, myEfficiency.uncertainty())
                            hTot.SetBinContent(j, k+(i-1)*nominator.getNbinsZ(), myEfficiency.value())
                            hTot.SetBinError(j, k+(i-1)*nominator.getNbinsZ(), myEfficiency.uncertainty())
                hlist.append(h)
            hlist.append(hTot)
        else:
             raise Exception(ErrorStyle()+"Warning: QCD:Factorised: Efficiency histogram not yet supported for more than 1 dimensions"+NormalStyle())
        return hlist

    def getNQCDForBin(self,idx,idy=-1,idz=-1):
        myBasicCounts = self._basicCount.getQCDCount(idx,idy,idz).value()
        myLeg1Counts = self._leg1Counts.getQCDCount(idx,idy,idz).value()
        myLeg2Counts = self._leg2Counts.getQCDCount(idx,idy,idz).value()
        myCount = 0.0
        myDataUncert = 0.0
        myMCStatUncert = 0.0
        myMCSystUncert = 0.0
        # Protect calculation against div by zero
        if (myBasicCounts > 0.0):
            myCount = myLeg1Counts * myLeg2Counts / myBasicCounts
            # Calculate uncertainty as f=a*b  (i.e. ignore basic counts uncertainty since it is the denominator to avoid double counting of uncertainties)
            # df = sqrt((b*da)^2 + (a*db)^2)
            myDataUncert   = sqrt(pow(myLeg2Counts*self._leg1Counts.getDataError(idx,idy,idz)  /myBasicCounts,2) + pow(myLeg1Counts*self._leg2Counts.getDataError(idx,idy,idz)  /myBasicCounts,2))
            myMCStatUncert = sqrt(pow(myLeg2Counts*self._leg1Counts.getMCStatError(idx,idy,idz)/myBasicCounts,2) + pow(myLeg1Counts*self._leg2Counts.getMCStatError(idx,idy,idz)/myBasicCounts,2))
            myMCSystUncert = sqrt(pow(myLeg2Counts*self._leg1Counts.getMCSystError(idx,idy,idz)/myBasicCounts,2) + pow(myLeg1Counts*self._leg2Counts.getMCSystError(idx,idy,idz)/myBasicCounts,2))
        return [myCount,myDataUncert,myMCStatUncert,myMCSystUncert]

    def getContracted1DNQCDForBin(self,idx,axis="X"):
        myBasicCounts = self._basicCount.getContracted1DQCDCount(idx,axis).value()
        myLeg1Counts = self._leg1Counts.getContracted1DQCDCount(idx,axis).value()
        myLeg2Counts = self._leg2Counts.getContracted1DQCDCount(idx,axis).value()
        myCount = 0.0
        myDataUncert = 0.0
        myMCStatUncert = 0.0
        myMCSystUncert = 0.0
        # Protect calculation against div by zero
        if (myBasicCounts > 0.0):
            myCount = myLeg1Counts * myLeg2Counts / myBasicCounts
            # Calculate uncertainty as f=a*b  (i.e. ignore basic counts uncertainty since it is the denominator to avoid double counting of uncertainties)
            # df = sqrt((b*da)^2 + (a*db)^2)
            myDataUncert   = sqrt(pow(myLeg2Counts*self._leg1Counts.getContracted1DDataError(idx,"X")  /myBasicCounts,2) + pow(myLeg1Counts*self._leg2Counts.getContracted1DDataError(idx,"X")  /myBasicCounts,2))
            myMCStatUncert = sqrt(pow(myLeg2Counts*self._leg1Counts.getContracted1DMCStatError(idx,"X")/myBasicCounts,2) + pow(myLeg1Counts*self._leg2Counts.getContracted1DMCStatError(idx,"X")/myBasicCounts,2))
            myMCSystUncert = sqrt(pow(myLeg2Counts*self._leg1Counts.getContracted1DMCSystError(idx,"X")/myBasicCounts,2) + pow(myLeg1Counts*self._leg2Counts.getContracted1DMCSystError(idx,"X")/myBasicCounts,2))
        return [myCount,myDataUncert,myMCStatUncert,myMCSystUncert]

    def _count(self, basicCounts, leg1Counts, leg2Counts, doHistograms=False):
        if basicCounts.is1D():
            h = None
            if doHistograms:
                h = basicCounts.getClonedHisto("NQCD")
                h.Reset()
                h.SetYTitle("NQCD")
            for i in range (1,basicCounts.getNbinsX()+1):
                myNQCD = self.getNQCDForBin(i)
                self._NQCD += myNQCD[0]
                self._dataUncertainty += pow(myNQCD[1],2)
                self._MCStatUncertainty += pow(myNQCD[2],2)
                self._MCSystUncertainty += pow(myNQCD[3],2)
                # Fill histogram
                if myCount > 0 and doHistograms:
                    h.SetBinContent(i, myNQCD[0])
                    h.SetBinError(i, sqrt(pow(myNQCD[1],2)+pow(myNQCD[2],2)+pow(myNQCD[3],2)))
            if doHistograms:
                self._nQCDHistograms.append(h)
        elif basicCounts.is2D():
            h = None
            if doHistograms:
                h = basicCounts.getClonedHisto("NQCD")
                h.Reset()
                h.SetZTitle("NQCD")
            for i in range (1,basicCounts.getNbinsX()+1):
                for j in range (1,basicCounts.getNbinsY()+1):
                    myNQCD = self.getNQCDForBin(i,j)
                    self._NQCD += myNQCD[0]
                    self._dataUncertainty += pow(myNQCD[1],2)
                    self._MCStatUncertainty += pow(myNQCD[2],2)
                    self._MCSystUncertainty += pow(myNQCD[3],2)
                    # Fill histogram
                    if myCount > 0 and doHistograms:
                        h.SetBinContent(i, j, myNQCD[0])
                        h.SetBinError(i, j, sqrt(pow(myNQCD[1],2)+pow(myNQCD[2],2)+pow(myNQCD[3],2)))
            if doHistograms:
                self._nQCDHistograms.append(h)
        elif basicCounts.is3D():
            hTot = None
            if doHistograms:
                myName = "NQCD_Total"
                hTot = ROOT.TH2F(myName,myName,basicCounts.getNbinsY(),0,basicCounts.getNbinsY(),basicCounts.getNbinsX()*basicCounts.getNbinsZ(),0,basicCounts.getNbinsX()*basicCounts.getNbinsZ())
                hTot.SetZTitle("NQCD")
            for i in range (1,basicCounts.getNbinsX()+1):
                h = None
                if doHistograms:
                    myName = "NQCD_bin_%d"%(i)
                    h = ROOT.TH2F(myName,myName,basicCounts.getNbinsY(),0,basicCounts.getNbinsY(),basicCounts.getNbinsZ(),0,basicCounts.getNbinsZ())
                    h.SetZTitle("NQCD")
                    for j in range (1,basicCounts.getNbinsY()+1):
                        h.GetXaxis().SetBinLabel(j,basicCounts.getBinLabel("Y",j))
                        hTot.GetXaxis().SetBinLabel(j,basicCounts.getBinLabel("Y",j))
                    for k in range (1,basicCounts.getNbinsZ()+1):
                        h.GetYaxis().SetBinLabel(k,basicCounts.getBinLabel("Z",k))
                        hTot.GetYaxis().SetBinLabel(k+(i-1)*basicCounts.getNbinsZ(),"("+basicCounts.getBinLabel("X",i)+"; "+basicCounts.getBinLabel("Z",k))
                # Calculate NQCD
                for j in range (1,basicCounts.getNbinsY()+1):
                    for k in range (1,basicCounts.getNbinsZ()+1):
                        myNQCD = self.getNQCDForBin(i,j,k)
                        self._NQCD += myNQCD[0]
                        self._dataUncertainty += pow(myNQCD[1],2)
                        self._MCStatUncertainty += pow(myNQCD[2],2)
                        self._MCSystUncertainty += pow(myNQCD[3],2)
                        # Fill histogram
                        if myNQCD[0] > 0 and doHistograms:
                            h.SetBinContent(j,k,myNQCD[0])
                            h.SetBinError(j,k,sqrt(pow(myNQCD[1],2)+pow(myNQCD[2],2)+pow(myNQCD[3],2)))
                            hTot.SetBinContent(j,k+(i-1)*basicCounts.getNbinsZ(),myNQCD[0])
                            hTot.SetBinError(j,k+(i-1)*basicCounts.getNbinsZ(),sqrt(pow(myNQCD[1],2)+pow(myNQCD[2],2)+pow(myNQCD[3],2)))
                if doHistograms:
                    self._nQCDHistograms.append(h)
            if doHistograms:
                self._nQCDHistograms.append(hTot)
        else:
            Exception(ErrorStyle()+"QCD factorised / factorisation data has more than 3 dimensions!"+NormalStyle())
        # Take sqrt of uncertainties (sum contains the variance)
        #print "nqcd=",self._NQCD," +- ", sqrt(self._dataUncertainty), "+- ", sqrt(self._MCStatUncertainty), "+-", sqrt(self._MCSystUncertainty)
        self._dataUncertainty = sqrt(self._dataUncertainty)
        self._MCStatUncertainty = sqrt(self._MCStatUncertainty)
        self._MCSystUncertainty = sqrt(self._MCSystUncertainty)

    def _contractedCount(self, basicCounts, leg1Counts, leg2Counts, axis, doHistograms = False):
        h = None
        heff1 = None
        heff2 = None
        heff12 = None
        contractedNQCD = 0
        contractedDataUncertainty = 0
        contractedMCStatUncertainty = 0
        contractedMCSystUncertainty = 0
        myBins = 0
        if axis == "X":
            myBins = basicCounts.getNbinsX()
        elif axis == "Y":
            myBins = basicCounts.getNbinsY()
        elif axis == "Z":
            myBins = basicCounts.getNbinsZ()
        if doHistograms:
            myName = "Contracted_NQCD_axis%s"%axis
            h = ROOT.TH1F(myName,myName,myBins,0,myBins)
            h.SetYTitle(myName)
            myName = "Contracted_EffLeg1_axis%s"%axis
            heff1 = ROOT.TH1F(myName,myName,myBins,0,myBins)
            heff1.SetYTitle(myName)
            myName = "Contracted_EffLeg2_axis%s"%axis
            heff2 = ROOT.TH1F(myName,myName,myBins,0,myBins)
            heff2.SetYTitle(myName)
            myName = "Contracted_EffLeg1AndLeg2_axis%s"%axis
            heff12 = ROOT.TH1F(myName,myName,myBins,0,myBins)
            heff12.SetYTitle(myName)
        for i in range (1,myBins+1):
            if doHistograms:
                h.GetXaxis().SetBinLabel(i,basicCounts.getBinLabel(axis,i))
                heff1.GetXaxis().SetBinLabel(i,basicCounts.getBinLabel(axis,i))
                heff2.GetXaxis().SetBinLabel(i,basicCounts.getBinLabel(axis,i))
                heff12.GetXaxis().SetBinLabel(i,basicCounts.getBinLabel(axis,i))
            myBasicCounts = basicCounts.getContracted1DQCDCount(i,axis).value()
            myLeg1Counts = leg1Counts.getContracted1DQCDCount(i,axis).value()
            myLeg2Counts = leg2Counts.getContracted1DQCDCount(i,axis).value()
            myCount = 0.0
            myDataUncert = 0.0
            myMCStatUncert = 0.0
            myMCSystUncert = 0.0
            myEff1 = 0.0
            myEff2 = 0.0
            myEff1Uncert = 0.0
            myEff2Uncert = 0.0
            # Protect calculation against div by zero
            if myBasicCounts > 0.0:
                myCount = myLeg1Counts * myLeg2Counts / myBasicCounts
                # Calculate uncertainty as f=a*b  (i.e. ignore basic counts uncertainty since it is the denominator to avoid double counting of uncertainties)
                myDataUncert = pow(myLeg2Counts*leg1Counts.getContracted1DDataError(i,axis)/myBasicCounts,2) + pow(myLeg1Counts*leg2Counts.getContracted1DDataError(i,axis)/myBasicCounts,2)
                myMCStatUncert = pow(myLeg2Counts*leg1Counts.getContracted1DMCStatError(i,axis)/myBasicCounts,2) + pow(myLeg1Counts*leg2Counts.getContracted1DMCStatError(i,axis)/myBasicCounts,2)
                myMCSystUncert = pow(myLeg2Counts*leg1Counts.getContracted1DMCSystError(i,axis)/myBasicCounts,2) + pow(myLeg1Counts*leg2Counts.getContracted1DMCSystError(i,axis)/myBasicCounts,2)
                # Calculate efficiencies
                myEff1 = myLeg1Counts / myBasicCounts
                if myEff1 > 0.0:
                    myEff1Uncert = (pow(basicCounts.getContracted1DDataError(i,axis)/myBasicCounts,2) +
                                    pow(leg1Counts.getContracted1DDataError(i,axis)/myLeg1Counts,2) +
                                    pow(basicCounts.getContracted1DMCStatError(i,axis)/myBasicCounts,2) +
                                    pow(leg1Counts.getContracted1DMCStatError(i,axis)/myLeg1Counts,2)) * pow(myEff1,2)
                myEff2 = myLeg2Counts / myBasicCounts
                if myEff2 > 0.0:
                    myEff2Uncert = (pow(basicCounts.getContracted1DDataError(i,axis)/myBasicCounts,2) +
                                    pow(leg2Counts.getContracted1DDataError(i,axis)/myLeg2Counts,2) +
                                    pow(basicCounts.getContracted1DMCStatError(i,axis)/myBasicCounts,2) +
                                    pow(leg2Counts.getContracted1DMCStatError(i,axis)/myLeg2Counts,2)) * pow(myEff2,2)
            # Make total sum
            contractedNQCD += myCount
            contractedDataUncertainty += myDataUncert
            contractedMCStatUncertainty += myMCStatUncert
            contractedMCSystUncertainty += myMCSystUncert
            # Fill histogram
            if myCount > 0 and doHistograms:
                h.SetBinContent(i, myCount)
                h.SetBinError(i, sqrt(myDataUncert+myMCStatUncert+myMCSystUncert))
                if myEff1 > 0:
                    heff1.SetBinContent(i, myEff1)
                    heff1.SetBinError(i, sqrt(myEff1Uncert))
                if myEff2 > 0:
                    heff2.SetBinContent(i, myEff2)
                    heff2.SetBinError(i, sqrt(myEff2Uncert))
                if myEff1 > 0 and myEff2 > 0:
                    heff12.SetBinContent(i, myEff1*myEff2)
                    heff12.SetBinError(i, sqrt(pow(myEff2,2)*myEff1Uncert + pow(myEff1,2)*myEff2Uncert))
        if doHistograms:
            self._nQCDHistograms.append(h)
            self._nQCDHistograms.append(heff1)
            self._nQCDHistograms.append(heff2)
            self._nQCDHistograms.append(heff12)
        self._contractedNQCD[axis] = contractedNQCD
        self._contractedDataUncertainty[axis] = sqrt(contractedDataUncertainty)
        self._contractedMCStatUncertainty[axis] = sqrt(contractedMCStatUncertainty)
        self._contractedMCSystUncertainty[axis] = sqrt(contractedMCSystUncertainty)

    def _createYieldTable(self):
        myOutput = ""
        for i in range(1,self._basicCount.getNbinsX()+1):
            for k in range(1,self._basicCount.getNbinsZ()+1):
                myTableStructure = "l"
                myBasicDataRow = "$N^{\\text{data}}_{\\text{basic sel.},ijk}$ "
                myBasicEWKRow = "$N^{\\text{EWK MC}}_{\\text{basic sel.},ijk}$ "
                myBasicPurityRow = "Purity after basic sel. "
                myMetDataRow = "$N^{\\text{data}}_{\\text{\\MET+btag+}\\Delta\\phi,ijk}$ "
                myMetEWKRow = "$N^{\\text{EWK MC}}_{\\text{\\MET+btag}+\\Delta\\phi,ijk}$ "
                myMetPurityRow = "Purity after \\MET+btag+$\\Delta\\phi$ "
                myTauDataRow = "$N^{\\text{data}}_{\\text{presel.},ijk}$ "
                myTauEWKRow = "$N^{\\text{EWK MC}}_{\\text{presel.},ijk}$ "
                myTauPurityRow = "Purity after presel. "
                myMetEffRow = "$\\varepsilon_{\\text{\\MET+btag+}\\Delta\\phi,ijk}$"
                myNQCDRow = "$N^{\\text{QCD}}_{ijk}$"
                myPtCaption = "$\\tau$-jet candidate \\pT bin"
                myEtaCaption = "$\\tau$-jet candidate $\\eta$ bin"
                myPtCaption += "& \\multicolumn{3}{c}{%s \\GeVc}"%(self._basicCount.getBinLabel("X",i).replace("<","$<$").replace(">","$>$"))
                for j in range(1,self._basicCount.getNbinsY()+1):
                    myTableStructure += "l"
                    myEtaCaption += "& \multicolumn{1}{c}{%s}"%(self._basicCount.getBinLabel("Y",j).replace("<","$<$").replace(">","$>$"))
                    myBasicDataRow += "& %.1f $\\pm$ %.1f"%(self._basicCount.getDataCount(i,j,k),self._basicCount.getDataError(i,j,k))
                    myBasicEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._basicCount.getMCCount(i,j,k),self._basicCount.getMCStatError(i,j,k),self._basicCount.getMCSystError(i,j,k))
                    myPurity = self._basicCount.getPurity(i,j,k)
                    myBasicPurityRow += "& %.2f $\\pm$ %.2f"%(myPurity.value(),myPurity.uncertainty())
                    myMetDataRow += "& %.1f $\\pm$ %.1f"%(self._leg1Counts.getDataCount(i,j,k),self._leg1Counts.getDataError(i,j,k))
                    myMetEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._leg1Counts.getMCCount(i,j,k),self._leg1Counts.getMCStatError(i,j,k),self._leg1Counts.getMCSystError(i,j,k))
                    myPurity = self._leg1Counts.getPurity(i,j,k)
                    myMetPurityRow += "& %.2f $\\pm$ %.2f"%(myPurity.value(),myPurity.uncertainty())
                    myTauDataRow += "& %.1f $\\pm$ %.1f"%(self._leg2Counts.getDataCount(i,j,k),self._leg2Counts.getDataError(i,j,k))
                    myTauEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._leg2Counts.getMCCount(i,j,k),self._leg2Counts.getMCStatError(i,j,k),self._leg2Counts.getMCSystError(i,j,k))
                    myPurity = self._leg2Counts.getPurity(i,j,k)
                    myTauPurityRow += "& %.2f $\\pm$ %.2f"%(myPurity.value(),myPurity.uncertainty())
                    myMetEfficiency = self.getLeg1Efficiency(i,j,k)
                    myMetEffRow += "& %.3f $\\pm$ %.3f"%(myMetEfficiency.value(),myMetEfficiency.uncertainty())
                    myNQCD = self.getNQCDForBin(i,j,k)
                    myNQCDRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(myNQCD[0],sqrt(pow(myNQCD[1],2)+pow(myNQCD[2],2)),myNQCD[3])
                # Construct table
                if k % 2 == 1: # FIXME assumed 2 bins for eta
                    myOutput += "\\renewcommand{\\arraystretch}{1.2}\n"
                    myOutput += "\\begin{table}\n"
                    myOutput += "\\caption{Analytical breakdown of the \\NQcd estimate, showing the number of data and EWK MC events and\n"
                    myOutput += "  the purity of the sample after standard selections, after basic selections plus \\MET+btag+$\\Delta\\phi$, and\n"
                    myOutput += "  after all preselections. The efficiency of \\MET+btag+$\\Delta\\phi$ relative to basic selections and \n"
                    myOutput += "  the estimate for the number of QCD multi-jet events in the signal region (\\NQcd) are shown.\n"
                    myOutput += "  The numbers are shown for tau candidate \\pT bin %s \\GeVc.\n"%(self._basicCount.getBinLabel("X",i).replace("<","$<$").replace(">","$>$"))
                    myOutput += "  The top table is for $N_{\\text{vertices}} < 8$,\n" #FIXME assumed 2 bins for eta
                    myOutput += "  whereas the bottom table is for $N_{\\text{vertices}} \geq 8$.\n"
                    myOutput += "  Wherever appropriate, the systematic uncertainty is shown in addition to the statistical uncertainty. } \n"
                    myOutput += "\\label{tab:background:qcdfact:evtyield:bin%d}\n"%(i)
                    myOutput += "\\vspace{1cm}\n"
                    myOutput += "%% NQCD analytical breakdown for tau pT bin %s and Nvtx bin = %s\n"%(self._basicCount.getBinLabel("X",i).replace("<","$<$").replace(">","$>$"),self._basicCount.getBinLabel("Z",k).replace("<","$<$").replace(">","$>$"))
                else:
                    myOutput += "\\\\ \n"
                    myOutput += "\\\\ \n"
                myOutput += "\\begin{tabular}{%s}\n"%myTableStructure
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myPtCaption
                myOutput += "%s \\\\ \n"%myEtaCaption
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myBasicDataRow
                myOutput += "%s \\\\ \n"%myBasicEWKRow
                myOutput += "%s \\\\ \n"%myBasicPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myMetDataRow
                myOutput += "%s \\\\ \n"%myMetEWKRow
                myOutput += "%s \\\\ \n"%myMetPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myTauDataRow
                myOutput += "%s \\\\ \n"%myTauEWKRow
                myOutput += "%s \\\\ \n"%myTauPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myMetEffRow
                myOutput += "%s \\\\ \n"%myNQCDRow
                myOutput += "\\hline\n"
                myOutput += "\\end{tabular}\n"
                if k % 2 == 0: # FIXME assumed 2 bins for eta
                    myOutput += "\\end{table}\n"
                    myOutput += "\\renewcommand{\\arraystretch}{1.0}\n"
                    myOutput += "\\newpage\n\n"
        return myOutput

    def _createCompactYieldTable(self):
        myTableStructure = ""
        myBasicDataRow = ""
        myBasicEWKRow = ""
        myBasicPurityRow = ""
        myMetDataRow = ""
        myMetEWKRow = ""
        myMetPurityRow = ""
        myTauDataRow = ""
        myTauEWKRow = ""
        myTauPurityRow = ""
        myMetEffRow = ""
        myNQCDRow = ""
        myPtCaption = ""
        myOutput = ""
        for i in range(1,self._basicCount.getNbinsX()+1):
            if (i-1) % 4 == 0:
                myOutput += "\\renewcommand{\\arraystretch}{1.2}\n"
                myOutput += "\\begin{table}\n"
                myOutput += "\\caption{Analytical breakdown of the \\NQcd estimate for tau candidate \\pT range X-X \\GeVc, showing the number of data and EWK MC events and\n"
                myOutput += "  the purity of the sample after standard selections, after basic selections plus \\MET+btag+$\\Delta\\phi$, and\n"
                myOutput += "  after all preselections. The efficiency of \\MET+btag+$\\Delta\\phi$ relative to basic selections and \n"
                myOutput += "  the estimate for the number of QCD multi-jet events in the signal region (\\NQcd) are shown.\n"
                myOutput += "  The bins of tau candidate $\\eta$ and $N_{\\text{vertices}}$ have been summed up.\n"
                myOutput += "  Wherever appropriate, the systematic uncertainty is shown in addition to the statistical uncertainty. } \n"
                myOutput += "\\label{tab:background:qcdfact:evtyield:tauptonly%d}\n"%((i-1)/4+1)
                myOutput += "\\vspace{1cm}\n"
            if (i-1) % 2 == 0:
                myTableStructure = "l"
                myBasicDataRow = "$N^{\\text{data}}_{\\text{basic sel.},i}$ "
                myBasicEWKRow = "$N^{\\text{EWK MC}}_{\\text{basic sel.},i}$ "
                myBasicPurityRow = "Purity after basic sel. "
                myMetDataRow = "$N^{\\text{data}}_{\\text{\\MET+btag+}\\Delta\\phi,i}$ "
                myMetEWKRow = "$N^{\\text{EWK MC}}_{\\text{\\MET+btag}+\\Delta\\phi,i}$ "
                myMetPurityRow = "Purity after \\MET+btag+$\\Delta\\phi$ "
                myTauDataRow = "$N^{\\text{data}}_{\\text{presel.},i}$ "
                myTauEWKRow = "$N^{\\text{EWK MC}}_{\\text{presel.},i}$ "
                myTauPurityRow = "Purity after presel. "
                myMetEffRow = "$\\varepsilon_{\\text{\\MET+btag+}\\Delta\\phi,i}$"
                myNQCDRow = "$N^{\\text{QCD}}_{i}$"
                myPtCaption = "$\\tau$-jet candidate \\pT bin"
            myPtCaption += "& %s \\GeVc"%(self._basicCount.getBinLabel("X",i).replace("<","$<$").replace(">","$>$"))
            myTableStructure += "l"
            myBasicDataRow += "& %.1f $\\pm$ %.1f"%(self._basicCount.getContracted1DDataCount(i,"X"),self._basicCount.getContracted1DDataError(i,"X"))
            myBasicEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._basicCount.getContracted1DMCCount(i,"X"),self._basicCount.getContracted1DMCStatError(i,"X"),self._basicCount.getContracted1DMCSystError(i,"X"))
            myPurity = self._basicCount.getContracted1DPurity(i,"X")
            myBasicPurityRow += "& %.3f $\\pm$ %.3f"%(myPurity.value(),myPurity.uncertainty())
            myMetDataRow += "& %.1f $\\pm$ %.1f"%(self._leg1Counts.getContracted1DDataCount(i,"X"),self._leg1Counts.getContracted1DDataError(i,"X"))
            myMetEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._leg1Counts.getContracted1DMCCount(i,"X"),self._leg1Counts.getContracted1DMCStatError(i,"X"),self._leg1Counts.getContracted1DMCSystError(i,"X"))
            myPurity = self._leg1Counts.getContracted1DPurity(i,"X")
            myMetPurityRow += "& %.2f $\\pm$ %.2f"%(myPurity.value(),myPurity.uncertainty())
            myTauDataRow += "& %.1f $\\pm$ %.1f"%(self._leg2Counts.getContracted1DDataCount(i,"X"),self._leg2Counts.getContracted1DDataError(i,"X"))
            myTauEWKRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(self._leg2Counts.getContracted1DMCCount(i,"X"),self._leg2Counts.getContracted1DMCStatError(i,"X"),self._leg2Counts.getContracted1DMCSystError(i,"X"))
            myPurity = self._leg2Counts.getContracted1DPurity(i,"X")
            myTauPurityRow += "& %.2f $\\pm$ %.2f"%(myPurity.value(),myPurity.uncertainty())
            myMetEfficiency = self.getContracted1DLeg1Efficiency(i,"X")
            myMetEffRow += "& %.4f $\\pm$ %.4f"%(myMetEfficiency.value(),myMetEfficiency.uncertainty())
            myNQCD = self.getContracted1DNQCDForBin(i,"X")
            myNQCDRow += "& %.1f $\\pm$ %.1f $\\pm$ %.1f"%(myNQCD[0],sqrt(pow(myNQCD[1],2)+pow(myNQCD[2],2)),myNQCD[3])
            # Construct table
            if i % 2 == 0:
                myOutput += "\\begin{tabular}{%s}\n"%myTableStructure
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myPtCaption
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myBasicDataRow
                myOutput += "%s \\\\ \n"%myBasicEWKRow
                myOutput += "%s \\\\ \n"%myBasicPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myMetDataRow
                myOutput += "%s \\\\ \n"%myMetEWKRow
                myOutput += "%s \\\\ \n"%myMetPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myTauDataRow
                myOutput += "%s \\\\ \n"%myTauEWKRow
                myOutput += "%s \\\\ \n"%myTauPurityRow
                myOutput += "\\hline\n"
                myOutput += "%s \\\\ \n"%myMetEffRow
                myOutput += "%s \\\\ \n"%myNQCDRow
                myOutput += "\\hline\n"
                myOutput += "\\end{tabular}\n"
                if i % 4 != 0:
                    myOutput += "\\\\ \n"
                    myOutput += "\\\\ \n"
            if i % 4 == 0:
                myOutput += "\\end{table}\n"
                myOutput += "\\renewcommand{\\arraystretch}{1.0}\n"
                myOutput += "\\newpage\n\n"
        return myOutput

## class QCDfactorisedColumn
# Inherits from DatacardColumn and extends its functionality to calculate the QCD measurement and its result in one go
# Note that only method one needs to add is 'doDataMining'; other methods are private
class QCDfactorisedColumn(DatacardColumn):
    ## Constructor
    def __init__(self,
                 landsProcess = -999,
                 enabledForMassPoints = [],
                 nuisanceIds = [],
                 datasetMgrColumn = "",
                 datasetMgrColumnForQCDMCEWK = "",
                 additionalNormalisationFactor = 1.0,
                 dirPrefix = "",
                 QCDfactorisedInfo = None,
                 debugMode = False):
        DatacardColumn.__init__(self,
                                label = "QCDfact",
                                landsProcess = landsProcess,
                                enabledForMassPoints = enabledForMassPoints,
                                datasetType = "QCD factorised",
                                nuisanceIds = nuisanceIds,
                                datasetMgrColumn = datasetMgrColumn,
                                datasetMgrColumnForQCDMCEWK = datasetMgrColumnForQCDMCEWK,
                                additionalNormalisationFactor = additionalNormalisationFactor,
                                dirPrefix = dirPrefix)
        # Set source histograms
        self._afterBigboxSource = QCDfactorisedInfo["afterBigboxSource"]
        self._afterMETLegSource = QCDfactorisedInfo["afterMETLegSource"]
        self._afterTauLegSource = QCDfactorisedInfo["afterTauLegSource"]
        self._basicMtHisto = QCDfactorisedInfo["basicMtHisto"]
        self._assumedMCEWKSystUncertainty = QCDfactorisedInfo["assumedMCEWKSystUncertainty"]
        self._factorisationMapAxisLabels = QCDfactorisedInfo["factorisationMapAxisLabels"]
        self._validationMETShapeSource = QCDfactorisedInfo["validationMETShapeSource"]
        self._validationMETShapeDetails = QCDfactorisedInfo["validationMETShapeDetails"]
        self._validationMtShapeSource = QCDfactorisedInfo["validationMtShapeSource"]
        # Other initialisation
        self._infoHistograms = []
        self._debugMode = debugMode
        self._messages = []
        self._yieldTable = ""
        self._compactYieldTable = ""

    ## Returns list of messages
    def getMessages(self):
        return self._messages

    def getYieldTable(self):
        return self._yieldTable

    def getCompactYieldTable(self):
        return self._compactYieldTable

    ## Do data mining and cache results
    def doDataMining(self, config, dsetMgr, luminosity, mainCounterTable, extractors, controlPlotExtractors):
        print "... processing column: "+HighlightStyle()+self._label+NormalStyle()
        if dsetMgr == None:
            raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" You called data mining for QCD factorised, but you disabled it config. Such undertaking is currently not supported.")
        print "... Calculating NQCD value ..."
        # Make event count objects
        myBigBoxEventCount = self._getQCDEventCount(dsetMgr=dsetMgr, histoName=self._afterBigboxSource, luminosity=luminosity)
        myMETLegEventCount = self._getQCDEventCount(dsetMgr=dsetMgr, histoName=self._afterMETLegSource, luminosity=luminosity)
        myTauLegEventCount = self._getQCDEventCount(dsetMgr=dsetMgr, histoName=self._afterTauLegSource, luminosity=luminosity)
        # Make control plot for NQCD event counts
        self._infoHistograms.extend(myBigBoxEventCount.getEventCountHistograms())
        self._infoHistograms.extend(myMETLegEventCount.getEventCountHistograms())
        self._infoHistograms.extend(myTauLegEventCount.getEventCountHistograms())
        # Make control plot for negative NQCD entries
        self._infoHistograms.extend(myBigBoxEventCount.getNegativeEventCountHistograms())
        self._infoHistograms.extend(myMETLegEventCount.getNegativeEventCountHistograms())
        self._infoHistograms.extend(myTauLegEventCount.getNegativeEventCountHistograms())
        # Make purity histograms
        self._infoHistograms.extend(myBigBoxEventCount.getPurityHistogram())
        self._infoHistograms.extend(myMETLegEventCount.getPurityHistogram())
        self._infoHistograms.extend(myTauLegEventCount.getPurityHistogram())
        # Calculate result of NQCD
        myQCDCalculator = QCDfactorisedCalculator(myBigBoxEventCount, myMETLegEventCount, myTauLegEventCount, True)
        self._yieldTable = myQCDCalculator.getYieldTable()
        self._compactYieldTable = myQCDCalculator.getCompactYieldTable()
        self._infoHistograms.extend(myQCDCalculator.getNQCDHistograms())
        # Make efficiency histograms
        self._infoHistograms.extend(myQCDCalculator.getLeg1EfficiencyHistogram())
        self._infoHistograms.extend(myQCDCalculator.getLeg2EfficiencyHistogram())
        # Print result
        print "... NQCD = %f +- %f (%% stat.) +- %f (%% syst.)"%(myQCDCalculator.getNQCD(),myQCDCalculator.getStatUncertainty(),myQCDCalculator.getSystUncertainty())
        print "... Contracted NQCD for x axis= %f +- %f (%% stat.) +- %f (%% syst.)"%(myQCDCalculator.getContractedNQCD("X"),myQCDCalculator.getContractedStatUncertainty("X"),myQCDCalculator.getContractedSystUncertainty("X"))
        if myBigBoxEventCount.is2D() or myBigBoxEventCount.is3D():
            print "... Contracted NQCD for y axis= %f +- %f (%% stat.) +- %f (%% syst.)"%(myQCDCalculator.getContractedNQCD("Y"),myQCDCalculator.getContractedStatUncertainty("Y"),myQCDCalculator.getContractedSystUncertainty("Y"))
        if myBigBoxEventCount.is3D():
            print "... Contracted NQCD for z axis= %f +- %f (%% stat.) +- %f (%% syst.)"%(myQCDCalculator.getContractedNQCD("Z"),myQCDCalculator.getContractedStatUncertainty("Z"),myQCDCalculator.getContractedSystUncertainty("Z"))
        # Make shape histogram
        print "... Calculating shape (looping over %d histograms)..."%myBigBoxEventCount.getTotalDimension()
        myRateHistograms=[]
        hRateShape = self._createShapeHistogram(config, dsetMgr, myQCDCalculator, myBigBoxEventCount, luminosity,
                                                config.ShapeHistogramsDimensions, self._label, self._dirPrefix, self._basicMtHisto,
                                                saveDetailedInfo = True) ##### FIXME
        # Normalise rate shape to NQCD
        if hRateShape.Integral() > 0:
            hRateShape.Scale(myQCDCalculator.getNQCD() / hRateShape.Integral())
        myRateHistograms.append(hRateShape)
        # Obtain messages
        self._messages.extend(myBigBoxEventCount.getMessages())
        self._messages.extend(myMETLegEventCount.getMessages())
        self._messages.extend(myTauLegEventCount.getMessages())
        # Cache result for rate
        self._rateResult = ExtractorResult("rate",
                                           "rate",
                                           myQCDCalculator.getNQCD(),
                                           myRateHistograms)
        # Make validation shapes
        print "... Producing validation histograms ..."
        for METshape in self._validationMETShapeSource:
            self._createValidationHistograms(config,dsetMgr,myBigBoxEventCount,luminosity,self._validationMETShapeDetails,
                                             "METvalidation", self._dirPrefix, METshape)
        for mTshape in self._validationMtShapeSource:
            self._createValidationHistograms(config,dsetMgr,myBigBoxEventCount,luminosity,config.ShapeHistogramsDimensions,
                                             "mTvalidation", self._dirPrefix, mTshape)
        # Construct results for nuisances
        print "... Constructing result ..."
        for nid in self._nuisanceIds:
            #sys.stdout.write("\r... data mining in progress: Column="+self._label+", obtaining Nuisance="+nid+"...                                              ")
            #sys.stdout.flush()
            myFoundStatus = False
            for e in extractors:
                if e.getId() == nid:
                    myFoundStatus = True
                    myResult = 0.0
                    # Obtain result
                    if e.getQCDmode() == "statistics":
                        myResult = myQCDCalculator.getStatUncertainty()
                    elif e.getQCDmode() == "systematics":
                        myResult = myQCDCalculator.getSystUncertainty()
                    # Obtain histograms
                    myHistograms = []
                    if e.getQCDmode() == "shapestat":
                        # Clone rate histogram as up and down histograms
                        myHistograms.append(myRateHistograms[0].Clone(self._label+"_%dDown"%int(e.getMasterId())))
                        myHistograms[0].SetTitle(self._label+"_%dDown"%int(e.getMasterId()))
                        myHistograms.append(myRateHistograms[0].Clone(self._label+"_%dUp"%int(e.getMasterId())))
                        myHistograms[1].SetTitle(self._label+"_%dUp"%int(e.getMasterId()))
                        # Substract/Add one sigma to get Down/Up variation
                        for k in range(1, myHistograms[0].GetNbinsX()+1):
                            myHistograms[0].SetBinContent(k, myHistograms[0].GetBinContent(k) - myHistograms[0].GetBinError(k))
                            myHistograms[1].SetBinContent(k, myHistograms[1].GetBinContent(k) + myHistograms[1].GetBinError(k))
                            if myHistograms[0].GetBinContent(k) < 0:
                                print WarningStyle()+"Warning: shapeStat Nuisance with id='"+e.getId()+"' for column '"+self._label+"':"+NormalStyle()+" shapeDown histo bin %d is negative (%f), it is forced to zero"%(k,myHistograms[0].GetBinContent(k))
                                myHistograms[0].SetBinContent(k, 0.0)
                            if myHistograms[1].GetBinContent(k) < 0:
                                print WarningStyle()+"Warning: shapeStat Nuisance with id='"+e.getId()+"' for column '"+self._label+"':"+NormalStyle()+" shapeUp histo bin %d is negative (%f), it is forced to zero"%(k,myHistograms[0].GetBinContent(k))
                                myHistograms[1].SetBinContent(k, 0.0)
                    # Cache result
                    self._nuisanceResults.append(ExtractorResult(e.getId(),
                                                                 e.getMasterId(),
                                                                 myResult,
                                                                 myHistograms,
                                                                 e.getQCDmode() == "statistics" or e.getQCDmode() == "shapestat"))
            if not myFoundStatus:
                raise Exception("\n"+ErrorStyle()+"Error (data group ='"+self._label+"'):"+NormalStyle()+" Cannot find nuisance with id '"+nid+"'!")
        # Obtain results for control plots
        if config.OptionDoControlPlots != None:
            if config.OptionDoControlPlots:
                print "... Obtaining control plots ..."
                if config.ControlPlots != None and dsetMgr != None:
                    for c in config.ControlPlots:
                        hShape = self._createShapeHistogram(config, dsetMgr, myQCDCalculator, myBigBoxEventCount, luminosity,
                                                            c.details, c.title, self._dirPrefix+"/"+c.QCDFactHistoPath, c.QCDFactHistoName)
                        # Normalise
                        myEventCount = self._getQCDEventCount(dsetMgr=dsetMgr, histoName=c.QCDFactNormalisation, luminosity=luminosity)
                        myQCDCalculator = QCDfactorisedCalculator(myBigBoxEventCount, myEventCount, myTauLegEventCount)
                        hShape.Scale(myQCDCalculator.getNQCD() / hShape.Integral())
                        print "     "+c.title+", NQCD=%f"%myQCDCalculator.getNQCD()
                        myEventCount.clean()
                        self._controlPlots.append(hShape)
        # Clean up
        myQCDCalculator.clean()

    def _getQCDEventCount(self, dsetMgr, histoName, luminosity):
        return QCDEventCount(histoPrefix=self._dirPrefix,
                             histoName=histoName,
                             dsetMgr=dsetMgr,
                             dsetMgrDataColumn=self._datasetMgrColumn,
                             dsetMgrMCEWKColumn=self._datasetMgrColumnForQCDMCEWK,
                             luminosity=luminosity,
                             assumedMCEWKSystUncertainty=self._assumedMCEWKSystUncertainty)

    def _createShapeHistogram(self, config, dsetMgr, QCDCalculator, QCDCount, luminosity, histoSpecs, title, histoDir, histoName, saveDetailedInfo = False):
        # Create empty shape histogram
        myShapeModifier = ShapeHistoModifier(histoSpecs)
        h = myShapeModifier.createEmptyShapeHistogram(title)
        # Obtain bin dimensions
        nbinsY = 1
        if QCDCount.is2D() or QCDCount.is3D():
            nbinsY = QCDCount.getNbinsY()
        nbinsZ = 1
        if QCDCount.is3D():
            nbinsZ = QCDCount.getNbinsZ()
        # Create info histogram with all info in one
        myName = "QCDFact_ShapeSummary_%s_Total"%title
        hTot = ROOT.TH2F(myName,myName,h.GetNbinsX()*QCDCount.getNbinsY(),0,h.GetNbinsX()*QCDCount.getNbinsY(),QCDCount.getNbinsX()*QCDCount.getNbinsZ(),0,QCDCount.getNbinsX()*QCDCount.getNbinsZ())
        hTot.SetZTitle("Events")
        # Setup axis titles for total histogram
        for i in range(1,h.GetNbinsX()+1):
            for j in range(1,nbinsY+1):
                if i == h.GetNbinsX()+1:
                    hTot.GetXaxis().SetBinLabel(i+(j-1)*h.GetNbinsX(), "(>%d; "%(h.GetXaxis().GetBinUpEdge(i))+QCDCount.getBinLabel("Y",j))
                else:
                    hTot.GetXaxis().SetBinLabel(i+(j-1)*h.GetNbinsX(), "(%d-%d; "%(h.GetXaxis().GetBinLowEdge(i),h.GetXaxis().GetBinUpEdge(i))+QCDCount.getBinLabel("Y",j))
        for i in range(1,QCDCount.getNbinsX()+1):
            for k in range(1,nbinsZ+1):
                hTot.GetYaxis().SetBinLabel(k+(i-1)*nbinsZ, "("+QCDCount.getBinLabel("X",i)+";"+QCDCount.getBinLabel("Z",k))
        # Loop over bins
        for i in range(1,QCDCount.getNbinsX()+1):
            myName = "QCDFact_ShapeSummary_%s_ContractedX_bin_%d"%(title,i)
            hTotContractedX = myShapeModifier.createEmptyShapeHistogram(myName)
            myName = "QCDFact_ShapeSummary_%s_ContractedXContractedEff_bin_%d"%(title,i)
            hTotContractedXeff = myShapeModifier.createEmptyShapeHistogram(myName)
            for j in range(1,nbinsY+1):
                for k in range(1,nbinsZ+1):
                    # Determine suffix for histograms
                    myFactorisationSuffix = "_%d"%(i-1)
                    if QCDCount.is2D() or QCDCount.is3D():
                        myFactorisationSuffix += "_%d"%(j-1)
                    if QCDCount.is3D():
                        myFactorisationSuffix += "_%d"%(k-1)
                    # Get histograms for the bin for data and MC EWK
                    myFullHistoName = "%s/%s%s"%(histoDir,histoName,myFactorisationSuffix)
                    hMtData = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumn, myFullHistoName, luminosity)
                    hMtMCEWK = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumnForQCDMCEWK, myFullHistoName, luminosity)
                    if self._debugMode:
                        print "  QCDfactorised / %s: bin%s, data=%f, MC EWK=%f, QCD=%f"%(title,myFactorisationSuffix,hMtData.Integral(0,hMtData.GetNbinsX()+1),hMtMCEWK.Integral(0,hMtMCEWK.GetNbinsX()+1),hMtData.Integral(0,hMtData.GetNbinsX()+1)-hMtMCEWK.Integral(0,hMtMCEWK.GetNbinsX()+1))
                    # Obtain empty histograms
                    myOutHistoName = "QCDFact_%s_QCD_bin%s"%(title,myFactorisationSuffix)
                    hMtBin = myShapeModifier.createEmptyShapeHistogram(myOutHistoName)
                    hMtBinData = None
                    hMtBinEWK = None
                    if saveDetailedInfo:
                        myOutHistoName = "QCDFact_%s_Data_bin%s"%(title,myFactorisationSuffix)
                        hMtBinData = myShapeModifier.createEmptyShapeHistogram(myOutHistoName)
                        myOutHistoName = "QCDFact_%s_MCEWK_bin%s"%(title,myFactorisationSuffix)
                        hMtBinEWK = myShapeModifier.createEmptyShapeHistogram(myOutHistoName)
                    # Add data to histograms
                    myShapeModifier.addShape(source=hMtData,dest=hMtBin)
                    myShapeModifier.addShape(source=hMtData,dest=hMtBinData)
                    myShapeModifier.addShape(source=hMtMCEWK,dest=hMtBinEWK)
                    # Subtract MC EWK from data to obtain QCD
                    myMessages = []
                    myMessages.extend(myShapeModifier.subtractShape(source=hMtMCEWK,dest=hMtBin,purityCheck=True))
                    if len(myMessages) > 0:
                        myTotal = hMtBin.Integral(0,hMtBin.GetNbinsX()+1)
                        for m in myMessages:
                            # Filter out only important warnings of inpurity (impact more than one percent to whole bin)
                            if myTotal > 0.0:
                                if m[1] / myTotal > 0.01:
                                    self._messages.extend(WarningStyle()+"Warning:"+NormalStyle()+" low purity in QCD factorised shape for bin %d,%d,%d (impact %f events / total=%f : %s"%(i,j,k,m[1],myTotal,m[0]))
                    # Finalise shape (underflow added to first bin, overflow added to last bin, variances converted to std.deviations)
                    myShapeModifier.finaliseShape(dest=hMtBin)
                    myShapeModifier.finaliseShape(dest=hMtBinData)
                    myShapeModifier.finaliseShape(dest=hMtBinEWK)
                    # Add to contracted histogram
                    myShapeModifier.addShape(source=hMtBin,dest=hTotContractedXeff)
                    # Multiply by efficiency of leg 2 (tau leg)
                    myEfficiency = QCDCalculator.getLeg2Efficiency(i,j,k)
                    if myEfficiency.value() > 0.0:
                        for l in range(1,hMtBin.GetNbinsX()+1):
                            hMtBin.SetBinError(l,sqrt(pow(hMtBin.GetBinError(l)*myEfficiency.value(),2)+pow(hMtBin.GetBinContent(l)*myEfficiency.uncertainty(),2)))
                            hMtBin.SetBinContent(l,hMtBin.GetBinContent(l)*myEfficiency.value())
                        if saveDetailedInfo:
                            hMtBinData.Scale(myEfficiency.value()) #FIXME
                            hMtBinEWK.Scale(myEfficiency.value())
                    else:
                        # Do not take this bin into account if cannot obtain efficiency
                        hMtBin.Reset()
                    if self._debugMode:
                        print "  QCDfactorised / %s shape: bin %d_%d_%d, eff=%f, eff*QCD=%f"%(title,i,j,k,myEfficiency.value(),hMtBin.Integral())
                    # Add to total shape histogram
                    #myShapeModifier.addShape(source=hMtBin,dest=h) # important to do before handling negative bins
                    myShapeModifier.addShape(source=hMtBin,dest=hTotContractedX)
                    # Remove negative bins, but retain original normalisation
                    for a in range(1,hMtBin.GetNbinsX()+1):
                        if hMtBin.GetBinContent(a) < 0.0:
                            #print WarningStyle()+"Warning: QCD factorised"+NormalStyle()+" in mT shape bin %d,%d,%d, histo bin %d is negative (%f / tot:%f), it is set to zero but total normalisation is maintained"%(i,j,k,a,hMtBin.GetBinContent(a),hMtBin.Integral())
                            myIntegral = hMtBin.Integral()
                            hMtBin.SetBinContent(a,0.0)
                            if (hMtBin.Integral() > 0.0):
                                hMtBin.Scale(myIntegral / hMtBin.Integral())
                    # Add to total info histogram
                    for l in range (1, hMtBin.GetNbinsX()+1):
                        hTot.SetBinContent(l+(j-1)*h.GetNbinsX(), k+(i-1)*nbinsZ, hMtBin.GetBinContent(l))
                        hTot.SetBinError(l+(j-1)*h.GetNbinsX(), k+(i-1)*nbinsZ, hMtBin.GetBinError(l))
                    # Store mT bin histogram for info
                    if saveDetailedInfo:
                        self._infoHistograms.append(hMtBin)
                        self._infoHistograms.append(hMtBinData)
                        self._infoHistograms.append(hMtBinEWK)
                    else:
                        hMtBin.IsA().Destructor(hMtBin)
                    # Delete data and MC EWK histograms from memory
                    hMtData.IsA().Destructor(hMtData)
                    hMtMCEWK.IsA().Destructor(hMtMCEWK)
            myEfficiency = QCDCalculator.getContracted1DLeg2Efficiency(i,"X")
            myShapeModifier.finaliseShape(dest=hTotContractedX)
            myShapeModifier.finaliseShape(dest=hTotContractedXeff)
            if myEfficiency.value() > 0.0:
                for l in range (1, hTotContractedXeff.GetNbinsX()+1):
                    hTotContractedXeff.SetBinError(l,sqrt(pow(hTotContractedXeff.GetBinError(l)*myEfficiency.value(),2)+pow(hTotContractedXeff.GetBinContent(l)*myEfficiency.uncertainty(),2)))
                    hTotContractedXeff.SetBinContent(l,hTotContractedXeff.GetBinContent(l)*myEfficiency.value())
                    #hTotContractedX.Scale(myEfficiency.value()) # FIXME should I also apply uncert of efficiency to weighted shape?
            self._infoHistograms.append(hTotContractedX)
            self._infoHistograms.append(hTotContractedXeff)
            myShapeModifier.addShape(source=hTotContractedXeff,dest=h)
        self._infoHistograms.append(hTot)
        # Finalise and return
        myShapeModifier.finaliseShape(dest=h)
        # Remove negative bins, but retain original normalisation
        for a in range(1,h.GetNbinsX()+1):
            if h.GetBinContent(a) < 0.0:
                #print WarningStyle()+"Warning: QCD factorised"+NormalStyle()+" in mT shape bin %d,%d,%d, histo bin %d is negative (%f / tot:%f), it is set to zero but total normalisation is maintained"%(i,j,k,a,hMtBin.GetBinContent(a),hMtBin.Integral())
                myIntegral = h.Integral()
                h.SetBinContent(a,0.0)
                if (h.Integral() > 0.0):
                    h.Scale(myIntegral / h.Integral())

        return h

    ## Extracts a shape histogram for a given bin
    def _extractShapeHistogram(self, dsetMgr, datasetMgrColumn, histoName, luminosity):
        dsetRootHistoMtData = dsetMgr.getDataset(datasetMgrColumn).getDatasetRootHisto(histoName)
        if dsetRootHistoMtData.isMC():
            dsetRootHistoMtData.normalizeToLuminosity(luminosity)
        h = dsetRootHistoMtData.getHistogram()
        if h == None:
            raise Exception(ErrorStyle()+"Error:"+NormalStyle()+" Cannot find histogram "+histoName+" for QCD factorised shape")
        return h

    def _createValidationHistograms(self, config, dsetMgr, QCDCount, luminosity, histoSpecs, title, histoDir, histoName):
        head,tail=os.path.split(histoName)
        title += "_%s"%tail
        print "      "+title
        # Create empty shape histogram
        myShapeModifier = ShapeHistoModifier(histoSpecs)
        # Obtain bin dimensions
        nbinsY = 1
        if QCDCount.is2D() or QCDCount.is3D():
            nbinsY = QCDCount.getNbinsY()
        nbinsZ = 1
        if QCDCount.is3D():
            nbinsZ = QCDCount.getNbinsZ()
        # Loop over bins
        for i in range(1,QCDCount.getNbinsX()+1):
            h = myShapeModifier.createEmptyShapeHistogram(title+"_bin_%d"%(i-1))
            for j in range(1,nbinsY+1):
                for k in range(1,nbinsZ+1):
                    # Determine suffix for histograms
                    myFactorisationSuffix = "_%d"%(i-1)
                    if QCDCount.is2D() or QCDCount.is3D():
                        myFactorisationSuffix += "_%d"%(j-1)
                    if QCDCount.is3D():
                        myFactorisationSuffix += "_%d"%(k-1)
                    # Get histograms for the bin for data and MC EWK
                    myFullHistoName = "%s/%s%s"%(histoDir,histoName,myFactorisationSuffix)
                    hMtData = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumn, myFullHistoName, luminosity)
                    hMtMCEWK = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumnForQCDMCEWK, myFullHistoName, luminosity)
                    # Obtain empty histograms
                    myOutHistoName = "QCDFact_%s_QCD_bin%s"%(title,myFactorisationSuffix)
                    hMtBin = myShapeModifier.createEmptyShapeHistogram(myOutHistoName)
                    # Add data to histograms
                    myShapeModifier.addShape(source=hMtData,dest=hMtBin)
                    # Subtract MC EWK from data to obtain QCD
                    myMessages = []
                    myMessages.extend(myShapeModifier.subtractShape(source=hMtMCEWK,dest=hMtBin,purityCheck=False))
                    # Finalise shape (underflow added to first bin, overflow added to last bin, variances converted to std.deviations)
                    myShapeModifier.finaliseShape(dest=hMtBin) # do not correct here for negative bins!
                    myShapeModifier.addShape(source=hMtBin,dest=h)
                    # Add to total shape histogram
                    # Store mT bin histogram for info
                    self._infoHistograms.append(hMtBin)
            # Finalise
            # Remove negative bins, but retain original normalisation
            for a in range(1,hMtBin.GetNbinsX()+1):
                if h.GetBinContent(a) < 0.0:
                    #print WarningStyle()+"Warning: QCD factorised"+NormalStyle()+" in mT shape bin %d,%d,%d, histo bin %d is negative (%f / tot:%f), it is set to zero but total normalisation is maintained"%(i,j,k,a,hMtBin.GetBinContent(a),hMtBin.Integral())
                    myIntegral = hMtBin.Integral()
                    h.SetBinContent(a,0.0)
                    h.SetBinError(a,0.0)
                    if (h.Integral() > 0.0):
                        h.Scale(myIntegral / h.Integral())
            myShapeModifier.finaliseShape(dest=h)
            self._infoHistograms.append(h)

    ## Saves information histograms into a histogram
    def saveQCDInfoHistograms(self, outputDir):
        # Open root file for saving
        myRootFilename = outputDir+"/QCDMeasurementFactorisedInfo.root"
        myRootFile = ROOT.TFile.Open(myRootFilename, "RECREATE")
        if myRootFile == None:
            print ErrorStyle()+"Error:"+NormalStyle()+" Cannot open file '"+myRootFilename+"' for output!"
            sys.exit()
        # Loop over info histograms
        myPreviousName = ""
        mySubDir = None
        for h in self._infoHistograms:
            histoname = h.GetName()
            myIndex = h.GetName().find("_bin")
            if myIndex >= 0:
                histoname = histoname[0:myIndex]
            # Store bin histograms in dedicated subdirectory
            if "bin" in h.GetName():
                # Make new subdirectory if necessary
                if myPreviousName != histoname:
                    if myRootFile.FindObject(histoname) == None:
                        mySubDir = myRootFile.mkdir(histoname)
                    else:
                        mySubDir = myRootFile.FindObject(histoname)
                h.SetDirectory(mySubDir)
            # Store summary histogram in main directory
            else:
                h.SetDirectory(myRootFile)
            myPreviousName = histoname

        # Close root file
        myRootFile.Write()
        myRootFile.Close()
        # Cleanup (closing the root file destroys the objects assigned to it, do not redestroy the histos in the _infoHistograms list
        self._infoHistograms = []
        print "\n"+HighlightStyle()+"QCD Measurement factorised info histograms saved to: "+NormalStyle()+myRootFilename

## QCDfactorisedExtractor class
# It is essentially wrapper for QCD mode string
class QCDfactorisedExtractor(ExtractorBase):
    ## Constructor
    def __init__(self, QCDmode, mode, exid = "", distribution = "lnN", description = ""):
        ExtractorBase.__init__(self, mode, exid, distribution, description)
        self._QCDmode = QCDmode

    ## Method for extracking information
    # Everything is processed 
    def extractResult(self, datasetColumn, datasetColumnForMCEWK, dsetMgr, luminosity, additionalNormalisation = 1.0):
        return 0.0

    ## Virtual method for extracting histograms
    # Returns the transverse mass plot
    def extractHistograms(self, datasetColumn, dsetMgr, mainCounterTable, luminosity, additionalNormalisation = 1.0):
        return []

    def getQCDmode(self):
        return self._QCDmode

    ## var _QCDmode
    # keyword for returning the stat, syst, or shapeStat results