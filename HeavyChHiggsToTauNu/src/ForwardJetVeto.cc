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
    fMetCut(iConfig.getUntrackedParameter<double>("METCut")),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    //fCount(eventCounter.addCounter(" ")),
    fEventWeight(eventWeight) {
    edm::Service<TFileService> fs;

    hForwJetEt = makeTH<TH1F>(*fs, "ForwJetEt", "ForwJetEt", 100, 0., 200.);
    hForwJetEta = makeTH<TH1F>(*fs, "ForwJetEta", "ForwJetEta", 100, -5., 5.);
    hMaxForwJetEt = makeTH<TH1F>(*fs, "MaxForwJetEt", "MaxForwJetEt", 100, 0., 200.);
    hEtSumCentral = makeTH<TH1F>(*fs, "EtSumCentral", "EtSumCentral", 100, 0., 1000.);
    hEtSumForward = makeTH<TH1F>(*fs, "EtSumForward", "EtSumForward", 100, 0., 1000.);
    hEtSumRatio = makeTH<TH1F>(*fs, "EtSumRatio", "EtSumRatio", 100, 0., 2.);
  }

  ForwardJetVeto::~ForwardJetVeto() {}

  ForwardJetVeto::Data ForwardJetVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& selectedjets) {
    bool passEvent = false;
   
    edm::Handle<edm::View<reco::MET> > metHandle;
    iEvent.getByLabel(fSrc_met, metHandle);
    edm::Ptr<reco::MET> met = metHandle->ptrAt(0);
   
    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(fSrc, hjets);

    const edm::PtrVector<pat::Jet>& jets(hjets->ptrVector());
    
    // Loop over selected jets
    double maxEt = 0.;
    double EtSumForward = 0.;
    double EtSumCentral = 0.;
    double EtSumRatio = -999;

    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      //      if ((**iter).et() < forwJetEtCut ) continue;
      if (fabs(iJet->eta()) < fEtaCut && iJet->pt() > fPtCut ) { 
	EtSumCentral += iJet->pt();
      }
      if (fabs(iJet->eta()) > fEtaCut && iJet->pt() > fPtCut ) { 
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

    // Add MET in the central sum
    if (met->et() > fMetCut )  EtSumCentral +=  met->et();
    if (EtSumCentral > 0) EtSumRatio = EtSumForward /EtSumCentral;
    hEtSumCentral->Fill(EtSumCentral, fEventWeight.getWeight());
    hEtSumForward->Fill(EtSumForward, fEventWeight.getWeight());
    hEtSumRatio->Fill(EtSumRatio, fEventWeight.getWeight());

    // Make cut
    passEvent = true; 
    if (maxEt > fForwJetEtCut)
      passEvent = false;

    return Data(this, passEvent);
  }
}
