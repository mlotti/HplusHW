import FWCore.ParameterSet.Config as cms

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion="44XmcS6"     # Fall11 MC
#dataVersion="44Xdata"    # Run2011 08Nov and 19Nov ReRecos

dataEras = [
    "Run2011AB", # This is the one for pickEvents, and for counter printout in CMSSW job
    "Run2011A",
    "Run2011B",
]


# Note: Keep number of variations below 200 to keep file sizes reasonable

from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme
myOptimisation = HPlusOptimisationScheme()

#myOptimisation.addTauPtVariation([40.0, 50.0, 60.0, 70., 80.])
#myOptimisation.addTauIsolationVariation([])
#myOptimisation.addTauIsolationContinuousVariation([])
#myOptimisation.addRtauVariation([0.0, 0.7, 0.8])
#myOptimisation.addJetNumberSelectionVariation(["GEQ3", "GEQ4"])
#myOptimisation.addJetEtVariation([20.0, 30.0])
#myOptimisation.addJetBetaVariation(["GT0.0","GT0.5","GT0.7"])
myOptimisation.addMETSelectionVariation([60.0, 70.0, 80.0, 90.,100.0])
#myOptimisation.addBJetLeadingDiscriminatorVariation([0.898, 0.679])
#myOptimisation.addBJetSubLeadingDiscriminatorVariation([0.679, 0.244])
#myOptimisation.addBJetEtVariation([])
#myOptimisation.addBJetNumberVariation(["GEQ1", "GEQ2"])
#myOptimisation.addDeltaPhiVariation([180.0,170.0,160.0,150.0])
#myOptimisation.addTopRecoVariation(["None","chi"]) # Valid options: None, chi, std, Wselection
#myOptimisation.disableMaxVariations()

def customize(signalAnalysis):
    # Apply beta cut for jets to reject PU jets
    signalAnalysis.jetSelection.betaCut = 0.2 # Disable by setting to 0.0; if you want to enable, set to 0.2

from HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisInvertedTauConfiguration import ConfigBuilder
builder = ConfigBuilder(dataVersion, dataEras,
                        maxEvents=-1, # default is -1
                        customizeAnalysis=customize,
                        #doAgainstElectronScan=True,
                        #doSystematics=True,
                        #histogramAmbientLevel = "Vital",
                        #doOptimisation=True, optimisationScheme=myOptimisation
                        )


process = builder.buildSignalAnalysis()


if builder.options.tauEmbeddingInput != 0:
    process.source.fileNames = [
        #"file:embedded.root"
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Tauembedding_embedding_v44_4_1_muiso0_TTJets_TuneZ2_Fall11/50da2d6a5b0c9c8a2f96f633ada0c1c6/embedded_1_1_GcS.root",
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Tauembedding_embedding_v44_4_1_muiso0_TTJets_TuneZ2_Fall11/50da2d6a5b0c9c8a2f96f633ada0c1c6/embedded_2_1_rhV.root",
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Tauembedding_embedding_v44_4_1_muiso0_TTJets_TuneZ2_Fall11/50da2d6a5b0c9c8a2f96f633ada0c1c6/embedded_3_1_aXd.root",
        # For testing data
        ]


    #process.maxEvents.input = 10


#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
