#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDPFTauBase.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  TauIDPFTauBase::TauIDPFTauBase(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, const std::string& baseLabel):
    TauIDBase(iConfig, eventCounter, eventWeight, baseLabel) {
  
  }

  TauIDPFTauBase::~TauIDPFTauBase() { }

  bool TauIDPFTauBase::passLeadingTrackCuts(const edm::Ptr<pat::Tau> tau) {
    // Check that leading track exists
    if (tau->leadPFChargedHadrCand().isNull()) return false;
    fCounterPackager.incrementSubCount(fIDLdgTrackExistsCut);
    // Leading track pt cut
    double myLdgTrackPt = tau->leadPFChargedHadrCand()->pt();
    fCounterPackager.fill(fIDLdgTrackPtCut, myLdgTrackPt);
    if (!(myLdgTrackPt > fLeadTrkPtCut)) return false;
    fCounterPackager.incrementSubCount(fIDLdgTrackPtCut);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDPFTauBase::passOneProngCut(const edm::Ptr<pat::Tau> tau) {
    size_t myTrackCount = tau->signalPFChargedHadrCands().size();
    //std::cout << "DEBUG: prong=" << tau->signalTracks().size() << " check=" << myTrackCount << std::endl;
    fCounterPackager.fill(fIDOneProngNumberCut, myTrackCount);
    if (!(myTrackCount == 1)) return false;
    fCounterPackager.incrementSubCount(fIDOneProngNumberCut);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDPFTauBase::passThreeProngCut(const edm::Ptr<pat::Tau> tau) {
    size_t myTrackCount = tau->signalPFChargedHadrCands().size();
    fCounterPackager.fill(fIDThreeProngNumberCut, myTrackCount);
    if (!(myTrackCount == 3)) return false;
    fCounterPackager.incrementSubCount(fIDThreeProngNumberCut);
    // All cuts passed, return true
    return true;
  }
    
  bool TauIDPFTauBase::passRTauCut(const edm::Ptr<pat::Tau> tau) {
    double myRtauValue = tau->leadPFChargedHadrCand()->pt() / tau->pt();
    hRtauVsEta->Fill(myRtauValue, tau->eta(), fEventWeight.getWeight());
    fCounterPackager.fill(fIDRTauCut, myRtauValue);
    if (!(myRtauValue > fRtauCut)) return false;
    fCounterPackager.incrementSubCount(fIDRTauCut);
    // All cuts passed, return true
    return true;
  }

  bool TauIDPFTauBase::passAntiRTauCut(const edm::Ptr<pat::Tau> tau) {
    double myRtauValue = tau->leadPFChargedHadrCand()->pt() / tau->pt();
    hRtauVsEta->Fill(myRtauValue, tau->eta(), fEventWeight.getWeight());
    fCounterPackager.fill(fIDRTauCut, myRtauValue);
    if (!(myRtauValue < fAntiRtauCut)) return false;
    fCounterPackager.incrementSubCount(fIDRTauCut);
    // All cuts passed, return true
    return true;
  }
  
  double TauIDPFTauBase::getRtauValue(const edm::Ptr<pat::Tau> tau) const {
    return tau->leadPFChargedHadrCand()->pt() / tau->pt();
  }
}
