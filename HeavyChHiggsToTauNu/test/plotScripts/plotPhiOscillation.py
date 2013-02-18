#! /usr/bin/env python

# -----------------------------------------------------------------------------------
# What this script does:
#   Produce tau fake rate curves as function of fake tau pT for selected datasets
# -----------------------------------------------------------------------------------

import sys
import ROOT
ROOT.gROOT.SetBatch(True)

import os
from optparse import OptionParser

#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle

def myfitfunc(x, par):
    return par[0]*x[0]+par[1]

def getHistogram(rootfile,histoname):
    h = rootfile.Get(histoname)
    if h == None:
        raise Exception ("Error: histogram '%s' not found!"%histoname)
    return h;

def produceCurve(rootfile, histoPath, histoNamePrefix):
    h = getHistogram(rootfile, "%s/%s"%(histoPath, histoNamePrefix))
    hOut = ROOT.TH1F("hout%s"%histoNamePrefix,"hout%s"%histoNamePrefix,h.GetNbinsX(),h.GetXaxis().GetXmin(),h.GetXaxis().GetXmax())
    htmp = ROOT.TH1F("tmp","tmp",h.GetNbinsY(),h.GetYaxis().GetXmin(),h.GetYaxis().GetXmax())
    for i in range(1,h.GetNbinsX()+1):
        htmp.Clear()
        for j in range(0,h.GetNbinsY()+2):
            htmp.SetBinContent(j, h.GetBinContent(i,j))
            htmp.SetBinError(j, h.GetBinError(i,j))
        hOut.SetBinContent(i, htmp.GetMean(1))
        hOut.SetBinError(i, htmp.GetMeanError(1))
    return hOut

def producePlot(h, axisLabel, title, maxbins):
    # Obtain canvas
    c = ROOT.TCanvas()
    # Do fit
    fit = ROOT.TF1("fit",myfitfunc,0,20,2)
    fit.SetParNames ("Slope","Offset")
    fit.SetLineWidth(2)

    hFrame = ROOT.TH1F("frame","frame",2,0,maxbins)
    hFrame.SetMinimum(0)
    hFrame.SetMaximum(200)
    hFrame.SetXTitle("N_{vertices}")
    hFrame.SetYTitle(axisLabel)
    #c.SetLogy()
    #hFrame.FindObject("stats").SetLineColor(ROOT.kBlue-6)
                #h1.FindObject("stats").SetTextColor(ROOT.kBlue-6)
                #h1.FindObject("stats").Draw()
    h.SetLineColor(ROOT.kBlack)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetMarkerSize(0.6)
    h.SetMarkerStyle(20)

    # Do ugly hack to force creation of fit stats object and make a clone of it (since drawing the frame destroys the stats object)
    # If the fit -command is called after the frame has been drawn, the axis labels on the frame diasppear :)
    h.Fit("fit")
    ROOT.gPad.Update()
    stats = h.FindObject("stats").Clone()

    hFrame.Draw()
    h.Draw("SAME E")
    stats.Draw()

    #h.FindObject("stats").Draw()
    chi2 = -1
    if fit.GetNDF() > 0:
        chi2 = fit.GetChisquare()/fit.GetNDF()
    print "Fit for %s: params: chi2/ndf %f slope %f +- %f constant %f +- %f"%(title,chi2,fit.GetParameter(0),fit.GetParError(0),fit.GetParameter(1),fit.GetParError(1))
    # FIXME : add here saving of the parameters into a config file
    # Legend
    leg = ROOT.TLegend(0.19, 0.82, 0.9, 0.88, "", "brNDC")
    leg.SetBorderSize(0)
    leg.SetTextFont(63)
    leg.SetTextSize(18)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.AddEntry(h, title, "lp")
    leg.Draw()
    
    c.Print("phiOscillation_%s.png"%title)

    
def main(opts):
    maxbins = 60
  
    tdrstyle.TDRStyle()
    # loop over datasets
    
    for mydir in opts.dirs:
        histoPath = "signalAnalysis%s"%opts.era[0]
        if "Tau_" in mydir:
            histoPath = "signalAnalysis"
        histos = []
        rootFile = ROOT.TFile.Open(os.path.join(mydir, "res", "histograms-%s.root"%mydir))
        if rootFile == None:
            raise Exception ("Error: File 'histograms-%s.root' not found!"%mydir)
        hX = produceCurve(rootFile, histoPath, "METPhiOscillationCorrection/NverticesVsMETX")
        hY = produceCurve(rootFile, histoPath, "METPhiOscillationCorrection/NverticesVsMETY")
        hTauX = produceCurve(rootFile, histoPath, "CommonPlots/Taus/TauPhiOscillationX")
        hTauY = produceCurve(rootFile, histoPath, "CommonPlots/Taus/TauPhiOscillationY")
        
        # We have the histograms and names, lets make the plot
        producePlot(hX, "Average MET_{x}, GeV", "METX_%s"%mydir, maxbins)
        producePlot(hY, "Average MET_{y}, GeV", "METY_%s"%mydir, maxbins)

        producePlot(hTauX, "Average #tau p_{x}, GeV", "TauX_%s"%mydir, maxbins)
        producePlot(hTauY, "Average #tau p_{y}, GeV", "TauY_%s"%mydir, maxbins)

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-d", dest="dirs", action="append", help="name of sample directory inside multicrab dir (multiple directories can be specified with multiple -d arguments)")
    parser.add_option("-v", dest="variation", action="append", help="name of variation")
    parser.add_option("-e", dest="era", action="append", help="name of era")
    (opts, args) = parser.parse_args()

    # Check that proper arguments were given
    mystatus = True
    if opts.dirs == None:
        print "Missing source for sample directories!\n"
        mystatus = False
    if opts.era == None:
        print "Missing specification for era!\n"
        mystatus = False
    if not mystatus:
        parser.print_help()
        sys.exit()

    # Arguments are ok, proceed to run
    main(opts)

