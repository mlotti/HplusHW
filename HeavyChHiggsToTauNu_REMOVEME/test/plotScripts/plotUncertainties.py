#!/usr/bin/env python

import math

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
    datasets.merge("EWK", ["TTJets",
                           "WJets",
                           "DYJetsToLL",
                           "SingleTop", "Diboson"
                           ], keepSources=True)

    style = tdrstyle.TDRStyle()

    # Setup the systematics recipe object
    systematics = dataset.Systematics(
        allShapes=True,
        #shapes=["SystVarJER", "SystVarJES", "SystVarMET", "SystVarTES"],
        #verbose=True,
        #additionalNormalizations={"Foo": 0.2, "Bar": 0.05},
                                      )

    histograms.uncertaintyMode.set(histograms.Uncertainty.StatOnly)

    def dop(datasetName):
        doPlots(datasets, datasetName, systematics)
        doCounters(datasets, datasetName, creator.getSystematicVariationSources())

#    dop("TTToHplus_M80")
    dop("TTToHplus_M120")
#    dop("TTToHplus_M160")
#    dop("HplusTB_M180")
    dop("HplusTB_M200")
#    dop("HplusTB_M300")
    dop("TTJets")
#    dop("DYJetsToLL")
    dop("WJets")
    dop("EWK")

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
                         ratio=True, addLuminosityText=True,
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
        plot.setLuminosity(mcOnlyLumi)
        plot.histoMgr.forEachHisto(styles.Generator(styleList))
        plot.appendPlotObject(histograms.PlotText(x=0.7, y=0.7, text=datasetName, size=17))
        plot.appendPlotObject(histograms.PlotText(x=0.7, y=0.65, text=source, size=17))
        if "TTToHplus_" in datasetName:
            plot.appendPlotObject(histograms.PlotText(x=0.7, y=0.6, text="#it{B}(H^{+}#rightarrow#tau#nu)=0.01", size=17))
        elif "HplusTB_" in datasetName:
            plot.appendPlotObject(histograms.PlotText(x=0.7, y=0.6, text="#sigma#times#it{B}=1 pb", size=17))
        args = {}
        if source == "SystVarTauTrgSF":
            args["opts2"] = {"ymin": 0.2, "ymax": 1.8}
        drawPlot(plot, "%s_%s" % (datasetName, source), **args)
    

def doCounters(datasets, datasetName, systematicVariationSources):
    dset = datasets.getDataset(datasetName)

    countName = "Selected events"
    def getCount(ec):
        return ec.getMainCounterTable().getCount(colName=datasetName, rowName=countName)
    def createEC(**kwargs):
        ec = counter.EventCounter([dset], **kwargs)
        ec.normalizeMCToLuminosity(mcOnlyLumi)
        return ec

    ecNominal = createEC()

    countNominal = getCount(ecNominal)

    print "Dataset %s" % datasetName
    print "Systematics from variations:"
    for source in systematicVariationSources:
        ecPlus = createEC(analysisPostfix=source+"Plus")
        ecMinus = createEC(analysisPostfix=source+"Minus")

        countPlus = getCount(ecPlus)
        countMinus = getCount(ecMinus)
    
        diffPlus = countPlus.value() - countNominal.value()
        diffMinus = countNominal.value() - countMinus.value()

        relPlus = (diffPlus / countNominal.value()) * 100
        relMinus = (diffMinus / countNominal.value()) * 100

        print "  %s: %.2f + %.2f - %.2f (+ %.2f - %.2f %%)" % (source, countNominal.value(), diffPlus, diffMinus, relPlus, relMinus)

    print "Systematics from propagation:"
    scaleFactors = ["BtagScaleFactor", "TauTriggerScaleFactor"]
    def getSum(drh):
        s = 0.0
        th1 = drh.getHistogram()
        for i in xrange(1, th1.GetNbinsX()+1):
            s += (th1.GetBinContent(i)*th1.GetBinCenter(i))**2
        return s
    def getCount(drh):
        return drh.getHistogram().GetBinContent(1)

    for sf in scaleFactors:
        drhAbsUnc = dset.getDatasetRootHisto("ScaleFactorUncertainties/%sAbsUncert_AfterSelection"%sf)
        drhCount = dset.getDatasetRootHisto("ScaleFactorUncertainties/%sAbsUncertCounts_AfterSelection"%sf)
        
        sums = drhAbsUnc.forEach(getSum)
        countsRaw = drhCount.forEach(getCount)

        drhCount.normalizeToLuminosity(mcOnlyLumi)
        countsNorm = drhCount.forEach(getCount)

        sigmaSquared = 0.0
        countNormSum = 0.0
        for squareSum, countRaw, countNorm in zip(sums, countsRaw, countsNorm):
            if countRaw == 0.0:
                continue

            relUnc = math.sqrt(squareSum)/countRaw
            absUnc = relUnc * countNorm
            sigmaSquared += absUnc**2
            countNormSum += countNorm

        sigma = math.sqrt(sigmaSquared)
        sigmaRel = sigma/countNormSum * 100
        print "  %s: %.2f +- %.2f (+- %.2f %%)" % (sf, countNormSum, sigma, sigmaRel)
    print

if __name__ == "__main__":
    main()
