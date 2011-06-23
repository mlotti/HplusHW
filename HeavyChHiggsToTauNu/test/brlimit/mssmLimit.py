#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True) # batch mode
from ROOT import TLatex, TLegend, TLegendEntry, TGraph

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.statisticalFunctions as statisticalFunctions

mu = 200
#mu = 1000

# write text to plot
def writeTitleTexts(lumi):
    x = 0.62
    y = 0.96
    l = TLatex()
    l.SetNDC()
    l.SetTextFont(l.GetTextFont()-20) # bold -> normal
    l.DrawLatex(x, y, "CMS Preliminary")
    x = 0.2
    l.DrawLatex(x, y, "#sqrt{s} = 7 TeV")
    x = 0.45
    l.DrawLatex(x, y, lumi + " pb^{-1}")
    return 0

def writeText( myText, y ):
    text = TLatex()
#    text.SetTextColor(1)
#    text.SetTextAlign(12)
    text.SetTextSize(20)
#    text.SetTextFont(1)
    text.SetNDC()
    text.DrawLatex(0.185,y,myText)
    return 0

# Create a TGraph for upper limit tanb y values from a TGraph with BR y values
# Convention: begin with low mH, lower limit for 1/2s band
# then go counterclockwise: increase mH, then switch to upper limit, decrease mH
def graphToTanBeta(graph, mymu, removeNotValid=True):
    # Don't modify the original
    graph = graph.Clone()

    # Loop over the graph points
    yvalues = graph.GetY()
    tanbRef = 20 # initial guess
    for i in xrange(0, graph.GetN()):
        mass = graph.GetX()[i]
        # For some reason tanbForBR gets stuck for some large values; solution: do not
        # even bother to calculate values for Br>=0.5
        if yvalues[i]<0.50:
            tanb = statisticalFunctions.tanbForBR(yvalues[i], mass, tanbRef, mymu)
        else:
            tanb = -1
        print "mass %d, BR %f, tanb %f, %d / %d" % (mass, yvalues[i], tanb, i, graph.GetN())
#        if tanb < 0:
#           print "No valid tanb for BR %f" % yvalues[i]

        graph.SetPoint(i, mass, tanb)

    # For points for which a valid tanb value can not be obtained,
    # either remove the point, or set a huge value
    if removeNotValid:
        found = True
        while found:
            found = False
            for i in xrange(0, graph.GetN()):
                if graph.GetY()[i] < 0:
                    graph.RemovePoint(i)
                    found = True
                    break
    else:
        for i in xrange(0, graph.GetN()):
            if graph.GetY()[i] < 0:
                # set huge value or zero
                if 2*i>=graph.GetN():
                    graph.SetPoint(i, graph.GetX()[i], 1e6)
                else:
                    graph.SetPoint(i, graph.GetX()[i], 0.0)
                
    return graph

# Create a TGraph for lower limit tanb y values from a TGraph with BR y values
# Convention: begin with low mH, lower limit for 1/2s band
# then go counterclockwise: increase mH, then switch to upper limit, decrease mH
def graphToTanBetaLow(graph, mymu, removeNotValid=True):
    # Don't modify the original
    graph = graph.Clone()

    # Loop over the graph points
    yvalues = graph.GetY()
    tanbRef = 10 # initial guess
    for i in xrange(0, graph.GetN()):
        mass = graph.GetX()[i]
        # For some reason tanbForBR gets stuck for some large values; solution: do not
        # even bother to calculate values for Br>=0.5
        if yvalues[i]<0.50:
            tanb = statisticalFunctions.tanbForBRlow(yvalues[i], mass, tanbRef, mymu)
        else:
            tanb = -1
        print "mass %d, BR %f, tanb %f, %d / %d" % (mass, yvalues[i], tanb, i, graph.GetN())
#        if tanb < 0:
#           print "No valid tanb for BR %f" % yvalues[i]

        graph.SetPoint(i, mass, tanb)

    # For points for which a valid tanb value can not be obtained,
    # either remove the point, or set a huge value
    #
    # Note that in tanb space the order of points for 1/2 sigma bands
    # is now reversed: first begin with low mH, upper limit for 1/2s
    # band, then go clockwise: increase mH, then switch to lower limit,
    # decrease mH
    if removeNotValid:
        found = True
        while found:
            found = False
            for i in xrange(0, graph.GetN()):
                if graph.GetY()[i] < 0:
                    graph.RemovePoint(i)
                    found = True
                    break
    else:
        for i in xrange(0, graph.GetN()):
            if graph.GetY()[i] < 0:
                # set huge value or zero
                if 2*i>=graph.GetN():
                    graph.SetPoint(i, graph.GetX()[i], 0.0)
                else:
                    graph.SetPoint(i, graph.GetX()[i], 1e6)
                
    return graph

# Get the mass points (x values) of a TGraph as integers, so that they
# can be reliably compared
def getMassPoints(graph):
    return [int(graph.GetX()[i]) for i in xrange(0, graph.GetN())]

# Remove mass points from TGraph which are *not* in massPoints list
def keepOnlyMassPoints(graph, massPoints):
    found = True
    while found:
        found = False
        for i in xrange(0, graph.GetN()):
            if int(graph.GetX()[i]) not in massPoints:
                graph.RemovePoint(i)
                found = True
                break

# Remove mass points lower than 100 since
# statisticalFunctions.tanbForBR cannot handle them (they are unphysical)
def cleanGraph(graph):
    for i in xrange(0, graph.GetN()):
        if int(graph.GetX()[i])<100:
            graph.RemovePoint(i)

# Draw Tevatron exclusion
# picked from P-TDR2, page 369
def getTevaCurve():
    curve = TGraph(11)
    curve.Set(11)
    curve.SetPoint(0,100,58)
    curve.SetPoint(1,105,60)
    curve.SetPoint(2,110,65)
    curve.SetPoint(3,120,78)
    curve.SetPoint(4,120,100)
    curve.SetPoint(5,100,100)
    curve.SetFillStyle(4)
    curve.SetFillColor(618)
    return curve

# Draw LEP exclusion
# picked from P-TDR2, page 369
def getLepCurve():
    curve = TGraph(11)
    curve.Set(11)
    curve.SetPoint(0,100,8.4)
    curve.SetPoint(1,105,9.0)
    curve.SetPoint(2,110,9.2)
    curve.SetPoint(3,115,9.1)
    curve.SetPoint(4,120,8.5)
    curve.SetPoint(5,130,7.7)
    curve.SetPoint(6,140,7.4)
    curve.SetPoint(7,150,6.9)
    curve.SetPoint(8,160,6.8)
    curve.SetPoint(9,160,0.0)
    curve.SetPoint(10,100,0.0)
#    curve.SetPoint(4,150,0.0)
#    curve.SetPoint(5,100,0.0)
    curve.SetFillStyle(4)
    curve.SetFillColor(407)
    return curve
    
# Main function, called explicilty from the end of the script
def main():
    # Apply TDR style
    style = tdrstyle.TDRStyle()

    # Open ROOT file
    f = ROOT.TFile.Open("brlimits.root")

    # Get TGraphs
    observed = f.Get("tg_obs")
    expected = f.Get("tg_exp")
    expected_1s = f.Get("tg_exp_cont1")
    expected_2s = f.Get("tg_exp_cont2")

    # Remove mass points lower than 100 from graphs since
    # gra
    cleanGraph(observed)
    cleanGraph(expected)
    cleanGraph(expected_1s)
    cleanGraph(expected_2s)

    # Create tan beta graphs
    # Convention: begin with low mH, lower limit for 1/2s band
    # then go counterclockwise: increase mH, then switch to upper limit, decrease mH
    print "Constructing observed"
    observed_tanb = graphToTanBeta(observed,mu)
    print "Constructing expected"
    expected_tanb = graphToTanBeta(expected,mu)
    print "Constructing expected 1 sigma"
    expected_1s_tanb = graphToTanBeta(expected_1s, mu, removeNotValid=False)
    print "Constructing expected 2 sigma"
    expected_2s_tanb = graphToTanBeta(expected_2s, mu, removeNotValid=False)
    showLow = 1
    if showLow:
        observed_tanb_low = graphToTanBetaLow(observed,mu)
        expected_tanb_low = graphToTanBetaLow(expected,mu)
        expected_1s_tanb_low = graphToTanBetaLow(expected_1s, mu, removeNotValid=False)
        expected_2s_tanb_low = graphToTanBetaLow(expected_2s, mu, removeNotValid=False)

    # Take the mass points of observed and expected graphs. If the
    # mass point is missing from both of them, remove it from the 1/2
    # sigma bands. Keep the point if it is in observed or in expected
    # graph.
    observed_mp = getMassPoints(observed_tanb)
    expected_mp = getMassPoints(expected_tanb)
    valid_mp = list(set(observed_mp) | set(expected_mp)) # make a union of observed and expected
    valid_mp.sort()
    keepOnlyMassPoints(expected_1s_tanb, valid_mp)
    keepOnlyMassPoints(expected_2s_tanb, valid_mp)
    # Similarly for lower limits
    if showLow:
        observed_mp_low = getMassPoints(observed_tanb_low)
        expected_mp_low = getMassPoints(expected_tanb_low)
        valid_mp_low = list(set(observed_mp_low) | set(expected_mp_low)) # make a union of observed and expected
        valid_mp_low.sort()
        keepOnlyMassPoints(expected_1s_tanb_low, valid_mp_low)
        keepOnlyMassPoints(expected_2s_tanb_low, valid_mp_low)

    # Define the axis ranges
    massMin = valid_mp[0] - 5
    massMax = valid_mp[-1] + 5
    tanbMax = 60#200

    # Create the TCanvas, frame, etc
    canvas = ROOT.TCanvas("mssmLimits")
    frame = canvas.DrawFrame(massMin, 0, massMax, tanbMax)

    # Draw the graphs
    expected_2s_tanb.Draw("F")
    expected_1s_tanb.Draw("F")
    expected_tanb.Draw("LP")
    observed_tanb.SetLineWidth(804)
    observed_tanb.Draw("LP")

    showTeva = 0
    if showTeva:
        TevaCurve = getTevaCurve()
        TevaCurve.Draw("F")

    showLEP = 0
    if showLEP:
        LepCurve = getLepCurve()
        LepCurve.Draw("F")

    if showLow:
        expected_2s_tanb_low.Draw("F")
        expected_1s_tanb_low.Draw("F")
        expected_tanb_low.Draw("LP")
#        observed_tanb_low.SetFillColor(1)
#        observed_tanb_low.SetFillStyle(3006)
        observed_tanb_low.SetLineWidth(-804)
        observed_tanb_low.Draw("LP")

    # Axis labels
    frame.GetXaxis().SetTitle("m_{H^{#pm}} (GeV/c^{2})")
    frame.GetYaxis().SetTitle("tan(#beta)")

    # Legends
    legeX = 0.60
    legeY = 0.28
    pl  = ROOT.TLegend(legeX,legeY,legeX+0.30,legeY+0.30)
    pl.SetTextSize(0.03)
    pl.SetFillStyle(4000)
    pl.SetTextFont(132)
    pl.SetBorderSize(0)
    ple = ROOT.TLegendEntry()
    pl.AddEntry(observed_tanb,     "Observed", "lp")
    pl.AddEntry(expected_tanb,     "Expected median", "lp")
    pl.AddEntry(expected_1s_tanb,  "Expected median #pm1 #sigma", "f")
    pl.AddEntry(expected_2s_tanb,  "Expected median #pm2 #sigma", "f")
    if showLEP:
        pl.AddEntry(LepCurve,  "LEP exclusion", "f")
    if showTeva:
        pl.AddEntry(TevaCurve,  "Tevatron exclusion", "f")
#    if showLow:
#        pl.AddEntry(observed_tanb_low,     "Observed", "lp")
    pl.Draw()
    
    # Text
    #    lumifile = ROOT.TFile.Open("input_luminosity")
    #    lumi = lumifile.Get("tg_obs")
    #     ifstream fileLumi("input_luminosity",ios::in); fileLumi>>L;
    #     ifstream fileLumi("input_luminosity",ios::in);
    #     fileLumi>>L;
    lumifile = open("input_luminosity","r")
    lumi = lumifile.readline()
#    print("Lumi is %d",(L))
    writeTitleTexts(lumi)
    top = 0.9
    lineSpace = 0.038
    writeText("t#rightarrowH^{#pm}b, H^{#pm}#rightarrow#tau#nu",top)
    writeText("Fully hadronic final state",   top - lineSpace)
#    writeText("Bayesian CL limit",           top - 2*lineSpace)
    writeText("Br(H^{#pm}#rightarrow#tau^{#pm} #nu) = 1", top - 3*lineSpace)
    writeText("#mu=%d GeV"%mu, top - 4*lineSpace)

    ROOT.gPad.RedrawAxis()

    # Save to file
    formats = [
        ".png",
        ".C",
        ".eps"
        ]
    for format in formats:
        canvas.SaveAs(format)

####################

            # Define the axis ranges
    massMin = valid_mp[0] - 5
    massMax = valid_mp[-1] + 5
    tanbMax = 60


    # Create the TCanvas, frame, etc
    canvas2 = ROOT.TCanvas("mssmLimits_mus")
    frame2 = canvas.DrawFrame(massMin, 0, massMax, tanbMax)

    # Axis labels
    frame2.GetXaxis().SetTitle("m_{H^{#pm}} (GeV/c^{2})")
    frame2.GetYaxis().SetTitle("tan(#beta)")

    observed_p2 = graphToTanBeta(observed,200)
    observed_m2 = graphToTanBeta(observed,-200)
    observed_pk = graphToTanBeta(observed,1000)
    observed_mk = graphToTanBeta(observed,-1000)

    observed_p2l = graphToTanBetaLow(observed,200)
    observed_m2l = graphToTanBetaLow(observed,-200)
    observed_pkl = graphToTanBetaLow(observed,1000)
    observed_mkl = graphToTanBetaLow(observed,-1000)
                                     
    observed_p2.SetLineColor(1)
    observed_p2.SetMarkerColor(1)
    observed_p2.SetMarkerStyle(20)
    observed_p2.SetLineWidth(504)
    observed_m2.SetLineColor(1)
    observed_m2.SetMarkerColor(1)
    observed_m2.SetMarkerStyle(20)
    observed_m2.SetLineStyle(2)
    observed_m2.SetLineWidth(504)
    observed_pk.SetLineColor(4)
    observed_pk.SetMarkerColor(4)
    observed_pk.SetMarkerStyle(21)
    observed_pk.SetLineWidth(504)
    observed_mk.SetLineColor(4)
    observed_mk.SetMarkerColor(4)
    observed_mk.SetMarkerStyle(21)
    observed_mk.SetLineStyle(2)
    observed_mk.SetLineWidth(504)

    observed_p2l.SetLineColor(1)
    observed_p2l.SetMarkerColor(1)
    observed_p2l.SetMarkerStyle(20)
    observed_p2l.SetLineWidth(-504)
    observed_m2l.SetLineColor(1)
    observed_m2l.SetMarkerColor(1)
    observed_m2l.SetMarkerStyle(20)
    observed_m2l.SetLineStyle(2)
    observed_m2l.SetLineWidth(-504)
    observed_pkl.SetLineColor(4)
    observed_pkl.SetMarkerColor(4)
    observed_pkl.SetMarkerStyle(21)
    observed_pkl.SetLineWidth(-504)
    observed_mkl.SetLineColor(4)
    observed_mkl.SetMarkerColor(4)
    observed_mkl.SetMarkerStyle(21)
    observed_mkl.SetLineStyle(2)
    observed_mkl.SetLineWidth(-504)

    observed_p2.Draw("LP")
    observed_m2.Draw("LP")
    observed_pk.Draw("LP")
    observed_mk.Draw("LP")

    observed_pkl.Draw("LP")
    observed_p2l.Draw("LP")
    observed_m2l.Draw("LP")    
    observed_mkl.Draw("LP")

    # Legends
    legeX = 0.58
    legeY = 0.20
    pl2  = ROOT.TLegend(legeX,legeY,legeX+0.35,legeY+0.24)
    pl2.SetTextSize(0.03)
    pl2.SetFillStyle(4000)
    pl2.SetTextFont(132)
    pl2.SetBorderSize(0)
    pl2.AddEntry(observed_pk,     "Observed, mu=1000", "lp")
    pl2.AddEntry(observed_p2,     "Observed, mu=200", "lp")
    pl2.AddEntry(observed_m2,     "Observed, mu=-200", "lp")
    pl2.AddEntry(observed_mk,     "Observed, mu=-1000", "lp")
                

    pl2.Draw()

    writeTitleTexts(lumi)
    top = 0.83
    lineSpace = 0.038
    writeText("t#rightarrowH^{#pm}b, H^{#pm}#rightarrow#tau#nu",top)
    writeText("Fully hadronic final state",   top - lineSpace)
#    writeText("Bayesian CL limit",           top - 2*lineSpace)
    writeText("Br(H^{#pm}#rightarrow#tau^{#pm} #nu) = 1", top - 3*lineSpace)

    # Save to file
    formats = [
        ".png",
        ".C",
        ".eps"
        ]
    for format in formats:
        canvas2.SaveAs(format)

# If the file is run (and not imported), call function main()
if __name__ == "__main__":
    main()

