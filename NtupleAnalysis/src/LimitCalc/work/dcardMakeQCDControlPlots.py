import sys
import os
import ROOT
from NtupleAnalysis.toolstdrstyle import TDRStyle
from math import pow,sqrt

def main(myFile):
    # Set style
    myStyle = TDRStyle()
    myStyle.setOptStat(False)
    myStyle.tdrStyle.SetPalette(1)
    myStyle.tdrStyle.SetPaintTextFormat(".1g")
    myStyle.tdrStyle.SetTextFont(42)
    myStyle.tdrStyle.SetTextSize(24)
    #myStyle.tdrStyle.SetTextSizePixels(20000)
    # Open file
    myRootFile = ROOT.TFile.Open(myFile)
    if myRootFile == None:
        raise Exception("Error: Failed to open root file '%s'!"%myRootFile)
    print "Opened file:",myFile
    # Do plots
    if True:
        #makeQCDPUdependancyPlot(myRootFile)
        makeQCDNQCDPlot(myRootFile)
        makeQCDPurityPlot(myRootFile)
        makeQCDEfficiencyPlot(myRootFile)
        makeQCDShapeBreakDown(myRootFile)

    makeTransverseMassPlots(myRootFile, "QCDFact_ShapeSummary_QCDfact_ContractedX", title="QCDfactorised_mtShapes", bins=[8])


    # MET validation plots 1D
    suffix = "MET30"
    suffix = ""
    #validationSpecs = { "denominator": "METvalidation_CtrlLeg1METAfterStandardSelections"+suffix,
                        #"denominatorTitle": "Basic selections",
                        ##"nominator":   "METvalidation_CtrlLeg1METAfterFullTauID",
                        #"nominator":   "METvalidation_CtrlLeg1METAfterTauIDNoRtau"+suffix,
                        #"nominatorTitle": "Basic selections + tau ID (no R_{#tau} cut)",
                        #"bins": [8],
                        #"title": "QCDfactorised_validation_MET_1D_NoRtau",
                        #"logy": "True",
                        #"ytitle": "A.u. / 20-200 GeV"
                        #}
    #makeQCDValidationPlots(myRootFile, validationSpecs)
    validationSpecs = { "denominator": "METvalidation_CtrlLeg1METAfterStandardSelections"+suffix,
                        "denominatorTitle": "Basic selections",
                        "nominator":   "METvalidation_CtrlLeg1METAfterFullTauID"+suffix,
                        "nominatorTitle": "Basic selections + tau ID (with R_{#tau} cut)",
                        "bins": [8],
                        "title": "QCDfactorised_validation_MET_1D_Full",
                        "logy": "True",
                        "ytitle": "A.u. / 10 GeV"
                        }
    makeQCDValidationPlots(myRootFile, validationSpecs)
    # MET validation plots 3D
    #validationSpecs = { "denominator": "QCDFact_METvalidation_CtrlLeg1METAfterStandardSelections_QCD",
                        #"denominatorTitle": "Basic selections",
                        #"nominator":   "QCDFact_METvalidation_CtrlLeg1METAfterTauIDNoRtau_QCD",
                        ##"nominator":   "QCDFact_METvalidation_CtrlLeg1METAfterFullTauID_QCD",
                        #"nominatorTitle": "Basic selections + tau ID",
                        #"bins": [8,3,2],
                        #"title": "QCDfactorised_validation_MET",
                        #"logy": "True",
                        #"ytitle": "A.u. / 20 GeV/c^{2}"
                        #}
    #makeQCDValidationPlots(myRootFile, validationSpecs)
    # mT validation plots 1D
    validationSpecs = { "denominator": "mTvalidation_MtShapesAfterStandardSelection"+suffix,
                        "denominatorTitle": "Basic selections",
                        ##"nominator":   "mTvalidation_MtShapesAfterTauID",
                        "nominator":   "mTvalidation_MtShapesAfterTauIDNoRtau"+suffix,
                        "nominatorTitle": "Basic selections + tau ID (no R_{#tau} cut)",
                        "bins": [8],
                        "title": "QCDfactorised_validation_mT_1D_NoRtau",
                        "logy": "True",
                        "ytitle": "A.u. / 20 GeV/c^{2}"
                        }
    makeQCDValidationPlots(myRootFile, validationSpecs)
    validationSpecs = { "denominator": "mTvalidation_MtShapesAfterStandardSelection"+suffix,
                        "denominatorTitle": "Basic selections",
                        #"nominator":   "mTvalidation_MtShapesAfterStandardSelection",
                        "nominator":   "mTvalidation_MtShapesAfterTauID"+suffix,
                        "nominatorTitle": "Basic selections + tau ID (with R_{#tau} cut)",
                        "bins": [8],
                        "title": "QCDfactorised_validation_mT_1D_Full",
                        "logy": "True",
                        "ytitle": "A.u. / 20 GeV/c^{2}"
                        }
    makeQCDValidationPlots(myRootFile, validationSpecs)
    # mT validation plots 3D
    #validationSpecs = { "denominator": "QCDFact_mTvalidation_MtShapesAfterStandardSelection_QCD",
                        #"denominatorTitle": "Basic selections",
                        ##"nominator":   "QCDFact_mTvalidation_MtShapesAfterTauID_QCD",
                        #"nominator":   "QCDFact_mTvalidation_MtShapesAfterTauIDNoRtau_QCD",
                        #"nominatorTitle": "Basic selections + tau ID",
                        #"bins": [8,3,2],
                        #"title": "QCDfactorised_validation_mT",
                        #"logy": "True"
                        #}
    #makeQCDValidationPlots(myRootFile, validationSpecs)



def setHistoStyle(hlist):
    myList = []
    if not isinstance(hlist,list):
        myList.append(hlist)
    else:
        myList.extend(hlist)
    for h in hlist:
        h.SetTitleFont(43, "xyz")
        h.SetTitleSize(27, "xyz")
        h.SetLabelFont(43, "xyz")
        h.SetLabelSize(24, "xyz")
        h.GetXaxis().SetLabelOffset(0.007)
        h.GetYaxis().SetLabelOffset(0.007)
        h.GetXaxis().SetTitleOffset(3.2)
        h.GetYaxis().SetTitleOffset(1.3)

def makeTransverseMassPlots(myRootFile, histopath, title, bins):
    # Determine number of bins
    binning = bins
    nbinsX = binning[0]
    nbinsY = 1
    nbinsZ = 1
    if len(binning)>1:
        nbinsY = binning[1]
    if len(binning)>2:
        nbinsZ = binning[2]
    hTotal = None
    for i in range(0,nbinsX):
        for j in range(0,nbinsY):
            for k in range(0,nbinsZ):
                myBinSuffix = "_%d"%(i+1)
                if len(binning)>1:
                    myBinSuffix += "_%d"%(j+1)
                if len(binning)>2:
                    myBinSuffix += "_%d"%(k+1)
                myTitle = "%s_bin%s"%(title,myBinSuffix)
                # get plots
                filename = "%s/%s_bin%s"%(histopath,histopath,myBinSuffix)
                print filename
                h = getHisto(myRootFile,filename)
                h.SetLineWidth(2)
                h.SetMarkerStyle(20)
                h.SetMarkerSize(1)
                h.SetLineColor(ROOT.kBlack)
                h.SetXTitle("m_{T}(#tau-jet candidate, E_{T}^{miss}, GeV/c^{2}")
                setHistoStyle([h])
                h.GetXaxis().SetTitleOffset(1.2)
                h.SetMinimum(0)
                h.SetYTitle("Events / 20 GeV/c^{2}")

                if hTotal == None:
                    hTotal = h.Clone(myTitle+"total")
                else:
                    hTotal.Add(h)
                # plot
                c = makeCanvas(myTitle+"canvas",False)
                h.Draw("")
                # Labels
                o=createTopCaption()
                binCaption = createTopCaptionText(0.52,0.88,"#tau p_{T}%s GeV/c"%getTauPtBinLabel(i))
                binCaption.Draw()
                # Make graph
                c.Print(myTitle+".png")
                c.Close()
    # Make total plot
    myTitle = "%s_total"%(title)
    c = makeCanvas(myTitle+"canvas",False)
    hTotal.Draw("")
    # Labels
    o=createTopCaption()
    # Make graph
    c.Print(myTitle+".png")
    c.Close()


def getTauPtBinLabel(idx):
    if idx == 0:
        return "=40-50"
    elif idx == 1:
        return "=50-60"
    elif idx == 2:
        return "=60-70"
    elif idx == 3:
        return "=70-80"
    elif idx == 4:
        return "=80-100"
    elif idx == 5:
        return "=100-120"
    elif idx == 6:
        return "=120-150"
    elif idx == 7:
        return ">150"

def makeQCDValidationPlots(myRootFile,specs):
    # Determine number of bins
    binning = specs["bins"]
    nbinsX = binning[0]
    nbinsY = 1
    nbinsZ = 1
    if len(binning)>1:
        nbinsY = binning[1]
    if len(binning)>2:
        nbinsZ = binning[2]
    # loop
    myCombinedTotal = 0.0
    myCombinedTotalErrorSquared = 0.0
    myCorrectionOutput = '"name": "%s",\n'%specs["title"]
    myCorrectionOutput += '"bins": [%d, %d, %d],\n'%(nbinsX,nbinsY,nbinsZ)
    myCorrectionBinning = ""
    for i in range(0,nbinsX):
        for j in range(0,nbinsY):
            for k in range(0,nbinsZ):
                myBinSuffix = "_%d"%i
                if len(binning)>1:
                    myBinSuffix += "_%d"%j
                if len(binning)>2:
                    myBinSuffix += "_%d"%k
                myTitle = "%s_bin%s"%(specs["title"],myBinSuffix)
                # get plots
                filename = "%s/%s_bin%s"%(specs["denominator"],specs["denominator"],myBinSuffix)
                print filename
                hDenominator = getHisto(myRootFile,filename)
                filename = "%s/%s_bin%s"%(specs["nominator"],specs["nominator"],myBinSuffix)
                hNominator = getHisto(myRootFile,filename)
                hNominatorUnscaled = hNominator.Clone(myTitle+"unscaled")
                # Normalise area to 1
                normaliseAreaToUnity(hDenominator)
                normaliseAreaToUnity(hNominator)
                hDenominator.SetYTitle(specs["ytitle"])
                # Obtain correction factor
                myCorrection = '"%s_Correction_bin%s": ['%(specs["title"],myBinSuffix)
                myCorrectionUncertainty = '"%s_CorrectionUncertainty_bin%s": ['%(specs["title"],myBinSuffix)
                myCorrectionBinning = '"%s_CorrectionBinLeftEdges": ['%(specs["title"])
                for l in range(1,hNominator.GetNbinsX()+1):
                    if l > 1:
                        myCorrection += ", "
                        myCorrectionUncertainty += ", "
                        myCorrectionBinning += ", "
                    myValue = 1.0
                    myUncert = 0.0
                    if hDenominator.GetBinContent(l) > 0:
                        myValue = hNominator.GetBinContent(l)/hDenominator.GetBinContent(l)
                        if hNominator.GetBinContent(l) > 0:
                            myUncert = myValue*sqrt(hNominator.GetBinError(l)/hNominator.GetBinContent(l)+hDenominator.GetBinError(l)/hDenominator.GetBinContent(l))
                    myCorrection += "%f"%myValue
                    myCorrectionUncertainty += "%f"%myUncert
                    myCorrectionBinning += "%.2f"%hDenominator.GetXaxis().GetBinLowEdge(l)
                myCorrection += "],"
                myCorrectionUncertainty += "],"
                myCorrectionBinning += "],"
                if i == 0:
                    myCorrectionOutput += myCorrectionBinning+"\n"
                myCorrectionOutput += myCorrection+"\n"
                myCorrectionOutput += myCorrectionUncertainty+"\n"

                # Calculate difference
                myTotal = 0.0
                myTotalErrorSquared = 0.0
                for l in range(0,hNominator.GetNbinsX()+2):
                    if hDenominator.GetBinContent(l) > 0 and hNominator.GetBinContent(l):
                        myWeight = hNominatorUnscaled.GetBinContent(l)
                        myTotal += pow(myWeight,2)
                        myRatio = hNominator.GetBinContent(l)/hDenominator.GetBinContent(l) - 1.0
                        myTotalErrorSquared += pow(myRatio*myWeight,2)
                myCombinedTotal += myTotal
                myCombinedTotalErrorSquared += myTotalErrorSquared
                if myTotal > 0:
                    print "Error: ",sqrt(myTotalErrorSquared/myTotal)*100.0," %"
                else:
                    print "Error: -- %"
                # Get extrema
                myFactor = 1.1
                if specs["logy"]:
                    myFactor = 1.5
                myMin = getMinimum([hNominator,hDenominator])/myFactor
                myMax = getMaximum([hNominator,hDenominator])*myFactor
                hDenominator.SetMinimum(myMin)
                hDenominator.SetMaximum(myMax)
                # Set style
                setHistoStyle([hNominator,hDenominator])
                hDenominator.GetXaxis().SetTitleSize(0)
                hDenominator.GetXaxis().SetLabelSize(0)
                hNominator.SetMarkerStyle(20)
                hNominator.SetMarkerSize(1)
                hNominator.SetMarkerColor(ROOT.kRed)
                hNominator.SetLineColor(ROOT.kRed)
                hDenominator.SetMarkerStyle(21)
                hDenominator.SetMarkerSize(1)
                hDenominator.SetFillStyle(3004)
                hDenominator.SetFillColor(ROOT.kBlack)
                # Get ratio plot
                hRatio = getRatioHistogram(hNominator,hDenominator)
                myDelta = 1
                hRatio.SetMinimum(1-myDelta)
                hRatio.SetMaximum(1+myDelta)
                hRatio.SetYTitle("Ratio")
                hRatio.GetYaxis().SetNdivisions(505)
                # Draw on same canvas
                c = ROOT.TCanvas(myTitle+"Canvas",myTitle+"Canvas",600,600)
                c.Range(0,0,1,1)
                c.cd()
                # Agreement pad
                apad = ROOT.TPad(myTitle+"apad",myTitle+"apad",0,0,1,.3)
                apad.Draw()
                apad.cd()
                apad.Range(0,0,1,1)
                apad.SetLeftMargin(0.16)
                apad.SetRightMargin(0.05)
                apad.SetTopMargin(0)
                apad.SetBottomMargin(0.34)
                hLine = hRatio.Clone(myTitle+"line")
                for l in range(1, hLine.GetNbinsX()+1):
                    hLine.SetBinContent(l,1)
                    hLine.SetBinError(l,0)
                hLine.SetLineColor(ROOT.kRed)
                hLine.SetLineWidth(2)
                hLine.SetLineStyle(3)
                hLine.Draw("hist")
                hRatio.Draw("ex0 same")
                # Cover pad
                c.cd()
                cpad = ROOT.TPad(myTitle+"cpad",myTitle+"cpad",0.105,0.300,0.155,0.36)
                cpad.Draw()
                cpad.cd()
                cpad.Range(0,0,1,1)
                # Plotpad
                c.cd()
                ppad = ROOT.TPad(myTitle+"ppad",myTitle+"ppad",0,0.3,1,1)
                ppad.Draw()
                ppad.cd()
                ppad.Range(0,0,1,1)
                ppad.SetLeftMargin(0.16)
                ppad.SetRightMargin(0.05)
                ppad.SetTopMargin(0.065)
                ppad.SetBottomMargin(0.0)
                if specs["logy"]:
                    ppad.SetLogy()
                hDenominator.Draw("e2")
                hNominator.Draw("ex0 same")
                ppad.RedrawAxis()
                # Legend
                leg = ROOT.TLegend(0.49,0.73,0.87,0.91,"","brNDC")
                leg.SetBorderSize(0)
                leg.SetTextFont(63)
                leg.SetTextSize(18)
                leg.SetLineColor(1)
                leg.SetLineStyle(1)
                leg.SetLineWidth(1)
                leg.SetFillColor(0)
                leg.SetFillStyle(3004)
                entry = leg.AddEntry(hDenominator, specs["denominatorTitle"], "P")
                entry = leg.AddEntry(hNominator, specs["nominatorTitle"], "P")
                leg.Draw()
                # Labels
                c.cd()
                o=createTopCaption()
                # Make graph
                c.Print(myTitle+".png")
                c.Close()
    print "\nCombined Error: ",sqrt(myCombinedTotalErrorSquared/myCombinedTotal)*100.0," %\n"
    print "\nCorrection details:\n"+myCorrectionOutput

def normaliseAreaToUnity(h):
    myValue = h.Integral(0,h.GetNbinsX()+2)
    if myValue:
        h.Scale(1.0 / myValue)

def getRatioHistogram(hNominator,hDenominator):
    h = hNominator.Clone(hNominator.GetTitle()+"_ratio")
    h.Divide(hDenominator)
    for l in range(1,h.GetNbinsX()+1):
        if hNominator.GetBinContent(l) == 0:
            h.SetBinContent(l,-1e9)
            h.SetBinError(l,0)
    return h

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
    c = makeCanvas(title,False)
    # Get plots
    hLeg1 = getHisto(myRootFile,"Contracted_NQCD_axisX")
    hLeg1.SetXTitle("#tau-jet candidate p_{T}, GeV/c")
    hLeg1.SetYTitle("Events")
    # Set styles
    setHistoStyle([hLeg1])
    hLeg1.GetXaxis().SetTitleOffset(1.4)
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

def makeQCDPurityPlot(myRootFile):
    title = "QCDfactorised_purity"
    c = makeCanvas(title,False)
    # Get plots
    h1 = getHisto(myRootFile,"purity_factorisation_AfterJetSelection_contractedX")
    h1.SetXTitle("#tau-jet candidate p_{T} bin, GeV/c")
    h1.SetYTitle("Purity of selected sample")
    h2 = getHisto(myRootFile,"purity_factorisation_Leg1AfterTopSelection_contractedX")
    h3 = getHisto(myRootFile,"purity_factorisation_Leg2AfterTauID_contractedX")
    # Set styles
    setHistoStyle([h1,h2,h3])
    h1.GetXaxis().SetTitleOffset(1.4)
    h1.SetLineColor(ROOT.kBlack)
    h1.SetMarkerColor(ROOT.kBlack)
    h1.SetMarkerStyle(24)
    h2.SetLineColor(ROOT.kBlue)
    h2.SetMarkerColor(ROOT.kBlue)
    h2.SetMarkerStyle(20)
    h3.SetLineColor(ROOT.kRed)
    h3.SetMarkerColor(ROOT.kRed)
    h3.SetMarkerStyle(21)
    h1.SetMinimum(getMinimum([h1,h2,h3])/1.1)
    h1.SetMaximum(getMaximum([h1,h2,h3])*1.1)
    # Draw
    h1.Draw("")
    h2.Draw("same")
    h3.Draw("same")
    # end
    leg = ROOT.TLegend(0.49,0.16,0.87,0.35,"","brNDC")
    leg.SetBorderSize(0)
    leg.SetTextFont(63)
    leg.SetTextSize(18)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    #leg.SetFillStyle(4000)
    entry = leg.AddEntry(h1, "Basic selections", "P")
    entry = leg.AddEntry(h2, "Basic sel.+E_{T}^{miss}+btag+#Delta#phi", "P")
    entry = leg.AddEntry(h3, "Basic sel.+#tau ID", "P")
    leg.Draw()
    # Labels
    o=createTopCaption()
    # Make graph
    c.Print(title+".png")
    c.Close()


def makeQCDEfficiencyPlot(myRootFile):
    title = "QCDfactorised_efficiencies"
    c = makeCanvas(title,True)
    # Get plots
    hLeg1 = getHisto(myRootFile,"Contracted_EffLeg1_axisX")
    hLeg1.SetXTitle("#tau-jet candidate p_{T} bin, GeV/c")
    hLeg1.SetYTitle("Efficiency vs. basic selections")
    hLeg2 = getHisto(myRootFile,"Contracted_EffLeg2_axisX")
    # Set styles
    setHistoStyle([hLeg1,hLeg2])
    hLeg1.GetXaxis().SetTitleOffset(1.4)
    hLeg1.SetLineColor(ROOT.kBlue)
    hLeg1.SetMarkerColor(ROOT.kBlue)
    hLeg1.SetMarkerStyle(20)
    hLeg2.SetLineColor(ROOT.kRed)
    hLeg2.SetMarkerColor(ROOT.kRed)
    hLeg2.SetMarkerStyle(21)
    hLeg1.SetMinimum(getMinimum([hLeg1,hLeg2])/1.5)
    hLeg1.SetMaximum(getMaximum([hLeg1,hLeg2])*1.5)
    # Draw
    hLeg1.Draw("")
    hLeg2.Draw("same")
    # Legend
    leg = ROOT.TLegend(0.59,0.73,0.87,0.91,"","brNDC")
    leg.SetBorderSize(0)
    leg.SetTextFont(63)
    leg.SetTextSize(28)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    #leg.SetFillStyle(4000)
    entry = leg.AddEntry(hLeg1, "#varepsilon_{E_{T}^{miss}+btag+#Delta#phi}", "P")
    entry = leg.AddEntry(hLeg2, "#varepsilon_{#tau ID}", "P")
    leg.Draw()
    # Labels
    o=createTopCaption()
    # Make graph
    c.Print(title+".png")
    c.Close()

def makeQCDShapeBreakDown(myRootFile):
    title = "QCDfactorised_mt_breakdown"
    c = makeCanvas(title,False)
    c.SetLeftMargin(0.19)
    c.SetRightMargin(0.15)
    c.SetBottomMargin(0.20)
    # Get plots
    h = getHisto(myRootFile,"QCDFact_ShapeSummary_TransverseMass_Total")
    # Set styles
    setHistoStyle([h])
    h.GetXaxis().SetTitleOffset(2.2)
    h.GetYaxis().SetTitleOffset(2.1)
    for i in range(1,h.GetNbinsX()+1):
        h.GetXaxis().SetBinLabel(i,h.GetXaxis().GetBinLabel(i).replace("(","").replace("; all",""))
    for i in range(1,h.GetNbinsY()+1):
        h.GetYaxis().SetBinLabel(i,h.GetYaxis().GetBinLabel(i).replace("(","").replace(";all","").replace("<50","40-50"))
    h.GetXaxis().SetLabelSize(20)
    h.GetXaxis().LabelsOption("v")
    h.GetYaxis().SetLabelSize(20)
    h.GetZaxis().SetLabelSize(20)
    h.SetXTitle("m_{T}(#tau, E_{T}^{miss}), GeV/c^{2}")
    h.SetYTitle("#tau-jet candidate p_{T}, GeV/c")
    
    # Draw
    h.Draw("COLZ,text")
    #h.Draw("text")
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
    return [CMSCaption,SqrtsCaption,LumiCaption] # Return the objects to keep them alive

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
