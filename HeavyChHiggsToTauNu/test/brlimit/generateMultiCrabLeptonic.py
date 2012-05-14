#!/usr/bin/env python

from optparse import OptionParser

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

lepType = False
lhcType = False
lhcTypeAsymptotic = False

#lepType = True
lhcType = True
#lhcTypeAsymptotic = True

mutau = False
etau = False
emu = False

#mutau = True
#etau = True
#emu = True


crabScheduler = "arc"
crabOptions = {
#        "GRID": [
#            "ce_white_list = jade-cms.hip.fi",
#            "ce_white_list = korundi.grid.helsinki.fi",
#            ]
    }

massPoints = lands.allMassPoints
#massPoints = ["155", "160"]

def main(opts):
    postfix = "taujets"


    opts.mutau:
        generate(opts, lands.mutauDatacardPattern, "mutau",
                 lepRmax={"default": "0.05",
                          "160": "0.3",
                          },
                 lhcRmax="0.5",
                 lhcvR={"default": ("0.02", "0.12"),
                        "155": ("0.03", "0.4"),
                        "160": ("0.03", "0.5"),
                        },
                 lhcJobs = {"default": 5,
                            "160": 10
                            },
                 lhcAsyRmax="0.2")
    opts.etau:
        generate(opts, lands.etauDatacardPattern,  "etau",
                 lepRmax={"default": "0.05",
                          "160": "0.3"
                          },
                 lhcRmax="0.5",
                 lhcvR={"default": ("0.03", "0.15"),
                        "140": ("0.04", "0.18"),
                        "150": ("0.05", "0.21"),
                        "155": ("0.05", "0.5"),
                        "160": ("0.05", "0.6"),
                        },
                 lhcToysCLsb=600, lhcToysCLb=300, lhcPostfix="jobs10_sb_600_b300",
                 lhcJobs = {"default": 10,
                            "160": 20,
                            },
                 lhcAsyRmax="0.2")
    opts.emu:
        generate(opts, lands.emuDatacardPattern,   "emu",   lepRmax="0.3")

def generate(opts, datacard, postfix,
             lepRmax=None,
             lhcRmax=None, lhcvR=None, lhcToysCLsb=1200, lhcToysCLb=600, lhcJobs=5, lhcPostfix="jobs5_sb1200_b600",
             lhcAsyRmax=None):
    opts.lepType:
        lands.generateMultiCrab(
            massPoints = massPoints, datacardPatterns = [datacard], rootfilePatterns = [],
            clsType = lands.LEPType(toysPerJob=1000, rMax=lepRmax),
            numberOfJobs = 1,
            postfix = postfix+"_lep_toys1k",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    opts.lhcType:
        lands.generateMultiCrab(
            massPoints = massPoints, datacardPatterns = [datacard], rootfilePatterns = [],
            clsType = lands.LHCType(toysCLsb=lhcToysCLsb, toysCLb=lhcToysCLb, rMax=lhcRmax, vR=lhcvR),
            numberOfJobs = lhcJobs,
            postfix = postfix+"_lhc_"+lhcPostfix,
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    opts.lhcTypeAsymptotic:
        lands.produceLHCAsymptotic(
            massPoints = massPoints, datacardPatterns = [datacard], rootfilePatterns = [],
            clsType = lands.LHCTypeAsymptotic(rMax=lhcAsyRmax, vR=lhcvR),
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
    parser.add_option("--etau", dest="etau", default=etau, action="store_true",
                      help="Generate for e+tau final state (default %s)" % str(lepType))
    parser.add_option("--mutau", dest="mutau", default=mutau, action="store_true",
                      help="Generate for mu+tau final state (default %s)" % str(lepType))
    parser.add_option("--emu", dest="emu", default=emu, action="store_true",
                      help="Generate for e+mu final state (default %s)" % str(lepType))


    (opts, args) = parser.parse_args()

    main()
