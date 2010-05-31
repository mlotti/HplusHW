#ifndef HPLUSANALYSISTRIGGERING_H
#define HPLUSANALYSISTRIGGERING_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusAnalysisBase.h"
#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusSelectionBase.h"

#include "DataFormats/Common/interface/Handle.h"

#include <vector>
#include <string>
#include <utility>

namespace HPlusAnalysis {

/**
Class for applying and handling trigger decisions

	@author Lauri Wendland
*/
class Triggering : public HPlusAnalysisBase, public HPlusSelectionBase {
 public:
  /// Default constructor
  Triggering();
  /// Default destructor
  ~Triggering();
  
  /// Method for parsing all necessary configuration things 
  void setup(const edm::ParameterSet& iConfig);
  /// Method for setting ROOT tree branches
  void setRootTreeBranches(TTree& tree);
  /// Applies the trigger selection; returns true if trigger was passed
  bool apply(const edm::Event& iEvent);
  /// Method for filling ROOT tree branches with data
  void fillRootTreeData(TTree& tree);
  
 private:
  /// Internal method for finding TriggerResults handle and trigger bit ID for each trigger
  void findTriggerBits(const std::vector<edm::Handle<edm::TriggerResults> >& handles,
                       std::vector<std::string>& requested,
                       std::vector<std::pair<int, int> >& bits);
  /// Prints to LogInfo names of all available triggers
  void printListOfTriggers(const std::vector<edm::Handle<edm::TriggerResults> >& handles);
  
  /// IDs of the event counters
  std::vector<int> fCounterIdPassedTrigger;
  /// List of trigger names of the triggers to be saved to a ROOT file
  std::vector<std::string> fTriggerNamesToBeSaved;
  /// List of trigger names of the triggers to be applied as event selection
  std::vector<std::string> fTriggerNamesToBeApplied;
  
  /// Status flag indicating wheather the trigger bits have been found
  bool fFoundTriggerBitsStatus;
  /// pair(index of handle(TriggerResults), index of trg inside the handle)
  std::vector<std::pair<int, int> > fTriggerBitsToBeSaved;
  /// pair(index of handle(TriggerResults), index of trg inside the handle)
  std::vector<std::pair<int, int> > fTriggerBitsToBeApplied; 
  
  /// Option flag for printing once per job the names of the available triggers
  bool fPrintTriggerNames;
  
  /// Variables for the ROOT tree
  std::vector<int> fTriggerStatusToBeSaved;
};

}

#endif
