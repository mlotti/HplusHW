import FWCore.ParameterSet.Config as cms
 
# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion="53XmcS10"
#dataVersion="53Xdata24Aug2012" # Now we have multiple dataVersions for data too, see HChDataVersion for them
 
dataEras = [
    "Run2012ABCD", # This is the one for pickEvents, and for counter printout in CMSSW job
    "Run2012ABC", 
    "Run2012AB",
#    "Run2012A",
#    "Run2012B",
    "Run2012C",
    "Run2012D",
]


# Note: Keep number of variations below 200 to keep file sizes reasonable

def customize(signalAnalysis):
#    signalAnalysis.jetSelection.jetPileUpWorkingPoint = "tight" # 
#    signalAnalysis.tauSelection.ptCut = 80.0 #
#    signalAnalysis.MET.METCut = 100.0
#    signalAnalysis.MET.preMETCut = 30.0
#    signalAnalysis.QCDTailKiller.disableCollinearCuts = True
    # Example for setting a certain tail killer scenario for the nominal module
    #import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
    #signalAnalysis.QCDTailKiller = param.QCDTailKillerMediumPlus.clone()

    # Disable trigger, and weight events by trigger MC efficiencies
    # signalAnalysis.trigger.selectionType = "disabled"
    # signalAnalysis.tauTriggerEfficiencyScaleFactor.mode = "mcEfficiency"
    # signalAnalysis.tauTriggerEfficiencyScaleFactor.dataSelect = ["runs_190456_208686"]
    # signalAnalysis.MET.preMETCut = 20
    # signalAnalysis.metTriggerEfficiencyScaleFactor.mode = "mcEfficiency"
    # signalAnalysis.metTriggerEfficiencyScaleFactor.dataSelect = ["runs_190456_208686"]

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
                        #doBTagScan=True,
                        #doSystematics=True,
                        #histogramAmbientLevel = "Vital",
                        #doOptimisation=True, optimisationScheme="metScenarios",
                        #doOptimisation=True, optimisationScheme="jetScenarios",
                        #doOptimisation=True, optimisationScheme="btagSymmetricScenarios",
                        #doOptimisation=True, optimisationScheme="myOptimisation",
                        )

process = builder.buildSignalAnalysis()

# An example how to use a non-default file(s)
#process.source.fileNames = [
#    "store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_5_3_X/TTJets_TuneZ2star_Summer12/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1/cad8d1056ca20d363262a3efa1d97a74/pattuple_570_1_k4M.root"
#]

if builder.options.tauEmbeddingInput != 0:

    if builder.dataVersion.isMC():
        process.source.fileNames = [
            "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_5_3_X/TTJets_TuneZ2star_Summer12/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_tauembedding_embedding_v53_3b/1af76047aea9759528c81258e6b8769f/embedded_100_1_y9H.root"
            ]
    else:
        # HLT_Mu40_eta2p1_v1
        process.source.fileNames = [
            "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_5_3_X/SingleMu_207214-208686_2012D_Jan22/SingleMu/Run2012D_22Jan2013_v1_AOD_207214_208686_tauembedding_embedding_v53_3b/82ba5743f53794eef04b654ef0f32265/embedded_1000_1_1rY.root"
            ]

    #process.maxEvents.input = 10


#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
