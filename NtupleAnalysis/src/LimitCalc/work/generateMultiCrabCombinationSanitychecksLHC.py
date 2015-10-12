#!/usr/bin/env python

import HiggsAnalysis.LimitCalc.LandSTools as lands


def main(opts):
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
        opts,
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
        opts,
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
    parser = lands.createOptionParser(lepType, lhcType, lhcTypeAsymptotic)
    opts = lands.parseOptionParser(parser)
    main(opts)
