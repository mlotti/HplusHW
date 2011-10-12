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
    fRawSrc(iConfig.getUntrackedParameter<edm::InputTag>("rawSrc")),
    fType1Src(iConfig.getUntrackedParameter<edm::InputTag>("type1Src")),
    fType2Src(iConfig.getUntrackedParameter<edm::InputTag>("type2Src")),
    fCaloSrc(iConfig.getUntrackedParameter<edm::InputTag>("caloSrc")),
    fTcSrc(iConfig.getUntrackedParameter<edm::InputTag>("tcSrc")),
    fMetCut(iConfig.getUntrackedParameter<double>("METCut")),
    fMetCutCount(eventCounter.addSubCounter(label+"_MET","MET cut")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(label);

    std::string select = iConfig.getUntrackedParameter<std::string>("select");
    if(select == "raw")
      fSelect = kRaw;
    else if(select == "type1")
      fSelect = kType1;
    else if(select == "type2")
      fSelect = kType2;
    else
      throw cms::Exception("Configuration") << "Invalid value for select '" << select << "', valid values are raw, type1, type2" << std::endl;
    
    hMet = makeTH<TH1F>(myDir, "met", "met", 400, 0., 400.);
    hMetSignif = makeTH<TH1F>(myDir, "metSignif", "metSignif", 100, 0., 50.);
    hMetSumEt  = makeTH<TH1F>(myDir, "metSumEt", "metSumEt", 50, 0., 1500.);
    hMetDivSumEt = makeTH<TH1F>(myDir, "hMetDivSumEt", "hMetDivSumEt", 50, 0., 1.);
    hMetDivSqrSumEt = makeTH<TH1F>(myDir, "hMetDivSqrSumEt", "hMetDivSqrSumEt", 50, 0., 1.);
  }

  METSelection::~METSelection() {}

  METSelection::Data METSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    bool passEvent = false;
    edm::Handle<edm::View<reco::MET> > hrawmet;
    iEvent.getByLabel(fRawSrc, hrawmet);

    edm::Handle<edm::View<reco::MET> > htype1met;
    iEvent.getByLabel(fType1Src, htype1met);

    edm::Handle<edm::View<reco::MET> > htype2met;
    iEvent.getByLabel(fType2Src, htype2met);

    edm::Handle<edm::View<reco::MET> > hcalomet;
    iEvent.getByLabel(fCaloSrc, hcalomet);

    edm::Handle<edm::View<reco::MET> > htcmet;
    iEvent.getByLabel(fTcSrc, htcmet);

    // Reset then handles
    fRawMET = edm::Ptr<reco::MET>();
    fType1MET = edm::Ptr<reco::MET>();
    fType2MET = edm::Ptr<reco::MET>();
    fCaloMET = edm::Ptr<reco::MET>();
    fTcMET = edm::Ptr<reco::MET>();

    // Set the handles, if object available
    if(hrawmet.isValid())
      fRawMET = hrawmet->ptrAt(0);
    if(htype1met.isValid())
      fType1MET = htype1met->ptrAt(0);
    if(htype2met.isValid())
      fType2MET = htype2met->ptrAt(0);
    if(hcalomet.isValid())
      fCaloMET = hcalomet->ptrAt(0);
    if(htcmet.isValid())
      fTcMET = htcmet->ptrAt(0);

    // Do the selection
    edm::Ptr<reco::MET> met;
    if(fSelect == kRaw)
      met = hrawmet->ptrAt(0);
    else if(fSelect == kType1)
      met = htype1met->ptrAt(0);
    else if(fSelect == kType2)
      met = htype2met->ptrAt(0);
    else
      throw cms::Exception("LogicError") << "This should never happen at " << __FILE__ << ":" << __LINE__ << std::endl;

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
