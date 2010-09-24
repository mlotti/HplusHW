import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion

#dataVersion = "35X"
dataVersion = "35Xredigi"
#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion
print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

process = cms.Process("HChSignalAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
        # For testing in lxplus
        dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        #dataVersion.getAnalysisDefaultFileMadhatter()
        #dataVersion.getAnalysisDefaultFileMadhatterDcap()
  )
)

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.categories.append("EventCounts")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
process.TFileService.fileName = "histograms.root"

import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param

# Tau ID and jet selection
process.tauSelection = cms.EDFilter("HPlusTauPtrSelectorFilter",
    tauSelection = param.tauSelection.clone()
)
process.tauSelection.tauSelection.ptCut = 20.
process.jetSelection = cms.EDFilter("HPlusJetPtrSelectorFilter",
    tauSrc = cms.untracked.InputTag("tauSelection"),
    jetSelection = param.jetSelection.clone()
)

# Add trigger bits to the ntuple
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTrigger_cfi as HChTrigger
HChTrigger.customise(process, dataVersion)

# Tau and jet ntuple producers
process.tauNtuple = cms.EDProducer("HPlusTauNtupleProducer",
    src = cms.untracked.InputTag("tauSelection"),
    prefix = cms.untracked.string("tau_"),
    tauDiscriminators = cms.untracked.VPSet(
        cms.untracked.PSet(
            discriminator = cms.untracked.string("HChTauIDtauPolarizationCont"),
            branch = cms.untracked.string("discrHChTauIDtauPolarizationCont")
        )
    )
)    
process.jetNtuple = cms.EDProducer("HPlusJetNtupleProducer",
    src = cms.untracked.InputTag("jetSelection"),
    prefix = cms.untracked.string("jet_"),
    # The module takes the *maximum* value of the b-discriminators
    # from the input jets, and stores that to the event
    bDiscriminators = cms.untracked.VPSet(
        cms.untracked.PSet(
            discriminator = cms.untracked.string("trackCountingHighEffBJetTags"),
            branch = cms.untracked.string("maxBtrackCountingHighEffBJetTags")
        )
    )
)

# All and ntuplized event counters
process.allEvents = cms.EDProducer("EventCountProducer")
process.ntupleEvents = cms.EDProducer("EventCountProducer")

# Path without MET data, they come below
process.ntuplePath = cms.Path(
    process.allEvents *
    process.HChTriggers *
    process.tauSelection *
    process.jetSelection *
    process.ntupleEvents *
    process.tauNtuple *
    process.jetNtuple
)

# Helper function for MET producers to decrease the mount of typing
def addMet(process, src, alias):
    metNtuple = cms.EDProducer("HPlusMETNtupleProducer",
        src = cms.untracked.InputTag(src),
        alias = cms.untracked.string(alias)
    )
    transverseMass = cms.EDProducer("HPlusTransverseMassProducer",
        tauSrc = cms.InputTag("tauSelection"),
        metSrc = cms.InputTag(src)
    )
    transverseMassNtuple = cms.EDProducer("HPlusMassNtupleProducer",
        src = cms.untracked.InputTag(alias+"TransverseMass"),
        alias = cms.untracked.string(alias+"_transverseMass")
    )
    deltaPhiNtuple = cms.EDProducer("HPlusDeltaPhiNtupleProducer",
        src1 = cms.untracked.InputTag("tauSelection"),
        src2 = cms.untracked.InputTag(src),
        alias = cms.untracked.string(alias+"_deltaPhi")
    )

    process.__setattr__(alias+"Ntuple", metNtuple)
    process.__setattr__(alias+"TransverseMass", transverseMass)
    process.__setattr__(alias+"TransverseMassNtuple", transverseMassNtuple)
    process.__setattr__(alias+"DeltaPhiNtuple", deltaPhiNtuple)
    process.ntuplePath *= metNtuple
    process.ntuplePath *= transverseMass
    process.ntuplePath *= transverseMassNtuple
    process.ntuplePath *= deltaPhiNtuple

# Add the METs with the helper function
addMet(process, "patMETs", "caloMET")
addMet(process, "patMETsPF", "pfMET")
addMet(process, "patMETsTC", "tcMET")


################################################################################

process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("ntuplePath")
    ),
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
        "drop *",
        "keep double_*_*_HChSignalAnalysis",
        "keep float_*_*_HChSignalAnalysis",
        "keep int_*_*_HChSignalAnalysis",
        "keep edmMergeableCounter_*_*_*",
        "drop edmMergeableCounter_*_subcount*_HChSignalAnalysis"
    )
)

# Uncomment the following line to get also the event output (can be
# useful for debugging purposes)
process.outpath = cms.EndPath(process.out)

