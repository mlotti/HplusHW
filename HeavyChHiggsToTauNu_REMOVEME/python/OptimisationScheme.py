import FWCore.ParameterSet.Config as cms
import sys
import ctypes
import copy

from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addAnalysis

class Scenario:
    def __init__(self, *args, **kwargs):
        if len(args) != 1:
            raise Exception("You must give exactly one positional argument for the scenario name, got %d" % len(args))
        self._name = args[0]
        self._data = copy.deepcopy(kwargs)

    def applyToPSet(self, pset):
        for key, value in self._data.iteritems():
            setattr(pset, key, value)

    def __str__(self):
        return self._name

class OptimisationItem:
    def __init__(self, name, variationList, attributeToChange, formatString):
        # Initialize
        self._name = name
        self._variationList = []
        if isinstance(variationList, list):
            self._variationList.extend(variationList)
        else:
            self._variationList.append(variationList)
        self._attributeToChange = attributeToChange
        self._formatString = formatString

    def getNumberOfVariations(self):
        return len(self._variationList)

    def getSuffixForName(self, idx):
        return self._formatString%self._variationList[idx]

    def setVariation(self, module, idx):
        def deepgetattr(obj, attr):
            #Recurses through an attribute chain to get the ultimate value.
            return reduce(getattr, attr.split('.'), obj)

        def deepsetattr(obj, attr, value):
            #Recurses through an attribute chain to set the ultimate value.
            if len(attr.split(".")) > 1:
                deepsetattr(getattr(obj, attr.split(".")[0]), attr[attr.find(".")+1:], value)
            else:
                if hasattr(value, "applyToPSet"):
                    value.applyToPSet(getattr(obj, attr))
                else:
                    setattr(obj, attr, value)

        if self.isDirectionalParameter():
            # separate direction and digit (operators are "GT","GEQ","NEQ","EQ","LT","LEQ")
            myDirection = ""
            myDigit = 0
            if self._variationList[idx][2].isdigit():
                myDirection = self._variationList[idx][:1]
                myDigit = int(self._variationList[idx][2:])
            else:
                myDirection = self._variationList[idx][:2]
                myDigit = int(self._variationList[idx][3:])
            deepsetattr(module, self._attributeToChange, myDigit)
            deepsetattr(module, self._attributeToChange+"CutDirection", myDirection)
        else:
            #print "value is: %s"%deepgetattr(module, self._attributeToChange)
            deepsetattr(module, self._attributeToChange, self._variationList[idx]) # FIXME
            #print "test: new attribute is: %s"%deepgetattr(module, self._attributeToChange)

    def isDirectionalParameter(self):
        # (operators are "GT","GEQ","NEQ","EQ","LT","LEQ")
        if "EQ" in self._attributeToChange:
            return True
        if "LT" in self._attributeToChange:
            return True
        if "GT" in self._attributeToChange:
            return True
        return False

    def printLabelAndValues(self):
        print "  %s: [%s]"%(self._name, (', '.join(map(str, self._variationList))))

## Class for generating variations to the analysis for optimisation
class HPlusOptimisationScheme:
    ## Constructor
    def __init__(self):
        # initialise internal variables
        self._variationItems = []

    def addTauPtVariation(self, values):
        self._variationItems.append(OptimisationItem("tau pT", values, "tauSelection.ptCut", "Taupt%.0f"))

    def addTauIsolationVariation(self, values):
        self._variationItems.append(OptimisationItem("tau isolation", values, "tauSelection.isolationDiscriminator", "Tau%s"))

    def addRtauVariation(self, values):
        self._variationItems.append(OptimisationItem("tau Rtau cut", values, "tauSelection.rtauCut", "Rtau%.1f"))

    def addTauVariations(self, scenarios):
        self._variationItems.append(OptimisationItem("tau", scenarios, "tauSelection", "Tau%s"))

    def addJetNumberSelectionVariation(self, values):
        self._variationItems.append(OptimisationItem("jet Njets", values, "jetSelection.jetNumber", "Jets%s"))

    def addJetEtVariation(self, values):
        self._variationItems.append(OptimisationItem("jet pT", values, "jetSelection.ptCut", "Jetpt%d"))

    def addJetVariations(self, scenarios):
        self._variationItems.append(OptimisationItem("jet", scenarios, "jetSelection", "Jets%s"))

    def addMETSelectionVariation(self, values):
        self._variationItems.append(OptimisationItem("MET", values, "MET.METCut", "MET%.0f"))

    def addMETVariations(self, scenarios):
        self._variationItems.append(OptimisationItem("MET", scenarios, "MET", "MET%s"))

    def addBJetLeadingDiscriminatorVariation(self, values):
        self._variationItems.append(OptimisationItem("btag discriminator", values, "bTagging.leadingDiscriminatorCut", "Bdiscr%.1f"))

    def addBJetSubLeadingDiscriminatorVariation(self, values):
        self._variationItems.append(OptimisationItem("btag subleading discriminator", values, "bTagging.subleadingDiscriminatorCut", "Bsubdiscr%.1f"))

    def addBJetNumberVariation(self, values):
        self._variationItems.append(OptimisationItem("btag Njets", values, "bTagging.jetNumber", "Bjets%d"))

    def addBJetEtVariation(self, values):
        self._variationItems.append(OptimisationItem("btag pT", values, "bTagging.ptCut", "BpT%.0f"))

    def addBTagVariations(self, scenarios):
        self._variationItems.append(OptimisationItem("btag", scenarios, "bTagging", "Btag%s"))

    def addTopRecoVariation(self, values):
        self._variationItems.append(OptimisationItem("top reco algorithm", values, "topReconstruction", "Top%s"))

    def addInvariantMassVariation(self, scenarios):
        self._variationItems.append(OptimisationItem("invariant mass algorithm", scenarios, "invMassReco", "InvMassReco%s"))

    def printOptimisationConfig(self, analysisName):
        print "Optimisation configuration for module %s:"%analysisName
        if len(self._variationItems) == 0:
            print "  No optimisation variations!"
            return
        for item in self._variationItems:
            item.printLabelAndValues()

    def printOptions(self):
        print "Implemented variation options in OptimisationScheme.py:"
        for item in dir(self):
            if "add" in item:
                print "  ",item
        sys.exit()

    def createVariationModule(self, idxlist, nominalAnalysis):
        myModule = nominalAnalysis.clone()
        for i in range(0, len(self._variationItems)):
            self._variationItems[i].setVariation(myModule, idxlist[i])
        return myModule

    def getVariationName(self, analysisName, idxlist):
        myName = "%sOpt"%analysisName
        for i in range(0, len(self._variationItems)):
            myName += "%s"%self._variationItems[i].getSuffixForName(idxlist[i])
        return myName.replace(".","")

    def doVariation(self, depth, idxlist, process, additionalCounters, commonSequence, nominalAnalysis, analysisName):
        myModuleNames = []
        if depth == len(idxlist):
            # Top reached, create module
            myVariationName = self.getVariationName(analysisName, idxlist)
            addAnalysis(process,
                        myVariationName,
                        self.createVariationModule(idxlist, nominalAnalysis),
                        preSequence=commonSequence,
                        additionalCounters=additionalCounters,
                        signalAnalysisCounters=True)
            myModuleNames.append(myVariationName)
            #print "Added module:",myVariationName
        else:
            for i in range(0, self._variationItems[depth].getNumberOfVariations()):
                # Enter recursion
                idxlist[depth] = i
                myModuleNames.extend(self.doVariation(depth+1, idxlist, process, additionalCounters, commonSequence, nominalAnalysis, analysisName))
        return myModuleNames

    def generateVariations(self, process, additionalCounters, commonSequence, nominalAnalysis, analysisName):
        #self.printOptions()
        # Print info
        self.printOptimisationConfig(analysisName)
        # loop over variations
        idxlist = []
        for item in self._variationItems:
            idxlist.append(0)
        variationModuleNames = self.doVariation(0, idxlist, process, additionalCounters, commonSequence, nominalAnalysis, analysisName)
        #if self._maxVariations > 0:
            #if nVariations > self._maxVariations:
                #print "You generated %d variations, which is more than the safety limit (%d)!"%(nVariations,self._maxVariations)
                #print "To remove the safety switch (if you REALLY know what you are doing), call disableMaxVariations()"
                #sys.exit()
        print "Added %d variations to the analysis"%len(variationModuleNames)
        return variationModuleNames
