triggerProcessMap = {
    "35X": "HLT",
    "data": "HLT",
    "35Xredigi": "REDIGI",
    "36X": "REDIGI36X",
    "36Xspring10": "REDIGI36",
    "37X": "REDIGI37X"
    }

class DataVersion:
    def __init__(self, dataVersion):
        if not dataVersion in triggerProcessMap:
            raise Exception("Unknown dataVersion '%s', look HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion for allowed versions")

        self.trigger = triggerProcessMap[dataVersion]

        if dataVersion == "data":
            self.is_data = True
            self.globalTag = "GR_R_38X_V13::All"

            self.patDefaultFileCastor = "/store/data/Run2010A/JetMETTau/RECO/Jul16thReReco-v1/0049/FE36C9D8-3891-DF11-829E-00261894395F.root"
        else:
            self.is_data = False
            self.globalTag = "START38_V9::All"

            if dataVersion == "35Xredigi":
                self.patDefaultFileCastor = "rfio:/castor/cern.ch/user/s/slehti/testData/Ztautau_Spring10-START3X_V26_S09-v1-RAW-RECO.root"
            if dataVersion == "36X":
                self.patDefaultFileMadhatter = "/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/FEFEE1D1-F17B-DF11-B911-00304867C16A.root"
            
                self.analysisDefaultFileCastor = "rfio:/castor/cern.ch/user/m/mkortela/hplus/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola_Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v2/pattuple_6_1_MSU.root"
                self.analysisDefaultFileMadhatter = "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/TTToHpmToTauNu_M100/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v2/d538bad796104165ef547eb8f3e812a0/pattuple_6_1_MSU.root"
                self.analysisDefaultFileMadhatterDcap = "dcap://madhatter.csc.fi:22125/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/TTToHpmToTauNu_M100/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v2/d538bad796104165ef547eb8f3e812a0/pattuple_6_1_MSU.root"

        self.is_35X = False
        if dataVersion in ["35X", "35Xredigi"]:
            self.is_35X = True

    def isData(self):
        return self.is_data

    def isMC(self):
        return not self.is_data

    def is35X(self):
        return self.is_35X

    def getTriggerProcess(self):
        return self.trigger

    def getGlobalTag(self):
        return self.globalTag

    def getPatDefaultFileCastor(self):
        return self.patDefaultFileCastor

    def getPatDefaultFileMadhatter(self):
        return self.patDefaultFileMadhatter

    def getAnalysisDefaultFileCastor(self):
        return self.getAnalysisDefaultFileCastor

    def getAnalysisDefaultFileMadhatter(self):
        return self.getAnalysisDefaultFileMadhatter

