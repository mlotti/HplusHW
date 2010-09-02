#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "DataFormats/Common/interface/MergeableCounter.h"

#include<algorithm>
#include<functional>
#include<memory>
#include<cstdio>

namespace {
  /*
  struct PairFirstEq: public std::binary_function<HPlus::EventCounter::CountValue, std::string, bool> {
    bool operator()(const HPlus::EventCounter::CountValue& count, const std::string& name) const {
      return count.first == name;
    }
  };

  struct BookProduct: public std::binary_function<HPlus::EventCounter::CountValue, edm::EDProducer *, void> {
    void operator()(const HPlus::EventCounter::CountValue& count, edm::EDProducer *producer) const {
      producer->produces<edm::MergeableCounter, edm::InLumi>(count.first);
    }
  };

  struct ResetCount: public std::unary_function<HPlus::EventCounter::CountValue, void> {
    void operator()(HPlus::EventCounter::CountValue& count) const {
      count.second = 0;
    }
  };

  struct ProduceCount: public std::binary_function<HPlus::EventCounter::CountValue, edm::LuminosityBlock *, void> {
    void operator()(const HPlus::EventCounter::CountValue& count, edm::LuminosityBlock *block) const {
      std::auto_ptr<edm::MergeableCounter> countsPtr(new edm::MergeableCounter);
      countsPtr->value = count.second;
      block->put(countsPtr, count.first);
    }
  };
  */
}

namespace HPlus {
  EventCounter::CountValue::CountValue(const std::string& n, const std::string& i, int v): name(n), instance(i), value(v) {}
  bool EventCounter::CountValue::equalName(std::string n) const {
    return name == n;
  }
  void EventCounter::CountValue::produces(edm::EDProducer *producer) const {
    producer->produces<edm::MergeableCounter, edm::InLumi>(instance);
  }
  void EventCounter::CountValue::produce(edm::LuminosityBlock *block) const {
    std::auto_ptr<edm::MergeableCounter> countsPtr(new edm::MergeableCounter);
    countsPtr->value = value;
    block->put(countsPtr, instance);
  }
  void EventCounter::CountValue::reset() {
    value = 0;
  }

  EventCounter::EventCounter(): finalized(false) {}
  EventCounter::~EventCounter() {}

  Count EventCounter::addCounter(const std::string& name) {
    if(finalized)
      throw cms::Exception("LogicError") << "Tried to add counter '" << name << "', but EventCounter::produces has already been called!" << std::endl;

    if(name.find_first_of("#") != std::string::npos)
      throw cms::Exception("LogicError") << "Tried to add counter '" << name << "', but it has # in it's name! (# is used to separate the subcounter names)" << std::endl; 


    if(std::find_if(counter_.begin(), counter_.end(), std::bind2nd(std::mem_fun_ref(&EventCounter::CountValue::equalName), name)) != counter_.end())
      throw cms::Exception("LogicError") << "Tried to add counter '" << name << "', but it already exists!" << std::endl;

    return insert(name);
  }

  Count EventCounter::addSubCounter(const std::string& base, const std::string& name) {
    if(finalized)
      throw cms::Exception("LogicError") << "Tried to add subcounter '" << name << "' under '" << base << "', but EventCounter::produces has already been called!" << std::endl;

    if(name.find_first_of("#") != std::string::npos || base.find_first_of("#") != std::string::npos)
      throw cms::Exception("LogicError") << "Tried to add subcounter '" << name << "' under '" << base << "', but it has # in it's name! (# is used to separate the subcounter names)" << std::endl; 

    std::string subname = base+"#"+name;

    if(std::find_if(counter_.begin(), counter_.end(), std::bind2nd(std::mem_fun_ref(&EventCounter::CountValue::equalName), subname)) != counter_.end())
      throw cms::Exception("LogicError") << "Tried to add subcounter '" << name << "' under '" << base << "', but it already exists!" << std::endl;

    return insert(subname);
  }

  Count EventCounter::insert(const std::string& name) {
    size_t index = counter_.size()-1;

    char tmp[100] = "";
    snprintf(tmp, 100, "count%u", index);

    counter_.push_back(CountValue(name, tmp, 0));
    return Count(this, counter_.size()-1);
  }

  void EventCounter::produces(edm::EDProducer *producer) const {
    if(finalized)
      throw cms::Exception("LogicError") << "Tried to call EventCounter::produces(), but it had already been called!" << std::endl;
    finalized = true;

    std::for_each(counter_.begin(), counter_.end(), std::bind2nd(std::mem_fun_ref(&EventCounter::CountValue::produces), producer));
    producer->produces<std::vector<std::string>, edm::InLumi>("counterInstances");
    producer->produces<std::vector<std::string>, edm::InLumi>("counterNames");
    
  }

  void EventCounter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
    std::for_each(counter_.begin(), counter_.end(), std::mem_fun_ref(&EventCounter::CountValue::reset));
  }
  void EventCounter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) const {
    std::for_each(counter_.begin(), counter_.end(), std::bind2nd(std::mem_fun_ref(&EventCounter::CountValue::produce), &iBlock));
    std::auto_ptr<std::vector<std::string> > names(new std::vector<std::string>);
    std::auto_ptr<std::vector<std::string> > instances(new std::vector<std::string>);
    names->resize(counter_.size());
    instances->resize(counter_.size());
    for(size_t i=0; i<counter_.size(); ++i) {
      names->at(i) = counter_[i].name;
      instances->at(i) = counter_[i].instance;
    }
    iBlock.put(names, "counterNames");
    iBlock.put(instances, "counterInstances");
  }

  Count::Count(): counter_(0), index_(0) {}
  Count::Count(EventCounter *counter, size_t index):
    counter_(counter), index_(index) {}
  Count::~Count() {}


  void Count::check() const {
    if(!counter_)
      throw cms::Exception("LogicError") << "Encountered uninitialized counter!" << std::endl;
  }
}
