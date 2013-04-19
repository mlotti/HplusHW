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
    return par[0]

def getHistogram(rootfile,histoname):
    h = rootfile.Get(histoname)
    if h == None:
        raise Exception ("Error: histogram '%s' not found!"%histoname)
    return h;

def produceEfficiencyCurve(rootfile, histoPath, histoNamePrefix, label):
    hBefore = getHistogram(rootfile, "%s/%sBefore"%(histoPath, histoNamePrefix))
    hBefore.Rebin(2)
    hAfter = getHistogram(rootfile, "%s/%sAfter"%(histoPath, histoNamePrefix))
    hAfter.Rebin(2)
    # Produce fake rate
    aint = hAfter.Integral()
    #print hAfter.GetNbinsX(),hBefore.GetNbinsX()
    #for i in range(0,hAfter.GetNbinsX()+2):
        #print i,hAfter.GetBinContent(i),hAfter.GetBinError(i),hBefore.GetBinContent(i),hBefore.GetBinError(i)
    ##eff = ROOT.TGraphAsymmErrors(hAfter, hBefore)
    #eff = ROOT.TGraphAsymmErrors(hAfter, hAfter)
    hAfter.Divide(hBefore);
    #for i in range(1,hAfter.GetNbinsX()+1):
        #print i,eff.GetY()[i-1],hAfter.GetBinContent(i)
    #print eff.GetN()
    #sys.exit()
    #hEff = hAfter
    return [hAfter, label, aint, hBefore.Integral()]

def makeFakeRatePlot(histos, label, fileprefix, mydir):
    c = ROOT.TCanvas()
    c.SetLogy()
    hFrame = ROOT.TH1F("frame","frame",2,40,200)
    hFrame.SetMinimum(1.0e-3)
    hFrame.SetMaximum(1.0)
    hFrame.Draw()
    hFrame.SetXTitle(label)
    hFrame.SetYTitle("Fake rate")
    for i in range(0,len(histos)):
        histos[i][0].SetLineColor(i+1)
        histos[i][0].SetMarkerColor(i+1)
        histos[i][0].SetMarkerSize(0.6)
        histos[i][0].SetMarkerStyle(i+18)
        histos[i][0].Draw("E SAME")
    leg = ROOT.TLegend(0.7, 0.7, 0.9, 0.9, "", "brNDC")
    leg.SetBorderSize(0)
    leg.SetTextFont(63)
    leg.SetTextSize(18)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    for i in range(0,len(histos)):
        leg.AddEntry(histos[i][0], histos[i][1], "lp")
    leg.Draw()
    c.Print("%s_%s.png"%(fileprefix,mydir))
    #c.Print("tauFakeRate_%s.C"%mydir)
    #c.Print("tauFakeRate_%s.eps"%mydir)
    # Let's output some stats
    myTotalAfter = 0.0
    for i in range(0,len(histos)):
        myTotalAfter += histos[i][2]
    for i in range(0,len(histos)):
        if histos[i][2] > 0:
            print "%s: Nafter = %f (%f %% of all), avg fake rate = %f"%(histos[i][1],histos[i][2],histos[i][2]/myTotalAfter,histos[i][2]/histos[i][3])
    
def makeDeltaPtPlot(histos, label, fileprefix, mydir):
    c = ROOT.TCanvas()
    #c.SetLogy()
    hFrame = ROOT.TH1F("frame","frame",2,-100,50)
    hFrame.SetMinimum(1.0e-3)
    hFrame.SetMaximum(0.5)
    hFrame.Draw()
    hFrame.SetXTitle(label)
    hFrame.SetYTitle("N (normalised to 1) / 5 Gev/c")
    for i in range(0,len(histos)):
        histos[i][0].SetLineColor(i+1)
        histos[i][0].SetMarkerColor(i+1)
        histos[i][0].SetMarkerSize(0.6)
        histos[i][0].SetMarkerStyle(i+18)
        if histos[i][0].Integral() > 0:
            histos[i][0].Scale(1.0/histos[i][0].Integral())
        histos[i][0].Draw("E SAME")
    leg = ROOT.TLegend(0.2, 0.7, 0.5, 0.9, "", "brNDC")
    leg.SetBorderSize(0)
    leg.SetTextFont(63)
    leg.SetTextSize(18)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    for i in range(0,len(histos)):
        leg.AddEntry(histos[i][0], histos[i][1], "lp")
    leg.Draw()
    c.Print("%s_%s.png"%(fileprefix,mydir))

def main(opts):
    tdrstyle.TDRStyle()
    # loop over datasets
    histoPath = "signalAnalysis%s%s/NormalisationAnalysis/TauFakeRate"%(opts.runType[0], opts.era[0])
    for mydir in opts.dirs:
        histosVsTauPt = []
        histosVsJetPt = []
        rootFile = ROOT.TFile.Open(os.path.join(mydir, "res", "histograms-%s.root"%mydir))
        if rootFile == None:
            raise Exception ("Error: File 'histograms-%s.root' not found!"%mydir)
        # Get histograms
        histosVsTauPt.append(produceEfficiencyCurve(rootFile, histoPath, "TauFakeRatePtb", "b#rightarrow#tau"))
        histosVsTauPt.append(produceEfficiencyCurve(rootFile, histoPath, "TauFakeRatePtc", "c#rightarrow#tau"))
        histosVsTauPt.append(produceEfficiencyCurve(rootFile, histoPath, "TauFakeRatePtuds", "uds#rightarrow#tau"))
        histosVsTauPt.append(produceEfficiencyCurve(rootFile, histoPath, "TauFakeRatePtg", "g#rightarrow#tau"))
        histosVsJetPt.append(produceEfficiencyCurve(rootFile, histoPath, "TauFakeRatePtbByJetPt", "b#rightarrow#tau"))
        histosVsJetPt.append(produceEfficiencyCurve(rootFile, histoPath, "TauFakeRatePtcByJetPt", "c#rightarrow#tau"))
        histosVsJetPt.append(produceEfficiencyCurve(rootFile, histoPath, "TauFakeRatePtudsByJetPt", "uds#rightarrow#tau"))
        histosVsJetPt.append(produceEfficiencyCurve(rootFile, histoPath, "TauFakeRatePtgByJetPt", "g#rightarrow#tau"))
        #histos.append(produceEfficiencyCurve(rootFile, histoPath, "TauFakeRatePte", "e#rightarrow#tau"))
        #histos.append(produceEfficiencyCurve(rootFile, histoPath, "TauFakeRatePtmu", "#mu#rightarrow#tau"))
        # We have the histograms and names, lets make the plot
        makeFakeRatePlot(histosVsTauPt, "#tau p_{T}, GeV/c", "tauFakeRateVsTauPt", mydir)
        makeFakeRatePlot(histosVsJetPt, "jet p_{T}, GeV/c", "tauFakeRateVsJetPt", mydir)
        # Get histograms for delta pT (tau,ref.jet)
        histosDeltaPt = [] 
        histosDeltaPt.append([getHistogram(rootFile, "%s/TauVsJetDeltaPttaus"%histoPath), "genuine #tau", -1, -1]);
        histosDeltaPt.append([getHistogram(rootFile, "%s/TauVsJetDeltaPtelectrons"%histoPath), "e#rightarrow#tau", -1, -1]);
        histosDeltaPt.append([getHistogram(rootFile, "%s/TauVsJetDeltaPtcb"%histoPath), "cb#rightarrow#tau", -1, -1]);
        histosDeltaPt.append([getHistogram(rootFile, "%s/TauVsJetDeltaPtuds"%histoPath), "uds#rightarrow#tau", -1, -1]);
        makeDeltaPtPlot(histosDeltaPt, "#tau p_{T} - ref.jet p_{T} , GeV/c", "tauRefJetDeltaPt", mydir)
        hDeltaPtMode0 = []
        myPath = "signalAnalysis%s%s"%(opts.runType[0],opts.era[0])
        hDeltaPtMode0.append([getHistogram(rootFile, "%s/DeltaPtDecayMode0"%myPath), "tau pT - jet pT", -1, -1]);
        hDeltaPtMode0.append([getHistogram(rootFile, "%s/DeltaPtDecayMode0NoNeutralHadrons"%myPath), "tau pT - jet pT*(1-neutralHadronEnergyFraction)", -1, -1]);
        makeDeltaPtPlot(hDeltaPtMode0, "e/jet#rightarrow#tau decay mode 0: #Delta p_{T}, GeV/c", "tauRefJetDeltaPtDecayMode0", mydir)
        hDeltaPtMode1 = []
        hDeltaPtMode1.append([getHistogram(rootFile, "%s/DeltaPtDecayMode1"%myPath), "tau pT - jet pT", -1, -1]);
        hDeltaPtMode1.append([getHistogram(rootFile, "%s/DeltaPtDecayMode1NoNeutralHadrons"%myPath), "tau pT - jet pT*(1-neutralHadronEnergyFraction)", -1, -1]);
        makeDeltaPtPlot(hDeltaPtMode1, "e/jet#rightarrow#tau decay mode 1: #Delta p_{T}, GeV/c", "tauRefJetDeltaPtDecayMode1", mydir)
        hDeltaPtMode2 = []
        hDeltaPtMode2.append([getHistogram(rootFile, "%s/DeltaPtDecayMode2"%myPath), "tau pT - jet pT", -1, -1]);
        hDeltaPtMode2.append([getHistogram(rootFile, "%s/DeltaPtDecayMode2NoNeutralHadrons"%myPath), "tau pT - jet pT*(1-neutralHadronEnergyFraction)", -1, -1]);
        makeDeltaPtPlot(hDeltaPtMode2, "e/jet#rightarrow#tau decay mode 2: #Delta p_{T}, GeV/c", "tauRefJetDeltaPtDecayMode2", mydir)
        rootFile.Close()

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("-d", dest="dirs", action="append", help="name of sample directory inside multicrab dir (multiple directories can be specified with multiple -d arguments)")
    parser.add_option("-v", dest="variation", action="append", help="name of variation")
    parser.add_option("-e", dest="era", action="append", help="name of era")
    parser.add_option("-t", dest="runType", action="append", help="type of run (light / heavy)")
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

