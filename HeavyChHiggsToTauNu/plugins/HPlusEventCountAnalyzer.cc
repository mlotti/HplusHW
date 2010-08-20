#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "DataFormats/Provenance/interface/Provenance.h"

#include<iostream>
#include<vector>

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

  private:
    edm::InputTag tag_;
    long long count_;
  };

  std::vector<Counter> counters;
  std::vector<edm::InputTag> available;
};

HPlusEventCountAnalyzer::HPlusEventCountAnalyzer(const edm::ParameterSet& pset) {
  const std::vector<edm::InputTag>& tags = pset.getUntrackedParameter<std::vector<edm::InputTag> >("counters");
  for(size_t i=0; i<tags.size(); ++i) {
    counters.push_back(tags[i]);
  }
}

HPlusEventCountAnalyzer::~HPlusEventCountAnalyzer() {}

void HPlusEventCountAnalyzer::beginJob() {
}

void HPlusEventCountAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
}

void HPlusEventCountAnalyzer::endLuminosityBlock(const edm::LuminosityBlock & lumi, const edm::EventSetup & setup) {
  /*
  edm::Handle<edm::MergeableCounter> counter;
  lumi.getByLabel("countAll", counter);

  int totalNumber = counter->value;
  lumi.getByLabel("countmuonsPt", counter);
  int numberAfterCut = counter->value;
  double efficiency = numberAfterCut/double(totalNumber);

  std::cout << "Foo: " << numberAfterCut << "/" << totalNumber << " = " << efficiency << std::endl;
  */


  std::vector<edm::Handle<edm::MergeableCounter> > counters;
  lumi.getManyByType(counters);

  std::cout << "Found " << counters.size() << " counters" << std::endl;
  for(size_t i=0; i<counters.size(); ++i) {
    const edm::Provenance *prov = counters[i].provenance();
    edm::InputTag tag(prov->moduleLabel(), prov->productInstanceName(), prov->processName());

    std::cout << prov->moduleLabel() << ":" << prov->productInstanceName() << ":" << prov->processName() << "  :  " << counters[i]->value << std::endl;
  }
}

void HPlusEventCountAnalyzer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusEventCountAnalyzer);
