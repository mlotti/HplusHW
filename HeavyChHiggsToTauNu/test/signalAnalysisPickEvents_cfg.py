import FWCore.ParameterSet.Config as cms

### FIXME: This file has not been tested after migration to AnalysisConfiguration

# Select the version of the data (needed only for interactice running
#dataVersion="44XmcS6"     # Fall11 MC
dataVersion="44Xdata"    # Run2011 08Nov and 19Nov ReRecos

dataEras = ["Run2011AB"]

from HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration import ConfigBuilder
builder = ConfigBuilder(dataVersion, dataEras)

# Always run PAT on the fly when running on PickEvents AOD file
builder.options.doPat=1
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
builder.options.trigger = param.singleTauMetTriggerPaths

process = builder.buildSignalAnalysis()

# Set input file(s)
process.source.fileNames = [
    "file:pickevents_Tau_Run2011A-May10ReReco-v1_AOD.root",
#    "file:pickevents_Tau_Run2011A-PromptReco-v4_AOD.root",
    ]

# Add output module
process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("signalAnalysisPath")
    ),
    fileName = cms.untracked.string('events.root'),
    outputCommands = cms.untracked.vstring(
        "keep *",
        "drop *_*_counterNames_*",
        "drop *_*_counterInstances_*"
#	"drop *",
#	"keep *",
#        "keep edmMergeableCounter_*_*_*"
    )
)
process.outpath = cms.EndPath(process.out)
