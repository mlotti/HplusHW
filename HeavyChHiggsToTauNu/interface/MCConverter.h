// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MCConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MCConverter_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMCParticle.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyGlobalPoint.h"

#include<vector>

#include "FWCore/Utilities/interface/InputTag.h"

namespace edm {
  class Event;
}
namespace reco {
  class GenJet;
}

class MyMET;
class MyEvent;

class MCConverter {
public:
  MCConverter(const edm::InputTag& genJetLabel, const edm::InputTag& simHitLabel,
              const edm::InputTag& genLabel, const edm::InputTag& hepMcReplLabel);
  ~MCConverter();

  static MyMCParticle convert(const reco::GenJet&);
  static void setSimTracks(const edm::Event&, MyEvent&);

  void addMC(MyEvent *, const edm::Event&) const;

  void addMCJets(const edm::Event& iEvent, std::vector<MyMCParticle>&) const;
  MyGlobalPoint getMCPrimaryVertex(const edm::Event& iEvent) const;
  void addMCParticles(const edm::Event&, std::vector<MyMCParticle>&, MyMET&) const;

private:
  edm::InputTag genJets;
  edm::InputTag simHits;
  edm::InputTag genParticles;
  edm::InputTag hepMcProductReplacement;
  
};

#endif
