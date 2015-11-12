from HiggsAnalysis.NtupleAnalysis.main import PSet

# This file contains all the scale factors and their uncertainties used in the analysis
# There are two types of scale factors:
#   1) simple scale factors (such as fake tau uncertainty)
#   2) scale factors as function of some variable (such as b tag uncertainties)
# Both are supplied as config parameters, but the type (2) SF's are accessed 
# via GenericScaleFactor c++ class, which causes some naming scheme rules

##===== Tau misidentification
# \param tauSelectionPset  the tau config PSet
# \param partonFakingTau   "eToTau", "muToTau", "jetToTau"
# \param etaRegion         "barrel", "endcap"
# \param direction         "nominal, "up", "down"
def assignTauMisidentificationSF(tauSelectionPset, partonFakingTau, etaRegion, direction):
    if not etaRegion in ["barrel", "endcap", "full"]:
        raise Exception("Error: unknown option for eta region('%s')!"%etaRegion)
    if not direction in ["nominal", "up", "down"]:
        raise Exception("Error: unknown option for direction('%s')!"%etaRegion)
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
  