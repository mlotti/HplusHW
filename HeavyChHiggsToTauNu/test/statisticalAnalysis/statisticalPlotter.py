from HiggsAnalysis.HeavyChHiggsToTauNu.tools.statisticalFunctions import *

def main():

    luminosity = 50

    mus  = [-1000,-200,200,1000] # mu parameters
    mHps = [90,100,120,140,160]  # H+ masses

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

#    tanbReach = []
#    for selection in massPoints.keys() :
#	for mu in mus.keys() :
#	    for mass in mHps.keys() :
#		tanbAt5sigma = 

    print signif(50,50,0)
    print signalAtNsigma(50,0,5)

main()
