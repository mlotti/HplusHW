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
  // Parse the list of triggers in the config file
  if (iConfig.exists("TriggersToBeApplied")) {
    fTriggerNamesToBeApplied = iConfig.getParameter<std::vector<std::string> >("TriggersToBeApplied");
  }
  if (iConfig.exists("TriggersToBeSaved")) {
    fTriggerNamesToBeSaved = iConfig.getParameter<std::vector<std::string> >("TriggersToBeSaved");
  }
  // Add counters for all triggers to be applied
  for (std::vector<std::string>::const_iterator it = fTriggerNamesToBeApplied.begin();
       it != fTriggerNamesToBeApplied.end(); ++it) {
    fCounterIdPassedTrigger.push_back(fCounter->addCounter("Passed trg " + *it));
  }
  // Parse options
  if (iConfig.exists("PrintTriggerNames")) {
    fPrintTriggerNames = iConfig.getParameter<bool>("PrintTriggerNames");
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
  /*  std::vector<edm::Handle<edm::TriggerResults> > myHLTHandles;
  iEvent.getManyByType(myHLTHandles);
  if (!myHLTHandles.size()) {
    edm::LogWarning("HPlus") << "Cannot find HLT handles!" << std::endl;
    return false;
  }
  // Find trigger bits, unless they are already searched
  if (!fFoundTriggerBitsStatus) {
    findTriggerBits(myHLTHandles, fTriggerNamesToBeSaved, fTriggerBitsToBeSaved);
    findTriggerBits(myHLTHandles, fTriggerNamesToBeApplied, fTriggerBitsToBeApplied);
    // Check if search was successful
    fFoundTriggerBitsStatus = (fTriggerNamesToBeApplied.size() && fTriggerBitsToBeApplied.size())
      || (fTriggerNamesToBeSaved.size() && fTriggerBitsToBeSaved.size());
    if (fFoundTriggerBitsStatus) {
      edm::LogInfo("HPlus") << "Found HLT trigger names and the corresponding bits" << std::endl;
      //std::cout << "Found HLT trigger names and the corresponding bits" << std::endl;
    }
  }
  */
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
  /*  
  // Set ROOT tree variable values
  int myTriggerCount = fTriggerBitsToBeSaved.size();
  for (int i = 0; i < myTriggerCount; ++i) {
    edm::Handle<edm::TriggerResults> myHandle = myHLTHandles[fTriggerBitsToBeSaved[i].first];
    fTriggerStatusToBeSaved[i] = myHandle->accept(fTriggerBitsToBeSaved[i].second);
  }
    
  // Apply trigger decision
  myTriggerCount = fTriggerBitsToBeApplied.size();
  for (int i = 0; i < myTriggerCount; ++i) {
    edm::Handle<edm::TriggerResults> myHandle = myHLTHandles[fTriggerBitsToBeApplied[i].first];
    if (!myHandle->accept(fTriggerBitsToBeApplied[i].second)) return false;
    fCounter->addCount(fCounterIdPassedTrigger[i]);
    }*/
  return true;
}

void HPlusTriggering::endJob() {

}

/*
void HPlusTriggering::findTriggerBits(const std::vector<edm::Handle<edm::TriggerResults> >& handles,
                                 std::vector<std::string>& requested,
                                 std::vector<std::pair<int, int> >& bits) {
    // Look for triggers
  for (std::vector<std::string>::const_iterator it = requested.begin();
      it != requested.end(); ++it) {
    bool myTriggerFoundStatus = false;
    int myHandleCount = handles.size();
    for (int j = 0; j < myHandleCount; ++j) {
      edm::TriggerNames myTriggerNames;
      myTriggerNames.init(*(handles[j]));
      int myTriggerSize = myTriggerNames.size();
      for (int i = 0; i < myTriggerSize; ++i) {
        if (*it == myTriggerNames.triggerName(i)) {
          std::pair<int, int> myPair;
          myPair.first = j;
          myPair.second = i;
          bits.push_back(myPair);
          myTriggerFoundStatus = true;
        }
      }
    }
    if (!myTriggerFoundStatus) {
      printListOfTriggers(handles);
      throw cms::Exception("Configuration") << "Trigger '" << *it << "' not found in HLT menu!" << std::endl; 
    }
  }
  if (fPrintTriggerNames) {
    printListOfTriggers(handles);
    fPrintTriggerNames = false; // just to make sure
  }

}


void HPlusTriggering::printListOfTriggers(const edm::TriggerNames& names) {
  int myTriggerSize = names.size();
  std::cout << "Available triggers:" << std::endl;
  for (int i = 0; i < myTriggerSize; ++i) {
    std::cout << "  " << i << " " << names.triggerName(i) << std::endl;
  }
}

void HPlusTriggering::printListOfTriggers(const std::vector<edm::Handle<edm::TriggerResults> >& handles) {
   std::stringstream myStream;
  myStream << "Available triggers:" << std::endl;
  for (std::vector<edm::Handle<edm::TriggerResults> >::const_iterator iHandle = handles.begin();
    iHandle != handles.end(); ++iHandle) {
    edm::TriggerNames myTriggerNames;
    myTriggerNames.init(**iHandle);
    int myTriggerSize = myTriggerNames.size();
    for (int i = 0; i < myTriggerSize; ++i) {
      myStream << "  " << i << " " << myTriggerNames.triggerName(i) << std::endl;
    }
  }
  edm::LogInfo("HPlus") << myStream.str();
  
}
*/
//}

DEFINE_FWK_MODULE(HPlusTriggering);

