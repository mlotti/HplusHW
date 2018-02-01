#/usr/bin/env python

# Trigger Efficiency PlotAux

#================================================================================================
# Imports
#================================================================================================
import os
import sys
from optparse import OptionParser
import getpass
import socket
import math

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux

import ROOT
import array

#================================================================================================
# Variable Definition
#================================================================================================

html = []

# Name shortcuts for saving name
trg = {
    "HLT_PFHT400_SixJet30_DoubleBTagCSV_p056" : "2BTag",
    "HLT_PFHT450_SixJet40_BTagCSV_p056"       : "1BTag"
    }

#================================================================================================
# Auxiliary Function Definition
#================================================================================================

def HasKeys(keyList, **kwargs):
    for key in keyList:
        if key not in kwargs:
            raise Exception("Could not find the keyword \"%s\" in kwargs" % (key) )
    return
# ------------------------------------------------------------------------------------------------
def fit(name, plot, graph, min, max):
    '''
    '''
    function = ROOT.TF1("fit"+name, "0.5*[0]*(1+TMath::Erf( (sqrt(x)-sqrt([1]))/(sqrt(2)*[2]) ))", min, max);
    function.SetParameters(1., 50., 1.);
    function.SetParLimits(0, 0.0, 1.0);
    fitResult = graph.Fit(function, "NRSE+EX0");
    aux.copyStyle(graph, function)
    plot.appendPlotObject(function)
# ------------------------------------------------------------------------------------------------
def Fit_Richards(xMin, xMax, p, histogram, par):
    '''

    Parameters:                                                     Limits:

    - p0 : Lower Asymptote                                        0  < p0 < 1
    - p1 : Upper Asymptote                                        0  < p1 < 1
    - p2 : Affects near which asymptote maximum growth occurs          p2 > 0
    - p3 : Growth rate
    - p4 : Inflection point                                       

    '''
    
    if len(par) == 0:
        return
    
    # Function 
    Richards = ROOT.TF1("Richards", "[0] + ( ([1]-[0]) / (1.0 +(   (2.0**[2]-1.0)* exp(-[3]*(x-[4]))))**(1.0/[2]))", xMin, xMax)
    
    # Limits
    Richards.SetParLimits(0, 0.0, 1.0)
    Richards.SetParLimits(1, 0.0, 1.0)
    Richards.SetParLimits(2, 0.0, 1.0)
    
    Richards.SetParName(0, "p0")
    Richards.SetParName(1, "p1")
    Richards.SetParName(2, "p2")
    Richards.SetParName(3, "p3")
    Richards.SetParName(4, "p4")
    
    p0 = par[0]
    p1 = par[1]
    p2 = par[2]
    p3 = par[3]
    p4 = par[4]
    
    Richards.SetParameter(0, p0)
    Richards.SetParameter(1, p1)
    Richards.SetParameter(2, p2)
    Richards.SetParameter(3, p3)
    Richards.SetParameter(4, p4)
    
    fitResult = histogram.Fit(Richards, "Richards")
    
    ROOT.gStyle.SetOptFit()
    #ROOT.gStyle.SetStatX(0.40)
    #ROOT.gStyle.SetStatY(0.40)

    print "-------------------------------------------------------------"
    chi2 = Richards.GetChisquare()
    ndf  = Richards.GetNDF()
    p0   = Richards.GetParameter(0)
    p1   = Richards.GetParameter(1)
    p2   = Richards.GetParameter(2)
    p3   = Richards.GetParameter(3)
    p4   = Richards.GetParameter(4)
    print " Fit Results: "
    print " x^{2} =", chi2
    print " ndf   =", ndf
    print " p0    =", p0
    print " p1    =", p1
    print " p2    =", p2
    print " p3    =", p3
    print " p4    =", p4
    print "-------------------------------------------------------------"
    
    aux.copyStyle(histogram, Richards)
    p.appendPlotObject(Richards)
    
    return
# --------------------------------------------------------------------------------------
'''
def GetDatasetsFromDir(mcrab, opts, **kwargs):
    
    HasKeys(["dataEra", "searchMode", "analysis", "optMode"], **kwargs)
    dataEra    = kwargs.get("dataEra")
    searchMode = kwargs.get("searchMode")
    analysis   = kwargs.get("analysis")
    optMode    = kwargs.get("optMode")
    
    if opts.includeTasks != "":
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, includeOnlyTasks=opts.includeTasks, optimizationMode=optMode)
    elif opts.excludeTasks != "":
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, excludeTasks=opts.excludeTasks, optimizationMode=optMode)
        
    else:
        datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)
        
    # Inform user of datasets retrieved                                                
    Verbose("Got the following datasets from multicrab dir \"%s\"" % mcrab)
    for d in datasets.getAllDatasets():
        Verbose( "\t", d.getName(), False)
    return datasets

'''
# ----------------------------------------------------------------------------------------

def GetSpecificDatasetsFromDir(mcrab, opts, RunEra, samples, **kwargs):
    '''
    
    '''
    HasKeys(["dataEra", "searchMode", "analysis", "optMode"], **kwargs)
    dataEra    = kwargs.get("dataEra")
    searchMode = kwargs.get("searchMode")
    analysis   = kwargs.get("analysis")
    optMode    = kwargs.get("optMode")
    
    datasets = dataset.getDatasetsFromMulticrabDirs([mcrab],
                                                    dataEra          = dataEra,
                                                    searchMode       = searchMode,
                                                    analysisName     = analysis+"_"+RunEra,
                                                    includeOnlyTasks = samples,
                                                    optimizationMode = optMode
                                                    )
    return datasets
# --------------------------------------------------------------------------------------
def getEfficiency(datasetsMgr, datasets, numerator="Numerator",denominator="Denominator", **kwargs):
    '''
    TEfficiency method:

    See https://root.cern.ch/doc/master/classTEfficiency.html
    
    
    '''
    HasKeys(["verbose"], **kwargs)
    verbose = True #kwargs.get("verbose")

    lumi = GetLumi(datasetsMgr)

    # Select Statistic Options
    statOption = ROOT.TEfficiency.kFCP
    '''
    statOption = ROOT.TEfficiency.kFCP      # Clopper-Pearson
    statOption = ROOT.TEfficiency.kFNormal  # Normal Approximation
    statOption = ROOT.TEfficiency.kFWilson  # Wilson
    statOption = ROOT.TEfficiency.kFAC      # Agresti-Coull
    statOption = ROOT.TEfficiency.kFFC      # Feldman-Cousins
    statOption = ROOT.TEfficiency.kBBJeffrey # Jeffrey
    statOption = ROOT.TEfficiency.kBBUniform # Uniform Prior
    statOption = ROOT.TEfficiency.kBBayesian # Custom Prior
    '''
    
    print "getEfficiency function"

    first  = True
    
    teff   = ROOT.TEfficiency()
    #    teff.SetStatisticOption(statOption)
    
    print "Loop over Datasets"
    for dataset in datasets:
        print "Datasets"

    #datasets.normalizeMCByLuminosity()
    for dataset in datasets:
        

        num = dataset.getDatasetRootHisto(numerator)
        den = dataset.getDatasetRootHisto(denominator)
        if dataset.isMC():
            num.normalizeToLuminosity(lumi)
            den.normalizeToLuminosity(lumi) 
        #num.normalizeMCByLuminosity() 
        #den.normalizeMCByLuminosity() 
        
        # Get Numerator and Denominator
        n = num.getHistogram()
        d = den.getHistogram()
        
        #tn = None
        #td = None
        #n.normalizeMCByLuminosity()
        #d.normalizeMCByLuminosity()

        #n = dataset.getDatasetRootHisto(numerator).getHistogram()
        #d = dataset.getDatasetRootHisto(denominator).getHistogram()
       
        if d.GetEntries() == 0 or n.GetEntries() == 0:
            print "Denominator Or Numerator has no entries"
            continue
        
        # Check Negatives
        CheckNegatives(n, d, True)
        
        # Remove Negatives
        RemoveNegatives(n)
        #RemoveNegatives(d)
       
        NumeratorBins   = n.GetNbinsX()
        DenominatorBins = d.GetNbinsX()


        # Sanity Check
        if (NumeratorBins != DenominatorBins) :
            raise Exception("Numerator and Denominator Bins are NOT equal!")
        
        nBins = d.GetNbinsX()
        xMin  = d.GetXaxis().GetXmin()
        xMax  = d.GetXaxis().GetXmax()
        
        print("NoProblem till here asdasd...")
        
        # ----------------------------------------------------------------------------------------- # 
        #      Ugly hack to ignore EMPTY (in the wanted range) histograms with overflows/underflows
        # ----------------------------------------------------------------------------------------- #
        
        print "\n"
        print "=========== getEfficiency:"
        print "Dataset             = ", dataset.getName()
        
        print "Numerator  :", n.GetName(), "   entries=", n.GetEntries(), " Bins=", n.GetNbinsX(), " Low edge=", n.GetBinLowEdge(1)
        print "Denominator:", d.GetName(), "   entries=", d.GetEntries(), " Bins=", d.GetNbinsX(), " Low edge=", d.GetBinLowEdge(1)
        print "\n"
        print ">>>>>>  Sanity Check:  <<<<<<"
        print "Numerator Mean       = ", n.GetMean()
        print "Numerator RMS        = ", n.GetRMS()
        print "Numerator Integral   = ", n.Integral(1, nBins)
        print "Denominator Mean     = ", d.GetMean()
        print "Denominator RMS      = ", d.GetRMS()
        print "Denominator Integral = ", d.Integral(1, nBins)
        
        
        if (n.GetMean() == 0 or d.GetMean() == 0): continue
        if (n.GetRMS()  == 0 or d.GetRMS()  == 0): continue
        if (n.Integral(1,nBins) == 0 or d.Integral(1,nBins) == 0): continue

        print "Passed the sanity check"
        
        eff = ROOT.TEfficiency(n, d)
        eff.SetStatisticOption(statOption)
        
        #        if "TT" in dataset.getName():
        #    print " "
        #    print " TT sample"
        for iBin in range(1, nBins+1):
            print iBin, "x=", n.GetBinLowEdge(iBin), " Num=", n.GetBinContent(iBin),  " Den=", d.GetBinContent(iBin)," Eff=", eff.GetEfficiency(iBin)
        # "Contrib. =", d.GetBinContent(iBin)/d.Integral(1, nBins)*100.0, "Contrib. = ", n.GetBinContent(iBin)/n.Integral(1, nBins)*100.0,
            
        '''
        #if (verbose):
        print "\n"
        for iBin in range(1,nBins+1):
        print iBin, "x=", n.GetBinLowEdge(iBin), " Numerator=", n.GetBinContent(iBin), " Denominator=", d.GetBinContent(iBin), " Efficiency=", eff.GetEfficiency(iBin), " Weight=", eff.GetWeight()
        print "\n"
        '''
        
        weight = 1
        if dataset.isMC():
            weight = dataset.getCrossSection()
        eff.SetWeight(weight)
        #print "dataset=", dataset.getName(), "has weight=", weight
        #print " Efficiency plot has weight=", eff.GetWeight()
        
        if first:
            teff  = eff
            first = False
            if dataset.isData():
                tn = n
                td = d
        else:
            teff.Add(eff)
            
            #print " "
            #print "Adding eff to TEfficiency="
            #for iBin in range(1, nBins+1):
            #    print iBin, "x=", n.GetBinLowEdge(iBin), " Numerator=", n.GetBinContent(iBin), "Contrib. = ", n.GetBinContent(iBin)/n.Integral(1, nBins)*100.0, " Denominator=", d.GetBinContent(iBin), "Contrib. =", d.GetBinContent(iBin)/d.Integral(1, nBins)*100.0, " Efficiency=", teff.GetEfficiency(iBin), " Weight=", teff.GetWeight()
            
            if dataset.isData():
                tn.Add(n)
                td.Add(d)
                
        if dataset.isData():
            teff = ROOT.TEfficiency(tn, td)
            teff.SetStatisticOption(statOption)
        
            '''
            print " ------------------------- Final Data Plot ------------------------- "
            print "Integral = ", tn.Integral(1, nBins)
            print "Numerator:"
            for iBin in range(1, nBins+1):
            print iBin, "x=", tn.GetBinLowEdge(iBin), " Bin Content = ", tn.GetBinContent(iBin), " Percentage=", tn.GetBinContent(iBin)/tn.Integral(1, nBins)*100.0
            
            print "Denominator:  "
            print "Integral = ", td.Integral(1,nBins)
            for iBin in range(1, nBins+1):
            print iBin, "x=", td.GetBinLowEdge(iBin), " Bin Content = ", td.GetBinContent(iBin), " Percentage=", td.GetBinContent(iBin)/td.Integral(1, nBins)*100
            print "-------------------------------------------------------------------- "
            '''
        
    print " -----------------> Final tEff"
    for iBin in range(1,nBins+1):
        print iBin, "x=", n.GetBinLowEdge(iBin)," Efficiency=", teff.GetEfficiency(iBin), " Weight = ", teff.GetWeight()
        
    return convert2TGraph(teff)

##ATHER
def getEfficiency2D(datasetsMgr, datasets, numerator="Numerator",denominator="Denominator", **kwargs):
    '''                                                                                                                                                               
    TEfficiency method:                                                                                                                                               
                                                                                                                                                                      
    See https://root.cern.ch/doc/master/classTEfficiency.html                                                                                                         
    
    
    '''
    HasKeys(["verbose"], **kwargs)
    verbose = True #kwargs.get("verbose")                                                                                                                             
    
    lumi = GetLumi(datasetsMgr)

    # Select Statistic Options                                                                                                                                        
    statOption = ROOT.TEfficiency.kFCP
    '''                                                                                                                                                               
    statOption = ROOT.TEfficiency.kFCP      # Clopper-Pearson                                                                                                         
    statOption = ROOT.TEfficiency.kFNormal  # Normal Approximation                                                                                                    
    statOption = ROOT.TEfficiency.kFWilson  # Wilson                                                                                                                  
    statOption = ROOT.TEfficiency.kFAC      # Agresti-Coull                                                                                                           
    statOption = ROOT.TEfficiency.kFFC      # Feldman-Cousins                                                                                                         
    statOption = ROOT.TEfficiency.kBBJeffrey # Jeffrey                                                                                                                
    statOption = ROOT.TEfficiency.kBBUniform # Uniform Prior                                                                                                          
    statOption = ROOT.TEfficiency.kBBayesian # Custom Prior                                                                                                           
    '''

    print "getEfficiency function"
    first  = True
    teff   = ROOT.TEfficiency()
    #    teff.SetStatisticOption(statOption)                                                                                                                          
    print "Loop over Datasets"
    for dataset in datasets:
        print "Datasets"

    #datasets.normalizeMCByLuminosity()                                                                                                                               
    for dataset in datasets:
        num = dataset.getDatasetRootHisto(numerator)
        den = dataset.getDatasetRootHisto(denominator)
        if dataset.isMC():
            num.normalizeToLuminosity(lumi)
            den.normalizeToLuminosity(lumi)
        #num.normalizeMCByLuminosity()                                                                                                                                
        #den.normalizeMCByLuminosity()                                                                                                                                

        # Get Numerator and Denominator                                                                                                                               
        n = num.getHistogram()
        d = den.getHistogram()

        #tn = None                                                                                                                                                    
        #td = None                                                                                                                                                    
        #n.normalizeMCByLuminosity()                                                                                                                                  
        #d.normalizeMCByLuminosity()                                                                                                                                  

        #n = dataset.getDatasetRootHisto(numerator).getHistogram()                                                                                                    
        #d = dataset.getDatasetRootHisto(denominator).getHistogram()                                                                                                  

        if d.GetEntries() == 0 or n.GetEntries() == 0:
            print "Denominator Or Numerator has no entries"
            continue

        # Check Negatives                                                                                                                                             
        CheckNegatives(n, d, True)
        # Remove Negatives                                                                                                                                            
        RemoveNegatives(n)
        #RemoveNegatives(d)                                                                                                                                           

        NumeratorBins   = n.GetNbinsX()
        DenominatorBins = d.GetNbinsX()

        # Sanity Check                                                                                                                                                
        if (NumeratorBins != DenominatorBins) :
            raise Exception("Numerator and Denominator Bins are NOT equal!")
        nBinsX = d.GetNbinsX()
        xMin  = d.GetXaxis().GetXmin()
        xMax  = d.GetXaxis().GetXmax()

        nBinsY = d.GetNbinsY()
        #yMin  = d.GetYaxis().GetYmin()
        #yMax  = d.GetYaxis().GetYmax()
        print("NoProblem till here asdasd...")

        # ----------------------------------------------------------------------------------------- #                                                                 
        #      Ugly hack to ignore EMPTY (in the wanted range) histograms with overflows/underflows                                                                   
        # ----------------------------------------------------------------------------------------- #                                                                 

        print "\n"
        print "=========== getEfficiency:"
        print "Dataset             = ", dataset.getName()

        #print "Numerator  :", n.GetName(), "   entries=", n.GetEntries(), " Bins=", n.GetNbinsX(), " Low edge=", n.GetBinLowEdge(1)
        #print "Denominator:", d.GetName(), "   entries=", d.GetEntries(), " Bins=", d.GetNbinsX(), " Low edge=", d.GetBinLowEdge(1)
        print "\n"
        print ">>>>>>  Sanity Check:  <<<<<<"
        print "Numerator Mean       = ", n.GetMean()
        print "Numerator RMS        = ", n.GetRMS()
        print "Numerator Integral   = ", n.Integral()
        print "Denominator Mean     = ", d.GetMean()
        print "Denominator RMS      = ", d.GetRMS()
        print "Denominator Integral = ", d.Integral()

        if (n.GetMean() == 0 or d.GetMean() == 0): continue
        if (n.GetRMS()  == 0 or d.GetRMS()  == 0): continue
        if (n.Integral() == 0 or d.Integral() == 0): continue

        print "Passed the sanity check"

        eff = ROOT.TEfficiency(n, d)
        eff.SetStatisticOption(statOption)

        #        if "TT" in dataset.getName():                                                                                                                        
        #    print " "                                                                                                                                                
        #    print " TT sample"                                                                                                                                       
        #for iBin in range(1, nBins+1):
        #    print iBin, "x=", n.GetBinLowEdge(iBin), " Num=", n.GetBinContent(iBin),  " Den=", d.GetBinContent(iBin)," Eff=", eff.GetEfficiency(iBin)
        # "Contrib. =", d.GetBinContent(iBin)/d.Integral(1, nBins)*100.0, "Contrib. = ", n.GetBinContent(iBin)/n.Integral(1, nBins)*100.0,                            

        '''                                                                                                                                                           
        #if (verbose):                                                                                                                                                
        print "\n"                                                                                                                                                    
        for iBin in range(1,nBins+1):                                                                                                                                 
        #print iBin, "x=", n.GetBinLowEdge(iBin), " Numerator=", n.GetBinContent(iBin), " Denominator=", d.GetBinContent(iBin), " Efficiency=", eff.GetEfficiency(iBin\
), " Weight=", eff.GetWeight()                                                                                                                                        
        print "\n"                                                                                                                                                    
        '''

        weight = 1
        if dataset.isMC():
            weight = dataset.getCrossSection()
        eff.SetWeight(weight)
        #print "dataset=", dataset.getName(), "has weight=", weight                                                                                                   
        #print " Efficiency plot has weight=", eff.GetWeight()

        if first:
            teff  = eff
            first = False
            if dataset.isData():
                tn = n
                td = d
        else:
            teff.Add(eff)

            #print " "                                                                                                                                                
            #print "Adding eff to TEfficiency="                                                                                                                       
            #for iBin in range(1, nBins+1):                                                                                                                           
            #    print iBin, "x=", n.GetBinLowEdge(iBin), " Numerator=", n.GetBinContent(iBin), "Contrib. = ", n.GetBinContent(iBin)/n.Integral(1, nBins)*100.0, " Denominator=", d.GetBinContent(iBin), "Contrib. =", d.GetBinContent(iBin)/d.Integral(1, nBins)*100.0, " Efficiency=", teff.GetEfficiency(iBin), " Weight=", teff.GetWeight()                                                                                                                                                                 

            if dataset.isData():
                tn.Add(n)
                td.Add(d)
        
        if dataset.isData():
            teff = ROOT.TEfficiency(tn, td)
            teff.SetStatisticOption(statOption)

            '''                                                                                                                                                       
            print " ------------------------- Final Data Plot ------------------------- "                                                                             
            print "Integral = ", tn.Integral(1, nBins)                                                                                                                
            print "Numerator:"                                                                                                                                        
            for iBin in range(1, nBins+1):                                                                                                                            
            print iBin, "x=", tn.GetBinLowEdge(iBin), " Bin Content = ", tn.GetBinContent(iBin), " Percentage=", tn.GetBinContent(iBin)/tn.Integral(1, nBins)*100.0   
                                                                                                                                                                      
            print "Denominator:  "                                                                                                                                    
            print "Integral = ", td.Integral(1,nBins)                                                                                                                 
            for iBin in range(1, nBins+1):                                                                                                                            
            print iBin, "x=", td.GetBinLowEdge(iBin), " Bin Content = ", td.GetBinContent(iBin), " Percentage=", td.GetBinContent(iBin)/td.Integral(1, nBins)*100     
            print "-------------------------------------------------------------------- "                                                                             
            '''
            
    print " -----------------> Final tEff"
    #for iBin in range(1,nBins+1):
    #    print iBin, "x=", n.GetBinLowEdge(iBin)," Efficiency=", teff.GetEfficiency(iBin), " Weight = ", teff.GetWeight()

    return teff



##ATHER


# ------------------------------------------------------------------------------------------------------
def SetLogAndGrid(p, **kwargs):
    '''
    '''
    HasKeys(["ratio", "logX", "logY", "gridX", "gridY"], **kwargs)
    ratio = kwargs.get("ratio")
    logX  = kwargs.get("logX")
    logY  = kwargs.get("logY")
    logZ  = kwargs.get("logZ")
    gridX = kwargs.get("gridX")
    gridY = kwargs.get("gridY")
    
    if ratio:
        p.getPad1().SetLogx(logX)
        p.getPad1().SetLogy(logY)
        #
        p.getPad2().SetLogx(logX)
        p.getPad2().SetLogy(logY)
        #
        p.getPad1().SetGridx(gridX)
        p.getPad1().SetGridy(gridY)
        #
        p.getPad2().SetGridx(gridX)
        p.getPad2().SetGridy(gridY)
    else:
        p.getPad().SetLogx(logX)
        p.getPad().SetLogy(logY)
        if logZ != None:
            p.getPad().SetLogz(logZ)
        p.getPad().SetGridx(gridX)
        p.getPad().SetGridy(gridY)
    return
# --------------------------------------------------------------------------------------------------
def CheckNegatives(n, d, verbose=False):
    '''
    '''
    table    = []
    txtAlign = "{:<5} {:>20} {:>20}"
    hLine    = "="*50
    table.append(hLine)
    table.append(txtAlign.format("Bin #", "Numerator (8f)", "Denominator (8f)"))
    table.append(hLine)
    
    # For-loop: All bins in x-axis
    for i in range(1, n.GetNbinsX()+1):
        nbin = n.GetBinContent(i)
        dbin = d.GetBinContent(i)

        table.append(txtAlign.format(i, "%0.8f" % (nbin), "%0.8f" % (dbin) ))
        
        # Numerator > Denominator
        if nbin > dbin:
            n.SetBinContent(i,dbin)

        # Numerator < 0 
        if nbin < 0:
            n.SetBinContent(i,0)

        # Denominator < 0
        if dbin < 0:
            n.SetBinContent(i,0)
            d.SetBinContent(i,0)

    #if verbose:                                                                                                                               
    #    for r in table:                                                                                                                       
    #        print r                                                                                                                           
    return

# -----------------------------------------------------------------------------------------
def RemoveNegatives(histo):
    '''
    '''
    for binX in range(histo.GetNbinsX()+1):
        if histo.GetBinContent(binX) < 0:
            histo.SetBinContent(binX, 0.0)
    return
# -----------------------------------------------------------------------------------------
def convert2TGraph(tefficiency):
    '''
    '''
    x     = []
    y     = []
    xerrl = []
    xerrh = []
    yerrl = []
    yerrh = []
    
    h = tefficiency.GetCopyTotalHisto()
    n = h.GetNbinsX()

    xMin= h.GetXaxis().GetXmin()
    xMax= h.GetXaxis().GetXmax()

    for i in range(1,n+1):
        #print "x = ", h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i), "      y = ",tefficiency.GetEfficiency(i)
        x.append(h.GetBinLowEdge(i)+0.5*h.GetBinWidth(i))
        xerrl.append(0.5*h.GetBinWidth(i))
        xerrh.append(0.5*h.GetBinWidth(i))
        y.append(tefficiency.GetEfficiency(i))
        yerrl.append(tefficiency.GetEfficiencyErrorLow(i))
        # ugly hack to prevent error going above 1 
        
        errUp = tefficiency.GetEfficiencyErrorUp(i)
        if y[-1] == 1.0:
            errUp = 0
        yerrh.append(errUp)

        tgraph= ROOT.TGraphAsymmErrors(n,array.array("d",x),
                                       array.array("d",y),
                                       array.array("d",xerrl),
                                       array.array("d",xerrh),
                                       array.array("d",yerrl),
                                       array.array("d",yerrh))
    return tgraph
# ----------------------------------------------------------------------------------------------
def GetSavePath(**kwargs):
    '''
    '''
    HasKeys(["savePath", "analysis", "verbose"], **kwargs)
    savePath = kwargs.get("savePath")
    analysis = kwargs.get("analysis")
    verbose  = kwargs.get("verbose")

    Verbose("Constructing path where plots will be saved", verbose)
    if savePath != None:
        return savePath
    user    = getpass.getuser()
    initial = getpass.getuser()[0]
    if "lxplus" in socket.gethostname():
        savePath = "/afs/cern.ch/user/%s/%s/public/html/%s/" % (initial, user, analysis)
    elif "fnal.gov" in socket.gethostname():#publicweb
        #savePath = "/publicweb/m/mather/JetTriggerSF/"
        #savePath = "/uscms_data/d3/mather/scratch0/CMSSW_8_0_27/src/HiggsAnalysis/NtupleAnalysis/src/JetTriggersSF/plots/" #% (initial, user, analysis)
        savePath = "../plots/"  
    else:
        savePath = "/Users/%s/Desktop/Plots/" % (user)
    return savePath
# ----------------------------------------------------------------------------------------------
def GetSaveName(savePathNew, hName, **kwargs):
    '''
    '''
    HasKeys(["savePath", "verbose"], **kwargs)
    verbose      = kwargs.get("verbose")
    cutDirection = kwargs.get("cutDirection")

    Verbose("Constructing name of plot to  be saved", verbose)
    forbidden   = ["/"]
    replacement = "_"
    for f in forbidden:
        if f in hName:
            Print("Replacing forbidden character \"%s\" with \"%s\" in saveName  \"%s\"" % (f, replacement, hName))
            hName = hName.replace(f, replacement)

    if cutDirection == None:
        saveName = os.path.join(savePathNew, hName)
    elif cutDirection == ">":
        saveName = os.path.join(savePathNew, hName + "_GreaterThan")
    else:
        saveName = os.path.join(savePathNew, hName + "_LessThan")

    return saveName
# ------------------------------------------------------------------------------------------------------
def GetSavePathAndName(hName, **kwargs):
    '''
    '''
    HasKeys(["verbose"], **kwargs)
    verbose  = kwargs.get("verbose")

    Verbose("Getting save path and name", verbose)
    savePathNew = GetSavePath(**kwargs)
    saveName    = GetSaveName(savePathNew, hName, **kwargs)
    return savePathNew, saveName
# -----------------------------------------------------------------------------------------------------
def SaveAs(p, savePath, saveName, saveFormats, verbose=True):
    '''
    '''
    Verbose("Saving plots in %s format(s)" % (len(saveFormats)), True)

    if verbose:
        Print("Saving plots in %s format(s)" % (len(saveFormats)), True)

    # For-loop: All formats to save file
    for ext in saveFormats:        
        sName = saveName + ext

        # Change print name if saved under html
        if "html" in sName:
            user    = getpass.getuser()
            initial = getpass.getuser()[0]
            sName   = sName.replace("/afs/cern.ch/user/%s/" % (initial), "http://cmsdoc.cern.ch/~")
            sName   = sName.replace("%s/public/html/" % (user), "%s/" % (user))
         
        if "publicweb" in sName:
            user    = getpass.getuser()
            initial = getpass.getuser()[0]
            sName   = sName.replace("/publicweb/%s/" % (initial), "http://home.fnal.gov/~")
            
        # Print save name
        print "\t", sName
        html.append(sName)
        
        # Check if dir exists
        #if not os.path.exists(savePath):
        #    os.mkdir(savePath)

        # Save the plots
        p.saveAs(saveName, saveFormats)
    return
# ------------------------------------------------------------------------------------------------------
def Verbose(msg, printHeader=True, verbose=False):
    if not verbose:
        return
    Print(msg, printHeader)
    return
# ------------------------------------------------------------------------------------------------------
def Print(msg, printHeader=False):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader==True:
        print "=== ", fName
        print "\t", msg
    else:
        print "\t", msg
    return

# ------------------------------------------------------------------------------------
def Print_html():
    '''
    Function to print all the html links 
    '''
    if len(html) == 0:
        return

    print "\n"
    Print("Find all the plots at the links below:")
    print "\n"

    for i, plot in enumerate(html):
        print i+1, " ", plot
    
    return
# ------------------------------------------------------------------------------------
def NormalizeRootHisto(datasetsMgr, rootHisto, isMC, normalizeTo):

    '''
    # \li \a normalizeToOne           Normalize the histograms to one (True/False)
    # \li \a normalizeByCrossSection  Normalize the histograms by the dataset cross sections (True/False)
    # \li \a normalizeToLuminosity    Normalize the histograms to a given luminosity (number)
    '''
    if normalizeTo == "One":
        rootHisto.normalizeToOne()
    elif normalizeTo == "XSection":
        if isMC:
            rootHisto.normalizeByCrossSection()
    elif normalizeTo == "Luminosity":
        intLumi = GetLumi(datasetsMgr)
        if not rootHisto.isData():
            rootHisto.normalizeToLuminosity(intLumi)
    else:
        IsValidNorm(normalizeTo)
    return
# --------------------------------------------------------------------------------------------
def GetLumi(datasetsMgr):
    '''
    '''
    Verbose("GetLumi()", True)

    intLumi  = -1
    jsonFile = "lumi.json"

    if len(datasetsMgr.getDataDatasets()) == 0:
        return intLumi

    # Either get luminosity from merged data, or load luminosity from JSON file (before merging datasets)
    if "Data" in datasetsMgr.getAllDatasetNames():
        Verbose("Loading luminosities from merge data", False)
        intLumi = datasetsMgr.getDataset("Data").getLuminosity()
    else:
        Verbose("Loading luminosities from \"%s\"" % (jsonFile), False)
        datasetsMgr.loadLuminosities(fname=jsonFile)

    # Load RUN range 
    # runRange = datasets.loadRunRange(fname="runrange.json")                                                  
        
    # For-loop: All Data datasets                                           
    for d in datasetsMgr.getDataDatasets():
        Verbose("%s, luminosity is %s pb" % (d.getName(), d.getLuminosity()), False)
        intLumi += d.getLuminosity()
    Verbose("Integrated Luminosity is %s (pb)" % (intLumi), False)
    return intLumi



    
