#!/usr/bin/env python
'''
  DESCRIPTION:
  
  Script to call for saving the uncertainties in a JSON file
  
  USAGE:
  In your plotting script add the following:

  from UncertaintyWriter import UncertaintyWriter
  uncWriter = UncertaintyWriter()
  uncWriter.addParameters(datasetName, analysis, saveDir, default_eff, ttVariationEff[i])
  uncWriter.writeJSON(jsonName)
    
'''

# ================
# Imports
# ================
import os
import re
import sys
from math import sqrt

import ROOT

# =================
# Class Definition
# =================
class UncertaintyWriter:

        
    class Parameters:
        
        def __init__(self, name, analyzer, path, eff_default, eff_variation):
            self.name     = name
            self.analyzer = analyzer
            self.path     = path
            self.default  = eff_default
            self.variation= eff_variation
            return
            
    def timeStamp(self):
        import datetime
        time = datetime.datetime.now().ctime()
        return time
            
    def __init__(self):
        self.ranges   = []
        self.analyzer = []
        self.bins     = []
        self.plotDir = "./"
        self.rootVersion = ROOT.gROOT.GetVersion()
        return
    
    
    def addParameters(self, name, analyzer, path, eff_default, eff_variation):
        self.ranges.append(self.Parameters(name, analyzer, path, eff_default, eff_variation))
        return
    
    def writeJSON(self, saveName):
        
        fOUT = open(saveName,"w")
        fOUT.write("{\n")
        
        time = self.timeStamp()
        fOUT.write("  \"_timestamp\":   \"Generated on "+time+" by HiggsAnalysis/NtupleAnalysis/src/TopTaggerEfficiency/work/plot_EfficiencySystTop.py\",\n")
        fOUT.write("  \"_rootVersion\": \"%s\",\n"%self.rootVersion)
        
        subranges = self.ranges
        comma = ","
        for i, r in enumerate(subranges):
            
            if i == len(subranges)-1:
                comma = ""
                
            self.writeBins(fOUT, r.name, r.default, r.variation)
            fOUT.write("      }"+comma+"\n")
            
            
        fOUT.write("}\n")
        fOUT.close()
        
        return

    def writeBins(self, fOUT, name, default, variation):
        
        fOUT.write("   \""+name+"\" : {\n")
        fOUT.write("         \"bins\" : [\n")
        nBins = default.GetN()
        
        comma = ","
        for i in range(0, nBins):
            
            if i == nBins-1:
                comma = ""

            ratio = float(default.GetY()[i])/float(variation.GetY()[i])
            unc = 0.5*(1.0-ratio)
            
            print "Bin = ", i, " Default TT=", default.GetY()[i], "   Variation TT=", variation.GetY()[i], "  Ratio=", ratio, "  Unc=", unc
            
            binLowEdge = default.GetX()[i]
            binLowEdge-= default.GetErrorXlow(i)
            
            fOUT.write("               {\n")
            fOUT.write("                 \"pt\"              :"+str(binLowEdge)+",\n")
            fOUT.write("                 \"uncertainty\"     :"+str(unc)+",\n")
            fOUT.write("                }%s\n"%comma)
        
        fOUT.write("          ]\n")
        return
               
