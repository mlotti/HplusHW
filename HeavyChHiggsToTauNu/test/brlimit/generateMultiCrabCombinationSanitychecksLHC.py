#!/usr/bin/env python

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands


def main():
    postfix = "combination_lhc"

    datacards = [lands.taujetsDatacardPattern,
                 lands.emuDatacardPattern,
                 lands.etauDatacardPattern,
                 lands.mutauDatacardPattern,
                 ]

    crabScheduler = "arc"
    crabOptions = {
#        "GRID": [
#            "ce_white_list = jade-cms.hip.fi",
#            "ce_white_list = korundi.grid.helsinki.fi",
#            ]
        }

    massPoints = lands.allMassPoints

    lands.generateMultiCrab(
        massPoints = massPoints[1:-1],
        datacardPatterns = datacards,
        rootfilePatterns = [lands.taujetsRootfilePattern],
        clsType = lands.LHCType(toysCLsb=100,
                                toysCLb=50,
                                vR=("0.005", "0.06"),
                                ),
        numberOfJobs = 120,
        postfix = postfix+"_sanitycheck_migrad",
        crabScheduler=crabScheduler, crabOptions=crabOptions)

    lands.generateMultiCrab(
        massPoints = massPoints,
        datacardPatterns = datacards,
        rootfilePatterns = [lands.taujetsRootfilePattern],
        clsType = lands.LHCType(toysCLsb=100,
                                toysCLb=50,
                                vR=("0.005", "0.06"),
                                options = lands.lhcHybridOptionsMinos
                                ),
        numberOfJobs = 120,
        postfix = postfix+"_sanitycheck_minos",
        crabScheduler=crabScheduler, crabOptions=crabOptions)



if __name__ == "__main__":
    main()
