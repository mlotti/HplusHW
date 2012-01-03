#!/usr/bin/env python

import math

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms

def getEfficiency(postfix, lumi):
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

    path = "tnpTree/All/%s_eff_plots" % cntfit
    plot = "pt_PLOT_abseta_bin0"
    graph = "hxy_%s_eff" % cntfit

    pathPt = "tnpTree/All_pt/%s_eff_plots" % cntfit
    plotPt = "pt_PLOT_abseta_bin0"

    pathEta = "tnpTree/All_abseta/%s_eff_plots" % cntfit
    plotEta = "abseta_PLOT_pt_bin0"

    ## Overall value
    canv = f.Get(path+"/"+plot)
    canv.SetName("TagProbe_%s_%s_%s" % (postfix, plot, graph))
#    canv.SaveAs(".eps")
    canv.SaveAs(".png")

    eff = canv.FindObject(graph)
    #print eff
    eff_value = eff.GetY()[0]
    eff_plus = eff.GetErrorYhigh(0)
    eff_minus = eff.GetErrorYlow(0)

    ## As a function of pT
    canv = f.Get(pathPt+"/"+plotPt)
    gr = canv.FindObject(graph).Clone()

    # 0-100
    name = "TagProbe_%s_%s_%s_Pt100" % (postfix, plot, graph)
    c = ROOT.TCanvas(name, name)
    frame = c.DrawFrame(0, 0, 100, 1.1)
    gr.Draw("EP")
    frame.GetXaxis().SetTitle("Probe muon p_{T} (GeV/c)")
    frame.GetYaxis().SetTitle("Trigger and ID efficiency")
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(None, None, lumi)
    l.DrawLatex(0.2, 0.4, trig)
    l.DrawLatex(0.2, 0.35, runs)
    c.SaveAs(".png")

    # 0-400
    gr = canv.FindObject(graph).Clone()
    name = "TagProbe_%s_%s_%s_Pt400" % (postfix, plot, graph)
    c = ROOT.TCanvas(name, name)
    frame = c.DrawFrame(0, 0, 400, 1.1)
    gr.Draw("EP")
    frame.GetXaxis().SetTitle("Probe muon p_{T} (GeV/c)")
    frame.GetYaxis().SetTitle("Trigger and ID efficiency")
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(None, None, lumi)
    l.DrawLatex(0.2, 0.4, trig)
    l.DrawLatex(0.2, 0.35, runs)
    c.SaveAs(".png")

    ## As a function of eta
    canv = f.Get(pathEta+"/"+plotEta)
    gr = canv.FindObject(graph).Clone()
    name = "TagProbe_%s_%s_%s_Eta" % (postfix, plot, graph)
    c = ROOT.TCanvas(name, name)
    frame = c.DrawFrame(0, 0, 2.2, 1.1)
    gr.Draw("EP")
    frame.GetXaxis().SetTitle("Probe muon |#eta|")
    frame.GetYaxis().SetTitle("Trigger and ID efficiency")
    histograms.addCmsPreliminaryText()
    histograms.addEnergyText()
    histograms.addLuminosityText(None, None, lumi)
    l.DrawLatex(0.2, 0.4, trig)
    l.DrawLatex(0.2, 0.35, runs)
    c.SaveAs(".png")
    

    print "%s overall efficiency %f + %f - %f" % (postfix, eff_value, eff_plus, eff_minus)
    return (eff_value, eff_plus, eff_minus)

def main():
    style = tdrstyle.TDRStyle()

    data = [
#        "Run2010A_Mu9",
#        "Run2010B_Mu9",
#        "Run2010B_Mu15",
#        ("Run2011A_Mu20", 5.0644747570000002+26.123554120999998),
#        ("Run2011A_Mu24", 157.79184244000001),
        #("Run2011A_Mu20", 20.300513+0.490643, 43.850900027000002+0.490643414),
        #("Run2011A_Mu24", 77.851037, 145.599256231),
        #("Run2011A_Mu30", 53.748971+0.000176, 172.02642060600002),
        #("Run2011A_Mu40", 3.381858+4.153168+424.330775+109.639076+105.026041, 3.3818575699999998+4.153168108+424.33077485900003+83.549892354000008+95.750128408000009),
        # after lumi DB update
        ("Run2011A_Mu20", 20.300513+0.490643, 47.008000000000003),
#        ("Run2011A_Mu24", 77.851037, 164.5),
#        ("Run2011A_Mu30", 53.748971+0.000176, 233.78800000000001),
#        ("Run2011A_Mu40", 3.381858+4.153168+424.330775+109.639076+105.026041, 3.4630000000000001+4.2910000000000004+445.12599999999998+243.08099999999999+373.21600000000001+412.35899999999998+246.52699999999999),
        ]
    mc = "DY_Mu20"
    doMC = False

    totalLumi = 0
    totalEff = 0
    totalErr = 0
    for d, ownLumi, targetLumi in data:
        (eff_value, eff_plus, eff_minus) = getEfficiency(d, ownLumi)
        print " lumi: %f" % targetLumi
        err = max(eff_plus, eff_minus)

        totalLumi += targetLumi
        totalEff += targetLumi * eff_value
        totalErr += targetLumi * err*err

    totalEff = totalEff/totalLumi
    totalErr = math.sqrt(totalErr/totalLumi)
    print "Data overall efficiency %f \\pm %f" % (totalEff, totalErr)

    if not doMC:
        return
    (mc_value, mc_plus, mc_minus) = getEfficiency(mc)
    mc_err = max(mc_plus, mc_minus)

    rho = totalEff/mc_value
    rho_err = math.sqrt( (totalErr/mc_value)**2 + (totalErr*mc_err/(mc_value**2))**2)

    syst = abs(totalEff-mc_value)/totalEff
    
    print "Data/MC rho %f \\pm %f" % (rho, rho_err)
    print "Systematic uncertainty %f, relative %f" % (syst, syst/totalEff)

if __name__ == "__main__":
    main()
