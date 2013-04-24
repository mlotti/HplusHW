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

from HiggsAnalysis.HeavyChHiggsToTauNu.OptimisationScheme import HPlusOptimisationScheme
myOptimisation = HPlusOptimisationScheme()
#myOptimisation.addTauPtVariation([40.0, 50.0])
#myOptimisation.addTauIsolationVariation([])
#myOptimisation.addTauIsolationContinuousVariation([])
#myOptimisation.addRtauVariation([0.0, 0.7])
#myOptimisation.addJetNumberSelectionVariation(["GEQ3", "GEQ4"])
#myOptimisation.addJetEtVariation([20.0, 30.0])
#myOptimisation.addJetBetaVariation(["GT0.0","GT0.5","GT0.7"])
#myOptimisation.addMETSelectionVariation([50.0, 60.0, 70.0])
#myOptimisation.addBJetLeadingDiscriminatorVariation([0.898, 0.679])
#myOptimisation.addBJetSubLeadingDiscriminatorVariation([0.679, 0.244])
#myOptimisation.addBJetEtVariation([])
#myOptimisation.addBJetNumberVariation(["GEQ1", "GEQ2"])
#myOptimisation.addDeltaPhiVariation([180.0,160.0,140.0])
#myOptimisation.addTopRecoVariation(["None","chi"]) # Valid options: None, chi, std, Wselection
#myOptimisation.disableMaxVariations()

def customize(signalAnalysis):
    # Choice of tau selection for tau candidate selection
    signalAnalysis.applyNprongsCutForTauCandidate = False
    signalAnalysis.applyRtauCutForTauCandidate = False
    # Binning of factorisation (note that first bin is below the first number and last bin is greater than the last number)
    signalAnalysis.factorisationTauPtBinLowEdges = cms.untracked.vdouble(50., 60., 70., 80., 100., 120., 150., 200., 300.)
    signalAnalysis.factorisationTauEtaBinLowEdges = cms.untracked.vdouble(-1.5, 1.5) # probably need to constrain to -1.5, 1.5, i.e. endcap-, barrel, endcap+
    signalAnalysis.factorisationNVerticesBinLowEdges = cms.untracked.vint32(10)
    # Variation options
    signalAnalysis.doAnalysisVariationWithTraditionalMethod = True
    signalAnalysis.doAnalysisVariationWithABCDMethod = False
    signalAnalysis.doAnalysisVariationWithDoubleABCDMethod = False
    # MET cut
    #signalAnalysis.MET.METCut = 60.0
    #signalAnalysis.MET.METCut = 50.0
    # Info
    print "\n*** QCD factorised customisations applied ***"
    print "- Nprongs cut included in tau candidate selections:",signalAnalysis.applyNprongsCutForTauCandidate.value()
    print "- Rtau cut included in tau candidate selections:",signalAnalysis.applyRtauCutForTauCandidate.value()
    print "- Traditional method used:",signalAnalysis.doAnalysisVariationWithTraditionalMethod.value()
    print "- ABCD method (experimental) used:",signalAnalysis.doAnalysisVariationWithABCDMethod.value()
    print "- Double ABCD method (very experymental) used:",signalAnalysis.doAnalysisVariationWithDoubleABCDMethod.value()
    print "- MET cut:",signalAnalysis.MET.METCut.value()

from HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration import ConfigBuilder
builder = ConfigBuilder(dataVersion, dataEras,
                        maxEvents=1000, # default is -1
                        customizeLightAnalysis=customize,
                        #doHeavyAnalysis=True,
                        #customizeHeavyAnalysis=customize,
                        tauSelectionOperatingMode="tauCandidateSelectionOnly",
                        customizeAnalysis=customize,
                        #doAgainstElectronScan=True,
                        #doSystematics=True,
                        doQCDTailKillerScenarios=True,
                        histogramAmbientLevel = "Informative", # Vital
                        #doOptimisation=True, optimisationScheme=myOptimisation
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
