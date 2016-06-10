lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-274421_13TeV_PromptReco_Collisions16_JSON.txt"


class Dataset :
    def __init__(self,url,dbs="global",dataVersion="80Xmc",lumiMask=lumiMask):
        self.URL = url
        self.DBS = dbs
        self.dataVersion = dataVersion
        self.lumiMask = lumiMask

    def isData(self):
        if "data" in self.dataVersion:
            return True
        return False



datasetsTauData = []
datasetsTauData.append(Dataset('/Tau/Run2016B-PromptReco-v1/MINIAOD',dataVersion="80Xdata"))
datasetsTauData.append(Dataset('/Tau/Run2016B-PromptReco-v2/MINIAOD',dataVersion="80Xdata"))

datasetsMuonData = []
datasetsMuonData.append(Dataset('/SingleMuon/Run2016B-PromptReco-v1/MINIAOD',dataVersion="80Xdata"))
datasetsMuonData.append(Dataset('/SingleMuon/Run2016B-PromptReco-v2/MINIAOD',dataVersion="80Xdata"))


