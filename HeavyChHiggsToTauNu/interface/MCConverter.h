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
              const edm::InputTag& hepMcLabel, const edm::InputTag& hepMcReplLabel);
  ~MCConverter();

  static MyMCParticle convert(const reco::GenJet&);
  void addMCJets(const edm::Event& iEvent, std::vector<MyMCParticle>&);
  MyGlobalPoint getMCPrimaryVertex(const edm::Event& iEvent);
  void addMCParticles(const edm::Event&, std::vector<MyMCParticle>&, MyMET&);
  static void setSimTracks(const edm::Event&, MyEvent&);
private:
  edm::InputTag genJets;
  edm::InputTag simHits;
  edm::InputTag hepMcProduct;
  edm::InputTag hepMcProductReplacement;
  
};

#endif
