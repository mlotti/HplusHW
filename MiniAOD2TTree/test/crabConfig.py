'''
Links:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile
https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial#Setup_the_environment
'''

#================================================================================================
# Import Modules
#================================================================================================
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import getUsernameFromSiteDB

# Definitions
jecDB = ['Summer16_23Sep2016AllV4_DATA_JEC.db','Summer16_23Sep2016V4_MC_JEC.db','Spring16_25nsV10_MC_JER.db']

#================================================================================================
# General Section: The user specifies generic parameters about the request (e.g. request name).
#================================================================================================
config = Configuration()
config.section_("General")
config.General.requestName = rName
config.General.workArea = dirName
config.General.transferOutputs = True
config.General.transferLogs = True
# options:
#config.General.failureLimit
#config.General.instance
#config.General.activity


#================================================================================================
# JobType Section: Contains all the parameters of the user job type and related configurables
#================================================================================================
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'miniAOD2TTree_cfg.py'
config.JobType.pyCfgParams = ''
config.JobType.outputFiles = ['miniaod2tree.root']
config.JobType.inputFiles  = ['jec']
config.JobType.inputFiles.extend(jecDB)


# options:
#config.JobType.generator
#config.JobType.inputFiles
#config.JobType.disableAutomaticOutputCollection
#config.JobType.eventsPerLumi
#config.JobType.allowUndistributedCMSSW
config.JobType.maxMemoryMB = 4000
#config.JobType.maxJobRuntimeMin
#config.JobType.numCores
#config.JobType.priority
#config.JobType.scriptExe
#config.JobType.scriptArgs
#config.JobType.sendPythonFolde
#config.JobType.externalPluginFile


#================================================================================================
# Data Section: Contains all parameters related to the data to be analyzed (incl. splitting params)
#================================================================================================
config.section_("Data")
config.Data.inputDataset = dataset
config.Data.inputDBS = 'global' #'phys03'
config.Data.splitting = 'FileBased'
#config.Data.totalUnits  = 10
config.Data.unitsPerJob = 5
config.Data.publication = False
config.Data.outLFNDirBase = '/store/user/%s/CRAB3_TransferData' % (getUsernameFromSiteDB())
# testing:
# config.Data.totalUnits    = 100000
# config.Data.unitsPerJob   = 10000 
# options:
# config.Data.allowNonValidInputDatase
# config.Data.outputPrimaryDataset
# config.Data.inputDBS
# config.Data.unitsPerJob
# config.Data.useParent
# config.Data.secondaryInputDataset
# config.Data.lumiMask
# config.Data.runRange
# config.Data.outLFNDirBase
# config.Data.publication
# config.Data.publishDBS
# config.Data.outputDatasetTag
# config.Data.publishWithGroupName
# config.Data.ignoreLocality
# config.Data.userInputFiles


#================================================================================================
# Site Section: Contains the Grid site parameters (incl. stage out information)
#================================================================================================
config.section_("Site")
config.Site.storageSite = 'T2_FI_HIP' #'T2_CH_CERN' 
# options:
# config.Site.blacklist = ['T2_US_Florida']
# config.Site.whitelist = ['T2_CH_CERN', 'T2_FI_HIP']


#================================================================================================
# Debug Section: For experts use only
#================================================================================================
# config.section_("Debug")
# config.Debug.oneEventMode = True
# config.Debug.ASOURL       = ''
# config.Debug.scheddName   = ''
# config.Debug.extraJDL     = ''
# config.Debug.collector    = ''
