#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"

#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CommonTools/Utils/interface/TFileDirectory.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"


#include "TTree.h"

#include <limits>

namespace HPlus {
  SignalAnalysisTree::SignalAnalysisTree(const edm::ParameterSet& iConfig, const std::string& bDiscriminator):
    fBdiscriminator(bDiscriminator), 
    fDoFill(iConfig.getUntrackedParameter<bool>("fill")),
    fTauEmbeddingInput(iConfig.getUntrackedParameter<bool>("tauEmbeddingInput", false)),
    fFillJetEnergyFractions(iConfig.getUntrackedParameter<bool>("fillJetEnergyFractions", true)),
    fTree(0)
  {
    if(fTauEmbeddingInput) {
      fTauEmbeddingMuonSource = iConfig.getUntrackedParameter<edm::InputTag>("tauEmbeddingMuonSource");
      fTauEmbeddingMetSource = iConfig.getUntrackedParameter<edm::InputTag>("tauEmbeddingMetSource");
      fTauEmbeddingCaloMetSource = iConfig.getUntrackedParameter<edm::InputTag>("tauEmbeddingCaloMetSource");
    }

    std::vector<std::string> tauIds = iConfig.getUntrackedParameter<std::vector<std::string> >("tauIDs");
    fTauIds.reserve(tauIds.size());
    for(size_t i=0; i<tauIds.size(); ++i) {
      fTauIds.push_back(TauId(tauIds[i]));
    }
    fillNonIsoLeptonVars = false;
    reset();    
  }
  SignalAnalysisTree::~SignalAnalysisTree() {}

  void SignalAnalysisTree::init(TFileDirectory& dir) {
    if(!fDoFill)
      return;

    fTree = dir.make<TTree>("tree", "Tree");

    fTree->Branch("event", &fEvent);
    fTree->Branch("lumi", &fLumi);
    fTree->Branch("run", &fRun);

    fTree->Branch("weightPrescale", &fPrescaleWeight);
    fTree->Branch("weightPileup", &fPileupWeight);
    fTree->Branch("weightTrigger", &fTriggerWeight);
    fTree->Branch("weightBTagging", &fBTaggingWeight);
    fTree->Branch("weightAtFill", &fFillWeight);

    fTree->Branch("goodPrimaryVertices_n", &fNVertices);

    fTree->Branch("hltTau_p4", &fHltTaus);

    fTree->Branch("tau_p4", &fTau);
    fTree->Branch("tau_leadPFChargedHadrCand_p4", &fTauLeadingChCand);
    fTree->Branch("tau_signalPFChargedHadrCands_n", &fTauSignalChCands);
    fTree->Branch("tau_emFraction", &fTauEmFraction);
    for(size_t i=0; i<fTauIds.size(); ++i) {
      fTree->Branch( ("tau_id_"+fTauIds[i].name).c_str(), &(fTauIds[i].value) );
    }
      
    fTree->Branch("jets_p4", &fJets);
    fTree->Branch("jets_btag", &fJetsBtags);
    if(fFillJetEnergyFractions) {
      fTree->Branch("jets_chf", &fJetsChf); // charged hadron
      fTree->Branch("jets_nhf", &fJetsNhf); // neutral hadron
      fTree->Branch("jets_elf", &fJetsElf);  // electron
      fTree->Branch("jets_phf", &fJetsPhf);  // photon
      fTree->Branch("jets_muf", &fJetsMuf);   // muon
    }
    fTree->Branch("jets_chm", &fJetsChm);
    fTree->Branch("jets_nhm", &fJetsNhm);
    fTree->Branch("jets_elm", &fJetsElm);
    fTree->Branch("jets_phm", &fJetsPhm);
    fTree->Branch("jets_mum", &fJetsMum);
    fTree->Branch("jets_jecToRaw", &fJetsJec);
    fTree->Branch("jets_area", &fJetsArea);
    fTree->Branch("jets_looseId", &fJetsLooseId);
    fTree->Branch("jets_tightId", &fJetsTightId);

    fTree->Branch("met_p4", &fRawMet);
    fTree->Branch("met_sumet", &fRawMetSumEt);
    fTree->Branch("met_significance", &fRawMetSignificance);

    fTree->Branch("metType1_p4", &fType1Met);
    fTree->Branch("metType2_p4", &fType2Met);
    fTree->Branch("caloMet_p4", &fCaloMet);
    fTree->Branch("tcMet_p4", &fTcMet);

    fTree->Branch("topreco_p4", &fTop);

    fTree->Branch("alphaT", &fAlphaT);

    fTree->Branch("deltaPhi", &fDeltaPhi);
    fTree->Branch("passedBTagging", &fPassedBTagging);

    fTree->Branch("genMet_p4", &fGenMet);

    if(fTauEmbeddingInput) {
      fTree->Branch("temuon_p4", &fTauEmbeddingMuon);
      fTree->Branch("temet_p4", &fTauEmbeddingMet);
      fTree->Branch("tecalomet_p4", &fTauEmbeddingCaloMet);
    }

    if(fillNonIsoLeptonVars){
      // nonIsoMuons
      fTree->Branch("nonIsoMuons_p4", &fNonIsoMuons);
      fTree->Branch("nonIsoMuons_IsGlobalMuon", &fNonIsoMuons_IsGlobalMuon);
      fTree->Branch("nonIsoMuons_IsTrackerMuon", &fNonIsoMuons_IsTrackerMuon);
      fTree->Branch("nonIsoMuons_ID_AllMuons", &fNonIsoMuons_AllMuons);
      fTree->Branch("nonIsoMuons_ID_AllGlobalMuons", & fNonIsoMuons_AllGlobalMuons);
      fTree->Branch("nonIsoMuons_ID_AllStandAloneMuons", & fNonIsoMuons_AllStandAloneMuons);
      fTree->Branch("nonIsoMuons_ID_AllTrackerMuons", & fNonIsoMuons_AllTrackerMuons);
      fTree->Branch("nonIsoMuons_ID_TrackerMuonArbitrated", & fNonIsoMuons_TrackerMuonArbitrated);
      fTree->Branch("nonIsoMuons_ID_AllArbitrated", & fNonIsoMuons_AllArbitrated);
      fTree->Branch("nonIsoMuons_ID_GlobalMuonPromptTight", & fNonIsoMuons_GlobalMuonPromptTight);
      fTree->Branch("nonIsoMuons_ID_TMLastStationLoose", & fNonIsoMuons_TMLastStationLoose);
      fTree->Branch("nonIsoMuons_ID_TMLastStationTight", & fNonIsoMuons_TMLastStationTight);
      fTree->Branch("nonIsoMuons_ID_TMOneStationLoose", & fNonIsoMuons_TMOneStationLoose);
      fTree->Branch("nonIsoMuons_ID_TMLastStationOptimizedLowPtLoose", & fNonIsoMuons_TMLastStationOptimizedLowPtLoose);
      fTree->Branch("nonIsoMuons_ID_TMLastStationOptimizedLowPtTight", & fNonIsoMuons_TMLastStationOptimizedLowPtTight);
      fTree->Branch("nonIsoMuons_ID_GMTkChiCompatibility", & fNonIsoMuons_GMTkChiCompatibility);
      fTree->Branch("nonIsoMuons_ID_GMTkKinkTight", & fNonIsoMuons_GMTkKinkTight);
      fTree->Branch("nonIsoMuons_ID_TMLastStationAngLoose", & fNonIsoMuons_TMLastStationAngLoose);
      fTree->Branch("nonIsoMuons_ID_TMLastStationAngTight", & fNonIsoMuons_TMLastStationAngTight);
      fTree->Branch("nonIsoMuons_ID_TMLastStationOptimizedBarrelLowPtLoose", & fNonIsoMuons_TMLastStationOptimizedBarrelLowPtLoose);
      fTree->Branch("nonIsoMuons_ID_TMLastStationOptimizedBarrelLowPtTight", & fNonIsoMuons_TMLastStationOptimizedBarrelLowPtTight);
      fTree->Branch("nonIsoMuons_InnerTrackNTrkHits", & fNonIsoMuons_InnerTrackNTrkHits);
      fTree->Branch("nonIsoMuons_InnerTrackNPixelHits", & fNonIsoMuons_InnerTrackNPixelHits);
      fTree->Branch("nonIsoMuons_GlobalTrackNMuonHits", & fNonIsoMuons_GlobalTrackNMuonHits);
      fTree->Branch("nonIsoMuons_NormChiSquare", & fNonIsoMuons_NormChiSquare);
      fTree->Branch("nonIsoMuons_IPTwrtBeamLine", & fNonIsoMuons_IPTwrtBeamLine); 
      fTree->Branch("nonIsoMuons_IPZwrtPV", & fNonIsoMuons_IPZwrtPV);
      fTree->Branch("nonIsoMuons_TrackIso", & fNonIsoMuons_TrackIso);
      fTree->Branch("nonIsoMuons_EcalIso", & fNonIsoMuons_EcalIso);
      fTree->Branch("nonIsoMuons_HcalIso", & fNonIsoMuons_HcalIso);
      fTree->Branch("nonIsoMuons_RelIso", & fNonIsoMuons_RelIso);
      // nonIsoElectrons
      fTree->Branch("nonIsoElectrons_p4", & fNonIsoElectrons);
      fTree->Branch("nonIsoElectrons_GsfTrkRefIsNull", & fNonIsoElectrons_GsfTrkRefIsNull);
      fTree->Branch("nonIsoElectrons_SuperClusterRefIsNull" , & fNonIsoElectrons_SuperClusterRefIsNull);
      fTree->Branch("nonIsoElectrons_SuperClusterRefEta" , & fNonIsoElectrons_SuperClusterRefEta);
      fTree->Branch("nonIsoElectrons_SuperClusterRefPhi" , & fNonIsoElectrons_SuperClusterRefPhi);
      fTree->Branch("nonIsoElectrons_SimpleId_Loose" , & fNonIsoElectrons_SimpleId_Loose);
      fTree->Branch("nonIsoElectrons_SimpleId_RobustLoose" , & fNonIsoElectrons_SimpleId_RobustLoose);
      fTree->Branch("nonIsoElectrons_SimpleId_Tight" , & fNonIsoElectrons_SimpleId_Tight);
      fTree->Branch("nonIsoElectrons_SimpleId_RobustTight" , & fNonIsoElectrons_SimpleId_RobustTight);
      fTree->Branch("nonIsoElectrons_SimpleId_RobustHighEnergy" , & fNonIsoElectrons_SimpleId_RobustHighEnergy);
      fTree->Branch("nonIsoElectrons_EleId95relIso" , & fNonIsoElectrons_ID_EleId95relIso);
      fTree->Branch("nonIsoElectrons_EleId90relIso" , & fNonIsoElectrons_ID_EleId90relIso);
      fTree->Branch("nonIsoElectrons_EleId85relIso" , & fNonIsoElectrons_ID_EleId85relIso); 
      fTree->Branch("nonIsoElectrons_EleId80relIso" , & fNonIsoElectrons_ID_EleId80relIso);
      fTree->Branch("nonIsoElectrons_EleId70relIso" , & fNonIsoElectrons_ID_EleId70relIso);
      fTree->Branch("nonIsoElectrons_EleId60relIso" , & fNonIsoElectrons_ID_EleId60relIso);
      fTree->Branch("nonIsoElectrons_TrackIso" , & fNonIsoElectrons_TrackIso);
      fTree->Branch("nonIsoElectrons_EcalIso" , & fNonIsoElectrons_EcalIso);
      fTree->Branch("nonIsoElectrons_HcalIso" , & fNonIsoElectrons_HcalIso);
      fTree->Branch("nonIsoElectrons_NLostHitsInTrker" , & fNonIsoElectrons_NLostHitsInTrker);
      fTree->Branch("nonIsoElectrons_RelIso" , & fNonIsoElectrons_RelIso);
      fTree->Branch("nonIsoElectrons_DeltaCotTheta" , & fNonIsoElectrons_DeltaCotTheta);
      fTree->Branch("nonIsoElectrons_DistanceOSTrk" , & fNonIsoElectrons_DistanceOSTrk);
      fTree->Branch("nonIsoElectrons_IPwrtBeamSpot" , & fNonIsoElectrons_IPwrtBeamSpot);
      fTree->Branch("nonIsoElectrons_ElectronMuonDeltaR" , & fNonIsoElectrons_ElectronMuonDeltaR);
    }
  
  }


  void SignalAnalysisTree::setHltTaus(const pat::TriggerObjectRefVector& hltTaus) {
    fHltTaus.clear();
    fHltTaus.reserve(hltTaus.size());
    for(size_t i=0; i<hltTaus.size(); ++i) {
      fHltTaus.push_back(hltTaus[i]->p4());
    }
  }
 
  void SignalAnalysisTree::fill(const edm::Event& iEvent, const edm::PtrVector<pat::Tau>& taus,
                                const edm::PtrVector<pat::Jet>& jets) {
    if(!fDoFill)
      return;

    if(taus.size() != 1)
      throw cms::Exception("LogicError") << "Expected tau collection size to be 1, was " << taus.size() << " at " << __FILE__ << ":" << __LINE__ << std::endl;

    fEvent = iEvent.id().event();
    fLumi = iEvent.id().luminosityBlock();
    fRun = iEvent.id().run();

    fTau = taus[0]->p4();
    fTauLeadingChCand = taus[0]->leadPFChargedHadrCand()->p4();
    fTauSignalChCands = taus[0]->signalPFChargedHadrCands().size();
    fTauEmFraction = taus[0]->emFraction();
    for(size_t i=0; i<fTauIds.size(); ++i) {
      fTauIds[i].value = taus[0]->tauID(fTauIds[i].name) > 0.5;
    }

    for(size_t i=0; i<jets.size(); ++i) {
      fJets.push_back(jets[i]->p4());
      fJetsBtags.push_back(jets[i]->bDiscriminator(fBdiscriminator));

      double eta = jets[i]->eta();

      double chf = jets[i]->chargedHadronEnergyFraction();
      double nhf = jets[i]->neutralHadronEnergyFraction();
      double elf = jets[i]->chargedEmEnergyFraction();
      double phf = jets[i]->neutralEmEnergyFraction();
      // for some reason the muonEnergyFraction is calculated w.r.t. *corrected* energy in pat::Jet
      double muf = jets[i]->muonEnergy() / (jets[i]->jecFactor(0) * jets[i]->energy());

      if(fFillJetEnergyFractions) {
        double sum = chf+nhf+elf+phf+muf;
        if(std::abs(sum - 1.0) > 0.000001) {
          throw cms::Exception("Assert") << "The assumption that chf+nhf+elf+phf+muf=1 failed, the sum was " << (chf+nhf+elf+phf+muf) 
                                         << " the sum-1 was " << (sum-1.0)
                                         << std::endl;
        }
        fJetsChf.push_back(chf);
        fJetsNhf.push_back(nhf);
        fJetsElf.push_back(elf);
        fJetsPhf.push_back(phf);
        fJetsMuf.push_back(muf);
      }

      int chm = jets[i]->chargedHadronMultiplicity();
      fJetsChm.push_back(chm);
      fJetsNhm.push_back(jets[i]->neutralHadronMultiplicity());
      fJetsElm.push_back(jets[i]->electronMultiplicity());
      fJetsPhm.push_back(jets[i]->photonMultiplicity());
      fJetsMum.push_back(jets[i]->muonMultiplicity());

      fJetsJec.push_back(jets[i]->jecFactor(0));

      int npr = jets[i]->chargedMultiplicity() + jets[i]->neutralMultiplicity();

      fJetsLooseId.push_back( npr > 1 && phf < 0.99 && nhf < 0.99 && ((std::abs(eta) <= 2.4 && elf < 0.99 && chf > 0 && chm > 0) ||
                                                                      std::abs(eta) > 2.4) );
      fJetsTightId.push_back( npr > 1 && phf < 0.99 && nhf < 0.99 && ((std::abs(eta) <= 2.4 && nhf < 0.9 && phf < 0.9 && elf < 0.99 && chf > 0 && chm > 0) ||
                                                                      std::abs(eta) > 2.4) );

      fJetsArea.push_back(jets[i]->jetArea());
    }

    if(fTauEmbeddingInput) {
      edm::Handle<edm::View<pat::Muon> > hmuon;
      iEvent.getByLabel(fTauEmbeddingMuonSource, hmuon);
      if(hmuon->size() != 1)
        throw cms::Exception("Assert") << "The assumption that tau embedding muon collection size is 1 failed, the size was " << hmuon->size() << std::endl;

      edm::Handle<edm::View<reco::MET> > hmet;
      iEvent.getByLabel(fTauEmbeddingMetSource, hmet);
      if(hmet->size() != 1)
        throw cms::Exception("Assert") << "The assumption that tau embedding met collection size is 1 failed, the size was " << hmet->size() << std::endl;

      edm::Handle<edm::View<reco::MET> > hcalomet;
      iEvent.getByLabel(fTauEmbeddingCaloMetSource, hcalomet);
      if(hcalomet->size() != 1)
        throw cms::Exception("Assert") << "The assumption that tau embedding calomet collection size is 1 failed, the size was " << hcalomet->size() << std::endl;

      fTauEmbeddingMuon = hmuon->at(0).p4();
      fTauEmbeddingMet = hmet->at(0).p4();
      fTauEmbeddingCaloMet = hcalomet->at(0).p4();
    }

    fTree->Fill();
    reset();
  }


  void SignalAnalysisTree::setNonIsoLeptons(edm::PtrVector<pat::Muon> nonIsoMuons, edm::PtrVector<pat::Electron> nonIsoElectrons) {
    if(!fDoFill)
      return;

    if(nonIsoMuons.size() >= 1){
      // throw cms::Exception("LogicError") << "Expected nonIsoMuon collection size to be >=1, but  was " << nonIsoMuons.size() << " instead at " << __FILE__ << ":" << __LINE__ << std::endl;
      // loop over all muons
      for(edm::PtrVector<pat::Muon>::const_iterator iMuon = nonIsoMuons.begin(); iMuon != nonIsoMuons.end(); ++iMuon) {
	
	// Obtain reference to a Muon track
	reco::TrackRef myGlobalTrackRef = (*iMuon)->globalTrack();
	reco::TrackRef myInnerTrackRef = (*iMuon)->innerTrack(); // inner tracks give best resolution for muons with Pt up to 200 GeV/c
      
	// Check that track was found.
	if ( myInnerTrackRef.isNull() || myGlobalTrackRef.isNull() ) continue; 

	// 1) Store the 4-momenta of muons
	fNonIsoMuons.push_back( (*iMuon)->p4() );

	// 2) Determine whether muon is a "GlobalMuon" and/or a "TrackerMuon"
	if( (*iMuon)->isGlobalMuon() ) fNonIsoMuons_IsGlobalMuon.push_back(true);
	else fNonIsoMuons_IsGlobalMuon.push_back(false);

	if( (*iMuon)->isTrackerMuon() ) fNonIsoMuons_IsTrackerMuon.push_back(true);
	else fNonIsoMuons_IsTrackerMuon.push_back(false);

	// 3) Store Muon Identification modes
	if( (*iMuon)->muonID("All") ) fNonIsoMuons_AllMuons.push_back(true);
	else fNonIsoMuons_AllMuons.push_back(false);
	//
	if( (*iMuon)->muonID("AllGlobalMuons") ) fNonIsoMuons_AllGlobalMuons.push_back(true);
	else fNonIsoMuons_AllGlobalMuons.push_back(false);
	//
	if( (*iMuon)->muonID("AllStandAloneMuons") )  fNonIsoMuons_AllStandAloneMuons.push_back(true);
	else fNonIsoMuons_AllStandAloneMuons.push_back(false);
	//
	if( (*iMuon)->muonID("AllTrackerMuons") )  fNonIsoMuons_AllTrackerMuons.push_back(true);
	else  fNonIsoMuons_AllTrackerMuons.push_back(false);
	//
	if( (*iMuon)->muonID("TrackerMuonArbitrated") ) fNonIsoMuons_TrackerMuonArbitrated.push_back(true);
	else  fNonIsoMuons_TrackerMuonArbitrated.push_back(false);
	//
	if( (*iMuon)->muonID("AllArbitrated") )  fNonIsoMuons_AllArbitrated.push_back(true);
	else  fNonIsoMuons_AllArbitrated.push_back(false);
	//
	if( (*iMuon)->muonID("GlobalMuonPromptTight")  ) fNonIsoMuons_GlobalMuonPromptTight.push_back(true);
	else fNonIsoMuons_GlobalMuonPromptTight.push_back(false);
	// 
	if( (*iMuon)->muonID("TMLastStationLoose") ) fNonIsoMuons_TMLastStationLoose.push_back(true);
	else fNonIsoMuons_TMLastStationLoose.push_back(false);
	// 
	if( (*iMuon)->muonID("TMLastStationTight") ) fNonIsoMuons_TMLastStationTight.push_back(true);
	else fNonIsoMuons_TMLastStationTight.push_back(false);
	// 
	if( (*iMuon)->muonID("TMOneStationLoose") ) fNonIsoMuons_TMOneStationLoose.push_back(true);
	else fNonIsoMuons_TMOneStationLoose.push_back(false);
	//
	if( (*iMuon)->muonID("TMLastStationOptimizedLowPtLoose") ) fNonIsoMuons_TMLastStationOptimizedLowPtLoose.push_back(true);
	else fNonIsoMuons_TMLastStationOptimizedLowPtLoose.push_back(false);
	//
	if( (*iMuon)->muonID("TMLastStationOptimizedLowPtTight") ) fNonIsoMuons_TMLastStationOptimizedLowPtTight.push_back(true);
	fNonIsoMuons_TMLastStationOptimizedLowPtTight.push_back(false);
	//
	if( (*iMuon)->muonID("GMTkChiCompatibility") ) fNonIsoMuons_GMTkChiCompatibility.push_back(true);
	else fNonIsoMuons_GMTkChiCompatibility.push_back(false);
	//
	if( (*iMuon)->muonID("GMTkKinkTight") )  fNonIsoMuons_GMTkKinkTight.push_back(true);
	else  fNonIsoMuons_GMTkKinkTight.push_back(false);
	//
	if( (*iMuon)->muonID("TMLastStationAngLoose") )   fNonIsoMuons_TMLastStationAngLoose.push_back(true);
	else fNonIsoMuons_TMLastStationAngLoose.push_back(false);
	//
	if( (*iMuon)->muonID("TMLastStationAngTight") ) fNonIsoMuons_TMLastStationAngTight.push_back(true);
	else fNonIsoMuons_TMLastStationAngTight.push_back(false);
	//
	if( (*iMuon)->muonID("TMLastStationOptimizedBarrelLowPtLoose") ) fNonIsoMuons_TMLastStationOptimizedBarrelLowPtLoose.push_back(true);
	else  fNonIsoMuons_TMLastStationOptimizedBarrelLowPtLoose.push_back(false);
	//
	if( (*iMuon)->muonID("TMLastStationOptimizedBarrelLowPtTight") ) fNonIsoMuons_TMLastStationOptimizedBarrelLowPtTight.push_back(true);
	else fNonIsoMuons_TMLastStationOptimizedBarrelLowPtTight.push_back(false);

	// 3) Store NHits (Trk, Pixel, Muon). There has to be at LEAST greater than 10 track hits.
	int myInnerTrackNTrkHits   = myInnerTrackRef->hitPattern().numberOfValidTrackerHits();
	int myInnerTrackNPixelHits = myInnerTrackRef->hitPattern().numberOfValidPixelHits();
	int myGlobalTrackNMuonHits  = myGlobalTrackRef->hitPattern().numberOfValidMuonHits(); 
	fNonIsoMuons_InnerTrackNTrkHits.push_back( myInnerTrackNTrkHits );
	fNonIsoMuons_InnerTrackNPixelHits.push_back( myInnerTrackNPixelHits );
	fNonIsoMuons_GlobalTrackNMuonHits.push_back( myGlobalTrackNMuonHits );

	// 4) Store Global Track Chi Square / ndof must be less than 10
	fNonIsoMuons_NormChiSquare.push_back( (*iMuon)->normChi2() );

	// 5) Store Impact Paremeter (d0) wrt beam spot < 0.02cm (applied to track from the inner tracker)
	fNonIsoMuons_IPTwrtBeamLine.push_back( (*iMuon)->dB() );

	// 6) Check that muon has good PV. Store diff between muon track at its vertex and the PV along the Z position ( cm)
	// fNonIsoMuons_IPZwrtPV.push_back(std::abs(myInnerTrackRef->dz(primaryVertex->position()))); // need PV collection for this
	fNonIsoMuons_IPZwrtPV.push_back(-1.0);
      
	// 7) Store several Isolation variables (around cone of DeltaR = 0.3)
	float myMuonPt  = (*iMuon)->pt();
	float myTrackIso =  (*iMuon)->trackIso(); // isolation cones are dR=0.3 
	float myEcalIso  =  (*iMuon)->ecalIso();  // isolation cones are dR=0.3 
	float myHcalIso  =  (*iMuon)->hcalIso();  // isolation cones are dR=0.3 
	float relIsol = ( myTrackIso + myEcalIso + myHcalIso )/(myMuonPt);
	// std::cout << "*** relIsol = (" << myTrackIso + myEcalIso + myHcalIso << ")/" << myMuonPt << " = " << relIsol << std::endl;
	fNonIsoMuons_TrackIso.push_back(myTrackIso);
	fNonIsoMuons_EcalIso.push_back(myEcalIso);
	fNonIsoMuons_HcalIso.push_back(myHcalIso);
	fNonIsoMuons_RelIso.push_back(relIsol);

      }//eof: for( nonIsoMuons )
    }//eof: if
    
    if(nonIsoElectrons.size() >= 1){

      // Loop over all Electrons
      for(edm::PtrVector<pat::Electron>::const_iterator iElectron = nonIsoElectrons.begin(); iElectron != nonIsoElectrons.end(); ++iElectron) {
	
	// Obtain reference to an Electron track
	reco::GsfTrackRef myGsfTrackRef = (*iElectron)->gsfTrack(); // gsfElecs were selected to create the current PatTuples
	// Check whether GSF track ref was found (the electron collection is passed to this function after this selection => GSF track should always be found)
	fNonIsoElectrons_GsfTrkRefIsNull.push_back( myGsfTrackRef.isNull() );

	// Apply electron fiducial volume cut (the electron collection is passed to this function after this selection => ECAL Fiducial cuts already applied)
	reco::SuperClusterRef mySuperClusterRef = (*iElectron)->superCluster(); 
	// Check that superCluster was found & fiducial volume cuts applied
	fNonIsoElectrons_SuperClusterRefIsNull.push_back( mySuperClusterRef.isNull() );
	fNonIsoElectrons_SuperClusterRefEta.push_back( mySuperClusterRef->eta() );
	fNonIsoElectrons_SuperClusterRefPhi.push_back( mySuperClusterRef->phi() );
		
	// 1) Store the 4-momenta
	fNonIsoElectrons.push_back( (*iElectron)->p4() );
      
	// 2) Simple Electron ID's return 1 or 0 (true or false)
	if( (*iElectron)->electronID("eidLoose") ) fNonIsoElectrons_SimpleId_Loose.push_back(true);
	else fNonIsoElectrons_SimpleId_Loose.push_back(false);
	//
	if( (*iElectron)->electronID("eidRobustLoose") ) fNonIsoElectrons_SimpleId_RobustLoose.push_back(true);
	else fNonIsoElectrons_SimpleId_RobustLoose.push_back(false);
	//
	if( (*iElectron)->electronID("eidTight") ) fNonIsoElectrons_SimpleId_Tight.push_back(true);
	else fNonIsoElectrons_SimpleId_Tight.push_back(false);
	//
	if( (*iElectron)->electronID("eidRobustTight") ) fNonIsoElectrons_SimpleId_RobustTight.push_back(true);
	else fNonIsoElectrons_SimpleId_RobustTight.push_back(false);
	//
	if( (*iElectron)->electronID("eidRobustHighEnergy") ) fNonIsoElectrons_SimpleId_RobustHighEnergy.push_back(true);
	else fNonIsoElectrons_SimpleId_RobustHighEnergy.push_back(false);
      
	// 3) Electron ID's with working points return 0,1,2,3,4,5,6,7.
	// Note: 0=fails, 1=passes eID , 2=passes eIsolation , 3=passes eID and eIsolation, 4=passes conversion rejection
	// 5=passes conversion rejection and eID, 6=passes conversion rejection and eIsolation, 7=passes the whole selection
	float fElecIDSimpleEleId95relIso = (*iElectron)->electronID("simpleEleId95relIso");
	float fElecIDSimpleEleId90relIso = (*iElectron)->electronID("simpleEleId90relIso");
	float fElecIDSimpleEleId85relIso = (*iElectron)->electronID("simpleEleId85relIso"); 
	float fElecIDSimpleEleId80relIso = (*iElectron)->electronID("simpleEleId80relIso");
	float fElecIDSimpleEleId70relIso = (*iElectron)->electronID("simpleEleId70relIso");
	float fElecIDSimpleEleId60relIso = (*iElectron)->electronID("simpleEleId60relIso");

	fNonIsoElectrons_ID_EleId95relIso.push_back( fElecIDSimpleEleId95relIso );
	fNonIsoElectrons_ID_EleId90relIso.push_back( fElecIDSimpleEleId90relIso );
	fNonIsoElectrons_ID_EleId85relIso.push_back( fElecIDSimpleEleId85relIso ); 
	fNonIsoElectrons_ID_EleId80relIso.push_back( fElecIDSimpleEleId80relIso );
	fNonIsoElectrons_ID_EleId70relIso.push_back( fElecIDSimpleEleId70relIso );
	fNonIsoElectrons_ID_EleId60relIso.push_back( fElecIDSimpleEleId60relIso );
    
	// 4) Transverse Impact Parameter wrt BeamSpot, applied on the gsfTrack of the Electron candidate
	float myTransverseImpactPar = fabs( (*iElectron)->dB() );  // This is the transverse IP w.r.t to beamline.
	fNonIsoElectrons_IPwrtBeamSpot.push_back( myTransverseImpactPar );
	
	// 5) Photon conversion rejection (gamma->e+e-): If an e- has: |dist| < 0.02 && |delta cot(theta)| < 0.02 then it is regarded as coming from a conversion=>rejected
	// a) Number of lost hits in the tracker
	int iNLostHitsInTrker = myGsfTrackRef->hitPattern().numberOfLostHits();
	fNonIsoElectrons_NLostHitsInTrker.push_back( iNLostHitsInTrker );
	
	/*
	// For Photon Conversion Rejection (Searching for the partner conversion track in the GeneralTrack Collection
	ConversionFinder convFinder;
	ConversionInfo convInfo = convFinder.getConversionInfo(*iElectron, myTracksHandle, myBFieldInZAtZeroZeroZero );

	// b) Define the minimal distance in r-phi plane between the electron and its closest opposite sign track. DeltaR > 0.02
	double myElectronDistance = convInfo.dist();
	fNonIsoElectrons_DistanceOSTrk.push_back( myElectronDistance );
	
	// c) Define the minimal distance between the electron and its closest opposite sign track |Delta cot(Theta) | > 0.02
	double myElectronDeltaCotTheta = convInfo.dcot();
	fNonIsoElectrons_DeltaCotTheta.push_back( myElectronDeltaCotTheta );
      
	// double convradius = convInfo.radiusOfConversion(); // not used in code
	math::XYZPoint convPoint = convInfo.pointOfConversion();
	*/ 
	// tmp
	fNonIsoElectrons_NLostHitsInTrker.push_back( -1.0 );
	fNonIsoElectrons_DistanceOSTrk.push_back( -1.0 );
	fNonIsoElectrons_DeltaCotTheta.push_back( -1.0);

	// 6) Isolation Variables for Electron candidate
	float myElectronPt  = (*iElectron)->pt();  // float myElectronPt = (*iElectron)->p4()->Pt();
	float myElectronEta = (*iElectron)->eta();
	float myElectronPhi = (*iElectron)->phi();
	
	float myTrackIso =  (*iElectron)->dr03TkSumPt();
	float myEcalIso  =  (*iElectron)->dr03EcalRecHitSumEt();
	float myHcalIso  =  (*iElectron)->dr03HcalTowerSumEt();

	// 	float myTrackIso =  (*iElectron)->trackIso();
	// 	float myEcalIso  =  (*iElectron)->ecalIso();
	// 	float myHcalIso  =  (*iElectron)->hcalIso();
	float myRelativeIsolation = (myTrackIso + myEcalIso + myHcalIso)/(myElectronPt); // isolation cones are dR=0.3 
	
	fNonIsoElectrons_TrackIso.push_back( myTrackIso );
	fNonIsoElectrons_EcalIso.push_back( myEcalIso );
	fNonIsoElectrons_HcalIso.push_back( myHcalIso );
	fNonIsoElectrons_RelIso.push_back( myRelativeIsolation );

      
	// 7) DeltaR between Electron candidate and any Global or Tracker Muon in the event whose number of hits in the inner tracker > 10
	float myElectronMuonDeltaR = -1.00;
      
	// Loop over all Muons
	// for(edm::PtrVector<pat::Electron>::const_iterator iElectron = nonIsoElectrons.begin(); iElectron != nonIsoElectrons.end(); ++iElectron) {
	// loop over all muons
	for(edm::PtrVector<pat::Muon>::const_iterator iMuon = nonIsoMuons.begin(); iMuon != nonIsoMuons.end(); ++iMuon) {
	  // for(edm::PtrVector<pat::Muon>::const_iterator iMuon = nonIsoMuons->begin(); iMuon != nonIsoMuons->end(); ++iMuon) {
	  
	  // Check that there are muons present
	  if( nonIsoMuons.size() < 1) continue;
	
	  // Obtain reference to a Muon track
	  reco::TrackRef myGlobalTrackRef = (*iMuon)->globalTrack();
	  reco::TrackRef myInnerTrackRef = (*iMuon)->innerTrack(); // inner tracks give best resolution for muons with Pt up to 200 GeV/c

	  // Check that track was found for both Global AND Tracker Muons
	  if ( myInnerTrackRef.isNull() || myGlobalTrackRef.isNull() ){
	    continue; 
	  }

	  // Muon Variables (Pt, Eta etc..)
	  // float myMuonPt = myInnerTrackRef->pt();
	  float myMuonEta = myInnerTrackRef->eta();
	  float myMuonPhi = myInnerTrackRef->phi();
	  int myInnerTrackNTrkHits   = myInnerTrackRef->hitPattern().numberOfValidTrackerHits();
      
	  // Demand that the Muon is both a "GlobalMuon" And a "TrackerMuon"
	  if( (!(*iMuon)->isGlobalMuon()) || (!(*iMuon)->isTrackerMuon()) ) continue;

	  // Demand Global or Tracker Muons to have at least 10 hits in the inner tracker
	  if ( myInnerTrackNTrkHits < 10) continue;

	  // Calculate DeltaR between Electron candidate and Global or Tracker Muon
	  myElectronMuonDeltaR = deltaR( myMuonEta, myMuonPhi,myElectronEta, myElectronPhi);
	  fNonIsoElectrons_ElectronMuonDeltaR.push_back( myElectronMuonDeltaR );
      
	}//eof: for( Muons) {

      
      }//eof: for (nonIsoElectrons)
    }//eof: if
    
    return;
  }



  void SignalAnalysisTree::reset() {
    fEvent = 0;
    fLumi = 0;
    fRun = 0;

    fPrescaleWeight = 1.0;
    fPileupWeight = 1.0;
    fTriggerWeight = 1.0;
    fBTaggingWeight = 1.0;
    fFillWeight = 1.0;

    fNVertices = 0;

    double nan = std::numeric_limits<double>::quiet_NaN();

    fHltTaus.clear();

    fTau.SetXYZT(nan, nan, nan, nan);
    fTauLeadingChCand.SetXYZT(nan, nan, nan, nan);
    fTauSignalChCands = 0;
    fTauEmFraction = nan;
    for(size_t i=0; i<fTauIds.size(); ++i)
      fTauIds[i].reset();

    fJets.clear();
    fJetsBtags.clear();

    if(fFillJetEnergyFractions) {
      fJetsChf.clear();
      fJetsNhf.clear();
      fJetsElf.clear();
      fJetsPhf.clear();
      fJetsMuf.clear();
    }

    fJetsChm.clear();
    fJetsNhm.clear();
    fJetsElm.clear();
    fJetsPhm.clear();
    fJetsMum.clear();

    fJetsJec.clear();
    fJetsArea.clear();

    fJetsLooseId.clear();
    fJetsTightId.clear();

    fRawMet.SetXYZT(nan, nan, nan, nan);
    fRawMetSumEt = nan;
    fRawMetSignificance = nan;

    fType1Met.SetXYZT(nan, nan, nan, nan);
    fType2Met.SetXYZT(nan, nan, nan, nan);
    fCaloMet.SetXYZT(nan, nan, nan, nan);
    fTcMet.SetXYZT(nan, nan, nan, nan);

    fTop.SetXYZT(nan, nan, nan, nan);

    fAlphaT = nan;
    fDeltaPhi = nan;

    fPassedBTagging = false;

    fGenMet.SetXYZT(nan, nan, nan, nan);

    fTauEmbeddingMuon.SetXYZT(nan, nan, nan, nan);
    fTauEmbeddingMet.SetXYZT(nan, nan, nan, nan);
    fTauEmbeddingCaloMet.SetXYZT(nan, nan, nan, nan);

    // nonIsoMuons
    fNonIsoMuons.clear();
    fNonIsoMuons_IsGlobalMuon.clear();
    fNonIsoMuons_IsTrackerMuon.clear();
    fNonIsoMuons_AllMuons.clear();
    fNonIsoMuons_AllGlobalMuons.clear();
    fNonIsoMuons_AllStandAloneMuons.clear();
    fNonIsoMuons_AllTrackerMuons.clear();
    fNonIsoMuons_TrackerMuonArbitrated.clear();
    fNonIsoMuons_AllArbitrated.clear();
    fNonIsoMuons_GlobalMuonPromptTight.clear();
    fNonIsoMuons_TMLastStationLoose.clear();
    fNonIsoMuons_TMLastStationTight.clear();
    fNonIsoMuons_TMOneStationLoose.clear();
    fNonIsoMuons_TMLastStationOptimizedLowPtLoose.clear();
    fNonIsoMuons_TMLastStationOptimizedLowPtTight.clear();
    fNonIsoMuons_GMTkChiCompatibility.clear();
    fNonIsoMuons_GMTkKinkTight.clear();
    fNonIsoMuons_TMLastStationAngLoose.clear();
    fNonIsoMuons_TMLastStationAngTight.clear();
    fNonIsoMuons_TMLastStationOptimizedBarrelLowPtLoose.clear();
    fNonIsoMuons_TMLastStationOptimizedBarrelLowPtTight.clear();
    fNonIsoMuons_InnerTrackNTrkHits.clear();
    fNonIsoMuons_InnerTrackNPixelHits.clear();
    fNonIsoMuons_GlobalTrackNMuonHits.clear();
    fNonIsoMuons_NormChiSquare.clear();
    fNonIsoMuons_IPTwrtBeamLine.clear(); 
    fNonIsoMuons_IPZwrtPV.clear();
    fNonIsoMuons_TrackIso.clear();
    fNonIsoMuons_EcalIso.clear();
    fNonIsoMuons_HcalIso.clear();
    fNonIsoMuons_RelIso.clear();

    // nonIsoElectrons
    fNonIsoElectrons.clear();
    fNonIsoElectrons_GsfTrkRefIsNull.clear();
    fNonIsoElectrons_SuperClusterRefIsNull.clear();
    fNonIsoElectrons_SuperClusterRefEta.clear();
    fNonIsoElectrons_SuperClusterRefPhi.clear();
    fNonIsoElectrons_SimpleId_Loose.clear();
    fNonIsoElectrons_SimpleId_RobustLoose.clear();
    fNonIsoElectrons_SimpleId_Tight.clear();
    fNonIsoElectrons_SimpleId_RobustTight.clear();
    fNonIsoElectrons_SimpleId_RobustHighEnergy.clear();
    fNonIsoElectrons_ID_EleId95relIso.clear();
    fNonIsoElectrons_ID_EleId90relIso.clear();
    fNonIsoElectrons_ID_EleId85relIso.clear(); 
    fNonIsoElectrons_ID_EleId80relIso.clear();
    fNonIsoElectrons_ID_EleId70relIso.clear();
    fNonIsoElectrons_ID_EleId60relIso.clear();
    fNonIsoElectrons_NLostHitsInTrker.clear();
    fNonIsoElectrons_RelIso.clear();
    fNonIsoElectrons_DeltaCotTheta.clear();
    fNonIsoElectrons_DistanceOSTrk.clear();
    fNonIsoElectrons_IPwrtBeamSpot.clear();
    fNonIsoElectrons_TrackIso.clear();
    fNonIsoElectrons_EcalIso.clear();
    fNonIsoElectrons_HcalIso.clear();
    fNonIsoElectrons_RelIso.clear();
    fNonIsoElectrons_ElectronMuonDeltaR.clear();

  }
}
