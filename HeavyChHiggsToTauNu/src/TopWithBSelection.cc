#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopWithBSelection.h"
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
  TopWithBSelection::Data::Data(const TopWithBSelection *topWithBSelection, bool passedEvent):
    fTopWithBSelection(topWithBSelection), fPassedEvent(passedEvent) {}
  TopWithBSelection::Data::~Data() {}

  TopWithBSelection::TopWithBSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fTopMassLow(iConfig.getUntrackedParameter<double>("TopMassLow")),
    fTopMassHigh(iConfig.getUntrackedParameter<double>("TopMassHigh")),
    fChi2Cut(iConfig.getUntrackedParameter<double>("Chi2Cut")),
    fTopWithBMassCount(eventCounter.addSubCounter("Top with B mass cut","Top with B Mass cut")),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src"))
  {
    edm::Service<TFileService> fs;

    TFileDirectory myDir = fs->mkdir("TopWithBSelection");

    hPtTop = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "PtTop", "PtTop", 100, 0., 400.);
    hPtTopChiCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "PtTopChiCut", "PtTopChiCut", 100, 0., 400.);
    hjjbMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "jjbMass", "jjbMass", 80, 0., 400);
    htopMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass", "TopMass", 80, 0., 400);
    hWMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass", "WMass", 100, 0., 200.);
    htopMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TopMass_fullMatch", "TopMass_fullMatch", 80, 0., 400);
    hWMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "WMass_fullMatch", "WMass_fullMatchMatch", 100, 0., 200.);
    htopMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TopMass_bMatch", "TopMass_bMatch", 80, 0., 400);
    hWMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "WMass_bMatch", "WMass_bMatch", 100, 0., 200.);
    htopMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TopMass_qMatch", "TopMass_qMatch", 80, 0., 400);
    hWMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "WMass_qMatch", "WMass_qMatch", 100, 0., 200.);
    htopMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TopMass_MatchWrongB", "TopMass_MatchWrongB", 80, 0., 400);
    hWMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "WMass_MatchWrongB", "WMass_MatchWrongB", 100, 0., 200.);
    hChi2Min = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "Chi2Min", "Chi2Min", 200, 0., 40.);
    htopMassChiCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMassChiCut", "TopMassChiCut", 80, 0., 400);
    hWMassChiCut = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMassChiCut", "WMassChiCut", 100, 0., 200.);
  }

  TopWithBSelection::~TopWithBSelection() {}

  TopWithBSelection::Data TopWithBSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> iJetb) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, jets, iJetb);
  }

  TopWithBSelection::Data TopWithBSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> iJetb) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, jets, iJetb);
  }

  TopWithBSelection::Data TopWithBSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<pat::Jet> iJetb) {
    // Reset variables
    topMass = -1;
    double nan = std::numeric_limits<double>::quiet_NaN();
    top.SetXYZT(nan, nan, nan, nan);
    W.SetXYZT(nan, nan, nan, nan);

    bool passEvent = false;

    bool topmassfound = false;
    double chi2Min = 999999;
    double nominalTop = 172.9;
    double nominalW = 80.4;
    double sigmaTop = 18.;
    double sigmaW = 11.;
  
    edm::Ptr<pat::Jet> Jet1;
    edm::Ptr<pat::Jet> Jet2;
    edm::Ptr<pat::Jet> Jetb;

    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet1 = *iter;


      for(edm::PtrVector<pat::Jet>::const_iterator iter2 = jets.begin(); iter2 != jets.end(); ++iter2) {
	edm::Ptr<pat::Jet> iJet2 = *iter2;

	if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJet2->p4()) < 0.4) continue;
	
	if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJetb->p4()) < 0.4) continue;
	if (ROOT::Math::VectorUtil::DeltaR(iJet2->p4(), iJetb->p4()) < 0.4) continue;	  
	
	XYZTLorentzVector candTop = iJet1->p4() + iJet2->p4() + iJetb->p4();
	XYZTLorentzVector candW = iJet1->p4() + iJet2->p4();
	
        
	hjjbMass->Fill(candTop.M());
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
 
  
    hPtTop->Fill(top.Pt());
    htopMass->Fill(top.M());
    hWMass->Fill(W.M());
    hChi2Min->Fill(sqrt(chi2Min));
    if ( sqrt(chi2Min) < fChi2Cut) {
      htopMassChiCut->Fill(top.M());
      hWMassChiCut->Fill(W.M());
      hPtTopChiCut->Fill(top.Pt());
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
	  //	  printImmediateMothers(p);
	  double deltaR1 = ROOT::Math::VectorUtil::DeltaR(Jet1->p4(),p.p4() );
	  if ( deltaR1 < 0.4) Jet1Match = true;
	  double deltaR2 = ROOT::Math::VectorUtil::DeltaR(Jet2->p4(),p.p4() );
	  if ( deltaR2 < 0.4) Jet2Match = true;
	  
	}
      }

      

       if ( bMatchTopSide && Jet1Match && Jet2Match) {
	 htopMassMatch->Fill(top.M());
	 hWMassMatch->Fill(W.M()); 
       }
       if ( bMatchHiggsSide && Jet1Match && Jet2Match) {
	 htopMassMatchWrongB->Fill(top.M());
	 hWMassMatchWrongB->Fill(W.M()); 
       }
       if ( bMatchTopSide ) {
	 htopMassBMatch->Fill(top.M());
	 hWMassBMatch->Fill(W.M()); 
       }
       if ( Jet1Match && Jet2Match ) {
	 htopMassQMatch->Fill(top.M());
	 hWMassQMatch->Fill(W.M()); 
       }
    }

    
    passEvent = true;
    if( topMass < fTopMassLow || topMass > fTopMassHigh ) passEvent = false;
    increment(fTopWithBMassCount);
    
    return Data(this, passEvent);
  }    
}
