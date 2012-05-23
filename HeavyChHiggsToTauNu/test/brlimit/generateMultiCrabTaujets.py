#!/usr/bin/env python

from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

lepType = True
lhcType = True
lhcTypeAsymptotic = True

lepType = False
lhcType = False
lhcTypeAsymptotic = False

massPoints = lands.allMassPoints
#massPoints = ["150", "155", "160"]
#massPoints = ["155"]

ntoys = {
    # njobs, ntoysCLsb, ntoysCLb
    "default": (160, 150, 75),
    "100":     (200, 120, 60),
    # for nominal
    "150":     (40,  600, 300),
    "160":     (40,  600, 300),
}
def _ntoys(index):
    ret = {}
    for key, value in ntoys.iteritems():
        ret[key] = value[index]
    return ret
def _njobs():
    return _ntoys(0)
def _ntoysCLsb():
    return _ntoys(1)
def _ntoysCLb():
    return _ntoys(2)

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

    if opts.lepType:
        lands.generateMultiCrab(
            massPoints = massPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LEPType(toysPerJob=100),
            numberOfJobs = 10,
            postfix = postfix+"_lep_toys1k",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if opts.lhcType:
        lands.generateMultiCrab(
            massPoints = massPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LHCType(toysCLsb=_ntoysCLsb(),
                                    toysCLb=_ntoysCLb(),
                                    vR={"default": None,
                                        # Initially obtained from asymp. limit as min/max of +-2 sigma and observed
                                        # After that, with trial and error of hybrid limit (e.g. by looking plot*.gif plots)
                                        "80":  ("0.01",  "0.15"), 
                                        "100": ("0.005", "0.15"), 
                                        "120": ("0.005", "0.08"), 
                                        "140": ("0.005", "0.05"), 
                                        "155": ("0.005", "0.05"), 

                                        # For rebin40
#                                        "150": ("0.005", "0.05"), 
#                                        "160": ("0.004", "0.04"), 
                                        # For testing without JES
#                                        "150": ("0.005", "0.1"), 
#                                        "155": ("0.005", "0.1"), 
#                                        "160": ("0.004", "0.1"), 
                                        }
                                    ),
            numberOfJobs = _njobs(),
            postfix = postfix+"_lhc_jobs160_sb150_b75",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if opts.lhcTypeAsymptotic:
        lands.produceLHCAsymptotic(
            massPoints = massPoints,
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
