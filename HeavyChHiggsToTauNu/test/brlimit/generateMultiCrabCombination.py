#!/usr/bin/env python

from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

lepType = False
lhcType = False
lhcTypeAsymptotic = False

#lepType = True
#lhcType = True
#lhcTypeAsymptotic = True

massPoints = lands.allMassPoints
massPoints = massPoints[1:]
massPoints = ["80", "160"]

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
            massPoints = massPoints,
            datacardPatterns = datacards,
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LEPType(toysPerJob=100),
            numberOfJobs = 10,
            postfix = postfix+"_lep_toys1k",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if opts.lhcType:
        lands.generateMultiCrab(
            massPoints = massPoints,
            datacardPatterns = datacards,
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LHCType(toysCLsb={"default": 100,
                                              "160": 100,
                                              },
                                    toysCLb={"default": 50,
                                             "160": 50
                                             },
                                    vR=("0.005", "0.06"),
                                    options = {"default": lands.lhcHybridOptions,
                                               "80": lands.lhcHybridOptionsMinos,
                                               "160": lands.lhcHybridOptionsMinos,
                                               },
                                    ),
            numberOfJobs = {"default": 120,
                            "160": 120
                            },
            postfix = postfix+"_lhc_jobs10_sb300_b150",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if opts.lhcTypeAsymptotic:
        lands.produceLHCAsymptotic(
            massPoints = massPoints,
            datacardPatterns = datacards,
            rootfilePatterns = [lands.taujetsRootfilePattern],
            postfix = postfix+"_lhcasy"
            )

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options]")
    parser.add_option("--lep", dest="lepType", default=lepType, action="store_true",
                      help="Use hybrid LEP-CLs (default %s)" % str(lepType))
    parser.add_option("--lhc", dest="lhcType", default=lepType, action="store_true",
                      help="Use hybrid LHC-CLs (default %s)" % str(lepType))
    parser.add_option("--lhcasy", dest="lhcTypeAsymptotic", default=lepType, action="store_true",
                      help="Use asymptotic LHC-CLs (default %s)" % str(lepType))

    (opts, args) = parser.parse_args()

    main(opts)
