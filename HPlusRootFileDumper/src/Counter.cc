#include "HiggsAnalysis/HPlusRootFileDumper/interface/Counter.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include <iostream>
#include <TH1I.h>

namespace HPlusAnalysis {

Counter::Counter(std::string aModuleName) {
  fModuleName = aModuleName;
}

Counter::~Counter() {
  std::vector<CounterItem*>::const_iterator itEnd = fCounters.end();
  for (std::vector<CounterItem*>::const_iterator it = fCounters.begin(); it != itEnd; ++it) {
    delete *it; 
  }
  fMainCountersIndices.clear();
  fSubCountersIndices.clear();
}

int Counter::addCounter(std::string name) {
  // Check that name does not exist already
  if (findCounter(name)) {
    throw cms::Exception("Configuration") << "You tried to add a counter named '" << name 
                           << "', but it already exists!" << std::endl;
    return -1;
  }
  // Add counter
  fCounters.push_back(new CounterItem(name, true));
  int myIndex = fCounters.size() - 1;
  fMainCountersIndices.push_back(myIndex);
  return myIndex;
}
  
int Counter::addSubCounter(std::string name) {
  // Check that name does not exist already
  if (findCounter(name)) {
    throw cms::Exception("Configuration") << "You tried to add a sub-counter named '" << name 
        << "', but it already exists!" << std::endl;
    return -1;
  }
  // Add sub-counter
  fCounters.push_back(new CounterItem(name, false));
  int myIndex = fCounters.size() - 1;
  fSubCountersIndices.push_back(myIndex);
  return myIndex;
}

void Counter::addCount(const int index, int increment) {
  // No check for out-of-range index, but come on - what could possibly go wrong?
  fCounters[index]->increment(increment); 
}

int Counter::getCount(const int index) const {
  // No check for out-of-range index, but come on - what could possibly go wrong?
  return fCounters[index]->getValue();
}

std::string Counter::getCounterName(unsigned int index) const {
  // No check for out-of-range index, but come on - what could possibly go wrong?
  return fCounters[index]->getName();
}

void Counter::storeCountersToHistogram(edm::Service<TFileService>& fileService) const {
  // Create histogram for top-level counters
  int myCount = fMainCountersIndices.size();
  TH1I* myCounterHisto = fileService->make<TH1I>("Counters", "Counters;Counter;N", myCount, 0, myCount);
  std::cout << "Counter(" << fModuleName << ") summary:" << std::endl;
  for (int i = 0; i < myCount; ++i) {
    int myIndex = fMainCountersIndices[i];
    myCounterHisto->GetXaxis()->SetBinLabel(i+1, fCounters[myIndex]->getName().c_str());
    myCounterHisto->Fill(i, fCounters[myIndex]->getValue());
    std::cout << "  " << fCounters[myIndex]->getName() << ": " << fCounters[myIndex]->getValue() << std::endl;
  }
  // Create histogram for sub-level counters
  myCount = fSubCountersIndices.size();
  myCounterHisto = fileService->make<TH1I>("SubCounters", "SubCounters;SubCounter;N", myCount, 0, myCount);
  if (myCount)
    std::cout << "Counter(" << fModuleName << ") sub counter summary:" << std::endl;
  for (int i = 0; i < myCount; ++i) {
    int myIndex = fSubCountersIndices[i];
    myCounterHisto->GetXaxis()->SetBinLabel(i+1, fCounters[myIndex]->getName().c_str());
    myCounterHisto->Fill(i, fCounters[myIndex]->getValue());
    std::cout << "  " << fCounters[myIndex]->getName() << ": " << fCounters[myIndex]->getValue() << std::endl;
  }
}

bool Counter::findCounter(std::string aName) {
  std::vector<CounterItem*>::const_iterator itEnd = fCounters.end();
  for (std::vector<CounterItem*>::const_iterator it = fCounters.begin(); it != itEnd; ++it) {
    if ((*it)->getName() == aName) return true;
  }
  return false;
}

}