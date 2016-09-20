from HiggsAnalysis.NtupleAnalysis.main import PSet
import json
import csv
import os

# This file contains all the scale factors and their uncertainties used in the analysis
# There are two types of scale factors:
#   1) simple scale factors (such as fake tau uncertainty)
#   2) scale factors as function of some variable (such as b tag uncertainties)
# Both are supplied as config parameters, but the type (2) SF's are accessed 
# via GenericScaleFactor c++ class, which causes some naming scheme rules

# Tau ID efficiency scale factor
# https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendation13TeV
def assignTauIdentificationSF(tauSelectionPset):
    tauSelectionPset.tauIdentificationSF = 0.83 # for Run-2 2016


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

    nprongs = "13prong"
    if tauSelectionPset.prongs == 1:
        nprongs = "1prong"
    if tauSelectionPset.prongs == 3:
        nprongs = "3prong"

####    tauTrgJson = "tauLegTriggerEfficiency2015_"+nprongs+".json"
    tauTrgJson = "tauLegTriggerEfficiency2016.json"
    print "Taking tau trigger eff/sf from",tauTrgJson

    reader = TriggerSFJsonReader("2016HIP", "runs_273150_278800", tauTrgJson)

    result = reader.getResult()
    if variationType == "MC":
        _assignTrgSF("tauTriggerSF", result["binEdges"], result["SF"], result["SFmcUp"], result["SFmcDown"], tauSelectionPset, direction)
    elif variationType == "Data":
        _assignTrgSF("tauTriggerSF", result["binEdges"], result["SF"], result["SFdataUp"], result["SFdataDown"], tauSelectionPset, direction)
    else:
        raise Exception("Error: Unsupported variation type '%s'! Valid options are: 'MC', 'data'"%variationType)

##===== MET trigger SF (SF as function of MET)
# \param METSelectionPset  the MET selection config PSet
# \param direction         "nominal, "up", "down"
# \param variationType     "MC", "data"  (the uncertainty in MC and data are variated separately)
def assignMETTriggerSF(METSelectionPset, btagDiscrWorkingPoint, direction, variationType="MC"):
    # FIXME: there is no mechanic right now to choose correct era / run range
    # FIXME: this approach works as long as there is just one efficiency for the simulated samples
####    reader = TriggerSFJsonReader("2015D", "runs_256629_260627", "metLegTriggerEfficiency2015_btag%s.json"%btagDiscrWorkingPoint)
    reader = TriggerSFJsonReader("2016", "runs_271036_279588", "metLegTriggerEfficiency2016.json") 
    result = reader.getResult()
    if variationType == "MC":
        _assignTrgSF("metTriggerSF", result["binEdges"], result["SF"], result["SFmcUp"], result["SFmcDown"], METSelectionPset, direction)
    elif variationType == "Data":
        _assignTrgSF("metTriggerSF", result["binEdges"], result["SF"], result["SFdataUp"], result["SFdataDown"], METSelectionPset, direction)
    else:
        raise Exception("Error: Unsupported variation type '%s'! Valid options are: 'MC', 'data'"%variationType)

##===== Btag SF 
# \param btagPset   PSet of btagging
# \param btagPayloadFilename     Filename to the csv file provided by btag POG (in the data directory)
# \param btagEfficiencyFilename  Filename to the json file produced with BTagEfficiencyAnalysis (in the data directory)
# \param direction  "nominal"/"down"/"up"
# \param variationInfo  "tag"/"mistag" This parameter specifies if the variation is applied for the b->b component or non-b->b component
def setupBtagSFInformation(btagPset, btagPayloadFilename, btagEfficiencyFilename, direction, variationInfo=None):
    if not variationInfo in [None, "tag", "mistag"]:
        raise Exception("Error: unknown parameter for variationInfo given (%s)! Valid options are: tag, mistag"%variationInfo)
    #print "Setting btagSF: %s, %s"%(btagPayloadFilename, btagEfficiencyFilename)
    # Process the csv from the btag POG and add the relevant information to the PSet
    _setupBtagSFDatabase(btagPset, btagPayloadFilename, direction, variationInfo)
    # Process the json produced with BTagEfficiencyAnalysis and add the relevant information to the PSet
    _setupBtagEfficiency(btagPset, btagEfficiencyFilename, direction, variationInfo)
    # Set syst. uncert. variation information
    btagPset.btagSFVariationDirection = direction
    if variationInfo == None:
        btagPset.btagSFVariationInfo = "None"
    else:
        btagPset.btagSFVariationInfo = variationInfo
    #print btagPset

## Helper function accessed through setupBtagSFInformation
def _setupBtagSFDatabase(btagPset, btagPayloadFilename, direction, variationInfo):
    fullname = os.path.join(os.getenv("HIGGSANALYSIS_BASE"), "NtupleAnalysis", "data", btagPayloadFilename)
    if not os.path.exists(fullname):
        raise Exception("Error: Could not find btag POG btag SF payload csv file! (tried: %s)"%fullname)
    # Obtain header row and rows
    headerRow = None
    rows = []
    validAlgoHeaderPairs = {
      "pfCombinedInclusiveSecondaryVertexV2BJetTags": "CSVv2"
    }
    if not btagPset.__getattr__("bjetDiscr") in validAlgoHeaderPairs.keys():
        raise Exception("Error: No valid payload header ID has been specified for btag algo %s"%btagPset.__getattr__("bjetDiscr"))
    directionLUT = { 
      "nominal": " central",
      "down": " down",
      "up": " up"
    }
    if not direction in directionLUT.keys():
        raise Exception("Error: direction '%s' is unknown! Valid options: %s"%(direction, ", ".join(map(str,directionLUT))))
    workingPointLUT = {
      "Loose": "0",
      "Medium": "1",
      "Tight": "2",
    }
    if not btagPset.__getattr__("bjetDiscrWorkingPoint") in workingPointLUT.keys():
        raise Exception("Error: Btag working point '%s' is not defined in the look-up table!"%(btagPset.__getattr__("bjetDiscrWorkingPoint")))
    # Column names in the btag payload file
    headerColumnIndices = {
      "OperatingPoint": None,
      "measurementType": None,
      "sysType": None,
      "jetFlavor": None,
      "etaMin": None,
      "etaMax": None,
      "ptMin": None,
      "ptMax": None,
      "discrMin": None,
      "discrMax": None,
      "formula": None
    }
    with open(fullname, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if headerRow == None:
                headerRow = row[1:]
                # Check that payload matches with tagger
                if validAlgoHeaderPairs[btagPset.__getattr__("bjetDiscr")] != row[0]:
                    raise Exception("Error: btag algo = %s is incompatible with btag SF payload file header '%s' (expected %s)!"%(btagPset.__getattr__("bjetDiscr"), row[0], validAlgoHeaderPairs[btagPset.__getattr__("bjetDiscr")]))
                # Obtain column indices
                for key in headerColumnIndices.keys():
                    for i in range(len(headerRow)):
                        if headerRow[i] == key or headerRow[i] == " "+key or headerRow[i] == " "+key+" ":
                            headerColumnIndices[key] = i
                    if headerColumnIndices[key] == None:
                        raise Exception("Error: could not find column '%s' in file %s:\n  header = %s"%(key, fullname, headerRow))
            else:
                # Store only the rows which apply for the desired variation and working point
                if row[headerColumnIndices["OperatingPoint"]] == workingPointLUT[btagPset.__getattr__("bjetDiscrWorkingPoint")]:
                    rows.append(row)
    if len(rows) == 0:
        raise Exception("Error: for unknown reason, no entries found from the btag SF payload (%s)!"%fullname)
    # Convert output into vector of PSets
    psetList = []
    for row in rows:
        p = PSet(jetFlavor=int(row[headerColumnIndices["jetFlavor"]]),
                 ptMin=float(row[headerColumnIndices["ptMin"]]), 
                 ptMax=float(row[headerColumnIndices["ptMax"]]), 
                 etaMin=float(row[headerColumnIndices["etaMin"]]), 
                 etaMax=float(row[headerColumnIndices["etaMax"]]), 
                 discrMin=float(row[headerColumnIndices["discrMin"]]), 
                 discrMax=float(row[headerColumnIndices["discrMax"]]), 
                 sysType=row[headerColumnIndices["sysType"]],
                 formula=row[headerColumnIndices["formula"]])
        psetList.append(p)
    btagPset.btagSF = psetList

## Helper function accessed through setupBtagSFInformation
def _setupBtagEfficiency(btagPset, btagEfficiencyFilename, direction, variationInfo):
    fullname = os.path.join(os.getenv("HIGGSANALYSIS_BASE"), "NtupleAnalysis", "data", btagEfficiencyFilename)
    if not os.path.exists(fullname):
        raise Exception("Error: Could not find the btag efficiency json file! (tried: %s)"%fullname)
    # Read the json file
    f = open(fullname)
    contents = json.load(f)
    f.close()
    # Loop over the contents to convert as list of PSets the requested information
    psetList = []
    for row in contents:
        # Require that the btag discriminator and working points match
        if row["discr"] == btagPset.__getattr__("bjetDiscr") and row["workingPoint"] == btagPset.__getattr__("bjetDiscrWorkingPoint"):
            #print row["discr"], row["workingPoint"], row["flavor"], row["ptMin"]
            p = PSet(jetFlavor=row["flavor"],
                    ptMin=row["ptMin"],
                    ptMax=row["ptMax"],
                    eff=float(row["eff"]),
                    effDown=float(row["effDown"]),
                    effUp=float(row["effUp"]))
            psetList.append(p)
    btagPset.btagEfficiency = psetList

## Helper function
def _assignTrgSF(name, binEdges, SF, SFup, SFdown, pset, direction):
    if not direction in ["nominal", "up", "down"]:
        raise Exception("Error: unknown option for SF direction('%s')!"%direction)
    myScaleFactors = SF[:]
    if direction == "up":
        myScaleFactors = SFup[:]
    elif direction == "down":
        myScaleFactors = SFdown[:]
    setattr(pset, name, PSet(
        binLeftEdges = binEdges[:],
        scaleFactors = myScaleFactors
    ))

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
        datadict = self._readValues(contents[param][runrange], "data")
        # Obtain MC efficiencies
        param = "mcParameters"
        if not param in contents.keys():
            raise Exception("Error: missing key '%s' in json '%s'! Options: %s"%(param,filename,", ".join(map(str,contents.keys()))))
        if not era in contents[param].keys():
            raise Exception("Error: missing era '%s' for mc in json '%s'! Options: %s"(runrange,filename,", ".join(map(str,contents[param].keys()))))
        mcdict = self._readValues(contents[param][era], "mc")
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
            self.result["SF"].append(datadict[key]["dataeff"] / mcdict[key]["mceff"])
            self.result["SFdataUp"].append(datadict[key]["dataeffup"] / mcdict[key]["mceff"])
            self.result["SFdataDown"].append(datadict[key]["dataeffdown"] / mcdict[key]["mceff"])
            self.result["SFmcUp"].append(datadict[key]["dataeff"] / mcdict[key]["mceffup"])
            if abs(mcdict[key]["mceffdown"]) < 0.00001:
                raise Exception("Down variation in bin '%s' is zero in json '%s'"%(key, filename))
            self.result["SFmcDown"].append(datadict[key]["dataeff"] / mcdict[key]["mceffdown"])
            # Sanity check
            if self.result["SF"][len(self.result["SF"])-1] < 0.00001:
                raise Exception("Error: In file '%s' bin %s the SF is zero! Please fix!"%(filename, key))

    def getResult(self):
        return self.result
        
    def _readValues(self, inputdict, label):
        outdict = {}
        for item in inputdict["bins"]:
            bindict = {}
            bindict[label+"eff"] = item["efficiency"]
            value = item["efficiency"]*(1.0+item["uncertaintyPlus"])
            if value > 1.0:
                bindict[label+"effup"] = 1.0
            else:
                bindict[label+"effup"] = value
            value = item["efficiency"]*(1.0-item["uncertaintyMinus"])
            if value < 0.0:
                bindict[label+"effdown"] = 0.0
            else:
                bindict[label+"effdown"] = value
            outdict[item["pt"]] = bindict
        return outdict
