#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "DataFormats/Common/interface/MergeableCounter.h"

#include<algorithm>
#include<functional>
#include<memory>
#include<cstdio>

namespace {
  std::string stripName(const std::string& str) {
    std::string result;
    result.reserve(str.size());

    size_t pos = 0;
    size_t prevPos = 0;
    do {
      pos = str.find_first_of(" _", prevPos);
      result += str.substr(prevPos, pos-prevPos);
      prevPos = pos+1;
    } while(pos != std::string::npos);
    return result;
  }
}

namespace HPlus {
  EventCounter::CountValue::CountValue(const std::string& n, const std::string& i, int v, double w):
    name(n), instance(i), instanceWeights(i+"Weights"), instanceWeightsSquared(i+"WeightsSquared"),
    value(v), weight(w), weightSquared(w*w) {}
  bool EventCounter::CountValue::equalName(std::string n) const {
    return name == n;
  }
  template <typename T>
  void EventCounter::CountValue::produces(T *producer) const {
    producer->template produces<edm::MergeableCounter, edm::InLumi>(instance);
    producer->template produces<double, edm::InLumi>(instanceWeights);
    producer->template produces<double, edm::InLumi>(instanceWeightsSquared);
  }
  void EventCounter::CountValue::produce(edm::LuminosityBlock *block) const {
    std::auto_ptr<edm::MergeableCounter> countsPtr(new edm::MergeableCounter);
    countsPtr->value = value;
    block->put(countsPtr, instance);
    std::auto_ptr<double> weightsPtr(new double);
    *weightsPtr = weight;
    block->put(weightsPtr, instanceWeights);
    std::auto_ptr<double> weightsSquaredPtr(new double);
    *weightsSquaredPtr = weightSquared;
    block->put(weightsSquaredPtr, instanceWeightsSquared);
  }
  void EventCounter::CountValue::reset() {
    value = 0;
    weight = 0;
    weightSquared = 0;
  }

  EventCounter::EventCounter(): finalized(false), eventWeightPointerProvided(false) {}
  EventCounter::~EventCounter() {}

  Count EventCounter::addCounter(const std::string& name) {
    if(finalized)
      throw cms::Exception("LogicError") << "Tried to add counter '" << name << "', but EventCounter::produces has already been called!" << std::endl;

    if(name.find_first_of("#") != std::string::npos)
      throw cms::Exception("LogicError") << "Tried to add counter '" << name << "', but it has # in it's name! (# is used to separate the subcounter names)" << std::endl; 


    if(std::find_if(counter_.begin(), counter_.end(), std::bind2nd(std::mem_fun_ref(&EventCounter::CountValue::equalName), name)) != counter_.end())
      throw cms::Exception("LogicError") << "Tried to add counter '" << name << "', but it already exists!" << std::endl;

    

    uint32_t& index = counterIndices["counter"];
    char tmp[100] = "";
    snprintf(tmp, 100, "count%u", index);
    ++index;

    counter_.push_back(CountValue(name, tmp+stripName(name), 0, 0));
    return Count(this, counter_.size()-1);
  }

  Count EventCounter::addSubCounter(const std::string& base, const std::string& name) {
    if(finalized)
      throw cms::Exception("LogicError") << "Tried to add subcounter '" << name << "' under '" << base << "', but EventCounter::produces has already been called!" << std::endl;

    if(base == "counter")
      throw cms::Exception("LogicError") << "Tried to add subcounter '" << name << "' under '" << base << "', but 'counter' is a reserved main counter name";

    if(name.find_first_of("#") != std::string::npos || base.find_first_of("#") != std::string::npos)
      throw cms::Exception("LogicError") << "Tried to add subcounter '" << name << "' under '" << base << "', but it has # in it's name! (# is used to separate the subcounter names)" << std::endl; 

    std::string subname = base+"#"+name;

    if(std::find_if(counter_.begin(), counter_.end(), std::bind2nd(std::mem_fun_ref(&EventCounter::CountValue::equalName), subname)) != counter_.end())
      throw cms::Exception("LogicError") << "Tried to add subcounter '" << name << "' under '" << base << "', but it already exists!" << std::endl;

    uint32_t& index = counterIndices[base];
    char tmp[20] = "";
    snprintf(tmp, 20, "%u", index);
    ++index;

    counter_.push_back(CountValue(subname, "subcount"+stripName(base)+"#"+tmp+stripName(name), 0, 0));
    return Count(this, counter_.size()-1);
  }

  template <typename T>
  void EventCounter::producesInternal(T *producer) const {
    if(finalized)
      throw cms::Exception("LogicError") << "Tried to call EventCounter::produces(), but it had already been called!" << std::endl;
    finalized = true;

    std::for_each(counter_.begin(), counter_.end(), std::bind2nd(std::mem_fun_ref(&EventCounter::CountValue::produces<T>), producer));
    producer->template produces<std::vector<std::string>, edm::InLumi>("counterInstances");
    producer->template produces<std::vector<std::string>, edm::InLumi>("counterNames");
  }

  void EventCounter::produces(edm::EDProducer *producer) const {
    producesInternal(producer);
  }
  void EventCounter::produces(edm::EDFilter *producer) const {
    producesInternal(producer);
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

  Count::Count(EventCounter *counter, size_t index):
    counter_(counter), index_(index) {}
  Count::~Count() {}


  void Count::check() const {
    if(!counter_)
      throw cms::Exception("LogicError") << "Encountered uninitialized counter!" << std::endl;
  }
}
