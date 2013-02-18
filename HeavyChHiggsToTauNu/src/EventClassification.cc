#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventClassification.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"


#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
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
IMPORTANT NOTE.
This code only works as it is expected/supposed to for events with at most 1 (one) charged Higgs boson.
It will have bugs in several places if used for events with 2+ charged Higgs bosons.

PURPOSE.
Classify simulated events with a reconstructed b, tau, and MET seeming to come from a Hplus decay
according to whether these objects were identified correctly or not by comparing to the MC truth.

This code is called from FullHiggsMassCalculator.cc
*/

std::vector<const reco::GenParticle*> getImmediateMothers(const reco::Candidate&);
std::vector<const reco::GenParticle*> getMothers(const reco::Candidate& p);
bool hasImmediateMother(const reco::Candidate& p, int id);
bool hasMother(const reco::Candidate& p, int id);
void printImmediateMothers(const reco::Candidate& p);
void printMothers(const reco::Candidate& p);
std::vector<const reco::GenParticle*> getImmediateDaughters(const reco::Candidate& p);
std::vector<const reco::GenParticle*> getDaughters(const reco::Candidate& p);
bool hasImmediateDaughter(const reco::Candidate& p, int id);
bool hasDaughter(const reco::Candidate& p, int id);
void printImmediateDaughters(const reco::Candidate& p);
void printDaughters(const reco::Candidate& p);

namespace HPlus {

//   edm::Service<TFileService> fs;
//   // Create folder to hold histograms
//   TFileDirectory myDir = fs->mkdir("EventClassification");



//------------------------> PRIVATE MEMBER FUNCTIONS <------------------------

  size_t getHiggsLine(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    // Find the line of the last H+ in the event.
    //size_t myHiggsLine = 0;
    size_t myHiggsLine = 0;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (TMath::Abs(p.pdgId()) == 37) myHiggsLine = i;
    }
    if (!myHiggsLine) return 0;
    return myHiggsLine;
    std::cout << "EventClassification: The (last!) Higgs line is " << myHiggsLine << std::endl;
  }

//------------------------> PUBLIC MEMBER FUNCTIONS <-------------------------

  // Improvement: return HiggsSideTopLine instead of pointer to reco::Candidate
  reco::Candidate* getGenHiggsSideTop(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    // Get Higgs line.
    size_t myHiggsLine = getHiggsLine(iEvent);
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

  reco::Candidate* getGenHiggsSideBJet(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    // Look at Higgs side top daughters to find b-jet.    
    reco::Candidate* myHiggsSideBJet = 0;
    reco::Candidate* myHiggsSideTop = getGenHiggsSideTop(iEvent);
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

  reco::Candidate* getGenTauFromHiggs(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    reco::Candidate* myTauFromHiggs = 0;
    size_t myHiggsLine = getHiggsLine(iEvent);
    if (myHiggsLine == 0) return NULL;       // CHECK IF THIS IS CORRECT!!! WHAT VALUES CAN mHiggsLine GET IF A HIGGS IS FOUND?
    // Grab charged Higgs and get its daughters
    const reco::Candidate& chargedHiggs = (*genParticles)[myHiggsLine];    
    std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(chargedHiggs);
    int daughterId = 9999999;
    //double px = 0, py = 0, pz = 0, E = 0;
    //bool tauFound = false;
    //bool neutrinoFound = false;
    // Loop over daughters and find tau
    for(size_t d=0; d<daughters.size(); ++d) {
      //const reco::GenParticle daughterParticle = *daughters[d];
      const reco::Candidate& daughterParticle = *daughters[d];
      daughterId = daughterParticle.pdgId();
      // If tau among immediate daughters
      if (abs(daughterId) == 15) {
	//myTauFromHiggs = const_cast<reco::Candidate*>(&daughterParticle);
	myTauFromHiggs = const_cast<reco::Candidate*>(&daughterParticle); // IS THIS DONE CORRECTLY???
	// TODO!
	return myTauFromHiggs;
      }
    }
    return NULL;
  }









//------------------------> OLD MEMBER FUNCTIONS <----------------------------

//   size_t getFirstHiggsLine(const edm::Event& iEvent) {
//     edm::Handle <reco::GenParticleCollection> genParticles;
//     iEvent.getByLabel("genParticles", genParticles);
//     // Find the line of the last H+ in the event.
//     size_t myHiggsLine = 0;
//     //int myHiggsLine = 0;
//     for (size_t i=0; i < genParticles->size(); ++i) {
//       const reco::Candidate & p = (*genParticles)[i];
//       if (TMath::Abs(p.pdgId()) == 37) {
// 	myHiggsLine = i;
// 	break;
//       }
//     }
//     if (!myHiggsLine) return -1;
//     return myHiggsLine;
//     std::cout << "EventClassification: First Higgs line is " << myHiggsLine << std::endl;
//   }

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
