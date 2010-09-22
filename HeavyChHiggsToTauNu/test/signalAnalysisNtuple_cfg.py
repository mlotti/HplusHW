import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions

options = getOptions()

process = cms.Process("HChSignalAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string("START38_V9::All")

process.source = cms.Source('PoolSource',
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
#    skipEvents = cms.untracked.uint32(500),
    fileNames = cms.untracked.vstring(
# For testing in lxplus
        "rfio:/castor/cern.ch/user/m/mkortela/hplus/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola_Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v2/pattuple_6_1_MSU.root"
# For testing in jade
        #"/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/TTToHpmToTauNu_M100/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v2/d538bad796104165ef547eb8f3e812a0/pattuple_6_1_MSU.root"
        #"dcap://madhatter.csc.fi:22125/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_3_8_X/TTToHpmToTauNu_M100/TTToHpmToTauNu_M-100_7TeV-pythia6-tauola/Spring10_START3X_V26_v1_GEN-SIM-RECO-pattuple_v2/d538bad796104165ef547eb8f3e812a0/pattuple_6_1_MSU.root"
  )
)

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.categories.append("EventCounts")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
process.TFileService.fileName = "histograms.root"

process.signalAnalysisNtuple = cms.EDFilter("HPlusSignalAnalysisNtupleProducer",
    branchAliasPrefix = cms.untracked.string(""),
    tauSelection = cms.untracked.PSet(
        src = cms.untracked.InputTag("patPFTauProducerFixedCone"),
        #src = cms.untracked.InputTag("selectedPatTaus"),
        ptCut = cms.untracked.double(20),
        etaCut = cms.untracked.double(2.4),
        leadingTrackPtCut = cms.untracked.double(10)
    ),
    tauDiscriminators = cms.untracked.VPSet(
        cms.untracked.PSet(
            discriminator = cms.untracked.string("HChTauIDtauPolarizationCont"),
            branch = cms.untracked.string("discrHChTauIDtauPolarizationCont")
        )
    ),
    jetSelection = cms.untracked.PSet(
        src = cms.untracked.InputTag("selectedPatJets"),
#        src = cms.untracked.InputTag("selectedPatJetsAK5JPT"),
        cleanTauDR = cms.untracked.double(0.5),
        ptCut = cms.untracked.double(20),
        etaCut = cms.untracked.double(2.4),
        minNumber = cms.untracked.uint32(3)
    ),
    btags = cms.untracked.vstring("trackCountingHighEffBJetTags"),
    METs = cms.untracked.VPSet(
       cms.untracked.PSet(
          src = cms.untracked.InputTag("patMETs"),
          label = cms.untracked.string("caloMET"),
       ),
       cms.untracked.PSet(
          src = cms.untracked.InputTag("patMETsPF"),
          label = cms.untracked.string("pfMET"),
       ),
       cms.untracked.PSet(
          src = cms.untracked.InputTag("patMETsTC"),
          label = cms.untracked.string("tcMET"),
       )
    )
)
process.allEvents = cms.EDProducer("EventCountProducer")
process.ntupleEvents = cms.EDProducer("EventCountProducer")
process.ntuplePath = cms.Path(
    process.allEvents *
    process.signalAnalysisNtuple *
    process.ntupleEvents
)

################################################################################

process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("ntuplePath")
    ),
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
        "keep *_*_*_HChSignalAnalysis",
        "drop *_counterNames_*_*",
        "drop *_counterInstances_*_*",
        "drop edmMergeableCounter_*_subcount*_*"
#	"drop *",
#        "keep edmMergeableCounter_*_*_*"
    )
)

# Uncomment the following line to get also the event output (can be
# useful for debugging purposes)
process.outpath = cms.EndPath(process.out)

