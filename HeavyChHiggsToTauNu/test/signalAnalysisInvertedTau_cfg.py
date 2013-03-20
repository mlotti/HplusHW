import FWCore.ParameterSet.Config as cms

# Select the version of the data (needed only for interactice running,
# overridden automatically from multicrab
dataVersion="53XmcS10"
#dataVersion="53Xdata24Aug2012" # Now we have multiple dataVersions for data too, see HChDataVersion for them

dataEras = [
    "Run2012ABC", # This is the one for pickEvents, and for counter printout in CMSSW job
    "Run2012AB",
    "Run2012A",
    "Run2012B",
    "Run2012C",
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
#    signalAnalysis.tauSelection.ptCut = 80.0 #
#    signalAnalysis.MET.METCut = 100.0 
    print "Customisation applied"

from HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration import ConfigBuilder
builder = ConfigBuilder(dataVersion, dataEras,
                        maxEvents=-1, # default is -1
                        customizeLightAnalysis=customize,
                        #applyTriggerScaleFactor=False,
                        #doTriggerMatching=False,
                        #useCHSJets=True,
                        #doAgainstElectronScan=True,
                        doSystematics=False,
                        #histogramAmbientLevel = "Vital",
                        #doOptimisation=True, optimisationScheme=myOptimisation
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
