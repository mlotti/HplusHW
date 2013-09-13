import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

# This is an analyzer to produce an ntuple with the number of true
# interactions per event. This is needed to obtain the PU-reweighted
# number of all events for each MC dataset.
#
# Also needed for TopPt-reweighted numer of all events for TTJets

# 44X:
# Runs in ~10 s / 5k events
# Output size ~25 kB / 5k events

# 53X:
# Runs in ~30 s / 6k events
# Output size ~37 kB / 6k events

#dataVersion = "44XmcS6"
dataVersion = "53XmcS10"

# Just to be compatible with our multicrab system, which assumes that
# the job configuration file reads the command line arguments
options, dataVersion = getOptionsDataVersion(dataVersion)

process = cms.Process("PUNTUPLE")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        # For testing in jade
        dataVersion.getPatDefaultFileMadhatter()
        #"file:/mnt/flustre/mkortela/data/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM/7EE6381E-D036-E111-9BF5-002354EF3BDF.root"
    )
)

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
#process.options.wantSummary = cms.untracked.bool(True)
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
#process.MessageLogger.cerr.FwkReport.reportEvery = 1
#process.MessageLogger.categories.append("TopGenEvent")
#process.MessageLogger.categories.append("Ntuple")
#process.MessageLogger.categories.append("GenParticleTools")

process.pileupNtuple = cms.EDAnalyzer("HPlusPileUpNtupleAnalyzer",
    puSummarySrc = cms.InputTag("addPileupInfo"),
    ttGenEventSrc = cms.InputTag("genEvt"),
    topBranchesEnabled = cms.bool(False)
)
process.begin = cms.Sequence()
if options.sample == "TTJets":
    import HiggsAnalysis.HeavyChHiggsToTauNu.TopPtWeight_cfi as topPtWeight
    topPtWeight.addTtGenEvent(process, process.begin)
    process.pileupNtuple.topBranchesEnabled = True;


process.path = cms.Path(
    process.begin +
    process.pileupNtuple
)

#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
