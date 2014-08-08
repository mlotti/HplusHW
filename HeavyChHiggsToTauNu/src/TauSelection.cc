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
#include "DataFormats/TauReco/interface/PFTauDecayMode.h"

#include "DataFormats/Math/interface/LorentzVector.h"
typedef math::XYZTLorentzVector LorentzVector;

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
    
    if(a->tauID("byTightCombinedIsolationDeltaBetaCorr3Hits") > 0.5 && b->tauID("byTightCombinedIsolationDeltaBetaCorr3Hits") < 0.5)
      return true;

    if(a->tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits") > 0.5) {
      if(b->tauID("byTightCombinedIsolationDeltaBetaCorr3Hits") > 0.5)
        return false;
      if(b->tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits") < 0.5)
        return true;
    }

    if(a->tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits") > 0.5) {
      // assume that if tau is medium isolated, it is also tight isolated
      if(b->tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits") > 0.5)
        return false;
      if(b->tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits") < 0.5)
        return true;
    }

    // VLoose isolation does not exist anymore
//     if(a->tauID("byVLooseCombinedIsolationDeltaBetaCorr3Hits") > 0.5) {
//       if(b->tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits") > 0.5)
//         return false;
//       if(b->tauID("byVLooseCombinedIsolationDeltaBetaCorr3Hits") < 0.5)
//         return true;
//     }

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
    MoreLikelyTauCompare(HPlus::TauIDBase *tauID, double vertexZ): fTauID(tauID), fVertexZ(vertexZ) {}

    bool operator()(const edm::Ptr<pat::Tau>& tauA, const edm::Ptr<pat::Tau>& tauB) {
      bool result = firstIsMoreLikely(tauA, tauB);
      //std::cout << "Is left-one more likely? " << result << std::endl;
      return result;
    }

    bool firstIsMoreIsolatedLargerPt(const edm::Ptr<pat::Tau>& tauA, const edm::Ptr<pat::Tau>& tauB) {
      bool resA = fTauID->passIsolation(tauA);
      bool resB = fTauID->passIsolation(tauB);
      /*
      std::cout << "  Isolation " << resA << " (" << tauA->tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")
                << ") " << resB << " (" << tauB->tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")
                << ")" << std::endl;
      */
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        // Both fail isolation, comparison by isolation is ok
        return tauA->tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits") < tauB->tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits");

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

      // VertexZ cut
      resA = fTauID->passVertexZCut(tauA,fVertexZ);
      resB = fTauID->passVertexZCut(tauB,fVertexZ);
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        return firstIsMoreIsolatedLargerPt(tauA, tauB);

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
      std::cout << "Isolation " << resA << " (" << tauA->tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")
                << ") " << resB << " (" << tauB->tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")
                << ")" << std::endl;
      */
      if(resA != resB)
        return resA;
      if(!resA && !resB)
        return tauA->tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits") < tauB->tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits");

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
    double fVertexZ;
  };
}

namespace HPlus {
  // TauSelection::Data methods ------------------------------------------------
  TauSelection::Data::Data():
    fPassedEvent(false),
    bSelectedTauPassesIsolation(false),
    bSelectedTauPassesNProngs(false),
    bSelectedTauPassesRtau(false),
    bSelectedTausDoNotPassIsolation(false),
    fSelectedTauNProngsValue(-1),
    fSelectedTauRtauValue(-1) {}
  TauSelection::Data::~Data() {}

  const edm::Ptr<pat::Tau> TauSelection::Data::getSelectedTau() const {
    //if (!fPassedEvent)
    //  throw cms::Exception("Assert") << "TauSelection::Data::getSelectedTau() was called even though TauSelection::Data::passedEvent() is false. Please add to your code requirement that passedEvent is true before asking for getSelectedTau!" << __FILE__ << ":" << __LINE__;
    //if (fSelectedTau.isNull())
      //edm::Ptr<pat::Tau> myZeroPointer;
      //return myZeroPointer;
      //throw cms::Exception("Assert") << "TauSelection::Data::getSelectedTau() is a zero pointer! Check your code! (for QCD factorised measurement, you should never call this method)" << __FILE__ << ":" << __LINE__;
    return fSelectedTau;
  }

  // TauSelection methods ------------------------------------------------
  TauSelection::TauSelection(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper, std::string label):
    BaseSelection(eventCounter, histoWrapper),
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fAnalyseFakeTauComposition(iConfig.getUntrackedParameter<bool>("analyseFakeTauComposition")),
    fDecayModeFilterValue(iConfig.getUntrackedParameter<int>("decayModeFilterValue")),
    fTauDecayModeReweightFactorForZero(iConfig.getUntrackedParameter<double>("tauDecayModeReweightingZero")),
    fTauDecayModeReweightFactorForOne(iConfig.getUntrackedParameter<double>("tauDecayModeReweightingOne")),
    fTauDecayModeReweightFactorForOther(iConfig.getUntrackedParameter<double>("tauDecayModeReweightingOther")),
    fTauID(0),
    fOperationMode(kNormalTauID)
  {
    const std::string mySelection = iConfig.getUntrackedParameter<std::string>("selection");
    edm::Service<TFileService> fs;
    TFileDirectory myDir = histoWrapper.mkdir(HistoWrapper::kInformative, *fs, label);
    
    // Create tauID algorithm handler
    //if(mySelection == "PFTauTaNCBased")
    //  fTauID = new TauIDPFTaNC(iConfig, eventCounter, histoWrapper, "TaNC", myDir);
    if(mySelection == "HPSTauBased")
      fTauID = new TauIDPFHPS(iConfig, eventCounter, histoWrapper, label+"_HPS", myDir);
    //else if(mySelection == "CombinedHPSTaNCTauBased")
    //  fTauID = new TauIDPFCombinedHPSTaNC(iConfig, eventCounter, histoWrapper, "HPS+TaNC", myDir);
    else throw cms::Exception("Configuration") << "TauSelection: no or unknown tau selection used! Options for 'selection' are: HPSTauBased (you chose '" << mySelection << "')" << std::endl;
    
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
    // Decay mode finding
    hDecayModeTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_all_tau_candidates_DecayModeFinding", "DecayModeFinding;DecayMode;N_{jets}", 30, 0, 30);
    hDecayModeSelectedTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "cleaned_all_tau_candidates_DecayModeFinding", "DecayModeFinding;DecayMode;N_{jets}", 30, 0, 30);
    hDecayModeSelectedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "selected_tau_DecayModeFinding", "DecayModeFinding;DecayMode;N_{jets}", 30, 0, 30);
    // Pt
    hPtTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_all_tau_candidates_pt",
      "tau_candidates_pt;#tau p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myTauJetPtBins, myTauJetPtMin, myTauJetPtMax);
    hPtSelectedTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_cleaned_tau_candidates_pt",
      "cleaned_tau_candidates_pt;#tau p_{T}, GeV/c;N_{jets} / 5 GeV/c",
      myTauJetPtBins, myTauJetPtMin, myTauJetPtMax);
    hPtSelectedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
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
    hEtaSelectedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
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
    hNumberOfSelectedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_selected_taus_N",
      "selected_tau_N;Number of #tau's;N_{jets}",
      myTauJetNumberBins, myTauJetNumberMin, myTauJetNumberMax);
    // MC purity
    hMCPurityOfTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_all_tau_candidates_MC_purity",
      "tau_candidates_MC_purity;;N_{jets}", 5, 0., 5.);
    if (hMCPurityOfTauCandidates->isActive()) {
      hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(1, "#tau from H#pm");
      hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(2, "#tau from W#pm");
      hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(3, "#tau from Z");
      hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(4, "Other #tau source");
      hMCPurityOfTauCandidates->GetXaxis()->SetBinLabel(5, "No MC #tau match");
    }
    hMCPurityOfSelectedTauCandidates = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_cleaned_tau_candidates_MC_purity",
      "cleaned_tau_candidates_MC_purity;;N_{jets}", 5, 0., 5.);
    if (hMCPurityOfSelectedTauCandidates->isActive()) {
      hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(1, "#tau from H#pm");
      hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(2, "#tau from W#pm");
      hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(3, "#tau from Z");
      hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(4, "Other #tau source");
      hMCPurityOfSelectedTauCandidates->GetXaxis()->SetBinLabel(5, "No MC #tau match");
    }
    hMCPurityOfSelectedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir,
      "TauSelection_selected_taus_MC_purity",
      "selected_tau_MC_purity;;N_{jets}", 5, 0., 5.);
    if (hMCPurityOfSelectedTaus->isActive()) {
      hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(1, "#tau from H#pm");
      hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(2, "#tau from W#pm");
      hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(3, "#tau from Z");
      hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(4, "Other #tau source");
      hMCPurityOfSelectedTaus->GetXaxis()->SetBinLabel(5, "No MC #tau match");
    }

    // Isolation variables
    //hVLooseIsoNcands = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TauSelection_all_tau_candidates_VLooseIsoNCands", "Number of isolation candidates in VLoose", 100, 0, 100);
    hLooseIsoNcands = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TauSelection_all_tau_candidates_LooseIsoNCands", "Number of isolation candidates in Loose", 100, 0, 100);
    hMediumIsoNcands = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TauSelection_all_tau_candidates_MediumIsoNCands", "Number of isolation candidates in Medium", 100, 0, 100);
    hTightIsoNcands = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TauSelection_all_tau_candidates_TightIsoNCands", "Number of isolation candidates in Tight", 100, 0, 100);

    // Operating mode of tau ID -- for quick validating that tau selection is doing what is expected 
    hTauIdOperatingMode = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "tauSelection_operating_mode", "tau_operating_mode;;N_{events}", 3, 0., 3.);
    if (hTauIdOperatingMode->isActive()) {
      hTauIdOperatingMode->GetXaxis()->SetBinLabel(1, "Control");
      hTauIdOperatingMode->GetXaxis()->SetBinLabel(2, "Normal tau ID");
      hTauIdOperatingMode->GetXaxis()->SetBinLabel(3, "tauCandidateSelectionOnly");
    }
    // Sorting category in tau candidate selection
    hTauIdCandidateSelectionSortCategory = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "CandidateSelectionSortCategory", "CandidateSelectionSortCategory;;N_{events}", 10, 0., 10.);
    if (hTauIdCandidateSelectionSortCategory->isActive()) {
      hTauIdCandidateSelectionSortCategory->GetXaxis()->SetBinLabel(1, "Beginning");
      hTauIdCandidateSelectionSortCategory->GetXaxis()->SetBinLabel(2, "None pass isol.");
      hTauIdCandidateSelectionSortCategory->GetXaxis()->SetBinLabel(3, "1 pass isol.");
      hTauIdCandidateSelectionSortCategory->GetXaxis()->SetBinLabel(4, "multi-pass isol.");
      hTauIdCandidateSelectionSortCategory->GetXaxis()->SetBinLabel(5, "None pass Npr");
      hTauIdCandidateSelectionSortCategory->GetXaxis()->SetBinLabel(6, "1 pass Npr");
      hTauIdCandidateSelectionSortCategory->GetXaxis()->SetBinLabel(7, "multi-pass Npr");
      hTauIdCandidateSelectionSortCategory->GetXaxis()->SetBinLabel(8, "None pass Rtau");
      hTauIdCandidateSelectionSortCategory->GetXaxis()->SetBinLabel(9, "1 pass Rtau");
      hTauIdCandidateSelectionSortCategory->GetXaxis()->SetBinLabel(10, "multi-pass Rtau");
    }

    hNTriggerMatchedTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "N_TriggerMatchedTaus", "NTriggerMatchedTaus;N(trigger matched taus);N_{events}", 10, 0., 10.);
    hNTriggerMatchedSeparateTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "N_TriggerMatchedSeparateTaus", "NTriggerMatchedSeparateTaus;N(trigger matched separate taus);N_{events}", 10, 0., 10.);

    hIsolationPFChargedHadrCandsPtSum = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "IsolationPFChargedHadrCandsPtSum", "IsolationPFChargedHadrCandsPtSum;IsolationPFChargedHadrCandsPtSum;N_{tau candidates}", 200, 0., 100.);
    hIsolationPFGammaCandsEtSum = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "IsolationPFGammaCandEtSum", "IsolationPFGammaCandEtSum;IsolationPFGammaCandEtSum;N_{tau candidates}", 200, 0., 100.);

    hTightChargedMaxPtBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightChargedMaxPtBeforeIsolation", "TightChargedMaxPtBeforeIsolation;TightChargedMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedSumPtBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightChargedSumPtBeforeIsolation", "TightChargedSumPtBeforeIsolation;TightChargedSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedOccupancyBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightChargedOccupancyBeforeIsolation", "TightChargedOccupancyBeforeIsolation;TightChargedOccupancy;N_{tau candidates}", 100, 0., 100.);
    hTightGammaMaxPtBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightGammaMaxPtBeforeIsolation", "TightGammaMaxPtBeforeIsolation;TightGammaMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaSumPtBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightGammaSumPtBeforeIsolation", "TightGammaSumPtBeforeIsolation;TightGammaSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaOccupancyBeforeIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightGammaOccupancyBeforeIsolation", "TightGammaOccupancyBeforeIsolation;TightGammaOccupancy;N_{tau candidates}", 100, 0., 100.); 

    hTightChargedMaxPtAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightChargedMaxPtAfterIsolation", "TightChargedMaxPtAfterIsolation;TightChargedMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedSumPtAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightChargedSumPtAfterIsolation", "TightChargedSumPtAfterIsolation;TightChargedSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightChargedOccupancyAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightChargedOccupancyAfterIsolation", "TightChargedOccupancyAfterIsolation;TightChargedOccupancy;N_{tau candidates}", 100, 0., 100.);
    hTightGammaMaxPtAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightGammaMaxPtAfterIsolation", "TightGammaMaxPtAfterIsolation;TightGammaMaxPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaSumPtAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightGammaSumPtAfterIsolation", "TightGammaSumPtAfterIsolation;TightGammaSumPt;N_{tau candidates}", 200, 0., 100.);
    hTightGammaOccupancyAfterIsolation = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TightGammaOccupancyAfterIsolation", "TightGammaOccupancyAfterIsolation;TightGammaOccupancy;N_{tau candidates}", 100, 0., 100.); 

    if (fAnalyseFakeTauComposition) {
      std::string myFakeLabel = label+"_fakeAnalysis";
      TFileDirectory myFakeDir = histoWrapper.mkdir(HistoWrapper::kInformative, *fs, myFakeLabel);
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

  TauSelection::Data TauSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, double vertexZ) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, vertexZ);
  }

  TauSelection::Data TauSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, double vertexZ) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, vertexZ);
  }

  TauSelection::Data TauSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, double vertexZ) {
    Data output;
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
      doTauSelection(iEvent, iSetup, myFilteredTaus, vertexZ, output);
      return output;
    }

    // Do selection
    doTauSelection(iEvent, iSetup, htaus->ptrVector(), vertexZ, output);
    return output;
  }

  TauSelection::Data TauSelection::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus, double vertexZ) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, taus, vertexZ);
  }

  TauSelection::Data TauSelection::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus, double vertexZ) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, taus, vertexZ);
  }

  TauSelection::Data TauSelection::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus, double vertexZ) {
    Data output;
    // Do selection
    doTauSelection(iEvent,iSetup,taus, vertexZ, output);
    return output;
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

  void TauSelection::doTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus, double vertexZ, TauSelection::Data& output) {
    doTauCandidateSelection(iEvent, iSetup, taus, vertexZ, output);
    doTauIdentification(iEvent, iSetup, output);
    finalizeSelection(output);
  }

  void TauSelection::doTauCandidateSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus, double vertexZ, TauSelection::Data& output){
    // Document operation mode
    fillOperationModeHistogram();

    // Initialize (needed for counters)
    fTauID->reset();

    // Analyze the separation of the trigger matched taus
    analyzeSeparationOfTriggerMatchedTaus(taus);

    // Need std:vector in order to be able to use std::sort
    std::vector<edm::Ptr<pat::Tau> > tmpSelectedTauCandidates;

    // Loop over the taus (default = all trigger matched taus)
    // Taus that pass these cuts are called selected tau candidates
    for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
      const edm::Ptr<pat::Tau> iTau = *iter;
      // Tau candidate selections
      fTauID->incrementAllCandidates();
      if (!fTauID->passDecayModeFinding(iTau)) continue;
      fillHistogramsForTauCandidates(iTau, iEvent); // Makes sense to look at pT and eta only after decay mode finding
      output.fAllTauCandidates.push_back(iTau);
      if (!fTauID->passVertexZCut(iTau, vertexZ)) continue;
      if (!fTauID->passKinematicSelection(iTau)) continue;
      if (!fTauID->passLeadingTrackCuts(iTau)) continue;
      if (!fTauID->passECALFiducialCuts(iTau)) continue;
      if (!fTauID->passTauCandidateEAndMuVetoCuts(iTau)) continue;
      if (!fTauID->passVetoAgainstDeadECALCells(iTau)) continue;
      fillHistogramsForSelectedTauCandidates(iTau, iEvent);
      tmpSelectedTauCandidates.push_back(iTau);
    }
    float mySortCategory = 0.; // For tracking errors and exceptions
    if (true) { // if sentence to limit histogram disabling to sorting only
      // Sort list of selected tau candidates such that most probable tau object is the first
      // Sort taus in an order of tau ET
      std::sort(tmpSelectedTauCandidates.begin(), tmpSelectedTauCandidates.end(), tauEtGreaterThan); // sort by Et

      // For the duration of sorting, Disable histogram filling and counter incrementing until the return call
      // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
      HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
      EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

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
        mySortCategory = 1.;
        std::sort(tmpSelectedTauCandidates.begin(), tmpSelectedTauCandidates.end(), isolationLessThan);
        for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
          output.fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
        }
      } else if (tmpIsolationPassed.size() == 1) {
        // Put the found one to the top of the list
        mySortCategory = 2.;
        output.fSelectedTauCandidates.push_back(tmpIsolationPassed[0]);
//         for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
//           if (!fTauID->passIsolation(tmpSelectedTauCandidates[i]))
//             output.fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
//         }
      } else {
        // 2) Multiple taus have passed isolation, lets see how many pass also the nprongs cut
        mySortCategory = 3.;
        std::sort(tmpIsolationPassed.begin(), tmpIsolationPassed.end(), isolationLessThan);
        for(size_t i=0; i<tmpIsolationPassed.size(); ++i) {
          if (fTauID->passNProngsCut(tmpIsolationPassed[i]))
            tmpNprongPassed.push_back(tmpIsolationPassed[i]);
        }
        if (tmpNprongPassed.size() == 0) {
          // none pass, take the most isolated one
          mySortCategory = 4.;
          for(size_t i=0; i<tmpIsolationPassed.size(); ++i) {
            output.fSelectedTauCandidates.push_back(tmpIsolationPassed[i]);
          }
//           for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
//             bool match = false;
//             for(size_t j=0; j<tmpIsolationPassed.size(); ++j) {
//               if (tmpSelectedTauCandidates[i] == tmpIsolationPassed[j])
//                 match = true;
//             }
//             if (!match) output.fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
//           }
        } else if (tmpNprongPassed.size() == 1) {
          // Put the passed one to the top of the list
          mySortCategory = 5.;
          output.fSelectedTauCandidates.push_back(tmpNprongPassed[0]);
//           for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
//             if (tmpSelectedTauCandidates[i] != tmpNprongPassed[0])
//               output.fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
//           }
        } else {
          // 3) Multiple taus have passed nprongs, lets see how many pass also the rtau cut
          mySortCategory = 6.;
          for(size_t i=0; i<tmpNprongPassed.size(); ++i) {
            if (fTauID->passRTauCut(tmpNprongPassed[i]))
              tmpRtauPassed.push_back(tmpNprongPassed[i]);
          }
          if (tmpRtauPassed.size() == 0) {
            // none pass, just take the most isolated one
            mySortCategory = 7.;
            std::sort(tmpNprongPassed.begin(), tmpNprongPassed.end(), isolationLessThan);
            for(size_t i=0; i<tmpNprongPassed.size(); ++i) {
              output.fSelectedTauCandidates.push_back(tmpNprongPassed[i]);
            }
//             for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
//               bool match = false;
//               for(size_t j=0; j<tmpNprongPassed.size(); ++j) {
//                 if (tmpSelectedTauCandidates[i] == tmpNprongPassed[j])
//                   match = true;
//               }
//               if (!match) output.fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
//            }
          } else if (tmpRtauPassed.size() == 1) {
            mySortCategory = 8.;
            // Put the one that passed both nprongs and rtau to the top of the list
            output.fSelectedTauCandidates.push_back(tmpRtauPassed[0]);
//             for(size_t i=0; i<tmpSelectedTauCandidates.size(); ++i) {
//               if (tmpSelectedTauCandidates[i] != tmpRtauPassed[0])
//                 output.fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
//             }
          } else {
            // 4) Multiple taus have passed nprongs, rtau, and isolation; take most energetic one
            mySortCategory = 9.;
            std::sort(tmpRtauPassed.begin(), tmpRtauPassed.end(), tauEtGreaterThan);
            for(size_t i=0; i<tmpRtauPassed.size(); ++i) {
              output.fSelectedTauCandidates.push_back(tmpRtauPassed[i]);
            }
          }
        }
      }
    }
    // Now at least one tau should be at the top of the selected tau candidates list; fill the rest
    size_t mySelectedSize = output.fSelectedTauCandidates.size();
    if (!mySelectedSize && tmpSelectedTauCandidates.size() > 0) {
      throw cms::Exception("LogicError") << "TauSelection::doTauCandidateSelection(): sorting did not select any tau candidate (sort category=" << mySortCategory << ")!";
    }
    for (size_t i = 0; i < tmpSelectedTauCandidates.size(); ++i) {
      bool myVetoStatus = false;
      for (size_t j = 0; j < mySelectedSize; ++j) {
        if (tmpSelectedTauCandidates[i] == output.fSelectedTauCandidates[j])
          myVetoStatus = true;
      }
      if (!myVetoStatus)
        output.fSelectedTauCandidates.push_back(tmpSelectedTauCandidates[i]);
    }

    hTauIdCandidateSelectionSortCategory->Fill(mySortCategory);
    // Check that sorting was ok
    if (output.fSelectedTauCandidates.size() != tmpSelectedTauCandidates.size()) {
      throw cms::Exception("LogicError") << "TauSelection::doTauCandidateSelection(): sorting of selected tau candidates lost tau objects (sort category=" << mySortCategory << ")!";
    }
    // Set first tau as selected tau for tauCandidateSelection only
    if (fOperationMode == kTauCandidateSelectionOnly) {
      if (output.fSelectedTauCandidates.size()) {
        output.fPassedEvent= true;
        output.fSelectedTau = output.fSelectedTauCandidates[0];
      } else {
        output.fPassedEvent= false;
      }
    }
    // End of tau candidate selection
  }

  void TauSelection::doTauIdentification(const edm::Event& iEvent, const edm::EventSetup& iSetup, TauSelection::Data& output) {
    if (!output.fSelectedTauCandidates.size() || fOperationMode == kTauCandidateSelectionOnly) return;

    // Need std::vector in order to be able to use std::sort
    std::vector<edm::Ptr<pat::Tau> > tmpSelectedTaus;

    // Loop over tau candidates
    for(edm::PtrVector<pat::Tau>::const_iterator iter = output.fSelectedTauCandidates.begin(); iter != output.fSelectedTauCandidates.end(); ++iter) {
      const edm::Ptr<pat::Tau> iTau = *iter;
      // Apply isolation and fill information histograms
      hIsolationPFChargedHadrCandsPtSum->Fill(iTau->isolationPFChargedHadrCandsPtSum());
      hIsolationPFGammaCandsEtSum->Fill(iTau->isolationPFGammaCandsEtSum());
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
      // Apply Nprongs cut
      if (!fTauID->passNProngsCut(iTau)) continue;
      // Apply Rtau cut
      if (!fTauID->passRTauCut(iTau)) continue;

      // All cuts have been passed, save tau
      fillHistogramsForSelectedTaus(iTau, iEvent);
      tmpSelectedTaus.push_back(iTau);
    }

    // Sort list by tau pT if multiple taus were found
    std::sort(tmpSelectedTaus.begin(), tmpSelectedTaus.end(), tauEtGreaterThan);
    for(size_t i=0; i<tmpSelectedTaus.size(); ++i)
      output.fSelectedTaus.push_back(tmpSelectedTaus[i]);

    // Check that sorting was ok
    if (output.fSelectedTaus.size() != tmpSelectedTaus.size()) {
      throw cms::Exception("LogicError") << "TauSelection::doTauIdentification(): sorting of selected taus is buggy!";
    }

    // Set first tau as selected tau for tauCandidateSelection only
    if (output.fSelectedTaus.size()) {
      output.fPassedEvent = true;
      output.fSelectedTau = output.fSelectedTaus[0];
    } else {
      output.fPassedEvent = false;
    }
  }

  void TauSelection::finalizeSelection(TauSelection::Data& output) {
    // Handle counters
    fTauID->updatePassedCounters();
    // Fill number of taus histograms (per event)
    hNumberOfTauCandidates->Fill(static_cast<float>(output.fAllTauCandidates.size()));
    hNumberOfSelectedTauCandidates->Fill(static_cast<float>(output.fSelectedTauCandidates.size()));
    if (fOperationMode != kTauCandidateSelectionOnly) {
      hNumberOfSelectedTaus->Fill(static_cast<float>(output.fSelectedTaus.size()));
    }
    if (output.passedEvent()) {
      // Set booleans in Data object, Disable histogram filling and counter incrementing until the return call
      // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
      HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
      EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
      // Isolation status
      output.bSelectedTauPassesIsolation = fTauID->passIsolation(output.fSelectedTau);
      // Nprongs status
      output.bSelectedTauPassesNProngs = fTauID->passNProngsCut(output.fSelectedTau);
      // Rtau status
      output.bSelectedTauPassesRtau = fTauID->passRTauCut(output.fSelectedTau);
      // Selected taus do not pass isolation
      bool myHasPassedIsolationStatus = false;
      for(edm::PtrVector<pat::Tau>::const_iterator iter = output.fSelectedTauCandidates.begin(); iter != output.fSelectedTauCandidates.end(); ++iter) {
        myHasPassedIsolationStatus = myHasPassedIsolationStatus && fTauID->passIsolation(*iter);
      }
      output.bSelectedTausDoNotPassIsolation = !myHasPassedIsolationStatus;
      // Nprongs value
      output.fSelectedTauNProngsValue = fTauID->getNProngs(output.fSelectedTau);
      // Rtau value
      output.fSelectedTauRtauValue = fTauID->getRtauValue(output.fSelectedTau);
    }
    output.fTauDecayModeReweightingFactor = getTauDecayModeReweightingFactor(output.fSelectedTau);
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
    hDecayModeTauCandidates->Fill(tau->decayMode());
    hPtTauCandidates->Fill(myTauPt);
    hEtaTauCandidates->Fill(myTauEta);
    hPhiTauCandidates->Fill(myTauPhi);
    hEtaPhiTauCandidates->Fill(myTauEta, myTauPhi);
    // Purity
    if (!iEvent.isRealData()) {
      ObtainMCPurity(tau, iEvent, hMCPurityOfTauCandidates);
    }

    //hVLooseIsoNcands->Fill(tau->userInt("byVLooseOccupancy"));
    hLooseIsoNcands->Fill(tau->userInt("byLooseOccupancy"));
    hMediumIsoNcands->Fill(tau->userInt("byMediumOccupancy"));
    hTightIsoNcands->Fill(tau->userInt("byTightOccupancy"));
  }
  
  void TauSelection::fillHistogramsForSelectedTauCandidates(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent) {
    double myTauPt = tau->pt();
    double myTauEta = tau->eta();
    double myTauPhi = tau->phi();
    hDecayModeSelectedTauCandidates->Fill(tau->decayMode());
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
    hDecayModeSelectedTaus->Fill(tau->decayMode());
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
    Data output;
    output.fPassedEvent = passEvent;
    //fSelectedTaus.clear();
    //fSelectedTaus.reserve(1);
    if (tau.isNonnull()) {
      output.fSelectedTaus.push_back(tau);
      output.fSelectedTau = tau;
      finalizeSelection(output);
    }
    return output;
  }

  void TauSelection::ObtainMCPurity(const edm::Ptr<pat::Tau> tau, const edm::Event& iEvent, WrappedTH1* histogram) {
    if (iEvent.isRealData()) return;
    // FIXME: This is essentially duplicate code w.r.t. FakeTauIdentifier
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (std::abs(p.pdgId()) == 15) {
        // Ignore tau that is radiating before decay
        bool myVetoStatus = false;
        for (size_t im=0; im < p.numberOfDaughters(); ++im){
          if (std::abs(p.daughter(im)->pdgId()) == 15) myVetoStatus = true;
        }
        if (myVetoStatus) continue;
        // Tau lepton found, let's find the stable daughters and sum up their four momentum
        LorentzVector myVisibleTau;
        // Subtract neutrino momenta from tau lepton momentum
        for (size_t j=0; j < genParticles->size(); ++j) {
          // Consider only stable particles
          if ((*genParticles)[j].status() != 1) continue;
          // Skip neutrinos
          int myId = std::abs((*genParticles)[j].pdgId());
          if (myId == 12 || myId == 14 || myId == 16) continue;
          // Check if particles mother is the tau lepton on row i
          const reco::Candidate* ppmother = (*genParticles)[j].mother();
          bool myBelongsToTauStatus = false;
          while (ppmother) {
            if (ppmother->p4() == p.p4() && ppmother->pdgId() == p.pdgId()) {
              myBelongsToTauStatus = true;
            }
            // move to next
            ppmother = ppmother->mother();
          }
          if (myBelongsToTauStatus) {
            //std::cout << "   add " << (*genParticles)[j].pdgId() << " status=" << (*genParticles)[j].status() << std::endl;
            myVisibleTau += (*genParticles)[j].p4();
          }
        }
        // Check match with tau
        if (reco::deltaR(myVisibleTau, tau->p4()) < 0.1) {
          // Check mother of tau
          const reco::Candidate* pmother = p.mother();
          while (pmother) {
            int idmother = std::abs(pmother->pdgId());
            //std::cout << "mother="<< idmother<< std::endl;
            if (idmother == 37) { // H+
              histogram->Fill(0.);
              return;
            } else if (idmother == 24) { // W+
              histogram->Fill(1.);
              return;
            } else if (idmother == 23) { // Z
              histogram->Fill(2.);
              return;
            }
            pmother = pmother->mother();
          }
          histogram->Fill(3.); // Other source of tau (B decays)
          return;
        }
      }
    }
    histogram->Fill(4.); // No MC match found
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

  void TauSelection::analyzeSeparationOfTriggerMatchedTaus(const edm::PtrVector<pat::Tau>& taus) {
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
  }


  void TauSelection::analyseFakeTauComposition(FakeTauIdentifier& fakeTauIdentifier, const edm::Event& iEvent) {
    if (!fAnalyseFakeTauComposition) return;
    // Disable histogram filling and counter incrementing temporarily (until end of this method)
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    // Get taus
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel(fSrc, htaus);
    for(edm::PtrVector<pat::Tau>::const_iterator iter = htaus->ptrVector().begin(); iter != htaus->ptrVector().end(); ++iter) {
      const edm::Ptr<pat::Tau> iTau = *iter;
      FakeTauIdentifier::Data tauMatchData = fakeTauIdentifier.matchTauToMC(iEvent, *iTau);
      bool isElectron = tauMatchData.isElectronToTau();
      bool isJet = tauMatchData.isJetToTau();
      bool isTau = tauMatchData.isGenuineTau();
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


  const edm::Ptr<pat::Tau> TauSelection::selectMostLikelyTau(const edm::PtrVector<pat::Tau>& taus, double vertexZ) {
    if(taus.empty())
      throw cms::Exception("Assert") << "TauSelection::selectMostLikelyTau(): empty vector of taus as an input" << std::endl;
    if(taus.size() == 1)
      return taus[0];

    // Disable histogram filling and counter incrementing temporarily (until end of this method)
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    // Exploit sorting
    std::vector<edm::Ptr<pat::Tau> > tmp;
    //std::cout << "Tau list" << std::endl;
    for(size_t i=0; i<taus.size(); ++i) {
      //std::cout << "  tau " << i << " pt " << taus[i]->pt() << " eta" << taus[i]->eta() << std::endl;
      tmp.push_back(taus[i]);
    }

    std::sort(tmp.begin(), tmp.end(), MoreLikelyTauCompare(fTauID, vertexZ));

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

  // Returns true if tau passes Decay Mode filter
  const bool TauSelection::passesDecayModeFilter(const edm::Ptr<pat::Tau>& tau) const {
    // Return true if filter is disabled
    if (fDecayModeFilterValue < 0) return true;
    return tau->decayMode() == fDecayModeFilterValue;
  }

  // Horror getters - these should never be used in analysis for other purposes than testing / debugging !!!
  // If you use these for analysis, you forget about the sorting in the case of multiple taus -> physics results will not be accurate
  const bool TauSelection::getPassesIsolationStatusOfTauObject(const edm::Ptr<pat::Tau>& tau, std::string isolationString) const {
    // Disable histogram filling and counter incrementing until the return call
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    if (isolationString.size())
      return tau->tauID(isolationString) > 0.5;
    return fTauID->passIsolation(tau) > 0.5;
  }

  const double TauSelection::getIsolationValueOfTauObject(const edm::Ptr<pat::Tau>& tau, std::string isolationString) const {
    // Disable histogram filling and counter incrementing until the return call
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    if (isolationString.size())
      return tau->tauID(isolationString);
    return fTauID->passIsolation(tau);
  }

  const bool TauSelection::getPassesNProngsStatusOfTauObject(const edm::Ptr<pat::Tau>& tau) const {
    // Disable histogram filling and counter incrementing until the return call
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    return fTauID->passNProngsCut(tau);
  }

  const bool TauSelection::getPassesRtauStatusOfTauObject(const edm::Ptr<pat::Tau>& tau) const {
    // Disable histogram filling and counter incrementing until the return call
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    return fTauID->passRTauCut(tau);
  }

  const int TauSelection::getNProngsOfTauObject(const edm::Ptr<pat::Tau>& tau) const {
    // Disable histogram filling and counter incrementing until the return call
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    return fTauID->getNProngs(tau);
  }

  const double TauSelection::getRtauOfTauObject(const edm::Ptr<pat::Tau>& tau) const {
    // Disable histogram filling and counter incrementing until the return call
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    return fTauID->getRtauValue(tau);
  }

  double TauSelection::getTauDecayModeReweightingFactor(const edm::Ptr<pat::Tau> tau) {
    if (tau.isNull())
      return 1.0;
    if (tau->decayMode() == reco::PFTauDecayMode::tauDecay1ChargedPion0PiZero)
      return fTauDecayModeReweightFactorForZero;
    if (tau->decayMode() == reco::PFTauDecayMode::tauDecay1ChargedPion1PiZero)
      return fTauDecayModeReweightFactorForOne;
    return fTauDecayModeReweightFactorForOther;
  }
  
}
