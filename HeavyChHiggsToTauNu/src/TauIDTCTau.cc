#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDTCTau.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "TH1F.h"

namespace HPlus {
  TauIDTCTau::TauIDTCTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, std::string label, TFileDirectory& myDir):
    TauIDBase(iConfig, eventCounter, eventWeight, label+"_TCTau", myDir)
  { }

  TauIDTCTau::~TauIDTCTau() { }

  bool TauIDTCTau::passDecayModeFinding(const edm::Ptr<pat::Tau>& tau) {
    fCounterPackager.incrementSubCount(fIDDecayModeFinding);
    // No decay mode finding equivalent in TCTau, always pass true
    return true;
  }

  bool TauIDTCTau::passLeadingTrackCuts(const edm::Ptr<pat::Tau> tau) {
    // Check that leading track exists
    if (tau->leadTrack().isNull()) return false;
    fCounterPackager.incrementSubCount(fIDLdgTrackExistsCut);
    // Leading track pt cut
    double myLdgTrackPt = tau->leadTrack()->pt();
    fCounterPackager.fill(fIDLdgTrackPtCut, myLdgTrackPt);
    if (!(myLdgTrackPt > fLeadTrkPtCut)) return false;
    fCounterPackager.incrementSubCount(fIDLdgTrackPtCut);
    // All cuts passed, return true
    return true;
  }

  bool TauIDTCTau::passNProngsCut(const edm::Ptr<pat::Tau> tau) {
    size_t myTrackCount = getNProngs(tau);
    fCounterPackager.fill(fIDNProngsCut, myTrackCount);
    if (!(myTrackCount == 1)) return false;
    fCounterPackager.incrementSubCount(fIDNProngsCut);
    // All cuts passed, return true
    return true;
  }
  
  size_t TauIDTCTau::getNProngs(const edm::Ptr<pat::Tau> tau) const {
    return tau->signalTracks().size();
  }

  bool TauIDTCTau::passRTauCut(const edm::Ptr<pat::Tau> tau) {
    double myRtauValue = getRtauValue(tau);
    hRtauVsEta->Fill(myRtauValue, tau->eta(), fEventWeight.getWeight());
    fCounterPackager.fill(fIDRTauCut, myRtauValue);
    if (!(myRtauValue > fRtauCut)) return false;
    fCounterPackager.incrementSubCount(fIDRTauCut);
    // All cuts passed, return true
    return true;
  }

  double TauIDTCTau::getRtauValue(const edm::Ptr<pat::Tau> tau) const {
    return tau->leadTrack()->p() / tau->p() - 1.0e-6; // value 1 goes in the bin below 1 in the histogram
  }
}
