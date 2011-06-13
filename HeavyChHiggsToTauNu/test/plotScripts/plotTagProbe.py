#!/usr/bin/env python

import math

import ROOT
ROOT.gROOT.SetBatch(True)

def getEfficiency(postfix):
    f = ROOT.TFile.Open("tagprobe_output_%s.root" % postfix)

#    cntfit = "cnt"
    cntfit = "fit"

    path = "tnpTree/All/%s_eff_plots" % cntfit
    plot = "pt_PLOT"
    graph = "hxy_%s_eff" % cntfit

    canv = f.Get(path+"/"+plot)
    canv.SetName("TagProbe_%s_%s_%s" % (postfix, plot, graph))
#    canv.SaveAs(".eps")
    canv.SaveAs(".png")


    eff = canv.FindObject(graph)
    #print eff
    eff_value = eff.GetY()[0]
    eff_plus = eff.GetErrorYhigh(0)
    eff_minus = eff.GetErrorYlow(0)

    print "%s overall efficiency %f + %f - %f" % (postfix, eff_value, eff_plus, eff_minus)
    return (eff_value, eff_plus, eff_minus)

def main():
    data = [
#        "Run2010A_Mu9",
#        "Run2010B_Mu9",
#        "Run2010B_Mu15",
        ("Run2011A_Mu20", 5.0644747570000002+26.123554120999998),
        ("Run2011A_Mu24", 157.79184244000001),
        ]
    mc = "DY_Mu9"

    totalLumi = 0
    totalEff = 0
    totalErr = 0
    for d, lumi in data:
        (eff_value, eff_plus, eff_minus) = getEfficiency(d)
        print " lumi: %f" % lumi
        err = max(eff_plus, eff_minus)

        totalLumi += lumi
        totalEff += lumi * eff_value
        totalErr += lumi * err*err

    totalEff = totalEff/totalLumi
    totalErr = math.sqrt(totalErr/totalLumi)
    print "Data overall efficiency %f \\pm %f" % (totalEff, totalErr)
    
    (mc_value, mc_plus, mc_minus) = getEfficiency(mc)
    mc_err = max(mc_plus, mc_minus)

    rho = totalEff/mc_value
    rho_err = math.sqrt( (totalErr/mc_value)**2 + (totalErr*mc_err/(mc_value**2))**2)

    syst = abs(totalEff-mc_value)/totalEff
    
    print "Data/MC rho %f \\pm %f" % (rho, rho_err)
    print "Systematic uncertainty %f, relative %f" % (syst, syst/totalEff)

if __name__ == "__main__":
    main()
