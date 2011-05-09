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
        "patMadhatter": "file:/mnt/flustre/mkortela/data/BTau/Run2010B-Apr21ReReco-v1/AOD/109B70F2-8471-E011-B3F1-001A64789D18.root",
#        "analysisCastor": "",
#        "analysisMadhatter": "",
    },
    
}


class DataVersion:
    def __init__(self, dataVersion):
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
            self.globalTag = "GR_R_42_V13::All"

        # MC
        else:
            self.is_data = False
            self.globalTag = "START42_V12::All"

            try:
                self.signalTrigger = conf["signalTrigger"]
            except KeyError:
                pass
                
    def isData(self):
        return self.is_data

    def isMC(self):
        return not self.is_data

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
            print "No default file for analysis in CASTOR for dataVersion "+self.version
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


