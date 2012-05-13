#!/usr/bin/env python

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

lepType = False
lhcType = False
lhcTypeAsymptotic = False

#lepType = True
#lhcType = True
lhcTypeAsymptotic = True

crabScheduler = "arc"
crabOptions = {
#        "GRID": [
#            "ce_white_list = jade-cms.hip.fi",
#            "ce_white_list = korundi.grid.helsinki.fi",
#            ]
    }

def main():
    postfix = "taujets"

    generate(lands.mutauDatacardPattern, "mutau", lepRmax="0.05", lhcAsyRmax="0.2")
    generate(lands.etauDatacardPattern,  "etau",  lepRmax="0.05", lhcAsyRmax="0.2")
#    generate(lands.emuDatacardPattern,   "emu",   lepRmax="0.3")

def generate(datacard, postfix, lepRmax=None, lhcRmax=None, lhcAsyRmax=None):
    if lepType:
        lands.generateMultiCrab(
            massPoints = lands.allMassPoints,
            datacardPatterns = [datacard],
            rootfilePatterns = [],
            clsType = lands.LEPType(toysPerJob=500, rMax=lepRmax),
            numberOfJobs = 2,
            postfix = postfix+"_lep_toys1k",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if lhcType:
        lands.generateMultiCrab(
            massPoints = lands.allMassPoints,
            datacardPatterns = [datacard],
            rootfilePatterns = [],
            clsType = lands.LHCType(toysCLsb=300, toysCLb=150, rMax=lhcRmax),
            numberOfJobs = 10,
            postfix = postfix+"_lhc_jobs10_sb300_b150",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if lhcTypeAsymptotic:
        lands.produceLHCAsymptotic(
            massPoints = lands.allMassPoints,
            datacardPatterns = [datacard],
            rootfilePatterns = [],
            clsType = lands.LHCTypeAsymptotic(rMax=lhcAsyRmax),
            postfix = postfix+"_lhcasy"
            )
    

if __name__ == "__main__":
    main()
