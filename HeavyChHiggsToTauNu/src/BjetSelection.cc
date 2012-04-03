#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"

#include <limits>

std::vector<const reco::GenParticle*>   getImmediateMothers(const reco::Candidate&);
std::vector<const reco::GenParticle*>   getMothers(const reco::Candidate& p);
bool  hasImmediateMother(const reco::Candidate& p, int id);
bool  hasMother(const reco::Candidate& p, int id);
void  printImmediateMothers(const reco::Candidate& p);
void  printMothers(const reco::Candidate& p);
std::vector<const reco::GenParticle*>  getImmediateDaughters(const reco::Candidate& p);
std::vector<const reco::GenParticle*>   getDaughters(const reco::Candidate& p);
bool  hasImmediateDaughter(const reco::Candidate& p, int id);
bool  hasDaughter(const reco::Candidate& p, int id);
void  printImmediateDaughters(const reco::Candidate& p);
void printDaughters(const reco::Candidate& p);



namespace HPlus {
  BjetSelection::Data::Data(const BjetSelection *bjetSelection, bool passedEvent):
    fBjetSelection(bjetSelection), fPassedEvent(passedEvent) {}
  BjetSelection::Data::~Data() {}

  BjetSelection::BjetSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fOneProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneProngTauSrc")),
    fOneAndThreeProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneAndThreeProngTauSrc")),
    fEventWeight(eventWeight)
  {

    edm::Service<TFileService> fs;

    TFileDirectory myDir = fs->mkdir("BjetSelection");

    hDeltaRmaxFromTop = makeTH<TH1F>(myDir, "DeltaRmaxFromTop", "DeltaRmaxFromTop", 200, 0., 6.);
    hDeltaMinTauB = makeTH<TH1F>(myDir, "DeltaMinTauB", "DeltaMinTauB", 200, 0., 6.);
    hDeltaMaxTauB = makeTH<TH1F>(myDir, "DeltaMaxTauB", "DeltaMaxTauB", 200, 0., 6.);
    hPtBjetTauSide = makeTH<TH1F>(myDir, "PtBjetTauSide", "PtBjetTauSide", 200, 0., 400.);
    hEtaBjetTauSide = makeTH<TH1F>(myDir, "EtaBjetTauSide", "EtaBjetTauSide", 250, -5., 5.);
    hPtBjetTopSide = makeTH<TH1F>(myDir, "PtBjetTopSide", "PtBjetTopSide", 200, 0., 400.);
    hEtaBjetTopSide = makeTH<TH1F>(myDir, "EtaBjetTopSide", "EtaBjetTopSide", 250, -5.,5.);
    hPtBjetMax = makeTH<TH1F>(myDir, "PtBjetMax", "PtBjetMax", 200, 0., 400.);
    hEtaBjetMax = makeTH<TH1F>(myDir, "EtaBjetMax", "EtaBjetMax", 250, -5.,5.);
    hPtBjetMaxTrue = makeTH<TH1F>(myDir, "PtBjetMaxTrue", "PtBjetMaxTrue", 200, 0., 400.);
    hEtaBjetMaxTrue = makeTH<TH1F>(myDir, "EtaBjetMaxTrue", "EtaBjetMaxTrue", 250, -5.,5.);
    hDeltaMinTauBTrue = makeTH<TH1F>(myDir, "DeltaMinTauBTrue", "DeltaMinTauBTrue", 200, 0., 6.);
    hDeltaMaxTopBTrue = makeTH<TH1F>(myDir, "DeltaMaxTopBTrue", "DeltaMaxTopBTrue", 200, 0., 6.);
    hPtBjetTauSideTrue = makeTH<TH1F>(myDir, "PtBjetTauSideTrue", "PtBjetTauSideTrue", 200, 0., 400.);
    hEtaBjetTauSideTrue = makeTH<TH1F>(myDir, "EtaBjetTauSideTrue", "EtaBjetTauSideTrue", 250, -5., 5.);
    hPtBjetTopSideTrue = makeTH<TH1F>(myDir, "PtBjetTopSideTrue", "PtBjetTopSideTrue", 200, 0., 400.);
    hEtaBjetTopSideTrue = makeTH<TH1F>(myDir, "EtaBjetTopSideTrue", "EtaBjetTopSideTrue", 250, -5.,5.);
    hMassTopTop = makeTH<TH1F>(myDir, "MassTopTop_matchJets", "MassTopTop_matchJets",400, 0.,400.);
    hMassTopHiggs = makeTH<TH1F>(myDir, "MassTopHiggs_matchJets", "MassTopHiggs_matchJets",400, 0.,400.);
    hMassW = makeTH<TH1F>(myDir, "MassW_matchJets", "MassW_matchJets",300, 0.,300.);
    hPtTopTop = makeTH<TH1F>(myDir, "PtTopTop_matchJets", "PtTopTop_matchJets",200, 0.,400.);
    hPtTopHiggs = makeTH<TH1F>(myDir, "PtTopHiggs_matchJets", "PtTopHiggs_matchJets",200, 0.,400.);
    hPtW = makeTH<TH1F>(myDir, "PtW_matchJets", "PtW_matchJets",200, 0.,400.);
    hBquarkFromHiggsSideEta = makeTH<TH1F>(myDir, "EtaBquarkFromHiggsSide", "EtaBquarkFromHiggsSide", 250, -5.,5.);
    hBquarkFromHiggsSidePt = makeTH<TH1F>(myDir, "PtBquarkFromHiggsSide", "PtBquarkFromHiggsSide", 200, 0.,400.);
    hBquarkFromTopSideEta = makeTH<TH1F>(myDir, "EtaBquarkFromTopSide", "EtaBquarkFromTopSide", 250, -5.,5.);
    hBquarkFromTopSidePt = makeTH<TH1F>(myDir, "PtBquarkFromTopSide", "PtBquarkFromTopSide", 200, 0.,400.);
    hQquarkFromTopSidePt = makeTH<TH1F>(myDir, "PtQquarkFromTopSide", "PtQquarkFromTopSide", 200, 0.,400.);
    hQquarkFromTopSideEta = makeTH<TH1F>(myDir, "EtaQquarkFromTopSide", "EtaQquarkFromTopSide", 250, -5.,5.);
    hDeltaRtauBtauSide = makeTH<TH1F>(myDir, "DeltaRtauBtauSide", "DeltaRtauBtauSide", 200, 0., 6.);
    hDeltaRHadTauBtauSide = makeTH<TH1F>(myDir, "DeltaRHadTauBtauSide", "DeltaRHadTauBtauSide", 200, 0., 6.);
    hDeltaRHadTauBtopSide = makeTH<TH1F>(myDir, "DeltaRHadTauBtopSide", "DeltaRHadTauBtopSide", 200, 0., 6.);
    hDeltaTauB = makeTH<TH1F>(myDir, "DeltaTauB", "DeltaTauB", 200, 0., 6.);
    

  }

  BjetSelection::~BjetSelection() {}

 
  BjetSelection::Data BjetSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets, const edm::Ptr<reco::Candidate>& tau , const edm::Ptr<reco::MET>& met ) {


    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel(fSrc, genParticles);

    typedef math::XYZTLorentzVectorD LorentzVector;
    typedef std::vector<LorentzVector> LorentzVectorCollection;

    edm::Handle <std::vector<LorentzVector> > oneProngTaus;
    iEvent.getByLabel(fOneProngTauSrc, oneProngTaus);

    edm::Handle <std::vector<LorentzVector> > oneAndThreeProngTaus;
    iEvent.getByLabel(fOneAndThreeProngTauSrc,oneAndThreeProngTaus);	  

    bool passEvent = false;
      
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
    for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjets.begin(); iterb != bjets.end(); ++iterb) {
      edm::Ptr<pat::Jet> iJetb = *iterb;

      nonbjets = 0;    
      // search non-b-jets
      for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter ) {
	edm::Ptr<pat::Jet> iJet = *iter;
	double deltaR = ROOT::Math::VectorUtil::DeltaR(iJetb->p4(), iJet->p4());
	if ( deltaR > 0.4 ) nonbjets++;
      }
      

      if (iJetb->pt() > pTmax ) {
	pTmax = iJetb->pt();
	bjetMaxFound = true;
	BjetMaxPt = iJetb;
      }
      double deltaRtau = ROOT::Math::VectorUtil::DeltaR((tau)->p4(), iJetb->p4());
      hDeltaTauB->Fill(deltaRtau, fEventWeight.getWeight());  
      if ( deltaRtau > deltaRMax) {
	deltaRMax = deltaRtau;	
	bjetTopSideFound = true;
	BjetTopSide = iJetb;
      }
    }


    if( !bjetTopSideFound  ) return Data(this, passEvent);
    hPtBjetTopSide->Fill(BjetTopSide->pt(), fEventWeight.getWeight());
    hEtaBjetTopSide->Fill(BjetTopSide->eta(), fEventWeight.getWeight());
    hDeltaMaxTauB->Fill(deltaRMax, fEventWeight.getWeight()); 
    hPtBjetMax->Fill(BjetMaxPt->pt(), fEventWeight.getWeight());  
    hEtaBjetMax->Fill(BjetMaxPt->eta(), fEventWeight.getWeight());  
    //    std::cout << " Jets.size() " << jets.size()<< " bjets.size() " << bjets.size() <<" nonbjets " << nonbjets << std::endl; 
    /*
    // hardest b jet in opposite hemisphere
    double pTmax = 0;
    for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjets.begin(); iterb != bjets.end(); ++iterb) {
      edm::Ptr<pat::Jet> iJetb = *iterb;
      double deltaRtau = ROOT::Math::VectorUtil::DeltaR((tau)->p4(), iJetb->p4());
      hDeltaTauB->Fill(deltaRtau, fEventWeight.getWeight());  
      if ( deltaRtau > 2.0 ) {
	if ( iJetb->pt() > pTmax) {
	  pTmax = iJetb->pt();	
	  bjetTopSideFound = true;
	  BjetTopSide = iJetb;
	}
      }
    }
    if( !bjetTopSideFound  ) return Data(this, passEvent);
    hPtBjetTopSide->Fill(BjetTopSide->pt(), fEventWeight.getWeight());
    hEtaBjetTopSide->Fill(BjetTopSide->eta(), fEventWeight.getWeight());
    hDeltaMaxTauB->Fill(deltaRMax, fEventWeight.getWeight()); 
    */



    // b jet closest to tau jet from remaining jets   
    for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjets.begin(); iterb != bjets.end(); ++iterb) {
      edm::Ptr<pat::Jet> iJetb = *iterb;
      double deltaRBTopSide = ROOT::Math::VectorUtil::DeltaR(BjetTopSide->p4(), iJetb->p4());
      if ( deltaRBTopSide < 0.4) continue;
      double deltaRtau = ROOT::Math::VectorUtil::DeltaR((tau)->p4(), iJetb->p4());
      if ( deltaRtau < deltaRMin) {
	deltaRMin = deltaRtau;	 
	bjetTauSideFound = true;
	BjetTauSide = iJetb;
      }
    }

    if( bjetTauSideFound  ) {
      hDeltaMinTauB->Fill(deltaRMin, fEventWeight.getWeight()); 
      hPtBjetTauSide->Fill(BjetTauSide->pt(), fEventWeight.getWeight());
      hEtaBjetTauSide->Fill(BjetTauSide->eta(), fEventWeight.getWeight());
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
	if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
	bEta = p.eta();
	bPt = p.pt();
	if(hasImmediateMother(p,6) || hasImmediateMother(p,-6)) {
	  if ( id * idHiggsSide < 0 ) {
	    bquarkTopSide.push_back(p.p4());
	    hBquarkFromTopSideEta->Fill(bEta, fEventWeight.getWeight());
	    hBquarkFromTopSidePt->Fill(bPt, fEventWeight.getWeight());
	  }
	  if ( id * idHiggsSide > 0 ) {
	    hBquarkFromHiggsSideEta->Fill(bEta, fEventWeight.getWeight());
	    hBquarkFromHiggsSidePt->Fill(bPt, fEventWeight.getWeight());
	  }	  
	  // 	    printImmediateMothers(p);
	  //	std::cout << " b quark1 " << id <<  " idHiggsSide " <<   idHiggsSide << std::endl;
	  
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
	if ( abs(id) > 4  )continue;
	if ( hasImmediateMother(p,1) || hasImmediateMother(p,-1) )continue;
	if ( hasImmediateMother(p,2) || hasImmediateMother(p,-2) )continue;
	if ( hasImmediateMother(p,3) || hasImmediateMother(p,-3) )continue;
	if ( hasImmediateMother(p,4) || hasImmediateMother(p,-4) )continue;
	bEta = p.eta();
	bPt = p.pt();
	if(hasImmediateMother(p,24) || hasImmediateMother(p,-24)) {
	  hQquarkFromTopSideEta->Fill(bEta, fEventWeight.getWeight());
	  hQquarkFromTopSidePt->Fill(bPt, fEventWeight.getWeight());
	  QquarksTopSide.push_back(p.p4());
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
	    
	    hPtW->Fill(candW.Pt(), fEventWeight.getWeight());
	    hMassW->Fill(candW.M(), fEventWeight.getWeight());
	  
	    if (bjetsTopSide.size() == 1) {	  
	      for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjetsTopSide.begin(); iterb != bjetsTopSide.end(); ++iterb) {
		edm::Ptr<pat::Jet> iJetb = *iterb;
		if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJetb->p4()) < 0.4) continue;
		if (ROOT::Math::VectorUtil::DeltaR(iJet2->p4(), iJetb->p4()) < 0.4) continue;	  
		
		XYZTLorentzVector candTop= iJet1->p4() + iJet2->p4() + iJetb->p4();
		
		hPtTopTop->Fill(candTop.Pt(), fEventWeight.getWeight());
		hMassTopTop->Fill(candTop.M(), fEventWeight.getWeight());	
	      }
	    }
	    if (bjetsHiggsSide.size() == 1) {	  
	      for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjetsHiggsSide.begin(); iterb != bjetsHiggsSide.end(); ++iterb) {
		edm::Ptr<pat::Jet> iJetb = *iterb;
		if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJetb->p4()) < 0.4) continue;
		if (ROOT::Math::VectorUtil::DeltaR(iJet2->p4(), iJetb->p4()) < 0.4) continue;	  
		
		XYZTLorentzVector candTop= iJet1->p4() + iJet2->p4() + iJetb->p4();
		
		hPtTopHiggs->Fill(candTop.Pt(), fEventWeight.getWeight());
		hMassTopHiggs->Fill(candTop.M(), fEventWeight.getWeight());
		
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
	      //	      hBquarkFromHiggsSideEta->Fill(bEta, fEventWeight.getWeight());
	      //	      hBquarkFromHiggsSidePt->Fill(bPt, fEventWeight.getWeight());
	      if ( tausFromHp.size() > 0) {
		double deltaRtaub = ROOT::Math::VectorUtil::DeltaR(tausFromHp[0],p.p4() );
		hDeltaRtauBtauSide->Fill(deltaRtaub, fEventWeight.getWeight());      
	      }
	      // test with b jet from tau side
	      double deltaR = ROOT::Math::VectorUtil::DeltaR(BjetTauSide->p4(),p.p4() );
	      if ( deltaR < 0.4) bjetHiggsSide = true;
	      idbjetHiggsSide = id;
	    }
	  }
	} 
	if(bjetHiggsSide) {
	  hDeltaMinTauBTrue->Fill(deltaRMin, fEventWeight.getWeight());      
	  hPtBjetTauSideTrue->Fill(BjetTauSide->pt(), fEventWeight.getWeight());
	  hEtaBjetTauSideTrue->Fill(BjetTauSide->eta(), fEventWeight.getWeight());
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
	      //	      hBquarkFromTopSideEta->Fill(bEta, fEventWeight.getWeight());
	      //	      hBquarkFromTopSidePt->Fill(bPt, fEventWeight.getWeight());
	      // test with b jet from tau side
	      double deltaR = ROOT::Math::VectorUtil::DeltaR(BjetTopSide->p4(),p.p4() ); 
	      if ( deltaR < 0.4) bjetTopSide = true;
	    }
	  }
	}
	if(  bjetTopSide ) {
	  hDeltaMaxTopBTrue->Fill(deltaRMax, fEventWeight.getWeight());     
	  hPtBjetTopSideTrue->Fill(BjetTopSide->pt(), fEventWeight.getWeight());
	  hEtaBjetTopSideTrue->Fill(BjetTopSide->eta(), fEventWeight.getWeight());
	}
      } 

  
      if ( bquarkTopSide.size() == 1 && bjetMaxFound ) {
	double deltaR = ROOT::Math::VectorUtil::DeltaR(BjetMaxPt->p4() ,bquarkTopSide[0] );
	if (deltaR < 0.4) {
	  hPtBjetMaxTrue->Fill(BjetMaxPt->pt(), fEventWeight.getWeight());
	  hEtaBjetMaxTrue->Fill(BjetMaxPt->eta(), fEventWeight.getWeight());
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
	      hDeltaRHadTauBtauSide->Fill(deltaR, fEventWeight.getWeight());
	    }
	    if ( id * idHiggsSide < 0 ) {
	      double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	      hDeltaRHadTauBtopSide->Fill(deltaR, fEventWeight.getWeight());
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
      if (deltaRmax > 0 ) hDeltaRmaxFromTop->Fill(deltaRmax, fEventWeight.getWeight());      
    }


  
    passEvent = true; 
    if( !bjetTopSideFound) passEvent = false;   
    return Data(this, passEvent);
  }
  
}
