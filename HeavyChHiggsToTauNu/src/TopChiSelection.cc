#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BjetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"
#include "TLorentzVector.h"
#include "TVector3.h"
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
  TopChiSelection::Data::Data(const TopChiSelection *topChiSelection, bool passedEvent):
    fTopChiSelection(topChiSelection), fPassedEvent(passedEvent) {}
  TopChiSelection::Data::~Data() {}

  TopChiSelection::TopChiSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fTopMassLow(iConfig.getUntrackedParameter<double>("TopMassLow")),
    fTopMassHigh(iConfig.getUntrackedParameter<double>("TopMassHigh")),
    fChi2Cut(iConfig.getUntrackedParameter<double>("Chi2Cut")),
    fTopChiMassCount(eventCounter.addSubCounter("Top Chi mass cut","Top Chi Mass cut")),
    fEventWeight(eventWeight),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src"))
  {
    edm::Service<TFileService> fs;

    TFileDirectory myDir = fs->mkdir("TopChiSelection");
    
    hPtTop = makeTH<TH1F>(myDir, "PtTop", "PtTop", 200, 0., 400.);
    hPtTopChiCut = makeTH<TH1F>(myDir, "PtTopChiCut", "PtTopChiCut", 200, 0., 400.);
    hjjbMass = makeTH<TH1F>(myDir, "jjbMass", "jjbMass", 400, 0., 400.);
    htopMass = makeTH<TH1F>(myDir, "TopMass", "TopMass", 400, 0., 400.);
    hWMass = makeTH<TH1F>(myDir, "WMass", "WMass", 400, 0., 200.);
    htopMassMatch = makeTH<TH1F>(myDir, "TopMass_fullMatch", "TopMass_fullMatch", 400, 0., 400.);
    hWMassMatch = makeTH<TH1F>(myDir, "WMass_fullMatch", "WMass_fullMatchMatch", 400, 0., 200.);
    htopMassBMatch = makeTH<TH1F>(myDir, "TopMass_bMatch", "TopMass_bMatch", 400, 0., 400.);
    hWMassBMatch = makeTH<TH1F>(myDir, "WMass_bMatch", "WMass_bMatch", 400, 0., 200.);
    htopMassQMatch = makeTH<TH1F>(myDir, "TopMass_qMatch", "TopMass_qMatch", 400, 0., 400.);
    hWMassQMatch = makeTH<TH1F>(myDir, "WMass_qMatch", "WMass_qMatch", 400, 0., 200.);
    htopMassMatchWrongB = makeTH<TH1F>(myDir, "TopMass_MatchWrongB", "TopMass_MatchWrongB", 400, 0., 400.);
    hWMassMatchWrongB = makeTH<TH1F>(myDir, "WMass_MatchWrongB", "WMass_MatchWrongB", 400, 0., 200.);
    hChi2Min = makeTH<TH1F>(myDir, "Chi2Min", "Chi2Min", 200, 0., 40.);
    htopMassChiCut = makeTH<TH1F>(myDir, "TopMassChiCut", "TopMassChiCut", 400, 0., 400.);
    hWMassChiCut = makeTH<TH1F>(myDir, "WMassChiCut", "WMassChiCut", 400, 0., 200.);
  }

  TopChiSelection::~TopChiSelection() {}

  TopChiSelection::Data TopChiSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {


    // Reset variables
    topMass = -1;
    double nan = std::numeric_limits<double>::quiet_NaN();
    top.SetXYZT(nan, nan, nan, nan);
    W.SetXYZT(nan, nan, nan, nan);

    bool passEvent = false;
    size_t passed = 0;

    double chi2Min = 999999;
    double nominalTop = 172.9;
    double nominalW = 80.4;
    double sigmaTop = 18.;
    double sigmaW = 12.;
    bool topmassfound = false;

    edm::Ptr<pat::Jet> Jet1;
    edm::Ptr<pat::Jet> Jet2;
    edm::Ptr<pat::Jet> Jetb;

    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet1 = *iter;


      for(edm::PtrVector<pat::Jet>::const_iterator iter2 = jets.begin(); iter2 != jets.end(); ++iter2) {
	edm::Ptr<pat::Jet> iJet2 = *iter2;

	if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJet2->p4()) < 0.4) continue;

	for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjets.begin(); iterb != bjets.end(); ++iterb) {
	  edm::Ptr<pat::Jet> iJetb = *iterb;
	  if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJetb->p4()) < 0.4) continue;
	  if (ROOT::Math::VectorUtil::DeltaR(iJet2->p4(), iJetb->p4()) < 0.4) continue;	  

	  XYZTLorentzVector candTop = iJet1->p4() + iJet2->p4() + iJetb->p4();
          XYZTLorentzVector candW = iJet1->p4() + iJet2->p4();

        
	  hjjbMass->Fill(candTop.M(), fEventWeight.getWeight());
	  double chi2 = ((candTop.M() - nominalTop)/sigmaTop)*((candTop.M() - nominalTop)/sigmaTop) + ((candW.M() - nominalW)/sigmaW)*((candW.M() - nominalW)/sigmaW); 

	  if (chi2 < chi2Min ) {
	    chi2Min = chi2;
	    Jet1 = iJet1;
	    Jet2 = iJet2;
	    Jetb = iJetb;            
            top = candTop;
	    W = candW;
	    topmassfound = true;
 	  }
	}
      }
    }
  
    hPtTop->Fill(top.Pt(), fEventWeight.getWeight());
    htopMass->Fill(top.M(), fEventWeight.getWeight());
    hWMass->Fill(W.M(), fEventWeight.getWeight());
    hChi2Min->Fill(sqrt(chi2Min), fEventWeight.getWeight());
    if ( sqrt(chi2Min) < fChi2Cut) {
      htopMassChiCut->Fill(top.M(), fEventWeight.getWeight());
      hWMassChiCut->Fill(W.M(), fEventWeight.getWeight());
      hPtTopChiCut->Fill(top.Pt(), fEventWeight.getWeight());
      topMass = top.M();
      wMass = W.M();
    }


    
    // search correct combinations
    //    if (!iEvent.isRealData() && chi2Min < fChi2Cut ) {
    if (!iEvent.isRealData() && topmassfound ) {
      edm::Handle <reco::GenParticleCollection> genParticles;
      iEvent.getByLabel(fSrc, genParticles);

      int idHiggsSide = 0;
      for (size_t i=0; i < genParticles->size(); ++i){
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	if(abs(id) == 6 && (hasImmediateDaughter(p,37) || hasImmediateDaughter(p,-37))) {
	  idHiggsSide = id;
	}
      }
       bool bMatchHiggsSide = false;
       bool bMatchTopSide = false;
       bool Jet1Match = false;
       bool Jet2Match = false;
     
      for (size_t i=0; i < genParticles->size(); ++i){
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	if ( abs(id) != 5 || hasImmediateMother(p,5) || hasImmediateMother(p,-5) )continue;
	if(hasImmediateMother(p,6) || hasImmediateMother(p,-6)) {
	  //	  printImmediateMothers(p);
	  //	  std::cout << " b quarks " << id <<  " idHiggsSide " <<   idHiggsSide << std::endl;
	  if ( id * idHiggsSide > 0 ) {
	    // test with b jet to tau side
	    double deltaR = ROOT::Math::VectorUtil::DeltaR(Jetb->p4(),p.p4() );
	    if ( deltaR < 0.4) bMatchHiggsSide = true;
	  }
	  if ( id * idHiggsSide < 0 ) {
	    // test with b jet to top side
	    double deltaR = ROOT::Math::VectorUtil::DeltaR(Jetb->p4(),p.p4() );
	    if ( deltaR < 0.4) bMatchTopSide = true;
	  }
	}
      } 
      
      
      for (size_t i=0; i < genParticles->size(); ++i){
	const reco::Candidate & p = (*genParticles)[i];
	int id = p.pdgId();
	if ( abs(id) > 4  )continue;
	if ( hasImmediateMother(p,1) || hasImmediateMother(p,-1) )continue;
	if ( hasImmediateMother(p,2) || hasImmediateMother(p,-2) )continue;
	if ( hasImmediateMother(p,3) || hasImmediateMother(p,-3) )continue;
	if ( hasImmediateMother(p,4) || hasImmediateMother(p,-4) )continue;

	if(hasImmediateMother(p,24) || hasImmediateMother(p,-24)) {
	  double deltaR1 = ROOT::Math::VectorUtil::DeltaR(Jet1->p4(),p.p4() );
	  if ( deltaR1 < 0.4) Jet1Match = true;
	  double deltaR2 = ROOT::Math::VectorUtil::DeltaR(Jet2->p4(),p.p4() );
	  if ( deltaR2 < 0.4) Jet2Match = true;
	  
	}
      }

      

       if ( bMatchTopSide && Jet1Match && Jet2Match) {
	 htopMassMatch->Fill(top.M(), fEventWeight.getWeight());
	 hWMassMatch->Fill(W.M(), fEventWeight.getWeight()); 
       }
       if ( bMatchHiggsSide && Jet1Match && Jet2Match) {
	 htopMassMatchWrongB->Fill(top.M(), fEventWeight.getWeight());
	 hWMassMatchWrongB->Fill(W.M(), fEventWeight.getWeight()); 
       }
       if ( bMatchTopSide ) {
	 htopMassBMatch->Fill(top.M(), fEventWeight.getWeight());
	 hWMassBMatch->Fill(W.M(), fEventWeight.getWeight()); 
       }
       if ( Jet1Match && Jet2Match ) {
	 htopMassQMatch->Fill(top.M(), fEventWeight.getWeight());
	 hWMassQMatch->Fill(W.M(), fEventWeight.getWeight()); 
       }
    }

    
    passEvent = true;
    if( topMass < fTopMassLow || topMass > fTopMassHigh ) passEvent = false;
    increment(fTopChiMassCount);
    
    return Data(this, passEvent);
  }



  /*  
      std::vector<const reco::GenParticle*>   TopChiSelection::getImmediateMothers(const reco::Candidate& p){ 
	std::vector<const reco::GenParticle*> mothers;
	for (size_t im=0; im < p.numberOfMothers(); ++im){
	  const reco::GenParticle* mparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
	  if (mparticle) mothers.push_back(mparticle);
	}
	return mothers;
      }
      
      std::vector<const reco::GenParticle*>   TopChiSelection::getMothers(const reco::Candidate& p){ 
	std::vector<const reco::GenParticle*> mothers;
	for (size_t im=0; im < p.numberOfMothers(); ++im){
	  const reco::GenParticle* mparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
	  if (mparticle) { 
	    mothers.push_back(mparticle);
	    std::vector<const reco::GenParticle*> mmothers = getMothers( * (dynamic_cast<const reco::Candidate*> (mparticle)) );
	    mothers.insert(mothers.end(), mmothers.begin(), mmothers.end()); 
	  }
	}
	return mothers;
      }
      
      bool  TopChiSelection::hasImmediateMother(const reco::Candidate& p, int id){
	std::vector<const reco::GenParticle*> mothers = getImmediateMothers(p);
	for (size_t im=0; im < mothers.size(); ++im){
	  if (mothers[im]->pdgId() == id) return true;
	}
	return false;
      }  
      
      bool  TopChiSelection::hasMother(const reco::Candidate& p, int id){
	std::vector<const reco::GenParticle*> mothers = getMothers(p);
	for (size_t im=0; im < mothers.size(); ++im){
	  if (mothers[im]->pdgId() == id) return true;
	}
	return false;
      } 
 
     void  TopChiSelection::printImmediateMothers(const reco::Candidate& p){
	std::vector<const reco::GenParticle*> mothers = getImmediateMothers(p);
	std::cout << "Immediate mothers of " << p.pdgId() << ":" << std::endl;
	for (size_t im=0; im < mothers.size(); ++im){
	  std::cout << "  " << mothers[im]->pdgId() << std::endl;
	}
	std::cout << std::endl;
      }  
      
      void  TopChiSelection::printMothers(const reco::Candidate& p){
	std::vector<const reco::GenParticle*> mothers = getMothers(p);
	std::cout << "Mothers of " << p.pdgId() << ":" << std::endl;
	for (size_t im=0; im < mothers.size(); ++im){
	  std::cout << "  " << mothers[im]->pdgId() << std::endl;
	}
	std::cout << std::endl;
      }  
      std::vector<const reco::GenParticle*>  TopChiSelection::getImmediateDaughters(const reco::Candidate& p){ 
	std::vector<const reco::GenParticle*> daughters;
	for (size_t im=0; im < p.numberOfDaughters(); ++im){
	  const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.daughter(im));
	  if (dparticle) daughters.push_back(dparticle);
	}
	return daughters;
      }
      
      std::vector<const reco::GenParticle*>   TopChiSelection::getDaughters(const reco::Candidate& p){ 
	std::vector<const reco::GenParticle*> daughters;
	for (size_t im=0; im < p.numberOfDaughters(); ++im){
	  const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.daughter(im));
	  if (dparticle) {
	    daughters.push_back(dparticle);
	    std::vector<const reco::GenParticle*> ddaughters = getDaughters( * (dynamic_cast<const reco::Candidate*> (dparticle)) );
	    daughters.insert(daughters.end(), ddaughters.begin(), ddaughters.end()); 
	  }
	}
	return daughters;
      }
      
      bool  TopChiSelection::hasImmediateDaughter(const reco::Candidate& p, int id){
	std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(p);
	for (size_t im=0; im < daughters.size(); ++im){
	  if (daughters[im]->pdgId() == id) return true;
	}
	return false;
      }
      bool  TopChiSelection::hasDaughter(const reco::Candidate& p, int id){
	std::vector<const reco::GenParticle*> daughters = getDaughters(p);
	for (size_t im=0; im < daughters.size(); ++im){
	  if (daughters[im]->pdgId() == id) return true;
	}
	return false;
      }
      
      void  TopChiSelection::printImmediateDaughters(const reco::Candidate& p){
	std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(p);
	std::cout << "Immediate daughters of " << p.pdgId() << ":" << std::endl;
	for (size_t im=0; im < daughters.size(); ++im){
	  std::cout << "  " << daughters[im]->pdgId() << std::endl;
	}
	std::cout << std::endl;
      }  
      
      void  TopChiSelection::printDaughters(const reco::Candidate& p){
	std::vector<const reco::GenParticle*> daughters = getDaughters(p);
	std::cout << "Daughters of " << p.pdgId() << ":" << std::endl;
	for (size_t im=0; im < daughters.size(); ++im){
	  std::cout << "  " << daughters[im]->pdgId() << std::endl;
	}
	std::cout << std::endl;
      }  
  */    
}
