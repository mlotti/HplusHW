# reading histograms.root produced from tctau.root
# JetMETCorrections/TauJet
# 21.6.2010/S.Lehti

#!/usr/bin/env python
import ROOT
import copy

#from TauAnalysis.TauIdEfficiency.ntauples.TauNtupleManager import TauNtupleManager
#from TauAnalysis.TauIdEfficiency.ntauples.plotting import *
import TauAnalysis.TauIdEfficiency.ntauples.styles as style

from ROOT import *

#from TauAnalysis.TauIdEfficiency.ntauples.plotting import *

if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetOptStat(0)
    canvas_style = copy.deepcopy(style.DEFAULT_STYLE)
    histo_style  = copy.deepcopy(style.QCD_MC_STYLE_HIST)

    fIN = TFile('histograms.root')

    h_TCTau_dEtRatio   = gROOT.FindObject('h_TCTau_dEtRatio')
    h_TCTau_dEtRatio.SetLineColor(1)
    h_TCTau_dEtRatio.SetFillColor(5)

    h_JPTTau_dEtRatio  = gROOT.FindObject('h_JPTTau_dEtRatio')
    h_JPTTau_dEtRatio.SetLineColor(1)
    h_JPTTau_dEtRatio.SetFillColor(5)

    h_CaloTau_dEtRatio = gROOT.FindObject('h_CaloTau_dEtRatio')
    h_CaloTau_dEtRatio.SetLineColor(1)
    h_CaloTau_dEtRatio.SetFillColor(5)

    h_PFTau_dEtRatio   = gROOT.FindObject('h_PFTau_dEtRatio')
    h_PFTau_dEtRatio.SetLineColor(1)
    h_PFTau_dEtRatio.SetFillColor(5)

####
    def plot(histo):

	name = histo.GetName()
        canvas = TCanvas("c_"+name,"",500,500)

	style.update_canvas_style(ROOT.gPad,canvas_style)
        style.LUMI_LABEL_UPPER_LEFT
	style.update_histo_style(histo,histo_style)

        histo.GetYaxis().SetTitle("Arbitrary units")
        histo.GetXaxis().SetTitle("p_{T}(RECO)/p_{T}(MC)")
        histo.Draw()
        histo.Fit("gaus")
        fit = histo.GetFunction("gaus")

        mean  = float(int(100*fit.GetParameter(1)))/100
	width = float(int(100*fit.GetParameter(2)))/100
        textX = 0.65*histo.GetNbinsX()*histo.GetXaxis().GetBinWidth(1)
        textY = 0.9*histo.GetMaximum()
        text1 = TLatex(textX,textY,"CaloTau")
        text1.Draw()

        textY = 0.8*histo.GetMaximum()
        s_mean = "mean = ";
        s_mean+= str(mean)
        text2 = TLatex(textX,textY,s_mean)
        text2.Draw()

        textY = 0.7*histo.GetMaximum()
        s_width = "width = ";
        s_width+= str(width)
        text3 = TLatex(textX,textY,s_width)
        text3.Draw()

	textX = 0.15*histo.GetNbinsX()*histo.GetXaxis().GetBinWidth(1)
        textY = 0.8*histo.GetMaximum()
        text4 = TLatex(textX,textY,"Z#rightarrow#tau#tau")
        text4.Draw()

        canvas.Print("dpt_"+name+".C")

    plot(h_CaloTau_dEtRatio)
    plot(h_JPTTau_dEtRatio)
    plot(h_TCTau_dEtRatio)

####

    c_CaloTaus = TCanvas("c_CaloTaus","",500,500)

    h_TCTau_dEtRatio.Draw()
    h_JPTTau_dEtRatio.Draw("same")
    h_CaloTau_dEtRatio.Draw("same")

    c_CaloTaus.Print("dpt_taus.C")
