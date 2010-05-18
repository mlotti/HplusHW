10.10.2007/S.Lehti CMSSW_1_6_5	jet calibration data needed:
				cvs co -r jet_corrections_16X JetMETCorrections/MCJet/data

29.10.2007/S.Lehti CMSSW_1_6_7	Old SimpleTree version tagged with name "SimpleTree". 
				Contains the analysis, event filter, and storing 
				data using a simple root tree.

29.10.2007/S.Lehti CMSSW_1_6_7	Analysis changed to pTDR ORCA style using MyEvent 
				class for storing information in the root files. 
				In cvs head.

1.11.2007/S.Lehti  CMSSW_1_6_7	PFlow tags needed, co version V02-06-00, and compile.
				List of all cvs tags to be checked out:
				cvs co -r jet_corrections_16X JetMETCorrections/MCJet/data
				cvs co -r V02-06-00 DataFormats/ParticleFlowReco
				cvs co -r V02-06-00 DataFormats/ParticleFlowCandidate
				cvs co -r V02-06-00 RecoParticleFlow

5.11.2007/S.Lehti  CMSSW_1_6_7	Type1MET added in analysis, MET storing changed
				to contain rawMET and muon correction separately

8.11.2007/S.Lehti  CMSSW_1_6_7  Tau changed to use CaloTau and PFTau classes. Old code using
				IsolatedTauTagInfo tagged with name "IsolatedTauTagInfo". 
				New code in cvs head. 
				List of all cvs tags to be checked out:
                                cvs co -r V02-06-00 DataFormats/ParticleFlowReco
                                cvs co -r V02-06-00 DataFormats/ParticleFlowCandidate
                                cvs co -r V02-06-00 RecoParticleFlow
				cvs co -r V00-00-17 DataFormats/TauReco
				cvs co -r V00-00-37 RecoTauTag/RecoTau 
				cvs co -r V00-00-06 RecoTauTag/TauTagTools
				cvs co -r jet_corrections_16X JetMETCorrections/MCJet/data

22.11.2007/S.Lehti CMSSW_1_6_7  Added particleType in MyTrack class for storing
				PF ParticleType: X=0,h=1,e=2,mu=3,gamma=4,h0=5

10.1.2008/S.Lehti CMSSW_1_6_8   Dictionary created automatically by BuildFile

16.1.2008/S.Lehti CMSSW_1_6_8	Adding barcodes in MyMCParticle class

17.1.2008/S.Lehti CMSSW_1_6_8	New pf tags. List of all cvs tags to be checked out:
				cvs co -r global_1_6_8_14jan01 RecoParticleFlow
				cvs co -r global_1_6_8_14jan01 DataFormats/ParticleFlowReco
				cvs co -r global_1_6_8_14jan01 DataFormats/ParticleFlowCandidate
                                cvs co -r V00-00-17 DataFormats/TauReco
                                cvs co -r V00-00-37 RecoTauTag/RecoTau
                                cvs co -r V00-00-06 RecoTauTag/TauTagTools
                                cvs co -r jet_corrections_16X JetMETCorrections/MCJet/data

7.2.2008/S.Lehti CMSSW_1_6_9	Analysis program renamed and moved to a git 
                                repository, instructions: 
				http://cmsdoc.cern.ch/~slehti/HipProofAnalysis.html

12.2.2008/S.Lehti CMSSW_1_6_9	New pf tags.
				cvs co -r global_1_6_9_11feb08 RecoParticleFlow
				cvs co -r global_1_6_9_11feb08 DataFormats/ParticleFlowReco
				cvs co -r global_1_6_9_11feb08 DataFormats/ParticleFlowCandidate
                                cvs co -r V00-00-17 DataFormats/TauReco
                                cvs co -r V00-00-37 RecoTauTag/RecoTau
                                cvs co -r V00-00-06 RecoTauTag/TauTagTools
                                cvs co -r jet_corrections_16X JetMETCorrections/MCJet/data

18.2.2008/S.Lehti CMSSW_1_6_9	Lauri's changes to MyEvent class, adding 
				MySimTrack and MyHit classes 
29.2.2008/S.Lehti CMSSW_1_6_10	GenJets added in vector<MyMCParticles>,
                                pid=0,status=4
17.3.2008/S.Lehti CMSSW_1_6_10	Bugfix: PFTau::isolationPFCands() missing from PT tracks
27.3.2008/S.Lehti CMSSW_1_6_11  HCAL recHits depth() == 1 requirement removed, added HO and HF
15.4.2008/S.Lehti CMSSW_1_6_11  Added option for selecting iterativeTrack collection
15.4.2008/S.Lehti CMSSW_1_6_11  Added TauJet jet energy corrections
24.4.2008/S.Lehti CMSSW_1_6_11  Added metNoHF and a number of type1 corrections. New tags:
                                cvs co -r global_1_6_9_11feb08 RecoParticleFlow
                                cvs co -r global_1_6_9_11feb08 DataFormats/ParticleFlowReco
                                cvs co -r global_1_6_9_11feb08 DataFormats/ParticleFlowCandidate
                                cvs co -r V00-00-17 DataFormats/TauReco
                                cvs co -r V00-00-37 RecoTauTag/RecoTau
                                cvs co -r V00-00-06 RecoTauTag/TauTagTools
                                cvs co -r jet_corrections_16X JetMETCorrections/MCJet/data
				cvs co -r CMSSW_2_0_0 RecoMET
				cvs co -r CMSSW_2_0_0 DataFormats/METReco
				cvs co -r CMSSW_2_0_0 RecoJets/Configuration/data
				cvs co -r CMSSW_2_0_0 RecoJets/JetProducers/data
				Edit RecoJets/Configuration/data/GenJetParticles.cff and
				remove double quotes from line 'InputTag src = "genParticles"'
13.5.2008/S.Lehti CMSSW_1_6_11	Bugfix: myTrackConverter, loop over hits
20.5.2008/S.Lehti CMSSW_1_6_11  Dataformat changed, since root doesnt support 2 level of loops
                                in addition to event loop. Therefore the hits associated to tracks
                                are moved from MyTrack to MyJet, and a label associating a hit to
                                a given track is added in the MyHit data members.
17.6.2008/S.Lehti CMSSW_1_6_12	Removed jet raw Et cut 10 GeV. Added more btagging discriminators
24.6.2008/S.Lehti CMSSW_1_6_12  Added trigger bit information in MyEvent

26.2.2009/S.Lehti CMSSW_2_2_5   Track corrected MET needs additional tags. All needed tags:
				cvs co -r V02-05-00-20 RecoMET/METAlgorithms 
				cvs co -r V02-08-02-16 RecoMET/METProducers 
				cvs co -r V00-04-02-16 RecoMET/Configuration 
				cvs co -r V00-06-02-09 DataFormats/METReco
24.9.2009/S.Lehti CMSSW_3_1_3	pat lepton dataformat requires the usage of 313, 312 wont work.
				No tags needed.
15.1.2010/S.Lehti CMSSW_3_1_6	TCTau tag needed:
				cvs co JetMETCorrections/TauJet
				cvs co JetMETCorrections/Configuration/data
19.1.2010/S.Lehti CMSSW_3_4_2   TCTau tag needed:
                                cvs co JetMETCorrections/TauJet
25.2.2010/S.Lehti CMSSW_3_5_2   TCTau (and JPT) and pat tags needed:
				cvs co JetMETCorrections/TauJet
				cvs co -r V01-08-13-09 CondFormats/JetMETObjects
				cvs co -r V01-09-07-02 JetMETCorrections/Algorithms
				cvs co -r V01-08-32-06 JetMETCorrections/Configuration
				cvs co -r V03-03-06-09 JetMETCorrections/JetPlusTrack
				cvs co -r V02-10-00-01 JetMETCorrections/Modules
				cvs co -r V02-04-00    JetMETCorrections/Objects
				cvs co -r V07-11-20    PhysicsTools/PatAlgos
15.4.2010/S.Lehti CMSSW_3_5_6	Tags needed:
				cvs co -r V02-04-04    JetMETCorrections/TauJet
10.5.2010/S.Lehti CMSSW_3_5_8	Tags needed:
				cvs co -r V02-04-04    JetMETCorrections/TauJet
				git clone http://cmsdoc.cern.ch/~attikis/RecoTauTag.git
				addpkg RecoTauTag
17.5.2010/S.Lehti CMSSW_3_6_1	Tags needed:
				git clone http://cmsdoc.cern.ch/~attikis/RecoTauTag.git
				cvs co -r V03-28-04 DataFormats/JetReco
				cvs co -r V00-16-00 DataFormats/TauReco
				cvs co -r V00-23-00 RecoTauTag/RecoTau
				cvs co -r V00-21-00 RecoTauTag/Configuration
				cvs co -r V02-07-01 JetMETCorrections/TauJet


	How to compile:
	-compile
		cd HiggsAnalysis/MyEventNTPLMaker
		scramv1 b

	      * if you have taken any tags, then the compilation should be
                done in  CMSSW_1_6_X/src directory instead of 
                HiggsAnalysis/MyEventNTPLMaker, so that everything gets
                compiled

	-run
	Take jet calibration data for 1_5_X samples:
	cvs co -r jet_corrections_16X JetMETCorrections/MCJet/data

	Program for reading and analyzing the produced root files:
	in a git repository:
	http://cmsdoc.cern.ch/~slehti/HipProofAnalysis/HipProofAnalysis.html
	in CVS:
	HiggsAnalysis/MyEventNTPLMaker/data/HipProofAnalysis.tar.gz
