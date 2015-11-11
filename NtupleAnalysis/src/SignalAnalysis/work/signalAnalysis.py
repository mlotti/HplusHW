#!/usr/bin/env python

dataEras = ["2015"]
#dataEras = ["2015B","2015C"]
searchModes = ["80to1000"]

from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer

process = Process("SignalAnalysis")

# Example of adding a dataset which has its files defined in data/<dataset_name>.txt file
#process.addDatasets(["TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6"])

# Example of adding datasets from a multicrab directory
import sys
if len(sys.argv) < 2:
    print "Usage: ./exampleAnalysis.py <path-to-multicrab-directory>"
    sys.exit(0)
process.addDatasetsFromMulticrab(sys.argv[1])

# Add config
from HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import allSelections

#allSelections.TauSelection.rtau = 0.0
allSelections.TauSelection.prongs = 123
allSelections.TauSelection.againstElectronDiscr = "againstElectronLooseMVA5"
allSelections.TauSelection.againstMuonDiscr = "againstMuonLoose3"
allSelections.AngularCutsCollinear.cutValueJet1 = 0.0
allSelections.AngularCutsCollinear.cutValueJet2 = 0.0
allSelections.AngularCutsCollinear.cutValueJet3 = 0.0
allSelections.AngularCutsCollinear.cutValueJet4 = 0.0
allSelections.JetSelection.jetType = "JetsPuppi"
#allSelections.BJetSelection.numberOfBJetsCutValue = 0
#allSelections.BJetSelection.numberOfBJetsCutDirection = "=="
allSelections.BJetSelection.bjetDiscrWorkingPoint = "Loose"
allSelections.METSelection.METCutValue = 80.0
allSelections.METSelection.METType = "MET_Puppi"
allSelections.AngularCutsBackToBack.cutValueJet1 = 0.0
allSelections.AngularCutsBackToBack.cutValueJet2 = 0.0
allSelections.AngularCutsBackToBack.cutValueJet3 = 0.0
allSelections.AngularCutsBackToBack.cutValueJet4 = 0.0

# Build analysis modules
from HiggsAnalysis.NtupleAnalysis.AnalysisBuilder import AnalysisBuilder
builder = AnalysisBuilder("SignalAnalysis", 
                          dataEras,
                          searchModes,
                          #### Options ####
                          #doSystematicVariations=True,
                          usePUreweighting=False
                          )
#builder.addVariation()
builder.build(process, allSelections)

# Example of adding an analyzer whose configuration depends on dataVersion
#def createAnalyzer(dataVersion):
    #a = Analyzer("ExampleAnalysis")
    #if dataVersion.isMC():
        #a.tauPtCut = 10
    #else:
        #a.tauPtCut = 20
    #return a
#process.addAnalyzer("test2", createAnalyzer)

# Pick events
#process.addOptions(EventSaver = PSet(enabled = True,pickEvents = True))

# Run the analysis
if "proof" in sys.argv:
    process.run(proof=True)
else:
    process.run()

# Run the analysis with PROOF
# By default it uses all cores, but you can give proofWorkers=<N> as a parameter
#process.run(proof=True)
