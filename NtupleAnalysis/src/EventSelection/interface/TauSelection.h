// -*- c++ -*-
#ifndef EventSelection_TauSelection_h
#define EventSelection_TauSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/Tau.h"
#include "Framework/interface/EventCounter.h"
#include "Framework/interface/GenericScaleFactor.h"

#include <string>
#include <vector>

class ParameterSet;
class CommonPlots;
class Event;
class EventCounter;
class HistoWrapper;
class WrappedTH1;
class WrappedTH2;

class TauSelection: public BaseSelection {
public:
    enum TauMisIDRegionType {
      kBarrel,
      kEndcap,
      kFullCoverage
    };
  
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
    const bool isGenuineTau() const { return fIsGenuineTau; }
    const size_t getFakeTauID() const { return getSelectedTau().pdgId(); } // For codes see MiniAOD2TTree/interface/NtupleAnalysis_fwd.h
    const float getTauIDSF() const { return fTauIDSF; }
    const float getTauMisIDSF() const { return fTauMisIDSF; }
    const float getTauTriggerSF() const { return fTauTriggerSF; }
    
    // Getters for anti-isolated taus (i.e. passed other cuts but not isolation)
    const bool isAntiIsolated() const { return !hasIdentifiedTaus(); }
    const bool hasAntiIsolatedTaus() const { return (fAntiIsolatedTaus.size() > 0); }
    const std::vector<Tau>& getAntiIsolatedTaus() const { return fAntiIsolatedTaus; }
    const Tau& getAntiIsolatedTau() const;
    const float getRtauOfAntiIsolatedTau() const { return fRtauAntiIsolatedTau; }
    const bool getAntiIsolatedTauIsGenuineTau() const { return fIsGenuineTauAntiIsolatedTau; }
    const size_t getAntiIsolatedFakeTauID() const { return getAntiIsolatedTau().pdgId(); } // For codes see MiniAOD2TTree/interface/NtupleAnalysis_fwd.h
    const float getAntiIsolatedTauMisIDSF() const { return fAntiIsolatedTauMisIDSF; }
    const float getAntiIsolatedTauTriggerSF() const { return fAntiIsolatedTauTriggerSF; }
    
    friend class TauSelection;

  private:
    /// Tau collection after all selections
    std::vector<Tau> fSelectedTaus;
    /// Cache Rtau value to save time
    float fRtau;
    /// Cache genuine tau status for selected tau (to avoid crashes for data)
    bool fIsGenuineTau;
    /// Cache tau identification scale factor
    float fTauIDSF;
    /// Cache tau misidentification scale factor 
    float fTauMisIDSF;
    /// Cache for tau trigger SF
    float fTauTriggerSF;
    /// Anti-isolated tau collection after pasisng all selections but not passing isolation
    std::vector<Tau> fAntiIsolatedTaus;
    /// Cache Rtau value to save time
    float fRtauAntiIsolatedTau;
    /// Cache anti-isolated tau genuine tau status for selected tau (to avoid crashes for data)
    bool fIsGenuineTauAntiIsolatedTau;
    /// Cache anti-isolated tau misidentification scale factor 
    float fAntiIsolatedTauMisIDSF;
    /// Cache for anti-isolated tau trigger SF
    float fAntiIsolatedTauTriggerSF;
  };
  
  // Main class
  /// Constructor with histogramming
  explicit TauSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix = "");
  /// Constructor without histogramming
  explicit TauSelection(const ParameterSet& config);
  virtual ~TauSelection();

  virtual void bookHistograms(TDirectory* dir);
  
  /// Use silentAnalyze if you do not want to fill histograms or increment counters
  Data silentAnalyze(const Event& event);
  /// analyze does fill histograms and incrementes counters
  Data analyze(const Event& event);

private:
  /// Initialisation called from constructor
  void initialize(const ParameterSet& config);
  /// The actual selection
  Data privateAnalyze(const Event& iEvent);
  bool passTrgMatching(const Tau& tau, std::vector<math::LorentzVectorT<double>>& trgTaus) const;
  // !!!!!!!!!!!!!!!!!!!!!!!!!! bool passDecayModeFinding(const Tau& tau) const { return tau.decayModeFinding(); }
  bool passDecayModeFinding(const Tau& tau) const { return tau.decayModeFindingNewDMs(); }
  bool passGenericDiscriminators(const Tau& tau) const { return tau.configurableDiscriminators(); }
  bool passPtCut(const Tau& tau) const { return tau.pt() > fTauPtCut; }
  bool passEtaCut(const Tau& tau) const { return std::abs(tau.eta()) < fTauEtaCut; }
  bool passLdgTrkPtCut(const Tau& tau) const { return tau.lChTrkPt() > fTauLdgTrkPtCut; }
  bool passElectronDiscriminator(const Tau& tau) const { return tau.againstElectronDiscriminator(); }
  bool passMuonDiscriminator(const Tau& tau) const { return tau.againstMuonDiscriminator(); }
  bool passNprongsCut(const Tau& tau) const;
  bool passIsolationDiscriminator(const Tau& tau) const { return tau.isolationDiscriminator(); }
  bool passRtauCut(const Tau& tau) const { return tau.rtau() > fTauRtauCut; }
  std::vector<TauMisIDRegionType> assignTauMisIDSFRegion(const ParameterSet& config, const std::string& label) const;
  std::vector<float> assignTauMisIDSFValue(const ParameterSet& config, const std::string& label) const;
  void setTauIDSFValue(Data& data);
  void setTauMisIDSFValue(Data& data);
  float setTauMisIDSFValueHelper(const Tau& tau);
  bool tauMisIDSFBelongsToRegion(TauMisIDRegionType region, double eta);
  
  // Input parameters (discriminators handled in Dataformat/src/Event.cc)
  const bool bApplyTriggerMatching;
  const float fTriggerTauMatchingCone;
  const float fTauPtCut;
  const float fTauEtaCut;
  const float fTauLdgTrkPtCut;
  const int fTauNprongs;
  const float fTauRtauCut;
  // tau identification SF
  float fTauIDSF;
  // tau misidentification SF
  std::vector<TauMisIDRegionType> fEToTauMisIDSFRegion;
  std::vector<float> fEToTauMisIDSFValue;
  std::vector<TauMisIDRegionType> fMuToTauMisIDSFRegion;
  std::vector<float> fMuToTauMisIDSFValue;
  std::vector<TauMisIDRegionType> fJetToTauMisIDSFRegion;
  std::vector<float> fJetToTauMisIDSFValue;
  // tau trigger SF
  GenericScaleFactor fTauTriggerSFReader;
  
  // Event counter for passing selection
  Count cPassedTauSelection;
  Count cPassedTauSelectionGenuine;
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
  WrappedTH2 *hNprongsMatrixForAllAfterIsolation;
  WrappedTH2 *hNprongsMatrixForBmesonsAfterIsolation;
  WrappedTH2 *hNprongsMatrixForAllAfterAntiIsolation;
  WrappedTH2 *hNprongsMatrixForBmesonsAfterAntiIsolation;
};

#endif
