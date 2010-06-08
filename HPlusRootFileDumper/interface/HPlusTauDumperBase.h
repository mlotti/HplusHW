#ifndef HPLUSTAUDUMPERBASE_H
#define HPLUSTAUDUMPERBASE_H

#include "DataFormats/TauReco/interface/PFTauTagInfo.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/EDProducer.h"

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusAnalysisBase.h"

#include "TTree.h"

#include <vector>

/**
Base class for dumping tau collection data to a ROOT tree

	@author Lauri Wendland
*/

namespace HPlusAnalysis {

class HPlusTauDumperBase : public HPlusAnalysisBase {
 public:
  /// Default constructor (takes a pointer to the ROOT tree object containing the data)
  HPlusTauDumperBase(edm::EDProducer& producer, edm::ParameterSet& aTauCollectionParameterSet, Counter* counter);
  /// Default destructor
  virtual ~HPlusTauDumperBase();
  /* /// Creates the branches common for all tau collections
  void setupCommonRootTreeBranches(edm::Event& iEvent);
  /// Creates the branches specific to this tau collection
  virtual void setupSpecificRootTreeBranches();
  /// Initializes the variables common for all tau collections
  void initializeCommonBranchData();
  /// Initializes the variables specific to this tau collection 
  virtual void initializeSpecificBranchData();
  */
  /// Sets the data specific to this tau collection; returns true if something was saved
  virtual bool setData(edm::Event& iEvent, const edm::EventSetup& iSetup); // Note: Event needs to be non-const
  
  //TVector3& getPrimaryVertex() const { return fPV; }
  
  
 protected:
  //edm::ParameterSet fTauCollectionParameterSet;
  edm::InputTag fTauCollection;
  edm::InputTag fPrimaryVertexSource;
  std::vector<edm::InputTag> fTauDiscriminators;
  //std::vector<float> fTauDiscriminatorValues;
  
  
  // FIXME: check if these are needed
  float fdByLeadingTrackFinding;
  float fdByLeadingTrackPtCut;
  float fdByIsolation;
  float fdAgainstElectron;
  int fjtau;
  double  fPVx, fPVy, fPVz;
    
};

}

#endif
