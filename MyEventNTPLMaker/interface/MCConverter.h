// -*- c++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_MCConverter_h
#define HiggsAnalysis_MyEventNTPLMaker_MCConverter_h

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyMCParticle.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyGlobalPoint.h"

#include "DataFormats/Math/interface/LorentzVector.h"

#include<vector>

#include "FWCore/Utilities/interface/InputTag.h"

namespace edm {
  class Event;
}
namespace reco {
  class GenJet;
  class GenParticle;
}

class MyMET;
class MyEvent;

class MCConverter {
public:
  MCConverter(const edm::InputTag& genJetLabel, const edm::InputTag& simHitLabel,
              const edm::InputTag& genLabel, const edm::InputTag& genReplLabel, const edm::InputTag& genVisTauLabel);
  ~MCConverter();

  static MyMCParticle convert(const reco::GenJet&);
  static MyMCParticle convert(const math::XYZTLorentzVectorD&);
  static void setSimTracks(const edm::Event&, MyEvent&);

  bool addMC(MyEvent *, const edm::Event&) const;

  void addMCJets(const edm::Event& iEvent, MyEvent *) const;
  MyGlobalPoint getMCPrimaryVertex(const edm::Event& iEvent) const;

  bool addMCParticles(const edm::Event&, MyEvent *, MyMET&, bool missingSilent=false) const;
  bool addMCParticles(const edm::Event&, MyEvent *, const edm::InputTag& label, bool missingSilent=false) const;
  bool addMCVisibleTaus(const edm::Event&, MyEvent *, const edm::InputTag& label, bool missingSilent=false) const;

private:
  const edm::InputTag& genJets;
  const edm::InputTag& simHits;
  const edm::InputTag& genParticles;
  const edm::InputTag& genVisibleTaus;
  const edm::InputTag& genParticlesReplacement;
  
};

#endif
