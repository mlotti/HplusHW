#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SelectionCounterPackager.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

namespace HPlus {
  SelectionCounterPackager::SelectionCounterPackager(HPlus::EventCounter& eventCounter)
  : fEventCounter(eventCounter) { }

  SelectionCounterPackager::~SelectionCounterPackager() { }

  size_t SelectionCounterPackager::addSubCounter(const std::string& base, const std::string& name, WrappedTH1* histogram) {
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

  SelectionCounterItem::SelectionCounterItem(Count passedCounter, Count subCounter, WrappedTH1* histogram)
  : fPassedCounter(passedCounter),
    fSubCounter(subCounter),
    fLocalCounter(0),
    fHistogramTH1(histogram) { }

  SelectionCounterItem::SelectionCounterItem(Count passedCounter, Count subCounter, WrappedTH2* histogram)
  : fPassedCounter(passedCounter),
    fSubCounter(subCounter),
    fLocalCounter(0),
    fHistogramTH2(histogram) { }

  SelectionCounterItem::~SelectionCounterItem() { }

  void SelectionCounterItem::fill(float value) const {
    fHistogramTH1->Fill(value);
  }

  void SelectionCounterItem::fill(float valueX, float valueY) const {
    fHistogramTH2->Fill(valueX, valueY);
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
