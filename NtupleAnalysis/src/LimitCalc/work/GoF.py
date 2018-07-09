#!/usr/bin/env python
'''
DESCRIPTION:
Plots goodness-of-fit plots
See https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#Goodness_of_fit_tests
for more details.


USAGE:
cd <datacards_dir>
./GoF.sh 500 <algorithm>
python GoF.py [opts]


EXAMPLES:
cd <datacards_dir>
./GoF.sh 500 saturated
python GoF.py --h2tb --algo saturated --mass 500


LAST USED:
python GoF.py --h2tb --algo saturated && cp GoF.png ~/public/html/tmp/.

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import ROOT
import sys
import os
from subprocess import call, check_output
from optparse import OptionParser

import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
import HiggsAnalysis.NtupleAnalysis.tools.histograms as histograms


#================================================================================================ 
# Function definition
#================================================================================================ 
def Verbose(msg, printHeader=False):
    '''
    Calls Print() only if verbose options is set to true
    '''
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return

def Print(msg, printHeader=True):
    '''
    Simple print function. If verbose option is enabled prints, otherwise does nothing.
    '''
    fName = __file__.split("/")[-1]
    if printHeader:
        print "=== ", fName
    print "\t", msg
    return

def main(opts):
    
    # Apply TDR style
    style = tdrstyle.TDRStyle()
    ROOT.gErrorIgnoreLevel = ROOT.kFatal # [Options: Print, kInfo, kWarning, kError, kBreak, kSysError, kFatal]
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)

    # Settings
    if opts.h2tb:
        analysis = "H^{+}#rightarrow tb fully hadronic"
    else:
        analysis = "H^{+}#rightarrow#tau_{h}#nu fully hadronic"
    
    # Hadd ROOT files
    if not os.path.isfile(opts.fileName):
        Print("Merging ROOT files", True)
        #call("hadd higgsCombineToys.GoodnessOfFit.mH120.root higgsCombinetoys*.GoodnessOfFit.mH120.*.root", shell=True)
        call("hadd %s %s" % (opts.fileName, opts.fileName.replace(".", "*.")), shell=True)
    else: 
        Print("Merge ROOT file already exists", True)
        
    # Perform GoF calculations
    fToys = ROOT.TFile(opts.fileName)
    fData = ROOT.TFile(opts.fileName)
    tToys = fToys.Get("limit")
    tData = fData.Get("limit")
    nToys = tToys.GetEntries()

    if opts.verbose:
        tData.Print()
    Verbose("NData = %.1f, NToys = %.1f" % (tData.GetEntries(), tToys.GetEntries()), False)
    tData.GetEntry(0)
    GoF_DATA = tData.limit
    Verbose(GoF_DATA, True)

    # Setting (Toys)
    GoF_TOYS_TOT = 0
    pval   = 0
    toys   = []
    minToy = +99999999
    maxToy = -99999999

    # For-loop: All toys
    for i in range(0, tToys.GetEntries()):
        tToys.GetEntry(i)

        # Toys counter
        GoF_TOYS_TOT += tToys.limit
        toys.append(tToys.limit)

        if tToys.limit > GoF_DATA: 
            pval += tToys.limit

    # Calculate p-value
    pval = pval / GoF_TOYS_TOT

    # Create GoF histo & fill it
    hist = ROOT.TH1D("GoF", "", 50, round(min(toys)), round(max(toys)))
    # For-loop: Toys
    for k in toys: 
        hist.Fill(k)

    # Customise canvas & histogram
    c = ROOT.TCanvas("canvas", "canvas")
    hist.GetYaxis().SetTitle("Entries")
    hist.GetXaxis().SetTitle("#chi^{2}_{%s}" % (opts.algorithm) )
    hist.SetLineColor(ROOT.kRed)
    hist.SetLineWidth(3)
    hist.Draw()

    # Customise arrow indicating data-observed
    arr = ROOT.TArrow(GoF_DATA, 0.0001, GoF_DATA, hist.GetMaximum()/8, 0.02, "<|")
    arr.SetLineColor(ROOT.kBlue)
    arr.SetFillColor(ROOT.kBlue)
    arr.SetFillStyle(1001)
    arr.SetLineWidth(3)
    arr.SetLineStyle(1)
    arr.SetAngle(60)
    arr.Draw("<|same")

    # Add data observed value
    left = ROOT.TLatex()
    #left.SetNDC()
    left.SetTextFont(43)
    left.SetTextSize(22)
    left.SetTextAlign(11)
    left.DrawLatex(GoF_DATA*0.9, (hist.GetMaximum()/8.0)*1.05, "#color[4]{data_{obs}}")

    # Analysis text
    anaText = ROOT.TLatex()
    anaText.SetNDC()
    anaText.SetTextFont(43)
    anaText.SetTextSize(22)
    anaText.SetTextAlign(31) 
    anaText.DrawLatex(0.92, 0.86, analysis)

    # p-value
    pvalText = ROOT.TLatex()
    pvalText.SetNDC()
    pvalText.SetTextFont(43)
    pvalText.SetTextSize(22)
    pvalText.SetTextAlign(31) #11
    pvalText.DrawLatex(0.92, 0.80, "# toys: %d" % nToys)
    pvalText.DrawLatex(0.92, 0.75, "p-value: %.2f" % pval)

    # Print some info
    Print("Toys = %.0f" % (nToys), True)
    Print("p-value = %.2f" % (pval), False)

    # Add default texts
    histograms.addStandardTexts(lumi=opts.lumi, sqrts="13 TeV", addCmsText=True, cmsTextPosition=None, cmsExtraTextPosition=None, cmsText="CMS", cmsExtraText="Internal   ")
    #histograms.addStandardTexts(lumi=opts.lumi, sqrts="13 TeV", addCmsText=True, cmsTextPosition=None, cmsExtraTextPosition=None, cmsText="CMS", cmsExtraText="Preliminary")

    # For-loop: Formats
    for i, ext in enumerate(opts.formats, 0):
        saveName = "GoF" + ext
        Print("Saving %s" % (saveName), i==0)
        c.SaveAs(saveName)
    return

#================================================================================================ 
# Function definition
#================================================================================================ 
if __name__ == "__main__":

    # Default Values
    HELP          = False
    VERBOSE       = False
    HToTB         = False
    MASS          = 120
    FILENAME      = None
    LUMI          = 35900 #pb-1
    FORMATS       = [".png", ".C", ".pdf"]
    ALGORITHM     = "saturated"

    # Object for selecting data eras, search modes, and optimization modes
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=False, conflict_handler="resolve")

    parser.add_option("-h", "--help", dest="helpStatus", action="store_true", default=HELP, 
                      help="Show this help message and exit [default: %s]" % HELP)

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE,
                      help="Print more information [default: %s]" % (VERBOSE) )

    parser.add_option("--h2tb", dest="h2tb", action="store_true", default=HToTB,
                      help="Flag to indicate that settings should reflect h2tb analysis [default: %s]" % (HToTB) )

    parser.add_option("-f", "--fileName", dest="fileName", default=FILENAME,
                      help="Name of ROOT file to use as input  [default: %s]" % (FILENAME) )

    parser.add_option("-m", "--mass", dest="mass", default=MASS,
                      help="Mass point to use [default: %s]" % (MASS) )

    parser.add_option("--lumi", dest="lumi", default=LUMI,
                      help="Integrated luminosity [default: %s]" % (LUMI) )

    parser.add_option("-a", "--algorithm", dest="algorithm", default=ALGORITHM,
                      help="Name of algorithm used in the goodness-of-fit test [default: %s]" % (ALGORITHM) )


    (opts, args) = parser.parse_args()

    opts.formats = FORMATS

    # https://cms-hcomb.gitbooks.io/combine/content/part3/commonstatsmethods.html#goodness-of-fit-tests
    allowedAlgos = ["saturated", "KS", "AD"] # KS = Kolmogorov-Smirnov, AD = Anderson-Darling
    if opts.algorithm not in allowedAlgos:
        raise Exception("The algorithm \"%s\" is invalid. Please select one of the following: %s" % (opts.algorithm, ", ".join(allowedAlgos)))
        
    if opts.fileName == None:
        opts.fileName = "higgsCombineToys.GoodnessOfFit.mH%s.root" % opts.mass

    Print("Using ROOT file \"%s\" as input" % (opts.fileName), True)
    main(opts)
