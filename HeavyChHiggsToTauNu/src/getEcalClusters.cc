#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

void MyEventConverter::getEcalClusters(const edm::Event& iEvent) {
	// ECAL clusters
	iEvent.getByLabel(BarrelBasicClustersInput,theBarrelBCCollection);
	iEvent.getByLabel(EndcapBasicClustersInput,theEndcapBCCollection);
}
