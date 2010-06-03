#ifndef HPLUSTAUDUMPERPF_H
#define HPLUSTAUDUMPERPF_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTauDumperBase.h"

/**
Class for dumping the relevant PF tau information to a root file

	@author Lauri Wendland
*/

namespace HPlusAnalysis {

class HPlusTauDumperPF : public HPlusTauDumperBase {
 public:
  /// Default constructor (takes a pointer to the ROOT tree object containing the data)
  HPlusTauDumperPF(edm::EDProducer& producer, edm::ParameterSet& aTauCollectionParameterSet,
                   Counter* counter);
  /// Default destructor
  ~HPlusTauDumperPF();

  /* /// Creates the branches specific to this tau collection
  void setupSpecificRootTreeBranches();
  /// Initializes the variables specific to this tau collection 
  void initializeSpecificBranchData();*/
  /// Sets the data specific to this tau collection; returns true if something was saved
  bool setData(edm::Event& iEvent, const edm::EventSetup& iSetup);
  
 private:
  
};

}

#endif
