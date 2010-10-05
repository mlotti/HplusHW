#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {

  METSelection::METSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fMetCut(iConfig.getUntrackedParameter<double>("METCut")),
    fMetCutCount(eventCounter.addCounter("MET cut"))
  {
    edm::Service<TFileService> fs;
    hMet = fs->make<TH1F>("met", "met", 100, 0., 200.);
  }

  METSelection::~METSelection() {}

  bool METSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<reco::MET> > hmet;
    iEvent.getByLabel(fSrc, hmet);

    edm::Ptr<reco::MET> met = hmet->ptrAt(0);

    hMet->Fill(met->et());
    if(!(met->et() > fMetCut)) return false;

    increment(fMetCutCount);
    fSelectedMET = met;
    return true;
  }
}
