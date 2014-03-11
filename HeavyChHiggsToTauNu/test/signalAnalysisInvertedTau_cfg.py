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
    print "QCD corrections to inverted leg are applied status:",signalAnalysis.bMakeEtaCorrectionStatus

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
                        #doSystematics=True,
                        #histogramAmbientLevel = "Vital",
                        #doOptimisation=True, optimisationScheme="metScenarios",
                        #doOptimisation=True, optimisationScheme="jetScenarios",
                        #doOptimisation=True, optimisationScheme="btagSymmetricScenarios",
                        #doOptimisation=True, optimisationScheme="myOptimisation"
                        )

process = builder.buildSignalAnalysisInvertedTau()


#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
