#ifndef HPLUSANALYSIHPLUSSTRIGGERING_H
#define HPLUSANALYSIHPLUSSTRIGGERING_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusAnalysisBase.h"
#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusSelectionBase.h"

#include "DataFormats/Common/interface/Handle.h"

#include <vector>
#include <string>
#include <utility>

//namespace HPlusAnalysis {

/**
Class for applying and handling trigger decisions

	@author Lauri Wendland
*/
class HPlusTriggering : public HPlusAnalysis::HPlusAnalysisBase, public HPlusAnalysis::HPlusSelectionBase {
 public:
  /// Default constructor
  HPlusTriggering(const edm::ParameterSet& iConfig);
  /// Default destructor
  ~HPlusTriggering();
  
  void beginJob();

  /// Applies the trigger selection; returns true if trigger was passed
  bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  
  void endJob();
  
 private:
  void findTriggerBits(edm::TriggerNames const& triggerNames,
                       std::vector<std::string>& requestedNames,
                       std::vector<int>& requestedBits);
  void printListOfTriggers(const edm::TriggerNames& names);
 
 private:
  edm::InputTag fTriggerResultsName;
  
  // Event counters
  /// IDs of the event counters
  std::vector<int> fCounterIdPassedTrigger;
  int fCounterInput;
  int fCounterPassedAll;
  
  /// List of trigger names of the triggers to be saved to a ROOT file
  std::vector<std::string> fTriggerNamesToBeSaved;
  /// List of aliases for trigger names to be saved (underscores removed)
  std::vector<std::string> fProductionTriggerNames;
  /// List of trigger names of the triggers to be applied as event selection
  std::vector<std::string> fTriggerNamesToBeApplied;
  
  /// Status flag indicating wheather the trigger bits have been found
  bool fFoundTriggerBitsStatus;
  /// pair(index of handle(TriggerResults), index of trg inside the handle)
  std::vector<int> fTriggerBitsToBeSaved;
  /// pair(index of handle(TriggerResults), index of trg inside the handle)
  std::vector<int> fTriggerBitsToBeApplied; 
  
  /// Option flag for printing once per job the names of the available triggers
  bool fPrintTriggerNames;
  
  /// Variables for the ROOT tree
  std::vector<int> fTriggerStatusToBeSaved;
};

//}

#endif
