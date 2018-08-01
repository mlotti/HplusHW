from HiggsAnalysis.NtupleAnalysis.main import PSet
import json
import csv
import os
import sys
import math

DEBUG = False

def Print(msg, printHeader=False):
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

def Verbose(msg, printHeader=False):
    if not DEBUG:
        return
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

# This file contains all the scale factors and their uncertainties used in the analysis
# There are two types of scale factors:
#   1) simple scale factors (such as fake tau uncertainty)
#   2) scale factors as function of some variable (such as b tag uncertainties)
# Both are supplied as config parameters, but the type (2) SF's are accessed 
# via GenericScaleFactor c++ class, which causes some naming scheme rules

# Tau ID efficiency scale factor
# https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendation13TeV
def assignTauIdentificationSF(tauSelectionPset):
    SF = 1.0
    if tauSelectionPset.isolationDiscr=="byLooseCombinedIsolationDeltaBetaCorr3Hits":    SF = 0.93
    elif tauSelectionPset.isolationDiscr=="byMediumCombinedIsolationDeltaBetaCorr3Hits": SF = 0.91
    elif tauSelectionPset.isolationDiscr=="byTightCombinedIsolationDeltaBetaCorr3Hits":  SF = 0.89
    elif tauSelectionPset.isolationDiscr=="byVLooseIsolationMVArun2v1DBoldDMwLT":        SF = 0.99
    elif tauSelectionPset.isolationDiscr=="byLooseIsolationMVArun2v1DBoldDMwLT":         SF = 0.99
    elif tauSelectionPset.isolationDiscr=="byMediumIsolationMVArun2v1DBoldDMwLT":        SF = 0.97
    elif tauSelectionPset.isolationDiscr=="byTightIsolationMVArun2v1DBoldDMwLT":         SF = 0.95
    else:
        raise Exception("Error: tau ID scale factor not defined for discriminator %s"%tauSelectionPset.isolationDiscr)
    tauSelectionPset.tauIdentificationSF = SF

##===== Tau misidentification (simple SF)
# \param tauSelectionPset  the tau config PSet
# \param partonFakingTau   "eToTau", "muToTau", "jetToTau"
# \param direction         "nominal, "up", "down"
def assignTauMisidentificationSF(tauSelectionPset, partonFakingTau, direction):
    dirNumber = 0
    if direction == "up":
        dirNumber = 1
    elif direction == "down":
        dirNumber = -1
    if partonFakingTau == "eToTau":
        _assignEToTauSF(tauSelectionPset, dirNumber)
    elif partonFakingTau == "muToTau":
        _assignMuToTauSF(tauSelectionPset, dirNumber)
    elif partonFakingTau == "jetToTau":
        _assignJetToTauSF(tauSelectionPset, dirNumber)
    else:
        raise Exception("Error: unknown option for parton faking tau ('%s')!"%partonFakingTau)

# Values from https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendation13TeV#Electron_to_tau_fake_rate
# Measured SF in Run-2 (2016), for Tight WP
def _assignEToTauSF(tauSelectionPset, dirNumber):
    tauSelectionPset.tauMisidetificationEToTauElectronBarrelSF = 1.40 + dirNumber*0.12
    tauSelectionPset.tauMisidetificationEToTauElectronEndcapSF = 1.90 + dirNumber*0.30
#    tauSelectionPset.tauMisidetificationEToTauSF = 1.0 + dirNumber*0.30

# Values from https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendation13TeV#Muon_Rejection,
# Measured SF in Run-2 with bad muon filter, for Cut-based Loose WP
def _assignMuToTauSF(tauSelectionPset, dirNumber):
    tauSelectionPset.tauMisidetificationMuToTauBarrel0to0p4SF   = 1.22 + dirNumber*0.04
    tauSelectionPset.tauMisidetificationMuToTauBarrel0p4to0p8SF = 1.12 + dirNumber*0.04
    tauSelectionPset.tauMisidetificationMuToTauBarrel0p8to1p2SF = 1.26 + dirNumber*0.04
    tauSelectionPset.tauMisidetificationMuToTauBarrel1p2to1p7SF = 1.22 + dirNumber*0.15
    tauSelectionPset.tauMisidetificationMuToTauEndcapSF = 2.39 + dirNumber*0.16
#    tauSelectionPset.tauMisidetificationMuToTauSF = 1.0 + dirNumber*0.30

def _assignJetToTauSF(tauSelectionPset, dirNumber):
    tauSelectionPset.tauMisidetificationJetToTauBarrelSF = 1.0 + dirNumber*0.20
    tauSelectionPset.tauMisidetificationJetToTauEndcapSF = 1.0 + dirNumber*0.20
#    tauSelectionPset.tauMisidetificationJetToTauSF = 1.0 + dirNumber*0.20

# Top-tagging
def assignMisIDSF(pset, direction, jsonfile, variationType="MC"):
    reader = TriggerSFJsonReader("2016", "runs_273150_284044", jsonfile)
    result = reader.getResult()
    if variationType == "MC":
        _assignTrgSF("MisIDSF", result["binEdges"], result["SF"], result["SFmcUp"], result["SFmcDown"], pset, direction)
    elif variationType == "Data":
        _assignTrgSF("MisIDSF", result["binEdges"], result["SF"], result["SFdataUp"], result["SFdataDown"], pset, direction)
    else:
        raise Exception("Error: Unsupported variation type '%s'! Valid options are: 'MC', 'data'"%variationType)
    return

##===== tau trigger SF (SF as function of pT)
# \param tauSelectionPset  the tau config PSet
# \param direction         "nominal, "up", "down"
# \param variationType     "MC", "data"  (the uncertainty in MC and data are variated separately)
def assignTauTriggerSF(tauSelectionPset, direction, tauTrgJson, variationType="MC"):
    # FIXME: there is no mechanic right now to choose correct era / run range
    # FIXME: this approach works as long as there is just one efficiency for the simulated samples

    nprongs = "13prong"
    if tauSelectionPset.prongs == 1:
        nprongs = "1prong"
    if tauSelectionPset.prongs == 3:
        nprongs = "3prong"

####    tauTrgJson = "tauLegTriggerEfficiency2015_"+nprongs+".json"
####    tauTrgJson = "tauLegTriggerEfficiency2016_ICHEP.json"

    print "Taking tau trigger eff/sf from",tauTrgJson

    reader = TriggerSFJsonReader("2016", "runs_273150_284044", tauTrgJson)

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
def assignMETTriggerSF(METSelectionPset, btagDiscrWorkingPoint, direction, metTrgJson, variationType="MC"):
    # FIXME: there is no mechanic right now to choose correct era / run range
    # FIXME: this approach works as long as there is just one efficiency for the simulated samples
####    reader = TriggerSFJsonReader("2015D", "runs_256629_260627", "metLegTriggerEfficiency2015_btag%s.json"%btagDiscrWorkingPoint)
####    reader = TriggerSFJsonReader("2016", "runs_271036_279588", "metLegTriggerEfficiency2016.json") 


    print "Taking MET trigger eff/sf from",metTrgJson

    reader = TriggerSFJsonReader("2016_MET90", "runs_273150_284044", metTrgJson)

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
    return

def setupToptagSFInformation(topTagPset, topTagMisidFilename, topTagEfficiencyFilename, topTagEffUncertaintiesFilename, direction, variationInfo=None):
    '''
    Top-tagging SF
    \param topTagPset   PSet of topSelection
    \param topTagMisifFilename  Filename to the json file containing the Misidintification rates (SystTopBDT + PythonWriter)
    \param topTagEfficiencyFilename  Filename to the json file containing the tagging effifiencies (SystTopBDT + PythonWriter)
    \param topTagEffUncertaintiesFilename Filename to the json file containing the tagging efficiencies uncertainties (TopTaggerEfficiency + UncertaintyWriter.py)
    \param direction  "nominal"/"down"/"up"
    \param variationInfo  "tag"/"mistag" This parameter specifies if the variation is applied for the top->top component or non-top->top component
    '''
    if not variationInfo in [None, "tag", "mistag"]:
        raise Exception("Error: unknown parameter for variationInfo given (%s)! Valid options are: %s" % (variationInfo, ", ".join(variationInfo)) )

    # Process the misidentification rates (MC and data)
    Print("Setting top-tag misid (data and MC) filename to \"%s\"" % (topTagMisidFilename), True)
    _setupToptagMisid(topTagPset, topTagMisidFilename, direction, variationInfo)

    # Process the tagging efficiencies (MC and data)
    Print("Setting top-tag tagging efficiency (data and MC) filename to \"%s\"" % (topTagEfficiencyFilename), False)
    _setupToptagEfficiency(topTagPset, topTagEfficiencyFilename, direction, variationInfo)
    
    # Process the tagging efficiency uncertainties (MC)
    Print("Setting top-tag tagging efficiency uncertainties (MC) filename to \"%s\"" % (topTagEffUncertaintiesFilename), False)
    _setupToptagEffUncertainties(topTagPset, topTagEffUncertaintiesFilename, direction, variationInfo)
    
    # Set syst. uncert. variation information
    topTagPset.topTagSFVariationDirection = direction
    if variationInfo == None:
        topTagPset.topTagSFVariationInfo = "None"
    else:
        topTagPset.topTagSFVariationInfo = variationInfo

    if 0:
        Print("Printing topTag PSet", True)
        print topTagPset
    return

def updateBtagSFInformationForVariations(btagPset, direction, variationInfo=None):
    '''
    A helper function to update b-tag SF information in AnalysisBuilder for syst. variations
    '''
    # Set syst. uncert. variation information
    btagPset.btagSFVariationDirection = direction
    if variationInfo == None:
        btagPset.btagSFVariationInfo = "None"
    else:
        btagPset.btagSFVariationInfo = variationInfo
    return

def updateTopTagSFInformationForVariations(topTagPset, direction, variationInfo=None):
    '''
    A helper function to update top-tag SF information in AnalysisBuilder for syst. variations
    '''
    # Set syst. uncert. variation information
    topTagPset.topTagSFVariationDirection = direction
    if variationInfo == None:
        topTagPset.topTagSFVariationInfo = "None"
    else:
        topTagPset.topTagSFVariationInfo = variationInfo
    return


## Helper function accessed through setupBtagSFInformation
def _setupBtagSFDatabase(btagPset, btagPayloadFilename, direction, variationInfo):
    fullname = os.path.join(os.getenv("HIGGSANALYSIS_BASE"), "NtupleAnalysis", "data", btagPayloadFilename)
    if not os.path.exists(fullname):
        raise Exception("Error: Could not find btag POG btag SF payload csv file! (tried: %s)"%fullname)
    # Obtain header row and rows
    headerRow = None
    rows = []
    validAlgoHeaderPairs = {
      "pfCombinedInclusiveSecondaryVertexV2BJetTags": "CSVv2",
      "pfCombinedMVAV2BJetTags": "cMVAv2"
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
    return

def _setupToptagMisid(topTagPset, topTagMisidFilename, direction, variationInfo):
    '''
    Helper function accessed through setupToptagSFInformation
    '''
    runrange = "runs_273150_284044" #fixme
    era      = "2016" #fixme
    fullname = os.path.join(os.getenv("HIGGSANALYSIS_BASE"), "NtupleAnalysis", "data", topTagMisidFilename)
    if not os.path.exists(fullname):
        raise Exception("Could not find the top-tag  misid json file! (tried: %s)"%fullname)

    # Read the json file
    Verbose("Opening file \"%s\" for reading the top-tag misidentification rates" % (fullname), True)
    f = open(fullname)
    contents = json.load(f)
    f.close()

    # Obtain data efficiencies
    param = "dataParameters"
    if not param in contents.keys():
        raise Exception("Missing key '%s' in json '%s'! Options: %s"%(param,filename,", ".join(map(str,contents.keys()))))
    if not runrange in contents[param].keys():
        raise Exception("Missing run range '%s' for data in json '%s'! Options: %s"(runrange,filename,", ".join(map(str,contents[param].keys()))))
    datadict = readValues(contents[param][runrange], "data")

    # Obtain MC efficiencies
    param = "mcParameters"
    if not param in contents.keys():
        raise Exception("Missing key '%s' in json '%s'! Options: %s"%(param,filename,", ".join(map(str,contents.keys()))))
    if not era in contents[param].keys():
        raise Exception("Error: missing era '%s' for mc in json '%s'! Options: %s"(runrange,filename,", ".join(map(str,contents[param].keys()))))
    mcdict = readValues(contents[param][era], "mc")

    # Calculate the SF = Eff(Data)/Eff(MC)
    keys = datadict.keys()
    if len(keys) != len(mcdict.keys()):
        raise Exception("Different number of bins for data and mc in json '%s'!" % filename)
    
    keys.sort()
    result = {}
    result["binEdges"] = []
    result["SF"]       = []
    result["SFUp"]     = []
    result["SFDown"]   = []
    psetList = []

    for i, pT in enumerate(keys, 0):
        
        if i > 0:
            result["binEdges"].append(pT)

        pTMin = pT
        if i == len(keys)-1:
            pTMax = 100000.0 # overflow bin (fixme?)
        else:
            pTMax = keys[i+1]

        # Get the efficiencies and their errors
        effData     = datadict[pT]["dataeff"]
        effDataUp   = datadict[pT]["dataeffup"]
        effDataDown = datadict[pT]["dataeffdown"]
        effMC       = mcdict[pT]["mceff"]
        effMCUp     = mcdict[pT]["mceffup"]
        effMCDown   = mcdict[pT]["mceffdown"]
        
        # Define the Scale Factor (SF) as: SF = Eff_Data / Eff_MC
        sf     = effData / effMC
        sfUp   = effDataUp / effMC
        dsf    = (sfUp-sf)
        sfDown = sf-dsf                # gives symmetric shape
        #sfDown = effDataDown / effMC  # gives asymmetric shape 
        Print("pT = %.1f, sf = %0.3f, sf+ = %0.3f, sf- = %0.3f" % (pT, sf, sfUp, sfDown), i==0)

        result["SF"].append(sf)
        result["SFUp"].append(sfUp)
        result["SFDown"].append(sfDown)
        if abs(mcdict[pT]["mceffdown"]) < 0.00001:
            raise Exception("Down variation in bin '%s' is zero in json '%s'"%(pT, filename))

        # Sanity check
        if result["SF"][len(result["SF"])-1] < 0.00001:
            raise Exception("In file '%s' bin %s the SF is zero! Please fix!" % (filename, pT) )
    
        # Define the PSet
        p = PSet(ptMin         = pTMin,
                 ptMax         = pTMax,
                 misidMC       = effMC,
                 misidMCUp     = effMCUp,
                 misidMCDown   = effMCDown,
                 misidData     = effData,
                 misidDataUp   = effDataUp,
                 misidDataDown = effDataDown,
                 sf            = sf,
                 sfUp          = sfUp,
                 sfDown        = sfDown,
                 )
        psetList.append(p)
    topTagPset.topTagMisid = psetList
    if 0:
        print topTagPset
        #print topTagPset.topTagMisid
    return

def _setupToptagEffUncertainties(topTagPset, topTagEffUncertaintiesFilename, direction, variationInfo):
    '''
    Helper function accessed through setupToptagSFInformation
    '''
    fullname = os.path.join(os.getenv("HIGGSANALYSIS_BASE"), "NtupleAnalysis", "data", topTagEffUncertaintiesFilename)
    if not os.path.exists(fullname):
        raise Exception("Could not find the top-tagging eff. uncertainties file! (tried: %s)" % fullname)
    
    # Read the json file
    Print("Opening file \"%s\" for reading the top-tag efficiency ucertainties" % (fullname), True)
    f = open(fullname)
    contents = json.load(f)
    f.close()
    
    # Obtain uncertainties (Use top-mass systematic only once! Take maximum deviation (31 July 2018)
    #params = ["TT_hdampUP", "TT_mtop1715", "TT_mtop1755", "TT_fsrdown", "TT_fsrup", "TT_isrdown", "TT_mtop1735", "TT_mtop1785", "TT_TuneEE5C",
    #          "TT_hdampDOWN", "TT_mtop1695", "TT_evtgen", "TT_ isrup", "TT_mtop1665", "matching"]
    params = ["TT_hdampUP", "TT_fsrdown", "TT_fsrup", "TT_isrdown", "TT_TuneEE5C", "TT_hdampDOWN", "TT_evtgen", "TT_isrup", "TT_mtop1665", "matching"]
    
    for param in params:
        if not param in contents.keys():
            raise Exception("Missing key '%s' in json '%s'! Options: %s"%(param, fullname,", ".join(map(str,contents.keys()))))
    
    psetList = []
    first = contents[params[0]]
    firstBins = first["bins"]
    
    # For-loop: All loops
    for i in range(0, len(firstBins)):
        
        dSF2 = 0.0
        pt = firstBins[i]["pt"]
        
        for param in params:
            paramDict = contents[param]
            binsList = paramDict["bins"]
            
            case = binsList[i]
            pT = case["pt"]
            uncertainty = case["uncertainty"] 
            
            dSF2 += uncertainty * uncertainty
                        
        dSF = math.sqrt(dSF2)
        
        # Find pTMin, pTMax
        pTMin = pt
        if i == len(firstBins)-1:
            pTMax = 100000.0 # overflow bin (fixme?)
        else:
            pTMax = firstBins[i+1]["pt"]
            
        # Uncertainty Up
        dSFUp = dSF

        # Uncertainty Down
        dSFDown = -dSF
        
        # Define a PSet
        p = PSet(ptMin       = pTMin,
                 ptMax       = pTMax,
                 dsfUp       = dSFUp,
                 dsfDown     = dSFDown,
                 )
        psetList.append(p)
        
    # Save the PSet
    topTagPset.topTagEffUncertainties = psetList
    return

def _setupToptagEfficiency(topTagPset, topTagEfficiencyFilename, direction, variationInfo):
    '''
    Helper function accessed through setupToptagSFInformation
    '''
    runrange = "runs_273150_284044" #fixme
    era      = "2016" #fixme
    fileName = topTagEfficiencyFilename
    fullname = os.path.join(os.getenv("HIGGSANALYSIS_BASE"), "NtupleAnalysis", "data", fileName)
    if not os.path.exists(fullname):
        raise Exception("Could not find the top-tag efficiency json file! (tried: %s)" % fullname)

    # Read the json file
    Print("Opening file \"%s\" for reading the top-tag efficiencies" % (fullname), True)
    f = open(fullname)
    contents = json.load(f)
    f.close()

    # Obtain data efficiencies
    param = "dataParameters"
    if not param in contents.keys():
        raise Exception("Missing key '%s' in json '%s'! Options: %s"%(param,fileName,", ".join(map(str,contents.keys()))))
    if not runrange in contents[param].keys():
        raise Exception("Missing run range '%s' for data in json '%s'! Options: %s"(runrange,fileName,", ".join(map(str,contents[param].keys()))))
    datadict = readValues(contents[param][runrange], "data")

    # Obtain MC efficiencies
    param = "mcParameters"
    if not param in contents.keys():
        raise Exception("Missing key '%s' in json '%s'! Options: %s"%(param,fileName,", ".join(map(str,contents.keys()))))
    if not era in contents[param].keys():
        raise Exception("Error: missing era '%s' for mc in json '%s'! Options: %s"(runrange,fileName,", ".join(map(str,contents[param].keys()))))
    mcdict = readValues(contents[param][era], "mc")

    # Calculate the SF = Eff(Data)/Eff(MC)
    keys = datadict.keys()
    if len(keys) != len(mcdict.keys()):
        raise Exception("Different number of bins for data and mc in json '%s'!"%fileName)
    
    keys.sort()
    result = {}
    result["binEdges"] = []
    result["SF"]       = []
    result["SFUp"]     = []
    result["SFDown"]   = []
    psetList = []

    # For-loop: All keys
    for i, pT in enumerate(keys, 0):
        
        if i > 0:
            result["binEdges"].append(pT)

        pTMin = pT
        if i == len(keys)-1:
            pTMax = 100000.0 # overflow bin (fixme?)
        else:
            pTMax = keys[i+1]

        # Get the efficiencies and their errors
        effData     = datadict[pT]["dataeff"]
        effDataUp   = datadict[pT]["dataeffup"]
        effDataDown = datadict[pT]["dataeffdown"]
        effMC       = mcdict[pT]["mceff"]
        effMCUp     = mcdict[pT]["mceffup"]
        effMCDown   = mcdict[pT]["mceffdown"]
        
        # Define the Scale Factor (SF) as: SF = Eff_Data / Eff_MC
        sf     = effData / effMC
        sfUp   = effDataUp / effMC
        dsf    = (sfUp-sf)
        sfDown = sf-dsf                # gives symmetric shape
        #sfDown = effDataDown / effMC  # gives asymmetric shape 
        Print("pT = %.1f, sf = %0.3f, sf+ = %0.3f, sf- = %0.3f" % (pT, sf, sfUp, sfDown), i==0)
        
        result["SF"].append(sf)
        result["SFUp"].append(sfUp)
        result["SFDown"].append(sfDown)
        if abs(mcdict[pT]["mceffdown"]) < 0.00001:
            raise Exception("Down variation in bin '%s' is zero in json '%s'"%(pT, fileName))

        # Sanity check
        if result["SF"][len(result["SF"])-1] < 0.00001:
            raise Exception("In file '%s' bin %s the SF is zero! Please fix!" % (fileName, pT) )
    

        # Define the PSet
        p = PSet(ptMin       = pTMin,
                 ptMax       = pTMax,
                 effMC       = effMC,
                 effMCUp     = effMCUp,
                 effMCDown   = effMCDown,
                 effData     = effData,
                 effDataUp   = effDataUp,
                 effDataDown = effDataDown,
                 sf          = sf,
                 sfUp       = sfUp,
                 sfDown     = sfDown,
                 )
        psetList.append(p)
        topTagPset.topTagEfficiency = psetList
    if 0:
        print topTagPset
        #print topTagPset.topTagEfficiency
    return

def readValues(inputdict, label):
    '''
    read the dictionary in json file 
    and return a dictionary with the following mapping:
    efficiency       -> label + eff
    uncertaintyPlus  -> label + effup
    uncertaintyMinus -> label + effdown
    '''
    outdict = {}
    for item in inputdict["bins"]:
        bindict = {}
        bindict[label+"eff"] = item["efficiency"]
        value = item["efficiency"]+item["uncertaintyPlus"]
        if value > 1.0:
            bindict[label+"effup"] = 1.0
        else:
            bindict[label+"effup"] = value

        value = item["efficiency"]-item["uncertaintyMinus"]
        if value < 0.0:
            bindict[label+"effdown"] = 0.000001
        else:
            bindict[label+"effdown"] = value
        outdict[item["pt"]] = bindict
    return outdict


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
#            value = item["efficiency"]*(1.0+item["uncertaintyPlus"])
	    value = item["efficiency"]+item["uncertaintyPlus"]
            if value > 1.0:
                bindict[label+"effup"] = 1.0
            else:
                bindict[label+"effup"] = value
#            value = item["efficiency"]*(1.0-item["uncertaintyMinus"])
	    value = item["efficiency"]-item["uncertaintyMinus"]
            if value < 0.0:
                bindict[label+"effdown"] = 0.000001
            else:
                bindict[label+"effdown"] = value
            outdict[item["pt"]] = bindict
        return outdict
