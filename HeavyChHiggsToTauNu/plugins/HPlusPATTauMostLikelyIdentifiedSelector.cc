#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"

#include<memory>
#include<vector>

class HPlusPATTauMostLikelyIdentifiedSelector: public edm::EDProducer {
public:
  HPlusPATTauMostLikelyIdentifiedSelector(const edm::ParameterSet& iConfig):
    eventCounter(iConfig),
    eventWeight(iConfig),
    histoWrapper(eventWeight, "Debug"),
    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, histoWrapper),
    fTauSrc(fOneProngTauSelection.getSrc())
  {
    produces<std::vector<pat::Tau> >();
  }

  ~HPlusPATTauMostLikelyIdentifiedSelector() {}

private:
  void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fTauSrc, htaus);
    
    std::auto_ptr<std::vector<pat::Tau> > prod(new std::vector<pat::Tau>());
    if(!htaus->empty()) {
      prod->reserve(1);

      edm::PtrVector<pat::Tau> taus = htaus->ptrVector();
      edm::Ptr<pat::Tau> mostLikelyTau = fOneProngTauSelection.selectMostLikelyTau(taus);
      prod->push_back(*mostLikelyTau);
    }

    iEvent.put(prod);
  }

  void endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
    eventCounter.endLuminosityBlock(iBlock, iSetup);
  }
  void endJob() {
    eventCounter.endJob();
  }

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::HistoWrapper histoWrapper;
  HPlus::TauSelection fOneProngTauSelection;
  edm::InputTag fTauSrc;
};

DEFINE_FWK_MODULE( HPlusPATTauMostLikelyIdentifiedSelector );
