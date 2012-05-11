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

    landsOptions = "-M Hybrid  --initialRmin 0. --initialRmax 0.09"
    landsOptionsB = "-M Hybrid  --initialRmin 0. --initialRmax 0.15"

    crabScheduler = "arc"
    crabOptions = {
#        "GRID": [
#            "ce_white_list = jade-cms.hip.fi",
#            "ce_white_list = korundi.grid.helsinki.fi",
#            ]
        }
    

    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_a,  rootfilePatterns = rootfiles,
        landsOptions = landsOptions,
        toysPerJob = 50,
        numberOfJobs = 200,
        firstSeed = 1000,
        postfix = "combination_toys10k_orderA_seed1000",
        crabScheduler=crabScheduler, crabOptions=crabOptions)

    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_a,  rootfilePatterns = rootfiles,
        landsOptions = landsOptions,
        toysPerJob = 50,
        numberOfJobs = 200,
        firstSeed = 2000,
        postfix = "combination_toys10k_orderA_seed2000",
        crabScheduler=crabScheduler, crabOptions=crabOptions)


    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_b,  rootfilePatterns = rootfiles,
        landsOptions = landsOptions,
        toysPerJob = 50,
        numberOfJobs = 200,
        firstSeed = 1000,
        postfix = "combination_toys10k_orderB_seed1000",
        crabScheduler=crabScheduler, crabOptions=crabOptions)

    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_b,  rootfilePatterns = rootfiles,
        landsOptions = landsOptions,
        toysPerJob = 50,
        numberOfJobs = 200,
        firstSeed = 2000,
        postfix = "combination_toys10k_orderB_seed2000",
        crabScheduler=crabScheduler, crabOptions=crabOptions)


    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_a,  rootfilePatterns = rootfiles,
        landsOptions = landsOptionsB,
        toysPerJob = 50,
        numberOfJobs = 200,
        firstSeed = 1000,
        postfix = "combination_toys10k_orderA_seed1000_Rmax015",
        crabScheduler=crabScheduler, crabOptions=crabOptions)

    lands.generateMultiCrab(
        massPoints = massPoints, datacardPatterns = datacards_a,  rootfilePatterns = rootfiles,
        landsOptions = landsOptionsB,
        toysPerJob = 50,
        numberOfJobs = 200,
        firstSeed = 2000,
        postfix = "combination_toys10k_orderA_seed2000_Rmax015",
        crabScheduler=crabScheduler, crabOptions=crabOptions)



if __name__ == "__main__":
    main()
