#include <string>

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTauDumperBase.h"
#include "DataFormats/Math/interface/Vector3D.h"

namespace HPlusAnalysis {

HPlusTauDumperBase::HPlusTauDumperBase(edm::EDProducer& producer, edm::ParameterSet& aTauCollectionParameterSet, Counter* counter)
: HPlusAnalysisBase(counter) {
  // Get tau collection input tag and the vector of discriminators
  fTauCollection = aTauCollectionParameterSet.getParameter<edm::InputTag>("src");
  fTauDiscriminators = aTauCollectionParameterSet.getParameter<std::vector<edm::InputTag> >("discriminators");
  // fPrimaryVertexSource = // FIXME later 
  
  // Create here aliases for variables common to all tau objects
  std::string alias;
  
  // General jet properties
  producer.produces<std::vector<math::XYZVector> >(alias = "jetE").setBranchAlias(alias);
  // Leading track properties
  producer.produces<std::vector<math::XYZVector> >(alias = "ldgChargedHadronP").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "ldgChargedHadronJetDR").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "ldgChargedHadronHits").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "ldgChargedHadronNormalizedChi").setBranchAlias(alias);
  producer.produces<std::vector<math::XYZVector> >(alias = "ldgChargedHadronIP").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "ldgChargedHadronIPTSignificance").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "Rtau").setBranchAlias(alias);
  
  // Charge related
  producer.produces<std::vector<int> >(alias = "chargeSum").setBranchAlias(alias);
  // Charged track isolation related
  producer.produces<std::vector<int> >(alias = "trIsoSignalTrackCount").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "trIsoLowestSignalTrackPt").setBranchAlias(alias);
  producer.produces<std::vector<int> >(alias = "trIsoIsolationTrackCount").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "trIsoHighestIsolationTrackPt").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "trIsoSignalMinTrackPt").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "trIsoIsolationMinTrackPt").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "trIsoIsolationMaxDz").setBranchAlias(alias);
    // Jet energy details
  producer.produces<std::vector<float> >(alias = "EMFraction").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "maxHCALOverLdgP").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "ECALIsolationET").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "maxHCALClusterET").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "chargedHadronET").setBranchAlias(alias);
  // Flight path related
  producer.produces<std::vector<math::XYZVector> >(alias = "flightPathLength").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "flightPathTransverseSignificance").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "flightPathSignificance").setBranchAlias(alias);
  // Invariant mass related
  producer.produces<std::vector<float> >(alias = "invariantMassFromTracksOnly").setBranchAlias(alias);
  producer.produces<std::vector<float> >(alias = "invariantMassFull").setBranchAlias(alias);
  
  // add here more produces-lines, if necessary
 
  // Discriminator aliases
  for (size_t i = 0; i < fTauDiscriminators.size(); ++i) {
    producer.produces<std::vector<float> >(alias = fTauDiscriminators[i].label()).setBranchAlias(alias);
  }

  // Primary vertex
  producer.produces<math::XYZVector>(alias = "primaryVertex").setBranchAlias(alias);
}

HPlusTauDumperBase::~HPlusTauDumperBase() {

}

//void HPlusTauDumperBase::setupSpecificRootTreeBranches() {
  // virtual

//}

/*
void HPlusTauDumperBase::setupCommonRootTreeBranches(edm::Event& iEvent) {
  auto_ptr<float> test( new float );
  *test = 123456.0;
  iEvent.put( test, "test" );
  return;
  
  
  //producer.produces<std::vector<float> >(alias = "emFraction", &f);

  // Add the discriminator branches and initialize the discriminator value vector
  fTauDiscriminatorValues.reserve(fTauDiscriminators.size());
  std::string myTauCollectionName = fTauCollection.label();
  for (size_t i = 0; i < fTauDiscriminators.size(); ++i) {
    fTauDiscriminatorValues.push_back(0.0);
    // Remove the tau collection title from the discriminator name
    // With this approach, the same discriminators of different tau collections can be adressed by the same name
    std::string myDiscriminatorName = fTauDiscriminators[i].label();
    size_t mySharedLength = 0;
    while (myDiscriminatorName.compare(0, mySharedLength+1, myTauCollectionName, 0, mySharedLength+1) == 0)
      ++mySharedLength;
    std::string myBranchName = myDiscriminatorName.substr(mySharedLength, fTauDiscriminators[i].label().length() - mySharedLength);
    producer.produces<std::vector<float> >(alias = myBranchName.c_str(), &(fTauDiscriminatorValues[i]));
  }
}*/

/*void HPlusTauDumperBase::initializeSpecificBranchData() {
  // virtual

}*/

/*
void HPlusTauDumperBase::initializeCommonBranchData() {
  // Initialize here variables common to all tau collections
  fJetET = -1;
  fJetEta = -1;
  fJetPhi = -1;
  fLdgChargedHadronPT = -1;
  fLdgChargedHadronHits = -1;
  fLdgChargedHadronNormalizedChi = -1;
  fLdgChargedHadronIPT = -1;
  fLdgChargedHadronIPTSignificance = -1;
  fLdgChargedHadronIPz = -1;
  fRtau = -1;
  fChargeSum = -10;
  fTrIsoSignalTrackCount = -1;
  fTrIsoIsolationTrackCount = -1;
  fTrIsoHighestIsolationTrackPt = -1;
  fEMFraction = -1;
  fMaxHCALOverLdgP = -1;
  fECALIsolationET = -1;
  fMaxHCALClusterET = -1;
  fChargedHadronET = -1;
  fFlightPathTransverseLength = -1;
  fFlightPathTransverseSignificance = -1;
  fFlightPathSignificance = -1;
  fInvariantMassFromTracksOnly = -1;
  fInvariantMassFull = -1;

  // Initialize discriminators
  for (size_t i = 0; i < fTauDiscriminators.size(); ++i) {
    fTauDiscriminatorValues[i] = -1;
  }
}*/

void HPlusTauDumperBase::setData(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  // virtual
}

}