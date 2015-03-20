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
    MetComparison(datasets)

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
    plots.drawPlot( plots.DataMCPlot(datasets, "tauEta", normalizeToLumi=20000), "tauEta", xlabel="", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 10}, log=False)
    plots.drawPlot( plots.DataMCPlot(datasets, "Met", normalizeToLumi=20000), "Met", xlabel="E_{T}^{miss} (GeV)", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)
    plots.drawPlot( plots.DataMCPlot(datasets, "MetPhi", normalizeToLumi=20000), "MetPhi", xlabel="#Phi^{miss} ", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 0.01}, log=False)
    plots.drawPlot( plots.DataMCPlot(datasets, "jetPt", normalizeToLumi=20000), "jetPt", xlabel="p_{T}^{jet} (GeV/c)", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 10}, log=True)
    plots.drawPlot( plots.DataMCPlot(datasets, "jetEta", normalizeToLumi=20000), "jetEta", xlabel="", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 0.01}, log=False)
    plots.drawPlot( plots.DataMCPlot(datasets, "jetPhi", normalizeToLumi=20000), "jetPhi", xlabel="#Phi^{jet}", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 0.01}, log=False)
#    plots.drawPlot( plots.DataMCPlot(datasets, "Pt3Jets", normalizeToLumi=20000), "Pt3Jets", xlabel="p_{T}^{3jets} (GeV/c)", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 0.01}, log=False)
    plots.drawPlot( plots.DataMCPlot(datasets, "DeltaPhiTauMet", normalizeToLumi=20000), "DeltaPhiTauMet", xlabel="#Delta#Phi(#tau,MET)", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 0.01}, log=False)
def getHistos(datasets,name1, name2):
     drh1 = datasets.getDataset("TTJets").getDatasetRootHisto("MetNoJetInHole")
     drh2 = datasets.getDataset("TTJets").getDatasetRootHisto("MetJetInHole")
     drh1.setName("MetNoJetInHole")
     drh2.setName("MetJetInHole")
     return [drh1, drh2]

#mt = plots.PlotBase(getHistos("MetNoJetInHole", "MetJetInHole"))

def MetComparison(datasets):
    mt = plots.PlotBase(getHistos(datasets,"MetNoJetInHole", "MetJetInHole"))
 #   mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    mt._setLegendLabels()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    mt.histoMgr.forHisto("MetNoJetInHole", st1)
    mt.histoMgr.forHisto("MetJetInHole", st2)
#    mt.histoMgr.setHistoDrawStyleAll("P")

    rtauGen(mt, "MetComparison", rebin=1, ratio=True, defaultStyles=False)

def rtauGen(h, name, rebin=2, ratio=False, defaultStyles=True):
    if defaultStyles:
        h.setDefaultStyles()
        h.histoMgr.forEachHisto(styles.generator())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))


    xlabel = "PF E_{T}^{miss} (GeV)"
#    xlabel = "#beta^{jet}"
    ylabel = "Events / %.2f" % h.binWidth()
    if "LeptonsInMt" in name:
        xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
    if "NoLeptonsRealTau" in name:
        xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()
    if "Mass" in name:
        xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
        ylabel = "Events / %.0f GeV/c^{2}" % h.binWidth()

        
    kwargs = {"ymin": 0.1, "ymax": 1000}
#    h.getPad().SetLogy(True)

    if "LeptonsInMt" in name: 
        kwargs = {"ymin": 0., "xmax": 300}
    if "NoLeptonsRealTau" in name: 
        kwargs = {"ymin": 0., "xmax": 300}
    if "Rtau" in name:
        kwargs = {"ymin": 0.0001, "xmax": 1.1}   
        kwargs = {"ymin": 0.1, "xmax": 1.1}     
        h.getPad().SetLogy(True)

#    kwargs["opts"] = {"ymin": 0, "xmax": 14, "ymaxfactor": 1.1}}
    if ratio:
        kwargs["opts2"] = {"ymin": 0.5, "ymax": 1.5}
        kwargs["createRatio"] = True
#    name = name+"_log"

    h.createFrame(name, **kwargs)

#    histograms.addText(0.65, 0.7, "BR(t #rightarrow bH^{#pm})=0.05", 20)
    h.getPad().SetLogy(True)
    
    leg = histograms.createLegend(0.6, 0.75, 0.8, 0.9)
 
    if "LeptonsInMt" in name:
        h.getPad().SetLogy(False)
        leg = histograms.moveLegend(leg, dx=-0.18)
        histograms.addText(0.5, 0.65, "TailKiller cut: Tight", 20)
  
    h.setLegend(leg)
    plots._legendLabels["MetNoJetInHole"] = "Jets outside dead cells"
    plots._legendLabels["MetJetInHole"] = "Jets within dead cells"
    histograms.addText(300, 300, "p_{T}^{jet} > 50 GeV/c", 20)


#    h.setLegend(leg)

    common(h, xlabel, ylabel)



# Common formatting
def common(h, xlabel, ylabel, addLuminosityText=True, textFunction=None):
    h.frame.GetXaxis().SetTitle(xlabel)
    h.frame.GetYaxis().SetTitle(ylabel)
    h.draw()
#    h.addStandardTexts(addLuminosityText=addLuminosityText)
#    if textFunction != None:
#        textFunction()
    h.save()

if __name__ == "__main__":
    main()
