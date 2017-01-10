#!/usr/bin/env python

dataEras = ["2016"]
#dataEras = ["2015B","2015C"]
searchModes = ["80to1000"]

import sys
from HiggsAnalysis.NtupleAnalysis.main import Process, PSet, Analyzer

process = Process("BTagEfficiencyAnalysis")

# Blaclist signal samples
blacklist = ["ChargedHiggs_HplusTB","ChargedHiggs_TTToHplusBWB"]
process.addDatasetsFromMulticrab(sys.argv[1],blacklist=blacklist)


# Example of adding a dataset which has its files defined in data/<dataset_name>.txt file
#process.addDatasets(["TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6"])

# Example of adding datasets from a multicrab directory
import sys
if len(sys.argv) < 2:
    print "Usage: ./btagEfficiencyAnalysis.py <path-to-multicrab-directory>"
    sys.exit(0)
process.addDatasetsFromMulticrab(sys.argv[1])

# Add config
from HiggsAnalysis.NtupleAnalysis.parameters.signalAnalysisParameters import allSelections
# Disable rtau
allSelections.TauSelection.prongs = 1
allSelections.TauSelection.rtau = 0.0
allSelections.__setattr__("jetPtCutMin", 0.0)
allSelections.__setattr__("jetPtCutMax", 99990.0)
allSelections.__setattr__("jetEtaCutMin", -2.5)
allSelections.__setattr__("jetEtaCutMax", 2.5)

#for algo in ["combinedInclusiveSecondaryVertexV2BJetTags"]:
#    for wp in ["Loose", "Medium", "Tight"]:
#        selections = allSelections.clone()
#        selections.BJetSelection.bjetDiscr = algo
#        selections.BJetSelection.bjetDiscrWorkingPoint = wp
#        suffix = "_%s_%s"%(algo,wp)
#        print "Added analyzer for algo/wp: %s"%suffix
#        process.addAnalyzer("BTagEfficiency"+suffix, Analyzer("BTagEfficiencyAnalysis", config=selections, silent=False))

# Build analysis modules
from HiggsAnalysis.NtupleAnalysis.AnalysisBuilder import AnalysisBuilder
builder = AnalysisBuilder("BTagEfficiencyAnalysis",
                          dataEras,
                          searchModes,
                          #### Options ####
                          usePUreweighting=False,
                          doSystematicVariations=False,
                          )
builder.addVariation("BJetSelection.bjetDiscr", ["pfCombinedInclusiveSecondaryVertexV2BJetTags"])
builder.addVariation("BJetSelection.bjetDiscrWorkingPoint", ["Loose", "Medium", "Tight"])
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
#if "proof" in sys.argv:
#    process.run(proof=True)
#else:
process.run()

# Run the analysis with PROOF
# By default it uses all cores, but you can give proofWorkers=<N> as a parameter
#process.run(proof=True)
