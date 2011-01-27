#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SelectionCounterPackager.h"

namespace HPlus {
  SelectionCounterPackager::SelectionCounterPackager(EventCounter& eventCounter, EventWeight& eventWeight)
  : fEventCounter(eventCounter),
    fEventWeight(eventWeight) { }
  
  SelectionCounterPackager::~SelectionCounterPackager() { }
  
  size_t SelectionCounterPackager::addSubCounter(const std::string& base, const std::string& name, TH1* histogram) {
    std::stringstream myPassedCounterBase;
    myPassedCounterBase << "TauIDPassedEvt::" << base; 
    std::stringstream mySubCounterBase;
    mySubCounterBase << "TauIDPassedJets::" << base; 
    SelectionCounterItem myItem(
      fEventCounter.addSubCounter(myPassedCounterBase.str(), name), 
      fEventCounter.addSubCounter(mySubCounterBase.str(), name),
      histogram);
    fSelectionCounterItems.push_back(myItem);

    return fSelectionCounterItems.size()-1;
  }

  void SelectionCounterPackager::reset() {
    for (std::vector<SelectionCounterItem>::iterator it = fSelectionCounterItems.begin();
         it != fSelectionCounterItems.end(); ++it) {
      (*it).reset();
    }
  }
  
  void SelectionCounterPackager::incrementPassedCounters() {
    for (std::vector<SelectionCounterItem>::iterator it = fSelectionCounterItems.begin();
      it != fSelectionCounterItems.end(); ++it) {
      (*it).incrementPassedCounter();
    }
  }

  SelectionCounterItem::SelectionCounterItem(Count passedCounter, Count subCounter, TH1* histogram)
  : //fEventWeight(eventWeight),
    fPassedCounter(passedCounter),
    fSubCounter(subCounter),
    fLocalCounter(0),
    fHistogram(histogram) { }

  SelectionCounterItem::SelectionCounterItem(Count passedCounter, Count subCounter, TH2* histogram)
  : //fEventWeight(eventWeight),
    fPassedCounter(passedCounter),
    fSubCounter(subCounter),
    fLocalCounter(0),
    fHistogram(histogram) { }

  SelectionCounterItem::~SelectionCounterItem() { }

  void SelectionCounterItem::fill(float value, float weight) const { 
    dynamic_cast<TH1*>(fHistogram)->Fill(value, weight);
  }

  void SelectionCounterItem::fill(float valueX, float valueY, float weight) const { 
    dynamic_cast<TH2*>(fHistogram)->Fill(valueX, valueY, weight);
  }

  void SelectionCounterItem::incrementSubCounter() {
    ++fLocalCounter;
    fSubCounter.increment(1);
  }
  
  void SelectionCounterItem::incrementPassedCounter() {
    if (fLocalCounter)
      fPassedCounter.increment(1);
  }
}
