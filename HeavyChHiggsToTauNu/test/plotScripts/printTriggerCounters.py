#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

analysis = "signalAnalysis"
counters = analysis+"Counters"

def main():
    # Read the datasets
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters)
    datasets.updateNAllEventsToPUWeighted()
           
    #datasets.loadLuminosities()

    plots.mergeRenameReorderForDataMC(datasets)

    # Set the signal cross sections to a given BR(t->H), BR(h->taunu)
    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.05, br_Htaunu=1)

    # Set the signal cross sections to a value from MSSM
    #    xsect.setHplusCrossSectionsToMSSM(datasets, tanbeta=20, mu=200)
                
    plots.mergeWHandHH(datasets) # merging of WH and HH signals must be done after setting the cross section

    # Create counter
    eventCounter = counter.EventCounter(datasets)

    #eventCounter.normalizeMCByLuminosity()
    eventCounter.normalizeMCToLuminosity(1000) # in pb^-1

    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    print eventCounter.getMainCounterTable().format()

    triggerCounter = eventCounter.getSubCounter("Trigger")
    triggerCounter.forEachDataset(printTriggerEfficiency)

def printTriggerEfficiency(simpleCounter):
    nall = simpleCounter.getCountByName("All events").value()
    npassed = simpleCounter.getCountByName("Passed").value()

    print "%s: passed/all = %.2f/%.2f = %.4f" % (simpleCounter.getName(), npassed, nall, npassed/nall)

    
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
