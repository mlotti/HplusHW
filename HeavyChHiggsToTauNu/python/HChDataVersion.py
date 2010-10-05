triggerProcessMap = {
    "35X": "HLT",
    "35Xredigi": "REDIGI",
    "36X": "REDIGI36X",
    "36Xdata": "HLT",
    "36Xspring10": "REDIGI36",
    "37X": "REDIGI37X",
    "38X": "REDIGI38X",
    "38XdataRun2010A": "HLT",
    "38XdataRun2010B": "HLT"
    }

class DataVersion:
    def __init__(self, dataVersion):
        if not dataVersion in triggerProcessMap:
            raise Exception("Unknown dataVersion '%s', look HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion for allowed versions")

        self.trigger = triggerProcessMap[dataVersion]
        self.version = dataVersion

        if dataVersion in ["36Xdata", "38XdataRun2010A", "38XdataRun2010B"]:
            self.is_data = True
            self.globalTag = "GR_R_38X_V13::All"

            if dataVersion == "36Xdata":
                self.patDefaultFileCastor = "/store/data/Run2010A/JetMETTau/RECO/Jul16thReReco-v1/0049/FE36C9D8-3891-DF11-829E-00261894395F.root"

            self.is_runA = False
            self.is_runB = False
            if dataVersion == "38XdataRun2010A":
                self.is_runA = True
            if dataVersion == "38XdataRun2010B":
                self.is_runB = True
        else:
            self.is_data = False
            self.globalTag = "START38_V12::All"

            if dataVersion == "35X":
                self.analysisDefaultFileCastor = "rfio:/castor/cern.ch/user/m/mkortela/hplus/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola_Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3/pattuple_6_1_Gv1.root"
                self.analysisDefaultFileMadhatter = "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/TTToHpmToTauNu_M100/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3/1c883eb3798701ca362caa0e5457977b/pattuple_6_1_Gv1.root"
                self.analysisDefaultFileMadhatterDcap = "dcap://madhatter.csc.fi:22125/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/TTToHpmToTauNu_M100/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v3/1c883eb3798701ca362caa0e5457977b/pattuple_6_1_Gv1.root"

            if dataVersion == "35Xredigi":
                self.patDefaultFileCastor = "rfio:/castor/cern.ch/user/s/slehti/testData/Ztautau_Spring10-START3X_V26_S09-v1-RAW-RECO.root"
            if dataVersion == "36X":
                self.patDefaultFileMadhatter = "/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/FEFEE1D1-F17B-DF11-B911-00304867C16A.root"

            if dataVersion == "38X":
                self.patDefaultFileMadhatter = "/store/mc/Fall10/QCD_Pt_50to80_TuneZ2_7TeV_pythia6/AODSIM/START38_V12-v1/0033/FE2DEA23-15CA-DF11-B86C-0026189438BF.root"

        self.is_35X = False
        self.is_38X = False
        if dataVersion in ["35X", "35Xredigi"]:
            self.is_35X = True
        elif dataVersion in ["38X", "38XdataRun2010A", "38XdataRun2010B"]:
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
        if not hasattr(self, "patDefaultFileCastor"):
            print "No default file for PAT in CASTOR for dataVersion "+self.version
            return ""
        return self.patDefaultFileCastor

    def getPatDefaultFileMadhatter(self):
        if not hasattr(self, "patDefaultFileMadhatter"):
            print "No default file for PAT in madhatter for dataVersion "+self.version
            return ""
        return self.patDefaultFileMadhatter

    def getAnalysisDefaultFileCastor(self):
        if not hasattr(self, "analysisDefaultFileCastor"):
            print "No default file for analysis in CASTOR for dataVersion "+self.version
            return ""
        return self.analysisDefaultFileCastor

    def getAnalysisDefaultFileMadhatter(self):
        if not hasattr(self, "analysisDefaultFileMadhatter"):
            print "No default file for analysis in madhatter for dataVersion "+self.version
            return ""
        return self.analysisDefaultFileMadhatter

