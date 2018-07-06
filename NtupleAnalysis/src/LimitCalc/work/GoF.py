#!/usr/bin/env python
'''
DESCRIPTION:
Plots goodness-of-fit plots
See https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#Goodness_of_fit_tests
for more details.


USAGE:
python GoF.py [opts]


EXAMPLES:
python GoF.py


LAST USED:
python GoF.py

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import ROOT
import sys
import os
from subprocess import call, check_output

#================================================================================================ 
# Function definition
#================================================================================================ 
def main():
    
    # ROOT
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)

    # Settings
    analysis = "H^{+}#rightarrow tb fully hadronic"
    #analysis = "H^{+}#rightarrow#tau_{h}#nu fully hadronic"
    
    ### hadd
    if not os.path.isfile("higgsCombineToys.GoodnessOfFit.mH120.root"):
        call("hadd higgsCombineToys.GoodnessOfFit.mH120.root higgsCombinetoys*.GoodnessOfFit.mH120.*.root", shell=True)
        
    ### perform GoF calculations
    fToys = ROOT.TFile("higgsCombineToys.GoodnessOfFit.mH120.root")
    fData = ROOT.TFile("higgsCombineData.GoodnessOfFit.mH120.root")

    tToys = fToys.Get("limit")
    tData = fData.Get("limit")

    nToys = tToys.GetEntries()

    #print tData.Print()
    #print tData.GetEntries(), tToys.GetEntries()

    tData.GetEntry(0)
    GoF_DATA = tData.limit
    print GoF_DATA

    GoF_TOYS_TOT = 0
    pval = 0
    toys = []
    minToy = 99999999
    maxToy = -99999999

    for i in range(0, tToys.GetEntries()):

        tToys.GetEntry(i)
        GoF_TOYS_TOT += tToys.limit
        toys.append(tToys.limit)
        if tToys.limit > GoF_DATA: pval += tToys.limit

        
    pval = pval / GoF_TOYS_TOT


    hist = ROOT.TH1D("GoF", "", 50, round(min(toys)), round(max(toys)))
    for k in toys: hist.Fill(k)


    ### start plotting
    c = ROOT.TCanvas("c", "c", 800, 800)
    c.SetTopMargin(0.055)
    c.SetRightMargin(0.05)
    c.SetLeftMargin(0.1)
    c.SetBottomMargin(0.05)

    hist.GetYaxis().SetTitle("Entries")
    hist.GetXaxis().SetTitle("")
                
    hist.GetXaxis().SetTitleFont(43)
    hist.GetXaxis().SetTitleSize(35)
    hist.GetXaxis().SetLabelFont(43)
    hist.GetXaxis().SetLabelSize(30)
            
    hist.GetYaxis().SetTitleFont(43)
    hist.GetYaxis().SetTitleSize(35)
    hist.GetYaxis().SetLabelFont(43)
    hist.GetYaxis().SetLabelSize(30)

    hist.GetXaxis().SetTitleOffset(1.1*hist.GetXaxis().GetTitleOffset())
    hist.GetYaxis().SetTitleOffset(1.1*hist.GetYaxis().GetTitleOffset())
    hist.GetXaxis().SetLabelOffset(1.1*hist.GetXaxis().GetLabelOffset())
    hist.GetYaxis().SetLabelOffset(1.1*hist.GetYaxis().GetLabelOffset())

    hist.SetLineColor(ROOT.kRed)
    hist.SetLineWidth(2)
    hist.Draw()

    arr = ROOT.TArrow(GoF_DATA, 0.0001, GoF_DATA, hist.GetMaximum()/8, 0.02, "<|")
    arr.SetLineColor(ROOT.kBlue)
    arr.SetFillColor(ROOT.kBlue)
    arr.SetFillStyle(1001)
    arr.SetLineWidth(3)
    arr.SetLineStyle(1)
    arr.SetAngle(60)
    arr.Draw("<|same")

    # top text left
    left = ROOT.TLatex()
    left.SetNDC()
    left.SetTextFont(43)
    left.SetTextSize(30)
    left.SetTextAlign(11)
    left.DrawLatex(.1,.95, "GoF - saturated model") # cfg['toptext_left']

    # top text right
    right = ROOT.TLatex()
    right.SetNDC()
    right.SetTextFont(43)
    right.SetTextSize(30)
    right.SetTextAlign(31)
    right.DrawLatex(.95,.95, analysis)

    # CMS preliminary
    right.SetTextSize(35)
    right.SetTextAlign(13)
    right.DrawLatex(.13,.91,"#bf{CMS} #scale[0.7]{#it{Internal}}")


    # p-value
    tt = ROOT.TLatex()
    tt.SetNDC()
    tt.SetTextFont(43)
    tt.SetTextSize(30)
    tt.SetTextAlign(11)
    tt.DrawLatex(.13,.80, "# toys: %d" % nToys)
    tt.DrawLatex(.13,.75, "p-value: %.2f" % pval)

    c.SaveAs("GoF.C")
    c.SaveAs("GoF.png")
    c.SaveAs("GoF.pdf")

    print "----------------------------"
    print "toys", nToys
    print "p-value", pval
    return

#================================================================================================ 
# Function definition
#================================================================================================ 
if __name__ == "__main__":


    main()
