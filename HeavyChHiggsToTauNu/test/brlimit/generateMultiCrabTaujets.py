#!/usr/bin/env python

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

def main():
    postfix = "taujets"
    lepType = False
    lhcType = False
    lhcTypeAsymptotic = False

#    lepType = True
    lhcType = True
#    lhcTypeAsymptotic = True

    crabScheduler = "arc"
    crabOptions = {
#        "GRID": [
#            "ce_white_list = jade-cms.hip.fi",
#            "ce_white_list = korundi.grid.helsinki.fi",
#            ]
        }

    if lepType:
        lands.generateMultiCrab(
            massPoints = lands.allMassPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LEPType(toysPerJob=100),
            numberOfJobs = 10,
            postfix = postfix+"_lep_toys1k",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if lhcType:
        lands.generateMultiCrab(
            massPoints = lands.allMassPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LHCType(toysCLsb=300, toysCLb=150,
                                    vR={"default": None,
                                        # obtained from asymp. limit as min/max of +-2 sigma and observed
                                        "160": ("0.007", "0.04"), 
                                        }
                                    ),
            numberOfJobs = 10,
            postfix = postfix+"_lhc_jobs10_sb300_b150",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if lhcTypeAsymptotic:
        lands.produceLHCAsymptotic(
            massPoints = lands.allMassPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
            rootfilePatterns = [lands.taujetsRootfilePattern],
            postfix = postfix+"_lhcasy"
            )

if __name__ == "__main__":
    main()
