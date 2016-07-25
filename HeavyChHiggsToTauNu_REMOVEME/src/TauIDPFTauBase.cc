#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDPFTauBase.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "DataFormats/TauReco/interface/PFTauDecayMode.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  TauIDPFTauBase::TauIDPFTauBase(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper, const std::string& baseLabel, TFileDirectory& myDir):
    TauIDBase(iConfig, eventCounter, histoWrapper, baseLabel, myDir) {
    hRtauOneProngZeroPiZero = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, fMyDir, "TauID_Rtau_DecayModeOneProng_ZeroPiZero", "TauID_Rtau_DecayModeOneProng_ZeroPiZero;Rtau 1-prong with 0 #pi^[0];N_{jets}", 60, 0.0, 1.2);
    hRtauOneProngOnePiZero = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, fMyDir, "TauID_Rtau_DecayModeOneProng_OnePiZero", "TauID_Rtau_DecayModeOneProng_OnePiZero;Rtau 1-prong with 1 #pi^[0];N_{jets}", 60, 0.0, 1.2);
    hRtauOneProngTwoPiZero = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, fMyDir, "TauID_Rtau_DecayModeOneProng_TwoPiZero", "TauID_Rtau_DecayModeOneProng_TwoPiZero;Rtau 1-prong with 2 #pi^[0];N_{jets}", 60, 0.0, 1.2);
    hRtauOneProngOther = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, fMyDir, "TauID_Rtau_DecayModeOneProng_Other", "TauID_Rtau_DecayModeOneProng_Other;Rtau 1-prong other;N_{jets}", 60, 0.0, 1.2);
    hRtauThreeProngZeroPiZero = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, fMyDir, "TauID_Rtau_DecayModeThreeProng_ZeroPiZero", "TauID_Rtau_DecayModeThreeProng_ZeroPiZero;Rtau 3-prong with 0 #pi^[0];N_{jets}", 60, 0.0, 1.2);
    hRtauThreeProngOnePiZero = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, fMyDir, "TauID_Rtau_DecayModeThreeProng_OnePiZero", "TauID_Rtau_DecayModeThreeProng_OnePiZero;Rtau 3-prong with 1 #pi^[0];N_{jets}", 60, 0.0, 1.2);
    hRtauThreeProngOther = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, fMyDir, "TauID_Rtau_DecayModeThreeProng_Other", "TauID_Rtau_DecayModeThreeProng_Other;Rtau 3-prong other;;N_{jets}", 60, 0.0, 1.2);
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
  
  bool TauIDPFTauBase::passNProngsCut(const edm::Ptr<pat::Tau> tau) {
    size_t myTrackCount = getNProngs(tau);
    //std::cout << "DEBUG: prong=" << tau->signalTracks().size() << " check=" << myTrackCount << std::endl;
    fCounterPackager.fill(fIDNProngsCut, myTrackCount);
    if (!(myTrackCount == fProngCount)) {
      if (fProngCount == 13) { // 1 or 3 prong
        if (myTrackCount != 1 && myTrackCount != 3) {
          return false;
        }
      } else {
        return false;
      }
    }
    fCounterPackager.incrementSubCount(fIDNProngsCut);
    // All cuts passed, return true
    return true;
  }
  
  size_t TauIDPFTauBase::getNProngs(const edm::Ptr< pat::Tau > tau) const {
    return tau->signalPFChargedHadrCands().size();
  }
  
  bool TauIDPFTauBase::passRTauCut(const edm::Ptr<pat::Tau> tau) {
    double myRtauValue = getRtauValue(tau);
    hRtauVsEta->Fill(myRtauValue, tau->eta());
    fCounterPackager.fill(fIDRTauCut, myRtauValue);
    // Fill Rtau plots based on decaymode
    if (tau->signalPFChargedHadrCands().size() == 1) {
      if (tau->decayMode() == reco::PFTauDecayMode::tauDecay1ChargedPion0PiZero)
        hRtauOneProngZeroPiZero->Fill(myRtauValue);
      else if (tau->decayMode() == reco::PFTauDecayMode::tauDecay1ChargedPion1PiZero)
        hRtauOneProngOnePiZero->Fill(myRtauValue);
      else if (tau->decayMode() == reco::PFTauDecayMode::tauDecay1ChargedPion2PiZero)
        hRtauOneProngTwoPiZero->Fill(myRtauValue);
      else 
        hRtauOneProngOther->Fill(myRtauValue);
    } else if (tau->signalPFChargedHadrCands().size() == 3) {
      if (tau->decayMode() == reco::PFTauDecayMode::tauDecay3ChargedPion0PiZero)
        hRtauThreeProngZeroPiZero->Fill(myRtauValue);
      else if (tau->decayMode() == reco::PFTauDecayMode::tauDecay3ChargedPion1PiZero)
        hRtauThreeProngOnePiZero->Fill(myRtauValue);
      else 
        hRtauThreeProngOther->Fill(myRtauValue);
    }
    // Make cut
    if (!(myRtauValue > fRtauCut)) return false;
    fCounterPackager.incrementSubCount(fIDRTauCut);
    // All cuts passed, return true
    return true;
  }
  
  double TauIDPFTauBase::getRtauValue(const edm::Ptr<pat::Tau> tau) const {
    return tau->leadPFChargedHadrCand()->p() / tau->p() - 1.0e-6; // value 1 goes in the bin below 1 in the histogram
  }
}
