## \package Extractor
# Classes for extracting observation/rate/nuisance from datasets
#
#

from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.Extractor import ExtractorBase
from HiggsAnalysis.HeavyChHiggsToTauNu.datacardtools.DatacardColumn import DatacardColumn
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles import *

from math import pow,sqrt
import os
import sys
import time
import ROOT

## EventYieldSummary class
class EventYieldSummary:
    ## Constructor
    def __init__(self):
        self._rate = 0.0
        self._absoluteStat = 0.0
        self._absoluteSystUp = 0.0
        self._absoluteSystDown = 0.0

    def extract(self, opts, config, datasetColumn, extractors):
        self._rate = datasetColumn.getRateResult()
        myAbsoluteSystUpSquared = 0.0
        myAbsoluteSystDownSquared = 0.0
        for n in sorted(extractors, key=lambda x: x.getId()):
            if n.isPrintable():
                if datasetColumn.hasNuisanceByMasterId(n.getId()):
                    myValue = datasetColumn.getNuisanceResultByMasterId(n.getId())
                    if "stat" in n.getDescription() and n.isNuisance():
                        self._absoluteStat = myValue * self._rate
                    else:
                        if n.isAsymmetricNuisance():
                            myAbsoluteSystDownSquared += pow(myValue[0] * self._rate,2)
                            myAbsoluteSystUpSquared += pow(myValue[1] * self._rate,2)
                        elif n.isNuisance():
                            myAbsoluteSystDownSquared += pow(myValue * self._rate,2)
                            myAbsoluteSystUpSquared += pow(myValue * self._rate,2)
                        elif n.isShapeNuisance() and n.getDistribution() == "shapeQ":
                            # Determine maximum of values
                            myMax = 0.0
                            for v in myValue:
                                if v > myMax:
                                    myMax = v
                            myAbsoluteSystDownSquared += pow(myMax * self._rate,2)
                            myAbsoluteSystUpSquared += pow(myMax * self._rate,2)
        self._absoluteSystDown = sqrt(myAbsoluteSystDownSquared)
        self._absoluteSystUp = sqrt(myAbsoluteSystUpSquared)

    ## Combines with another event yield summary
    def add(self,summary):
        self._rate += summary.getRate()
        self._absoluteStat = sqrt(pow(self._absoluteStat,2)+pow(summary.getAbsoluteStat(),2))
        self._absoluteSystDown = sqrt(pow(self._absoluteSystDown,2)+pow(summary.getAbsoluteSystDown(),2))
        self._absoluteSystUp = sqrt(pow(self._absoluteSystUp,2)+pow(summary.getAbsoluteSystUp(),2))

    def getRate(self):
        return self._rate

    def getAbsoluteStat(self):
        return self._absoluteStat

    def getAbsoluteSystDown(self):
        return self._absoluteSystDown

    def getAbsoluteSystUp(self):
        return self._absoluteSystUp

## TableProducer class
class TableProducer:
    ## Constructor
    def __init__(self, opts, config, outputPrefix, luminosity, observation, datasetGroups, extractors):
        self._opts = opts
        self._config = config
        self._outputPrefix = outputPrefix
        self._luminosity = luminosity
        self._observation = observation
        self._datasetGroups = datasetGroups
        self._extractors = extractors
        self._timestamp = time.strftime("%y%m%d_%H%M%S", time.gmtime(time.time()))
        self._outputFileStem = "lands_datacard_hplushadronic_m"
        self._outputRootFileStem = "lands_histograms_hplushadronic_m"
        # Calculate number of nuisance parameters
        self._nNuisances = 0
        for n in self._extractors:
            if n.isPrintable():
                self._nNuisances += 1
        # Make directory for output
        self._dirname = "datacards_"+self._timestamp+"_"+self._outputPrefix+"_"+self._config.DataCardName
        os.mkdir(self._dirname)

        # Make datacards
        self.makeDataCards()

        # Make other reports
        print "\n"+HighlightStyle()+"Generating reports"+NormalStyle()
        # Print table of shape variation for shapeQ nuisances
        self.makeShapeVariationTable()
        # Print event yield summary table
        self.makeEventYieldSummary()
        # Print systematics summary table
        self.makeSystematicsSummary()

    ## Generates datacards
    def makeDataCards(self):
        # Obtain observation line
        for m in self._config.MassPoints:
            print "\n"+HighlightStyle()+"Generating datacard for mass point %d for "%m +self._outputPrefix+NormalStyle()
            # Open output root file
            myFilename = self._dirname+"/"+self._outputFileStem+"%d.txt"%m
            myRootFilename = self._dirname+"/"+self._outputRootFileStem+"%d.root"%m
            myRootFile = ROOT.TFile.Open(myRootFilename, "RECREATE")
            if myRootFile == None:
                print ErrorStyle()+"Error:"+NormalStyle()+" Cannot open file '"+myRootFilename+"' for output!"
                sys.exit()
            # Invoke extractors
            myObservationLine = self._generateObservationLine()
            myRateHeaderTable = self._generateRateHeaderTable(m)
            myRateDataTable = self._generateRateDataTable(m)
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
            # Save histograms to root file
            self._saveHistograms(myRootFile,m),
            # Close root file
            myRootFile.Write()
            myRootFile.Close()
            print "Written shape root file to:",myRootFilename

    ## Generates header of datacard
    def _generateHeader(self, mass):
        myString = "Description: LandS datacard (auto generated) mass=%d, luminosity=%f 1/fb, %s/%s\n"%(mass,self._luminosity,self._config.DataCardName,self._outputPrefix)
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
        myObsCount = self._observation.getRateResult()
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
                myRateValue = c.getRateResult()
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
        myResult = []
        # Loop over rows
        for n in sorted(self._extractors, key=lambda x: x.getId()):
            if n.isPrintable():
                myRow = ["%d"%int(n.getId()), n.getDistribution()]
                # Loop over columns
                for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
                    if c.isActiveForMass(mass):
                        # Check that column has current nuisance or has nuisance that is slave to current nuisance
                        if c.hasNuisanceByMasterId(n.getId()):
                            myValue = c.getNuisanceResultByMasterId(n.getId())
                            myValueString = ""
                            # Check output format
                            if myValue == None or n.isShapeNuisance():
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
        return myResult

    ## Generates nuisance table as list
    def _generateShapeNuisanceVariationTable(self,mass):
        myResult = []
        # Loop over rows
        for n in sorted(self._extractors, key=lambda x: x.getId()):
            if n.isPrintable() and n.getDistribution() == "shapeQ":
                myDownRow = ["%d"%int(n.getId())+"_Down", ""]
                myUpRow = ["%d"%int(n.getId())+"_Up", ""]
                # Loop over columns
                for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
                    if c.isActiveForMass(mass):
                        # Check that column has current nuisance or has nuisance that is slave to current nuisance
                        if c.hasNuisanceByMasterId(n.getId()):
                            myValue = c.getNuisanceResultByMasterId(n.getId())
                            # Check output format
                            if not isinstance(myValue, list):
                                print ErrorStyle()+"Error: Nuisance '"+n.getId()+"'did strangely not return a list of results for shapeQ. Check code."+NormalStyle()
                                sys.exit()
                            myDownRow.append("%.3f"%(myValue[0]))
                            myUpRow.append("%.3f"%(myValue[1]))
                        else:
                            myDownRow.append("-")
                            myUpRow.append("-")
                # Add description to end of the row
                myDownRow.append(n.getDescription())
                myUpRow.append(n.getDescription())
                myResult.append(myDownRow)
                myResult.append(myUpRow)
        return myResult

    ## Save histograms to root file
    def _saveHistograms(self,rootFile,mass):
        # Observation
        self._observation.setResultHistogramsToRootFile(rootFile)
        # Loop over columns
        for c in sorted(self._datasetGroups, key=lambda x: x.getLandsProcess()):
            if c.isActiveForMass(mass):
                c.setResultHistogramsToRootFile(rootFile)

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

    ## Generates table of shape variation for shapeQ nuisances
    def makeShapeVariationTable(self):
        myOutput = ""
        for m in self._config.MassPoints:
            # Invoke extractors
            myRateHeaderTable = self._generateRateHeaderTable(m)
            myNuisanceTable = self._generateShapeNuisanceVariationTable(m)
            # Calculate dimensions of tables
            myWidths = []
            myWidths = self._calculateCellWidths(myWidths, myRateHeaderTable)
            myWidths = self._calculateCellWidths(myWidths, myNuisanceTable)
            mySeparatorLine = self._getSeparatorLine(myWidths)
            # Construct output
            myOutput += "*** Shape nuisance variation summary ***\n"
            myOutput += self._generateHeader(m)
            myOutput += mySeparatorLine
            myOutput += self._getTableOutput(myWidths,myRateHeaderTable)
            myOutput += mySeparatorLine
            myOutput += self._getTableOutput(myWidths,myNuisanceTable)
            myOutput += "\n"
        # Save output to file
        myFilename = self._dirname+"/shapeVariationResults.txt"
        myFile = open(myFilename, "w")
        myFile.write(myOutput)
        myFile.close()
        print "Shape variation tables written to:",myFilename

    ## Prints event yield summary table
    def makeEventYieldSummary(self):
        Data = EventYieldSummary()
        Data.extract(self._opts,self._config,self._observation,self._extractors)
        for m in self._config.MassPoints:
            myOutput = ""
            myOutputLatex = ""
            HH = EventYieldSummary()
            HW = EventYieldSummary()
            QCD = EventYieldSummary()
            Embedding = EventYieldSummary()
            EWKFakes = EventYieldSummary()
            # Loop over columns
            for c in self._datasetGroups:
                if c.isActiveForMass(m):
                    mySummary = EventYieldSummary()
                    mySummary.extract(self._opts,self._config,c,self._extractors)
                    # Find out what type the column is
                    if c.getLandsProcess() == -1:
                        HH.add(mySummary)
                    elif c.getLandsProcess() == 0:
                        HW.add(mySummary)
                    elif c.typeIsQCD():
                        QCD.add(mySummary)
                    elif c.typeIsEWK():
                        Embedding.add(mySummary)
                    else:
                        EWKFakes.add(mySummary)
            # Calculate signal yield
            myBr = 0.05
            if self._config.OptionBr == None:
                print WarningStyle()+"Warning: Br(t->bH+) has not been specified in config file, using default 0.05! To specify, add OptionBr=0.05 to the config file."+NormalStyle()
                myBr = self._config.OptionBr
            mySignalRate = HH.getRate() * pow(myBr,2) + HW.getRate() * 2.0 * myBr * (1.0 - myBr)
            mySignalStat = sqrt(pow(HH.getAbsoluteStat() * pow(myBr,2),2) + pow(HW.getAbsoluteStat() * 2.0 * myBr * (1.0 - myBr),2))
            mySignalSystDown = sqrt(pow(HH.getAbsoluteSystDown() * pow(myBr,2),2) + pow(HW.getAbsoluteSystDown() * 2.0 * myBr * (1.0 - myBr),2))
            mySignalSystUp = sqrt(pow(HH.getAbsoluteSystUp() * pow(myBr,2),2) + pow(HW.getAbsoluteSystUp() * 2.0 * myBr * (1.0 - myBr),2))
            # Calculate expected yield
            TotalExpected = EventYieldSummary()
            TotalExpected.add(QCD)
            TotalExpected.add(Embedding)
            TotalExpected.add(EWKFakes)
            # Construct table
            myOutput = "*** Event yield summary ***\n"
            myOutput += self._generateHeader(m)
            myOutput += "\n"
            myOutput += "Number of events\n"
            myOutput += "Signal, mH+=%3d GeV, Br(t->bH+)=%.2f:  %5.0f +- %4.0f (stat.) "%(m,myBr,mySignalRate,mySignalStat)
            if round(mySignalSystDown) == round(mySignalSystUp):
                myOutput += "+- %4.0f (syst.)\n"%mySignalSystDown
            else:
                myOutput += "+%4.0f -%4.0f (syst.)\n"%(mySignalSystUp, mySignalSystDown)
            myOutput += "Backgrounds:\n"
            myOutput += "                           Multijets: %5.0f +- %4.0f (stat.) +- %4.0f (syst.)\n"%(QCD.getRate(),QCD.getAbsoluteStat(),QCD.getAbsoluteSystDown())
            myOutput += "                    EWK+tt with taus: %5.0f +- %4.0f (stat.) +- %4.0f (syst.)\n"%(Embedding.getRate(),Embedding.getAbsoluteStat(),Embedding.getAbsoluteSystDown())
            myOutput += "               EWK+tt with fake taus: %5.0f +- %4.0f (stat.) "%(EWKFakes.getRate(),EWKFakes.getAbsoluteStat())
            if round(EWKFakes.getAbsoluteSystDown()) == round(EWKFakes.getAbsoluteSystUp()):
                myOutput += "+- %4.0f (syst.)\n"%EWKFakes.getAbsoluteSystDown()
            else:
                myOutput += "+%4.0f -%4.0f (syst.)\n"%(EWKFakes.getAbsoluteSystUp(), EWKFakes.getAbsoluteSystDown())
            myOutput += "                      Total expected: %5.0f +- %4.0f (stat.) "%(TotalExpected.getRate(),TotalExpected.getAbsoluteStat())
            if round(TotalExpected.getAbsoluteSystDown()) == round(TotalExpected.getAbsoluteSystUp()):
                myOutput += "+- %4.0f (syst.)\n"%(TotalExpected.getAbsoluteSystUp())
            else:
                myOutput += "+%4.0f -%4.0f (syst.)\n"%(TotalExpected.getAbsoluteSystUp(), TotalExpected.getAbsoluteSystDown())
            myOutput += "                            Observed: %5d\n\n"%Data.getRate() #FIXME add blinding
            # Save output to file
            myFilename = self._dirname+"/EventYieldSummary_m%d.txt"%m
            myFile = open(myFilename, "w")
            myFile.write(myOutput)
            myFile.close()

            # FIXME add timestamp to latex table
            myOutputLatex += "\renewcommand{\arraystretch}{1.2}\n"
            myOutputLatex += "\begin{table}\n"
            myOutputLatex += "  \centering\n"
            myOutputLatex += "  \caption{Summary of the number of events from the signal with mass point $\mHpm=%d\GeVcc$ with $\BRtH=%.2f$,\n"%(m,myBr)
            myOutputLatex += "           from the background measurements, and the observed event yield. Luminosity uncertainty is not included in the numbers.}\n"
            myOutputLatex += "  \label{tab:summary:yields}\n"
            myOutputLatex += "  \vskip 0.1 in\n"
            myOutputLatex += "  \hspace*{-.8cm}\n"
            myOutputLatex += "  \begin{tabular}{ l c }\n"
            myOutputLatex += "  \hline\n"
            myOutputLatex += "  \multicolumn{1}{ c }{Source}  & {$N_{\text{events}} \pm \text{stat.} \pm \text{syst.}$}  \\ \n"
            myOutputLatex += "  \hline\n"
            if round(mySignalSystDown) == round(mySignalSystUp):
                myOutputLatex += "  HH+HW, $\mHplus = %d\GeVcc & $%.0f \pm %.0f \pm %0.f $\n"%(m, mySignalRate, mySignalStat, mySignalSystDown)
            else:
                myOutputLatex += "  HH+HW, $\mHplus = %d\GeVcc & $%.0f \pm $%.0f~^{+%.0f}_{%0.f} $\n"%(m, mySignalRate, mySignalStat, mySignalSystUp, mySignalSystDown)
            myOutputLatex += "  \hline\n"
            #QCD background (data-driven)      #FIXME finish latex
            #EWK+\ttbar $\tau$ (data-driven)     
            #EWK+\ttbar $\tau$ fakes (MC)           
            myOutputLatex += "  \hline\n"
            #Total expected from the SM             
            #Data                          
            myOutputLatex += "  \hline\n"
            myOutputLatex += "  \end{tabular}\n"
            myOutputLatex += "  \end{table}\n"
            myOutputLatex += "  \renewcommand{\arraystretch}{1}\n"

            print "Event yield summary for mass %d written to: "%m +myFilename

    ## Prints systematics summary table
    def makeSystematicsSummary(self):
        print "FIXME makeSystematicsSummary"