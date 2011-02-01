#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"

class CandViewSizePrinter: public edm::EDAnalyzer {
 public:

  explicit CandViewSizePrinter(const edm::ParameterSet&);
  ~CandViewSizePrinter();

 private:
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  edm::InputTag src_;
};

CandViewSizePrinter::CandViewSizePrinter(const edm::ParameterSet& iConfig):
  src_(iConfig.getUntrackedParameter<edm::InputTag>("src"))
{}
CandViewSizePrinter::~CandViewSizePrinter() {}

void CandViewSizePrinter::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcand;
  iEvent.getByLabel(src_, hcand);

  edm::LogInfo("CandViewSizePrinter") << "Size " << hcand->size() << std::endl;
}

//define this as a plug-in
DEFINE_FWK_MODULE(CandViewSizePrinter);
