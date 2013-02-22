import FWCore.ParameterSet.Config as cms

dataVersion="44XmcS6"     # Fall11 MC

dataEras = [
    "Run2011AB", # This is the one for pickEvents, and for counter printout in CMSSW job
#    "Run2011A",
#    "Run2011B",
]

def customize(analysis):
    analysis.embeddingMuonSrc = "tauEmbeddingMuons"
#    analysis.tauPtCut = 41.0
#    analysis.tauEtaCut = 2.1

from HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration import ConfigBuilder
builder = ConfigBuilder(dataVersion, dataEras,
                        pickEvents=False,
                        maxEvents=1000, # default is -1
                        #doAgainstElectronScan=True,
                        #doSystematics=True,
                        #histogramAmbientLevel = "Vital",
                        #doOptimisation=True, optimisationScheme=myOptimisation
                        )

process = builder.buildEwkBackgroundCoverageAnalysis()

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

f = open("configDump.py", "w")
f.write(process.dumpPython())
f.close()
