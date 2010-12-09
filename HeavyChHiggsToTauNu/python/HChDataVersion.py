# The purpose of default files is testing only. For production
# processing use either CRAB or explicit file names in PoolSource

# triggerProcess:  the process containing the HLT information
# patCastor:         default file for PATtuple at castor
# patMadhatter:      default file for PATtuple at madhatter
# analysisCastor:    default file for analysis at castor
# analysisMadhatter: default file for analysis at madhatter
config = {
    "35X": {
        "triggerProcess": "HLT",
        "analysisCastor": "/castor/cern.ch/user/s/slehti/HiggsAnalysisData/pattuple_1_1_AcP_TTToHplusBWB_M-100_7TeV-pythia6-tauola_Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b.root",
        "analysisMadhatter": "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/TTToHpmToTauNu_M100/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/Spring10_START3X_V26_v1_GEN-SIM-RECO_pattuple_v6_1/94799423eedb9d1f02c6c0ed06eb3738/pattuple_4_1_pvI.root",
    },
    "35Xredigi": {
        "triggerProcess": "REDIGI",
        "patCastor": "rfio:/castor/cern.ch/user/s/slehti/testData/Ztautau_Spring10-START3X_V26_S09-v1-RAW-RECO.root"
    },
    "36X": {
        "triggerProcess": "REDIGI36X",
        "patMadhatter": "/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/FEFEE1D1-F17B-DF11-B911-00304867C16A.root",
        "analysisMadhatter": "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/WJets/WJets_7TeV-madgraph-tauola/Summer10_START36_V9_S09_v1_GEN-SIM-RECO_pattuple_v6_1/2366fe480375ff6f751e0b7e8ec70b52/pattuple_93_1_xbp.root"
    },
    "36Xdata": {
        "triggerProcess": "HLT",
        "patCastor": "/store/data/Run2010A/JetMETTau/RECO/Jul16thReReco-v1/0049/FE36C9D8-3891-DF11-829E-00261894395F.root"
    },
    "36Xspring10": {"triggerProcess": "REDIGI36"},
    "37X": {"triggerProcess": "REDIGI37X"},
    "38X": {
        "triggerProcess": "REDIGI38X",
        "patMadhatter": "/store/mc/Fall10/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/AODSIM/START38_V12-v1/0033/FE2DEA23-15CA-DF11-B86C-0026189438BF.root"
    },
    "38Xrelval": {
        "triggerProcess": "HLT",
        "patCastor": '/store/relval/CMSSW_3_8_4/RelValTTbar/GEN-SIM-RECO/START38_V12-v1/0025/34CD73F6-9AC2-DF11-9B42-002618943857.root',
        "analysisCastor": "rfio:/castor/cern.ch/user/s/slehti/HiggsAnalysisData/pattuple_1_1_AcP_TTToHplusBWB_M-100_7TeV-pythia6-tauola_Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b.root",
        "analysisMadhatter": "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/TTToHplusBWB_M120/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall10_START38_V12_v1_GEN-SIM-RECO_pattuple_v6_1b/78d4b6b79bb86567b5da3e176aad4eb3/pattuple_9_1_RL8.root"
    },
    "38XdataRun2010A": {"triggerProcess": "HLT"},
    "38XdataRun2010B": {
        "triggerProcess": "HLT",
        "analysisMadhatter": "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/BTau_146240-148107/BTau/Run2010B_PromptReco_v2_RECO_pattuple_v6_1/43c3132ebadd44967499e6cca288e3ab/pattuple_7_1_cJr.root"
    }
}


class DataVersion:
    def __init__(self, dataVersion):
        if not dataVersion in config:
            raise Exception("Unknown dataVersion '%s', look HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion for allowed versions")

        conf = config[dataVersion]

        self.trigger = conf["triggerProcess"]
        self.version = dataVersion

        for f in ["patCastor", "patMadhatter", "analysisCastor", "analysisMadhatter"]:
            if f in conf:
                setattr(self, f, conf[f])

        # Collision data
        if dataVersion in ["36Xdata", "38XdataRun2010A", "38XdataRun2010B"]:
            self.is_data = True
            self.globalTag = "GR_R_38X_V15::All"

            self.is_runA = False
            self.is_runB = False
            if dataVersion == "38XdataRun2010A":
                self.is_runA = True
            if dataVersion == "38XdataRun2010B":
                self.is_runB = True

        # MC
        else:
            self.is_data = False
            self.globalTag = "START38_V14::All"

        self.is_35X = False
        self.is_38X = False
        if dataVersion in ["35X", "35Xredigi"]:
            self.is_35X = True
        elif dataVersion in ["38X", "38Xrelval", "38XdataRun2010A", "38XdataRun2010B"]:
            self.is_38X = True

    def isData(self):
        return self.is_data

    def isRun2010A(self):
        return self.is_runA

    def isRun2010B(self):
        return self.is_runB

    def isMC(self):
        return not self.is_data

    def is35X(self):
        return self.is_35X

    def is38X(self):
        return self.is_38X

    def getTriggerProcess(self):
        return self.trigger

    def getGlobalTag(self):
        return self.globalTag

    def getPatDefaultFileCastor(self):
        if not hasattr(self, "patCastor"):
            print "No default file for PAT in CASTOR for dataVersion "+self.version
            return ""
        return self.patCastor

    def getPatDefaultFileMadhatter(self, dcap=False):
        if not hasattr(self, "patMadhatter"):
            print "No default file for PAT in madhatter for dataVersion "+self.version
            return ""
        if dcap:
            return "dcap://madhatter.csc.fi:22125/pnfs/csc.fi/data/cms"+self.patMadhatter
        else:
            return self.patMadhatter

    def getAnalysisDefaultFileCastor(self):
        if not hasattr(self, "analysisCastor"):
            print "No default file for analysis in CASTOR for dataVersion "+self.version
            return ""
        return self.analysisCastor

    def getAnalysisDefaultFileMadhatter(self, dcap=False):
        if not hasattr(self, "analysisMadhatter"):
            print "No default file for analysis in madhatter for dataVersion "+self.version
            return ""
        if dcap:
            return "dcap://madhatter.csc.fi:22125/pnfs/csc.fi/data/cms"+self.analysisMadhatter
        else:
            return self.analysisMadhatter


