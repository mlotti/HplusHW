// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MCConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MCConverter_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMCParticle.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyGlobalPoint.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMET.h"

#include<vector>

namespace edm {
  class Event;
}
namespace reco {
  class GenJet;
}

class MyMCParticle;

class MCConverter {
public:
  MCConverter();
  ~MCConverter();

  static MyMCParticle convert(const reco::GenJet&);
  static void addMCJets(const edm::Event& iEvent, std::vector<MyMCParticle>&);
  static MyGlobalPoint getMCPrimaryVertex(const edm::Event& iEvent);

  MyMET getMCMET();
  void addMCParticles(const edm::Event&, std::vector<MyMCParticle>&);

private:
  MyMET mcMET;
};

#endif
