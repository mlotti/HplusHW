/*#include "HiggsAnalysis/HPlusRootFileDumper/interface/SelectionManager.h"
#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusSelectionFwd.h"

#include <iostream>

namespace HPlusAnalysis {

SelectionManager::SelectionManager(edm::Service<TFileService>& fileService, Counter& counter)
: HPlusAnalysisBase(fileService, counter) {
}

SelectionManager::~SelectionManager() {
  for (std::vector<HPlusSelectionBase*>::iterator it = fSelections.begin(); it != fSelections.end(); ++it) {
    //delete *it; // This throws the core dump; guess the deleted object must be a pointer to the correct class
  }
  fSelections.clear();
}

void SelectionManager::setup(const edm::ParameterSet& iConfig) {
  // Parse config
  edm::ParameterSet mySelectionSet;
  if (iConfig.exists("EventSelectionManager")) {
    mySelectionSet = iConfig.getParameter<edm::ParameterSet>("EventSelectionManager");
  }
  // Set options
  bool myDefaultAppliedStatus = true;
  if (mySelectionSet.exists("DefaultIsAppliedStatus")) {
    myDefaultAppliedStatus = mySelectionSet.getParameter<bool>("DefaultIsAppliedStatus");
  }
  bool myDefaultHistogrammedStatus = true;
  if (mySelectionSet.exists("DefaultIsHistogrammedStatus")) {
    myDefaultHistogrammedStatus = mySelectionSet.getParameter<bool>("DefaultIsHistogrammedStatus");
  }
  // Retrieve vector of event selection parametersets
  std::vector<edm::ParameterSet> mySelectionDefinitions;
  if (mySelectionSet.exists("EventSelection")) {
    mySelectionDefinitions = mySelectionSet.getParameter< std::vector<edm::ParameterSet> >("EventSelection");
  }
  // Loop over set of event selections
  for (std::vector<edm::ParameterSet>::const_iterator it = mySelectionDefinitions.begin();
       it != mySelectionDefinitions.end(); ++it) {
    if ((*it).exists("Name")) {
      std::string mySelectionName = (*it).getParameter<std::string>("Name"); 
      createSelection(mySelectionName, *it);
    } else {
      throw cms::Exception("Configuration") << "No 'Name' field specified for an event selection in config file!"; 
    }
  }
}

void SelectionManager::setRootTreeBranches(TTree& tree) {
  for (std::vector<HPlusSelectionBase*>::iterator it = fSelections.begin(); it != fSelections.end(); ++it) {
    (*it)->setRootTreeBranches(tree);
  }
}

bool SelectionManager::apply(const edm::Event& iEvent) {
  for (std::vector<HPlusSelectionBase*>::iterator it = fSelections.begin(); it != fSelections.end(); ++it) {
    // Note: execute apply method in the event selection implementation because it might do
    // histogramming or calculate root tree variables 
    if (!(*it)->apply(iEvent) || !(*it)->isApplied()) return false;
  }
  return true;
}

void SelectionManager::fillRootTreeData(TTree& tree) {
  for (std::vector<HPlusSelectionBase*>::iterator it = fSelections.begin(); it != fSelections.end(); ++it) {
    (*it)->fillRootTreeData(tree);
  }
}

void SelectionManager::createSelection(const std::string& name, const edm::ParameterSet& parameters) {
  HPlusSelectionBase* mySelection = 0;
  if (name == "HLTTrigger") {
    mySelection = new Triggering(fFileService, fCounter);
  } else if (name == "GlobalMuonVeto") {
    mySelection = new GlobalMuonVeto(fFileService, fCounter);
  } else {
    throw cms::Exception("Configuration") << "Event selection '" << name << " does not exist!";
  }
  fSelections.push_back(mySelection);
  edm::LogInfo("HPlus") << "Added event selection '" << name << "' to list of selections";
  
  // Get general settings, if they have been specified
  bool myIsAppliedStatus = true;
  if (parameters.exists("IsAppliedStatus")) {
    myIsAppliedStatus = parameters.getParameter<bool>("IsAppliedStatus");
  }
  bool myHistogrammedStatus = true;
  if (parameters.exists("IsHistogrammedStatus")) {
    myHistogrammedStatus = parameters.getParameter<bool>("IsHistogrammedStatus");
    std::cout << "Histogram status=" << myHistogrammedStatus << std::endl;
  }
  // Apply settings
  mySelection->setOptions(myIsAppliedStatus, myHistogrammedStatus);
  // Setup event selection
  mySelection->setup(parameters);
}

}
*/