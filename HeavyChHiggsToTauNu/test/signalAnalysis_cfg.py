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
#myOptimisation.printOptions() # Uncomment to find out the implemented methods
#myOptimisation.addTauPtVariation([40.0, 50.0, 60.0, 70., 80.])
#myOptimisation.addTauIsolationVariation([])
#myOptimisation.addTauIsolationContinuousVariation([])
#myOptimisation.addRtauVariation([0.0, 0.7, 0.8])
#myOptimisation.addJetNumberSelectionVariation(["GEQ3", "GEQ4"])
#myOptimisation.addJetEtVariation([20.0, 30.0])
#myOptimisation.addJetBetaVariation(["GT0.0","GT0.5","GT0.7"])
#myOptimisation.addMETSelectionVariation([60.0, 70.0, 80.0, 90.,100.0])
#myOptimisation.addBJetLeadingDiscriminatorVariation([0.898, 0.679])
#myOptimisation.addBJetSubLeadingDiscriminatorVariation([0.679, 0.244])
#myOptimisation.addBJetEtVariation([])
#myOptimisation.addBJetNumberVariation(["GEQ1", "GEQ2"])
#myOptimisation.addDeltaPhiVariation([180.0,170.0,160.0,150.0])
#myOptimisation.addTopRecoVariation(["None"]) # Valid options: None, chi, std, Wselection

def customize(signalAnalysis):
    # Apply beta cut for jets to reject PU jets
#    signalAnalysis.jetSelection.jetPileUpWorkingPoint = "tight" # 
#    signalAnalysis.tauSelection.ptCut = 80.0 #
#    signalAnalysis.MET.METCut = 100.0
#    signalAnalysis.MET.preMETCut = 30.0
    # Example for setting a certain tail killer scenario for the nominal module
    #import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
    #signalAnalysis.QCDTailKiller = param.QCDTailKillerMediumPlus.clone()

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
                        #doInvariantMassReconstructionScenarios=True,
                        #doAgainstElectronScan=True,
                        #doTauIsolationAndJetPUScan=True,
                        #doBTagScan=True,
                        #doSystematics=True,
                        #histogramAmbientLevel = "Vital",
                        #doOptimisation=True, optimisationScheme=myOptimisation
                        )


process = builder.buildSignalAnalysis()

process.source.fileNames = [
    #"file:skim_TTJetsFall11.root"
    "file:TTToHplusBWB_M-120_7TeV-pythia6-tauola_pattuple_v44_5_10_1_zI8.root"
    ]

if builder.options.tauEmbeddingInput != 0:

    if builder.dataVersion.isMC():
        process.source.fileNames = [
            "file:skim_TTJetsFall11.root"
            #        "/store/group/local/HiggsChToTauNuFullyHadronic/embedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_tauembedding_embedding_v44_5_1_notrg2/b4444849cbd68cba8058d20690fa09f4/embedded_1000_1_M8J.root",
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
