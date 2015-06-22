// -*- c++ -*-
#ifndef EventSelection_TauSelection_h
#define EventSelection_TauSelection_h

#include "EventSelection/interface/BaseSelection.h"
#include "DataFormat/interface/Tau.h"
#include "Framework/interface/EventCounter.h"

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

    const bool hasIdentifiedTaus() const { return (fSelectedTaus.size() > 0); }
    const Tau& getSelectedTau() const;
    const std::vector<Tau>& getSelectedTaus() const { return fSelectedTaus; }
    const float getRtauOfSelectedTau() const { return fRtau; }
    
    // FIXME: Add MC information if deemed necessary
//     const bool eventContainsTauFromCJet() const { return fHasTauFromCjetStatus; }
//     const bool eventContainsTauFromBJet() const { return fHasTauFromBjetStatus; }
//     const bool eventContainsTauFromCorBJet() const { return eventContainsTauFromCJet() || eventContainsTauFromBJet(); }
    friend class TauSelection;

  private:
    float fRtau;
    // FIXME: add mechanism for finding out if the tau is genuine or not
    /// Tau collection after all selections
    std::vector<Tau> fSelectedTaus;
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
  bool passPtCut(const Tau& tau) const { return tau.pt() > fTauPtCut; }
  bool passEtaCut(const Tau& tau) const { return std::fabs(tau.eta()) < fTauEtaCut; }
  bool passLdgTrkPtCut(const Tau& tau) const { return tau.lTrkPt() > fTauLdgTrkPtCut; }
  bool passElectronDiscriminator(const Tau& tau) const { return tau.againstElectronDiscriminator(); }
  bool passMuonDiscriminator(const Tau& tau) const { return tau.againstMuonDiscriminator(); }
  bool passNprongsCut(const Tau& tau) const;
  bool passIsolationDiscriminator(const Tau& tau) const { return tau.isolationDiscriminator(); }
  bool passRtauCut(const Tau& tau) const { return this->getRtau(tau) > fTauRtauCut; }
  double getRtau(const Tau& tau) const;

  // Input parameters (discriminators handled in Dataformat/src/Event.cc)
  const bool bApplyTriggerMatching;
  const float fTriggerTauMatchingCone;
  const float fTauPtCut;
  const float fTauEtaCut;
  const float fTauLdgTrkPtCut;
  const int fTauNprongs;
  const float fTauRtauCut;
  const bool bInvertTauIsolation;
  
  // Event counter for passing selection
  Count cPassedTauSelection;
  Count cPassedTauSelectionMultipleTaus;
  // Sub counters
  Count cSubAll;
  Count cSubPassedTriggerMatching;
  Count cSubPassedDecayMode;
  Count cSubPassedElectronDiscr;
  Count cSubPassedMuonDiscr;
  Count cSubPassedPt;
  Count cSubPassedEta;
  Count cSubPassedLdgTrk;
  Count cSubPassedNprongs;
  Count cSubPassedIsolation;
  Count cSubPassedRtau;
  // Histograms
  WrappedTH1 *hTriggerMatchDeltaR;
  WrappedTH1 *hTauPtTriggerMatched;
  WrappedTH1 *hTauEtaTriggerMatched;
  WrappedTH1 *hNPassed;
};

#endif
