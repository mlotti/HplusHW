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

#    generate(lands.mutauDatacardPattern, "mutau", "0.05")
#    generate(lands.etauDatacardPattern,  "etau",  "0.05")
    generate(lands.emuDatacardPattern,   "emu",   "0.3")

def generate(datacard, postfix, Rmax):
    if lepType:
        lands.generateMultiCrab(
            massPoints = lands.allMassPoints,
            datacardPatterns = [datacard],
            rootfilePatterns = [],
            clsType = lands.LEPType(toysPerJob=500, options=lands.lepHybridOptions.replace("0.09", Rmax)),
            numberOfJobs = 2,
            postfix = postfix+"_lep_toys1k",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if lhcType:
        lands.generateMultiCrab(
            massPoints = lands.allMassPoints,
            datacardPatterns = [datacard],
            rootfilePatterns = [],
            clsType = lands.LHCType(toysCLsb=300, toysCLb=150),
            numberOfJobs = 10,
            postfix = postfix+"_lhc_jobs10_sb300_b150",
            crabScheduler=crabScheduler, crabOptions=crabOptions)
    if lhcTypeAsymptotic:
        lands.produceLHCAsymptotic(
            massPoints = lands.allMassPoints,
            datacardPatterns = [datacard],
            rootfilePatterns = [],
            postfix = postfix+"_lhcasy"
            )
    

if __name__ == "__main__":
    main()
