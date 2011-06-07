#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)

def main():
#    postfix = "_Run2010A_Mu9"
#    postfix = "_Run2010B_Mu9"
#    postfix = "_Run2010B_Mu15"
    postfix = "_Run2011A_Mu20"
#    postfix = "_DY_Mu9"

    f = ROOT.TFile.Open("tagprobe_output%s.root" % postfix)

    path = "tnpTree/All/cnt_eff_plots"
    plot = "pt_PLOT"
    graph = "hxy_cnt_eff"

    canv = f.Get(path+"/"+plot)
    canv.SetName("TagProbe%s_%s_%s" % (postfix, plot, graph))
#    canv.SaveAs(".eps")
    canv.SaveAs(".png")


    eff = canv.FindObject(graph)
    #print eff
    eff_value = eff.GetY()[0]
    eff_plus = eff.GetErrorYhigh(0)
    eff_minus = eff.GetErrorYlow(0)

    print "Overall efficiency %f + %f - %f" % (eff_value, eff_plus, eff_minus)

if __name__ == "__main__":
    main()
