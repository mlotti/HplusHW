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
    hPtjjb = makeTH<TH1F>(*fs, "hPt_jjb", "hPt_jjb", 400, 0., 800.);
    hPtmax = makeTH<TH1F>(*fs, "hPt_top", "hPt_top", 400, 0., 800.);
    hjjbMass = makeTH<TH1F>(*fs, "jjbMass", "jjbMass", 400, 0., 800.);
    htopMass = makeTH<TH1F>(*fs, "topMass", "topMass", 400, 0., 800.);
  }

  TopSelection::~TopSelection() {}

  TopSelection::Data TopSelection::analyze(const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets) {
    // Reset variables

    bool passEvent = false;

    //    fSelectedJets.clear();
    //    fSelectedJets.reserve(jets.size());

    size_t passed = 0;
    double ptmax = 0;
    double topMass = -999;

    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet1 = *iter;
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
	  }
	}
      }
    }

    hPtmax->Fill(ptmax, fEventWeight.getWeight());
    htopMass->Fill(topMass, fEventWeight.getWeight());

    passEvent = true;
    if(topMass < fTopMassLow || topMass > fTopMassHigh ) passEvent = false;
    increment(fTopMassCount);

    return Data(this, passEvent);
  }
}
