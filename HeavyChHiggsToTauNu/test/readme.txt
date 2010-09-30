7.7.2010/S.Lehti CMSSW_3_6_3    
    Tags needed:
	cvs co -r V03-28-04 DataFormats/JetReco
	cvs co -r V00-16-00 DataFormats/TauReco
	cvs co -r V00-23-00 RecoTauTag/RecoTau
	cvs co -r V00-21-00 RecoTauTag/Configuration
	cvs co HiggsAnalysis/Skimming
	rm HiggsAnalysis/Skimming/python/earlyDataInterestingEvents_cff.py

9.8.2010/M.Kortelainen CMSSW_3_7_0_patch_3
    Tags needed:
        cvs co HiggsAnalysis/Skimming
        rm HiggsAnalysis/Skimming/python/earlyDataInterestingEvents_cff.py

21.9.2010/S.Lehti CMSSW_3_8_4
    Tags needed:
	cvs co -r V08-00-26 PhysicsTools/PatAlgos
	cvs up -r 1.30 PhysicsTools/PatAlgos/python/tools/tauTools.py
	cvs co -r V00-24-00 RecoTauTag/Configuration
	cvs co -r V00-24-00 RecoTauTag/RecoTau
	cvs co -r V02-07-04 JetMETCorrections/TauJet

27.9.2010/M.Kortelainen CMSSW_3_8_4_patch2
    Tags needed:
        cvs co -r V08-00-26 PhysicsTools/PatAlgos
        cvs up -r 1.30 PhysicsTools/PatAlgos/python/tools/tauTools.py
        cvs co -r V00-24-00 RecoTauTag/Configuration
        cvs co -r V00-24-00 RecoTauTag/RecoTau
        cvs co -r V02-07-04 JetMETCorrections/TauJet
        cvs co -r lumi2010-Sep21b RecoLuminosity/LumiDB
        cvs co HiggsAnalysis/Skimming
        rm HiggsAnalysis/Skimming/python/earlyDataInterestingEvents_cff.py

29.9.2010/S.Lehti CMSSW_3_8_4_patch2 (discriminators moved under RecoTau)
    Tags needed:
        cvs co -r V08-00-26 PhysicsTools/PatAlgos
        cvs up -r 1.30 PhysicsTools/PatAlgos/python/tools/tauTools.py
        cvs co -r V00-24-00 RecoTauTag/Configuration
        cvs co -r V00-24-00 RecoTauTag/RecoTau
	cvs co RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByCharge.cc
	cvs co RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByDeltaE.cc
        cvs co RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByFlightPathSignificance.cc
        cvs co RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByInvMass.cc     
        cvs co RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByNProngs.cc
        cvs co RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByTauPolarization.cc
	cvs co RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByIsolation.cc
        cvs co RecoTauTag/RecoTau/plugins/PFRecoTauDiscriminationByDeltaE.cc
        cvs co RecoTauTag/RecoTau/plugins/PFRecoTauDiscriminationByFlightPathSignificance.cc
        cvs co RecoTauTag/RecoTau/plugins/PFRecoTauDiscriminationByInvMass.cc
        cvs co RecoTauTag/RecoTau/plugins/PFRecoTauDiscriminationByNProngs.cc
        cvs co RecoTauTag/RecoTau/plugins/PFRecoTauDiscriminationByTauPolarization.cc
        cvs co RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByCharge_cfi.py                       
        cvs co RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByDeltaE_cfi.py
        cvs co RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByFlightPathSignificance_cfi.py       
        cvs co RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByInvMass_cfi.py                      
        cvs co RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByNProngs_cfi.py                      
        cvs co RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByTauPolarization_cfi.py
        cvs co RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByDeltaE_cfi.py
        cvs co RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByFlightPathSignificance_cfi.py
        cvs co RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByInvMass_cfi.py
        cvs co RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByNProngs_cfi.py
        cvs co RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByTauPolarization_cfi.py
	cvs co RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByIsolation_cfi.py
	cvs up -r 1.2 RecoTauTag/RecoTau/plugins/BuildFile.xml
        cvs co -r lumi2010-Sep21b RecoLuminosity/LumiDB
        cvs co HiggsAnalysis/Skimming
        rm HiggsAnalysis/Skimming/python/earlyDataInterestingEvents_cff.py

Multicrab instructions
https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMultiCrab

Look also the instructions on our twiki
https://twiki.cern.ch/twiki/bin/view/CMS/HiggsChToTauNuFullyHadronic
