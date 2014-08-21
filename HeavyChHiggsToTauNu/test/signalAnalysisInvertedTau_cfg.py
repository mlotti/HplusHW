import FWCore.ParameterSet.Config as cms

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion="53XmcS10"
#dataVersion="53Xdata24Aug2012" # Now we have multiple dataVersions for data too, see HChDataVersion for them

dataEras = [
    "Run2012ABCD", # This is the one for pickEvents, and for counter printout in CMSSW job
#    "Run2012ABC",
    "Run2012AB",
#    "Run2012A",
#    "Run2012B",
    "Run2012C",
    "Run2012D",
#    "Run2011AB", # This is the one for pickEvents, and for counter printout in CMSSW job
#    "Run2011A",
#    "Run2011B",
]


# Note: Keep number of variations below 200 to keep file sizes reasonable


def customize(signalAnalysis):
    # Set here splitting of phase space (underflow bin will be automatically added; last value is edge for overflow bin)
    signalAnalysis.commonPlotsSettings.histogramSplitting.splitHistogramByTauPtBinLowEdges = cms.untracked.vdouble(50., 60., 70., 80., 100., 120., 150.)
    #signalAnalysis.commonPlotsSettings.histogramSplitting.splitHistogramByTauEtaBinLowEdges = cms.untracked.vdouble(-1.5, 1.5)
    #signalAnalysis.commonPlotsSettings.histogramSplitting.splitHistogramByNVerticesBinLowEdges = cms.untracked.vint32(10)
    #signalAnalysis.commonPlotsSettings.histogramSplitting.splitHistogramByDeltaPhiTauMetInDegrees = cms.untracked.vdouble(90.) # If used, one could disable collinear cuts
    #signalAnalysis.QCDTailKiller.disableCollinearCuts = True # enable, if splitting by delta phi(tau,MET)
    print "Phase space is splitted in analysis as follows:"
    print signalAnalysis.commonPlotsSettings.histogramSplitting
    
    #signalAnalysis.bMakeEtaCorrectionStatus = True
    #signalAnalysis.lowBoundForQCDInvertedIsolation = "byVLooseCombinedIsolationDeltaBetaCorr"
    print "QCD corrections to inverted leg are applied status:",signalAnalysis.makeQCDEtaCorrectionStatus
    signalAnalysis.tauSelection.tauDecayModeReweightingZero = 1.0
    signalAnalysis.tauSelection.tauDecayModeReweightingOne = 1.0 # set to 0.88 according to Christian (HIG-13-004)
    signalAnalysis.tauSelection.tauDecayModeReweightingOther = 1.0
    
    if len(signalAnalysis.lowBoundForQCDInvertedIsolation.value()):
        print "Applying low bound for QCD inverted isolation in addition to inverting the isolation, low bound=",signalAnalysis.lowBoundForQCDInvertedIsolation.value()

    signalAnalysis.bTagging.subleadingDiscriminatorCut = 0.244
    #signalAnalysis.MET.METCut = 50.0
    #signalAnalysis.MET.preMETCut = 30.0
    print "Customisation applied"

from HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration import ConfigBuilder
builder = ConfigBuilder(dataVersion, dataEras,
                        maxEvents=-1, # default is -1
                        customizeLightAnalysis=customize,
                        doQCDTailKillerScenarios=True,
                        applyTauTriggerScaleFactor=True,
                        #applyTauTriggerLowPurityScaleFactor=True,
                        #applyMETTriggerScaleFactor=True,
                        #doAgainstElectronScan=True,

                        doSystematics=False,

                        #histogramAmbientLevel = "Vital",
                        #doOptimisation=True, optimisationScheme="metScenarios",
                        #doOptimisation=True, optimisationScheme="jetScenarios",
                        #doOptimisation=True, optimisationScheme="btagSymmetricScenarios",
                        #doOptimisation=True, optimisationScheme="myOptimisation"
                        )


process = builder.buildSignalAnalysisInvertedTau()

# An example how to use a non-default file(s)
#process.source.fileNames = [
#    "store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_5_3_X/TTJets_TuneZ2star_Summer12/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X_PU_S10_START53_V7A_v1_AODSIM_pattuple_v53_1/cad8d1056ca20d363262a3efa1d97a74/pattuple_570_1_k4M.root"
#]

if builder.options.tauEmbeddingInput != 0:

    if builder.dataVersion.isMC():
        process.source.fileNames = [
            ]
    else:
        # HLT_Mu40_eta2p1_v1
        process.source.fileNames = [
            "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/SingleMu_Mu_173693-177452_2011B_Nov19/SingleMu/Run2011B_19Nov2011_v1_AOD_173693_tauembedding_embedding_v44_4_2_seed0/a55cb9805ad247805760f23e605c41e5/embedded_9_1_ccy.root",
            "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/SingleMu_Mu_173693-177452_2011B_Nov19/SingleMu/Run2011B_19Nov2011_v1_AOD_173693_tauembedding_embedding_v44_4_2_seed0/a55cb9805ad247805760f23e605c41e5/embedded_99_1_Wje.root",
            "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/SingleMu_Mu_173693-177452_2011B_Nov19/SingleMu/Run2011B_19Nov2011_v1_AOD_173693_tauembedding_embedding_v44_4_2_seed0/a55cb9805ad247805760f23e605c41e5/embedded_98_1_Qmf.root",
            ]

    #process.maxEvents.input = 10


#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
