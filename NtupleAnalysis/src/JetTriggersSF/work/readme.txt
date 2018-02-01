
To measure trigger effencies with singleMu reference trigger. First we need to create singleMu datasets for this purpose. 

To create datasets, we should use  "HiggsAnalysis/MiniAOD2TTree/test/miniAOD2TTree_JetTriggersSkim_cfg.py"

if running on FNAL LPC, do following (after setting up crab environment.)

>>> multicrab.py --create -s T3_US_FNALLPC -p miniAOD2TTree_JetTriggersSkim_cfg.py

For Data, we need SingleMuonData, 
For MC, we need ttbar, DiBososn, WJetsToLNu-HT binned, QCD_MuEnriched-pt binned.
This tree maker creates datasets with "HLT_IsoMu24_v" trigger skimming + electron veto presence of at-least one quality Mu. (pt>26, |eta|<2.4, muIDLoose)

Once Datasets are ready, We need to run JetTriggersSF analyser to create numerator and denomenator histograms for efficiency measurement. 

To do so, 
Go to HiggsAnalysis/NtupleAnalysis/src/JetTriggersSF/work/ and execute JetTriggersSF.cc using.

./runAnalysis.py -m  <multicrabDIR>

Once analyser is completed, the efficiency plots can be obtained using EffPlotter.py script as follows.

./EffPlotter.py -m JetTriggersSF_TIMEDATESTAMP.

The efficiency plots will be copied to HiggsAnalysis/NtupleAnalysis/src/JetTriggersSF/plots/
