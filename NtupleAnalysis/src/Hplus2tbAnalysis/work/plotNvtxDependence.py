#!/usr/bin/env python

######################################################################
#
# This plot script is for analyzing the selection step efficiency
# dependence on the number of vertices in the event. Ideally,
# a flat curve would be obtained for each item. If not, then
# one risks biasing the measurement unless the analysis is done in
# bins of number of vertices.
#
# Authors: Lauri Wendland
#
######################################################################
import ROOT
import sys,os,math
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetPalette(1)
import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
from HiggsAnalysis.NtupleAnalysis.tools.OrderedDict import OrderedDict

# Configuration
#_analysis = "SignalAnalysis"
_analysis = "Hplus2tbAnalysis"
searchMode = "80to1000"
dataEra = "Run2015"
optMode = ""

def usage():
    print "\n"
    print "### Usage:   plotNvtxDependence.py <multicrab dir>\n"
    print "\n"
    sys.exit()

# main function
def main():
    if len(sys.argv) < 2:
        usage()
    analysis = _analysis
    if "--QCD" in sys.argv:
        analysis = "QCDMeasurement"

    dirs = []
    dirs.append(sys.argv[1])
    dsetMgr = dataset.getDatasetsFromMulticrabDirs(dirs,dataEra=dataEra, searchMode=searchMode, analysisName=analysis, optimizationMode=optMode) 
    dsetMgr.loadLuminosities()
    dsetMgr.updateNAllEventsToPUWeighted()
    plots.mergeRenameReorderForDataMC(dsetMgr)
    #dsetMgr.normalizeToLuminosity()
    lumi = dsetMgr.getDataset("Data").getLuminosity()

    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Format: list of [denominator, numerator] pairs
    plotSources = OrderedDict()
    plotSources["trg_vs_vtx"] = ["PUDependency/NvtxTrg","PUDependency/NvtxVtx"]
    plotSources["vtx_vs_antiIsolTau"] = ["PUDependency/NvtxVtx","PUDependency/NvtxAntiIsolatedTau"]
    plotSources["vtx_vs_tau"] = ["PUDependency/NvtxVtx","PUDependency/NvtxTau"]
    if not "--QCD" in sys.argv:
        plotSources["tau_vs_eveto"] = ["PUDependency/NvtxTau","PUDependency/NvtxElectronVeto"]
    else:
        plotSources["tau_vs_eveto"] = ["PUDependency/NvtxAntiIsolatedTau","PUDependency/NvtxElectronVeto"]
    plotSources["eveto_vs_muveto"] = ["PUDependency/NvtxElectronVeto","PUDependency/NvtxMuonVeto"]
    plotSources["jet_vs_muveto"] = ["PUDependency/NvtxMuonVeto","PUDependency/NvtxJetSelection"]
    plotSources["rcoll_vs_jet"] = ["PUDependency/NvtxJetSelection","PUDependency/NvtxAngularCutsCollinear"]
    plotSources["btag_vs_rcoll"] = ["PUDependency/NvtxAngularCutsCollinear","PUDependency/NvtxBtagging"]
    plotSources["met_vs_btag"] = ["PUDependency/NvtxBtagging","PUDependency/NvtxMETSelection"]
    plotSources["rbb_vs_met"] = ["PUDependency/NvtxMETSelection","PUDependency/NvtxAngularCutsBackToBack"]
    plotSources["allsel_vs_rbb"] = ["PUDependency/NvtxAngularCutsBackToBack","PUDependency/NvtxAllSelections"]
    if not "--QCD" in sys.argv:
        plotSources["propbtag_vs_btag"] = ["PUDependency/NvtxBtagging","PUDependency/NvtxAllSelectionsWithProbabilisticBtag"]
    plotSources["allsel_vs_trg"] = ["PUDependency/NvtxTrg","PUDependency/NvtxAllSelections"]
    #plotSources["tau_isol_pt"] = ["tauSelection_/IsolPtBefore","tauSelection_/IsolPtAfter"]
    #plotSources["tau_isol_eta"] = ["tauSelection_/IsolEtaBefore","tauSelection_/IsolEtaAfter"]
    #plotSources["tau_isol_vtx"] = ["tauSelection_/IsolVtxBefore","tauSelection_/IsolVtxAfter"]
    #plotSources["e_isol_pt"] = ["eSelection_Veto/IsolPtBefore","eSelection_Veto/IsolPtAfter"]
    #plotSources["e_isol_eta"] = ["eSelection_Veto/IsolEtaBefore","eSelection_Veto/IsolEtaAfter"]
    #plotSources["e_isol_vtx"] = ["eSelection_Veto/IsolVtxBefore","eSelection_Veto/IsolVtxAfter"]
    #plotSources["mu_isol_pt"] = ["muSelection_Veto/IsolPtBefore","muSelection_Veto/IsolPtAfter"]
    #plotSources["mu_isol_eta"] = ["muSelection_Veto/IsolEtaBefore","muSelection_Veto/IsolEtaAfter"]
    #plotSources["mu_isol_vtx"] = ["muSelection_Veto/IsolVtxBefore","muSelection_Veto/IsolVtxAfter"]
    dsetInputs = {
        #"TTJets": ["TTJets"], # Madgraph with negative weights
        "TT": ["TT"], # Powheg, no neg. weights -> large stats.
        "TTJets": ["TTJets"],
        "WJets": ["WJetsHT"],
        "EWK": ["TTJets", "WJetsHT", "DYJetsToLL", "SingleTop"],
        "QCD": ["QCD"],
        "Data": ["Data"],
    }
    summarySources = ["vtx_vs_antiIsolTau",
                      "vtx_vs_tau",
                      "tau_vs_eveto",
                      "eveto_vs_muveto",
                      "jet_vs_muveto",
                      "btag_vs_rcoll",
                      "met_vs_btag",
                      "allsel_vs_trg"]

    # Create plots (MC vs. MC)
    doPlots(dsetMgr, lumi, plotSources, dsetInputs, summarySources)
    # Create plots (data vs. MC)
    doPlots(dsetMgr, lumi, plotSources, dsetInputs, summarySources, "Data")

def getPlot(dsetMgr, dsetItems, plotname, lumi, rebinFactor):
    h = None
    for dsetItem in dsetItems:
        if dsetMgr.hasDataset(dsetItem):
            hTmp = None
            hTmp = dsetMgr.getDataset(dsetItem).getDatasetRootHisto(plotname)
            if dsetItem != "Data":
                hTmp.normalizeToLuminosity(lumi)
            if h == None:
                h = hTmp.getHistogram().Clone()
            else:
                h.Add(hTmp.getHistogram())
        else:
            raise Exception("Cannot find key '%s' in dsetMgr! Options: %s"%(dsetItem, ", ".join(map(str, dsetMgr.getAllDatasetNames()))))
        for k in range(1, h.GetNbinsX()+1):
            if h.GetBinContent(k) < 0: 
                h.SetBinContent(k, 0.0)
    h.Rebin(rebinFactor)
    return h

def obtainRatioPlot(hNum, hDenom, numName, denomName):
    if hDenom.GetNbinsX() != hNum.GetNbinsX() or hDenom.GetXaxis().GetXmin() != hNum.GetXaxis().GetXmin() or hDenom.GetXaxis().GetXmax() != hNum.GetXaxis().GetXmax():
        raise Exception("Binning different in histograms '%s' and '%s'!"%(numName, denomName))
    if hNum.Integral() > hDenom.Integral():
        raise Exception("Histogram '%s' has more events than '%s'!"%(numName, denomName))
    # Solve ambiguous bins
    for k in range(1, hDenom.GetNbinsX()+1):
        if hNum.GetBinContent(k) > hDenom.GetBinContent(k):
            hNum.SetBinContent(k, 0.0)
    myFactor = hNum.Integral()/hDenom.Integral()
    g = ROOT.TGraphAsymmErrors()
    g.BayesDivide(hNum, hDenom)
    for k in range(g.GetN()):
        g.SetPoint(k, g.GetX()[k], g.GetY()[k]/myFactor)
        g.SetPointEYhigh(k, g.GetErrorYhigh(k)/myFactor)
        g.SetPointEYlow(k, g.GetErrorYlow(k)/myFactor)
    return g

def obtainRatioOfGraphs(gNom, gRef):
    g = ROOT.TGraphAsymmErrors()
    for k in range(gNom.GetN()):
        yvalue = -1
        ymerror = 0
        yperror = 0
        if gRef.GetY()[k] > 1e-12:
            yvalue = gNom.GetY()[k] / gRef.GetY()[k]
            ap = 0
            am = 0
            if gNom.GetY()[k] > 1e-12:
                ap = gNom.GetErrorYhigh(k) / gNom.GetY()[k]
                am = gNom.GetErrorYlow(k) / gNom.GetY()[k]
            bp = 0
            bm = 0
            if gRef.GetY()[k] > 1e-12:
                bp = gRef.GetErrorYhigh(k) / gRef.GetY()[k]
                bm = gRef.GetErrorYlow(k) / gRef.GetY()[k]
            yperror = yvalue*math.sqrt(ap*ap+bp*bp+1e-12)
            ymerror = yvalue*math.sqrt(am*am+bm*bm+1e-12)
        g.SetPoint(k, gNom.GetX()[k], yvalue)
        g.SetPointEXlow(k, gNom.GetErrorXlow(k))
        g.SetPointEXhigh(k, gNom.GetErrorXhigh(k))
        g.SetPointEYlow(k, ymerror)
        g.SetPointEYhigh(k, yperror)
    return g

def drawDecorations(label, xmin, xmax, cache=None):
    l = ROOT.TLatex(0.15, 0.955, label)
    l.SetNDC()
    l.Draw()
    line = ROOT.TLine(xmin, 1, xmax, 1)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kGray+1)
    line.SetLineWidth(2)
    line.Draw()
    if cache != None:
        cache.append(l)
        cache.append(line)

def doPlots(dsetMgr, lumi, plotSources, dsetInputs, summarySources, dataref=None):
    _tolerance = 0.7
    _rebinFactor = 4
    ylabel = "Ratio"
    if dataref != None:
        ylabel = "Data / simulation"
    summaryLabels = []
    # Loop over dsetMgr
    for dsetkey in dsetInputs.keys():
        if dsetkey == dataref:
            continue
        print "***", dsetkey
        summaryGraphs = []
        # Loop over plot sources
        plotCounter = 1
        xmin = None
        xmax = None
        for plotItemKey in plotSources.keys():
            # Obtain source histograms and ratio
            hDenom = getPlot(dsetMgr, dsetInputs[dsetkey], plotSources[plotItemKey][0], lumi, _rebinFactor)
            hNum = getPlot(dsetMgr, dsetInputs[dsetkey], plotSources[plotItemKey][1], lumi, _rebinFactor)
            g = obtainRatioPlot(hNum, hDenom, plotSources[plotItemKey][1], plotSources[plotItemKey][0])
            xmin = hDenom.GetXaxis().GetXmin()
            xmax = hDenom.GetXaxis().GetXmax()
            # Obtain source histograms and ratio for data
            if dataref != None:
                hDenomRef = getPlot(dsetMgr, [dataref], plotSources[plotItemKey][0], lumi, _rebinFactor)
                hNumRef = getPlot(dsetMgr, [dataref], plotSources[plotItemKey][1], lumi, _rebinFactor)
                gRef = obtainRatioPlot(hNumRef, hDenomRef, plotSources[plotItemKey][1], plotSources[plotItemKey][0])
                # Calculate ratio of ratios
                g = obtainRatioOfGraphs(gRef, g)
            # Store for summary
            if plotItemKey in summarySources:
                summaryGraphs.append(g)#.Clone())
                summaryLabels.append(plotItemKey)
            # Create frame
            frameTitle = "frame%d_%s"%(plotCounter, dsetkey)
            h = ROOT.TH2F(frameTitle, frameTitle, 2, hDenom.GetXaxis().GetXmin(), hDenom.GetXaxis().GetXmax(),2,1-_tolerance,1+_tolerance)
            h.GetXaxis().SetTitle(hDenom.GetXaxis().GetTitle())
            h.GetYaxis().SetTitle(ylabel)
            # Create plot
            c = ROOT.TCanvas()
            c.cd()
            h.Draw()
            drawDecorations(plotItemKey, xmin, xmax)
            g.Draw("P same")
            for suffix in ["png"]:
                name = "nvtxDependence_%s"%dsetkey
                if dataref != None:
                    name += "VsData"
                name += "_%02d_%s.%s"%(plotCounter, plotItemKey, suffix)
                c.Print(name)
            plotCounter += 1
        # Make summary graph
        cc = ROOT.TCanvas("summary_%s"%dsetkey, "summary_%s"%dsetkey, 2400, 1200)
        cc.Divide(4,2)
        cache = [] # Needed to make objects persistent
        for i in range(len(summaryGraphs)):
            frameTitle = "summary_%s_%d"%(dsetkey, i)
            hh = ROOT.TH2F(frameTitle, frameTitle, 2, 0, 60, 2, 1-_tolerance, 1+_tolerance)
            hh.GetXaxis().SetTitle("N_{vtx}")
            hh.GetYaxis().SetTitle(ylabel)
            hh.GetXaxis().SetTitleOffset(2.0)
            hh.GetYaxis().SetTitleOffset(3.5)
            cache.append(hh)
            cc.cd(i+1)
            hh.Draw()
            drawDecorations(summaryLabels[i], xmin, xmax, cache)
            summaryGraphs[i].Draw("p same")
            cc.Draw()
        for suffix in ["png", "C"]:
            name = "nvtxDependence_%s"%dsetkey
            if dataref != None:
                name += "VsData"
            name += "_summary.%s"%(suffix)
            cc.Print(name)
        
      
# Call the main function if the script is executed (i.e. not imported)
if __name__ == "__main__":
    main()
