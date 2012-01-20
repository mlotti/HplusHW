# The purpose of default files is testing only. For production
# processing use either CRAB or explicit file names in PoolSource

# triggerProcess:  the process containing the HLT information
# patCastor:         default file for PATtuple at castor
# patMadhatter:      default file for PATtuple at madhatter
# analysisCastor:    default file for analysis at castor
# analysisMadhatter: default file for analysis at madhatter
config = {
    "42Xdata": {
        "triggerProcess": "HLT",
        "recoProcess": "RECO",
#        "signalTrigger": "HLT_SingleIsoTau20_Trk15_MET20",
#        "patCastor": "",
        "patMadhatter": "file:/mnt/flustre/mkortela/data/Tau/Run2011A-PromptReco-v4/AOD/FCF1CBDD-878F-E011-885B-003048F118D4.root",
#        "patMadhatter": "file:/mnt/flustre/mkortela/data/SingleMu/PromptReco-v4/AOD/F2B6FB32-7AA3-E011-BCAF-BCAEC5329710.root",
#        "analysisCastor": "",
        "analysisMadhatter": "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_2_X/Tau_160431-163869_May10/Tau/Run2011A_May10ReReco_v1_AOD_160431_pattuple_v19/95bdfb89e63988c1ffa2ad610b62da8e/pattuple_101_1_cDq.root",
    },
    "42XmcS3": {
        "triggerProcess": "HLT",
        "recoProcess": "RECO",
        "signalTrigger": "HLT_IsoPFTau35_Trk20_MET45_v2",
        "patMadhatter": "file:/mnt/flustre/mkortela/data/TT_TuneZ2_7TeV-pythia6-tauola/Summer11-PU_S3_START42_V11-v1/AODSIM/84A5EB09-0A77-E011-A8C3-00266CF252D4.root",
#        "patMadhatter": "file:/mnt/flustre/mkortela/data/QCD_Pt-170to300_TuneZ2_7TeV_pythia6/Summer11-PU_S3_START42_V11-v2/AODSIM/FE47C9F3-C97D-E011-B103-003048670B66.root",
    },
    "42XmcS4": {
        "triggerProcess": "HLT",
        "recoProcess": "RECO",
        "signalTrigger": "HLT_IsoPFTau35_Trk20_MET45_v2",
#        "patMadhatter": "/store/mc/Summer11/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S4_START42_V11-v1/0000/0428EC7E-F199-E011-B474-002618943861.root",
        "patMadhatter": "file:/mnt/flustre/mkortela/data//TTJets_TuneZ2_7TeV-madgraph-tauola/Summer11-PU_S4_START42_V11-v1/AODSIM/F498AD1D-8298-E011-BFB9-003048678F92.root",
        "analysisMadhatter": "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_2_X/TTToHplusBWB_M120_Summer11/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v19b/9436cd413e1f831f4594f528a53faac6/pattuple_10_1_TsT.root"
    },
    "42XmcS6": {
        "triggerProcess": "HLT",
        "recoProcess": "RECO",
        "signalTrigger": "HLT_MediumIsoPFTau35_Trk20_MET60_v1",
        "patMadhatter": "file:/mnt/flustre/mkortela/data/TTToHplusBWB_M-120_7TeV-pythia6-tauola/Fall11-PU_S6_START42_V14B-v1/AODSIM/A87958F4-92F3-E011-9CBC-0018F3D0966C.root",
    },
    "44XmcS4": {                                                                                                                                                                                      
        "triggerProcess": "HLT",                                                                                                                                                                      
        "recoProcess": "RECO",                                                                                                                                                                        
        "signalTrigger": "HLT_MediumIsoPFTau35_Trk20_MET60_v6",
        "analysisMadhatter": "file:/mnt/flustre/slehti/Fall11_TTToHplusBWB_M-90_7TeV-pythia6-tauola_B2AD85E1-D520-E111-B5AC-001A928116EA.root",         
    }
}


class DataVersion:
    def __init__(self, dataVersion):
        if dataVersion == "42Xmc":
            dataVersion = "42XmcS4"

        if dataVersion == "44Xmc":
            dataVersion = "44XmcS4"
        
        if not dataVersion in config:
            names = config.keys()
            names.sort()
            raise Exception("Unknown dataVersion '%s',  allowed versions are %s" % (dataVersion, ", ".join(names)))

        conf = config[dataVersion]

        self.trigger = conf["triggerProcess"]
        self.recoProcess = conf.get("recoProcess", None)
        self.version = dataVersion

        for f in ["patCastor", "patMadhatter", "analysisCastor", "analysisMadhatter"]:
            if f in conf:
                setattr(self, f, conf[f])

        # Collision data
        if "data" in dataVersion:
            self.is_data = True
            self.globalTag = "GR_R_44_V13::All"

        # MC
        else:
            self.is_data = False
            self.globalTag = "START44_V12::All"

            try:
                self.signalTrigger = conf["signalTrigger"]
            except KeyError:
                pass
                
    def isData(self):
        return self.is_data

    def isMC(self):
        return not self.is_data

    def isS4(self):
        return self.isMC() and ("S4" in self.version or "S6" in self.version)

    def isS6(self):
        return self.isMC() and "S6" in self.version

    def getTriggerProcess(self):
        return self.trigger

    def getDefaultSignalTrigger(self):
        # The trigger names in data can change so often that encoding
        # it in the dataVersion is not flexible enough
        if self.isData():
            raise Exception("Default signal trigger is available only for MC")
        return self.signalTrigger

    def getRecoProcess(self):
        if not self.recoProcess:
            raise Exception("Reco process name is not available for %s" % self.version)
        return self.recoProcess

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
        if dcap and self.patMadhatter.find("/store") == 0:
            return "dcap://madhatter.csc.fi:22125/pnfs/csc.fi/data/cms"+self.patMadhatter
        else:
            return self.patMadhatter

    def getAnalysisDefaultFileCastor(self):
        if not hasattr(self, "analysisCastor"):
            print "No default file for analysis in CASTOR for dataVersion "+self.version+ ". Perhaps you could copy one there?"
            return ""
        return self.analysisCastor

    def getAnalysisDefaultFileMadhatter(self, dcap=False):
        if not hasattr(self, "analysisMadhatter"):
            print "No default file for analysis in madhatter for dataVersion "+self.version
            return ""
        if dcap and self.analysisMadhatter.find("/store") == 0:
            return "dcap://madhatter.csc.fi:22125/pnfs/csc.fi/data/cms"+self.analysisMadhatter
        else:
            return self.analysisMadhatter


