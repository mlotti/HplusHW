#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter2.h"

#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/MergeableCounter.h"

#include "TH1F.h"

#include<algorithm>
#include<functional>
#include<memory>
#include<cstdio>

namespace {
  static const double defaultWeight = 1.0;
}

namespace HPlus {
  EventCounter2::Counter2::Counter2(const std::string& n): name(n) {}
  bool EventCounter2::Counter2::equalName(const std::string n) const {
    return name == n;
  }
  bool EventCounter2::Counter2::contains(const std::string& l) const {
    return std::find(labels.begin(), labels.end(), l) != labels.end();
  }
  size_t EventCounter2::Counter2::insert(const std::string& label) {
    size_t index = labels.size();
    labels.push_back(label);
    values.push_back(0);
    weights.push_back(0);
    weightsSquared.push_back(0);
    return index;
  }

  EventCounter2::EventCounter2(const edm::ParameterSet& iConfig): finalized(false), eventWeightPointer(&defaultWeight) {
    allCounters_.push_back(Counter2("counter")); // ensure main counter has always index 0

    // The first elements in the in main counter are from the external edm::MergeableCounters
    const edm::ParameterSet& pset = iConfig.getParameter<edm::ParameterSet>("eventCounter");
    inputCountTags_ = pset.getUntrackedParameter<std::vector<edm::InputTag> >("counters");
    for(size_t i=0; i<inputCountTags_.size(); ++i) {
      allCounters_[0].insert(inputCountTags_[i].encode());
    }
  }
  EventCounter2::~EventCounter2() {}

  Count2 EventCounter2::addCounter(const std::string& name) {
    if(finalized)
      throw cms::Exception("LogicError") << "Tried to add counter '" << name << "', but EventCounter::produces has already been called!" << std::endl;


    size_t counterIndex = findOrInsertCounter("counter");
    if(allCounters_[counterIndex].contains(name))
      throw cms::Exception("LogicError") << "Tried to add count '" << name << "' to main counter, but it already exists!" << std::endl;

    size_t countIndex = allCounters_[counterIndex].insert(name);

    return Count2(this, counterIndex, countIndex);
  }

  Count2 EventCounter2::addSubCounter(const std::string& base, const std::string& name) {
    if(finalized)
      throw cms::Exception("LogicError") << "Tried to add subcounter '" << name << "' under '" << base << "', but EventCounter::produces has already been called!" << std::endl;

    if(base == "counter")
      throw cms::Exception("LogicError") << "Tried to add subcounter '" << name << "' under '" << base << "', but 'counter' is a reserved main counter name";


    size_t counterIndex = findOrInsertCounter(base);
    if(allCounters_[counterIndex].contains(name))
      throw cms::Exception("LogicError") << "Tried to add count '" << name << "' to subcounter '" << base << "', but it already exists!" << std::endl;

    size_t countIndex = allCounters_[counterIndex].insert(name);

    return Count2(this, counterIndex, countIndex);
  }

  void EventCounter2::beginLuminosityBlock(const edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
    eventWeightPointer = &defaultWeight;

    // Read counts from file
    edm::Handle<edm::MergeableCounter> hcount;
    for(size_t i=0; i<inputCountTags_.size(); ++i) {
      iBlock.getByLabel(inputCountTags_[i], hcount);
      incrementCount(0, i, hcount->value);
    }
  }

  void EventCounter2::endJob() {
    edm::Service<TFileService> fs;
    if(!fs.isAvailable())
      return;

    TFileDirectory counterDir = fs->mkdir("counters");
    TFileDirectory weightedDir = counterDir.mkdir("weighted");

    // Write contents to histograms
    for(std::vector<Counter2>::const_iterator iCounter = allCounters_.begin(); iCounter != allCounters_.end(); ++iCounter) {
      size_t ncounts = iCounter->labels.size();
      TH1F *counts = counterDir.make<TH1F>(iCounter->name.c_str(), iCounter->name.c_str(), ncounts, 0, ncounts);
      counts->Sumw2();
      for(size_t i=0; i<ncounts; ++i) {
        size_t bin = i+1;
        counts->SetBinContent(bin, iCounter->values[i]);
        counts->SetBinError(bin, std::sqrt(static_cast<double>(iCounter->values[i])));
        counts->GetXaxis()->SetBinLabel(bin, iCounter->name.c_str());
      }

      counts = weightedDir.make<TH1F>(iCounter->name.c_str(), iCounter->name.c_str(), ncounts, 0, ncounts);
      counts->Sumw2();
      for(size_t i=0; i<ncounts; ++i) {
        size_t bin = i+1;
        counts->SetBinContent(bin, iCounter->weights[i]);
        counts->SetBinError(bin, std::sqrt(iCounter->weightsSquared[i]));
        counts->GetXaxis()->SetBinLabel(bin, iCounter->name.c_str());
      }
    }
  }

  size_t EventCounter2::findOrInsertCounter(const std::string& name) {
    std::vector<Counter2>::iterator found = std::find_if(allCounters_.begin(), allCounters_.end(), std::bind2nd(std::mem_fun_ref(&EventCounter2::Counter2::equalName), name));
    if(found != allCounters_.end())
      return found - allCounters_.begin();
    size_t index = allCounters_.size();
    allCounters_.push_back(Counter2(name));
    return index;
  }


  Count2::Count2(EventCounter2 *counter, size_t counterIndex, size_t countIndex):
    counter_(counter), counterIndex_(counterIndex), countIndex_(countIndex_) {}
  Count2::~Count2() {}


  void Count2::check() const {
    if(!counter_)
      throw cms::Exception("LogicError") << "Encountered uninitialized counter!" << std::endl;
  }
}
