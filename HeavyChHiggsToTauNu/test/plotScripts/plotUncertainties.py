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

dataEra = "Run2011AB"

mcOnly = False
#mcOnly = True
mcOnlyLumi = 5000 # pb

def main():
    creator = dataset.readFromMulticrabCfg()
    print creator.getSystematicVariations()
    print creator.getSystematicVariationSources()

    datasets = creator.createDatasetManager(dataEra=dataEra)

    if not mcOnly:
        datasets.loadLuminosities()

    datasets.updateNAllEventsToPUWeighted()    
    plots.mergeRenameReorderForDataMC(datasets)

    if not mcOnly:
        mcOnlyLumi = datasets.getDataset("Data").getLuminosity()

    datasets.remove(datasets.getDataDatasetNames())
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION

    histograms.createLegend.moveDefaults(dx=-0.05, dh=-0.15)

    xsect.setHplusCrossSectionsToBR(datasets, br_tH=0.01, br_Htaunu=1)
    for dset in datasets.getAllDatasets():
        if "HplusTB_" in dset.getName():
            dset.setCrossSection(1.0)

    plots.mergeWHandHH(datasets)

    style = tdrstyle.TDRStyle()

    # Setup the systematics recipe object
    systematics = dataset.Systematics(shapes=["SystVarJER", "SystVarJES", "SystVarMET", "SystVarTES"],
                                      #verbose=True,
                                      additionalNormalizations={"Foo": 0.2, "Bar": 0.05},
                                      )

    def dop(datasetName):
        doPlots(datasets, datasetName, systematics)
        doCounters(datasets, datasetName)

    dop("TTToHplus_M80")
    dop("TTToHplus_M120")
    dop("TTToHplus_M160")
    dop("HplusTB_M180")
    dop("HplusTB_M200")
    dop("HplusTB_M300")
    dop("TTJets")
    dop("WJets")

drawPlot = plots.PlotDrawer()

def doPlots(datasets, datasetName, systematics):
    dset = datasets.getDataset(datasetName)

    ptBinning = range(0, 200, 40)+[200, 300, 400]
    if "HplusTB_" in datasetName:
        ptBinning = range(0, 400, 40)+[400]
    elif "WJets" in datasetName:
        ptBinning = range(0, 160, 40)+[160, 400]
        
        

    drawPlot.setDefaults(xlabel="m_{T}(#tau, E_{T}^{miss}) (GeV)", ylabel="dN/dm_{T} (%.0f-%.0f GeV)",
                         rebinX=ptBinning, divideByBinWidth=True,
                         ratio=True,
                         opts2={"ymin": 0.8, "ymax": 1.2})

    drh = dset.getDatasetRootHisto(systematics.histogram("transverseMass"))
    drh.normalizeToLuminosity(mcOnlyLumi)
    h = drh.getHistogramWithUncertainties() # RootHistoWithUncertainties

    def makeStyle(color, markerStyle):
        return styles.StyleCompound([
                styles.StyleLine(lineColor=color, lineWidth=2),
                styles.StyleMarker(markerColor=color, markerStyle=markerStyle)
                ])

    styleList = [
        makeStyle(ROOT.kBlack, ROOT.kDot),
        makeStyle(ROOT.kRed, 24),
        makeStyle(ROOT.kBlue, 25),
        ]

    th1 = h.getRootHisto()
    for source, tpl in h.getShapeUncertainties().iteritems():
        plot = plots.ComparisonManyPlot(
                histograms.Histo(th1, "Nominal"),# drawStyle="L"),
                [
                histograms.Histo(tpl[0], "Plus"),# drawStyle="L"),
                histograms.Histo(tpl[1], "Minus"),# drawStyle="L")
                ])
        plot.histoMgr.forEachHisto(styles.Generator(styleList))
        plot.appendPlotObject(histograms.PlotText(x=0.7, y=0.7, text=datasetName, size=17))
        plot.appendPlotObject(histograms.PlotText(x=0.7, y=0.65, text=source, size=17))
        drawPlot(plot, "%s_%s" % (datasetName, source))
    

def doCounters(datasets, datasetName):
    pass


if __name__ == "__main__":
    main()
