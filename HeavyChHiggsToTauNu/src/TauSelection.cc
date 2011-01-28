#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDPFTauBasedAlgorithms.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauIDTCTau.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "TH1F.h"

namespace HPlus {
  TauSelection::Data::Data(const TauSelection *tauSelection, bool passedEvent):
    fTauSelection(tauSelection), fPassedEvent(passedEvent) {}
  TauSelection::Data::~Data() {}

  TauSelection::TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, int prongNumber):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fSelection(iConfig.getUntrackedParameter<std::string>("selection")),
    fProngNumber(prongNumber),
    fTauID(0),
    fOperationMode(kNormalTauID),
    fFactorizationTable(iConfig),
    fTauFound(eventCounter.addSubCounter("TauSelection","Tau found")), // FIXME: include prong number into counter name
    fEventWeight(eventWeight)
  {
    // Histograms
    edm::Service<TFileService> fs;

    // Selected tau pt, eta, and N_jets distributions
    int myTauJetPtBins = 60;
    float myTauJetPtMin = 0.;
    float myTauJetPtMax = 300.; 
    int myTauJetEtaBins = 60;
    float myTauJetEtaMin = -3.;
    float myTauJetEtaMax = 3.;
    int myTauJetNumberBins = 20;
    float myTauJetNumberMin = 0.;
    float myTauJetNumberMax = 20.; 
    hPtTauCandidates = makeTH<TH1F>(*fs,
      "tauID_tau_candidates_pt",
      "selected_tau_pt;#tau p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myTauJetPtBins, myTauJetPtMin, myTauJetPtMax);
    hPtCleanedTauCandidates = makeTH<TH1F>(*fs,
      "tauID_cleaned_tau_candidates_pt",
      "selected_tau_pt;#tau p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myTauJetPtBins, myTauJetPtMin, myTauJetPtMax);
    hPtSelectedTaus = makeTH<TH1F>(*fs,
      "tauID_selected_tau_pt",
      "selected_tau_pt;#tau p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myTauJetPtBins, myTauJetPtMin, myTauJetPtMax);
    hEtaTauCandidates = makeTH<TH1F>(*fs,
      "tauID_tau_candidates_eta",
      "tau_candidates_eta;#tau #eta;N_{jets} / 0.1",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax);
    hEtaCleanedTauCandidates = makeTH<TH1F>(*fs,
      "tauID_cleaned_tau_candidates_eta",
      "cleaned_tau_candidates_eta;#tau #eta;N_{jets} / 0.1",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax);
    hEtaSelectedTaus = makeTH<TH1F>(*fs,
      "tauID_selected_tau_eta",
      "selected_tau_eta;#tau #eta;N_{jets} / 0.1",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax);
    hNumberOfTauCandidates = makeTH<TH1F>(*fs,
      "tauID_tau_candidates_N",
      "tau_candidates_N;Number of #tau's;N_{jets}",
      myTauJetNumberBins, myTauJetNumberMin, myTauJetNumberMax);
    hNumberOfCleanedTauCandidates = makeTH<TH1F>(*fs,
      "tauID_cleaned_tau_candidates_N",
      "cleaned_tau_candidates_N;Number of #tau's;N_{jets}",
      myTauJetNumberBins, myTauJetNumberMin, myTauJetNumberMax);
    hNumberOfSelectedTaus = makeTH<TH1F>(*fs,
      "tauID_selected_tau_N",
      "selected_tau_N;Number of #tau's;N_{jets}",
      myTauJetNumberBins, myTauJetNumberMin, myTauJetNumberMax);
    // Operating mode of tau ID -- for quick validating that tau selection is doing what is expected 
    hTauIdOperatingMode = makeTH<TH1F>(*fs, "tau_operating_mode", "tau_operating_mode;;N_{events}", 5, 0., 5.);
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(1, "Control");
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(2, "Normal tau ID");
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(3, "Factorized tau ID");
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(4, "Anti-tau ID");
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(5, "Anti-isolated tau");

    // Factorization / general histograms
    // NB! change binning and range only if you ARE sure what you are doing ...
    int myFactorizationJetPtBins = 60;
    float myFactorizationJetPtMin = 0.;
    float myFactorizationJetPtMax = 300.; 
    int myFactorizationJetEtaBins = 60;
    float myFactorizationJetEtaMin = -3.;
    float myFactorizationJetEtaMax = 3.;
    hFactorizationPtSelectedTaus = makeTH<TH1F>(*fs,
      "tauID_factorization_selected_tau_pt",
      "factorized_selected_tau_pt;Selected #tau p_{T}, GeV/c;N_{events} / 5 GeV/c",
      myFactorizationJetPtBins, myFactorizationJetPtMin, myFactorizationJetPtMax);
    hFactorizationEtaSelectedTaus = makeTH<TH1F>(*fs,
      "tauID_factorization_selected_tau_eta",
      "factorized_selected_tau_eta;Selected #tau #eta;N_{events} / 0.1",
      myFactorizationJetEtaBins, myFactorizationJetEtaMin, myFactorizationJetEtaMax);
    hFactorizationCategory = makeTH<TH1F>(*fs,
      "tauID_factorized_tau_category",
      "factorized_tau_category",
      5, 0, 5);
    hFactorizationCategory->GetXaxis()->SetBinLabel(1, "All events");
    hFactorizationCategory->GetXaxis()->SetBinLabel(2, "No tau candidates");
    hFactorizationCategory->GetXaxis()->SetBinLabel(3, "Only one tau candidate");
    hFactorizationCategory->GetXaxis()->SetBinLabel(4, "Highest tau that passed tauID");
    hFactorizationCategory->GetXaxis()->SetBinLabel(5, "No tau after tauID; tau=highest tau candidate");
    // Factorization / weighted histograms
    hFactorizationPtBeforeTauID = makeTH<TH1F>(*fs,
      "tauID_factorization_calculation_pt_before_tauID",
      "tau_pt_before_weighted;#tau jet p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myFactorizationJetPtBins, myFactorizationJetPtMin, myFactorizationJetPtMax);
    hFactorizationPtAfterTauID = makeTH<TH1F>(*fs,
      "tauID_factorization_calculation_pt_after_tauID",
      "tau_pt_after_weighted;#tau jet p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myFactorizationJetPtBins, myFactorizationJetPtMin, myFactorizationJetPtMax);
    hFactorizationEtaBeforeTauID = makeTH<TH1F>(*fs,
      "tauID_factorization_calculation_eta_before_tauID",
      "tau_eta_before_weighted;#tau jet #eta;N_{jets} / 0.1", 
      myFactorizationJetEtaBins, myFactorizationJetEtaMin, myFactorizationJetEtaMax);
    hFactorizationEtaAfterTauID = makeTH<TH1F>(*fs,
      "tauID_factorization_calculation_eta_after_tauID",
      "tau_eta_after_weighted;#tau jet #eta;N_{jets} / 0.1",
      myFactorizationJetEtaBins, myFactorizationJetEtaMin, myFactorizationJetEtaMax);
    hFactorizationPtVsEtaBeforeTauID = makeTH<TH2F>(*fs,
      "tauID_factorization_calculation_pt_vs_eta_before_tauID",
      "tau_pt_vs_eta_before_weighted;#tau jet p_{T}, GeV/c;#tau jet #eta",
      myFactorizationJetPtBins, myFactorizationJetPtMin, myFactorizationJetPtMax,
      myFactorizationJetEtaBins, myFactorizationJetEtaMin, myFactorizationJetEtaMax);
    hFactorizationPtVsEtaAfterTauID = makeTH<TH2F>(*fs,
      "tauID_factorization_calculation_pt_vs_eta_after_tauID",
      "tau_pt_vs_eta_after_weighted;#tau jet p_{T}, GeV/c;#tau jet #eta",
      myFactorizationJetPtBins, myFactorizationJetPtMin, myFactorizationJetPtMax,
      myFactorizationJetEtaBins, myFactorizationJetEtaMin, myFactorizationJetEtaMax);
    // Factorization / unweighted histograms
    hFactorizationPtBeforeTauIDUnweighted = makeTH<TH1F>(*fs,
      "tauID_factorization_calculation_pt_before_tauID_unweighted",
      "tau_pt_before_unweighted;#tau jet p_{T}, GeV/c;N",
      myFactorizationJetPtBins, myFactorizationJetPtMin, myFactorizationJetPtMax);
    hFactorizationPtAfterTauIDUnweighted = makeTH<TH1F>(*fs,
      "tauID_factorization_calculation_pt_after_tauID_unweighted",
      "tau_pt_after_unweighted;#tau jet p_{T}, GeV/c;N",
      myFactorizationJetPtBins, myFactorizationJetPtMin, myFactorizationJetPtMax);
    hFactorizationEtaBeforeTauIDUnweighted = makeTH<TH1F>(*fs,
      "tauID_factorization_calculation_eta_before_tauID_unweighted",
      "tau_eta_before_unweighted;#tau jet #eta;N",
      myFactorizationJetEtaBins, myFactorizationJetEtaMin, myFactorizationJetEtaMax);
    hFactorizationEtaAfterTauIDUnweighted = makeTH<TH1F>(*fs,
      "tauID_factorization_calculation_eta_after_tauID_unweighted",
      "tau_eta_after_unweighted;#tau jet #eta;N",
      myFactorizationJetEtaBins, myFactorizationJetEtaMin, myFactorizationJetEtaMax);
    hFactorizationPtVsEtaBeforeTauIDUnweighted = makeTH<TH2F>(*fs,
      "tauID_factorization_calculation_pt_vs_eta_before_tauID_unweighted",
      "tau_pt_vs_eta_before_unweighted;#tau jet p_{T}, GeV/c;#tau jet #eta",
      myFactorizationJetPtBins, myFactorizationJetPtMin, myFactorizationJetPtMax, 
      myFactorizationJetEtaBins, myFactorizationJetEtaMin, myFactorizationJetEtaMax);
    hFactorizationPtVsEtaAfterTauIDUnweighted = makeTH<TH2F>(*fs,
      "tauID_factorization_calculation_pt_vs_eta_after_tauID_unweighted",
      "tau_pt_vs_eta_after_unweighted;#tau jet p_{T}, GeV/c;#tau jet #eta", 
      myFactorizationJetPtBins, myFactorizationJetPtMin, myFactorizationJetPtMax, 
      myFactorizationJetEtaBins, myFactorizationJetEtaMin, myFactorizationJetEtaMax);

    // Create tauID algorithm handler
    if     (fSelection == "CaloTauCutBased")
      fTauID = new TauIDTCTau(iConfig, eventCounter, eventWeight);
    else if(fSelection == "ShrinkingConePFTauCutBased")
      fTauID = new TauIDPFShrinkingCone(iConfig, eventCounter, eventWeight);
    else if(fSelection == "ShrinkingConePFTauTaNCBased")
      fTauID = new TauIDPFShrinkingConeTaNC(iConfig, eventCounter, eventWeight);
    else if(fSelection == "HPSTauBased")
      fTauID = new TauIDPFShrinkingConeHPS(iConfig, eventCounter, eventWeight);
    else if(fSelection == "CombinedHPSTaNCTauBased")
      fTauID = new TauIDPFShrinkingConeCombinedHPSTaNC(iConfig, eventCounter, eventWeight);
    else throw cms::Exception("Configuration") << "TauSelection: no or unknown tau selection used! Options for 'selection' are: CaloTauCutBased, ShrinkingConePFTauCutBased, ShrinkingConePFTauTaNCBased, HPSTauBased, CombinedHPSTaNCBased (you chose '" << fSelection << "')" << std::endl;
    
    // Define tau selection operation mode
    std::string myOperatingModeSelection = iConfig.getUntrackedParameter<std::string>("operatingMode");
    if      (myOperatingModeSelection == "standard")
      fOperationMode = kNormalTauID;
    else if (myOperatingModeSelection == "factorized")
      fOperationMode = kFactorizedTauID;
    else if (myOperatingModeSelection == "antitautag")
      fOperationMode = kAntiTauTag;
    else if (myOperatingModeSelection == "antiisolatedtau")
      fOperationMode = kAntiTauTagIsolationOnly;
    else throw cms::Exception("Configuration") << "TauSelection: no or unknown operating mode! Options for 'operatingMode' are: 'standard', 'factorized', 'antitautag', 'antiisolatedtau' (you chose '" << myOperatingModeSelection << "')" << std::endl;
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

  bool TauSelection::doTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus){
    // Document operation mode
    fillOperationModeHistogram();
    
    // Initialize
    fSelectedTaus.clear();
    fSelectedTaus.reserve(taus.size());
    fCleanedTauCandidates.clear();
    fCleanedTauCandidates.reserve(taus.size());
    bool fAntiTauTagStatus = true;

    // Loop over the taus
    for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
      const edm::Ptr<pat::Tau> iTau = *iter;

      fillHistogramsForTauCandidates(iTau, iEvent);
      
      // Tau candidate selections
      if (!fTauID->passTauCandidateSelection(iTau)) continue;
      if (!fTauID->passLeadingTrackCuts(iTau)) continue;
      if (!fTauID->passTauCandidateEAndMuVetoCuts(iTau)) continue;
      fillHistogramsForCleanedTauCandidates(iTau, iEvent);
      fCleanedTauCandidates.push_back(iTau);
      
      // Tau ID selections
      if (fOperationMode == kNormalTauID || fOperationMode == kFactorizedTauID) {
        // Standard tau ID or factorized tau ID (necessary for the tau selection logic) 
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
      } else if (fOperationMode == kAntiTauTag || fOperationMode == kAntiTauTagIsolationOnly) {
        // Anti-tau tag
        if (fProngNumber == 1) {
          if (!fTauID->passOneProngCut(iTau)) continue;
        } else if (fProngNumber == 3) {
          if (!fTauID->passThreeProngCut(iTau)) continue;
        }
        if (!fTauID->passAntiIsolation(iTau)) {
          fAntiTauTagStatus = false; // Reject event if even one isolated jet exists
          continue;
        }
        if (fOperationMode == kAntiTauTag) {
          if (!fTauID->passAntiRTauCut(iTau)) {
            fAntiTauTagStatus = false; // Reject event if even one jet fails the anti rtau cut
            continue;
          }
          // NOTE: it is possible to add here some cut on E(hadr.energy)/E(jet) 
          //if (!fTauID->passAntiDeltaECut(iTau)) continue;
        }
      }
      // All cuts have been passed, save tau
      fillHistogramsForSelectedTaus(iTau, iEvent);
      fSelectedTaus.push_back(iTau);
    }
    // Fill number of taus histograms
    hNumberOfTauCandidates->Fill(static_cast<float>(taus.size()), fEventWeight.getWeight());
    hNumberOfCleanedTauCandidates->Fill(static_cast<float>(fCleanedTauCandidates.size()), fEventWeight.getWeight());
    hNumberOfSelectedTaus->Fill(static_cast<float>(fSelectedTaus.size()), fEventWeight.getWeight()); 

    // Handle result of factorized tau ID
    if (fOperationMode == kFactorizedTauID) {
      if (!doFactorizationLookup())
        // No tau found
        return false;
      // Selected tau is the first entry in the fSelectedTaus vector
      double myTauPt = fSelectedTaus[0]->pt();
      double myTauEta = fSelectedTaus[0]->eta();
      hFactorizationPtSelectedTaus->Fill(myTauPt, fEventWeight.getWeight());
      hFactorizationEtaSelectedTaus->Fill(myTauEta, fEventWeight.getWeight());
      increment(fTauFound);
      // Update event weight with the factorization coefficient
      fEventWeight.multiplyWeight(fFactorizationTable.getWeightByPtAndEta(myTauPt, myTauEta));
    }

    // Check if taus have been found
    if (fSelectedTaus.size() == 0)
      return false;
    // Found at least 1 tau beyond this line
    increment(fTauFound);
    
    // Handle result of standard tau ID 
    if (fOperationMode == kNormalTauID)
      return true;

    // Handle result of anti-tau tag
    if (fOperationMode == kAntiTauTag || fOperationMode == kAntiTauTagIsolationOnly)
      return fAntiTauTagStatus;

    // Never reached
    return true;
  }

  bool TauSelection::doFactorizationLookup() {
    // If the method returns true, the selected tau is the first entry of the fSelectedTaus vector
  
    // Check if there are entries in the tau collection
    hFactorizationCategory->Fill(0.0, fEventWeight.getWeight());
    if (!fCleanedTauCandidates.size()) {
      hFactorizationCategory->Fill(1.0, fEventWeight.getWeight());
      return false;
    }
    if (fCleanedTauCandidates.size() == 1) {
      // Only one tau in the cleaned tau candidate collection: take as tau the only tau object
      fSelectedTaus.clear();
      fSelectedTaus.push_back(fCleanedTauCandidates[0]);
      hFactorizationCategory->Fill(2.0, fEventWeight.getWeight());
      return true;
    }
    // More than one tau exists in the cleaned tau candidate collection
    // Strategy: apply tauID and see if any of the candidates pass
    if (fSelectedTaus.size()) {
      // At least one tau object has passed tauID, take as tau the tau object with highest ET
      hFactorizationCategory->Fill(3.0, fEventWeight.getWeight());
      return true;
    }
    // No tau objects have passed the tauID, take as tau the tau object with the highest ET
    fSelectedTaus.clear();
    fSelectedTaus.push_back(fCleanedTauCandidates[0]);
    hFactorizationCategory->Fill(4.0, fEventWeight.getWeight());
    return true;
  }

  void TauSelection::fillOperationModeHistogram() {
    hTauIdOperatingMode->Fill(1); // Control
    if (fOperationMode == kNormalTauID)
      hTauIdOperatingMode->Fill(2);
    else if (fOperationMode == kFactorizedTauID)
      hTauIdOperatingMode->Fill(3);
    else if (fOperationMode == kAntiTauTag)
      hTauIdOperatingMode->Fill(4);
    else if (fOperationMode == kAntiTauTagIsolationOnly)
      hTauIdOperatingMode->Fill(5);
  }

  void TauSelection::fillHistogramsForTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent) {
    double myTauPt = tau->pt();
    double myTauEta = tau->eta();
    hPtTauCandidates->Fill(myTauPt, fEventWeight.getWeight());
    hEtaTauCandidates->Fill(myTauEta, fEventWeight.getWeight());
  }
  
  void TauSelection::fillHistogramsForCleanedTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent) {
    double myTauPt = tau->pt();
    double myTauEta = tau->eta();
    hPtCleanedTauCandidates->Fill(myTauPt, fEventWeight.getWeight());
    hEtaCleanedTauCandidates->Fill(myTauEta, fEventWeight.getWeight());
    // Factorization histograms
    if (fOperationMode == kNormalTauID || fOperationMode == kFactorizedTauID) {
      hFactorizationPtBeforeTauIDUnweighted->Fill(myTauPt, fEventWeight.getWeight());
      hFactorizationEtaBeforeTauIDUnweighted->Fill(myTauEta, fEventWeight.getWeight());
      hFactorizationPtVsEtaBeforeTauIDUnweighted->Fill(myTauPt, myTauEta, fEventWeight.getWeight());
      hFactorizationPtBeforeTauIDUnweighted->Fill(myTauPt);
      hFactorizationEtaBeforeTauIDUnweighted->Fill(myTauEta);
      hFactorizationPtVsEtaBeforeTauIDUnweighted->Fill(myTauPt, myTauEta);
    }
    // Purity
    if (!iEvent.isRealData()) {
      // FIXME: add check if the tau object matches with a MC tau 
    }
  }
  
  void TauSelection::fillHistogramsForSelectedTaus(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent) {
    double myTauPt = tau->pt();
    double myTauEta = tau->eta();
    hPtSelectedTaus->Fill(myTauPt, fEventWeight.getWeight());
    hEtaSelectedTaus->Fill(myTauEta, fEventWeight.getWeight());
    // Factorization histograms
    if (fOperationMode == kNormalTauID || fOperationMode == kFactorizedTauID) {
      hFactorizationPtAfterTauIDUnweighted->Fill(myTauPt, fEventWeight.getWeight());
      hFactorizationEtaAfterTauIDUnweighted->Fill(myTauEta, fEventWeight.getWeight());
      hFactorizationPtVsEtaAfterTauIDUnweighted->Fill(myTauPt, myTauEta, fEventWeight.getWeight());
      hFactorizationPtAfterTauIDUnweighted->Fill(myTauPt);
      hFactorizationEtaAfterTauIDUnweighted->Fill(myTauEta);
      hFactorizationPtVsEtaAfterTauIDUnweighted->Fill(myTauPt, myTauEta);
    }
    // Purity
    if (!iEvent.isRealData()) {
      // FIXME: add check if the tau object matches with a MC tau 
    }
  
  }

  TauSelection::Data TauSelection::setSelectedTau(edm::Ptr<pat::Tau>& tau, bool passEvent) {
    fSelectedTaus.clear();
    fSelectedTaus.reserve(1);
    if (tau.isNonnull())
      fSelectedTaus.push_back(tau);
    return Data(this, passEvent);
  }
}
