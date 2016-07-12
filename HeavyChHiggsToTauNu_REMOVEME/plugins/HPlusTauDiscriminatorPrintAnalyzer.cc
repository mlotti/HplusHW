#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

class HPlusTauDiscriminatorPrintAnalyzer: public edm::EDAnalyzer {
 public:

  /// Default EDAnalyzer constructor
  explicit HPlusTauDiscriminatorPrintAnalyzer(const edm::ParameterSet&);
  /// Default EDAnalyzer destructor
  ~HPlusTauDiscriminatorPrintAnalyzer();

 private:
  /// Default EDAnalyzer method - called at the beginning of the job
  virtual void beginJob();
  /// Default EDAnalyzer method - called for each event
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  /// Default EDAnalyzer method - called at the end of the job
  virtual void endJob();

  edm::InputTag tauSrc_;
  bool printed_;
};

HPlusTauDiscriminatorPrintAnalyzer::HPlusTauDiscriminatorPrintAnalyzer(const edm::ParameterSet& pset):
  tauSrc_(pset.getUntrackedParameter<edm::InputTag>("src")),
  printed_(false)
{}

HPlusTauDiscriminatorPrintAnalyzer::~HPlusTauDiscriminatorPrintAnalyzer() {}

void HPlusTauDiscriminatorPrintAnalyzer::beginJob() {
}

void HPlusTauDiscriminatorPrintAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  if(printed_)
    return;

  edm::Handle<edm::View<pat::Tau> > taus;
  iEvent.getByLabel(tauSrc_, taus);

  if(taus->size() == 0)
    return;

  const std::vector<pat::Tau::IdPair>& ids = taus->front().tauIDs();
  edm::LogPrint("TauDiscriminator") << "========================================" << std::endl;
  edm::LogPrint("TauDiscriminator") << "Tau discriminants (" << ids.size() << ")" << std::endl;
  for(size_t i=0; i<ids.size(); ++i) {
    edm::LogPrint("TauDiscriminator") << "  " << ids[i].first << " : " << ids[i].second << std::endl;
  }
  edm::LogPrint("TauDiscriminator") << "========================================" << std::endl;

  printed_ = true;
}


void HPlusTauDiscriminatorPrintAnalyzer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauDiscriminatorPrintAnalyzer);
