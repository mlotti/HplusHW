/*#ifndef HPLUSANALYSISSELECTIONMANAGER_H
#define HPLUSANALYSISSELECTIONMANAGER_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusAnalysisBase.h"
#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusSelectionBase.h"

#include "TTree.h"
#include <vector>

namespace HPlusAnalysis {


Class for managing and applying n event selections

	@author Lauri Wendland


class SelectionManager : public HPlusAnalysisBase {
 public:
  SelectionManager(edm::Service<TFileService>& fileService, Counter& counter);
  ~SelectionManager();
  
  /// Creates the selections that have been asked for in the config file
  void setup(const edm::ParameterSet& iConfig);
  /// Method for setting ROOT tree branches
  void setRootTreeBranches(TTree& tree);
  /// Applies the selections; returns true if all selections were passed, otherwise false
  bool apply(const edm::Event& iEvent);
  /// Method for filling ROOT tree branches with data
  void fillRootTreeData(TTree& tree);

 private:
  /// Creates an event selection object
  void createSelection(const std::string& name, const edm::ParameterSet& parameters);
 
  /// Collection of selections to be applied
  std::vector<HPlusSelectionBase*> fSelections;
  
};

}

#endif
*/