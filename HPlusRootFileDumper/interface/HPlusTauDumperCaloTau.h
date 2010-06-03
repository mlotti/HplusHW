#ifndef HPLUSTAUDUMPERCALOTAU_H
#define HPLUSTAUDUMPERCALOTAU_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTauDumperBase.h"

#include <string>

/**
Class for dumping the relevant CaloTau information to a ROOT tree

	@author Lauri Wendland, Ritva Kinnunen
*/

namespace HPlusAnalysis {

class HPlusTauDumperCaloTau : public HPlusTauDumperBase {
 public:
  /// Default constructor (takes a pointer to the ROOT tree object containing the data)
  HPlusTauDumperCaloTau(edm::EDProducer& producer,
                        edm::ParameterSet& aTauCollectionParameterSet,
                        Counter* counter);
  /// Default destructor
  ~HPlusTauDumperCaloTau();

  // /// Creates the branches specific to this tau collection
  //void setupSpecificRootTreeBranches();
  // /// Initializes the variables specific to this tau collection 
  // void initializeSpecificBranchData();
  /// Sets the data specific to this tau collection; returns true if something was saved
  bool setData(edm::Event& iEvent, const edm::EventSetup& iSetup);
  
 private:
  std::string calojetsSrc;
  std::string jetsIDSrc;
  std::string jetExtenderSrc;

  int eventCount;
  int jetCount;
  int jet2Count;
};

}

#endif
