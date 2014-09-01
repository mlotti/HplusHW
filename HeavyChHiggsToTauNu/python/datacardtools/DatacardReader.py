import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as limitTools
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles as ShellStyles

import os
import ROOT
ROOT.gROOT.SetBatch(True)

_fineBinningSuffix = "_fineBinning"

## Get list of mass points
def getMassPoints(directory="."):
    # Find out the mass points
    mySettings = limitTools.GeneralSettings(directory,[])
    massPoints = mySettings.getMassPoints(limitTools.LimitProcessType.TAUJETS)
    return massPoints

## Get luminosity
def getLuminosity(directory=".", mass=None):
    m = mass
    if mass == None:
        masslist = getMassPoints(directory)
        m = masslist[0]
    myLuminosity = float(limitTools.readLuminosityFromDatacard(directory, mySettings.getDatacardPattern(limitTools.LimitProcessType.TAUJETS)%m))
    return myLuminosity
  
## Class for containing all information related to a single datacard
class DataCardReader:
    def __init__(self, directory, mass):
        # Initialize
        self._directory = directory
        self._mass = mass
        self._rootFilename = None
        self._rootFile = None
        self._datasetNuisances = {} # Dictionary, where key is dataset name and value is list of nuisances (including bin by bin uncert.)
        
        # Read contents
        self._readRootFileContents(directory, mass)
        
    def __del__(self):
        print "Closing file:",self._rootFilename
        self._rootFile.Close()

    def getDatasetNames(self):
        return self._datasetNuisances.keys()

    def getNuisanceNamesByDatasetName(self, datasetName):
        self.hasDatasetByName(datasetName, exceptionOnFail=True)
        return self._datasetNuisances[datasetName]

    def hasDatasetByName(self, datasetName, exceptionOnFail=False):
        if not datasetName in self._datasetNuisances.keys():
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
        name = datasetName
        if fineBinned:
            name += _fineBinningSuffix
        h = self._rootFile.Get(name)
        if h == None:
            if exceptionOnFail:
                raise Exception("Could not find histogram '%s'!"%name)
            return None
        return aux.Clone(h)
    
    def getNuisanceHistos(self, datasetName, nuisanceName, exceptionOnFail=True, fineBinned=False):
        self.datasetHasNuisance(datasetName, nuisanceName, exceptionOnFail=True)
        name = "%s_%s"%(datasetName, nuisanceName)
        if "Bin" in name:
            name = "%s_%s"%(datasetName, name) # bin-by-bin uncert. replicate the dataset name
        if fineBinned:
            name += _fineBinningSuffix
        up = self._rootFile.Get(name+"Up")
        if up == None:
            if exceptionOnFail:
                raise Exception("Could not find histogram '%s'!"%name+"Up")
            return (None, None)
        down = self._rootFile.Get(name+"Down")
        if down == None:
            if exceptionOnFail:
              raise Exception("Could not find histogram '%s'!"%name+"Down")
            return (None, None)
        return (aux.Clone(up), aux.Clone(down))

    def debug(self):
        print "DEBUG info of DataCardReader:"
        names = self.getDatasetNames()
        for n in names:
            print "..  dset=%s has shape nuisances:"%n
            print ".... %s"%", ".join(map(str,self.getNuisanceNamesByDatasetName(n)))
    
    def _readRootFileContents(self, directory, mass):
        mySettings = limitTools.GeneralSettings(directory,[])
        rootFilePattern = mySettings.getRootfilePattern(limitTools.LimitProcessType.TAUJETS)
        self._rootFilename = os.path.join(directory, rootFilePattern%mass)
        print "Opening file:",self._rootFilename
        self._rootFile = ROOT.TFile.Open(self._rootFilename)
        content = self._rootFile.GetListOfKeys()
        # Suppress the warning message of missing dictionary for some iterator
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kError
        diriter = content.MakeIterator()
        ROOT.gErrorIgnoreLevel = backup
        # Find the names of datasets and uncertainties
        myPreviousSplitList = None
        myPreviousDsetName = None
        key = diriter.Next()
        shapeNuisances = []
        while key:
            splitList = key.GetName().split("_")
            if not _fineBinningSuffix in key.GetName():
                if myPreviousSplitList != None:
                    if myPreviousSplitList[0] != splitList[0]:
                        # New dataset column, store list of nuisances
                        if not "data_obs" in myPreviousDsetName and not "res." in myPreviousDsetName:
                            self._datasetNuisances[myPreviousDsetName] = shapeNuisances[:]
                            shapeNuisances = []
                if not key.GetName().endswith("Up") and not key.GetName().endswith("Down") and not "Source" in key.GetName() and not "beforeFit" in key.GetName():
                    myPreviousDsetName = key.GetName()
                if key.GetName().endswith("Up"):
                    myNuisanceName = key.GetName().replace("Up","").replace("%s_"%myPreviousDsetName,"")
                    shapeNuisances.append(myNuisanceName)
                
                # Store old key
                myPreviousSplitList = splitList
            # Advance to next
            key = diriter.Next()
        # Store nuisances for last dataset
        if not "data_obs" in myPreviousDsetName and not "res." in myPreviousDsetName:
            self._datasetNuisances[myPreviousDsetName] = shapeNuisances[:]

def validateDatacards(directory="."):
    def checkItem(testName, booleanTest, failMsg):
        if booleanTest:
            print ".. Test: %s: %sPASSED%s"%(testName, ShellStyles.TestPassedStyle(), ShellStyles.NormalStyle())
        else:
            print ".. Test: %s: %sFAILED%s"%(testName, ShellStyles.ErrorStyle(), ShellStyles.NormalStyle())
            print failMsg
            raise Exception()
        return 1
  
    nTests = 0
    nMassPoints = 0
    print "\n%sValidating datacards in directory: %s%s"%(ShellStyles.HighlightStyle(),directory,ShellStyles.NormalStyle())
    massPoints = getMassPoints(directory)
    if len(massPoints) == 0:
        raise Exception ("No datacards found in directory '.'!"%directory)
    for m in massPoints:
        nMassPoints += 1
        print "%sConsidering mass: %s%s"%(ShellStyles.HighlightStyle(),m,ShellStyles.NormalStyle())
        reader = DataCardReader(directory, m)
        for dset in reader.getDatasetNames():
            hRate = reader.getRateHisto(dset)
            myNuisanceNames = reader.getNuisanceNamesByDatasetName(dset)
            # Check integral of fine binned and non-fine binned histogram
            hRateFine = reader.getRateHisto(dset, fineBinned=True, exceptionOnFail=False)
            if hRateFine != None and not "QCD" in dset: # for QCD there can be a difference because negative rate bins are forced to zero in rate histo
                nTests += checkItem("(%s) Nominal rate vs. fine binned rate "%dset, 
                          abs(hRate.Integral() / hRateFine.Integral()-1.0) < 0.0000001,
                          "Nominal rate = %f, fine binned rate = %f"%(hRate.Integral(), hRateFine.Integral()))
            else:
                print "   (skipping test for Nominal rate vs. fine binned rate)"
            # Check if rate is negative
            for i in range(1,hRate.GetNbinsX()+1):
                nTests += checkItem("(%s) rate >= 0 for bin %d"%(dset,i), hRate.GetBinContent(i) >= 0.0, "")
            # Check bin-by-bin nuisances
            if not "NoFitUncert" in directory and not "noSystUncert" in directory:
                for i in range(1,hRate.GetNbinsX()+1):
                    myNames = []
                    for n in myNuisanceNames:
                        if n.endswith("Bin%d"%i):
                            myNames.append(n)
                    # Check existence of bin-by-bin uncert.
                    nTests += checkItem("(%s) has at least one bin-by-bin uncert. for bin %d"%(dset,i), len(myNames) > 0, "")
                    nTests += checkItem("(%s) has exactly one bin-by-bin uncert. for bin %d"%(dset, i), len(myNames) == 1, "found nuisances: %s"%", ".join(map(str,myNames)))
                    (up,down) = reader.getNuisanceHistos(dset, myNames[0])
                    rate = hRate.GetBinContent(i)
                    if (rate < 0.000001):
                        # Check if zero rate bins are treated properly
                        nTests += checkItem("(%s) rate=0 and bin-by-bin uncert. (%s) up != 0 for bin %d"%(dset,myNames[0],i), up.GetBinContent(i) > 0.000001, "You need to a non-zero value for the up uncert. in this case!")
                    else:
                        # Check that non-zero bins are no have a proper treatment
                        nTests += checkItem("(%s) rate>0 and bin-by-bin uncert. (%s) up != rate for bin %d"%(dset,myNames[0],i), abs(rate-up.GetBinContent(i)) > 0.000001, "Sounds like a bug")
                        nTests += checkItem("(%s) rate>0 and bin-by-bin uncert. (%s) down != rate for bin %d"%(dset,myNames[0],i), abs(rate-down.GetBinContent(i)) > 0.000001, "Sounds like a bug")
    return (nTests, nMassPoints)
