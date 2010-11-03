from HiggsAnalysis.HeavyChHiggsToTauNu.tools.statisticalFunctions import *

def main():

    luminosity = 100

    massPoints = {
        "PFTauCutBased": {
	    90:  MassPoint(luminosity*0.1359,20,luminosity*(0.3601+0.2010)),
	    100: MassPoint(luminosity*0.1262,20,luminosity*(0.3601+0.2010)),
	    120: MassPoint(luminosity*0.0943,20,luminosity*(0.3601+0.2010)),
	    140: MassPoint(luminosity*0.0381,20,luminosity*(0.3601+0.2010)),
	    160: MassPoint(luminosity*0.00833,20,luminosity*(0.3601+0.2010))
	},
	"PFTauTaNCBased": {
            90:  MassPoint(luminosity*0.148,20,luminosity*(0.1297+0.2192)),
            100: MassPoint(luminosity*0.1349,20,luminosity*(0.1297+0.2192)),
            120: MassPoint(luminosity*0.1015,20,luminosity*(0.1297+0.2192)),
            140: MassPoint(luminosity*0.0520,20,luminosity*(0.1297+0.2192)),
            160: MassPoint(luminosity*0.0095,20,luminosity*(0.1297+0.2192))
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


#    print signif(50,50,0)
#    print signalAtNsigma(50,0,5)

main()
