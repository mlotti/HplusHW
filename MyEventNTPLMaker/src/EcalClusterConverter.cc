#include "HiggsAnalysis/MyEventNTPLMaker/interface/EcalClusterConverter.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyJet.h"

#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/EgammaReco/interface/BasicCluster.h"

#include "Math/VectorUtil.h"

using reco::BasicCluster;

template <class T>
inline const T& helper(const edm::Event& iEvent, const edm::InputTag& label) {
  edm::Handle<T> handle;
  iEvent.getByLabel(label, handle);
  return *handle;
}

EcalClusterConverter::EcalClusterConverter(const edm::Event& iEvent, const edm::InputTag& barrelLabel, const edm::InputTag& endcapLabel):
  barrelBCCollection(helper<reco::BasicClusterCollection>(iEvent, barrelLabel)),
  endcapBCCollection(helper<reco::BasicClusterCollection>(iEvent, endcapLabel))
{}

EcalClusterConverter::~EcalClusterConverter() {}

template <class T>
inline void addClustersHelper(MyJet *jet, const T& collection, const MyGlobalPoint& myECALHitPoint) {
  unsigned int myCollectionSize = collection.size();
  for(unsigned int i=0; i != myCollectionSize; ++i) { 
    const BasicCluster& theBasicCluster(collection[i]);
    if (ROOT::Math::VectorUtil::DeltaR(math::XYZPoint(myECALHitPoint), theBasicCluster.position()) <= 0.7) {
      const math::XYZPoint& pos(theBasicCluster.position());
      jet->clusters.push_back(TLorentzVector(pos.x(), pos.y(), pos.z(), theBasicCluster.energy()));
    }
  }
}

void EcalClusterConverter::addClusters(MyJet *jet) const {
  // Loops over barrel and endcap ECAL cluster
  // and stores to jet those, which are within specified DR to
  // leading track hit point on ECAL surface

  const MyTrack *myLeadingTrack = jet->leadingTrack();
  if (!myLeadingTrack || myLeadingTrack->Pt() < 0.0001) return;
  MyGlobalPoint myECALHitPoint = myLeadingTrack->ecalHitPoint();

  // Loop over barrel ECAL clusters
  addClustersHelper(jet, barrelBCCollection, myECALHitPoint);

  // Loop over endcap ECAL clusters
  addClustersHelper(jet, endcapBCCollection, myECALHitPoint);
}
