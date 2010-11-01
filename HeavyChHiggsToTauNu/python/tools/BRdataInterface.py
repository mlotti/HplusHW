from HiggsAnalysis.HeavyChHiggsToTauNu.tools.FeynHiggsBRdata import *

def getBR_top2bHp(mHp,tanb,mu):
    return interpolate(mHp,tanb,mu).BRt2bH

def get_mA(mHp,tanb,mu):
    return interpolate(mHp,tanb,mu).mA

def getBR_Hp2tau(mHp,tanb,mu):
    return interpolate(mHp,tanb,mu).BRH2taunu

def getDataPoint(mHp,tanb,mu):
    return hplusBranchingRatio[mHp][tanb][mu]

def interpolate(mHp,tanb,mu):
    return linearInterpolation(mHp,tanb,mu)

def lowerTanBPoint(mHp,tanbRef,mu):
    returnTanb = 0
    for tanb in hplusBranchingRatio[mHp].keys():
        if tanb > tanbRef: 
	    return returnTanb
	returnTanb = tanb
    return 0

def higherTanBPoint(mHp,tanbRef,mu):
    if tanbRef < hplusBranchingRatio[mHp].keys()[0]:
	return 0
    for tanb in hplusBranchingRatio[mHp].keys():
        if tanb > tanbRef:
            return tanb
    return 0

def linearInterpolation(mHp,tanb,mu):
    tanb1 = lowerTanBPoint(mHp,tanb,mu)
    tanb2 = higherTanBPoint(mHp,tanb,mu)

    if (tanb1 > int(tanb) or tanb2 < int(tanb)) :
	return BranchingRatio(0,0,0)

    fraction = (tanb - tanb1)/(tanb2 - tanb1)

    point1 = hplusBranchingRatio[mHp][tanb1][mu]
    point2 = hplusBranchingRatio[mHp][tanb2][mu]

    newBRt2bH    = point1.BRt2bH + (point2.BRt2bH - point1.BRt2bH)*fraction
    newBRH2taunu = point1.BRH2taunu + (point2.BRH2taunu - point1.BRH2taunu)*fraction
    newmA        = point1.mA + (point2.mA - point1.mA)*fraction

    return BranchingRatio(newBRt2bH,newBRH2taunu,newmA)

#def main():
#    print lowerTanBPoint(100,121.2,1000)
#    print higherTanBPoint(100,121.2,1000)
#    print interpolate(100,121.2,1000).BRt2bH
#    print interpolate(100,121.2,1000).BRH2taunu
#    print interpolate(100,121.2,1000).mA
#
#main()
