#!/usr/bin/env python

# Script for generating NLO (and LO) samples using MadGraph5_aMC@NLO (hardest processes), 
# MadSpin (NLO decays) and Pythia 8 (hadronization)

# author: E. Pekkarinen

# Steps of the script:
# 1. Run MadGraph5_aMC@NLO using the appropriate data card in the data card directory (datacardDirPath)
#    - Specify masses and number of events in the data card
#    - Location of MadGraph is specified by madgraphPath
# 2. Run MadSpin to simulate the NLO decays specified in the decay data card (madspinCardPath)  
# 3. Run hadronization for the generated events using Pythia 8 
#    - Location of Pythia is specified by pythiaPath
#    - Hadronizer configuration is determined by hadronizerCfgName

# run script as ./gensamples.py --model [MODEL NAME] --mass [MASS RANGE] --order [ORDER OF SIMULATION]
# e.g. ./genNLOsamples.py --model 2HDMtypeII --mass heavy --order NLO

# NOTE 1: Run cmsenv before this script

# NOTE 2: This script can be run on several terminals simultaneously to 
# obtain high statistics with parallelized computation. HOWEVER, wait until 
# a new data directory is created (approx. 30 seconds) after relaunching 
# the script

import os
import sys
import glob
import random
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

def main(opts):
    if opts.model not in ['2HDMdefault', '2HDMtypeII', 'MSSM']:
        raise Exception("No datacard available for model "+opts.model)
    if opts.mass not in ['light', 'heavy']:
        raise Exception("No datacard available for mass range "+opts.mass)
    if opts.order not in ['LO', 'NLO']:
        raise Exception("Simulation cannot be performed in the "+opts.model+" order")

    # default paths
    cwd = os.getcwd()
    taskPath = cwd+"/"+opts.model+"/"+opts.mass

     # paths and filenames (MODIFY)
    pythiaPath = "$HOME/Hadronizer/CMSSW_7_4_0_pre8/src/GeneratorInterface/LHEInterface/test/"
    hadronizerCfgName = "hadronizer_cfg.py"
    datacardDirPath = "$HOME/MG_datacards/"
    datacardPath = datacardDirPath+opts.model+"_"+opts.order+"_"+opts.mass+"Hp.dat"
    madgraphPath = "$HOME/programs/MG5_aMC_v2_2_3/"
    madgraphExePath = madgraphPath+"bin/mg5_aMC"
    madspinCardPath = madgraphPath+"Template/Common/Cards/madspin_card_default.dat"

    # make task directory
    os.system("mkdir -p "+opts.model)
    os.system("mkdir -p "+opts.model+"/"+opts.mass)
    
    # replace iseed with random integer (any integer will do, as long as they are different)
    os.system("sed -i 's/set iseed .*/set iseed "+str(random.randint(0,1000))+"/g' "+datacardPath)

    # replace default datacard of MadSpin with datacard specifying the decays of the investigated process
    os.system("cp "+datacardDirPath+"madspinDecays"+"_"+opts.mass+"Hp.dat "+madspinCardPath)

    # find correct event file
    fileList = os.listdir(taskPath)
    nFolders = 0
    for f in fileList:
        if os.path.isdir(taskPath+"/"+f):
            nFolders += 1

    orderstring = ""
    decaystring = ""
    if opts.order != "LO":
        orderstring += opts.order
        decaystring += "_decayed_1"

    eventsPath = taskPath+"/PROC"+orderstring+"_"+opts.model+"_"+str(nFolders)+"/Events/run_01"+decaystring+"/events.lhe"

    # run madgraph
    os.system("cd "+taskPath+" && "+madgraphExePath+" "+datacardPath)

    # uncompress event file
    os.system("gunzip "+eventsPath+".gz")
    
    # run hadronizer
    sedDefault = "filename = \"\""
    sedReplaced = "filename = \""+eventsPath.replace("/","\/")+"\""
    newHadronizerCfgName = hadronizerCfgName.replace("cfg", "cfg"+str(nFolders-1))
    os.system("cp "+pythiaPath+hadronizerCfgName+" "+pythiaPath+newHadronizerCfgName)
    os.system("sed -i 's:"+sedDefault+":"+sedReplaced+":g' "+pythiaPath+newHadronizerCfgName)
    os.system("cd "+pythiaPath+" && cmsRun "+newHadronizerCfgName)
    
    return 0

if __name__ == "__main__":
    # parse command line options
    parser = OptionParser(usage="Usage: ")
    parser.add_option("--test", dest="test", default=False, action="store_true", help="test")
    parser.add_option("--model", "-m", dest="model", type="string", default="MSSM", help="Model; available: '2HDMdefault', '2HDMtypeII', 'MSSM' (default: 'MSSM')")
    parser.add_option("--mass", dest="mass", type="string", default="light", help="Mass range; available: 'light', 'heavy', (default: 'light')")
    parser.add_option("--order", dest="order", type="string", default="LO", help="Perturbative order; available: 'LO', 'NLO', (default: 'LO')")

    (opts, args) = parser.parse_args()

    sys.exit(main(opts))
