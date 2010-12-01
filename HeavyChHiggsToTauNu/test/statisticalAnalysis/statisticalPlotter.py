from HiggsAnalysis.HeavyChHiggsToTauNu.tools.statisticalFunctions import *

import ROOT
from ROOT import TTree, gROOT, TGraph, TCanvas, TMultiGraph, TLegend, TAxis, TLatex
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from array import array

### Apply TDR style
style = TDRStyle()

gROOT.Reset()
ROOT.gROOT.SetBatch(True)

def getLegend():
    lege = TLegend(0.2, 0.48, 0.55, 0.68)
    lege.SetFillStyle(0)
    lege.SetBorderSize(0)
    lege.SetTextSize(0.03)
    return lege

def writeText( myText, y ):
    text = TLatex()
    text.SetTextAlign(12)
    text.SetTextSize(0.04)
    text.SetNDC()
    text.DrawLatex(0.2,y,myText)
    return 0

def fillDataTeva( ):
    ## Tevatron 1/fb results, D0
    tevaData = {
        "mass":array( 'd' ),
        "tanb":array( 'd' )
        }
    tevaData["mass"].extend([  90,  100,  110, 120,  130,   140, 145  , 148.4])
    tevaData["tanb"].extend([30.8, 33.5, 39.8,  50, 68.4, 103.5, 147.6, 200  ])
    return tevaData

def getGraphTevatron():
    dataTevaMhMax = fillDataTeva()
    myGraph = TGraph(len(dataTevaMhMax["mass"]),dataTevaMhMax["mass"],dataTevaMhMax["tanb"])
    myGraph.SetLineStyle(2)
    myGraph.SetLineWidth(2)
    myGraph.SetMarkerStyle(8)
    return myGraph

def fillDataTheory(mu):
    theoryData  = {
        "mass":array( 'd' ),
        "tanb":array( 'd' )}
    # can only use the following values
    masses = [  90,  100,  120, 140, 160]
    for mass in masses:
        theoryValue = tanbForTheoryLimit(mass,mu)
        if theoryValue>0:
            theoryData["tanb"].append( theoryValue )
            theoryData["mass"].append( mass )
#         else:
#             maxTanbTheory = 219
#             theoryData["tanb"].append( maxTanbTheory )
#             theoryData["mass"].append( mass )
#        print "Theoretical m:",mass,", mu:",mu,", tanb:",theoryValue
    return theoryData

def getGraphTheory(mu):
    # can only go as high as calculated in FeynHiggs
    dataTheory = fillDataTheory(mu)
    myGraph = TGraph(len(dataTheory["mass"]),dataTheory["mass"],dataTheory["tanb"])
    myGraph.SetLineColor(1)
    ## exclWidth = 10
    ## myGraph.SetLineWidth(100*exclWidth+3)
    myGraph.SetLineStyle(1)
    ## myGraph.SetFillStyle(3005)
    myGraph.SetMarkerStyle(8)
    myGraph.SetFillColor(1);
    myGraph.SetFillStyle(3004);
    return myGraph

def fillAreaTheory(mu):
    theoryArea  = {
        "mass":array( 'd' ),
        "tanb":array( 'd' )}
    # can only use the following values
    masses = [  90,  100,  120, 140, 160]
    for mass in masses:
        theoryValue = tanbForTheoryLimit(mass,mu)
        theoryMax = theoryValue + 20
        if theoryValue>0:
            theoryArea["tanb"].insert( 0, theoryValue )
            theoryArea["mass"].insert( 0, mass )
            theoryArea["tanb"].append( theoryMax )
            theoryArea["mass"].append( mass )
    return theoryArea


def getAreaTheory(mu):
    # can only go as high as calculated in FeynHiggs
    dataTheory = fillAreaTheory(mu)
    myArea = TGraph(len(dataTheory["mass"]),dataTheory["mass"],dataTheory["tanb"])
#    myArea.SetLineColor(1)
#    myArea.SetLineWidth(0)
#    myArea.SetFillStyle(3)
    myArea.SetFillColor(1);
    myArea.SetFillStyle(3004);
    myArea.SetLineColor(418);
    myArea.SetLineWidth(0);
    myArea.SetLineColor(0);
    return myArea
    
def main():

    luminosity = 80  #35.76

    # add here data to be plotted
#     dataName = "PFTauCutBased"
#     background = 0.3601+0.2010
#     sigmas = [ 0.1359, 0.1262, 0.0943, 0.0381, 0.00833 ]
    
#     dataName = "PFTauTaNCBased"
#     qcd = 0.1297
#     wjets = 0.0266
#     NttNoH = 0.1926
#     background = qcd + wjets + NttNoH
#     sigmas = [ 0.148, 0.1349, 0.1015, 0.0520, 0.0095 ] # signaalin vaikutusala

    dataName = "HPS_TauID"#"HPS TauID, MET>70 GeV, 3 jets"
    qcd = 0.0016
    wjets = 0.0257
    NttNoH = 0.0522
    background = qcd + wjets + NttNoH
    sigmas = [ 0.04812, 0.044, 0.0334, 0.0169, 0.00324 ]
#    [  0.540728, 0.579466, 0.690689, 0.745804, 0.7433 ]
            #      0.148, 0.1349, 0.1015, 0.0520, 0.0095 ]
    
    massPoints = {
	dataName: {
            90:  MassPoint(luminosity*sigmas[0],20,luminosity*background),
            100: MassPoint(luminosity*sigmas[1],20,luminosity*background),
            120: MassPoint(luminosity*sigmas[2],20,luminosity*background),
            140: MassPoint(luminosity*sigmas[3],20,luminosity*background),
            160: MassPoint(luminosity*sigmas[4],20,luminosity*background)
	}
    }

    mus  = [-1000,-200,200,1000] # mu parameters for plot with different mus
    mHps  = massPoints[dataName].keys() # H+ masses
    mHps.sort()

    data = {}
        
    nSigma = 5
    clSigma = 1.95996
    sysError = 0.2
    for selection in massPoints.keys() :
	print selection
        data[selection] = {}
	for mu in mus :
	    print "mu = ",mu
            nPoints = 5
            data[selection][mu] = {}
            listOfGraphs = ["Exclusion","exclusion_syst","ReachNoErr","ReachWErr","ReachTheory"]
            for thisGraphType in listOfGraphs:
                data[selection][mu][thisGraphType] = {
                    "mass":array( 'd' ),
                    "tanb":array( 'd' )
                    }
            massArray  = array( 'd' )
	    for mass in mHps :
		tanbTheoryReach = tanbForTheoryLimit(mass,mu)
#		print massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,mass,mu
#		print signif(massPoints[selection][mass].nSignal,massPoints[selection][mass].nBackgr,0),signalAtNsigma(massPoints[selection][mass].nBackgr,0,5)
		tanbAt5sigmaNoErr = tanbAtNsigma(massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,0,mass,mu,nSigma)
		tanbAt5sigmaWErr = tanbAtNsigma(massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,sysError,mass,mu,nSigma)
		tanbAt95CLNoErr = tanbAtNsigma(massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,0,mass,mu,clSigma)
		tanbAt95CLWErr = tanbAtNsigma(massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,sysError,mass,mu,clSigma)
		print "mass,th-reach,reach,reach(sys),excl,excl(sys) = ",mass,tanbTheoryReach,tanbAt5sigmaNoErr,tanbAt5sigmaWErr,tanbAt95CLNoErr,tanbAt95CLWErr
                massArray.append(mass)

                # Fill data structures
                if tanbAt95CLNoErr>0:
                    data[selection][mu]["Exclusion"]["mass"].append(mass)
                    data[selection][mu]["Exclusion"]["tanb"].append(tanbAt95CLNoErr)
                if tanbAt95CLWErr>0:
                    data[selection][mu]["exclusion_syst"]["mass"].append(mass)
                    data[selection][mu]["exclusion_syst"]["tanb"].append(tanbAt95CLWErr)
                if tanbAt5sigmaNoErr>0:    
                    data[selection][mu]["ReachNoErr"]["mass"].append(mass)
                    data[selection][mu]["ReachNoErr"]["tanb"].append(tanbAt5sigmaNoErr)
                if tanbAt5sigmaWErr>0:
                    data[selection][mu]["ReachWErr"]["mass"].append(mass)
                    data[selection][mu]["ReachWErr"]["tanb"].append(tanbAt5sigmaWErr)
                if tanbTheoryReach>0:
                    data[selection][mu]["ReachTheory"]["mass"].append(mass)
                    data[selection][mu]["ReachTheory"]["tanb"].append(tanbTheoryReach)
                    
    ## Graph: different mu values
    ## plot theory reach & 5sigmaNoErr & Tevatron exclusion
    ## this code could be improved to use the data structure "data"                    
    for selection in massPoints.keys() :
        color = 1
#        print 'muPlot'+selection
        c1 = TCanvas( 'muPlot'+selection, 'tanbReach'+selection, 200, 10, 700, 500 )
        multi = TMultiGraph()
        lege = getLegend()
        writeText("L = "+str(luminosity)+" pb^{-1}", 0.9)
        writeText("m_{H}^{max} scenario",0.84)
        writeText("t#rightarrowbH#pm#rightarrowb#tau#nu#rightarrowhadrons + #nu", 0.78)
        writeText(selection+", no syst. errors", 0.72)
        for mu in mus :
            yvalues, massArray = array( 'd' ), array( 'd' )
#            print "mu = ",mu
            for mass in mHps :
                tanbTheoryReach = tanbForTheoryLimit(mass,mu)
                tanbAt5sigmaNoErr = tanbAtNsigma(massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,0,mass,mu,nSigma)
                # Skip points with tanB = -1 
                if tanbAt5sigmaNoErr != -1 :
                    yvalues.append( tanbAt5sigmaNoErr )
                    massArray.append(mass)
#                print "graph1, theory & 5sigma & mass: ",tanbTheoryReach,tanbAt5sigmaNoErr, mass
            if len(massArray)>0:
                graphMus = TGraph(len(massArray),massArray,yvalues)
                graphMus.SetLineColor(color)
                graphMus.SetMarkerColor(color)
                multi.Add(graphMus,"lp")
                lege.AddEntry(graphMus,"5 sigma, mu = "+str(mu),"l")
            color = color + 1
        # Tevatron result
        graphTeva = getGraphTevatron()
        multi.Add(graphTeva,"lp")
        lege.AddEntry(graphTeva,"Tevatron 1fb^{-1} exclusion","l")
        lege.Draw()
        multi.Draw("a")
        c1.Update()
        multi.GetYaxis().SetRangeUser(0,210)
        multi.GetYaxis().SetTitle("tan(#beta)")
        multi.GetXaxis().SetTitle("M_{H^{#pm}} [GeV/c^{2}]")
        addCmsPreliminaryText()
        c1.SaveAs(".png")

## Plot comparison of reach and exclusion for the 2 selections
## fix mu=200       
## make one plot without errors, one with errors
    setOfSetOfGraphs = [ ["ReachNoErr","Exclusion"],
                         ["ReachWErr", "exclusion_syst"]   ]
    for index, setOfGraphs in enumerate(setOfSetOfGraphs):
        c1 = TCanvas("exclusions"+str(index),"exclusions"+str(index),200, 10, 700, 500 )
        multi = TMultiGraph()
        lege = getLegend()
        fixedMu = 200
        color = 1
        for selection in massPoints.keys() :
            for oneGraph in setOfGraphs:
                graph = TGraph(len(data[selection][fixedMu][oneGraph]["mass"]),
                               data[selection][fixedMu][oneGraph]["mass"],
                               data[selection][fixedMu][oneGraph]["tanb"])
                graph.SetLineColor(color)
                graph.SetMarkerColor(color)
                lege.AddEntry(graph,selection+", "+oneGraph,"l")
                multi.Add(graph,"cp")
                color = color + 1
        graphTeva = getGraphTevatron()
        multi.Add(graphTeva,"cp")
        lege.AddEntry(graphTeva,"Tevatron 1fb^{-1} exclusion","l")

        graphTheory = getGraphTheory(fixedMu)
        graphTheoryArea = getAreaTheory(fixedMu)
        multi.Add(graphTheory)
        lege.AddEntry(graphTheory,"Theoretically inaccessible","f")
        multi.Draw("alp")
        graphTheoryArea.Draw("f")
        multi.Draw("lp")
        lege.Draw()
        addCmsPreliminaryText()
        writeText("L = "+str(luminosity)+" pb^{-1}", 0.9)
        writeText("m_{H}^{max} scenario",0.85)
        writeText("t#rightarrowbH#pm#rightarrowb#tau#nu#rightarrowhadrons + #nu", 0.8)
        writeText("#mu = "+str(fixedMu)+" GeV/c^{2}, "+str(100*sysError)+"% syst.error", 0.75)
        multi.GetYaxis().SetRangeUser(0,210)
        multi.GetYaxis().SetTitle("tan(#beta)")
        multi.GetXaxis().SetTitle("M_{H^{#pm}} [GeV/c^{2}]")
        c1.SaveAs(".png")

    ## Plot reach in 
    ## fix mu=200       
    ## make one plot without errors, one with errors
    setOfSetOfGraphs = [ ["ReachNoErr","ReachWErr"],
                         ["Exclusion","exclusion_syst"] ]
    for index, setOfGraphs in enumerate(setOfSetOfGraphs):
        c1 = TCanvas("newexclusions"+str(index),"exclusions"+str(index),200, 10, 700, 500 )
        multi = TMultiGraph()
        lege = getLegend()
        fixedMu = 200
        color = 1
        for selection in massPoints.keys() :
            for oneGraph in setOfGraphs:
                graph = TGraph(len(data[selection][fixedMu][oneGraph]["mass"]),
                               data[selection][fixedMu][oneGraph]["mass"],
                               data[selection][fixedMu][oneGraph]["tanb"])
                graph.SetLineColor(color)
                graph.SetMarkerColor(color)
                lege.AddEntry(graph,selection+", "+oneGraph,"l")
                multi.Add(graph)
                color = color + 1
        graphTeva = getGraphTevatron()
#        multi.Add(graphTeva,"cp")
        multi.Add(graphTeva)
        lege.AddEntry(graphTeva,"Tevatron 1fb^{-1} exclusion","l")
        graphTheory = getGraphTheory(fixedMu)
        graphTheoryArea = getAreaTheory(fixedMu)
        multi.Add(graphTheory)
        lege.AddEntry(graphTheory,"Theoretically inaccessible","f")
        multi.Draw("alp")
        graphTheoryArea.Draw("f")
        multi.Draw("lp")
        lege.Draw()
        addCmsPreliminaryText()
        writeText("L = "+str(luminosity)+" pb^{-1}", 0.9)
        writeText("m_{H}^{max} scenario",0.85)
        writeText("t#rightarrowbH#pm#rightarrowb#tau#nu#rightarrowhadrons + #nu", 0.8)
        writeText("#mu = "+str(fixedMu)+" GeV/c^{2}, "+str(100*sysError)+"% syst.error", 0.75)
        multi.GetYaxis().SetRangeUser(0,215)
        multi.GetYaxis().SetTitle("tan(#beta)")
        multi.GetXaxis().SetTitle("M_{H^{#pm}} [GeV/c^{2}]")
        c1.SaveAs(".png")

    ############################### EXECUTION ###############################
    ### Script execution can be paused like this, it will continue after
    ### user has given some input (which must include enter)
#    raw_input("Hit enter to continue") ### keep canvas open until you hit enter

#    print signif(50,50,0)
#    print signalAtNsigma(50,0,5)

main()
