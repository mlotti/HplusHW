#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

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

  void printJetDiscriminants(const edm::Event& iEvent) const;
  void printTauDiscriminants(const edm::Event& iEvent) const;
  void printTriggerPaths(const edm::Event& iEvent) const;

  edm::InputTag jetSrc_;
  edm::InputTag tauSrc_;
  edm::InputTag trigSrc_;
  edm::InputTag patTrigSrc_;
};

HPlusDebugAnalyzer::HPlusDebugAnalyzer(const edm::ParameterSet& pset):
  jetSrc_(pset.getUntrackedParameter<edm::InputTag>("jetSrc")),
  tauSrc_(pset.getUntrackedParameter<edm::InputTag>("tauSrc")),
  trigSrc_(pset.getUntrackedParameter<edm::InputTag>("trigSrc"))
  //patTrigSrc_(pset.getUntrackedParameter<edm::InputTag>("patTrigSrc"))
{}

HPlusDebugAnalyzer::~HPlusDebugAnalyzer() {}

void HPlusDebugAnalyzer::beginJob() {
}

void HPlusDebugAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  //printJetDiscriminants(iEvent);
  printTauDiscriminants(iEvent);
  //printTriggerPaths(iEvent);
}

void HPlusDebugAnalyzer::printJetDiscriminants(const edm::Event& iEvent) const {
  edm::Handle<edm::View<pat::Jet> > jets;
  iEvent.getByLabel(jetSrc_, jets);

  if(jets->size() == 0)
    return;

  const std::vector<std::pair<std::string, float> >& bdiscrs = jets->front().getPairDiscri();
  std::cout << "Number of discriminants " << bdiscrs.size() << std::endl;
  for(size_t i=0; i<bdiscrs.size(); ++i) {
    std::cout << "  " << bdiscrs[i].first << ": " << bdiscrs[i].second << std::endl;
  }
}

void HPlusDebugAnalyzer::printTauDiscriminants(const edm::Event& iEvent) const {
  edm::Handle<edm::View<pat::Tau> > taus;
  iEvent.getByLabel(tauSrc_, taus);

  if(taus->size() == 0)
    return;

  const std::vector<pat::Tau::IdPair>& ids = taus->front().tauIDs();
  std::cout << "Number of discriminants " << ids.size() << std::endl;
  for(size_t i=0; i<ids.size(); ++i) {
    std::cout << "  " << ids[i].first << ": " << ids[i].second << std::endl;
  }
}

void HPlusDebugAnalyzer::printTriggerPaths(const edm::Event& iEvent) const {
  edm::Handle<edm::TriggerResults> trigger;
  iEvent.getByLabel(trigSrc_, trigger);

  const edm::TriggerNames& triggerNames = iEvent.triggerNames(*trigger);

  std::cout << "Available triggers:" << std::endl;
  for(size_t i=0; i<triggerNames.size(); ++i) {
    std::cout << "  " << triggerNames.triggerName(i) << std::endl;
  }
}


void HPlusDebugAnalyzer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusDebugAnalyzer);
