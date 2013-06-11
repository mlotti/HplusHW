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
#myOptimisation.addDeltaPhiVariation([180.0,160.0,140.0])
#myOptimisation.addTopRecoVariation(["None","chi"]) # Valid options: None, chi, std, Wselection
#myOptimisation.disableMaxVariations()

def customize(signalAnalysis):
    print "Customisation applied"
   # signalAnalysis.MET.METCut = 50.
    
    
from HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration import ConfigBuilder
builder = ConfigBuilder(dataVersion, dataEras,
                        maxEvents=-1, # default is -1
                        customizeLightAnalysis=customize,
                        doQCDTailKillerScenarios=True,
                        #doAgainstElectronScan=True,
                        #doSystematics=True,
                        #histogramAmbientLevel = "Vital",
                        #doOptimisation=True, optimisationScheme=myOptimisation
                        )

process = builder.buildSignalAnalysisInvertedTau()


#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
