from MCatNLOxsecData import *

def getXsecTimesBR(ecm,mHp,tanb,mu):
    return getBR_Hp2tau(mHp,tanb,mu)*getXsec(ecm,mHp,tanb,mu)

def get_mA(mHp,tanb,mu):
    return interpolate(mHp,tanb,mu).mA

def getBR_Hp2tau(mHp,tanb,mu):
#    return interpolate(mHp,tanb,mu).BRH2taunu
    return interpolate(mHp,tanb,mu).brHp2taunu

def getXsec(ecm,mHp,tanb,mu):
    if ecm == 7:
	return getXsec7TeV(mHp,tanb,mu)
    if ecm == 8:
	return getXsec8TeV(mHp,tanb,mu)
    if ecm == 14:
	return getXsec14TeV(mHp,tanb,mu)

# Xsecs scaled from FH(at 14TeV) values using MC@NLO. Other option is to use MC@NLO xsecs directly
def getXsec7TeV(mHp,tanb,mu):
#    return getDataPoint(mHp,tanb,mu).xsec7_mcatnlo
    return getDataPoint(mHp,tanb,mu).xsec14_fh/getDataPoint(mHp,tanb,mu).xsec14_mcatnlo*getDataPoint(mHp,tanb,mu).xsec7_mcatnlo

def getXsec8TeV(mHp,tanb,mu):
#    return getDataPoint(mHp,tanb,mu).xsec8_mcatnlo
    return getDataPoint(mHp,tanb,mu).xsec14_fh/getDataPoint(mHp,tanb,mu).xsec14_mcatnlo*getDataPoint(mHp,tanb,mu).xsec8_mcatnlo

def getXsec14TeV(mHp,tanb,mu):
#    return getDataPoint(mHp,tanb,mu).xsec14_mcatnlo
    return getDataPoint(mHp,tanb,mu).xsec14_fh

def getDataPoint(mHp,tanb,mu):
    return hplusXsec[mHp][tanb][mu]

def interpolate(mHp,tanb,mu):
    return linearInterpolation(mHp,tanb,mu)

def lowerTanBPoint(mHp,tanbRef,mu):
    returnTanb = 0
    for tanb in sorted(hplusXsec[mHp].keys()):
	if tanb == tanbRef:
	    return tanb
        if tanb > tanbRef: 
	    return returnTanb
	returnTanb = tanb
    return 0

def higherTanBPoint(mHp,tanbRef,mu):
    if tanbRef < sorted(hplusXsec[mHp].keys())[0]:
	return 0
    for tanb in sorted(hplusXsec[mHp].keys()):
        if tanb >= tanbRef:
            return tanb
    return 0

def linearInterpolation(mHp,tanb,mu):
    tanb1 = lowerTanBPoint(mHp,tanb,mu)
    tanb2 = higherTanBPoint(mHp,tanb,mu)

    if (tanb1 == 0 or tanb2 == 0 or tanb1 > int(tanb) or tanb2 < int(tanb)) :
	return DataHelper(0,0,0,0,0,0)

    fraction = 1
    if tanb1 < tanb2:
        fraction = (tanb - tanb1)/(tanb2 - tanb1)

    point1 = hplusXsec[mHp][tanb1][mu]
    point2 = hplusXsec[mHp][tanb2][mu]

    newmA             = point1.mA + (point2.mA - point1.mA)*fraction
    newxsec14_fh      = point1.xsec14_fh + (point2.xsec14_fh - point1.xsec14_fh)*fraction
    newxsec14_mcatnlo = point1.xsec14_mcatnlo + (point2.xsec14_mcatnlo - point1.xsec14_mcatnlo)*fraction
    newxsec7_mcatnlo  = point1.xsec7_mcatnlo + (point2.xsec7_mcatnlo - point1.xsec7_mcatnlo)*fraction
    newxsec8_mcatnlo  = point1.xsec8_mcatnlo + (point2.xsec8_mcatnlo - point1.xsec8_mcatnlo)*fraction
    newbrHp2taunu     = point1.brHp2taunu + (point2.brHp2taunu - point1.brHp2taunu)*fraction

    return DataHelper(newmA,newxsec14_fh,newxsec14_mcatnlo,newxsec7_mcatnlo,newxsec8_mcatnlo,newbrHp2taunu)

def getTanb(mHp,mu,targetBRt2bH):
    tanb = 20 # initial guess
    BRt2bH = interpolate(mHp,tanb,mu).BRt2bH
    while abs(BRt2bH - targetBRt2bH)/targetBRt2bH > 0.00001 and tanb < 219 :
        tanb = tanb - 0.01*tanb*(BRt2bH - targetBRt2bH)/targetBRt2bH
	BRt2bH = interpolate(mHp,tanb,mu).BRt2bH
	#print targetBRt2bH,BRt2bH,tanb

    return tanb

def main():
#    print lowerTanBPoint(100,121.2,1000)
#    print higherTanBPoint(100,121.2,1000)
#    print interpolate(100,121.2,1000).BRt2bH
#    print interpolate(100,121.2,1000).BRH2taunu
#    print interpolate(100,121.2,1000).mA
    print getTanb(100,200,0.05);

#main()
