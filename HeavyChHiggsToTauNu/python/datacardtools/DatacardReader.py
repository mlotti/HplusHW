#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as limitTools
#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles as ShellStyles

import os
import math
import array
import ROOT
ROOT.gROOT.SetBatch(True)

def Clone(obj, *args):
    cl = obj.Clone(*args)
    ROOT.SetOwnership(cl, True)
    if hasattr(cl, "SetDirectory"):
        cl.SetDirectory(0)
    return cl

_fineBinningSuffix = "_fineBinning"
_originalDatacardDirectory = "originalDatacards"

### Get list of mass points
#def getMassPoints(directory="."):
    ## Find out the mass points
    #mySettings = limitTools.GeneralSettings(directory,[])
    #massPoints = mySettings.getMassPoints(limitTools.LimitProcessType.TAUJETS)
    #return massPoints

### Get luminosity
#def getLuminosity(directory=".", mass=None):
    #m = mass
    #if mass == None:
        #masslist = getMassPoints(directory)
        #m = masslist[0]
    #myLuminosity = float(limitTools.readLuminosityFromDatacard(directory, mySettings.getDatacardPattern(limitTools.LimitProcessType.TAUJETS)%m))
    #return myLuminosity

#mySettings = limitTools.GeneralSettings(directory,[])
#rootFilePattern = mySettings.getRootfilePattern(limitTools.LimitProcessType.TAUJETS)

def getMassPointsForDatacardPattern(directory, datacardFilePattern, massPoints = []):
    # Find datacard files
    myList = os.listdir(directory)
    mySplit = datacardFilePattern.split("%s")
    masses = []
    for item in myList:
        myStatus = True
        myStub = item
        for part in mySplit:
            myStub = myStub.replace(part,"")
            if not part in item:
                myStatus = False
        if myStatus:
            masses.append(myStub)
    if len(masses) > 0:
        masses.sort()

    if len(massPoints) > 0:
        mlist = massPoints[:]
        if len(masses) > 0:
            i = 0
            while i < len(mlist) and len(mlist) > 0:
                if not mlist[i] in masses:
                    mlist.remove(mlist[i])
                else:
                    i += 1
        return mlist
    return masses

class DataCardDirectoryManager:
    def __init__(self, directory, datacardFilePattern, rootFilePattern, rootFileDirectory="", readOnly=False, outSuffix=None):
        self._datacards = {} # Dictionary, where key is mass and value is DataCardReader object for that mass point
        if '%' in datacardFilePattern:
            self._massPoints = getMassPointsForDatacardPattern(directory, datacardFilePattern)
            # initialize datacard objects
            print "Found mass points:",self._massPoints
            for m in self._massPoints:
                self._datacards[m] = DataCardReader(directory, m, datacardFilePattern, rootFilePattern, rootFileDirectory=rootFileDirectory, readOnly=readOnly, outSuffix=outSuffix)
        else:
           self._massPoints = None
           # initialize datacard objects
           print "Assuming a control datacard"
           self._datacards["CR"] = DataCardReader(directory, None, datacardFilePattern, rootFilePattern, rootFileDirectory=rootFileDirectory, readOnly=readOnly, outSuffix=outSuffix)
        # check integrity
        #self.checkIntegrity()

    def close(self):
        for key in self._datacards.keys():
            self._datacards[key].close()

    def getColumnNames(self):
        if len(self._datacards.keys()) > 0:
            return self._datacards[self._datacards.keys()[0]].getDatasetNames()
        return []

    def replaceColumnNames(self, replaceDictionary):
        print "datacards: replacing column names"
        for m in self._datacards.keys():
            self._datacards[m].replaceColumnNames(replaceDictionary)
    
    def replaceNuisanceNames(self, replaceDictionary):
        print "datacards: replacing nuisance names"
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Do replace in txt file
            for item in replaceDictionary.keys():
                for i in range(0,len(dcard._datasetNuisances)):
                    if dcard._datasetNuisances[i]["name"] == item:
                        dcard._datasetNuisances[i]["name"] = dcard._datasetNuisances[i]["name"].replace(item, replaceDictionary[item])
            # Do Replace in root file
            for item in replaceDictionary.keys():
                myList = dcard.getRootFileObjectsWithPattern(item)
                # Loop over root objects
                for objectName in myList:
                    o = self._datacards[m].getRootFileObject(objectName)
                    if "_"+item+"Up" in o.GetName() or "_"+item+"Down" in o.GetName():
                        o.SetName(o.GetName().replace(item, replaceDictionary[item]))

    def removeStatUncert(self, signalOnly=False):
        for m in self._datacards.keys():
            self._datacards[m].removeStatUncert(signalOnly)

    def recreateShapeStatUncert(self, signalOnly=False, threshold=0.001):
        print "datacards: recreating shape stat. uncert. entries and histograms"
        for m in self._datacards.keys():
            self._datacards[m].recreateShapeStatUncert(signalOnly, threshold)

    ## This method is for testing the effect of zero bins for the background
    def smoothBackgroundByLinearExtrapolation(self, column):
        print "datacards: smoothening background '%s' with linear extrapolation"%column
        for m in self._datacards.keys():
            self._datacards[m].smoothBackgroundByLinearExtrapolation(column)

    def removeColumn(self, name):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Loop over nuisances
            i = 0
            while i < len(dcard._datasetNuisances):
                if name in dcard._datasetNuisances[i].keys():
                    del dcard._datasetNuisances[i][name]
                i += 1
            # Loop over histograms
            i = 0
            while i < len(dcard._hCache):
                hName = dcard._hCache[i].GetName()
                if hName == name or hName.startswith(name+"_"):
                    del dcard._hCache[i]
                else:
                    i += 1
            # Remove column from lists
            i = 0
            while i < len(dcard._datacardColumnNames):
                if dcard._datacardColumnNames[i] == name:
                    del dcard._datacardColumnNames[i]
                    del dcard._rateValues[i]
                else:
                    i += 1

    def addNuisance(self, name, distribution, columns, value):
        for m in self._datacards.keys():
            self._datacards[m].addNuisance(name, distribution, columns, value)

    def removeNuisance(self, name):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Remove histograms
            i = 0
            while i < len(dcard._hCache):
                if "_"+name+"Up" in dcard._hCache[i].GetName() or "_"+name+"Down" in dcard._hCache[i].GetName():
                    dcard._hCache[i].Delete()
                    dcard._hCache.remove(dcard._hCache[i])
                else:
                    i += 1
            # Remove nuisances
            i = 0
            while i < len(dcard._datasetNuisances):
                if dcard._datasetNuisances[i]["name"] == name:
                    del dcard._datasetNuisances[i]
                else:
                    i += 1
                    
    def removeManyNuisances(self, nameList):
        if nameList == None:
            return
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            for n in nameList:
                if n == "*":
                    # Remove all
                    while len(dcard._datasetNuisances) > 0:
                        self.removeNuisance(dcard._datasetNuisances[i]["name"])
                elif "*" in n:
                    # Find wildcarded nuisances
                    mySplit = n.split("*")
                    if len(mySplit) > 2:
                        raise Exception("only one wild card supported")
                    i = 0
                    while i < len(dcard._datasetNuisances):
                        name = dcard._datasetNuisances[i]["name"]
                        if name.startswith(mySplit[0]) and name.endswith(mySplit[1]):
                            self.removeNuisance(name)
                        else:
                            i += 1
                else:
                    self.removeNuisance(n)
                
    def keepManyNuisances(self, nameList):
        if nameList == None:
            return
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            myKeepList = []
            for n in nameList:
                if n == "*":
                    # Remove all
                    i = 0
                    while i < len(dcard._datasetNuisances):
                        myKeepList.append(dcard._datasetNuisances[i]["name"])
                        i += 1
                elif "*" in n:
                    # Find wildcarded nuisances
                    mySplit = n.split("*")
                    if len(mySplit) > 2:
                        raise Exception("only one wild card supported")
                    i = 0
                    while i < len(dcard._datasetNuisances):
                        name = dcard._datasetNuisances[i]["name"]
                        if name.startswith(mySplit[0]) and name.endswith(mySplit[1]):
                            myKeepList.append(name)
                        i += 1
                else:
                    myKeepList.append(n)
            # Obtain remove list
            myRemoveList = []
            for n in dcard._datasetNuisances:
                if not n["name"] in myKeepList:
                    myRemoveList.append(n["name"])
            # Remove items on remove list
            for n in myRemoveList:
                self.removeNuisance(n)

    def replaceNuisanceValue(self, name, newValue, columns=[]):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            myColumns = []
            if isinstance(columns, list):
                myColumns.extend(columns)
            elif isinstance(columns, str):
                myColumns.append(columns)
            else:
                raise Exception("should not happen")
            if len(myColumns) == 0:
                myColumns = dcard.getDatasetNames()
            for i in range(0,len(dcard._datasetNuisances)):
                if dcard._datasetNuisances[i]["name"] == name:
                    if dcard._datasetNuisances[i]["distribution"] == "shape":
                        raise Exception("Error: replaceNuisanceValue works only for normalization nuisances; '%s' is a shape nuisance!"%name)
                    for k in myColumns:
                        if k in dcard.getDatasetNames():
                            dcard._datasetNuisances[i][k] = newValue
                        #else:
                        #    print k

    def convertShapeToNormalizationNuisance(self, nameList, columnList=[]):
        for m in self._datacards.keys():
            self._datacards[m].convertShapeToNormalizationNuisance(nameList, columnList)
    
    def mergeShapeNuisances(self, namesList, newName):
        if len(namesList) < 2:
            raise Exception("Error: mergeShapeNuisances needs at least two nuisance names for the merge!")
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Look for first item
            targetIndex = None
            for i in range(0,len(dcard._datasetNuisances)):
                if dcard._datasetNuisances[i]["name"] == namesList[0]:
                    if dcard._datasetNuisances[i]["distribution"] != "shape":
                        raise Exception("Error: mergeShapeNuisances: nuisance '%s' is not a shape nuisance!"%namesList[0])
                    targetIndex = i
            # Do merge
            for item in namesList[1:]:
                for i in range(0,len(dcard._datasetNuisances)):
                    if dcard._datasetNuisances[i]["name"] == item:
                        if dcard._datasetNuisances[i]["distribution"] != "shape":
                            raise Exception("Error: mergeShapeNuisances: nuisance '%s' is not a shape nuisance!"%item)
                        # Update nuisance histograms and datacard nuisance lines
                        for c in dcard.getDatasetNames():
                            if dcard._datasetNuisances[i][c] == "1":
                                if dcard._datasetNuisances[targetIndex][c] == "1":
                                    # Add histogram contents
                                    myTargetList = dcard.getRootFileObjectsWithPattern("%s_%s"%(c, dcard._datasetNuisances[targetIndex]["name"]))
                                    mySourceList = dcard.getRootFileObjectsWithPattern("%s_%s"%(c, dcard._datasetNuisances[i]["name"]))
                                    myRateHisto = dcard.getRateHisto(c)
                                    if len(myTargetList) != len(mySourceList):
                                        raise Exception("This should not happen")
                                    for h in range(0, len(myTargetList)):
                                        if myTargetList[h].startswith(c):
                                            hTarget = dcard.getRootFileObject(myTargetList[h])
                                            hSource = dcard.getRootFileObject(mySourceList[h])
                                            for k in range(1, hTarget.GetNbinsX()+1):
                                                myOffset = myRateHisto.GetBinContent(k)
                                                myVariation = (hTarget.GetBinContent(k) - myOffset)**2
                                                myVariation += (hSource.GetBinContent(k) - myOffset)**2
                                                #print c, hTarget.GetBinContent(k), hSource.GetBinContent(k), myOffset, math.sqrt(myVariation), math.sqrt(myVariation)+myOffset, myOffset-math.sqrt(myVariation)
                                                if mySourceList[h].endswith("Up"):
                                                    hTarget.SetBinContent(k, math.sqrt(myVariation)+myOffset)
                                                elif mySourceList[h].endswith("Down"):
                                                    hTarget.SetBinContent(k, myOffset-math.sqrt(myVariation))
                                else:
                                    # Update nuisance line
                                    dcard._datasetNuisances[i][c] = "1"
                                    # Copy histogram
                                    mySourceList = dcard.getRootFileObjectsWithPattern("%s_%s"%(c, dcard._datasetNuisances[i]["name"]))
                                    for h in mySourceList:
                                        hSource = dcard.getRootFileObject(h)
                                        if hSource.GetName().endswith("Up"):
                                            hnew = Clone(hSource, "%s_%sUp"%(c, dcard._datasetNuisances[i]["name"]))
                                            dcard._hCache.append(hnew)
                                        elif hSource.GetName().endswith("Down"):
                                            hnew = Clone(hSource, "%s_%sDown"%(c, dcard._datasetNuisances[i]["name"]))
                                            dcard._hCache.append(hnew)
        # Rename
        myDict = {namesList[0]: newName}
        self.replaceNuisanceNames(myDict)
        # Remove items
        for item in namesList[1:]:
            self.removeNuisance(item)

    ## This method subtracts a systematic shift from the shape
    def subtractPedestalFromShapeNuisances(self, target):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Look for target nuisance (for determining which columns are affected)
            myTargetNuisance = None
            for i in range(0,len(dcard._datasetNuisances)):
                if dcard._datasetNuisances[i]["name"] == target:
                    myTargetNuisance = dcard._datasetNuisances[i]
            if myTargetNuisance == None:
                raise Exception("Error: Could not find target nuisance '%s'!"%target)
            if myTargetNuisance["distribution"] != "shape":
                raise Exception("Error: Target is not a shape nuisance!")
            # Loop over columns
            for c in dcard.getDatasetNames():
                if myTargetNuisance[c] == "1":
                    # Find target histograms
                    hTargetUp = dcard.getRootFileObject("%s_%sUp"%(c,target))
                    hTargetDown = dcard.getRootFileObject("%s_%sDown"%(c,target))
                    hNominal = dcard.getRateHisto(c)
                    # Do correction
                    for h in [hTargetUp, hTargetDown]:
                        for k in range(1, hTargetUp.GetNbinsX()+1):
                            myDelta = (hTargetUp.GetBinContent(k) + hTargetDown.GetBinContent(k)) / 2.0 - hNominal.GetBinContent(k)
                            #print hTargetUp.GetBinContent(k), hTargetDown.GetBinContent(k), hNominal.GetBinContent(k), "delta=", myDelta
                            hTargetUp.SetBinContent(k, hTargetUp.GetBinContent(k) - myDelta)
                            hTargetDown.SetBinContent(k, hTargetDown.GetBinContent(k) - myDelta)
                            #print "after:",hTargetUp.GetBinContent(k), hTargetDown.GetBinContent(k)
                    myNominalRate = hNominal.Integral()
                    #print "... Pedestal correction applied to shape '%s': new nuisance up: %f down: %f"%(target, hTargetUp.Integral() / myNominalRate, hTargetDown.Integral() / myNominalRate)

    ## Set minimum stat. uncert. for bins with zero rate or very small rate
    def fixTooSmallStatUncertProblem(self, signalMinimumAbsStatValue, bkgMinimumAbsStatValue, signalOnly=False):
        print "datacards: Checking for and fixing if stat. uncert. is too small"
        for m in self._datacards.keys():
            self._datacards[m].fixTooSmallStatUncertProblem(signalMinimumAbsStatValue, bkgMinimumAbsStatValue, signalOnly)

    ## Rebins the shape histograms (assumes that only shape variations are used)
    def rebinShapes(self, rebinList):
        print "datacards: Rebinning shapes"
        for m in self._datacards.keys():
            self._datacards[m].rebinShapes(rebinList)

    ## Checks if the root file background and observation items are the same between the datacards
    def checkIntegrity(self):
        if len(self._datacards.keys()) == 0:
            return
        refCard = self._datacards[self._datacards.keys()[0]]
        cardList = self._datacards.keys()[1:]
        for testCardKey in cardList:
            print "Integrity check, test: m%s ref: m%s"%(self._datacards.keys()[0], testCardKey)
            testCard = self._datacards[testCardKey]
            # Compare root objects
            nHistos = len(refCard._hCache)
            for i in range(nHistos):
                refName = refCard._hCache[i].GetName()
                testName = testCard._hCache[i].GetName()
                if refName == testName:
                    nbins = refCard._hCache[i].GetNbinsX()
                    for k in range(1, nbins+1):
                        if abs(refCard._hCache[i].GetBinContent(k) - testCard._hCache[i].GetBinContent(k)) > 0.00000001:
                            if not (testName.startswith("%s_"%testCard.getDatasetNames()[0]) or testName == testCard.getDatasetNames()[0]):
                                print "  bin %d mismatch: test %s %f vs. ref %s %f"%(k, testName, testCard._hCache[i].GetBinContent(k), refName, refCard._hCache[i].GetBinContent(k))
                        else:
                            if testName.startswith("%s_"%testCard.getDatasetNames()[0]) or testName == testCard.getDatasetNames()[0]:
                                if refCard._hCache[i].GetBinContent(k) > 0:
                                    print "  signal bin %d is the same: test %s %f vs. ref %s %f"%(k, testName, testCard._hCache[i].GetBinContent(k), refName, refCard._hCache[i].GetBinContent(k))
                else:
                    if not refName.startswith(refCard.getDatasetNames()[0]):
                        print "  Name mismatch:",refName, testName
            # Compare nuisances
            nNuisances = len(refCard._datasetNuisances)
            for i in range(nNuisances):
                for c in testCard.getDatasetNames()[1:]:
                    if c in refCard._datasetNuisances[i].keys():
                        if refCard._datasetNuisances[i][c] != testCard._datasetNuisances[i][c]:
                            print "  nuisance %s / column %s mismatch: test %s vs. ref. %s"%(refCard._datasetNuisances[i]["name"], c, testCard._datasetNuisances[i][c], refCard._datasetNuisances[i][c])
        print "Integrity test passed"

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

## Class for containing all information related to a single datacard
class DataCardReader:
    def __init__(self, directory, mass, datacardFilePattern, rootFilePattern, rootFileDirectory="", readOnly=True, silent=True, outSuffix=None):
        # Initialize
        self._directory = directory
        self._mass = mass
        self._datacardFilePattern = datacardFilePattern
        self._rootFilePattern = rootFilePattern
        self._rootFileDirectory = rootFileDirectory
        self._readOnly = readOnly
        self._outSuffix = outSuffix
        self._rootFilename = None
        self._datacardFilename = None
        self._hCache = [] # Cache for persistent histograms
        # DatacardInfo
        self._datacardColumnNames = [] # List of columns in datacard
        self._datacardBinName = None
        self._datacardColumnStartIndex = None # Index of first column
        self._datacardHeaderLines = []
        self._observationValue = None
        self._rateValues = {} # Dictionary, where key is dataset name and value is a string of the rate value
        self._datasetNuisances = [] # List of dictionaries, where key is nuisance name
        
        self._silentStatus = silent

        # Read contents
        self._readDatacardContents(directory, mass)
        if rootFilePattern != None:
            self._readRootFileContents(directory, mass)
        
    def close(self):

        if not self._silentStatus:
            print "Writing datacard:",self._datacardFilename
        self._writeDatacardContents()

        if self._rootFilePattern == None:
            return
        if not self._silentStatus:
            print "Closing file:",self._rootFilename
        self._writeRootFileContents()

    def getDatasetNames(self):
        return self._datacardColumnNames

    def getRateValue(self, column):
        return self._rateValues[column]

    #def getNuisanceNamesByDatasetName(self, datasetName):
        #self.hasDatasetByName(datasetName, exceptionOnFail=True)
        #return self._datasetNuisances[datasetName]

    def hasDatasetByName(self, datasetName, exceptionOnFail=False):
        if not datasetName in self._datacardColumnNames:
            if exceptionOnFail:
                raise Exception("Dataset '%s' not found!"%datasetName)
            return False
        return True

    def datasetHasNuisance(self, datasetName, nuisanceName, exceptionOnFail=False):
        self.hasDatasetByName(datasetName)
        if not nuisanceName in self._datasetNuisances[datasetName]:
            if exceptionOnFail:
                raise Exception("Dataset '%s' does not have nuisance '%s'!"%(datasetName,nuisanceName))
            return False
        return True
      
    def getRateHisto(self, datasetName, fineBinned=False, exceptionOnFail=True):
        self.hasDatasetByName(datasetName, exceptionOnFail=True)
        name = self.getHistoNameForColumn(datasetName)
        if fineBinned:
            name += _fineBinningSuffix
        for item in self._hCache:
            if item.GetName() == name:
                return item # no clone should be returned
        # Not found, strip directory
        s = name.split("/")
        shortName = s[len(s)-1]
        for item in self._hCache:
            if item.GetName() == shortName:
                return item # no clone should be returned
        if exceptionOnFail:
            raise Exception("Could not find histogram '%s'!"%name)
        return None
    
    def getNuisanceNames(self, datasetName):
        l = []
        for n in self._datasetNuisances:
            if datasetName not in n.keys():
                raise Exception("Error '%s' not found in datasets!"%datasetName)
            if n[datasetName] != "-":
                l.append(n["name"])
        return l
    
    def getShapeNuisanceNames(self, datasetName):
        l = []
        for n in self._datasetNuisances:
            if datasetName not in n.keys():
                raise Exception("Error '%s' not found in datasets!"%datasetName)
            if n["distribution"] == "shape":
                if n[datasetName] == "1":
                    l.append(n["name"])
        return l
    
    def getNuisanceHistos(self, datasetName, nuisanceName, exceptionOnFail=True, fineBinned=False):
        self.datasetHasNuisance(datasetName, nuisanceName, exceptionOnFail=True)
        name = self.getHistoNameForNuisance(datasetName, nuisanceName)
        if "Bin" in name:
            name = "%s_%s"%(datasetName, name) # bin-by-bin uncert. replicate the dataset name
        if fineBinned:
            name += _fineBinningSuffix
        up = None
        down = None
        for item in self._hCache:
            if item.GetName == name+"Up":
                up = item
            elif item.GetName == name+"Down":
                down = item
        if up == None and down == None:
            # Not found, strip directory
            s = name.split("/")
            shortName = s[len(s)-1]
            for item in self._hCache:
                if item.GetName() == shortName:
                    if item.GetName == shortName+"Up":
                        up = item
                    elif item.GetName == shortName+"Down":
                        down = item    
        if up == None:
            if exceptionOnFail:
                raise Exception("Could not find histogram '%s'!"%name+"Up")
            return (None, None)
        if down == None:
            if exceptionOnFail:
              raise Exception("Could not find histogram '%s'!"%name+"Down")
            return (None, None)
        return (up, down) # no clone should be returned

    def debug(self):
        print "DEBUG info of DataCardReader:"
        names = self.getDatasetNames()
        #for n in names:
            #print "..  dset=%s has shape nuisances:"%n
            #print ".... %s"%", ".join(map(str,self.getNuisanceNamesByDatasetName(n)))
    
    def addNuisance(self, name, distribution, columns, value):
        myDict = None
        for n in self._datasetNuisances:
            if n["name"] == name:
                myDict = n
        if myDict == None:
            myDict = {}
            myDict["name"] = name
            myDict["distribution"] = distribution
            self._datasetNuisances.append(myDict)
        for c in self.getDatasetNames():
            if c in columns:
                myDict[c] = value
            else:
                #if c not in myDict.keys():
                #print c, name
                myDict[c] = "-"
    
    def scaleSignal(self, value):
        if self._datacardColumnStartIndex >= 1:
            # No signal column
            return
        signalColumn = self._datacardColumnNames[0]
        # Update rate
        a = float(self._rateValues[signalColumn])*value
        self._rateValues[signalColumn] = "%.6f"%a
        # Update rate and nuisance histograms
        # Note: both need to be scaled 
        if self._rootFilePattern == None:
            return
        olist = self.getRootFileObjectsWithPattern(signalColumn)
        hRate = self.getRateHisto(signalColumn)
        hOriginalRate = Clone(hRate)
        hRate.Scale(value)
        for oname in olist:
            if oname.startswith(signalColumn+"_"): # Do not apply twice to rate histogram
                h = self.getRootFileObject(oname)
                deltaOriginal = None
                deltaOriginal = h.Integral() / hOriginalRate.Integral()
                backup = ROOT.gErrorIgnoreLevel
                ROOT.gErrorIgnoreLevel = ROOT.kError # suppress complaints about different bin labels
                h.Add(hOriginalRate, -1.0)
                h.Scale(value)
                h.Add(hRate, 1.0)
                ROOT.gErrorIgnoreLevel = backup
                deltaNew = h.Integral() / hRate.Integral()
                if abs(deltaOriginal-deltaNew) > 0.0001:
                    print "Something is wrong, the rel. uncertainty is not concerved: %f->%f!"%(deltaOriginal, deltaNew)

    def addHistogram(self, h):
        self._hCache.append(Clone(h))

    def convertShapeToNormalizationNuisance(self, nameList, columnList=[]):
        myList = []
        if isinstance(nameList, str):
            myList.append(nameList)
        elif isinstance(nameList, list):
            myList.extend(nameList)
        myAffectedColumns = columnList[:]
        if len(myAffectedColumns) == 0:
            myAffectedColumns.extend(self.getDatasetNames())
        for item in myList:
            for i in range(0,len(self._datasetNuisances)):
                if self._datasetNuisances[i]["name"] == item:
                    hasShapesStatus = False
                    for c in self.getDatasetNames():
                        if self._datasetNuisances[i][c] == "1":
                            if c in myAffectedColumns:
                                # Find histograms
                                hup = self.getRootFileObject("%s_%sUp"%(c, self._datasetNuisances[i]["name"]))
                                hdown = self.getRootFileObject("%s_%sDown"%(c, self._datasetNuisances[i]["name"]))
                                hRate = self.getRateHisto(c)
                                # Calculate nuisance value by integrating
                                myNominalRate = hRate.Integral()
                                myMinus = hdown.Integral()/myNominalRate
                                myPlus = hup.Integral()/myNominalRate
                                s = ""
                                if abs(myMinus-myPlus) > 0.0005:
                                    s = "%.3f/%.3f"%(myMinus, myPlus)
                                else:
                                    s = "%.3f"%(myPlus)
                                # Remove histograms
                                self._hCache.remove(hup)
                                self._hCache.remove(hdown)
                                hup.Delete()
                                hdown.Delete()
                                # Replace value for column in datacard
                                self._datasetNuisances[i][c] = s
                            else:
                                hasShapesStatus = True
                    if hasShapesStatus:
                        self._datasetNuisances[i]["distribution"] = "shape?"
                    else:
                        self._datasetNuisances[i]["distribution"] = "lnN"

    def replaceColumnNames(self, replaceDictionary):
        # Do replace in txt file
        for item in replaceDictionary.keys():
            for i in range(0,len(self.getDatasetNames())):
                if self._datacardColumnNames[i] == item:
                    self._datacardColumnNames[i] = replaceDictionary[item]
            for i in range(0,len(self._datasetNuisances)):
                if item in self._datasetNuisances[i].keys():
                    self._datasetNuisances[i][replaceDictionary[item]] = self._datasetNuisances[i][item]
                    del self._datasetNuisances[i][item]
                if self._datasetNuisances[i]["name"].startswith(item):
                    name = replaceDictionary[item]+self._datasetNuisances[i]["name"][len(item):]
                    self._datasetNuisances[i]["name"] = name
        # Do replace in header lines of datacard file
        for i in range(len(self._datacardHeaderLines)):
            s = self._datacardHeaderLines[i].split()
            if s[0] == "shapes":
                for item in replaceDictionary.keys():
                    if s[1] == item:
                        s[1] = replaceDictionary[item]
                        self._datacardHeaderLines[i] = " ".join(map(str, s))+"\n"
        # Do replace in root file
        if self._rootFilePattern != None:
            for item in replaceDictionary.keys():
                myList = self.getRootFileObjectsWithPattern(item)
                # Loop over root objects
                for objectName in myList:
                    o = self.getRootFileObject(objectName)
                    if self.getHistoNameForColumn(item) == objectName:
                        # Rate
                        o.SetName(self.getHistoNameForColumn(replaceDictionary[item]))
                    else:
                        # Shape nuisances (no stat)
                        for i in range(0,len(self._datasetNuisances)):
                            name = self.getHistoNameForNuisance(item, self._datasetNuisances[i]["name"])
                            if objectName.startswith(item):
                                newName = replaceDictionary[item]+objectName[len(item):]
                                #new2 = objectName.replace(self.getHistoNameForNuisance(item, self._datasetNuisances[i]["name"]),self.getHistoNameForNuisance(replaceDictionary[item], self._datasetNuisances[i]["name"]))
                                #if item == "ttbb":
                                #    print "***",objectName, "***", newName, "***", new2
                                o.SetName(newName)
                        # stat nuisance FIXME: it seems that this does not work in all cases
                        #if "%s_%s"%(item,item) in objectName:
                            #name = objectName.replace(self.getHistoNameForNuisance(item, item),self.getHistoNameForNuisance(replaceDictionary[item], replaceDictionary[item]))
                            #o.SetName(name)
                                
                    #if objectName.startswith(self.getHistoNameForNuisance(item,"")):
                        #s = item+"_"+item+"_"
                        #name = "%s_%s_"%(replaceDictionary[item],replaceDictionary[item])+o.GetName()[len(s):]
                        #o.SetName(name)
                    #elif objectName.startswith(item+"_"):
                        #name = replaceDictionary[item]+o.GetName()[len(item):]
                        #o.SetName(name)
        # Do replace in data structures
        for item in replaceDictionary.keys():
            for key in self._rateValues.keys():
                if item == key:
                    self._rateValues[replaceDictionary[item]] = self._rateValues[key]
                    del self._rateValues[key]
            #for histoItem in self._hCache:
                #if histoItem.GetName().startswith(item):
                    #histoItem.SetName(replaceDictionary[item]+histoItem.GetName()[len(item):])
    
    def removeStatUncert(self, signalOnly=False):
        # Remove previous entries from datacard
        i = 0
        while i < len(self._datasetNuisances):
            nuisanceName = self._datasetNuisances[i]["name"]
            myStatus = True
            if signalOnly:
                myStatus = self._datacardColumnNames[0] in nuisanceName
            if myStatus and "stat" in nuisanceName or "Stat" in nuisanceName:
                self._datasetNuisances.remove(self._datasetNuisances[i])
            else:
                i += 1
        # Remove previous histograms from datacard
        i = 0
        while i < len(self._hCache):
            histoName = self._hCache[i].GetName()
            myStatus = True
            if signalOnly:
                myStatus = self._datacardColumnNames[0] in histoName
            if myStatus and "stat" in histoName or "Stat" in histoName:
                self._hCache[i].Delete()
                self._hCache.remove(self._hCache[i])
            else:
                i += 1

    def recreateShapeStatUncert(self, signalOnly=False, threshold=0.001):
        # Remove previous entries from datacard
        self.removeStatUncert(signalOnly)
        # Loop over columns and
        for c in self.getDatasetNames():
            myStatus = True
            if signalOnly:
                myStatus = self._datacardColumnNames[0] == c
            if myStatus:
                hRate = self.getRateHisto(c)
                # Loop over bins in rate
                for nbin in range(1, hRate.GetNbinsX()+1):
                    # Check for overlapping bin-by-bin stat. uncertainties
                    myList = self.getRootFileObjectsWithPattern(c)
                    if not ("bin%s"%nbin in myList or "Bin%s"%nbin in myList):
                        myRelUncert = 0.0
                        if hRate.GetBinContent(nbin) > 0.0:
                            myRelUncert = abs(hRate.GetBinError(nbin) / hRate.GetBinContent(nbin))
                        myStatus = False
                        if threshold == None:
                            myStatus = True
                        elif myRelUncert > threshold:
                            myStatus = True
                        #else:
                        #    print "... skipping",c,nbin,myRelUncert
                        if myStatus:
                            # Add entries to datacard
                            myDict = {}
                            myDict["name"] = "%s_statBin%d"%(c, nbin)
                            myDict["distribution"] = "shape"
                            for cc in self.getDatasetNames():
                                if cc == c:
                                    myDict[cc] = "1"
                                else:
                                    myDict[cc] = "-"
                            self._datasetNuisances.append(myDict)
                            # Add histograms
                            hUp = Clone(hRate)
                            hDown = Clone(hRate)
                            s = self.getHistoNameForNuisance(c, "%s_statBin%dUp"%(c, nbin)).split("/")
                            hUp.SetName(s[len(s)-1])
                            s = self.getHistoNameForNuisance(c, "%s_statBin%dDown"%(c, nbin)).split("/")
                            hDown.SetName(s[len(s)-1])
                            hUp.SetBinContent(nbin, hUp.GetBinContent(nbin)+hUp.GetBinError(nbin))
                            myMinValue = max(hDown.GetBinContent(nbin)-hDown.GetBinError(nbin), 0.0)
                            hDown.SetBinContent(nbin, myMinValue)
                            for k in range(1, hRate.GetNbinsX()+1):
                                hUp.SetBinError(k, 0.0)
                                hDown.SetBinError(k, 0.0)
                            self.addHistogram(hUp)
                            self.addHistogram(hDown)
    
    ## This method is for testing the effect of zero bins for the background
    def smoothBackgroundByLinearExtrapolation(self, column):
        myFoundStatus = False
        datasetIndex = 0
        for c in self.getDatasetNames():
            if c == column:
                myFoundStatus = True
                hRate = self.getRateHisto(c)
                # Obtain list of non-zero bins
                binList = []
                for k in range(1, hRate.GetNbinsX()+1):
                    if abs(hRate.GetBinContent(k)) > 0.0000001:
                        binList.append(k)
                # Add last bin
                if hRate.GetNbinsX() not in binList:
                    binList.append(hRate.GetNbinsX())
                # Tweak to see if the tail matters
                #hRate.SetBinContent(hRate.GetNbinsX(), 10.0)
                # Interpolate
                for i in range(len(binList)-1):
                    # y = ax + b, parametrize content
                    adenom = float(hRate.GetXaxis().GetBinCenter(binList[i+1])) - float(hRate.GetXaxis().GetBinCenter(binList[i]))
                    anum = hRate.GetBinContent(binList[i+1]) - hRate.GetBinContent(binList[i])
                    a = 0.0
                    if abs(adenom) > 0.0000001:
                        a = anum / adenom
                    b = hRate.GetBinContent(binList[i+1]) - float(hRate.GetXaxis().GetBinCenter(binList[i+1])) * a
                    for k in range(binList[i]+1,binList[i+1]):
                        hRate.SetBinContent(k, a*hRate.GetXaxis().GetBinCenter(k) + b)
                    # parametrize uncertainty (linear interpolation also here)
                    anum = hRate.GetBinError(binList[i+1]) - hRate.GetBinError(binList[i])
                    a = 0.0
                    if abs(adenom) > 0.0000001:
                        a = anum / adenom
                    b = hRate.GetBinError(binList[i+1]) - float(hRate.GetXaxis().GetBinCenter(binList[i+1])) * a
                    for k in range(binList[i]+1,binList[i+1]):
                        hRate.SetBinError(k, a*hRate.GetXaxis().GetBinCenter(k) + b)
                # Update rate number in table
                print "sample yield changed %s -> %f"%(self._rateValues[datasetIndex], hRate.Integral())
                self._rateValues[datasetIndex] = "%f"%hRate.Integral()
            datasetIndex += 1
        if not myFoundStatus:
            raise Exception("Error: cannot find background '%s'!"%column)
    
    def fixTooSmallStatUncertProblem(self, signalMinimumAbsStatValue, bkgMinimumAbsStatValue, signalOnly=False):
        # Loop over columns
        for c in self.getDatasetNames():
            myStatus = True
            if signalOnly:
                myStatus = self._datacardColumnNames[0] == c
            if myStatus:
                # Find min value by background
                minValue = 0
                if c == self.getDatasetNames()[0]:
                    minValue = signalMinimumAbsStatValue
                else:
                    for k in bkgMinimumAbsStatValue.keys():
                        if k == c:
                            minValue = bkgMinimumAbsStatValue[k]
                # Loop over rate histogram
                hRate = self.getRateHisto(c)
                for k in range(1, hRate.GetNbinsX()+1):
                    a = hRate.GetBinContent(k)
                    #print c,k,a,hRate.GetBinError(k), minValue
                    if abs(a) < minValue or hRate.GetBinError(k) < minValue:
                        hRate.SetBinError(k, minValue)
    
    def _readRootFileContents(self, directory, mass):
        if mass != None:
            self._rootFilename = os.path.join(directory, self._rootFilePattern%mass)
        else:
            self._rootFilename = os.path.join(directory, self._rootFilePattern)
            
        # Make backup of original cards
        if not self._readOnly:
            if not os.path.exists(_originalDatacardDirectory):
                os.mkdir(_originalDatacardDirectory)
            if not os.path.exists(os.path.join(_originalDatacardDirectory,self._rootFilename)):
                os.system("cp %s %s/."%(os.path.join(directory,self._rootFilename), _originalDatacardDirectory))
            else:
                os.system("cp %s ."%(os.path.join(_originalDatacardDirectory,self._rootFilename)))
        # Open file
        if not self._silentStatus:
            print "Opening file:",self._rootFilename
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kError
        f = ROOT.TFile.Open(self._rootFilename)
        ROOT.gErrorIgnoreLevel = backup
        if f == None:
            raise Exception("Error opening file '%s'!"%self._rootFilename)
        #f.Cd(self._rootFileDirectory)
        # Read histograms to cache
        myHistoNames = []
        for c in self._datacardColumnNames:
            #s = self.getHistoNameForColumn(c).split("/")
            #myHistoNames.append(s[len(s)-1])
            myHistoNames.append(self.getHistoNameForColumn(c))
            for n in self._datasetNuisances:
                s = self.getHistoNameForNuisance(c, n["name"]).split("/")
                myTemplate = s[len(s)-1]
                #myTemplate = self.getHistoNameForNuisance(c, n["name"])
                if n["distribution"] == "shape" and n[c] == "1":
                    myHistoNames.append(myTemplate+"Up")
                    myHistoNames.append(myTemplate+"Down")
        myDir = f.GetDirectory(self._rootFileDirectory)
        klist = myDir.GetListOfKeys()
        #for k in klist:
            #print k.GetName()
        #print "***"
        #print myHistoNames
        #print self._rootFileDirectory
        for name in myHistoNames:
            s = name.split("/")
            realName = s[len(s)-1]
            k = klist.FindObject(realName)
            if k == None:
                raise Exception("Error: cannot find histo '%s' in root file '%s'!"%(name, self._rootFilename))
            o = k.ReadObj()
            o.SetName(k.GetName()) # The key has the correct name, but the histogram name might be something else
            #print k.GetName()
            self._hCache.append(Clone(o))
        # Add also histogram for observation
        myDataName = self.getHistoNameForData()
        k = klist.FindObject(myDataName)
        if k == None:
            raise Exception("Error: cannot find histo '%s' in root file '%s'!"%(name, myDataName))
        o = k.ReadObj()
        o.SetName(k.GetName()) # The key has the correct name, but the histogram name might be something else
        #print k.GetName()
        self._hCache.append(Clone(o))
        f.Close()
        
        if not self._silentStatus:
            # Print stat.uncert.
            for c in self._datacardColumnNames:
                hRate = self.getRateHisto(c)
                myTotalUp = 0.0
                myTotal = 0.0
                for nbin in range(1, hRate.GetNbinsX()+1):
                    myTotalUp += hRate.GetBinError(nbin)**2
                    myTotal += hRate.GetBinContent(nbin)
                print "  %s / m%s: stat.uncert.: %f"%(c, self._mass, math.sqrt(myTotalUp)/myTotal)

    def getHistoNameForData(self):
        return self._datacardShapeDataTemplate.replace("$CHANNEL",self._datacardBinName)

    def getHistoNameForColumn(self, columnName):
        if self._datacardShapeColumnTemplate == None:
            raise Exception()
        return self._datacardShapeColumnTemplate.replace("$PROCESS",columnName).replace("$CHANNEL",self._datacardBinName)
    
    def getHistoNameForNuisance(self, columnName, nuisanceName):
        if self._datacardShapeNuisanceTemplate == None:
            raise Exception()
        return self._datacardShapeNuisanceTemplate.replace("$PROCESS",columnName).replace("$CHANNEL",self._datacardBinName).replace("$SYSTEMATIC",nuisanceName)
    
    def _writeRootFileContents(self):
        if self._readOnly:
            return
        myFilename = self._rootFilename
        if self._outSuffix != None:
            myFilename = myFilename.replace(".root","_%s.root"%self._outSuffix)
        if len(self._rootFileDirectory) > 0:
            myFilename = myFilename.replace(".root","_%s.root"%self._rootFileDirectory)
        f = ROOT.TFile.Open(myFilename, "RECREATE")
        if f == None:
            raise Exception("Error opening file '%s'!"%self._rootFilename)
        for h in self._hCache:
            h.SetDirectory(f)
            #print h.GetName()
        f.Write()
        f.Close()
        self._hCache = []

    def getRootFileObjectsWithPattern(self, pattern):
        myOutList = []
        for item in self._hCache:
            if pattern in item.GetName():
                myOutList.append(item.GetName())
        return myOutList

    def getRootFileObject(self, objectName):
        for item in self._hCache:
            if item.GetName() == objectName:
                return item
        for item in self._hCache:
            print item.GetName()
        print self._datacardColumnNames
        raise Exception("Error: Cannot find root object '%s' in root file '%s'!"%(objectName, self._rootFilename))

    def _readDatacardContents(self, directory, mass):
        if mass != None and "%s" in self._datacardFilePattern:
            self._datacardFilename = os.path.join(directory, self._datacardFilePattern%mass)
        else:
            self._datacardFilename = os.path.join(directory, self._datacardFilePattern)
        # Make backup of original cards
        if not self._readOnly:
            if not os.path.exists(_originalDatacardDirectory):
                os.mkdir(_originalDatacardDirectory)
            if not os.path.exists(os.path.join(_originalDatacardDirectory,self._datacardFilename)):
                os.system("cp %s %s/."%(os.path.join(directory,self._datacardFilename), _originalDatacardDirectory))
            else:
                os.system("cp %s ."%(os.path.join(_originalDatacardDirectory,self._datacardFilename)))
        # Obtain datacard
        myOriginalCardFile = open(self._datacardFilename)
        myOriginalCardLines = myOriginalCardFile.readlines()
        myOriginalCardFile.close()
        # Parse datacard contents
        self._parseDatacardHeader(myOriginalCardLines)
        self._parseDatacardColumnNames(myOriginalCardLines)
        self._parseDatacardNuisanceNames(myOriginalCardLines)
        #print self._datacardHeaderLines
        #print self._observationValue
        #print self._rateValues
        #print self._datasetNuisances
    
    def _writeDatacardContents(self):
        if self._readOnly:
            return
        
        # Determine order of columns (sort them descending by count)
        mySortList = []
        for i in range(len(self._datacardColumnNames)):
            if i <= -self._datacardColumnStartIndex:
                mySortList.append((i, 100000000-i))
            else:
                mySortList.append((i, float(self._rateValues[self._datacardColumnNames[i]])))
        mySortList.sort(key=lambda x: x[1], reverse=True)
        myOutput = ""
        myObservedLine = ""
        # Create header
        for l in self._datacardHeaderLines:
            mySplit = l.split()
            if mySplit[0] == "observation":
                myOutput += "observation    %s\n"%self._observationValue
            elif "%s/"%self._rootFileDirectory in l:
                myOutput += l.replace("%s/"%self._rootFileDirectory,"").replace(".root","_%s.root"%self._rootFileDirectory)
            else:
                myOutput += l
        # Create process lines
        myProcessTable = []
        myLine = ["bin",""]
        for c in self._datacardColumnNames:
            myLine.append(self._datacardBinName)
        myProcessTable.append(myLine)
        myProcessLine = ["process",""]
        for i in range(len(self._datacardColumnNames)):
            myProcessLine.append(self._datacardColumnNames[mySortList[i][0]])
        myProcessTable.append(myProcessLine)
        myLine = ["process",""]
        for i in range(0, len(self._datacardColumnNames)):
            myLine.append("%d"%(self._datacardColumnStartIndex+i))
        myProcessTable.append(myLine)
        # Create rate table
        myRateTable = []
        myLine = ["rate",""]
        for i in range(len(self._datacardColumnNames)):
            myLine.append(self._rateValues[self._datacardColumnNames[mySortList[i][0]]])
        myRateTable.append(myLine)
        # Create nuisance table
        myNuisanceTable = []
        myStatTable = []
        for n in self._datasetNuisances:
            myRow = []
            # add first two entries
            myRow.append(n["name"])
            myRow.append(n["distribution"])
            # add data from columns
            for c in myProcessLine[2:]:
                myRow.append(n[c])
            # store
            if "stat" in n["name"] or "Stat" in n["name"]:
                myStatTable.append(myRow)
            else:
                myNuisanceTable.append(myRow)
        
        # Create stat.uncert. table
        
        # Do formatting
        myWidths = []
        for c in self._datacardColumnNames:
            myWidths.append(0)
        calculateCellWidths(myWidths, myProcessTable)
        calculateCellWidths(myWidths, myRateTable)
        calculateCellWidths(myWidths, myNuisanceTable)
        calculateCellWidths(myWidths, myStatTable)
        for i in range(0,len(myWidths)):
            if myWidths[i] < 9:
                myWidths[i] = 9
        mySeparatorLine = getSeparatorLine(myWidths)
        # Add tables to output
        myOutput += getTableOutput(myWidths, myProcessTable)
        myOutput += mySeparatorLine
        myOutput += getTableOutput(myWidths, myRateTable)
        myOutput += mySeparatorLine
        myOutput += getTableOutput(myWidths, myNuisanceTable)
        myOutput += mySeparatorLine
        myOutput += getTableOutput(myWidths, myStatTable)
        myOutput += mySeparatorLine
        # Save
        myOriginalCardFile = open(self._datacardFilename, "w")
        myOriginalCardFile.write(myOutput)
        myOriginalCardFile.close()

    ## Parse header from datacard file
    def _parseDatacardHeader(self, lines):
        self._dataObsName = None
        self._datacardBinName = None
        self._datacardShapeDataTemplate = "data_obs"
        self._datacardShapeColumnTemplate = None
        self._datacardShapeNuisanceTemplate = None
        self._datacardHeaderLines = []
        for l in lines:
            mySplit = l.split()
            if mySplit[0] == "bin":
                if self._dataObsName == None:
                    self._dataObsName  = mySplit[1]
                elif self._datacardBinName == None:
                    self._datacardBinName = mySplit[1]
            if mySplit[0] == "process":
                del self._datacardHeaderLines[len(self._datacardHeaderLines)-1]
                return
            if mySplit[0] == "shapes":
                if len(mySplit) == 5:
                    if mySplit[1] == "data_obs":
                        self._datacardShapeDataTemplate = mySplit[4]
                if len(mySplit) == 6:
                    self._datacardShapeColumnTemplate = mySplit[4]
                    self._datacardShapeNuisanceTemplate = mySplit[5]
            # Store header line
            if mySplit[0] == "shapes":
                # Remove path from root file
                s = mySplit[3].split("/")
                mySplit[3] = s[len(s)-1]
                # Add suffix to fle
                if self._outSuffix != None:
                    mySplit[3] = mySplit[3].replace(".root", "_%s.root"%self._outSuffix)
                if self._rootFilePattern != None:
                    self._datacardHeaderLines.append(" ".join(map(str,mySplit))+"\n")
            elif mySplit[0] == "jmax":
                # Set number of backgrounds to auto-detect
                mySplit[1] = "*"
                self._datacardHeaderLines.append(" ".join(map(str,mySplit))+"\n")
            elif mySplit[0] == "kmax":
                # Set number of nuisance parameters to auto-detect
                mySplit[1] = "*"
                self._datacardHeaderLines.append(" ".join(map(str,mySplit))+"\n")
            else:
                self._datacardHeaderLines.append(l)
        raise Exception("This line should never be reached")
    
    ## Parse column names from datacard file
    def _parseDatacardColumnNames(self, lines):
        for i in range(0, len(lines)):
            mySplit = lines[i].split()
            if mySplit[0] == "process":
                self._datacardColumnNames = mySplit[1:]
                mySplitNext = lines[i+1].split()
                if mySplitNext[0] != "process":
                    raise Exception("Failed to find two consecutive rows starting with 'process'!")
                self._datacardColumnStartIndex = int(mySplitNext[1])
                #print self._datacardColumnStartIndex
                return
        raise Exception("This line should never be reached")

    ## Parse info of nuisances from datacard file
    def _parseDatacardNuisanceNames(self, lines):
        if len(self._datacardColumnNames) == 0:
            raise Exception("No column names found in datacard!")
        myNames = []
        myRateLinePassedStatus = False
        for l in lines:
            if l != "\n":
                mySplit = l.split()
                if myRateLinePassedStatus and len(mySplit) > 1:# and not "statBin" in mySplit[0]:
                    # store nuisance
                    myDict = {}
                    myDict["name"] = mySplit[0]
                    myDict["distribution"] = mySplit[1]
                    for i in range(0,len(self._datacardColumnNames)):
                        myDict[self._datacardColumnNames[i]] = mySplit[i+2]
                    # Ignore stat. uncertainty
                    #if not myDict["name"].endswith("stat"):
                    self._datasetNuisances.append(myDict)
                if len(mySplit[0]) > 3:
                    if mySplit[0] == "observation":
                    # store observation
                        self._observationValue = mySplit[1]
                    if mySplit[0] == "rate":
                        # store rate
                        for i in range(1,len(mySplit)):
                            self._rateValues[self._datacardColumnNames[i-1]] = mySplit[i]
                        myRateLinePassedStatus = True
        if len(self._datasetNuisances) == 0:
            raise Exception("No nuisances found!")

    ## Rebins the shape histograms (assumes that only shape variations are used)
    def rebinShapes(self, rebinList):
        # Check that bin edges make sense
        for h in self._hCache:
            for i in range(len(rebinList)-1):
                myFoundStatus = False
                k = 0
                while not myFoundStatus and k < h.GetNbinsX():
                    if h.GetXaxis().GetBinLowEdge(k+1) == rebinList[i]:
                        myFoundStatus = True
                    k += 1
                if not myFoundStatus:
                    l = []
                    for k in range(h.GetNbinsX()):
                        l.append("%f"%h.GetXaxis().GetBinLowEdge(k+1))
                    print "Histogram (%s) binning: %s"%(h.GetName(), ", ".join(map(str, l)))
                    raise Exception("Error: specified rebin edge (%f) is not found in the bin low edges!"%rebinList[i])
        # Rebin
        hlist = []
        for h in self._hCache:
            myArray = array.array("d",rebinList)
            hnew = h.Rebin(len(rebinList)-1,h.GetName(),myArray)
            h.Delete()
            hlist.append(hnew)
        # Store
        self._hCache = hlist[:]

    ## Add signal from another datacard (usecase: combination of inclusive signals for tan beta limits)
    def addSignal(self, reader):
        def getNuisanceDictIndex(nuisanceDictList, nuisanceName):
            for i in range(len(nuisanceDictList)):
                if nuisanceDictList[i]["name"] == nuisanceName:
                    return i
            raise Exception("Error: could not find nuisance by name %s"%nuisanceName)
      
        if self._datacardColumnStartIndex != 0 or reader._datacardColumnStartIndex != 0:
            raise Exception("Multiple signals/datacard use case is not supported for this method")

        # Find source and target column name and rate
        sourceColumnName = reader._datacardColumnNames[0]
        sourceRate = None
        for i in range(len(reader._datacardColumnNames)):
            if reader._datacardColumnNames[i] == sourceColumnName:
                sourceRate = float(reader._rateValues[reader._datacardColumnNames[i]])
        targetColumnName = self._datacardColumnNames[0]
        targetRate = None
        targetRateIndex = None
        for i in range(len(self._datacardColumnNames)):
            if self._datacardColumnNames[i] == targetColumnName:
                targetRate = float(self._rateValues[self._datacardColumnNames[i]])
                targetRateIndex = i
        # Find source and target nuisance names and shape nuisance names
        sourceNuisances = reader.getNuisanceNames(sourceColumnName)
        sourceShapeNuisances = reader.getShapeNuisanceNames(sourceColumnName)
        targetNuisances = self.getNuisanceNames(targetColumnName)
        targetShapeNuisances = self.getShapeNuisanceNames(targetColumnName)
        #print "target:",targetNuisances
        #print "source:",sourceNuisances
        # Update rate value (signal only)
        self._rateValues[self._datacardColumnNames[targetRateIndex]] = "%.6f"%(sourceRate+targetRate)
        # Update shape nuisance histograms (signal only)
        for sourceShapeName in sourceShapeNuisances:
            if not "statBin" in sourceShapeName and not sourceShapeName.endswith("_stat"):
                myFoundStatus = False
                for targetShapeName in targetShapeNuisances:
                    #if sourceShapeName.replace(sourceColumnName,"") == targetShapeName.replace(targetColumnName,""):
                    if sourceShapeName == targetShapeName:
                        myFoundStatus = True
                        for suffix in ["Up", "Down"]:
                            mySourceHistoName = "%s_%s%s"%(sourceColumnName, sourceShapeName, suffix)
                            myTargetHistoName = "%s_%s%s"%(targetColumnName, targetShapeName, suffix)
                            self.getRootFileObject(myTargetHistoName).Add(reader.getRootFileObject(mySourceHistoName))
                if not myFoundStatus:
                    # here one must add a new nuisance with the source histogram + target rate histogram 
                    mySourceHistoName = "%s%s"%(sourceShapeName, suffix)
                    h = reader.getRootFileObject(mySourceHistoName)
                    h.Add(self.getRootFileObject(targetColumnName))
                    self.addHistogram(h)
                    # that was the easy part, now one should add the the nuisance to the nuisance table
                    raise Exception("operation not supported at the moment")
        for targetShapeName in targetShapeNuisances:
            if not "statBin" in targetShapeName and not targetShapeName.endswith("_stat"):
                myFoundStatus = False
                for sourceShapeName in sourceShapeNuisances:
                    if sourceShapeName == targetShapeName:
                        myFoundStatus = True
                if not myFoundStatus:
                    # here one must add the rate histogram of source to target
                    for suffix in ["Up", "Down"]:
                        myTargetHistoName = "%s%s"%(targetShapeName, suffix)
                        self.getRootFileObject(myTargetHistoName).Add(reader.getRootFileObject(sourceColumnName))
        # Update rate histogram (signal only); must be done after shape nuisance histo update
        self.getRootFileObject(targetColumnName).Add(reader.getRootFileObject(sourceColumnName))
        # Add normalization nuisances (signal only)
        for sourceName in sourceNuisances:
            if not "statBin" in sourceName and not sourceShapeName.endswith("_stat") and not sourceName in sourceShapeNuisances:
                myFoundStatus = False
                for targetName in targetNuisances:
                    if sourceName == targetName:
                        myFoundStatus = True
                        sourceIndex = getNuisanceDictIndex(reader._datasetNuisances, sourceName)
                        targetIndex = getNuisanceDictIndex(self._datasetNuisances, targetName)
                        sourceValueList = reader._datasetNuisances[sourceIndex][sourceColumnName].split("/")
                        targetValueList = self._datasetNuisances[targetIndex][targetColumnName].split("/")
                        if len(sourceValueList) != len(targetValueList):
                            if len(sourceValueList) == 1:
                                sourceValueList.append(sourceValueList[0])
                            if len(targetValueList) == 1:
                                targetValueList.append(targetValueList[0])
                        result = ""
                        for i in range(len(sourceValueList)):
                            # Calculate in absolute uncertainty
                            a = (float(sourceValueList[i]) - 1.0) * sourceRate
                            b = (float(targetValueList[i]) - 1.0) * targetRate
                            #newRelUncert = math.sqrt(a**2+b**2) / (sourceRate + targetRate)
                            newRelUncert = (a+b) / (sourceRate + targetRate)
                            if result != "":
                                result += "/"
                            result += "%.3f"%(1.0+newRelUncert)
                        self._datasetNuisances[targetIndex][targetColumnName] = result
                if not myFoundStatus:
                    raise Exception("operation not supported at the moment (%s/%s was not found in source)"%(sourceColumnName,sourceName))
        for targetName in targetNuisances:
            if not "statBin" in targetName and not targetShapeName.endswith("_stat") and not targetName in targetShapeNuisances:
                myFoundStatus = False
                for sourceName in sourceNuisances:
                    if sourceName == targetName:
                        myFoundStatus = True
                if not myFoundStatus:
                    raise Exception("operation not supported at the moment (%s/%s missing from target)"%(targetColumnName,targetName))
        # Combine column names (signal only)
        myReplaceDict = {}
        myReplaceDict[targetColumnName] = "%s_and_%s"%(targetColumnName, sourceColumnName.replace("CMS_",""))
        self.replaceColumnNames(myReplaceDict)
        # Redo stat.uncertainties (signal only)
        self.fixTooSmallStatUncertProblem(signalMinimumAbsStatValue=0.3, bkgMinimumAbsStatValue=0.0, signalOnly=True)
        self.recreateShapeStatUncert(signalOnly=True)

#def validateDatacards(directory="."):
    #def checkItem(testName, booleanTest, failMsg):
        #if booleanTest:
            #print ".. Test: %s: %sPASSED%s"%(testName, ShellStyles.TestPassedStyle(), ShellStyles.NormalStyle())
        #else:
            #print ".. Test: %s: %sFAILED%s"%(testName, ShellStyles.ErrorStyle(), ShellStyles.NormalStyle())
            #print failMsg
            #raise Exception()
        #return 1
  
    #nTests = 0
    #nMassPoints = 0
    #print "\n%sValidating datacards in directory: %s%s"%(ShellStyles.HighlightStyle(),directory,ShellStyles.NormalStyle())
    #massPoints = getMassPoints(directory)
    #if len(massPoints) == 0:
        #raise Exception ("No datacards found in directory '.'!"%directory)
    #for m in massPoints:
        #nMassPoints += 1
        #print "%sConsidering mass: %s%s"%(ShellStyles.HighlightStyle(),m,ShellStyles.NormalStyle())
        #reader = DataCardReader(directory, m)
        #for dset in reader.getDatasetNames():
            #hRate = reader.getRateHisto(dset)
            #myNuisanceNames = reader.getNuisanceNamesByDatasetName(dset)
            ## Check integral of fine binned and non-fine binned histogram
            #hRateFine = reader.getRateHisto(dset, fineBinned=True, exceptionOnFail=False)
            #if hRateFine != None and not "QCD" in dset: # for QCD there can be a difference because negative rate bins are forced to zero in rate histo
                #nTests += checkItem("(%s) Nominal rate vs. fine binned rate "%dset, 
                          #abs(hRate.Integral() / hRateFine.Integral()-1.0) < 0.0000001,
                          #"Nominal rate = %f, fine binned rate = %f"%(hRate.Integral(), hRateFine.Integral()))
            #else:
                #print "   (skipping test for Nominal rate vs. fine binned rate)"
            ## Check if rate is negative
            #for i in range(1,hRate.GetNbinsX()+1):
                #nTests += checkItem("(%s) rate >= 0 for bin %d"%(dset,i), hRate.GetBinContent(i) >= 0.0, "")
            ## Check bin-by-bin nuisances
            #if not "NoFitUncert" in directory and not "noSystUncert" in directory:
                #for i in range(1,hRate.GetNbinsX()+1):
                    #myNames = []
                    #for n in myNuisanceNames:
                        #if n.endswith("Bin%d"%i):
                            #myNames.append(n)
                    ## Check existence of bin-by-bin uncert.
                    #nTests += checkItem("(%s) has at least one bin-by-bin uncert. for bin %d"%(dset,i), len(myNames) > 0, "")
                    #nTests += checkItem("(%s) has exactly one bin-by-bin uncert. for bin %d"%(dset, i), len(myNames) == 1, "found nuisances: %s"%", ".join(map(str,myNames)))
                    #(up,down) = reader.getNuisanceHistos(dset, myNames[0])
                    #rate = hRate.GetBinContent(i)
                    #if (rate < 0.000001):
                        ## Check if zero rate bins are treated properly
                        #nTests += checkItem("(%s) rate=0 and bin-by-bin uncert. (%s) up != 0 for bin %d"%(dset,myNames[0],i), up.GetBinContent(i) > 0.000001, "You need to a non-zero value for the up uncert. in this case!")
                    #else:
                        ## Check that non-zero bins are no have a proper treatment
                        #nTests += checkItem("(%s) rate>0 and bin-by-bin uncert. (%s) up != rate for bin %d"%(dset,myNames[0],i), abs(rate-up.GetBinContent(i)) > 0.000001, "Sounds like a bug")
                        #nTests += checkItem("(%s) rate>0 and bin-by-bin uncert. (%s) down != rate for bin %d"%(dset,myNames[0],i), abs(rate-down.GetBinContent(i)) > 0.000001, "Sounds like a bug")
    #return (nTests, nMassPoints)
