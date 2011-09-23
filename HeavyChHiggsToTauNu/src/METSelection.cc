#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {
  METSelection::Data::Data(const METSelection *metSelection, bool passedEvent):
    fMETSelection(metSelection), fPassedEvent(passedEvent) {}
  METSelection::Data::~Data() {}
  
  METSelection::METSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, std::string label):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fMetCut(iConfig.getUntrackedParameter<double>("METCut")),
    fMetCutCount(eventCounter.addSubCounter(label+"_MET","MET cut")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(label);
    
    hMet = makeTH<TH1F>(myDir, "met", "met", 400, 0., 400.);
    hMetSignif = makeTH<TH1F>(myDir, "metSignif", "metSignif", 100, 0., 50.);
    hMetSumEt  = makeTH<TH1F>(myDir, "metSumEt", "metSumEt", 50, 0., 1500.);
    hMetDivSumEt = makeTH<TH1F>(myDir, "hMetDivSumEt", "hMetDivSumEt", 50, 0., 1.);
    hMetDivSqrSumEt = makeTH<TH1F>(myDir, "hMetDivSqrSumEt", "hMetDivSqrSumEt", 50, 0., 1.);
  }

  METSelection::~METSelection() {}

  METSelection::Data METSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    bool passEvent = false;
    edm::Handle<edm::View<reco::MET> > hmet;
    iEvent.getByLabel(fSrc, hmet);

    edm::Ptr<reco::MET> met = hmet->ptrAt(0);

    hMet->Fill(met->et(), fEventWeight.getWeight());
    hMetSignif->Fill(met->significance(), fEventWeight.getWeight());
    hMetSumEt->Fill(met->sumEt(), fEventWeight.getWeight());
    double sumEt = met->sumEt();
    if(sumEt != 0){
        hMetDivSumEt->Fill(met->et()/sumEt, fEventWeight.getWeight());
        hMetDivSqrSumEt->Fill(met->et()/sumEt, fEventWeight.getWeight());
    }

    if(met->et() > fMetCut) {
      passEvent = true;
      increment(fMetCutCount);
    }
    fSelectedMET = met;
    
    return Data(this, passEvent);
  }
}
