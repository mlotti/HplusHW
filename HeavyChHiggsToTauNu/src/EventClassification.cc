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
    size_t myHiggsLine = 0;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (TMath::Abs(p.pdgId()) == 37) {
	myHiggsLine = i;
	return myHiggsLine;
      }
    }
    //std::cout << "EventClassification: The (first!) Higgs line is " << myHiggsLine << std::endl;
    return 999999999;
  }

//------------------------> PUBLIC MEMBER FUNCTIONS <-------------------------

  bool eventHasGenChargedHiggs(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (TMath::Abs(p.pdgId()) == 37) {
	//std::cout << "Event has a genuine charged Higgs boson!" << std::endl;
	return true;
      }
    }
    //std::cout << "Event does not have a genuine charged Higgs boson." << std::endl;
    return false;
  }

  // Improvement: return HiggsSideTopLine instead of pointer to reco::Candidate?
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
    //std::cout << "EventClassification: First Higgs side top selected!" << std::endl;
  }

  reco::Candidate* getGenHiggsSideBJet(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    // Look at Higgs side top daughters to find b-jet.    
    reco::Candidate* myHiggsSideBJet = NULL;
    reco::Candidate* myHiggsSideTop = getGenHiggsSideTop(iEvent);
    if (!myHiggsSideTop) return NULL;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (TMath::Abs(p.pdgId()) == 5) { // or 
	reco::Candidate* myBMother = const_cast<reco::Candidate*>(p.mother());
        bool myStatus = true;
        while (myStatus) {
          if (!myBMother)  myStatus = false;
          else {
	    //std::cout << "EventClassification: B quark mother = " << myBMother->pdgId() << std::endl;
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
    //std::cout << "FullMass: Higgs side bjet found, pt=" << myHiggsSideBJet->pt() << ", eta=" << myHiggsSideBJet->eta() << std::endl;
    return myHiggsSideBJet;
  }

//   reco::Candidate* getGenHiggsSideBJetVector(const edm::Event& iEvent) {
//     edm::Handle <reco::GenParticleCollection> genParticles;
//     iEvent.getByLabel("genParticles", genParticles);
//     TVector3 myGenHiggsSideBJetVector(0.0, 0.0, 0.0);
//     // Look at Higgs side top daughters to find b-jet.    
//     reco::Candidate* myHiggsSideTop = getGenHiggsSideTop(iEvent); // ->CHECK!
//     if (!myHiggsSideTop) return myGenHiggsSideBJetVector;
//     for (size_t i=0; i < genParticles->size(); ++i) {
//       const reco::Candidate & p = (*genParticles)[i];
//       if (TMath::Abs(p.pdgId()) == 5) { // or 
// 	reco::Candidate* myBMother = const_cast<reco::Candidate*>(p.mother());
//         bool myStatus = true;
//         while (myStatus) {
//           if (!myBMother)  myStatus = false;
//           else {
// 	    std::cout << "EventClassification: B quark mother = " << myBMother->pdgId() << std::endl;
//             if (TMath::Abs(myBMother->pdgId()) == 6) {
//               myStatus = false;
//               // Below is where we check if the b jet comes from the Higgs side top.   
// 	      double myDeltaR = ROOT::Math::VectorUtil::DeltaR(myBMother->p4(), myHiggsSideTop->p4());
//               if (myDeltaR < 0.01) {
// 		myGenHiggsSideBJetVector.SetXYZ(p.px(), p.py(), p.pz());
//                 myHiggsSideBJet = const_cast<reco::Candidate*>(&p);
//                 i = genParticles->size(); // to end the enclosing for loop
//               }
//             }
//             if (myStatus)
//               myBMother = const_cast<reco::Candidate*>(myBMother->mother());
//           }
//         }
//       }
//     }
//     std::cout << "FullMass: Higgs side bjet found, pt=" << std::endl;
//     //<< myHiggsSideBJet->pt() << ", eta=" << myHiggsSideBJet->eta() << std::endl;
//     return myGenHiggsSideBJetVector;
//   }
  
  //bool eventHasTauFromHiggs() {}

  reco::Candidate* getGenTauFromHiggs(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    //    reco::Candidate& myTauFromHiggs;
    size_t myHiggsLine = getHiggsLine(iEvent);
    if (myHiggsLine > 999999) return NULL;
    // Grab charged Higgs and get its daughters
    const reco::Candidate& chargedHiggs = (*genParticles)[myHiggsLine];    
    std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(chargedHiggs);
    int daughterId = 9999999;
    for(size_t d=0; d<daughters.size(); ++d) {
      //const reco::GenParticle daughterParticle = *daughters[d];
      const reco::Candidate& daughterParticle = *daughters[d];
      daughterId = daughterParticle.pdgId();
      // If tau among immediate daughters
      if (abs(daughterId) == 15) {
	//myTauFromHiggs = const_cast<reco::Candidate*>(&daughterParticle);
	//myTauFromHiggs = const_cast<reco::Candidate*>(&daughterParticle);
	reco::Candidate* myTauFromHiggs = const_cast<reco::Candidate*>(&daughterParticle);
	return myTauFromHiggs;
      }
    }
    return NULL;
  }

  TVector3 getGenTauFromHiggsVector(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    TVector3 myGenTauFromHiggsVector(0.0, 0.0, 0.0);
    size_t myHiggsLine = getHiggsLine(iEvent);
    if (myHiggsLine > 999999) return myGenTauFromHiggsVector;
    // Grab charged Higgs and get its daughters
    const reco::Candidate& chargedHiggs = (*genParticles)[myHiggsLine];    
    //std::cout << "EventClassification: ID of particle found on Higgs line (" << myHiggsLine << ") = " << chargedHiggs.pdgId() << std::endl;
    std::vector<const reco::GenParticle*> daughters = getImmediateDaughters(chargedHiggs);
    //std::cout << "******************************************" << daughters.size() << std::endl;
    int daughterId = 9999999;
    for(size_t d=0; d<daughters.size(); ++d) {
      //const reco::GenParticle daughterParticle = *daughters[d];
      const reco::Candidate& daughterParticle = *daughters[d];
      daughterId = daughterParticle.pdgId();
      //std::cout << "EventClassification: Higgs daughter ID: " << daughterId << std::endl;
      // If tau among immediate daughters, return its momentum vector
      if (abs(daughterId) == 15) {
	myGenTauFromHiggsVector.SetXYZ(daughterParticle.px(), daughterParticle.py(), daughterParticle.pz());
	return myGenTauFromHiggsVector;
      }
    }
    return myGenTauFromHiggsVector;
  }

  bool decaysHadronically(const reco::Candidate& tau) {
    std::vector<const reco::GenParticle*> tauDaughters = getImmediateDaughters(tau);
    int tauDaughterId = 9999999;
    for(size_t t=0; t<tauDaughters.size(); ++t) {
      const reco::Candidate& tauDaughter = *tauDaughters[t];
      tauDaughterId = tauDaughter.pdgId();
      // If there is an electron or a muon among the tau daughters, return false
      if (abs(tauDaughterId) == 11 || abs(tauDaughterId) == 13) return false;
    }
    return true;
  }

//   // NOTE: it is not that relevant whether the reco tau was really 1-p, as long as it is the right one
//   bool decaysToOneProng(reco::Candidate* tau) {
//     std::vector<const reco::GenParticle*> tauDaughters = getImmediateDaughters(tau);
//     int tauDaughterId = 9999999;
//     int numberOfProngs = 0;
//     for(size_t t=0; t<tauDaughters.size(); ++t) {
//       const reco::Candidate& tauDaughter = *tauDaughters[t];
//       tauDaughterId = tauDaughter.pdgId();
//       // If tau daughter is a charged pion or kaon, increase numberOfProngs // CHECK IF THIS IS CORRECT!
//       // TODO: calculate charge of immediate daughters and check if there is one (and only one) charged particle
//       if (abs(tauDaughterId) == 211 || abs(tauDaughterId) == 321) numberOfProngs++;
//       std::cout << "EventClassification: Charged pion or kaon from tau decay found -> incrementing number of prongs" << std::endl;
//       // If tau daughter is an electron or a muon, increase numberOfProngs (I don't know if this is what we need,
//       // but the method should do exactly what its name suggests in any case)
//       if (abs(tauDaughterId) == 11 || abs(tauDaughterId) == 13) numberOfProngs++;
//       std::cout << "EventClassification: Electron or muon from tau decay found -> incrementing number of prongs" << std::endl;
//     }
//     if (numberOfProngs == 1) return true;
//     return false;
//   }

  TVector3 getVisibleMomentum(const reco::Candidate& tau) {
    std::vector<const reco::GenParticle*> tauDaughters = getImmediateDaughters(tau);
    int tauDaughterId = 9999999;
    TVector3 myVisibleTauMomentum;
    myVisibleTauMomentum.SetXYZ(tau.px(), tau.py(), tau.pz());
    for(size_t t=0; t<tauDaughters.size(); ++t) {
      const reco::Candidate& tauDaughter = *tauDaughters[t];
      tauDaughterId = tauDaughter.pdgId();
      // If a tau neutrino is found, subtract its momentum from the tau momentum to get the visible part
      if (abs(tauDaughterId) == 12 || abs(tauDaughterId) == 14 || abs(tauDaughterId) == 16) {
	myVisibleTauMomentum.SetXYZ(
				    myVisibleTauMomentum.Px() - tauDaughter.px(),
				    myVisibleTauMomentum.Py() - tauDaughter.py(),
				    myVisibleTauMomentum.Pz() - tauDaughter.pz());
	//std::cout << "EventClassification: neutrino (ID = " << tauDaughterId << ") momentum subtracted from tau momentum" << std::endl;
      }
    }
    return myVisibleTauMomentum;
  }

  TVector3 getGenMETVector(const edm::Event& iEvent) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    int pId = 9999999;
    TVector3 myGenMET(0.0, 0.0, 0.0);
    TVector3 oldGenMET(0.0, 0.0, 0.0);
    TVector3 currentNeutrinoVector(0.0, 0.0, 0.0); // auxiliary
    // Find neutrinos in the event and sum their transverse momenta. This will be the "GenNeutrinoMET"
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      pId = p.pdgId();
      // Ignore daughters of neutrinos (to avoid multiple counting of neutrinos)
      if (hasImmediateMother(p,12) || hasImmediateMother(p,14) || hasImmediateMother(p,16)) {
	// do nothing
      } else {
	if (TMath::Abs(pId) == 12 || TMath::Abs(pId) == 14 || TMath::Abs(pId) == 16) {
	  currentNeutrinoVector.SetXYZ(p.px(), p.py(), p.pz());
	  oldGenMET += currentNeutrinoVector;
	}
      }
      if (hasImmediateMother(p,12) || hasImmediateMother(p,14) || hasImmediateMother(p,16) ||
	  hasImmediateMother(p,-12) || hasImmediateMother(p,-14) || hasImmediateMother(p,-16)) continue;
      if (TMath::Abs(pId) == 12 || TMath::Abs(pId) == 14 || TMath::Abs(pId) == 16) {
	currentNeutrinoVector.SetXYZ(p.px(), p.py(), p.pz());
	myGenMET += currentNeutrinoVector;
      }

//       if (hasImmediateMother(p,12) || hasImmediateMother(p,14) || hasImmediateMother(p,16) ||
// 	  hasImmediateMother(p,-12) || hasImmediateMother(p,-14) || hasImmediateMother(p,-16)) continue;
//       if (TMath::Abs(pId) == 12 || TMath::Abs(pId) == 14 || TMath::Abs(pId) == 16) {
// 	currentNeutrinoVector.SetXYZ(p.px(), p.py(), p.pz());
// 	myGenMET += currentNeutrinoVector;
//       }
    }
    //std::cout << "EventClassification:   Old GenMET.Pt() = " << oldGenMET.Pt() << std::endl;
    //std::cout << "EventClassification:   New GenMET.Pt() = " << myGenMET.Pt() << std::endl;
    return myGenMET;
  }
  
  bool hasGenVisibleTauWithinDeltaR(const edm::Event& iEvent, TVector3 recoTauVector, double deltaRCut) {
    TVector3 genVisibleTauVector(0.0, 0.0, 0.0);
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    int pId = 9999999;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      pId = p.pdgId();
      // Ignore daughters of taus
      if (hasImmediateMother(p,15) || hasImmediateMother(p,-15)) continue;
      if (abs(pId) == 15) {
	genVisibleTauVector = getVisibleMomentum(p);
	if (recoTauVector.DeltaR(genVisibleTauVector) < deltaRCut) return true;
      }
    }
    return false;
  }

  double getClosestGenVisibleTauDeltaR(const edm::Event& iEvent, TVector3 recoTauVector) {
    TVector3 genVisibleTauVector(0.0, 0.0, 0.0);
    double currentDeltaR = 999999.9;
    double smallestDeltaR = 9999.9;
    int pId = 9999999;
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      pId = p.pdgId();
      // Ignore daughters of taus
      if (hasImmediateMother(p,15) || hasImmediateMother(p,-15)) continue;
      if (abs(pId) == 15) {
	genVisibleTauVector = getVisibleMomentum(p);
	currentDeltaR = recoTauVector.DeltaR(genVisibleTauVector);
	if (currentDeltaR < smallestDeltaR) smallestDeltaR = currentDeltaR;
      }
    }
    return smallestDeltaR; // will return a very large (initialization) value if no GEN tau is found
  }

  bool hasGenBQuarkWithinDeltaR(const edm::Event& iEvent, TVector3 recoBJetVector, double deltaRCut) {
    // DESCRIPTION: Loop over all gen particles in event. If a b quark is found (that is not the daughter
    //              of a b quark), check if its momentum vector is within deltaRCut of the reconstructed
    //              b-jet momentum vector. As soon as a b-jet is found for which this is the case, return
    //              true.
    TVector3 genBQuarkVector(0.0, 0.0, 0.0);
    int pId = 9999999;
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      pId = p.pdgId();
      // Ignore daughters of b quarks
      if (hasImmediateMother(p,5) || hasImmediateMother(p,-5)) continue;
      if (abs(pId) == 5) {
	genBQuarkVector.SetXYZ(p.px(), p.py(), p.pz());
	if (recoBJetVector.DeltaR(genBQuarkVector) < deltaRCut) return true;
      }
    }
    return false;
  }

  double getClosestGenBQuarkDeltaR(const edm::Event& iEvent, TVector3 recoBJetVector) {
    TVector3 genBQuarkVector(0.0, 0.0, 0.0);
    double currentDeltaR = 999999.9;
    double smallestDeltaR = 999.9;
    int pId = 9999999;
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      pId = p.pdgId();
      // Ignore daughters of b quarks
      if (hasImmediateMother(p,5) || hasImmediateMother(p,-5)) continue;
      if (abs(pId) == 5) {
	genBQuarkVector.SetXYZ(p.px(), p.py(), p.pz());
	currentDeltaR = recoBJetVector.DeltaR(genBQuarkVector);
	if (currentDeltaR < smallestDeltaR) smallestDeltaR = currentDeltaR;
      }
    }
    return smallestDeltaR; // will return a very large (initialization) value if no GEN b quark is found
  }

  
//   bool tauIsFromChargedHiggs() {
    
//   }

//   bool tauIsFromChargedHiggs() {
    
//   }
}











//------------------------> OLD MEMBER FUNCTIONS <----------------------------

//   TVector3 getGenVisibleTauDecayingHadronicallyToOneProngFromHiggs(const edm::Event& iEvent) {
//     edm::Handle <reco::GenParticleCollection> genParticles;
//     iEvent.getByLabel("genParticles", genParticles);
//     reco::Candidate* myTauFromHiggs = 0;
//     size_t myHiggsLine = getHiggsLine(iEvent);
//     //if (myHiggsLine == 0) return NULL;       // CHECK IF THIS IS CORRECT!!! WHAT VALUES CAN mHiggsLine GET IF A HIGGS IS FOUND?
//     // Grab charged Higgs and get its daughters
//     const reco::Candidate& chargedHiggs = (*genParticles)[myHiggsLine];    
//     std::vector<const reco::GenParticle*> higgsDaughters = getImmediateDaughters(chargedHiggs);
//     int higgsDaughterId = 9999999;
//     for(size_t h=0; h<higgsDaughters.size(); ++h) {
//       const reco::Candidate& higgsDaughter = *higgsDaughters[h];
//       higgsDaughterId = higgsDaughter.pdgId();
//       // If current daughter of Higgs is tau
//       if (abs(higgsDaughterId) == 15) {
// 	myTauFromHiggs = const_cast<reco::Candidate*>(&higgsDaughter);
// 	// Get daughters of tau (= the current higgsDaughter)
// 	std::vector<const reco::GenParticle*> tauDaughters = getImmediateDaughters(higgsDaughter);
// 	int tauDaughterId = 9999999;
// 	bool tauDecaysIntoOneProng = true;
// 	bool tauDecaysHadronically = true;
// 	int numberOfProngs = 0;
// 	TVector3 myVisibleTauMomentum;
// 	for(size_t t=0; t<tauDaughters.size(); ++t) {
// 	  const reco::Candidate& tauDaughter = *tauDaughters[t];
// 	  tauDaughterId = tauDaughter.pdgId();
// 	  // If there is an electron or a muon among the tau daughters...
// 	  if (abs(tauDaughterId) == 11 || abs(tauDaughterId) == 13) tauDecaysHadronically = false;
// 	  // If a tau neutrino is found, remove its momentum 
// 	  if (abs(tauDaughterId) == 16) {
// 	    myVisibleTauMomentum.SetXYZ(
// 					higgsDaughter.px() - tauDaughter.px(),
// 					higgsDaughter.py() - tauDaughter.py(),
// 					higgsDaughter.pz() - tauDaughter.pz());
// 	    //std::cout << "EventClassification: neutrino momentum removed from tau momentum" << std::endl;
// 	  }
// 	  // If tau daughter is a charged pion or kaon // CHECK IF THIS IS CORRECT!
// 	  if (abs(tauDaughterId) == 211 || abs(tauDaughterId) == 321) {
// 	    numberOfProngs++;
// 	  }
// 	}
// 	if (numberOfProngs != 1) myVisibleTauMomentum.SetXYZ(0.0, 0.0, 0.0);
	
//       }
//     }
//     return myVisibleTauMomentum;
//   }

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
//     //std::cout << "EventClassification: First Higgs line is " << myHiggsLine << std::endl;
//   }

// tau decay produces neutrino; use visibleTau (1-prong)

//   // Alternative way:
//   void checkIfGenuineTau(const edm::Event& iEvent, const reco::Candidate *tau) {
//     int identifiedGenuineTauCount = 0;
//     int unidentifiedGenuineTauCount = 0;
//     int fakeTauInEventWithGenuineTauCount = 0;

//     edm::Handle <reco::GenParticleCollection> genParticles;
//     iEvent.getByLabel("genParticles", genParticles);
//     ////std::cout << "matchfinding:" << std::endl;
//     for (size_t i=0; i < genParticles->size(); ++i) {
//       const reco::Candidate & p = (*genParticles)[i];
//       // If a GEN tau is found...
//       if (std::abs(p.pdgId()) == 15) {
// 	// ... check if there is a RECO tau within deltaR < 0.1
// 	if (tau && reco::deltaR(p, tau.p4()) < 0.1) {
// 	  //std::cout << "Hooooraaaaayyyy!" << std::endl;
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

//     //std::cout << "identified genuine taus:   " << identifiedGenuineTauCount << std::endl;
//     //std::cout << "unidentified genuine taus: " << unidentifiedGenuineTauCount << std::endl;
//     //std::cout << "fake taus in event with genuine taus: " << fakeTauInEventWithGenuineTauCount << std::endl;
//   }

