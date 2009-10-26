#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EcalClusterConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"

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



void EcalClusterConverter::addClusters(MyJet *jet) const {
  // Loops over barrel and endcap ECAL cluster
  // and stores to jet those, which are within specified DR to
  // leading track hit point on ECAL surface

  const MyTrack *myLeadingTrack = jet->leadingTrack();
  if (!myLeadingTrack || myLeadingTrack->Pt() < 0.0001) return;
  MyGlobalPoint myECALHitPoint = myLeadingTrack->ecalHitPoint();
  //double myLdgEta = myECALHitPoint.Eta();
  //double myLdgPhi = myECALHitPoint.Phi();

  // Loop over barrel ECAL clusters
  unsigned int myBarrelCollectionSize = barrelBCCollection.size();
  for(unsigned int i_BC=0; i_BC != myBarrelCollectionSize; ++i_BC) { 
    const BasicCluster& theBasicCluster(barrelBCCollection[i_BC]);
    if (ROOT::Math::VectorUtil::DeltaR(math::XYZPoint(myECALHitPoint), theBasicCluster.position()) <= 0.7) {
      TLorentzVector myCluster(theBasicCluster.position().x(),
			       theBasicCluster.position().y(),
			       theBasicCluster.position().z(),
			       theBasicCluster.energy());
      jet->clusters.push_back(myCluster);
    }
  }
  // Loop over endcap ECAL clusters
  unsigned int myEndcapCollectionSize = endcapBCCollection.size();
  for(unsigned int i_BC=0; i_BC != myEndcapCollectionSize; ++i_BC) { 
    const BasicCluster& theBasicCluster(endcapBCCollection[i_BC]);
    if (ROOT::Math::VectorUtil::DeltaR(math::XYZPoint(myECALHitPoint), theBasicCluster.position()) <= 0.7) {
      TLorentzVector myCluster(theBasicCluster.position().x(),
			       theBasicCluster.position().y(),
			       theBasicCluster.position().z(),
			       theBasicCluster.energy());
      jet->clusters.push_back(myCluster);
    }
  }
}
