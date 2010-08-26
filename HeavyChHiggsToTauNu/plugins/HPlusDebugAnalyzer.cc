#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include<iostream>

class HPlusDebugAnalyzer: public edm::EDAnalyzer {
 public:

  /// Default EDAnalyzer constructor
  explicit HPlusDebugAnalyzer(const edm::ParameterSet&);
  /// Default EDAnalyzer destructor
  ~HPlusDebugAnalyzer();

 private:
  /// Default EDAnalyzer method - called at the beginning of the job
  virtual void beginJob();
  /// Default EDAnalyzer method - called for each event
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  /// Default EDAnalyzer method - called at the end of the job
  virtual void endJob();

  edm::InputTag src_;
};

HPlusDebugAnalyzer::HPlusDebugAnalyzer(const edm::ParameterSet& pset):
  src_(pset.getUntrackedParameter<edm::InputTag>("src"))
{}

HPlusDebugAnalyzer::~HPlusDebugAnalyzer() {}

void HPlusDebugAnalyzer::beginJob() {
}

void HPlusDebugAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<pat::Jet> > jets;
  iEvent.getByLabel(src_, jets);

  if(jets->size() == 0)
    return;

  const std::vector<std::pair<std::string, float> >& bdiscrs = jets->front().getPairDiscri();
  std::cout << "Number of discriminants " << bdiscrs.size() << std::endl;
  for(size_t i=0; i<bdiscrs.size(); ++i) {
    std::cout << "  " << bdiscrs[i].first << ": " << bdiscrs[i].second << std::endl;
  }
}

void HPlusDebugAnalyzer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusDebugAnalyzer);
