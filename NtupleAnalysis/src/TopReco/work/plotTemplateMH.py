#!/usr/bin/env python
'''

Usage:
./plotTemplate.py -m <pseudo_mcrab_directory>

'''

#================================================================================================
# Imports
#================================================================================================
import os
import sys
from optparse import OptionParser
import getpass
import socket

import HiggsAnalysis.NtupleAnalysis.tools.dataset as dataset
import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.styles as styles
import HiggsAnalysis.NtupleAnalysis.tools.plots as plots
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms
import HiggsAnalysis.NtupleAnalysis.tools.aux as aux
from plotAuxMH import *

import ROOT

#================================================================================================
# Variable Definition
#================================================================================================
kwargs = {
    "analysis"       : "HplusHadronic",
    "savePath"       : "/publicweb/s/skonstan/Plots/",
    #"savePath"       : None,
    "refDataset"     : "TT",
    #"rmDataset"      : ["ChargedHiggs_HplusTB_HplusToTB_M_300"], #["QCD"],
    "saveFormats"    : [".pdf"],
    "normalizeTo"    : "One", #One", "XSection", "Luminosity"
    "createRatio"    : False,
    "logX"           : False,
    "logY"           : False,
    "gridX"          : True,
    "gridY"          : True,
    "drawStyle"      : "F", # "P",  #"HIST9"
    "legStyle"       : "F",     # "LP", "F"
    "verbose"        : True,
    "cutValue"       : 5,
    "cutBox"         : False,
    "cutLine"        : False,
    "cutLessthan"    : False,
    "cutFillColour"  : ROOT.kAzure-4,
    "rebinX"         : 2,
}


hNames  = []

hNames.append("METoverSqrtHT")
#================================================================================================
# Main
#================================================================================================
def main():

    style    = tdrstyle.TDRStyle()

    # Set ROOT batch mode boolean
    ROOT.gROOT.SetBatch(parseOpts.batchMode)

    # Get all datasets from the mcrab dir
    datasetsMgr  = GetDatasetsFromDir(parseOpts.mcrab, kwargs.get("analysis"))
    
    # Determine Integrated Luminosity (If Data datasets present)
    intLumi = GetLumi(datasetsMgr)
    
    # Update to PU
    datasetsMgr.updateNAllEventsToPUWeighted()

    # Remove datasets
    # datasetsMgr.remove(kwargs.get("rmDataset"))
    # datasetsMgr.remove(filter(lambda name: not "QCD" in name, datasetsMgr.getAllDatasetNames()))
    # datasetsMgr.remove(filter(lambda name: "QCD" in name in name, datasetsMgr.getAllDatasetNames()))
    
    # Set custom XSections
    # d.getDataset("TT_ext3").setCrossSection(831.76)
    
    # Default merging & ordering: "Data", "QCD", "SingleTop", "Diboson"
    plots.mergeRenameReorderForDataMC(datasetsMgr) #WARNING: Merged MC histograms must be normalized to something!

    # Remove datasets (for merged names)
    datasetsMgr.remove(kwargs.get("rmDataset")) #soti

 
    
    # For-loop: All Histogram names
    for counter, hName in enumerate(hNames):
        
        # Get the save path and name
        savePath, saveName = GetSavePathAndName(hName, **kwargs)

        # Get Histos for Plotter
        refHisto, otherHistos = GetHistosForPlotter(datasetsMgr, hName, **kwargs)

        # Create a comparison plot                             
        p = plots.PlotBase([refHisto], kwargs.get("saveFormats"))
        
        p.histoMgr.forEachHisto(lambda h: h.getRootHisto().RebinX(kwargs.get("rebinX")))
    
        # Fit                                                                                                                                 
        if (hName == "h_WplusWminus_dijet_masses"):
            GaussianFit = ROOT.TF1("GaussianFit", "[0]*exp(-pow(x-[1],2)/(2*pow([2],2)))", 65, 100) #edw
            par1 = [0.07,83,20]
            GaussianFit.SetParameter(0,par1[0])
            GaussianFit.SetParameter(1,par1[1])
            GaussianFit.SetParameter(2,par1[2])

            histo = refHisto.getRootHisto()
            histo.Fit(GaussianFit,"R")
            histo.GetFunction("GaussianFit").SetLineWidth(3);
            histo.Draw()
            print("********************")
            print(GaussianFit.GetNDF())
            print(GaussianFit.GetChisquare())
            print(GaussianFit.GetChisquare()/GaussianFit.GetNDF())

            
            ROOT.gStyle.SetOptFit(1);
            sb1 = ROOT.TPaveStats()
            ROOT.gPad.Update()
            sb1 = histo.FindObject("stats")
            sb1.SetX1NDC(0.65)
            sb1.SetX2NDC(0.92)
            sb1.SetY1NDC(0.65)
            sb1.SetY2NDC(0.8)
            sb1.SetLineColor(2)


        if (hName == "h_TopANDAssoTop_trijet_masses"):
            GaussianFit = ROOT.TF1("GaussianFit", "[0]*exp(-pow(x-[1],2)/(2*pow([2],2)))", 140, 200)
            par1 = [0.1,172,16.7]
            GaussianFit.SetParameter(0,par1[0])
            GaussianFit.SetParameter(1,par1[1])
            GaussianFit.SetParameter(2,par1[2])

            histo = refHisto.getRootHisto()
            histo.Fit(GaussianFit,"R")
            histo.GetFunction("GaussianFit").SetLineColor(9);
            histo.Draw()
            print("********************")
            print(GaussianFit.GetNDF())
            print(GaussianFit.GetChisquare())
            print(GaussianFit.GetChisquare()/GaussianFit.GetNDF())

        if (hName == "h_TopANDAssoTop_trijet_DMass"):
            GaussianFit = ROOT.TF1("GaussianFit", "[0]*exp(-pow(x-[1],2)/(2*pow([2],2)))", -50, 50)
            par1 = [0.03,0,50]
            GaussianFit.SetParameter(0,par1[0])
            GaussianFit.SetParameter(1,par1[1])
            GaussianFit.SetParameter(2,par1[2])

            histo = refHisto.getRootHisto()
            histo.Fit(GaussianFit,"R")
            histo.GetFunction("GaussianFit").SetLineWidth(3);
            histo.Draw()
            print("********************")
            print(GaussianFit.GetNDF())
            print(GaussianFit.GetChisquare())
            print(GaussianFit.GetChisquare()/GaussianFit.GetNDF())
            
            ROOT.gStyle.SetOptFit(1);
            sb1 = ROOT.TPaveStats()
            ROOT.gPad.Update()
            sb1 = histo.FindObject("stats")
            sb1.SetX1NDC(0.65)
            sb1.SetX2NDC(0.92)
            sb1.SetY1NDC(0.65)
            sb1.SetY2NDC(0.8)
            sb1.SetLineColor(2)


        if (hName == "h_GenPS1_Higgs_Mass"):
            GaussianFit = ROOT.TF1("GaussianFit", "[0]*exp(-pow(x-[1],2)/(2*pow([2],2)))", 290, 310) #edw
            par1 = [0.03,500,50]
            GaussianFit.SetParameter(0,par1[0])
            GaussianFit.SetParameter(1,par1[1])
            GaussianFit.SetParameter(2,par1[2])

            histo = refHisto.getRootHisto()
            histo.Fit(GaussianFit,"R")
            histo.Draw()
            print("********************")
            #print(GaussianFit.GetNDF())
            #print(GaussianFit.GetChisquare())
            #print(GaussianFit.GetChisquare()/GaussianFit.GetNDF())

            ROOT.gStyle.SetOptFit(1);
            sb1 = ROOT.TPaveStats()
            ROOT.gPad.Update()
            sb1 = histo.FindObject("stats")
            sb1.SetX1NDC(0.65)
            sb1.SetX2NDC(0.92)
            sb1.SetY1NDC(0.65)
            sb1.SetY2NDC(0.8)
            sb1.SetLineColor(2)
            #edw

            
        
        # Remove negative contributions
        #RemoveNegativeBins(datasetsMgr, hName, p)

        # Create a frame
        if kwargs.get("logY"):
            opts = {"ymin": 1e-5, "ymaxfactor": 10}
        else:
            opts = {"ymin": 0.0, "ymaxfactor": 1.2}
        ratioOpts = {"ymin": 0.0, "ymax": 2.0}
        p.createFrame(saveName, opts=opts)
        
        # Customise Legend
        moveLegend = {"dx": -0.1, "dy": 0.0, "dh": -0.2}
        p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
        #p.removeLegend()

        # Customise frame
        p.getFrame().GetYaxis().SetTitle( getTitleY(refHisto, **kwargs) )
        #p.setEnergy("13")
        if kwargs.get("createRatio"):
            p.getFrame2().GetYaxis().SetTitle("Ratio")
            p.getFrame2().GetYaxis().SetTitleOffset(1.6)

        if "masses" in hName:
            p.getFrame().GetXaxis().SetTitle("Mass (GeV/c^{2})")
        elif "DMass" in hName:
            p.getFrame().GetXaxis().SetTitle("#Delta Mass (GeV/c^{2})")

        #if (hName == "h_diJetBJet_Mass"):
        #    _kwargs = {"lessThan": True}
        #    p.addCutBoxAndLine(cutValue=173.24, fillColor=ROOT.kRed, box=False, line=True, **_kwargs)

            '''
        if (hName == "h_WplusWminus_dijet_masses"):
            p.getFrame().GetXaxis().SetRangeUser(0,200)
        if (hName == "h_TopANDAssoTop_trijet_masses"):
            p.getFrame().GetXaxis().SetRangeUser(50,300)
        if (hName == "h_TopANDAssoTop_trijet_DMass"):
            p.getFrame().GetXaxis().SetRangeUser(-100,100)

        p.getFrame().GetXaxis().SetRangeUser(200,400)
        '''

        if (hName == "TriJetMass_0extrab_Before" or 
            hName == "TriJetMass_1extrab_Before" or
            hName == "TriJetMass_2extrab_Before"     ):
            p.getFrame().GetXaxis().SetRangeUser(0,500);
            p.getFrame().GetYaxis().SetRangeUser(0,0.07);

        if (hName == "TriJetMass_0extrab_After" or 
            hName == "TriJetMass_1extrab_After" or
            hName == "TriJetMass_2extrab_After"      ):
            p.getFrame().GetXaxis().SetRangeUser(0,500);
            p.getFrame().GetYaxis().SetRangeUser(0,0.125);

        # SetLog
        SetLogAndGrid(p, **kwargs)

        # Add cut line/box
        _kwargs = { "lessThan": kwargs.get("cutLessThan")}
        p.addCutBoxAndLine(cutValue=kwargs.get("cutValue"), fillColor=kwargs.get("cutFillColour"), box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs)

        # Move the refDataset to first in the draw order (back)
        #histoNames = [h.getName() for h in p.histoMgr.getHistos()]
        #p.histoMgr.reorder(filter(lambda n: plots._legendLabels[kwargs.get("refDataset") ] not in n, histoNames))
                
        
        #  Draw plots
        p.draw()

        # Customise text
        #histograms.addStandardTexts(lumi=intLumi)
        histograms.addStandardTexts()
        # histograms.addText(0.4, 0.9, "Alexandros Attikis", 17)
        # histograms.addText(0.4, 0.11, "Runs " + datasetsMgr.loadRunRange(), 17)


        # Save canvas under custom dir
        SaveAs(p, savePath, saveName, kwargs.get("saveFormats"))

        #edw
    return


#================================================================================================
# Main
#================================================================================================
if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab"    , dest="mcrab"    , action="store", help="Path to the multicrab directory for input")
    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=True, help="Enables batch mode (canvas creation does NOT generates a window)")
    parser.add_option("-v", "--verbose"  , dest="verbose"  , action="store_true", default=False, help="Enables verbose mode (for debugging purposes)")
    (parseOpts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if parseOpts.mcrab == None:
        Print("Not enough arguments passed to script execution. Printing docstring & EXIT.")
        print __doc__
        sys.exit(0)
    else:
        pass

    # Program execution
    main()

    if not parseOpts.batchMode:
        raw_input("=== plotTemplate.py: Press any key to quit ROOT ...")
        
