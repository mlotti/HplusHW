#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"

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
  TopSelection::Data::Data(const TopSelection *topSelection, bool passedEvent):
    fTopSelection(topSelection), fPassedEvent(passedEvent) {}
  TopSelection::Data::~Data() {}

  TopSelection::TopSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    fTopMassLow(iConfig.getUntrackedParameter<double>("TopMassLow")),
    fTopMassHigh(iConfig.getUntrackedParameter<double>("TopMassHigh")),
    fTopMassCount(eventCounter.addSubCounter("Top mass","Top Mass cut")),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src"))
  {
    edm::Service<TFileService> fs;

    TFileDirectory myDir = fs->mkdir("TopSelection");

    hPtjjb = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "Pt_jjb", "Pt_jjb", 160, 0., 800.);
    hPtmax = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "Ptmax", "Ptmax", 160, 0., 800.);
    hPtmaxMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "PtmaxMatch", "PtmaxMatch", 160, 0., 800.);
    hPtmaxBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "PtmaxBMatch", "PtmaxBMatch", 160, 0., 800.);
    hPtmaxQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "PtmaxQMatch", "PtmaxQMatch", 160, 0., 800.);
    hPtmaxMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "PtmaxMatchWrongB", "PtmaxMatchWrongB", 160, 0., 800.);

    hjjbMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "jjbMass", "jjbMass", 80, 0., 400.);
    htopMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "TopMass", "TopMass", 80, 0., 400.);
    hWMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "WMass", "WMass", 100, 0., 200.);
    htopMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TopMass_fullMatch", "TopMass_fullMatch", 80, 0., 400.);
    hWMassMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "WMass_fullMatch", "WMass_fullMatchMatch", 100, 0., 200.);
    htopMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TopMass_bMatch", "TopMass_bMatch", 80, 0., 400.);
    hWMassBMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "WMass_bMatch", "WMass_bMatch", 100, 0., 200.);
    htopMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TopMass_qMatch", "TopMass_qMatch", 80, 0., 400.);
    hWMassQMatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "WMass_qMatch", "WMass_qMatch", 100, 0., 200.);
    htopMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TopMass_MatchWrongB", "TopMass_MatchWrongB", 80, 0., 400.);
    hWMassMatchWrongB = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "WMass_MatchWrongB", "WMass_MatchWrongB", 100, 0., 200.);
  }

  TopSelection::~TopSelection() {}

  TopSelection::Data TopSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {
    // Reset variables
    topMass = -1;
    double nan = std::numeric_limits<double>::quiet_NaN();
    top.SetXYZT(nan, nan, nan, nan);
    W.SetXYZT(nan, nan, nan, nan);

    bool passEvent = false;

    double ptmax = 0;
   
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
	
	  hPtjjb->Fill(candTop.Pt());
	  hjjbMass->Fill(candTop.M());

	  if (candTop.Pt() > ptmax ) {
	    Jet1 = iJet1;
	    Jet2 = iJet2;
	    Jetb = iJetb;
	    ptmax = candTop.Pt();
            topMass = candTop.M();
            top = candTop;
	    W = candW; 
	  }
	}
      }
    }

    hPtmax->Fill(ptmax);
    htopMass->Fill(topMass);
    hWMass->Fill(W.M());



   
    // search correct combinations
    if (!iEvent.isRealData()  && ptmax > 0 ) {

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
	 hPtmaxMatch->Fill(ptmax);
       }
       if ( bMatchHiggsSide && Jet1Match && Jet2Match) {
	 htopMassMatchWrongB->Fill(top.M());
	 hWMassMatchWrongB->Fill(W.M()); 
	 hPtmaxMatchWrongB->Fill(ptmax);
       }
       if ( bMatchTopSide ) {
	 htopMassBMatch->Fill(top.M());
	 hWMassBMatch->Fill(W.M()); 
	 hPtmaxBMatch->Fill(ptmax);
       }
       if ( Jet1Match && Jet2Match ) {
	 htopMassQMatch->Fill(top.M());
	 hWMassQMatch->Fill(W.M());
	 hPtmaxQMatch->Fill(ptmax); 
       }
    }


    passEvent = true;
    if(topMass < fTopMassLow || topMass > fTopMassHigh ) passEvent = false;
    increment(fTopMassCount);
    
    return Data(this, passEvent);
  }
    
    
}
   


 
