#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"

namespace {
  template <typename T>
  class SizePrinter: public edm::EDAnalyzer {
  public:

    explicit SizePrinter(const edm::ParameterSet&); 
    ~SizePrinter();

  private:
    virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    edm::InputTag src_;
  };

  template <typename T>
  SizePrinter<T>::SizePrinter(const edm::ParameterSet& iConfig):
    src_(iConfig.getUntrackedParameter<edm::InputTag>("src"))
  {}
  template <typename T>
  SizePrinter<T>::~SizePrinter() {}

  template <typename T>
  void SizePrinter<T>::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<T> hcand;
    iEvent.getByLabel(src_, hcand);

    edm::LogWarning("SizePrinter") << "Collection " << src_.encode() << " size " << hcand->size() << std::endl;
  }
}

typedef SizePrinter<edm::View<reco::Candidate> > HPlusCandViewSizePrinter;

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusCandViewSizePrinter);
