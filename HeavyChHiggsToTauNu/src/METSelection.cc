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
    hMet = fs->make<TH1F>("met", "met", 50, 0., 200.);
    hMetSignif = fs->make<TH1F>("metSignif", "metSignif", 50, 0., 500.);
    hMetSumEt  = fs->make<TH1F>("metSumEt", "metSumEt", 50, 0., 1500.);
    hMetDivSumEt = fs->make<TH1F>("hMetDivSumEt", "hMetDivSumEt", 50, 0., 1.);
    hMetDivSqrSumEt = fs->make<TH1F>("hMetDivSqrSumEt", "hMetDivSqrSumEt", 50, 0., 1.);
  }

  METSelection::~METSelection() {}

  bool METSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<reco::MET> > hmet;
    iEvent.getByLabel(fSrc, hmet);

    edm::Ptr<reco::MET> met = hmet->ptrAt(0);

    hMet->Fill(met->et());
    hMetSignif->Fill(met->significance());
    hMetSumEt->Fill(met->sumEt());
    double sumEt = met->sumEt();
    if(sumEt != 0){
        hMetDivSumEt->Fill(met->et()/sumEt);
        hMetDivSqrSumEt->Fill(met->et()/sumEt);
    }

    if(!(met->et() > fMetCut)) return false;

    increment(fMetCutCount);
    fSelectedMET = met;
    return true;
  }
}
