## \package Extractor
# Classes for extracting observation/rate/nuisance from datasets
#
#

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.Extractor import ExtractorBase
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardColumn import DatacardColumn
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ProgressBar import ProgressBar

from math import pow,sqrt
import os
import sys
import time
import ROOT

## ExtractorBase class
class TableProducer:
    ## Constructor
    def __init__(self, opts, config, luminosity, observation, datasetGroups, extractors):
        self._opts = opts
        self._config = config
        self._luminosity = luminosity
        self._observation = observation
        self._datasetGroups = datasetGroups
        self._extractors = extractors
        self._outfile = None
        self._timestamp = time.strftime("%y%m%d_%H%M%S", time.gmtime(time.time()))
        self._outputFileStem = "lands_datacard_hplushadronic_m"
        self._outputRootFileStem = "lands_histograms_hplushadronic_m"
        # Calculate number of nuisance parameters
        self._nNuisances = 0
        for n in self._extractors:
            if n.isPrintable():
                self._nNuisances += 1

        self.makeDataCards()

    ## Generates datacards
    def makeDataCards(self):
        # Make directory for output
        myDirname = "datacards_"+self._timestamp+"_"+self._config.DataCardName
        os.mkdir(myDirname)
        # Obtain observation line
        for m in self._config.MassPoints:
            print "\n\033[0;44m\033[1;37mGenerating datacard for mass point %d\033[0;0m"%m
            # Open output root file
            myFilename = myDirname+"/"+self._outputFileStem+"%d.txt"%m
            myRootFilename = myDirname+"/"+self._outputRootFileStem+"%d.root"%m
            self._outfile = ROOT.TFile.Open(myRootFilename, "RECREATE")
            if self._outfile == None:
                print "\033[0;41m\033[1;37mError:\033[0;0m Cannot open file '"+myRootFilename+"' for output!"
                sys.exit()
            # Invoke extractors
            print "... obtaining observation"
            myObservationLine = self._generateObservationLine()
            print "... obtaining rates"
            myRateHeaderTable = self._generateRateHeaderTable(m)
            myRateDataTable = self._generateRateDataTable(m)
            print "... obtaining nuisances"
            myNuisanceTable = self._generateNuisanceTable(m)
            # Calculate dimensions of tables
            myWidths = []
            myWidths = self._calculateCellWidths(myWidths, myRateHeaderTable)
            myWidths = self._calculateCellWidths(myWidths, myRateDataTable)
            myWidths = self._calculateCellWidths(myWidths, myNuisanceTable)
            mySeparatorLine = self._getSeparatorLine(myWidths)
            # Construct datacard
            myCard = ""
            myCard += self._generateHeader(m)
            myCard += mySeparatorLine
            myCard += self._generateParameterLines()
            myCard += mySeparatorLine
            myCard += self._generateShapeHeader(m)
            myCard += mySeparatorLine
            myCard += myObservationLine
            myCard += mySeparatorLine
            myCard += self._getTableOutput(myWidths,myRateHeaderTable)
            myCard += mySeparatorLine
            myCard += self._getTableOutput(myWidths,myRateDataTable)
            myCard += mySeparatorLine
            myCard += self._getTableOutput(myWidths,myNuisanceTable)
            # Print datacard to screen if requested
            if self._opts.showDatacard:
                print myCard
            # Save datacard to file
            myFile = open(myFilename, "w")
            myFile.write(myCard)
            myFile.close()
            print "Written datacard to:",myFilename
            # Close root file
            self._outfile.Write()
            self._outfile.Close()
            print "Written shape root file to:",myRootFilename

    ## Generates header of datacard
    def _generateHeader(self, mass):
        myString = "Description: LandS datacard (auto generated) mass=%d, luminosity=%f 1/fb, %s\n"%(mass,self._luminosity,self._config.DataCardName)
        myString += "Date: %s\n"%time.ctime()
        return myString

    ## Generates parameter lines
    def _generateParameterLines(self):
        # Produce result
        myResult =  "imax     1     number of channels\n"
        myResult += "jmax     *     number of backgrounds\n"
        myResult += "kmax    %2d     number of parameters\n"%self._nNuisances
        return myResult

    ## Generates shape header
    def _generateShapeHeader(self,mass):
        myResult = "shapes * * %s%d.root $PROCESS $PROCESS_$SYSTEMATIC\n"%(self._outputRootFileStem,mass)
        return myResult

    ## Generates observation lines
    def _generateObservationLine(self):
        # Obtain observed number of events
        myObsCount = self._observation.getRateValue(self._luminosity)
        if self._opts.debugMining:
            print "  Observation is %d"%myObsCount
        myResult = "Observation    %d\n"%myObsCount
        # FIXME add here call to store histograms from nuisance to root file
        return myResult

    ## Generates header for rate table as list
    def _generateRateHeaderTable(self,mass):
        myResult = []
        # obtain bin numbers
        myRow = ["bin",""]
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass):
                myRow.append("1")
        myResult.append(myRow)
        # obtain labels
        myRow = ["process",""]
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass):
                myRow.append(c.getLabel())
        myResult.append(myRow)
        # obtain process numbers
        myRow = ["process",""]
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass):
                myRow.append(str(c.getLandsProcess()))
        myResult.append(myRow)
        return myResult

    ## Generates rate numbers for rate table as list
    def _generateRateDataTable(self,mass):
        myResult = []
        myRow = ["rate",""]
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass):
                myRateValue = c.getRateValue(self._luminosity)
                if myRateValue == None:
                    myRateValue = 0.0
                if self._opts.debugMining:
                    print "  Rate for '%s' = %.3f"%(c.getLabel(),myRateValue)
                myRow.append("%.3f"%myRateValue)
                # FIXME add here call to store histograms from nuisance to root file
        myResult.append(myRow)
        return myResult

    ## Generates nuisance table as list
    def _generateNuisanceTable(self,mass):
        myBar = ProgressBar(self._nNuisances)
        myResult = []
        # Loop over rows
        myN = 0.0
        for n in sorted(self._extractors, key=lambda x: x.getId()):
            if n.isPrintable():
                myN += 1.0
                myBar.draw(float(myN) / float(self._nNuisances))
                myRow = ["%d"%int(n.getId()), n.getDistribution()]
                # Loop over columns
                for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
                    if c.isActiveForMass(mass):
                        # Check that column has current nuisance or has nuisance that is slave to current nuisance
                        myStatus = c.hasNuisanceId(n.getId())
                        myValue = 0.0
                        if myStatus:
                            if n.isShapeNuisance():
                                myValue = None
                                # FIXME add here call to store histograms from nuisance to root file
                            else:
                                myValue = n.doExtract(c, self._luminosity)
                        mySlaveStatus = False
                        for slaveCandidate in self._extractors:
                            if not slaveCandidate.isPrintable() and slaveCandidate.getMasterId() == n.getId():
                                if c.hasNuisanceId(slaveCandidate.getId()):
                                    #print "id=",slaveCandidate.getId(),"is slave of",n.getId()
                                    mySlaveStatus = True
                                    if slaveCandidate.isShapeNuisance():
                                        myValue = None
                                        # FIXME add here call to store histograms from nuisance to root file
                                    else:
                                        myValue = slaveCandidate.doExtract(c, self._luminosity)
                        if myStatus or mySlaveStatus:
                            myValueString = ""
                            # Check output format
                            if myValue == None:
                                myValueString = "1"
                            else:
                                if isinstance(myValue, list):
                                    for i in range(0,len(myValue)):
                                        if i == 0:
                                            myValueString += "%.3f"%(myValue[i]+1.0)
                                        else:
                                            myValueString += "/%.3f"%(myValue[i]+1.0)
                                else:
                                    # Assume that result is a plain number
                                    myValueString += "%.3f"%(myValue+1.0)
                            if self._opts.debugMining:
                                print "  Nuisance for '%s/%s' in column '%s': %s"%(n.getId(),n.getDescription(),c.getLabel(),myValueString)
                            myRow.append(myValueString)
                        else:
                            if n.isShapeNuisance():
                                myRow.append("0")
                            else:
                                myRow.append("1")
                # Add description to end of the row
                myRow.append(n.getDescription())
                myResult.append(myRow)
        myBar.finished()
        return myResult

    ## Calculates maximum width of each table cell
    def _calculateCellWidths(self,widths,table):
        myResult = widths
        # Initialise widths if necessary
        for i in range(len(widths),len(table[0])):
            myResult.append(0)
        # Loop over table cells
        for row in table:
            for i in range(0,len(row)):
                if len(row[i]) > myResult[i]:
                    myResult[i] = len(row[i])
        return myResult

    ## Returns a separator line of correct total width
    def _getSeparatorLine(self,widths):
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
    def _getTableOutput(self,widths,table):
        myResult = ""
        for row in table:
            for i in range(0,len(row)):
                if i != 0:
                    myResult += " "
                myResult += row[i].ljust(widths[i])
            myResult += "\n"
        return myResult
