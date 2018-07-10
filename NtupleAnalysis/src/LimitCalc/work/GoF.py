#!/usr/bin/env python
'''
DESCRIPTION:
Plots goodness-of-fit plots
See https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#Goodness_of_fit_tests
for more details.


USAGE:
cd <datacards_dir>
./GoF.sh 500 <algorithm>
cd GoF_<algo>
python ../../../GoF.py [opts]


EXAMPLES:
cd <datacards_dir>
./GoF.sh 500 saturated && ./GoF.sh 500 AD && ./GoF.sh 500 KS
cd GoF_saturated
python ../../../GoF.py --h2tb --mass 180 && python ../../../GoF.py --h2tb --mass 500


LAST USED:
cd GoF_AD/
python ../../../GoF.py --h2tb --mass 180 && cp GoF_*.png ~/public/html/tmp/.

'''

#================================================================================================ 
# Imports
#================================================================================================ 
import ROOT
import sys
import os
import glob
import shutil
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


def CleanFiles(opts):
    if not opts.clean:
        return
        
    dirName  = "lxbatch"
    fullPath = os.path.join(os.getcwd(), dirName)
    if not os.path.exists("%s" % (fullPath)):
        os.mkdir(fullPath)
        
    bMatchJob  = False
    bMatchRoot = False
    for fname in os.listdir('.'):
        if fname.startswith('job_'):
            bMatchJob = True
            break
        if fname.startswith('higgsCombinetoys') and fname.endswith(".root"):
            bMatchRoot = True
            break

    if bMatchJob:
        Print("Cleaning auxiliary \"job\" files (lxbatch job) by moving them to a dedicated directory \"%s\"" % (dirName), True)
        srcFiles = "job_*.*"
        call("mv %s %s" % (srcFiles, fullPath), shell=True)

    if bMatchRoot:
        Print("Cleaning auxiliary \"ROOT\" files (lxbatch job) by moving them to a dedicated directory \"%s\"" % (dirName), True)
        call("mv %s %s" % (opts.inputfile, fullPath), shell=True )
    return


def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    ROOT.gErrorIgnoreLevel = ROOT.kFatal # [Options: Print, kInfo, kWarning, kError, kBreak, kSysError, kFatal]
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetNdivisions(5, "X")

    # Settings
    if opts.h2tb:
        analysis = "H^{+}#rightarrow tb fully hadronic"
    else:
        analysis = "H^{+}#rightarrow#tau_{h}#nu fully hadronic"
    
    # Hadd ROOT files
    rootFiles = glob.glob1(os.getcwd(), "higgsCombinetoys*.root")
    if len(rootFiles) > 0:
        if not os.path.isfile(opts.outputfile):
            Print("Merging \"%s\" ROOT files into \"%s\"" % (opts.inputfile, opts.inputfile), True)
            call("hadd %s %s" % (opts.outputfile, opts.inputfile), shell=True)
    
    # Clean auxiliary jobs files?
    CleanFiles(opts)
        
    # Perform GoF calculations
    if not os.path.isfile(opts.outputfile):
        raise Exception("The output ROOT file \"%s\" does not exist!" % (opts.outputfile) )
    else:
        Print("Opening merged ROOT file \"%s\" to read results" % (opts.outputfile), True)
    fToys = ROOT.TFile(opts.outputfile)
    fData = ROOT.TFile(opts.outputfile)
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
    Verbose("Toys = %.0f" % (nToys), True)
    Verbose("p-value = %.2f" % (pval), False)

    # Add default texts
    histograms.addStandardTexts(lumi=opts.lumi, sqrts="13 TeV", addCmsText=True, cmsTextPosition=None, cmsExtraTextPosition=None, cmsText="CMS", cmsExtraText="Internal   ")
    #histograms.addStandardTexts(lumi=opts.lumi, sqrts="13 TeV", addCmsText=True, cmsTextPosition=None, cmsExtraTextPosition=None, cmsText="CMS", cmsExtraText="Preliminary")

    # For-loop: Formats
    for i, ext in enumerate(opts.formats, 0):
        saveName = "GoF_m%s_%s%s" % (opts.mass, opts.algorithm, ext)
        Print("%s" % (saveName), i==0)
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
    INPUTFILE     = None
    OUTPUTFILE    = None
    LUMI          = 35900 #pb-1
    FORMATS       = [".png", ".C", ".pdf"]
    ALGORITHM     = "saturated"
    CLEAN         = False

    # Object for selecting data eras, search modes, and optimization modes
    parser = OptionParser(usage="Usage: %prog [options]", add_help_option=False, conflict_handler="resolve")

    parser.add_option("-h", "--help", dest="help", action="store_true", default=HELP, 
                      help="Show this help message and exit [default: %s]" % HELP)

    parser.add_option("--clean", dest="clean", action="store_true", default=CLEAN, 
                      help="Move all GoF.sh output (lxbatch) to a dedicated directory [default: %s]" % CLEAN)

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE,
                      help="Print more information [default: %s]" % (VERBOSE) )

    parser.add_option("--h2tb", dest="h2tb", action="store_true", default=HToTB,
                      help="Flag to indicate that settings should reflect h2tb analysis [default: %s]" % (HToTB) )

    parser.add_option("--inputfile", dest="inputfile", default=INPUTFILE,
                      help="Name of ROOT file to use as input (of hadd command) [default: %s]" % (INPUTFILE) )

    parser.add_option("--outputfile", dest="outputfile", default=OUTPUTFILE,
                      help="Name of ROOT file to use as output (of hadd command)  [default: %s]" % (OUTPUTFILE) )

    parser.add_option("-m", "--mass", dest="mass", default=MASS,
                      help="Mass point to use [default: %s]" % (MASS) )

    parser.add_option("--lumi", dest="lumi", default=LUMI,
                      help="Integrated luminosity [default: %s]" % (LUMI) )

    #parser.add_option("-a", "--algorithm", dest="algorithm", default=ALGORITHM,
    #                  help="Name of algorithm used in the goodness-of-fit test [default: %s]" % (ALGORITHM) )


    (opts, args) = parser.parse_args()

    opts.formats = FORMATS

    # Determine current working directory and hence the algorithm used for the GoF results
    # https://cms-hcomb.gitbooks.io/combine/content/part3/commonstatsmethods.html#goodness-of-fit-tests
    cwd = os.path.basename(os.getcwd())
    opts.algorithm = cwd.split("_")[-1]
    allowedAlgos   = ["saturated", "KS", "AD"] # KS = Kolmogorov-Smirnov, AD = Anderson-Darling
    if opts.algorithm not in allowedAlgos:
        raise Exception("The algorithm \"%s\" is invalid. Expected one of the following: %s" % (opts.algorithm, ", ".join(allowedAlgos)))
        
    if opts.inputfile == None:
        opts.inputfile = "higgsCombinetoys*.GoodnessOfFit.mH%s.*.root" % opts.mass

    if opts.outputfile == None:
        #opts.outputfile = "GoodnessOfFit_mH%s.root" % opts.mass
        opts.outputfile = "GoF_%s_mH%s.root" % (opts.algorithm, opts.mass)

    Verbose("Using ROOT file(s) \"%s\" as input" % (opts.inputfile), True)
    main(opts)
