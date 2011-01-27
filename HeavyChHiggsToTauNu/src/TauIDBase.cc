#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDBase.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  TauIDBase::TauIDBase(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, const std::string& baseLabel):
    fPtCut(iConfig.getUntrackedParameter<double>("ptCut")),
    fEtaCut(iConfig.getUntrackedParameter<double>("etaCut")),
    fLeadTrkPtCut(iConfig.getUntrackedParameter<double>("leadingTrackPtCut")),
    fRtauCut(iConfig.getUntrackedParameter<double>("rtauCut")),
    fAntiRtauCut(iConfig.getUntrackedParameter<double>("antiRtauCut")),
    fInvMassCut(iConfig.getUntrackedParameter<double>("invMassCut")),
    fCounterPackager(eventCounter, eventWeight),
    fEventWeight(eventWeight),
    fBaseLabel(baseLabel)
  {
    edm::Service<TFileService> fs;
    
    // Initialize counter objects for tau candidate selection
    fIDAllTauCandidates = fCounterPackager.addSubCounter(baseLabel, "AllTauCandidates", 0);
    fIDJetPtCut = fCounterPackager.addSubCounter(baseLabel, "TauJetPt",
      makeTH<TH1F>(*fs, "TauJetPt", "TauJetPt;#tau jet p_{T}, GeV/c;N_{jets} / 2 GeV/c", 100, 0., 200.));
    fIDJetEtaCut = fCounterPackager.addSubCounter(baseLabel, "TauJetEta",
      makeTH<TH1F>(*fs, "TauJetEta", "TauJetEta;#tau jet #eta;N_{jets} / 0.1", 60, -3., 3.));
    fIDLdgTrackExistsCut = fCounterPackager.addSubCounter(baseLabel, "TauLdgTrackExists", 0);
    fIDLdgTrackPtCut = fCounterPackager.addSubCounter(baseLabel, "TauLdgTrackPtCut",
      makeTH<TH1F>(*fs, "TauLdgTrackPtCut", "TauLdgTrackPtCut;#tau leading track, GeV/c; N_{jets} / 2 GeV/c", 100, 0., 200.));
    fIDAgainstElectronCut = fCounterPackager.addSubCounter(baseLabel, "TauAgainstElectronCut", 0);
    fIDAgainstMuonCut = fCounterPackager.addSubCounter(baseLabel, "TauAgainstMuonCut", 0);
    // Initialize counter objects for tau identification
    fIDOneProngNumberCut = -1;
    fIDThreeProngNumberCut = -1;
    fIDChargeCut = -1; 
    fIDRTauCut = -1;
    fIDInvMassCut = -1;
    fIDDeltaECut = -1; 
    fIDFlightpathCut = -1;
    // Histograms
    hRtauVsEta = makeTH<TH2F>(*fs, "TauEtaVsRtau", "TauEtaVsRtau;R_{#tau};#tau eta", 60, -3., 3., 20, 0., 200.);
    /*
    hPtAfterTauSelCuts = makeTH<TH1F>(*fs, "tau_pt_afterTauSelCuts", "tau_pt_afterTauSelCuts", 100, 0., 200.);
    hEtaAfterTauSelCuts = makeTH<TH1F>(*fs, "tau_eta_afterTauSelCuts", "tau_eta_afterTauSelCuts", 60, -3., 3.);
    hEtaRtau = makeTH<TH1F>(*fs, "tau_eta_Rtau", "tau_eta_Rtau", 60, -3., 3.);
    hLeadTrkPt = );
    hIsolTrkPt = makeTH<TH1F>(*fs, "tau_isoltrk_pt", "tau_isoltrk_pt", 100, 0., 20.);
    hIsolTrkPtSum = makeTH<TH1F>(*fs, "tau_isoltrk_ptsum", "tau_isoltrk_ptsum", 100, 0., 20.);
    hIsolTrkPtSumVsPtCut = makeTH<TH2F>(*fs, "tau_isoltrk_ptsum_vs_ptcut", "tau_isoltrk_ptsum_vs_ptcut", 6, 0.45, 1.05, 100, 0., 20.);
    hNIsolTrksVsPtCut = makeTH<TH2F>(*fs, "tau_ntrks_vs_ptcut", "tau_ntrks_vs_ptcut", 6, 0.45, 1.05,10,0.,10.);
    hIsolMaxTrkPt = makeTH<TH1F>(*fs, "tau_isomaxltrk_pt", "tau_isolmaxtrk_pt", 100, 0., 20.);
    hnProngs = 
    hRtau = 
    hDeltaE = 
    hFlightPathSignif = 
    hInvMass = 
    hbyTaNC = makeTH<TH1F>(*fs, "tau_TaNC", "tau_TaNC", 100, 0., 1.);
    */
  }

  TauIDBase::~TauIDBase() { }

  void TauIDBase::createSelectionCounterPackagesBeyondIsolation() {
    edm::Service<TFileService> fs;
    fIDOneProngNumberCut = fCounterPackager.addSubCounter(fBaseLabel, "TauOneProngCut",
      makeTH<TH1F>(*fs, "TauOneProngNumberCut", "TauOneProngNumberCut;N_{#tau prong};N_{jets}", 10, 0., 10.));
    fIDThreeProngNumberCut = fCounterPackager.addSubCounter(fBaseLabel, "TauThreeProngCut",
      makeTH<TH1F>(*fs, "TauThreeProngNumberCut", "TauThreeProngNumberCut;N_{#tau prong};N_{jets}", 10, 0., 10.));
    fIDChargeCut = fCounterPackager.addSubCounter(fBaseLabel, "TauChargeCut",
      makeTH<TH1F>(*fs, "TauChargeCut", "TauChargeCut;#tau charge;N_{jets}", 7, -3., 4.));
    fIDRTauCut = fCounterPackager.addSubCounter(fBaseLabel, "TauRtauCut",
      makeTH<TH1F>(*fs, "TauRtauCut", "TauRtauCut;R_{#tau}=p^{ldg.track}/E^{vis.#tau jet};N_{jets} / 0.02", 60, 0., 1.2));
    fIDInvMassCut = fCounterPackager.addSubCounter(fBaseLabel, "TauInvMassCut",
      makeTH<TH1F>(*fs, "TauInvMassCut", "TauInvMassCut;m_{vis.#tau}, GeV/c^{2};N_{jets} / 0.1 GeV/c^{2}", 60, 0., 6.));
    fIDDeltaECut = fCounterPackager.addSubCounter(fBaseLabel, "TauDeltaECut",
      makeTH<TH1F>(*fs, "TauDeltaECut", "TauDeltaECut;#tau #DeltaE;N_{jets} / 0.02", 100, -1., 1.));
    fIDFlightpathCut = fCounterPackager.addSubCounter(fBaseLabel, "TauFlightpathCut",
      makeTH<TH1F>(*fs, "TauFlightpathCut", "TauFlightpathCut;#tau flight path signif.;N_{jets} / 0.2", 75, -5., 10));
  }

  bool TauIDBase::passTauCandidateSelection(const edm::Ptr<pat::Tau> tau) {
    fCounterPackager.incrementSubCount(fIDAllTauCandidates);
    // Jet pt cut
    double myJetPt = tau->pt();
    fCounterPackager.fill(fIDJetPtCut, myJetPt);
    if(!(myJetPt > fPtCut)) return false;
    fCounterPackager.incrementSubCount(fIDJetPtCut);
    // Jet eta cut
    double myJetEta = tau->eta();
    fCounterPackager.fill(fIDJetEtaCut, myJetEta);
    if(!(std::abs(myJetEta) < fEtaCut)) return false;
    fCounterPackager.incrementSubCount(fIDJetEtaCut);
    // All cuts passed, return true
    return true;
  }

  bool TauIDBase::passTauCandidateEAndMuVetoCuts(const edm::Ptr<pat::Tau> tau) {
    // Electron veto
    if(tau->tauID("againstElectron") < 0.5 ) return false;
    fCounterPackager.incrementSubCount(fIDAgainstElectronCut);
    // Muon veto
    if(tau->tauID("againstMuon") < 0.5 ) return false;
    fCounterPackager.incrementSubCount(fIDAgainstMuonCut);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDBase::passOneProngCut(const edm::Ptr<pat::Tau> tau) {
    fCounterPackager.fill(fIDOneProngNumberCut, tau->tauID("HChTauIDnProngsCont"));
    if (tau->tauID("HChTauID1Prong") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDOneProngNumberCut);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDBase::passThreeProngCut(const edm::Ptr<pat::Tau> tau) {
    fCounterPackager.fill(fIDThreeProngNumberCut, tau->tauID("HChTauIDnProngsCont"));
    if (tau->tauID("HChTauID3Prong") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDThreeProngNumberCut);
    // All cuts passed, return true
    return true;
  }

  bool TauIDBase::passChargeCut(const edm::Ptr<pat::Tau> tau) {
    // FIXME: add histogramming
    if (tau->tauID("HChTauIDcharge") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDChargeCut);
    // All cuts passed, return true
    return true;
  }

  bool TauIDBase::passInvMassCut(const edm::Ptr<pat::Tau> tau) {
    fCounterPackager.fill(fIDInvMassCut, tau->tauID("HChTauIDInvMassCont"));
    if (tau->tauID("HChTauIDInvMass") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDInvMassCut);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDBase::passDeltaECut(const edm::Ptr<pat::Tau> tau) {
    fCounterPackager.fill(fIDDeltaECut, tau->tauID("HChTauIDDeltaECont"));
    if (tau->tauID("HChTauIDDeltaE") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDDeltaECut);
    // All cuts passed, return true
    return true;
  }
  
  bool TauIDBase::passFlightpathCut(const edm::Ptr<pat::Tau> tau) {
    fCounterPackager.fill(fIDFlightpathCut, tau->tauID("HChTauIDFlightPathSignifCont"));
    if (tau->tauID("HChTauIDFlightPathSignif") < 0.5) return false;
    fCounterPackager.incrementSubCount(fIDFlightpathCut);
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
