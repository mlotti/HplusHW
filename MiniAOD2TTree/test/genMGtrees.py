#!/usr/bin/env python

# Script for generating trees from MadGraph samples with default folder structure 
# Example usage: ./genMGtrees.py --pathtofirst $HOME/2HDMtypeII_GEN//heavy/PROCNLO_2HDMtypeII_0/Events/run_01_decayed_1/events.root 
#                --model 2HDMtypeII

import os
import sys
import glob
import random
from optparse import OptionParser

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

def main(opts):
    os.system("mkdir -p "+opts.model)

    cwd = os.getcwd()

    cfgPath = cwd+"/template_tree_cfg.py"

    path = opts.path
    for i in range(0,10):
        if i > 0:
            path = path.replace(opts.model+"_"+str(i-1), opts.model+"_"+str(i))
        os.system("sed -i 's:\"file\:.*\":\"file\:"+path+"\":g' "+cfgPath)
        os.system("cmsRun "+cfgPath)
        os.system("mv miniaod2tree.root "+opts.model+"/miniaod2tree_"+str(i)+".root")

    return 0

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: ")
    parser.add_option("--pathtofirst", "-m", dest="path", type="string", default=".", help="Path to gen-samples")
    parser.add_option("--model", dest="model", type="string", default="2HDMtypeII", help="Model")

    (opts, args) = parser.parse_args()

    sys.exit(main(opts))
