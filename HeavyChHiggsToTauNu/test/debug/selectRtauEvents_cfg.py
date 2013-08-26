import FWCore.ParameterSet.Config as cms

process = cms.Process("SELECTRTAU")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string("START38_V9::All")

process.source = cms.Source('PoolSource',
#    skipEvents = cms.untracked.uint32(500),
    fileNames = cms.untracked.vstring(
    "/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/FEFEE1D1-F17B-DF11-B911-00304867C16A.root"
  )
)

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.TFileService.fileName = "histograms.root"

process.goodTaus = cms.EDFilter("PFTauSelector",
    src = cms.InputTag("fixedConePFTauProducer"),
    cut = cms.string("et() > 40 && leadTrack().isNonnull() && leadTrack().pt() > 20."),
    discriminators = cms.VPSet(
        cms.PSet(discriminator=cms.InputTag("fixedConePFTauDiscriminationByIsolation"), selectionCut=cms.double(0.5)),
        cms.PSet(discriminator=cms.InputTag("fixedConePFTauDiscriminationAgainstElectron"), selectionCut=cms.double(0.5)),
        cms.PSet(discriminator=cms.InputTag("fixedConePFTauDiscriminationAgainstMuon"), selectionCut=cms.double(0.5))
    )
)

process.goodTausFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("goodTaus"),
    minNumber = cms.uint32(1)
)

process.rtau = cms.EDAnalyzer("CandViewHistoAnalyzer",
    src = cms.InputTag("goodTaus"),
    histograms = cms.VPSet(
        cms.PSet(
            min = cms.untracked.double(0.),
            max = cms.untracked.double(2.),
            nbins = cms.untracked.int32(100),
            name = cms.untracked.string("rtau"),
            plotquantity = cms.untracked.string("leadTrack().pt() / et()"),
            description = cms.untracked.string("leadTrack().pt() / et()"),
            lazyParsing = cms.untracked.bool(True)
        )
    )
)

process.selectedTaus = cms.EDFilter("PFTauSelector",
    src = cms.InputTag("goodTaus"),
    cut = cms.string("leadTrack().pt() / et() > 1.0"),
    discriminators = cms.VPSet()
)

process.selectedTausFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("selectedTaus"),
    minNumber = cms.uint32(1)
)

process.selection = cms.Path(
    process.goodTaus *
    process.goodTausFilter *
    process.rtau *
    process.selectedTaus *
    process.selectedTausFilter
)

################################################################################

process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("selection")
    ),
    fileName = cms.untracked.string('output.root'),
    outputCommands = cms.untracked.vstring(
        "keep *",
	"drop *_goodTaus_*_*",
    )
)
process.outpath = cms.EndPath(process.out)
