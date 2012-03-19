#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDBase.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include <sstream>
#include <iomanip>

namespace HPlus {
  TauIDBase::TauIDBase(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, const std::string& baseLabel, TFileDirectory& myDir):
    fMyDir(myDir),
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fLeadTrkPtCut(iConfig.getUntrackedParameter<double>("leadingTrackPtCut")),
    fAgainstElectronDiscriminator(iConfig.getUntrackedParameter<std::string>("againstElectronDiscriminator")),
    fAgainstMuonDiscriminator(iConfig.getUntrackedParameter<std::string>("againstMuonDiscriminator")),
    fProngCount(iConfig.getUntrackedParameter<uint32_t>("nprongs")),
    fIsolationDiscriminator(iConfig.getUntrackedParameter<std::string>("isolationDiscriminator")),
    fIsolationDiscriminatorContinuousCutPoint(iConfig.getUntrackedParameter<double>("isolationDiscriminatorContinuousCutPoint")),
    fRtauCut(iConfig.getUntrackedParameter<double>("rtauCut")),
    fCounterPackager(eventCounter, eventWeight),
    fEventWeight(eventWeight)
  {
    // contstuct base label suffix
    std::stringstream mySuffix;
    mySuffix << baseLabel << "_" << fIsolationDiscriminator;
    if (fIsolationDiscriminatorContinuousCutPoint > 0)
      mySuffix << std::setprecision(2) << fIsolationDiscriminatorContinuousCutPoint;
    if (fRtauCut > 0)
      mySuffix << "_Rtau" << std::setprecision(2) << fRtauCut;
    else
      mySuffix << "_noRtau";
    fBaseLabel = mySuffix.str();
        
    // Histograms
    hEtaTauCands_nocut = makeTH<TH1F>(fMyDir,
      "hEtaTauCands_nocuts",
      "hEtaTauCands_nocuts;#tau #eta;N_{jets} / 0.1",60, -3., 3.);
    hEtaTauCands_ptcut = makeTH<TH1F>(fMyDir,
      "hEtaTauCands_ptcut",
      "hEtaTauCands_ptcut;#tau #eta;N_{jets} / 0.1",60, -3., 3.);
    
    // Initialize counter objects for tau candidate selection
    fIDAllTauCandidates = fCounterPackager.addSubCounter(baseLabel, "AllTauCandidates", 0);
    fIDDecayModeFinding = fCounterPackager.addSubCounter(baseLabel, "DecayModeFinding", 0);
    fIDJetPtCut = fCounterPackager.addSubCounter(baseLabel, "TauJetPt",
      makeTH<TH1F>(fMyDir, "TauCand_JetPt", "TauJetPt;#tau jet p_{T}, GeV/c;N_{jets} / 2 GeV/c", 100, 0., 200.));
    fIDJetEtaCut = fCounterPackager.addSubCounter(baseLabel, "TauJetEta",
      makeTH<TH1F>(fMyDir, "TauCand_JetEta", "TauJetEta;#tau jet #eta;N_{jets} / 0.1", 60, -3., 3.));
    fIDLdgTrackExistsCut = fCounterPackager.addSubCounter(baseLabel, "TauLdgTrackExists", 0);
    fIDLdgTrackPtCut = fCounterPackager.addSubCounter(baseLabel, "TauLdgTrackPtCut",
      makeTH<TH1F>(fMyDir, "TauCand_LdgTrackPtCut", "TauLdgTrackPtCut;#tau leading track, GeV/c; N_{jets} / 2 GeV/c", 100, 0., 200.));
    fIDECALFiducialCutCracksOnly = fCounterPackager.addSubCounter(baseLabel, "TauECALFiducialCutsCracks", 0);
    fIDECALFiducialCut = fCounterPackager.addSubCounter(baseLabel, "TauECALFiducialCutsCracksAndGap", 0);
    fIDAgainstElectronCut = fCounterPackager.addSubCounter(baseLabel, "TauAgainstElectronCut", 0);
    fIDAgainstMuonCut = fCounterPackager.addSubCounter(baseLabel, "TauAgainstMuonCut", 0);
    // Initialize counter objects for tau identification
    fIDIsolationCut = fCounterPackager.addSubCounter(baseLabel, "TauIsolation", 0);
    fIDNProngsCut = fCounterPackager.addSubCounter(baseLabel, "TauProngCut",
      makeTH<TH1F>(fMyDir, "TauID_NProngsCut", "TauNProngsCut;N_{#tau prong};N_{jets}", 10, 0., 10.));
    fIDRTauCut = fCounterPackager.addSubCounter(baseLabel, "TauRtauCut",
      makeTH<TH1F>(fMyDir, "TauID_RtauCut", "TauRtauCut;R_{#tau}=p^{ldg.track}/E^{vis.#tau jet};N_{jets} / 0.02", 60, 0., 1.2));
    // Histograms
    hRtauVsEta = makeTH<TH2F>(fMyDir, "TauID_RtauDetail_RtauVsEta", "RtauVsEta;R_{#tau};#tau eta", 60, 0.0, 1.2, 60, -3., 3.); // FIXME: check if this is necessary
  }

  TauIDBase::~TauIDBase() { }

  void TauIDBase::incrementAllCandidates() {
    fCounterPackager.incrementSubCount(fIDAllTauCandidates);
  }

  bool TauIDBase::passKinematicSelection(const edm::Ptr<pat::Tau> tau) {
    // Jet pt cut
    double myJetPt = tau->pt();
    double myJetEta = tau->eta();
    fCounterPackager.fill(fIDJetPtCut, myJetPt);
    hEtaTauCands_nocut->Fill(myJetEta, fEventWeight.getWeight());
    if(!(myJetPt > fPtCut)) return false;
    fCounterPackager.incrementSubCount(fIDJetPtCut);
    hEtaTauCands_ptcut->Fill(myJetEta, fEventWeight.getWeight());
    // Jet eta cut
    fCounterPackager.fill(fIDJetEtaCut, myJetEta);
    if(!(std::abs(myJetEta) < fEtaCut)) return false;
    fCounterPackager.incrementSubCount(fIDJetEtaCut);
    // All cuts passed, return true
    return true;
  }

  bool TauIDBase::passTauCandidateEAndMuVetoCuts(const edm::Ptr<pat::Tau> tau) {
    // Electron veto
    if (tau->tauID(fAgainstElectronDiscriminator) < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDAgainstElectronCut);
    // Muon veto
    if (tau->tauID(fAgainstMuonDiscriminator) < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDAgainstMuonCut);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDBase::passIsolation(const edm::Ptr<pat::Tau> tau) {
    // If no continuous cut point was set, set the default cut point for discrete discriminator
    if (fIsolationDiscriminatorContinuousCutPoint < 0)
      if (tau->tauID(fIsolationDiscriminator) < 0.5) return false;
    else if (tau->tauID(fIsolationDiscriminator) > fIsolationDiscriminatorContinuousCutPoint) return false;
    fCounterPackager.incrementSubCount(fIDIsolationCut);
    return true;
  }
  
  bool TauIDBase::passAntiIsolation(const edm::Ptr<pat::Tau> tau) {
    if (fIsolationDiscriminatorContinuousCutPoint < 0)
      if (tau->tauID(fIsolationDiscriminator) > 0.5) return false;
    else if (tau->tauID(fIsolationDiscriminator) < fIsolationDiscriminatorContinuousCutPoint) return false;
    fCounterPackager.incrementSubCount(fIDIsolationCut);
    return true;
  }

  bool TauIDBase::passECALFiducialCuts(const edm::Ptr<pat::Tau> tau) {
    double myEta = std::abs(tau->eta());
    // true, if eta is in ECAL crack
    bool myECALCrackStatus = (myEta < 0.018 ||
                              (myEta>0.423 && myEta<0.461) ||
                              (myEta>0.770 && myEta<0.806) ||
                              (myEta>1.127 && myEta<1.163));
    if (myECALCrackStatus) return false;
    fCounterPackager.incrementSubCount(fIDECALFiducialCutCracksOnly);
    // true, if eta is in ECAL gap
    bool myECALGapStatus = (myEta>1.460 && myEta<1.558);
    if (myECALGapStatus) return false;
    fCounterPackager.incrementSubCount(fIDECALFiducialCut);
    // All cuts passed, return true
    return true;
  }

  void TauIDBase::reset() {
    fCounterPackager.reset();
  }
  
  void TauIDBase::updatePassedCounters() {
    fCounterPackager.incrementPassedCounters();
  }
}
