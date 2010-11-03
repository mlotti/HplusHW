from HiggsAnalysis.HeavyChHiggsToTauNu.tools.statisticalFunctions import *

import ROOT
from ROOT import TTree, gROOT, TGraph, TCanvas, TMultiGraph, TLegend, TAxis
#from HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms import *
from HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle import *
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
from array import array

### Apply TDR style
style = TDRStyle()
gROOT.Reset()
ROOT.gROOT.SetBatch(True) 

def main():

    luminosity = 100

    ## Tevatron 1/fb results
    tanbExclwErrTevatronArray = array( 'd' )
    tanbExclwErrTevatronArray.append(30.8)
    tanbExclwErrTevatronArray.append(33.5)
    tanbExclwErrTevatronArray.append(50)
    tanbExclwErrTevatronArray.append(103.5)
    massTevatronArray = array( 'd' )
    massTevatronArray.append(90)
    massTevatronArray.append(100)
    massTevatronArray.append(120)
    massTevatronArray.append(140)
                             
    massPoints = {
        "PFTauCutBased": {
	    90:  MassPoint(luminosity*0.1359,20,luminosity*(0.3601+0.2010)),
	    100: MassPoint(luminosity*0.1262,20,luminosity*(0.3601+0.2010)),
	    120: MassPoint(luminosity*0.0943,20,luminosity*(0.3601+0.2010)),
	    140: MassPoint(luminosity*0.0381,20,luminosity*(0.3601+0.2010)),
#	    160: MassPoint(luminosity*0.00833,20,luminosity*(0.3601+0.2010))
	},
	"PFTauTaNCBased": {
            90:  MassPoint(luminosity*0.148,20,luminosity*(0.1297+0.2192)),
            100: MassPoint(luminosity*0.1349,20,luminosity*(0.1297+0.2192)),
            120: MassPoint(luminosity*0.1015,20,luminosity*(0.1297+0.2192)),
            140: MassPoint(luminosity*0.0520,20,luminosity*(0.1297+0.2192)),
#            160: MassPoint(luminosity*0.0095,20,luminosity*(0.1297+0.2192))
	}
    }

    mus  = [-1000,-200,200,1000] # mu parameters
    mHps  = massPoints["PFTauCutBased"].keys() # H+ masses
    mHps.sort()
#    mus  = [200]
#    mHps = [120]

    nSigma = 5
    clSigma = 1.95996
    sysError = 0.1
    for selection in massPoints.keys() :
	print selection
	for mu in mus :
	    print "mu = ",mu
	    tanbExclNoErr   = []
	    tanbExclWErr    = []
	    tanbReachNoErr  = []
	    tanbReachWErr   = []
	    tanbReachTheory = []
            nPoints = 4
            massArray, tanbExclNoErrArray, tanbExclWErrArray, tanbReachNoErrArray, tanbReachWErrArray, tanbReachTheoryArray = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' ),array( 'd' )
	    for mass in mHps :
		tanbTheoryReach = tanbForTheoryLimit(mass,mu)
		tanbReachTheory.append(tanbTheoryReach)
#		print massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,mass,mu
#		print signif(massPoints[selection][mass].nSignal,massPoints[selection][mass].nBackgr,0),signalAtNsigma(massPoints[selection][mass].nBackgr,0,5)
		tanbAt5sigmaNoErr = tanbAtNsigma(massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,0,mass,mu,nSigma)
		tanbAt5sigmaWErr = tanbAtNsigma(massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,sysError,mass,mu,nSigma)
		tanbAt95CLNoErr = tanbAtNsigma(massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,0,mass,mu,clSigma)
		tanbAt95CLWErr = tanbAtNsigma(massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,sysError,mass,mu,clSigma)
		print "mass,th-reach,reach,reach(sys),excl,excl(sys) = ",mass,tanbTheoryReach,tanbAt5sigmaNoErr,tanbAt5sigmaWErr,tanbAt95CLNoErr,tanbAt95CLWErr
		tanbReachNoErr.append(tanbAt5sigmaNoErr)
		tanbReachWErr.append(tanbAt5sigmaWErr)
		tanbExclNoErr.append(tanbAt95CLNoErr)
		tanbExclWErr.append(tanbAt95CLWErr)
                massArray.append(mass)
                tanbExclNoErrArray.append(tanbAt5sigmaNoErr)
                tanbExclWErrArray.append(tanbAt5sigmaWErr)
                tanbReachNoErrArray.append(tanbAt95CLNoErr)
                tanbReachWErrArray.append(tanbAt95CLNoErr)
                tanbReachTheoryArray.append(tanbAt95CLWErr)

# Plot everything in one canvas
#    c1 = TCanvas( 'c1', 'tanbReach', 200, 10, 700, 500 )
#    graphExclNoErr   = TGraph(nPoints,massArray,tanbExclNoErrArray)
#    graphExclWErr    = TGraph(nPoints,massArray,tanbExclWErrArray)
#    graphReachNoErr  = TGraph(nPoints,massArray,tanbReachNoErrArray)
#    graphReachWErr   = TGraph(nPoints,massArray,tanbReachWErrArray)
#    graphReachTheory = TGraph(nPoints,massArray,tanbReachTheoryArray)
#    graphTevatron = TGraph(nPoints,massTevatronArray,tanbExclwErrTevatronArray)
#    graphExclNoErr.Draw('ALP')   
#    graphExclWErr.Draw('LP')    
#    graphReachNoErr.Draw('LP')      
#    graphReachWErr.Draw('LP')       
#    graphReachTheory.Draw('LP')
#    graphTevatron.SetLineColor(2)     
#    graphTevatron.Draw('LP')     
#    addCmsPreliminaryText()
#    c1.Update()
#    c1.SaveAs(".png")

    ## Graph: different mu values
    ## plot theory reach & 5sigmaNoErr & Tevatron exclusion
    for selection in massPoints.keys() :
        color = 1
        print 'muPlot'+selection
        c1 = TCanvas( 'muPlot'+selection, 'tanbReach'+selection, 200, 10, 700, 500 )
        multi = TMultiGraph();
        lege = TLegend(0.75, 0.8, 0.95, 0.93)
        lege.SetFillStyle(0)
        lege.SetBorderSize(0)
        for mu in mus :
            yvalues, massArray = array( 'd' ), array( 'd' )
            print "mu = ",mu
            for mass in mHps :
                tanbTheoryReach = tanbForTheoryLimit(mass,mu)
                tanbAt5sigmaNoErr = tanbAtNsigma(massPoints[selection][mass].nSignal,massPoints[selection][mass].tanbRef,massPoints[selection][mass].nBackgr,0,mass,mu,nSigma)
                # Skip points with tanB = -1 
                if tanbAt5sigmaNoErr != -1 :
                    yvalues.append( tanbAt5sigmaNoErr )
                    massArray.append(mass)
                print "graph1, theory & 5sigma & mass: ",tanbTheoryReach,tanbAt5sigmaNoErr, mass
            if len(massArray)>0:
                graphMus = TGraph(len(massArray),massArray,yvalues)
                graphMus.SetLineColor(color)
                graphMus.SetMarkerColor(color)
                multi.Add(graphMus,"lp")
                lege.AddEntry(graphMus,"5 sigma, mu = "+str(mu),"l")
            color = color + 1
        # Tevatron result
        graphTeva = TGraph(len(tanbExclwErrTevatronArray),massTevatronArray,tanbExclwErrTevatronArray)
        multi.Add(graphTeva,"lp")
        lege.AddEntry(graphTeva,"Tevatron 1/fb exclusion","l")
        lege.Draw()
        multi.Draw("a")
        c1.Update()
        multi.GetYaxis().SetTitle("tan(#beta)")
        multi.GetXaxis().SetTitle("M_{H^{#pm}} [GeV/c^{2}]")
        addCmsPreliminaryText()
        c1.SaveAs(".png")
                
    ############################### EXECUTION ###############################
    ### Script execution can be paused like this, it will continue after
    ### user has given some input (which must include enter)
#    raw_input("Hit enter to continue") ### keep canvas open until you hit enter

#    print signif(50,50,0)
#    print signalAtNsigma(50,0,5)



main()
