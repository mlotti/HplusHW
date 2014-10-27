#!/usr/bin/env python

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CombineTools as combine
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as commonLimitTools

lepType = False
lhcType = False
lhcTypeAsymptotic = False

#lepType = True
#lhcType = True
#lhcTypeAsymptotic = True

#massPoints = lands.allMassPoints
#massPoints = massPoints[1:]
#massPoints = ["80", "160"]

def main(opts, settings, myDir):
    postfix = "combination"

    furtherDatacards = ["datacard_mutau_taunu_m%s_mutau.txt"]
    furtherRootFiles = ["shapes_taunu_m%s_btagmultiplicity_j.root"]

    crabScheduler = "arc"
    crabOptions = {
#        "GRID": [
#            "ce_white_list = jade-cms.hip.fi",
#            "ce_white_list = korundi.grid.helsinki.fi",
#            ]
        }
    # Obtain mass mass points
    massPoints = settings.getMassPoints(commonLimitTools.LimitProcessType.TAUJETS)
    
    # run
    if settings.isLands():
        print "no guarantees than LandS works ... proceed at your own risk"
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
    elif settings.isCombine():
        if opts.lepType:
            raise Exception("LEP type Hybrid CLs not implemented yet for combine")
        elif opts.lhcType:
            raise Exception("LHC type Hybrid CLs not implemented yet for combine")
        elif opts.lhcTypeAsymptotic:
            combine.produceLHCAsymptotic(
                opts,
                myDir,
                massPoints = massPoints,
                datacardPatterns = [settings.getDatacardPattern(commonLimitTools.LimitProcessType.TAUJETS)]+furtherDatacards[:],
                rootfilePatterns = [settings.getRootfilePattern(commonLimitTools.LimitProcessType.TAUJETS)]+furtherRootFiles[:],
                clsType = combine.LHCTypeAsymptotic(opts),
                postfix = postfix+"_lhcasy"
                )
        else:
            return False
    return True

if __name__ == "__main__":
    parser = commonLimitTools.createOptionParser(lepType, lhcType, lhcTypeAsymptotic)
    opts = commonLimitTools.parseOptionParser(parser)
    # General settings

    myDirs = opts.dirs[:]
    if len(myDirs) == 0:
        myDirs.append(".")

    for myDir in myDirs:
        print "Considering directory:",myDir
        settings = commonLimitTools.GeneralSettings(myDir, opts.masspoints)
        print "The following masses are considered:",settings.getMassPoints(commonLimitTools.LimitProcessType.TAUJETS)
        if not main(opts, settings, myDir):
            print ""
            parser.print_help()
            print ""
            raise Exception("You forgot to specify limit calculation method as a command line parameter!")
    