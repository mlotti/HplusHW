// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EventClassification_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EventClassification_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "TVector3.h"
#include "FWCore/Framework/interface/Event.h"


namespace edm {
  class Event;
  class ParameterSet;
  class EventSetup;
}

namespace reco {
  class Candidate;
}

namespace HPlus {
//   class HistoWrapper;
//   class WrappedTH1;

//   class EventClassification: public BaseSelection {
//   public:
//     EventClassification(EventCounter& eventCounter, HistoWrapper& histoWrapper);
//     ~EventClassification();

  bool eventHasTopQuark(const edm::Event& iEvent);
  double getTopQuarkInvariantMass(const edm::Event& iEvent);
  bool eventHasLightChargedHiggs(const edm::Event& iEvent);
  size_t getHiggsLine(const edm::Event& iEvent);
  reco::Candidate* getChargedHiggs(const edm::Event& iEvent);
  //size_t getFirstHiggsLine(const edm::Event& iEvent);
  //size_t getLastHiggsLine(const edm::Event& iEvent);
  reco::Candidate* getGenHiggsSideTop(const edm::Event& iEvent);
  reco::Candidate* getGenHiggsSideBJet(const edm::Event& iEvent);
  //TVector3 getGenHiggsSideBJetVector(const edm::Event& iEvent);
  reco::Candidate* getGenTauFromHiggs(const edm::Event& iEvent);
  reco::Candidate* getGenNeutrinoFromHiggs(const edm::Event& iEvent);
  TVector3 getGenTauFromHiggsVector(const edm::Event& iEvent);
  bool decaysHadronically(const reco::Candidate& tau);
  //bool decaysToOneProng(reco::Candidate* tau);
  TVector3 getVisibleMomentum(const reco::Candidate& tau);
  TVector3 getInvisibleMomentum(const reco::Candidate& tau);
  TVector3 calculateGenMETVectorFromNeutrinos(const edm::Event& iEvent);
  TVector3 getTauNeutrinoMomentum(const edm::Event& iEvent);
  bool hasGenVisibleTauWithinDeltaR(const edm::Event& iEvent, TVector3 recoTauVector, double deltaRCut);
  double getClosestGenVisibleTauDeltaR(const edm::Event& iEvent, TVector3 recoTauVector);
  bool hasGenBQuarkWithinDeltaR(const edm::Event& iEvent, TVector3 recoBJetVector, double deltaRCut);
  double getClosestGenBQuarkDeltaR(const edm::Event& iEvent, TVector3 recoBJetVector);
  int getNumberOfNeutrinosInEvent(const edm::Event& iEvent);
  void checkIfGenuineTau(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& tau);
  reco::Candidate* getClosestGenTau(const edm::Event& iEvent, TVector3 recoTauVector);
  reco::Candidate* getClosestGenBquark(const edm::Event& iEvent, TVector3 bjetVector);
  bool tauAndBJetFromSameTopQuark(const edm::Event& iEvent,const reco::Candidate& closestGenTau, 
				  const reco::Candidate& closestGenB);
  // };
}
#endif
