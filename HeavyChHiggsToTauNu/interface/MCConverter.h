// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MCConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MCConverter_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMCParticle.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyGlobalPoint.h"

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
  edm::InputTag genJets;
  edm::InputTag simHits;
  edm::InputTag genParticles;
  edm::InputTag genVisibleTaus;
  edm::InputTag genParticlesReplacement;
  
};

#endif
