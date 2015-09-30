// -*- c++ -*-
#ifndef EventSelection_TauSelection_h
#define EventSelection_TauSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/Tau.h"
#include "Framework/interface/EventCounter.h"

#include <string>
#include <vector>

extern Branch< short int > b;
class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

class TauSelection: public BaseSelection {
public:
    /**
    * Class to encapsulate the access to the data members of
    * TauSelection. If you want to add a new accessor, add it here
    * and keep all the data of TauSelection private.
    */
  class Data {
  public:
    // The reason for pointer instead of reference is that const
    // reference allows temporaries, while const pointer does not.
    // Here the object pointed-to must live longer than this object.
    Data();
    ~Data();

    // Getters for selected taus (i.e. passed isolation amongst others)
    const bool hasIdentifiedTaus() const { return (fSelectedTaus.size() > 0); }
    const Tau& getSelectedTau() const;
    const std::vector<Tau>& getSelectedTaus() const { return fSelectedTaus; }
    const float getRtauOfSelectedTau() const { return fRtau; }
    const bool isGenuineTau() const { return getSelectedTau().isGenuineTau(); }
    const size_t getFakeTauID() const { return getSelectedTau().pdgId(); } // For codes see MiniAOD2TTree/interface/NtupleAnalysis_fwd.h
    
    // Getters for anti-isolated taus (i.e. passed other cuts but not isolation)
    const bool isAntiIsolated() const { return !hasIdentifiedTaus(); }
    const bool hasAntiIsolatedTaus() const { return (fAntiIsolatedTaus.size() > 0); }
    const std::vector<Tau>& getAntiIsolatedTaus() const { return fAntiIsolatedTaus; }
    const Tau& getAntiIsolatedTau() const;
    const float getRtauOfAntiIsolatedTau() const { return fRtauAntiIsolatedTau; }
    const bool getAntiIsolatedTauIsGenuineTau() const { return getAntiIsolatedTau().isGenuineTau(); }
    const size_t getAntiIsolatedFakeTauID() const { return getAntiIsolatedTau().pdgId(); } // For codes see MiniAOD2TTree/interface/NtupleAnalysis_fwd.h
    
    friend class TauSelection;

  private:
    /// Tau collection after all selections
    std::vector<Tau> fSelectedTaus;
    /// Cache Rtau value to save time
    float fRtau;
    /// Anti-isolated tau collection after pasisng all selections but not passing isolation
    std::vector<Tau> fAntiIsolatedTaus;
    /// Cache Rtau value to save time
    float fRtauAntiIsolatedTau;
  };
  
  // Main class
  explicit TauSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  virtual ~TauSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event);

private:
  Data privateAnalyze(const Event& iEvent);
  bool passTrgMatching(const Tau& tau, std::vector<math::LorentzVectorT<double>>& trgTaus) const;
  bool passDecayModeFinding(const Tau& tau) const { return tau.decayModeFinding(); }
  bool passGenericDiscriminators(const Tau& tau) const { return tau.configurableDiscriminators(); }
  bool passPtCut(const Tau& tau) const { return tau.pt() > fTauPtCut; }
  bool passEtaCut(const Tau& tau) const { return std::abs(tau.eta()) < fTauEtaCut; }
  bool passLdgTrkPtCut(const Tau& tau) const { return tau.lChTrkPt() > fTauLdgTrkPtCut; }
  bool passElectronDiscriminator(const Tau& tau) const { return tau.againstElectronDiscriminator(); }
  bool passMuonDiscriminator(const Tau& tau) const { return tau.againstMuonDiscriminator(); }
  bool passNprongsCut(const Tau& tau) const;
  bool passIsolationDiscriminator(const Tau& tau) const { return tau.isolationDiscriminator(); }
  bool passRtauCut(const Tau& tau) const { return tau.rtau() > fTauRtauCut; }

  // Input parameters (discriminators handled in Dataformat/src/Event.cc)
  const bool bApplyTriggerMatching;
  const float fTriggerTauMatchingCone;
  const float fTauPtCut;
  const float fTauEtaCut;
  const float fTauLdgTrkPtCut;
  const int fTauNprongs;
  const float fTauRtauCut;
  
  // Event counter for passing selection
  Count cPassedTauSelection;
  Count cPassedTauSelectionMultipleTaus;
  Count cPassedAntiIsolatedTauSelection;
  Count cPassedAntiIsolatedTauSelectionMultipleTaus;
  // Sub counters
  Count cSubAll;
  Count cSubPassedTriggerMatching;
  Count cSubPassedDecayMode;
  Count cSubPassedGenericDiscriminators;
  Count cSubPassedElectronDiscr;
  Count cSubPassedMuonDiscr;
  Count cSubPassedPt;
  Count cSubPassedEta;
  Count cSubPassedLdgTrk;
  Count cSubPassedNprongs;
  Count cSubPassedIsolation;
  Count cSubPassedRtau;
  Count cSubPassedAntiIsolation;
  Count cSubPassedAntiIsolationRtau;
  // Histograms
  WrappedTH1 *hTriggerMatchDeltaR;
  WrappedTH1 *hTauPtTriggerMatched;
  WrappedTH1 *hTauEtaTriggerMatched;
  WrappedTH1 *hNPassed;
  WrappedTH1 *hPtResolution;
  WrappedTH1 *hEtaResolution;
  WrappedTH1 *hPhiResolution;
  WrappedTH1 *hIsolPtBefore;
  WrappedTH1 *hIsolEtaBefore;
  WrappedTH1 *hIsolVtxBefore;
  WrappedTH1 *hIsolPtAfter;
  WrappedTH1 *hIsolEtaAfter;
  WrappedTH1 *hIsolVtxAfter;
};

#endif
