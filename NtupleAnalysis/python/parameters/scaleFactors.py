from HiggsAnalysis.NtupleAnalysis.main import PSet
import json
import os

# This file contains all the scale factors and their uncertainties used in the analysis
# There are two types of scale factors:
#   1) simple scale factors (such as fake tau uncertainty)
#   2) scale factors as function of some variable (such as b tag uncertainties)
# Both are supplied as config parameters, but the type (2) SF's are accessed 
# via GenericScaleFactor c++ class, which causes some naming scheme rules


##===== Tau misidentification (simple SF)
# \param tauSelectionPset  the tau config PSet
# \param partonFakingTau   "eToTau", "muToTau", "jetToTau"
# \param etaRegion         "barrel", "endcap"
# \param direction         "nominal, "up", "down"
def assignTauMisidentificationSF(tauSelectionPset, partonFakingTau, etaRegion, direction):
    if not etaRegion in ["barrel", "endcap", "full"]:
        raise Exception("Error: unknown option for eta region('%s')!"%etaRegion)
    if not direction in ["nominal", "up", "down"]:
        raise Exception("Error: unknown option for direction('%s')!"%direction)
    dirNumber = 0
    if direction == "up":
        dirNumber = 1
    elif direction == "down":
        dirNumber = -1
    if partonFakingTau == "eToTau":
        _assignEToTauSF(tauSelectionPset, etaRegion, dirNumber)
    elif partonFakingTau == "muToTau":
        _assignMuToTauSF(tauSelectionPset, etaRegion, dirNumber)
    elif partonFakingTau == "jetToTau":
        _assignJetToTauSF(tauSelectionPset, etaRegion, dirNumber)
    else:
        raise Exception("Error: unknown option for parton faking tau ('%s')!"%partonFakingTau)
    
def _assignEToTauSF(tauSelectionPset, etaRegion, dirNumber):
    if etaRegion == "barrel":
        tauSelectionPset.tauMisidetificationEToTauBarrelSF = 1.0 + dirNumber*0.20
    elif etaRegion == "endcap":
        tauSelectionPset.tauMisidetificationEToTauEndcapSF = 1.0 + dirNumber*0.20
    elif etaRegion == "full":
        tauSelectionPset.tauMisidetificationEToTauSF = 1.0 + dirNumber*0.20

def _assignMuToTauSF(tauSelectionPset, etaRegion, dirNumber):
    if etaRegion == "barrel":
        tauSelectionPset.tauMisidetificationMuToTauBarrelSF = 1.0 + dirNumber*0.30
    elif etaRegion == "endcap":
        tauSelectionPset.tauMisidetificationMuToTauEndcapSF = 1.0 + dirNumber*0.30
    elif etaRegion == "full":
        tauSelectionPset.tauMisidetificationMuToTauSF = 1.0 + dirNumber*0.30

def _assignJetToTauSF(tauSelectionPset, etaRegion, dirNumber):
    if etaRegion == "barrel":
        tauSelectionPset.tauMisidetificationJetToTauBarrelSF = 1.0 + dirNumber*0.20
    elif etaRegion == "endcap":
        tauSelectionPset.tauMisidetificationJetToTauEndcapSF = 1.0 + dirNumber*0.20
    elif etaRegion == "full":
        tauSelectionPset.tauMisidetificationJetToTauSF = 1.0 + dirNumber*0.20

##===== tau trigger SF (SF as function of pT)
# \param tauSelectionPset  the tau config PSet
# \param direction         "nominal, "up", "down"
# \param variationType     "MC", "data"  (the uncertainty in MC and data are variated separately)
def assignTauTriggerSF(tauSelectionPset, direction, variationType="MC"):
    # FIXME: there is no mechanic right now to choose correct era / run range
    # FIXME: this approach works as long as there is just one efficiency for the simulated samples
    reader = TriggerSFJsonReader("2015D", "runs_256629_260627", "tauLegTriggerEfficiency2015.json")
    result = reader.getResult()
    if variationType == "MC":
        _assignSF(result["binEdges"], result["SF"], result["mcup"], result["mcdown"], tauSelectionPset, direction)
    elif variationType == "data":
        _assignSF(result["binEdges"], result["SF"], result["dataup"], result["datadown"], tauSelectionPset, direction)
    else:
        raise Exception("Error: Unsupported variation type '%s'! Valid options are: 'MC', 'data'"%variationType)

##===== MET trigger SF


##===== Btag SF 


## Helper function
def _assignSF(binEdges, SF, SFup, SFdown, pset, direction):
    if not direction in ["nominal", "up", "down"]:
        raise Exception("Error: unknown option for SF direction('%s')!"%direction)
    myScaleFactors = SF[:]
    if direction == "up":
        myScaleFactors = SFup[:]
    elif direction == "down":
        myScaleFactors = SFdown[:]
    pset.tauTriggerSF = PSet(
        binLeftEdges = binEdges[:],
        scaleFactors = myScaleFactors
    )

## Reader for trigger SF json files
class TriggerSFJsonReader:
    def __init__(self, era, runrange, jsonname):
        # Read json
        _jsonpath = os.path.join(os.getenv("HIGGSANALYSIS_BASE"), "NtupleAnalysis", "data", "TriggerEfficiency")
        filename = os.path.join(_jsonpath, jsonname)
        if not os.path.exists(filename):
            raise Exception("Error: file '%s' does not exist!"%filename)
        f = open(filename)
        contents = json.load(f)
        f.close()
        # Obtain data efficiencies
        param = "dataParameters"
        if not param in contents.keys():
            raise Exception("Error: missing key '%s' in json '%s'! Options: %s"%(param,filename,", ".join(map(str,contents.keys()))))
        if not runrange in contents[param].keys():
            raise Exception("Error: missing run range '%s' for data in json '%s'! Options: %s"(runrange,filename,", ".join(map(str,contents[param].keys()))))
        if not era in contents[param][runrange].keys():
            raise Exception("Error: missing era '%s' for data in json '%s'! Options: %s"(runrange,filename,", ".join(map(str,contents[param][runrange].keys()))))
        datadict = self._readValues(contents[param][runrange][era], "data")
        # Obtain MC efficiencies
        param = "mcParameters"
        if not param in contents.keys():
            raise Exception("Error: missing key '%s' in json '%s'! Options: %s"%(param,filename,", ".join(map(str,contents.keys()))))
        if not era in contents[param].keys():
            raise Exception("Error: missing era '%s' for mc in json '%s'! Options: %s"(runrange,filename,", ".join(map(str,contents[param].keys()))))
        mcdict = self._readValues(contents[param][runrange][era], "mc")
        # Calculate SF's
        keys = datadict.keys()
        if len(keys) != len(mcdict.keys()):
            raise Exception("Error: different number of bins for data and mc in json '%s'!"%filename)
        keys.sort()
        self.result = {}
        self.result["binEdges"] = []
        self.result["SF"] = []
        self.result["SFdataUp"] = []
        self.result["SFdataDown"] = []
        self.result["SFmcUp"] = []
        self.result["SFmcDown"] = []
        i = 0
        for key in keys:
            if i > 0:
                self.result["binEdges"].append(key)
            i += 1
            self.result["SF"].append(datadict[key]["eff"] / mcdict[key]["eff"])
            self.result["SFdataUp"].append(datadict[key]["effup"] / mcdict[key]["eff"])
            self.result["SFdataDown"].append(datadict[key]["effdown"] / mcdict[key]["eff"])
            self.result["SFmcUp"].append(datadict[key]["eff"] / mcdict[key]["effup"])
            if abs(mcdict[key]["effdown"] - 0.00001):
                raise Exception("Down variation in bin '%s' is zero in json '%s'"%(key, filename))
            self.result["SFmcDown"].append(datadict[key]["eff"] / mcdict[key]["effdown"])

    def getResult(self):
        return self.result
        
    def _readValues(inputdict, label):
        outdict = {}
        for item in inputdict["bins"]:
            bindict = {}
            bindict[label+"eff"] = item["efficiency"]
            # FIXME: check if the uncertainties are relative or absolute uncertainties
            value = item["efficiency"]+item["efficiencyPlus"]
            if value > 1.0:
                bindict[label+"effup"] = 1.0
            else:
                bindict[label+"effup"] = value
            value = item["efficiency"]+item["efficiencyMinus"]
            if value < 0.0:
                bindict[label+"effdown"] = 0.0
            else:
                bindict[label+"effdown"] = value
            outdict[item["pt"]] = bindict
        return outdict
