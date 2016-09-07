#!/usr/bin/env python

import os
import sys
import ROOT
import array

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

from PythonWriter import PythonWriter
pythonWriter = PythonWriter()

ROOT.gROOT.SetBatch(True)
plotDir = "TauLeg2016"

formats = [".pdf",".png"]

def usage():
    print "\n"
    print "### Usage:   "+sys.argv[0]+" <multicrab dir>\n"
    print "\n"
    sys.exit()

def fit(name,plot,graph,min,max):
    function = ROOT.TF1("fit"+name, "0.5*[0]*(1+TMath::Erf( (sqrt(x)-sqrt([1]))/(sqrt(2)*[2]) ))", min, max);
    function.SetParameters(1., 50., 1.);
    function.SetParLimits(0, 0.0, 1.0);
    fitResult = graph.Fit(function, "NRSE+EX0");
    aux.copyStyle(graph, function)
    plot.appendPlotObject(function)

def getEfficiency(datasets,numerator="Numerator",denominator="Denominator"):

#    statOption = ROOT.TEfficiency.kFNormal
    statOption = ROOT.TEfficiency.kFCP # Clopper-Pearson
#    statOption = ROOT.TEfficiency.kFFC # Feldman-Cousins

    first = True
    isData = False

    teff = ROOT.TEfficiency()
    for dataset in datasets:
        n = dataset.getDatasetRootHisto(numerator).getHistogram()                                               
        d = dataset.getDatasetRootHisto(denominator).getHistogram()

        if d.GetEntries() == 0:
            continue

        checkNegatives(n,d)

#        removeNegatives(n)
#        removeNegatives(d)
        print dataset.getName(),"entries",n.GetEntries(),d.GetEntries()
        print "    bins",n.GetNbinsX(),d.GetNbinsX()
        print "    lowedge",n.GetBinLowEdge(1),d.GetBinLowEdge(1)
        eff = ROOT.TEfficiency(n,d)
        eff.SetStatisticOption(statOption)

        weight = 1
        if dataset.isMC():
            weight = dataset.getCrossSection()
            for i in range(1,d.GetNbinsX()+1):
                print "    bin",i,d.GetBinLowEdge(i),n.GetBinContent(i),d.GetBinContent(i)
        eff.SetWeight(weight)

        if first:
            teff = eff
            if dataset.isData():
                tn = n
                td = d
            first = False
        else:
            teff.Add(eff)
            if dataset.isData():
                tn.Add(n)
                td.Add(d)
    if isData:
        teff = ROOT.TEfficiency(tn, td)
        teff.SetStatisticOption(self.statOption)
    return convert2TGraph(teff)

def checkNegatives(n,d):
    for i in range(1,n.GetNbinsX()+1):
        nbin = n.GetBinContent(i)
        dbin = d.GetBinContent(i)
        print "Bin",i,"Numerator=",nbin,", denominator=",dbin
        if nbin > dbin:
#            if nbin < dbin*1.005:
                n.SetBinContent(i,dbin)
#            else:
##                print "Bin",i,"Numerator=",nbin,", denominator=",dbin
#                print "REBIN!",n.GetBinLowEdge(i),"-",n.GetBinLowEdge(i)+n.GetBinWidth(i)
##                sys.exit()
        if nbin < 0:
            n.SetBinContent(i,0)
        if dbin < 0:
            n.SetBinContent(i,0)
            d.SetBinContent(i,0)

def removeNegatives(histo):
    for bin in range(histo.GetNbinsX()):
        if histo.GetBinContent(bin) < 0:
            histo.SetBinContent(bin,0.)

def convert2TGraph(tefficiency):
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    h = tefficiency.GetCopyTotalHisto()
    n = h.GetNbinsX()
    for i in range(1,n+1):
        x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
        xerrl.append(0.5*h.GetBinWidth(i))
        xerrh.append(0.5*h.GetBinWidth(i))
        y.append(tefficiency.GetEfficiency(i))
        yerrl.append(tefficiency.GetEfficiencyErrorLow(i))
        # ugly hack to prevent error going above 1                                                                                                              
        errUp = tefficiency.GetEfficiencyErrorUp(i)
        if y[-1] == 1.0:
            errUp = 0
        yerrh.append(errUp)
    return ROOT.TGraphAsymmErrors(n,array.array("d",x),
                                    array.array("d",y),
                                    array.array("d",xerrl),
                                    array.array("d",xerrh),
                                    array.array("d",yerrl),
                                    array.array("d",yerrh))

def Print(graph):
    N = graph.GetN()
    for i in range(N):
        x = ROOT.Double()
        y = ROOT.Double()
        graph.GetPoint(i,x,y)
        print "x,y",x,y


def analyze(analysis=None):

    paths = [sys.argv[1]]

    if not analysis == None:
        datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,excludeTasks="Silver|GluGluHToTauTau_M125")
    else:
        datasets = dataset.getDatasetsFromMulticrabDirs(paths,excludeTasks="Silver|GluGluHToTauTau_M125")
        analysis = datasets.getAllDatasets()[0].getAnalysisName()

#    datasetsDY = None
    datasetsDY = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,includeOnlyTasks="DYJetsToLL")
#    datasets = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,excludeTasks="GluGluHToTauTau_M125|TTJets")
    datasetsH125 = None
#    datasetsH125 = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,includeOnlyTasks="GluGluHToTauTau_M125",emptyDatasetsAsNone=True)
#    datasetsH125 = dataset.getDatasetsFromMulticrabDirs(paths,analysisName=analysis,includeOnlyTasks="GluGluHToTauTau_M125")

    datasets.loadLuminosities()

    style = tdrstyle.TDRStyle()

    dataset1 = datasets.getDataDatasets()
    dataset2 = dataset1
#    dataset2 = datasets.getMCDatasets()
    if not datasetsDY == None:
        dataset2 = datasetsDY.getMCDatasets()


    eff1 = getEfficiency(dataset1)
    eff2 = getEfficiency(dataset2)
    if isinstance(datasetsH125,dataset.DatasetManager):
        eff3 = getEfficiency(datasetsH125.getMCDatasets())


    styles.dataStyle.apply(eff1)
    styles.mcStyle.apply(eff2)
    eff1.SetMarkerSize(1)
#    eff2.SetMarkerSize(1.5)
    if isinstance(datasetsH125,dataset.DatasetManager):
        styles.mcStyle.apply(eff3)
        eff3.SetMarkerSize(1.5)
        eff3.SetMarkerColor(4)
        eff3.SetLineColor(4)

#    p = plots.ComparisonPlot(histograms.HistoGraph(eff1, "eff1", "p", "P"),
#                             histograms.HistoGraph(eff2, "eff2", "p", "P"))

    if isinstance(datasetsH125,dataset.DatasetManager):
        p = plots.ComparisonManyPlot(histograms.HistoGraph(eff1, "eff1", "p", "P"),
                                    [histograms.HistoGraph(eff2, "eff2", "p", "P"),
                                     histograms.HistoGraph(eff3, "eff3", "p", "P")])
    elif isinstance(datasetsDY,dataset.DatasetManager):
        p = plots.ComparisonPlot(histograms.HistoGraph(eff1, "eff1", "p", "P"),
                                 histograms.HistoGraph(eff2, "eff2", "p", "P"))
    else:
        p = plots.PlotBase([histograms.HistoGraph(eff1, "eff1", "p", "P")])


    fit("Data",p,eff1,20,200)
    fit("MC",p,eff2,20,200)
    if isinstance(datasetsH125,dataset.DatasetManager):
        fit("H125",p,eff3,20,200)

    opts = {"ymin": 0, "ymax": 1.1}
    opts2 = {"ymin": 0.5, "ymax": 1.5}
#    moveLegend = {"dx": -0.55, "dy": -0.15, "dh": -0.1}
    moveLegend = {"dx": -0.2, "dy": -0.5, "dh": -0.1}
    name = "TauMET_"+analysis+"_DataVsMC_PFTauPt"

    legend1 = "Data"
    legend2 = "MC (DY)"
    legend3 = "MC (H125)"
    createRatio = False
    p.histoMgr.setHistoLegendLabelMany({"eff1": legend1})
    if isinstance(datasetsDY,dataset.DatasetManager):
        p.histoMgr.setHistoLegendLabelMany({"eff1": legend1, "eff2": legend2})
        createRatio = True
    if isinstance(datasetsH125,dataset.DatasetManager):
        p.histoMgr.setHistoLegendLabelMany({"eff1": legend1, "eff2": legend2, "eff3": legend3})

    if createRatio:
        p.createFrame(os.path.join(plotDir, name), createRatio=createRatio, opts=opts, opts2=opts2)
    else:
        p.createFrame(os.path.join(plotDir, name), opts=opts, opts2=opts2)
    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

    p.getFrame().GetYaxis().SetTitle("HLT tau efficiency")
    p.getFrame().GetXaxis().SetTitle("#tau-jet p_{T} (GeV/c)")
    if createRatio:
        p.getFrame2().GetYaxis().SetTitle("Ratio")
        p.getFrame2().GetYaxis().SetTitleOffset(1.6)

    histograms.addText(0.5, 0.6, "LooseIsoPFTau50_Trk30_eta2p1", 17)
    label = analysis.split("_")[len(analysis.split("_")) -1]
    histograms.addText(0.5, 0.53, label, 17)
    runRange = datasets.loadRunRange()
    histograms.addText(0.5, 0.46, "Runs "+runRange, 17)

    p.draw()
    lumi = 0.0
    for d in datasets.getDataDatasets():
        print "luminosity",d.getName(),d.getLuminosity()
        lumi += d.getLuminosity()
    print "luminosity, sum",lumi
    histograms.addStandardTexts(lumi=lumi)

    if not os.path.exists(plotDir):
        os.mkdir(plotDir)
    p.save(formats)


    pythonWriter.addParameters(plotDir,label,runRange,lumi,eff1)
    pythonWriter.addMCParameters(label,eff2)

    pythonWriter.writeJSON(os.path.join(plotDir,"tauLegTriggerEfficiency_"+label+".json"))

#    if not createRatio:
#        sys.exit()

    #########################################################################                                                                                                                              

    eff1eta = getEfficiency(dataset1,"NumeratorEta","DenominatorEta")
    eff2eta = getEfficiency(dataset2,"NumeratorEta","DenominatorEta")
    if isinstance(datasetsH125,dataset.DatasetManager):
        eff3eta = getEfficiency(datasetsH125.getMCDatasets(),"NumeratorEta","DenominatorEta")

    styles.dataStyle.apply(eff1eta)
    styles.mcStyle.apply(eff2eta)
    eff1eta.SetMarkerSize(1)

    if isinstance(datasetsH125,dataset.DatasetManager):
        styles.mcStyle.apply(eff3eta)
        eff3eta.SetMarkerSize(1.5)
        eff3eta.SetMarkerColor(4)
        eff3eta.SetLineColor(4)


    if isinstance(datasetsH125,dataset.DatasetManager):
        p_eta = plots.ComparisonManyPlot(histograms.HistoGraph(eff1eta, "eff1eta", "p", "P"),
                                        [histograms.HistoGraph(eff2eta, "eff2eta", "p", "P"),
                                         histograms.HistoGraph(eff3eta, "eff3eta", "p", "P")])
    elif isinstance(datasetsDY,dataset.DatasetManager):
        p_eta = plots.ComparisonPlot(histograms.HistoGraph(eff1eta, "eff1eta", "p", "P"),
                                     histograms.HistoGraph(eff2eta, "eff2eta", "p", "P"))
    else:
        p_eta = plots.PlotBase([histograms.HistoGraph(eff1eta, "eff1eta", "p", "P")])

    p_eta.histoMgr.setHistoLegendLabelMany({"eff1eta": legend1})
    if isinstance(datasetsDY,dataset.DatasetManager):
        p_eta.histoMgr.setHistoLegendLabelMany({"eff1eta": legend1, "eff2eta": legend2})
    if isinstance(datasetsH125,dataset.DatasetManager):
        p_eta.histoMgr.setHistoLegendLabelMany({"eff1eta": legend1, "eff2eta": legend2, "eff3eta": legend3})

    name = "TauMET_"+analysis+"_DataVsMC_PFTauEta"

    if createRatio:
        p_eta.createFrame(os.path.join(plotDir, name), createRatio=createRatio, opts=opts, opts2=opts2)
    else:
        p_eta.createFrame(os.path.join(plotDir, name), opts=opts, opts2=opts2)

    moveLegendEta = {"dx": -0.5, "dy": -0.65, "dh": -0.1}
    p_eta.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegendEta))

    p_eta.getFrame().GetYaxis().SetTitle("HLT tau efficiency")
    p_eta.getFrame().GetXaxis().SetTitle("#tau-jet #eta")
    if createRatio:
        p_eta.getFrame2().GetYaxis().SetTitle("Ratio")
        p_eta.getFrame2().GetYaxis().SetTitleOffset(1.6)

    histograms.addText(0.2, 0.46, "LooseIsoPFTau50_Trk30_eta2p1", 17)
    histograms.addText(0.2, 0.38, analysis.split("_")[len(analysis.split("_")) -1], 17)
    histograms.addText(0.2, 0.31, "Runs "+datasets.loadRunRange(), 17)

    p_eta.draw()
    histograms.addStandardTexts(lumi=lumi)

    p_eta.save(formats)

    #########################################################################
    
    eff1phi = getEfficiency(dataset1,"NumeratorPhi","DenominatorPhi")
    eff2phi = getEfficiency(dataset2,"NumeratorPhi","DenominatorPhi")
    if isinstance(datasetsH125,dataset.DatasetManager):
        eff3phi = getEfficiency(datasetsH125.getMCDatasets(),"NumeratorPhi","DenominatorPhi")

    styles.dataStyle.apply(eff1phi)
    styles.mcStyle.apply(eff2phi)
    eff1phi.SetMarkerSize(1)

    if isinstance(datasetsH125,dataset.DatasetManager):
        styles.mcStyle.apply(eff3phi)
        eff3phi.SetMarkerSize(1.5)
        eff3phi.SetMarkerColor(4)
        eff3phi.SetLineColor(4)

    if isinstance(datasetsH125,dataset.DatasetManager):
        p_phi = plots.ComparisonManyPlot(histograms.HistoGraph(eff1phi, "eff1phi", "p", "P"),
                                        [histograms.HistoGraph(eff2phi, "eff2phi", "p", "P"),
                                         histograms.HistoGraph(eff3phi, "eff3phi", "p", "P")])
    elif isinstance(datasetsDY,dataset.DatasetManager):
        p_phi = plots.ComparisonPlot(histograms.HistoGraph(eff1phi, "eff1phi", "p", "P"),
                                     histograms.HistoGraph(eff2phi, "eff2phi", "p", "P"))
    else:
        p_phi = plots.PlotBase([histograms.HistoGraph(eff1phi, "eff1phi", "p", "P")])

    p_phi.histoMgr.setHistoLegendLabelMany({"eff1phi": legend1})
    if isinstance(datasetsDY,dataset.DatasetManager):
        p_phi.histoMgr.setHistoLegendLabelMany({"eff1phi": legend1, "eff2phi": legend2})
    if isinstance(datasetsH125,dataset.DatasetManager):
        p_phi.histoMgr.setHistoLegendLabelMany({"eff1phi": legend1, "eff2phi": legend2, "eff3phi": legend3})

    name = "TauMET_"+analysis+"_DataVsMC_PFTauPhi"

    if createRatio:
        p_phi.createFrame(os.path.join(plotDir, name), createRatio=createRatio, opts=opts, opts2=opts2)
    else:
        p_phi.createFrame(os.path.join(plotDir, name), opts=opts, opts2=opts2)

    moveLegendPhi = {"dx": -0.5, "dy": -0.65, "dh": -0.1}
    p_phi.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegendPhi))

    p_phi.getFrame().GetYaxis().SetTitle("HLT tau efficiency")
    p_phi.getFrame().GetXaxis().SetTitle("#tau-jet #phi")
    if createRatio:
        p_phi.getFrame2().GetYaxis().SetTitle("Ratio")
        p_phi.getFrame2().GetYaxis().SetTitleOffset(1.6)

    histograms.addText(0.2, 0.46, "LooseIsoPFTau50_Trk30_eta2p1", 17)
    histograms.addText(0.2, 0.38, analysis.split("_")[len(analysis.split("_")) -1], 17)
    histograms.addText(0.2, 0.31, "Runs "+datasets.loadRunRange(), 17)

    p_phi.draw()
    histograms.addStandardTexts(lumi=lumi)

    p_phi.save(formats)
    
    ######################################################################### 

    namePU = "TauMET_"+analysis+"_DataVsMC_nVtx"

    eff1PU = getEfficiency(dataset1,"NumeratorPU","DenominatorPU")
    eff2PU = getEfficiency(dataset2,"NumeratorPU","DenominatorPU")

    styles.dataStyle.apply(eff1PU)
    styles.mcStyle.apply(eff2PU)
    eff1PU.SetMarkerSize(1)
    eff2PU.SetMarkerSize(1.5)

    if isinstance(datasetsDY,dataset.DatasetManager):
        pPU = plots.ComparisonManyPlot(histograms.HistoGraph(eff1PU, "eff1", "p", "P"),
                                      [histograms.HistoGraph(eff2PU, "eff2", "p", "P")])
        pPU.histoMgr.setHistoLegendLabelMany({"eff1": legend1, "eff2": legend2})
    else:
        pPU = plots.PlotBase([histograms.HistoGraph(eff1PU, "eff1", "p", "P")])
        pPU.histoMgr.setHistoLegendLabelMany({"eff1": legend1})

    optsPU = {"ymin": 0.01, "ymax": 1.0}
    if createRatio:
        pPU.createFrame(os.path.join(plotDir, namePU), createRatio=True, opts=optsPU, opts2=opts2)
    else:
        pPU.createFrame(os.path.join(plotDir, namePU), opts=optsPU, opts2=opts2)

    moveLegend = {"dx": -0.2, "dy": -0.6, "dh": -0.1}
    pPU.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
#    if createRatio:
#        pPU.getPad1().SetLogy(True)
#    else:
#        pPU.getPad().SetLogy(True)

    pPU.getFrame().GetYaxis().SetTitle("HLT tau efficiency")
    pPU.getFrame().GetXaxis().SetTitle("Number of reco vertices")
    if createRatio:
        pPU.getFrame2().GetYaxis().SetTitle("Ratio")
        pPU.getFrame2().GetYaxis().SetTitleOffset(1.6)

    histograms.addText(0.5, 0.5, "LooseIsoPFTau50_Trk30_eta2p1", 17)
    histograms.addText(0.5, 0.43, analysis.split("_")[len(analysis.split("_")) -1], 17)
    histograms.addText(0.5, 0.36, "Runs "+datasets.loadRunRange(), 17)

    pPU.draw()
    histograms.addStandardTexts(lumi=lumi)

    pPU.save(formats)

    #########################################################################
    """
    hName = "Pull"
#    hName = "Sub"
    namePull = "TauMET_"+analysis+"_DataVsMC_"+hName+"s"

    plots.mergeRenameReorderForDataMC(datasets)
    datasets.merge("MC", ["TT","WJets","DYJetsToLL","SingleTop","QCD"], keepSources=True)

    drh1 = datasets.getDataset("Data").getDatasetRootHisto(hName)
    drh2 = datasets.getDataset("MC").getDatasetRootHisto(hName)
    drh1.normalizeToOne()
    drh2.normalizeToOne()
    pull1 = drh1.getHistogram()
    pull2 = drh2.getHistogram()

    if isinstance(datasetsH125,dataset.DatasetManager):
        plots.mergeRenameReorderForDataMC(datasetsH125)
        drh3 = datasetsH125.getMCDatasets()[0].getDatasetRootHisto(hName)
        drh3.normalizeToOne()
        pull3 = drh3.getHistogram()

    styles.dataStyle.apply(pull1)
    styles.mcStyle.apply(pull2)
    pull1.SetMarkerSize(1)

    if isinstance(datasetsH125,dataset.DatasetManager):
        styles.mcStyle.apply(pull3)
        pull3.SetMarkerSize(1.5)
        pull3.SetMarkerColor(4)
        pull3.SetLineColor(4)

    if isinstance(datasetsH125,dataset.DatasetManager):
        p_pull = plots.ComparisonManyPlot(histograms.Histo(pull1, "pull1", "p", "P"),
                                         [histograms.Histo(pull2, "pull2", "p", "P"),
                                          histograms.Histo(pull3, "pull3", "p", "P")])
    else:
        p_pull = plots.ComparisonPlot(histograms.Histo(pull1, "pull1", "p", "P"),
                                      histograms.Histo(pull2, "pull2", "p", "P"))

    p_pull.histoMgr.setHistoLegendLabelMany({"pull1": legend1, "pull2": legend2})
    if isinstance(datasetsH125,dataset.DatasetManager):
        p_pull.histoMgr.setHistoLegendLabelMany({"pull1": legend1, "pull2": legend2, "pull3": legend3})

    p_pull.createFrame(os.path.join(plotDir, namePull), createRatio=True, opts=opts, opts2=opts2)
    moveLegendPull = {"dx": -0.5, "dy": -0.35, "dh": -0.1}
    p_pull.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegendPull))

    p_pull.getFrame().GetYaxis().SetTitle("Arbitrary units")
#    p_pull.getFrame().GetXaxis().SetTitle("HLT #tau p_{T} - #tau-jet p_{T} (GeV/c)")
    p_pull.getFrame().GetXaxis().SetTitle("HLT #tau p_{T}/ #tau-jet p_{T} - 1")                                                                                                                                     
    p_pull.getFrame2().GetYaxis().SetTitle("Ratio")
    p_pull.getFrame2().GetYaxis().SetTitleOffset(1.6)

    histograms.addText(0.2, 0.75, "LooseIsoPFTau50_Trk30_eta2p1", 17)
    histograms.addText(0.2, 0.68, analysis.split("_")[len(analysis.split("_")) -1], 17)
    histograms.addText(0.2, 0.61, "Runs "+runRange, 17)

    p_pull.draw()

    histograms.addStandardTexts(lumi=lumi)
    p_pull.save(formats)
    """
    #########################################################################                                                                                                                               
    print "Output written in",plotDir


def main():

    if len(sys.argv) < 2:
        usage()

#    analyze("TauLeg_2015C")
#    analyze("TauLeg_2015D")
#    analyze("TauLeg_2015CD")
#    analyze("TauLeg_2016B")
#    analyze("TauLeg_2016C")
#    analyze("TauLeg_2016ICHEP")
    analyze()

if __name__ == "__main__":
    main()
