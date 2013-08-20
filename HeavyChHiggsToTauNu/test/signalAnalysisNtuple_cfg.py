import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################

dataVersion="42XmcS4"     # Summer11 MC
#dataVersion="42Xdata" # Run2010 Apr21 ReReco, Run2011 May10 ReReco, Run2011 PromptReco

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

process = cms.Process("HChSignalAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        # For testing in lxplus
        #dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        dataVersion.getAnalysisDefaultFileMadhatter()
        #dataVersion.getAnalysisDefaultFileMadhatterDcap()
  )
)

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
process.TFileService.fileName = "histograms.root"

# Counter of all events
process.allEvents = cms.EDProducer("EventCountProducer")
process.ntupleSequence = cms.Sequence(process.allEvents)

# Object selections
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
process.ntupleSequence *= process.goodPrimaryVertices

process.jetSelection = cms.EDFilter("HPlusCandViewLazyPtrSelector",
    src = cms.InputTag("selectedPatJetsAK5PF"),
    cut = cms.string("pt() > 20 && abs(eta()) < 2.4 && numberOfDaughters() > 1 && chargedEmEnergyFraction() < 0.99 && neutralHadronEnergyFraction() < 0.99 && neutralEmEnergyFraction < 0.99 && chargedHadronEnergyFraction() > 0 && chargedMultiplicity() > 0")
)
process.ntupleSequence *= process.jetSelection

# Add trigger bits to the ntuple
#import HiggsAnalysis.HeavyChHiggsToTauNu.HChTrigger_cfi as HChTrigger
#HChTrigger.customise(process, dataVersion)



# Ntuple producers
process.pileupNtuple = cms.EDProducer("HPlusPileupNtupleProducer",
    alias = cms.string("pileup_ave_nvtx"),
    src = cms.InputTag("addPileupInfo")
)
process.ntupleSequence *= process.pileupNtuple
process.vertexNtuple = cms.EDProducer("HPlusVertexNtupleProducer",
    prefix = cms.string("vertex_"),
    src = cms.InputTag("offlinePrimaryVertices"),
    goodSrc = cms.InputTag("goodPrimaryVertices"),
    maxDelta = cms.double(0.001),
    sumPtSrc = cms.InputTag("offlinePrimaryVerticesSumPt", "sumPt"),
    sumPt2Src = cms.InputTag("offlinePrimaryVerticesSumPt", "sumPt2"),
)
process.ntupleSequence *= process.vertexNtuple

process.tauNtuple = cms.EDProducer("HPlusTauNtupleProducer",
    src = cms.InputTag("patTausHpsPFTauTauTriggerMatched"),
    prefix = cms.string("tau_"),
    tauDiscriminators = cms.vstring(
        "decayModeFinding",
        "byVLooseIsolation",
        "byLooseIsolation",
        "byMediumIsolation",
        "byTightIsolation",
        "againstMuonLoose",
        "againstMuonTight",
        "againstElectronLoose",
        "againstElectronMedium",
        "againstElectronTight",
    ),
    vertexSrc = cms.InputTag("offlinePrimaryVertices"),
    vertexMaxDelta = cms.double(0.001)
)    
process.ntupleSequence *= process.tauNtuple

process.jetNtuple = cms.EDProducer("HPlusJetNtupleProducer",
    src = cms.InputTag("jetSelection"),
    prefix = cms.string("jet_"),
    # The module takes the *maximum* value of the b-discriminators
    # from the input jets, and stores that to the event
    bDiscriminators = cms.vstring("trackCountingHighEffBJetTags")
)
process.ntupleSequence *= process.jetNtuple

process.pfMETNtuple = cms.EDProducer("HPlusMETNtupleProducer",
    src = cms.InputTag("patMETsPF"),
    alias = cms.string("pfMET")
)
process.ntupleSequence *= process.pfMETNtuple


process.ntuplePath = cms.Path(
    process.ntupleSequence
)

################################################################################

process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("ntuplePath")
    ),
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
        "drop *",
        "keep *_pileupNtuple_*_HChSignalAnalysis",
        "keep *_vertexNtuple_*_HChSignalAnalysis",
        "keep *_tauNtuple_*_HChSignalAnalysis",
        "keep *_jetNtuple_*_HChSignalAnalysis",
        "keep *_pfMETNtuple_*_HChSignalAnalysis",
        "keep edmMergeableCounter_*_*_*",
        "drop edmMergeableCounter_*_subcount*_HChSignalAnalysis"
    )
)

# Uncomment the following line to get also the event output (can be
# useful for debugging purposes)
process.outpath = cms.EndPath(process.out)

