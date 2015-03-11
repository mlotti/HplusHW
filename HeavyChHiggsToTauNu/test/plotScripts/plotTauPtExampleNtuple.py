#!/usr/bin/env python

###########################################################################
#
# This script is only intended as an example, please do NOT modify it.
# For example, start from scratch and look here for help, or make a
# copy of it and modify the copy (including removing all unnecessary
# code).
#
###########################################################################

drawToScreen = True
drawToScreen = False

import ROOT
if not drawToScreen:
    ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect

def main():
    # Create all datasets from a multicrab task
    datasets = dataset.getDatasetsFromMulticrabCfg(analysisName="test")

    # We don't have yet the lumi information handled in NtupleAnalysis, so remove data for now
    datasets.remove(datasets.getDataDatasetNames())

    # For this we don't have cross section
    datasets.remove(["DYJetsToLL_M10to50_TuneZ2star_Summer12"])

    # These have 0 events after skim in multicrab_TEST5, and the code crashes because of that
    datasets.remove([
        "QCD_Pt30to50_TuneZ2star_Summer12",
        "QCD_Pt50to80_TuneZ2star_Summer12",
        "QCD_Pt80to120_TuneZ2star_Summer12",
        "QCD_Pt120to170_TuneZ2star_Summer12"
        ])

    # As we use weighted counters for MC normalisation, we have to
    # update the all event count to a separately defined value because
    # the analysis job uses skimmed pattuple as an input
    datasets.updateNAllEventsToPUWeighted(era="Run2012ABCD")

    # At the moment the collision energy must be set by hand
    for dset in datasets.getMCDatasets():
        dset.setEnergy("8")

    # At the moment the cross sections must be set by hand
    xsect.setBackgroundCrossSections(datasets)

    # Default merging and ordering of data and MC datasets
    # All data datasets to "Data"
    # All QCD datasets to "QCD"
    # All single top datasets to "SingleTop"
    # WW, WZ, ZZ to "Diboson"
    plots.mergeRenameReorderForDataMC(datasets)

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    dataMCExample(datasets)

    # Script execution can be paused like this, it will continue after
    # user has given some input (which must include enter)
    if drawToScreen:
        raw_input("Hit enter to continue")


def dataMCExample(datasets):
    # Create data-MC comparison plot, with the default
    # - legend labels (defined in plots._legendLabels)
    # - plot styles (defined in plots._plotStyles, and in styles)
    # - drawing styles ('HIST' for MC, 'EP' for data)
    # - legend styles ('L' for MC, 'P' for data)
    plot = plots.DataMCPlot(datasets,
                            #"ForDataDrivenCtrlPlots/SelectedTau_pT_AfterStandardSelections"
                            "tauPt",
                            # Since the data datasets were removed, we have to set the luminosity by hand
                            normalizeToLumi=20000
    )

    # Same as below, but more compact
    plots.drawPlot(plot, "taupt", xlabel="Tau p_{T} (GeV/c)", ylabel="Number of events",
                   rebin=10, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True,
                   opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)

if __name__ == "__main__":
    main()
