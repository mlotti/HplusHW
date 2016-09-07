## \package TableProducer
# Classes for producing output
#
#

from HiggsAnalysis.LimitCalc.Extractor import ExtractorBase
from HiggsAnalysis.LimitCalc.DatacardColumn import DatacardColumn
from HiggsAnalysis.LimitCalc.ControlPlotMaker import ControlPlotMaker
from HiggsAnalysis.NtupleAnalysis.tools.systematics import ScalarUncertaintyItem
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.git as git

from math import pow,sqrt
import os
import sys
import time
import ROOT

## Creates and returns a list of bin-by-bin stat. uncert. histograms
# Inputs:
#   hRate  rate histogram
#   xmin   float, specifies minimum value for which bin-by-bin histograms are created (default: all)
#   xmax   float, specifies maximum value for which bin-by-bin histograms are created (default: all)
def createBinByBinStatUncertHistograms(hRate, minimumStatUncertainty=0.5, xmin=None, xmax=None):
    myList = []
    myName = hRate.GetTitle()
    # Construct range
    myRangeMin = xmin
    myRangeMax = xmax
    if myRangeMin == None:
        myRangeMin = hRate.GetXaxis().GetBinLowEdge(1)
    if myRangeMax == None:
        myRangeMax = hRate.GetXaxis().GetBinUpEdge(hRate.GetNbinsX())
    # Loop over bins
    for i in range(1, hRate.GetNbinsX()+1):
        #print hRate.GetXaxis().GetBinLowEdge(i), xmin, hRate.GetXaxis().GetBinUpEdge(i), xmax
        if hRate.GetXaxis().GetBinLowEdge(i) > myRangeMin-0.0001 and hRate.GetXaxis().GetBinUpEdge(i) < myRangeMax+0.0001:
            #print "*"
            hUp = aux.Clone(hRate, "%s_%s_statBin%dUp"%(myName,myName,i))
            hDown = aux.Clone(hRate, "%s_%s_statBin%dDown"%(myName,myName,i))
            hUp.SetTitle(hUp.GetName())
            hDown.SetTitle(hDown.GetName())
            if hRate.GetBinContent(i) < minimumStatUncertainty:
                hUp.SetBinContent(i, minimumStatUncertainty)
                print ShellStyles.WarningLabel()+"Rate is zero for bin %d, setting up stat. uncert. to %f for %s."%(i,minimumStatUncertainty,hRate.GetTitle())
                if hRate.GetBinContent(i) < 0.0:
                    print ShellStyles.WarningLabel()+"Rate is negative for bin %d, continue at your own risk!"%i
            else:
                hUp.SetBinContent(i, hUp.GetBinContent(i)+hUp.GetBinError(i))
            
            hDown.SetBinContent(i, hDown.GetBinContent(i)-hDown.GetBinError(i))
            # Clear uncertainty bins, because they have no effect on LandS/Combine
            for j in range(1, hRate.GetNbinsX()+1):
                hUp.SetBinError(j, 0.0)
                hDown.SetBinError(j, 0.0)
            myList.append(hUp)
            myList.append(hDown)
    return myList

## Creates and returns a list of bin-by-bin stat. uncert. name strings
# Inputs:
#   hRate  rate histogram
def createBinByBinStatUncertNames(hRate):
    myList = []
    myName = hRate.GetTitle()
    for i in range(1, hRate.GetNbinsX()+1):
        myList.append(myName+"_statBin%d"%i)
    return myList

## Calculates maximum width of each table cell
def calculateCellWidths(widths,table):
    myResult = widths
    # Initialise widths if necessary
    if len(table) == 0:
      return myResult

    for i in range(len(widths),len(table[0])):
        myResult.append(0)
    # Loop over table cells
    for row in table:
        for i in range(0,len(row)):
            if len(row[i]) > myResult[i]:
                myResult[i] = len(row[i])
    return myResult

## Returns a separator line of correct total width
def getSeparatorLine(widths):
    myTotalSize = 0
    for cell in widths:
        myTotalSize += cell+1
    myTotalSize -= 1
    myResult = ""
    for i in range(0,myTotalSize):
        myResult += "-"
    myResult += "\n"
    return myResult

## Converts a list into a string
def getTableOutput(widths,table,latexMode=False):
    myResult = ""
    for row in table:
        for i in range(0,len(row)):
            if i != 0:
                myResult += " "
                if latexMode:
                    myResult += "& "
            myResult += row[i].ljust(widths[i])
        if latexMode:
            myResult += " \\\\ "
        myResult += "\n"
    return myResult

## TableProducer class
class TableProducer:
    ## Constructor
    def __init__(self, opts, config, outputPrefix, luminosity, observation, datasetGroups, extractors, mcrabInfoOutput):
        self._opts = opts
        self._config = config
        self._outputPrefix = outputPrefix
        self._luminosity = luminosity
        self._observation = observation
        self._datasetGroups = datasetGroups
        self._purgeColumnsWithSmallRateDoneStatus = False
        self._extractors = extractors[:]
        self._timestamp = time.strftime("%y%m%d_%H%M%S", time.gmtime(time.time()))
        if self._opts.lands:
            self._outputFileStem = "lands_datacard_hplushadronic_m"
            self._outputRootFileStem = "lands_histograms_hplushadronic_m"
        elif self._opts.combine:
            self._outputFileStem = "combine_datacard_hplushadronic_m"
            self._outputRootFileStem = "combine_histograms_hplushadronic_m"
        # Calculate number of nuisance parameters
        # Make directory for output
        myLimitCode = None
        if opts.lands:
            myLimitCode = "lands"
        elif opts.combine:
            myLimitCode = "combine"
        self._dirname = "datacards_%s_%s_%s_%s"%(myLimitCode,self._timestamp,self._config.DataCardName.replace(" ","_"),self._outputPrefix)
        if hasattr(self._config, "OptionSignalInjection"):
            self._dirname += "_SignalInjection"
        os.mkdir(self._dirname)
        self._infoDirname = self._dirname + "/info"
        os.mkdir(self._infoDirname)
        self._ctrlPlotDirname = self._dirname + "/controlPlots"
        os.mkdir(self._ctrlPlotDirname)
        # Copy datacard to directory
        os.system("cp %s %s/inputDatacardForDatacardGenerator.py"%(opts.datacard, self._dirname))

        # Make control plots
        if self._config.OptionDoControlPlots:
            ControlPlotMaker(self._opts, self._config, self._ctrlPlotDirname, self._luminosity, self._observation, self._datasetGroups)
        else:
            print "\n"+ShellStyles.WarningLabel()+"Skipped making of data-driven Control plots. To enable, set OptionDoControlPlots = True in the input datacard."

        # Make other reports
        print "\n"+ShellStyles.HighlightStyle()+"Generating reports"+ShellStyles.NormalStyle()
        # Print table of shape variation for shapeQ nuisances
        self.makeShapeVariationTable()
        # Print event yield summary table
        self.makeEventYieldSummary()
        # Print systematics summary table
        self.makeSystematicsSummary(light=True)
        self.makeSystematicsSummary(light=False)        
        # Prints QCD purity information
        #self.makeQCDPuritySummary() #FIXME missing

        # Make datacards
        self.makeDataCards()

        # Debugging info
        # Make copy of input datacard
        os.system("cp %s %s/input_datacard.py"%(self._opts.datacard,self._infoDirname))
        # Write input multicrab directory names
        f = open(os.path.join(self._infoDirname, "inputDirectories.txt"), "w")
        f.write("\n".join(map(str, mcrabInfoOutput))+"\n")
        f.close()
        f = open(os.path.join(self._infoDirname, "codeVersion.txt"), "w")
        f.write(git.getCommitId()+"\n")
        f.close()
        f = open(os.path.join(self._infoDirname, "codeStatus.txt"), "w")
        f.write(git.getStatus()+"\n")
        f.close()
        f = open(os.path.join(self._infoDirname, "codeDiff.txt"), "w")
        f.write(git.getDiff()+"\n")
        f.close()
        
        self._extractors = extractors[:]
        
        # Create for each shape nuisance a variation 
        if opts.testShapeSensitivity:
            self._createDatacardsForShapeSensitivityTest()
            
    ## Returns name of results directory
    def getDirectory(self):
        return self._dirname

    ## Generates datacards
    def makeDataCards(self):

        # For combine, do some formatting
        if self._opts.combine and not self._purgeColumnsWithSmallRateDoneStatus:
            mySubtractAfterId = None
            mySmallestColumnId = 9
            # Find and remove empty column
            myRemoveList = []
            for c in self._datasetGroups:
                if c.getLandsProcess() < mySmallestColumnId:
                    mySmallestColumnId = c.getLandsProcess()
                if c.typeIsEmptyColumn():
                    mySubtractAfterId = c.getLandsProcess()
                    myRemoveList.append(c)
            if len(myRemoveList) > 0:
                self._datasetGroups.remove(c)
                print "Removed empty column for combine datacard"
            for c in self._datasetGroups:
                if c.getLandsProcess() > mySubtractAfterId:
                    c._landsProcess = c.getLandsProcess() - 1
            # Move column with ID -1 to zero
            #if mySmallestColumnId < 0:
            #    for c in self._datasetGroups:
            #        c._landsProcess = c.getLandsProcess() + 1

        self._purgeColumnsWithSmallRate()

        # Loop over mass points
        for m in self._config.MassPoints:
            print "\n"+ShellStyles.HighlightStyle()+"Generating datacard for mass point %d for "%m +self._outputPrefix+ShellStyles.NormalStyle()
            # Open output root file
            myFilename = self._dirname+"/"+self._outputFileStem+"%d.txt"%m
            myRootFilename = self._dirname+"/"+self._outputRootFileStem+"%d.root"%m
            myRootFile = ROOT.TFile.Open(myRootFilename, "RECREATE")
            if myRootFile == None:
                print ErrorStyle()+"Error:"+ShellStyles.NormalStyle()+" Cannot open file '"+myRootFilename+"' for output!"
                sys.exit()
            # Invoke extractors
            if self._opts.verbose:
                print "TableProducer/producing observation line"
            myObservationLine = self._generateObservationLine()
            if self._opts.verbose:
                print "TableProducer/producing rate line"
            myRateHeaderTable = self._generateRateHeaderTable(m)
            myRateDataTable = self._generateRateDataTable(m)
            if self._opts.verbose:
                print "TableProducer/producing nuisance lines"
            myNuisanceTable = self._generateNuisanceTable(m)
            if self._opts.verbose:
                print "TableProducer/producing bin-by-bin stat. lines"
            myBinByBinStatUncertTable = self._generateBinByBinStatUncertTable(m)
            # Calculate dimensions of tables
            myWidths = []
            myWidths = calculateCellWidths(myWidths, myRateHeaderTable)
            myWidths = calculateCellWidths(myWidths, myRateDataTable)
            myWidths = calculateCellWidths(myWidths, myNuisanceTable)
            myWidths = calculateCellWidths(myWidths, myBinByBinStatUncertTable)
            mySeparatorLine = getSeparatorLine(myWidths)
            # Construct datacard
            myCard = ""
            myCard += self._generateHeader(m)
            myCard += mySeparatorLine
            myCard += self._generateParameterLines(len(myNuisanceTable))
            myCard += mySeparatorLine
            myCard += self._generateShapeHeader(m)
            myCard += mySeparatorLine
            myCard += myObservationLine
            myCard += mySeparatorLine
            myCard += getTableOutput(myWidths,myRateHeaderTable)
            myCard += mySeparatorLine
            myCard += getTableOutput(myWidths,myRateDataTable)
            myCard += mySeparatorLine
            myCard += getTableOutput(myWidths,myNuisanceTable)
            if self._opts.combine:
                myCard += mySeparatorLine
                myCard += getTableOutput(myWidths,myBinByBinStatUncertTable)
            # Print datacard to screen if requested
            if self._opts.showDatacard:
                if self._config.BlindAnalysis:
                    print ShellStyles.WarningStyle()+"You are BLINDED: Refused cowardly to print datacard on screen (you're not supposed to look at it)!"+ShellStyles.NormalStyle()
                else:
                    print myCard
            # Save datacard to file
            myFile = open(myFilename, "w")
            myFile.write(myCard)
            myFile.close()
            print "Written datacard to:",myFilename
            # Save histograms to root file
            self._saveHistograms(myRootFile,m),
            # Close root file
            myRootFile.Write()
            myRootFile.Close()
            print "Written shape root file to:",myRootFilename

    ## Purge columns with zero rate
    def _purgeColumnsWithSmallRate(self):
        if self._purgeColumnsWithSmallRateDoneStatus:
            return
        myLastUntouchableLandsProcessNumber = 0 # For sigma x br
        if not self._config.OptionLimitOnSigmaBr and (self._datasetGroups[0].getLabel()[:2] == "HW" or self._datasetGroups[1].getLabel()[:2] == "HW"):
            if self._opts.lands:
                myLastUntouchableLandsProcessNumber = 2 # For light H+ physics model
            elif self._opts.combine:
                myLastUntouchableLandsProcessNumber = 1 # For light H+ physics model
        myIdsForRemoval = []
        for c in self._datasetGroups:
            if c.getLandsProcess() > myLastUntouchableLandsProcessNumber:
                if abs(c._rateResult.getResult()) < self._config.ToleranceForMinimumRate:
                    # Zero rate, flag column for removal
                    myIdsForRemoval.append(c.getLandsProcess())
        # Remove columns
        for i in myIdsForRemoval:
            for c in self._datasetGroups:
                if c.getLandsProcess() == i:
                    print ShellStyles.WarningLabel()+"Rate for column '%s' (%f) is smaller than %.2f. Removing column from datacard. The threshold is set by the ToleranceForMinimumRate flag."%(c.getLabel(),c._rateResult.getResult(),self._config.ToleranceForMinimumRate)
                    self._datasetGroups.remove(c)
        # Update process numbers
        for c in self._datasetGroups:
            offset = 0
            for i in myIdsForRemoval:
                if int(c.getLandsProcess()) > int(i):
                    offset += 1
            c._landsProcess -= offset
        self._purgeColumnsWithSmallRateDoneStatus = True

    ## Generates header of datacard
    def _generateHeader(self, mass=None):
        myString = ""
        myLimitCode = None
        if self._opts.lands:
            myLimitCode = "LandS"
        elif self._opts.combine:
            myLimitCode = "Combine"
        if hasattr(self._config, "OptionSignalInjection"):
            myLimitCode = "SIGNALINJECTION(%s, norm=%f) %s"%(self._config.OptionSignalInjection["sample"], self._config.OptionSignalInjection["normalization"], myLimitCode)
        if mass == None:
            myString += "Description: %s datacard (auto generated) luminosity=%f 1/pb, %s/%s\n"%(myLimitCode, self._luminosity,self._config.DataCardName,self._outputPrefix)
        else:
            myString += "Description: %s datacard (auto generated) mass=%d, luminosity=%f 1/pb, %s/%s\n"%(myLimitCode, mass,self._luminosity,self._config.DataCardName,self._outputPrefix)
        myString += "Date: %s\n"%time.ctime()
        return myString

    ## Generates parameter lines
    def _generateParameterLines(self, kmax):
        # Produce result
        myResult =  "imax     1     number of channels\n"
        myResult += "jmax     *     number of backgrounds\n"
        #myResult += "kmax    %2d     number of parameters\n"%kmax
        myResult += "kmax    *     number of parameters\n"
        return myResult

    ## Generates shape header
    def _generateShapeHeader(self,mass):
        myResult = "shapes * * %s%d.root $PROCESS $PROCESS_$SYSTEMATIC\n"%(self._outputRootFileStem,mass)
        return myResult

    ## Generates observation lines
    def _generateObservationLine(self):
        # Obtain observed number of events
        if self._observation == None:
            return "Observation    is not specified\n"
        myObsCount = self._observation._rateResult._histograms[0].Integral()
        if self._opts.debugMining:
            print "  Observation is %d"%myObsCount
        if self._opts.lands:
            myResult = "Observation    %d\n"%myObsCount
        elif self._opts.combine:
            myResult =  "bin            taunuhadr\n"
            if hasattr(self._config, "OptionSignalInjection") or self._opts.testShapeSensitivity:
                myResult += "observation    %f\n"%myObsCount
            else:
                myResult += "observation    %d\n"%myObsCount
        return myResult

    ## Generates header for rate table as list
    def _generateRateHeaderTable(self,mass):
        myResult = []
        # obtain bin numbers
        myRow = ["bin",""]
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass,self._config):
                if self._opts.lands:
                    myRow.append("1")
                elif self._opts.combine:
                    myRow.append("taunuhadr")
        myResult.append(myRow)
        # obtain labels
        myRow = ["process",""]
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass,self._config):
                myRow.append(c.getLabel())
        myResult.append(myRow)
        # obtain process numbers
        myRow = ["process",""]
        myOffset = 0
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass,self._config):
                if c.getLabel() == "res.": # Take into account that the empty column is no longer needed for sigma x Br limits
                    myOffset -= 1
                else:
                    myRow.append(str(c.getLandsProcess()+myOffset))
        myResult.append(myRow)
        return myResult

    ## Generates rate numbers for rate table as list
    def _generateRateDataTable(self,mass):
        myResult = []
        myRow = ["rate",""]
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass,self._config):
                if self._opts.verbose:
                    print "- obtaining cached rate for column %s"%c.getLabel()
                myRateValue = c.getRateResult()
                if myRateValue == None:
                    myRateValue = 0.0
                if self._opts.debugMining:
                    print "  Rate for '%s' = %.3f"%(c.getLabel(),myRateValue)
                # Need better precision for sigma x br limits
                if (self._config.OptionLimitOnSigmaBr or mass > 179) and c.getLandsProcess() <= 0:
                    myRow.append("%.6f"%myRateValue)
                else:
                    myRow.append("%.3f"%myRateValue)
        myResult.append(myRow)
        return myResult

    ## Generates nuisance table as list
    def _generateNuisanceTable(self,mass):
        myResult = []
        myVetoList = [] # List of nuisance id's to veto
        mySingleList = [] # List of nuisance id's that apply only to single column
        # Suppress nuisance rows that are not affecting anything
        for n in self._extractors:
            myCount = 0
            for c in self._datasetGroups:
                if c.isActiveForMass(mass,self._config) and n.isPrintable() and c.hasNuisanceByMasterId(n.getId()):
                    myCount += 1
            if myCount == 0 and n.isPrintable():
                print ShellStyles.WarningLabel()+"Suppressed nuisance %s: '%s' because it does not affect any data column!"%(n.getId(),n.getDescription())
                myVetoList.append(n.getId())
            if myCount == 1:
                mySingleList.append(n.getId())
        # Merge nuisances (quadratic sum) together, if they apply to only one column (is mathematically equal treatrment, but makes datacard running faster)
        # Note that it is not possible to merge physically the nuisances, because it would affect all other parts as well
        # Only solution is to do a virtual merge affecting only this method
        myVirtualMergeInformation = {}
        myVirtuallyInactivatedIds = []
        if self._config.OptionCombineSingleColumnUncertainties:
            for c in self._datasetGroups:
                if c.isActiveForMass(mass,self._config):
                    myFoundSingles = []
                    for n in self._extractors:
                        if c.hasNuisanceByMasterId(n.getId()) and n.getId() in mySingleList and not n.isShapeNuisance():
                            myFoundSingles.append(n.getId())
                    if len(myFoundSingles) > 1:
                        # Do virtual merge
                        myDescription = ""
                        myID = ""
                        myValue = ScalarUncertaintyItem("sum",0.0)
                        for n in self._extractors:
                            if n.getId() in myFoundSingles:
                                if myDescription == "":
                                    myDescription = n.getDescription()
                                    myID = n.getId()
                                    myValue.add(c.getNuisanceResultByMasterId(n.getId())) # Is added quadratically via ScalarUncertaintyItem
                                else:
                                    myDescription += " + "+n.getDescription()
                                    myID += "_AND_"+n.getId()
                                    myValue.add(c.getNuisanceResultByMasterId(n.getId())) # Is added quadratically via ScalarUncertaintyItem
                                    myVetoList.append(n.getId())
                        myVirtualMergeInformation[myFoundSingles[0]] = myValue
                        myVirtualMergeInformation[myFoundSingles[0]+"ID"] = myID
                        myVirtualMergeInformation["%sdescription"%myFoundSingles[0]] = myDescription
                        print ShellStyles.WarningLabel()+"Combined nuisances '%s' for column %s!"%(myDescription, c.getLabel())
        # Loop over rows
        for n in self._extractors:
            if n.isPrintable() and n.getId() not in myVetoList:
                # Suppress rows that are not affecting anything
                if n.getId() in myVirtualMergeInformation.keys():
                    myRow = [myVirtualMergeInformation[n.getId()+"ID"]]
                else:
                    myRow = ["%s"%(n.getId())]
                if self._opts.lands:
                    myRow.append(n.getDistribution())
                elif self._opts.combine:
                    # Check if there are shapes and scalars on the same row
                    shapeAndScalarStatus = False
                    for subN in self._extractors:
                        if n != subN:
                            if subN.getMasterId() == n.getId():
                                nIsShape = n.getDistribution().startswith("shape")
                                subnIsShape = subN.getDistribution().startswith("shape")
                                if (nIsShape and not subnIsShape) or (not nIsShape and subnIsShape):
                                    shapeAndScalarStatus = True
                    if shapeAndScalarStatus:
                        myRow.append("shape?")
                    else:
                        myRow.append(n.getDistribution().replace("shapeQ","shape").replace("shapeStat","shape"))
                # Loop over columns
                for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
                    if c.isActiveForMass(mass,self._config):
                        # Check that column has current nuisance or has nuisance that is slave to current nuisance
                        if c.hasNuisanceByMasterId(n.getId()):
                            if self._opts.verbose:
                                print "- obtaining cached nuisance %s for column %s"%(n.getId(),c.getLabel())
                            myValue = c.getNuisanceResultByMasterId(n.getId())
                            if n.getId() in myVirtualMergeInformation.keys():
                                myValue = myVirtualMergeInformation[n.getId()] # Overwrite virtually merged value
                            myValueString = ""
                            # Check if the slave is a shape nuisance
                            isShapeStatus = False
                            for columnNuisanceId in c._nuisanceIds:
                                for tmpNuisance in self._extractors:
                                   if tmpNuisance.getId() == columnNuisanceId:
                                       if n.getId() == tmpNuisance.getId() or n.getId() == tmpNuisance.getMasterId():
                                           isShapeStatus = tmpNuisance.isShapeNuisance()

                            # Check output format
                            if isShapeStatus:
                                myValueString = "1"
                            else:
                                if isinstance(myValue, ScalarUncertaintyItem):
                                    # Check if nuisance is asymmetric
                                    if myValue.isAsymmetric():
                                        myValueString += "%.3f/%.3f"%(1.0-myValue.getUncertaintyDown(),1.0+myValue.getUncertaintyUp())
                                    else:
                                        myValueString += "%.3f"%(myValue.getUncertaintyUp()+1.0)
                                elif isinstance(myValue, list):
                                    myValueString += "%.3f/%.3f"%(1.0+myValue[0],1.0+myValue[1])
                                else:
                                    # Assume that result is a plain number
                                    #print "nid=",n.getId(),"c=",c.getLabel()
                                    myValueString += "%.3f"%(myValue+1.0)
                            if self._opts.debugMining:
                                print "  Nuisance for '%s/%s' in column '%s': %s"%(n.getId(),n.getDescription(),c.getLabel(),myValueString)
                            myRow.append(myValueString)
                        else:
                            if n.isShapeNuisance():
                                if self._opts.lands:
                                    myRow.append("0")
                                elif self._opts.combine:
                                    myRow.append("-")
                            else:
                                myRow.append("-")
                if self._opts.lands:
                    # Add description to end of the row for LandS
                    if n.getId() in myVirtualMergeInformation.keys():
                        myRow.append(myVirtualMergeInformation["%sdescription"%n.getId()])
                    else:
                        myRow.append(n.getDescription())
                myResult.append(myRow)
        return myResult

    ## Generates nuisance table as list
    def _generateBinByBinStatUncertTable(self,mass):
        myTable = []
        # Loop over columns
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass,self._config):
                hRate = c._rateResult.getHistograms()[0]
                myNames = createBinByBinStatUncertNames(hRate)
                for name in myNames:
                    myRow = []
                    myRow.append(name)
                    myRow.append("shape")
                    for cc in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
                        if cc.isActiveForMass(mass,self._config):
                            if cc.getLabel() == c.getLabel():
                                myRow.append("1")
                            else:
                                myRow.append("-")
                    myTable.append(myRow)
        return myTable

    ## Generates nuisance table as list
    # Recipe is to integrate first (linear sum for variations), then to evaluate
    def _generateShapeNuisanceVariationTable(self,mass):
        myResult = []
        # Loop over rows
        for n in self._extractors:
            if n.isPrintable() and (n.getDistribution() == "shapeQ"):
                myDownRow = ["%s_ShapeDown"%(n.getId()), ""]
                myScalarDownRow = ["%s_DownDevFromScalar"%(n.getId()), ""]
                myUpRow = ["%s_ShapeUp"%(n.getId()), ""]
                myScalarUpRow = ["%s_UpDevFromScalar"%(n.getId()), ""]
                # Loop over columns
                for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
                    if c.isActiveForMass(mass,self._config):
                        # Check that column has current nuisance or has nuisance that is slave to current nuisance
                        if c.hasNuisanceByMasterId(n.getId()):
                            #print "column=%s extractor id=%s"%(c.getLabel(),n.getId())
                            # Obtain histograms
                            myHistograms = c.getFullNuisanceResultByMasterId(n.getId()).getHistograms()
                            if len(myHistograms) > 0:
                                hUp = myHistograms[0]
                                hDown = myHistograms[1]
                                hNominal = c.getRateHistogram()
                                # Calculate
                                myDownDeltaSquared = 0.0
                                myUpDeltaSquared = 0.0
                                myDownAverage = 0.0
                                myUpAverage = 0.0
                                if hNominal.Integral() > 0.0:
                                    myDownAverage = abs(hDown.Integral()-hNominal.Integral())/hNominal.Integral()
                                    myUpAverage = abs(hUp.Integral()-hNominal.Integral())/hNominal.Integral()
                                for i in range(1,hNominal.GetNbinsX()):
                                    myDownDeltaSquared += (abs(hDown.GetBinContent(i) - hNominal.GetBinContent(i)) - myDownAverage)**2
                                    myUpDeltaSquared += (abs(hUp.GetBinContent(i) - hNominal.GetBinContent(i)) - myUpAverage)**2
                                if hNominal.Integral() > 0.0:
                                    myDownDeltaSquared = sqrt(myDownDeltaSquared)/hNominal.Integral()
                                    myUpDeltaSquared = sqrt(myUpDeltaSquared)/hNominal.Integral()
                                else:
                                    myDownDeltaSquared = 0.0
                                    myUpDeltaSquared = 0.0
                                    myScalarDownRow.append("%.3f"%(myDownDeltaSquared))
                                    myScalarUpRow.append("%.3f"%(myUpDeltaSquared))
                                myDownRow.append("%.3f"%(myDownAverage))
                                myUpRow.append("%.3f"%(myUpAverage))
                            else:
                                myDownRow.append("ignored")
                                myUpRow.append("ignored")
                                myScalarDownRow.append("ignored")
                                myScalarUpRow.append("ignored")
                        else:
                            myDownRow.append("-")
                            myUpRow.append("-")
                            myScalarDownRow.append("-")
                            myScalarUpRow.append("-")
                # Add description to end of the row
                myDownRow.append(n.getDescription())
                myUpRow.append(n.getDescription())
                myScalarDownRow.append(n.getDescription())
                myScalarUpRow.append(n.getDescription())
                myResult.append(myDownRow)
                #myResult.append(myScalarDownRow)
                myResult.append(myUpRow)
                #myResult.append(myScalarUpRow)
            if n.isPrintable() and (n.getDistribution() == "shapeStat"):
                myDownRow = ["%s_ShapeStat"%(n.getId()), ""]
                # Loop over columns
                for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
                    if c.isActiveForMass(mass,self._config):
                        # Check that column has current nuisance or has nuisance that is slave to current nuisance
                        if c.hasNuisanceByMasterId(n.getId()):
                            mySum = 0.0
                            hNominal = c.getRateHistogram()
                            for i in range(1,hNominal.GetNbinsX()+1):
                                mySum += hNominal.GetBinError(i)**2
                            myIntegral = hNominal.Integral()
                            if myIntegral > 0.0:
                                myDownRow.append("%.3f"%(sqrt(mySum)/myIntegral))
                            else:
                                myDownRow.append("0.0")
                        else:
                            myDownRow.append("-")
                myResult.append(myDownRow)
        return myResult

    ## Save histograms to root file
    def _saveHistograms(self,rootFile,mass):
        # Observation
        if self._observation != None:
            self._observation.setResultHistogramsToRootFile(rootFile)
        # Loop over columns
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass,self._config):
                c.setResultHistogramsToRootFile(rootFile)
                # Add bin-by-bin stat.uncert.
                hRate = c._rateResult.getHistograms()[0]
                myHistos = createBinByBinStatUncertHistograms(hRate, self._config.MinimumStatUncertainty)
                for h in myHistos:
                    h.SetDirectory(rootFile)
                c._rateResult._tempHistos.extend(myHistos)

    ## Generates table of shape variation for shapeQ nuisances
    def makeShapeVariationTable(self):
        myOutput = ""
        for m in self._config.MassPoints:
            # Invoke extractors
            myRateHeaderTable = self._generateRateHeaderTable(m)
            myNuisanceTable = self._generateShapeNuisanceVariationTable(m)
            # Calculate dimensions of tables
            myWidths = []
            myWidths = calculateCellWidths(myWidths, myRateHeaderTable)
            myWidths = calculateCellWidths(myWidths, myNuisanceTable)
            mySeparatorLine = getSeparatorLine(myWidths)
            # Construct output
            myOutput += "*** Shape nuisance variation summary ***\n"
            myOutput += self._generateHeader(m)
            myOutput += mySeparatorLine
            myOutput += getTableOutput(myWidths,myRateHeaderTable)
            myOutput += mySeparatorLine
            myOutput += getTableOutput(myWidths,myNuisanceTable)
            myOutput += "\n"
            myOutput += "Note: Linear sum is used to obtain the values, i.e. cancellations might occur. Bin-by-bin uncertainties could be larger.\n"
        # Save output to file
        myFilename = self._infoDirname+"/shapeVariationResults.txt"
        myFile = open(myFilename, "w")
        myFile.write(myOutput)
        myFile.close()
        print ShellStyles.HighlightStyle()+"Shape variation tables written to: "+ShellStyles.NormalStyle()+myFilename

    ## Prints event yield summary table
    def makeEventYieldSummary(self):
        formatStr = "%6."
        myPrecision = None
        if self._config.OptionNumberOfDecimalsInSummaries == None:
            print ShellStyles.WarningLabel()+"Using default value for number of decimals in summaries. To change, set OptionNumberOfDecimalsInSummaries in your config."+ShellStyles.NormalStyle()
            formatStr += "1"
            myPrecision = 1
        else:
            formatStr += "%d"%self._config.OptionNumberOfDecimalsInSummaries
            myPrecision = self._config.OptionNumberOfDecimalsInSummaries
        formatStr += "f"

        def getFormattedUnc(formatStr,myPrecision,uncUp,uncDown):
            if abs(round(uncDown,myPrecision)-round(uncUp,myPrecision)) < pow(0.1,myPrecision)-pow(0.1,myPrecision+2): # last term needed because of float point fluctuations
                # symmetric
                return "+- %s"%(formatStr%uncDown)
            else:
                # asymmetric
                return "+%s -%s"%(formatStr%uncUp,formatStr%uncDown)

        def getResultString(hwu,formatStr,myPrecision):
            return "%s +- %s (stat.) %s (syst.)\n"%(formatStr%hwu.getRate(),formatStr%hwu.getRateStatUncertainty(),
                getFormattedUnc(formatStr,myPrecision,*hwu.getRateSystUncertainty()))

        def getLatexFormattedUnc(formatStr,myPrecision,uncUp,uncDown):
            if abs(round(uncDown,myPrecision)-round(uncUp,myPrecision)) < pow(0.1,myPrecision)-pow(0.1,myPrecision+2): # last term needed because of float point fluctuations
                # symmetric
                return "\\pm %s"%(formatStr%uncDown)
            else:
                # asymmetric
                return "~^{+%s}){-%s}"%(formatStr%uncUp, formatStr%uncDown)

        def getLatexResultString(hwu,formatStr,myPrecision):
            return "$%s \\pm %s %s $"%(formatStr%hwu.getRate(),formatStr%hwu.getRateStatUncertainty(),
                getLatexFormattedUnc(formatStr,myPrecision,*hwu.getRateSystUncertainty()))

        # Loop over mass points
        for m in self._config.MassPoints:
            # Initialize
            HH = None
            HW = None
            HST = None # Single top signal
            QCD = None
            Embedding = None
            EWKFakes = None
            # Loop over columns to obtain RootHistoWithUncertainties objects
            for c in self._datasetGroups:
                if c.isActiveForMass(m,self._config) and not c.typeIsEmptyColumn():
                    # Find out what type the column is
                    if c.getLabel().startswith("HH") or c.getLabel().startswith("CMS_Hptntj_HH"):
                        HH = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                    elif c.getLabel().startswith("WH") or c.getLabel().startswith("HW") or c.getLabel().startswith("CMS_Hptntj_HW") or c.getLabel().startswith("CMS_Hptntj_WH"):
                        HW = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                    elif c.getLabel().startswith("Hp") or c.getLabel().startswith("CMS_Hptntj_Hp"):
                        HW = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                    elif c.getLabel().startswith("HST") or c.getLabel().startswith("CMS_Hptntj_HST"):
                        HST = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                    elif c.typeIsQCD():
                        if QCD == None:
                            QCD = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                        else:
                            QCD.Add(c.getCachedShapeRootHistogramWithUncertainties())
                    elif c.typeIsEWK() or (c.typeIsEWKfake() and self._config.OptionGenuineTauBackgroundSource == "MC_FakeAndGenuineTauNotSeparated"):
                        if Embedding == None:
                            Embedding = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                        else:
                            Embedding.Add(c.getCachedShapeRootHistogramWithUncertainties())
                    elif c.typeIsEWKfake():
                        if EWKFakes == None:
                            EWKFakes = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                        else:
                            EWKFakes.Add(c.getCachedShapeRootHistogramWithUncertainties())
                    else:
                        raise Exception(ShellStyles.ErrorLabel()+"Unknown dataset type for dataset %s!%s"%(c.getLabel(),ShellStyles.NormalStyle()))
            # Calculate signal yield
            myBr = self._config.OptionBr
            if not (self._config.OptionLimitOnSigmaBr or m > 179):
                if self._config.OptionBr == None:
                    print ShellStyles.WarningLabel()+"Br(t->bH+) has not been specified in config file, using default 0.01! To specify, add OptionBr=0.05 to the config file."+ShellStyles.NormalStyle()
                    myBr = 0.01
                HW.Scale(2.0 * myBr * (1.0 - myBr))
            if HH != None:
                HH.Scale(myBr**2)
                HW.Add(HH)
            if HST != None:
                HST.Scale(myBr)
                HW.Add(HST)
            # From this line on, HW includes all signal
            # Calculate expected yield
            TotalExpected = QCD.Clone()
            TotalExpected.Add(Embedding)
            if not self._config.OptionGenuineTauBackgroundSource == "MC_FakeAndGenuineTauNotSeparated":
                if EWKFakes != None:
                    TotalExpected.Add(EWKFakes)

            # Construct table
            myOutput = "*** Event yield summary ***\n"
            myOutput += self._generateHeader(m)
            myOutput += "\n"
            myOutput += "Number of events\n"
            if not (self._config.OptionLimitOnSigmaBr or m > 179):
                myOutput += "Signal, mH+=%3d GeV, Br(t->bH+)=%.2f: %s"%(m,myBr,getResultString(HW,formatStr,myPrecision))
            else:
                myOutput += "Signal, mH+=%3d GeV, sigma x Br=1 pb: %s"%(m,getResultString(HW,formatStr,myPrecision))
            myOutput += "Backgrounds:\n"
            myOutput += "                           Multijets: %s"%getResultString(QCD,formatStr,myPrecision)
            if self._config.OptionGenuineTauBackgroundSource == "MC_FakeAndGenuineTauNotSeparated":
                myOutput += "                           MC EWK+tt: %s"%getResultString(Embedding,formatStr,myPrecision)
            else:
                myOutput += "                    EWK+tt with taus: %s"%getResultString(Embedding,formatStr,myPrecision)
                if EWKFakes != None:
                    myOutput += "               EWK+tt with fake taus: %s"%getResultString(EWKFakes,formatStr,myPrecision)
            myOutput += "                      Total expected: %s"%getResultString(TotalExpected,formatStr,myPrecision)
            #if self._config.BlindAnalysis:
            #    myOutput += "                            Observed: BLINDED\n\n"
            #else:
	    myOutput += "                            Observed: %5d\n\n"%self._observation.getCachedShapeRootHistogramWithUncertainties().getRate()
            # Print to screen
            if self._config.OptionDisplayEventYieldSummary:
                print myOutput
            # Save output to file
            myFilename = self._infoDirname+"/EventYieldSummary_m%d.txt"%m
            myFile = open(myFilename, "w")
            myFile.write(myOutput)
            myFile.close()
            print ShellStyles.HighlightStyle()+"Event yield summary for mass %d written to: "%m +ShellStyles.NormalStyle()+myFilename

            myOutputLatex = "% table auto generated by datacard generator on "+self._timestamp+" for "+self._config.DataCardName+" / "+self._outputPrefix+"\n"
            myOutputLatex += "\\renewcommand{\\arraystretch}{1.2}\n"
            myOutputLatex += "\\begin{table}\n"
            myOutputLatex += "  \\centering\n"
            if not (self._config.OptionLimitOnSigmaBr or m > 179):
                myOutputLatex += "  \\caption{Summary of the number of events from the signal with mass point $\\mHpm=%d\\GeVcc$ with $\\BRtH=%.2f$,\n"%(m,myBr)
            else:
                myOutputLatex += "  \\caption{Summary of the number of events from the signal with mass point $\\mHpm=%d\\GeVcc$,\n"%(m)
            myOutputLatex += "           from the background measurements, and the observed event yield. Luminosity uncertainty is not included in the numbers.}\n"
            myOutputLatex += "  \\label{tab:summary:yields}\n"
            myOutputLatex += "  \\vskip 0.1 in\n"
            myOutputLatex += "  \\hspace*{-.8cm}\n"
            myOutputLatex += "  \\begin{tabular}{ l c }\n"
            myOutputLatex += "  \\hline\n"
            myOutputLatex += "  \\multicolumn{1}{ c }{Source}  & $N_{\\text{events}} \\pm \\text{stat.} \\pm \\text{syst.}$  \\\\ \n"
            myOutputLatex += "  \\hline\n"
            myOutputLatex += "  HH+HW, $\\mHplus = %3d\\GeVcc             & %s \\\\ \n"%(m,getLatexResultString(HW,formatStr,myPrecision))
            myOutputLatex += "  \\hline\n"
            myOutputLatex += "  Multijet background (data-driven)       & %s \\\\ \n"%getLatexResultString(QCD,formatStr,myPrecision)
            if self._config.OptionGenuineTauBackgroundSource == "MC_FakeAndGenuineTauNotSeparated":
                myOutputLatex += "  MC EWK+\\ttbar                           & %s \\\\ \n"%getLatexResultString(Embedding,formatStr,myPrecision)
            else:
                myOutputLatex += "  EWK+\\ttbar with $\\tau$ (data-driven)    & %s \\\\ \n"%getLatexResultString(Embedding,formatStr,myPrecision)
                if EWKFakes != None:
                    myOutputLatex += "  EWK+\\ttbar with e/\\mu/jet\\to$\\tau$ (MC) & %s \\\\ \n"%getLatexResultString(EWKFakes,formatStr,myPrecision)
            myOutputLatex += "  \\hline\n"
            myOutputLatex += "  Total expected from the SM              & %s \\\\ \n"%getLatexResultString(TotalExpected,formatStr,myPrecision)
            #if self._config.BlindAnalysis:
            #    myOutputLatex += "  Observed: & BLINDED \\\\ \n"
            #else:
	    myOutputLatex += "  Observed: & %5d \\\\ \n"%self._observation.getCachedShapeRootHistogramWithUncertainties().getRate()
            myOutputLatex += "  \\hline\n"
            myOutputLatex += "  \\end{tabular}\n"
            myOutputLatex += "\\end{table}\n"
            myOutputLatex += "\\renewcommand{\\arraystretch}{1}\n"
            # Save output to file
            myFilename = self._infoDirname+"/EventYieldSummary_m%d_"%(m) +self._timestamp+"_"+self._outputPrefix+"_"+self._config.DataCardName.replace(" ","_")+".tex"
            myFile = open(myFilename, "w")
            myFile.write(myOutputLatex)
            myFile.close()
            print ShellStyles.HighlightStyle()+"Latex table of event yield summary for mass %d written to: "%m +ShellStyles.NormalStyle()+myFilename

    ## Returns a string with proper numerical formatting
    def _getFormattedSystematicsNumber(self,value):
        if abs(value) >= 0.1:
            return "%.0f"%(abs(value)*100)
        elif abs(value) >= 0.001:
            return "%.1f"%(abs(value)*100)
        else:
            return "\\textless~0.1"

    ## Prints systematics summary table
    def makeSystematicsSummary(self,light=False):
#        myColumnOrder = ["HH",
#                         "HW",
#                         "QCD",
#                         "EWK_Tau",
#                         "EWK_DY",
#                         "EWK_VV",
#                         "EWK_tt_faketau",
#                         "EWK_W_faketau",
#                         "EWK_t_faketau"]
        signalColumn="CMS_Hptntj_Hp"
        if light:
            signalColumn="HW"
        myColumnOrder = ["CMS_Hptntj_Hp",
                         "QCDandFakeTau",
                         "ttbar_t_genuine",
                         "W_t_genuine",
                         "singleTop_t_genuine",
                         "DY_t_genuine",
                         "VV_t_genuine"]

# Old list:
#        myNuisanceOrder = [["01","$\\tau - p_T^{miss}$ trigger"], # trg
#                           ["03", "$\\tau$ jet ID (excl. $R_\\tau$"], # tau ID
#                           ["04", "jet, $\\mathcal{l}\\to\\tau$ mis-ID"], # tau mis-ID
#                           ["45", "TES"], # energy scale
#                           ["46", "JES"], # energy scale
#                           ["47", "Unclustered MET ES"], # energy scale
#                           ["09", "lepton veto"], # lepton veto
#                           ["10", "b-jet tagging"], # b tagging
#                           ["11", "jet$\\to$b mis-ID"], # b mis-tagging
#                           ["12", "multi-jet stat."], # QCD stat.
#                           ["13", "multi-jet syst."], # QCD syst.
#                           ["19", "EWK+$t\\bar{t}$ $\\tau$ stat."], # embedding stat.
#                           ["14", "multi-jet contam."], # QCD contamination in embedding
#                           ["15", "$f_{W\\to\\tau\\to\\mu}"], # tau decays to muons in embedding
#                           ["16", "muon selections"], # muon selections in embedding
#                           ["34", "pile-up"], # pile-up
#                           [["17","18","19","22","24","25","26","27"], "simulation stat."], # MC statistics
#                           [["28","29","30","31","32"], "cross section"], # cross section
#                           ["33", "luminosity"]] # luminosity
        myNuisanceOrder = [["CMS_eff_t","tau ID"], # first ID, then the text that goes to the table
                           ["CMS_eff_t_highpt","high-$p_{T}$ tau ID"],        
                           ["CMS_eff_t_trg_data","trigger tau leg eff. for data"],
                           ["CMS_eff_t_trg_MC","trigger tau leg eff. for MC"],
                           ["CMS_eff_met_trg_data","trigger MET leg eff. for data"],
                           ["CMS_eff_met_trg_MC","trigger MET leg eff. for MC"],
                           ["CMS_eff_e_veto","electron veto eff."],
                           ["CMS_eff_m_veto","muon veto eff."],
#                           ["CMS_fake_eToTau","CMS fake eToTau"],
#                           ["CMS_fake_muToTau","CMS fake muToTau"],
#                           ["CMS_fake_jetToTau","CMS fake jetToTau"],
                           ["CMS_eff_b","b-tagging eff."],
                           ["CMS_fake_b","b-mistagging eff."],
                           ["CMS_scale_t","tau energy scale"],
                           ["CMS_scale_j","jet energy scale"],
                           ["CMS_scale_met","MET unclustered energy scale"],
                           ["CMS_res_j","jet energy resolution"],
                           ["CMS_Hptntj_topPtReweight","top $p_T$ reweighting"],
                           ["CMS_pileup","pileup reweighting"],
                           ["CMS_scale_ttbar", "ttbar scale"],
                           ["CMS_pdf_ttbar", "ttbar pdf"],
                           ["CMS_mass_ttbar", "ttbar mass"],
                           ["CMS_scale_Wjets", "W+jets scale"],
                           ["CMS_pdf_Wjets", "W+jets pdf"],
                           ["CMS_scale_DY", "DY scale"],
                           ["CMS_pdf_DY", "DY pdf"],
                           ["CMS_scale_VV", "diboson scale"],
                           ["CMS_pdf_VV", "diboson pdf"],
                           ["lumi_13TeV","luminosity (13 TeV)"],
                           ["CMS_Hptntj_QCDbkg_templateFit","QCD template fit"],
                           ["CMS_Hptntj_QCDkbg_metshape","QCD MET shape"]
                       ]
        # Make table
        myTable = []
        for n in myNuisanceOrder: # for each nuisance
            resultFound=False
            myRow = [n[1]]
            isShape=False
            for columnName in myColumnOrder:
                myMinErrorUp = 9999.0
                myMinErrorDown = 9999.0
                myMaxErrorUp = -9999.0
                myMaxErrorDown = -9999.0
                myErrorUp = 0.0
                myErrorDown = 0.0
                for c in self._datasetGroups: 
                    if columnName in c.getLabel(): # if column name matches to dataset group label
                        if isinstance(n[0], list): # if this column+nuisance combination matches to a list, loop over the list
                            for nid in n[0]:
                                if c.hasNuisanceByMasterId(nid):
                                    # find error up and error down
                                    myResult = c.getFullNuisanceResultByMasterId(nid)
                                    if isinstance(myResult.getResult(), ScalarUncertaintyItem):
                                        myErrorDown = myResult.getResult().getUncertaintyDown()
                                        myErrorUp = myResult.getResult().getUncertaintyUp()
                                    elif isinstance(myResult.getResult(), list):
                                        myErrorDown = max(myResult.getResult())
                                        myErrorUp = myErrorDown
                                    else: #if shape systematic
                                        myErrorDown = self._getAverageShapeUncertainty(nid,c)
                                        myErrorUp = myErrorDown
                                        myRow += " (S)"
                                        isShape=True
                                    # update min and max values for error up
                                    if (myErrorUp < myMinErrorUp):
                                        myMinErrorUp = myErrorUp
                                    if (myErrorUp > myMaxErrorUp):
                                        myMaxErrorUp = myErrorUp
                                    # update min and max values for error down
                                    if (myErrorDown < myMinErrorDown):
                                        myMinErrorDown = myErrorDown
                                    if (myErrorDown > myMaxErrorDown):
                                        myMaxErrorDown = myErrorDown     
                        else: # if this column+nuisance does not match to a list, but just one entry
                            if c.hasNuisanceByMasterId(n[0]): 
                                myResult = c.getFullNuisanceResultByMasterId(n[0])
                                if isinstance(myResult.getResult(), ScalarUncertaintyItem):
                                    myErrorDown = myResult.getResult().getUncertaintyDown()
                                    myErrorUp = myResult.getResult().getUncertaintyUp()
                                elif isinstance(myResult, list):
                                    myErrorDown = max(myResult.getResult())
                                    myErrorUp = myErrorDown
                                else: # if shape systematic
                                    myErrorDown = self._getAverageShapeUncertainty(n[0],c)
                                    myErrorUp = myErrorDown
                                    isShape=True
                                # update min and max values for error up
                                if (myErrorUp < myMinErrorUp):
                                    myMinErrorUp = myErrorUp
                                if (myErrorUp > myMaxErrorUp):
                                    myMaxErrorUp = myErrorUp
                                # update min and max values for error down
                                if (myErrorDown < myMinErrorDown):
                                    myMinErrorDown = myErrorDown
                                if (myErrorDown > myMaxErrorDown):
                                    myMaxErrorDown = myErrorDown
#                        print "  n[0]="+str(n[0])+", columnName="+columnName+"was in c.getLabel()="+c.getLabel()+", so min/max might be updated:"              
#                        print "    -myMinErrorUp = ",myMinErrorUp
#                        print "    -myMinErrorDown = ",myMinErrorDown
#                        print "    -myMaxErrorUp = ",myMaxErrorUp
#                        print "    -myMaxErrorDown = ",myMaxErrorDown

#                print "The final min/max for columnName="+columnName+" are:"
#                print "-myMinErrorUp = ",myMinErrorUp
#                print "-myMinErrorDown = ",myMinErrorDown
#                print "-myMaxErrorUp = ",myMaxErrorUp
#                print "-myMaxErrorDown = ",myMaxErrorDown

                myStr = ""

                # if result not found
                if (abs(myMaxErrorUp) > 9000 or abs(myMinErrorUp) > 9000 or abs(myMaxErrorDown) > 9000 or abs(myMinErrorDown) > 9000):
                    myStr = "$-$"
                # if result found and no need for writing range
                elif ( (myMaxErrorUp-myMinErrorUp)<0.001 and (myMaxErrorDown-myMinErrorDown)<0.001 ): #PROBLEM HERE!
                    if abs(myMaxErrorDown-myMaxErrorUp) < 0.001: # if symmetric error
                        myStr = self._getFormattedSystematicsNumber(myMaxErrorUp)
                    else: # if asymmetric
                        myStr = "$_{-%s}^{+%s}$"%(self._getFormattedSystematicsNumber(myMaxErrorDown),
                                                    self._getFormattedSystematicsNumber(myMaxErrorUp))
                else: #if result found and range is needed                   
                    if abs(myMaxErrorDown-myMaxErrorUp) < 0.001: # if symmetric error
                        myStr = "%s..%s"%(self._getFormattedSystematicsNumber(myMinErrorUp),
                                              self._getFormattedSystematicsNumber(myMaxErrorUp))
                    else: # if asymmetric
                            myStr = "$_{-%s..%s}^{+%s..%s}$"%(self._getFormattedSystematicsNumber(myMinErrorDown),
                                                            self._getFormattedSystematicsNumber(myMaxErrorDown),
                                                            self._getFormattedSystematicsNumber(myMinErrorUp),
                                                            self._getFormattedSystematicsNumber(myMaxErrorUp))


                myRow.append(myStr)
            if isShape:
                myRow[0]+=" (S)"
            myTable.append(myRow)

        # Make table
        myOutput = "% table auto generated by datacard generator on "+self._timestamp+" for "+self._config.DataCardName+" / "+self._outputPrefix+"\n\n"
        myOutput += "\\documentclass{article}\n"
        myOutput += "\\begin{document}\n\n"
        myOutput += "\\renewcommand{\\arraystretch}{1.2}\n"
        myOutput += "\\begin{table}%%[h]\n"
        myOutput += "\\begin{center}\n"
        myOutput += "\\caption{The systematic uncertainties (in \\%) for signal and the backgrounds. The uncertainties, which depend on the final distribution bin, are marked with (S) and for them the maximum contracted value of the negative or positive variation is displayed.}"
        myOutput += "\\label{tab:summary:systematics}\n"
        myOutput += "\\vskip 0.1 in\n"
        myOutput += "\\noindent\\makebox[\\textwidth]{\n"
        myOutput += "\\begin{tabular}{l|c|c|ccccc}\n"
        myOutput += "\\hline\n"
        myOutput += "& Signal & Fake tau & \multicolumn{5}{c}{EWK+t\={t} genuine tau}"
        myOutput += "\n \\\\"
        myCaptionLine = [["","","","t\={t}","W+jets","single top","DY","Diboson"]] 
        # Calculate dimensions of tables
        myWidths = []
        myWidths = calculateCellWidths(myWidths, myTable)
        myWidths = calculateCellWidths(myWidths, myCaptionLine)
        mySeparatorLine = getSeparatorLine(myWidths)
        # Add caption and table
        myOutput += getTableOutput(myWidths,myCaptionLine,True)
        myOutput += "\n \\hline\n"
        myOutput += getTableOutput(myWidths,myTable,True)
        myOutput += "\\hline\n"
        myOutput += "\\end{tabular}\n"
        myOutput += "}\n"
        myOutput += "\\end{center}\n"
        myOutput += "\\end{table}\n"
        myOutput += "\\renewcommand{\\arraystretch}{1}\n"
        myOutput += "\\end{document}"
        # Save output to file
        mySignalText="heavy"
        if light:
           mySignalText="light"
        myFilename = self._infoDirname+"/SystematicsSummary_"+mySignalText
#        myFilename += "_"+self._timestamp+"_"+self._outputPrefix+"_"+self._config.DataCardName.replace(" ","_")
        myFilename+=".tex"
        myFile = open(myFilename, "w")
        myFile.write(myOutput)
        myFile.close()
        print ShellStyles.HighlightStyle()+"Latex table of systematics summary written to: "+ShellStyles.NormalStyle()+myFilename

    ## Prints QCD purity information
    def makeQCDPuritySummary(self):
        h = aux.Clone(self._observation.getRateHistogram(), "dummy")
        h.Reset()
        hQCD = None
        hQCDPurity = None
        for c in self._datasetGroups:
            if c.typeIsQCD() and not c.typeIsQCDMC():
                hQCD = c.getRateHistogram()
                hQCDPurity = c.getPurityHistogram()
            elif not c.typeIsSignal() and not c.typeIsEmptyColumn():
                h.Add(c.getRateHistogram())
        if hQCD == None:
            return
        s = "QCD purity by bins for shape histogram:\n"
        for i in range(1,hQCD.GetNbinsX()+1):
            # bin
            s += "  bin: %03d..%03d"%(hQCDPurity.GetXaxis().GetBinLowEdge(i), hQCDPurity.GetXaxis().GetBinUpEdge(i))
            # QCD purity
            myGoodPurityStatus = hQCDPurity.GetBinContent(i) > 0.5
            s += "  purity: %.3f +- %.3f"%(hQCDPurity.GetBinContent(i), hQCDPurity.GetBinError(i))
            # QCD fraction out of all expected events
            f = 0.0
            if abs(h.GetBinContent(i)+hQCD.GetBinContent(i)) > 0.0:
                f = (hQCD.GetBinContent(i)) / (h.GetBinContent(i)+hQCD.GetBinContent(i))
            s += "  QCD/Exp.: %.3f"%f
            mySignificantFractionStatus = f > 0.2
            if not myGoodPurityStatus and mySignificantFractionStatus:
                s += "  #W# check if bad purity of QCD has impact on results!"
            else:
                s += "  OK"
            s += "\n"
        print "\n%s"%s.replace("#W#",ShellStyles.WarningLabel())
        myFilename = self._infoDirname+"/QCDpurity.txt"
        myFile = open(myFilename, "w")
        myFile.write(s.replace("#W#","Warning:"))
        myFile.close()
        h.IsA().Destructor(h)

    ## Gets the maximum of the average values of up and down variations for a given shape systematic and dataset
    def _getAverageShapeUncertainty(self,syst_id,c): # arguments: ID of the nuisance and dataset group
         myDownAverage = 0.0
         myUpAverage = 0.0
         for n in self._extractors: # loop over systematics
            if (n.getDistribution() == "shapeQ") and (n.getId() == syst_id) and c.hasNuisanceByMasterId(syst_id): # if shape systematic
                myHistograms = c.getFullNuisanceResultByMasterId(syst_id).getHistograms()
                if len(myHistograms) > 0:
                    hDown = myHistograms[1]
                    hUp = myHistograms[0]
                    hNominal = c.getRateHistogram()
                    # Calculate
                    if hNominal.Integral() > 0.0:
                        myDownAverage = abs(hDown.Integral()-hNominal.Integral())/hNominal.Integral()
                        myUpAverage = abs(hUp.Integral()-hNominal.Integral())/hNominal.Integral()
         return max(myDownAverage,myUpAverage)
    
    ## Creates datacards with 0 +-1 -> 1 +- 0 shift for each shape nuisance
    def _createDatacardsForShapeSensitivityTest(self):
        myIdList = []
        myBlackList = ["umerator","enominator"]
        # Obtain list of shape nuisances
        for e in self._extractors:
            #print e.getId()
            if e.isShapeNuisance() and e.getId() == e.getMasterId():
                #print "***"
                myIdList.append(e.getId())
        # Loop over shape nuisances
        myOriginalDirName = self._dirname
        hOriginalObservationFinalHistogram = self._observation._rateResult.getFinalBinningHistograms()[0]
        hOriginalObservationFineBinningHistogram = self._observation._rateResult.getFineBinnedHistograms()[0]
        myOriginalExtractors = self._extractors[:]
        # Calculate sum of backgrounds
        hTmpFinal = aux.Clone(hOriginalObservationFinalHistogram)
        hTmpFinal.Reset()
        hTmpFine = aux.Clone(hOriginalObservationFineBinningHistogram)
        hTmpFine.Reset()
        hBkgSum = [hTmpFinal, hTmpFine]
        #for h in hBkgSum:
        #     print "DEBUG bkgsum: %s"%h.GetTitle()
        for b in self._datasetGroups:
            if b.typeIsEWK() or b.typeIsEWKfake() or b.typeIsQCD():
                for i in range(0,len(hBkgSum)):
                    hBkgSum[i].Add(b._rateResult._histograms[i])
        # Create control
        myOutList = []
        self._extractors = myOriginalExtractors[:]
        self._dirname = "%s_SHAPETEST_CONTROL"%(myOriginalDirName)
        self._observation._rateResult._histograms = [hOriginalObservationFinalHistogram, hOriginalObservationFineBinningHistogram]
        myControlIntegral = hBkgSum[0].Integral()
        self._observation._result = myControlIntegral
        myOutList.append("... shape sensitivity test CONTROL: obs integral = %f"%(myControlIntegral))
        os.mkdir(self._dirname)
        self.makeDataCards()
        # Loop over shape nuisances
        for direction in [0,1]:
            dirStr = "UP"
            if direction == 1:
                dirStr = "DOWN"
            for item in myIdList:
                self._dirname = "%s_SHAPETEST_%s%s"%(myOriginalDirName, item, dirStr)
                self._extractors = []
                hBkgSumCloned = []
                for h in hBkgSum:
                    hh = aux.Clone(h)
                    hBkgSumCloned.append(hh)
                for e in myOriginalExtractors:
                    if e.isShapeNuisance() and e.getMasterId() == item:
                        # Replace observation by bkg rate sum + 1 sigma shift
                        for b in self._datasetGroups:
                            if b.typeIsEWK() or b.typeIsEWKfake() or b.typeIsQCD():
                                #for result in b._nuisanceResults:
                                #    print item,result.getMasterId()
                                if b.hasNuisanceByMasterId(item):
                                    myResult = b.getFullNuisanceResultByMasterId(item)
                                    hBkgSumCloned[0].Add(myResult.getFinalBinningHistograms(blackList=myBlackList)[direction])
                                    hBkgSumCloned[0].Add(b._rateResult.getFinalBinningHistograms(blackList=myBlackList)[0], -1.0)
                                    hBkgSumCloned[1].Add(myResult.getFineBinnedHistograms(blackList=myBlackList)[direction])
                                    hBkgSumCloned[1].Add(b._rateResult.getFineBinnedHistograms(blackList=myBlackList)[0], -1.0)
                                    #for h in myResult.getFineBinnedHistograms(blackList=myBlackList):
                                    #    print "DEBUG nuisance %s column %s dir %s: %s bins %d"%(item, b.getLabel(), dirStr, h.GetName(),h.GetNbinsX())
                    else:
                        self._extractors.append(e)
                myOutList.append("... shape sensitivity test for %s%s: obs integral = %f (diff to ctrl: %f)"%(item, dirStr, hBkgSumCloned[0].Integral(), hBkgSumCloned[0].Integral()/myControlIntegral))
                self._observation._rateResult._histograms = hBkgSumCloned[:]
                self._observation._result = hBkgSumCloned[0].Integral()
                print "shape sensitivity test %s, %s"%(item, dirStr)
                os.mkdir(self._dirname)
                self.makeDataCards()
        # Revert
        myOriginalDirName = self._dirname
        self._observation._rateResult._histograms = [hOriginalObservationFinalHistogram, hOriginalObservationFineBinningHistogram]
        self._observation._result = hOriginalObservationFinalHistogram.Integral()
        self._extractors = myOriginalExtractors[:]
        # Output
        print "\nCreated datacards with 0 +-1 -> 1 +- 0 shift for each shape nuisance"
        for item in myOutList:
            print item
        
