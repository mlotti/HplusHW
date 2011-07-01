#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDPFTauBasedAlgorithms.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDTCTau.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "Math/GenVector/VectorUtil.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "TH1F.h"

namespace HPlus {
  TauSelection::Data::Data(const TauSelection *tauSelection, bool passedEvent):
    fTauSelection(tauSelection), fPassedEvent(passedEvent) {}
  TauSelection::Data::~Data() {}

  TauSelection::TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongNumber, std::string label):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fSelection(iConfig.getUntrackedParameter<std::string>("selection")),
    fProngNumber(prongNumber),
    fLabel(label),
    fTauID(0),
    fOperationMode(kNormalTauID),
    fTauFound(eventCounter.addSubCounter(label+"TauSelection","Tau found")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(label);
    
    // Create tauID algorithm handler
    if     (fSelection == "CaloTauCutBased")
      fTauID = new TauIDTCTau(iConfig, eventCounter, eventWeight, prongNumber, label, myDir);
    else if(fSelection == "ShrinkingConePFTauCutBased")
      fTauID = new TauIDPFShrinkingCone(iConfig, eventCounter, eventWeight, prongNumber, label, myDir);
    else if(fSelection == "ShrinkingConePFTauTaNCBased")
      fTauID = new TauIDPFShrinkingConeTaNC(iConfig, eventCounter, eventWeight, prongNumber, label, myDir);
    else if(fSelection == "HPSTightTauBased")
      fTauID = new TauIDPFHPSTight(iConfig, eventCounter, eventWeight, prongNumber, label, myDir);
    else if(fSelection == "HPSMediumTauBased")
      fTauID = new TauIDPFHPSMedium(iConfig, eventCounter, eventWeight, prongNumber, label, myDir);
    else if(fSelection == "HPSLooseTauBased")
      fTauID = new TauIDPFHPSLoose(iConfig, eventCounter, eventWeight, prongNumber, label, myDir);
    else if(fSelection == "HPSVeryLooseTauBased")
      fTauID = new TauIDPFHPSVeryLoose(iConfig, eventCounter, eventWeight, prongNumber, label, myDir);
    else if(fSelection == "CombinedHPSTaNCTauBased")
      fTauID = new TauIDPFShrinkingConeCombinedHPSTaNC(iConfig, eventCounter, eventWeight, prongNumber, label, myDir);
    else throw cms::Exception("Configuration") << "TauSelection: no or unknown tau selection used! Options for 'selection' are: CaloTauCutBased, ShrinkingConePFTauCutBased, ShrinkingConePFTauTaNCBased, HPSTightTauBased, HPSMediumTauBased, HPSLooseTauBased, HPSVeryLooseTauBased, CombinedHPSTaNCBased (you chose '" << fSelection << "')" << std::endl;
    
    // Define tau selection operation mode
    std::string myOperatingModeSelection = iConfig.getUntrackedParameter<std::string>("operatingMode");
    if      (myOperatingModeSelection == "standard")
      fOperationMode = kNormalTauID;
    else if (myOperatingModeSelection == "tauCandidateSelectionOnly")
      fOperationMode = kTauCandidateSelectionOnly;
    else throw cms::Exception("Configuration") << "TauSelection: no or unknown operating mode! Options for 'operatingMode' are: 'standard', 'tauCandidateSelectionOnly' (you chose '" << myOperatingModeSelection << "')" << std::endl;

    // Histograms

    // Selected tau pt, eta, and N_jets distributions
    int myTauJetPtBins = 60;
    float myTauJetPtMin = 0.;
    float myTauJetPtMax = 300.; 
    int myTauJetEtaBins = 60;
    float myTauJetEtaMin = -3.;
    float myTauJetEtaMax = 3.;
    int myTauJetPhiBins = 72;
    float myTauJetPhiMin = -3.14159265;
    float myTauJetPhiMax = 3.14159265;
    int myTauJetNumberBins = 20;
    float myTauJetNumberMin = 0.;
    float myTauJetNumberMax = 20.; 
    // Pt
    hPtTauCandidates = makeTH<TH1F>(myDir,
      "TauSelection_all_tau_candidates_pt",
      "selected_tau_pt;#tau p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myTauJetPtBins, myTauJetPtMin, myTauJetPtMax);
    hPtCleanedTauCandidates = makeTH<TH1F>(myDir,
      "TauSelection_cleaned_tau_candidates_pt",
      "selected_tau_pt;#tau p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myTauJetPtBins, myTauJetPtMin, myTauJetPtMax);
    hPtSelectedTaus = makeTH<TH1F>(myDir,
      "TauSelection_selected_taus_pt",
      "selected_tau_pt;#tau p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myTauJetPtBins, myTauJetPtMin, myTauJetPtMax);
    // Eta
    hEtaTauCandidates = makeTH<TH1F>(myDir,
      "TauSelection_all_tau_candidates_eta",
      "tau_candidates_eta;#tau #eta;N_{jets} / 0.1",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax);
    hEtaCleanedTauCandidates = makeTH<TH1F>(myDir,
      "TauSelection_cleaned_tau_candidates_eta",
      "cleaned_tau_candidates_eta;#tau #eta;N_{jets} / 0.1",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax);
    hEtaSelectedTaus = makeTH<TH1F>(myDir,
      "TauSelection_selected_taus_eta",
      "selected_tau_eta;#tau #eta;N_{jets} / 0.1",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax);
    // Eta vs. phi
    hEtaPhiTauCandidates = makeTH<TH2F>(myDir,
      "TauSelection_all_tau_candidates_eta_vs_phi",
      "tau_candidates_eta_vs_phi;#tau #eta;#tau phi",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax,
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    hEtaPhiCleanedTauCandidates = makeTH<TH2F>(myDir,
      "TauSelection_cleaned_tau_candidates_eta_vs_phi",
      "cleaned_tau_candidates_eta_vs_phi;#tau #eta;#tau phi",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax,
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    hEtaPhiSelectedTaus = makeTH<TH2F>(myDir,
      "TauSelection_selected_taus_eta_vs_phi",
      "selected_tau_eta_vs_phi;#tau #eta;#tau phi",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax,
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    // Phi
    hPhiTauCandidates = makeTH<TH1F>(myDir,
      "TauSelection_all_tau_candidates_phi",
      "tau_candidates_phi;#tau #phi;N_{jets} / 0.087",
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    hPhiCleanedTauCandidates = makeTH<TH1F>(myDir,
      "TauSelection_cleaned_tau_candidates_phi",
      "cleaned_tau_candidates_phi;#tau #phi;N_{jets} / 0.087",
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    hPhiSelectedTaus = makeTH<TH1F>(myDir,
      "TauSelection_selected_taus_phi",
      "selected_tau_phi;#tau #phi;N_{jets} / 0.087",
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    // N
    hNumberOfTauCandidates = makeTH<TH1F>(myDir,
      "TauSelection_all_tau_candidates_N",
      "tau_candidates_N;Number of #tau's;N_{jets}",
      myTauJetNumberBins, myTauJetNumberMin, myTauJetNumberMax);
    hNumberOfCleanedTauCandidates = makeTH<TH1F>(myDir,
      "TauSelection_cleaned_tau_candidates_N",
      "cleaned_tau_candidates_N;Number of #tau's;N_{jets}",
      myTauJetNumberBins, myTauJetNumberMin, myTauJetNumberMax);
    hNumberOfSelectedTaus = makeTH<TH1F>(myDir,
      "TauSelection_selected_taus_N",
      "selected_tau_N;Number of #tau's;N_{jets}",
      myTauJetNumberBins, myTauJetNumberMin, myTauJetNumberMax);
    // MC purity
    hMCPurityOfTauCandidates = makeTH<TH1F>(myDir,
      "TauSelection_all_tau_candidates_MC_purity",
      "tau_candidates_MC_purity;;N_{jets}", 4, 0., 4.);
    hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(1, "#tau from H#pm");
    hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(2, "#tau from W#pm");
    hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(3, "Other #tau source");
    hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(4, "No MC #tau match");
    hMCPurityOfCleanedTauCandidates = makeTH<TH1F>(myDir,
      "TauSelection_cleaned_tau_candidates_MC_purity",
      "cleaned_tau_candidates_MC_purity;;N_{jets}", 4, 0., 4.);
    hMCPurityOfCleanedTauCandidates->GetXaxis()->SetBinLabel(1, "#tau from H#pm");
    hMCPurityOfCleanedTauCandidates->GetXaxis()->SetBinLabel(2, "#tau from W#pm");
    hMCPurityOfCleanedTauCandidates->GetXaxis()->SetBinLabel(3, "Other #tau source");
    hMCPurityOfCleanedTauCandidates->GetXaxis()->SetBinLabel(4, "No MC #tau match");
    hMCPurityOfSelectedTaus = makeTH<TH1F>(myDir,
      "TauSelection_selected_taus_MC_purity",
      "selected_tau_MC_purity;;N_{jets}", 4, 0., 4.);
    hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(1, "#tau from H#pm");
    hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(2, "#tau from W#pm");
    hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(3, "Other #tau source");
    hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(4, "No MC #tau match");

    // Isolation variables
    hVLooseIsoNcands = makeTH<TH1F>(myDir, "TauSelection_all_tau_candidates_VLooseIsoNCands", "Number of isolation candidates in VLoose", 100, 0, 100);
    hLooseIsoNcands = makeTH<TH1F>(myDir, "TauSelection_all_tau_candidates_LooseIsoNCands", "Number of isolation candidates in Loose", 100, 0, 100);
    hMediumIsoNcands = makeTH<TH1F>(myDir, "TauSelection_all_tau_candidates_MediumIsoNCands", "Number of isolation candidates in Medium", 100, 0, 100);
    hTightIsoNcands = makeTH<TH1F>(myDir, "TauSelection_all_tau_candidates_TightIsoNCands", "Number of isolation candidates in Tight", 100, 0, 100);

    // Operating mode of tau ID -- for quick validating that tau selection is doing what is expected 
    hTauIdOperatingMode = makeTH<TH1F>(myDir, "tauSelection_operating_mode", "tau_operating_mode;;N_{events}", 6, 0., 6.);
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(1, "Control");
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(2, "Normal tau ID");
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(4, "tauCandidateSelectionOnly");
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(5, "tauIDWithoutRtauOnly");
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(6, "tauIDWithRtauOnly");
  }

  TauSelection::~TauSelection() {
    if (fTauID) delete fTauID;
  }

  TauSelection::Data TauSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {   
    bool passEvent = false;
    // Obtain tau collection from src specified in config
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fSrc, htaus);
    // Do selection
    passEvent = doTauSelection(iEvent,iSetup,htaus->ptrVector());
    return Data(this, passEvent);
  }

  TauSelection::Data TauSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus) {
    bool passEvent = false;
    // Do selection
    passEvent = doTauSelection(iEvent,iSetup,taus);
    return Data(this, passEvent);
  }

  TauSelection::Data TauSelection::analyzeTauIDWithoutRtauOnCleanedTauCandidates(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> tauCandidate) {
    // Initialize
    bool passEvent = false;
    fSelectedTaus.clear();
    fSelectedTaus.reserve(1);
    fTauID->reset();
    // Document operation mode
    TauSelectionOperationMode fOriginalOperationMode = fOperationMode;
    fOperationMode = kTauIDWithoutRtauOnly;
    fillOperationModeHistogram();
    fOperationMode = fOriginalOperationMode;
    // Do selection
    if (fTauID->passIsolation(tauCandidate)) {
      if (fProngNumber == 1) {
        if (fTauID->passOneProngCut(tauCandidate)) {
          if (fTauID->passChargeCut(tauCandidate)) {
            // All cuts have been passed, save tau
            fillHistogramsForSelectedTaus(tauCandidate, iEvent);
            fSelectedTaus.push_back(tauCandidate);
          }
        }
      }
    }
    // Handle counters
    fTauID->updatePassedCounters();
    // Fill number of taus histograms
    hNumberOfSelectedTaus->Fill(static_cast<float>(fSelectedTaus.size()), fEventWeight.getWeight()); 
    // Make decision
    if (fSelectedTaus.size() > 0)
      passEvent = true;
    // Return data object
    return Data(this, passEvent);
  }

  bool TauSelection::doTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus){
    // Document operation mode
    fillOperationModeHistogram();
    
    // Initialize
    fSelectedTaus.clear();
    fSelectedTaus.reserve(taus.size());
    fCleanedTauCandidates.clear();
    fCleanedTauCandidates.reserve(taus.size());
    fTauID->reset();

    // Loop over the taus
    for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
      const edm::Ptr<pat::Tau> iTau = *iter;

      fillHistogramsForTauCandidates(iTau, iEvent);
      
      // Tau candidate selections
      if (!fTauID->passTauCandidateSelection(iTau)) continue;
      if (!fTauID->passLeadingTrackCuts(iTau)) continue;
      if (!fTauID->passECALFiducialCuts(iTau)) continue;
      if (!fTauID->passTauCandidateEAndMuVetoCuts(iTau)) continue;      
      fillHistogramsForCleanedTauCandidates(iTau, iEvent);
      fCleanedTauCandidates.push_back(iTau);
      
      // Tau ID selections
      if (fOperationMode == kNormalTauID) {
        // Standard tau ID (necessary for the tau selection logic) 
        if (!fTauID->passIsolation(iTau)) continue;

        if (fProngNumber == 1) {
          if (!fTauID->passOneProngCut(iTau)) continue;
          if (!fTauID->passChargeCut(iTau)) continue;
          if (!fTauID->passRTauCut(iTau)) continue;
        } else if (fProngNumber == 3) {
          if (!fTauID->passThreeProngCut(iTau)) continue;
          if (!fTauID->passChargeCut(iTau)) continue;
          //if (!fTauID->passInvMassCut(iTau)) continue; // FIXME: not tested, not validated
          //if (!fTauID->passDeltaECut(iTau)) continue; // FIXME: not tested, not validated
          //if (!fTauID->passFlightpathCut(iTau)) continue; // FIXME: not tested, not validated
          if (!fTauID->passRTauCut(iTau)) continue;
        }
      }
      // All cuts have been passed, save tau
      fillHistogramsForSelectedTaus(iTau, iEvent);
      fSelectedTaus.push_back(iTau);
    }
    // Handle counters
    fTauID->updatePassedCounters();
    // Fill number of taus histograms
    hNumberOfTauCandidates->Fill(static_cast<float>(taus.size()), fEventWeight.getWeight());
    hNumberOfCleanedTauCandidates->Fill(static_cast<float>(fCleanedTauCandidates.size()), fEventWeight.getWeight());
    if (fOperationMode != kTauCandidateSelectionOnly) {
      hNumberOfSelectedTaus->Fill(static_cast<float>(fSelectedTaus.size()), fEventWeight.getWeight());
    }

    // Handle result of tau candidate selection only
    if (fOperationMode == kTauCandidateSelectionOnly) {
      return (fCleanedTauCandidates.size() > 0);
    }

    // Check if taus have been found
    if (fSelectedTaus.size() == 0)
      return false;
    // Found at least 1 tau beyond this line
    increment(fTauFound);
    
    // Handle result of standard tau ID 
    if (fOperationMode == kNormalTauID)
      return true;

    // Never reached
    return true;
  }

  void TauSelection::fillOperationModeHistogram() {
    hTauIdOperatingMode->Fill(0., fEventWeight.getWeight()); // Control
    if (fOperationMode == kNormalTauID)
      hTauIdOperatingMode->Fill(1., fEventWeight.getWeight());
    else if (fOperationMode == kTauCandidateSelectionOnly)
      hTauIdOperatingMode->Fill(3., fEventWeight.getWeight());
    else if (fOperationMode == kTauIDWithoutRtauOnly)
      hTauIdOperatingMode->Fill(4., fEventWeight.getWeight());
    else if (fOperationMode == kTauIDWithRtauOnly)
      hTauIdOperatingMode->Fill(5., fEventWeight.getWeight());
  }

  void TauSelection::fillHistogramsForTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent) {
    double myTauPt = tau->pt();
    double myTauEta = tau->eta();
    double myTauPhi = tau->phi();
    hPtTauCandidates->Fill(myTauPt, fEventWeight.getWeight());
    hEtaTauCandidates->Fill(myTauEta, fEventWeight.getWeight());
    hPhiTauCandidates->Fill(myTauPhi, fEventWeight.getWeight());
    hEtaPhiTauCandidates->Fill(myTauEta, myTauPhi, fEventWeight.getWeight());
    // Purity
    if (!iEvent.isRealData()) {
      ObtainMCPurity(tau, iEvent, hMCPurityOfTauCandidates); 
    }

    hVLooseIsoNcands->Fill(tau->userInt("byVLooseOccupancy"), fEventWeight.getWeight());
    hLooseIsoNcands->Fill(tau->userInt("byLooseOccupancy"), fEventWeight.getWeight());
    hMediumIsoNcands->Fill(tau->userInt("byMediumOccupancy"), fEventWeight.getWeight());
    hTightIsoNcands->Fill(tau->userInt("byTightOccupancy"), fEventWeight.getWeight());
  }
  
  void TauSelection::fillHistogramsForCleanedTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent) {
    double myTauPt = tau->pt();
    double myTauEta = tau->eta();
    double myTauPhi = tau->phi();
    hPtCleanedTauCandidates->Fill(myTauPt, fEventWeight.getWeight());
    hEtaCleanedTauCandidates->Fill(myTauEta, fEventWeight.getWeight());
    hPhiCleanedTauCandidates->Fill(myTauPhi, fEventWeight.getWeight());
    hEtaPhiCleanedTauCandidates->Fill(myTauEta, myTauPhi, fEventWeight.getWeight());

    // Purity
    if (!iEvent.isRealData()) {
      ObtainMCPurity(tau, iEvent, hMCPurityOfCleanedTauCandidates); 
    }
  }
  
  void TauSelection::fillHistogramsForSelectedTaus(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent) {
    double myTauPt = tau->pt();
    double myTauEta = tau->eta();
    double myTauPhi = tau->phi();
    hPtSelectedTaus->Fill(myTauPt, fEventWeight.getWeight());
    hEtaSelectedTaus->Fill(myTauEta, fEventWeight.getWeight());

    hPhiSelectedTaus->Fill(myTauPhi, fEventWeight.getWeight());
    hEtaPhiSelectedTaus->Fill(myTauEta, myTauPhi, fEventWeight.getWeight());

    // Purity
    if (!iEvent.isRealData()) {
      ObtainMCPurity(tau, iEvent, hMCPurityOfSelectedTaus); 
    }  
  }

  TauSelection::Data TauSelection::setSelectedTau(edm::Ptr<pat::Tau>& tau, bool passEvent) {
    fSelectedTaus.clear();
    fSelectedTaus.reserve(1);
    if (tau.isNonnull())
      fSelectedTaus.push_back(tau);
    return Data(this, passEvent);
  }

  void TauSelection::ObtainMCPurity(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent, TH1* histogram) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    for (size_t i=0; i < genParticles->size(); ++i) {  
      const reco::Candidate & p = (*genParticles)[i];
      if (std::abs(p.pdgId()) == 15) {
        // Check match with tau
        if (reco::deltaR(p, tau->p4()) < 0.1) {
          // Check mother of tau
          int numberOfTauMothers = p.numberOfMothers(); 
          for (int im=0; im < numberOfTauMothers; ++im){  
            const reco::GenParticle* dparticle = dynamic_cast<const reco::GenParticle*>(p.mother(im));
            if (!dparticle) continue;
            int idmother = std::abs(dparticle->pdgId());
            if (idmother == 37) { // H+
              histogram->Fill(0., fEventWeight.getWeight());
              return;
            }
            if (idmother == 24) { // W+
              histogram->Fill(1., fEventWeight.getWeight());
              return;
            }
          }
          histogram->Fill(2., fEventWeight.getWeight()); // Other source of tau (B decays)
        }
      }
    }
    histogram->Fill(3., fEventWeight.getWeight()); // No MC match found
  }

}
