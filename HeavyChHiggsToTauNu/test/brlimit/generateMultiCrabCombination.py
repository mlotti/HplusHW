#!/usr/bin/env python

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

lepType = False
lhcType = False
lhcTypeAsymptotic = False

#lepType = True
#lhcType = True
#lhcTypeAsymptotic = True

massPoints = lands.allMassPoints
#massPoints = massPoints[1:]
#massPoints = ["80", "160"]

def main(opts):
    postfix = "combination"

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

    if opts.lepType:
        lands.generateMultiCrab(
            opts,
            massPoints = massPoints,
            datacardPatterns = datacards,
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LEPType(toysPerJob=100),
            numberOfJobs = 10,
            postfix = postfix+"_lep_toys1k",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if opts.lhcType:
        lands.generateMultiCrab(
            opts,
            massPoints = massPoints,
            datacardPatterns = datacards,
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LHCType(toysCLsb=100,
                                    toysCLb=50,
                                    vR=("0.005", "0.06"),
                                    options = {"default": lands.lhcHybridOptions,
                                               "80": lands.lhcHybridOptionsMinos,
                                               "160": lands.lhcHybridOptionsMinos,
                                               },
                                    ),
            numberOfJobs = 120,
            postfix = postfix+"_lhc_jobs120_sb100_b50",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if opts.lhcTypeAsymptotic:
        lands.produceLHCAsymptotic(
            opts,
            massPoints = massPoints,
            datacardPatterns = datacards,
            rootfilePatterns = [lands.taujetsRootfilePattern],
            postfix = postfix+"_lhcasy"
            )

if __name__ == "__main__":
    parser = lands.createOptionParser(lepType, lhcType, lhcTypeAsymptotic)
    opts = lands.parseOptionParser(parser)
    main(opts)
