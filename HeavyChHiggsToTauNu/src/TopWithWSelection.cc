#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithWSelection.h"
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
  TopWithWSelection::Data::Data(const TopWithWSelection *topWithWSelection, bool passedEvent):
    fTopWithWSelection(topWithWSelection), fPassedEvent(passedEvent) {}
  TopWithWSelection::Data::~Data() {}

  TopWithWSelection::TopWithWSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fTopMassLow(iConfig.getUntrackedParameter<double>("TopMassLow")),
    fTopMassHigh(iConfig.getUntrackedParameter<double>("TopMassHigh")),
    fChi2Cut(iConfig.getUntrackedParameter<double>("Chi2Cut")),
    fTopWithWMassCount(eventCounter.addSubCounter("Top with W mass cut","Top with W Mass cut")),
    fEventWeight(eventWeight),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src"))
  {
    edm::Service<TFileService> fs;

    TFileDirectory myDir = fs->mkdir("TopWithWSelection");
    
    hPtTop = makeTH<TH1F>(myDir, "PtTop", "PtTop", 200, 0., 400.);
    hPtTopChiCut = makeTH<TH1F>(myDir, "PtTopChiCut", "PtTopChiCut", 200, 0., 400.);
    hjjMass = makeTH<TH1F>(myDir, "jjMass", "jjMass", 400, 0., 400.);
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

  TopWithWSelection::~TopWithWSelection() {}

  TopWithWSelection::Data TopWithWSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> iJetb) {


    // Reset variables
    topMass = -1;
    double nan = std::numeric_limits<double>::quiet_NaN();
    top.SetXYZT(nan, nan, nan, nan);
    W.SetXYZT(nan, nan, nan, nan);

    bool passEvent = false;

    bool wmassfound = false;
    bool topmassfound = false;
    double chi2Min = 999999;
    double nominalW = 80.4;
    double sigmaW = 11.;
  
    edm::Ptr<pat::Jet> Jet1;
    edm::Ptr<pat::Jet> Jet2;

    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet1 = *iter;


      for(edm::PtrVector<pat::Jet>::const_iterator iter2 = jets.begin(); iter2 != jets.end(); ++iter2) {
	edm::Ptr<pat::Jet> iJet2 = *iter2;

	if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJet2->p4()) < 0.4) continue;
	
	if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJetb->p4()) < 0.4) continue;
	if (ROOT::Math::VectorUtil::DeltaR(iJet2->p4(), iJetb->p4()) < 0.4) continue;	  
	
	XYZTLorentzVector candW = iJet1->p4() + iJet2->p4();
	
        
	hjjMass->Fill(candW.M(), fEventWeight.getWeight());
	double chi2 = ((candW.M() - nominalW)/sigmaW)*((candW.M() - nominalW)/sigmaW); 
	
	if (chi2 < chi2Min ) {
	  chi2Min = chi2;
	  Jet1 = iJet1;
	  Jet2 = iJet2;        
	  wmassfound = true;  
	  W = candW;          
	}
      }
    }

    if ( wmassfound ) {
      XYZTLorentzVector top = Jet1->p4() + Jet2->p4() + iJetb->p4(); 
      hWMass->Fill(W.M(), fEventWeight.getWeight());
      hChi2Min->Fill(sqrt(chi2Min), fEventWeight.getWeight());
      topMass = top.M();
      wMass = W.M();
      hPtTop->Fill(top.Pt(), fEventWeight.getWeight());
      htopMass->Fill(top.M(), fEventWeight.getWeight());
      if ( sqrt(chi2Min) < fChi2Cut) {
	topmassfound = true;
	htopMassChiCut->Fill(top.M(), fEventWeight.getWeight());
	hWMassChiCut->Fill(W.M(), fEventWeight.getWeight());
	hPtTopChiCut->Fill(top.Pt(), fEventWeight.getWeight());
      }
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
	    double deltaR = ROOT::Math::VectorUtil::DeltaR(iJetb->p4(),p.p4() );
	    if ( deltaR < 0.4) bMatchHiggsSide = true;
	  }
	  if ( id * idHiggsSide < 0 ) {
	    double deltaR = ROOT::Math::VectorUtil::DeltaR(iJetb->p4(),p.p4() );
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
	  //	  printImmediateMothers(p);
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
    increment(fTopWithWMassCount);
    
    return Data(this, passEvent);
  }    
}
