#!/usr/bin/env python

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

def main():
    postfix = "taujets"
    lepType = False
#    lepType = True
    lhcType = False
    lhcType = True
    lhcTypeAsymptotic = False
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
            clsType = lands.LEPType(toysPerJob=50),
            numberOfJobs = 20,
            postfix = postfix+"_lep_toys1k",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if lhcType:
        lands.generateMultiCrab(
            massPoints = lands.allMassPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LHCType(toysCLsb=300, toysCLb=150),
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
