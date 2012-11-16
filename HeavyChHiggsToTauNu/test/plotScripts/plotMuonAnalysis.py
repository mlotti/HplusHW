#!/usr/bin/env python

######################################################################
#
# This plot script is for analysing the muon selection part of the EWK
# background measurement. The corresponding python job configuration
# is tauEmbedding/muonAnalysis_cfg.py.
#
# Author: Matti Kortelainen
#
######################################################################

import sys
import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding

analysis = "muonNtuple"
counters = analysis+"Counters"
countersWeighted = counters+"/weighted"

era = "Run2011AB"

weight = {
    "Run2011A": "weightPileup_Run2011A",
    "Run2011B": "weightPileup_Run2011B",
    "Run2011AB": "weightPileup_Run2011AB",
    }[era]
#weight = ""

mcOnly = True
#mcOnly = False
mcLuminosity = 5049.069000

mergeMC = True
#mergeMC = False

def main():
    datasets = dataset.getDatasetsFromMulticrabCfg(counters=counters, weightedCounters=len(weight)>0)
    datasets.updateNAllEventsToPUWeighted(era=era)

    if era == "Run2011A":
        datasets.remove(filter(lambda name: "2011B_" in name, datasets.getDataDatasetNames()))
    elif era == "Run2011B":
        datasets.remove(filter(lambda name: "2011A_" in name, datasets.getDataDatasetNames()))
    elif era == "Run2011AB":
        pass

    #keepOnly = "SingleMu_Mu_160431-163261_2011A_Nov08"
    #keepOnly = "SingleMu_Mu_163270-163869_2011A_Nov08"
    #keepOnly = "SingleMu_Mu_165088-166150_2011A_Nov08"
    #keepOnly = "SingleMu_Mu_166161-166164_2011A_Nov08"
    #keepOnly = "SingleMu_Mu_166346-166346_2011A_Nov08"
    #keepOnly = "SingleMu_Mu_166374-167043_2011A_Nov08"
    #keepOnly = "SingleMu_Mu_167078-167913_2011A_Nov08"
    #keepOnly = "SingleMu_Mu_170722-172619_2011A_Nov08"
    #keepOnly = "SingleMu_Mu_172620-173198_2011A_Nov08"
    #keepOnly = "SingleMu_Mu_173236-173692_2011A_Nov08"
    #keepOnly = "SingleMu_Mu_173693-177452_2011B_Nov19"
    #keepOnly = "SingleMu_Mu_177453-178380_2011B_Nov19"
    #keepOnly = "SingleMu_Mu_178411-179889_2011B_Nov19"
    #keepOnly = "SingleMu_Mu_179942-180371_2011B_Nov19"
    #datasets.remove(filter(lambda name: name != keepOnly, datasets.getDataDatasetNames()))

    #datasets.remove(datasets.getMCDatasetNames())
    if mcOnly:
        datasets.remove(datasets.getDataDatasetNames())
    else:
        datasets.loadLuminosities()

    #datasetsMC = datasets.deepCopy()
    #datasetsMC.remove(datasets.getDataDatasetNames())
    
    if mergeMC:
        plots.mergeRenameReorderForDataMC(datasets)
    
    styleGenerator = styles.generator(fill=True)

    style = tdrstyle.TDRStyle()
    #histograms.createLegend.moveDefaults(dx=-0.15)
    plots._legendLabels["QCD_Pt20_MuEnriched"] = "QCD"
    histograms.createLegend.moveDefaults(dx=-0.04)

    wtaumuRatioFile = ROOT.TFile.Open("embedding-wtaumuRatio.root", "RECREATE")
#    ROOT.TH1.AddDirectory(False)

    selections = [
#        ("FullTauLike", "taulike"),
#        ("FullNoIso", "disabled"),
#        ("FullStandardIso", "standard"),
        ("FullChargedHadrRelIso10", "chargedHadrRel10"),
#        ("FullChargedHadrRelIso15", "chargedHadrRel15"),
        ]
    for name, isolation in selections:
        ntupleCache = dataset.NtupleCache(analysis+"/tree", "MuonAnalysisSelector",
                                          selectorArgs=tauEmbedding.MuonAnalysisSelectorArgs(puWeight=weight, isolationMode=isolation),
                                          cacheFileName="histogramCache-%s.root" % name,
                                          #process=False,
                                          maxEvents=10000,
                                          )


        doPlots(datasets, name, ntupleCache)
        printCounters(datasets, name, ntupleCache)
#        printCounters(datasets, name, ntupleCache, onlyDataset="TTJets")

        if False and name == "FullChargedHadrRelIso10":
            directory = wtaumuRatioFile.mkdir(name)
            ratios = []
            for dname in ["TTJets", "WJets", "SingleTop"]:
            #for dname in ["TTJets"]:
                (ratio, fit) = doPlotsWTauMu(datasets, name, dname, ntupleCache)
                cl = ratio.Clone()
                cl.SetDirectory(directory)
                ratios.append( (ratio, fit, dname) )

            doPlotsWTauMuRatio(name, ratios)

    wtaumuRatioFile.Write()
    wtaumuRatioFile.Close()

def doPlots(datasets, selectionName, ntupleCache):
    def createPlot(name, **kwargs):
        args = kwargs.copy()
        if mcOnly:
            args["normalizeToLumi"] = mcLuminosity
        return plots.DataMCPlot(datasets, name, **args)
    drawPlot = plots.PlotDrawer(stackMCHistograms=True, addMCUncertainty=True, log=True, ratio=not mcOnly, addLuminosityText=True,
                                ratioYlabel="Ratio",
                                optsLog={"ymin": 1e-1}, opts2={"ymin": 0, "ymax": 2})


    prefix = era+"_"+selectionName+"_"
    drawPlot(createPlot(ntupleCache.histogram("selectedMuonPt_AfterJetSelection")),
             prefix+"muon_pt_log", "Muon p_{T} (GeV/c)", ylabel="Events / %.0f GeV/c", cutBox={"cutValue":40, "greaterThan":True})

    drawPlot(createPlot(ntupleCache.histogram("uncorrectedMet_AfterJetSelection")),
             prefix+"met_pt_log", "Uncorrected PF E_{T}^{miss} (GeV)", ylabel="Events / %.0f GeV")

    drawPlot(createPlot(ntupleCache.histogram("transverseMassUncorrectedMet_AfterJetSelection")),
             prefix+"mt_log", "m_{T}(#mu, E_{T}^{miss}) (GeV/c^{2})", ylabel="Events / %.0f GeV/c^{2}")

    # plotEfficiency(datasets, ["Data", "TTJets", "WJets", "QCD_Pt20_MuEnriched"],
    #                allPath=ntupleCache.histogram("muonVertexCount_AfterDB"),
    #                passedPath=ntupleCache.histogram("muonVertexCount_AfterIsolation"),
    #                name=prefix+"muonIsolationEfficiency", xlabel="Number of good vertices", ylabel="Muon selection efficiency",
    #                rebinBins=range(0, 25)+[25, 30, 35, 40, 50]
    #                )

    # plotEfficiency(datasets, ["TTJets", "WJets"],
    #                allPath=ntupleCache.histogram("muonVertexCount_AfterDB_MuFromW"),
    #                passedPath=ntupleCache.histogram("muonVertexCount_AfterIsolation_MuFromW"),
    #                name=prefix+"muonIsolationEfficiency_MuFromW", xlabel="Number of good vertices", ylabel="Muon selection efficiency",
    #                rebinBins=range(0, 25)+[25, 30, 35, 40, 50]
    #                )
                   

    if "NoIso" in selectionName:
        drawPlot(createPlot(ntupleCache.histogram("selectedMuonChargedHadronEmbIso_AfterJetSelection")),
                 prefix+"chargedHadronIso_log", "Charged hadron #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")
        drawPlot(createPlot(ntupleCache.histogram("selectedMuonPuChargedHadronEmbIso_AfterJetSelection")),
                 prefix+"puChargedHadronIso_log", "Charged hadron #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")
        drawPlot(createPlot(ntupleCache.histogram("selectedMuonNeutralHadronEmbIso_AfterJetSelection")),
                 prefix+"neutralHadronIso_log", "Neutral hadron #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")
        drawPlot(createPlot(ntupleCache.histogram("selectedMuonPhotonEmbIso_AfterJetSelection")),
                 prefix+"photonIso_log", "Photon #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")

        drawPlot(createPlot(ntupleCache.histogram("selectedMuonEmbIso_AfterJetSelection")),
                 prefix+"embeddingIso_log", "Isolation variable (GeV/c)", ylabel="Events / %.1f GeV/c")

        drawPlot(createPlot(ntupleCache.histogram("selectedMuonStdIso_AfterJetSelection")),
                 prefix+"standardIso_log", "Isolation variable", ylabel="Events / %.1f GeV/c")

def plotEfficiency(datasets, datasetNames, allPath, passedPath, name, xlabel, rebinBins=None, **kwargs):
    if mcOnly:
        return

    def rebin(h):
        return h.Rebin(len(rebinBins)-1, h.GetName(), array.array("d", rebinBins))
    for dname in datasetNames:
        dset = datasets.getDataset(dname)
        allHisto = dset.getDatasetRootHisto(allPath).getHistogram()
        passedHisto = dset.getDatasetRootHisto(passedPath).getHistogram()

        if allHisto.Integral() < 1:
            continue

        if rebinBins != None:
            allHisto = rebin(allHisto)
            passedHisto = rebin(passedHisto)

        eff = ROOT.TGraphAsymmErrors(passedHisto, allHisto, "cp") # 0.683 cl is default
        p = plots.PlotBase([histograms.HistoGraph(eff, dname, "p", "P")])
        if dset.isData():
            p.setLuminosity(dset.getLuminosity())
        opts = {"ymin": 0.0, "ymax": 1.1}

        plots.drawPlot(p, name+"_"+dname, xlabel, addLuminosityText=dset.isData(), opts=opts, **kwargs)


def doPlotsWTauMu(datasets, name, datasetName, ntupleCache):
    ds = datasets.getDataset(datasetName)

    # Take first unweighted histograms for the fraction plot
    drh_all = ds.getDatasetRootHisto(ntupleCache.histogram("selectedMuonPt_AfterJetSelection_Unweighted"))
    drh_pure = ds.getDatasetRootHisto(ntupleCache.histogram("selectedMuonPt_AfterJetSelection_MuFromW_Unweighted"))

    def createTEfficiency(drhAll, drhPure):
        hallUn = drhAll.getHistogram()
        hpureUn = drhPure.getHistogram()
        teff = ROOT.TEfficiency(hpureUn, hallUn)
        teff.SetDirectory(0)
        teff.SetWeight(drhAll.getDataset().getCrossSection())
        return teff
    teffs = drh_all.forEach(createTEfficiency, drh_pure)
    #coll = ROOT.TList()
    #for o in teffs:
    #    coll.AddLast(o)
    #ratio = ROOT.TEfficiency.Combine(coll)
    ratio = teffs[0]
    for e in teffs[1:]:
        ratio.Add(e)
    styles.getDataStyle().apply(ratio)
    ratio.SetName(datasetName)

    ROOT.gStyle.SetStatY(0.99)
    ROOT.gStyle.SetStatX(0.52)
    ROOT.gStyle.SetStatW(0.18)
    ROOT.gStyle.SetStatH(0.23)

    expFit = ROOT.TF1("purityFit",
                      #"1/(1+[0]*exp(-[1]*x))",
                      "1-[0]*exp(-[1]*x)",
                      #"1-([0]/(x^[1]))",
                      histograms.th1Xmin(ratio.GetPassedHistogram()), histograms.th1Xmax(ratio.GetPassedHistogram()))
    expFit.SetParameter(0, 0.05)
    #ratio.Fit(expFit)
    expFit.SetLineColor(ROOT.kRed)
    expFit.SetLineWidth(2)
    expFit = None

    # Then the correctly weighted for the main plot
    drh_all = ds.getDatasetRootHisto(ntupleCache.histogram("selectedMuonPt_AfterJetSelection"))
    drh_pure = ds.getDatasetRootHisto(ntupleCache.histogram("selectedMuonPt_AfterJetSelection_MuFromW"))
    if mcOnly:
        lumi = mcLuminosity
    else:
        lumi = datasets.getDataset("Data").getLuminosity()
    drh_all.normalizeToLuminosity(lumi)
    drh_pure.normalizeToLuminosity(lumi)
    hall = drh_all.getHistogram()
    hpure = drh_pure.getHistogram()

    hall.SetName("All")
    hpure.SetName("Pure")

    p = plots.ComparisonPlot(hall, hpure)
    p.setLuminosity(lumi)
    p.histoMgr.setHistoLegendLabelMany({
            "All": "All muons",
#            "Pure": "W#rightarrow#tau#rightarrow#mu"
            "Pure": "W#rightarrow#mu"
            })
    p.histoMgr.forEachHisto(styles.generator())

    hallErr = hall.Clone("AllError")
    hallErr.SetFillColor(ROOT.kBlue-7)
    hallErr.SetFillStyle(3004)
    hallErr.SetMarkerSize(0)
    p.prependPlotObject(hallErr, "E2")

    hpureErr = hpure.Clone("PureErr")
    hpureErr.SetFillColor(ROOT.kRed-7)
    hpureErr.SetFillStyle(3005)
    hpureErr.SetMarkerSize(0)
    p.prependPlotObject(hpureErr, "E2")

    p.createFrame(era+"_"+name+"_selectedMuonPt_AFterJetSelection_MuFromW_"+datasetName, createRatio=True, opts={"ymin": 1e-1, "ymaxfactor": 2}, opts2={"ymin": 0.9, "ymax": 1.05}
                  )
    p.setRatios([ratio])
    xmin = p.frame.GetXaxis().GetXmin()
    xmax = p.frame.GetXaxis().GetXmax()
    val = 1-0.038479
    l = ROOT.TLine(xmin, val, xmax, val)
    l.SetLineWidth(2)
    l.SetLineColor(ROOT.kBlue)
    l.SetLineStyle(4)
    p.prependPlotObjectToRatio(l)
    #p.appendPlotObjectToRatio(histograms.PlotText(0.18, 0.61, "1-0.038", size=18, color=ROOT.kBlue))
    p.appendPlotObjectToRatio(histograms.PlotText(0.18, 0.61, "0.038", size=18, color=ROOT.kBlue))
    if expFit is not None:
        p.appendPlotObjectToRatio(expFit)
    p.getFrame2().GetYaxis().SetTitle("W#rightarrow#mu fraction")

    p.getPad().SetLogy(True)
    p.setLegend(histograms.moveLegend(histograms.createLegend()))
    tmp = hpureErr.Clone("tmp")
    tmp.SetFillColor(ROOT.kBlack)
    tmp.SetFillStyle(3013)
    tmp.SetLineColor(ROOT.kWhite)
    p.legend.AddEntry(tmp, "Stat. unc.", "F")

    p.frame.GetXaxis().SetTitle("Muon p_{T} (GeV/c)")
    p.frame.GetYaxis().SetTitle("Events / %.0f GeV/c" % p.binWidth())
    p.appendPlotObject(histograms.PlotText(0.5, 0.9, plots._legendLabels.get(datasetName, datasetName), size=18))

    p.draw()
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    p.addLuminosityText()
    p.save()

    return (ratio, expFit)

def doPlotsWTauMuRatio(selectionName, ratios):
    prefix = era+"_"+selectionName+"_"

    st = [styles.StyleCompound(styles=[s, styles.StyleMarker(markerSize=1.5)]) for s in styles.getStyles()]

    p = plots.PlotBase([x[0] for x in ratios])
    p.histoMgr.setHistoDrawStyleAll("P")
    p.histoMgr.setHistoLegendStyleAll("P")
    p.histoMgr.forEachHisto(styles.Generator(st))

    def customize(plot):
        xmin = plot.frame.GetXaxis().GetXmin()
        xmax = plot.frame.GetXaxis().GetXmax()

        val = 1
        l = ROOT.TLine(xmin, val, xmax, val)
        l.SetLineWidth(2)
        l.SetLineColor(ROOT.kRed)
        l.SetLineStyle(2)
        plot.prependPlotObject(l)

        val = 1-0.038479
        l = ROOT.TLine(xmin, val, xmax, val)
        l.SetLineWidth(2)
        l.SetLineColor(ROOT.kBlue)
        l.SetLineStyle(4)
        plot.prependPlotObject(l)
        plot.appendPlotObject(histograms.PlotText(0.18, 0.57, "0.038", size=18, color=ROOT.kBlue))

    plots.drawPlot(p, prefix+"WMuFraction", "Muon p_{T} (GeV/c)", ylabel="W#rightarrow#mu fraction",
                   opts={"ymin": 0.9, "ymax": 1.02},
                   moveLegend={"dh": -0.15, "dx": -0.5},
                   customizeBeforeDraw=customize)

    #for ratio, fit, dname in ratios:
    #    pass

printed = False
def printCounters(datasets, selectionName, ntupleCache, onlyDataset=None):
    global printed
    if not printed:
        print "============================================================"
        print "Dataset info: "
        datasets.printInfo()
        printed = True


    if len(weight) == 0:
        eventCounter = counter.EventCounter(datasets, counters=counters)
        counterPath = "counters/counter"
    else:
        eventCounter = counter.EventCounter(datasets)
        counterPath = "counters/weighted/counter"

    if onlyDataset != None:
        eventCounter.removeColumns(filter(lambda n: n != onlyDataset, datasets.getAllDatasetNames()))

    eventCounter.getMainCounter().appendRows(ntupleCache.histogram(counterPath))

    if mergeMC:
        if mcOnly:
            eventCounter.normalizeMCToLuminosity(mcLuminosity)
        else:
            eventCounter.normalizeMCByLuminosity()

    table = eventCounter.getMainCounterTable()
    mcDatasets = filter(lambda n: n != "Data", table.getColumnNames())
    if len(mcDatasets) != 0:
        col = 1
        if mcOnly:
            col = 0
        table.insertColumn(col, counter.sumColumn("MCSum", [table.getColumn(name=name) for name in mcDatasets]))

    cellFormat = counter.TableFormatText(counter.CellFormatText(valueFormat='%.3f'))
#    cellFormat = counter.TableFormatText(counter.CellFormatTeX(valueFormat='%.1f'))
    output = table.format(cellFormat)

    print
    print "########################################"
    print "Selection", selectionName
    print output

    prefix = era+"_"+selectionName+"_counters"
    if len(weight) == 0:
        prefix += "_nonweighted"
    f = open(prefix+".txt", "w")
    f.write(output)
    f.close()
    

if __name__ == "__main__":
    main()
