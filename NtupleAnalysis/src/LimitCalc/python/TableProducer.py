'''
\package TableProducer

DESCRIPTION:
Classes for producing output

'''

#================================================================================================ 
# Import modules
#================================================================================================ 
from HiggsAnalysis.LimitCalc.Extractor import ExtractorBase
from HiggsAnalysis.LimitCalc.DatacardColumn import DatacardColumn
from HiggsAnalysis.LimitCalc.ControlPlotMaker import ControlPlotMaker
from HiggsAnalysis.LimitCalc.ControlPlotMakerHToTB import ControlPlotMakerHToTB
from HiggsAnalysis.NtupleAnalysis.tools.systematics import ScalarUncertaintyItem
import HiggsAnalysis.NtupleAnalysis.tools.ShellStyles as ShellStyles
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
import HiggsAnalysis.NtupleAnalysis.tools.git as git

from math import pow,sqrt
import os
import sys
import time
import ROOT

#================================================================================================ 
# Function definition
#================================================================================================ 
VERBOSE = False

def Verbose(msg, printHeader=False):
    if not VERBOSE:
        return
    if printHeader:
        print "=== dcardHplus2tb2017Datacard_v2.py:"

    if msg !="":
        print "\t", msg
    return

def GetFName():
    fName = __file__.split("/")[-1]
    fName = fName.replace(".pyc", ".py")
    return fName

def Print(msg, printHeader=True):
    fName = GetFName()
    if printHeader:
        print "=== ", fName
    if msg !="":
        print "\t", msg
    return

def PrintFlushed(msg, printHeader=True):
    '''
    Useful when printing progress in a loop
    '''
    msg = "\r\t" + msg 
    if printHeader:
        print "=== ", GetFName()
    sys.stdout.write(msg)
    sys.stdout.flush()
    return

def createBinByBinStatUncertHistograms(hRate, xmin=None, xmax=None, binByBinLabel=""):
    '''
    Creates and returns a list of bin-by-bin stat. uncert. histograms
    Inputs:
    hRate  rate histogram
    xmin   float, specifies minimum value for which bin-by-bin histograms are created (default: all)
    xmax   float, specifies maximum value for which bin-by-bin histograms are created (default: all)
    binByBinLabel string, specifies an optional postfix used to name bin-by-bin stat. nuisances (default: "")
    '''
    myList = []
    myName = hRate.GetTitle()
    # Construct range
    myRangeMin = xmin
    myRangeMax = xmax
    if myRangeMin == None:
        myRangeMin = hRate.GetXaxis().GetBinLowEdge(1)
    if myRangeMax == None:
        myRangeMax = hRate.GetXaxis().GetBinUpEdge(hRate.GetNbinsX())

    nNegativeRate = 0
    nBelowMinStatUncert = 0
    nEmptyDownHistograms = 0

#   TEST PRINT
#    print "Contents of histogram %s:"%hRate.GetTitle()
#    for i in range(1, hRate.GetNbinsX()+1):
#        print "bin %d (from %f to %f): %f +- %f"%(i,hRate.GetXaxis().GetBinLowEdge(i),hRate.GetXaxis().GetBinUpEdge(i),hRate.GetBinContent(i),hRate.GetBinError(i))
         

    # For-loop: All histogram bins
    for i in range(1, hRate.GetNbinsX()+1):
        #print hRate.GetXaxis().GetBinLowEdge(i), xmin, hRate.GetXaxis().GetBinUpEdge(i), xmax
        
        if hRate.GetXaxis().GetBinLowEdge(i) > myRangeMin-0.0001 and hRate.GetXaxis().GetBinUpEdge(i) < myRangeMax+0.0001:

            # Make sure that there are no negative rates in nominal histogram (hRate)
            if hRate.GetBinContent(i) < 0.0:
                nNegativeRate += 1

            # Clone hRate histogram to hUp and hDown
            hUp   = aux.Clone(hRate, "%s_%s_statBin%s%dUp"  % (myName, myName,binByBinLabel,i) )
            hDown = aux.Clone(hRate, "%s_%s_statBin%s%dDown"% (myName, myName,binByBinLabel,i) )
            hUp.SetTitle(hUp.GetName())
            hDown.SetTitle(hDown.GetName())

            # The stat. uncerntainties are set and stored as errors to the nominal histogram in DatacardColumn.py

            # Set hUp rate
            hUp.SetBinContent(i, hUp.GetBinContent(i) + hUp.GetBinError(i))
            # Set hDown rate
            statBinDown = hDown.GetBinContent(i)-hDown.GetBinError(i)
            # hDown.SetBinContent(i, statBinDown) # Bug fix (8Nov2017)
            hDown.SetBinContent(i, max(0.0, statBinDown)) # make sure hDown rate is not negative

            # Varying dowards can in rare cases lead to a completely empty hDown histo, not accepted as input by Combine
            # To prevent this from happening, we do as follows:
            if hDown.Integral() <= 0:
                 hDown.SetBinContent(i, max(0.00001, statBinDown))
                 nEmptyDownHistograms += 1
                    
            # Clear uncertainty bins, because they have no effect on LandS/Combine
            for j in range(1, hRate.GetNbinsX()+1):
                hUp.SetBinError(j, 0.0)
                hDown.SetBinError(j, 0.0)

            # Append to list before returning it
            myList.append(hUp)
            myList.append(hDown)

    # Print summarty of warnings/errors (if any)
    if nNegativeRate > 0:
        msg = "Rate value for \"%s\" was negative (hence forced to zero) in %d bins" % (hRate.GetName(), nNegativeRate)
        Verbose(ShellStyles.WarningLabel() + msg)

    if nBelowMinStatUncert > 0:
        msg = "Rate value for \"%s\" was below minimum statistical uncertainty" % (hRate.GetName(), nBelowMinStatUncert)
        Verbose(ShellStyles.WarningLabel() + msg, False)

    if nEmptyDownHistograms > 0:
        msg = "Rate value for \"%s\" was negative but it could not be forced to zero (this would lead to empty hDown histogram), so it was set to 0.00001 in %d bins" % (hRate.GetName(), nEmptyDownHistograms)
        Verbose(ShellStyles.WarningLabel() + msg)

    return myList

def createBinByBinStatUncertNames(hRate,binByBinLabel=""):
    '''
    Creates and returns a list of bin-by-bin stat. uncert. name strings
    Inputs:
    hRate  rate histogram
    '''
    myList = []
    myName = hRate.GetTitle()
    for i in range(1, hRate.GetNbinsX()+1):
        myList.append( myName+"_statBin%s%d"%(binByBinLabel,i) )
    return myList

def calculateCellWidths(widths,table):
    '''
    Calculates maximum width of each table cell
    '''
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


#================================================================================================ 
# Class definition
#================================================================================================ 
class TableProducer:
    def __init__(self, opts, config, outputPrefix, luminosity, observation, datasetGroups, extractors, mcrabInfoOutput, h2tb, verbose=False):
        '''
        Constructor
        '''
        self._opts = opts
        self._config = config
        self._binByBinLabel = ""
        if hasattr(self._config, 'OptionBinByBinLabel'):
            self._binByBinLabel = self._config.OptionBinByBinLabel
        self._outputPrefix = outputPrefix
        self._luminosity = luminosity
        self._observation = observation
        self._datasetGroups = datasetGroups
        self._purgeColumnsWithSmallRateDoneStatus = False
        self._extractors = extractors[:]
        self._h2tb = h2tb
        self._timestamp = time.strftime("%y%m%d_%H%M%S", time.gmtime(time.time()))
        self._outputFileStem = "combine_datacard_hplushadronic_m"
        self._outputRootFileStem = "combine_histograms_hplushadronic_m"
        if hasattr(self._config, 'OptionPaper'):
            self._Paper = self._config.OptionPaper
        else:
            self._Paper = False
        if self._h2tb:
            self.channelLabel = "tbhadr"
        else:
            self.channelLabel = "taunuhadr"
        self._verbose = verbose
        self.makeDirectory()
            
        # Make control plots
        if self._config.OptionDoControlPlots:
            if hasattr(self._config, 'OptionGenuineTauBackgroundSource'):
                ControlPlotMaker(self._opts, self._config, self._ctrlPlotDirname, self._luminosity, self._observation, self._datasetGroups)
            if hasattr(self._config, 'OptionFakeBMeasurementSource'):
                ControlPlotMakerHToTB(self._opts, self._config, self._ctrlPlotDirname, self._luminosity, self._observation, self._datasetGroups)
        else:
            msg = "Skipped making of data-driven control plots. To enable, set OptionDoControlPlots = True in the input datacard."
            if self._opts.verbose:
                Print(ShellStyles.WarningLabel() + msg)

        # Make other reports
        if self._opts.verbose:
            Print(ShellStyles.HighlightStyle() + "Generating reports" + ShellStyles.NormalStyle())

        # Create table of shape variation for shapeQ nuisances
        self.makeShapeVariationTable()

        # Create event yield summary table
        self.makeEventYieldSummary()

        # Create systematics summary table
        self.makeSystematicsSummary(light=True)
        self.makeSystematicsSummary(light=False)        

        # Prints QCD purity information
        #self.makeQCDPuritySummary() #FIXME missing

        # Make datacards
        self.makeDataCards()        

        # Make copy of input datacard
        os.system("cp %s %s/input_datacard.py" % (self._opts.datacard, self._infoDirname) )

        # Write input multicrab directory names
        fileAndContents = {}
        filePath     = os.path.join(self._infoDirname, "inputDirectories.txt")
        fileContents = "\n".join(map(str, mcrabInfoOutput)) + "\n"
        fileAndContents[filePath] = fileContents

        filePath     = os.path.join(self._infoDirname, "codeVersion.txt")
        fileContents = git.getCommitId()+"\n"
        fileAndContents[filePath] = fileContents

        filePath      = os.path.join(self._infoDirname, "codeStatus.txt")
        fileContents = git.getStatus()+"\n"
        fileAndContents[filePath] = fileContents

        filePath     = os.path.join(self._infoDirname, "codeDiff.txt")
        fileContents = git.getDiff()+"\n"
        fileAndContents[filePath] = fileContents
        
        # For-loop: All file path-content pairs
        for index, theFile in enumerate(fileAndContents, 1):
            theContents = fileAndContents[theFile]
            f = open(theFile, "w")
            f.write(theContents)
            f.close()
            # Inform user of code status txt files
            msg = "Created file " 
            Verbose(msg + ShellStyles.SuccessStyle() + theFile + ShellStyles.NormalStyle(), index==1)

        self._extractors = extractors[:]
        
        # Create for each shape nuisance a variation 
        if opts.testShapeSensitivity:
            self._createDatacardsForShapeSensitivityTest()
        return


    def Verbose(self, msg, printHeader=False):
        if not self._verbose:
            return
        if printHeader:
            print "=== %s:" % self.GetFName()
        if msg !="":
            print "\t", msg
        return

    def GetFName(self):
        fName = __file__.split("/")[-1]
        fName = fName.replace(".pyc", ".py")
        return fName
    
    def Print(self, msg, printHeader=True):
        fName = self.GetFName()
        if printHeader:
            print "=== ", fName
        if msg !="":
            print "\t", msg
        return

    def makeDirectory(self):
        '''
        The original code is now obsolete since LandS is not used. 
        All results are with combine => implied

        myLimitCode  = "combine"
        self._dirname = "datacards_%s_%s_%s_%s" % (myLimitCode,self._timestamp,self._config.DataCardName.replace(" ","_"),self._outputPrefix)
        '''

        # Make directory for output
        self._dirname = "datacards_%s_%s_%s" % (self._config.DataCardName.replace(" ","_"), self._outputPrefix, self._timestamp)
        if hasattr(self._config, "OptionSignalInjection"):
            self._dirname += "_SignalInjection"
        self.Verbose("Creating main directory %s" % (self._dirname), True)
        os.mkdir(self._dirname)

        # Create sub directory for informative files
        self._infoDirname = self._dirname + "/info"
        self.Verbose("Creating sub-directory %s" % (self._infoDirname), False)
        os.mkdir(self._infoDirname)

        # Create sub directory for control plots
        self._ctrlPlotDirname = self._dirname + "/controlPlots"
        self.Verbose("Creating sub-directory %s" % (self._ctrlPlotDirname), False)
        os.mkdir(self._ctrlPlotDirname)

        # Copy the datacards for future reference
        dcardName = "inputDatacardForDatacardGenerator.py"
        self.Verbose("Copying datacard %s to main directory %s as %s" % (self._opts.datacard, self._dirname, dcardName), False)
        os.system("cp %s %s/%s" % (self._opts.datacard, self._dirname, dcardName))
        return

    def getDirectory(self):
        '''
        Returns name of results directory
        '''
        return self._dirname

    def makeDataCards(self):
        '''
        Generates datacards
        '''

        # For combine, do some formatting
        if self._opts.combine and not self._purgeColumnsWithSmallRateDoneStatus:
            mySubtractAfterId = None
            mySmallestColumnId = 9
            # Find and remove empty column
            myRemoveList = []
            
            # For-loop: Dataset groups
            for c in self._datasetGroups:
                if c.getLandsProcess() < mySmallestColumnId:
                    mySmallestColumnId = c.getLandsProcess()
                if c.typeIsEmptyColumn():
                    mySubtractAfterId = c.getLandsProcess()
                    myRemoveList.append(c)
            if len(myRemoveList) > 0:
                self._datasetGroups.remove(c)
                print "Removed empty column for combine datacard"

            # For-loop: Dataset groups
            for c in self._datasetGroups:
                if c.getLandsProcess() > mySubtractAfterId:
                    c._landsProcess = c.getLandsProcess() - 1
            # Move column with ID -1 to zero
            #if mySmallestColumnId < 0:
            #    for c in self._datasetGroups:
            #        c._landsProcess = c.getLandsProcess() + 1

        self._purgeColumnsWithSmallRate()

        # For-loop: All mass points
        for index, m in enumerate(self._config.MassPoints, 1):
            
            # Print progress 
            msg = "Datacard %s/%s (mH=%s)" % (index, len(self._config.MassPoints), str(m)) 
            PrintFlushed(ShellStyles.HighlightStyle() + msg + ShellStyles.NormalStyle(), index==1)
            if index == len(self._config.MassPoints):
                print 

            # Open output root file
            myFilename = self._dirname+"/"+self._outputFileStem+"%d.txt"%m
            myRootFilename = self._dirname+"/"+self._outputRootFileStem+"%d.root"%m
            myRootFile = ROOT.TFile.Open(myRootFilename, "RECREATE")

            if myRootFile == None:
                msg = " Cannot open file %s for output!" % (myRootFilename)
                Print(ShellStyles.ErrorLabel() + msg + ShellStyles.NormalStyle())
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

            # Save & close datacard to file
            myFile = open(myFilename, "w")
            myFile.write(myCard)
            myFile.close()
            Verbose("Written datacard to %s" % (ShellStyles.SuccessStyle() + myFilename + ShellStyles.NormalStyle() ))

            # Save & close histograms to root file and create bin-by-bin stat. uncertainties
            self._saveHistograms(myRootFile,m,binByBinLabel=self._binByBinLabel),
            myRootFile.Write()
            myRootFile.Close()
            Verbose("Written shape ROOT file to %s" % (ShellStyles.SuccessStyle() + myRootFilename + ShellStyles.NormalStyle() ))
        return

    def _purgeColumnsWithSmallRate(self):
        '''
        Purge columns with zero rate
        '''
        if self._purgeColumnsWithSmallRateDoneStatus:
            return
        myLastUntouchableLandsProcessNumber = 0 # For sigma x br
        if not self._config.OptionLimitOnSigmaBr and (self._datasetGroups[0].getLabel()[:2] == "HW" or self._datasetGroups[1].getLabel()[:2] == "HW"):
#            if self._opts.lands:
#                myLastUntouchableLandsProcessNumber = 2 # For light H+ physics model
            if self._opts.combine:
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
        #if self._opts.lands:
        #    myLimitCode = "LandS"
        #elif self._opts.combine:
        #    myLimitCode = "Combine"
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

        if 1:
            myResult =  "bin            %s\n" % (self.channelLabel)
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
                #if self._opts.lands:
                #    myRow.append("1")
                #elif self._opts.combine:
                #    myRow.append("taunuhadr")
                myRow.append(self.channelLabel)

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

    def _generateNuisanceTable(self, mass):
        '''
        Generates nuisance table as list
        '''
        myResult     = []
        myVetoList   = [] # List of nuisance id's to veto
        mySingleList = [] # List of nuisance id's that apply only to single column

        # Suppress nuisance rows that are not affecting anything
        for n in self._extractors:
            myCount = 0

            for c in self._datasetGroups:
                if c.isActiveForMass(mass,self._config) and n.isPrintable() and c.hasNuisanceByMasterId(n.getId()):
                    myCount += 1

            if myCount == 0 and n.isPrintable():
                msg = "Suppressed nuisance %s: '%s' because it does not affect any data column!" % (n.getId(),n.getDescription())
                if self._opts.verbose:
                    Print(ShellStyles.WarningLabel() + msg, len(myVetoList) < 1)
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
                if 0: #self._opts.lands:
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
                                if 0:#self._opts.lands:
                                    myRow.append("0")
                                elif self._opts.combine:
                                    myRow.append("-")
                            else:
                                myRow.append("-")
                if 0: #self._opts.lands:
                    # Add description to end of the row for LandS
                    if n.getId() in myVirtualMergeInformation.keys():
                        myRow.append(myVirtualMergeInformation["%sdescription"%n.getId()])
                    else:
                        myRow.append(n.getDescription())
                myResult.append(myRow)
        return myResult

    def _generateBinByBinStatUncertTable(self,mass):
        '''
        Generates nuisance table as list
        '''
        myTable = []
        # Loop over columns
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass,self._config):
                hRate = c._rateResult.getHistograms()[0]
                myNames = createBinByBinStatUncertNames(hRate,binByBinLabel=self._binByBinLabel)
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

    def _generateShapeNuisanceVariationTable(self,mass):
        '''
        Generates nuisance table as list
        Recipe is to integrate first (linear sum for variations), then to evaluate
        '''
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

    def _saveHistograms(self, rootFile, mass, binByBinLabel=""):
        '''
        Save histograms to root file
        '''
        # Observation
        if self._observation != None:
            self._observation.setResultHistogramsToRootFile(rootFile)
        # Loop over columns
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass,self._config):
                c.setResultHistogramsToRootFile(rootFile)
                # Add bin-by-bin stat.uncert.
                hRate = c._rateResult.getHistograms()[0]
                myHistos = createBinByBinStatUncertHistograms(hRate, binByBinLabel=binByBinLabel)
                for h in myHistos:
                    h.SetDirectory(rootFile)
                c._rateResult._tempHistos.extend(myHistos)
        return

    def makeShapeVariationTable(self):
        '''
        Generates table of shape variation for shapeQ nuisances
        '''
        myOutput = ""

        # For-loop: All signal mass points
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

        # Inform the user
        msg = "Shape variation tables written to "
        Verbose(msg + ShellStyles.SuccessStyle() + myFilename + ShellStyles.NormalStyle() ) #ShellStyles.HighlightAltStyle()
        return

    def getFormattedUnc(self, formatStr,myPrecision,uncUp,uncDown):
        if abs(round(uncDown,myPrecision)-round(uncUp,myPrecision)) < pow(0.1,myPrecision)-pow(0.1,myPrecision+2): # last term needed because of float point fluctuations
            # symmetric
            return "+- %s"%(formatStr%uncDown)
        else:
            # asymmetric
            return "+%s -%s"%(formatStr%uncUp,formatStr%uncDown)

    def getResultString(self, hwu,formatStr,myPrecision):
        if not hwu==None:
            return "%s +- %s (stat.) %s (syst.)\n"%(formatStr%hwu.getRate(),formatStr%hwu.getRateStatUncertainty(),
                                                    self.getFormattedUnc(formatStr,myPrecision,*hwu.getRateSystUncertainty()))
        else: return ""

    def getLatexFormattedUnc(self, formatStr,myPrecision,uncUp,uncDown):
        if abs(round(uncDown,myPrecision)-round(uncUp,myPrecision)) < pow(0.1,myPrecision)-pow(0.1,myPrecision+2): # last term needed because of float point fluctuations
            # symmetric
                return "\\pm %s"%(formatStr%uncDown)
        else:
            # asymmetric
            return "~^{+%s}_{-%s}"%(formatStr%uncUp, formatStr%uncDown)

    def getLatexResultString(self, hwu, formatStr, myPrecision):
        '''
        hwu = Histo With Uncertainties
        '''
        if hwu==None:
            return ""
        
        # For sanity checks
        if 0:
            hwu.printUncertainties()
            hwu.Debug()
        
        # Construct the result with the given precision
        rate   = formatStr % hwu.getRate()
        stat   = formatStr % hwu.getRateStatUncertainty()
        syst   = self.getLatexFormattedUnc(formatStr, myPrecision, *hwu.getRateSystUncertainty())
        result = "$%s \\pm %s %s $" % (rate, stat, syst)
        return result

    def makeEventYieldSummary(self):
        '''
        Prints event yield summary table
        '''
        self.formatStr = "%6."
        self.myPrecision = None
        if self._config.OptionNumberOfDecimalsInSummaries == None:
            print ShellStyles.WarningLabel()+"Using default value for number of decimals in summaries. To change, set OptionNumberOfDecimalsInSummaries in your config."+ShellStyles.NormalStyle()
            self.formatStr += "1"
            self.myPrecision = 1
        else:
            self.formatStr += "%d"%self._config.OptionNumberOfDecimalsInSummaries
            self.myPrecision = self._config.OptionNumberOfDecimalsInSummaries
        self.formatStr += "f"
        
        # For-loop: All mass points
        global HW 
        global containsQCDdataset
        for i, m in enumerate(self._config.MassPoints, 1):
            Verbose("Mass point is %d" % (m), i==1)

            # Initialize
            HH        = None
            HW        = None
            HST       = None # Single top signal
            QCD       = None
            Embedding = None
            EWKFakes  = None

            containsQCDdataset = False
            # For-loop: All columns t(o obtain RootHistoWithUncertainties objects)
            for j, c in enumerate(self._datasetGroups, 1):
                Verbose("Column label is %s" % (c.getLabel()), j==1)

                # FIXME: What a mess!
                if c.isActiveForMass(m, self._config) and not c.typeIsEmptyColumn():
                    # Find out what type the column is
                    if c.getLabel().startswith("HH") or c.getLabel().startswith("CMS_Hptntj_HH"):
                        HH = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                    elif c.getLabel().startswith("WH") or c.getLabel().startswith("HW") or c.getLabel().startswith("CMS_Hptntj_HW") or c.getLabel().startswith("CMS_Hptntj_WH"):
                        HW = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                    elif c.getLabel().startswith("Hp") or c.getLabel().startswith("CMS_Hptntj_Hp"):
                        HW = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                    elif c.getLabel().startswith("HST") or c.getLabel().startswith("CMS_Hptntj_HST"):
                        HST = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                    elif c.typeIsQCD() or c.typeIsFakeB():
                        containsQCDdataset = True
                        if QCD == None:
                            try:
                                QCD = c.getCachedShapeRootHistogramWithUncertainties().Clone()
                            except AttributeError:
                                msg = "Did you create the pseudo-Multicrab containing the correctly normalized QCD background? Step 3) in the QCD background measurement instructions."
                                raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())
                        else:
                            QCD.Add(c.getCachedShapeRootHistogramWithUncertainties())
                    elif c.typeIsEWK() or (c.typeIsEWKfake() and self._config.OptionGenuineTauBackgroundSource == "MC_FakeAndGenuineTauNotSeparated") or c.typeIsEWKMC() or c.typeIsGenuineB():
                        # fixme: what a mess! c.typeIsEWKMC() and c.typeIsGenuineB() ORs added for h2tb. must make a proper code!
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
                        msg = "Unknown dataset type for dataset %s!%s" % (c.getLabel(), ShellStyles.NormalStyle())
                        raise Exception(ShellStyles.ErrorStyle() + msg + ShellStyles.NormalStyle())
                    

            # Calculate signal yield
            global myBr
            myBr = self._config.OptionBr
            if not (self._config.OptionLimitOnSigmaBr or m > 161 or HW==None):
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
            if containsQCDdataset:
                TotalExpected = QCD.Clone()
                TotalExpected.Add(Embedding)
            else:
                TotalExpected = Embedding.Clone()

            if hasattr(self._config, 'OptionGenuineTauBackgroundSource'):
                if not self._config.OptionGenuineTauBackgroundSource == "MC_FakeAndGenuineTauNotSeparated":
                    if EWKFakes != None:
                        TotalExpected.Add(EWKFakes)

            # Construct table (FIXME: what a mess!)
            '''
            Example: 
            align   = "{:<3} {:<50} {:>20} {:<3} {:>20} {:>15} {:<3}"
            header  = align.format("#", "Dataset", "Cross Section", "", "Norm. Factor",  "Int. Lumi", "")
            table   = [] 
            table.append(header)
            '''
            myOutput = "*** Event yield summary ***\n"
            myOutput += self._generateHeader(m)
            myOutput += "\n"
            myOutput += "Number of events\n"
            if not (self._config.OptionLimitOnSigmaBr or m > 179):
                myOutput += "Signal, mH+=%3d GeV, Br(t->bH+)=%.2f: %s"%(m,myBr,self.getResultString(HW, self.formatStr, self.myPrecision))
            else:
                myOutput += "Signal, mH+=%3d GeV, sigma x Br=1 pb: %s"%(m,self.getResultString(HW, self.formatStr, self.myPrecision))
            myOutput += "Backgrounds:\n"
            if containsQCDdataset:
                myOutput += "                           Multijets: %s"%self.getResultString(QCD, self.formatStr, self.myPrecision)

            if hasattr(self._config, 'OptionGenuineTauBackgroundSource'):
                if self._config.OptionGenuineTauBackgroundSource == "MC_FakeAndGenuineTauNotSeparated":
                    myOutput += "                           MC EWK+tt: %s"%self.getResultString(Embedding, self.formatStr, self.myPrecision)
                else:
                    myOutput += "                    EWK+tt with taus: %s"%self.getResultString(Embedding, self.formatStr, self.myPrecision)
                    if EWKFakes != None:
                        myOutput += "               EWK+tt with fake taus: %s"%self.getResultString(EWKFakes, self.formatStr, self.myPrecision)
                myOutput += "                      Total expected: %s"%self.getResultString(TotalExpected, self.formatStr, self.myPrecision)
            # FIXME: Add support for config.OptionFakeBMeasurementSource?

            #if self._config.BlindAnalysis:
            #    myOutput += "                            Observed: BLINDED\n\n"
            #else:
	    myOutput += "                            Observed: %5d\n\n"%self._observation.getCachedShapeRootHistogramWithUncertainties().getRate()

            # Print to screen
            if self._config.OptionDisplayEventYieldSummary:
               Print(myOutput)

            # Save output to file & infor user
            myFilename = self._infoDirname + "/EventYieldSummary_m%d.txt" % m
            myFile = open(myFilename, "w")
            myFile.write(myOutput)
            myFile.close()
            msg = "Event yield summary written to "
            self.Verbose(msg + ShellStyles.SuccessStyle() + msg + myFilename + ShellStyles.NormalStyle(), True) #HighlightAltStyle

            # Save the event yield to a file (LaTeX table)
            self.saveEventYieldsToFile(m, QCD, Embedding, TotalExpected)
        return

    def saveEventYieldsToFile(self, m, QCD, Embedding, TotalExpected):
        # First construct the file name
        baseName = "EventYieldSummary_m%d_" % (m)
        fileName  = os.path.join(self._infoDirname, baseName)
        if self._h2tb:
            fileName += self._outputPrefix + "_" + self._config.DataCardName.replace(" ","_")
        else:
            fileName += self._timestamp + "_" + self._outputPrefix + "_" + self._config.DataCardName.replace(" ","_")
        fileName += ".tex"
        # Get the contents of the table
        myOutputLatex = self.getEventYieldTable(m, QCD, Embedding, TotalExpected)

        # Now save the file
        myFile = open(fileName, "w")
        myFile.write(myOutputLatex)
        myFile.close()

        # Inform user before returning
        msg = "Event yield summary (LaTeX) written to %s" % (ShellStyles.SuccessStyle() + os.path.basename(fileName) + ShellStyles.NormalStyle())
        self.Verbose(msg, True)
        return
    
    def getEventYieldTable(self, mass, QCD, Embedding, TotalExpected):
        if self._h2tb:
            return self.getEventYieldTableHToTB(mass, QCD, Embedding, TotalExpected)
        else:
            return self.getEventYieldTableHToTauNu(mass, QCD, Embedding, TotalExpected)

    def getEventYieldTableHToTB(self, m, QCD, Embedding, TotalExpected):
        myOutputLatex = "% table auto gene rated by datacard generator on "+self._timestamp+" for "+self._config.DataCardName+" / "+self._outputPrefix+"\n"
        myOutputLatex += "\\renewcommand{\\arraystretch}{1.2}\n"
        #myOutputLatex += "\\begin{table}\n"
        #myOutputLatex += "\\centering\n"
        #myOutputLatex += "\\caption{Summary of the number of events from the signal with mass point $\\mHpm=%d\\GeVcc$,\n"%(m)
        #myOutputLatex += "           from the background measurements, and the observed event yield. Luminosity uncertainty is not included in the numbers.}\n"
        #myOutputLatex += "\\label{tab:summary:yields}\n"
        #myOutputLatex += "\\vskip 0.1 in\n"
        #myOutputLatex += "\\hspace*{-.8cm}\n"
        myOutputLatex += "\\begin{tabular}{ l c }\n"
        myOutputLatex += "\\hline\n"
        myOutputLatex += "\\multicolumn{1}{ c }{Source}  & Events $\\pm$ stat. $\\pm$ syst.  \\\\ \n"
        myOutputLatex += "\\hline\n"
        # myOutputLatex += "HH+HW, $\\mHplus = %3d\\GeVcc             & %s \\\\ \n"%(m,getLatexResultString(HW, self.formatStr, self.myPrecision))
        # myOutputLatex += "\\hline\n"
        if self._config.OptionFakeBMeasurementSource:
            myOutputLatex += "\\FakeB background (data-driven)   & %s \\\\ \n" % self.getLatexResultString(QCD, self.formatStr, self.myPrecision)
            myOutputLatex += "\\GenuineB background              & %s \\\\ \n" % self.getLatexResultString(Embedding, self.formatStr, self.myPrecision)
        myOutputLatex += "  \\hline\n"
        myOutputLatex += "  Total expected from the SM              & %s \\\\ \n" % self.getLatexResultString(TotalExpected, self.formatStr, self.myPrecision)
        if self._config.BlindAnalysis:
            myOutputLatex += "  Observed & BLINDED \\\\ \n"
        else:
            myOutputLatex += "  Observed & %5d \\\\ \n"%self._observation.getCachedShapeRootHistogramWithUncertainties().getRate()
        myOutputLatex += "  \\hline\n"
        myOutputLatex += "  \\end{tabular}\n"
        #myOutputLatex += "\\end{table}\n"
        myOutputLatex += "\\renewcommand{\\arraystretch}{1}\n"
        return myOutputLatex

    def getEventYieldTableHToTauNu(self, m, QCD, Embedding, TotalExpected):
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
        myOutputLatex += "  HH+HW, $\\mHplus = %3d\\GeVcc             & %s \\\\ \n" % (m, self.getLatexResultString(HW, self.formatStr, self.myPrecision))
        myOutputLatex += "  \\hline\n"
        if containsQCDdataset:
            myOutputLatex += "  Multijet background (data-driven)       & %s \\\\ \n" % self.getLatexResultString(QCD, self.formatStr, self.myPrecision)
            

        if hasattr(self._config, 'OptionGenuineTauBackgroundSource'):
            if self._config.OptionGenuineTauBackgroundSource == "MC_FakeAndGenuineTauNotSeparated":
                myOutputLatex += "  MC EWK+\\ttbar                           & %s \\\\ \n" % self.getLatexResultString(Embedding, self.formatStr, self.myPrecision)
            else:
                myOutputLatex += "  EWK+\\ttbar with $\\tau$ (data-driven)    & %s \\\\ \n" % self.getLatexResultString(Embedding, self.formatStr, self.myPrecision)
                if EWKFakes != None:
                    myOutputLatex += "  EWK+\\ttbar with e/\\mu/jet\\to$\\tau$ (MC) & %s \\\\ \n" % self.getLatexResultString(EWKFakes, self.formatStr, self.myPrecision)
        # FIXME: Add support for config.OptionFakeBMeasurementSource?
        myOutputLatex += "  \\hline\n"
        myOutputLatex += "  Total expected from the SM              & %s \\\\ \n" % self.getLatexResultString(TotalExpected, self.formatStr, self.myPrecision)
        # if self._config.BlindAnalysis:
        #    myOutputLatex += "  Observed: & BLINDED \\\\ \n"
        # else:
        myOutputLatex += "  Observed: & %5d \\\\ \n"%self._observation.getCachedShapeRootHistogramWithUncertainties().getRate()
        myOutputLatex += "  \\hline\n"
        myOutputLatex += "  \\end{tabular}\n"
        myOutputLatex += "\\end{table}\n"
        myOutputLatex += "\\renewcommand{\\arraystretch}{1}\n"
        return myOutputLatex

    def _getFormattedSystematicsNumber(self, value):
        '''
        Returns a string with proper numerical formatting
        '''
        if abs(value) >= 0.1:
            return "%.0f"%(abs(value)*100)
        elif abs(value) >= 0.001:
            return "%.1f"%(abs(value)*100)
        else:
            return "\\textless~0.1"

    def makeSystematicsSummary(self,light=False):
        '''
        Prints systematics summary table
        '''
        if self._h2tb and light==True:
            return
        signalColumn="CMS_Hptntj_Hp"
        if light:
            signalColumn="HW"
        myColumnOrder = [signalColumn, 
                         "CMS_Hptntj_QCDandFakeTau", 
                         "ttbar_CMS_Hptntj", 
                         "CMS_Hptntj_W", 
                         "CMS_Hptntj_singleTop",
                         "CMS_Hptntj_DY", 
                         "CMS_Hptntj_VV"]


        if self._h2tb:
            myColumnOrder = ["Hp",  "FakeB", "TT_GenuineB", "SingleTop_GenuineB"]
            if self._Paper:
                myColumnOrder = ["Hp",  "FakeB", "TT_GenuineB", "ttX_GenuineB", "EWK_GenuineB"]
                myNuisanceOrder = [["lumi_13TeV"         , "luminosity (13 TeV)"],
                                   ["CMS_eff_trg_MC"     , "trigger efficiency"],
                                   ["CMS_eff_e_veto"     , "electron veto eff."],
                                   ["CMS_eff_m_veto"     , "muon veto eff."],
                                   ["CMS_eff_tau_veto"   , "tau veto eff."],
                                   ["CMS_eff_b"          , "b-tagging eff."],
                                   ["CMS_scale_j"        , "jet energy scale"],
                                   ["CMS_res_j"          , "jet energy resolution"],
                                   #["CMS_topreweight"    ,"top $p_T$ reweighting"],
                                   ["CMS_pileup"         , "pileup reweighting"],
                                   ["CMS_HPTB_toptagging", "top tagging"],
                                   ["QCDscale_ttbar"     , "$t\\bar{t}$ scale"],
                                   ["pdf_ttbar"          , "$t\\bar{t}$ pdf"],
                                   ["mass_top"           , "top mass"],
                                   ["QCDscale_singleTop" , "$t\\bar{t}$+X scale"],
                                   ["pdf_singleTop"      , "$t\\bar{t}$+X pdf"],
                                   ["QCDscale_ewk"       , "EWK scale"],
                                   ["pdf_ewk"            , "EWK pdf"],
                                   ["CMS_HPTB_pdf_HPTB"  , "pdf acceptance (signal)"],
                                   ["CMS_HPTB_pdf_top"   , "pdf acceptance (top)"],
                                   ["CMS_HPTB_pdf_ewk"   , "pdf acceptance (EWK)"],
                                   ["CMS_HPTB_mu_RF_HPTB", "RF scale acceptance (signal)"],
                                   ["CMS_HPTB_mu_RF_top" , "RF scale acceptance (top)"],
                                   ["CMS_HPTB_mu_RF_ewk" , "RF scale acceptance (EWK)"],
                                   ]
            else:
                myNuisanceOrder = [["CMS_eff_trg_MC", "trigger efficiency"],
                                   ["CMS_eff_e_veto", "electron veto eff."],
                                   ["CMS_eff_m_veto", "muon veto eff."],
                                   ["CMS_eff_tau_veto", "tau veto eff."],
                                   ["CMS_eff_b", "b-tagging eff."],
                                   ["CMS_scale_j", "jet energy scale"],
                                   ["CMS_res_j", "jet energy resolution"],
                                   #["CMS_topreweight","top $p_T$ reweighting"],
                                   ["CMS_pileup", "pileup reweighting"],
                                   ["CMS_HPTB_toptagging", "top tagging"],
                                   ["QCDscale_ttbar", "$t\\bar{t}$ scale"],
                                   ["pdf_ttbar", "$t\\bar{t}$ pdf"],
                                   ["mass_top", "top mass"],
                                   ["QCDscale_ttW", "$t\\bar{t}$W scale"],
                                   ["pdf_ttW", "$t\\bar{t}$W pdf"],
                                   ["QCDscale_ttZ", "$t\\bar{t}$Z scale"],
                                   ["pdf_ttZ", "$t\\bar{t}$Z pdf"],
                                   ["QCDscale_Wjets", "W+jets scale"],
                                   ["pdf_Wjets", "W+jets pdf"],
                                   ["QCDscale_DY",  "DY scale"],
                                   ["pdf_DY", "DY pdf"],
                                   ["QCDscale_VV", "Diboson scale"],
                                   ["pdf_VV", "Diboson pdf"],
                                   ["lumi_13TeV", "luminosity (13 TeV)"],
                                   ["CMS_HPTB_pdf_HPTB"  , "pdf acceptance (signal)"],
                                   ["CMS_HPTB_pdf_top"   , "pdf acceptance (top)"],
                                   ["CMS_HPTB_pdf_ewk"   , "pdf acceptance (EWK)"],
                                   ["CMS_HPTB_mu_RF_HPTB", "RF scale acceptance (signal)"],
                                   ["CMS_HPTB_mu_RF_top" , "RF scale acceptance (top)"],
                                   ["CMS_HPTB_mu_RF_ewk" , "RF scale acceptance (EWK)"],
                                   ["CMS_HPTB_fakeB_transferfactor", "Fake $b$ transfer factors"]
                                   ]
                for d in aux.GetListOfRareDatasets():
                    dName = d + "_GenuineB"
                    myColumnOrder.append(dName)
        else:
            myNuisanceOrder = [["CMS_eff_t","tau ID"], # first ID, then the text that goes to the table
                               ["CMS_eff_t_highpt","high-$p_{T}$ tau ID"],        
                               ["CMS_eff_t_trg_data","trigger tau leg eff. for data"],
                               ["CMS_eff_t_trg_MC","trigger tau leg eff. for MC"],
                               ["CMS_eff_met_trg_data","trigger MET leg eff. for data"],
                               ["CMS_eff_met_trg_MC","trigger MET leg eff. for MC"],
                               ["CMS_eff_e_veto","electron veto eff."],
                               ["CMS_eff_m_veto","muon veto eff."],
                               ["CMS_fake_e_to_t","electrons mis-id. as taus"],
                               ["CMS_fake_m_to_t","muons mis-id. as taus"],
                               ["CMS_eff_b","b-tagging eff."],
                               ["CMS_fake_b","b-mistagging eff."],
                               ["CMS_scale_t","tau energy scale"],
                               ["CMS_scale_j","jet energy scale"],
                               ["CMS_scale_met","MET unclustered energy scale"],
                               ["CMS_res_j","jet energy resolution"],
                               ["CMS_topPtReweight","top $p_T$ reweighting"],
                               ["CMS_pileup","pileup reweighting"],
                               ["CMS_Hptn_pdf_Hptn", "pdf acceptance (signal)"],
                               ["CMS_Hptn_pdf_top", "pdf acceptance (top BG)"],
                               ["CMS_Hptn_pdf_ewk", "pdf acceptance (EWK BG)"],
                               ["CMS_Hptn_mu_RF_Hptn", "RF scale acceptance (signal)"],
                               ["CMS_Hptn_mu_RF_top", "RF scale acceptance (top BG)"],
                               ["CMS_Hptn_mu_RF_ewk", "RF scale acceptance (EWK BG)"],
                               ["QCDscale_ttbar", "ttbar scale"],
                               ["pdf_ttbar", "ttbar pdf"],
                               ["mass_top", "top mass"],
                               ["QCDscale_Wjets", "W+jets scale"],
                               ["pdf_Wjets", "W+jets pdf"],
                               ["QCDscale_DY", "DY scale"],
                               ["pdf_DY", "DY pdf"],
                               ["QCDscale_VV", "diboson scale"],
                               ["pdf_VV", "diboson pdf"],
                               ["lumi_13TeV","luminosity (13 TeV)"],
                               ["CMS_Hptntj_fake_t_fit","Fake tau template fit"],
                               ["CMS_Hptntj_fake_t_shape","Fake tau mT shape"]
                               ]
            
        # Make table - The horror!
        myTable = []
        for n in myNuisanceOrder: # for each nuisance
            resultFound=False
            myRow = [n[1]]
            isShape=False
            # For-loop: All columns (in pre-defined order)
            for columnName in myColumnOrder:
                myMinErrorUp   = 9999.0
                myMinErrorDown = 9999.0
                myMaxErrorUp   = -9999.0
                myMaxErrorDown = -9999.0
                myErrorUp      = 0.0
                myErrorDown    = 0.0
                
                # For-loop: All datasets
                for c in self._datasetGroups: 

                    # if column name matches to dataset group label
                    foundMatch = columnName in c.getLabel()
                    if self._h2tb and not "Hp" in c.getLabel():
                        foundMatch = (columnName == c.getLabel())
                    if foundMatch: 
                        # if this column+nuisance combination matches to a list, loop over the list
                        if isinstance(n[0], list): 
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
                elif ( (myMaxErrorUp-myMinErrorUp)<0.001 and (myMaxErrorDown-myMinErrorDown)<0.001 ):
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

        # Make systematics table & save to file        
        myOutput = self.getSystematicsTable(myTable)
        fileName = self.getSystematicsFileName(light)
        myFile   = open(fileName, "w")
        myFile.write(myOutput)
        myFile.close()
        msg = "Created systematics LaTeX table %s" % (ShellStyles.SuccessStyle() + fileName + ShellStyles.NormalStyle())
        self.Verbose(msg, True)
        return

    def getSystematicsTable(self, myTable):
        if self._h2tb:
            return self.getSystematicsTableHToTB(myTable)
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
        myOutput += "& Signal & Jet \to \taujet & \multicolumn{5}{c}{EWK+t\={t} genuine tau and e/\mu \to \taujet}"
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
        return myOutput 

    def getSystematicsTableHToTB(self, myTable):
        myOutput  = "\\renewcommand{\\arraystretch}{1.2}\n"
        myOutput += "\\resizebox{1.0\\linewidth}{!}{%\n"
        myOutput += "\\label{tab:summary:systematics}\n"
        if self._Paper: #can do this much smarter!
            myOutput += "\\begin{tabular}{l|c|c|ccc}\n"
        else:
            myOutput += "\\begin{tabular}{l|c|c|cccccccc}\n"            
        myOutput += "\\hline\n"
        if self._Paper: #can do this much smarter!
            myOutput += "& Signal & Fake b & \multicolumn{3}{c}{Genuine b}"
        else:
            myOutput += "& Signal & Fake b & \multicolumn{8}{c}{Genuine b}"
        myOutput += "\n \\\\"
        if self._Paper:
            myCaptionLine = [["","","","$t\\bar{t}$", "$t\\bar{t}$+X", "EWK"]] 
            #myCaptionLine = [["","","","$t\\bar{t}$", "Single top", "Rares"]] 
        else:
            myCaptionLine = [["","","","$t\\bar{t}$", "Single top", "$t\\bar{t}$+Z", "$t\\bar{t}t\\bar{t}$", "$Z/\gamma^{*}$+jets", "$t\\bar{t}$+W", "W+jets", "Diboson"]] 
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
        #myOutput += "\\end{center}\n"
        #myOutput += "\\end{table}\n"
        myOutput += "\\renewcommand{\\arraystretch}{1}\n"
        #myOutput += "\\end{document}"
        #myOutput += "}\n"
        return myOutput 

    def getSystematicsFileName(self, light):
        postFix = "_heavy.tex"
        if light:
            postFix = "_light.tex"
        if self._h2tb:
            postFix = ".tex"

        filePath = os.path.join(self._infoDirname, "SystematicsSummary")
        fileName = filePath + postFix
        return fileName
             
    def makeQCDPuritySummary(self):
        '''
        Prints QCD purity information
        '''
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
        Print("Created datacards with 0 +-1 -> 1 +- 0 shift for each shape nuisance", True)
        for item in myOutList:
            print item
        
