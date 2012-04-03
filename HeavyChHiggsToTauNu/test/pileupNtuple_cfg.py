import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

# This is an analyzer to produce an ntuple with the number of true
# interactions per event. This is needed to obtain the PU-reweighted
# number of all events for each MC dataset.

# Runs in ~10 s / 5k events
# Output size ~25 kB / 5k events

dataVersion = "44XmcS6"

# Just to be compatible with our multicrab system, which assumes that
# the job configuration file reads the command line arguments
options, dataVersion = getOptionsDataVersion(dataVersion)

process = cms.Process("PUNTUPLE")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        # For testing in jade
        dataVersion.getPatDefaultFileMadhatter()
    )
)

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
#process.options.wantSummary = cms.untracked.bool(True)
process.MessageLogger.cerr.FwkReport.reportEvery = 5000

process.pileupNtuple = cms.EDAnalyzer("HPlusPileUpNtupleAnalyzer",
    puSummarySrc = cms.InputTag("addPileupInfo")
)

process.path = cms.Path(
    process.pileupNtuple
)
