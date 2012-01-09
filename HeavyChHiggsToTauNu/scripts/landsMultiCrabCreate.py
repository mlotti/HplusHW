#!/usr/bin/env python

from HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools import *

#LandS_tag           = "t3-04-13"
LandS_tag	    = "HEAD"
LandS_options       = "--PhysicsModel ChargedHiggs  -M Hybrid --bQuickEstimateInitialLimit 0 --initialRmin 0. --initialRmax 0.09"
LandS_nToysPerJob   = 50
number_of_jobs      = 10	# used only for making the expected limits, making the observed limits does not need splitting 
LandSDataCardNaming = "lands_datacard_hplushadronic_m"
LandSRootFileNaming = "lands_histograms_hplushadronic_m"


def main():

    lands = MultiCrabLandS()
    lands.CreateMultiCrabDir()
    lands.CopyLandsInputFiles()
    lands.writeLandsScripts()
    lands.writeCrabCfg()
    lands.writeMultiCrabCfg()
    lands.printInstruction()


if __name__ == "__main__":
    main()
