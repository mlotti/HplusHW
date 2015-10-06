## \package QCDfactorised
# Classes for extracting and calculating multijet background with factorised approach

from LimitCalcExtractor import ExtractorMode,ExtractorBase
from LimitCalcDatacardColumn import ExtractorResult,DatacardColumn
from LimitCalcMulticrabPathFinder import MulticrabDirectoryDataType
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles as ShellStyles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import Count
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShapeHistoModifier import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.UnfoldedHistogramReader import *
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.dataDrivenQCDCount import *
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdCommon.systematicsForMetShapeDifference import *
from HiggsAnalysis.HeavyChHiggsToTauNu.qcdFactorised.qcdFactorisedResult import *

import math
import os
import sys
import ROOT

class QCDResultObject:
    def __init__(self, title):
        self._title = title
        self._NQCDResult = None
        self._minPurityObjects = [None, None, None]
        self._avgPurityObjects = [None, None, None]

    def setNQCDResult(self, r):
        self._NQCDResult = r.copy()

    def getNQCDResult(self):
        return self._NQCDResult

    def setPurityInfo(self, minPurity, avgPurity, i):
        self._minPurityObjects[i] = minPurity
        self._avgPurityObjects[i] = avgPurity

    def getInfoString(self, chosenResult=False):
        myOutput = "QCD factorised results summary for %s\n"%self._title
        if chosenResult:
            myOutput += "%s... NQCD = %s  (data stat=%.2f, MC EWK stat=%.2f)%s\n"%(ShellStyles.HighlightStyle(),self._NQCDResult.getResultStringFull("%.2f"),self._NQCDResult._dataUncert.uncertainty(),self._NQCDResult._mcUncert.uncertainty(),ShellStyles.NormalStyle())
        else:
            myOutput += "... NQCD = %s  (data stat=%.2f, MC EWK stat=%.2f)\n"%(self._NQCDResult.getResultStringFull("%.2f"),self._NQCDResult._dataUncert.uncertainty(),self._NQCDResult._mcUncert.uncertainty())
        myOutput += "... Purity after std. sel.: minimum = %s, average = %s\n"%(self._minPurityObjects[0].getResultStringFull("%.3f"),self._avgPurityObjects[0].getResultStringFull("%.3f"))
        myOutput += "... Purity after     leg1.: minimum = %s, average = %s\n"%(self._minPurityObjects[1].getResultStringFull("%.3f"),self._avgPurityObjects[1].getResultStringFull("%.3f"))
        myOutput += "... Purity after     leg2.: minimum = %s, average = %s\n"%(self._minPurityObjects[2].getResultStringFull("%.3f"),self._avgPurityObjects[2].getResultStringFull("%.3f"))
        return myOutput

        
        #FIXME
        
    ## Create a full size table assuming 3D factorisation
    def _createYieldTable(self):
        myBinDimensions = self.getReaderObject().getNbinsList()
        myBinCaptions = self.getReaderObject().getFactorisationRanges()
        myLatexBinCaptions = []
        for i in range(0,len(myBinCaptions)):
            myLatexBinCaptions.append([])
            for j in range(0,len(myBinCaptions[i])):
                myLatexBinCaptions[i].append(myBinCaptions[i][j].replace("<","$<$").replace(">","$>$"))
        #myBinCaptions = self.getReaderObject().getFactorisationFullBinLabels()
        ## Latexify bin captions
        #for i in range(0,len(myLatexBinCaptions)):
            #for j in range(0,len(myLatexBinCaptions[i])):
                ## replace root style greek letters by latex style
                #myStatus = True
                #pos = 0
                #while myStatus:
                    #a = myLatexBinCaptions[i][j].find("#",pos)
                    #if a < 0:
                        #myStatus = False
                    #else:
                        ## found
                        #b = myLatexBinCaptions[i][j].find(" ",a)
                        #myWord = myLatexBinCaptions[i][j][a:b]
                        #myLatexBinCaptions[i][j] = myLatexBinCaptions[i][j].replace(myWord,"$\\%s$"%myWord.replace("#",""))
                        #pos = b
                ## replace root style subscript by latex style
                #myStatus = True
                #pos = 0
                #while myStatus:
                    #a = myLatexBinCaptions[i][j].find("_",pos)
                    #if a < 0:
                        #myStatus = False
                    #else:
                        ## found
                        #b = myLatexBinCaptions[i][j].find("}",a)
                        #myWord = myLatexBinCaptions[i][j][a:b+1]
                        #myLatexBinCaptions[i][j] = myLatexBinCaptions[i][j].replace(myWord,"$%s$"%myWord)
                        #pos = b
                #myLatexBinCaptions[i][j] = myLatexBinCaptions[i][j].replace("<","$<$").replace(">","$>$")
        if len(myBinDimensions) != 3:
            return ""
        myOutput = ""
        # 3D table
        for i in range(0,myBinDimensions[0]):
            for k in range(0,myBinDimensions[2]):
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
                myPtCaption += "& \\multicolumn{3}{c}{%s \\GeVc}"%myLatexBinCaptions[0][i]
                for j in range(0,myBinDimensions[1]):
                    myTableStructure += "l"
                    myEtaCaption += "& \multicolumn{1}{c}{%s}"%myLatexBinCaptions[1][j]
                    myBasicDataRow += "& %s"%(self._basicCount.getDataCountObjects([i,j,k])[0].getLatexStringNoSyst("%.1f"))
                    myBasicEWKRow += "& %s"%(self._basicCount.getMCCountObjects([i,j,k])[0].getLatexStringFull("%.1f"))
                    myBasicPurityRow += "& %s"%(self._basicCount.getPurity([i,j,k])[0].getLatexStringFull("%.3f"))
                    myMetDataRow += "& %s"%(self._leg1Counts.getDataCountObjects([i,j,k])[0].getLatexStringNoSyst("%.1f"))
                    myMetEWKRow += "& %s"%(self._leg1Counts.getMCCountObjects([i,j,k])[0].getLatexStringFull("%.1f"))
                    myMetPurityRow += "& %s"%(self._leg1Counts.getPurity([i,j,k])[0].getLatexStringFull("%.2f"))
                    myTauDataRow += "& %s"%(self._leg2Counts.getDataCountObjects([i,j,k])[0].getLatexStringNoSyst("%.1f"))
                    myTauEWKRow += "& %s"%(self._leg2Counts.getMCCountObjects([i,j,k])[0].getLatexStringFull("%.1f"))
                    myTauPurityRow += "& %s"%(self._leg2Counts.getPurity([i,j,k])[0].getLatexStringFull("%.2f"))
                    myMetEffRow += "& %s"%(self.getLeg1Efficiency([i,j,k])[0].getLatexStringFull("%.4f"))
                    myNQCDRow += "& %s"%(self.getNQCD([i,j,k]).getLatexStringFull("%.1f"))
                # Construct table
                if k % 2 == 1: # FIXME assumed 2 bins for eta
                    myOutput += "\\renewcommand{\\arraystretch}{1.2}\n"
                    myOutput += "\\begin{table}[ht!]\n"
                    myOutput += "\\caption{Analytical breakdown of the \\NQcd estimate, showing the number of data and EWK MC events and\n"
                    myOutput += "  the purity of the sample after standard selections, after basic selections plus \\MET+btag+$\\Delta\\phi$, and\n"
                    myOutput += "  after all preselections. The efficiency of \\MET+btag+$\\Delta\\phi$ relative to basic selections and \n"
                    myOutput += "  the estimate for the number of QCD multi-jet events in the signal region (\\NQcd) are shown.\n"
                    myOutput += "  The numbers are shown for tau candidate \\pT bin %s \\GeVc.\n"%myLatexBinCaptions[0][i]
                    myOutput += "  The top table is for $N_{\\text{vertices}} < 8$,\n" #FIXME assumed 2 bins for eta
                    myOutput += "  whereas the bottom table is for $N_{\\text{vertices}} \geq 8$.\n"
                    myOutput += "  Wherever appropriate, the systematic uncertainty is shown in addition to the statistical uncertainty. } \n"
                    myOutput += "\\label{tab:background:qcdfact:evtyield:bin%d}\n"%(i)
                    myOutput += "\\vspace{1cm}\n"
                    myOutput += "%% NQCD analytical breakdown for tau pT bin %s and Nvtx bin %s\n"%(myLatexBinCaptions[0][i],myLatexBinCaptions[2][k])
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
        def _convertRangeToStr(ranges):
            if len(ranges) == 1:
                return ranges[0]
            if len(ranges) == 2:
                return "%s and %s"%(ranges[0],ranges[1])
            s = ""
            for i in range(0,len(ranges)-1):
                s += "%s, "%ranges[i]
            s += "and %s"%ranges[len(ranges)-1]
            return s

        myBinDimensions = self.getReaderObject().getNbinsList()
        myBinCaptions = self.getReaderObject().getFactorisationRanges()
        myLatexBinCaptions = []
        for i in range(0,len(myBinCaptions)):
            myLatexBinCaptions.append([])
            for j in range(0,len(myBinCaptions[i])):
                myLatexBinCaptions[i].append(myBinCaptions[i][j].replace("<","$<$").replace(">","$>$"))
        myTableStructure = ""
        myRanges = []
        myOutput = ""
        n = 0
        rows = 4
        for i in range(0,myBinDimensions[0]):
            if n == 0:
                myRanges = []
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
            myRanges.append(myLatexBinCaptions[0][i])
            myPtCaption += "& %s \\GeVc"%(myLatexBinCaptions[0][i])
            myTableStructure += "l"
            myBasicDataRow += "& %s"%(self._basicCount.getContracted1DDataCountObjects(i,0)[0].getLatexStringNoSyst("%.1f"))
            myBasicEWKRow += "& %s"%(self._basicCount.getContracted1DMCCountObjects(i,0)[0].getLatexStringFull("%.1f"))
            myBasicPurityRow += "& %s"%(self._basicCount.getContracted1DPurity(i,0)[0].getLatexStringFull("%.3f"))
            myMetDataRow += "& %s"%(self._leg1Counts.getContracted1DDataCountObjects(i,0)[0].getLatexStringNoSyst("%.1f"))
            myMetEWKRow += "& %s"%(self._leg1Counts.getContracted1DMCCountObjects(i,0)[0].getLatexStringFull("%.1f"))
            myMetPurityRow += "& %s"%(self._leg1Counts.getContracted1DPurity(i,0)[0].getLatexStringFull("%.2f"))
            myTauDataRow += "& %s"%(self._leg2Counts.getContracted1DDataCountObjects(i,0)[0].getLatexStringNoSyst("%.1f"))
            myTauEWKRow += "& %s"%(self._leg2Counts.getContracted1DMCCountObjects(i,0)[0].getLatexStringFull("%.1f"))
            myTauPurityRow += "& %s"%(self._leg2Counts.getContracted1DPurity(i,0)[0].getLatexStringFull("%.2f"))
            myMetEffRow += "& %s"%(self.getContracted1DLeg1Efficiency(i,0)[0].getLatexStringFull("%.4f"))
            myNQCDRow += "& %s"%(self.getContracted1DNQCDForBin(i,0).getLatexStringFull("%.1f"))
            # Construct table
            if n == rows-1 or i == myBinDimensions[0]-1:
                myOutput += "\\renewcommand{\\arraystretch}{1.2}\n"
                myOutput += "\\begin{table}[ht!]\n"
                myOutput += "\\caption{Analytical breakdown of the \\NQcd estimate for tau candidate \\pT ranges %s \\GeVc, showing the number of data and EWK MC events and\n"%_convertRangeToStr(myRanges)
                myOutput += "  the purity of the sample after standard selections, after basic selections plus \\MET+btag+$\\Delta\\phi$, and\n"
                myOutput += "  after all preselections. The efficiency of \\MET+btag+$\\Delta\\phi$ relative to basic selections and \n"
                myOutput += "  the estimate for the number of QCD multi-jet events in the signal region (\\NQcd) are shown.\n"
                myOutput += "  The bins of tau candidate $\\eta$ and $N_{\\text{vertices}}$ have been summed up.\n"
                myOutput += "  Wherever appropriate, the systematic uncertainty is shown in addition to the statistical uncertainty. } \n"
                myOutput += "\\label{tab:background:qcdfact:evtyield:tauptonly%d}\n"%((i-1)/rows+1)
                myOutput += "\\vspace{1cm}\n"
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
                #if i % 4 != 0:
                    #myOutput += "\\\\ \n"
                    #myOutput += "\\\\ \n"
            if n == rows-1 or i == myBinDimensions[0]-1:
                myOutput += "\\end{table}\n"
                myOutput += "\\renewcommand{\\arraystretch}{1.0}\n"
                myOutput += "\\newpage\n\n"
                n = 0
            else:
                n += 1
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
                 additionalNormalisationFactor = 1.0,
                 QCDfactorisedInfo = None,
                 debugMode = False):
        DatacardColumn.__init__(self,
                                label = "QCDfact",
                                landsProcess = landsProcess,
                                enabledForMassPoints = enabledForMassPoints,
                                datasetType = "QCD factorised",
                                nuisanceIds = nuisanceIds,
                                datasetMgrColumn = datasetMgrColumn,
                                additionalNormalisationFactor = additionalNormalisationFactor)
        # Store info dictionary for QCD factorised
        self._factorisedConfig = QCDfactorisedInfo
        # Other initialisation
        self._infoHistograms = []
        self._debugMode = debugMode
        self._messages = []
        self._yieldTable = ""
        self._compactYieldTable = ""
        self._METCorrectionFactorsForTauPtBins = []
        self._METCorrectionFactorUncertaintyForTauPtBins = []
        self._MTCorrectionFactorsForTauPtBins = []
        self._MTCorrectionFactorUncertaintyForTauPtBins = []
        self._contractedLabels = [] # Needed for histogram saving into subdirs


    ## Returns list of messages
    def getMessages(self):
        return self._messages

    def getYieldTable(self):
        return self._yieldTable

    def getCompactYieldTable(self):
        return self._compactYieldTable

    ## Do data mining and cache results
    def doDataMining(self, config, dsetMgr, luminosity, mainCounterTable, extractors, controlPlotExtractors):
        print "... processing column: "+ShellStyles.HighlightStyle()+self._label+ShellStyles.NormalStyle()
        if dsetMgr == None:
            raise Exception(ShellStyles.ErrorLabel()+"You called data mining for QCD factorised, but it's multicrab directory is not there. Such undertaking is currently not supported.")
        # Obtain data driven QCD shape objects for the points
        myQCDCountAfterStdSel = DataDrivenQCDShape(dsetMgr, self._datasetMgrColumn, self._datasetMgrColumnForQCDMCEWK, self._factorisedConfig["afterStdSelSource"], luminosity)
        myQCDCountAfterTauLeg = DataDrivenQCDShape(dsetMgr, self._datasetMgrColumn, self._datasetMgrColumnForQCDMCEWK, self._factorisedConfig["afterTauLegSource"], luminosity)
        myQCDCountAfterMETLeg = DataDrivenQCDShape(dsetMgr, self._datasetMgrColumn, self._datasetMgrColumnForQCDMCEWK, self._factorisedConfig["afterMETLegSource"], luminosity)
        # Print purity summary
        self._printPuritySummary(myQCDCountAfterStdSel, myQCDCountAfterTauLeg, myQCDCountAfterMETLeg)
        # Calculate result (notice that moduleInfoString is not needed because results of each module go already into a separate directory)
        myResult = QCDFactorisedResult(myQCDCountAfterStdSel, myQCDCountAfterMETLeg, myQCDCountAfterTauLeg, config.ShapeHistogramsDimensions, "")
        # Get final shape and cache it
        hRateShape = myResult.getResultShape().Clone()
        self._rateResult = ExtractorResult("rate", "rate", hRateShape.Integral(), [hRateShape])
        # Obtain MET shape difference systematics histograms (shape nuisance)
        myMETShapeSyst = SystematicsForMetShapeDifference(myQCDCountAfterTauLeg, myQCDCountAfterStdSel, myResult.getResultShape(), config.ShapeHistogramsDimensions, "")
        #self._yieldTable = myQCDCalculator.getYieldTable()
        #self._compactYieldTable = myQCDCalculator.getCompactYieldTable()
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
                        myResult = myChosenQCDResult.getRelativeStatUncertainty()
                    elif e.getQCDmode() == "systematics":
                        myResult = myChosenQCDResult.getRelativeMCSystUncertainty()
                    # Obtain histograms
                    myHistograms = []
                    if e.getQCDmode() == "shapestat":
                        # Clone rate histogram as up and down histograms
                        myHistograms.append(hRateShape.Clone(self._label+"_%sDown"%(e.getMasterId())))
                        myHistograms[0].SetTitle(self._label+"_%sDown"%(e.getMasterId()))
                        myHistograms.append(hRateShape.Clone(self._label+"_%sUp"%(e.getMasterId())))
                        myHistograms[1].SetTitle(self._label+"_%sUp"%(e.getMasterId()))
                        # Substract/Add one sigma to get Down/Up variation
                        for k in range(1, myHistograms[0].GetNbinsX()+1):
                            myHistograms[0].SetBinContent(k, myHistograms[0].GetBinContent(k) - myHistograms[0].GetBinError(k))
                            myHistograms[1].SetBinContent(k, myHistograms[1].GetBinContent(k) + myHistograms[1].GetBinError(k))
                    if e.getQCDmode() == "metShapeSyst":
                        # The +- 1 sigma variation is already in place, just clone histograms
                        myHistograms.append(myMETShapeSyst.getDownHistogram().Clone(self._label+"_%sDown"%(e.getMasterId())))
                        myHistograms[0].SetTitle(self._label+"_%sDown"%(e.getMasterId()))
                        myHistograms.append(myMETShapeSyst.getUpHistogram().Clone(self._label+"_%sUp"%(e.getMasterId())))
                        myHistograms[1].SetTitle(self._label+"_%sUp"%(e.getMasterId()))
                    # Cache result
                    self._nuisanceResults.append(ExtractorResult(e.getId(),
                                                                 e.getMasterId(),
                                                                 myResult,
                                                                 myHistograms,
                                                                 e.getQCDmode() == "statistics" or e.getQCDmode() == "shapestat"))
            if not myFoundStatus:
                raise Exception("\n"+ErrorStyle()+"Error (data group ='"+self._label+"'):"+ShellStyles.NormalStyle()+" Cannot find nuisance with id '"+nid+"'!")
        # Obtain results for control plots
        if config.OptionDoControlPlots != None:
            if config.OptionDoControlPlots:
                print "... Obtaining control plots ..."
                if config.ControlPlots != None and dsetMgr != None:
                    for c in config.ControlPlots:
                        # Obtain normalisation
                        myEventCount = self._getQCDEventCount(dsetMgr=dsetMgr, histoName=c.QCDFactNormalisation, luminosity=luminosity)
                        myQCDCalculator = QCDfactorisedCalculator(myStdSelEventCount, myEventCount, myTauLegEventCount, doHistograms=False)
                        #myQCDCalculator.getResult().getNQCDResult().printContents()
                        # Obtain shape histogram
                        hShape = None
                        if myFactorisationContractionIndex == None:
                            hShape = self._createControlHistogram(dsetMgr,luminosity,myQCDCalculator,histoSpecs=c.details,
                                                                  histoName=c.QCDFactHistoName, title=c.title)
                        else:
                            hShape = self._createContractedControlHistogram(myFactorisationContractionIndex,dsetMgr,luminosity,myQCDCalculator,histoSpecs=c.details,
                                                                            histoName=c.QCDFactHistoName, title=c.title)
                        # Do normalisation
                        myIntegral = None
                        if myFactorisationContractionIndex == None:
                            myIntegral = myQCDCalculator.getResult().getNQCDResult().value()
                        else:
                            myIntegral = myQCDCalculator.getContractedResultsList()[myFactorisationContractionIndex].getNQCDResult().value()
                        hShape.Scale(myIntegral / hShape.Integral())
                        #print "     "+c.title+", NQCD=%f"%myQCDCalculator.getResult().getNQCDResult().value()
                        myEventCount.clean()
                        self._controlPlots.append(hShape)
        # Clean up
        myQCDCalculator.clean()

###################################
    def _printPuritySummary(self, myQCDCountAfterStdSel, myQCDCountAfterTauLeg, myQCDCountAfterMETLeg):
        self._printPuritySummaryItem("after std.sel.", myQCDCountAfterStdSel.getIntegratedPurity(), myQCDCountAfterStdSel.getMinimumPurity())
        self._printPuritySummaryItem("after  tau leg", myQCDCountAfterTauLeg.getIntegratedPurity(), myQCDCountAfterTauLeg.getMinimumPurity())
        self._printPuritySummaryItem("after  MET leg", myQCDCountAfterMETLeg.getIntegratedPurity(), myQCDCountAfterMETLeg.getMinimumPurity())

    def _printPuritySummaryItem(self, label, purity, minPurity):
        myOutput = "QCDfactorised: Purity after %s: %.1f +- %.1f %%; min. purity = "%(label, purity.value()*100.0, purity.uncert()*100.0)
        if abs(minPurity.value()) < 0.00001:
            myOutput += "n.a."
        else:
            myOutput += "%.1f +- %.1f %%"%(minPurity.value()*100.0, minPurity.uncert()*100.0)
        print myOutput
        # TODO: add a warning for small purity?

###################################

                    
        
        
        
        
    def _getQCDEventCount(self, dsetMgr, histoName, luminosity):
        return QCDEventCount(histoName=histoName,
                             dsetMgr=dsetMgr,
                             dsetMgrDataColumn=self._datasetMgrColumn,
                             dsetMgrMCEWKColumn=self._datasetMgrColumnForQCDMCEWK,
                             luminosity=luminosity)

    #def _calculateMETCorrectionFactors(self, dsetMgr, luminosity):
        #myBinEdges = self._METCorrectionDetails[self._METCorrectionDetails["name"]+"_CorrectionBinLeftEdges"]
        #myMETHistoSpecs = { "bins": len(myBinEdges),
                            #"rangeMin": 0.0,
                            #"rangeMax": 400.0,
                            #"variableBinSizeLowEdges": myBinEdges,
                            #"xtitle": "",
                            #"ytitle": "" }
        #myShapeModifier = ShapeHistoModifier(myMETHistoSpecs)
        #h = myShapeModifier.createEmptyShapeHistogram("dummy")
        #myBins = self._METCorrectionDetails["bins"]
        ## Loop over bins
        ##print "***"
        #for i in range(0,myBins[0]):
            #for j in range(0,myBins[1]):
                #for k in range(0,myBins[2]):
                    ## Get data and MC EWK histogram
                    #myFullHistoName = "/%s_%d_%d_%d"%(self._METCorrectionDetails["source"],i,j,k)
                    #hMtData = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumn, myFullHistoName, luminosity)
                    #hMtMCEWK = self._extractShapeHistogram(dsetMgr, self._datasetMgrColumnForQCDMCEWK, myFullHistoName, luminosity)
                    ## Add to shape
                    #h.Reset()
                    #myShapeModifier.addShape(source=hMtData,dest=h)
                    #myShapeModifier.subtractShape(source=hMtMCEWK,dest=h,purityCheck=False)
                    #myShapeModifier.finaliseShape(dest=h)
                    ## Calculate nominal integral and corrected integral
                    #myNominalCount = h.Integral()
                    #myCorrections = self._METCorrectionDetails[self._METCorrectionDetails["name"]+"_Correction_bin_%d"%(i)]
                    #myCorrectionUncertainty = self._METCorrectionDetails[self._METCorrectionDetails["name"]+"_CorrectionUncertainty_bin_%d"%(i)]
                    #myCorrectedCount = 0.0
                    #myCorrectedUncertainty = 0.0
                    #for l in range(1,h.GetNbinsX()+1):
                        ##print "%f, %f"%( h.GetBinContent(l), myCorrections[l-1])
                        #myCorrectedCount += h.GetBinContent(l)*myCorrections[l-1]
                        #myCorrectedUncertainty += pow(h.GetBinContent(l)*myCorrectionUncertainty[l-1],2)
                    #myCorrectedUncertainty = sqrt(myCorrectedUncertainty)
                    ##print "*** MET correction %d: nominal = %f, corrected = %f +- %f"%(i,myNominalCount,myCorrectedCount,myCorrectedUncertainty)
                    #self._METCorrectionFactorsForTauPtBins.append(myCorrectedCount)
                    #self._METCorrectionFactorUncertaintyForTauPtBins.append(myCorrectedUncertainty)
                    #hMtData.IsA().Destructor(hMtData)
                    #hMtMCEWK.IsA().Destructor(hMtMCEWK)
        #h.IsA().Destructor(h)

    def _createControlHistogram(self, dsetMgr, luminosity, myQCDCalculator, histoSpecs, title, histoName):
        return self._createShapeHistogram(dsetMgr,luminosity,myQCDCalculator,histoSpecs=histoSpecs,
                                          histoName=histoName,title=title,label="Ctrl",
                                          saveDetailedInfo=False,makeCorrectionToShape=True,applyFullSystematics=False)

    def _createContractedControlHistogram(self, axisToKeep, dsetMgr, luminosity, myQCDCalculator, histoSpecs, title, histoName):
        return self._createContractedShapeHistogram(axisToKeep,dsetMgr,luminosity,myQCDCalculator,histoSpecs=histoSpecs,
                                          histoName=histoName,title=title,label="Ctrl",
                                          saveDetailedInfo=False,makeCorrectionToShape=True,applyFullSystematics=False)

    def _createClosureHistogram(self, dsetMgr, luminosity, myQCDCalculator, histoSpecs, histoName):
        return self._createShapeHistogram(dsetMgr,luminosity,myQCDCalculator,histoSpecs=histoSpecs,
                                          histoName=histoName,title=None,label="Closure",
                                          saveDetailedInfo=False,makeCorrectionToShape=True,applyFullSystematics=False,applyNQCDWeighting=False)

    def _createContractedClosureHistogram(self, axisToKeep, dsetMgr, luminosity, myQCDCalculator, histoSpecs, histoName):
        return self._createContractedShapeHistogram(axisToKeep,dsetMgr,luminosity,myQCDCalculator,histoSpecs=histoSpecs,
                                          histoName=histoName,title=None,label="Closure",
                                          saveDetailedInfo=True,makeCorrectionToShape=True,applyFullSystematics=False,applyNQCDWeighting=False)

    def _createShapeHistogram(self, dsetMgr, luminosity, myQCDCalculator, histoSpecs, title, histoName, label=None, saveDetailedInfo=False, makeCorrectionToShape=False, applyFullSystematics=False, applyNQCDWeighting=True):
        # Open histograms and create QCD event object
        myEventCountObject = self._getQCDEventCount(dsetMgr, histoName, luminosity)
        # Create empty shape histogram
        myShapeModifier = ShapeHistoModifier(histoSpecs)
        myName = "Shape_%s"%histoName.replace("/","_")
        if label != None:
            myName = "%s_%s"%(label,myName)
        hStat = myShapeModifier.createEmptyShapeHistogram(myName+"_statUncert")
        hFull = myShapeModifier.createEmptyShapeHistogram(myName+"_fullUncert")
        # Obtain bin dimensions
        myNUnfoldedFactorisationBins = myEventCountObject.getReader().getUnfoldedBinCount()
        # Loop over unfoldedfactorisation bins
        for i in range(0,myNUnfoldedFactorisationBins):
            # Get histograms for the bin for data and MC EWK
            hShapeData = myEventCountObject.getDataShapeByUnfoldedBin(i)
            hShapeMCEWK = myEventCountObject.getMCShapeByUnfoldedBin(i,includeSystematics=False)
            hShapeMCEWKFullSyst = myEventCountObject.getMCShapeByUnfoldedBin(i,includeSystematics=True)
            if self._debugMode:
                print "  QCDfactorised / %s: bin%d, data=%f, MC EWK=%f, QCD=%f"%(myName,i,hShapeData.Integral(0,hShapeData.GetNbinsX()+1),hShapeMCEWK.Integral(0,hShapeMCEWK.GetNbinsX()+1),hShapeData.Integral(0,hShapeData.GetNbinsX()+1)-hShapeMCEWK.Integral(0,hShapeMCEWK.GetNbinsX()+1))
            else:
                sys.stdout.write("\r... Obtaining shape: %s %3d/%d"%(histoName, i+1,myNUnfoldedFactorisationBins))
                sys.stdout.flush()
            # Weight shape by efficiency of tau leg
            if applyNQCDWeighting:
                myEfficiency = myQCDCalculator.getLeg2EfficiencyByUnfoldedBin(i, onlyNominatorUncert=True)
                for k in range(0,hShapeData.GetNbinsX()+2):
                    # f=a*b; Delta f^2 = (b Delta a)^2 + (a Delta b)^2
                    hShapeData.SetBinError(k,          sqrt((myEfficiency[0].value()*hShapeData.GetBinError(k))**2 +          (myEfficiency[0].uncertainty()    *hShapeData.GetBinContent(k))**2))
                    hShapeMCEWK.SetBinError(k,         sqrt((myEfficiency[0].value()*hShapeMCEWK.GetBinError(k))**2 +         (myEfficiency[0].uncertainty()    *hShapeMCEWK.GetBinContent(k))**2))
                    hShapeMCEWKFullSyst.SetBinError(k, sqrt((myEfficiency[0].value()*hShapeMCEWKFullSyst.GetBinError(k))**2 + (myEfficiency[0].totalUncertainty()*hShapeMCEWKFullSyst.GetBinContent(k))**2))
                    hShapeData.SetBinContent(k,hShapeData.GetBinContent(k)*myEfficiency[0].value())
                    hShapeMCEWK.SetBinContent(k,hShapeMCEWK.GetBinContent(k)*myEfficiency[0].value())
                    hShapeMCEWKFullSyst.SetBinContent(k,hShapeMCEWKFullSyst.GetBinContent(k)*myEfficiency[0].value())
            # Add data
            myShapeModifier.addShape(source=hShapeData,dest=hStat)
            myShapeModifier.addShape(source=hShapeData,dest=hFull)
            # Subtract MC EWK from data to obtain QCD shape, obtain also warning messages concerning purity
            myShapeModifier.subtractShape(source=hShapeMCEWK,dest=hStat,purityCheck=False)
            myShapeModifier.subtractShape(source=hShapeMCEWKFullSyst,dest=hFull,purityCheck=False)
            # Create a histogram for each bin
            if saveDetailedInfo:
                hStatBin = myShapeModifier.createEmptyShapeHistogram(myName+"_binInfo%d_statUncert"%i)
                myShapeModifier.addShape(source=hShapeData,dest=hStatBin)
                myMessages = myShapeModifier.subtractShape(source=hShapeMCEWK,dest=hStatBin,purityCheck=True)
                myShapeModifier.finaliseShape(dest=hStatBin)
                hFullBin = myShapeModifier.createEmptyShapeHistogram(myName+"_binInfo%d_fullUncert"%i)
                myShapeModifier.subtractShape(source=hShapeMCEWKFullSyst,dest=hFullBin,purityCheck=False)
                myShapeModifier.addShape(source=hShapeData,dest=hFullBin)
                myShapeModifier.finaliseShape(dest=hFullBin)
                # No correction applied to see the shape like it is
                #if makeCorrectionToShape:
                    #myShapeModifier.correctNegativeBins(dest=hStatBin)
                    #myShapeModifier.correctNegativeBins(dest=hSFullBin)
                # Filter away unimportant messages
                if len(myMessages) > 0:
                    myTotal = hStatBin.Integral(0,hStatBin.GetNbinsX()+2)
                    for m in myMessages:
                        # Filter out only important warnings of inpurity (impact more than one percent to whole bin)
                        if myTotal > 0.0:
                            if m[1] / myTotal > 0.01:
                                self._messages.append(ShellStyles.WarningLabel()+"Low purity in QCD factorised shape %s for unfolded bin %d : %s"%(histoName, i, m[0]))
                # Save histograms
                self._infoHistograms.append(hStatBin)
                self._infoHistograms.append(hFullBin)
        # Finalise shape (underflow added to first bin, overflow added to last bin, variances converted to std.deviations)
        myShapeModifier.finaliseShape(dest=hStat)
        myShapeModifier.finaliseShape(dest=hFull)
        # Set negative bins to zero, but keep normalisationn
        if makeCorrectionToShape:
            myShapeModifier.correctNegativeBins(dest=hStat)
            myShapeModifier.correctNegativeBins(dest=hFull)
        # Normalise to NQCD
        if applyNQCDWeighting:
            myValue = myQCDCalculator.getResult().getNQCDResult().value()
            hStat.Scale(myValue / hStat.Integral(0,hStat.GetNbinsX()+2))
            hFull.Scale(myValue / hFull.Integral(0,hStat.GetNbinsX()+2))
        # Save histograms
        self._infoHistograms.append(hStat)
        self._infoHistograms.append(hFull)
        # Return the one asked for
        myEventCountObject.clean()
        sys.stdout.write("\n")
        if title == None:
            return None
        h = None
        if applyFullSystematics:
            h = hFull.Clone(title)
        else:
            h = hStat.Clone(title)
        h.SetTitle(title)
        return h

    def _createContractedShapeHistogram(self, axisToKeep, dsetMgr, luminosity, myQCDCalculator, histoSpecs, title, histoName, label=None, saveDetailedInfo=False, makeCorrectionToShape=False, applyFullSystematics=False, applyNQCDWeighting=True):
        # Open histograms and create QCD event object
        myEventCountObject = QCDEventCount(histoName, dsetMgr, self._datasetMgrColumn, self._datasetMgrColumnForQCDMCEWK, luminosity)
        # Create empty shape histogram
        myShapeModifier = ShapeHistoModifier(histoSpecs)
        myContractionLabel = myEventCountObject.getReader().getBinLabelList()[axisToKeep]
        myName = "Shape_%s_%s"%(myContractionLabel,histoName.replace("/","_"))
        if label != None:
            myName = "%s_%s"%(label,myName)
        hStat = myShapeModifier.createEmptyShapeHistogram(myName+"_statUncert")
        hFull = myShapeModifier.createEmptyShapeHistogram(myName+"_fullUncert")
        # Obtain bin dimensions
        myNUnfoldedFactorisationBins = myEventCountObject.getReader().getUnfoldedBinCount()
        # Loop over unfoldedfactorisation bins
        myNbins = myEventCountObject.getReader().getNbinsList()
        myMaxBins = myNbins[axisToKeep]
        for i in range(0,myMaxBins):
            # Get histograms for the bin for data and MC EWK
            hShapeData = myEventCountObject.getContracted1DDataShape(i,axisToKeep)
            hShapeMCEWK = myEventCountObject.getContracted1DMCShape(i,axisToKeep,includeSystematics=False)
            hShapeMCEWKFullSyst = myEventCountObject.getContracted1DMCShape(i,axisToKeep,includeSystematics=True)
            if self._debugMode:
                print "  QCDfactorised / %s: contraction%d bin%d, data=%f, MC EWK=%f, QCD=%f"%(myName,axisToKeep,i,hShapeData.Integral(0,hShapeData.GetNbinsX()+1),hShapeMCEWK.Integral(0,hShapeMCEWK.GetNbinsX()+1),hShapeData.Integral(0,hShapeData.GetNbinsX()+1)-hShapeMCEWK.Integral(0,hShapeMCEWK.GetNbinsX()+1))
            else:
                sys.stdout.write("\r... Obtaining contracted (%s) shape %s:  %3d/%d"%(myContractionLabel, histoName, i+1,myMaxBins))
                sys.stdout.flush()
            # Weight shape by efficiency of tau leg
            if applyNQCDWeighting:
                myEfficiency = myQCDCalculator.getLeg2EfficiencyByUnfoldedBin(i, onlyNominatorUncert=True)
                for k in range(0,hShapeData.GetNbinsX()+2):
                    # f=a*b; Delta f^2 = (b Delta a)^2 + (a Delta b)^2
                    hShapeData.SetBinError(k,          sqrt((myEfficiency[0].value()*hShapeData.GetBinError(k))**2 +          (myEfficiency[0].uncertainty()    *hShapeData.GetBinContent(k))**2))
                    hShapeMCEWK.SetBinError(k,         sqrt((myEfficiency[0].value()*hShapeMCEWK.GetBinError(k))**2 +         (myEfficiency[0].uncertainty()    *hShapeMCEWK.GetBinContent(k))**2))
                    hShapeMCEWKFullSyst.SetBinError(k, sqrt((myEfficiency[0].value()*hShapeMCEWKFullSyst.GetBinError(k))**2 + (myEfficiency[0].totalUncertainty()*hShapeMCEWKFullSyst.GetBinContent(k))**2))
                    hShapeData.SetBinContent(k,hShapeData.GetBinContent(k)*myEfficiency[0].value())
                    hShapeMCEWK.SetBinContent(k,hShapeMCEWK.GetBinContent(k)*myEfficiency[0].value())
                    hShapeMCEWKFullSyst.SetBinContent(k,hShapeMCEWKFullSyst.GetBinContent(k)*myEfficiency[0].value())
            # Add data
            myShapeModifier.addShape(source=hShapeData,dest=hStat)
            myShapeModifier.addShape(source=hShapeData,dest=hFull)
            # Subtract MC EWK from data to obtain QCD shape, obtain also warning messages concerning purity
            myShapeModifier.subtractShape(source=hShapeMCEWK,dest=hStat,purityCheck=False)
            myShapeModifier.subtractShape(source=hShapeMCEWKFullSyst,dest=hFull,purityCheck=False)
            # Create a histogram for each bin
            if saveDetailedInfo:
                hStatBin = myShapeModifier.createEmptyShapeHistogram(myName+"_binInfo%d_statUncert"%i)
                myShapeModifier.addShape(source=hShapeData,dest=hStatBin)
                myMessages = myShapeModifier.subtractShape(source=hShapeMCEWK,dest=hStatBin,purityCheck=True)
                myShapeModifier.finaliseShape(dest=hStatBin)
                hFullBin = myShapeModifier.createEmptyShapeHistogram(myName+"_binInfo%d_fullUncert"%i)
                myShapeModifier.subtractShape(source=hShapeMCEWKFullSyst,dest=hFullBin,purityCheck=False)
                myShapeModifier.addShape(source=hShapeData,dest=hFullBin)
                myShapeModifier.finaliseShape(dest=hFullBin)
                # No correction applied to see the shape like it is
                #if makeCorrectionToShape:
                    #myShapeModifier.correctNegativeBins(dest=hStatBin)
                    #myShapeModifier.correctNegativeBins(dest=hSFullBin)
                # Filter away unimportant messages
                if len(myMessages) > 0:
                    myTotal = hStatBin.Integral(0,hStatBin.GetNbinsX()+2)
                    for m in myMessages:
                        # Filter out only important warnings of inpurity (impact more than one percent to whole bin)
                        if myTotal > 0.0:
                            if m[1] / myTotal > 0.01:
                                self._messages.append(ShellStyles.WarningLabel()+"Low purity in QCD factorised shape %s for contraction %d bin %d : %s"%(histoName, axisToKeep, i, m[0]))
                # Save histograms
                self._infoHistograms.append(hStatBin)
                self._infoHistograms.append(hFullBin)
        # Finalise shape (underflow added to first bin, overflow added to last bin, variances converted to std.deviations)
        myShapeModifier.finaliseShape(dest=hStat)
        myShapeModifier.finaliseShape(dest=hFull)
        # Set negative bins to zero, but keep normalisationn
        if makeCorrectionToShape:
            myShapeModifier.correctNegativeBins(dest=hStat)
            myShapeModifier.correctNegativeBins(dest=hFull)
        # Save histograms
        self._infoHistograms.append(hStat)
        self._infoHistograms.append(hFull)
        # Normalise to NQCD
        if applyNQCDWeighting:
            myValue = myQCDCalculator.getContractedResultsList()[axisToKeep].getNQCDResult().value()
            hStat.Scale(myValue / hStat.Integral(0,hStat.GetNbinsX()+2))
            hFull.Scale(myValue / hFull.Integral(0,hStat.GetNbinsX()+2))
        # Return the one asked for
        myEventCountObject.clean()
        sys.stdout.write("\n")
        if title == None:
            return None
        h = None
        if applyFullSystematics:
            h = hFull.Clone(title)
        else:
            h = hStat.Clone(title)
        h.SetTitle(title)
        return h

    ## Saves information histograms into a histogram
    def saveQCDInfoHistograms(self, outputDir):
        # Open root file for saving
        myRootFilename = outputDir+"/QCDMeasurementFactorisedInfo.root"
        myRootFile = ROOT.TFile.Open(myRootFilename, "RECREATE")
        if myRootFile == None:
            print ErrorStyle()+"Error:"+ShellStyles.NormalStyle()+" Cannot open file '"+myRootFilename+"' for output!"
            sys.exit()
        # Make base directories
        myBaseDirs = []
        myDirs = []
        for contractionLabel in self._contractedLabels:
            myBaseDirs.append(myRootFile.mkdir("Contraction_%s"%contractionLabel.replace(" ","_")))
            myDirs.append({})
        myBaseDirs.append(myRootFile.mkdir("Full_factorisation"))
        myDirs.append({})
        # Loop over info histograms

        for k in range(0, len(self._infoHistograms)):
            histoname = self._infoHistograms[k].GetName()
            # Determine base directory
            myBaseDirIndex = len(myBaseDirs)-1
            for i in range(0,len(self._contractedLabels)):
                label = self._contractedLabels[i].replace(" ","_")
                if label in histoname:
                    myBaseDirIndex = i
                    self._infoHistograms[k].SetTitle(self._infoHistograms[k].GetTitle().replace(label+"_",""))
                    self._infoHistograms[k].SetName(self._infoHistograms[k].GetName().replace(label+"_",""))
                    histoname = self._infoHistograms[k].GetName()
            # Store bin histograms in dedicated subdirectory
            if "Shape" in histoname:
                # Find stem
                mySplit = histoname.split("_")
                myStatus = True
                s = ""
                for subs in mySplit:
                    if "Uncert" in subs or "binInfo" in subs:
                        myStatus = False
                    if myStatus:
                        s += subs+"_"
                s = s[0:len(s)-1] # Remove trailing underscore
                # Make new subdirectory if necessary
                if not s in myDirs[myBaseDirIndex].keys():
                    myDirs[myBaseDirIndex][s] = myBaseDirs[myBaseDirIndex].mkdir(s)
                self._infoHistograms[k].SetDirectory(myDirs[myBaseDirIndex][s])
            # Store summary histogram in main directory
            else:
                self._infoHistograms[k].SetDirectory(myBaseDirs[myBaseDirIndex])

        # Close root file
        myRootFile.Write()
        myRootFile.Close()
        # Cleanup (closing the root file destroys the objects assigned to it, do not redestroy the histos in the _infoHistograms list
        self._infoHistograms = []
        print "\n"+ShellStyles.HighlightStyle()+"QCD Measurement factorised info histograms saved to: "+ShellStyles.NormalStyle()+myRootFilename

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
    # keyword for returning the stat, syst, or bin-by-bin stat. uncert. results

def validateQCDCountObject():
    def check(a,b):
        if abs(a-b) < 0.00001:
            return TestPassedStyle()+"PASSED"+ShellStyles.NormalStyle()
        else:
            print ErrorStyle()+"FAILED (%f != %f)"%(a,b)+ShellStyles.NormalStyle()
            raise Exception("Error: validation test failed!")
    print ShellStyles.HighlightStyle()+"validate: QCDCountObject\n"+ShellStyles.NormalStyle()
    #aa = Count(25.0, 3.0, 0.0)
    #bb = Count(30.0, 0.0, 2.0)
    #cc = aa.copy()
    #cc.multiply(bb)
    #print cc._value, cc._uncertainty, cc._systUncertainty
    a = QCDCountObject(25.0, 3.0, 0.0, 0.0)
    #a.printContents()
    b = QCDCountObject(30.0, 0.0, 2.0, 1.0)
    #b.printContents()
    c = a.copy()
    c.add(b)
    #c.printContents()
    print "validate: QCDCountObject::add() value:",check(c.value(), 55.0)
    print "validate: QCDCountObject::add() data uncert:",check(c._dataUncert.uncertainty(), 3.0)
    print "validate: QCDCountObject::add() mc stat uncert:",check(c._mcUncert.uncertainty(), 2.0)
    print "validate: QCDCountObject::add() mc stat uncert:",check(c._mcUncert.systUncertainty(), 1.0)
    print "validate: QCDCountObject::sanityCheck() mc stat uncert:",check(c.sanityCheck(), True)
    d = QCDCountObject(10.0, 4.0, 2.0, 3.0)
    d.multiply(a)
    #d.printContents()
    print "validate: QCDCountObject::multiply() value:",check(d.value(), 250.0)
    print "validate: QCDCountObject::multiply() data uncert:",check(d._dataUncert.uncertainty(), sqrt(10900.0))
    print "validate: QCDCountObject::multiply() mc stat uncert:",check(d._mcUncert.uncertainty(), 50.0)
    print "validate: QCDCountObject::multiply() mc stat uncert:",check(d._mcUncert.systUncertainty(), 75.0)
    print "validate: QCDCountObject::sanityCheck() mc stat uncert:",check(d.sanityCheck(), True)
    e = QCDCountObject(10.0, 4.0, 2.0, 3.0)
    e.divide(a)
    #e.printContents()
    print "validate: QCDCountObject::divide() value:",check(e.value(), 0.4)
    print "validate: QCDCountObject::divide() data uncert:",check(e._dataUncert.uncertainty(), 0.4*sqrt(109.0/625.0))
    print "validate: QCDCountObject::divide() mc stat uncert:",check(e._mcUncert.uncertainty(), 0.4*2.0/10.0)
    print "validate: QCDCountObject::divide() mc stat uncert:",check(e._mcUncert.systUncertainty(), 0.4*3.0/10.0)
    print "validate: QCDCountObject::sanityCheck() mc stat uncert:",check(e.sanityCheck(), True)
