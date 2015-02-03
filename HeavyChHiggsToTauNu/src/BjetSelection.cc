#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"

#include <limits>


namespace HPlus {
  BjetSelection::Data::Data():
    fPassedEvent(false) {}
  BjetSelection::Data::~Data() {}

  BjetSelection::BjetSelection(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fOneProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneProngTauSrc")),
    fOneAndThreeProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneAndThreeProngTauSrc"))
  {

    edm::Service<TFileService> fs;

    TFileDirectory myDir = fs->mkdir("BjetSelection");

    hDeltaRmaxFromTop = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaRmaxFromTop", "DeltaRmaxFromTop", 200, 0., 6.);
    hDeltaMinTauB = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaMinTauB", "DeltaMinTauB", 200, 0., 6.);
    hDeltaMaxTauB = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaMaxTauB", "DeltaMaxTauB", 200, 0., 6.);
    hPtBjetTauSide = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtBjetTauSide", "PtBjetTauSide", 200, 0., 400.);
    hEtaBjetTauSide = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "EtaBjetTauSide", "EtaBjetTauSide", 250, -5., 5.);
    hPtBjetTopSide = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "PtBjetTopSide", "PtBjetTopSide", 200, 0., 400.);
    hEtaBjetTopSide = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "EtaBjetTopSide", "EtaBjetTopSide", 250, -5.,5.);
    hPtBjetMax = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtBjetMax", "PtBjetMax", 200, 0., 400.);
    hEtaBjetMax = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "EtaBjetMax", "EtaBjetMax", 250, -5.,5.);
    hPtBjetMaxTrue = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtBjetMaxTrue", "PtBjetMaxTrue", 200, 0., 400.);
    hEtaBjetMaxTrue = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "EtaBjetMaxTrue", "EtaBjetMaxTrue", 250, -5.,5.);
    hDeltaMinTauBTrue = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaMinTauBTrue", "DeltaMinTauBTrue", 200, 0., 6.);
    hDeltaMaxTopBTrue = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaMaxTopBTrue", "DeltaMaxTopBTrue", 200, 0., 6.);
    hPtBjetTauSideTrue = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtBjetTauSideTrue", "PtBjetTauSideTrue", 200, 0., 400.);
    hEtaBjetTauSideTrue = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "EtaBjetTauSideTrue", "EtaBjetTauSideTrue", 250, -5., 5.);
    hPtBjetTopSideTrue = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "PtBjetTopSideTrue", "PtBjetTopSideTrue", 200, 0., 400.);
    hEtaBjetTopSideTrue = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "EtaBjetTopSideTrue", "EtaBjetTopSideTrue", 250, -5.,5.);
    hMassTopTop = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MassTopTop_matchJets", "MassTopTop_matchJets",400, 0.,400.);
    hMassTopHiggs = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MassTopHiggs_matchJets", "MassTopHiggs_matchJets",400, 0.,400.);
    hMassW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MassW_matchJets", "MassW_matchJets",300, 0.,300.);
    hPtTopTop = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtTopTop_matchJets", "PtTopTop_matchJets",200, 0.,400.);
    hPtTopHiggs = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtTopHiggs_matchJets", "PtTopHiggs_matchJets",200, 0.,400.);
    hPtW = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtW_matchJets", "PtW_matchJets",200, 0.,400.);
    hBquarkFromHiggsSideEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "EtaBquarkFromHiggsSide", "EtaBquarkFromHiggsSide", 250, -5.,5.);
    hBquarkFromHiggsSidePt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtBquarkFromHiggsSide", "PtBquarkFromHiggsSide", 200, 0.,400.);
    hBquarkFromTopSideEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "EtaBquarkFromTopSide", "EtaBquarkFromTopSide", 250, -5.,5.);
    hBquarkFromTopSidePt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtBquarkFromTopSide", "PtBquarkFromTopSide", 200, 0.,400.);
    hQquarkFromTopSidePt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtQquarkFromTopSide", "PtQquarkFromTopSide", 200, 0.,400.);
    hQquarkFromTopSideEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "EtaQquarkFromTopSide", "EtaQquarkFromTopSide", 250, -5.,5.);
    hDeltaRtauBtauSide = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaRtauBtauSide", "DeltaRtauBtauSide", 200, 0., 6.);
    hDeltaRHadTauBtauSide = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaRHadTauBtauSide", "DeltaRHadTauBtauSide", 200, 0., 6.);
    hDeltaRHadTauBtopSide = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaRHadTauBtopSide", "DeltaRHadTauBtopSide", 200, 0., 6.);
    hDeltaTauB = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaTauB", "DeltaTauB", 200, 0., 6.);
    

  }

  BjetSelection::~BjetSelection() {}

  BjetSelection::Data BjetSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<reco::Candidate>& tau , const edm::Ptr<reco::MET>& met ) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, jets, bjets, tau, met);
  }

  BjetSelection::Data BjetSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<reco::Candidate>& tau , const edm::Ptr<reco::MET>& met ) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, jets, bjets, tau, met);
  }

  BjetSelection::Data BjetSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<reco::Candidate>& tau , const edm::Ptr<reco::MET>& met ) {
    Data output;

    edm::Handle <reco::GenParticleCollection> genParticles;
    if (!iEvent.isRealData())
      iEvent.getByLabel(fSrc, genParticles);

    typedef math::XYZTLorentzVectorD LorentzVector;
    typedef std::vector<LorentzVector> LorentzVectorCollection;

    edm::Handle <std::vector<LorentzVector> > oneProngTaus;
    iEvent.getByLabel(fOneProngTauSrc, oneProngTaus);

    edm::Handle <std::vector<LorentzVector> > oneAndThreeProngTaus;
    iEvent.getByLabel(fOneAndThreeProngTauSrc,oneAndThreeProngTaus);	  

//    double nan = std::numeric_limits<double>::quiet_NaN();

    bool bjetTopSideFound = false;
    bool bjetTauSideFound = false;
    bool bjetMaxFound = false;
    double deltaRMax = 0;
    double deltaRMin = 999999;
    double pTmax = 0;
    edm::Ptr<pat::Jet> BjetMaxPt;
    int nonbjets;

    // max pt b jet and b jet most far from tau jet
    
    // loop over b jets
    for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjets.begin(); iterb != bjets.end(); ++iterb) {
      edm::Ptr<pat::Jet> iJetb = *iterb;

      //loop over jets and count non-b jets
      nonbjets = 0;
      // search non-b-jets
      for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter ) {
	edm::Ptr<pat::Jet> iJet = *iter;
	double deltaR = ROOT::Math::VectorUtil::DeltaR(iJetb->p4(), iJet->p4());
	if ( deltaR > 0.4 ) nonbjets++;
      }

      //search the hardest b jet
      if (iJetb->pt() > pTmax ) {
	pTmax = iJetb->pt();
	bjetMaxFound = true;
	BjetMaxPt = iJetb;
      }
      //search the "top side" (W side) b jet, i.e. the one with highes dR from tau
      double deltaRtau = ROOT::Math::VectorUtil::DeltaR((tau)->p4(), iJetb->p4());
      hDeltaTauB->Fill(deltaRtau);  
      if ( deltaRtau > deltaRMax) {
	deltaRMax = deltaRtau;	
	bjetTopSideFound = true;
	output.BjetTopSide = iJetb;
      }
    }


    if( !bjetTopSideFound  ) return output;
    hPtBjetTopSide->Fill(output.BjetTopSide->pt());
    hEtaBjetTopSide->Fill(output.BjetTopSide->eta());
    hDeltaMaxTauB->Fill(deltaRMax); 
    hPtBjetMax->Fill(BjetMaxPt->pt());  
    hEtaBjetMax->Fill(BjetMaxPt->eta());  
    
    //old version: search the hardest b jet in the opposite hemisphere
    
    //    std::cout << " Jets.size() " << jets.size()<< " bjets.size() " << bjets.size() <<" nonbjets " << nonbjets << std::endl; 
    /*
    // hardest b jet in opposite hemisphere
    double pTmax = 0;
    for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjets.begin(); iterb != bjets.end(); ++iterb) {
      edm::Ptr<pat::Jet> iJetb = *iterb;
      double deltaRtau = ROOT::Math::VectorUtil::DeltaR((tau)->p4(), iJetb->p4());
      hDeltaTauB->Fill(deltaRtau);  
      if ( deltaRtau > 2.0 ) {
	if ( iJetb->pt() > pTmax) {
	  pTmax = iJetb->pt();	
	  bjetTopSideFound = true;
	  BjetTopSide = iJetb;
	}
      }
    }
    if( !bjetTopSideFound  ) return Data(this, passEvent);
    hPtBjetTopSide->Fill(output.BjetTopSide->pt());
    hEtaBjetTopSide->Fill(output.BjetTopSide->eta());
    hDeltaMaxTauB->Fill(deltaRMax); 
    */



    // b jet closest to tau jet from remaining jets   
    for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjets.begin(); iterb != bjets.end(); ++iterb) {
      edm::Ptr<pat::Jet> iJetb = *iterb;
      double deltaRBTopSide = ROOT::Math::VectorUtil::DeltaR(output.BjetTopSide->p4(), iJetb->p4());
      if ( deltaRBTopSide < 0.4) continue;
      double deltaRtau = ROOT::Math::VectorUtil::DeltaR((tau)->p4(), iJetb->p4());
      if ( deltaRtau < deltaRMin) {
	deltaRMin = deltaRtau;	 
	bjetTauSideFound = true;
	output.BjetTauSide = iJetb;
      }
    }

    if( bjetTauSideFound  ) {
      hDeltaMinTauB->Fill(deltaRMin); 
      hPtBjetTauSide->Fill(output.BjetTauSide->pt());
      hEtaBjetTauSide->Fill(output.BjetTauSide->eta());
    }

    // matched event

    if (!iEvent.isRealData()) {

      int idHiggsSide = 0;
      // Identity of Higgs side
      LorentzVector topHiggsSide;

      for (size_t i=0; i < genParticles->size(); ++i){
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	//	if(abs(id) == 6 ) printImmediateDaughters(p);
	
	// if particle is top and decays to H+
	if(abs(id) == 6 && (hasImmediateDaughter(p,37) || hasImmediateDaughter(p,-37))) {
	  idHiggsSide = id;
	}
      }

    
      edm::PtrVector<pat::Jet> bjetsAny;
      edm::PtrVector<pat::Jet> jetsFromW;
      edm::PtrVector<pat::Jet> bjetsFromTop;
      edm::PtrVector<pat::Jet> bjetsHiggsSide;
      edm::PtrVector<pat::Jet> bjetsTopSide;
      std::vector<LorentzVector> bquarkTopSide;
      std::vector<LorentzVector> QquarksTopSide;
      bjetsAny.clear();
      jetsFromW.clear();
      bjetsFromTop.clear();
      bjetsHiggsSide.clear();
      bjetsTopSide.clear();
      double bPt, bEta;
      

      // search matched b jets
      for (size_t i=0; i < genParticles->size(); ++i){
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	//if particle is not b or is coming from b, skip
	if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
	bEta = p.eta();
	bPt = p.pt();
	//if b comes from top, check which top
	if(hasImmediateMother(p,6) || hasImmediateMother(p,-6)) {
	  if ( id * idHiggsSide < 0 ) {
	    bquarkTopSide.push_back(p.p4());
	    hBquarkFromTopSideEta->Fill(bEta);
	    hBquarkFromTopSidePt->Fill(bPt);
	  }
	  if ( id * idHiggsSide > 0 ) {
	    hBquarkFromHiggsSideEta->Fill(bEta);
	    hBquarkFromHiggsSidePt->Fill(bPt);
	  }	  
	  // 	    printImmediateMothers(p);
	  //	std::cout << " b quark1 " << id <<  " idHiggsSide " <<   idHiggsSide << std::endl;
	  
	  //loop over b jets and store them into different vectors
	  for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjets.begin(); iterb != bjets.end(); ++iterb ) {
	    edm::Ptr<pat::Jet> iJetb = *iterb;
	    double deltaR = ROOT::Math::VectorUtil::DeltaR(p.p4(), iJetb->p4());
	    if ( deltaR < 0.4 ) {
	      bjetsAny.push_back(iJetb);
	      //b jets from top
	      if( hasImmediateMother(p,6) || hasImmediateMother(p,-6)) {
		bjetsFromTop.push_back(iJetb);
		// b from Higgs side
		if ( id * idHiggsSide > 0 ) {
		  bjetsHiggsSide.push_back(iJetb);
		}
		// b from Top side
		if ( id * idHiggsSide < 0 ) {
		  bjetsTopSide.push_back(iJetb);
		}
	      }
	    }
	  }
	  
	}
      }	
      
						
     // search for matched light quark jets
      for (size_t i=0; i < genParticles->size(); ++i){
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	// if particle is not a light quark or is coming from a light quark, skip
	if ( abs(id) > 4  )continue;
	if ( hasImmediateMother(p,1) || hasImmediateMother(p,-1) )continue;
	if ( hasImmediateMother(p,2) || hasImmediateMother(p,-2) )continue;
	if ( hasImmediateMother(p,3) || hasImmediateMother(p,-3) )continue;
	if ( hasImmediateMother(p,4) || hasImmediateMother(p,-4) )continue;
	bEta = p.eta();
	bPt = p.pt();
	// if light quark is coming from W
	if(hasImmediateMother(p,24) || hasImmediateMother(p,-24)) {
	  hQquarkFromTopSideEta->Fill(bEta);
	  hQquarkFromTopSidePt->Fill(bPt);
	  QquarksTopSide.push_back(p.p4());
	  //loop over jets and select the light quarks coming from W
	  for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter ) {
	    edm::Ptr<pat::Jet> iJet = *iter;
	    double deltaR = ROOT::Math::VectorUtil::DeltaR(p.p4(), iJet->p4());
	    //	    printImmediateMothers(p);
	    //	    std::cout << " q quark1 " << id <<  " deltaR " <<   deltaR << " jet Et " << iJet->p4().pt() << std::endl;
	    if ( deltaR < 0.5) jetsFromW.push_back(iJet);
	  }
	}
      							   
      }
      //      std::cout << " QquarksTopSide.size() " << QquarksTopSide.size()<< " bquarkTopSide.size() " << bquarkTopSide.size() << std::endl


    
      // W and top mass from matched jets
      if (jetsFromW.size() == 2) {
	
	//	edm::PtrVector<pat::Jet>::const_iterator iJet1 = jetsFromW.begin();
	//	edm::PtrVector<pat::Jet>::const_iterator iJet2 = jetsFromW.begin()+1;

	for(edm::PtrVector<pat::Jet>::const_iterator iter = jetsFromW.begin(); iter != jetsFromW.end(); ++iter) {
	  edm::Ptr<pat::Jet> iJet1 = *iter;
	  
	  for(edm::PtrVector<pat::Jet>::const_iterator iter2 = jetsFromW.begin(); iter2 != jetsFromW.end(); ++iter2) {
	    edm::Ptr<pat::Jet> iJet2 = *iter2;
	    
	    if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJet2->p4()) < 0.4) continue;
	    XYZTLorentzVector candW = iJet1->p4() + iJet2->p4();
	    
	    hPtW->Fill(candW.Pt());
	    hMassW->Fill(candW.M());
	  
	    if (bjetsTopSide.size() == 1) {	  
	      for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjetsTopSide.begin(); iterb != bjetsTopSide.end(); ++iterb) {
		edm::Ptr<pat::Jet> iJetb = *iterb;
		if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJetb->p4()) < 0.4) continue;
		if (ROOT::Math::VectorUtil::DeltaR(iJet2->p4(), iJetb->p4()) < 0.4) continue;	  
		
		XYZTLorentzVector candTop= iJet1->p4() + iJet2->p4() + iJetb->p4();
		
		hPtTopTop->Fill(candTop.Pt());
		hMassTopTop->Fill(candTop.M());	
	      }
	    }
	    if (bjetsHiggsSide.size() == 1) {	  
	      for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjetsHiggsSide.begin(); iterb != bjetsHiggsSide.end(); ++iterb) {
		edm::Ptr<pat::Jet> iJetb = *iterb;
		if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJetb->p4()) < 0.4) continue;
		if (ROOT::Math::VectorUtil::DeltaR(iJet2->p4(), iJetb->p4()) < 0.4) continue;	  
		
		XYZTLorentzVector candTop= iJet1->p4() + iJet2->p4() + iJetb->p4();
		
		hPtTopHiggs->Fill(candTop.Pt());
		hMassTopHiggs->Fill(candTop.M());
		
	      }
	    }
	  }
	}
      }


// match selected jets 

      bool bjetHiggsSide = false; 
      if( bjetTauSideFound  ) {

	int idbjetHiggsSide = 0;
      
	std::vector<LorentzVector> tausFromHp;

    //search taus which come from H+
	for (size_t i=0; i < genParticles->size(); ++i){
	  const reco::Candidate & p = (*genParticles)[i];
	  int id = p.pdgId();	  
	  if ( abs(id) != 15 || hasImmediateMother(p,15) || hasImmediateMother(p,-15) )continue;
	  if(hasImmediateMother(p,37) || hasImmediateMother(p,-37)) {
	    tausFromHp.push_back(p.p4());	    
	  }
	}


	for (size_t i=0; i < genParticles->size(); ++i){
	  const reco::Candidate & p = (*genParticles)[i];
	  int id = p.pdgId();

	  if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
	  bEta = p.eta();
	  bPt = p.pt();
	  if(hasImmediateMother(p,6) || hasImmediateMother(p,-6)) {
	    //	  printImmediateMothers(p);
	    //	    std::cout << " p " << p.p4() <<  " tau " <<  tau.p4() << std::endl;
	    if ( id * idHiggsSide > 0 ) {
	      //	      hBquarkFromHiggsSideEta->Fill(bEta);
	      //	      hBquarkFromHiggsSidePt->Fill(bPt);
	      if ( tausFromHp.size() > 0) {
		double deltaRtaub = ROOT::Math::VectorUtil::DeltaR(tausFromHp[0],p.p4() );
		hDeltaRtauBtauSide->Fill(deltaRtaub);      
	      }
	      // test with b jet from tau side
	      double deltaR = ROOT::Math::VectorUtil::DeltaR(output.BjetTauSide->p4(),p.p4() );
	      if ( deltaR < 0.4) bjetHiggsSide = true;
	      idbjetHiggsSide = id;
	    }
	  }
	} 
	if(bjetHiggsSide) {
	  hDeltaMinTauBTrue->Fill(deltaRMin);      
	  hPtBjetTauSideTrue->Fill(output.BjetTauSide->pt());
	  hEtaBjetTauSideTrue->Fill(output.BjetTauSide->eta());
	}
      }
      
      
      bool bjetTopSide  = false;
      if ( bjetTopSideFound ) {
	for (size_t i=0; i < genParticles->size(); ++i){
	  const reco::Candidate & p = (*genParticles)[i];
	  int id = p.pdgId();
	  if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
	  bEta = p.eta();
	  bPt = p.pt();
	  if(hasImmediateMother(p,6) || hasImmediateMother(p,-6)) {
	    if ( id * idHiggsSide < 0 ) {
	      //	      printImmediateMothers(p);
	      //	      hBquarkFromTopSideEta->Fill(bEta);
	      //	      hBquarkFromTopSidePt->Fill(bPt);
	      // test with b jet from tau side
	      double deltaR = ROOT::Math::VectorUtil::DeltaR(output.BjetTopSide->p4(),p.p4() ); 
	      if ( deltaR < 0.4) bjetTopSide = true;
	    }
	  }
	}
	if(  bjetTopSide ) {
	  hDeltaMaxTopBTrue->Fill(deltaRMax);     
	  hPtBjetTopSideTrue->Fill(output.BjetTopSide->pt());
	  hEtaBjetTopSideTrue->Fill(output.BjetTopSide->eta());
	}
      } 

  
      if ( bquarkTopSide.size() == 1 && bjetMaxFound ) {
	double deltaR = ROOT::Math::VectorUtil::DeltaR(BjetMaxPt->p4() ,bquarkTopSide[0] );
	if (deltaR < 0.4) {
	  hPtBjetMaxTrue->Fill(BjetMaxPt->pt());
	  hEtaBjetMaxTrue->Fill(BjetMaxPt->eta());
	}
      }
      
    // pure MC
      for( LorentzVectorCollection::const_iterator tau = oneProngTaus->begin();tau!=oneProngTaus->end();++tau) { 
	bool tauFromHplus = false;
	for (size_t i=0; i < genParticles->size(); ++i){
	  const reco::Candidate & p = (*genParticles)[i];
	  int id = p.pdgId();	  
	  if ( abs(id) != 15 || hasImmediateMother(p,15) || hasImmediateMother(p,-15) )continue;
	  if(hasImmediateMother(p,37) || hasImmediateMother(p,-37)) {
	    double deltaR = ROOT::Math::VectorUtil::DeltaR(*tau,p.p4() );
	    if (deltaR < 0.4) tauFromHplus = true;	    
	  }
	}
	if( !tauFromHplus ) continue;
	if( tau->pt() < 40) continue;

	for (size_t i=0; i < genParticles->size(); ++i){  
	  const reco::Candidate & p = (*genParticles)[i];  
	  int id = p.pdgId();
	  if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
	  if(hasImmediateMother(p,6) || hasImmediateMother(p,-6)) {
	    if ( id * idHiggsSide > 0 ) {
	      double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	      hDeltaRHadTauBtauSide->Fill(deltaR);
	    }
	    if ( id * idHiggsSide < 0 ) {
	      double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	      hDeltaRHadTauBtopSide->Fill(deltaR);
	    }
	  }  
	}
      }


      // maximum DR between top decay products
      double deltaRmax = 0;
      if ( QquarksTopSide.size() == 2 ) {
	double deltaRqq = ROOT::Math::VectorUtil::DeltaR(QquarksTopSide[0] ,QquarksTopSide[1] );
	if ( bquarkTopSide.size() == 1 ) {
	  double deltaRq1b = ROOT::Math::VectorUtil::DeltaR(QquarksTopSide[0] ,bquarkTopSide[0] );
	  double deltaRq2b = ROOT::Math::VectorUtil::DeltaR(QquarksTopSide[1] ,bquarkTopSide[0] );	  
	  deltaRmax = deltaRqq;
	  if (deltaRq1b > deltaRmax ) deltaRmax= deltaRq1b;
	  if (deltaRq2b > deltaRmax ) deltaRmax= deltaRq2b;
	}
      }

      //      std::cout << " deltaRmax " << deltaRmax << std::endl;
      if (deltaRmax > 0 ) hDeltaRmaxFromTop->Fill(deltaRmax);      
    }


  
    output.fPassedEvent = true;
    if( !bjetTopSideFound) output.fPassedEvent = false;
    return output;
  }
  
}
