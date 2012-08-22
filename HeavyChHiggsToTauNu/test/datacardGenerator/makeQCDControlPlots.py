import sys
import os
import ROOT
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import TDRStyle


def main(myFile):
    # Set style
    myStyle = TDRStyle()
    myStyle.setOptStat(False)
    # Open file
    myRootFile = ROOT.TFile.Open(myFile)
    if myRootFile == None:
        raise Exception("Error: Failed to open root file '%s'!"%myRootFile)
    # Do plots
    makeQCDPUdependancyPlot(myRootFile)
    makeQCDNQCDPlot(myRootFile)
    makeQCDEffLeg1Plot(myRootFile)
    makeQCDEffLeg2Plot(myRootFile)

def getMinimum(hlist):
    a = 9999.9
    for h in hlist:
        for i in range(1,h.GetNbinsX()+1):
            v = h.GetBinContent(i)-h.GetBinError(i)
            if v < a and v > 0:
                a = v
    return a

def getMaximum(hlist):
    a = 0.0
    for h in hlist:
        for i in range(1,h.GetNbinsX()+1):
            v = h.GetBinContent(i)+h.GetBinError(i)
            if v > a:
                a = v
    return a

def getHisto(myRootFile,name):
    h = myRootFile.Get(name)
    if h == None:
        raise Exception("Error: cannot obtain histogram %s!"%name)
    return h

def makeCanvas(title,logy=False):
    c = ROOT.TCanvas(title,title,600,600)
    c.Range(0,0,1,1)
    c.SetLogy(logy)
    c.cd()
    return c

def makeQCDPUdependancyPlot(myRootFile):
    title = "QCDPUdependancy"
    c = makeCanvas(title,True)
    # Get plots
    hLeg1 = getHisto(myRootFile,"Contracted_EffLeg1_axisZ")
    hLeg2 = getHisto(myRootFile,"Contracted_EffLeg2_axisZ")
    hLeg12 = getHisto(myRootFile,"Contracted_EffLeg1AndLeg2_axisZ")
    # Make frame
    bins = 20
    hFrame = ROOT.TH1F(title+"frame",title+"frame",bins,0,bins)
    hFrame.SetMinimum(getMinimum([hLeg1,hLeg2,hLeg12])*.9)
    hFrame.SetMaximum(getMaximum([hLeg1,hLeg2,hLeg12])*1.1)
    hFrame.SetXTitle("Number of vertices")
    hFrame.SetYTitle("Efficiency")
    # Set styles
    hLeg1.SetLineColor(ROOT.kRed)
    hLeg2.SetLineColor(ROOT.kBlue)
    hLeg12.SetLineColor(ROOT.kBlack)
    hLeg1.SetMarkerColor(ROOT.kRed)
    hLeg2.SetMarkerColor(ROOT.kBlue)
    hLeg12.SetMarkerColor(ROOT.kBlack)
    hLeg1.SetMarkerStyle(20)
    hLeg2.SetMarkerStyle(20)
    hLeg12.SetMarkerStyle(20)
    # Draw
    hFrame.Draw()
    hLeg1.Draw("same")
    hLeg2.Draw("same")
    hLeg12.Draw("same")
    # Legend
    leg = ROOT.TLegend(0.33,0.53,0.77,0.71,"","brNDC")
    leg.SetBorderSize(0)
    leg.SetTextFont(63)
    leg.SetTextSize(18)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    #leg.SetFillStyle(4000)
    entry = leg.AddEntry(hLeg1, "eff(E_{T}^{miss}+btag+#Delta#phi)", "P")
    entry = leg.AddEntry(hLeg2, "eff(#tau ID)", "P")
    entry = leg.AddEntry(hLeg12, "eff(E_{T}^{miss}+btag+#Delta#phi)*eff(#tau ID)", "P")
    leg.Draw()
    # Labels
    o=createTopCaption()
    # Make graph
    c.Print(title+".png")
    c.Close()

def makeQCDNQCDPlot(myRootFile):
    title = "QCD_NQCD"
    c = makeCanvas(title,True)
    # Get plots
    hLeg1 = getHisto(myRootFile,"Contracted_NQCD_axisX")
    hLeg1.SetXTitle("#tau p_{T}, GeV/c")
    hLeg1.SetYTitle("Events")
    # Set styles
    hLeg1.SetLineColor(ROOT.kBlack)
    hLeg1.SetMarkerColor(ROOT.kBlack)
    hLeg1.SetMarkerStyle(20)
    # Draw
    hLeg1.Draw("")
    # Labels
    o=createTopCaption()
    # Make graph
    c.Print(title+".png")
    c.Close()

def makeQCDEffLeg1Plot(myRootFile):
    title = "QCDEffLeg1"
    c = makeCanvas(title,True)
    # Get plots
    hLeg1 = getHisto(myRootFile,"Contracted_EffLeg1_axisX")
    hLeg1.SetXTitle("#tau p_{T}, GeV/c")
    hLeg1.SetYTitle("eff(E_{T}^{miss}+btag+#Delta#phi)")
    # Set styles
    hLeg1.SetLineColor(ROOT.kBlack)
    hLeg1.SetMarkerColor(ROOT.kBlack)
    hLeg1.SetMarkerStyle(20)
    # Draw
    hLeg1.Draw("")
    # Labels
    o=createTopCaption()
    # Make graph
    c.Print(title+".png")
    c.Close()

def makeQCDEffLeg2Plot(myRootFile):
    title = "QCDEffLeg2"
    c = makeCanvas(title,True)
    # Get plots
    hLeg1 = getHisto(myRootFile,"Contracted_EffLeg2_axisX")
    hLeg1.SetXTitle("#tau p_{T}, GeV/c")
    hLeg1.SetYTitle("eff(#tau ID)")
    # Set styles
    hLeg1.SetLineColor(ROOT.kBlack)
    hLeg1.SetMarkerColor(ROOT.kBlack)
    hLeg1.SetMarkerStyle(20)
    # Draw
    hLeg1.Draw("")
    # Labels
    o=createTopCaption()
    # Make graph
    c.Print(title+".png")
    c.Close()

## Creates top text
def createTopCaption():
    CMSCaption = createTopCaptionText(0.62,0.96,"CMS Preliminary")
    CMSCaption.Draw()
    SqrtsCaption = createTopCaptionText(0.2,0.96,"#sqrt{s} = 7 TeV")
    SqrtsCaption.Draw()
    LumiCaption = createTopCaptionText(0.43,0.96,"L=%3.1f fb^{-1}"%(5.0))
    LumiCaption.Draw()
    return [CMSCaption,SqrtsCaption,LumiCaption]

## Creates a TLatex object
def createTopCaptionText(x, y, title):
    tex = ROOT.TLatex(x,y,title)
    tex.SetNDC()
    tex.SetTextFont(43)
    tex.SetTextSize(27)
    tex.SetLineWidth(2)
    return tex

if __name__ == "__main__":
    myFiles = []
    # Check input file
    for arg in sys.argv:
        if ".root" in arg:
            # check if file exists
            if os.path.exists(arg):
                myFiles.append(arg)
            else:
                raise Exception("Error: File '%s' does not exist!"%arg)
    ROOT.gROOT.SetBatch() # no flashing canvases
    for myFile in myFiles:
        main(myFile)