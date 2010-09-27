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


Multicrab instructions
https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMultiCrab

# Multicrab doesn't seem to work well with multiple configuration files
cp multicrab_(pat|analysis).cfg multicrab.cfg 
  edit multicrab.cfg
multicrab -create
multicrab -submit
