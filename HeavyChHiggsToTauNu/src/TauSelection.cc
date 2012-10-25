#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

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

#include<functional>

namespace {
  
  bool tauEtGreaterThan(const edm::Ptr<pat::Tau>& a, const edm::Ptr<pat::Tau>& b) {
    return (a->pt() > b->pt());
  }

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
/*
  bool isolationProngRtauLessThan(const edm::Ptr<pat::Tau>& a, const edm::Ptr<pat::Tau>& b) {
    // FIXME: not safe to use this method. better to first look at nprongs and rtau and after that make comparison based on isolation

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
    size_t aProng = a->signalPFChargedHadrCands().size(); // FIXdoes not work for TCTau
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
  }*/

  struct MoreLikelyTauCompare: std::binary_function<edm::Ptr<pat::Tau>, edm::Ptr<pat::Tau>, bool> {
    MoreLikelyTauCompare(HPlus::TauIDBase *tauID): fTauID(tauID) {}

    bool operator()(const edm::Ptr<pat::Tau>& tauA, const edm::Ptr<pat::Tau>& tauB) {
      bool result = firstIsMoreLikely(tauA, tauB);
      //std::cout << "Is left-one more likely? " << result << std::endl;
      return result;
    }

    bool firstIsMoreIsolatedLargerPt(const edm::Ptr<pat::Tau>& tauA, const edm::Ptr<pat::Tau>& tauB) {
      bool resA = fTauID->passIsolation(tauA);
      bool resB = fTauID->passIsolation(tauB);
      /*
      std::cout << "  Isolation " << resA << " (" << tauA->tauID("byRawCombinedIsolationDeltaBetaCorr")
                << ") " << resB << " (" << tauB->tauID("byRawCombinedIsolationDeltaBetaCorr")
                << ")" << std::endl;
      */
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        // Both fail isolation, comparison by isolation is ok
        return tauA->tauID("byRawCombinedIsolationDeltaBetaCorr") < tauB->tauID("byRawCombinedIsolationDeltaBetaCorr");

      // Both pass isolation, compare by pt
      return tauA->pt() > tauB->pt();
    }

    bool firstIsMoreLikely(const edm::Ptr<pat::Tau>& tauA, const edm::Ptr<pat::Tau>& tauB) {
      bool resA;
      bool resB;

      // DecayModeFinding
      resA = fTauID->passDecayModeFinding(tauA);
      resB = fTauID->passDecayModeFinding(tauB);
      //std::cout << std::endl << "DecayModeFinding " << resA << " " << resB << std::endl;
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        // ??? pick one with larger pt, isolation doesn't really make sense because it requires decay mode internally
        return tauA->pt() > tauB->pt();

      // pT
      resA = fTauID->passKinematicSelectionPt(tauA);
      resB = fTauID->passKinematicSelectionPt(tauB);
      //std::cout << "pT " << resA << " (" << tauA->pt() << ") " << resB << " (" << tauB->pt() << ")" << std::endl;
      if(resA != resB)
        return resA;
      if(!resA && !resB) {
        //return tauA->pt() > tauB->pt();
        return firstIsMoreIsolatedLargerPt(tauA, tauB);
      }
    
      // eta
      resA = fTauID->passKinematicSelectionEta(tauA);
      resB = fTauID->passKinematicSelectionEta(tauB);
      //std::cout << "eta " << resA << " (" << tauA->eta() << ") " << resB << " (" << tauB->eta() << ")" << std::endl;
      if(resA != resB)
        return resA;
      if(!resA && !resB) {
        //return std::abs(tauA->eta()) < std::abs(tauB->eta());
        return firstIsMoreIsolatedLargerPt(tauA, tauB);
      }

      // leading track
      resA = fTauID->passLeadingTrackCuts(tauA);
      resB = fTauID->passLeadingTrackCuts(tauB);
      //std::cout << "LeadingTrack " << resA << " " << resB << std::endl;
      if(resA != resB)
        return resA;
      if(!resA && !resB) {
        /*
        resA = tauA->leadPFChargedHadrCand().isNull();
        resB = tauB->leadPFChargedHadrCand().isNull();
        std::cout << "LeadingTrack failed, does exist? " << resA << " " << resB << std::endl;
        if(resA != resB)
          return resA;
        if(!resA && !resB) {
          // ??? pick one with larger pt
          return tauA->pt() > tauB->pt();
        }
        std::cout << "LeadingTrack failed, exists, pT " << tauA->leadPFChargedHadrCand()->pt() << " " << tauB->leadPFChargedHadrCand()->pt() << std::endl;
        // both have leading track, comparison with leading track pt
        return tauA->leadPFChargedHadrCand()->pt() > tauB->leadPFChargedHadrCand()->pt();
        */
        return firstIsMoreIsolatedLargerPt(tauA, tauB);
      }

      // ECAL Fiducial
      resA = fTauID->passECALFiducialCuts(tauA);
      resB = fTauID->passECALFiducialCuts(tauB);
      //std::cout << "ECAL fiducial cuts " << resA << " " << resB << std::endl;
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        return firstIsMoreIsolatedLargerPt(tauA, tauB);

      // E veto
      resA = fTauID->passTauCandidateEVetoCuts(tauA);
      resB = fTauID->passTauCandidateEVetoCuts(tauB);
      //std::cout << "againstElectron " << resA << " " << resB << std::endl;
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        return firstIsMoreIsolatedLargerPt(tauA, tauB);

      // Mu veto
      resA = fTauID->passTauCandidateMuVetoCuts(tauA);
      resB = fTauID->passTauCandidateMuVetoCuts(tauB);
      //std::cout << "againstMuon " << resA << " " << resB << std::endl;
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        return firstIsMoreIsolatedLargerPt(tauA, tauB);

      // Dead cells
      resA = fTauID->passVetoAgainstDeadECALCells(tauA);
      resB = fTauID->passVetoAgainstDeadECALCells(tauB);
      //std::cout << "ECAL dead cells " << resA << " " << resB << std::endl;
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        return firstIsMoreIsolatedLargerPt(tauA, tauB);

      // isolation
      resA = fTauID->passIsolation(tauA);
      resB = fTauID->passIsolation(tauB);
      /*
      std::cout << "Isolation " << resA << " (" << tauA->tauID("byRawCombinedIsolationDeltaBetaCorr")
                << ") " << resB << " (" << tauB->tauID("byRawCombinedIsolationDeltaBetaCorr")
                << ")" << std::endl;
      */
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        return tauA->tauID("byRawCombinedIsolationDeltaBetaCorr") < tauB->tauID("byRawCombinedIsolationDeltaBetaCorr");

      // nprongs
      resA = fTauID->passNProngsCut(tauA);
      resB = fTauID->passNProngsCut(tauB);
      //std::cout << "NProngs " << resA << " " << resB << std::endl;
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        // ??? pick one with larger pt
        return tauA->pt() > tauB->pt();
  
      // Rtau        
      resA = fTauID->passRTauCut(tauA);
      resB = fTauID->passRTauCut(tauB);
      /*
      std::cout << "Rtau " << resA << " (" << fTauID->getRtauValue(tauA)
                << ") " << resB << " (" << fTauID->getRtauValue(tauB)
                << ")" << std::endl;
      */
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        return fTauID->getRtauValue(tauA) > fTauID->getRtauValue(tauB);

      // Still here? Can I do anything more intelligent than compare pT?
      return tauA->pt() > tauB->pt();
    }

    HPlus::TauIDBase *fTauID;
  };
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

  const bool TauSelection::Data::selectedTauPassesNProngsAndRtauButNotIsolation() const {
    if (selectedTauPassesNProngs() && selectedTauPassesRtau()) {
      return (!fTauSelection->fTauID->passIsolation(getSelectedTau()));
    }
    return false;
  }

  const bool TauSelection::Data::selectedTauPassesDiscriminator(std::string discr, double cutPoint) const {
    if (!fPassedEvent) return false;
    return (getSelectedTau()->tauID(discr) > cutPoint);
  }
  
  // TauSelection methods ------------------------------------------------
  TauSelection::TauSelection(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper, std::string label):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fSelection(iConfig.getUntrackedParameter<std::string>("selection")),
    fAnalyseFakeTauComposition(iConfig.getUntrackedParameter<bool>("analyseFakeTauComposition")),
    fTauID(0),
    fOperationMode(kNormalTauID),
    fTauFound(eventCounter.addSubCounter(label,"Tau found"))
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(label);
    
    // Create tauID algorithm handler
    //if(fSelection == "PFTauTaNCBased")
    //  fTauID = new TauIDPFTaNC(iConfig, eventCounter, histoWrapper, "TaNC", myDir);
    if(fSelection == "HPSTauBased")
      fTauID = new TauIDPFHPS(iConfig, eventCounter, histoWrapper, label+"_HPS", myDir);
    //else if(fSelection == "CombinedHPSTaNCTauBased")
    //  fTauID = new TauIDPFCombinedHPSTaNC(iConfig, eventCounter, histoWrapper, "HPS+TaNC", myDir);
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
    hPtTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_all_tau_candidates_pt",
      "selected_tau_pt;#tau p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myTauJetPtBins, myTauJetPtMin, myTauJetPtMax);
    hPtSelectedTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_cleaned_tau_candidates_pt",
      "selected_tau_pt;#tau p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myTauJetPtBins, myTauJetPtMin, myTauJetPtMax);
    hPtSelectedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir,
      "TauSelection_selected_taus_pt",
      "selected_tau_pt;#tau p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myTauJetPtBins, myTauJetPtMin, myTauJetPtMax);
    // Eta
    hEtaTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_all_tau_candidates_eta",
      "tau_candidates_eta;#tau #eta;N_{jets} / 0.1",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax);
    hEtaSelectedTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_cleaned_tau_candidates_eta",
      "cleaned_tau_candidates_eta;#tau #eta;N_{jets} / 0.1",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax);
    hEtaSelectedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir,
      "TauSelection_selected_taus_eta",
      "selected_tau_eta;#tau #eta;N_{jets} / 0.1",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax);
    // Eta vs. phi
    hEtaPhiTauCandidates = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir,
      "TauSelection_all_tau_candidates_eta_vs_phi",
      "tau_candidates_eta_vs_phi;#tau #eta;#tau phi",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax,
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    hEtaPhiSelectedTauCandidates = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir,
      "TauSelection_cleaned_tau_candidates_eta_vs_phi",
      "cleaned_tau_candidates_eta_vs_phi;#tau #eta;#tau phi",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax,
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    hEtaPhiSelectedTaus = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir,
      "TauSelection_selected_taus_eta_vs_phi",
      "selected_tau_eta_vs_phi;#tau #eta;#tau phi",
      myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax,
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    // Phi
    hPhiTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_all_tau_candidates_phi",
      "tau_candidates_phi;#tau #phi;N_{jets} / 0.087",
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    hPhiSelectedTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_cleaned_tau_candidates_phi",
      "cleaned_tau_candidates_phi;#tau #phi;N_{jets} / 0.087",
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    hPhiSelectedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_selected_taus_phi",
      "selected_tau_phi;#tau #phi;N_{jets} / 0.087",
      myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    // N
    hNumberOfTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_all_tau_candidates_N",
      "tau_candidates_N;Number of #tau's;N_{jets}",
      myTauJetNumberBins, myTauJetNumberMin, myTauJetNumberMax);
    hNumberOfSelectedTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_cleaned_tau_candidates_N",
      "cleaned_tau_candidates_N;Number of #tau's;N_{jets}",
      myTauJetNumberBins, myTauJetNumberMin, myTauJetNumberMax);
    hNumberOfSelectedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir,
      "TauSelection_selected_taus_N",
      "selected_tau_N;Number of #tau's;N_{jets}",
      myTauJetNumberBins, myTauJetNumberMin, myTauJetNumberMax);
    // MC purity
    hMCPurityOfTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_all_tau_candidates_MC_purity",
      "tau_candidates_MC_purity;;N_{jets}", 4, 0., 4.);
    if (hMCPurityOfTauCandidates->isActive()) {
      hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(1, "#tau from H#pm");
      hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(2, "#tau from W#pm");
      hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(3, "Other #tau source");
      hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(4, "No MC #tau match");
    }
    hMCPurityOfSelectedTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_cleaned_tau_candidates_MC_purity",
      "cleaned_tau_candidates_MC_purity;;N_{jets}", 4, 0., 4.);
    if (hMCPurityOfSelectedTauCandidates->isActive()) {
      hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(1, "#tau from H#pm");
      hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(2, "#tau from W#pm");
      hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(3, "Other #tau source");
      hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(4, "No MC #tau match");
    }
    hMCPurityOfSelectedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_selected_taus_MC_purity",
      "selected_tau_MC_purity;;N_{jets}", 4, 0., 4.);
    if (hMCPurityOfSelectedTaus->isActive()) {
      hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(1, "#tau from H#pm");
      hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(2, "#tau from W#pm");
      hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(3, "Other #tau source");
      hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(4, "No MC #tau match");
    }

    // Isolation variables
    hVLooseIsoNcands = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TauSelection_all_tau_candidates_VLooseIsoNCands", "Number of isolation candidates in VLoose", 100, 0, 100);
    hLooseIsoNcands = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TauSelection_all_tau_candidates_LooseIsoNCands", "Number of isolation candidates in Loose", 100, 0, 100);
    hMediumIsoNcands = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TauSelection_all_tau_candidates_MediumIsoNCands", "Number of isolation candidates in Medium", 100, 0, 100);
    hTightIsoNcands = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TauSelection_all_tau_candidates_TightIsoNCands", "Number of isolation candidates in Tight", 100, 0, 100);

    // Operating mode of tau ID -- for quick validating that tau selection is doing what is expected 
    hTauIdOperatingMode = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "tauSelection_operating_mode", "tau_operating_mode;;N_{events}", 3, 0., 3.);
    if (hTauIdOperatingMode->isActive()) {
      hTauIdOperatingMode->GetXaxis()->SetBinLabel(1, "Control");
      hTauIdOperatingMode->GetXaxis()->SetBinLabel(2, "Normal tau ID");
      hTauIdOperatingMode->GetXaxis()->SetBinLabel(3, "tauCandidateSelectionOnly");
    }

    hNTriggerMatchedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "N_TriggerMatchedTaus", "NTriggerMatchedTaus;N(trigger matched taus);N_{events}", 10, 0., 10.);
    hNTriggerMatchedSeparateTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "N_TriggerMatchedSeparateTaus", "NTriggerMatchedSeparateTaus;N(trigger matched separate taus);N_{events}", 10, 0., 10.);

    hIsolationPFChargedHadrCandsPtSum = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "IsolationPFChargedHadrCandsPtSum", "IsolationPFChargedHadrCandsPtSum;IsolationPFChargedHadrCandsPtSum;N_{tau candidates}", 200, 0., 100.);
    hIsolationPFGammaCandsEtSum = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "IsolationPFGammaCandEtSum", "IsolationPFGammaCandEtSum;IsolationPFGammaCandEtSum;N_{tau candidates}", 200, 0., 100.);

    hTightChargedMaxPtBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightChargedMaxPtBeforeIsolation", "TightChargedMaxPtBeforeIsolation;TightChargedMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedSumPtBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightChargedSumPtBeforeIsolation", "TightChargedSumPtBeforeIsolation;TightChargedSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedOccupancyBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightChargedOccupancyBeforeIsolation", "TightChargedOccupancyBeforeIsolation;TightChargedOccupancy;N_{tau candidates}", 100, 0., 100.);
    hTightGammaMaxPtBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightGammaMaxPtBeforeIsolation", "TightGammaMaxPtBeforeIsolation;TightGammaMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaSumPtBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightGammaSumPtBeforeIsolation", "TightGammaSumPtBeforeIsolation;TightGammaSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaOccupancyBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightGammaOccupancyBeforeIsolation", "TightGammaOccupancyBeforeIsolation;TightGammaOccupancy;N_{tau candidates}", 100, 0., 100.); 

    hTightChargedMaxPtAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightChargedMaxPtAfterIsolation", "TightChargedMaxPtAfterIsolation;TightChargedMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedSumPtAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightChargedSumPtAfterIsolation", "TightChargedSumPtAfterIsolation;TightChargedSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedOccupancyAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightChargedOccupancyAfterIsolation", "TightChargedOccupancyAfterIsolation;TightChargedOccupancy;N_{tau candidates}", 100, 0., 100.);
    hTightGammaMaxPtAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightGammaMaxPtAfterIsolation", "TightGammaMaxPtAfterIsolation;TightGammaMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaSumPtAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightGammaSumPtAfterIsolation", "TightGammaSumPtAfterIsolation;TightGammaSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaOccupancyAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, myDir, "TightGammaOccupancyAfterIsolation", "TightGammaOccupancyAfterIsolation;TightGammaOccupancy;N_{tau candidates}", 100, 0., 100.); 

    hHPSDecayMode = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HPSDecayMode", "HPSDecayMode;HPSDecayMode;N_{tau candidates}",100,0,100);

    if (fAnalyseFakeTauComposition) {
      std::string myFakeLabel = label+"_fakeAnalysis";
      TFileDirectory myFakeDir = fs->mkdir(myFakeLabel);
      hFakeElectronEtaPhiAfterKinematics = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "eToTauAfterKinematicalCuts", "eToTauAfterKinematicalCuts;e#rightarrow#tau #eta;e#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeElectronEtaPhiAfterAgainstElectron = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "eToTauAfterAgainstElectron", "eToTauAfterAgainstElectron;e#rightarrow#tau #eta;e#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeElectronEtaPhiAfterAgainstElectronAndDeadVeto = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "eToTauAfterAgainstElectronAndDeadVeto", "eToTauAfterAgainstElectronAndDeadVeto;e#rightarrow#tau #eta;e#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeElectronEtaPhiAfterIsolation = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "eToTauAfterIsolation", "eToTauAfterIsolation;e#rightarrow#tau #eta;e#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeElectronEtaPhiAfterIsolationAndDeadVeto = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "eToTauAfterIsolationAndDeadVeto", "eToTauAfterIsolationAndDeadVeto;e#rightarrow#tau #eta;e#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeElectronEtaPhiAfterNProngs = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "eToTauAfterNProngs", "eToTauAfterNProngs;e#rightarrow#tau #eta;e#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeElectronEtaPhiAfterNProngsAndDeadVeto = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "eToTauAfterNProngsAndDeadVeto", "eToTauAfterNProngsAndDeadVeto;e#rightarrow#tau #eta;e#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);

      hFakeJetEtaPhiAfterKinematics = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "jetToTauAfterKinematicalCuts", "jetToTauAfterKinematicalCuts;jet#rightarrow#tau #eta;jet#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeJetEtaPhiAfterAgainstElectron = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "jetToTauAfterAgainstElectron", "jetToTauAfterAgainstElectron;jet#rightarrow#tau #eta;jet#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeJetEtaPhiAfterAgainstElectronAndDeadVeto = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "jetToTauAfterAgainstElectronAndDeadVeto", "jetToTauAfterAgainstElectronAndDeadVeto;jet#rightarrow#tau #eta;jet#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeJetEtaPhiAfterIsolation = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "jetToTauAfterIsolation", "jetToTauAfterIsolation;jet#rightarrow#tau #eta;jet#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeJetEtaPhiAfterIsolationAndDeadVeto = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "jetToTauAfterIsolationAndDeadVeto", "jetToTauAfterIsolationAndDeadVeto;jet#rightarrow#tau #eta;jet#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeJetEtaPhiAfterNProngs = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "jetToTauAfterNProngs", "jetToTauAfterNProngs;jet#rightarrow#tau #eta;jet#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hFakeJetEtaPhiAfterNProngsAndDeadVeto = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "jetToTauAfterNProngsAndDeadVeto", "jetToTauAfterNProngsAndDeadVeto;jet#rightarrow#tau #eta;jet#rightarrow#tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);

      hGenuineTauEtaPhiAfterKinematics = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "GenuineTauAfterKinematicalCuts", "GenuineTauAfterKinematicalCuts;Genuine #tau #eta;Genuine #tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hGenuineTauEtaPhiAfterAgainstElectron = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "GenuineTauAfterAgainstElectron", "GenuineTauAfterAgainstElectron;Genuine #tau #eta;Genuine #tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hGenuineTauEtaPhiAfterAgainstElectronAndDeadVeto = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "GenuineTauAfterAgainstElectronAndDeadVeto", "GenuineTauAfterAgainstElectronAndDeadVeto;Genuine #tau #eta;Genuine #tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hGenuineTauEtaPhiAfterIsolation = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "GenuineTauAfterIsolation", "GenuineTauAfterIsolation;Genuine #tau #eta;Genuine #tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hGenuineTauEtaPhiAfterIsolationAndDeadVeto = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "GenuineTauAfterIsolationAndDeadVeto", "GenuineTauAfterIsolationAndDeadVeto;Genuine #tau #eta;Genuine #tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hGenuineTauEtaPhiAfterNProngs = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "GenuineTauAfterNProngs", "GenuineTauAfterNProngs;Genuine #tau #eta;Genuine #tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
      hGenuineTauEtaPhiAfterNProngsAndDeadVeto = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFakeDir,
        "GenuineTauAfterNProngsAndDeadVeto", "GenuineTauAfterNProngsAndDeadVeto;Genuine #tau #eta;Genuine #tau phi", myTauJetEtaBins, myTauJetEtaMin, myTauJetEtaMax, myTauJetPhiBins, myTauJetPhiMin, myTauJetPhiMax);
    }
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
        hNTriggerMatchedSeparateTaus->Fill(taus.size());
    }
    hNTriggerMatchedTaus->Fill(taus.size());

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
      if (!fTauID->passVetoAgainstDeadECALCells(iTau)) continue;
      fillHistogramsForSelectedTauCandidates(iTau, iEvent);
      tmpSelectedTauCandidates.push_back(iTau);
      
      // Tau ID selections
      if (fOperationMode == kNormalTauID) {
      
        // Standard tau ID (necessary for the tau selection logic) 
        hIsolationPFChargedHadrCandsPtSum->Fill(iTau->isolationPFChargedHadrCandsPtSum());
        hIsolationPFGammaCandsEtSum->Fill(iTau->isolationPFGammaCandsEtSum());

        hHPSDecayMode->Fill(iTau->decayMode());


        hTightChargedMaxPtBeforeIsolation->Fill(iTau->userFloat("byTightChargedMaxPt"));
        hTightChargedSumPtBeforeIsolation->Fill(iTau->userFloat("byTightChargedSumPt"));
        hTightChargedOccupancyBeforeIsolation->Fill((float)iTau->userInt("byTightChargedOccupancy"));
        hTightGammaMaxPtBeforeIsolation->Fill(iTau->userFloat("byTightGammaMaxPt"));
        hTightGammaSumPtBeforeIsolation->Fill(iTau->userFloat("byTightGammaSumPt"));
        hTightGammaOccupancyBeforeIsolation->Fill((float)iTau->userInt("byTightGammaOccupancy"));
        if (!fTauID->passIsolation(iTau)) continue;
        hTightChargedMaxPtAfterIsolation->Fill(iTau->userFloat("byTightChargedMaxPt"));
        hTightChargedSumPtAfterIsolation->Fill(iTau->userFloat("byTightChargedSumPt"));
        hTightChargedOccupancyAfterIsolation->Fill((float)iTau->userInt("byTightChargedOccupancy"));
        hTightGammaMaxPtAfterIsolation->Fill(iTau->userFloat("byTightGammaMaxPt"));
        hTightGammaSumPtAfterIsolation->Fill(iTau->userFloat("byTightGammaSumPt"));
        hTightGammaOccupancyAfterIsolation->Fill((float)iTau->userInt("byTightGammaOccupancy"));

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
    std::sort(tmpSelectedTauCandidates.begin(), tmpSelectedTauCandidates.end(), tauEtGreaterThan); // sort by Et

    // Sort tau candidates into order of likeliness of passing the full tau ID (a bit complicated)
    // 1) Check if more than 1 tau candidate passes isolation cut
    std::vector<edm::Ptr<pat::Tau> > tmpIsolationPassed;
    std::vector<edm::Ptr<pat::Tau> > tmpNprongPassed;
    std::vector<edm::Ptr<pat::Tau> > tmpRtauPassed;
    for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
      if (fTauID->passIsolation(tmpSelectedTauCandidates[i]))
        tmpIsolationPassed.push_back(tmpSelectedTauCandidates[i]);
    }
    if (tmpIsolationPassed.size() == 0) {
      // none pass, just take the most isolated one
      std::sort(tmpSelectedTauCandidates.begin(), tmpSelectedTauCandidates.end(), isolationLessThan);
    } else if (tmpIsolationPassed.size() == 1) {
      // Put the found one to the top of the list
      fSelectedTauCandidates.push_back(tmpIsolationPassed[0]);
      for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
        if (!fTauID->passIsolation(tmpSelectedTauCandidates[i]))
          fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
      }
    } else {
      // 2) Multiple taus have passed isolation, lets see how many pass also the nprongs cut
      std::sort(tmpIsolationPassed.begin(), tmpIsolationPassed.end(), isolationLessThan);
      for(size_t i=0; i<tmpIsolationPassed.size(); ++i) {
        if (fTauID->passNProngsCut(tmpIsolationPassed[i]))
          tmpNprongPassed.push_back(tmpIsolationPassed[i]);
      }
      if (tmpNprongPassed.size() == 0) {
        // none pass, take the most isolated one
        for(size_t i=0; i<tmpIsolationPassed.size(); ++i) {
          fSelectedTauCandidates.push_back(tmpIsolationPassed[i]);
        }
        for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
          bool match = false;
          for(size_t j=0; j<tmpIsolationPassed.size(); ++j) {
            if (tmpSelectedTauCandidates[i] == tmpIsolationPassed[j])
              match = true;
          }
          if (!match) fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
        }
      } else if (tmpNprongPassed.size() == 1) {
        // Put the passed one to the top of the list
        fSelectedTauCandidates.push_back(tmpNprongPassed[0]);
        for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
          if (tmpSelectedTauCandidates[i] != tmpNprongPassed[0])
            fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
        }
      } else {
        // 3) Multiple taus have passed nprongs, lets see how many pass also the rtau cut
        for(size_t i=0; i<tmpNprongPassed.size(); ++i) {
          if (fTauID->passRTauCut(tmpNprongPassed[i]))
            tmpRtauPassed.push_back(tmpNprongPassed[i]);
        }
        if (tmpRtauPassed.size() == 0) {
          // none pass, just take the most isolated one
          std::sort(tmpNprongPassed.begin(), tmpNprongPassed.end(), isolationLessThan);
          for(size_t i=0; i<tmpNprongPassed.size(); ++i) {
            fSelectedTauCandidates.push_back(tmpNprongPassed[i]);
          }
          for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
            bool match = false;
            for(size_t j=0; j<tmpNprongPassed.size(); ++j) {
              if (tmpSelectedTauCandidates[i] == tmpNprongPassed[j])
                match = true;
            }
            if (!match) fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
          }
        } else if (tmpRtauPassed.size() == 1) {
          // Put the one that passed both nprongs and rtau to the top of the list
          fSelectedTauCandidates.push_back(tmpRtauPassed[0]);
          for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
            if (tmpSelectedTauCandidates[i] != tmpRtauPassed[0])
              fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
          }
        } else {
          // 4) Multiple taus have passed nprongs, rtau, and isolation; take most energetic one
          std::sort(tmpRtauPassed.begin(), tmpRtauPassed.end(), tauEtGreaterThan);
          for(size_t i=0; i<tmpRtauPassed.size(); ++i) {
            fSelectedTauCandidates.push_back(tmpRtauPassed[i]);
          }
        }
      }
    }
    if (fSelectedTauCandidates.size() == 0) {
      for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i)
        fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
    }

    // Sort selected taus (i.e. passed full tau ID) by Et
    std::sort(tmpSelectedTaus.begin(), tmpSelectedTaus.end(), tauEtGreaterThan);
    for(size_t i=0; i<tmpSelectedTaus.size(); ++i)
      fSelectedTaus.push_back(tmpSelectedTaus[i]);


    // Handle counters
    fTauID->updatePassedCounters();
    // Fill number of taus histograms
    hNumberOfTauCandidates->Fill(static_cast<float>(taus.size()));
    hNumberOfSelectedTauCandidates->Fill(static_cast<float>(fSelectedTauCandidates.size()));
    if (fOperationMode != kTauCandidateSelectionOnly) {
      hNumberOfSelectedTaus->Fill(static_cast<float>(fSelectedTaus.size()));
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
    hTauIdOperatingMode->Fill(0.); // Control
    if (fOperationMode == kNormalTauID)
      hTauIdOperatingMode->Fill(1.);
    else if (fOperationMode == kTauCandidateSelectionOnly)
      hTauIdOperatingMode->Fill(2.);
  }

  void TauSelection::fillHistogramsForTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent) {
    double myTauPt = tau->pt();
    double myTauEta = tau->eta();
    double myTauPhi = tau->phi();
    hPtTauCandidates->Fill(myTauPt);
    hEtaTauCandidates->Fill(myTauEta);
    hPhiTauCandidates->Fill(myTauPhi);
    hEtaPhiTauCandidates->Fill(myTauEta, myTauPhi);
    // Purity
    if (!iEvent.isRealData()) {
      ObtainMCPurity(tau, iEvent, hMCPurityOfTauCandidates);
    }

    hVLooseIsoNcands->Fill(tau->userInt("byVLooseOccupancy"));
    hLooseIsoNcands->Fill(tau->userInt("byLooseOccupancy"));
    hMediumIsoNcands->Fill(tau->userInt("byMediumOccupancy"));
    hTightIsoNcands->Fill(tau->userInt("byTightOccupancy"));
  }
  
  void TauSelection::fillHistogramsForSelectedTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent) {
    double myTauPt = tau->pt();
    double myTauEta = tau->eta();
    double myTauPhi = tau->phi();
    hPtSelectedTauCandidates->Fill(myTauPt);
    hEtaSelectedTauCandidates->Fill(myTauEta);
    hPhiSelectedTauCandidates->Fill(myTauPhi);
    hEtaPhiSelectedTauCandidates->Fill(myTauEta, myTauPhi);

    // Purity
    if (!iEvent.isRealData()) {
      ObtainMCPurity(tau, iEvent, hMCPurityOfSelectedTauCandidates);
    }
  }
  
  void TauSelection::fillHistogramsForSelectedTaus(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent) {
    double myTauPt = tau->pt();
    double myTauEta = tau->eta();
    double myTauPhi = tau->phi();
    hPtSelectedTaus->Fill(myTauPt);
    hEtaSelectedTaus->Fill(myTauEta);

    hPhiSelectedTaus->Fill(myTauPhi);
    hEtaPhiSelectedTaus->Fill(myTauEta, myTauPhi);

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

  void TauSelection::ObtainMCPurity(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent, WrappedTH1* histogram) {
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
              histogram->Fill(0.);
              return;
            }
            if (idmother == 24) { // W+
              histogram->Fill(1.);
              return;
            }
          }
          histogram->Fill(2.); // Other source of tau (B decays)
        }
      }
    }
    histogram->Fill(3.); // No MC match found
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

  // Notice that using this routine will cause tau ID histograms to be filled multiple times
  void TauSelection::analyseFakeTauComposition(FakeTauIdentifier& fakeTauIdentifier, const edm::Event& iEvent) {
    if (!fAnalyseFakeTauComposition) return;
    // Get taus
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fSrc, htaus);
    for(edm::PtrVector<pat::Tau>::const_iterator iter = htaus->ptrVector().begin(); iter != htaus->ptrVector().end(); ++iter) {
      const edm::Ptr<pat::Tau> iTau = *iter;
      FakeTauIdentifier::MCSelectedTauMatchType myTauMatch = fakeTauIdentifier.matchTauToMC(iEvent, *iTau);
      bool isElectron = (myTauMatch == FakeTauIdentifier::kkElectronToTau || myTauMatch == FakeTauIdentifier::kkElectronToTauAndTauOutsideAcceptance);
      bool isJet = (myTauMatch == FakeTauIdentifier::kkJetToTau || myTauMatch == FakeTauIdentifier::kkJetToTauAndTauOutsideAcceptance);
      bool isTau = (myTauMatch == FakeTauIdentifier::kkTauToTau || myTauMatch == FakeTauIdentifier::kkTauToTauAndTauOutsideAcceptance);
      bool isAtDeadCell = !fTauID->passVetoAgainstDeadECALCells(iTau);
      // Tau candidate selections
      if (!fTauID->passDecayModeFinding(iTau)) continue;
      if (!fTauID->passKinematicSelection(iTau)) continue;
      if (!fTauID->passLeadingTrackCuts(iTau)) continue;
      //if (!fTauID->passECALFiducialCuts(iTau)) continue;
      if (isElectron) {
        hFakeElectronEtaPhiAfterKinematics->Fill(iTau->eta(),iTau->phi());
      } else if (isJet) {
        hFakeJetEtaPhiAfterKinematics->Fill(iTau->eta(),iTau->phi());
      } else if (isTau) {
        hGenuineTauEtaPhiAfterKinematics->Fill(iTau->eta(),iTau->phi());
      }

      if (!fTauID->passTauCandidateEAndMuVetoCuts(iTau)) continue;
      if (isElectron) {
        hFakeElectronEtaPhiAfterAgainstElectron->Fill(iTau->eta(),iTau->phi());
        if (!isAtDeadCell) hFakeElectronEtaPhiAfterAgainstElectronAndDeadVeto->Fill(iTau->eta(),iTau->phi());
      } else if (isJet) {
        hFakeJetEtaPhiAfterAgainstElectron->Fill(iTau->eta(),iTau->phi());
        if (!isAtDeadCell) hFakeJetEtaPhiAfterAgainstElectronAndDeadVeto->Fill(iTau->eta(),iTau->phi());
      } else if (isTau) {
        hGenuineTauEtaPhiAfterAgainstElectron->Fill(iTau->eta(),iTau->phi());
        if (!isAtDeadCell) hGenuineTauEtaPhiAfterAgainstElectronAndDeadVeto->Fill(iTau->eta(),iTau->phi());
      }

      // Tau ID selections
      if (!fTauID->passIsolation(iTau)) continue;
      if (isElectron) {
        hFakeElectronEtaPhiAfterIsolation->Fill(iTau->eta(),iTau->phi());
        if (!isAtDeadCell) hFakeElectronEtaPhiAfterIsolationAndDeadVeto->Fill(iTau->eta(),iTau->phi());
      } else if (isJet) {
        hFakeJetEtaPhiAfterIsolation->Fill(iTau->eta(),iTau->phi());
        if (!isAtDeadCell) hFakeJetEtaPhiAfterIsolationAndDeadVeto->Fill(iTau->eta(),iTau->phi());
      } else if (isTau) {
        hGenuineTauEtaPhiAfterIsolation->Fill(iTau->eta(),iTau->phi());
        if (!isAtDeadCell) hGenuineTauEtaPhiAfterIsolationAndDeadVeto->Fill(iTau->eta(),iTau->phi());
      }

      if (!fTauID->passNProngsCut(iTau)) continue;
      if (isElectron) {
        hFakeElectronEtaPhiAfterNProngs->Fill(iTau->eta(),iTau->phi());
        if (!isAtDeadCell) hFakeElectronEtaPhiAfterNProngsAndDeadVeto->Fill(iTau->eta(),iTau->phi());
      } else if (isJet) {
        hFakeJetEtaPhiAfterNProngs->Fill(iTau->eta(),iTau->phi());
        if (!isAtDeadCell) hFakeJetEtaPhiAfterNProngsAndDeadVeto->Fill(iTau->eta(),iTau->phi());
      } else if (isTau) {
        hGenuineTauEtaPhiAfterNProngs->Fill(iTau->eta(),iTau->phi());
        if (!isAtDeadCell) hGenuineTauEtaPhiAfterNProngsAndDeadVeto->Fill(iTau->eta(),iTau->phi());
      }
    }
  }


  const edm::Ptr<pat::Tau> TauSelection::selectMostLikelyTau(const edm::PtrVector<pat::Tau>& taus) {
    if(taus.empty())
      throw cms::Exception("Assert") << "TauSelection::selectMostLikelyTau(): empty vector of taus as an input" << std::endl;
    if(taus.size() == 1)
      return taus[0];

    // Exploit sorting
    std::vector<edm::Ptr<pat::Tau> > tmp;
    //std::cout << "Tau list" << std::endl;
    for(size_t i=0; i<taus.size(); ++i) {
      //std::cout << "  tau " << i << " pt " << taus[i]->pt() << " eta" << taus[i]->eta() << std::endl;
      tmp.push_back(taus[i]);
    }
    std::sort(tmp.begin(), tmp.end(), MoreLikelyTauCompare(fTauID));

    // First element in the sorted vector is the one which is most likely passing the taujet ID
    return tmp[0];

      /*
    // Decay mode finding
    std::vector<edm::Ptr<pat::Tau> > selected;
    std::vector<edm::Ptr<pat::Tau> > tmp;
    for(size_t i=0; i<taus.size(); ++i) {
      if(fTauID->passDecayModeFinding(taus[i]))
        selected.push_back(taus[i]);
    }
    if(selected.empty()) {
      // None passes decay mode, what should I do?
      // Pick the one with largest pt?
      edm::Ptr<pat::Tau> ret = taus[0];
      for(size_t i=1; i<taus.size(); ++i) {
        if(taus[i]->pt() > ret->pt())
          ret = taus[i];
      }
      return ret;
    }
    if(selected.size() == 1)
      return selected[0];

    // Still >= 2 taus, continue with kinematic selection
    
    // FIXME: order eta, pt?
    for(size_t i=0; i<selected.size(); ++i) {
      if(fTauID->passKinematicSelectionPt(selected[i]))
        tmp.push_back(selected[i]);
    }
      */
  }
}
