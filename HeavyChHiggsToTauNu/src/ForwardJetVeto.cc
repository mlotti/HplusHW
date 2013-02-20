#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ForwardJetVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  ForwardJetVeto::Data::Data():
    fPassedEvent(false) {}
  ForwardJetVeto::Data::~Data() {}

  ForwardJetVeto::ForwardJetVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fForwJetEtaCut(iConfig.getUntrackedParameter<double>("ForwJetEtaCut")),
    fForwJetEtCut(iConfig.getUntrackedParameter<double>("ForwJetEtCut")),
    fEtSumRatioCut(iConfig.getUntrackedParameter<double>("EtSumRatioCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fForwardJetSubCount(eventCounter.addSubCounter("Forward jet veto","Forward jet cut")),
    fEtSumRatioSubCount(eventCounter.addSubCounter("Forward jet veto","EtSum(forward/central) cut")),
    fEtMetSumRatioSubCount(eventCounter.addSubCounter("Forward jet veto","EtMetSum(forward/central) cut")) {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("ForwardJetVeto");

    hForwJetEt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ForwJetEt", "ForwJetEt", 100, 0., 200.);
    hForwJetEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "ForwJetEta", "ForwJetEta", 100, -5., 5.);
    hMaxForwJetEt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MaxForwJetEt", "MaxForwJetEt", 100, 0., 100.);
    hEtSumCentral = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "EtSumCentral", "EtSumCentral", 100, 0., 1000.);
    hEtSumForward = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "EtSumForward", "EtSumForward", 100, 0., 1000.);
    hEtMetSumRatio = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "EtMetSumRatio", "EtMetSumRatio", 100, 0., 2.);
    hEtSumRatio = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "EtSumRatio", "EtSumRatio", 100, 0., 2.);
  }

  ForwardJetVeto::~ForwardJetVeto() {}

  ForwardJetVeto::Data ForwardJetVeto::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::MET>& met) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, met);
  }

  ForwardJetVeto::Data ForwardJetVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::MET>& met) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, met);
  }

  ForwardJetVeto::Data ForwardJetVeto::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::MET>& met) {
    Data output;

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
      if(fabs(iJet->eta()) > fForwJetEtaCut) hForwJetEt->Fill(iJet->pt());
      if (iJet->pt() > fForwJetEtCut ) hForwJetEta->Fill(iJet->eta());
      if (fabs(iJet->eta()) < fForwJetEtaCut ) continue;
      if (iJet->pt() > maxEt) {
	maxEt = iJet->pt();
      }
    }
    hMaxForwJetEt->Fill(maxEt);
    if (EtSumCentral > 0) EtSumRatio = EtSumForward /EtSumCentral;
    hEtSumRatio->Fill(EtSumRatio);
    // Add MET in the central sum
    EtSumCentral +=  met->et();
    if (EtSumCentral > 0) EtMetSumRatio = EtSumForward /EtSumCentral;
    hEtSumCentral->Fill(EtSumCentral);
    hEtSumForward->Fill(EtSumForward);
    hEtMetSumRatio->Fill(EtMetSumRatio);

    if (maxEt < fForwJetEtCut) increment(fForwardJetSubCount);
    if (EtSumRatio < fEtSumRatioCut) increment(fEtSumRatioSubCount);
    if (EtMetSumRatio < fEtSumRatioCut) increment(fEtMetSumRatioSubCount);
    // Make cut
  
    output.fPassedEvent = true;
    //    if (maxEt > fForwJetEtCut) passEvent = false;
  
    if( EtSumRatio > fEtSumRatioCut ) output.fPassedEvent = false;

    return output;
  }
}
