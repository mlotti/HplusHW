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

# Create Process
process = cms.Process("HChPatTuple")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

# Global tag
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string("START38_V9::All")

# Source
process.source = cms.Source('PoolSource',
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
    "/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/FEFEE1D1-F17B-DF11-B911-00304867C16A.root"
  )
)

# Load common stuff
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
del process.TFileService

# Output module
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

# Add PAT sequences
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *
process.s = addPat(process, dataVersion)

# Create paths
process.path    = cms.Path(process.s)
process.outpath = cms.EndPath(process.out)

