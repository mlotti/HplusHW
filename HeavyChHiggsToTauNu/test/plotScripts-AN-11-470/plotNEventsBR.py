#!/usr/bin/env python

######################################################################
#
# Plot the number of ttbar events as a function of the BR
#
######################################################################

import array

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle

lumi = 2.3

x1 = 0.21
def main():
    style = tdrstyle.TDRStyle()
    histograms.createLegend.setDefaults(x1=x1, y1=0.72, x2=0.51, y2=0.92)
    histograms.cmsTextMode = histograms.CMSMode.SIMULATION

    br = map(lambda n: n*0.01, xrange(100))

    massPoint(br, 80,  n_hh=733.758, n_hw=324.653, n_ww=2.109)
    massPoint(br, 120, n_hh=882.446, n_hw=513.739, n_ww=2.109)
    massPoint(br, 140, n_hh=745.910, n_hw=593.838, n_ww=2.109)
    massPoint(br, 150, n_hh=510.609, n_hw=675.326, n_ww=2.109)
    massPoint(br, 160, n_hh=310.913, n_hw=708.799, n_ww=2.109)

def massPoint(br, mass, n_hh, n_hw, n_ww):
    gr_hh = createGraph("HH", br, lambda b: b*b*n_hh)
    gr_hw = createGraph("HW", br, lambda b: 2*b*(1-b)*n_hw)
    gr_ww = createGraph("WW", br, lambda b: (1-b)*(1-b)*n_ww)
    gr_sum = ROOT.TGraph(len(br))
    for i in xrange(len(br)):
        gr_sum.SetPoint(i, br[i], sum([gr_hh.GetY()[i],
                                       gr_hw.GetY()[i],
                                       gr_ww.GetY()[i]]))
    gr_sum.SetName("Sum")

    gr_hh.SetLineColor(3)
    gr_hh.SetLineStyle(7)
    gr_hh.SetLineWidth(3)
    
    gr_hw.SetLineColor(2)
    gr_hw.SetLineStyle(2)
    gr_hw.SetLineWidth(3)

    gr_ww.SetLineColor(4)
    gr_ww.SetLineStyle(3)
    gr_ww.SetLineWidth(3)

    gr_sum.SetLineColor(6)
    gr_sum.SetLineStyle(1)
    gr_sum.SetLineWidth(4)

    p = plots.PlotBase([
            gr_sum,
            gr_ww,
            gr_hw,
            gr_hh,
            ])
    p.histoMgr.setHistoLegendLabelMany({
            "Sum": "t#bar{t} (WW + WH^{#pm} + H^{+}H^{-})",
            "WW": "WW (t#bar{t} #rightarrow W^{+}bW^{-}#bar{b})",
            "HW": "WH^{#pm} (t#bar{t} #rightarrow W^{+}bH^{-}#bar{b})",
            "HH": "H^{+}H^{-} (t#bar{t} #rightarrow H^{+}bH^{-}#bar{b})"})
    p.appendPlotObject(histograms.PlotText(x1, 0.68, "m_{H^{#pm}} = %d GeV/c^{2}"%mass, size=17))
    p.appendPlotObject(histograms.PlotText(x1, 0.64, "#tau_{h}+jets final state", size=17))

    opts = {}
    if mass == 150:
        opts["ymaxfactor"] = 1.2
    elif mass == 160:
        opts["ymaxfactor"] = 1.4

    p.histoMgr.luminosity = 2300 # ugly hack, only for display
    plots.drawPlot(p, "nevents_ttbar_br_mass%d"%mass, "BR(t#rightarrowH^{+}b)", ylabel="Events", opts=opts, addLuminosityText=True)

def createGraph(name, br, func):
    gr = ROOT.TGraph(len(br), array.array("d", br), array.array("d", map(func, br)))
    gr.SetName(name)
    return gr


if __name__ == "__main__":
    main()
