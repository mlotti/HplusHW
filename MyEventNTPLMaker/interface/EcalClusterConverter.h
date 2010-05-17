// -*- C++ -*-
#ifndef HiggsAnalysis_MyEventNTPLMaker_EcalClusterConverter_h
#define HiggsAnalysis_MyEventNTPLMaker_EcalClusterConverter_h

#include "DataFormats/EgammaReco/interface/BasicClusterFwd.h" 

namespace edm {
  class Event;
  class InputTag;
}

class MyJet;

class EcalClusterConverter {
public:
  EcalClusterConverter(const edm::Event&, const edm::InputTag&, const edm::InputTag&);
  ~EcalClusterConverter();

  void addClusters(MyJet *jet) const;

private:
  const reco::BasicClusterCollection& barrelBCCollection;
  const reco::BasicClusterCollection& endcapBCCollection;
};

#endif
