// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MCConverter_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MCConverter_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMCParticle.h"

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
  static MyMCParticle convert(const reco::GenJet&);
  static void addMCJets(const edm::Event& iEvent, std::vector<MyMCParticle>&);
};

#endif
