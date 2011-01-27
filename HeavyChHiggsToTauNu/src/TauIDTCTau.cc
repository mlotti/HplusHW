#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDTCTau.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "TH1F.h"

namespace HPlus {
  TauIDTCTau::TauIDTCTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    TauIDBase(iConfig, eventCounter, eventWeight, "TCTau")
  {
    edm::Service<TFileService> fs;

    // Initialize counter objects for tau isolation
    fIDIsolation = fCounterPackager.addSubCounter("TCTau", "Isolation", 0);
    // Histograms
    
    // Initialize rest counter objects 
    createSelectionCounterPackagesBeyondIsolation();
  }

  TauIDTCTau::~TauIDTCTau() { }

  bool TauIDTCTau::passLeadingTrackCuts(pat::Tau& tau) {
    // Check that leading track exists
    if (tau.leadTrack().isNull()) return false;
    fCounterPackager.incrementSubCount(fIDLdgTrackExistsCut);
    // Leading track pt cut
    double myLdgTrackPt = tau.leadTrack()->pt();
    fCounterPackager.fill(fIDLdgTrackPtCut, myLdgTrackPt);
    if (!(myLdgTrackPt > fLeadTrkPtCut)) return false;
    fCounterPackager.incrementSubCount(fIDLdgTrackPtCut);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDTCTau::passIsolation(pat::Tau& tau) {
    if (tau.tauID("byIsolation") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDIsolation);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDTCTau::passAntiIsolation(pat::Tau& tau) {
    if (tau.tauID("byIsolation") > 0.5) return false;
    fCounterPackager.incrementSubCount(fIDIsolation);
    // All cuts passed, return true
    return true;
  }

  bool TauIDTCTau::passRTauCut(pat::Tau& tau) {
    double myRtauValue = tau.leadTrack()->pt() / tau.pt();
    hRtauVsEta->Fill(myRtauValue, tau.eta(), fEventWeight.getWeight());
    fCounterPackager.fill(fIDRTauCut, myRtauValue);
    if (!(myRtauValue < fRtauCut)) return false;
    fCounterPackager.incrementSubCount(fIDRTauCut);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDTCTau::passAntiRTauCut(pat::Tau& tau) {
    double myRtauValue = tau.leadTrack()->pt() / tau.pt();
    hRtauVsEta->Fill(myRtauValue, tau.eta(), fEventWeight.getWeight());
    fCounterPackager.fill(fIDRTauCut, myRtauValue);
    if (!(myRtauValue > fAntiRtauCut)) return false;
    fCounterPackager.incrementSubCount(fIDRTauCut);
    // All cuts passed, return true
    return true;
  }

}
