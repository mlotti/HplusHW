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
    datasets = dataset.getDatasetsFromMulticrabCfg(analysisName="test", setCrossSectionAutomatically=False)

    # We don't have yet the lumi information handled in NtupleAnalysis, so remove data for now
    datasets.remove(datasets.getDataDatasetNames())

#    datasets.getDataset("TBHp_HToTauNu_M_200_13TeV_pythia6").setCrossSection(0.336902*2*0.955592) # pb  
    datasets.getDataset("TBHp_HToTauNu_M_200_13TeV_pythia6").setCrossSection(10) # pb ##  test 
    datasets.getDataset("TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6").setCrossSection(0.336902*2*0.955592) # pb   
    datasets.getDataset("TTJets_MSDecaysCKM_central_Tune4C_13TeV_madgraph_tauola").setCrossSection(245.8) # pb   
    datasets.getDataset("TT_Tune4C_13TeV_pythia8_tauola").setCrossSection(245.8) # pb 
    datasets.getDataset("QCD_Pt_50to80_TuneZ2star_13TeV_pythia6").setCrossSection(8148778.0) # pb   
    datasets.getDataset("QCD_Pt_50to80_Tune4C_13TeV_pythia8").setCrossSection(8.1487780) # pb test  
   # datasets.getDataset("DYToTauTau_M_20_CT10_TuneZ2star_v2_powheg_tauola_Summer12").setCrossSection(8.1487780) # pb test    
    datasets.getDataset("DYJetsToLL_M_50_13TeV_madgraph_pythia8_tauola_v2").setCrossSection(8.1487780) # pb test  

    # For this we don't have cross section
    datasets.remove(["DYJetsToLL_M10to50_TuneZ2star_Summer12"])
#    datasets.remove(["TBHp_HToTauNu_M_200_13TeV_pythia6"])
    datasets.remove(["QCD_Pt_50to80_TuneZ2star_13TeV_pythia6"])
#    datasets.remove(["QCD_Pt_50to80_Tune4C_13TeV_pythia8"])
    datasets.remove(["TTbar_HBWB_HToTauNu_M_160_13TeV_pythia6"])
#    datasets.remove(["TT_Tune4C_13TeV_pythia8_tauola"])
    datasets.remove(["TTJets_MSDecaysCKM_central_Tune4C_13TeV_madgraph_tauola"])
    datasets.remove(["DYJetsToLL_M_50_13TeV_madgraph_pythia8_tauola_v2"])
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
        dset.setEnergy("13")

    # At the moment the cross sections must be set by hand
    #xsect.setBackgroundCrossSections(datasets)

    # Default merging and ordering of data and MC datasets
    # All data datasets to "Data"
    # All QCD datasets to "QCD"
    # All single top datasets to "SingleTop"
    # WW, WZ, ZZ to "Diboson"
    plots.mergeRenameReorderForDataMC(datasets)
#    datasets.rename("TTJets_MSDecaysCKM_central_Tune4C_13TeV_madgraph_tauola", "TTJets")
    datasets.rename("QCD_Pt_50to80_Tune4C_13TeV_pythia8", "QCD")
#    datasets.rename("TT_Tune4C_13TeV_pythia8_tauola", "TT_pythia8")
    datasets.rename("TT_Tune4C_13TeV_pythia8_tauola", "TTJets")

 
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    dataMCExample(datasets)
    MtComparison(datasets)
    MetComparison(datasets)
    TauPtComparison(datasets)

   # Print counters                                                                                                                                                                                                                                               
    doCounters(datasets)



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


    drawPlot = plots.PlotDrawer(stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 1})

    def createDrawPlot(name, **kwargs):
        drawPlot( plots.DataMCPlot(datasets, name, normalizeToLumi=20000), name, **kwargs)

    createDrawPlot("tauEta", xlabel="#eta^{#tau jet}", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("tauPhi", xlabel="#phi^{#tau jet}", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("Rtau", xlabel="p_{T}^{leading track}/p_{T}^{#tau jet}", ylabel="Number of events", rebin=1, log=True)
    createDrawPlot("Met", xlabel="E_{T}^{miss} (GeV)", ylabel="Number of events", rebin=5, log=True,opts={"ymin": 1e-1, "ymaxfactor": 10})
    createDrawPlot("MetPhi", xlabel="#phi^{ETmiss} ", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("jetPt", xlabel="p_{T}^{jet} (GeV/c)", ylabel="Number of events", rebin=2, log=True)
    createDrawPlot("electronPt", xlabel="p_{T}^{electron} (GeV/c)", ylabel="Number of events", rebin=2, log=True)
    createDrawPlot("electronEta", xlabel="#eta^{electron}", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("muonPt", xlabel="p_{T}^{muon} (GeV/c)", ylabel="Number of events", rebin=2, log=True)
    createDrawPlot("muonEta", xlabel="#eta^{muon}", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("Nelectrons", xlabel="N_{electrons}", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("Nmuons", xlabel="N_{muons}", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("bJetPt", xlabel="p_{T}^{b-jet} (GeV/c)", ylabel="Number of events", rebin=1, log=True)
    createDrawPlot("bjetEta", xlabel="#eta^{b-jet}", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("realBJetPt", xlabel="p_{T}^{b-jet} (GeV/c)", ylabel="Number of events", rebin=1, log=True)
    createDrawPlot("realBJetEta", xlabel="#eta^{b-jet}", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("realMaxBJetPt", xlabel="p_{T}^{b-jet} (GeV/c)", ylabel="Number of events", rebin=1, log=True)
    createDrawPlot("realMaxBJetEta", xlabel="#eta^{b-jet}", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("jetEta", xlabel="#eta^{jet}", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("jetPhi", xlabel="#phi^{jet}", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("DeltaPhiTauMet", xlabel="#Delta#Phi(#tau,MET)", ylabel="Number of events", rebin=1, log=False, opts={"ymin": 0, "xmin":0})
    createDrawPlot("Njets", xlabel="Number of Jets", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("NBjets", xlabel="Number of B-jets", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("NtrueBjets", xlabel="Number of B-jets", ylabel="Number of events", rebin=1, log=False)

    createDrawPlot("jetBProbabilityBJetTags", xlabel="Discriminator", ylabel="Number of events", rebin=1, log=True)
    createDrawPlot("jetProbabilityBJetTags", xlabel="Discriminator", ylabel="Number of events", rebin=1, log=True, opts={"xmax":4, "xmin":0})
    createDrawPlot("trackCountingHighEffBJetTags", xlabel="Discriminator", ylabel="Number of events", rebin=1, log=True)
    createDrawPlot("trackCountingHighPurBJetTags", xlabel="Discriminator", ylabel="Number of events", rebin=1, log=True)
    createDrawPlot("Pt3Jets", xlabel="p_{T}^{3jets} (GeV/c)", ylabel="Number of events", rebin=1, log=False)
    createDrawPlot("TheeJetPtcut", xlabel="ThreeJetPtcut (GeV/c)", ylabel="Number of events", rebin=4, log=True, opts={"xmax":450, "xmin":0})
    createDrawPlot("DPhi3JetsMet", xlabel="#Delta#phi(3 jets, MET)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("DrTau3Jets", xlabel="#DeltaR(3 jets, #tau jet)", ylabel="Number of events", rebin=2, log=False)

    createDrawPlot("JetTauEtSum", xlabel="#Sigma(Jets,#tau jet) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("JetTauMetEtSum", xlabel="#Sigma(Jets,#tau jet, MET) (GeV)", ylabel="Number of events", rebin=2, log=False)
#    createDrawPlot("TauMetEtSum", xlabel="#Sigma(#tau jet, MET) (GeV)", ylabel="Number of events", rebin=2, log=False)

#    createDrawPlot("transverseMass", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=1, log=False, opts={"ymin": 0, "xmin":5, "ymaxfactor": 0.1})
    createDrawPlot("transverseMass", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("transverseMassTriangleCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("transverseMass3JetCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("transverseMass_bbCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("transverseMass_bbAndColCut", xlabel="m_{T}(#tau,MET) (GeV)", ylabel="Number of events", rebin=2, log=False)
    createDrawPlot("Radiusbb",  xlabel="Back-to-Back radius (^{o})", ylabel="Number of events", rebin=2, log=True)
    createDrawPlot("RadiusCol", xlabel="Collinear radius (^{o})", ylabel="Number of events", rebin=2, log=True)
    createDrawPlot("constantEtSum", xlabel="Constant term (GeV)", ylabel="Number of events", rebin=2, log=True)
    createDrawPlot("slopeEtSum", xlabel="Slope", ylabel="Number of events", rebin=2, log=True)
#    plots.drawPlot( plots.DataMCPlot(datasets, "Pt3Jets", normalizeToLumi=20000), "Pt3Jets", xlabel="p_{T}^{3jets} (GeV/c)", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 0.01}, log=False)
#    plots.drawPlot( plots.DataMCPlot(datasets, "DeltaPhiTauMet", normalizeToLumi=20000), "DeltaPhiTauMet", xlabel="#Delta#Phi(#tau,MET)", ylabel="Number of events", rebin=1, stackMCHistograms=True, addMCUncertainty=True, addLuminosityText=True, opts={"ymin": 1e-1, "ymaxfactor": 0.01}, log=False)



def getHistos(datasets,name1, name2, name3):
     drh1 = datasets.getDataset("TTJets").getDatasetRootHisto(name1)
     drh2 = datasets.getDataset("TTJets").getDatasetRootHisto(name2)
     drh3 = datasets.getDataset("TTJets").getDatasetRootHisto(name3)
     drh1.setName("transverseMass")
     drh2.setName("transverseMassTriangleCut")
     drh3.setName("transverseMass3JetCut")
     return [drh1, drh2, drh3]

#mt = plots.PlotBase(getHistos("MetNoJetInHole", "MetJetInHole"))

def MtComparison(datasets):
    mt = plots.PlotBase(getHistos(datasets,"transverseMass", "transverseMassTriangleCut", "transverseMass3JetCut"))
#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())
    mt._setLegendStyles()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st3 = styles.StyleCompound([styles.styles[3]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=3, lineWidth=3))
    mt.histoMgr.forHisto("transverseMass", st1)
    mt.histoMgr.forHisto("transverseMassTriangleCut", st2)
    mt.histoMgr.forHisto("transverseMass3JetCut", st3)

    mt.histoMgr.setHistoLegendLabelMany({
            "transverseMass": "m_{T}(#tau jet, E_{T}^{miss})",
            "transverseMassTriangleCut": "m_{T}(#tau jet, E_{T}^{miss}) with Triangle Cut",
            "transverseMass3JetCut": "m_{T}(#tau jet, E_{T}^{miss}) with 3-jet Cut"
            })
#    mt.histoMgr.setHistoDrawStyleAll("P")

    mt.appendPlotObject(histograms.PlotText(300, 50, "p_{T}^{jet} > 50 GeV/c", size=20))
    xlabel = "m_{T}(#tau jet, E_{T}^{miss}) (GeV/c^{2})"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "MtComparison", xlabel=xlabel, ylabel=ylabel, rebinX=2, log=False,
                   createLegend={"x1": 0.4, "y1": 0.75, "x2": 0.8, "y2": 0.9},
                   ratio=False, opts2={"ymin": 0.5, "ymax": 1.5})
          
#    rtauGen(mt, "MetComparison", rebin=1, ratio=True, defaultStyles=False)


def getHistos2(datasets,name1, name2):
     drh1 = datasets.getDataset("TTJets").getDatasetRootHisto("Met")
     #drh2 = datasets.getDataset("TT_pythia8").getDatasetRootHisto("Met")
     drh2 = datasets.getDataset("TTJets").getDatasetRootHisto("Met")

     drh1.setName("Met_madgraph")
     drh2.setName("Met_pythia8")
     return [drh1, drh2]

#mt = plots.PlotBase(getHistos("MetNoJetInHole", "MetJetInHole"))                                                                                                                                                                                                      

def MetComparison(datasets):
    mt = plots.ComparisonPlot(*getHistos2(datasets,"Met","Met"))
#    mt.histoMgr.normalizeMCToLuminosity(datasets.getDataset("Data").getLuminosity())                                                                                                                                                                                  
    mt._setLegendStyles()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    mt.histoMgr.forHisto("Met_madgraph", st1)
    mt.histoMgr.forHisto("Met_pythia8", st2)
    mt.histoMgr.setHistoLegendLabelMany({
            "Met_madgraph": "Met from Madgraph",
            "Met_pythia8": "Met from Pythia8"
            })
    mt.histoMgr.setHistoDrawStyleAll("PE")


    mt.appendPlotObject(histograms.PlotText(100, 0.01, "tt events", size=20))
    xlabel = "PF E_{T}^{miss} (GeV)"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "MetComparison", xlabel=xlabel, ylabel=ylabel, rebinX=2, log=True,
                   createLegend={"x1": 0.6, "y1": 0.75, "x2": 0.8, "y2": 0.9},
                   ratio=False, opts2={"ymin": 0.5, "ymax": 50}, opts={"xmax": 500})


def getHistos3(datasets,name1, name2):
     drh1 = datasets.getDataset("TTJets").getDatasetRootHisto("tauPt")
    # drh2 = datasets.getDataset("TT_pythia8").getDatasetRootHisto("tauPt")
     drh2 = datasets.getDataset("TTJets").getDatasetRootHisto("tauPt")

     drh1.setName("Taupt_madgraph")
     drh2.setName("Taupt_pythia8")
     return [drh1, drh2]

def TauPtComparison(datasets):
    mt = plots.ComparisonPlot(*getHistos3(datasets,"tauPt","tauPt"))
                                                                                                                                                                                                                                                                       
    mt._setLegendStyles()
    st1 = styles.StyleCompound([styles.styles[2]])
    st2 = styles.StyleCompound([styles.styles[1]])
    st1.append(styles.StyleLine(lineWidth=3))
    st2.append(styles.StyleLine(lineStyle=2, lineWidth=3))
    mt.histoMgr.forHisto("Taupt_madgraph", st1)
    mt.histoMgr.forHisto("Taupt_pythia8", st2)
    mt.histoMgr.setHistoLegendLabelMany({
            "Taupt_madgraph": "Tau pt from Madgraph",
            "Taupt_pythia8": "Tau pt from Pythia8"
            })
    mt.histoMgr.setHistoDrawStyleAll("PE")

    mt.appendPlotObject(histograms.PlotText(100, 0.01, "tt events", size=20))
    xlabel = "p_{T}^{#tau jet} (GeV)"
    ylabel = "Events / %.2f"
    plots.drawPlot(mt, "TauPtComparison", xlabel=xlabel, ylabel=ylabel, rebinX=2, log=True,
                   createLegend={"x1": 0.6, "y1": 0.75, "x2": 0.8, "y2": 0.9},
                   ratio=False, opts2={"ymin": 0.5, "ymax": 50}, opts={"xmax": 800, "ymin":1, "ymax":1000000})






def rtauGen(h, name, rebin=2, ratio=False, defaultStyles=True):
    if defaultStyles:
        h.setDefaultStyles()
        h.histoMgr.forEachHisto(styles.generator())

    h.histoMgr.forEachHisto(lambda h: h.getRootHisto().Rebin(rebin))


    xlabel = "PF E_{T}^{miss} (GeV)"
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
    kwargs["opts2"] = {"ymin": 0.5, "ymax": 1.5}
    kwargs["createRatio"] = True
#    if ratio:
#        h.createFrameFraction(name, opts=opts, opts2=opts2)
#    h.setLegend(leg)

    common(h, xlabel, ylabel)



def doCounters(datasets):
    eventCounter = counter.EventCounter(datasets)

    print "============================================================"
    print "Main counter (MC normalized by collision data luminosity)"
    mainTable = eventCounter.getMainCounterTable()
#    mainTable.insertColumn(2, counter.sumColumn("EWKMCsum", [mainTable.getColumn(name=name) for name in ewkDatasets]))
    # Default                                                                                                                                                                                                                                                      
#    cellFormat = counter.TableFormatText()                                                                                                                                                                                                                        
    # No uncertainties                                                                                                                                                                                                                                             
    cellFormat = counter.TableFormatText(cellFormat=counter.CellFormatText(valueOnly=True))
    print mainTable.format(cellFormat)

#    print eventCounter.getSubCounterTable("MCinfo for selected events").format(cellFormat)

    print eventCounter.getSubCounterTable("Tau-jet selection").format()                                                                                                                                                                                                
#    print eventCounter.getSubCounterTable("TauIDPassedEvt::TauSelection_HPS").format(cellFormat)                                                                                                                                                                  
#    print eventCounter.getSubCounterTable("TauIDPassedJets::TauSelection_HPS").format(cellFormat)                                                                                                                                                                 
    print eventCounter.getSubCounterTable("B-jet selection").format(cellFormat)                                                                                                                                                                                         
#    print eventCounter.getSubCounterTable("Jet selection").format(cellFormat)                                                                                                                                                                                     
#    print eventCounter.getSubCounterTable("Jet main").format(cellFormat)                                                                                                                                                                                          
#    print eventCounter.getSubCounterTable("VetoTauSelection").format(cellFormat)                                                                                                                                                                                  
#    print eventCounter.getSubCounterTable("MuonSelection").format(cellFormat)                                                         




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
