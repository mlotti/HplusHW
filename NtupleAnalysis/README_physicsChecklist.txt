Checklist for physics
=====================

Go through this checklist every time changes are made to the ttrees
(i.e. features added/removed, new POG recommendations used, new samples are used, etc.).

Purpose: make sure that the physics output is trustworthy and reduce the amount of
unnoticed bugs arising from the complexity of the analysis.

Table of contents:

1. Checklist BEFORE generating ttrees
2. Checklist AFTER generating ttrees and BEFORE doing any analysis


The full checklist follows:

1. Checklist BEFORE generating ttrees:
--------------------------------------

1.1. CMSSW version
1.1.1. Check that you have a valid CMSSW version for producing ttrees
... Are you able to run MC samples on the CMSSW version?
... Are you able to run data samples on the CMSSW version?
... Are the POG's recommendations supporting that CMSSW version?

1.2. Datasets
1.2.1. Check that all the relevant MC datasets are generated
... List of available samples: https://cmsweb.cern.ch/das/
... Files:
        MiniAOD2TTree/test/datasets.py 
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py

1.2.2. Check that all the relevant data datasets are generated
... List of available samples: https://cmsweb.cern.ch/das/
... Note that the different vX and vY dataset names are not necessarily overlapping!
    (i.e. generate all of them and see if their run numbers overlap or not; for
     physics only unique events should be used to avoid double-counting, but obviously
     one wants to maximize the statistics ...)
... Files:
        MiniAOD2TTree/test/datasets.py

1.2.3. Check that the luminosity mask is up-to-date
... The luminosity json's are available on lxplus at
        /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/
    Please use the "golden" json for physics ("silver" should only be used with utmost caution)
... Files:
        MiniAOD2TTree/test/datasets.py
        
1.3. Trigger
1.3.1. Check that the trigger names are ok
... The trigger bits are used for skimming and only the relevant trigger bits are stored to the ttrees.
... At the end of the day we use an or-function of the triggers (i.e. trg1_fired or trg2_fired or ...).
    This is done because:
    1) trigger names are different in MC and data.
    2) trigger names do change in different data eras (suffix v1, v2, v3, ... in trigger path name).
... Files:
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py
        MiniAOD2TTree/python/SignalAnalysisSkim_cfi.py
        MiniAOD2TTree/interface/TriggerDumper.h
        MiniAOD2TTree/src/TriggerDumper.cc

1.4. MET noise filters
1.4.1. Check that the latest recommendations are followed for the MET noise filters
... Recommendations are at: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
... If necessary, add/remove/edit MET noise filters.
... Files:
        MiniAOD2TTree/python/CommonFragments.py
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py
        MiniAOD2TTree/interface/METNoiseFilterDumper.h
        MiniAOD2TTree/src/METNoiseFilterDumper.cc
        
1.5. Taus
1.5.1. Check that the latest tau POG recommendations are followed for the taus
... Recommendations are at: https://twiki.cern.ch/twiki/bin/view/CMS/TauIDRecommendation13TeV
... If necessary, add/remove/edit discriminators or items.
... Be sure to generate the tau four vectors with the plus/minus variations of the tau energy scale
... Files:
        MiniAOD2TTree/python/CommonFragments.py
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py
        MiniAOD2TTree/interface/TauDumper.h
        MiniAOD2TTree/src/TauDumper.cc
        MiniAOD2TTree/plugins/SignalAnalysisSkim.cc

1.6. Electrons
1.6.1. Check that the latest electron POG recommendations are followed for the electrons
... Recommendations are at: https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2
... Further recommendations of potential relevance are at: https://twiki.cern.ch/twiki/bin/view/CMS/EGMSmearer
... Be suspicious that the above recommendations might not contain all of the recommendations.
    The level of documentation for electrons has been very poor for several years.
... If necessary, add/remove/edit discriminators or items.
... If necessary, update the common code fragments for producing the smeared/scale-corrected/electron ID corrections
... Note that there are different ID options for vetoing electrons or actually selecting electrons
... Note that there are instructions for cut-based and MVA electron ID. MVA is recommended.
... Note that there are different methods for pileup-mitigated relative isolation (at least delta beta and effective area).
... Files:
        MiniAOD2TTree/python/CommonFragments.py
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py
        MiniAOD2TTree/interface/ElectronDumper.h
        MiniAOD2TTree/src/ElectronDumper.cc
        MiniAOD2TTree/plugins/SignalAnalysisSkim.cc

1.7. Muons
1.7.1. Check that the latest muon POG recommendations are followed for the muons
... Recommendations are at:
        https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2
        https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonIsolationForRun2
        https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonReferenceEffsRun2
... If necessary, add/remove/edit discriminators or items.
... If necessary, update the common code fragments for producing the smeared/scale-corrected/muon ID corrections
... Note that there are different ID options for vetoing muons or actually selecting muons.
... Note that there are different methods for pileup-mitigated relative isolation (at least delta beta and effective area).
... Files:
        MiniAOD2TTree/python/CommonFragments.py
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py
        MiniAOD2TTree/interface/MuonDumper.h
        MiniAOD2TTree/src/MuonDumper.cc
        MiniAOD2TTree/plugins/SignalAnalysisSkim.cc

1.8. Jets
1.8.1. Check that the latest JME POG recommendations are followed for the jets
... Recommendations are at:
        https://twiki.cern.ch/twiki/bin/view/CMS/JetID
        https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetID
        https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
... If necessary, add/remove/edit discriminators or items.
... If necessary, update the common code fragments for producing the smeared/scale-corrected/jet ID corrections
... Note that there are different ID options for vetoing muons or actually selecting muons.
... Note that there are various jet collections (PFak04CHS, puppi jets, fat jets, ...)
... Note that even though usually CHS (charged hadron subtraction) is applied to the jets, it is recommended to
    apply also the jet pileup ID (i.e. a flag for rejecting a jet as pileup). Be sure to use the working point
    which is documented properly and preferably used in other analyses (in 2012 this was the loose working
    point, although in a fully hadronic final state it would be tempting to use the tight working point).
... Be sure to generate the jet four vectors with the plus/minus variations for the JEC and JER uncertainties
... Files:
        MiniAOD2TTree/python/CommonFragments.py
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py
        MiniAOD2TTree/interface/JetDumper.h
        MiniAOD2TTree/src/JetDumper.cc
        MiniAOD2TTree/plugins/SignalAnalysisSkim.cc

1.9. b tagging/mistagging
1.9.1. Check that the b tag discriminators of interest and recommended by the BTV POG are included
    to the jet collections
... Recommendations are at https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation  
... Files:
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py
        MiniAOD2TTree/interface/JetDumper.h
        MiniAOD2TTree/src/JetDumper.cc

1.10. MET
1.10.1. Check that the MET types and uncertainties recommended by the JME POG are included
... Recommendations are (at least) at:
        https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2016#ETmiss
        https://twiki.cern.ch/twiki/bin/view/CMS/MissingET
        https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETRun2Corrections
... Several requests have been made for a centrally available tool to obtain the MET variations
    for the unclustered MET energy scale (clustered part of variation should be done through
    the variation of JEC and JER)
... Make sure you understand if/how the selected tau is handled in terms of MET (recommend to
    do a residual correction by subtracting the tau four momentum from MET and adding the
    four momentum of the jet corresponding to the tau; this is done because the response of taus is
    practically 1, while for jets it is something else). Make sure all the necessary information
    to do this is stored to the ttree.
... Note that there are several interesting MET types (HLT uncorrected, type-I corrected, puppi MET, ...)
... Files:
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py
        MiniAOD2TTree/interface/METDumper.h
        MiniAOD2TTree/src/METDumper.cc

1.11. Top quark
1.11.1. Check that the top pt weighting recipy is still recommended by the TOP PAG
... The top pt weight and weight**2 values need to be calculated when doing the ttrees
    because one needs to know the number of all events when the top pt weight or weight**2 are applied.
    This is because the top pt weight is supposed to change only the shape, but not the overall
    normalization (analogous to vertex reweighting). The number of all events replacing is done
    in NtupleAnalysis/python/tools/dataset.py for any dataset accessing operation (plotting etc.).
... The recipy of top pt reweighting is described at:
        https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
... Files:
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py
        MiniAOD2TTree/plugins/HplusTopPtWeightProducer.cc
        MiniAOD2TTree/interface/EventInfoDumper.h
        MiniAOD2TTree/interface/EventInfoDumper.cc

1.11.2. Check that the items related ot top quark scale and pdf uncertainties are included
... Follow the recipy at:
        https://twiki.cern.ch/twiki/bin/view/CMS/TopSystematics

1.11.3. Check that the top tagger information is included

1.12. Vertex reweighting
1.12.1. Check that the vertex spectrum for vertex reweighting is correctly obtained for both
    MC (generated when producing the ttrees) and data (generated through brilcalc when calculating
    the luminosity for data).
... The number of all events with vertex reweighting needs to replace the unweighted number of all events,
    since the vertex reweighting should only change the shape, not overall normalization of the samples.
    In practice, this is done on the fly in NtupleAnalysis/python/main.py when running an analysis based
    on histograms created in ttree generation, lumicalc, and hplusMergeHistograms.py .
... Also the up and down variations for data should be obtained through brilcalc (for pileup uncertainty).    
... Files:
        MiniAOD2TTree/plugins/PUInfo.cc
        MiniAOD2TTree/scripts/hplusLumiCalc.py
        MiniAOD2TTree/scripts/hplusMergeHistograms.py
        NtupleAnalysis/python/main.py

1.13. Skim
1.13.1. Check that the skim conditions are reasonable and make sense physically
... A lot of disk space and hence analysis time can be saved if not all events need to be stored to ttrees
... Make sure that the number of all events is stored (for normalization).
... Make sure that the skim does not interfere with syst. uncertainty variations.
... Files:
        MiniAOD2TTree/plugins/SignalAnalysisSkim.cc
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py
   
1.14. Additional collections
1.14.1. Check if additional collections (GenMET, PFcandidates, ...) are needed
... If not needed, disc space can be saved
... Files:
        MiniAOD2TTree/test/miniAOD2TTree_SignalAnalysisSkim_cfg.py
        MiniAOD2TTree/plugins/MiniAOD2TTreeFilter.cc
   
1.15. Common code fragments
1.15.1. Check that the common code fragments, i.e. pieces of code which create new collections
    to the EDM dataformat, are available for all the different ttree producers
    (signal analysis, embedding, trigger efficiency, ...)
... For this purpose, such pieces of code should all be placed into CommonFragments.py and
    accessed from there
... Files:
        MiniAOD2TTree/python/CommonFragments.py
        MiniAOD2TTree/test/*_cfg.py

1.16. Synchronization issues
1.16.1. Check with other H+ analyses that the object definitions are synchronized to guarantee
    orthogonality between analyses targeting different final states
... The most relevant objects for this are the electron, muon, and tau object definitions
... The agreed definitions are listed at:
        https://twiki.cern.ch/twiki/bin/view/CMS/ChargedHiggsSearchesAt13TeV


2. Checklist AFTER generating ttrees and BEFORE doing any analysis:
-------------------------------------------------------------------

2.1. Luminosity
2.1.1. Check that the luminosity of the data datasets is reasonable 
... Run MiniAOD2TTree/scripts/hplusLumiCalc.py on lxplus in the multicrab directory (takes a few minutes)
... This creates also a couple of root files with histograms of pileup spectra inside the data dataset directories

2.2. Merging of datasets
2.2.1. Merge the crab job outputs
... Run MiniAOD2TTree/scripts/hplusMergeHistograms.py in the multicrab directory (takes tens of minutes)
... This adds also the pileup spectra histograms inside the merged root files; check that it is done properly

2.3. Dataformat
2.3.1. Generate the code for the dataformat 
... The code is autogenerated with
        NtupleAnalysis/scripts/hplusGenerateDataFormats.py path_to_a_flat_ntuple_root_file
... It creates the *Generated.h and *Generated.cc files to NtupleAnalysis/src/DataFormat/interface and src.
... Check that all the branches and getters are created; the tool 
        NtupleAnalysis/scripts/hplusPrintEventFormat.py path_to_a_flat_ntuple_root_file
    should alert if something is missing.
... Try to compile the code (go to NtupleAnalysis and make -j8 ). Fix the hplusGenerateDataFormats.py script
    if necessary and try again to generate the code and compile. Repeat until it compiles.

2.3.2. Run unit tests on the code to spot problems
... Go to NtupleAnalysis directory and make test -j8 .
... Fix any problems and rerun until all tests are passed.
    
2.4. Trigger scalefactors
2.4.1. tau leg scale factor
... These are created by Sami in json format. The json is stored under NtupleAnalysis/data/TriggerEfficiency directory.
... The tau leg SF is assumed to be as function of tau pt.
... Files:
    NtupleAnalysis/data/TriggerEfficiency/*.json
    NtupleAnalysis/python/parameters/scaleFactors.py

2.4.2. MET leg scale factor
... These are created by Sami in json format. The json is stored under NtupleAnalysis/data/TriggerEfficiency directory.
... The MET leg SF is assumed to be as function of MET.
... Files:
        NtupleAnalysis/data/TriggerEfficiency/*.json
        NtupleAnalysis/python/parameters/scaleFactors.py
    
2.5. btag SF
2.5.1. btag SF payload from POG
... Obtain the latest btag SF payload from BTV POG, see
         https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation
... Copy the btag SF payload csv file to NtupleAnalysis/data/ .
... Check that the dataformat of the csv file has not changed with assumptions in the code.
... Check that the python fragments in python/parameters are configured to read the correct csv file.
... Files:
        NtupleAnalysis/data/CSVv2.csv
        NtupleAnalysis/python/parameters/signalAnalysisParameters.py
        NtupleAnalysis/python/parameters/scaleFactors.py
        NtupleAnalysis/src/EventSelection/interface/BTagSFCalculator.h
        NtupleAnalysis/src/EventSelection/src/BTagSFCalculator.cc

2.5.2. btag efficiency
... Calculate the btag efficiency for the tau+jets topology using the BTagEfficiencyAnalysis code by following the instructions at
        NtupleAnalysis/src/BTagEfficiencyAnalysis/work/readme.txt
... Check that the json file makes sense and adjust the level of max. stat. uncert. if necessary.
... Copy the resulting json file to NtupleAnalysis/data/. .
... Check that the python fragments in python/parameters are configured to read the correct json file.
... Files:
        NtupleAnalysis/data/btageff_*.json
        NtupleAnalysis/python/parameters/signalAnalysisParameters.py
        NtupleAnalysis/python/parameters/scaleFactors.py
        NtupleAnalysis/src/EventSelection/interface/BTagSFCalculator.h
        NtupleAnalysis/src/EventSelection/src/BTagSFCalculator.cc

2.6. Benchmark plots
2.6.1. Compare standardized plots against older plots to spot problems
... Run the analyses with a predefined set of plots.
... Compare the plots against older plots of the same standard to spot problems. Fix if problems arise.
... Once problem-free, one is ready to take up the quest of running the full analysis and producing results.
... No script exist at this stage for this purpose.

TODO items:
- hplusWritePaper.py or hplusMakePhD.py do not yet work. Requires still manual work, yet rewards when completed :)
