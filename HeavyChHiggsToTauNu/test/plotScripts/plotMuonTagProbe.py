#!/usr/bin/env python

import math

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset

def main():
    style = tdrstyle.TDRStyle()
    style.setPalettePretty()

    datasets = dataset.getDatasetsFromMulticrabCfg(counters="tnpCounters")
    datasets.loadLuminosities()
    def getLumi(names):
        return sum([datasets.getDataset(name).getLuminosity() for name in names])

    data = [
#        ("Run2011A_Mu20", 5.0644747570000002+26.123554120999998),
#        ("Run2011A_Mu24", 157.79184244000001),
        #("Run2011A_Mu20", 20.300513+0.490643, 43.850900027000002+0.490643414),
        #("Run2011A_Mu24", 77.851037, 145.599256231),
        #("Run2011A_Mu30", 53.748971+0.000176, 172.02642060600002),
        #("Run2011A_Mu40", 3.381858+4.153168+424.330775+109.639076+105.026041, 3.3818575699999998+4.153168108+424.33077485900003+83.549892354000008+95.750128408000009),
        ("Run2011A_Mu20", getLumi(["SingleMu_160431-163261_May10"]), 20),
#        ("Run2011A_Mu24", getLumi(["SingleMu_163270-163869_May10"]), 20),
#        ("Run2011A_Mu30", getLumi(["SingleMu_165088-165633_Prompt", "SingleMu_165970-166150_Prompt"]), 20),
#        ("Run2011A_Mu40", getLumi(["SingleMu_166161-166164_Prompt", "SingleMu_166346-166346_Prompt", "SingleMu_166374-166967_Prompt", "SingleMu_167039-167043_Prompt", "SingleMu_167078-167913_Prompt", "SingleMu_172620-173198_Prompt"]), 20),
#        ("Run2011A_Mu40eta2p1", getLumi(["SingleMu_173236-173692_Prompt"]), 20),
        ]
    mc = "DY_Mu20"
    doMC = False

    totalLumi = 0
    totalEff = 0
    totalErr = 0
    for d, ownLumi, targetLumi in data:
        (eff_value, eff_plus, eff_minus) = getEfficiency(d, style, ownLumi)
        print " lumi: %f %f" % (ownLumi, targetLumi)
        err = max(eff_plus, eff_minus)

        totalLumi += targetLumi
        totalEff += targetLumi * eff_value
        totalErr += targetLumi * err*err

    totalEff = totalEff/totalLumi
    totalErr = math.sqrt(totalErr/totalLumi)
    print "Data overall efficiency %f \\pm %f" % (totalEff, totalErr)

    if not doMC:
        return
    (mc_value, mc_plus, mc_minus) = getEfficiency(mc, style)
    mc_err = max(mc_plus, mc_minus)

    rho = totalEff/mc_value
    rho_err = math.sqrt( (totalErr/mc_value)**2 + (totalErr*mc_err/(mc_value**2))**2)

    syst = abs(totalEff-mc_value)/totalEff
    
    print "Data/MC rho %f \\pm %f" % (rho, rho_err)
    print "Systematic uncertainty %f, relative %f" % (syst, syst/totalEff)

def getEfficiency(postfix, style, lumi=None):
    f = ROOT.TFile.Open("tagprobe_output_%s.root" % postfix)

    (trig, runs) = {
        "Run2011A_Mu20": ("HLT_Mu20", "160431-163261"),
        "Run2011A_Mu24": ("HLT_Mu24", "163270-163869"),
        "Run2011A_Mu30": ("HLT_Mu30", "165088-166150"),
        "Run2011A_Mu40": ("HLT_Mu40", "166161-167913, 172620-173198"),
        "Run2011A_Mu40eta2p1": ("HLT_Mu40eta2p1", "173236-173692"),
        "DY_Mu20": ("HLT_Mu20", "DY+jets MC"),
        }[postfix]

    l = ROOT.TLatex()
    l.SetNDC()
    l.SetTextFont(l.GetTextFont()-20) # bold -> normal

    cntfit = "cnt"
#    cntfit = "fit"

    plotPostfix = "_tauTightIc04Iso_bin0"

    path = "tnpTree/All/%s_eff_plots" % cntfit
    plot = "pt_PLOT_abseta_bin0_&"+plotPostfix
    graph = "hxy_%s_eff" % cntfit

    pathPt = "tnpTree/All_pt/%s_eff_plots" % cntfit
    plotPt = "pt_PLOT_abseta_bin0_&"+plotPostfix

    pathEta = "tnpTree/All_abseta/%s_eff_plots" % cntfit
    #plotEta = "abseta_PLOT_pt_bin0"
    plotEta = "abseta_PLOT_pt_bin0_&"+plotPostfix
    pathTriggerEta = "tnpTree/Trigger_abseta/%s_eff_plots" % cntfit
    plotTriggerEta = "abseta_PLOT_pt_bin0_&_tauTightIc04Iso_bin0_&_dB_pass_&_hitQuality_pass_&_isGlobalMuon_pass_&_isTrackerMuon_pass"
    pathIdEta = "tnpTree/Id_abseta/%s_eff_plots" % cntfit
    plotIdEta = "abseta_PLOT_pt_bin0_&_tauTightIc04Iso_bin0_&_isHLT%s_pass" % trig.replace("HLT_", "")

    pathPtEta = "tnpTree/All_pt_abseta/%s_eff_plots" % cntfit
    plotPtEta = "abseta_pt_PLOT"+plotPostfix
    graphPtEta = plotPtEta

    ## Overall value
    canv = f.Get(path+"/"+plot)
    gr = canv.FindObject(graph)
    eff_value = gr.GetY()[0]
    eff_plus = gr.GetErrorYhigh(0)
    eff_minus = gr.GetErrorYlow(0)

    opts = {"xmin": 0, "ymin": 0, "ymax": 1.1}
    name = "TagProbe_%s_All_%s_%s" % (postfix, plot, graph)
    def createPlot(graph_, **kwargs):
        if isinstance(graph_, ROOT.TH1):
            defaults = {"legendStyle": "l"}
            defaults.update(kwargs)
            graph_.GetZaxis().SetTitle("")
            return plots.PlotBase([histograms.HistoBase(graph_, "efficiency", **defaults)])
        else:
            defaults = {"drawStyle": "EP"}
            defaults.update(kwargs)
            return plots.PlotBase([histograms.HistoGraph(graph_, "efficiency", **defaults)])
    def drawPlot(plot, xlabel, ylabel="Trigger and ID efficiency", cutLine=None, updatePaletteStyle=False, addText=True):
        if cutLine != None:
            lst = cutLine
            if not isinstance(lst, list):
                lst = [lst]

            for line in lst:
                p.addCutBoxAndLine(line, box=False, line=True)

        plot.frame.GetXaxis().SetTitle(xlabel)
        plot.frame.GetYaxis().SetTitle(ylabel)
        plot.draw()
        if updatePaletteStyle:
            histograms.updatePaletteStyle(p.histoMgr.getHistos()[0].getRootHisto())
        histograms.addCmsPreliminaryText()
        histograms.addEnergyText()
        if lumi != None:
            histograms.addLuminosityText(None, None, lumi)
        if addText:
            l.DrawLatex(0.2, 0.4, trig)
            l.DrawLatex(0.2, 0.35, runs)
        plot.save()

    p = createPlot(gr)
    p.createFrame(name, xmax=200, **opts)
    drawPlot(p, "Probe muon p_{T} (GeV/c)")

    #print eff

    ## As a function of pT
    canv = f.Get(pathPt+"/"+plotPt)
    gr = canv.FindObject(graph).Clone()
    name = "TagProbe_%s_All_%s_%s" % (postfix, plotPt, graph)

    # 0-100
    p = createPlot(gr)
    p.createFrame(name+"_Pt100", xmax=100, **opts)
    drawPlot(p, "Probe muon p_{T} (GeV/c)", cutLine=40)

    p = createPlot(gr)
    p.createFrame(name+"_Pt400", xmax=400, **opts)
    drawPlot(p, "Probe muon p_{T} (GeV/c)", cutLine=40)

    ## As a function of eta
    canv = f.Get(pathEta+"/"+plotEta)
    gr = canv.FindObject(graph).Clone()
    name = "TagProbe_%s_All_%s_%s" % (postfix, plotEta, graph)
    p = createPlot(gr)
    p.createFrame(name+"_Eta", xmax=2.2, **opts)
    drawPlot(p, "Probe muon |#eta|", cutLine=2.1)

    ## As a function of pt and eta
    plotOpts = {"xlabel": "Probe muon |#eta|", "ylabel": "Probe muon p_{T} (GeV/c)", "addText": False, "updatePaletteStyle": True}
    opts2 = {"xmin": 0, "xmax": 2.2, "ymin": 30, "ymax": 100}
    canv = f.Get(pathPtEta+"/"+plotPtEta)
    h = canv.FindObject(graphPtEta).Clone()
    name = "TagProbe_%s_All_%s_%s" % (postfix, plotPtEta, graphPtEta)
    style.setWide(True)
    p = createPlot(h, drawStyle="COLZ")
    p.createFrame(name+"_EtaPt100", **opts2)
    drawPlot(p, **plotOpts)
    p = createPlot(createUncertainty(h), drawStyle="COLZ")
    p.createFrame(name+"_EtaPt100_Uncertainty", **opts2)
    drawPlot(p, **plotOpts)

    style.setWide(False)


    ### Trigger as a function of eta
    canv = f.Get(pathTriggerEta+"/"+plotTriggerEta)
    gr = canv.FindObject(graph).Clone()
    name = "TagProbe_%s_Trigger_%s_%s" % (postfix, plotTriggerEta, graph)
    p = createPlot(gr)
    p.createFrame(name+"_Eta", xmax=2.2, **opts)
    drawPlot(p, "Probe muon |#eta|", cutLine=2.1)
    

    ### ID as a function of eta
    canv = f.Get(pathIdEta+"/"+plotIdEta)
    gr = canv.FindObject(graph).Clone()
    name = "TagProbe_%s_Id_%s_%s" % (postfix, plotIdEta, graph)
    p = createPlot(gr)
    p.createFrame(name+"_Eta", xmax=2.2, **opts)
    drawPlot(p, "Probe muon |#eta|", cutLine=2.1)

    print "%s overall efficiency %f + %f - %f" % (postfix, eff_value, eff_plus, eff_minus)
    return (eff_value, eff_plus, eff_minus)


def createUncertainty(th2, relative=True):
    result = th2.Clone(th2.GetName()+"_uncertainty")

    for xbin in xrange(1, result.GetNbinsX()+1):
        for ybin in xrange(1, result.GetNbinsY()+1):
            unc = result.GetBinError(xbin, ybin)
            if relative:
                val = result.GetBinContent(xbin, ybin)
                if val != 0:
                    unc = unc/val
            result.SetBinContent(xbin, ybin, unc)
            result.SetBinError(xbin, ybin, 0)
    return result

if __name__ == "__main__":
    main()
