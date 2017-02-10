README of the btag efficiency analysis
Authors: L. Wendland, S. Laurila

Purpose: Produce plot and json files which contain the btag efficiency for various partons.
         This information is needed for applying the btag SF for events (together with
         the btag/mistag probabilities obtained from BTV POG as a csv file).
         For formulae and more detailed description, see Analysis note 14-017 sections 6.5 and 10.5.
         See also: https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation

Instructions for using:
0) If necessary, alter the event selection which is determined before the btag efficiency
   is calculated. File: ../src/BTagEfficiencyAnalysis.cc

1) Run the btag efficiency analysis on the latest dataset to obtain the necessary histograms:
     ./btagEfficiencyAnalysis.py path_to_multicrab_dir

2) Produce plots and json files from the histograms, for example:
     ./plotBTagEfficiency.py --mcrab BTagEfficiencyAnalysis_160114_124705 --dataset T -e 0.10
   Notice that this is done for one dataset only (such as TT or TTJets or WJets). The last
   parameter is the maximum allowed uncertainty in a pt bin (the bin width is automatically
   widened to meet this requirement)

3) Once one is satisfied with the plots, the corresponding json file should be copied to the
   NtupleAnlysis/data directory:
     cp btageff*json ../../../data/.

4) Efficiency jsons for TT and WJets samples can be manually combined into one "hybrid" json, where
   the b-tag efficiencies (entries with "flavor": "B") are taken from the TT sample (the 
   largest    simulated background with true b jets in the final state), while mis-tag efficiencies
   (entries with "flavor": "C", "flavor": "G" or "flavor": "Light") are taken from the WJets
   sample. This file (btageff_hybrid.json) should be preferably used in the analysis.
