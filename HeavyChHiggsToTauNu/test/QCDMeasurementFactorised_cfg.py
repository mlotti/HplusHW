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
]

# Note: Keep number of variations below 200 to keep file sizes reasonable
# Note: Currently it is not possible to vary the tau selection -related variables, because only one JES and MET producer is made (tau selection influences type I MET correction and JES)

### Boolean flags
bCustomizeTailKiller = False

def customize(signalAnalysis):
    # Choice of tau selection for tau candidate selection
    signalAnalysis.applyNprongsCutForTauCandidate = False
    signalAnalysis.applyRtauCutForTauCandidate = False
    # Splitting of analysis phase space (note that first bin is below the first number and last bin is greater than the last number)
    signalAnalysis.commonPlotsSettings.histogramSplitting.splitHistogramByTauPtBinLowEdges = cms.untracked.vdouble(50., 60., 70., 80., 100., 120., 150.)
    #signalAnalysis.commonPlotsSettings.histogramSplitting.splitHistogramByTauEtaBinLowEdges = cms.untracked.vdouble(-1.5, 1.5)
    #signalAnalysis.commonPlotsSettings.histogramSplitting.splitHistogramByNVerticesBinLowEdges = cms.untracked.vint32(10)
    #signalAnalysis.commonPlotsSettings.histogramSplitting.splitHistogramByDeltaPhiTauMetInDegrees = cms.untracked.vdouble(90.) # If used, one could disable collinear cuts
    #signalAnalysis.QCDTailKiller.disableCollinearCuts = True # enable, if splitting by delta phi(tau,MET)
    print "Phase space is splitted in analysis as follows:"
    print signalAnalysis.commonPlotsSettings.histogramSplitting
    # Variation options
    signalAnalysis.analysisMode = cms.untracked.string("traditional") # options: "traditional", "ABCD"
    # MET cut
    #signalAnalysis.MET.METCut = 60.0
    signalAnalysis.MET.METCut = 50.0
    #signalAnalysis.MET.preMETCut = 30.0
    signalAnalysis.MET.doTypeICorrectionForPossiblyIsolatedTaus = "always"
    # Tail-Killer 
    if bCustomizeTailKiller:
        from HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff import QCDTailKillerBin
        signalAnalysis.QCDTailKiller.maxJetsToConsider = cms.untracked.uint32(4)
        # Back-To-Back
        signalAnalysis.QCDTailKiller.backToBack = cms.untracked.VPSet(
            QCDTailKillerBin("circular", 60.0, 60.0), # jet 1
            QCDTailKillerBin("circular", 60.0, 60.0), # jet 2
            QCDTailKillerBin("circular", 60.0, 60.0), # jet 3
            QCDTailKillerBin("noCut", 0.0, 0.0), # jet 4
            )
        # Collinear
        signalAnalysis.QCDTailKiller.collinear = cms.untracked.VPSet(
            QCDTailKillerBin("triangular", 40.0, 40.0), # jet 1
            QCDTailKillerBin("triangular", 40.0, 40.0), # jet 2
            QCDTailKillerBin("triangular", 40.0, 40.0), # jet 3
            QCDTailKillerBin("noCut", 0.0, 0.0), # jet 4
            )

    # Info    
    print "\n*** QCD factorised customisations applied ***"
    print "- Nprongs cut included in tau candidate selections:",signalAnalysis.applyNprongsCutForTauCandidate.value()
    print "- Rtau cut included in tau candidate selections:",signalAnalysis.applyRtauCutForTauCandidate.value()
    print "- Analysis method used:",signalAnalysis.analysisMode.value()
    print "- MET cut:",signalAnalysis.MET.METCut.value()
    print "- pre-MET cut:",signalAnalysis.MET.preMETCut.value()
    print "- Tail-Killer:", signalAnalysis.QCDTailKiller
    
from HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration import ConfigBuilder
builder = ConfigBuilder(dataVersion, dataEras,
                        maxEvents=1000, # default is -1
                        customizeLightAnalysis=customize,
                        #doHeavyAnalysis=True,
                        #customizeHeavyAnalysis=customize,
                        #useCHSJets=True,
                        applyTauTriggerScaleFactor=True,
                        #applyTauTriggerLowPurityScaleFactor=True,
                        #applyMETTriggerScaleFactor=True,
                        tauSelectionOperatingMode="tauCandidateSelectionOnly",
                        #doSystematics=True,
                        #doQCDTailKillerScenarios=True,
                        doFillTree=False,
                        #histogramAmbientLevel = "Vital", # Informative by default
                        #doOptimisation=True, optimisationScheme="myOptimisation"
                        )

process = builder.buildQCDMeasurementFactorised()

if builder.options.tauEmbeddingInput != 0:
    process.source.fileNames = [
        #"file:/mnt/flustre/wendland/embedded_latest.root"
        "file:/home/wendland/v25_embed/CMSSW_4_4_4/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/tauEmbedding/embedded.root"
        # For testing data
        #"/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/SingleMu_Mu_160431-163261_2011A_Nov08/SingleMu/Tauembedding_embedding_v44_2_SingleMu_Mu_160431-163261_2011A_Nov08/c7fbae985f4002d5d76ea04408a27e38/embedded_1_1_Lka.root"
        ]
    process.maxEvents.input = 10

f = open("configDump.py", "w")
f.write(process.dumpPython())
f.close()
