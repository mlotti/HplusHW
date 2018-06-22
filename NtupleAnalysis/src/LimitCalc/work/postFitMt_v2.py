#!/usr/bin/env python

import os
import sys
import re
import array

import ROOT

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms

import ROOT
ROOT.gROOT.SetBatch(True)

formats = [".pdf",".png",".C"]
plotDir = "PostFitMt2016"
lumi = "35.9"

XBIN_MIN = 0
XBIN_MAX = 3000

DATAROOTFILE    = "combineCards_taunu_mH200_combined.root"
POSTFITROOTFILE = "fitDiagnostics.root"

class Category:
    def __init__(self,name):
        self.name = name
        self.histonames = []
        self.labels = {}
        self.colors = {}
        self.h_data = None
        self.histograms = {}

    def addData(self,datarootfile):
        self.datafile = datarootfile

    def addHisto(self,histo,legendlabel,color=0):
        self.histonames.append(histo)
        self.labels[histo] = legendlabel
        self.colors[histo] = color

    def clone(self,name):
        returnCat = Category(name)
        returnCat.histonames = self.histonames
        returnCat.labels = self.labels
        returnCat.colors = self.colors
#        returnCat.histograms = self.histograms
#        returnCat.h_data = self.h_data
#        if not self.h_data == None:
#            print "check clone1",self.h_data.GetEntries()
#            print "check clone2",returnCat.h_data.GetEntries()
        return returnCat

    def __add__(self,cat):
        returnCat = Category("sum")
        returnCat.colors = self.colors
        returnCat.histonames = self.histonames

        if self.h_data == None:
            returnCat.h_data = self.h_data
        else:
            returnCat.h_data = self.h_data.Add(cat.h_data)
        if len(self.histograms) == 0:
            returnCat.histograms = cat.histograms
        else:
            returnCat.histograms = []
            for hname in self.histonames:
                h_sum = self.histograms[hname].Add(cat.histograms[hname])
                returnCat.histograms.append(h_sum)
        return returnCat

    def fetchHistograms(self,fINdata,fINpost):

        histoData = fINdata.Get(os.path.join(self.name,"data_obs"))
        self.h_data = histoData.Clone("Data")
        nbins = 0
        binning = []
        for iBin in range(self.h_data.GetNbinsX()+1):
            #print "Data",iBin,self.h_data.GetBinLowEdge(iBin),self.h_data.GetBinWidth(iBin)
            binLowEdge = self.h_data.GetBinLowEdge(iBin)
            if binLowEdge >= XBIN_MIN and binLowEdge < XBIN_MAX:
                nbins += 1
                binning.append(binLowEdge)
        binning.append(XBIN_MAX)

        n = len(binning)-1
        self.h_data.SetBins(nbins,array.array("d",binning))


        for hname in self.histonames:
            template = self.h_data.Clone(hname)
            template.Reset()

            n = len(binning)-1
            template.SetBins(n,array.array("d",binning))

            #for iBin in range(template.GetNbinsX()+1):
            #    print "template",iBin,template.GetBinLowEdge(iBin),template.GetBinWidth(iBin)

            histo = fINpost.Get(os.path.join("shapes_fit_b",self.name,hname))
            for iBin in range(0,histo.GetNbinsX()):
                template.SetBinContent(iBin,histo.GetBinContent(iBin))
            template.SetFillColor(self.colors[hname])
            ####template.SetLineColor(self.colors[hname])
            self.histograms[hname] = template
            #print "check histo",template.GetEntries()


    def plot(self,plotDir):

        histolist = []
#        self.h_data.SetMarkerStyle(21)
#        self.h_data.SetMarkerSize(2)
        styles.dataStyle.apply(self.h_data)
        hhd = histograms.Histo(self.h_data,"Data",legendStyle="E1P", drawStyle="E1P")
        hhd.setIsDataMC(isData=True,isMC=False)
        histolist.append(hhd)
        for hname in self.histonames:
            hhp = histograms.Histo(self.histograms[hname],hname,legendStyle="F", drawStyle="HIST",legendLabel=self.labels[hname])
            hhp.setIsDataMC(isData=False,isMC=True)
            histolist.append(hhp)


        name = "postFitMt_"+self.name

        style = tdrstyle.TDRStyle()

        p = plots.DataMCPlot2(histolist)
        p.stackMCHistograms()

        opts = {}
        opts2 = {"ymin": 0.5, "ymax": 1.5}
        p.createFrame(os.path.join(plotDir, name), logx=True, createRatio=True, opts=opts, opts2=opts2)
        p.getFrame().GetXaxis().SetTitle("m_{T}(GeV)")
        p.getFrame().GetYaxis().SetTitle("< Events / bin >")
        p.getFrame2().GetYaxis().SetTitle("Data/Bkg.")

        p.getPad().SetLogx(True)
        p.getPad2().SetLogx(True)  
#        ROOT.gPad.SetLogx(True)

	moveLegend = {"dx": -0.1, "dy": -0.1, "dh": 0.}
	p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

        p.draw()

        histograms.addStandardTexts(lumi=lumi)
        
        if not os.path.exists(plotDir):
            os.mkdir(plotDir)
        p.save(formats)
        print "Saved plot",os.path.join(plotDir, name)


# List categories and add the histogram names
taunuHadr_1 = Category("taunuhadr_a")
taunuHadr_1.addHisto("qcdfaketau","Mis-ID.#tau_{h}(data)",color=ROOT.kOrange-2)
taunuHadr_1.addHisto("ttbar","t#bar{t}",color=ROOT.kMagenta-2)
taunuHadr_1.addHisto("wjets","W+jets",color=ROOT.kOrange+9)
taunuHadr_1.addHisto("singletop","Single t",color=ROOT.kSpring+4)
taunuHadr_1.addHisto("dy","Z/#gamma^{*}+jets",color=ROOT.kTeal-9)
taunuHadr_1.addHisto("diboson","Diboson",color=ROOT.kBlue-4)

taunuHadr_2 = taunuHadr_1.clone("taunuhadr_b")

categories = [taunuHadr_1,taunuHadr_2]

#--------------------------------------------------

taunuLept_1 = Category("ch1_R1_0_1El")
taunuLept_1.addHisto("ttlf","ttlf",color=ROOT.kRed-7)
taunuLept_1.addHisto("ttcc","ttcc",color=ROOT.kRed-3)
taunuLept_1.addHisto("ttb","ttb",color=ROOT.kRed-5)
taunuLept_1.addHisto("ttbb","ttbb",color=ROOT.kRed+3)
taunuLept_1.addHisto("wjets","W+jets",color=ROOT.kOrange+9)
taunuLept_1.addHisto("singletop","Single t",color=ROOT.kSpring+4)
taunuLept_1.addHisto("vv","Diboson",color=ROOT.kBlue-4)
taunuLept_1.addHisto("dy","Z/#gamma^{*}+jets",color=ROOT.kTeal-9)

taunuLept_2  = taunuLept_1.clone("ch1_R1_0_1Mu")
taunuLept_3  = taunuLept_1.clone("ch1_R1_1_1El")
taunuLept_4  = taunuLept_1.clone("ch1_R1_1_1Mu")
taunuLept_5  = taunuLept_1.clone("ch1_R2_0_1El")
taunuLept_6  = taunuLept_1.clone("ch1_R2_0_1Mu")
taunuLept_7  = taunuLept_1.clone("ch1_R2_1_1El")
taunuLept_8  = taunuLept_1.clone("ch1_R2_1_1Mu")
taunuLept_9  = taunuLept_1.clone("ch1_R3_0_1El")
taunuLept_10 = taunuLept_1.clone("ch1_R3_0_1Mu")
taunuLept_11 = taunuLept_1.clone("ch1_R3_1_1El")
taunuLept_12 = taunuLept_1.clone("ch1_R3_1_1Mu")
taunuLept_13 = taunuLept_1.clone("ch1_R4_0_1El")
taunuLept_14 = taunuLept_1.clone("ch1_R4_0_1Mu")
taunuLept_15 = taunuLept_1.clone("ch1_R4_1_1El")
taunuLept_16 = taunuLept_1.clone("ch1_R4_1_1Mu")

#categories = [taunuLept_1]#,taunuLept_2,taunuLept_3,taunuLept_4,taunuLept_5,taunuLept_6,taunuLept_7,taunuLept_8,taunuLept_9,taunuLept_10,taunuLept_11,taunuLept_12,taunuLept_13,taunuLept_14,taunuLept_15,taunuLept_16]

# ttlf kRed-7
# ttcc kRed-3
# ttbb kRed+3
# ttb  kRed-5

#--------------------------------------------------

def usage():
    print
    print "### Usage:   "+sys.argv[0]+" <combine fitDiagnostics rootfile>"
    print
    sys.exit()

        
def main():

    
#    if len(sys.argv) < 2:
#        usage()

#    fIN = ROOT.TFile.Open(sys.argv[1],"R")
    fIN_data = ROOT.TFile.Open(DATAROOTFILE,"R")
    fIN_post = ROOT.TFile.Open(POSTFITROOTFILE,"R")


    categorySum = categories[0].clone("sum")
    for c in categories:
        c.fetchHistograms(fIN_data,fIN_post)
#### DIFFERENT BINNING!!        categorySum = categorySum + c
#### DIFFERENT BINNING!!    categories.append(categorySum)
    for c in categories:
        c.plot(plotDir)
    

    fIN_data.Close()
    fIN_post.Close()

if __name__=="__main__":
    main()
