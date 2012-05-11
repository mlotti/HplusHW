#!/usr/bin/env python

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.LandSTools as lands

def main():
    massPoints = ["160"]
    datacards_a = [
        lands.taujetsDatacardPattern,
        lands.emuDatacardPattern,
        lands.etauDatacardPattern,
        lands.mutauDatacardPattern,
        ]
    datacards_b = [datacards_a[i] for i in [3, 1, 0, 2]]
    rootfiles = [lands.taujetsRootfilePattern]

    njobs = 100
    clsA = lands.LEPType(toysPerJob=100, options="-M Hybrid --bQuickEstimateInitialLimit 0 --initialRmin 0. --initialRmax 0.015")
    clsAS = clsA.clone(firstSeed=2000)

    clsB = clsA.clone(options="-M Hybrid --bQuickEstimateInitialLimit 0 --initialRmin 0. --initialRmax 0.015")
    clsBS = clsB.clone(firstSeed=2000)

    crabScheduler = "arc"
    crabOptions = {
#        "GRID": [
#            "ce_white_list = jade-cms.hip.fi",
#            "ce_white_list = korundi.grid.helsinki.fi",
#            ]
        }
    

    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_a,  rootfilePatterns = rootfiles,
        clsType=clsA,
        numberOfJobs = njobs,
        postfix = "combination_toys10k_orderA_seed1000",
        crabScheduler=crabScheduler, crabOptions=crabOptions)

    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_a,  rootfilePatterns = rootfiles,
        clsType = clsAS,
        numberOfJobs = njobs,
        postfix = "combination_toys10k_orderA_seed2000",
        crabScheduler=crabScheduler, crabOptions=crabOptions)


    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_b,  rootfilePatterns = rootfiles,
        clsType = clsA,
        numberOfJobs = njobs,
        postfix = "combination_toys10k_orderB_seed1000",
        crabScheduler=crabScheduler, crabOptions=crabOptions)

    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_b,  rootfilePatterns = rootfiles,
        clsType = clsAS,
        numberOfJobs = njobs,
        postfix = "combination_toys10k_orderB_seed2000",
        crabScheduler=crabScheduler, crabOptions=crabOptions)


    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_a,  rootfilePatterns = rootfiles,
        clsType = clsB,
        numberOfJobs = njobs,
        postfix = "combination_toys10k_orderA_seed1000_Rmax015",
        crabScheduler=crabScheduler, crabOptions=crabOptions)

    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_a,  rootfilePatterns = rootfiles,
        clsType = clsBS,
        numberOfJobs = njobs,
        postfix = "combination_toys10k_orderA_seed2000_Rmax015",
        crabScheduler=crabScheduler, crabOptions=crabOptions)


if __name__ == "__main__":
    main()
