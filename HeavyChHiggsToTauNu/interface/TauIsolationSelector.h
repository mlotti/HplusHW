// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauIsolationSelector_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauIsolationSelector_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "TH1F.h"

#include<string>

namespace HPlus {

  template <typename T>
  class TauIsolationSelector: public edm::EDProducer {
  public:
    explicit TauIsolationSelector(const edm::ParameterSet&);
    ~TauIsolationSelector();

  private:

    typedef edm::PtrVector<T> ProductType;
    typedef edm::ValueMap<float> MapType;

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

  template <typename T>
  TauIsolationSelector<T>::TauIsolationSelector(const edm::ParameterSet& iConfig):
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
        produces<MapType>();

        edm::Service<TFileService> fs;
        if(fs.isAvailable()) {
          hDR = fs->make<TH1F>("deltaR", "DeltaR(obj, tau)", 60, 0, 6);
        }
      }

  template <typename T>
  TauIsolationSelector<T>::~TauIsolationSelector() {}

  template <typename T>
  void TauIsolationSelector<T>::beginJob() {}

  template <typename T>
  void TauIsolationSelector<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<T> > hcand;
    iEvent.getByLabel(candSrc, hcand);

    edm::Handle<edm::View<pat::Tau> > htau;
    iEvent.getByLabel(tauSrc, htau);

    std::auto_ptr<ProductType> product(new ProductType());
    std::vector<float> isolated(hcand->size(), 0);
    isolated.reserve(hcand->size());

    // Loop over the candidates to check the isolation
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
      isolated[iCand] = 1;
    }

    // Fill the value map
    std::auto_ptr<MapType> valueMap(new MapType());
    MapType::Filler filler(*valueMap);
    filler.insert(hcand, isolated.begin(), isolated.end());
    filler.fill();

    // Cut on number
    std::auto_ptr<bool> pass(new bool(true));
    if(product->size() < minCands)
      *pass = false;
  
    iEvent.put(product);
    iEvent.put(valueMap);
    iEvent.put(pass);
  }

  template <typename T>
  void TauIsolationSelector<T>::endJob() {
    if(nAssumptionFailed) {
      edm::LogWarning("TauIsolationSelector") << "The assumption that there is a PFTau object for each candidate too failed for "
                                              << nAssumptionFailed << " of " << nCand << " candidates" << std::endl;
    }
  }
}

#endif
