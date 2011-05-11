#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "Math/GenVector/VectorUtil.h"
#include "TH1F.h"

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
    hPtjjb = makeTH<TH1F>(*fs, "Pt_jjb", "Pt_jjb", 400, 0., 800.);
    hPtmax = makeTH<TH1F>(*fs, "Pt_jjbmax", "Pt_jjbmax", 400, 0., 800.);
    hPtmaxTop = makeTH<TH1F>(*fs, "Pt_top", "Pt_top", 400, 0., 800.);
    hjjbMass = makeTH<TH1F>(*fs, "jjbMass", "jjbMass", 400, 0., 800.);
    htopMass = makeTH<TH1F>(*fs, "Mass_jjbMax", "Mass_jjbMax", 400, 0., 800.);
    htopMassReal = makeTH<TH1F>(*fs, "Mass_Top", "Mass_Top", 400, 0., 800.);
    htopMassRealb = makeTH<TH1F>(*fs, "Mass_bFromTop", "Mass_bFromTop", 400, 0., 800.);
  }

  TopSelection::~TopSelection() {}

  TopSelection::Data TopSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {
    // Reset variables

    bool passEvent = false;

    //    fSelectedJets.clear();
    //    fSelectedJets.reserve(jets.size());

    size_t passed = 0;
    double ptmax = 0;
    double topMass = -999;
    bool bFromTop = false;
    bool q1FromTop = false;
    bool q2FromTop = false;

    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet1 = *iter;
      //      const reco::GenParticle* dparticle =  iJet1->genParticle();
      // if ( dparticle) std::cout << " jet particle " << dparticle->pdgId();

      for(edm::PtrVector<pat::Jet>::const_iterator iter2 = jets.begin(); iter2 != jets.end(); ++iter2) {
	edm::Ptr<pat::Jet> iJet2 = *iter2;

	if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJet2->p4()) < 0.4) continue;

	for(edm::PtrVector<pat::Jet>::const_iterator iterb = bjets.begin(); iterb != bjets.end(); ++iterb) {
	  edm::Ptr<pat::Jet> iJetb = *iterb;
	  if (ROOT::Math::VectorUtil::DeltaR(iJet1->p4(), iJetb->p4()) < 0.4) continue;
	  if (ROOT::Math::VectorUtil::DeltaR(iJet2->p4(), iJetb->p4()) < 0.4) continue;	  
	
	  double jjbMass2 = (iJet1->p() + iJet2->p() + iJetb->p())*(iJet1->p() + iJet2->p() + iJetb->p())
	    -(iJet1->px() + iJet2->px() + iJetb->px())*(iJet1->px() + iJet2->px() + iJetb->px())
	    -(iJet1->py() + iJet2->py() + iJetb->py())*(iJet1->py() + iJet2->py() + iJetb->py())
	    -(iJet1->pz() + iJet2->pz() + iJetb->pz())*(iJet1->pz() + iJet2->pz() + iJetb->pz());
	  double ptjjb = sqrt((iJet1->px() + iJet2->px() + iJetb->px())*(iJet1->px() + iJet2->px() + iJetb->px())
			      +(iJet1->py() + iJet2->py() + iJetb->py())*(iJet1->py() + iJet2->py() + iJetb->py()));

	  double jjbMass = -999; 	  
	  if ( jjbMass2 > 0)  jjbMass = sqrt(jjbMass2);
	  hPtjjb->Fill(ptjjb, fEventWeight.getWeight());
	  hjjbMass->Fill(jjbMass, fEventWeight.getWeight());
	  if (ptjjb > ptmax ) {
	    ptmax = ptjjb;
	    topMass = jjbMass;


	    if (iEvent.isRealData()) continue;

	    int bmother = 99999;
	    const reco::GenParticle* bparticle =  iJetb->genParticle();
	    if ( bparticle) {
	      if (abs(bparticle->pdgId()) == 5) {
		int numberOfbMothers = bparticle->numberOfMothers();
		for (int im=0; im < numberOfbMothers; ++im){
		  const reco::GenParticle* mparticle = dynamic_cast<const reco::GenParticle*>(bparticle->mother(im));
		  if ( !mparticle) continue;
		  bmother = mparticle->pdgId();
		  if (abs(bmother) != 6) continue;
		  bFromTop = true;
		}
	      }
	    }
	    if (!bFromTop) continue;

	    const reco::GenParticle* q1particle =  iJet1->genParticle();
	    if ( q1particle) {
	      if (abs(q1particle->pdgId()) < 5) {
		int numberOfq1Mothers = q1particle->numberOfMothers();
		for (int im2=0; im2 < numberOfq1Mothers; ++im2){
		  const reco::GenParticle* m1particle = dynamic_cast<const reco::GenParticle*>(q1particle->mother(im2));
		  if ( !m1particle) continue;
		  int q1mother = m1particle->pdgId();
		  if (abs(q1mother) == 24 && (q1mother * bmother) > 0 ) q1FromTop = true;
		  //		  std::cout << " jet1 particle " << q1particle->pdgId() << " jet1 mother " << q1mother  << " b mother " << bmother  << std::endl;
		}
	      }
	    }
	    const reco::GenParticle* q2particle =  iJet2->genParticle();
	    if ( q2particle) {
	      if (abs(q2particle->pdgId()) < 5) {
		int numberOfq2Mothers = q2particle->numberOfMothers();
		for (int im3=0; im3 < numberOfq2Mothers; ++im3){
		  const reco::GenParticle* m2particle = dynamic_cast<const reco::GenParticle*>(q2particle->mother(im3));
		  if ( !m2particle) continue;
		  int q2mother = m2particle->pdgId();
		  if (abs(q2mother) == 24 && (q2mother * bmother) > 0 ) q2FromTop = true;
		  //		  std::cout << " jet2 particle " << q2particle->pdgId() << " jet2 mother " << q2mother  << " b mother " << bmother << std::endl;
		}												 
	      }
	    }
	  }
	}
      }
    }
  
  
    hPtmax->Fill(ptmax, fEventWeight.getWeight());
    htopMass->Fill(topMass, fEventWeight.getWeight());
    if (bFromTop && q1FromTop && q2FromTop ) {
      hPtmaxTop->Fill(ptmax, fEventWeight.getWeight());
      htopMassReal->Fill(topMass, fEventWeight.getWeight());
    }
    if (bFromTop ) htopMassRealb->Fill(topMass, fEventWeight.getWeight());

    passEvent = true;
    if(topMass < fTopMassLow || topMass > fTopMassHigh ) passEvent = false;
    increment(fTopMassCount);

    return Data(this, passEvent);
  }
}
