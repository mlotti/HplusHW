#!/usr/bin/env python

import sys
import os
import ROOT
import array

rebin = [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,600,700,800]

def findfiles(inputDir):

    files = []

    subdirs = []
    cands = execute("ls %s"%inputDir)
    for d in cands:
        if "SignalAnalysis" in d or d == "pseudoMulticrab_QCDMeasurement":
            subdirs.append(os.path.join(inputDir,d))

    for d in subdirs:
        ssdirs = execute("ls %s"%d)
        for sd in ssdirs:
            cand = os.path.join(d,sd)
            if os.path.isdir(cand):
                fcand = os.path.join(cand,"res","histograms-%s.root"%sd)
                if os.path.exists(fcand):
                    files.append(fcand)
    return files

def addPostFit(fnameIN):
    print "Adding postfit",fnameIN

#    fnameIN = sys.argv[1]
    fnameIN2 = "outputHeavy.root"
#    fnameIN2 = "outputLight.root"
    histoIn = "SignalAnalysis_80to1000_Run2016BCD/ForDataDrivenCtrlPlots/shapeTransverseMass"

    rootpath1,rootpath2,histoname = histoIn.split("/")

    doNotChange = False
####    if "Tau_" in fnameIN or "ChargedHiggs_" in fnameIN:
    if "ChargedHiggs_" in fnameIN:
        doNotChange = True

    fIN2 = ROOT.TFile.Open(fnameIN2,"R")

    if not doNotChange:
        bgr = ""
        if "-DYJetsToLL_M_50." in fnameIN:
            bgr = "DY_t_genuine"
        if "-WJetsToLNu." in fnameIN:
            bgr = "W_t_genuine"
        if "-TT." in fnameIN:
            bgr = "ttbar_t_genuine"
        if "-ST_t_channel_top_4f_inclusiveDecays." in fnameIN:
            bgr = "singleTop_t_genuine"
        if "-WW." in fnameIN:
            bgr = "VV_t_genuine"
        if "-QCDMeasurementMT." in fnameIN:
            bgr = "QCDandFakeTau"
            rootpath1 = "signalAnalysis_80to1000_Run2016BCD" # lowercase s in QCD analysis, FIX qcd pseudo making
	if "-Tau_Run2016B" in fnameIN:
            bgr = "data_obs"


        histoIN2 = "CMS_Hptntj_"+bgr
	if bgr == "data_obs":
            histoIN2 = bgr
####        histoIN2 = bgr

#        fIN2 = ROOT.TFile.Open(fnameIN2,"R")
        fIN2.cd()
        if bgr == "":
            histoIN2 = "CMS_Hptntj_ttbar_t_genuine"
####            histoIN2 = "ttbar_t_genuine"
            h_IN2 = fIN2.Get(histoIN2)
            h_IN2.Reset()
        else:
            h_IN2 = fIN2.Get(histoIN2)

    fIN  = ROOT.TFile.Open(fnameIN,"UPDATE")
    fIN.cd(os.path.join(rootpath1,rootpath2))

    if doNotChange: # copy unmodified histo as <histoname>_POSTFIT
        h_IN2 = fIN.Get(os.path.join(rootpath1,rootpath2,histoname))
    h_IN2 = h_IN2.Rebin(len(rebin)-1,h_IN2.GetName(),array.array("d",rebin))

    h_IN2.Write(histoname+"_POSTFIT")

    fIN.Close()
    fIN2.Close()

def execute(cmd):
    f = os.popen4(cmd)[1]
    ret=[]
    for line in f:
        ret.append(line.replace("\n", ""))
    f.close()
    return ret

def main():

    inputDir = sys.argv[1]
    rootFiles = findfiles(inputDir)

    for f in rootFiles:
        addPostFit(f)

if __name__ == "__main__":
    main()

### DY W ttbar QCDanfFakeTau
