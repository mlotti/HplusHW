#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True) # batch mode
from ROOT import TLatex, TLegend, TLegendEntry

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
def graphToTanBeta(graph, removeNotValid=True):
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
            tanb = statisticalFunctions.tanbForBR(yvalues[i], mass, tanbRef, mu)
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
def graphToTanBetaLow(graph, mu=200, removeNotValid=True):
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
            tanb = statisticalFunctions.tanbForBRlow(yvalues[i], mass, tanbRef, mu)
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

    # Create tan beta graphs
    # Convention: begin with low mH, lower limit for 1/2s band
    # then go counterclockwise: increase mH, then switch to upper limit, decrease mH
    print "Constructing observed"
    observed_tanb = graphToTanBeta(observed)
    print "Constructing expected"
    expected_tanb = graphToTanBeta(expected)
    print "Constructing expected 1 sigma"
    expected_1s_tanb = graphToTanBeta(expected_1s, removeNotValid=False)
    print "Constructing expected 2 sigma"
    expected_2s_tanb = graphToTanBeta(expected_2s, removeNotValid=False)
    showLow = 1
    if showLow:
        observed_tanb_low = graphToTanBetaLow(observed)
        expected_tanb_low = graphToTanBetaLow(expected)
        expected_1s_tanb_low = graphToTanBetaLow(expected_1s, removeNotValid=False)
        expected_2s_tanb_low = graphToTanBetaLow(expected_2s, removeNotValid=False)

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
    pl  = ROOT.TLegend(0.58,0.73,0.8,0.92)
    pl.SetTextSize(0.03)
    pl.SetFillStyle(4000)
    pl.SetTextFont(132)
    pl.SetBorderSize(0)
    ple = ROOT.TLegendEntry()
    pl.AddEntry(observed_tanb,     "Observed", "lp")
    pl.AddEntry(expected_tanb,     "Expected median", "lp")
    pl.AddEntry(expected_1s_tanb,  "Expected median #pm1 #sigma", "f")
    pl.AddEntry(expected_2s_tanb,  "Expected median #pm2 #sigma", "f")
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
    
    # Save to file
    formats = [
        ".png",
        ".C",
        ".eps"
        ]
    for format in formats:
        canvas.SaveAs(format)


# If the file is run (and not imported), call function main()
if __name__ == "__main__":
    main()

