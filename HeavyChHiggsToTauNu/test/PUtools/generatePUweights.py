#! /usr/bin/env python

import sys
import ROOT

# https://twiki.cern.ch/twiki/bin/view/CMS/Pileup_MC_Gen_Scenarios
def Summer12_S10():
    # 60 bins
    distribution = [
        2.560E-06,
        5.239E-06,
        1.420E-05,
        5.005E-05,
        1.001E-04,
        2.705E-04,
        1.999E-03,
        6.097E-03,
        1.046E-02,
        1.383E-02,
        1.685E-02,
        2.055E-02,
        2.572E-02,
        3.262E-02,
        4.121E-02,
        4.977E-02,
        5.539E-02,
        5.725E-02,
        5.607E-02,
        5.312E-02,
        5.008E-02,
        4.763E-02,
        4.558E-02,
        4.363E-02,
        4.159E-02,
        3.933E-02,
        3.681E-02,
        3.406E-02,
        3.116E-02,
        2.818E-02,
        2.519E-02,
        2.226E-02,
        1.946E-02,
        1.682E-02,
        1.437E-02,
        1.215E-02,
        1.016E-02,
        8.400E-03,
        6.873E-03,
        5.564E-03,
        4.457E-03,
        3.533E-03,
        2.772E-03,
        2.154E-03,
        1.656E-03,
        1.261E-03,
        9.513E-04,
        7.107E-04,
        5.259E-04,
        3.856E-04,
        2.801E-04,
        2.017E-04,
        1.439E-04,
        1.017E-04,
        7.126E-05,
        4.948E-05,
        3.405E-05,
        2.322E-05,
        1.570E-05,
        5.005E-06
        ]
    return distribution

def Summer12_S7():
    # 60 bins
    distribution = [
        2.344E-05,
        2.344E-05,
        2.344E-05,
        2.344E-05,
        4.687E-04,
        4.687E-04,
        7.032E-04,
        9.414E-04,
        1.234E-03,
        1.603E-03,
        2.464E-03,
        3.250E-03,
        5.021E-03,
        6.644E-03,
        8.502E-03,
        1.121E-02,
        1.518E-02,
        2.033E-02,
        2.608E-02,
        3.171E-02,
        3.667E-02,
        4.060E-02,
        4.338E-02,
        4.520E-02,
        4.641E-02,
        4.735E-02,
        4.816E-02,
        4.881E-02,
        4.917E-02,
        4.909E-02,
        4.842E-02,
        4.707E-02,
        4.501E-02,
        4.228E-02,
        3.896E-02,
        3.521E-02,
        3.118E-02,
        2.702E-02,
        2.287E-02,
        1.885E-02,
        1.508E-02,
        1.166E-02,
        8.673E-03,
        6.190E-03,
        4.222E-03,
        2.746E-03,
        1.698E-03,
        9.971E-04,
        5.549E-04,
        2.924E-04,
        1.457E-04,
        6.864E-05,
        3.054E-05,
        1.282E-05,
        5.081E-06,
        1.898E-06,
        6.688E-07,
        2.221E-07,
        6.947E-08,
        2.047E-08
        ]
    return distribution

def Fall11():
    # 50 bins
    distribution = [
        0.003388501,
        0.010357558,
        0.024724258,
        0.042348605,
        0.058279812,
        0.068851751,
        0.072914824,
        0.071579609,
        0.066811668,
        0.060672356,
        0.054528356,
        0.04919354,
        0.044886042,
        0.041341896,
        0.0384679,
        0.035871463,
        0.03341952,
        0.030915649,
        0.028395374,
        0.025798107,
        0.023237445,
        0.020602754,
        0.0180688,
        0.015559693,
        0.013211063,
        0.010964293,
        0.008920993,
        0.007080504,
        0.005499239,
        0.004187022,
        0.003096474,
        0.002237361,
        0.001566428,
        0.001074149,
        0.000721755,
        0.000470838,
        0.00030268,
        0.000184665,
        0.000112883,
        6.74043E-05,
        3.82178E-05,
        2.22847E-05,
        1.20933E-05,
        6.96173E-06,
        3.4689E-06,
        1.96172E-06,
        8.49283E-07,
        5.02393E-07,
        2.15311E-07,
        9.56938E-08
        ]
    return distribution

def usage():
    print "Usage: -datainput datadistribution.root -mcdistribution Fall11/Summer12_S7/Summer12_S10 -o output.root"
    print ""
    print "Obtain MC distributions from:"
    print "  https://twiki.cern.ch/twiki/bin/view/CMS/Pileup_MC_Gen_Scenarios"
    print "Instructions for obtaining distribution from data:"
    print "  https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData"
    print ""
    sys.exit()


def expandMC(name, distribution):
    # Expand MC histogram to number of data bins
    hMC = ROOT.TH1F("pileup","pileup",len(distribution)*20,0,len(distribution))
    i = 0
    mylistindex = 0
    for j in range(1, hMC.GetNbinsX()):
        hMC.SetBinContent(j, distribution[mylistindex])
        i += 1
        if (i == 20):
            i = 0
            mylistindex += 1
    hMC.Scale(1.0 / hMC.Integral())
    mymcfile = ROOT.TFile("PU_MC_"+name+".root","RECREATE")
    hMC.SetDirectory(mymcfile)
    mymcfile.Write()
    mymcfile.Close()
    print "PU distribution for MC written to","PU_MC_"+name+".root"
    print "N.B. if you want to use the result root file, copy it to the data directory so that CRAB jobs find it\n"

def main():
    myinput = ""
    myoutput = ""
    mcdistribution = "unknown"
    distribution = []

    if len(sys.argv) == 1:
        usage()

    if "-h" in sys.argv:
        usage()
    if "--help" in sys.argv:
        usage()

    # Find mc distribution
    if "-mcdistribution" in sys.argv:
        i = 0
        for arg in sys.argv:
            i += 1
            if arg == "-mcdistribution":
                mcdistribution = sys.argv[i]
                if sys.argv[i] == "Fall11":
                    distribution = Fall11()
                elif sys.argv[i] == "Summer12_S7":
                    distribution = Summer12_S7()
                elif sys.argv[i] == "Summer12_S10":
                    distribution = Summer12_S10()
                else:
                    print "Unsupported mcdistribution (options: Fall11, Summer12_S7, Summer_S10)"
                    sys.exit()
                expandMC(mcdistribution, distribution)
    else:
        print "Missing parameter '-mcdistribution'!\n"
        usage()
    # Find input file
    if "-datainput" in sys.argv:
        i = 0
        for arg in sys.argv:
            i += 1
            if arg == "-datainput":
                myinput = sys.argv[i]
    # Find output file name
    if "-o" in sys.argv:
        i = 0
        for arg in sys.argv:
            i += 1
            if arg == "-o":
                myoutput = sys.argv[i]

    if myinput=="" or myoutput=="":
        print "skipping weight histogram calculation (supply the -datainput and -o parameters if you want to obtain the weight histogram)"
        sys.exit()

    # Parameters ok, open input file
    myfile = ROOT.TFile.Open(myinput, "r")
    if myfile.IsZombie():
        sys.exit()
    hinput = myfile.Get("pileup")
    if hinput == 0:
        sys.exit()
    # Check bin count
    if len(distribution) * 20 != hinput.GetNbinsX():
        print "Error: data distribution has", hinput.GetNbinsX(),"bins and MC distribution has",len(distribution),"bins!"
        print "Data distribution should have", len(distribution)*20, "bins"
        sys.exit()
    print "Reading PU information of data from", myinput
    # Clone result histogram
    houtput = hinput.Clone("PUweights")
    # Normalise to one
    houtput.Scale(1.0 / houtput.Integral())
    # Calculate weights (data / MC) bin by bin
    i = 0
    mylistindex = 0
    for j in range(1, hinput.GetNbinsX()+1):
        #print "data=", houtput.GetBinContent(j), "MC=", distribution[mylistindex] / 20.0
        # Note: the bin width is wider in MC, i.e. one has to divide the MC counts with the bin size difference
        houtput.SetBinContent(j, houtput.GetBinContent(j) / (distribution[mylistindex] / 20.0))
        i += 1
        # move to next MC bin index
        if (i == 20):
            i = 0
            mylistindex += 1
    # Open file for output
    myoutputfile = ROOT.TFile(myoutput,"RECREATE")
    if myoutputfile.IsZombie():
        sys.exit()
    houtput.SetDirectory(myoutputfile)
    myoutputfile.Write()
    myoutputfile.Close()
    print "PU weights written to", myoutput
    

if __name__ == "__main__":
    main()
