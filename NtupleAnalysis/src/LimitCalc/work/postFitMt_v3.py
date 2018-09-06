#!/usr/bin/env python

#Script for plotting post-fit mT shapes.
#
#Usage:
#0) Create a new directory, copy the combine input datacard txt file and the corresponding root file(s) in there
#1) Produce fitDiagnostics.root file containing post-fit shapes by running combine with this set of command line parameters:
#combine -M FitDiagnostics --robustFit=1  --X-rtd MINIMIZER_analytic ws.root --saveShapes --saveWithUncertainties --saveOverallShapes --saveNormalizations  --saveWorkspace --plots --expectSignal=0 --rMin=-4 #<path-to-datacard-txt-file>
#2) Copy this script inside the directory and do necessary modifications, e.g. update DATAROOTFILE variable to point to your combine input root file
#3) Run this script

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

formats = [".pdf",".png"] #,".C"]
plotDir = "" #PostFitMt2016"
lumi = "35.9"

XBIN_MIN = 0     #left edge of the first bin in rebinned input data histogram
XBIN_MAX = 10000 #right edge of the last bin in re-binned input datahistogram
XMAX_IN_PLOT = 1200.0

DATAROOTFILE    = "taunu_combined.root"
POSTFITROOTFILE = "fitDiagnostics.root"

class Category:
    def __init__(self,name):
        self.name = name
        self.histonames = []
        self.labels = {}
        self.colors = {}
        self.h_data = None
        self.histograms = {}
        self.opts = {"xmin": 2.0, "xmax" : XMAX_IN_PLOT, "ymin" : 0}
        self.optsLogx = {"xmin": 2.0, "xmax": XMAX_IN_PLOT}
        self.opts2 = {"ymin": 0.0, "ymax": 1.999999}
        self.moveLegend = {}

    def addData(self,datarootfile):
        self.datafile = datarootfile

    def addHisto(self,histo,legendlabel,color=0):
        self.histonames.append(histo)
        self.labels[histo] = legendlabel
        self.colors[histo] = color

    def setXmax(self,xmax):
        self.opts["xmax"] = xmax
        self.optsLogx["xmax"] = xmax

    def setXmin(self,xmin):
        self.opts["xmin"] = xmin
        self.optsLogx["xmin"] = xmin

    def setMoveLegend(self,move):
        self.moveLegend = move



    def clone(self,name):
        returnCat = Category(name)
        returnCat.histonames = self.histonames
        returnCat.labels = self.labels
        returnCat.colors = self.colors
        returnCat.opts = self.opts
        returnCat.opts2 = self.opts2
        returnCat.moveLegend = self.moveLegend
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
            binLowEdge = self.h_data.GetBinLowEdge(iBin)
            if binLowEdge >= XBIN_MIN and binLowEdge < XBIN_MAX:
                nbins += 1
                binning.append(binLowEdge)
        binning.append(XMAX_IN_PLOT)

        n = len(binning)-1
        self.h_data.SetBins(nbins,array.array("d",binning))
#        print "after SetBins self.h_data has %d bins, they are as follows:"%self.h_data.GetNbinsX()
#        for iBin in range(self.h_data.GetNbinsX()+1):
#            print "    DATA: Content of bin %d set to %.6f +- %.6f, low edge is %.1f, width is %.1f"%(iBin,self.h_data.GetBinContent(iBin),self.h_data.GetBinError(iBin),self.h_data.GetBinLowEdge(iBin),self.h_data.GetBinWidth(iBin))


        for hname in self.histonames:
            template = self.h_data.Clone(hname)
            template.Reset()
        
            n = len(binning)-1
            template.SetBins(n,array.array("d",binning))
#            print "after template.SetBins template has %d bins"%template.GetNbinsX()

            #for iBin in range(template.GetNbinsX()+1):
            #    print "template",iBin,template.GetBinLowEdge(iBin),template.GetBinWidth(iBin)
            print "hname=" + hname
            histo = fINpost.Get(os.path.join("shapes_fit_b",self.name,hname))
            print "trying to get histo: %s"%os.path.join("shapes_fit_b",self.name,hname)
            print "histo name is %s"%histo.GetName()
            print "template has %d bins"%template.GetNbinsX()
            print "histo has %d bins"%histo.GetNbinsX()
            for iBin in range(0,template.GetNbinsX()+1):
                template.SetBinContent(iBin,histo.GetBinContent(iBin))
                template.SetBinError(iBin,histo.GetBinError(iBin))
      #          print "Content of bin %d set to %.6f +- %.6f, low edge is %.1f, width is %.1f"%(iBin,template.GetBinContent(iBin),template.GetBinError(iBin),template.GetBinLowEdge(iBin),template.GetBinWidth(iBin))
            template.SetFillColor(self.colors[hname])
            ####template.SetLineColor(self.colors[hname])
            self.histograms[hname] = template
            #print "check histo",template.GetEntries()
    


    def plot(self,plotDir):

        histolist = []
#        self.h_data.SetMarkerStyle(21)
#        self.h_data.SetMarkerSize(2)
        styles.dataStyle.apply(self.h_data)
        hhd = histograms.Histo(self.h_data,"Data",legendStyle="PL", drawStyle="E1P")
        hhd.setIsDataMC(isData=True,isMC=False)
        histolist.append(hhd)
        for hname in self.histonames:
            hhp = histograms.Histo(self.histograms[hname],hname,legendStyle="F", drawStyle="HIST",legendLabel=self.labels[hname])
            hhp.setIsDataMC(isData=False,isMC=True)
            histolist.append(hhp)


        name = "postFitMt_"+self.name
#        name = "preFitMt_"+self.name

        style = tdrstyle.TDRStyle()

        p = plots.DataMCPlot2(histolist)
        p.setDefaultStyles()
        p.stackMCHistograms()
        p.setLuminosity(lumi)

        p.addMCUncertainty(postfit=True)
#        p.addText(0.7, 0.84, "2016", size=20) #FIXME
        p.setLegendHeader(self.getCategoryName())

        myParams = {}
        myParams["xlabel"] = "m_{T} (GeV)"
        myParams["ylabel"] = "< Events / GeV >"
        myParams["ratio"] = True
        myParams["ratioYlabel"] = "Data/Bkg. "
        myParams["logx"] = True
        myParams["ratioType"] ="errorScale" 
        myParams["ratioErrorOptions"] = {"numeratorStatSyst": False, "denominatorStatSyst": True}
        myParams["opts"] = self.opts
        myParams["optsLogx"] = self.optsLogx
        myParams["opts2"] = self.opts2
        myParams["errorBarsX"] = True
        myParams["xlabelsize"] = 25
        myParams["ylabelsize"] = 25
        myParams["addMCUncertainty"] = True
        myParams["addLuminosityText"] = True #FIXME
        myParams["moveLegend"] = self.moveLegend
        plots.drawPlot(p,os.path.join(plotDir, name),**myParams)
        print "Saved plot",os.path.join(plotDir, name)

### DEFINITION ###
    def getCategoryName(self):

        cat1 = "" # e.g. 1Mu + tauH, 1j1b
        cat2 = "" # e.g. 1Mu + tauH, 1j1b
    
        # hadronic cases

        if "taunuhadr_a" in self.name:
            return "#tau_{h}+jets, R_{#tau} < 0.75"
        if "taunuhadr_b" in self.name:
            return "#tau_{h}+jets, R_{#tau} > 0.75"

        # electron of muon
        if "_1Mu" in self.name:
            cat1 += "1#mu"
        elif "_1El" in self.name:
            cat1 += "1e"

        # category
        if "_notauh" in self.name:
            cat1 += " + #tau_{h}"
        elif "_tauh" in self.name:
            cat1 += ", no #tau_{h}"
 
        # jets
        if "_notauh" in self.name:
            if 'R1_0'  in self.name:  
                cat2 += '2j1b, p_{T}^{miss} < 150 GeV'
            elif 'R1_1'  in self.name:  
                cat2 = '2j1b, p_{T}^{miss} > 150 GeV'            
            elif 'R2_0'  in self.name:  
                cat2 = '2j2b, p_{T}^{miss} < 150 GeV'        
            elif 'R2_1'  in self.name:  
                cat2 = '2j2b, p_{T}^{miss} > 150 GeV'                
            elif 'R3_0'  in self.name:  
                cat2 = '3j1b, p_{T}^{miss} < 150 GeV'      
            elif 'R3_1'  in self.name:  
                cat2 = '3j1b, p_{T}^{miss} > 150 GeV'          
            elif 'R4_0'  in self.name:  
                cat2 = '3j2b, p_{T}^{miss} < 150 GeV'  
            elif 'R4_1'  in self.name:  
                cat2 = '3j2b, p_{T}^{miss} > 150 GeV'  

        # no tauh
        if "_tauh" in self.name:
            if 'R0_0'  in self.name:  
                cat2 = '1j1b, 100 < p_{T}^{miss} < 150 GeV'      
            elif 'R0_1'  in self.name:  
                cat2 = '1j1b, p_{T}^{miss} > 150 GeV'  
            elif 'R0_2'  in self.name:  
                cat2 = '1j1b, p_{T}^{miss} <  100 GeV'  
   
            elif 'R1_0'  in self.name:  
                cat2 = '2-3j,1b, 100 < p_{T}^{miss} < 150 GeV'      
            elif 'R1_1'  in self.name:  
                cat2 = '2-3j,1b, p_{T}^{miss} > 150 GeV'
            elif 'R1_2'  in self.name:  
                cat2 = '2-3j,1b, p_{T}^{miss} <  100 GeV'  
            
            elif 'R2_0'  in self.name:  
                cat2 = '2-3j,2b, 100 < p_{T}^{miss} < 150 GeV'             
            elif 'R2_1'  in self.name:  
                cat2 = '2-3j,2b, p_{T}^{miss} > 150 GeV'  
            elif 'R2_2'  in self.name:  
                cat2 = '2-3j,2b, p_{T}^{miss} <  100 GeV'  

        categoryName = "%s, %s"%(cat1,cat2)
        print "The category name is: %s"%categoryName
        return categoryName


# List categories and add the histogram names
taunuHadr_1 = Category("taunuhadr_a")
hadrMoveLegend = {"dx": -0.07, "dy": -0.03, "dh": 0.12}
taunuHadr_1.setMoveLegend(hadrMoveLegend)
taunuHadr_1.addHisto("qcdfaketau","Jets#rightarrow#tau_{h} (data)",color=ROOT.kOrange-2)
taunuHadr_1.addHisto("ttbar","t#bar{t}",color=ROOT.kMagenta-2)
taunuHadr_1.addHisto("wjets","W+jets",color=ROOT.kOrange+9)
taunuHadr_1.addHisto("singletop","Single t",color=ROOT.kSpring+4)
taunuHadr_1.addHisto("dy","Z/#gamma^{*}+jets",color=ROOT.kTeal-9)
taunuHadr_1.addHisto("vv","Diboson",color=ROOT.kBlue-4)
taunuHadr_1.setXmax(XMAX_IN_PLOT)
taunuHadr_2 = taunuHadr_1.clone("taunuhadr_b")

categories = [taunuHadr_1,taunuHadr_2]

#categories = [taunuHadr_1]

#--------------------------------------------------

# R0, tauh
taunuLept_1 = Category("ch1_ch1_R0_0_1El_tauh")
leptMoveLegend = {"dx": -0.22, "dy": -0.03, "dh": 0.2}
taunuLept_1.setMoveLegend(leptMoveLegend)
taunuLept_1.addHisto("ttbar","t#bar{t}",color=ROOT.kMagenta-2)
#taunuLept_1.addHisto("ttlf","ttlf",color=ROOT.kRed-7)
#taunuLept_1.addHisto("ttcc","ttcc",color=ROOT.kRed-3)
#taunuLept_1.addHisto("ttb","ttb",color=ROOT.kRed-5)
#taunuLept_1.addHisto("ttbb","ttbb",color=ROOT.kRed+3)
taunuLept_1.addHisto("wjets","W+jets",color=ROOT.kOrange+9)
taunuLept_1.addHisto("singletop","Single t",color=ROOT.kSpring+4)
taunuLept_1.addHisto("vv","Diboson",color=ROOT.kBlue-4)
taunuLept_1.addHisto("dy","Z/#gamma^{*}+jets",color=ROOT.kTeal-9)
taunuLept_1.setXmin(9.95)
taunuLept_1.setXmax(XMAX_IN_PLOT)
taunuLept_2  = taunuLept_1.clone("ch1_ch1_R0_0_1Mu_tauh")
taunuLept_3  = taunuLept_1.clone("ch1_ch1_R0_1_1El_tauh")
taunuLept_4  = taunuLept_1.clone("ch1_ch1_R0_1_1Mu_tauh")
taunuLept_5  = taunuLept_1.clone("ch1_ch1_R0_2_1El_tauh")
taunuLept_6  = taunuLept_1.clone("ch1_ch1_R0_2_1Mu_tauh")
# R1, tauh
taunuLept_7  = taunuLept_1.clone("ch1_ch1_R1_0_1El_tauh")
taunuLept_8  = taunuLept_1.clone("ch1_ch1_R1_0_1Mu_tauh")
taunuLept_9  = taunuLept_1.clone("ch1_ch1_R1_1_1El_tauh")
taunuLept_10 = taunuLept_1.clone("ch1_ch1_R1_1_1Mu_tauh")
taunuLept_11 = taunuLept_1.clone("ch1_ch1_R1_2_1El_tauh")
taunuLept_12 = taunuLept_1.clone("ch1_ch1_R1_2_1Mu_tauh")
# R2, tauh
taunuLept_13 = taunuLept_1.clone("ch1_ch1_R2_0_1El_tauh")
taunuLept_14 = taunuLept_1.clone("ch1_ch1_R2_0_1Mu_tauh")
taunuLept_15 = taunuLept_1.clone("ch1_ch1_R2_1_1El_tauh")
taunuLept_16 = taunuLept_1.clone("ch1_ch1_R2_1_1Mu_tauh")
taunuLept_17 = taunuLept_1.clone("ch1_ch1_R2_2_1El_tauh")
taunuLept_18 = taunuLept_1.clone("ch1_ch1_R2_2_1Mu_tauh")
# R1, notauh
taunuLept_19 = taunuLept_1.clone("ch2_ch1_R1_0_1El_notauh")
taunuLept_20 = taunuLept_1.clone("ch2_ch1_R1_0_1Mu_notauh")
taunuLept_21 = taunuLept_1.clone("ch2_ch1_R1_1_1El_notauh")
taunuLept_22 = taunuLept_1.clone("ch2_ch1_R1_1_1Mu_notauh")
# R2, notauh
taunuLept_23 = taunuLept_1.clone("ch2_ch1_R2_0_1El_notauh")
taunuLept_24 = taunuLept_1.clone("ch2_ch1_R2_0_1Mu_notauh")
taunuLept_25 = taunuLept_1.clone("ch2_ch1_R2_1_1El_notauh")
taunuLept_26 = taunuLept_1.clone("ch2_ch1_R2_1_1Mu_notauh")
# R3, notauh
taunuLept_27 = taunuLept_1.clone("ch2_ch1_R3_0_1El_notauh")
taunuLept_28 = taunuLept_1.clone("ch2_ch1_R3_0_1Mu_notauh")
taunuLept_29 = taunuLept_1.clone("ch2_ch1_R3_1_1El_notauh")
taunuLept_30 = taunuLept_1.clone("ch2_ch1_R3_1_1Mu_notauh")
# R4, notauh
taunuLept_31 = taunuLept_1.clone("ch2_ch1_R4_0_1El_notauh")
taunuLept_32 = taunuLept_1.clone("ch2_ch1_R4_0_1Mu_notauh")
taunuLept_33 = taunuLept_1.clone("ch2_ch1_R4_1_1El_notauh")
taunuLept_34 = taunuLept_1.clone("ch2_ch1_R4_1_1Mu_notauh")

#categories += [taunuLept_1,taunuLept_2,taunuLept_3,taunuLept_4,taunuLept_5,taunuLept_6,taunuLept_7,taunuLept_8,taunuLept_9,taunuLept_10,taunuLept_11,taunuLept_12,taunuLept_13,taunuLept_14,taunuLept_15,taunuLept_16,taunuLept_17,taunuLept_18,taunuLept_19,taunuLept_20,taunuLept_21,taunuLept_22,taunuLept_23,taunuLept_24,taunuLept_25,taunuLept_26,taunuLept_27,taunuLept_28,taunuLept_29,taunuLept_30,taunuLept_31,taunuLept_32,taunuLept_33,taunuLept_34]

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
