import FWCore.ParameterSet.Config as cms

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion="44XmcS6"     # Fall11 MC
#dataVersion="44Xdata"    # Run2011 08Nov and 19Nov ReRecos

dataEras = [
    "Run2011AB", # This is the one for pickEvents, and for counter printout in CMSSW job
#    "Run2011A",
#    "Run2011B",
]


# Note: Keep number of variations below 200 to keep file sizes reasonable

def customize(signalAnalysis):
    signalAnalysis.tauSelection.rtauCut = 0.0 # this disables the R_{tau} cut for efficiency measurement (gives better statistics)
    print "Customisations done"

from HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration import ConfigBuilder
builder = ConfigBuilder(dataVersion, dataEras,
                        maxEvents=-1, # default is -1
                        customizeLightAnalysis=customize,
                        #doHeavyAnalysis=True,
                        #customizeHeavyAnalysis=customize,
                        #useCHSJets=True,
                        applyTauTriggerScaleFactor=True,
                        #applyTauTriggerLowPurityScaleFactor=True,
                        #applyMETTriggerScaleFactor=True,
                        #doQCDTailKillerScenarios=True,
                        #doAgainstElectronScan=True,
                        #doTauIsolationAndJetPUScan=True,
                        doBTagScan=True,
                        #doSystematics=True,
                        histogramAmbientLevel = "Informative", # at least "Informative" required for eff. measurement
                        #doOptimisation=True, optimisationScheme="myOptimisation"
                        )


process = builder.buildSignalAnalysis()

if builder.options.tauEmbeddingInput != 0:

    if builder.dataVersion.isMC():
        process.source.fileNames = [
        "/store/group/local/HiggsChToTauNuFullyHadronic/embedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_tauembedding_embedding_v44_5_1_notrg2/b4444849cbd68cba8058d20690fa09f4/embedded_1000_1_M8J.root",
#        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_tauembedding_embedding_v44_5_1_tauhad_vispt30_b/d57ea742826c3abce18a6ceed0c3bca3/embedded_1000_2_vFL.root",
            
            ]
    else:
        # HLT_Mu40_eta2p1_v1
        process.source.fileNames = [
            ]

    #process.maxEvents.input = 10


#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
