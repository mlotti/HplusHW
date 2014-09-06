#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.cutstring import * # And, Not, Or
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect


def main():
    style = tdrstyle.TDRStyle()
    

    # hand-picked values from an output from Lauri
    th1 = ROOT.TH1F("factors", "factors", 7, 0, 7)
    th1.SetBinContent(1, 0.0614187118715)
    th1.SetBinContent(2, 0.0579929858899)
    th1.SetBinContent(3, 0.0502462685164)
    th1.SetBinContent(4, 0.0524329776127)
    th1.SetBinContent(5, 0.0519288842156)
    th1.SetBinContent(6, 0.0499747490482)
    th1.SetBinContent(7, 0.0503459705535)

    for i in xrange(1, 8):
        th1.SetBinError(i, th1.GetBinContent(i)*0.03)

    th1.SetMarkerSize(1.5)
    th1.SetLineWidth(2)

    xaxis = th1.GetXaxis()
    xaxis.SetBinLabel(1, "41-50")
    xaxis.SetBinLabel(2, "50-60")
    xaxis.SetBinLabel(3, "60-70")
    xaxis.SetBinLabel(4, "70-80")
    xaxis.SetBinLabel(5, "80-100")
    xaxis.SetBinLabel(6, "100-120")
    xaxis.SetBinLabel(7, "> 120")

    def foo(p):
        xaxis = p.getFrame().GetXaxis()
        xaxis.LabelsOption("u")
        xaxis.SetTitleOffset(xaxis.GetTitleOffset()*1.4)
        p.getPad().SetBottomMargin(0.16)


    p = plots.PlotBase([th1])
    p.setLuminosity("19.7")
    h = p.histoMgr.getHisto("factors")
    h.setDrawStyle("PE")
    plots.drawPlot(p, "qcd_normalization",
#                   ylabel="Normalization coefficient ^{}w_{j}",
#                   ylabel="Fake rate probability ^{}w_{j}",
                   ylabel="Fake rate probability",
                   xlabel="p_{T}^{#tau_{h}} bin (GeV)",
                   cmsTextPosition="right", createLegend=None,
                   customizeBeforeDraw=foo
    )

if __name__ == "__main__":
    main()
