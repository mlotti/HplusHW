#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventClassification.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


/*
About this code
***************
PURPOSE.
Classify simulated events with a reconstructed b, tau, and MET seeming to come from a Hplus decay
according to whether these objects were identified correctly or not by comparing to the MC truth.

IMPLEMENTATION OUTLINE.


This code is called from SignalAnalysis.cc
*/


/*
Next steps:
*Loop over events, doing nothing (note: the event loop itself sits somewhere else, but I can refer to the events being looped over)
*Find gen taus and check if there's a reco tau nearby
Find reco taus that do not correspond to any gen taus
*/


namespace HPlus {

//   edm::Service<TFileService> fs;
//   // Create folder to hold histograms
//   TFileDirectory myDir = fs->mkdir("EventClassification");


// tau decay produces neutrino; use visibleTau (1-prong)
  void checkIfGenuineTau(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& tau) {
    // These counts are for test purposes only. They will not be able to do what their name suggests, because
    // this method is called separately for each event (reference iEvent)
    int identifiedGenuineTauCount = 0;
    int unidentifiedGenuineTauCount = 0;
    int fakeTauInEventWithGenuineTauCount = 0;
    
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    //std::cout << "matchfinding:" << std::endl;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      // If a GEN tau is found...
      if (std::abs(p.pdgId()) == 15) {
	// ... check if there is a RECO tau within deltaR < 0.1
	if (tau.isNonnull() && reco::deltaR(p, *tau) < 0.1) {
	  std::cout << "RECO tau corresponds to GEN tau!" << std::endl;
	  identifiedGenuineTauCount++;
 	}
	// ... or if there is no reconstructed tau (i.e. tau is null pointer)
	else if (tau.isNull()) {
	  unidentifiedGenuineTauCount++;
	}
	// ... else the tau was faked
	else if (tau.isNonnull()) {
	  fakeTauInEventWithGenuineTauCount++;
	}
      }
    }
    //   std::cout << "identified genuine taus:              " << identifiedGenuineTauCount << std::endl;
    //   std::cout << "unidentified genuine taus:            " << unidentifiedGenuineTauCount << std::endl;
    //   std::cout << "fake taus in event with genuine taus: " << fakeTauInEventWithGenuineTauCount << std::endl;
  }

//   // Alternative way:
//   void checkIfGenuineTau(const edm::Event& iEvent, const reco::Candidate *tau) {
//     int identifiedGenuineTauCount = 0;
//     int unidentifiedGenuineTauCount = 0;
//     int fakeTauInEventWithGenuineTauCount = 0;

//     edm::Handle <reco::GenParticleCollection> genParticles;
//     iEvent.getByLabel("genParticles", genParticles);
//     //std::cout << "matchfinding:" << std::endl;
//     for (size_t i=0; i < genParticles->size(); ++i) {
//       const reco::Candidate & p = (*genParticles)[i];
//       // If a GEN tau is found...
//       if (std::abs(p.pdgId()) == 15) {
// 	// ... check if there is a RECO tau within deltaR < 0.1
// 	if (tau && reco::deltaR(p, tau.p4()) < 0.1) {
// 	  std::cout << "Hooooraaaaayyyy!" << std::endl;
// 	  identifiedGenuineTauCount++;
//  	}
// 	// ... or if there is no reconstructed tau (i.e. tau is null pointer)
// 	else if (! tau) {
// 	  unidentifiedGenuineTauCount++;
// 	}
// 	// ... else the tau was faked
// 	else if (tau) {
// 	  fakeTauInEventWithGenuineTauCount++;
// 	}
//       }
//     }

//     std::cout << "identified genuine taus:   " << identifiedGenuineTauCount << std::endl;
//     std::cout << "unidentified genuine taus: " << unidentifiedGenuineTauCount << std::endl;
//     std::cout << "fake taus in event with genuine taus: " << fakeTauInEventWithGenuineTauCount << std::endl;
//   }

}
