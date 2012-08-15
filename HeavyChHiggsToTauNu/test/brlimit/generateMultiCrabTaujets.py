#!/usr/bin/env python

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
    #"default": (160, 150, 75),
    "default": (40, 150, 75),
    #"100":     (200, 120, 60),
    # for nominal
    #"150":     (40,  600, 300),
    #"160":     (40,  600, 300),
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
            opts,
            massPoints = massPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LEPType(toysPerJob=100),
            numberOfJobs = 10,
            postfix = postfix+"_lep_toys1k",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if opts.lhcType:
        lands.generateMultiCrab(
            opts,
            massPoints = massPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
            rootfilePatterns = [lands.taujetsRootfilePattern],
            clsType = lands.LHCType(toysCLsb=_ntoysCLsb(),
                                    toysCLb=_ntoysCLb(),
                                    vR={"default": None,
                                        # Initially obtained from asymp. limit as min/max of +-2 sigma and observed
                                        # After that, with trial and error of hybrid limit (e.g. by looking plot*.gif plots)
                                        "80":  ("0.001",  "0.08", "x1.05"), 
                                        "90":  ("0.001",  "0.08", "x1.05"), 
                                        "100": ("0.001", "0.08", "x1.05"), 
                                        "120": ("0.001", "0.04", "x1.05"), 
                                        "140": ("0.0005", "0.03", "x1.05"), 
                                        "150": ("0.0005", "0.03", "x1.05"),
                                        "155": ("0.0005", "0.02", "x1.05"),
                                        "160": ("0.0005", "0.02", "x1.05"), 
                                        }
                                    ),
            numberOfJobs = _njobs(),
            postfix = postfix+"_lhc_jobs160_sb150_b75",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if opts.lhcTypeAsymptotic:
        lands.produceLHCAsymptotic(
            opts,
            massPoints = massPoints,
            datacardPatterns = [lands.taujetsDatacardPattern],
            rootfilePatterns = [lands.taujetsRootfilePattern],
            postfix = postfix+"_lhcasy"
            )

if __name__ == "__main__":
    parser = lands.createOptionParser(lepType, lhcType, lhcTypeAsymptotic)
    opts = lands.parseOptionParser(parser)
    main(opts)
