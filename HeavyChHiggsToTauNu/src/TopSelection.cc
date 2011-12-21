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
    //    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
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
      bool q1FromW = false;
      bool q2FromW = false;
      int q1Mother = 0;
      int q2Mother = 0;
      int bMother = 0;
   
      edm::Handle <reco::GenParticleCollection> genParticles;
      iEvent.getByLabel(fSrc, genParticles);

     
      int q1mother = 999999;
      if( ptmax > 0 ) {
	
	const reco::GenParticle* q1particle =  Jet1->genParticle();
	if ( q1particle) {
	  //	  if (abs(q1particle->pdgId()) < 5 && q1particle->status() == 2) {
	  if (abs(q1particle->pdgId()) < 5 ) {
	    int numberOfq1Mothers = q1particle->numberOfMothers();
	    if (numberOfq1Mothers > 0 ) {
	      for (int im2=0; im2 < numberOfq1Mothers; ++im2){
		const reco::GenParticle* m1particle = dynamic_cast<const reco::GenParticle*>(q1particle->mother(im2));
		if ( !m1particle) continue;
		q1mother = m1particle->pdgId();
		//		if (abs(q1mother) == 24 ) q1FromTop = true;
		if (abs(q1mother) == 24 ) {
		  q1FromW = true;
		  q1Mother = q1mother;
		  //		  std::cout << " q1particle->pdgId() " << q1particle->pdgId() << std::endl;
		}
	      }
	    }
	  }
	}
	//      	std::cout << " q1mother " << q1mother << " q1FromW " << q1FromW << std::endl;

	if ( false) {
      bool bFromTop = false;
      bool q1FromW = false;
      bool q2FromW = false;
      int q1Mother = 0;
      int q2Mother = 0;
      int bMother = 0;

	for (size_t i=0; i < genParticles->size(); ++i){
	  const reco::Candidate & p = (*genParticles)[i];
	  int id = p.pdgId();
	  if ( abs(id) != 24 ) continue;
	  bool hasDaughter = false;
	  // Check whether the genParticle decays to itself. If yes do not consider in counting
	  if ( p.numberOfDaughters() != 0 ){
	    // Loop over all 1st daughters of genParticle
	    for(size_t j = 0; j < p.numberOfDaughters() ; ++ j) {
	      const reco::Candidate *d = p.daughter( j );

	      if( p.pdgId() == d->pdgId() ) hasDaughter = true;
	      if ( p.pdgId() < 5 ) {
		  q1FromW = true;
		  q1Mother = id;
	      } 
	    }
	  }
	}
	std::cout << " q1mother " << q1mother << " q1FromW " << q1FromW << std::endl;
	}


	int q2mother = -999999;
	const reco::GenParticle* q2particle =  Jet2->genParticle();
	if ( q2particle) {
	  //	  if (abs(q2particle->pdgId()) < 5 && q2particle->status() == 2 ) {
	  if (abs(q2particle->pdgId()) < 5 ) {
	    int numberOfq2Mothers = q2particle->numberOfMothers();
	    if (numberOfq2Mothers > 0 ) {
	      for (int im3=0; im3 < numberOfq2Mothers; ++im3){
		const reco::GenParticle* m2particle = dynamic_cast<const reco::GenParticle*>(q2particle->mother(im3));
		if ( !m2particle) continue;
		q2mother = m2particle->pdgId();
		//		if (abs(q1mother) == 24 ) q2FromTop = true;
		if (abs(q2mother) == 24 ) {
		  q2FromW = true;
		  q2Mother = q2mother;
		  //		  std::cout << " q2particle->pdgId() " << q2particle->pdgId() << std::endl;
		}
	      }												 
	    }
	  }
	}
	//       	if ( q2particle) std::cout << " q2mother " << q2mother << "  q1mother " <<  q1mother  << std::endl;
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
	    if (numberOfbMothers > 0 ) {
	      for (int im=0; im < numberOfbMothers; ++im){
		const reco::GenParticle* mparticle = dynamic_cast<const reco::GenParticle*>(bparticle->mother(im));
		if ( !mparticle) continue;
		bmother = mparticle->pdgId();
		//		if ( abs(bmother) == 6 ) bFromTop = true;
		if (abs(bmother) == 6 ) {
		  bFromTop = true;
		  bMother = bmother;
		  //		  std::cout << " bparticle->pdgId() " << bparticle->pdgId() << std::endl;
		}
	      }
	    }
	  }
	}
	//	std::cout << " bFromTop " << bFromTop << " q1FromW " << q1FromW << " q2FromW " << q2FromW << " bmother " <<  bMother << " q2mother " << q2Mother << std::endl;

	//	  if( abs(bmother) == 6 &&  (q1mother * bmother) > 0 ) {	    
	//  bFromTop = true;
	// }
	if (bFromTop && q1FromW  && q2FromW && (q1Mother == q2Mother)  && (q1Mother * bMother) > 0  ) {
	  correctCombination = true;
	  hPtmaxTop->Fill(ptjjb, fEventWeight.getWeight());
	  htopMassReal->Fill(topMass, fEventWeight.getWeight());
	  //	  std::cout << " correctCombination " << std::endl;
	}
	//	  if (q1FromTop && q2FromTop && abs(bmother) == 6 && (q1mother * bmother) < 0 ) {
	if (bFromTop && q1FromW  && q2FromW && (q1Mother == q2Mother)  && (q1Mother * bMother)<0  ) {
	  hPtmaxTopHplus->Fill(ptjjb, fEventWeight.getWeight());
	  htopMassRealHplus->Fill(topMass, fEventWeight.getWeight());
	  //	  std::cout << " wrong combination " << std::endl;
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
