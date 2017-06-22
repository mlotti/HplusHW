#!/usr/bin/env python

import ROOT

ROOT.gROOT.SetStyle("Plain")

def main():
   
    # Create functions
    xMin     =    0.0
    xMax     = 1500.0

    ewk_1 = CreateLandau("Landau", xMin, xMax, constant=1.0, mpv=199.99999, sigma=40.92105, colour=ROOT.kBlue-3)
    ewk_2 = CreateBreitWigner("BreitWigner", xMin, xMax, constant=1000.0, sigma= 0.10011, mean=193.63249, colour=ROOT.kOrange)
    ewk_3 = CreateCrystalBall("CrystalBall", xMin, xMax, constant=1.0, mean=197.14516, sigma=73.01814, n=10.0, alpha=-4.91511, colour=ROOT.kRed)
    qcd   = CreateLogNormal("LogNormal", xMin, xMax, constant=10.0, sigma=0.4, theta=6.0, m=200, colour=ROOT.kRed)
    #Double_t TMath::LogNormal( sigma, Double_t theta = 0, Double_t m = 1)
    #qcd   = CreateLogNormalPDF("LogNormal", xMin, xMax, constant=10.0, sigma=5.0, theta=-0.4, m=1, colour=ROOT.kRed)

    # Append histos to a list
    fList = []
    #fList.append(ewk_1)
    #fList.append(ewk_2)
    #fList.append(ewk_3)
    #fList.append(qcd)
    #DrawList("test", fList, 1.0)

    testList = []
    for i in range(0, 4):
        constant =  10.0 + i
        sigma    =   0.38 # + (0.1*i)
        theta    =   5.8 #- (i*20)
        m        = 234.5 # + (i*10)
        qcd      = CreateLogNormal("LogNormal_%s" % (i), xMin, xMax, constant, sigma, theta, m, i+1)
        testList.append(qcd)
    
    DrawList("fakeBFits", testList)

    return

######################################################################
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

######################################################################
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

######################################################################
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

######################################################################
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

######################################################################
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


def DrawList(cName, fList, yMax=None):

    canvas = ROOT.TCanvas(cName, cName, 600, 600)
    legend = ROOT.TLegend(0.75, 0.75, 0.90, 0.90);

    for i, f in enumerate(fList):
        if i ==0:
            f.Draw()
            if yMax != None:
                f.SetMaximum(yMax)
        else:
            f.Draw("same")
        legend.AddEntry(f, f.GetName(), "L")

    legend.Draw()
    #canvas.GetYaxis().SetRangeUser(0, 100)
    formats = [".png"] #[".C", ".png", ".pdf"]
    for f in formats:
        canvas.SaveAs(cName + f)
        
    return
######################################################################
def CustomiseTF1(f, myColour, fill=True):
    
    if fill==True:
        f.SetFillColor(myColour)
        
    #f.SetFillStyle(3001)
    f.SetLineColor(myColour)
    f.SetLineWidth(2)

    return

######################################################################
def CreateTH1F(hName, hTitle, binWidthX, xMin, xMax, xMean):
    
    if xMin == None:
        xMin  =  xMean*(-5)
    if xMax == None:
        xMax  =  xMean*(+5)
    nBinsX = int((xMax-xMin)/binWidthX)

    h = ROOT.TH1F(hName, hTitle, nBinsX, xMin, xMax)
    
    return h

######################################################################
if __name__ == "__main__":

    main()

    #raw_input("\n*** DONE! Press \"ENTER\" key exit session: ")
