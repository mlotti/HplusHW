#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {
  ForwardJetVeto::Data::Data(const ForwardJetVeto *forwardJetVeto, bool passedEvent):
    fForwardJetVeto(forwardJetVeto), fPassedEvent(passedEvent) {}
  ForwardJetVeto::Data::~Data() {}
  
  ForwardJetVeto::ForwardJetVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fSrc_met(iConfig.getUntrackedParameter<edm::InputTag>("src_met")),
    fForwJetEtaCut(iConfig.getUntrackedParameter<double>("ForwJetEtaCut")),
    fForwJetEtCut(iConfig.getUntrackedParameter<double>("ForwJetEtCut")),
    fEtSumRatioCut(iConfig.getUntrackedParameter<double>("EtSumRatioCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fForwardJetSubCount(eventCounter.addSubCounter("Forward jet veto","Forward jet cut")),
    fEtSumRatioSubCount(eventCounter.addSubCounter("Forward jet veto","EtSum(forward/central) cut")),
    fEtMetSumRatioSubCount(eventCounter.addSubCounter("Forward jet veto","EtMetSum(forward/central) cut")),
    //fCount(eventCounter.addCounter(" ")),
    fEventWeight(eventWeight) {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("ForwardJetVeto");

    hForwJetEt = makeTH<TH1F>(myDir, "ForwJetEt", "ForwJetEt", 100, 0., 200.);
    hForwJetEta = makeTH<TH1F>(myDir, "ForwJetEta", "ForwJetEta", 100, -5., 5.);
    hMaxForwJetEt = makeTH<TH1F>(myDir, "MaxForwJetEt", "MaxForwJetEt", 100, 0., 100.);
    hEtSumCentral = makeTH<TH1F>(myDir, "EtSumCentral", "EtSumCentral", 100, 0., 1000.);
    hEtSumForward = makeTH<TH1F>(myDir, "EtSumForward", "EtSumForward", 100, 0., 1000.);
    hEtMetSumRatio = makeTH<TH1F>(myDir, "EtMetSumRatio", "EtMetSumRatio", 100, 0., 2.);
    hEtSumRatio = makeTH<TH1F>(myDir, "EtSumRatio", "EtSumRatio", 100, 0., 2.);
  }

  ForwardJetVeto::~ForwardJetVeto() {}

  ForwardJetVeto::Data ForwardJetVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    bool passEvent = false;
   
    edm::Handle<edm::View<reco::MET> > metHandle;
    iEvent.getByLabel(fSrc_met, metHandle);
    edm::Ptr<reco::MET> met = metHandle->ptrAt(0);
   
    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(fSrc, hjets);

    const edm::PtrVector<pat::Jet>& jets(hjets->ptrVector());
    
    // Loop over jets
    double maxEt = 0.;
    double EtSumForward = 0.;
    double EtSumCentral = 0.;
    double EtSumRatio = -999;
    double EtMetSumRatio = -999;

    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      //      if ((**iter).et() < forwJetEtCut ) continue;
      if (fabs(iJet->eta()) < fForwJetEtaCut && iJet->pt() > fPtCut ) { 
	EtSumCentral += iJet->pt();
      }
      if (fabs(iJet->eta()) > fForwJetEtaCut && iJet->pt() > fForwJetEtCut ) { 
	EtSumForward += iJet->pt();
      }
      if(fabs(iJet->eta()) > fForwJetEtaCut) hForwJetEt->Fill(iJet->pt(), fEventWeight.getWeight());
      if (iJet->pt() > fForwJetEtCut ) hForwJetEta->Fill(iJet->eta(), fEventWeight.getWeight());
      if (fabs(iJet->eta()) < fForwJetEtaCut ) continue;
      if (iJet->pt() > maxEt) {
	maxEt = iJet->pt();
      }
    }
    hMaxForwJetEt->Fill(maxEt, fEventWeight.getWeight());
    if (EtSumCentral > 0) EtSumRatio = EtSumForward /EtSumCentral;
    hEtSumRatio->Fill(EtSumRatio, fEventWeight.getWeight());
    // Add MET in the central sum
    EtSumCentral +=  met->et();
    if (EtSumCentral > 0) EtMetSumRatio = EtSumForward /EtSumCentral;
    hEtSumCentral->Fill(EtSumCentral, fEventWeight.getWeight());
    hEtSumForward->Fill(EtSumForward, fEventWeight.getWeight());
    hEtMetSumRatio->Fill(EtMetSumRatio, fEventWeight.getWeight());

    if (maxEt < fForwJetEtCut) increment(fForwardJetSubCount);
    if (EtSumRatio < fEtSumRatioCut) increment(fEtSumRatioSubCount);
    if (EtMetSumRatio < fEtSumRatioCut) increment(fEtMetSumRatioSubCount);
    // Make cut
  
    passEvent = true; 
    //    if (maxEt > fForwJetEtCut) passEvent = false;
  
    if( EtSumRatio > fEtSumRatioCut ) passEvent = false;

    return Data(this, passEvent);
  }
}
