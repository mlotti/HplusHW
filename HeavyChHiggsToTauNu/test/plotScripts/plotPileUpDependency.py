#! /usr/bin/env python

import sys
import ROOT
ROOT.gROOT.SetBatch(True)

import os
from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.multicrab as multicrab
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle

def myfitfunc(x, par):
    return par[0]

def main(opts):
    tdrstyle.TDRStyle()
    # loop over datasets
    histos = []
    labels = []
    for multicrabDir in opts.multicrabdir:
        crabDirs = multicrab.getTaskDirectories(None, os.path.join(multicrabDir, "multicrab.cfg"))
        for crabDir in crabDirs:
            taskName = os.path.split(crabDir)[1]
            rootFile = ROOT.TFile.Open(os.path.join(crabDir, "res", "histograms-%s.root"%taskName))
            if rootFile.IsZombie():
                sys.exit()
            # Get histogram
            h = rootFile.Get("signalAnalysis/SignalSelectionFlowVsVertices")
            if h == 0:
                sys.exit()
            histos.append(h)
            labels.append(taskName)
    # We have the histograms and names, lets loop over the selection steps
    idx = 0
    for i in range(0, histos[0].GetNbinsY()-1):
        myvtxbins = 35
        myrebinfactor = 5
        hout = ROOT.TH1F("PUdependency","PUdependency",myvtxbins,0,myvtxbins)
        hout.SetMinimum(0.0)
        hout.SetMaximum(1.1)
        hout.SetXTitle("N_{vertices}")
        if i == 0:
            hout.SetYTitle("Offline selection efficiency")
        else:
            hout.SetYTitle("Efficiency of "+histos[0].GetYaxis().GetBinLabel(i+1))
        myGraphs = []
        myLines = []
        myMin = 1.0
        myMax = 0.0
        for j in range(0,len(histos)):
            idx += 1
            htotal = ROOT.TH1F("htot"+str(idx),"htot",hout.GetNbinsX(),0,hout.GetNbinsX())
            hpassed = ROOT.TH1F("hpass"+str(idx),"hpass",hout.GetNbinsX(),0,hout.GetNbinsX())
            for k in range(1, hout.GetNbinsX()+1):
                if i == 0:
                    # dphi<160 vs. trg
                    htotal.SetBinContent(k, histos[j].GetBinContent(k, 1))
                    htotal.SetBinError(k, histos[j].GetBinError(k, 1))
                    hpassed.SetBinContent(k, histos[j].GetBinContent(k, histos[0].GetNbinsY()-1))
                    hpassed.SetBinError(k, histos[j].GetBinError(k, histos[0].GetNbinsY()-1))                 
                else:
                    htotal.SetBinContent(k, histos[j].GetBinContent(k, i))
                    htotal.SetBinError(k, histos[j].GetBinError(k, i))
                    hpassed.SetBinContent(k, histos[j].GetBinContent(k, i+1))
                    hpassed.SetBinError(k, histos[j].GetBinError(k, i+1))
            htotal.Rebin(myrebinfactor)
            hpassed.Rebin(myrebinfactor)
            hpassed.Divide(htotal)
            for k in range(0, htotal.GetNbinsX()):
                if hpassed.GetBinContent(k)+hpassed.GetBinError(k) > myMax and htotal.GetBinContent(k+1) > 0:
                    myMax = hpassed.GetBinContent(k)+hpassed.GetBinError(k)
                if hpassed.GetBinContent(k)-hpassed.GetBinError(k) < myMin and hpassed.GetBinContent(k)-hpassed.GetBinError(k) > 0 and htotal.GetBinContent(k+1) > 0 and hpassed.GetBinContent(k+1) > 0:
                    myMin = hpassed.GetBinContent(k)-hpassed.GetBinError(k)
            mycolor = 2+j
            if mycolor > 4:
                mycolor += 1
            hpassed.SetLineColor(mycolor)
            hpassed.SetLineWidth(3)
            hpassed.SetMarkerSize(1.0)
            hpassed.SetMarkerColor(mycolor)
            hpassed.SetMarkerStyle(21+j)
            myGraphs.append(hpassed)
            hcloned = hpassed.Clone("hclone"+str(idx))
            myfit = ROOT.TF1("myfunc",myfitfunc,5.0,30.0,1)
            myfit.SetLineWidth(0)
            hcloned.Fit(myfit)
            # add line for average
            myline = ROOT.TH1F("hline"+str(idx),"hline"+str(idx),hout.GetNbinsX(),0,hout.GetNbinsX())
            for k in range (1, hout.GetNbinsX()+1):
                myline.SetBinContent(k, myfit.GetParameter(0))
                #myline.SetBinError(k, myfit.GetParError(0))
            print myfit.GetParameter(0)
            myline.SetLineWidth(3)
            myline.SetLineColor(mycolor)
            myline.SetLineStyle(2)
            myline.SetMarkerSize(0)
            myLines.append(myline)
        # plot graph
        c = ROOT.TCanvas()
        if myMin > 0.0:
            hout.SetMinimum(myMin)
        if myMax < 1.0:
            if myMax < 0.15:
                hout.SetMaximum(0.15)
            else:
                hout.SetMaximum(myMax)
        if i == 0:
            c.SetLogy()
        hout.Draw()
        for l in myLines:
            l.Draw("h same")
        myGraphs.reverse()
        for g in myGraphs:
            g.Draw("e same")
        leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9, "", "brNDC")
        for g in range(0,len(myGraphs)):
            leg.AddEntry(myGraphs[g], labels[g], "lv")
        #leg.Draw()
        c.Print("pileUpDependency_%d_"%i+opts.multicrabdir[0]+".png")

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--mdir", dest="multicrabdir", action="append", help="name of multicrab dir (multiple directories can be specified with multiple --mdir arguments)")
    (opts, args) = parser.parse_args()
    
    # Check that proper arguments were given
    mystatus = True
    if opts.multicrabdir == None:
        print "Missing source for multicrab directories!\n"
        mystatus = False
    if not mystatus:
        parser.print_help()
        sys.exit()

    # Arguments are ok, proceed to run
    main(opts)
    
    #sys.exit(main(opts))
