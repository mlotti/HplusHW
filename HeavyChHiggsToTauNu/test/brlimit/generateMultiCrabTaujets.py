#!/usr/bin/env python

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

lepType = True
lhcType = True
lhcTypeAsymptotic = True

lepType = False
lhcType = False
lhcTypeAsymptotic = False

def main(opts):
    postfix = "taujets"

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

    opts.lepType:
        lands.generateMultiCrab(
            massPoints = lands.allMassPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LEPType(toysPerJob=100),
            numberOfJobs = 10,
            postfix = postfix+"_lep_toys1k",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    opts.lhcType:
        lands.generateMultiCrab(
            massPoints = lands.allMassPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LHCType(toysCLsb={"default": 600, "140": 300},
                                    toysCLb={"default": 300, "140": 150},
                                    vR={"default": None,
                                        # Initially obtained from asymp. limit as min/max of +-2 sigma and observed
                                        # After that, with trial and error of hybrid limit (e.g. by looking plot*.gif plots)
                                        "80":  ("0.01",  "0.15"), 
                                        "100": ("0.005", "0.15"), 
                                        "120": ("0.005", "0.08"), 
                                        "140": ("0.005", "0.05"), 
                                        "155": ("0.005", "0.05"), 
                                        }
                                    ),
            #numberOfJobs = {"default": 5, "140": 10},
            #postfix = postfix+"_lhc_jobs5_sb600_b300",
            numberOfJobs = {"default": 40, "140": 80},
            #numberOfJobs = {"default": 80, "140": 160},
            postfix = postfix+"_lhc_jobs40_sb600_b300",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    opts.lhcTypeAsymptotic:
        lands.produceLHCAsymptotic(
            massPoints = lands.allMassPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
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
