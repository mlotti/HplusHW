import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

# This configuration requires CMSSW.pycfg_params to be set!

#dataVersion = "35X"
dataVersion = "36X"
#dataVersion = "37X"

# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#Passing_Command_Line_Arguments_T
options = VarParsing.VarParsing()
options.register("dataVersion",
                 "", # default value
                 options.multiplicity.singleton, # singleton or list
                 options.varType.string,          # string, int, or float
                 "Data version")
options.parseArguments()

if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion


process = cms.Process("HChPatTuple")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('GR10_P_V6::All') # GR10_P_V6::All
if dataVersion == "37X":
    process.GlobalTag.globaltag = cms.string("START37_V6::All")
else:
    process.GlobalTag.globaltag = cms.string("START36_V10::All")

process.GlobalTag.globaltag = cms.string("START38_V9::All")

process.source = cms.Source('PoolSource',
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
    "/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/FEFEE1D1-F17B-DF11-B911-00304867C16A.root"
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/FA6E6683-C844-DF11-A2D8-0018F3D0961E.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/D0E1C289-C744-DF11-B84C-00261894389F.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/A24BB684-C544-DF11-81ED-00261894391D.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/284100C7-4E45-DF11-9AF9-0018F3D09710.root',
#       '/store/relval/CMSSW_3_6_0_pre6/RelValZTT/GEN-SIM-RECO/START36_V4-v1/0011/06A4E187-C644-DF11-BC3E-0018F3D096AA.root'
  )
)
if dataVersion == "35X":
    process.source.fileNames = cms.untracked.vstring(
	"rfio:/castor/cern.ch/user/s/slehti/testData/testHplus_35X.root"
#        '/store/relval/CMSSW_3_5_8/RelValZTT/GEN-SIM-RECO/START3X_V26-v1/0017/86C58057-8F52-DF11-9160-002618FDA28E.root',
#        '/store/relval/CMSSW_3_5_8/RelValZTT/GEN-SIM-RECO/START3X_V26-v1/0016/FC9BCE19-5152-DF11-8EDC-002618FDA204.root',
#        '/store/relval/CMSSW_3_5_8/RelValZTT/GEN-SIM-RECO/START3X_V26-v1/0016/64D9835B-5052-DF11-8343-002618FDA279.root',
#        '/store/relval/CMSSW_3_5_8/RelValZTT/GEN-SIM-RECO/START3X_V26-v1/0016/50C0224A-4F52-DF11-B8A0-002618943906.root',
#        '/store/relval/CMSSW_3_5_8/RelValZTT/GEN-SIM-RECO/START3X_V26-v1/0016/207DFCE2-4F52-DF11-8D25-0018F3D096BA.root'
    )
    


################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
del process.TFileService

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('pattuple.root'),
    outputCommands = cms.untracked.vstring(
        "drop *",
        "keep *_genParticles_*_*",
        "keep GenEventInfoProduct_*_*_*",
        "keep GenRunInfoProduct_*_*_*",
        "keep edmTriggerResults_*_*_*",
        "keep triggerTriggerEvent_*_*_*"
    )
)

from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *
process.s = addPat(process, dataVersion)

process.path    = cms.Path(process.s)

process.outpath = cms.EndPath(process.out)

