#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTriggering.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "FWCore/Common/interface/TriggerNames.h"

#include <iostream>
#include <sstream>

//namespace HPlusAnalysis {

HPlusTriggering::HPlusTriggering(const edm::ParameterSet& iConfig) :
HPlusAnalysis::HPlusAnalysisBase("HLTTrigger"), 
HPlusAnalysis::HPlusSelectionBase(iConfig) {
  fFoundTriggerBitsStatus = false;
  fPrintTriggerNames = false;
  
  if (iConfig.exists("TriggerResultsName")) {
    fTriggerResultsName = iConfig.getParameter<edm::InputTag>("TriggerResultsName");
  } else {
    throw cms::Exception("HPlus") << "HPlusTriggering: You forgot to specify 'TriggerResultsName' in the config!" << std::endl;
  }
  // Parse the list of triggers in the config file
  if (iConfig.exists("TriggersToBeApplied")) {
    fTriggerNamesToBeApplied = iConfig.getParameter<std::vector<std::string> >("TriggersToBeApplied");
  }
  if (iConfig.exists("TriggersToBeSaved")) {
    fTriggerNamesToBeSaved = iConfig.getParameter<std::vector<std::string> >("TriggersToBeSaved");
  }
  // Add counters for all triggers to be applied
  fCounterInput = fCounter->addCounter("HLTTrigger: input");
  for (std::vector<std::string>::const_iterator it = fTriggerNamesToBeApplied.begin();
       it != fTriggerNamesToBeApplied.end(); ++it) {
    fCounterIdPassedTrigger.push_back(fCounter->addCounter("HLTTrigger: passed trg " + *it));
  }
  fCounterPassedAll = fCounter->addCounter("HLTTrigger: passed all");
  // Parse options
  if (iConfig.exists("PrintTriggerNames")) {
    fPrintTriggerNames = iConfig.getParameter<bool>("PrintTriggerNames");
  }
  
  // Declare produced items
  std::string alias;
  int myTriggerCount = fTriggerNamesToBeSaved.size();
  for (int i = 0; i < myTriggerCount; ++i) {
    std::string myName = fTriggerNamesToBeSaved[i];
    size_t myPosition = 0;
    while (myPosition < myName.size()) {
      size_t myIndex = myName.find("_", myPosition);
      if (myIndex < myName.size()) {
        myName = myName.erase(myIndex, 1);
        //myName[myIndex] = '-';
      }
      myPosition = myIndex;
    }
    produces<int>(alias = myName.c_str()).setBranchAlias(alias);
    fProductionTriggerNames.push_back(myName);
  }
}

HPlusTriggering::~HPlusTriggering() {
  fTriggerNamesToBeSaved.clear();
  fTriggerNamesToBeApplied.clear();
  fTriggerBitsToBeSaved.clear();
  fTriggerBitsToBeApplied.clear();
  fCounterIdPassedTrigger.clear();
  fTriggerStatusToBeSaved.clear();
}

void HPlusTriggering::beginJob() {

}

/*
void HPlusTriggering::setRootTreeBranches(TTree& tree) {
  // Initialize trigger status variables
  if (!fTriggerStatusToBeSaved.size()) {
    for (std::vector<std::string>::const_iterator it = fTriggerNamesToBeSaved.begin();
        it != fTriggerNamesToBeSaved.end(); ++it) {
      fTriggerStatusToBeSaved.push_back(0);
    }
  }
  // Setup branches
  int myTriggerCount = fTriggerNamesToBeSaved.size();
  for (int i = 0; i < myTriggerCount; ++i) {
    std::stringstream myName;
    myName << "Trigger_" << fTriggerNamesToBeSaved[i];
    tree.Branch(myName.str().c_str(), &(fTriggerStatusToBeSaved[i]));
  }
}
*/
bool HPlusTriggering::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fCounter->addCount(fCounterInput);
  edm::Handle<edm::TriggerResults> myHLTHandle;
  iEvent.getByLabel(fTriggerResultsName, myHLTHandle);
  if (!myHLTHandle.isValid()) {
    throw cms::Exception("HPlus") << "HPlusTriggering: Cannot find HLT handle!" << std::endl;
    return false;
  }
  
  // Find trigger bits, unless they are already searched
  if (!fFoundTriggerBitsStatus) {
    edm::TriggerNames const& myTriggerNames = iEvent.triggerNames(*myHLTHandle);
    findTriggerBits(myTriggerNames, fTriggerNamesToBeApplied, fTriggerBitsToBeApplied);
    findTriggerBits(myTriggerNames, fTriggerNamesToBeSaved, fTriggerBitsToBeSaved);
    if (fPrintTriggerNames) {
      printListOfTriggers(myTriggerNames);
      fPrintTriggerNames = false; // just to make sure
    }
    fFoundTriggerBitsStatus = true;
  }
     
  // Apply trigger decision
  int myTriggerCount = fTriggerBitsToBeApplied.size();
  for (int i = 0; i < myTriggerCount; ++i) {
    if (!myHLTHandle->accept(fTriggerBitsToBeApplied[i])) return false;
    fCounter->addCount(fCounterIdPassedTrigger[i]);
  }
  
  // Set saved trigger values
  myTriggerCount = fTriggerBitsToBeSaved.size();
  for (int i = 0; i < myTriggerCount; ++i) {
    std::auto_ptr<int> myTrgValue(new int);
    *myTrgValue = myHLTHandle->accept(fTriggerBitsToBeSaved[i]);
    iEvent.put(myTrgValue, fProductionTriggerNames[i]);
  }
  
  fCounter->addCount(fCounterPassedAll);
  return true;

  /* CODE EXAMPLE FOR HANDLING HLT OBJECTS
  std::vector<edm::Handle<trigger::TriggerEvent> > handles;
  iEvent.getManyByType(handles);

  for(std::vector<edm::Handle<trigger::TriggerEvent> >::const_iterator iHandle = handles.begin(); iHandle != handles.end(); ++iHandle) {
    std::string name("HLTObjects_");
    name += iHandle->provenance()->processName();
    //std::cout << name << std::endl;
    const trigger::TriggerObjectCollection& objects((*iHandle)->getObjects());
    for(trigger::TriggerObjectCollection::const_iterator iObject = objects.begin(); iObject != objects.end(); ++iObject) {
      std::cout << "  " << iObject->id() << "  " << iObject->pt() << std::endl;
    }
    //std::cout << "Adding " << objects.size() << " HLT objects with name " << name << std::endl;
    //std::cout << "Object collection size " << objects.size() << std::endl;
  }
  */
}

void HPlusTriggering::endJob() {

}
/*
void HPlusTriggering::findTriggerBits(const edm::Event& iEvent,
                                      const edm::TriggerResults& triggerResults, 
                                      std::vector<std::string>& requested)
  edm::TriggerNames const& myTriggerNames = iEvent.triggerNames(*myHLTHandle);
  int myTriggerSize = myTriggerNames.size();
  
  int myRequestedSize = requested.size();
  for (int j = 0; j < myRequestedSize; ++j) {
    std::cout << requested[j] << ", idx=" << myTriggerNames.triggerIndex(requested[j]) << std::endl;
  }
    for (int i = 0; i < myTriggerSize; ++i) {
      if (requested[j] == 
    }
  }
  
  
  std::stringstream myStream;
  myStream << "Available triggers:" << std::endl;
  edm::TriggerNames const& myTriggerNames = iEvent.triggerNames(*myHLTHandle);
  int myTriggerSize = myTriggerNames.size();
  for (int i = 0; i < myTriggerSize; ++i) {
    myStream << "  " << i << " " << myTriggerNames.triggerName(i) << std::endl;
  }
  edm::LogInfo("HPlus") << myStream.str();
*/

void HPlusTriggering::findTriggerBits(edm::TriggerNames const& triggerNames,
                                      std::vector<std::string>& requestedNames,
                                      std::vector<int>& requestedBits) {
  // Look for trigger bits
  int myRequestedSize = requestedNames.size();
  int myTriggerNamesSize = triggerNames.size();
  for (int j = 0; j < myRequestedSize; ++j) {
    int myIndex = triggerNames.triggerIndex(requestedNames[j]);
    if (myIndex == myTriggerNamesSize) {
      printListOfTriggers(triggerNames);
      throw cms::Exception("HPlus") << "HPlusTriggering: Cannot find trigger index for trigger '"
                                    << requestedNames[j] << "'!" << std::endl;
    }
    requestedBits.push_back(myIndex);
  }
}

void HPlusTriggering::printListOfTriggers(const edm::TriggerNames& names) {
  std::stringstream myStream;
  int myTriggerSize = names.size();
  myStream << "Available triggers:" << std::endl;
  for (int i = 0; i < myTriggerSize; ++i) {
    myStream << "  " << i << " " << names.triggerName(i) << std::endl;
  }
  edm::LogInfo("HPlus") << myStream.str();
}

DEFINE_FWK_MODULE(HPlusTriggering);
