#!/usr/bin/env python
'''
Help:
./plotBRvMass.py --help


Usage:
1) root -l
2) root [0] .L mssm_xs_tools.C+
3) root [1] .q
4) ./plotBRvMass.py -f 13TeV/mhmodm_mu200_13TeV.root -t 5 -l 80 -u 170 -v
or
4) ./plotBRvMass.py --file mhmodp_mu200_13TeV.root --tanbeta 5 --massMin 80 --massMax 170 --verbose
[NOTE: Steps 1)->3) only need to be done once (creates/compiles required C++ libraries).]


for comparison:
./plotBRvMass.py -f 13TeV/newmhmax_mu200_13TeV.root -l 100 -u 600 -t 10


for AN (light):
./plotBRvMass.py -f 13TeV/mhmodm_mu200_13TeV.root -l 80 -u 160 -t 10 && ./plotBRvMass.py -f 13TeV/mhmodp_mu200_13TeV.root -l 80 -u 160 -t 10
./plotBRvMass.py -f 13TeV/mhmodm_mu200_13TeV.root -l 80 -u 160 -t 20 && ./plotBRvMass.py -f 13TeV/mhmodp_mu200_13TeV.root -l 80 -u 160 -t 20
./plotBRvMass.py -f 13TeV/mhmodm_mu200_13TeV.root -l 80 -u 160 -t 30 && ./plotBRvMass.py -f 13TeV/mhmodp_mu200_13TeV.root -l 80 -u 160 -t 30
./plotBRvMass.py -f 13TeV/newmhmax_mu200_13TeV.root -l 80 -u 160 -t 10
./plotBRvMass.py -f 13TeV/newmhmax_mu200_13TeV.root -l 80 -u 160 -t 20
./plotBRvMass.py -f 13TeV/newmhmax_mu200_13TeV.root -l 80 -u 160 -t 30


for AN (heavy):
./plotBRvMass.py -f 13TeV/mhmodm_mu200_13TeV.root -l 160 -u 2000 -t 10 && ./plotBRvMass.py -f 13TeV/mhmodp_mu200_13TeV.root -l 160 -u 2000 -t 10
./plotBRvMass.py -f 13TeV/mhmodm_mu200_13TeV.root -l 160 -u 2000 -t 20 && ./plotBRvMass.py -f 13TeV/mhmodp_mu200_13TeV.root -l 160 -u 2000 -t 20
./plotBRvMass.py -f 13TeV/mhmodm_mu200_13TeV.root -l 160 -u 2000 -t 30 && ./plotBRvMass.py -f 13TeV/mhmodp_mu200_13TeV.root -l 160 -u 2000 -t 30
./plotBRvMass.py -f 13TeV/newmhmax_mu200_13TeV.root -l 160 -u 2000 -t 10
./plotBRvMass.py -f 13TeV/newmhmax_mu200_13TeV.root -l 160 -u 2000 -t 20
./plotBRvMass.py -f 13TeV/newmhmax_mu200_13TeV.root -l 160 -u 2000 -t 30


Links:
https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHXSWGMSSMNeutral#ROOT_histograms_MSSM_benchmark_s
https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHXSWGMSSMNeutral#Access_tool_for_the_ROOT_files
https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHXSWGCrossSectionsFigures#MSSM_BR_plots


ROOT files: 
wget https://twiki.cern.ch/twiki/pub/LHCPhysics/HXSWG3LowTanB/low-tb-high_13TeV.root
wget https://twiki.cern.ch/twiki/pub/LHCPhysics/HXSWG3LowTanB/hMSSM_13TeV.root
wget https://twiki.cern.ch/twiki/pub/LHCPhysics/LHCHXSWGMSSMNeutral/newmhmax_mu200_13TeV.root
wget https://twiki.cern.ch/twiki/pub/LHCPhysics/LHCHXSWGMSSMNeutral/mhmodp_mu200_13TeV.root
wget https://twiki.cern.ch/twiki/pub/LHCPhysics/LHCHXSWGMSSMNeutral/mhmodm_13TeV.root
...
[see: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHXSWGMSSMNeutral#ROOT_histograms_MSSM_benchmark_s]


macOS: 
self.lib = cdll.LoadLibrary('./mssm_xs_tools_C.so')  # fails! macOS needs absolute path
'''

#================================================================================================
# Import Modules
#================================================================================================
import sys
import os
from optparse import OptionParser
from ctypes import cdll
from ctypes import c_bool
from ctypes import c_uint
from ctypes import c_double
from array import array
import string

import ROOT
from ROOT import TCanvas
from ROOT import gStyle
from ROOT import gROOT
from ROOT import TFile

import tdrstyle as tdrstyle


#================================================================================================
# Options
#================================================================================================
yLog = True
xLog = False
yMin = 1e-04
yMax = 1.1
#savePath    = os.getcwd()
savePath    = "/afs/cern.ch/user/a/attikis/public/html/brPlots/"
saveFormats = ["png", "pdf", "C"]
Colours     = {}
Colours["AA"]    = ROOT.kGray+2
Colours["AW"]    = ROOT.kMagenta
Colours["HW"]    = ROOT.kOrange
Colours["SUSY"]  = ROOT.kCyan-5
Colours["WHp"]   = ROOT.kTeal-3
Colours["WW"]    = ROOT.kOrange-7
Colours["ZA"]    = ROOT.kMagenta+2
Colours["ZZ"]    = ROOT.kOrange-9
Colours["Zgam"]  = ROOT.kMagenta+3
Colours["Zh"]    = ROOT.kRed-5
Colours["bb"]    = ROOT.kRed
Colours["cb"]    = ROOT.kGreen
Colours["cc"]    = ROOT.kOrange+3
Colours["cs"]    = ROOT.kBlack
Colours["dd"]    = ROOT.kYellow+1
Colours["ee"]    = ROOT.kMagenta-7
Colours["enu"]   = ROOT.kViolet-6
Colours["gamgam"]= ROOT.kMagenta-2
Colours["gluglu"]= ROOT.kYellow+1
Colours["hW"]    = ROOT.kGreen+3
Colours["hh"]    = ROOT.kBlack
Colours["mumu"]  = ROOT.kSpring-8
Colours["munu"]  = ROOT.kCyan
Colours["ss"]    = ROOT.kAzure+7
Colours["taunu"] = ROOT.kBlue
Colours["tautau"]= ROOT.kBlue
Colours["tb"]    = ROOT.kRed
Colours["tt"]    = ROOT.kTeal-3
Colours["us"]    = ROOT.kGray+1
Colours["uu"]    = ROOT.kMagenta+2

    
#================================================================================================
# Class definition
#================================================================================================
class PlotText:
    '''
    Constructor takes the following parameters:
    \param x       X coordinate of the text (in NDC)
    \param y       Y coordinate of the text (in NDC)
    \param text    String to draw
    \param size    Size of text (None for the default value, taken from gStyle)
    \param bold    Should the text be bold?
    \param align   Alignment of text (left, center, right)
    \param color   Color of the text
    \param font    Specify font explicitly
    '''
    def __init__(self, x, y, text, size=None, bold=True, align="left", color=ROOT.kBlack, font=None):
        self.x = x
        self.y = y
        self.text = text

        self.l = ROOT.TLatex()
        self.l.SetNDC()
        if not bold:
            self.l.SetTextFont(self.l.GetTextFont()-20) # bold -> normal
        if font is not None:
            self.l.SetTextFont(font)
        if size is not None:
            self.l.SetTextSize(size)
        if isinstance(align, basestring):
            if align.lower() == "left":
                self.l.SetTextAlign(11)
            elif align.lower() == "center":
                self.l.SetTextAlign(21)
            elif align.lower() == "right":
                self.l.SetTextAlign(31)
            else:
                raise Exception("Error: Invalid option '%s' for text alignment! Options are: 'left', 'center', 'right'."%align)
        else:
            self.l.SetTextAlign(align)
        self.l.SetTextColor(color)

    def Draw(self, options=None):
        '''
        Draw the text to the current TPad
        
        \param options   For interface compatibility, ignored
        Provides interface compatible with ROOT's drawable objects.
        '''
        self.l.DrawLatex(self.x, self.y, self.text)    
        return
        

class mssm_xs_tools(object):
    """
    Class mssm_xs_tools:
      
    This is a python wrapper class to make the core functionality of mssm_xs_tools available also 
    in python. 
    
    """
    def __init__(self, filename, kINTERPOLATION, verbosity):
        ## pointer to the shared library containing the C wrapper functions
        self.lib = cdll.LoadLibrary('./mssm_xs_tools_C.so') # macOS needs aboslute paths
        
        ## pointer to the C++ object
        self.obj = self.lib.mssm_xs_tools_new(filename, c_bool(kINTERPOLATION), c_uint(verbosity))

        ## pointer to function mass
        self.mssm_xs_tools_mass = self.lib.mssm_xs_tools_mass
        self.mssm_xs_tools_mass.restype = c_double

        ## pointer to function width
        self.mssm_xs_tools_width = self.lib.mssm_xs_tools_width
        self.mssm_xs_tools_width.restype = c_double

        ## pointer to function br
        self.mssm_xs_tools_br = self.lib.mssm_xs_tools_br
        self.mssm_xs_tools_br.restype = c_double

        ## pointer to function xsec
        self.mssm_xs_tools_xsec = self.lib.mssm_xs_tools_xsec
        self.mssm_xs_tools_xsec.restype = c_double
         
    def mass(self, boson, mA, tanb):
        return self.mssm_xs_tools_mass(self.obj, boson, c_double(mA), c_double(tanb))

    def width(self, boson, mA, tanb):
        return self.mssm_xs_tools_width(self.obj, boson, c_double(mA), c_double(tanb))

    def br(self, decay, mA, tanb):
        return self.mssm_xs_tools_br(self.obj, decay, c_double(mA), c_double(tanb))

    def xsec(self, mode, mA, tanb):
        return self.mssm_xs_tools_xsec(self.obj, mode, c_double(mA), c_double(tanb))


#================================================================================================
# Function Definition
#================================================================================================
def Print(msg, printHeader=False):
    if printHeader:
        print "=== mssm_xs_tools.py:\n\t", msg
    else:
        print "\t", msg 
    return


def SaveCanvas(canvas, saveFormats, savePath, parseOpts):
    '''
    Save & close canvas in the desired formats and to 
    the desired path.
    '''
    fName = GetSaveName(parseOpts)
    # For-loop: All save formats
    for f in saveFormats:
        saveName = savePath + "%s.%s" % (fName, f) 
        canvas.SaveAs(saveName)
    canvas.Close()
    return


def GetSaveName(parseOpts):
    '''
    Returns the name to be used for saving the canvas, 
    including all input parameters values.
    '''
    name = parseOpts.file.split("/")[-1].replace(".root", "")
    name += "_tanb" + parseOpts.tanb
    name += "_"     + parseOpts.boson 
    name += "_m"    + parseOpts.massMin
    name += "to"    + parseOpts.massMax
    return name


def GetListSize(listOfLists):
    '''
    Ensure that all lists in the given list have same size.
    Return the (common) list size
    '''

    lSize = len(listOfLists[0])
    # For-loop: All lists    
    for l in listOfLists:
        
        tmpSize = len(l)
        if tmpSize != lSize:
            Print("ERROR! Arrays have different size (%s != %s)" % (tmpSize, lSize) )
            sys.exit()
        else:
            continue
    return lSize


def Verbose(msg, printHeader=True):
    if parseOpts.verbose == False:
        return
    else:
        Print(msg)
    return


def ConvertFileToScenario(fileName):
    '''
    Use input file to determine the scenario used to 
    generate the Branching Ratios.
    '''

    name = fileName.split("/")[-1]
    name = name.replace(".root" , "")
    name = name.replace("_8TeV" , "")
    name = name.replace("_13TeV", "")
    name = name.replace("_14TeV", "")
    name = name.replace("tauphobic", "#tau-phobic")
    name = name.replace("mhmodp"   , "m_{h}^{mod+}")
    name = name.replace("mhmodm"   , "m_{h}^{mod-}")
    name = name.replace("newmhmax" , "m_{h}^{max}") #(upd.)
    name = name.replace("hMSSM"    , "MSSM")
    name = name.replace("_mu200"   , "") #", #mu=200")
    name = name.replace("MSSM"          , "MSSM")    
    name = name.replace("lightstau1"    , "light stau")

    scenario = name + " scenario"
    return scenario


def ConvertToLatex(text):
    '''
    Convert special characters to LaTeX format for plotting purposes.
    '''
    Verbose("Converting normal text (%s) to LaTeX format" % (text))

    # Single replacements & Special cases
    if text == "H":
        return "H^{0}"
    elif text == "AW":
        return "A^{0}W^{+}"
    elif text == "hW":
        return "h^{0}W^{+}"
    elif text == "HW":
        return "H^{0}W^{+}"
    elif text == "Zgam":
        return "Z^{0}#gamma"
    elif text == "Zh":
        return "Z^{0}h^{0}"
    elif text == "ZZ":
        return "Z^{0}Z^{0}"
    elif text == "AA":
        return "A^{0}A^{0}"
    else:
        pass

    # Other cases
    text = text.replace("Hp"     , "H^{+}")
    text = text.replace("enu"    , "e^{+}#nu_{e}")
    text = text.replace("munu"   , "#mu^{+}#nu_{#mu}")
    text = text.replace("taunu"  , "#tau^{+}#nu_{#tau}")
    text = text.replace("us"     , "u#bar{s}")
    text = text.replace("cb"     , "c#bar{b}")
    text = text.replace("cs"     , "c#bar{s}")
    text = text.replace("tb"     , "t#bar{b}")
    text = text.replace("ee"     , "e^{+}e^{-}")
    text = text.replace("mumu"   , "#mu^{+}#mu^{-}")
    text = text.replace("tautau" , "#tau^{+}#tau^{-}")
    text = text.replace("gluglu" , "gg")
    text = text.replace("gamgam" , "#gamma#gamma")
    return text


def GetKeyNames(f, folder = "" ):
    '''
    Loop over all objects in a ROOT file. Return a list.
    '''
    Verbose("Getting list of key-names from folder \"%s\" in ROOT file %s" % (folder, f.GetName()))
    f.cd(folder)
    return [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]


def GetListOfHistoNames(f, higgs):
    '''
    Returns the list of BR/Decays available for a given mother list.
    '''
    Verbose("Getting list of histogram names (non-zero integral) from ROOT file %s" % (f.GetName()) )
    decays = []

    # Get all objects in the ROOT file
    keyList = GetKeyNames(f, "")

    # For-loop: All objects in the ROOT file
    for key in keyList:
            
        # If key not BR of interest skip it
        if 'br_' + higgs + '_' not in key:
            continue

        # Get the decay and corresponding BR [2D histogram with x = mass, y=tan(beta), z=BR]
        decay = key.split("_")[-1]
        hist  = f.Get(key)
            
        # Skip decays with zero BR 
        if hist.Integral() <= 0.0:
            pass
        else:
           decays.append(key)
    return decays


def PrintTable(mom, decayTo, massValues, brValues):
    '''
    Print table of higgs mass and BR for a given channel.
    '''
    Verbose("Printing decays table")

    # Construct the msg list & title format
    msgList  = []
    txtAlign = "{:<20} {:<20}"
    title    = txtAlign.format("Mass (GeV)", "B(%s -> %s)" % (mom, decayTo))
    hLine    = "="*40

    # Append title to message list
    msgList.append(hLine)
    msgList.append(title)
    msgList.append(hLine)
    
    # For-loop: Two lists simultaneously
    for m, br in zip(massValues, brValues):
        msg = txtAlign.format(m, br)
        msgList.append(msg)

    # For-loop: All messages to be printed
    for m in msgList:
        print m
    print

    return


def CustomiseGraph(gr, grName, colour, gTitle, xTitle, yTitle):
    '''
    Customise TGraphs according to input parameters.
    '''
    gr.SetName("TGraph_" + grName)
    Verbose("Customising TGraph with name %s" % (gr.GetName()))

    # General
    gr.SetTitle(gTitle)
    gr.GetXaxis().SetTitle(xTitle)
    gr.GetYaxis().SetTitle(yTitle)
    
    # Marker Style
    gr.SetMarkerColor(colour)
    gr.SetMarkerStyle(ROOT.kFullCircle)
    gr.SetMarkerSize(0.0)

    # Line Style
    gr.SetLineWidth(3)
    gr.SetLineColor(colour)      
    gr.SetLineStyle(ROOT.kSolid) 
    
    # Fill Style
    gr.SetFillColor(colour)
    gr.SetFillStyle(3001)

    return   


def main():
    '''
    The main function.
    '''
    
    # Setup the correct style
    Print("Setting the TDR style", True)
    style = tdrstyle.TDRStyle()
        
    # Global Setting: Sets max digits permitted for the axis labels (above this notation with 10^N is used)
    ROOT.TGaxis.SetMaxDigits(10)

    # Set ROOT batch mode boolean
    Print("Batch-Mode is set to %s" % (parseOpts.batchMode))
    ROOT.gROOT.SetBatch(parseOpts.batchMode)

    # Create an access tools object to calculate stuff
    Print("Using file %s, tan(beta) = %s, higgs = %s" % (parseOpts.file, parseOpts.tanb, parseOpts.boson) )
    mssm = mssm_xs_tools(parseOpts.file, True, 0)

    # Open ROOT file
    Print("Opening ROOT file %s" % (parseOpts.file) )
    f = ROOT.TFile(parseOpts.file)
    energy = parseOpts.file.split("/")[0]

    # For-loop: All available higgs bosons
    histoNames = GetListOfHistoNames(f, parseOpts.boson)

    # Create canvas
    cName = "TCanvas_" + parseOpts.boson + "_tanb" + parseOpts.tanb
    Print("Creating canvas with name %s" % (cName) )
    c1 = ROOT.TCanvas(cName, cName)
    c1.cd()
    
    # Create & Customise a TMultiGraph
    Print("Creating  TMultiGraph")
    mGraph = ROOT.TMultiGraph()
    xTitle = "m_{"+ ConvertToLatex(parseOpts.boson) +"} [GeV]"
    yTitle = "BR("+ ConvertToLatex(parseOpts.boson) + ")"
    mGraph.SetTitle("; %s ; %s" % (xTitle, yTitle) )

    # Create & Customise a TLegend
    Print("Creating  TMultiGraph")
    leg = ROOT.TLegend(0.65, 0.45, 0.92, 0.92)
    leg.SetFillColor(0)
    leg.SetFillStyle(3002)
    leg.SetBorderSize(0)

    # For-loop: All decays for given boson
    for hName in histoNames:

        massList    = []
        brList      = []

        # Get the TH2 from the ROOT file (x=mass, y=tan(beta), z=BR)
        hist = f.Get(hName)

        # Get the X in the decay (Higgs->X)
        decayTo = hName.split("_")[-1]

        # For-loop: All available mass values (ignore zero-bin)
        for x in range(1, hist.GetNbinsX()+1):
            
            # Get x- and y-values of histogram
            mass = hist.GetXaxis().GetBinCenter(x)
            br   = mssm.br(parseOpts.boson + "->" + decayTo, mass, float(parseOpts.tanb))
              
            # Apply mass cut-off values
            if mass < float(parseOpts.massMin):
                continue
            if mass > float(parseOpts.massMax):
                break

            # If decay outside range don't add it!
            if br < yMin:
                continue 

            # Save mass/br values to a list
            massList.append(mass)
            brList.append(br)

        # Sanity check
        nPoints = GetListSize([massList, brList])

        # Skip empty decays
        if nPoints < 1:
            continue

        # Create arrays compatible with TGraph
        massValues = array('f', massList)
        brValues   = array('f', brList)

        # Print mass-BR values
        if parseOpts.verbose:
            PrintTable(parseOpts.boson, decayTo, massValues, brValues)
                    
        # Create & Customise a TGraph
        tGraph = ROOT.TGraph(len(massValues), massValues, brValues)
        CustomiseGraph(tGraph, hName, Colours[decayTo] , "", "", "")

        # Add the TGraph to the TMultiGraph
        mGraph.Add(tGraph)

        # Add to TLegend
        leg.AddEntry(tGraph, "BR("+ ConvertToLatex(parseOpts.boson) + "#rightarrow" + ConvertToLatex(decayTo) + ")", "lp")

    # Create text to be drawn on the canvas
    Print("Creating information text for canvas")
    t1 = PlotText(0.16, 0.95, "tan#beta=%s" % (parseOpts.tanb), None, False )
    t2 = PlotText(0.40, 0.95, "#sqrt{s}=%s" % (energy.replace("TeV", " TeV")), None, False)
    t3 = PlotText(0.57, 0.95, "LHC HIGGS XS WG", None, False)
    t4 = PlotText(0.67, 0.95, ConvertFileToScenario(parseOpts.file), None, False)

    # Draw stuff on the canvas
    Print("Drawing various objects on the canvas")
    mGraph.Draw("AC") #fixme
    mGraph.GetXaxis().SetNoExponent()
    mGraph.GetXaxis().SetMoreLogLabels()
    mGraph.GetXaxis().SetTitleOffset(1.05)
    leg.Draw()
    t1.Draw()
    # t2.Draw()
    # t3.Draw()
    t4.Draw()
    if xLog==True or float(parseOpts.massMax) > 1000.0:
        Print("Setting x-axis to log-scale (xLog=%s)" % (xLog))
        c1.SetLogx()
    if yLog==True:
        Print("Setting y-axis to log-scale (yLog=%s)" % (yLog))
        mGraph.SetMinimum(yMin)
        c1.SetLogy()
    c1.Update()
    
    # Customise axes
    Print("Customising TMultiGraph axes")
    mGraph.GetYaxis().SetRangeUser(yMin, yMax)
    mGraph.GetXaxis().SetRangeUser(float(parseOpts.massMin), float(parseOpts.massMax))

    # Save & Close the canvas
    Print("Saving plots in %s format(s)" % (len(saveFormats)) )
    SaveCanvas(c1, saveFormats, savePath, parseOpts)
    return


#================================================================================================
# Main
#================================================================================================
if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]" , add_help_option=False,conflict_handler="resolve")
    parser.add_option("-v", "--verbose"   , dest="verbose"  , action="store_true" , default=False , help="Enables verbose mode (for debugging)")
    parser.add_option("-b", "--batchMode" , dest="batchMode", action="store_false", default=True  , help="Enables batch mode (does NOT generates a window)")
    parser.add_option("-t", "--tanb"      , dest="tanb"     , action="store"      , default=-1.0  , help="The value of tan(beta) to use in plots")
    parser.add_option("-f", "--file"      , dest="file"     , action="store"      , default=None  , help="The (ROOT) file to be used in the plots")
    parser.add_option("-b", "--boson"     , dest="boson"    , action="store"      , default="Hp"  , help="The (Higgs) boson to consider in the plots (H, Hp, h, A)")
    parser.add_option("-l", "--massMin"   , dest="massMin"  , action="store"      , default=80.0  , help="The lower (Higgs) boson mass in the plots (H, Hp, h, A)")
    parser.add_option("-u", "--massMax"   , dest="massMax"  , action="store"      , default=2000.0, help="The upper (Higgs) boson mass in the plots (H, Hp, h, A)")
    (parseOpts, parseArgs) = parser.parse_args()

    # Require at least two arguments (script-name, path to multicrab)
    if parseOpts.tanb == -1.0 or parseOpts.file == None:
        print "Not enough arguments passed to script execution. Printing docstring & EXIT."
        print __doc__
        sys.exit(0)
    else:
        pass

    # Program execution
    main()

    if not parseOpts.batchMode:
        raw_input("=== plotTemplate.py: Press any key to quit ROOT ...")
