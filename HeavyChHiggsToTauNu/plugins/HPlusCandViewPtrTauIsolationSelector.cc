#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "TH1F.h"

#include<string>

class HPlusCandViewPtrTauIsolationSelector : public edm::EDProducer {
public:
  explicit HPlusCandViewPtrTauIsolationSelector(const edm::ParameterSet&);
  ~HPlusCandViewPtrTauIsolationSelector();

private:

  typedef edm::PtrVector<reco::Candidate> ProductType;

  virtual void beginJob();
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob();

  edm::InputTag candSrc;
  edm::InputTag tauSrc;
  std::string tauDiscriminator;
  std::string againstMuonDiscriminator;
  double maxDR;
  uint32_t minCands;

  TH1 *hDR;
  uint32_t nCand;
  uint32_t nAssumptionFailed;
};

HPlusCandViewPtrTauIsolationSelector::HPlusCandViewPtrTauIsolationSelector(const edm::ParameterSet& iConfig):
  candSrc(iConfig.getParameter<edm::InputTag>("candSrc")),
  tauSrc(iConfig.getParameter<edm::InputTag>("tauSrc")),
  tauDiscriminator(iConfig.getParameter<std::string>("isolationDiscriminator")),
  againstMuonDiscriminator(iConfig.getParameter<std::string>("againstMuonDiscriminator")),
  maxDR(iConfig.getParameter<double>("deltaR")),
  minCands(iConfig.getParameter<uint32_t>("minCands")),
  hDR(0),
  nCand(0),
  nAssumptionFailed(0)
{
  produces<ProductType>();
  produces<bool>();

  edm::Service<TFileService> fs;
  if(fs.isAvailable()) {
    hDR = fs->make<TH1F>("deltaR", "DeltaR(obj, tau)", 60, 0, 6);
  }
}

HPlusCandViewPtrTauIsolationSelector::~HPlusCandViewPtrTauIsolationSelector() {}

void HPlusCandViewPtrTauIsolationSelector::beginJob() {}

void HPlusCandViewPtrTauIsolationSelector::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcand;
  iEvent.getByLabel(candSrc, hcand);

  edm::Handle<edm::View<pat::Tau> > htau;
  iEvent.getByLabel(tauSrc, htau);

  std::auto_ptr<ProductType> product(new ProductType());
  for(size_t iCand=0; iCand<hcand->size(); ++iCand) {
    ++nCand;
    edm::Ptr<pat::Tau> found;
    double maxDr = 9999;

    for(size_t iTau=0; iTau<htau->size(); ++iTau) {
      // Select only the objects which are discriminated as muons
      if(htau->at(iTau).tauID(againstMuonDiscriminator) > 0.5)
        continue;

      double dr = reco::deltaR(hcand->at(iCand), htau->at(iTau));
      if(dr < maxDr) {
        maxDr = dr;
        found = htau->ptrAt(iTau);
      }
    }

    if(hDR) hDR->Fill(maxDr);
    if(found.get() == 0 || maxDr > this->maxDR) {
      ++nAssumptionFailed;
      //edm::LogWarning("TauIsolationSelector") << "The assumption that there is a PFTau object for each muon too, failed with DR " << maxDr << std::endl;
      //throw cms::Exception("LogicError") << "The assumption that there is a PFTau object for each muon too, failed with DR " << maxDr << std::endl;
      continue;
    }
    if(found->tauID(tauDiscriminator) < 0.5)
      continue;

    product->push_back(hcand->ptrAt(iCand));
  }

  std::auto_ptr<bool> pass(new bool(true));
  if(product->size() < minCands)
    *pass = false;
  
  iEvent.put(product);
  iEvent.put(pass);
}

void HPlusCandViewPtrTauIsolationSelector::endJob() {
  if(nAssumptionFailed) {
    edm::LogWarning("TauIsolationSelector") << "The assumption that there is a PFTau object for each muon too failed for "
                                            << nAssumptionFailed << " of " << nCand << " candidates" << std::endl;
  }
}

DEFINE_FWK_MODULE(HPlusCandViewPtrTauIsolationSelector);
