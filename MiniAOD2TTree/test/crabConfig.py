from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = rName
config.General.workArea = dirName
config.General.transferOutputs = True
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'miniAOD2TTree_cfg.py'
config.JobType.pyCfgParams = ''
config.JobType.outputFiles = ['miniaod2tree.root']

config.section_("Data")
config.Data.inputDataset = dataset
config.Data.inputDBS = 'global'
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
#config.Data.totalUnits  = 10
config.Data.unitsPerJob = 5
config.Data.publication = False
config.Data.outLFNDirBase = '/store/user/%s/CRAB3_TransferData' % (getUsernameFromSiteDB())

config.section_("Site")
config.Site.storageSite = 'T2_FI_HIP'

