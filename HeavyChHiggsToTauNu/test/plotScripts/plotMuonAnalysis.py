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
import math
import array
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tauEmbedding as tauEmbedding
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.pileupReweightedAllEvents import PileupWeightType

analysis = "muonNtuple"
counters = analysis+"Counters"
countersWeighted = counters+"/weighted"

era = "Run2011AB"
#era = "Run2012ABCD"
#era = "Run2012ABC"
#era = "Run2012D"
doWeighted = True
doTopPtReweighting = True
#doTopPtReweighting = False
doVariations = True
#doVariations = False
topPtReweightingScheme = "" # default
#topPtReweightingScheme = "TopPtWeightSeparate"
topPtReweightingBranch = "topPtWeight"

mcOnly = True
mcOnly = False
mcLuminosity = 5049.069000

mergeMC = True
#mergeMC = False

#muonDir = "/home/mjkortel/data/embedding/v44_5/multicrab_muonAnalysis_130918_105847"
muonDir = "/home/mjkortel/data/embedding/v44_5/multicrab_muonAnalysis_131125_140216"
if "2012" in era:
    muonDir = "/home/mjkortel/data/embedding/v53_3/multicrab_muonAnalysis_130917_121833"

def splitWJets(datasets):
    wjetsName = "WJets_TuneZ2_Fall11"

    wjets = datasets.getDataset(wjetsName).deepCopy()
    wjets.setName(wjetsName+"_B")
    datasets.append(wjets)
    datasets.rename(wjetsName, wjetsName+"_NoB")

    plots._physicalToLogical.update({
            wjetsName+"_NoB": "WJets_NoB",
            wjetsName+"_B": "WJets_B",
            })

    wjetsIndex = plots._datasetOrder.index("WJets")
    plots._datasetOrder.insert(wjetsIndex+1, "WJets_NoB")
    plots._datasetOrder.insert(wjetsIndex+2, "WJets_B")
    plots._legendLabels.update({
            "WJets_NoB": "W+jets (no b)",
            "WJets_B":   "W+b+jets",
            })
    wStyle = plots._plotStyles["WJets"]
    w2Style = wStyle.clone()
    w2Style.color = ROOT.kOrange+7
    plots._plotStyles.update({
            "WJets_NoB": wStyle,
            "WJets_B": w2Style
            })

def splitDYJets(datasets):
    dyjetsName = "DYJetsToLL_M50_TuneZ2_Fall11"

    dyjets = datasets.getDataset(dyjetsName).deepCopy()
    dyjets.setName(dyjetsName+"_B")
    datasets.append(dyjets)
    datasets.rename(dyjetsName, dyjetsName+"_NoB")

    plots._physicalToLogical.update({
            dyjetsName+"_NoB": "DYJetsToLL_NoB",
            dyjetsName+"_B": "DYJetsToLL_B",
            })

    wjetsIndex = plots._datasetOrder.index("DYJetsToLL")
    plots._datasetOrder.insert(wjetsIndex+1, "DYJetsToLL_NoB")
    plots._datasetOrder.insert(wjetsIndex+2, "DYJetsToLL_B")
    plots._legendLabels.update({
            "DYJetsToLL_NoB": "Z/#gamma*+jets (no b)",
            "DYJetsToLL_B":   "Z/#gamma*+b+jets",
            })
    dyStyle = plots._plotStyles["DYJetsToLL"]
    dy2Style = dyStyle.clone()
    dy2Style.color = ROOT.kTeal-8
    plots._plotStyles.update({
            "DYJetsToLL_NoB": dyStyle,
            "DYJetsToLL_B": dy2Style
            })

def main(opts):
    datasets = dataset.getDatasetsFromMulticrabCfg(directory=muonDir, weightedCounters=doWeighted, dataEra=era, analysisName=analysis, useAnalysisNameOnly=True)
    args = {}
    if doTopPtReweighting:
        args["topPtWeightType"] = PileupWeightType.NOMINAL

        if topPtReweightingScheme != "":
            ttjetsName = filter(lambda n: "TTJets" in n, datasets.getMCDatasetNames())[0]
            datasets.getDataset(ttjetsName).info["topPtReweightScheme"] = topPtReweightingScheme
    datasets.updateNAllEventsToPUWeighted(era=era, **args)

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

#    splitWJets(datasets)
#    splitDYJets(datasets)

    if mergeMC:
        plots.mergeRenameReorderForDataMC(datasets)

    styleGenerator = styles.generator(fill=True)

    style = tdrstyle.TDRStyle()
    #histograms.createLegend.moveDefaults(dx=-0.15)
    plots._legendLabels["QCD_Pt20_MuEnriched"] = "QCD"
    histograms.createLegend.moveDefaults(dx=-0.04)

    wtaumuRatioFile = ROOT.TFile.Open("embedding-wtaumuRatio.root", "RECREATE")
#    ROOT.TH1.AddDirectory(False)

    selectorArgs = tauEmbedding.MuonAnalysisSelectorArgs(era=era, isolationMode="chargedHadrRel10",
                                                         topPtReweighting=doTopPtReweighting,
                                                         topPtReweightingScheme=topPtReweightingBranch)
    args = {}
    if opts.cache is not None:
        args["cacheFileName"] = opts.cache
    ntupleCache = dataset.NtupleCache("tree", "MuonAnalysisSelector",
                                      selectorArgs=selectorArgs,
                                      process=opts.process,
                                      #maxEvents=1000,
                                      **args
                                      )

    ntupleCache.addSelector("FullStandardIso", "MuonAnalysisSelector", selectorArgs.clone(isolationMode="standard"))
    variations = []
    if doVariations:
        def doVar(name, **kwargs):
            ntupleCache.addSelector(name, "MuonAnalysisSelector", selectorArgs.clone(**kwargs))
            variations.append(name)

        doVar("SystVarPUWeightPlus", puVariation="up")
        doVar("SystVarPUWeightMinus", puVariation="down")
        if doTopPtReweighting:
            doVar("SystVarTopPtWeightPlus", topPtReweightingScheme=topPtReweightingBranch+"Plus")
            doVar("SystVarTopPtWeightMinus", topPtReweightingScheme=topPtReweightingBranch+"Minus")

    selections = [
#        ("FullTauLike", "taulike"),
#        ("FullNoIso", "disabled"),
#        ("FullStandardIso", "standard"),
#        ("FullChargedHadrRelIso10", "chargedHadrRel10"),
#        ("FullChargedHadrRelIso15", "chargedHadrRel15"),

        ("FullStandardIso", "FullStandardIso"),
        ("FullChargedHadrRelIso10", None)
        ]
    for v in variations:
        selections.append( ("FullChargedHadrRelIso10"+v, v) )

    print selections

#    for name, isolation in selections:
    allRatios = {}
    for name, selectorName in selections:
        # ntupleCache = dataset.NtupleCache("tree", "MuonAnalysisSelector",
        #                                   ,
        #                                   cacheFileName="histogramCache-%s.root" % name,
        #                                   process=opts.process,
        #                                   #maxEvents=10000,
        #                                   )
        # ntupleCache.setDatasetSelectorArgs({
        #         "WJets_NoB": tauEmbedding.MuonAnalysisSelectorArgs(bquarkMode="breject"),
        #         "WJets_B": tauEmbedding.MuonAnalysisSelectorArgs(bquarkMode="baccept"),
        #         "DYJetsToLL_NoB": tauEmbedding.MuonAnalysisSelectorArgs(bquarkMode="breject"),
        #         "DYJetsToLL_B": tauEmbedding.MuonAnalysisSelectorArgs(bquarkMode="baccept"),
        #         })


#        doPlots(datasets, name, ntupleCache, selectorName)
#        printCounters(datasets, name, ntupleCache, selectorName)
#        printCounters(datasets, name, ntupleCache, onlyDataset="TTJets")

        if True and "FullChargedHadrRelIso10" in name:
            def dop(unweighted, fitFunction):
                directory = wtaumuRatioFile.mkdir(name)
                ratios = []
                rebin = {
                    "TTJets": range(0, 350, 10) + [350, 400],
                    "WJets": range(0, 260, 10) + range(260, 300, 20) + [300, 350, 400],
                    "SingleTop": range(0, 200, 10) + range(200, 300, 20) + [300, 400]
                    }
                for dname in ["TTJets", "WJets", "SingleTop"]:
                #for dname in ["TTJets"]:
                    (ratio, fit) = doPlotsWTauMu(datasets, name, dname, ntupleCache, selectorName, unweighted, fitFunction, rebin=rebin[dname])
                    cl = ratio.Clone()
                    cl.SetDirectory(directory)
                    ratios.append( (ratio, fit, dname) )

                doPlotsWTauMuRatio(datasets, name, ratios, unweighted, fitFunction)
                return ratios

            #dop("", 2)
            if "SystVar" in name:
                tmp = dop("", 2)
                for ratio, fit, dname in tmp:
                    if dname == "TTJets":
                        allRatios[name] = (ratio, fit)
            else:
                for w in ["", "_Unweighted"]:
                    for fitFunction in [0, 1, 2]:
                        tmp = dop(w, fitFunction)
#                        break
                        if w == "":
                            n = name
                            if fitFunction != 2:
                                n += "SystFunc%d" % fitFunction
                            for ratio, fit, dname in tmp:
                                if dname == "TTJets":
                                    allRatios[n] = (ratio, fit)
                                elif fitFunction == 2:
                                    allRatios[name+"Syst"+dname] = (ratio, fit)
#                    break

    keys = allRatios.keys()
    keys.sort()
    print "\n".join(keys)
    doPlotsWTauMuRatioUncertaintyEstimate(datasets, allRatios, "FullChargedHadrRelIso10")
    fitLine = allRatios["FullChargedHadrRelIso10"][1]
    print "Fit result: p0 %f, p1 %f" % (fitLine.GetParameter(0), fitLine.GetParameter(1))


    wtaumuRatioFile.Write()
    wtaumuRatioFile.Close()

def doPlots(datasets, selectionName, ntupleCache, selectorName):
    def createPlot(name, **kwargs):
        args = kwargs.copy()
        if mcOnly:
            args["normalizeToLumi"] = mcLuminosity
        return plots.DataMCPlot(datasets, ntupleCache.histogram(name, selectorName), **args)
    drawPlot = plots.PlotDrawer(stackMCHistograms=True, addMCUncertainty=True, log=True, ratio=not mcOnly, addLuminosityText=True,
                                ratioYlabel="Ratio",
                                optsLog={"ymin": 1e-1},
                                opts2={"ymin": 0, "ymax": 2},
                                #opts2={"ymin": 0.6, "ymax": 1.4},
                                )

    metBinning = range(0, 200, 10) + range(200, 300, 20) + [300, 350, 400]
    ptBinning = range(0, 40, 10)+[41] + range(50, 200, 10) + range(200, 400, 20)
    zoomedOpts2 = {"ymin": 0.6, "ymax": 1.4}


    prefix = era+"_"+selectionName+"_"
    drawPlot(createPlot("selectedMuonPt_AfterJetSelection"),
             prefix+"muon_pt_log", "Muon p_{T} (GeV/c)", ylabel="dN/dp_{T} / %.0f-%.0f GeV/c", cutBox={"cutValue":41, "greaterThan":True}, rebin=ptBinning, divideByBinWidth=True, opts2=zoomedOpts2)
    drawPlot(createPlot("selectedMuonEta_AfterJetSelection"),
             prefix+"muon_eta", "Muon #eta", ylabel="Events / %.1f", cutLine=[-2.1, 2.1], log=False, rebin=5)
    drawPlot(createPlot("selectedMuonPhi_AfterJetSelection"),
             prefix+"muon_phi", "Muon #phi", ylabel="Events / %.1f", log=False, rebin=8)


    drawPlot(createPlot("uncorrectedMet_AfterJetSelection"),
             prefix+"rawmet_pt_log", "Uncorrected PF E_{T}^{miss} (GeV)", ylabel="dN/dE_{T}^{miss} / %.0f-%.0f 1/GeV", rebin=metBinning, divideByBinWidth=True)

    drawPlot(createPlot("transverseMassUncorrectedMet_AfterJetSelection"),
             prefix+"rawmt_log", "m_{T}(#mu, E_{T}^{miss}) (GeV/c^{2})", ylabel="dN/dm_{T} / %.0f-%.0f 1/GeV/c^{2}", rebin=metBinning, divideByBinWidth=True)

    drawPlot(createPlot("type1Met_AfterJetSelection"),
             prefix+"met_pt_log", "Type-1 PF E_{T}^{miss} (GeV)", ylabel="dN/dE_{T}^{miss} / %.0f-%.0f 1/GeV", rebin=metBinning, divideByBinWidth=True, opts2=zoomedOpts2)
    drawPlot(createPlot("type1MetPhi_AfterJetSelection"),
             prefix+"met_phi", "Type-1 PF E_{T}^{miss} #phi", ylabel="Events / %.2f", log=False, rebin=2, moveLegend={"dy": -0.4})

    drawPlot(createPlot("transverseMassType1Met_AfterJetSelection"),
             prefix+"mt_log", "m_{T}(#mu, E_{T}^{miss}) (GeV/c^{2})", ylabel="dN/dm_{T} / %.0f-%.0f 1/GeV/c^{2}", rebin=metBinning, divideByBinWidth=True, opts2=zoomedOpts2)

    drawPlot(createPlot("nbjets_AfterJetSelection"),
             prefix+"nbjets_log", "Number of b jets", ylabel="Events")


    for x in ["0", "1", "2", "ging"]:
        drawPlot(createPlot("selectedMuonPt_AfterBTag%s"%x),
                 prefix+"muon_pt_btag%s_log"%x, "Muon p_{T} (GeV/c)", ylabel="dN/dp_{T} / %.0f-%.0f GeV/c", cutBox={"cutValue":41, "greaterThan":True}, rebin=ptBinning, divideByBinWidth=True)
        drawPlot(createPlot("type1Met_AfterBTag%s"%x),
                 prefix+"met_pt_btag%s_log"%x, "Type-1 PF E_{T}^{miss} (GeV)", ylabel="dN/dE_{T}^{miss} / %.0f-%.0f GeV", rebin=metBinning, divideByBinWidth=True)
        drawPlot(createPlot("transverseMassType1Met_AfterBTag%s"%x),
                 prefix+"mt_btag%s_log"%x, "m_{T}(#mu, E_{T}^{miss}) (GeV/c^{2})", ylabel="dN/dm_{T} / %.0f-%.0f 1/GeV/c^{2}", rebin=metBinning, divideByBinWidth=True)

    drawPlot(createPlot("type1MetPhi_AfterBTagging"),
             prefix+"met_phi_btagging", "Type-1 PF E_{T}^{miss} #phi ", ylabel="Events / %.2f", log=False, rebin=2, moveLegend={"dy": -0.4})

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
        drawPlot(createPlot("selectedMuonChargedHadronEmbIso_AfterJetSelection"),
                 prefix+"chargedHadronIso_log", "Charged hadron #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")
        drawPlot(createPlot("selectedMuonPuChargedHadronEmbIso_AfterJetSelection"),
                 prefix+"puChargedHadronIso_log", "Charged hadron #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")
        drawPlot(createPlot("selectedMuonNeutralHadronEmbIso_AfterJetSelection"),
                 prefix+"neutralHadronIso_log", "Neutral hadron #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")
        drawPlot(createPlot("selectedMuonPhotonEmbIso_AfterJetSelection"),
                 prefix+"photonIso_log", "Photon #Sigma p_{T} (GeV/c)", ylabel="Events / %.1f GeV/c")

        drawPlot(createPlot("selectedMuonEmbIso_AfterJetSelection"),
                 prefix+"embeddingIso_log", "Isolation variable (GeV/c)", ylabel="Events / %.1f GeV/c")

        drawPlot(createPlot("selectedMuonStdIso_AfterJetSelection"),
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


def doPlotsWTauMu(datasets, name, datasetName, ntupleCache, selectorName, unweighted, fitFunction, rebin=None):
    ds = datasets.getDataset(datasetName)

    # Take first unweighted histograms for the fraction plot
    drh_all = ds.getDatasetRootHisto(ntupleCache.histogram("selectedMuonPt_AfterJetSelection"+unweighted, selectorName))
    drh_pure = ds.getDatasetRootHisto(ntupleCache.histogram("selectedMuonPt_AfterJetSelection_MuFromW"+unweighted, selectorName))

    def Rebin(th1, div=False):
        if rebin is None:
            return th1
        else:
            h = th1.Rebin(len(rebin)-1, th1.GetName(), array.array("d", rebin))
            if div:
                h.Scale(1, "width")
            return h

    def createTEfficiency(drhAll, drhPure):
        hallUn = Rebin(drhAll.getHistogram())
        hpureUn = Rebin(drhPure.getHistogram())
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
                      ["1/(1+[0]*exp(-[1]*x))",
                       "1-[0]*exp(-[1]*x)",
                       "1-([0]/(x^[1]))",
                       ][fitFunction],
                      aux.th1Xmin(ratio.GetPassedHistogram()), aux.th1Xmax(ratio.GetPassedHistogram()))
    expFit.SetParameter(0, 0.05)
    ratio.Fit(expFit, "N")
    expFit.SetLineColor(ROOT.kRed)
    expFit.SetLineWidth(2)
#    expFit = None

    # Then the correctly weighted for the main plot
    drh_all = ds.getDatasetRootHisto(ntupleCache.histogram("selectedMuonPt_AfterJetSelection", selectorName))
    drh_pure = ds.getDatasetRootHisto(ntupleCache.histogram("selectedMuonPt_AfterJetSelection_MuFromW", selectorName))
    if mcOnly:
        lumi = mcLuminosity
    else:
        lumi = datasets.getDataset("Data").getLuminosity()
    drh_all.normalizeToLuminosity(lumi)
    drh_pure.normalizeToLuminosity(lumi)
    hall = Rebin(drh_all.getHistogram(), div=True)
    hpure = Rebin(drh_pure.getHistogram(), div=True)

    hall.SetName("All")
    hpure.SetName("Pure")

    p = plots.ComparisonPlot(hall, hpure)
    p.setLuminosity(lumi)
    p.setEnergy(ds.getEnergy())
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

    p.createFrame(era+"_"+name+"_selectedMuonPt_AFterJetSelection_MuFromW_%s_fit%d"%(datasetName, fitFunction)+unweighted, createRatio=True, opts={"ymin": 1e-1, "ymaxfactor": 2}, opts2={"ymin": 0.9, "ymax": 1.05}
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
    p.frame.GetYaxis().SetTitle("Events / #Deltap_{T} %.0f-%.0f GeV/c" % (min(p.binWidths()), max(p.binWidths())))
    p.appendPlotObject(histograms.PlotText(0.5, 0.9, plots._legendLabels.get(datasetName, datasetName), size=18))

    p.draw()
    p.addStandardTexts()
    p.save()

    # Clear list of functions
    ratio.GetListOfFunctions().Delete();

    return (ratio, expFit)

def doPlotsWTauMuRatio(dsetMgr, selectionName, ratios, unweighted, fitFunction):
    prefix = era+"_"+selectionName+"_fitFunction%d"%fitFunction+unweighted+"_"

    st = [s.clone() for s in styles.getStyles()]
    st[0].marker = 33
    st[1].marker = 26
    st[2].marker = 32
    st = [styles.StyleCompound(styles=[s, styles.StyleMarker(markerSize=1.5)]) for s in st]


    # Do clone to get rid of statistics box
    p = plots.PlotBase([x[0].Clone() for x in ratios])
    p.setEnergy(dsetMgr.getEnergies())
    p.histoMgr.setHistoDrawStyleAll("P")
    p.histoMgr.setHistoLegendStyleAll("P")
    p.histoMgr.forEachHisto(styles.Generator(st))
    for i, x in enumerate(ratios):
        fitLine = x[1]
        st[i].apply(fitLine)
        p.appendPlotObject(fitLine)

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

def doPlotsWTauMuRatioUncertaintyEstimate(dsetMgr, ratios, analysisName):
    prefix = era+"_"

    st = [s.clone() for s in styles.getStyles()]
    st[0].marker = 33
    st = [styles.StyleCompound(styles=[s, styles.StyleMarker(markerSize=1.5)]) for s in st]

    # Nominal
    p = plots.PlotBase([ratios[analysisName][0].Clone()])
    p.setEnergy(dsetMgr.getEnergies())
    p.histoMgr.setHistoDrawStyleAll("P")
    p.histoMgr.setHistoLegendStyleAll("P")
    p.histoMgr.forEachHisto(styles.Generator(st))

    fitLine = ratios[analysisName][1]
    st[0].apply(fitLine)
    p.appendPlotObject(fitLine)

    # Stat. unc. from parameters
    pars = [fitLine.GetParameter(i) for i in xrange(0, fitLine.GetNpar())]
    parErrors = [fitLine.GetParError(i) for i in xrange(0, fitLine.GetNpar())]
    def evalPar(x, i, shift):
        pars_ = pars[:]
        pars_[i] += shift
        return fitLine.EvalPar(x, array.array("d", pars_))
        
    # Fit function
    fits = [
        ratios[analysisName+"SystFunc0"][1],
        ratios[analysisName+"SystFunc1"][1]
        ]
    def maxDiff(x, tf1s, nominal):
        return max([abs(tf1.Eval(x[0])-nominal) for tf1 in tf1s])

    # Sample
    samples = [
         ratios[analysisName+"SystWJets"][1],
         ratios[analysisName+"SystSingleTop"][1]
         ]

    # Weight systematic variations
    keys = filter(lambda n: "SystVar" in n, ratios.keys())
    weightSources = {}
    for key in keys:
        src = key[key.find("SystVar")+7:].replace("Plus", "").replace("Minus", "")
#        if src != "TopPtWeight":
#            continue
#        if src != "PUWeight":
#            continue
#        print src

        if not src in weightSources:
            weightSources[src] = [ratios[key][1]]
        else:
            weightSources[src].append(ratios[key][1])

    def comb(plus, x, p):
        nominal = fitLine.Eval(x[0])
        diff = 0

        # stat unc
        uncStat = 0.0
        for i, parErr in enumerate(parErrors):
            diffI = max(abs(evalPar(x, i, parErr)-nominal), abs(evalPar(x, i, -parErr))-nominal)
            uncStat += diffI**2
        diff += uncStat
            
        # Fit function
        diffFit = maxDiff(x, fits, nominal)
        diff += diffFit**2

        # Sample
        diffSample = maxDiff(x, samples, nominal)
        diff += diffSample**2

        # Weights
        for src, tf1s in weightSources.iteritems():
            diffWeight = maxDiff(x, tf1s, nominal)
            diff += diffWeight**2


        diff = math.sqrt(diff)
        if plus:
            ret = nominal + diff
        else:
            ret = nominal - diff

        if ret > 1:
            ret = 1.0
        if ret < 0:
            ret = 0.0

#        if ret > 0:
#            print x[0], (ret-nominal)/ret

        return ret


    p.appendPlotObject(ROOT.TF1("combPlus", lambda x, p: comb(True, x, p), fitLine.GetXmin(), fitLine.GetXmax(), fitLine.GetNpar()))
    p.appendPlotObject(ROOT.TF1("combMinus", lambda x, p: comb(False, x, p), fitLine.GetXmin(), fitLine.GetXmax(), fitLine.GetNpar()))

    # Simple relative uncertainty
    def rel(x):
        return 0.012
    def relUnc(plus, x, p):
        nominal = fitLine.Eval(x[0])
        if plus:
            f = 1+rel(x[0])
        else:
            f = 1-rel(x[0])
        return nominal * f

    relPlus = ROOT.TF1("relPlus", lambda x, p: relUnc(True, x, p), fitLine.GetXmin(), fitLine.GetXmax(), fitLine.GetNpar())
    relMinus = ROOT.TF1("relMinus", lambda x, p: relUnc(False, x, p), fitLine.GetXmin(), fitLine.GetXmax(), fitLine.GetNpar())
    relPlus.SetLineColor(ROOT.kGreen)
    relMinus.SetLineColor(ROOT.kGreen)
    p.appendPlotObject(relPlus)
    p.appendPlotObject(relMinus)


    def customize(plot):
        xmin = plot.frame.GetXaxis().GetXmin()
        xmax = plot.frame.GetXaxis().GetXmax()
        ymin = plot.frame.GetYaxis().GetXmin()
        ymax = plot.frame.GetYaxis().GetXmax()

        val = 1
        l = ROOT.TLine(xmin, val, xmax, val)
        l.SetLineWidth(2)
        l.SetLineColor(ROOT.kRed)
        l.SetLineStyle(2)
        plot.prependPlotObject(l)

        l = ROOT.TLine(41, ymin, 41, ymax)
        l.SetLineWidth(2)
        l.SetLineColor(ROOT.kRed)
        l.SetLineStyle(2)
        plot.prependPlotObject(l)

    plots.drawPlot(p, prefix+"WMuFractionUncertainty", "Muon p_{T} (GeV/c)", ylabel="W#rightarrow#mu fraction",
                   opts={"ymin": 0.9, "ymax": 1.02},
                   createLegend=None,
                   #moveLegend={"dh": -0.15, "dx": -0.5},
                   customizeBeforeDraw=customize)

printed = False
def printCounters(datasets, selectionName, ntupleCache, selectorName, onlyDataset=None):
    global printed
    if not printed:
        print "============================================================"
        print "Dataset info: "
        datasets.printInfo()
        printed = True


    if not doWeighted:
        eventCounter = counter.EventCounter(datasets, counters=counters)
        counterPath = "counters/counter"
    else:
        eventCounter = counter.EventCounter(datasets)
        counterPath = "counters/weighted/counter"

    if onlyDataset != None:
        eventCounter.removeColumns(filter(lambda n: n != onlyDataset, datasets.getAllDatasetNames()))

    eventCounter.getMainCounter().appendRows(ntupleCache.histogram(counterPath, selectorName))

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
    if not doWeighted:
        prefix += "_nonweighted"
    f = open(prefix+".txt", "w")
    f.write(output)
    f.close()
    

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--process", dest="process", default=False, action="store_true",
                      help="Process ntuples")
    parser.add_option("--cache", dest="cache", default=None, type="string",
                      help="Cache file (if not default)")
    (opts, args) = parser.parse_args()
    main(opts)
