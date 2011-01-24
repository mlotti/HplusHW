#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SelectionCounterPackager.h"

namespace HPlus {
  SelectionCounterPackager::SelectionCounterPackager(EventCounter& eventCounter)
  : fEventCounter(eventCounter) { }
  
  SelectionCounterPackager::~SelectionCounterPackager() { }
  
  size_t SelectionCounterPackager::addSubCounter(const std::string& base, const std::string& name) {
    fSubCounter.push_back(fEventCounter.addSubCounter(base, name));
    fLocalCounter.push_back(0);
    return fLocalCounter.size()-1;
  }

  void SelectionCounterPackager::increment(int index) {
    fSubCounter.at(index).increment(1);
    ++(fLocalCounter.at(index));
  }
  
  void SelectionCounterPackager::reset() {
    for (std::vector<int>::iterator it = fLocalCounter.begin();
         it != fLocalCounter.end(); ++it) {
      (*it) = 0;
    }
  }
}
