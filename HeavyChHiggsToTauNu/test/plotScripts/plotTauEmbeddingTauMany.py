#!/usr/bin/env python

######################################################################
#
# This plot script is for comparing the embedded data to embedding MC
# within the tau ID. The corresponding python job
# configuration is embeddingAnalysis_cfg.py
#
# Author: Matti Kortelainen
#
######################################################################

import math, array, os

import ROOT
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.HeavyChHiggsToTauNu.tools.dataset as dataset
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.histograms as histograms
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.plots as plots
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.counter as counter
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.styles as styles
import HiggsAnalysis.HeavyChHiggsToTauNu.tools.crosssection as xsect
import plotTauEmbeddingSignalAnalysis as tauEmbedding
import plotTauEmbeddingTau as tauID
import produceTauEmbeddingResult as result

dirEmbs_120110 = [
    ".", # multicrab_analysis_v13_3_Run2011A_120110_150535
    "../multicrab_analysis_v13_3_seedTest1_Run2011A_120110_203953",
    "../multicrab_analysis_v13_3_seedTest2_Run2011A_120110_205101",
    "../multicrab_analysis_v13_3_seedTest3_Run2011A_120110_210157",
    "../multicrab_analysis_v13_3_seedTest4_Run2011A_120110_211348",
    "../multicrab_analysis_v13_3_seedTest5_Run2011A_120110_212548",
    "../multicrab_analysis_v13_3_seedTest6_Run2011A_120126_211602"
    "../multicrab_analysis_v13_3_seedTest7_Run2011A_120110_214901",
    "../multicrab_analysis_v13_3_seedTest8_Run2011A_120110_220005",
    "../multicrab_analysis_v13_3_seedTest9_Run2011A_120110_221143",
    ]

dirEmbs = dirEmbs_120110

def main():
    tauEmbedding.normalize = True
    tauEmbedding.era = "Run2011A"

#    datasetsEmb = result.DatasetsMany(dirEmbs, 


if __name__ == "__main__":
    main()
