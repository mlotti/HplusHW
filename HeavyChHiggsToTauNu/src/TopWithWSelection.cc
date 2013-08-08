#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithWSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"
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
/*  TopWithWSelection::Data::Data():
    fPassedEvent(false) {}
  TopWithWSelection::Data::~Data() {} */

  //constructor
  TopWithWSelection::TopWithWSelection(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper) : TopSelectionBase::TopSelectionBase(iConfig, eventCounter, histoWrapper),
    //BaseSelection(eventCounter, histoWrapper),
    fTopMassLow(iConfig.getUntrackedParameter<double>("TopMassLow")),
    fTopMassHigh(iConfig.getUntrackedParameter<double>("TopMassHigh")),
    fChi2Cut(iConfig.getUntrackedParameter<double>("Chi2Cut")),
    fTopWithWMassCount(eventCounter.addSubCounter("Top with W mass cut","Top with W Mass cut")),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src"))
  {
    edm::Service<TFileService> fs;

    TFileDirectory myDir = fs->mkdir("TopWithWSelection");
    
    hPtTop = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtTop", "PtTop", 80, 0., 400);
    hPtTopChiCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "PtTopChiCut", "PtTopChiCut", 80, 0., 400);
    hjjMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jjMass", "jjMass", 80, 0., 400);
    htopMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass", "TopMass", 80, 0., 400);
    hWMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass", "WMass", 100, 0., 200.);
    htopMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass_fullMatch", "TopMass_fullMatch", 80, 0., 400);
    hWMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMass_fullMatch", "WMass_fullMatchMatch", 100, 0., 200.);
    htopMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass_bMatch", "TopMass_bMatch", 80, 0., 400);
    hWMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMass_bMatch", "WMass_bMatch", 100, 0., 200.);
    htopMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass_qMatch", "TopMass_qMatch", 80, 0., 400);
    hWMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMass_qMatch", "WMass_qMatch", 100, 0., 200.);
    htopMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass_MatchWrongB", "TopMass_MatchWrongB", 80, 0., 400);
    hWMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMass_MatchWrongB", "WMass_MatchWrongB", 100, 0., 200.);
    hChi2Min = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Chi2Min", "Chi2Min", 200, 0., 40.);
    htopMassChiCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMassChiCut", "TopMassChiCut", 80, 0., 400);
    hWMassChiCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMassChiCut", "WMassChiCut", 100, 0., 200.);
  }

  //destructor
  TopWithWSelection::~TopWithWSelection() {}

/*  TopWithWSelection::Data TopWithWSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> iJetb) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, jets, iJetb);
  }

  TopWithWSelection::Data TopWithWSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> iJetb) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, jets, iJetb);
  } */

  TopWithWSelection::Data TopWithWSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> iJetb) { 
    Data output;

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
	
	hjjMass->Fill(candW.M());
	double chi2 = ((candW.M() - nominalW)/sigmaW)*((candW.M() - nominalW)/sigmaW); 
	
	if (chi2 < chi2Min ) {
	  chi2Min = chi2;
	  Jet1 = iJet1;
	  Jet2 = iJet2;        
	  wmassfound = true;  
	  output.W = candW;          
	}
      }
    }

    if ( wmassfound ) {
      output.top = Jet1->p4() + Jet2->p4() + iJetb->p4(); 
      hWMass->Fill(output.getWMass());
      hChi2Min->Fill(sqrt(chi2Min));
      hPtTop->Fill(output.top.Pt());
      htopMass->Fill(output.getTopMass());
      if ( sqrt(chi2Min) < fChi2Cut) {
	topmassfound = true;
	htopMassChiCut->Fill(output.getTopMass());
	hWMassChiCut->Fill(output.getWMass());
	hPtTopChiCut->Fill(output.top.Pt());
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
	 htopMassMatch->Fill(output.getTopMass());
	 hWMassMatch->Fill(output.getWMass()); 
       }
       if ( bMatchHiggsSide && Jet1Match && Jet2Match) {
	 htopMassMatchWrongB->Fill(output.getTopMass());
	 hWMassMatchWrongB->Fill(output.getWMass()); 
       }
       if ( bMatchTopSide ) {
	 htopMassBMatch->Fill(output.getTopMass());
	 hWMassBMatch->Fill(output.getWMass()); 
       }
       if ( Jet1Match && Jet2Match ) {
	 htopMassQMatch->Fill(output.getTopMass());
	 hWMassQMatch->Fill(output.getWMass()); 
       }
    }

    if( output.getTopMass() < fTopMassLow || output.getTopMass() > fTopMassHigh ) {
      output.fPassedEvent = false;
    } else {
      output.fPassedEvent = true;
      increment(fTopWithWMassCount);
    }
    return output;
  }
}
