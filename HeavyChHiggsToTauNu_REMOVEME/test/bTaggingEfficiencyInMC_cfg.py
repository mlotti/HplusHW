import FWCore.ParameterSet.Config as cms

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion="53XmcS10"
#dataVersion="53Xdata24Aug2012" # Now we have multiple dataVersions for data too, see HChDataVersion for them

dataEras = [
    "Run2012ABCD", # This is the one for pickEvents, and for counter printout in CMSSW job
#    "Run2012ABC", 
#    "Run2012AB",
#    "Run2012A",
#    "Run2012B",
#    "Run2012C",
#    "Run2012D",
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
                        #applyTauTriggerScaleFactor=False,
                        #applyTauTriggerLowPurityScaleFactor=True,
                        #applyMETTriggerScaleFactor=True,
                        #doTriggerMatching=False,
                        #useCHSJets=True,
                        #doQCDTailKillerScenarios=True,
                        #doAgainstElectronScan=True,
                        #doTauIsolationAndJetPUScan=True,
                        doBTagScan=True,
                        #doSystematics=True,
                        histogramAmbientLevel = "Informative", # at least "Informative" required for eff. measurement
                        #doOptimisation=True, optimisationScheme="myOptimisation"
                        )


process = builder.buildSignalAnalysis()

# An example how to use a non-default file(s)
#process.source.fileNames = [
#    "store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_5_3_X/TTJets_TuneZ2star_Summer12/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1/cad8d1056ca20d363262a3efa1d97a74/pattuple_570_1_k4M.root"
#]

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
