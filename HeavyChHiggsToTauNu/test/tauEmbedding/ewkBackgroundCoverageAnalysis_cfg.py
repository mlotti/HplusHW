import FWCore.ParameterSet.Config as cms

dataVersion="44XmcS6"     # Fall11 MC

dataEras = [
    "Run2011AB", # This is the one for pickEvents, and for counter printout in CMSSW job
#    "Run2011A",
#    "Run2011B",
]

def customize(analysis):
    analysis.trigger.selectionType = "disabled"

#    analysis.embeddingMuonSrc = "tauEmbeddingMuons"
#    analysis.tauPtCut = 41.0
#    analysis.tauEtaCut = 2.1

from HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration import ConfigBuilder
builder = ConfigBuilder(dataVersion, dataEras,
                        pickEvents=False,
#                        maxEvents=1000, # default is -1
                        customizeLightAnalysis=customize,
                        #doAgainstElectronScan=True,
                        #doSystematics=True,
                        histogramAmbientLevel = "Systematics",
                        #doOptimisation=True, optimisationScheme=myOptimisation
                        )

process = builder.buildEwkBackgroundCoverageAnalysis()

if builder.options.doPat != 0:
    process.source.fileNames = ["file:/mnt/flustre/wendland/AODSIM_PU_S6_START44_V9B_7TeV/Fall11_TTJets_TuneZ2_7TeV-madgraph-tauola_AODSIM_PU_S6_START44_V9B-v1_testfile.root"]

    # We want some kind of preselection before running PAT
    import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations
    import HiggsAnalysis.HeavyChHiggsToTauNu.ewkBackgroundCoverageAnalysis as ewkBackgroundCoverageAnalysis
    s = cms.Sequence()
    process.preGenTausSequence = s
    process.preGenTausAllEvents = cms.EDProducer("EventCountProducer")
    s *= process.preGenTausAllEvents

    process.preGenTaus = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("genParticles"),
        cut = cms.string(customisations.generatorTauSelection % ewkBackgroundCoverageAnalysis.genTauPtCut)
    )
    s *= process.preGenTaus
    process.preGenTausFilter = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag("preGenTaus"),
        minNumber = cms.uint32(1),
    )
    s *= process.preGenTausFilter

    process.preGenTausSelected = cms.EDProducer("EventCountProducer")
    s *= process.preGenTausSelected

    process.eventPreSelection *= s

    # Update counters
    for name in builder.getAnalyzerModuleNames():
        module = getattr(process, name)
        module.eventCounter.counters.extend([
                cms.InputTag("preGenTausAllEvents"),
                cms.InputTag("preGenTausSelected")
                ])
    


import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF as muonSelection
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.PFEmbeddingSource_cff as PFEmbeddingSource

process.tightMuons = muonSelection.getTightMuonsDefinition()
process.tightenedMuons = PFEmbeddingSource.tightenedMuons.clone()
process.tightenedMuonsWithIso = PFEmbeddingSource.tightenedMuonsWithIso.clone()
process.tauEmbeddingMuons = PFEmbeddingSource.tauEmbeddingMuons.clone()
process.commonSequence *= (
    process.tightMuons *
    process.tightenedMuons *
    process.tightenedMuonsWithIso *
    process.tauEmbeddingMuons
)

f = open("configDumpEwkBackgroundCoverage.py", "w")
f.write(process.dumpPython())
f.close()
