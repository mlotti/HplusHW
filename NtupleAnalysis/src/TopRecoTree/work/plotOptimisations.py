#!/usr/bin/env python

'''

Usage:

-Launch default script                                                                                                                 
./plotOptimisations.py -m <pseudo_mcrab_directory>                                                                                     
      
-Launch default script with verbose mode enabled (printing debugging info)                                                    
./plotOptimisations.py -m <pseudo_mcrab_directory> -v

-Launch but exclude the M_180 sample                                                                                               
./plotOptimisations.py -m <pseudo_mcrab_directory> -e M_180                                                                              
                                                                                                                                 
-Launch but exclude the various samples                                                                           
./plotOptimisations.py -m <pseudo_mcrab_directory> -e "M_180|M_200|M_220|M_250|M_300|M_350|M_400|ZZTo4Q"         
                                
-Launch but only include the QCD_Pt samples                                                            
./plotOptimisations.py -m <pseudo_mcrab_directory> -i QCD_Pt                                                                         

-Launch script for cut Direction 'GreaterThan' or 'LessThan' 
./plotOptimisations.py -m <pseudo_mcrab_directory> -c ">"
OR
./plotOptimisations.py -m <pseudo_mcrab_directory> -c "<"

-Launch script for significance definition "S1" (S1 = S/sqrt(B)) or "S2" (S2 = S/B)
./plotOptimisations.py -m <pseudo_mcrab_directory> -s "S1"
OR 
./plotOptimisations.py -m <pseudo_mcrab_directory> -s "S2"
    


ROOT:
The available ROOT options for the Error-Ignore-Level are (const Int_t):
        kUnset    =  -1
        kPrint    =   0
        kInfo     =   1000
        kWarning  =   2000
        kError    =   3000
        kBreak    =   4000

'''

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
#from plotAux import *

import ROOT
import array


#================================================================================================
# User Options
#================================================================================================
kwargs = {
     "analysis"       : "HplusHadronic",
     "savePath"       : None,
     "saveFormats"    : [".pdf"],
     "normalizeTo"    : "Luminosity", #One", "XSection", "Luminosity"
     "createRatio"    : False,
     "logX"           : False,
     "logY"           : False,
     "gridX"          : True,
     "gridY"          : True,
     "drawStyle"      : "CPE",  #CPE
     "legStyle"       : "LP", 
     "verbose"        : False,
     "cutValue"       : 0,
     "cutBox"         : False,
     "cutLine"        : True,
     "cutLessthan"    : False,
     "cutFillColour"  : ROOT.kViolet,
     "folder"         : None, #"TTree",
     }


#================================================================================================
# Histograms
#================================================================================================

hNames  = [
#     "LdgTop_Mass", 
#     "SubLdgTop_Mass",
#     "recoJet7_Pt"
     ]


hNames2D_wCuts = [
     "DPhiJ34vsDPhiJ56_wCut025",
     "DPhiJ34vsDPhiJ56_wCut05",
     "DPhiJ34vsDPhiJ56_wCut075",
     "DPhiJ34vsDPhiJ56_wCut10",
     "DPhiJ34vsDPhiJ56_wCut125",
     "DPhiJ34vsDPhiJ56_wCut15",
     ]

hNames2D = [
     "DPhiJ34vsDPhiJ56",
#     "HiggsInvMass_Vs_LdgTopMass",
#     "HiggsInvMass_Vs_SubLdgTopMass",
     ]

'''
hNames  = [
     #"METoverSqrtHT",
     "R32_LdgTop",
     "R32_SubLdgTop",
     "LdgTop_Mass", 
     "SubLdgTop_Mass",
     "BJetPair_MaxMass_M",
     "BJetPair_MaxMass_dR",
     "BJetPair_MaxMass_dEta",
     "BJetPair_MaxMass_dPhi",
     "BJetPair_MaxPt_M",
     "BJetPair_MaxPt_dR",
     "BJetPair_MaxPt_dEta",
     "BJetPair_MaxPt_dPhi",
     "BJetPair_dRMin_Mass",
     "BJetPair_dRMin_dR",
     "BJetPair_dRMin_dEta",
     "BJetPair_dRMin_dPhi",
     "BJetPair_dRMax_Mass",
     "BJetPair_dRMax_dR",
     "BJetPair_dRMax_dEta",
     "BJetPair_dRMax_dPhi",
     "BJetPair_dRAverage",
     "BJetPair_dEtaAverage",
     "BJetPair_dPhiAverage",
     "dRMinDiJet_NoBJets_Mass",
     "dRMinDiJet_NoBJets_dR",
     "dRMinDiJet_NoBJets_dEta",
     "dRMinDiJet_NoBJets_dPhi",
     "Hplus_LdgTop_dEta", 
     "Hplus_LdgTop_dPhi",
     "Hplus_LdgTop_dR",
     "Hplus_SubLdgTop_dEta",
     "Hplus_SubLdgTop_dPhi",
     "Hplus_SubLdgTop_dR",
     "TetraJetBJet_LdgTriJetBJet_dR", 
     "TetraJetBJet_LdgTriJetBJet_dEta",
     "TetraJetBJet_LdgTriJetBJet_dPhi",
     "TetraJetBJet_SubLdgTriJetBJet_dR",
     "TetraJetBJet_SubLdgTriJetBJet_dEta",
     "TetraJetBJet_SubLdgTriJetBJet_dPhi",
     "TetraJetBJet_LdgTriJetDiJet_dR",
     "TetraJetBJet_LdgTriJetDiJet_dEta",
     "TetraJetBJet_LdgTriJetDiJet_dPhi",
     "TetraJetBJet_SubLdgTriJetDiJet_dR",
     "TetraJetBJet_SubLdgTriJetDiJet_dEta",
     "TetraJetBJet_SubLdgTriJetDiJet_dPhi",
     "LdgTriJetDiJet_SubLdgTriJetDiJet_dR",
     "LdgTriJetDiJet_SubLdgTriJetDiJet_dEta",
     "LdgTriJetDiJet_SubLdgTriJetDiJet_dPhi",


    ]
'''

#================================================================================================                                   
# Variable Definition                                                                                                                   
#================================================================================================                               

htb = "ChargedHiggs_HplusTB_HplusToTB_"
styleDict = {
     "Data"             : styles.dataStyle,
     htb + "M_800"      : styles.signal800Style,
     htb + "M_2000"     : styles.signal2000Style,
     htb + "M_1000"     : styles.signal1000Style,
     htb + "M_500"      : styles.signal500Style,
     htb + "M_400"      : styles.signal400Style,
     htb + "M_350"      : styles.signal350Style,
     htb + "M_300"      : styles.signal300Style,
     htb + "M_250"      : styles.signal250Style,
     htb + "M_220"      : styles.signal220Style,
     htb + "M_200"      : styles.signal200Style,
     htb + "M_180"      : styles.signal180Style,
     "QCD-b"            : styles.qcdBEnrichedStyle,
     "QCD"              : styles.qcdStyle, #qcdFillStyle,                                                                           
     "QCD_Pt_15to30"    : styles.qcdFillStyle,
     "QCD_Pt_30to50"    : styles.qcdFillStyle,
     "QCD_Pt_50to80"    : styles.qcdFillStyle,
     "QCD_Pt_80to120"   : styles.qcdFillStyle,
     "QCD_Pt_120to170"  : styles.qcdFillStyle,
     "QCD_Pt_170to300"  : styles.qcdFillStyle,
     "QCD_Pt_300to470"  : styles.qcdFillStyle,
     "QCD_Pt_470to600"  : styles.qcdFillStyle,
     "QCD_Pt_600to800"  : styles.qcdFillStyle,
     "QCD_Pt_800to1000" : styles.qcdFillStyle,
     "QCD_Pt_1000to1400": styles.qcdFillStyle,
     "QCD_Pt_1400to1800": styles.qcdFillStyle,
     "QCD_Pt_1800to2400": styles.qcdFillStyle,
     "QCD_Pt_2400to3200": styles.qcdFillStyle,
     "QCD_Pt_3200toInf" : styles.qcdFillStyle,
     
     "QCD_bEnriched_HT300to500"  : styles.qcdFillStyle,
     "QCD_bEnriched_HT500to700"  : styles.qcdFillStyle,
     "QCD_bEnriched_HT700to1000" : styles.qcdFillStyle,
     "QCD_bEnriched_HT1000to1500": styles.qcdFillStyle,
     "QCD_bEnriched_HT1500to2000": styles.qcdFillStyle,
     "QCD_bEnriched_HT2000toInf" : styles.qcdFillStyle,
     
     "TTBB"                   : styles.ttbbStyle,
     "TT"                   : styles.signal350Style,#styles.ttStyle, #here
     "TTJets"               : styles.ttjetsStyle,
     "SingleTop"            : styles.singleTopStyle,
     "TTTT"                 : styles.ttttStyle,
     "TTWJetsToQQ"          : styles.ttwStyle,
     "TTZToQQ"              : styles.ttzStyle,
     "WJetsToQQ_HT_600ToInf": styles.wjetsStyle,
     "WWTo4Q"               : styles.wStyle,
     "ZJetsToQQ_HT600toInf" : styles.zjetsStyle,
     "ZZTo4Q"               : styles.zzStyle ,
     "Diboson"              : styles.dibStyle,
     "ttbb"                 : styles.ttbbStyle,
     "QCD"                  : styles.ttbbStyle,
     "EWK"                  : styles.ttStyle,
     "Top"                  : styles.qcdBEnrichedStyle,
     "QCD+Top"              : styles.zjetsStyle,
     }


#================================================================================================
# Main
#================================================================================================

def Print(msg, printHeader=False):
     fName = __file__.split("/")[-1]
     if printHeader==True:
          print "=== ", fName
          print "\t", msg
     else:
          print "\t", msg
     return



def Verbose(msg, printHeader=True, verbose=False):
     if not parseOpts.verbose:
          return
     Print(msg, printHeader)
     return



def GetLumi(datasetsMgr):
     Verbose("Determininig Integrated Luminosity")

     lumi = 0.0
     for d in datasetsMgr.getAllDatasets():
          if d.isMC():
               continue
          else:
               lumi += dataset.getLuminosity()
     Verbose("Luminosity = %s (pb)" % (lumi), True )
     return lumi



def HasKeys(keyList, **kwargs):
     for key in keyList:
          if key not in kwargs:
               raise Exception("Could not find the keyword \"%s\" in kwargs" % (key) )
     return



def GetDatasetsFromDir(mcrab, opts, **kwargs):

     dataEra    = kwargs.get("dataEra")
     searchMode = kwargs.get("searchMode")
     analysis   = kwargs.get("analysis")
     optMode    = kwargs.get("optMode")

     datasets = dataset.getDatasetsFromMulticrabDirs([mcrab], dataEra=dataEra, searchMode=searchMode, analysisName=analysis, optimizationMode=optMode)
     
     # Inform user of datasets retrieved                                                                                                   
     Verbose("Got the following datasets from multicrab dir \"%s\"" % mcrab)
     for d in datasets.getAllDatasets():
          Verbose( "\t", d.getName(), False)
     return datasets



def GetSavePath(**kwargs):
     
     HasKeys(["savePath", "analysis", "verbose"], **kwargs)
     savePath = kwargs.get("savePath")
     analysis = kwargs.get("analysis")
     verbose  = parseOpts.verbose
     
     if verbose:
          print "\t--- Constructing path where plots will be saved"

     if savePath != None:
          return savePath

     # Get username and the initial of the username
     user    = getpass.getuser()
     initial = getpass.getuser()[0]

     # Set the save path depending on the host
     if "lxplus" in socket.gethostname():
          savePath = "/afs/cern.ch/user/%s/%s/public/html/%s/" % (initial, user, analysis)
     if "lpc" in socket.gethostname():
          savePath = "/publicweb/%s/%s/%s/" % (initial, user, analysis)
     else:
          savePath = "/Users/%s/Desktop/Plots/" % (user)

     return savePath



def GetSaveName(savePathNew, hName, **kwargs):

     HasKeys(["savePath", "verbose"], **kwargs)
     verbose      = parseOpts.verbose
     cutDirection =parseOpts.cutDirection
     
     if verbose:
          print "\t--- Constructing name of plot to  be saved"

     # Replace "/" with "_" for the save name
     forbidden   = ["/"]
     replacement = "_"
     for f in forbidden:
          if f in hName:
               Print("Replacing forbidden character \"%s\" with \"%s\" in saveName  \"%s\"" % (f, replacement, hName))
               hName = hName.replace(f, replacement)

     # Set the save name 
     if cutDirection == None:
          saveName = os.path.join(savePathNew, hName)
     elif cutDirection == ">":
          saveName = os.path.join(savePathNew, hName + "_GreaterThan")
     else:
          saveName = os.path.join(savePathNew, hName + "_LessThan")
          
     return saveName



def GetSavePathAndName(hName, **kwargs):
     
     HasKeys(["verbose"], **kwargs)
     verbose  = parseOpts.verbose
     
     Verbose("Getting save path and name for histo with name %s" %(hName), verbose)
     
     # Get the save name and the save path
     savePathNew = GetSavePath(**kwargs)
     saveName    = GetSaveName(savePathNew, hName, **kwargs)

     return savePathNew, saveName


def IsValidNorm(normalizeTo):
    validNorms = ["One", "XSection", "Luminosity", ""]

    if normalizeTo not in validNorms:
        raise Exception("Invalid normalization option \"%s\". Please choose one of the following: %s" % (normalizeTo, "\"" + "\", \"".join
(validNorms) ) + "\"")
    return


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
         #intLumi = GetLumi(datasetsMgr)
         #if not rootHisto.isData():
         #   rootHisto.normalizeToLuminosity(intLumi)
         rootHisto.normalizeToLuminosity(36.3*(10**3))
    else:
         IsValidNorm(normalizeTo)
    return
 


def GetBinwidthDecimals(binWidth):
     if binWidth < 0.0001:
          return " %0.5f"
     elif binWidth < 0.001:
          return " %0.4f"
     elif binWidth < 0.01:
          return " %0.3f"
     elif binWidth < 0.1:
          return " %0.2f"
     elif binWidth < 1:
          return " %0.1f"
     else:
          return " %0.0f"

     

def CheckNegatives(n, d, verbose=False):

     # Create a Table with Numerator and Denominator Values for all the bins 
     table    = []
     txtAlign = "{:<5} {:>20} {:>20}"
     hLine    = "="*50
     table.append(hLine)
     table.append(txtAlign.format("Bin #", "Numerator (8f)", "Denominator (8f)"))
     table.append(hLine)
     
     # For-loop: All bins in x-axis                                                                                                      
     for i in range(1, n.GetNbinsX()+1):

          # Get the value of the numerator and the denominator
          nBin = n.GetBinContent(i)
          dBin = d.GetBinContent(i)
          
          # Add binNo, Nominator and Denominator to the table 
          table.append(txtAlign.format(i, "%0.8f" % (nBin), "%0.8f" % (dBin) ))
          
          # Numerator > Denominator                                                                        
          if nBin > dBin:
               n.SetBinContent(i, dBin)
               
          # Numerator < 0                                                                                                                 
          if nBin < 0:
               n.SetBinContent(i, 0)

          # Denominator < 0                                                                                                              
          if dBin < 0:
               n.SetBinContent(i, 0)
               d.SetBinContent(i, 0)
               
     if verbose:
          for r in table:
               print r
     return



def Convert2TGraph(tefficiency, dataset, style, titleX, titleY):
     
     # Create lists for x-y values and their errors (low and high)
     x     = []
     y     = []
     xerrl = []
     xerrh = []
     yerrl = []
     yerrh = []

     # Get the copy of the tefficiency graph
     h = tefficiency.GetCopyTotalHisto()
     
     # Get the Number of the bins
     n = h.GetNbinsX()

     # For-Lopp over the bins
     for i in range(1,n+1):

          # Append to the lists the values for x,y and their errors
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

     # Create a TGraph with Asymmetric errors
     # tgraph = ROOT.TGraphAsymmErrors(n, array.array("d",x), array.array("d",y), array.array("d",xerrl), array.array("d",xerrh), array.array("d",yerrl), array.array("d",yerrh))     

     # Create a TGraph
     tgraph = ROOT.TGraph(n, array.array("d", x), array.array("d", y))
     
     # Customize graph
     legName = plots._legendLabels[dataset.getName()]
     tgraph.SetName(dataset.getName())
     tgraph.GetXaxis().SetTitle(titleX)
     tgraph.GetYaxis().SetTitle(titleY)
     styleDict[dataset.getName()].apply(tgraph)
     #
     effGraph = histograms.HistoGraph(tgraph, legName, "CPE" , "LP")
     
     return effGraph



def GetCumulativePlot(dataset, histoName, **kwargs):
     HasKeys(["verbose", "normalizeTo"], **kwargs)
     verbose     = parseOpts.verbose
     normalizeTo = kwargs.get("normalizeTo")
     cutDirection=parseOpts.cutDirection
     
     Verbose("Getting the Cumulative Plot (%s) for histo with name %s for dataset: %s" % (cutDirection, histoName, dataset.getName()) )
    
     # Get the ROOT histogram                                                                                                   
     rootHisto = dataset.getDatasetRootHisto(histoName)
     
     # Normalise the histogram                                                                                                           
     NormalizeRootHisto(dataset, rootHisto, dataset.isMC(), normalizeTo)

     # Get a clone of the wrapped histogram normalized as requested.                                                         
     h = rootHisto.getHistogram()

     # Get x-axis title and binwidth 
     titleX   = h.GetXaxis().GetTitle()
     binWidth = h.GetXaxis().GetBinWidth(0)

     # Set y-axis title value 
     titleY   = "EventsNo (%s) / %s" % (cutDirection, GetBinwidthDecimals(binWidth) % (binWidth) )
     
     # If empty return                                                                                                    
     if h.GetEntries() == 0:
          return

     # Create the eventsNo histogram                                                                                  
     eventsNo   = h.Clone("eventsNo")

     # Reset and Edit the eventsNo histogram                                                                                
     eventsNo.Reset()
     eventsNo.GetXaxis().SetTitle(titleX)
     eventsNo.GetYaxis().SetTitle(titleY)
    
     # Create a table to save info (for debugging)                                                                
     table    = []
     hLine    = "="*75
     msgAlign = '{:<5} {:<25} {:<20} {:<20}'
     title    = msgAlign.format("Bin", "Integral(Bin,BinsNo)", "nPassed", "nTotal")
     table.append("\n" + hLine)
     table.append(title)
     table.append(hLine)

     # Calculate the instances passing a given cut (all bins)                                                                       
     nBinsX = h.GetNbinsX()+1
     for iBin in range(1, nBinsX):

          # Get the total number of events
          nTotal = h.Integral(0, nBinsX)
          
          # Get the number of events that passed the specific bin value (depending on the cut Direction) 
          if cutDirection == ">":
               nPass  = h.Integral(iBin, nBinsX)
          elif cutDirection == "<":
               nPass  = nTotal - h.Integral(iBin, nBinsX)
          else:
               raise Exception("Invalid cut direction  \"%s\". Please choose either \">\" or \"<\"" % (cutDirection))

          # Sanity check                                                                                                                  
          if nPass < 0:
               nPass = 0
               
          # Fill the eventNo histogram                                                                                               
          eventsNo.SetBinContent(iBin, nPass)
          eventsNo.SetBinError(iBin, math.sqrt(nPass)/10)

          # Save info to table (debugging)
          values = msgAlign.format(iBin, h.Integral(iBin, nBinsX), nPass, nTotal)
          table.append(values)
     table.append(hLine)

     # Verbose mode                                                                                     
     if verbose:
          print "\t--- Number of events is normalized to %s" %(kwargs.get("normalizeTo"))
          for l in table:
               print l

     return eventsNo


def my_range(start, end, step):
     while start <= end:
          yield start
          start += step


def GetSignificanceForCutWithinWindow(signal_dataset, background_dataset, histoName, windowCenter, **kwargs):
     normalizeTo = kwargs.get("normalizeTo")
     drawStyle    = kwargs.get("drawStyle")
     legStyle     = kwargs.get("legStyle")
     legName      = plots._legendLabels[signal_dataset.getName()]

     # Get the ROOT histogram                                                                                                                                                                             
     rootHistoBkg    = background_dataset.getDatasetRootHisto(histoName)
     rootHistoSignal = signal_dataset.getDatasetRootHisto(histoName)

     # Normalise the histogram                                                                                                                                                                            
     NormalizeRootHisto(background_dataset, rootHistoBkg, background_dataset.isMC(), normalizeTo)
     NormalizeRootHisto(signal_dataset, rootHistoSignal, signal_dataset.isMC(), normalizeTo)

     # Get a clone of the wrapped histogram normalized as requested.                                                                                                                                      
     h_Bkg = rootHistoBkg.getHistogram()
     h_Signal = rootHistoSignal.getHistogram()

     # Create lists to append the window opening values and the significance of signal of each one
     x_values=[]
     y_values=[]

     # Create variables for Maximum Significance                                                                                                                                                          
     maxSignX = 0
     maxSignY = 0

     # For-loop: All possible (equal for both sides) window opening values
     for windowOpening in my_range(0, 170, 10):

          # Get the number of the events which survive in the window
          signalEvents = h_Signal.Integral(h_Signal.FindBin(windowCenter-windowOpening),h_Signal.FindBin(windowCenter+windowOpening)) 
          bkgEvents    = h_Bkg.Integral(h_Bkg.FindBin(windowCenter-windowOpening),h_Bkg.FindBin(windowCenter+windowOpening))
          
          # Calculate the significance (S=S/sqrt(B))
          #Significance.SetBinContent( Significance.FindBin(windowOpening), float(signalEvents)/math.sqrt(float(bkgEvents)) )
          significance = float(signalEvents)/math.sqrt(float(bkgEvents))

          # Find the Maximum Significance variables                                                                                                                                                       
          if (significance > maxSignY):
               maxSignY = significance
               maxSignX = windowOpening

          x_values.append(windowOpening)
          y_values.append(significance)


          #maxSignX = x_values.index(maxSignXvalue)
     
     # Create the Significance Plot                                                                                                                                                                       
     tGraph = ROOT.TGraph(len(x_values), array.array("d", x_values), array.array("d", y_values))

     # Customize the Significance Plot                                                                                                                                                                    
     ytitle = "S/ #sqrt{B} "
     styleDict[signal_dataset.getName()].apply(tGraph)
     tGraph.SetName(signal_dataset.getName())
     tGraph.GetYaxis().SetTitle( ytitle + " /10" ) #%s" % (GetBinwidthDecimals(binWidth) % (binWidth) ))
     tGraph.GetXaxis().SetTitle("Cut window opening")#h_signal.GetXaxis().GetTitle())
     #                                                                                                                                                                                                    
     significanceGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)



     return significanceGraph, maxSignX


def GetEfficiencyForCutWithinWindow(dataset, histoName, windowCenter, **kwargs):
     normalizeTo = kwargs.get("normalizeTo")
     drawStyle    = kwargs.get("drawStyle")
     legStyle     = kwargs.get("legStyle")
     legName      = plots._legendLabels[dataset.getName()]

     # Get the ROOT histogram                                                                                                                                                                             
     rootHisto    = dataset.getDatasetRootHisto(histoName)

     # Normalise the histogram                                                                                                                                                                            
     NormalizeRootHisto(dataset, rootHisto, dataset.isMC(), normalizeTo)

     # Get a clone of the wrapped histogram normalized as requested.                                                                                                                                      
     h = rootHisto.getHistogram()
     
     # Get the bin number of the histogram
     binsNo = h.GetNbinsX()

     # Create lists to append the window opening values and the significance of signal of each one                                                                                                        
     x_values=[]
     y_values=[]

     # For-loop: All possible (equal for both sides) window opening values                                                                                                                                
     for windowOpening in my_range(0, 170, 20):
          
          # Get the number of the events which survive in the window                                                                                                                                 
          signalEvents = h.Integral(h.FindBin(windowCenter-windowOpening),h.FindBin(windowCenter+windowOpening))
          allEvents    = h.Integral(0, binsNo)
          
          # Calculate the significance (S=S/sqrt(B))                                                                                                                                                      
          efficiency = float(signalEvents)/float(allEvents)
          
          x_values.append(windowOpening)
          y_values.append(efficiency)

     # Create the Significance Plot                                                                                                                                                                       
     tGraph = ROOT.TGraph(len(x_values), array.array("d", x_values), array.array("d", y_values))

     # Customize the Significance Plot                                                                                                                                                                    
     ytitle = "Efficiency"
     styleDict[dataset.getName()].apply(tGraph)
     tGraph.SetName(dataset.getName())
     tGraph.GetYaxis().SetTitle( ytitle + " /20" ) #%s" % (GetBinwidthDecimals(binWidth) % (binWidth) ))                                                                                      
     tGraph.GetXaxis().SetTitle("Cut window opening on m_{top}")#h_signal.GetXaxis().GetTitle())                                                                                                                      
     #                                                                                                                                                                                                    
     efficiencyGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)

     return efficiencyGraph

          
          


def GetOptimisationPlot(signal_dataset, background_dataset, histoName, **kwargs):
     HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
     drawStyle    = kwargs.get("drawStyle")
     legStyle     = kwargs.get("legStyle")
     legName      = plots._legendLabels[signal_dataset.getName()]
     cutDirection = parseOpts.cutDirection
     verbose      = parseOpts.verbose

     Verbose("Signal Dataset: %s --- Bkg Dataset: %s" % (signal_dataset.getName(), background_dataset.getName()))

     # Get the Cumulative Plots for Signal & Bkg                                                                            
     Signal_Cumul     = GetCumulativePlot(signal_dataset, histoName, **kwargs)
     Background_Cumul = GetCumulativePlot(background_dataset, histoName, **kwargs)

     # Create lists to append the x-y values of the Cumulative Plots for Signal & Bkg 
     x_signal     = []
     y_signal     = []
     x_background = []
     y_background = []

     # Clone the Cumulative plots for Signal & Bkg                                                                                    
     h_signal     = Signal_Cumul.Clone()
     h_background = Background_Cumul.Clone()
     
     # Rebin CSV histos                                                                                         
     if "AvgCSV" in histoName:
          h_signal.Rebin(2)
          h_background.Rebin(2)

     # Get the binNo of the Cumulative plots for Signal and Bkg                 
     n_signal = h_signal.GetNbinsX()
     n_background = h_background.GetNbinsX()
     
     # Get the bin-width of the plots                                                                               
     binWidth_signal     = h_signal.GetBinWidth(0)
     binWidth_background = h_background.GetBinWidth(0)
     
     # Sanity Checks                                                                                                                
     # === for binNo
     if (n_signal != n_background):
          print "Warning: Number of Bins of signal and background are different!"
     # === for binWidth
     if (binWidth_signal == binWidth_background):
          binWidth = binWidth_signal
     else:
          print "Warning: Bin Width of signal and background is different!"
          

     # Get the x-y values of the Cumulative Histogram                                                                                   
     for i in range(1, n_signal+1):

          # Signal (x,y) Values                                                                                                      
          x_signal.append(h_signal.GetBinLowEdge(i)+0.5*h_signal.GetBinWidth(i))
          y_signal.append(h_signal.GetBinContent(i))
          
          # Background (x,y) Values                                                                     
          x_background.append(h_background.GetBinLowEdge(i)+0.5*h_background.GetBinWidth(i))
          y_background.append(h_background.GetBinContent(i))

     # Create the (x-y) list to append the significance value for each x value                                                      
     x = []
     y = []
     
     # Create variables for Maximum Significance                                                                        
     maxSignX = 0
     maxSignY = 0

     # Verbose Mode
     Verbose("Getting the Optimisation Plot (%s) for histo with name %s for:" % (cutDirection, histoName) )
     if verbose:
          print "\tSignal Dataset: %s & Bkg Dataset: %s" % (signal_dataset.getName(), background_dataset.getName())

     # Create a table to save info (for debugging)                                                                                  
     table    = []
     hLine    = "="*90
     msgAlign = '{:<5}{:<20}{:<20} {:<20} {:<20}'
     title    = msgAlign.format("Bin", "Value", "Significance", "Signal Events", "Background Events")
     table.append("\n" + hLine)
     table.append(title)
     table.append(hLine)

     # Calculate the Significance of the Signal (depending on the definition)         
     for i in range(0, n_signal):
          if ((float(y_background[i]) <= 1 ) or (float(y_signal[i]) <= 0)):
               significance = 0
          elif (parseOpts.significanceDef == "S1"): # S1 = S/sqrt(B)
               significance = float(y_signal[i])/math.sqrt(float(y_background[i]))
          elif (parseOpts.significanceDef == "S2"): # S2 = S/B
               significance = float(y_signal[i]) / float(y_background[i])
               
          # Find the Maximum Significance variables                                                                                 
          if (significance > maxSignY):
               maxSignY = significance
               maxSignX = x_signal[i]

          # Fill the lists with the x-y values for the Significance Plot                                                                
          x.append(x_signal[i])
          y.append(significance)

          # Save info in a table (debugging)                                                                                  
          values = msgAlign.format(i, x_signal[i], significance, y_signal[i], y_background[i])
          table.append(values)
     table.append(hLine)

     # Verbose mode                                                                                                         
     if verbose:
          print "\t--- Number of events is normalized to %s" %(kwargs.get("normalizeTo"))
          for l in table:
               print l

     # Create the Significance Plot                                                                                   
     tGraph = ROOT.TGraph(n_signal, array.array("d", x), array.array("d", y))

     # Customize y-axis title (depending on significance definition)                                       
     if (parseOpts.significanceDef == "S1"):
          ytitle = "S/ #sqrt{B} "
     elif (parseOpts.significanceDef == "S2"):
          ytitle = "S/B"

     # Customize the Significance Plot                                                                                          
     styleDict[signal_dataset.getName()].apply(tGraph)
     tGraph.SetName(signal_dataset.getName())
     tGraph.GetYaxis().SetTitle( ytitle +" (%s) / %s" % (cutDirection, GetBinwidthDecimals(binWidth) % (binWidth) ))
     tGraph.GetXaxis().SetTitle(h_signal.GetXaxis().GetTitle())
     #
     optGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)

     return optGraph, maxSignX


 
def GetCutEfficiencyHisto(dataset, histoName, statOpt, **kwargs):
     '''                                                                                                                                   
     See https://root.cern.ch/doc/master/classTEfficiency.html                                                                            
     '''
     HasKeys(["verbose", "normalizeTo"], **kwargs)
     verbose     = parseOpts.verbose
     normalizeTo = kwargs.get("normalizeTo")
     cutDirection=parseOpts.cutDirection

     Verbose("Calculating the cut-efficiency (%s) for histo with name %s for dataset: %s" % (cutDirection, histoName, dataset.getName() ) )
     
     # Choose statistics options                                                                                                      
     statOpts = ["kFCP", "kFNormal", "KFWilson", "kFAC", "kFFC", "kBJeffrey", "kBUniform", "kBayesian"]
     if statOpt not in statOpts:
          raise Exception("Invalid statistics option \"%s\". Please choose one from the following:\n\t%s" % (statOpt, "\n\t".join(statOpts)))
     # Get the TEfficiency depending on the statistics option
     if statOpt == "kFCP":
          statOption = ROOT.TEfficiency.kFCP      # Clopper-Pearson                                                                    
     elif statOpt == "kFNormal":
          statOption = ROOT.TEfficiency.kFNormal  # Normal Approximation                                                                 
     elif statOpt == "kFWilson":
          statOption = ROOT.TEfficiency.kFWilson  # Wilson                                                                            
     elif statOpt == "kFAC":
          statOption = ROOT.TEfficiency.kFAC      # Agresti-Coull                                                                    
     elif statOpt == "kFFC":
          statOption = ROOT.TEfficiency.kFFC      # Feldman-Cousins                                                                   
     elif statOpt == "kBJeffrey":
          statOption = ROOT.TEfficiency.kBJeffrey # Jeffrey                                                                    
     elif statOpt == "kBUniform":
          statOption = ROOT.TEfficiency.kBUniform # Uniform Prior                                                       
     elif statOpt == "kBayesian":
          statOption = ROOT.TEfficiency.kBayesian # Custom Prior
     else:
          raise Exception("This should never be reached")

     
     # Declare variables & options                                                                                              
     first  = True
     isData = False
     teff   = ROOT.TEfficiency()
     
     # Get the ROOT histogram                                                                                                
     rootHisto = dataset.getDatasetRootHisto(histoName)
     
     # Normalise the histogram                                                                                                            
     NormalizeRootHisto(dataset, rootHisto, dataset.isMC(), normalizeTo)
     
     # Get a clone of the wrapped histogram normalized as requested.                                                                     
     h = rootHisto.getHistogram()
    
     # Rebin CSV histos                                                                                
     if "AvgCSV" in histoName:
          h.Rebin(2)


     # Get x-axis title and binwidth 
     titleX   = h.GetXaxis().GetTitle()
     binWidth = h.GetXaxis().GetBinWidth(0)
     
     # Set y-axis title 
     titleY   = "efficiency (%s) / %s" % (cutDirection, GetBinwidthDecimals(binWidth) % (binWidth) )
     
     # If empty return                                                                                                      
     if h.GetEntries() == 0:
          return

     # Create the numerator/denominator histograms                                                                    
     numerator   = h.Clone("Numerator")
     denominator = h.Clone("Denominator")
     
     # Reset the numerator/denominator histograms                                                                        
     numerator.Reset()
     denominator.Reset()
     
     # Calculate the instances passing a given cut (all bins)                                                         
     nBinsX = h.GetNbinsX()+1
     for iBin in range(1, nBinsX):
          
          # Get the total number of events 
          nTotal = h.Integral(0, nBinsX)
          
          # Get the number of events that passed the specific bin value (depending on the cut Direction) 
          if cutDirection == ">":
               nPass  = h.Integral(iBin+1, nBinsX)
          elif cutDirection == "<":
               nPass  = nTotal - h.Integral(iBin+1, nBinsX)
          else:
               raise Exception("Invalid cut direction  \"%s\". Please choose either \">\" or \"<\"" % (cutDirection))
          
          # Sanity check                                                                                                            
          if nPass < 0:
               nPass = 0
               
          # Fill the numerator/denominator histograms (values and errors)                                                          
          numerator.SetBinContent(iBin, nPass)
          numerator.SetBinError(iBin, math.sqrt(nPass)/10)
          #                                                                                                                
          denominator.SetBinContent(iBin, nTotal)
          denominator.SetBinError(iBin, math.sqrt(nTotal)/10)

     # Check for negative values                                                                                                  
     CheckNegatives(numerator, denominator)
     
     # Create TEfficiency object using the two histos                                                                
     eff = ROOT.TEfficiency(numerator, denominator)
     eff.SetStatisticOption(statOption)
     
     # Verbose Mode
     if verbose:
          print "\t--- The statistic option was set to %s" % (eff.GetStatisticOption())
     

     # Save info in a table (debugging)                                                                                  
     table    = []
     hLine    = "="*70
     msgAlign = '{:<5} {:<20} {:<20} {:<20}'
     title    = msgAlign.format("Bin", "Efficiency", "Error-Low", "Error-Up")
     table.append("\n" + hLine)
     table.append(title)
     table.append(hLine)
     for iBin in range(1, nBinsX):
          e      = eff.GetEfficiency(iBin)
          errLow = eff.GetEfficiencyErrorLow(iBin)
          errUp  = eff.GetEfficiencyErrorUp(iBin)
          values = msgAlign.format(iBin, e, errLow, errUp)
          table.append(values)
     table.append(hLine)
    
     # Verbose mode                                                                                                         
     if verbose:
          for l in table:
               print l
               
     # Get the weight
     weight = 1
     if dataset.isMC():
          weight = dataset.getCrossSection()
     eff.SetWeight(weight)

     if first:
          teff = eff
          if dataset.isData():
               tn = numerator
               td = denominator
          first = False
     else:
          teff.Add(eff)
          if dataset.isData():
               tn.Add(numerator)
               td.Add(denominator)

     # Get TEfficiency if datasets are Data
     if isData:
          teff = ROOT.TEfficiency(tn, td)
          teff.SetStatisticOption(self.statOption)

     style = styleDict[dataset.getName()]


     return Convert2TGraph(teff, dataset, style, titleX, titleY)


def GetChiSquareProbabilityPlot(dataset, ndof, alpha):

     drawStyle    = kwargs.get("drawStyle")                                                         
     legStyle     = kwargs.get("legStyle")                                                                 
     legName      = plots._legendLabels[dataset.getName()]                                                        
     normalizeTo  = kwargs.get("normalizeTo")

      # Get the ROOT histogram                                                                            
     chiSqr_rootHisto = dataset.getDatasetRootHisto("ChiSqr")

     # Normalise the histogram                                                                 
     NormalizeRootHisto(dataset, chiSqr_rootHisto, dataset.isMC(), normalizeTo)

     # Get a clone of the wrapped histogram normalized as requested.                                               
     ChiSquare_Distribution = chiSqr_rootHisto.getHistogram()

     # Get binsNo, xMin, xMax of the Chi Square Distribution                                              
     ChiSqr_bins   = ChiSquare_Distribution.GetXaxis().GetNbins()
     #ChiSqr_xMin   = ChiSquare_Distribution.GetXaxis().GetXmin()
     #ChiSqr_xMax   = ChiSquare_Distribution.GetXaxis().GetXmax()

     # Create lists to append the chi square values and the corresponding probabilities                           
     chiSqr_values=[]
     chiSqr_prob_values =[]

     # For-loop: All bins of Chi Square Distribution                                                       
     for iBin in range(0, ChiSqr_bins-1):

          # Get the chi square value and its probability                                                         
          chiSqr = ChiSquare_Distribution.GetBinLowEdge(iBin)+0.5*ChiSquare_Distribution.GetBinWidth(iBin)
          p      = ROOT.TMath.Prob(chiSqr, ndof)

          # Append values to lists                                                                        
          chiSqr_values.append(chiSqr)
          chiSqr_prob_values.append(p)

     # Create the Chi Square Probability Plot                                                            
     pGraph = ROOT.TGraph(ChiSqr_bins, array.array("d", chiSqr_values), array.array("d", chiSqr_prob_values))

     # Customize the Chi Square Probability Plot                                                         
     styleDict[dataset.getName()].apply(pGraph)                                                    
     #pGraph.SetName(dataset.getName())
     pGraph.GetYaxis().SetTitle("P(#chi^{2})")
     pGraph.GetXaxis().SetTitle("#chi^{2}")
     #                                                                                                                                   
     probGraph = histograms.HistoGraph(pGraph, legName, legStyle, drawStyle)                                                              

     # Get the Low and High Quantiles
     ChiSqr_quantileLow  = ROOT.TMath.ChisquareQuantile(float(alpha), ndof)
     ChiSqr_quantileHigh = ROOT.TMath.ChisquareQuantile(1.0-float(alpha), ndof)

     return probGraph, ChiSqr_quantileLow, ChiSqr_quantileHigh


def GetSignificance2DwithWindowOpening(signal_dataset, background_dataset, histoName, yaxisWindowCenter, **kwargs):
     HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
     drawStyle    = kwargs.get("drawStyle")
     legStyle     = kwargs.get("legStyle")
     legName      = plots._legendLabels[signal_dataset.getName()]
     cutDirection = parseOpts.cutDirection
     verbose      = parseOpts.verbose
     normalizeTo = kwargs.get("normalizeTo")


      # Get the ROOT histogram                                                                                                                                                                            
     rootHistoBkg    = background_dataset.getDatasetRootHisto(histoName)
     rootHistoSignal = signal_dataset.getDatasetRootHisto(histoName)

     # Normalise the histogram                                                                                                                                                                            
     NormalizeRootHisto(background_dataset, rootHistoBkg, background_dataset.isMC(), normalizeTo)
     NormalizeRootHisto(signal_dataset, rootHistoSignal, signal_dataset.isMC(), normalizeTo)

     # Get a clone of the wrapped histogram normalized as requested.                                                                                                                                      
     h_Bkg = rootHistoBkg.getHistogram()
     h_Signal = rootHistoSignal.getHistogram()

     significancePlots =[]
     maxSignXvalues = []     
     windowOpeningValues = []

     # For-loop: All possible (equal for both sides) window opening values                                                                              
     for windowOpening in my_range(0, 200, 20):
          
          if (windowOpening != 200):
               windowOpeningValues.append(windowOpening)
          else:
               windowOpeningValues.append("NoCuts")

          x=[]
          y=[]
          
          maxSignY = 0
          maxSignX = 0
          
          x_bins = h_Signal.GetXaxis().GetNbins()
          y_bins = h_Signal.GetYaxis().GetNbins()
          

          #print windowOpening, h_Signal.GetYaxis().FindBin(yaxisWindowCenter-windowOpening)
          if (windowOpening != 200):
               for bin in range (0, x_bins):
                    
                    x_value = h_Signal.GetXaxis().GetBinLowEdge(bin)+0.5*h_Signal.GetXaxis().GetBinWidth(bin)
                    
                    passBkg    = h_Bkg.Integral(bin,bin, h_Bkg.GetYaxis().FindBin(yaxisWindowCenter-windowOpening), h_Bkg.GetYaxis().FindBin(yaxisWindowCenter+windowOpening) )
                    passSignal = h_Signal.Integral(bin, bin, h_Signal.GetYaxis().FindBin(yaxisWindowCenter-windowOpening), h_Signal.GetYaxis().FindBin(yaxisWindowCenter+windowOpening) )
                    
                    
                    if ((float(passBkg) <= 1 ) or (float(passSignal) <= 0)):
                         significance = 0
                    else:
                         significance = float(passSignal)/math.sqrt(float(passBkg))
                         
                         
                    x.append(x_value)
                    y.append(significance)
                    
                    # Find the Maximum Significance variables                                                                                                                               
                    if (significance > maxSignY):
                         maxSignY = significance
                         maxSignX = x_value
          else:
               for bin in range (0, x_bins):
                    
                    x_value = h_Signal.GetXaxis().GetBinLowEdge(bin)+0.5*h_Signal.GetXaxis().GetBinWidth(bin)
                    
                    passBkg    = h_Bkg.Integral(bin,bin, 0, y_bins)
                    passSignal = h_Signal.Integral(bin, bin, 0, y_bins)
                    
                    
                    if ((float(passBkg) <= 1 ) or (float(passSignal) <= 0)):
                         significance = 0
                    else:
                         significance = float(passSignal)/math.sqrt(float(passBkg))


                    x.append(x_value)
                    y.append(significance)

                    # Find the Maximum Significance variables                                                                                                                                              
                    if (significance > maxSignY):
                         maxSignY = significance
                         maxSignX = x_value

               
          # Create the Significance Plot                                                                               
          tGraph = ROOT.TGraph(len(x), array.array("d", x), array.array("d", y))
     
          # Customize the Significance Plot        
          if (windowOpening !=200):
               ytitle = "S/ #sqrt{B} (w="+str(windowOpening)+")"
          else:
               ytitle = "S/ #sqrt{B} (No cuts)"
          styleDict[signal_dataset.getName()].apply(tGraph)
          tGraph.SetName(signal_dataset.getName())
          tGraph.GetYaxis().SetTitle( ytitle + " /20" ) #%s" % (GetBinwidthDecimals(binWidth) % (binWidth) ))                                                     
          tGraph.GetXaxis().SetTitle(h_Signal.GetXaxis().GetTitle())#h_signal.GetXaxis().GetTitle())                                                          
          #                                                                                                                  
          significanceGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)
          
          significancePlots.append(significanceGraph)
          maxSignXvalues.append(maxSignX)
               

     return significancePlots, maxSignXvalues, windowOpeningValues



##Soti fix me!!!
def GetSignificance2D_DPhiRadius(signal_dataset, background_dataset, histoName,  **kwargs):
     
     HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
     drawStyle    = kwargs.get("drawStyle")
     legStyle     = kwargs.get("legStyle")
     legName      = plots._legendLabels[signal_dataset.getName()]
     cutDirection = parseOpts.cutDirection
     verbose      = parseOpts.verbose
     normalizeTo = kwargs.get("normalizeTo")


      # Get the ROOT histogram                                                                                                                                                                            
     rootHistoBkg    = background_dataset.getDatasetRootHisto(histoName)
     rootHistoSignal = signal_dataset.getDatasetRootHisto(histoName)

     # Normalise the histogram                                                                                                                                                                            
     NormalizeRootHisto(background_dataset, rootHistoBkg, background_dataset.isMC(), normalizeTo)
     NormalizeRootHisto(signal_dataset, rootHistoSignal, signal_dataset.isMC(), normalizeTo)

     # Get a clone of the wrapped histogram normalized as requested.                                                                                                                                      
     h_Bkg = rootHistoBkg.getHistogram()
     h_Signal = rootHistoSignal.getHistogram()

#     significancePlots =[]
#     maxSignXvalues = []     
#     windowOpeningValues = []
     radiusValues = []
     # For-loop: All possible (equal for both sides) window opening values                                                                              
     x=[]
     y=[]
          
     
     RADIUS = [0,0.25,0.5,0.75,1.0,1.25,1.5]
     #WHILE LOOP
#     r = 0
#     while r<2.5:
#          RADIUS.append(r)
#          r = r + 0.1

     for radius in RADIUS: 
#     for windowOpening in my_range(0, 200, 20):
#          radiusValues.append(radius)
#         if (windowOpening != 200):
#               windowOpeningValues.append(windowOpening)
#          else:
#               windowOpeningValues.append("NoCuts")

#          maxSignY = 0
#          maxSignX = 0
          
          x_bins = h_Signal.GetXaxis().GetNbins()
          y_bins = h_Signal.GetYaxis().GetNbins()
          

          #print windowOpening, h_Signal.GetYaxis().FindBin(yaxisWindowCenter-windowOpening)
#          if (windowOpening != 200):
          passBkg = 0
          passSignal = 0
          for xbin in range (0, x_bins-1):
               
               x_value = h_Signal.GetXaxis().GetBinLowEdge(xbin)+0.5*h_Signal.GetXaxis().GetBinWidth(xbin)

               
               for ybin in range (0, y_bins-1):

                    y_value = h_Signal.GetYaxis().GetBinLowEdge(ybin)+0.5*h_Signal.GetYaxis().GetBinWidth(ybin)
     
#                    if (x_value < 0): print x_value, y_value, xbin, ybin
                    if ( (x_value-3.14)*(x_value-3.14) + (y_value-3.14)*(y_value-3.14) < radius*radius ): continue

                    passBkg  = passBkg + h_Bkg.GetBinContent(xbin, ybin)
                    passSignal  = passSignal + h_Signal.GetBinContent(xbin,ybin)
#               passBkg    = h_Bkg.Integral(bin,bin, h_Bkg.GetYaxis().FindBin(yaxisWindowCenter-windowOpening), h_Bkg.GetYaxis().FindBin(yaxisWindowCenter+windowOpening) )
#               passSignal = h_Signal.Integral(bin, bin, h_Signal.GetYaxis().FindBin(yaxisWindowCenter-windowOpening), h_Signal.GetYaxis().FindBin(yaxisWindowCenter+windowOpening) )
#          print passBkg, passSignal, radius     
               ###FIXME SOTI
          if ((float(passBkg) <= 1 ) or (float(passSignal) <= 0)):
               significance = 0
          else:
               significance = float(passSignal)/math.sqrt(float(passBkg))
                    
                    
          x.append(radius)
          y.append(significance)
                    
                    # Find the Maximum Significance variables                                                                                                                               
#                    if (significance > maxSignY):
#                         maxSignY = significance
#                         maxSignX = x_value

               
     # Create the Significance Plot                                                                               
     tGraph = ROOT.TGraph(len(x), array.array("d", x), array.array("d", y))
     
     # Customize the Significance Plot       
     ytitle = "S/ #sqrt{B}"

     styleDict[signal_dataset.getName()].apply(tGraph)
     tGraph.SetName(signal_dataset.getName())
     tGraph.GetYaxis().SetTitle( ytitle + " /0.5" ) #%s" % (GetBinwidthDecimals(binWidth) % (binWidth) ))                                                     
     tGraph.GetXaxis().SetTitle("R_{#Delta #phi}")#h_signal.GetXaxis().GetTitle())                                                          
          #                                                                                                                  
     significanceGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)
     
     significancePlots = significanceGraph #FIXME
#          maxSignXvalues.append(maxSignX)
     

     return significancePlots

##Soti fix me!!!




####Plan B for R_DPHI radius Significance plot
def GetSignificance2D_DPhiRadius_wCuts(signal_dataset, background_dataset,  **kwargs):
     
     HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
     drawStyle    = kwargs.get("drawStyle")
     legStyle     = kwargs.get("legStyle")
     legName      = plots._legendLabels[signal_dataset.getName()]
     cutDirection = parseOpts.cutDirection
     verbose      = parseOpts.verbose
     normalizeTo = kwargs.get("normalizeTo")

     hNames2Ds_wCuts = [
          "DPhiJ34vsDPhiJ56",
          "DPhiJ34vsDPhiJ56_wCut025",
          "DPhiJ34vsDPhiJ56_wCut05",
          "DPhiJ34vsDPhiJ56_wCut075",
          "DPhiJ34vsDPhiJ56_wCut10",
          "DPhiJ34vsDPhiJ56_wCut125",
          "DPhiJ34vsDPhiJ56_wCut15",
          ]
     
     RADIUS = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
     radCounter = 0

     x=[]
     y=[]
          
     

     for hist in hNames2Ds_wCuts:

          # Get the ROOT histogram                                                                                                                                                                            
          rootHistoBkg    = background_dataset.getDatasetRootHisto(hist)
          rootHistoSignal = signal_dataset.getDatasetRootHisto(hist)

     # Normalise the histogram                                                                                                                                                                            
          NormalizeRootHisto(background_dataset, rootHistoBkg, background_dataset.isMC(), normalizeTo)
          NormalizeRootHisto(signal_dataset, rootHistoSignal, signal_dataset.isMC(), normalizeTo)
          
     # Get a clone of the wrapped histogram normalized as requested.                                                                                                                                      
          h_Bkg = rootHistoBkg.getHistogram()
          h_Signal = rootHistoSignal.getHistogram()
          
          
          x_bins = h_Signal.GetXaxis().GetNbins()
          y_bins = h_Signal.GetYaxis().GetNbins()

          passBkg = h_Bkg.Integral(0,x_bins,0, y_bins)
          passSignal = h_Signal.Integral(0,x_bins,0, y_bins)
     
          if ((float(passBkg) <= 1 ) or (float(passSignal) <= 0)):
               significance = 0
          else:
               significance = float(passSignal)/math.sqrt(float(passBkg))
               
               
          x.append(RADIUS[radCounter])
          y.append(significance)
          
          radCounter = radCounter + 1

               
     # Create the Significance Plot                                                                               
     tGraph = ROOT.TGraph(len(x), array.array("d", x), array.array("d", y))
     
     # Customize the Significance Plot       
     ytitle = "S/ #sqrt{B}"

     styleDict[signal_dataset.getName()].apply(tGraph)
     tGraph.SetName(signal_dataset.getName())
     tGraph.GetYaxis().SetTitle( ytitle + " /0.25" ) #%s" % (GetBinwidthDecimals(binWidth) % (binWidth) ))                                                     
     tGraph.GetXaxis().SetTitle("R_{#Delta #phi}")#h_signal.GetXaxis().GetTitle())                                                          
          #                                                                                                                  
     significanceGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)
     
     significancePlots = significanceGraph #FIXME
#          maxSignXvalues.append(maxSignX)
     

     return significancePlots

##Soti fix me!!!
def GetSignificance1D_DPhiDistance(signal_dataset, background_dataset, histoName,  **kwargs):
     
     HasKeys(["verbose", "drawStyle", "legStyle"], **kwargs)
     drawStyle    = kwargs.get("drawStyle")
     legStyle     = kwargs.get("legStyle")
     legName      = plots._legendLabels[signal_dataset.getName()]
     cutDirection = parseOpts.cutDirection
     verbose      = parseOpts.verbose
     normalizeTo = kwargs.get("normalizeTo")


      # Get the ROOT histogram                                                                                                                                                                            
     rootHistoBkg    = background_dataset.getDatasetRootHisto(histoName)
     rootHistoSignal = signal_dataset.getDatasetRootHisto(histoName)

     # Normalise the histogram                                                                                                                                                                            
     NormalizeRootHisto(background_dataset, rootHistoBkg, background_dataset.isMC(), normalizeTo)
     NormalizeRootHisto(signal_dataset, rootHistoSignal, signal_dataset.isMC(), normalizeTo)

     # Get a clone of the wrapped histogram normalized as requested.                                                                                                                                      
     h_Bkg = rootHistoBkg.getHistogram()
     h_Signal = rootHistoSignal.getHistogram()


     # For-loop: All possible (equal for both sides) window opening values                                                                              
     x=[]
     y=[]
          
     
     RADIUS = [0,0.25, 0.5,0.75, 1.0,1.25, 1.5,1.75,2.0,2.25, 2.5, 2.75, 3.0, 3.25, 3.5,3.75, 4.0,4.25,4.5]

     for radius in RADIUS: 
#     for windowOpening in my_range(0, 200, 20):
#          radiusValues.append(radius)

          x_bins = h_Signal.GetXaxis().GetNbins()

          

          #print windowOpening, h_Signal.GetYaxis().FindBin(yaxisWindowCenter-windowOpening)
#          if (windowOpening != 200):
          passBkg = 0
          passSignal = 0
          for xbin in range (0, x_bins-1):
               
               x_value = h_Signal.GetXaxis().GetBinLowEdge(xbin)+0.5*h_Signal.GetXaxis().GetBinWidth(xbin)

               if (x_value > radius ):               
                    passBkg  = passBkg + h_Bkg.GetBinContent(xbin)
                    passSignal  = passSignal + h_Signal.GetBinContent(xbin)
#               passBkg    = h_Bkg.Integral(bin,bin, h_Bkg.GetYaxis().FindBin(yaxisWindowCenter-windowOpening), h_Bkg.GetYaxis().FindBin(yaxisWindowCenter+windowOpening) )
#               passSignal = h_Signal.Integral(bin, bin, h_Signal.GetYaxis().FindBin(yaxisWindowCenter-windowOpening), h_Signal.GetYaxis().FindBin(yaxisWindowCenter+windowOpening) )
#          print passBkg, passSignal, radius     
               ###FIXME SOTI
          if ((float(passBkg) <= 1 ) or (float(passSignal) <= 0)):
               significance = 0
          else:
               significance = float(passSignal)/math.sqrt(float(passBkg))
                    
                    
          x.append(radius)
          y.append(significance)
                    
                    # Find the Maximum Significance variables                                                                                                                               
#                    if (significance > maxSignY):
#                         maxSignY = significance
#                         maxSignX = x_value

               
     # Create the Significance Plot                                                                               
     tGraph = ROOT.TGraph(len(x), array.array("d", x), array.array("d", y))
     
     # Customize the Significance Plot       
     ytitle = "S/ #sqrt{B}"

     styleDict[signal_dataset.getName()].apply(tGraph)
     tGraph.SetName(signal_dataset.getName())
     tGraph.GetYaxis().SetTitle( ytitle + " /0.5" ) #%s" % (GetBinwidthDecimals(binWidth) % (binWidth) ))                                                     
     tGraph.GetXaxis().SetTitle("R_{#Delta #phi}")#h_signal.GetXaxis().GetTitle())                                                          
          #                                                                                                                  
     significanceGraph = histograms.HistoGraph(tGraph, legName, legStyle, drawStyle)
     
     significancePlots = significanceGraph #FIXME
#          maxSignXvalues.append(maxSignX)
     

     return significancePlots

##Soti fix me!!!






def SetLogAndGrid(p, **kwargs):
     HasKeys(["createRatio", "logX", "logY", "gridX", "gridY"], **kwargs)
     ratio = kwargs.get("createRatio")
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
         


def SaveAs(p, savePath, saveName, saveFormats, verbose=True):

     Verbose("Saving plots in %s format(s)" % (len(saveFormats)))
     
     # For-loop: All formats to save file                                                                                                
     for ext in saveFormats:
          sName = saveName + ext
          # Change print name if saved under html                                                                             
          if "html" in sName:
               user    = getpass.getuser()
               initial = getpass.getuser()[0]
               sName   = sName.replace("/afs/cern.ch/user/%s/" % (initial), "http://cmsdoc.cern.ch/~")
               sName   = sName.replace("%s/public/html/" % (user), "%s/" % (user))
          elif "publicweb" in sName:
               user    = getpass.getuser()
               initial = getpass.getuser()[0]
               sName   = sName.replace("/publicweb/%s/%s/" % (initial, user), "http://home.fnal.gov/~%s/" % (user))
               
          # Print save name                                                                                                      
          print "\t", sName

          # Check if dir exists                                                                                                           
          if not os.path.exists(savePath):
               os.mkdir(savePath)

          # Save the plots                                                                                             
          p.saveAs(saveName, saveFormats)
     
     return







def main():
     
     style = tdrstyle.TDRStyle()
     
     # Set ROOT batch mode boolean
     ROOT.gROOT.SetBatch(parseOpts.batchMode)
     ROOT.gErrorIgnoreLevel = 3000

     # Get Verbose mode
     verbose = parseOpts.verbose
     
     # Get all datasets from the mcrab dir
     # All Datasets
     datasetsMgr  = GetDatasetsFromDir(parseOpts.mcrab, kwargs.get("analysis"))
     
     # Signal
     Signal_datasetsMgr = dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=kwargs.get("analysis"), includeOnlyTasks="ChargedHiggs_HplusTB_HplusToTB_M_", folder=parseOpts.folder) 

     # Background 1: QCD
     #Background1_datasetsMgr=dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=kwargs.get("analysis"), includeOnlyTasks= "QCD_HT1000to1500|QCD_HT1500to2000|QCD_HT2000toInf|QCD_HT300to500|QCD_HT500to700|QCD_HT700to1000", folder=parseOpts.folder)
     
     #Temporary background1,2
     Background1_datasetsMgr=dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=kwargs.get("analysis"), includeOnlyTasks= "TT", folder=parseOpts.folder)
     Background2_datasetsMgr=dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=kwargs.get("analysis"), includeOnlyTasks= "TT", folder=parseOpts.folder)
     
     # Background 2: (ELECTROWEAK)
#     Background2_datasetsMgr=dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=kwargs.get("analysis"), includeOnlyTasks= "DYJetsToQQ|ZJetsToQQ|WZ|WWTo4Q|WJetsToQQ_|ZZTo4Q", folder=parseOpts.folder)
     
     # Background 3: (TOP)
     Background3_datasetsMgr=dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=kwargs.get("analysis"), includeOnlyTasks="TT|ST_t|ttbb|TTZToQQ|TTWJetsToQQ|TTTT", folder=parseOpts.folder)
     
     # Background 4: (QCD+Top)
     Background4_datasetsMgr=dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=kwargs.get("analysis"), includeOnlyTasks= "QCD_HT1000to1500|QCD_HT1500to2000|QCD_HT2000toInf|QCD_HT300to500|QCD_HT500to700|QCD_HT700to1000|TT|ST_t|ttbb|TTZToQQ|TTWJetsToQQ|TTTT", folder=parseOpts.folder)


     #here
     # Background3_datasetsMgr=dataset.getDatasetsFromMulticrabDirs([parseOpts.mcrab], analysisName=kwargs.get("analysis"), includeOnlyTasks="TT", folder=parseOpts.folder)
     # Background3_datasetsMgr.remove("TTZToQQ")
     # Background3_datasetsMgr.remove("TTWJetsToQQ")
     # Background3_datasetsMgr.remove("TTTT")

     # Print the samples in each dataset category
     print "----------------------------------------------------------------"
     print "All Datasets:"
     for d in datasetsMgr.getAllDatasets():
          print "\t", d.getName()
     print "----------------------------------------------------------------"
     print "Signal Datasets:"
     for d in Signal_datasetsMgr.getAllDatasets():
          print "\t", d.getName()
     print "----------------------------------------------------------------"
     print "Background 1 (QCD) Datasets:"
     Background1Names = []
     for d in Background1_datasetsMgr.getAllDatasets():
          print "\t", d.getName()
          Background1Names.append(d.getName())
     print "----------------------------------------------------------------"
     print "Background 2 (Electroweak) Datasets:"
     Background2Names = []
     for d in Background2_datasetsMgr.getAllDatasets():
          print "\t", d.getName()
          Background2Names.append(d.getName())
     print "----------------------------------------------------------------"
     print "Background 3 (TOP) Datasets:"
     Background3Names = []
     for d in Background3_datasetsMgr.getAllDatasets():
          print "\t", d.getName()
          Background3Names.append(d.getName())
     print "----------------------------------------------------------------"
     print "Background 4 (QCD+TOP) Datasets:"
     Background4Names = []
     for d in Background4_datasetsMgr.getAllDatasets():
          print "\t", d.getName()
          Background4Names.append(d.getName())
     print "----------------------------------------------------------------"




     # Determine Integrated Luminosity
     intLumi = GetLumi(datasetsMgr)
     
     # Update to PU
     datasetsMgr.updateNAllEventsToPUWeighted()
     Signal_datasetsMgr.updateNAllEventsToPUWeighted()
     Background1_datasetsMgr.updateNAllEventsToPUWeighted()
     Background2_datasetsMgr.updateNAllEventsToPUWeighted()
     Background3_datasetsMgr.updateNAllEventsToPUWeighted()
     Background4_datasetsMgr.updateNAllEventsToPUWeighted()


     for d in Signal_datasetsMgr.getAllDatasets():
          if "ChargedHiggs" in d.getName():
               datasetsMgr.getDataset(d.getName()).setCrossSection(1.0)



     # Default merging & ordering: "Data", "QCD", "SingleTop", "Diboson"
     plots.mergeRenameReorderForDataMC(datasetsMgr) 
     #plots.mergeRenameReorderForDataMC(Signal_datasetsMgr) 
     #plots.mergeRenameReorderForDataMC(Background_datasetsMgr)
     
     # MergingTotalBackground     
     Background1_datasetsMgr.merge("QCD", Background1Names, False)
     Background2_datasetsMgr.merge("EWK", Background2Names, False)
     Background3_datasetsMgr.merge("Top", Background3Names, False)
     Background4_datasetsMgr.merge("QCD+Top", Background4Names, False)


     # Print datasets Info 
     datasetsMgr.PrintInfo()
     
     # Print merged samples
     if verbose:
          print "----------------------------------------------------------------"
          print "                      MERGED DATASETS                           "
          print "----------------------------------------------------------------"
          print "Merged all background 1 samples to one 'QCD' Dataset."
          for d in Background1_datasetsMgr.getAllDatasets():
               print "\t", d.getName()
          print "----------------------------------------------------------------"
          
          print "Merged all background 2 samples to one 'EWK (electroweak)' Dataset."
          for d in Background2_datasetsMgr.getAllDatasets():
               print "\t", d.getName()
          print "----------------------------------------------------------------"
          
          print "Merged all background 3 samples to one 'Top' Dataset."
          for d in Background3_datasetsMgr.getAllDatasets():                                                  
               print "\t", d.getName()                                                                                                 
          print "----------------------------------------------------------------"

          print "Merged all background 4 samples to one 'QCD+Top' Dataset."
          for d in Background4_datasetsMgr.getAllDatasets():
               print "\t", d.getName()
          print "----------------------------------------------------------------"


     # Get Datasets
 #    Signal_Dataset_180 = Signal_datasetsMgr.getDataset("ChargedHiggs_HplusTB_HplusToTB_M_180")
     Signal_Dataset_300 = Signal_datasetsMgr.getDataset("ChargedHiggs_HplusTB_HplusToTB_M_300")
     Signal_Dataset_200 = Signal_datasetsMgr.getDataset("ChargedHiggs_HplusTB_HplusToTB_M_200")
     Signal_Dataset_500 = Signal_datasetsMgr.getDataset("ChargedHiggs_HplusTB_HplusToTB_M_500")
     Signal_Dataset_800 = Signal_datasetsMgr.getDataset("ChargedHiggs_HplusTB_HplusToTB_M_800")
#     Signal_Dataset_1000 = Signal_datasetsMgr.getDataset("ChargedHiggs_HplusTB_HplusToTB_M_1000")
     Signal_Dataset_1000 = Signal_datasetsMgr.getDataset("ChargedHiggs_HplusTB_HplusToTB_M_2000")      #TEMPORARY
     Signal_Dataset_2000 = Signal_datasetsMgr.getDataset("ChargedHiggs_HplusTB_HplusToTB_M_2000")

     Background1_Dataset = Background1_datasetsMgr.getDataset("QCD")
     Background2_Dataset = Background2_datasetsMgr.getDataset("EWK")
     Background3_Dataset = Background3_datasetsMgr.getDataset("Top")
     Background4_Dataset = Background4_datasetsMgr.getDataset("QCD+Top")


     #================================================================================================                                 
     # Distributions for Signal and Background
     #================================================================================================

     print "==============================================================================================="
     print " Distributions (Signal & Background)"
     print "==============================================================================================="


     drawStyle    = kwargs.get("drawStyle")
     legStyle     = kwargs.get("legStyle")
     legName200   = plots._legendLabels[Signal_Dataset_200.getName()]
     legName300   = plots._legendLabels[Signal_Dataset_300.getName()]
     legName500   = plots._legendLabels[Signal_Dataset_500.getName()]
     legName800   = plots._legendLabels[Signal_Dataset_800.getName()]
     legName1000   = plots._legendLabels[Signal_Dataset_1000.getName()]
     legName2000   = plots._legendLabels[Signal_Dataset_2000.getName()]


     legNameBkg1  = "QCD"
     legNameBkg2  = "EWK"
     legNameBkg3  = "Top"   #"t#bar{t}"
     legNameBkg4  = "QCD+Top"
     legNameBkg5  = "QCD+TT"

     # For-loop: All Histogram names                                                                                                      
     for counter, hName in enumerate(hNames):
          
          # Get the save path and name                                                                     
          savePath, saveName = GetSavePathAndName(hName, **kwargs)
          if  (parseOpts.cutDirection == ">"):
               saveName1 = saveName.split("GreaterThan")[0]+"Distribution"
          if  (parseOpts.cutDirection == "<"):
               saveName1 = saveName.split("LessThan")[0]+"Distribution"

          # Get Root Histos from Datasets 
          rootHisto_200 = Signal_Dataset_200.getDatasetRootHisto(hName)
          rootHisto_300 = Signal_Dataset_300.getDatasetRootHisto(hName)
          rootHisto_500 = Signal_Dataset_500.getDatasetRootHisto(hName)
          rootHisto_800 = Signal_Dataset_800.getDatasetRootHisto(hName)
          rootHisto_1000 = Signal_Dataset_1000.getDatasetRootHisto(hName)
          rootHisto_2000 = Signal_Dataset_2000.getDatasetRootHisto(hName)
          
          rootHisto_Bkg1 = Background1_Dataset.getDatasetRootHisto(hName)
          rootHisto_Bkg2 = Background2_Dataset.getDatasetRootHisto(hName)
          rootHisto_Bkg3 = Background3_Dataset.getDatasetRootHisto(hName)
          rootHisto_Bkg4 = Background4_Dataset.getDatasetRootHisto(hName)


          # Normalize Root Histos                                                                        
          NormalizeRootHisto(Signal_Dataset_200, rootHisto_200, Signal_Dataset_200.isMC(), "One")               
          NormalizeRootHisto(Signal_Dataset_300, rootHisto_300, Signal_Dataset_300.isMC(), "One")
          NormalizeRootHisto(Signal_Dataset_500, rootHisto_500, Signal_Dataset_500.isMC(), "One")
          NormalizeRootHisto(Signal_Dataset_800, rootHisto_800, Signal_Dataset_800.isMC(), "One")
          NormalizeRootHisto(Signal_Dataset_1000, rootHisto_1000, Signal_Dataset_1000.isMC(), "One")
          NormalizeRootHisto(Signal_Dataset_2000, rootHisto_2000, Signal_Dataset_2000.isMC(), "One")
          NormalizeRootHisto(Background1_Dataset, rootHisto_Bkg1, Background1_Dataset.isMC(), "One")
          NormalizeRootHisto(Background2_Dataset, rootHisto_Bkg2, Background2_Dataset.isMC(), "One")
          NormalizeRootHisto(Background3_Dataset, rootHisto_Bkg3, Background3_Dataset.isMC(), "One")
          NormalizeRootHisto(Background4_Dataset, rootHisto_Bkg4, Background4_Dataset.isMC(), "One")



          # Get Histograms from Root Histos                                                          
          histo180 = rootHisto_200.getHistogram()
          histo300 = rootHisto_300.getHistogram()
          histo500 = rootHisto_500.getHistogram()
          histo800 = rootHisto_800.getHistogram()
          histo1000 = rootHisto_1000.getHistogram()
          histo2000 = rootHisto_2000.getHistogram()

          histoBkg1 = rootHisto_Bkg1.getHistogram()
          histoBkg2 = rootHisto_Bkg2.getHistogram()
          histoBkg3 = rootHisto_Bkg3.getHistogram()
          histoBkg4 = rootHisto_Bkg4.getHistogram()



          # Customize Histos 
          styles.signal200Style.apply(histo200)
          styles.signal300Style.apply(histo300)
          styles.signal500Style.apply(histo500)
          styles.signal800Style.apply(histo800)
          styles.signal2000Style.apply(histo1000)
          styles.signal2000Style.apply(histo2000)
          

          styles.ttbbStyle.apply(histoBkg1)
          histoBkg1.SetFillStyle(3001)
          histoBkg1.SetFillColor(ROOT.kPink-9)

          styles.ttStyle.apply(histoBkg2)
          histoBkg2.SetFillStyle(3001)
          histoBkg2.SetFillColor(ROOT.kViolet)
     
          styles.qcdBEnrichedStyle.apply(histoBkg3)
          histoBkg3.SetFillStyle(3001)
          histoBkg3.SetFillColor(ROOT.kOrange-3)
          
          styles.qcdBEnrichedStyle.apply(histoBkg4)
          histoBkg4.SetFillStyle(3001)
          histoBkg4.SetFillColor(ROOT.kOrange-3)


          

          # Rebin CSV histos                                                                                                          
          if "AvgCSV" in hName:
               histo180.Rebin(2)
               histo300.Rebin(2)
               histo500.Rebin(2)
               histoBkg1.Rebin(2)
               histoBkg2.Rebin(2)
               histoBkg3.Rebin(2)


          # Get the histos binWidth                                                                                                  
          binWidth = histo200.GetBinWidth(0)


          # Get Histos for Plotter                                                                 
          signal_histo_200 = histograms.Histo(histo200, legName200, legStyle, "p", "P")  #, "F", "HIST9")
          signal_histo_300 = histograms.Histo(histo300, legName300, legStyle, "p", "P")  #, "F", "HIST9")
          signal_histo_500 = histograms.Histo(histo500, legName500, legStyle, "p", "P")  #, "F", "HIST9")
          signal_histo_800 = histograms.Histo(histo800, legName800, legStyle, "p", "P")  #, "F", "HIST9")           
          signal_histo_1000 = histograms.Histo(histo1000, legName1000, legStyle, "p", "P")
          signal_histo_2000 = histograms.Histo(histo2000, legName2000, legStyle, "p", "P")  #, "F", "HIST9")  
          background1_histo = histograms.Histo(histoBkg1, legNameBkg1, "F", "HIST9" )
          background2_histo = histograms.Histo(histoBkg2, legNameBkg2, "F", "HIST9" )
          background3_histo = histograms.Histo(histoBkg3, legNameBkg3, "F", "HIST9" ) 
          background4_histo = histograms.Histo(histoBkg4, legNameBkg4, "F", "HIST9" )



          for background_histo in [background1_histo,background2_histo, background3_histo, background4_histo]:
               
               # Create a comparison plot                                                              
               #p = plots.ComparisonManyPlot(background_histo,[signal_histo_300, signal_histo_500])
               p = plots.ComparisonManyPlot(background_histo,[signal_histo_300, signal_histo_500, signal_histo_200, signal_histo_800, signal_histo_1000])
               
               # Set LogY on Yaxis for the distributions of some variables
               LogY_hNames=["dRMinDiJet_NoBJets_dR", "dRMinDiJet_NoBJets_dEta", "dRMinDiJet_NoBJets_dPhi"]

               # Create Frame and Set Log and Grid
               if hName not in LogY_hNames:
                    if kwargs.get("logY")==True:                                                                                    
                         opts = {"ymin": 1e-4, "ymaxfactor": 10}                                                                      
                    else:                                                                              
                         opts = {"ymin": 0.0, "ymaxfactor": 1.2}                                                      
                    ratioOpts = {"ymin": 0.0, "ymax": 0.004}                                                                      
                    p.createFrame(saveName1, createRatio=kwargs.get("createRatio"), opts=opts, opts2=ratioOpts)
                    SetLogAndGrid(p, **kwargs)
               else:
                    _kwargs= {"createRatio": False, "logX": False, "logY": True, "gridX": True, "gridY": True}                          
                    opts = {"ymin": 1e-3, "ymaxfactor": 1.2}                                  
                    ratioOpts = {"ymin": 0.0, "ymax": 0.004}
                    p.createFrame(saveName1, createRatio=_kwargs.get("createRatio"), opts=opts, opts2=ratioOpts)                          
                    p.getFrame().GetYaxis().SetRangeUser(1E-5,1.5)
                    SetLogAndGrid(p, **_kwargs)  
          

               # Customise Legend                                                                                                         
               moveLegend = {"dx": -0.1, "dy": -0.01, "dh": -0.1}
               p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
               

               # Customise frame                                                                    
               p.getFrame().GetYaxis().SetTitle( "Arbitrary Units / %s" % (GetBinwidthDecimals(binWidth) % (binWidth) ))
               p.getFrame().GetYaxis().SetLabelSize(18)
               p.getFrame().GetXaxis().SetLabelSize(20)
               # p.setEnergy("13")                                                                            
               if kwargs.get("createRatio"):
                    p.getFrame2().GetYaxis().SetTitle("Ratio")
                    p.getFrame2().GetYaxis().SetTitleOffset(1.6)
            

               # Customise axis titles                                                                                  
               if "_Pt" in hName:
                    #     p.getFrame().GetXaxis().SetTitle("p_{T} (GeV/c)")
                    if "recoJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("p_{T} of Jet "+hName.split("_")[0].split("Jet")[-1]+ " (GeV/c)")
                    elif "BJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("p_{T} of B-Jet "+hName.split("_")[0].split("BJet")[-1]+ " (GeV/c)")
               elif "_AbsEta" in hName:
                    if "recoJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("|#eta| of Jet "+hName.split("_")[0].split("Jet")[-1])
                    elif "BJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("|#eta| of B-Jet "+hName.split("_")[0].split("BJet")[-1]+ " (GeV/c)")
               
               if "AvgCSV" in hName:
                    p.getFrame().GetXaxis().SetTitle("Average CSV")
                    if "PtWeighted" in hName:
                         p.getFrame().GetXaxis().SetTitle("Average CSV (p_{T} weighted)")
                    if "PtSqrWeighted" in hName:
                         p.getFrame().GetXaxis().SetTitle("Average CSV (p_{T}^{2} weighted)")

               
               # Set X-axis range for some plots                                                                                      
               if (hName =="genMET_Et"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 120.0)
               if (hName == "MaxTriJetPt_dEtaMin"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 2.0)
               if (hName =="MaxTriJetPt_dRMin"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 2.5)
               if (hName == "MaxTriJetPt_dPhiMin"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0,1.0)
               if (hName == "ChiSqr"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 20.0)
               if (hName == "BJetPair_dRMax_Mass"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 1000.0)
               if (hName == "BJetPair_dRMin_Mass"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 1000.0)     
               if (hName =="recoJet7_Pt"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 120.0)


               # Add Standard Texts to plot
               histograms.addStandardTexts()

               # Move the refDataset to first in the draw order (back)                                             
               histoNames = [h.getName() for h in p.histoMgr.getHistos()]
               #p.histoMgr.reorder([signal_histo_180.getName(), signal_histo_300.getName(), signal_histo_500.getName(),signal_histo_800.getName(), signal_histo_2000.getName(), background_histo.getName()])
               p.histoMgr.reorder([signal_histo_300.getName(), signal_histo_500.getName(), background_histo.getName()]) 
               
               #  Draw plots                                                                                
               p.draw()
          
               # Save canvas under custom dir
               if (background_histo==background1_histo):
                    SaveAs(p, savePath, saveName1+"_Bkg1", kwargs.get("saveFormats"))
               elif (background_histo==background2_histo):
                    SaveAs(p, savePath, saveName1+"_Bkg2", kwargs.get("saveFormats"))
               elif (background_histo==background3_histo):
                    SaveAs(p, savePath, saveName1+"_Bkg3", kwargs.get("saveFormats"))
               elif (background_histo==background4_histo):
                    SaveAs(p, savePath, saveName1+"_Bkg4", kwargs.get("saveFormats"))

               if verbose:
                    print "**************************************************************************************************************"

     '''
     #================================================================================================                         
     # Efficiency Plots
     #================================================================================================ 
     print "==============================================================================================="
     print " Efficiency Plots ( "+parseOpts.cutDirection+" )"
     print "==============================================================================================="

     # For-Loop: Backgrounds
     for Background_Dataset in [Background1_Dataset, Background2_Dataset, Background3_Dataset, Background4_Dataset, Background5_Dataset,]:

          # For-loop: All Histogram names
          for hName in hNames:
               
               # Create a list for the efficiency plots
               EfficiencyPlots =[]
               
               # Get SavePath & SaveName
               savePath, saveName = GetSavePathAndName(hName, **kwargs)

               # Get the Efficiency Plot 
               effPlot180 = GetCutEfficiencyHisto(Signal_Dataset_200, hName, "kFNormal", **kwargs)
               effPlot300 = GetCutEfficiencyHisto(Signal_Dataset_300, hName, "kFNormal", **kwargs)
               effPlot500 = GetCutEfficiencyHisto(Signal_Dataset_500, hName, "kFNormal", **kwargs)
               effPlot800 = GetCutEfficiencyHisto(Signal_Dataset_800, hName, "kFNormal", **kwargs)
               effPlot1000 = GetCutEfficiencyHisto(Signal_Dataset_1000, hName, "kFNormal", **kwargs)
               effPlot2000 = GetCutEfficiencyHisto(Signal_Dataset_2000, hName, "kFNormal", **kwargs)
               

               effPlotBkg = GetCutEfficiencyHisto(Background_Dataset, hName, "kFNormal", **kwargs)
    

               # Add the efficiency plots to the list for plotting
               EfficiencyPlots=[effPlotBkg, effPlot300, effPlot500, effPlot800, effPlot1000]
               # EfficiencyPlots=[effPlotBkg, effPlot180, effPlot300, effPlot500, effPlot800, effPlot2000] 

               # Create the plot with all the efficiency plots 
               p = plots.PlotBase(EfficiencyPlots, kwargs.get("saveFormats"))
               

               # Create a frame
               opts      = {"ymin": 0.0, "ymaxfactor": 1.1} 
               p.createFrame(saveName, opts=opts)
               
               # Customise Legend
               moveLegend = {"dx": -0.1, "dy": -0.01, "dh": -0.1}
               p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

              
               # Customise frame
               p.setEnergy("13")
               p.getFrame().GetYaxis().SetLabelSize(18)
               p.getFrame().GetXaxis().SetLabelSize(20)
               if kwargs.get("createRatio"):
                    p.getFrame2().GetYaxis().SetTitle("Ratio")
                    p.getFrame2().GetYaxis().SetTitleOffset(1.6)


               # Customise axis titles
               if "_Pt" in hName:
                    p.getFrame().GetXaxis().SetTitle("p_{T} (GeV/c)")
                    if "recoJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("p_{T} of Jet "+hName.split("_")[0].split("Jet")[-1]+ " (GeV/c)")
                    if "BJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("p_{T} of B-Jet "+hName.split("_")[0].split("BJet")[-1]+ " (GeV/c)")
               elif "_AbsEta" in hName:
                    if "recoJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("|#eta| of Jet "+hName.split("_")[0].split("Jet")[-1])
                    elif "BJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("|#eta| of B-Jet "+hName.split("_")[0].split("BJet")[-1]+ " (GeV/c)")


               if "AvgCSV" in hName:
                    p.getFrame().GetXaxis().SetTitle("Average CSV")
                    if "PtWeighted" in hName:
                         p.getFrame().GetXaxis().SetTitle("Average CSV (p_{T} weighted)")
                    if "PtSqrWeighted" in hName:
                         p.getFrame().GetXaxis().SetTitle("Average CSV (p_{T}^{2} weighted)")


                         
               # Set X-axis range to some plots 
               if (hName =="genMET_Et"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 120.0)
               if (hName == "MaxTriJetPt_dEtaMin"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 2.0)
               if (hName =="MaxTriJetPt_dRMin"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 2.5)
               if (hName == "MaxTriJetPt_dPhiMin"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 1.0)
               if (hName == "ChiSqr"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 20.0)
               if (hName == "BJetPair_dRMax_Mass"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 1000.0)
               if (hName == "BJetPair_dRMin_Mass"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 1000.0)
               if (hName =="recoJet7_Pt"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 120.0)


               # SetLog 
               SetLogAndGrid(p, **kwargs)

               # Add Standard Texts to plot
               histograms.addStandardTexts()

               #  Draw plots
               p.draw()

               # Save canvas under custom dir
               if (Background_Dataset==Background1_Dataset):
                    SaveAs(p, savePath, saveName+"Efficiency_Bkg1", kwargs.get("saveFormats"))
               elif (Background_Dataset==Background2_Dataset):
                    SaveAs(p, savePath, saveName+"Efficiency_Bkg2", kwargs.get("saveFormats"))
               elif (Background_Dataset==Background3_Dataset):
                    SaveAs(p, savePath, saveName+"Efficiency_Bkg3", kwargs.get("saveFormats"))
               elif (Background_Dataset==Background4_Dataset):
                    SaveAs(p, savePath, saveName+"Efficiency_Bkg4", kwargs.get("saveFormats"))
               elif (Background_Dataset==Background5_Dataset):
                    SaveAs(p, savePath, saveName+"Efficiency_Bkg5", kwargs.get("saveFormats"))

               if verbose:
                    print "**************************************************************************************************************"


   

     #================================================================================================                         
     # Optimisation Plots
     #================================================================================================ 
     print "==============================================================================================="
     print " Optimisation Plots ( "+parseOpts.cutDirection+" )"
     print "==============================================================================================="

     # For-Loop: Backgrounds
     for Background_Dataset in [Background1_Dataset, Background2_Dataset, Background3_Dataset]:

          # For-loop: All Histogram names
          for hName in hNames:
               
               # Create a list for the significance plots
               OptimisationPlots =[]
               
               # Get SavePath & SaveName
               savePath, saveName = GetSavePathAndName(hName, **kwargs)

               # Get the Significance Plot and the value of maximum significance
               optPlot180, maxSignX180 = GetOptimisationPlot(Signal_Dataset_180, Background_Dataset, hName, **kwargs)
               optPlot300, maxSignX300 = GetOptimisationPlot(Signal_Dataset_300, Background_Dataset, hName, **kwargs)
               optPlot500, maxSignX500 = GetOptimisationPlot(Signal_Dataset_500, Background_Dataset, hName, **kwargs)
               optPlot800, maxSignX800 = GetOptimisationPlot(Signal_Dataset_800, Background_Dataset, hName, **kwargs)
               optPlot2000, maxSignX2000 = GetOptimisationPlot(Signal_Dataset_2000, Background_Dataset, hName, **kwargs)
               
               # Add the significance plots to the list for plotting
               OptimisationPlots=[optPlot300 ,optPlot500]
               # OptimisationPlots=[optPlot180, optPlot300 ,optPlot500, optPlot800, optPlot2000]
 
               # Create the plot with all the significance plots 
               p = plots.PlotBase(OptimisationPlots, kwargs.get("saveFormats"))
               

               # Create a frame
               opts      = {"ymin": 1E-4, "ymaxfactor": 1.2} 
               p.createFrame(saveName, opts=opts)
               
               # Customise Legend
               moveLegend = {"dx": -0.1, "dy": -0.01, "dh": -0.1}
               p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

              
               # Customise frame
               p.setEnergy("13")
               p.getFrame().GetYaxis().SetLabelSize(18)
               p.getFrame().GetXaxis().SetLabelSize(20)
               if kwargs.get("createRatio"):
                    p.getFrame2().GetYaxis().SetTitle("Ratio")
                    p.getFrame2().GetYaxis().SetTitleOffset(1.6)


               # Customise axis titles
               if "_Pt" in hName:
                    p.getFrame().GetXaxis().SetTitle("p_{T} (GeV/c)")
                    if "recoJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("p_{T} of Jet "+hName.split("_")[0].split("Jet")[-1]+ " (GeV/c)")
                    if "BJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("p_{T} of B-Jet "+hName.split("_")[0].split("BJet")[-1]+ " (GeV/c)")
               elif "_AbsEta" in hName:
                    if "recoJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("|#eta| of Jet "+hName.split("_")[0].split("Jet")[-1])
                    elif "BJet" in hName:
                         p.getFrame().GetXaxis().SetTitle("|#eta| of B-Jet "+hName.split("_")[0].split("BJet")[-1]+ " (GeV/c)")
               
               if "AvgCSV" in hName:
                    p.getFrame().GetXaxis().SetTitle("Average CSV")
                    if "PtWeighted" in hName:
                         p.getFrame().GetXaxis().SetTitle("Average CSV (p_{T} weighted)")
                    if "PtSqrWeighted" in hName:
                         p.getFrame().GetXaxis().SetTitle("Average CSV (p_{T}^{2} weighted)")



               # Set X-axis range to some plots 
               if (hName =="genMET_Et"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 120.0)
               if (hName == "MaxTriJetPt_dEtaMin"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 2.0)
               if (hName =="MaxTriJetPt_dRMin"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 2.5)
               if (hName == "MaxTriJetPt_dPhiMin"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 1.0)
               if (hName == "ChiSqr"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 20.0)
               if (hName == "BJetPair_dRMax_Mass"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 1000.0)
               if (hName == "BJetPair_dRMin_Mass"):
                    p.getFrame().GetXaxis().SetRangeUser(0.0, 1000.0)
                    
               # SetLog 
               _kwargs= {"createRatio": False, "logX": False, "logY": False, "gridX": True, "gridY": True}
               #if (parseOpts.significanceDef=="S1"):
               #     p.getFrame().GetYaxis().SetRangeUser(1,1E4)
               #else:
               #     p.getFrame().GetYaxis().SetRangeUser(1E-2,1E2)
               SetLogAndGrid(p, **_kwargs)

          

               # Add cut line/box
               _kwargs = { "lessThan": kwargs.get("cutLessThan")}
               #p.addCutBoxAndLine(cutValue=maxSignX180, fillColor=kwargs.get("cutFillColour"), lineColor=ROOT.kAzure+9, box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs) 
               p.addCutBoxAndLine(cutValue=maxSignX300, fillColor=kwargs.get("cutFillColour"), lineColor=ROOT.kMagenta+2,box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs)
               p.addCutBoxAndLine(cutValue=maxSignX500, fillColor=kwargs.get("cutFillColour"), lineColor=ROOT.kBlue, box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs) 
               #p.addCutBoxAndLine(cutValue=maxSignX800, fillColor=kwargs.get("cutFillColour"), lineColor=ROOT.kPink-3,box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs)
               #p.addCutBoxAndLine(cutValue=maxSignX2000, fillColor=kwargs.get("cutFillColour"), lineColor=ROOT.kSpring+9, box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs)

               # Add Standard Texts to plot
               histograms.addStandardTexts()
                              
               #  Draw plots
               p.draw()

          
               # Save canvas under custom dir
               if (Background_Dataset==Background1_Dataset):
                    SaveAs(p, savePath, saveName+"_Bkg1_"+parseOpts.significanceDef, kwargs.get("saveFormats"))
               elif (Background_Dataset==Background2_Dataset):
                    SaveAs(p, savePath, saveName+"_Bkg2_"+parseOpts.significanceDef, kwargs.get("saveFormats"))
               elif (Background_Dataset==Background3_Dataset):
                    SaveAs(p, savePath, saveName+"_Bkg3_"+parseOpts.significanceDef, kwargs.get("saveFormats"))

               if verbose:
                    print "**************************************************************************************************************"

     #================================================================================================                         
     # Significance for window cut on Top Mass
     #================================================================================================ 
     print "==============================================================================================="
     print " Top Mass Cut - Significance Plots ( "+parseOpts.cutDirection+" )"
     print "==============================================================================================="


     windowCenter = 172.5
    

     # For-Loop: Backgrounds
     for Background_Dataset in [Background1_Dataset, Background2_Dataset, Background3_Dataset, Background4_Dataset]:

          # For-loop: All Histogram names
          for hName in ["LdgTop_Mass", "SubLdgTop_Mass"]:
    
               # Create a list for the significance plots
               TopMassSignificancePlots = []
               TopMassEfficiencyPlots   = []

               # Get SavePath & SaveName
               savePath, saveName = GetSavePathAndName(hName, **kwargs)

               # Get the Significance Plot and the value of maximum significance for all the window cut openings
               topMassSign300, maxSignX300 = GetSignificanceForCutWithinWindow(Signal_Dataset_300, Background_Dataset, hName, windowCenter, **kwargs)
               topMassSign500, maxSignX500 = GetSignificanceForCutWithinWindow(Signal_Dataset_500, Background_Dataset, hName, windowCenter, **kwargs)

               # Add the significance plots to the list for plotting
               TopMassSignificancePlots =[topMassSign300, topMassSign500]

               # Get the Significance Plot and the value of maximum significance for all the window cut openings                                                                 
               topMassEff300  = GetEfficiencyForCutWithinWindow(Signal_Dataset_300 , hName, windowCenter, **kwargs)
               topMassEff500  = GetEfficiencyForCutWithinWindow(Signal_Dataset_500 , hName, windowCenter, **kwargs)
               topMassEff800  = GetEfficiencyForCutWithinWindow(Signal_Dataset_800 , hName, windowCenter, **kwargs)
               topMassEff1000 = GetEfficiencyForCutWithinWindow(Signal_Dataset_1000, hName, windowCenter, **kwargs)
               topMassEffBkg  = GetEfficiencyForCutWithinWindow(Background_Dataset , hName, windowCenter, **kwargs)

               # Add the efficiency plots to the list for plotting                                                                                                                                      
               TopMassEfficiencyPlots =[topMassEff300, topMassEff500, topMassEff800, topMassEff1000, topMassEffBkg]

               # Create the plot with all the significance plots 
               #p = plots.PlotBase(TopMassSignificancePlots, kwargs.get("saveFormats"))
               
               # Create the plot with all the significance plots                                                                                                                                          
               p1 = plots.PlotBase(TopMassEfficiencyPlots, kwargs.get("saveFormats"))


               # Create a frame
               opts      = {"ymin": 1E-4, "ymaxfactor": 1.2} 
               #p.createFrame(saveName, opts=opts)
               p1.createFrame(saveName, opts=opts)

               # Customise Legend
               moveLegend = {"dx": -0.1, "dy": -0.5, "dh": -0.1}
               #p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
               p1.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))
               
              
               # Customise frame
               #p.setEnergy("13")
               #p.getFrame().GetYaxis().SetLabelSize(18)
               #p.getFrame().GetXaxis().SetLabelSize(20)
               #if kwargs.get("createRatio"):
               #     p.getFrame2().GetYaxis().SetTitle("Ratio")
               #     p.getFrame2().GetYaxis().SetTitleOffset(1.6)
               p1.setEnergy("13")
               p1.getFrame().GetYaxis().SetRangeUser(0, 1.02)
               p1.getFrame().GetYaxis().SetLabelSize(18)
               p1.getFrame().GetXaxis().SetLabelSize(20)
               if kwargs.get("createRatio"):
                    p1.getFrame2().GetYaxis().SetTitle("Ratio")
                    p1.getFrame2().GetYaxis().SetTitleOffset(1.6)


                    

                    
               # SetLog 
               _kwargs= {"createRatio": False, "logX": False, "logY": False, "gridX": True, "gridY": True}
               #SetLogAndGrid(p, **_kwargs)
               SetLogAndGrid(p1, **_kwargs)


               # Add cut line/box
               _kwargs = { "lessThan": kwargs.get("cutLessThan")}
               #p.addCutBoxAndLine(cutValue=maxSignX300, fillColor=kwargs.get("cutFillColour"), lineColor=ROOT.kMagenta+2,box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs)
               #p.addCutBoxAndLine(cutValue=maxSignX500, fillColor=kwargs.get("cutFillColour"), lineColor=ROOT.kBlue, box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs) 



               # Add Standard Texts to plot
               histograms.addStandardTexts()
                              
               #  Draw plots
               #p.draw()
               p1.draw()
          
               # Save canvas under custom dir                                                                                                                                                             
               if (Background_Dataset==Background1_Dataset):
                    SaveAs(p1, savePath, saveName+"_WindowCutEfficiency_Bkg1", kwargs.get("saveFormats"))
               elif (Background_Dataset==Background2_Dataset):
                    SaveAs(p1, savePath, saveName+"_WindowCutEfficiency_Bkg2", kwargs.get("saveFormats"))
               elif (Background_Dataset==Background3_Dataset):
                    SaveAs(p1, savePath, saveName+"_WindowCutEfficiency_Bkg3", kwargs.get("saveFormats"))
               elif (Background_Dataset==Background4_Dataset):
                    SaveAs(p1, savePath, saveName+"_WindowCutEfficiency_Bkg4", kwargs.get("saveFormats"))



               if verbose:
                    print "**************************************************************************************************************"
     #================================================================================================                         
     # Significance 2D
     #================================================================================================ 
     print "==============================================================================================="
     print " Significance Plots for 2D( "+parseOpts.cutDirection+" )"
     print "==============================================================================================="

     windowCenter = 172.5


     # For-Loop: Backgrounds
     for Background_Dataset in [Background1_Dataset, Background2_Dataset, Background3_Dataset, Background4_Dataset]:

          # For-loop: All Histogram names
          for hName in hNames2D:
               
               # Create a list for the significance plots
               SignificancePlots2D =[]
               MaxSignXvalues=[]
               windowOpeningValues=[]

               # Get SavePath & SaveName
               savePath, saveName = GetSavePathAndName(hName+"Sign2D", **kwargs)

               # Get the Significance Plot and the value of maximum significance
               SignificancePlots2D,MaxSignXvalues, windowOpeningValues = GetSignificance2DwithWindowOpening(Signal_Dataset_300, Background_Dataset, hName, windowCenter, **kwargs) 


               # Add the significance plots to the list for plotting
               #SignificancePlots2D =[sign2D_800, sign2D_800]
               
               for plot in SignificancePlots2D:

                    position = SignificancePlots2D.index(plot)
                    windowOpening = windowOpeningValues[position]
                    #print position, windowOpening

                    # Create the plot with all the significance plots 
                    #p = plots.PlotBase(SignificancePlots2D, kwargs.get("saveFormats"))
                    p = plots.PlotBase([plot], kwargs.get("saveFormats"))

                    # Create a frame
                    opts      = {"ymin": 1E-4, "ymaxfactor": 1.2} 
                    p.createFrame(saveName, opts=opts)
               
                    # Customise Legend
                    moveLegend = {"dx": -0.1, "dy": -0.01, "dh": -0.1}
                    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

              
                    # Customise frame
                    p.getFrame().GetYaxis().SetRangeUser(0,2) #M=300, 500
                    #p.getFrame().GetYaxis().SetRangeUser(0,7) #M=800, 1000
                    p.setEnergy("13")
                    p.getFrame().GetYaxis().SetLabelSize(18)
                    p.getFrame().GetXaxis().SetLabelSize(20)
                    if kwargs.get("createRatio"):
                         p.getFrame2().GetYaxis().SetTitle("Ratio")
                         p.getFrame2().GetYaxis().SetTitleOffset(1.6)

                    
                    # SetLog 
                    _kwargs= {"createRatio": False, "logX": False, "logY": False, "gridX": True, "gridY": True}
                    SetLogAndGrid(p, **_kwargs)


                    # Add cut line/box
                    _kwargs = { "lessThan": kwargs.get("cutLessThan")}
                    p.addCutBoxAndLine(cutValue=MaxSignXvalues[position], fillColor=kwargs.get("cutFillColour"), lineColor=ROOT.kMagenta+2,box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs)
                    #p.addCutBoxAndLine(cutValue=maxSignX1000, fillColor=kwargs.get("cutFillColour"), lineColor=ROOT.kBlue, box=kwargs.get("cutBox"), line=kwargs.get("cutLine"), **_kwargs) 
                    


                    # Add Standard Texts to plot
                    histograms.addStandardTexts()
                              
                    #  Draw plots
                    p.draw()
          
                    # Save canvas under custom dir
                    if (Background_Dataset==Background1_Dataset):
                         SaveAs(p, savePath, saveName+"_Bkg1_w"+str(windowOpening)+"_M300", kwargs.get("saveFormats"))
                    elif (Background_Dataset==Background2_Dataset):
                         SaveAs(p, savePath, saveName+"_Bkg2_w"+str(windowOpening)+"_M300", kwargs.get("saveFormats"))
                    elif (Background_Dataset==Background3_Dataset):
                         SaveAs(p, savePath, saveName+"_Bkg3_w"+str(windowOpening)+"_M300", kwargs.get("saveFormats"))
                    elif (Background_Dataset==Background4_Dataset):
                         SaveAs(p, savePath, saveName+"_Bkg4_w"+str(windowOpening)+"_M300", kwargs.get("saveFormats"))


               if verbose:
                    print "**************************************************************************************************************"




     return
     
     '''
     windowCenter = 172.5
     #================================================================================================                         
     # Significance 2D
     #================================================================================================ 
     print "==============================================================================================="
     print " Significance Plots for 2D( "+parseOpts.cutDirection+" )"
     print "==============================================================================================="

     # For-Loop: Backgrounds
     for Background_Dataset in [Background1_Dataset, Background2_Dataset, Background3_Dataset, Background4_Dataset]:

          # For-loop: All Histogram names
          for hName in hNames2D:
               
               # Create a list for the significance plots

               SignificancePlots2D = []
               MaxSignXvalues=[]
               windowOpeningValues=[]

               # Get SavePath & SaveName
               savePath, saveName = GetSavePathAndName(hName+"Sign2D", **kwargs)
#               savePath, saveName = GetSavePathAndName(hName+"Sign1Ddistance", **kwargs)
               histo1d = "DPhiDistance_J34_J56"
               SignificancePlots2D.append(GetSignificance1D_DPhiDistance(Signal_Dataset_200, Background_Dataset, histo1d, **kwargs) )
               SignificancePlots2D.append(GetSignificance1D_DPhiDistance(Signal_Dataset_300, Background_Dataset, histo1d, **kwargs) )
               SignificancePlots2D.append(GetSignificance1D_DPhiDistance(Signal_Dataset_500, Background_Dataset, histo1d, **kwargs) )

               # Get the Significance Plot and the value of maximum significance
#               SignificancePlots2D.append(GetSignificance2D_DPhiRadius(Signal_Dataset_200, Background_Dataset, hName,  **kwargs) )
#               SignificancePlots2D.append(GetSignificance2D_DPhiRadius(Signal_Dataset_300, Background_Dataset, hName,  **kwargs) )
#               SignificancePlots2D.append(GetSignificance2D_DPhiRadius(Signal_Dataset_500, Background_Dataset, hName,  **kwargs) )
                              # Add the significance plots to the list for plotting

#               OptimisationPlots=[optPlot300 ,optPlot500]
#               # OptimisationPlots=[optPlot180, optPlot300 ,optPlot500, optPlot800, optPlot2000]
 
#               # Create the plot with all the significance plots 
##               p = plots.PlotBase(OptimisationPlots, kwargs.get("saveFormats"))


               
               # Add the significance plots to the list for plotting
               #SignificancePlots2D =sign2D_800, sign2D_800]
               
#               for plot in SignificancePlots2D:
               if (1):
#               for plot in SignificancePlots2D:
                    p=plots.PlotBase(SignificancePlots2D,kwargs.get("saveFormats"))
#                    plot = SignificancePlots2D

                    # Create the plot with all the significance plots             
                    #p = plots.PlotBase(SignificancePlots2D, kwargs.get("saveFormats"))                       
##                    p = plots.PlotBase([plot], kwargs.get("saveFormats"))                                                                                                                                               

                    # Create a frame
                    opts      = {"ymin": 1E-4, "ymaxfactor": 1.2} 
                    p.createFrame(saveName, opts=opts)
               
                    # Customise Legend
                    moveLegend = {"dx": -0.1, "dy": -0.01, "dh": -0.1}
                    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))

              
                    # Customise frame
                    p.setEnergy("13")
                    p.getFrame().GetYaxis().SetLabelSize(18)
                    p.getFrame().GetXaxis().SetLabelSize(20)
                    if kwargs.get("createRatio"):
                         p.getFrame2().GetYaxis().SetTitle("Ratio")
                         p.getFrame2().GetYaxis().SetTitleOffset(1.6)

                    
                    # SetLog 
                    _kwargs= {"createRatio": False, "logX": False, "logY": False, "gridX": True, "gridY": True}
                    SetLogAndGrid(p, **_kwargs)


                    # Add cut line/box
                    _kwargs = { "lessThan": kwargs.get("cutLessThan")}

                    # Add Standard Texts to plot
                    histograms.addStandardTexts()
                              
                    #  Draw plots
                    p.draw()
               
                    # Save canvas under custom dir
               if (Background_Dataset==Background1_Dataset):
                    SaveAs(p, savePath, saveName+"_Bkg1", kwargs.get("saveFormats"))
               elif (Background_Dataset==Background2_Dataset):
                    SaveAs(p, savePath, saveName+"_Bkg2", kwargs.get("saveFormats"))
               elif (Background_Dataset==Background3_Dataset):
                    SaveAs(p, savePath, saveName+"_Bkg3", kwargs.get("saveFormats"))
               elif (Background_Dataset==Background4_Dataset):
                    SaveAs(p, savePath, saveName+"_Bkg4", kwargs.get("saveFormats"))


               if verbose:
                    print "**************************************************************************************************************"


               SignificancePlots2D_wCuts = GetSignificance2D_DPhiRadius_wCuts(Signal_Dataset_200, Background_Dataset,  **kwargs)
               SignificancePlots2D_wCuts = GetSignificance2D_DPhiRadius_wCuts(Signal_Dataset_300, Background_Dataset,  **kwargs)
               SignificancePlots2D_wCuts = GetSignificance2D_DPhiRadius_wCuts(Signal_Dataset_500, Background_Dataset,  **kwargs)

               if (1):

                    plot = SignificancePlots2D_wCuts
                    
                    p = plots.PlotBase([plot], kwargs.get("saveFormats"))
                    
                    # Create a frame                                                                                                                                                                                                                                                                                                
                    opts      = {"ymin": 1E-4, "ymaxfactor": 1.2}
                    p.createFrame(saveName, opts=opts)

                    # Customise Legend                                                                                                                                                                                                                                                                                              
                    moveLegend = {"dx": -0.1, "dy": -0.01, "dh": -0.1}
                    p.setLegend(histograms.moveLegend(histograms.createLegend(), **moveLegend))


                    # Customise frame                                                                                                                                                                                                                                                                                               
                    p.setEnergy("13")
                    p.getFrame().GetYaxis().SetLabelSize(18)
                    p.getFrame().GetXaxis().SetLabelSize(20)
                    if kwargs.get("createRatio"):
                         p.getFrame2().GetYaxis().SetTitle("Ratio")
                         p.getFrame2().GetYaxis().SetTitleOffset(1.6)


                    # SetLog                                                                                                                                                               
                    _kwargs= {"createRatio": False, "logX": False, "logY": False, "gridX": True, "gridY": True}
                    SetLogAndGrid(p, **_kwargs)


                    # Add cut line/box                                                                                                                                                                                               
                    _kwargs = { "lessThan": kwargs.get("cutLessThan")}

                    # Add Standard Texts to plot                                                                                                                                                                                                                                 
                    histograms.addStandardTexts()

                    #  Draw plots                                                                                                                                                                       

                    p.draw()
                    # Save canvas under custom dir                                                                                                                                                                                                        

                    if (Background_Dataset==Background1_Dataset):
                         SaveAs(p, savePath, saveName+"_Bkg1_M300wCuts", kwargs.get("saveFormats"))
                    elif (Background_Dataset==Background2_Dataset):
                         SaveAs(p, savePath, saveName+"_Bkg2_M300wCuts", kwargs.get("saveFormats"))
                    elif (Background_Dataset==Background3_Dataset):
                         SaveAs(p, savePath, saveName+"_Bkg3_M300wCuts", kwargs.get("saveFormats"))
                    elif (Background_Dataset==Background4_Dataset):
                         SaveAs(p, savePath, saveName+"_Bkg4_M300wCuts", kwargs.get("saveFormats"))


               
     return




#================================================================================================
# Main
#================================================================================================
if __name__ == "__main__":
#if __name__ in ["__main__":
    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False ,conflict_handler="resolve")
    parser.add_option("-m", "--mcrab"    , dest="mcrab"    , action="store", help="Path to the multicrab directory for input")
    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=True, help="Enables batch mode (canvas creation does NOT generates a window)")
    parser.add_option("-v", "--verbose"  , dest="verbose"  , action="store_true", default=False, help="Enables verbose mode (for debugging purposes)")
    parser.add_option("-i", "--includeTasks", dest="includeTasks" , default="", type="string",   help="Only perform action for this dataset(s) [default: '']")

    parser.add_option("-e", "--excludeTasks", dest="excludeTasks" , default="", type="string",   help="Exclude this dataset(s) from action [default: '']")
    parser.add_option("-c", "--cutDirection", dest="cutDirection" , default=">", type="string",   help="Define the cut direction >,<")
    parser.add_option("-s", "--significanceDef", dest="significanceDef" , default="S1", type="string",   help="Define the significance definition [S1=S/sqrt(B) , S2=S/B]")

    parser.add_option("-f", "--folder", dest="folder" , default=None, type="string",   help="Define whether to plot histos or TTree branches")
    parser.add_option("-a", "--alpha", dest="alpha" , default=0.01, type="string",   help="Define the significance level for chi^2")


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
         
