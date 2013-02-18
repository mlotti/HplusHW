#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventClassification.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "Math/GenVector/VectorUtil.h"
#include "TLorentzVector.h"
#include "TVector3.h"
#include "TMath.h"


#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


/*
About this code
***************
PURPOSE.
Classify simulated events with a reconstructed b, tau, and MET seeming to come from a Hplus decay
according to whether these objects were identified correctly or not by comparing to the MC truth.

This code is called from FullHiggsMassCalculator.cc
*/

namespace HPlus {

//   edm::Service<TFileService> fs;
//   // Create folder to hold histograms
//   TFileDirectory myDir = fs->mkdir("EventClassification");

//------------------------> PUBLIC MEMBER FUNCTIONS <-------------------------




//------------------------> PRIVATE MEMBER FUNCTIONS <------------------------

  size_t getFirstHiggsLine(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    // Find the line of the last H+ in the event.
    size_t myHiggsLine = 0;
    //int myHiggsLine = 0;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (TMath::Abs(p.pdgId()) == 37) {
	myHiggsLine = i;
	break;
      }
    }
    if (!myHiggsLine) return -1;
    return myHiggsLine;
    std::cout << "EventClassification: First Higgs line is " << myHiggsLine << std::endl;
  }

  size_t getLastHiggsLine(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    // Find the line of the last H+ in the event.
    //size_t myHiggsLine = 0;
    size_t myHiggsLine = 0;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (TMath::Abs(p.pdgId()) == 37) myHiggsLine = i;
    }
    if (!myHiggsLine) return -1;
    return myHiggsLine;
    std::cout << "EventClassification: Last Higgs line is " << myHiggsLine << std::endl;
  }

  // IMPORTANT: AS IT IS, THIS FUNCTION GETS THE MOTHER OF THE SECOND HIGGS IN THE EVENT. IF THERE ARE TWO,
  // THE FUNCTION WILL NOT WORK AS EXPECTED.
  // Improvement: return HiggsSideTopLine instead of pointer to reco::Candidate
  reco::Candidate* getHiggsSideTop(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    // Get Higgs line.
    size_t myHiggsLine = getLastHiggsLine(iEvent);
    // Get Higgs' mother (she must be a million years old...).
    reco::Candidate* myHiggsSideTop = const_cast<reco::Candidate*>(genParticles->at(myHiggsLine).mother());
    bool myStatus = true;
    while (myStatus) {
      if (!myHiggsSideTop) return NULL;
      //std::cout << "FullMass: Higgs side mother = " << myHiggsSideTop->pdgId() << std::endl;
      if (TMath::Abs(myHiggsSideTop->pdgId()) == 6) myStatus = false;
      if (myStatus) myHiggsSideTop = const_cast<reco::Candidate*>(myHiggsSideTop->mother());
    }
    if (!myHiggsSideTop) return NULL;
    return myHiggsSideTop;
    std::cout << "EventClassification: First Higgs side top selected!" << std::endl;
  }

  reco::Candidate* getHiggsSideBJet(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    // Look at Higgs side top daughters to find b-jet.    
    reco::Candidate* myHiggsSideBJet = 0;
    reco::Candidate* myHiggsSideTop = getHiggsSideTop(iEvent);
    if (!myHiggsSideTop) return NULL;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (TMath::Abs(p.pdgId()) == 5) {
	reco::Candidate* myBMother = const_cast<reco::Candidate*>(p.mother());
        bool myStatus = true;
        while (myStatus) {
          if (!myBMother)  myStatus = false;
          else {
	    std::cout << "EventClassification: B quark mother = " << myBMother->pdgId() << std::endl;
            if (TMath::Abs(myBMother->pdgId()) == 6) {
              myStatus = false;
              // Below is where we check if the b jet comes from the Higgs side top.   
	      double myDeltaR = ROOT::Math::VectorUtil::DeltaR(myBMother->p4(), myHiggsSideTop->p4());
              if (myDeltaR < 0.01) {
                myHiggsSideBJet = const_cast<reco::Candidate*>(&p);
                i = genParticles->size(); // to end the enclosing for loop
              }
            }
            if (myStatus)
              myBMother = const_cast<reco::Candidate*>(myBMother->mother());
          }
        }
      }
    }
    if (!myHiggsSideBJet) return NULL;
    return myHiggsSideBJet;
    std::cout << "FullMass: Higgs side bjet found, pt=" << myHiggsSideBJet->pt() << ", eta=" << myHiggsSideBJet->eta() << std::endl;
  }



//------------------------> OLD MEMBER FUNCTIONS <----------------------------

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
