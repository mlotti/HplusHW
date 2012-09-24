#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauEmbeddingMuonIsolationQuantifier.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h" 

#include <cmath>

// FIXME: hard-coded InputTags are bad, should be delivered via configuration
namespace HPlus {
  //TauEmbeddingMuonIsolationQuantifier::TauEmbeddingMuonIsolationQuantifier(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
  //fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
  TauEmbeddingMuonIsolationQuantifier::TauEmbeddingMuonIsolationQuantifier(HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper) {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("TauEmbeddingMuonIsolationQuantifier");
    hChargedIsoPtSum = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "chargedIsoPtSum", "chargedIsoPtSum;chargedIsoPtSum p_{T}, GeV/c;Events / 0.1 GeV/c", 100., 0., 10.);
    hGammaIsoPtSum = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "gammaIsoPtSum", "gammaIsoPtSum;gammaIsoPtSum p_{T}, GeV/c;Events / 0.1 GeV/c", 100., 0., 10.);
    hChargedPUIsoPtSum = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "chargedPUIsoPtSum", "chargedPUIsoPtSum;chargedPUIsoPtSum p_{T}, GeV/c;Events / 0.1 GeV/c", 100., 0., 10.);
    hTotalIsoPtSum = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "totalIsoPtSum", "totalIsoPtSum;totalIsoPtSum p_{T}, GeV/c;Events / 0.1 GeV/c", 100., 0., 10.);
    hKParam = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "MaxKParameter", "MaxKParameter;Max k parameter;Events", 100., 0., 1.);
    hChargedIsoPtSumAfterJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "chargedIsoPtSumAfterJets", "chargedIsoPtSumAfterJets;chargedIsoPtSum p_{T}, GeV/c;Events / 0.1 GeV/c", 100., 0., 10.);
    hTotalIsoPtSumAfterJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "totalIsoPtSumAfterJets", "totalIsoPtSumAfterJets;totalIsoPtSumAfterJets p_{T}, GeV/c;Events / 0.1 GeV/c", 100., 0., 10.);
    hKParamAfterJets = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "MaxKParameterAfterJets", "MaxKParameterAfterJets;Max k parameter;Events", 100., 0., 1.);
 }

  TauEmbeddingMuonIsolationQuantifier::~TauEmbeddingMuonIsolationQuantifier() {}

  void TauEmbeddingMuonIsolationQuantifier::analyzeAfterTrigger(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<pat::Muon> > myMuonHandle;
    iEvent.getByLabel("patMuonsUserOnTheFlyIso", myMuonHandle);
    edm::PtrVector<pat::Muon> muons = myMuonHandle->ptrVector();
    // Loop over all Muons
    for(edm::PtrVector<pat::Muon>::const_iterator iMuon = muons.begin(); iMuon != muons.end(); ++iMuon) {
      double muPFIsoValuePU04 = (*iMuon)->userFloat("ontheflyiso_pfPUChargedHadrons");
      double muPFIsoValueCharged04 = (*iMuon)->userFloat("ontheflyiso_pfChargedHadrons");
      double muPFIsoValueGamma04 = (*iMuon)->userFloat("ontheflyiso_pfPhotons");
      hChargedIsoPtSum->Fill(muPFIsoValueCharged04);
      hGammaIsoPtSum->Fill(muPFIsoValueGamma04);
      hChargedPUIsoPtSum->Fill(muPFIsoValuePU04);
      // Calculate k for which isolation is passed
      if (muPFIsoValueCharged04 < 1.0) {
        hKParamAfterJets->Fill(getMaxK(muPFIsoValueCharged04, muPFIsoValueGamma04, muPFIsoValuePU04));
      }
      // Calculate total isolation
      hTotalIsoPtSum->Fill(getTotalIsolationPt(muPFIsoValueCharged04, muPFIsoValueGamma04, muPFIsoValuePU04, 0.5));
    }
  }

  void TauEmbeddingMuonIsolationQuantifier::analyzeAfterJets(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<pat::Muon> > myMuonHandle;
    iEvent.getByLabel("patMuonsUserOnTheFlyIso", myMuonHandle);
    edm::PtrVector<pat::Muon> muons = myMuonHandle->ptrVector();
    // Loop over all Muons
    for(edm::PtrVector<pat::Muon>::const_iterator iMuon = muons.begin(); iMuon != muons.end(); ++iMuon) {
      double muPFIsoValuePU04 = (*iMuon)->userFloat("ontheflyiso_pfPUChargedHadrons");
      double muPFIsoValueCharged04 = (*iMuon)->userFloat("ontheflyiso_pfChargedHadrons");
      double muPFIsoValueGamma04 = (*iMuon)->userFloat("ontheflyiso_pfPhotons");
      // Calculate k for which isolation is passed
      if (muPFIsoValueCharged04 < 1.0) {
        hKParamAfterJets->Fill(getMaxK(muPFIsoValueCharged04, muPFIsoValueGamma04, muPFIsoValuePU04));
      }
      // Calculate total isolation
      hChargedIsoPtSumAfterJets->Fill(muPFIsoValueCharged04);
      hTotalIsoPtSumAfterJets->Fill(getTotalIsolationPt(muPFIsoValueCharged04, muPFIsoValueGamma04, muPFIsoValuePU04, 0.5));
    }
  }

  double TauEmbeddingMuonIsolationQuantifier::getTotalIsolationPt(double charged, double gamma, double puCharged, double k) {
    double myDeltaBeta = gamma - k*puCharged;
    if (myDeltaBeta < 0)
      myDeltaBeta = 0;
    return charged+myDeltaBeta;
  }

  double TauEmbeddingMuonIsolationQuantifier::getMaxK(double charged, double gamma, double puCharged) {
    double kParameter = 0.0;
    if (puCharged) {
      kParameter = (charged+gamma-1.0) / puCharged;
      if (kParameter < 0.0)
        kParameter = 0.0;
    }
    return kParameter;
  }


}
