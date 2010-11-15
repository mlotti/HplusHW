#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "DataFormats/Provenance/interface/Provenance.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

#include<iostream>
#include<iomanip> 
#include<vector>
#include<algorithm>
#include<functional>

namespace {
  struct MainCounter {
    MainCounter(const std::string& name, long long count, double weight, double weightSquared):
      name_(name), count_(count), weight_(weight), weightSquared_(weightSquared) {}

    std::string name_;
    long long count_;
    double weight_;
    double weightSquared_;
  };

  struct SubCounters {
    SubCounters(const std::string& name): name_(name) {}

    std::string name_;
    std::vector<MainCounter> counts_;
  };

  struct SubCounterEq: public std::binary_function<SubCounters, std::string, bool> {
    bool operator()(const SubCounters& c, const std::string& name) const {
      return c.name_ == name;
    }
  };
}

class HPlusEventCountAnalyzer: public edm::EDAnalyzer {
 public:

  /// Default EDAnalyzer constructor
  explicit HPlusEventCountAnalyzer(const edm::ParameterSet&);
  /// Default EDAnalyzer destructor
  ~HPlusEventCountAnalyzer();

 private:
  /// Default EDAnalyzer method - called at the beginning of the job
  virtual void beginJob();
  /// Default EDAnalyzer method - called for each event
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  virtual void endLuminosityBlock(const edm::LuminosityBlock & lumi, const edm::EventSetup & setup);

  /// Default EDAnalyzer method - called at the end of the job
  virtual void endJob();

  class Counter {
  public:
    Counter(const edm::InputTag& tag): tag_(tag), name_(tag.encode()), count_(0), weight_(0), weightSquared_(0) {}
    Counter(const edm::InputTag& tag, const std::string& name): tag_(tag), name_(name),
                                                                count_(0), weight_(0), weightSquared_(0) {}

    edm::InputTag tag_;
    std::string name_;
    long long count_;
    double weight_;
    double weightSquared_;
  };

  struct CounterEq: public std::binary_function<Counter, edm::InputTag, bool> {
    bool operator()(const Counter& counter, const edm::InputTag& tag) const {
      return counter.tag_ == tag;
    }
  };

  std::vector<Counter> counters;
  std::vector<edm::InputTag> available;
  edm::InputTag counterNames;
  edm::InputTag counterInstances;

  size_t countersPlainEnd;

  bool printMainCounter;
  bool printSubCounters;
  bool printAvailableCounters;
  bool countersGiven;
  bool counterNamesGiven;
};

HPlusEventCountAnalyzer::HPlusEventCountAnalyzer(const edm::ParameterSet& pset):
  countersPlainEnd(0),
  printMainCounter(pset.getUntrackedParameter<bool>("printMainCounter", false)), 
  printSubCounters(pset.getUntrackedParameter<bool>("printSubCounters", false)), 
  printAvailableCounters(pset.getUntrackedParameter<bool>("printAvailableCounters", false)), 
  countersGiven(false), 
  counterNamesGiven(false)
{
  if(pset.exists("counters")) {
    const std::vector<edm::InputTag>& tags = pset.getUntrackedParameter<std::vector<edm::InputTag> >("counters");
    for(size_t i=0; i<tags.size(); ++i) {
      counters.push_back(tags[i]);
    }
  }
  countersPlainEnd = counters.size();
  countersGiven = !counters.empty();

  if(pset.exists("counterNames")) {
    counterNames = pset.getUntrackedParameter<edm::InputTag>("counterNames");
    counterInstances = pset.getUntrackedParameter<edm::InputTag>("counterInstances");
    counterNamesGiven = true;
  }
}

HPlusEventCountAnalyzer::~HPlusEventCountAnalyzer() {}

void HPlusEventCountAnalyzer::beginJob() {
}

void HPlusEventCountAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
}

void HPlusEventCountAnalyzer::endLuminosityBlock(const edm::LuminosityBlock & lumi, const edm::EventSetup & setup) {
  if(counterNamesGiven || countersGiven) {
    // Read first the plain edm::MergeableCounters 
    if(countersGiven) {
      edm::Handle<edm::MergeableCounter> count;
      for(size_t i=0; i<countersPlainEnd; ++i) {
        lumi.getByLabel(counters[i].tag_, count);
        counters[i].count_ += count->value;
      }
    }
    // Then, read the ones produced in EventCounter
    if(counterNamesGiven) {
      edm::Handle<std::vector<std::string> > names;
      lumi.getByLabel(counterNames, names);

      edm::Handle<std::vector<std::string> > instances;
      lumi.getByLabel(counterInstances, instances);

      if(names->size() != instances->size())
        throw cms::Exception("LogicError") << "Size of names is " << names->size() << ", size of instances is " << instances->size()
                                           << "; names is from " << counterNames.encode() << " and instances from " << counterInstances.encode() << std::endl;

      edm::Handle<edm::MergeableCounter> count;
      edm::Handle<double> weight;
      for(size_t i=0; i<instances->size(); ++i) {
        edm::InputTag tag(counterInstances.label(), instances->at(i), counterNames.process());
        lumi.getByLabel(tag, count);
        std::vector<Counter>::iterator found = std::find_if(counters.begin(), counters.end(), std::bind2nd(CounterEq(), tag));
        if(found == counters.end())
          found = counters.insert(counters.end(), Counter(tag, names->at(i)));
        found->count_ += count->value;

        edm::InputTag tag2(counterInstances.label(), instances->at(i)+"Weights", counterNames.process());
        if(lumi.getByLabel(tag2, weight)) {
          found->weight_ += *weight;

          edm::InputTag tag3(counterInstances.label(), instances->at(i)+"WeightsSquared", counterNames.process());
          lumi.getByLabel(tag3, weight);
          found->weightSquared_ += *weight;
        }
        else {
          found->weight_ += count->value;
          found->weightSquared_ += count->value;
        }
      }
    }

    // Minor performance improvement: there's no need to gather the
    // information of available counters if they're not printed.
    if(printAvailableCounters) {
      std::vector<edm::Handle<edm::MergeableCounter> > counts;
      lumi.getManyByType(counts);
      for(size_t i=0; i<counts.size(); ++i) {
        const edm::Provenance *prov = counts[i].provenance();
        edm::InputTag tag(prov->moduleLabel(), prov->productInstanceName(), prov->processName());
        std::vector<edm::InputTag> ::iterator found = std::find(available.begin(),  available.end(), tag);
        if(found == available.end())
          available.push_back(tag);
      }
    }
  }
  else {
    std::vector<edm::Handle<edm::MergeableCounter> > counts;
    lumi.getManyByType(counts);

    for(size_t i=0; i<counts.size(); ++i) {
      const edm::Provenance *prov = counts[i].provenance();
      edm::InputTag tag(prov->moduleLabel(), prov->productInstanceName(), prov->processName());
      std::vector<Counter>::iterator found = std::find_if(counters.begin(), counters.end(), std::bind2nd(CounterEq(), tag));
      if(found == counters.end()) {
        found = counters.insert(counters.end(), Counter(tag));
      }
      found->count_ += counts[i]->value;
    }
  }
}


void printCounter(const std::string& cat, bool order, const std::vector<MainCounter>& counter, const char *counterName) {
  const size_t name_w = 50;
  const size_t count_w = 20;

  edm::LogVerbatim(cat) << "========================================" << std::endl;
  edm::LogVerbatim(cat) << "Event counts in " << counterName << " " << (order ?  "(order given in python configuration)" : "(semi-alphabetical order, all counters in the file)") << std::endl;
  edm::LogVerbatim(cat) << std::endl << std::endl;
  edm::LogVerbatim(cat) << std::setw(name_w) << std::left << "Counter" << std::setw(count_w) << std::right << "Counts" << std::endl;
  for(size_t i=0; i<counter.size(); ++i)
    edm::LogVerbatim(cat) << std::setw(name_w) << std::left << counter[i].name_ << std::setw(count_w) << std::right << counter[i].count_ << std::endl;
}

void serializeCounter(TFileDirectory& dir, TFileDirectory& weightDir, const std::vector<MainCounter>& counter, const char *name) {
  TH1F * counts = dir.make<TH1F>(name, name, counter.size(), 0, counter.size());
  counts->Sumw2();
  for(size_t i=0; i<counter.size(); ++i) {
    size_t bin = i+1;
    counts->SetBinContent(bin, counter[i].count_);
    counts->SetBinError(bin, std::sqrt(static_cast<double>(counter[i].count_)));
    counts->GetXaxis()->SetBinLabel(bin, counter[i].name_.c_str());
  }

  counts = weightDir.make<TH1F>(name, name, counter.size(), 0, counter.size());
  counts->Sumw2();
  for(size_t i=0; i<counter.size(); ++i) {
    size_t bin = i+1;
    counts->SetBinContent(bin, counter[i].weight_);
    counts->SetBinError(bin, std::sqrt(counter[i].weightSquared_));
    counts->GetXaxis()->SetBinLabel(bin, counter[i].name_.c_str());
  }
}

void HPlusEventCountAnalyzer::endJob() {
  std::string cat("EventCounts");

  edm::Service<TFileService> fs;

  std::vector<MainCounter> mainCounter;
  std::vector<SubCounters> subCounters;

  for(size_t i=0; i<counters.size(); ++i) {
    size_t subIndex = counters[i].name_.find("#");
    if(subIndex != std::string::npos) {
      std::string name = counters[i].name_.substr(0, subIndex);
      std::string subname = counters[i].name_.substr(subIndex+1, std::string::npos);
      std::vector<SubCounters>::iterator found = std::find_if(subCounters.begin(), subCounters.end(), std::bind2nd(SubCounterEq(), name));
      if(found != subCounters.end()) {
        found->counts_.push_back(MainCounter(subname, counters[i].count_, counters[i].weight_, counters[i].weightSquared_));
      }
      else {
        subCounters.push_back(SubCounters(name));
        subCounters.back().counts_.push_back(MainCounter(subname, counters[i].count_, counters[i].weight_, counters[i].weightSquared_));
      }
    }
    else {
      mainCounter.push_back(MainCounter(counters[i].name_, counters[i].count_, counters[i].weight_, counters[i].weightSquared_));
    }
  }

  if(fs.isAvailable()) {
    TFileDirectory weightDir = fs->mkdir("weighted");

    serializeCounter(*fs, weightDir, mainCounter, "counter");
    for(size_t i=0; i<subCounters.size(); ++i) {
      serializeCounter(*fs, weightDir, subCounters[i].counts_, subCounters[i].name_.c_str());
    }
  }

  bool order = counterNamesGiven || countersGiven;
  if(printMainCounter) {
    printCounter(cat, order, mainCounter, "main counter");
  }
  if(printSubCounters) {
    for(size_t i=0; i<subCounters.size(); ++i) {
      printCounter(cat, order, subCounters[i].counts_, subCounters[i].name_.c_str());
    }
  }

  if(printAvailableCounters && countersGiven) {
    edm::LogVerbatim(cat) << std::endl;
    edm::LogVerbatim(cat) << "Available counters in the file" << std::endl;
    for(size_t i=0; i<available.size(); ++i) {
      edm::LogVerbatim(cat) << available[i].encode() << std::endl;
    }
  }

}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusEventCountAnalyzer);
