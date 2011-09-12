#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"

#include <limits>

namespace HPlus {
  TopSelection::Data::Data(const TopSelection *topSelection, bool passedEvent):
    fTopSelection(topSelection), fPassedEvent(passedEvent) {}
  TopSelection::Data::~Data() {}

  TopSelection::TopSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fTopMassLow(iConfig.getUntrackedParameter<double>("TopMassLow")),
    fTopMassHigh(iConfig.getUntrackedParameter<double>("TopMassHigh")),
    fTopMassCount(eventCounter.addSubCounter("Top mass","Top Mass cut")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;

    TFileDirectory myDir = fs->mkdir("TopSelection");
    
    hPtjjb = makeTH<TH1F>(myDir, "Pt_jjb", "Pt_jjb", 400, 0., 800.);
    hPtmax = makeTH<TH1F>(myDir, "Pt_jjbmax", "Pt_jjbmax", 400, 0., 800.);
    hPtmaxTop = makeTH<TH1F>(myDir, "Pt_top", "Pt_top", 400, 0., 800.);
    hPtmaxTopReal = makeTH<TH1F>(myDir, "Pt_topReal", "Pt_topReal", 400, 0., 800.);
    hPtmaxTopHplus = makeTH<TH1F>(myDir, "Pt_topHplus", "Pt_topHplus", 400, 0., 800.);
    hjjbMass = makeTH<TH1F>(myDir, "jjbMass", "jjbMass", 400, 0., 800.);
    htopMass = makeTH<TH1F>(myDir, "Mass_jjbMax", "Mass_jjbMax", 400, 0., 800.);
    htopMassReal = makeTH<TH1F>(myDir, "Mass_Top", "Mass_Top", 400, 0., 800.);
    htopMassMaxReal = makeTH<TH1F>(myDir, "MassMax_Top", "MassMax_Top", 400, 0., 800.);
    htopMassRealb = makeTH<TH1F>(myDir, "Mass_bFromTop", "Mass_bFromTop", 400, 0., 800.);
    htopMassRealHplus = makeTH<TH1F>(myDir, "Mass_TopHplus", "Mass_TopHplus", 400, 0., 800.);
  }

  TopSelection::~TopSelection() {}

  TopSelection::Data TopSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {
    // Reset variables
    topMass = -1;
    double nan = std::numeric_limits<double>::quiet_NaN();
    top.SetXYZT(nan, nan, nan, nan);

    bool passEvent = false;
    size_t passed = 0;

    double ptmax = 0;
    double ptjjb = 0;
    bool correctCombination = false;
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

          XYZTLorentzVector cand = iJet1->p4() + iJet2->p4() + iJetb->p4();
	
	  hPtjjb->Fill(cand.Pt(), fEventWeight.getWeight());
	  hjjbMass->Fill(cand.M(), fEventWeight.getWeight());

	  if (cand.Pt() > ptmax ) {
	    Jet1 = iJet1;
	    Jet2 = iJet2;
	    Jetb = iJetb;
	    ptmax = cand.Pt();
            topMass = cand.M();
            top = cand;
	  }
	}
      }
    }
    hPtmax->Fill(ptmax, fEventWeight.getWeight());
    htopMass->Fill(topMass, fEventWeight.getWeight());

    // real top in all combinations
    if (!iEvent.isRealData()) {
      
      bool bFromTop = false;
      bool q1FromTop = false;
      bool q2FromTop = false;
      int q1Top = 0;
      int q2Top = 0;
      int bTop = 0;
      
      int q1mother = 999999;
      if( ptmax > 0 ) {
	
	const reco::GenParticle* q1particle =  Jet1->genParticle();
	if ( q1particle) {
	  //	  if (abs(q1particle->pdgId()) < 5 && q1particle->status() == 2) {
	  if (abs(q1particle->pdgId()) < 5 ) {
	    int numberOfq1Mothers = q1particle->numberOfMothers();
	    for (int im2=0; im2 < numberOfq1Mothers; ++im2){
	      const reco::GenParticle* m1particle = dynamic_cast<const reco::GenParticle*>(q1particle->mother(im2));
	      if ( !m1particle) continue;
	      q1mother = m1particle->pdgId();
	      //		if (abs(q1mother) == 24 ) q1FromTop = true;
	      if (abs(q1mother) == 24 ) {
		q1FromTop = true;
		q1Top = q1mother;
	      }
	    }
	  }
	}
	//	std::cout << " q1FromTop " << q1FromTop << " q1Top " << q1Top << std::endl;

	int q2mother = -999999;
	const reco::GenParticle* q2particle =  Jet2->genParticle();
	if ( q2particle) {
	  //	  if (abs(q2particle->pdgId()) < 5 && q2particle->status() == 2 ) {
	  if (abs(q2particle->pdgId()) < 5 ) {
	    int numberOfq2Mothers = q2particle->numberOfMothers();
	    for (int im3=0; im3 < numberOfq2Mothers; ++im3){
	      const reco::GenParticle* m2particle = dynamic_cast<const reco::GenParticle*>(q2particle->mother(im3));
	      if ( !m2particle) continue;
	      q2mother = m2particle->pdgId();
	      //		if (abs(q1mother) == 24 ) q2FromTop = true;
	      if (abs(q2mother) == 24 ) {
		q2FromTop = true;
		q2Top = q2mother;
	      }
	    }												 
	  }
	}
	  //	  if( abs(q1mother) == 24 && abs(q2mother) == 24 &&  (q1mother == q2mother)) {	    
	  //  q1FromTop = true;
	  //  q2FromTop = true;
	  // }
	
	
	int bmother = 99999;
	const reco::GenParticle* bparticle =  Jetb->genParticle();
	if ( bparticle) {
	  //	  if (abs(bparticle->pdgId()) == 5 && bparticle->status() == 2 ) {
	  if (abs(bparticle->pdgId()) == 5 ) {
	    int numberOfbMothers = bparticle->numberOfMothers();
	    for (int im=0; im < numberOfbMothers; ++im){
	      const reco::GenParticle* mparticle = dynamic_cast<const reco::GenParticle*>(bparticle->mother(im));
	      if ( !mparticle) continue;
	      bmother = mparticle->pdgId();
	      //		if ( abs(bmother) == 6 ) bFromTop = true;
	      if (abs(bmother) == 6 ) {
		bFromTop = true;
		bTop = bmother;
	      }
	    }
	  }
	}
	//	std::cout << " bFromTop " << bFromTop << " bTop " << bTop << std::endl;

	//	  if( abs(bmother) == 6 &&  (q1mother * bmother) > 0 ) {	    
	//  bFromTop = true;
	// }
	if (bFromTop && q1FromTop  && q2FromTop && (q1Top == q2Top)  && (q1Top * bTop) > 0  ) {
	  correctCombination = true;
	  hPtmaxTop->Fill(ptjjb, fEventWeight.getWeight());
	  htopMassReal->Fill(topMass, fEventWeight.getWeight());
	}
	//	  if (q1FromTop && q2FromTop && abs(bmother) == 6 && (q1mother * bmother) < 0 ) {
	if (bFromTop && q1FromTop  && q2FromTop && (q1Top == q2Top)  && (q1Top * bTop)<0  ) {
	  hPtmaxTopHplus->Fill(ptjjb, fEventWeight.getWeight());
	  htopMassRealHplus->Fill(topMass, fEventWeight.getWeight());
	}
	if (bFromTop ) htopMassRealb->Fill(topMass, fEventWeight.getWeight());
      }
      
  
      if ( correctCombination ) {
	hPtmaxTopReal->Fill(ptmax, fEventWeight.getWeight());
	htopMassMaxReal->Fill(topMass, fEventWeight.getWeight());
      }
      //    if (bFromTop ) htopMassRealb->Fill(topMass, fEventWeight.getWeight());
    }
    
    
    passEvent = true;
    if(topMass < fTopMassLow || topMass > fTopMassHigh ) passEvent = false;
    increment(fTopMassCount);
    
    return Data(this, passEvent);
  }
}
