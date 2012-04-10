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

namespace {
  bool isolationLessThan(const edm::Ptr<pat::Tau>& a, const edm::Ptr<pat::Tau>& b) {
    // Return true if a becomes before b, false if b becomes before a
    
    // Do first comparisons of the isolation discriminators, because
    // they are bullet proof way of using exactly the same isolation
    // defitions as in the discriminators
    
    // FIXME change to delta beta discriminators or eventually to continuous discriminator
    
    if(a->tauID("byTightIsolation") > 0.5 && b->tauID("byTightIsolation") < 0.5)
      return true;

    if(a->tauID("byMediumIsolation") > 0.5) {
      if(b->tauID("byTightIsolation") > 0.5)
        return false;
      if(b->tauID("byMediumIsolation") < 0.5)
        return true;
    }

    if(a->tauID("byLooseIsolation") > 0.5) {
      // assume that if tau is medium isolated, it is also tight isolated
      if(b->tauID("byMediumIsolation") > 0.5)
        return false;
      if(b->tauID("byLooseIsolation") < 0.5)
        return true;
    }

    if(a->tauID("byVLooseIsolation") > 0.5) {
      if(b->tauID("byLooseIsolation") > 0.5)
        return false;
      if(b->tauID("byVLooseIsolation") < 0.5)
        return true;
    }

    // At this point both a and b are in the same isolation class, and
    // we need a continous isolation variable. This is calculated by
    // us, it should be more or less the same as the official
    // discriminators, but it's possible that it's not.
    return a->userFloat("byTightChargedMaxPt") < b->userFloat("byTightChargedMaxPt");
  }

  bool isolationProngRtauLessThan(const edm::Ptr<pat::Tau>& a, const edm::Ptr<pat::Tau>& b) {
    // Return true if a becomes before b, false if b becomes before a
    
    // Do first comparisons of the isolation discriminators, because
    // they are bullet proof way of using exactly the same isolation
    // defitions as in the discriminators
    if(a->tauID("byTightIsolation") > 0.5 && b->tauID("byTightIsolation") < 0.5)
      return true;

    if(a->tauID("byMediumIsolation") > 0.5) {
      if(b->tauID("byTightIsolation") > 0.5)
        return false;
      if(b->tauID("byMediumIsolation") < 0.5)
        return true;
    }

    if(a->tauID("byLooseIsolation") > 0.5) {
      // assume that if tau is medium isolated, it is also tight isolated
      if(b->tauID("byMediumIsolation") > 0.5)
        return false;
      if(b->tauID("byLooseIsolation") < 0.5)
        return true;
    }

    if(a->tauID("byVLooseIsolation") > 0.5) {
      if(b->tauID("byLooseIsolation") > 0.5)
        return false;
      if(b->tauID("byVLooseIsolation") < 0.5)
        return true;

    }

    // At this point bot a and b are in the same isolation class. Next
    // see, if either is one prong
    size_t aProng = a->signalPFChargedHadrCands().size(); // FIXME: does not work for TCTau
    size_t bProng = b->signalPFChargedHadrCands().size();

    if(aProng == 1 && bProng != 1)
      return true;
    if(aProng != 1 && bProng == 1)
      return false;

    // Either a and b are both one prong, or neither is. Do final
    // comparison with Rtau.
    double aRtau = a->leadPFChargedHadrCand()->p() / a->p();
    double bRtau = b->leadPFChargedHadrCand()->p() / b->p();

    return aRtau < bRtau;
  }
}

namespace HPlus {
  // TauSelection::Data methods ------------------------------------------------
  TauSelection::Data::Data(const TauSelection *tauSelection, bool passedEvent):
    fTauSelection(tauSelection), fPassedEvent(passedEvent) {}
  TauSelection::Data::~Data() {}
  
  const edm::PtrVector<pat::Tau>& TauSelection::Data::getSelectedTaus() const {
    if (fTauSelection->fOperationMode == TauSelection::kTauCandidateSelectionOnly)
      return fTauSelection->fSelectedTauCandidates;
    else if (fTauSelection->fOperationMode == TauSelection::kNormalTauID)
      return fTauSelection->fSelectedTaus;
    return fTauSelection->fSelectedTaus; // never reached
  }

  const edm::Ptr<pat::Tau> TauSelection::Data::getSelectedTau() const {
    if (!fPassedEvent) return fTauSelection->fSelectedTauCandidates[0]; // No tau was selected, return zero pointer
    if (fTauSelection->fOperationMode == TauSelection::kTauCandidateSelectionOnly)
      return fTauSelection->fSelectedTauCandidates[0];
    else if (fTauSelection->fOperationMode == TauSelection::kNormalTauID)
      return fTauSelection->fSelectedTaus[0];
    return fTauSelection->fSelectedTauCandidates[0]; // never reached
  }

  const size_t TauSelection::Data::getNProngsOfSelectedTau() const {
    if (!fPassedEvent) return 0;
    return fTauSelection->fTauID->getNProngs(getSelectedTau());
  }

  const double TauSelection::Data::getRtauOfSelectedTau() const {
    if (!fPassedEvent) return 0;
    return fTauSelection->fTauID->getRtauValue(getSelectedTau());
  }

  const bool TauSelection::Data::selectedTauPassesIsolation() const {
    if (!fPassedEvent) return false;
    return fTauSelection->fTauID->passIsolation(getSelectedTau());
  }

  const bool TauSelection::Data::selectedTauPassesNProngs() const {
    if (!fPassedEvent) return false;
    return fTauSelection->fTauID->passNProngsCut(getSelectedTau());
  }

  const bool TauSelection::Data::selectedTauPassesRtau() const {
    if (!fPassedEvent) return false;
    return fTauSelection->fTauID->passRTauCut(getSelectedTau());
  }
  
  const bool TauSelection::Data::selectedTausDoNotPassIsolation() const {
    //    if (!fPassedEvent) return false;
    for (edm::PtrVector<pat::Tau>::const_iterator iter = getSelectedTaus().begin(); iter != getSelectedTaus().end(); ++iter) {
      //      std::cout << "passIsolation" << fTauSelection->fTauID->passIsolation(*iter) << std::endl;
      if (fTauSelection->fTauID->passIsolation(*iter)) return false;
    }
    return true;
  }

  const bool TauSelection::Data::selectedTauPassesDiscriminator(std::string discr, double cutPoint) const {
    if (!fPassedEvent) return false;
    return (getSelectedTau()->tauID(discr) > cutPoint);
  }
  
  // TauSelection methods ------------------------------------------------
  TauSelection::TauSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, std::string label):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fSelection(iConfig.getUntrackedParameter<std::string>("selection")),
    fTauID(0),
    fOperationMode(kNormalTauID),
    fTauFound(eventCounter.addSubCounter(label,"Tau found")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(label);
    
    // Create tauID algorithm handler
    //if(fSelection == "PFTauTaNCBased")
    //  fTauID = new TauIDPFTaNC(iConfig, eventCounter, eventWeight, "TaNC", myDir);
    if(fSelection == "HPSTauBased")
      fTauID = new TauIDPFHPS(iConfig, eventCounter, eventWeight, label+"_HPS", myDir);
    //else if(fSelection == "CombinedHPSTaNCTauBased")
    //  fTauID = new TauIDPFCombinedHPSTaNC(iConfig, eventCounter, eventWeight, "HPS+TaNC", myDir);
    else throw cms::Exception("Configuration") << "TauSelection: no or unknown tau selection used! Options for 'selection' are: HPSTauBased (you chose '" << fSelection << "')" << std::endl;
    
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
    int myTauJetPhiBins = 72; // five degrees
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
    hPtSelectedTauCandidates = makeTH<TH1F>(myDir,
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
    hEtaSelectedTauCandidates = makeTH<TH1F>(myDir,
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
    hEtaPhiSelectedTauCandidates = makeTH<TH2F>(myDir,
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
    hPhiSelectedTauCandidates = makeTH<TH1F>(myDir,
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
    hNumberOfSelectedTauCandidates = makeTH<TH1F>(myDir,
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
    hMCPurityOfSelectedTauCandidates = makeTH<TH1F>(myDir,
      "TauSelection_cleaned_tau_candidates_MC_purity",
      "cleaned_tau_candidates_MC_purity;;N_{jets}", 4, 0., 4.);
    hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(1, "#tau from H#pm");
    hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(2, "#tau from W#pm");
    hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(3, "Other #tau source");
    hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(4, "No MC #tau match");
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
    hTauIdOperatingMode = makeTH<TH1F>(myDir, "tauSelection_operating_mode", "tau_operating_mode;;N_{events}", 3, 0., 3.);
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(1, "Control");
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(2, "Normal tau ID");
    hTauIdOperatingMode->GetXaxis()->SetBinLabel(3, "tauCandidateSelectionOnly");

    hNTriggerMatchedTaus = makeTH<TH1F>(myDir, "N_TriggerMatchedTaus", "NTriggerMatchedTaus;N(trigger matched taus);N_{events}", 10, 0., 10.);
    hNTriggerMatchedSeparateTaus = makeTH<TH1F>(myDir, "N_TriggerMatchedSeparateTaus", "NTriggerMatchedSeparateTaus;N(trigger matched separate taus);N_{events}", 10, 0., 10.);

    hIsolationPFChargedHadrCandsPtSum = makeTH<TH1F>(myDir, "IsolationPFChargedHadrCandsPtSum", "IsolationPFChargedHadrCandsPtSum;IsolationPFChargedHadrCandsPtSum;N_{tau candidates}", 200, 0., 100.);
    hIsolationPFGammaCandsEtSum = makeTH<TH1F>(myDir, "IsolationPFGammaCandEtSum", "IsolationPFGammaCandEtSum;IsolationPFGammaCandEtSum;N_{tau candidates}", 200, 0., 100.);

    hTightChargedMaxPtBeforeIsolation = makeTH<TH1F>(myDir, "TightChargedMaxPtBeforeIsolation", "TightChargedMaxPtBeforeIsolation;TightChargedMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedSumPtBeforeIsolation = makeTH<TH1F>(myDir, "TightChargedSumPtBeforeIsolation", "TightChargedSumPtBeforeIsolation;TightChargedSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedOccupancyBeforeIsolation = makeTH<TH1F>(myDir, "TightChargedOccupancyBeforeIsolation", "TightChargedOccupancyBeforeIsolation;TightChargedOccupancy;N_{tau candidates}", 100, 0., 100.);
    hTightGammaMaxPtBeforeIsolation = makeTH<TH1F>(myDir, "TightGammaMaxPtBeforeIsolation", "TightGammaMaxPtBeforeIsolation;TightGammaMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaSumPtBeforeIsolation = makeTH<TH1F>(myDir, "TightGammaSumPtBeforeIsolation", "TightGammaSumPtBeforeIsolation;TightGammaSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaOccupancyBeforeIsolation = makeTH<TH1F>(myDir, "TightGammaOccupancyBeforeIsolation", "TightGammaOccupancyBeforeIsolation;TightGammaOccupancy;N_{tau candidates}", 100, 0., 100.); 
    
    hTightChargedMaxPtAfterIsolation = makeTH<TH1F>(myDir, "TightChargedMaxPtAfterIsolation", "TightChargedMaxPtAfterIsolation;TightChargedMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedSumPtAfterIsolation = makeTH<TH1F>(myDir, "TightChargedSumPtAfterIsolation", "TightChargedSumPtAfterIsolation;TightChargedSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedOccupancyAfterIsolation = makeTH<TH1F>(myDir, "TightChargedOccupancyAfterIsolation", "TightChargedOccupancyAfterIsolation;TightChargedOccupancy;N_{tau candidates}", 100, 0., 100.);
    hTightGammaMaxPtAfterIsolation = makeTH<TH1F>(myDir, "TightGammaMaxPtAfterIsolation", "TightGammaMaxPtAfterIsolation;TightGammaMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaSumPtAfterIsolation = makeTH<TH1F>(myDir, "TightGammaSumPtAfterIsolation", "TightGammaSumPtAfterIsolation;TightGammaSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaOccupancyAfterIsolation = makeTH<TH1F>(myDir, "TightGammaOccupancyAfterIsolation", "TightGammaOccupancyAfterIsolation;TightGammaOccupancy;N_{tau candidates}", 100, 0., 100.); 

    hHPSDecayMode = makeTH<TH1F>(myDir, "HPSDecayMode", "HPSDecayMode;HPSDecayMode;N_{tau candidates}",100,0,100);
    
    
    //tau->emFraction()
  }

  TauSelection::~TauSelection() {
    if (fTauID) delete fTauID;
  }

  TauSelection::Data TauSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {   
    bool passEvent = false;
    // Obtain tau collection from src specified in config
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fSrc, htaus);

    bool myRemoveFakeStatus = false;
    if (myRemoveFakeStatus && !iEvent.isRealData()) {
      edm::PtrVector<pat::Tau> myFilteredTaus;
      edm::Handle <reco::GenParticleCollection> genParticles;
      iEvent.getByLabel("genParticles", genParticles);
      for (edm::PtrVector<pat::Tau>::iterator it = htaus->ptrVector().begin(); it != htaus->ptrVector().end(); ++it) {
        // Remove fake taus from list
        bool myTauFoundStatus = false;
        bool myLeptonVetoStatus = false;
        for (size_t i=0; i < genParticles->size(); ++i) {
          const reco::Candidate & p = (*genParticles)[i];
          if (std::abs(p.pdgId()) == 11 || std::abs(p.pdgId()) == 13 || std::abs(p.pdgId()) == 15) {
            // Check match with tau
            if (reco::deltaR(p, (*it)->p4()) < 0.2) {
              if (p.pt() > 5.) {
              // match found
                if (std::abs(p.pdgId()) == 11 || std::abs(p.pdgId()) == 13) {
                  myLeptonVetoStatus = true;
                  i = genParticles->size(); // finish loop
                }
                if (std::abs(p.pdgId()) == 15) myTauFoundStatus = true;
              }
            }
          }
        }
        if (myTauFoundStatus && !myLeptonVetoStatus)
          myFilteredTaus.push_back(*it);
      } // end of tau loop
      passEvent = doTauSelection(iEvent,iSetup,myFilteredTaus);
      return Data(this, passEvent);
    }

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

/*  TauSelection::Data TauSelection::analyzeTriggerTau(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Obtain tau collection from src specified in config
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fSrc, htaus);
    edm::PtrVector<pat::Tau> taus = htaus->ptrVector();

    // Initialize
    fSelectedTaus.clear();
    fSelectedTaus.reserve(taus.size());
    fSelectedTauCandidates.clear();
    fSelectedTauCandidates.reserve(taus.size());
    fTauID->reset();

    // Require at least one tau in the trigger matched collection
    if (!taus.size()) return Data(this, false);
    increment(fTauFound);

    edm::PtrVector<pat::Tau> myBestTau;
    // Tau candidate selection
    edm::PtrVector<pat::Tau> myTauCandidates;
    for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter)
      if (fTauID->passDecayModeFinding(*iter) && fTauID->passKinematicSelection(*iter)) myTauCandidates.push_back(*iter);
    if (myTauCandidates.size() <= 1) {
      if (!myTauCandidates.size()) { // no taus left
	findBestTau(myBestTau, taus);
	fSelectedTaus.push_back(myBestTau[0]);
      } else // just one tau left
	fSelectedTaus.push_back(myTauCandidates[0]);
      return Data(this, true);
    }
    // Leading track cut
    edm::PtrVector<pat::Tau> myLdgTrackPassedTaus;
    for(edm::PtrVector<pat::Tau>::const_iterator iter = myTauCandidates.begin(); iter != myTauCandidates.end(); ++iter)
      if (fTauID->passLeadingTrackCuts(*iter)) myLdgTrackPassedTaus.push_back(*iter);
    if (myLdgTrackPassedTaus.size() <= 1) {
      if (!myLdgTrackPassedTaus.size()) {
	findBestTau(myBestTau, myTauCandidates);
	fSelectedTaus.push_back(myBestTau[0]);
      } else
	fSelectedTaus.push_back(myLdgTrackPassedTaus[0]);
      return Data(this, true);
    }
    // Lepton vetoes and fiducial cuts
    edm::PtrVector<pat::Tau> myLeptonVetoPassedTaus;
    for(edm::PtrVector<pat::Tau>::const_iterator iter = myLdgTrackPassedTaus.begin(); iter != myLdgTrackPassedTaus.end(); ++iter)
      if (fTauID->passECALFiducialCuts(*iter) && fTauID->passTauCandidateEAndMuVetoCuts(*iter)) myLeptonVetoPassedTaus.push_back(*iter);
    if (myLeptonVetoPassedTaus.size() <= 1) {
      if (!myLeptonVetoPassedTaus.size()) {
	findBestTau(myBestTau, myLdgTrackPassedTaus);
	fSelectedTaus.push_back(myBestTau[0]);
      } else
	fSelectedTaus.push_back(myLeptonVetoPassedTaus[0]);
      return Data(this, true);
    }
    // Isolation
    edm::PtrVector<pat::Tau> myIsolatedTaus;
    for(edm::PtrVector<pat::Tau>::const_iterator iter = myLeptonVetoPassedTaus.begin(); iter != myLeptonVetoPassedTaus.end(); ++iter)
      if (fTauID->passIsolation(*iter)) myIsolatedTaus.push_back(*iter);
    if (!myIsolatedTaus.size()) {
      findBestTau(myBestTau, myLeptonVetoPassedTaus);
      fSelectedTaus.push_back(myBestTau[0]);
    } else
      fSelectedTaus.push_back(myIsolatedTaus[0]);
    return Data(this, true);
  }*/

  bool TauSelection::doTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus){
    // Document operation mode
    fillOperationModeHistogram();
    
    // Initialize
    fSelectedTaus.clear();
    fSelectedTaus.reserve(taus.size());
    fSelectedTauCandidates.clear();
    fSelectedTauCandidates.reserve(taus.size());
    fTauID->reset();

    // Analyze the separation of the trigger matched taus
    if (taus.size() > 0) {
      int mySeparateCounter = 0;
      edm::Ptr<pat::Tau> myTau = taus[0];
      for (int i = 1; i < (int)taus.size(); ++i) {
        double myDeltaR = reco::deltaR(*myTau, *(taus[i]));
        if (myDeltaR>0.5) ++mySeparateCounter;
      }
      if (mySeparateCounter)
        hNTriggerMatchedSeparateTaus->Fill(taus.size(),fEventWeight.getWeight());
    }
    hNTriggerMatchedTaus->Fill(taus.size(),fEventWeight.getWeight());

    // Need std:vector in order to be able to use std::sort
    std::vector<edm::Ptr<pat::Tau> > tmpSelectedTauCandidates;
    std::vector<edm::Ptr<pat::Tau> > tmpSelectedTaus;

    // Loop over the taus
    for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
      const edm::Ptr<pat::Tau> iTau = *iter;

      fillHistogramsForTauCandidates(iTau, iEvent);
      
      // Tau candidate selections
      fTauID->incrementAllCandidates();
      if (!fTauID->passDecayModeFinding(iTau)) continue;
      if (!fTauID->passKinematicSelection(iTau)) continue;
      if (!fTauID->passLeadingTrackCuts(iTau)) continue;
      if (!fTauID->passECALFiducialCuts(iTau)) continue;
      if (!fTauID->passTauCandidateEAndMuVetoCuts(iTau)) continue;      
      fillHistogramsForSelectedTauCandidates(iTau, iEvent);
      tmpSelectedTauCandidates.push_back(iTau);
      
      // Tau ID selections
      if (fOperationMode == kNormalTauID) {
      
        // Standard tau ID (necessary for the tau selection logic) 
        hIsolationPFChargedHadrCandsPtSum->Fill(iTau->isolationPFChargedHadrCandsPtSum(), fEventWeight.getWeight());
        hIsolationPFGammaCandsEtSum->Fill(iTau->isolationPFGammaCandsEtSum(), fEventWeight.getWeight());

        hHPSDecayMode->Fill(iTau->decayMode(), fEventWeight.getWeight());

        hTightChargedMaxPtBeforeIsolation->Fill(iTau->userFloat("byTightChargedMaxPt"), fEventWeight.getWeight());
        hTightChargedSumPtBeforeIsolation->Fill(iTau->userFloat("byTightChargedSumPt"), fEventWeight.getWeight());
        hTightChargedOccupancyBeforeIsolation->Fill((float)iTau->userInt("byTightChargedOccupancy"), fEventWeight.getWeight());
        hTightGammaMaxPtBeforeIsolation->Fill(iTau->userFloat("byTightGammaMaxPt"), fEventWeight.getWeight());
        hTightGammaSumPtBeforeIsolation->Fill(iTau->userFloat("byTightGammaSumPt"), fEventWeight.getWeight());
        hTightGammaOccupancyBeforeIsolation->Fill((float)iTau->userInt("byTightGammaOccupancy"), fEventWeight.getWeight());
        if (!fTauID->passIsolation(iTau)) continue;
        hTightChargedMaxPtAfterIsolation->Fill(iTau->userFloat("byTightChargedMaxPt"), fEventWeight.getWeight());
        hTightChargedSumPtAfterIsolation->Fill(iTau->userFloat("byTightChargedSumPt"), fEventWeight.getWeight());
        hTightChargedOccupancyAfterIsolation->Fill((float)iTau->userInt("byTightChargedOccupancy"), fEventWeight.getWeight());
        hTightGammaMaxPtAfterIsolation->Fill(iTau->userFloat("byTightGammaMaxPt"), fEventWeight.getWeight());
        hTightGammaSumPtAfterIsolation->Fill(iTau->userFloat("byTightGammaSumPt"), fEventWeight.getWeight());
        hTightGammaOccupancyAfterIsolation->Fill((float)iTau->userInt("byTightGammaOccupancy"), fEventWeight.getWeight());
        if (!fTauID->passNProngsCut(iTau)) continue;
        if (!fTauID->passRTauCut(iTau)) continue;
      }

      // All cuts have been passed, save tau
      fillHistogramsForSelectedTaus(iTau, iEvent);
      tmpSelectedTaus.push_back(iTau);
    }
    // Sort taus in an order of isolation, most isolated first
    //std::sort(tmpSelectedTauCandidates.begin(), tmpSelectedTauCandidates.end(), isolationLessThan); // sort by isolation only
    //std::sort(tmpSelectedTaus.begin(), tmpSelectedTaus.end(), isolationLessThan);
    std::sort(tmpSelectedTauCandidates.begin(), tmpSelectedTauCandidates.end(), isolationProngRtauLessThan); // sort by isolation, prong and Rtau
    std::sort(tmpSelectedTaus.begin(), tmpSelectedTaus.end(), isolationProngRtauLessThan);
    for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i)
      fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
    for(size_t i=0; i<tmpSelectedTaus.size(); ++i)
      fSelectedTaus.push_back(tmpSelectedTaus[i]);
 

    // Handle counters
    fTauID->updatePassedCounters();
    // Fill number of taus histograms
    hNumberOfTauCandidates->Fill(static_cast<float>(taus.size()), fEventWeight.getWeight());
    hNumberOfSelectedTauCandidates->Fill(static_cast<float>(fSelectedTauCandidates.size()), fEventWeight.getWeight());
    if (fOperationMode != kTauCandidateSelectionOnly) {
      hNumberOfSelectedTaus->Fill(static_cast<float>(fSelectedTaus.size()), fEventWeight.getWeight());
    }

    // Handle result of tau candidate selection only
    if (fOperationMode == kTauCandidateSelectionOnly) {
      if (fSelectedTauCandidates.size()) {
        increment(fTauFound);
        return true;
      } else
        return false;
    }
   
    // Handle result of standard tau ID 
    if (fOperationMode == kNormalTauID) {
      if (fSelectedTaus.size()) {
	//	std::cout << " result true  " << std::endl;
        increment(fTauFound);
        return true;

      } else
        return false;
    }
    
    // Never reached
    return true;
  }

  void TauSelection::fillOperationModeHistogram() {
    hTauIdOperatingMode->Fill(0., fEventWeight.getWeight()); // Control
    if (fOperationMode == kNormalTauID)
      hTauIdOperatingMode->Fill(1., fEventWeight.getWeight());
    else if (fOperationMode == kTauCandidateSelectionOnly)
      hTauIdOperatingMode->Fill(2., fEventWeight.getWeight());
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
  
  void TauSelection::fillHistogramsForSelectedTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent) {
    double myTauPt = tau->pt();
    double myTauEta = tau->eta();
    double myTauPhi = tau->phi();
    hPtSelectedTauCandidates->Fill(myTauPt, fEventWeight.getWeight());
    hEtaSelectedTauCandidates->Fill(myTauEta, fEventWeight.getWeight());
    hPhiSelectedTauCandidates->Fill(myTauPhi, fEventWeight.getWeight());
    hEtaPhiSelectedTauCandidates->Fill(myTauEta, myTauPhi, fEventWeight.getWeight());

    // Purity
    if (!iEvent.isRealData()) {
      ObtainMCPurity(tau, iEvent, hMCPurityOfSelectedTauCandidates); 
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

/*  void TauSelection::findBestTau(edm::PtrVector<pat::Tau>& bestTau, edm::PtrVector<pat::Tau>& taus) {
    double myBestValue = 1e99;
    edm::Ptr<pat::Tau> myBestTau = taus[0];
    edm::PtrVector<pat::Tau> myIsolatedTaus;
    for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
      double myValue = (*iter)->userFloat("byTightChargedMaxPt");
      if (myValue < myBestValue) {
	if (myValue < 0.5) {
	  myIsolatedTaus.push_back(*iter);
	  myBestValue = 0.5;
	} else {
	  myBestValue = myValue;
	}
	myBestTau = *iter;
      }
    }
    // If there are isolated taus, return the one with highest pt
    if (myIsolatedTaus.size())
      bestTau.push_back(myIsolatedTaus[0]);
    else
      bestTau.push_back(myBestTau);
  }*/
  
}
