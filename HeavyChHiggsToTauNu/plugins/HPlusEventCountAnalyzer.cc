#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "DataFormats/Provenance/interface/Provenance.h"

#include<iostream>
#include<iomanip> 
#include<vector>
#include<algorithm>
#include<functional>

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
    Counter(const edm::InputTag& tag): tag_(tag), count_(0) {}

    edm::InputTag tag_;
    long long count_;
  };

  struct CounterEq: public std::binary_function<Counter, edm::InputTag, bool> {
    bool operator()(const Counter& counter, const edm::InputTag& tag) const {
      return counter.tag_ == tag;
    }
  };

  std::vector<Counter> counters;
  std::vector<edm::InputTag> available;
  bool countersGiven;

};

HPlusEventCountAnalyzer::HPlusEventCountAnalyzer(const edm::ParameterSet& pset): countersGiven(false) {
  const std::vector<edm::InputTag>& tags = pset.getUntrackedParameter<std::vector<edm::InputTag> >("counters");
  for(size_t i=0; i<tags.size(); ++i) {
    counters.push_back(tags[i]);
  }
  countersGiven = !counters.empty();
}

HPlusEventCountAnalyzer::~HPlusEventCountAnalyzer() {}

void HPlusEventCountAnalyzer::beginJob() {
}

void HPlusEventCountAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
}

void HPlusEventCountAnalyzer::endLuminosityBlock(const edm::LuminosityBlock & lumi, const edm::EventSetup & setup) {
  if(countersGiven) {
    edm::Handle<edm::MergeableCounter> count;
    for(size_t i=0; i<counters.size(); ++i) {
      lumi.getByLabel(counters[i].tag_, count);
      counters[i].count_ += count->value;
    }

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

void HPlusEventCountAnalyzer::endJob() {
  std::string cat("EventCounts");
  const size_t name_w = 50;
  const size_t count_w = 20;

  edm::LogVerbatim(cat) << "========================================" << std::endl;
  edm::LogVerbatim(cat) << "Event counts " << (countersGiven ?  "(order given in python configuration)" : "(semi-alphabetical order, all counters in the file)") << std::endl;
  edm::LogVerbatim(cat) << std::endl << std::endl;
  edm::LogVerbatim(cat) << std::setw(name_w) << std::left << "Counter" << std::setw(count_w) << std::right << "Counts" << std::endl;
  for(size_t i=0; i<counters.size(); ++i) {
    edm::LogVerbatim(cat) << std::setw(name_w) << std::left << counters[i].tag_.encode() << std::setw(count_w) << std::right << counters[i].count_ << std::endl;
  }

  if(countersGiven) {
    edm::LogVerbatim(cat) << std::endl;
    edm::LogVerbatim(cat) << "Available counters in the file" << std::endl;
    for(size_t i=0; i<available.size(); ++i) {
      edm::LogVerbatim(cat) << available[i].encode() << std::endl;
    }
  }

}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusEventCountAnalyzer);
