#!/usr/bin/env python
'''
Description:
This script produces plots for various functions considered for fitting.
This is not an analysis-related script but simply educational.

Usage:
./drawFitFunctions.py [opts]

Example:
./drawFitFunctions.py --url --nPlots 4 --shape "All"
./drawFitFunctions.py --url --nPlots 8 --shape "Landau"
./drawFitFunctions.py --url --nPlots 7 --shape "CrystalBall"

Links:
http://home.fnal.gov/~aattikis/FakeBMeasurement/LogNormal.png
http://home.fnal.gov/~aattikis/FakeBMeasurement/RooLogNormal.png
http://home.fnal.gov/~aattikis/FakeBMeasurement/BreitWigner.png
http://home.fnal.gov/~aattikis/FakeBMeasurement/CrystalBall.png
http://home.fnal.gov/~aattikis/FakeBMeasurement/Landau.png
http://home.fnal.gov/~aattikis/FakeBMeasurement/RooCBShape.png
http://home.fnal.gov/~aattikis/FakeBMeasurement/RooGaussian.png
http://home.fnal.gov/~aattikis/FakeBMeasurement/RooExponential.png
'''

#================================================================================================ 
# Imports
#================================================================================================ 
import sys
import os
from optparse import OptionParser
import ROOT

import HiggsAnalysis.NtupleAnalysis.tools.tdrstyle as tdrstyle
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kFatal 
#kPrint = 0,  kInfo = 1000, kWarning = 2000, kError = 3000, kBreak = 4000, kSysError = 5000, kFatal = 6000

#================================================================================================ 
# Main
#================================================================================================ 
def main(opts):

    # Apply TDR style
    style = tdrstyle.TDRStyle()
    style.setOptStat(True)
    style.setGridX(False)
    style.setGridY(False)
   
    # Create functions
    xMin        =    0.0
    xMax        = 1500.0
    histoDict   = {}
    landauList  = []
    bwList      = []
    cbList      = []
    logNList    = []
    rooLogNList = [] 
    rooCBList   = []
    rooGausList = []
    rooExpoList = []

    # For-loop: All plots
    for i in range(0, opts.nPlots):

        # Landau
        const =   1 - (i*0.1)
        mpv   = 190 + (i*20)
        sigma =  30 + (i*10)
        leg   = "k = %.0f, mpv = %.0f, #sigma = %.0f" % (const, mpv, sigma)
        plot  = CreateLandau(leg, xMin, xMax, const, mpv, sigma, colour=i+1)
        landauList.append(plot)

        # BreitWigner
        const =  100.0 
        mean  =  180.0 + (i*50)
        sigma =   10.0 + (i*30)
        leg   = "k = %.0f, #bar{x} = %.0f, #sigma = %.0f" % (const, mean, sigma)
        plot  = CreateBreitWigner(leg, xMin, xMax, const, sigma, mean, colour=i+1)
        bwList.append(plot)

        # CrystalBall
        const =    1.0 
        mean  =  190.0 + (i*10)
        sigma =   60.0 + (i*10)
        n     =   10.0
        alpha =   -1.0 + (i*0.1)
        leg   = "k = %.0f, #bar{x} = %.0f, #sigma = %.0f, n = %.0f, #alpha = %0.1f" % (const, mean, sigma, n, alpha)
        plot  = CreateCrystalBall(leg, xMin, xMax, const, mean, sigma, n, alpha, colour=i+1)
        cbList.append(plot)
        
        # LogNormal
        const =  10.0 
        sigma =   0.3 + (i*0.1)
        theta =   5.0 - (i*1)
        m     = 230.0 + (i*5)
        leg   = "k = %.0f, #sigma = %.0f, #theta = %.1f, m = %0.1f" % (const, sigma, theta, m)
        plot  = CreateLogNormal(leg, xMin, xMax, const, sigma, theta, m, i+1)
        logNList.append(plot)

        # RooLogNormal
        const = 1
        m0    = 230 + (10*i)
        k     =   1.4 + (0.1*i)
        leg   = "k = %.0f, m_{0}=%s, k=%s" % (const, m0, k)
        plot  = CreateRooLogNormal(leg, xMin, xMax, const, m0, k, i+1)
        rooLogNList.append(plot)
        
        # RooCBShape
        const =    1
        mean  =  173  #+ (10*i)
        sigma =  27   #+ (2*i)
        n     =  25   #+ (2*i)
        alpha =  -1.0 + (0.2*i)
        leg   = "k = %.0f, #bar{x}=%s, #sigma=%s, n=%s, #alpha=%s" % (const, mean, sigma, n, alpha)
        plot  =  CreateRooCBShape(leg, xMin, xMax, const, mean, sigma, alpha, n, i+1)
        rooCBList.append(plot)

        # RooGaussian
        const =   1
        mean  = 200 + (10*i)
        sigma =  35 + (10*i)
        leg   = "k = %.0f, #bar{x}=%s, #sigma=%s" % (const, mean, sigma)
        plot  = CreateRooGaussian(leg, xMin, xMax, const, mean, sigma, i+2)
        rooGausList.append(plot)

        # RooExponential
        const =  1.0
        a     = -0.08 + (0.01*i)
        leg   = "k = %0.f, a=%s" % (const, a)
        plot  = CreateRooExponential(leg, xMin, xMax, const, a, i+3)
        rooExpoList.append(plot)

    # Fill the dictionary    
    histoDict["LogNormal"]      = logNList
    histoDict["Landau"]         = landauList
    histoDict["BreitWigner"]    = bwList
    histoDict["CrystalBall"]    = cbList
    histoDict["RooLogNormal"]   = rooLogNList
    histoDict["RooCBShape"]     = rooCBList
    histoDict["RooGaussian"]    = rooGausList
    histoDict["RooExponential"] = rooExpoList

    if opts.shape == "All":
        for k in histoDict:
            DrawHistoList(k, histoDict[k], opts)
    else:
        DrawHistoList(opts.shape, histoDict[opts.shape], opts)

    return

#================================================================================================ 
# Function definitions
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
    if not opts.verbose:
        return
    Print(msg, printHeader)
    return

def CreateRooGaussian(name, xMin, xMax, constant=1, mean=200.0, sigma=20.0, colour=ROOT.kOrange):
    '''
    "x" invariant mass 
    "sigma" width
    "mean" mean
    '''
    #f1 = ROOT.TF1(name, "gaus", xMin, xMax)
    f1  = ROOT.TF1(name, "[0]*TMath::Exp(-0.5*((x-[1])**2)/([2]**2))", xMin, xMax)
    f1.SetParameters(constant, mean, sigma)                
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1

def CreateRooExponential(name, xMin, xMax, constant=1, exponent=1, colour=ROOT.kOrange):
    '''
    "x" invariant mass 
    "exponent" is coefficient in exponent
    '''
    #f1 = ROOT.TF1(name, "expo", xMin, xMax)
    f1 = ROOT.TF1(name, "[0]*TMath::Exp([1]*x)", xMin, xMax)
    f1.SetParameters(constant, exponent)
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1

def CreateRooCBShape(name, xMin, xMax, constant, m0, sigma, alpha, n, colour=ROOT.kRed):
    '''
    https://root.cern.ch/doc/master/classRooCBShape.html#ac81db429cde612e553cf61ec7c126ac1
    https://root.cern.ch/doc/master/RooCBShape_8cxx_source.html
    
    par[0]*ROOT.Math.crystalball_function(x[0], par[1], par[2], par[3], par[4])
    '''
    
    #f1 = ROOT.TF1(name, "[0]*ROOT::TMath::Power([1]-((x-[2]/[3])), [4])", xMin, xMax)
    nParams = 5
    f1 = ROOT.TF1(name, RooCBShape, xMin, xMax, nParams) # In this case you must define the number of variables
    f1.SetParameters(constant, m0, sigma, alpha, n)
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1

def RooCBShape(x, par):
    '''
    https://root.cern.ch/doc/master/classRooCBShape.html#ac81db429cde612e553cf61ec7c126ac1
    https://root.cern.ch/doc/master/RooCBShape_8cxx_source.html
    http://www.nbi.dk/~petersen/Teaching/Stat2013/Week1/RootIntro.py
    
    par[0]*ROOT.Math.crystalball_function(x[0], par[1], par[2], par[3], par[4])
    '''
    t = (x[0]-par[1])/par[2]
    if (par[3] < 0):
        t = -t
         
    absAlpha = abs(par[3])
    
    if (t >= -absAlpha):
        return par[0]*ROOT.TMath.Exp(-0.5*t*t)
    else:
        a = ROOT.TMath.Power(par[4]/absAlpha,par[4])*ROOT.TMath.Exp(-0.5*absAlpha*absAlpha)
        b = (par[4]/absAlpha) - absAlpha
        return par[0]*(a/ROOT.TMath.Power(b - t, par[4]))


def func_advanced(x, p):
    '''
    http://www.nbi.dk/~petersen/Teaching/Stat2013/Week1/RootIntro.py
    '''
    if (x[0] < 1.25) :
        return p[0] + p[1]*x[0] + p[2]*x[0]*x[0]
    else :
        return p[0] + p[1]*x[0] + 0.9*x[0]*x[0]

def RooLogNormal(self, x, const, m0, k):
    '''
    https://root.cern.ch/doc/v608/classRooLognormal.html
    https://root.cern.ch/doc/v608/RooLognormal_8cxx_source.html
    
    RooFit Lognormal PDF. The two parameters are:
    - m0 = median    [the median of the distribution]
    - k = exp(sigma) [sigma is called the shape parameter in the TMath parametrization]
    
    \begin{align}
    \mathrm{Lognormal}(x,m_{0},k) = \frac{e^{(-\ln^2(x/m_0))/(2\ln^2(k))}}{\sqrt{2\pi \cdot \ln(k)\cdot x}}
    \end{align}
    
    The parametrization here is physics driven and differs from the ROOT::Math::lognormal_pdf(x, m, s, x0) with:
    - m = log(m0)
    - s = log(k)
    - x0 = 0
    
    Double_t RooLognormal::evaluate() const
    {
    Double_t xv = x;
    Double_t ln_k = TMath::Abs(TMath::Log(k));
    Double_t ln_m0 = TMath::Log(m0);
    Double_t x0 = 0;
    Double_t ret = ROOT::Math::lognormal_pdf(xv,ln_m0,ln_k,x0);
    return ret;
    }
    
    #  ln(k)<1 would correspond to sigma < 0 in the parametrization
    #  resulting by transforming a normal random variable in its
    #  standard parametrization to a lognormal random variable
    #  => treat ln(k) as -ln(k) for k<1
    '''
    #return par[0]*ROOT.TMath.Exp(-(ROOT.TMath.Log(x[0]/par[1]))**2/(2*ROOT.TMath.Log(par[2]))**2)/(ROOT.TMath.Sqrt(2*ROOT.TMath.Pi()*ROOT.TMath.Log(par[2])*x[0]))              
    xv    = x[0]
    ln_k  = ROOT.TMath.Abs(ROOT.TMath.Log(k))
    ln_m0 = ROOT.TMath.Log(m0)
    x0    = 0
    return const*ROOT.Math.lognormal_pdf(xv, ln_m0, ln_k, x0)

def CreateRayleigh(name, xMin, xMax, constant=1, sigma=1, colour=ROOT.kCyan):
    '''
    "x" invariant mass 
    "sigma" is scale parameter
    "mean" is approximaterl 1.25*sigma
    '''    
    f1 = ROOT.TF1(name, "([p0]*x)/([p1]*[p1]) * TMath::Exp(-(x**2)/(2*[p1]*[p1]))", xMin, xMax)
    #f1 = ROOT.TF1(name, "[0]*TMath::Exp(-x*[1])", xMin, xMax)
    #f1 = ROOT.TF1("func","[0]*[1]*TMath::Exp(-x/[2])**[3]", 0,6);
    f1.SetParameters(constant, sigma)
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1

def CreateLogNormal(name, xMin=0.0, xMax=1500, constant=1.0, sigma=0.5, theta=0.0, m=1, colour=ROOT.kOrange):
    '''
    http://www.itl.nist.gov/div898/handbook/eda/section3/eda3669.htm
    https://root.cern.ch/doc/v608/namespaceTMath.html#a0503deae555bc6c0766801e4642365d2

    TMath::LogNormal(x, sigma, theta, m)

    "x" invariant mass 
    sigma is the shape parameter
    theta is the location shape parameter (and is the standard deviation of the log of the distribution)
    m is the scale parameter (and is also the median of the distribution)
    '''
    f1 = ROOT.TF1(name, "[0]*TMath::LogNormal(x, [1], [2], [3])", xMin, xMax)
    f1.SetParameters(constant, sigma, theta, m)
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1

def CreateRooLogNormal(name, xMin=0.0, xMax=1500, constant=1.0, m0=232.4, k=1.43, colour=ROOT.kOrange):
    '''
    '''
    ln_k  = ROOT.TMath.Abs(ROOT.TMath.Log(k))
    ln_m0 = ROOT.TMath.Log(m0)
    x0    = 0
    f1    = ROOT.TF1(name, "[0]*ROOT::Math::lognormal_pdf(x, [1], [2], [3])", xMin, xMax)
    f1.SetParameters(constant, ln_m0, ln_k, x0)
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1


def CreateLogNormal(name, xMin=0.0, xMax=1500, constant=1.0, sigma=0.5, theta=0.0, m=1, colour=ROOT.kOrange):
    '''
    http://www.itl.nist.gov/div898/handbook/eda/section3/eda3669.htm
    https://root.cern.ch/doc/v608/namespaceTMath.html#a0503deae555bc6c0766801e4642365d2

    TMath::LogNormal(x, sigma, theta, m)

    "x" invariant mass 
    sigma is the shape parameter
    theta is the location shape parameter (and is the standard deviation of the log of the distribution)
    m is the scale parameter (and is also the median of the distribution)
    '''
    f1 = ROOT.TF1(name, "[0]*TMath::LogNormal(x, [1], [2], [3])", xMin, xMax)
    f1.SetParameters(constant, sigma, theta, m)
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1

def CreateLogNormalPDF(name, xMin=0.0, xMax=1500, constant=1.0, m=1.0, sigma=0.5, theta=0.0, colour=ROOT.kOrange):
    '''
    https://root.cern.ch/doc/v608/group__PdfFunc.html#ga20ece8c1bb9f81af22ed65dba4a1b025
    
    http://www.itl.nist.gov/div898/handbook/eda/section3/eda3669.htm

    "x" invariant mass 
    m is the scale parameter (and is also the median of the distribution)
    sigma is the shape parameter (and is the standard deviation of the log of the distribution)
    theta is the location shape parameter
    '''
    f1 = ROOT.TF1(name, "[0]*ROOT::Math::lognormal_pdf(x, [1], [2], [3])", xMin, xMax)
    f1.SetParameters(constant, m, sigma, theta)
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1

def CreateBreitWigner(name, xMin, xMax, constant=1, sigma=1, mean=0.0, colour=ROOT.kOrange):
    '''
    "x" invariant mass 
    "sigma" width
    "mean" mean
    '''
    f1 = ROOT.TF1(name, "breitwigner", xMin, xMax)
    f1.SetParameters(constant, mean, sigma)
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1

def CreateCrystalBall(name, xMin, xMax, constant=1, mean=0, sigma=1, n=1, alpha=1, colour=ROOT.kRed):
    '''
    "x" invariant mass 
    "m" mass mean value 
    "s" mass resolution 
    "a" Gaussian tail
    "n" normalization

    From fit-panel: Set Parameters of "crystalball"
    par0 = Constant
    par1 = Mean
    par2 = Sigma
    par3 = Alpha
    par4 = N
    '''
    f1 = ROOT.TF1(name, "crystalball", xMin, xMax)
    f1.SetParameters(constant, mean, sigma, alpha, n)
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1

def CreateLandau(name, xMin, xMax, constant=1, mpv=0, sigma=1, colour=ROOT.kBlue):
    '''
    "x" invariant mass 
    "mpv" most probable value
    "sigma" width
    '''
    f1 = ROOT.TF1(name, "landau", xMin, xMax)
    f1.SetParameters(constant, mpv, sigma)
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1

def CreateCrystalBallMath(name, xMin, xMax, mean=0, sigma=1, n=1, alpha=1, colour=ROOT.kRed):

    f1 = ROOT.TF1(name, "ROOT::Math::crystalball_function(x, %s, %s, %s, %s)" % (alpha, n, sigma, mean), xMin, xMax)
    f1.SetLineColor(colour)
    CustomiseTF1(f1, colour)
    return f1

def DrawHistoList(cName, fList, opts, yMax=None):

    canvas = ROOT.TCanvas(cName, cName, 600, 600)
    legend = ROOT.TLegend(0.45, 0.70-(opts.nPlots*0.02), 0.90, 0.90);
    legend.SetLineColor(ROOT.kWhite)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.022)

    for i, f in enumerate(fList):
        f.GetXaxis().SetTitle("m_{jjb} (GeV/c^{2})")
        f.GetYaxis().SetTitle("Arbitrary Units")

        if i ==0:
            f.Draw()
            if yMax != None:
                f.SetMaximum(yMax)
        else:
            f.Draw("same")
        legend.AddEntry(f, f.GetName(), "L")

    legend.Draw()
    #canvas.GetYaxis().SetRangeUser(0, 100)
    formats = [".C", ".png", ".pdf"]

    # For-loop: All formats
    for i, ext in enumerate(formats): 
        saveName    = os.path.join(opts.saveDir, cName + ext)
        saveNameURL = saveName.replace("/publicweb/a/aattikis/", "http://home.fnal.gov/~aattikis/")
        if opts.url:
            Print(saveNameURL, i % len(formats) == 0)
        else:
            Print(saveName,i % len(formats) == 0)
        canvas.SaveAs(saveName)
    return

def CustomiseTF1(f, myColour, fill=True):
    
    if fill==True:
        f.SetFillColor(myColour)
        
    #f.SetFillStyle(3001)
    f.SetLineColor(myColour)
    f.SetLineWidth(2)

    return

def CreateTH1F(hName, hTitle, binWidthX, xMin, xMax, xMean):
    
    if xMin == None:
        xMin  =  xMean*(-5)
    if xMax == None:
        xMax  =  xMean*(+5)
    nBinsX = int((xMax-xMin)/binWidthX)

    h = ROOT.TH1F(hName, hTitle, nBinsX, xMin, xMax)
    
    return h

if __name__ == "__main__":

    '''
    https://docs.python.org/3/library/argparse.html
 
    name or flags...: Either a name or a list of option strings, e.g. foo or -f, --foo.
    action..........: The basic type of action to be taken when this argument is encountered at the command line.
    nargs...........: The number of command-line arguments that should be consumed.
    const...........: A constant value required by some action and nargs selections.
    default.........: The value produced if the argument is absent from the command line.
    type............: The type to which the command-line argument should be converted.
    choices.........: A container of the allowable values for the argument.
    required........: Whether or not the command-line option may be omitted (optionals only).
    help............: A brief description of what the argument does.
    metavar.........: A name for the argument in usage messages.
    dest............: The name of the attribute to be added to the object returned by parse_args().
    '''

    # Default Settings
    BATCHMODE    = True
    URL          = False
    SAVEDIR      = "/publicweb/a/aattikis/FakeBMeasurement/"
    VERBOSE      = False
    NPLOTS       = 6
    SHAPE        = "All"

    # Define the available script options
    parser = OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-b", "--batchMode", dest="batchMode", action="store_false", default=BATCHMODE, 
                      help="Enables batch mode (canvas creation does NOT generate a window) [default: %s]" % BATCHMODE)

    parser.add_option("--saveDir", dest="saveDir", type="string", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

    parser.add_option("--url", dest="url", action="store_true", default=URL, 
                      help="Don't print the actual save path the histogram is saved, but print the URL instead [default: %s]" % URL)
    
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=VERBOSE, 
                      help="Enables verbose mode (for debugging purposes) [default: %s]" % VERBOSE)

    parser.add_option("-n", "--nPlots", dest="nPlots", type=int, default=NPLOTS, 
                      help="Number of plots to generate for the given shape [default: %s]" % NPLOTS)

    parser.add_option("-s", "--shape", dest="shape", default=SHAPE, 
                      help="The shape type to plot from the pool of supported ones [default: %s]" % SHAPE)

    (opts, parseArgs) = parser.parse_args()

    validShapes = ["Landau", "BreitWigner", "CrystalBall", "LogNormal",     
                   "RooLogNormal", "RooCBShape", "RooGaussian", "RooExponential", 
                   "All"]

    myShapes = [s for s in validShapes]
    if opts.shape not in myShapes:
        Print("Invalid shape \"%s\" selected. Please select one of the following:\n\t%s"% (opts.shape, "\n\t".join(validShapes) ), True)
        parser.print_help()
        print __doc__
        sys.exit(1)

    # Call the main function
    main(opts)

    if not opts.batchMode:
        raw_input("=== drawFitFunctions: Press any key to quit ROOT ...")
