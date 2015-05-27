// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauIDBase_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauIDBase_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SelectionCounterPackager.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeadECALCells.h"

#include "CommonTools/Utils/interface/TFileDirectory.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

#include <string>

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class WrappedTH2;

  class TauIDBase {
  public:

    /**
     * Base class for tau ID operations.
     * Actual tau ID specific classes are inherited from this class.
     */
    TauIDBase(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, const std::string& baseLabel, TFileDirectory& myDir);
    virtual ~TauIDBase();

    /// Returns true, if the tau candidate conditions are fulfilled (jet et, eta, ldg pt, e/mu veto) 

    void incrementAllCandidates();
    virtual bool passDecayModeFinding(const edm::Ptr<pat::Tau>& tau) = 0;
    bool passVertexZCut(const edm::Ptr<pat::Tau> tau, double vertexZ);
    bool passKinematicSelection(const edm::Ptr<pat::Tau> tau);
    bool passKinematicSelectionPt(const edm::Ptr<pat::Tau>& tau);
    bool passKinematicSelectionEta(const edm::Ptr<pat::Tau>& tau);

    virtual bool passLeadingTrackCuts(const edm::Ptr<pat::Tau> tau) = 0;
    bool passTauCandidateEAndMuVetoCuts(const edm::Ptr<pat::Tau> tau);
    bool passTauCandidateEVetoCuts(const edm::Ptr<pat::Tau>& tau);
    bool passTauCandidateMuVetoCuts(const edm::Ptr<pat::Tau>& tau);

    bool passVetoAgainstDeadECALCells(const edm::Ptr<pat::Tau> tau);
    bool passIsolation(const edm::Ptr<pat::Tau> tau);
    bool passAntiIsolation(const edm::Ptr<pat::Tau> tau);
    virtual bool passNProngsCut(const edm::Ptr<pat::Tau> tau) = 0;
    virtual size_t getNProngs(const edm::Ptr<pat::Tau> tau) const = 0;
    virtual bool passRTauCut(const edm::Ptr<pat::Tau> tau) = 0;
    virtual double getRtauValue(const edm::Ptr<pat::Tau> tau) const = 0;
    bool passECALFiducialCuts(const edm::Ptr<pat::Tau> tau);

    /// Call at the beginning of the event (before looping over all tau-jet candidates) 
    void reset();
    /// Call at the end of event (after looping over all tau-jet candidates)
    void updatePassedCounters();

    std::string getIsolationDiscriminator() const { return fIsolationDiscriminator; }

  protected:
    TFileDirectory fMyDir;
    
    // Input parameters
    const double fVertexZCut;
    const double fPtCut;
    const double fEtaCut;
    const double fLeadTrkPtCut;
    const std::string fAgainstElectronDiscriminator;
    const bool fApplyVetoForDeadECALCells;
    const double fDeadECALCellsDeltaR;
    const std::string fAgainstMuonDiscriminator;
    const size_t fProngCount;
    const std::string fIsolationDiscriminator;
    double fIsolationDiscriminatorContinuousCutPoint;
    const double fRtauCut;
    
    // Counters packaged in one object
    SelectionCounterPackager fCounterPackager;
    // Tau-jet candidate selections (same for all tau ID algorithms)
    size_t fIDAllTauCandidates;
    size_t fIDDecayModeFinding;
    size_t fIDVertexZCut;
    size_t fIDJetPtCut;
    size_t fIDJetEtaCut;
    size_t fIDLdgTrackExistsCut;
    size_t fIDLdgTrackPtCut;
    size_t fIDECALFiducialCutCracksOnly;
    size_t fIDECALFiducialCut;
    size_t fIDAgainstElectronCut;
    size_t fVetoAgainstDeadECALCells;
    size_t fIDAgainstMuonCut;
    size_t fIDIsolationCut;
    size_t fIDNProngsCut;
    size_t fIDRTauCut;

    DeadECALCells fDeadECALCells;

    /// Label of the specific tau ID algorithm (applied to counters and histograms)
    std::string fBaseLabel;

    // Histograms
    WrappedTH2* hRtauVsEta;
    WrappedTH1* hEtaTauCands_nocut;
    WrappedTH1* hEtaTauCands_ptcut;
  };
}

#endif
