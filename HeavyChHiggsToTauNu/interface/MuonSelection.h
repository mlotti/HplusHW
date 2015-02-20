// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_MuonSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_MuonSelection_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h" 
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"


/// The class is designed so that when the methond analyze is called it returns FALSE if a Global Muon is found passing all criteria. 
/// It returns TRUE if no muons are found or if the muons present do NOT satisfy the "Selection of muons" as chosen by TTbar analyses.
namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class WrappedTH2;

  class MuonSelection: public BaseSelection {
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
      // Getters for veto on isolated muons
      const bool passedEvent() const { return passedMuonVeto(); }
      const bool passedMuonVeto() const { return (fSelectedMuonsLoose.size() == 0); }
      const float getSelectedMuonPt() const { return fSelectedMuonPt; }
      const float getSelectedMuonEta() const { return fSelectedMuonEta; }
      const float getSelectedMuonPtBeforePtCut() const { return fSelectedMuonPtBeforePtCut; }
      // Getters for finding isolated muons
      const bool foundTightMuon() const { return (fSelectedMuonsTight.size() > 0); }
      const bool foundLooseMuon() const { return (fSelectedMuonsLoose.size() > 0); }
      // Getters for MC info about non-isolated muons for events that passed veto
      const bool eventContainsMuonFromCJet() const { return fHasMuonFromCjetStatus; }
      const bool eventContainsMuonFromBJet() const { return fHasMuonFromBjetStatus; }
      const bool eventContainsMuonFromCorBJet() const { return eventContainsMuonFromCJet() || eventContainsMuonFromBJet(); }

      /// Muon collection after all selections - size should be zero if veto condition is passed
      const edm::PtrVector<pat::Muon>& getSelectedMuons() const { return fSelectedMuonsLoose; }
      /// Muon collection after all selections - loose isolation
      const edm::PtrVector<pat::Muon>& getSelectedLooseMuons() const { return fSelectedMuonsLoose; }
      /// Muon collection after all selections - loose isolation
      const edm::PtrVector<pat::Muon>& getSelectedTightMuons() const { return fSelectedMuonsTight; }
      /// Muon collection after all selections - anti-isolated (relIsol > 0.2)
      const edm::PtrVector<pat::Muon>& getNonIsolatedMuons() const { return fSelectedNonIsolatedMuons; }
      /// Muon collection after all selections except pt and eta cuts
      const edm::PtrVector<pat::Muon>& getSelectedMuonsBeforePtAndEtaCuts() const { return fSelectedMuonsBeforePtAndEtaCuts; }
      /// Muon collection after all selections except isolation, needed for embedding studies (a custom isolation is calculated)
      const edm::PtrVector<pat::Muon>& getSelectedMuonsBeforeIsolation() const { return fSelectedMuonsBeforeIsolation; }

      friend class MuonSelection;

    private:
      /// pt and eta of muon with highest pt passing the selections
      float fSelectedMuonPt;
      float fSelectedMuonEta;
      float fSelectedMuonPtBeforePtCut;
      /// MC info about non-isolated muons
      bool fHasMuonFromCjetStatus;
      bool fHasMuonFromBjetStatus;
      /// Muon collection after all selections
      edm::PtrVector<pat::Muon> fSelectedMuonsTight;
      edm::PtrVector<pat::Muon> fSelectedMuonsLoose;
      edm::PtrVector<pat::Muon> fSelectedNonIsolatedMuons;
      edm::PtrVector<pat::Muon> fSelectedMuonsBeforePtAndEtaCuts;
      edm::PtrVector<pat::Muon> fSelectedMuonsBeforeIsolation;

    };

    MuonSelection(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~MuonSelection();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex);

    void debug(void);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex);

    void doMuonSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex, MuonSelection::Data& output);

    // Input parameters
    const edm::InputTag fGenParticleSrc;
    const edm::InputTag fMuonCollectionName;
    const bool fApplyMuonIsolation;
    const double fMuonPtCut;
    const double fMuonEtaCut;
    
    /// Sub-Counters
    Count fMuonSelectionSubCountAllEvents;
    Count fMuonSelectionSubCountMuonPresent;
    Count fMuonSelectionSubCountMuonHasGlobalOrInnerTrk;
    Count fMuonSelectionSubCountMuonGlobalMuonOrTrkerMuon;
    Count fMuonSelectionSubCountPFMuonSelection;
    Count fMuonSelectionSubCountNTrkerHitsCut;
    Count fMuonSelectionSubCountNPixelHitsCut;
    Count fMuonSelectionSubCountNMuonlHitsCut;
    Count fMuonSelectionSubCountGlobalTrkChiSqCut;
    Count fMuonSelectionSubCountImpactParCut;
    Count fMuonSelectionSubCountGoodPVCut;
    Count fMuonSelectionSubCountRelIsolationCut;
    Count fMuonSelectionSubCountEtaCut;
    Count fMuonSelectionSubCountPtCut;
    Count fMuonSelectionSubCountVetoMuonFound;
    Count fMuonSelectionSubCountMatchingMCmuon;
    Count fMuonSelectionSubCountMatchingMCmuonFromW;
    Count fMuonSelectionSubCountTightMuonFound;
    Count fMuonSelectionSubCountMuonVetoPassed;
    Count fMuonSelectionSubCountPassedVetoAndMuonFromCjet;
    Count fMuonSelectionSubCountPassedVetoAndMuonFromBjet;

    // Histograms
    //    WrappedTH1 *hMuonPt_test;
    //    WrappedTH1 *hMuonEta_test;
    WrappedTH1 *hTightMuonPt;
    WrappedTH1 *hTightMuonEta;
    WrappedTH1 *hLooseMuonPt;
    WrappedTH1 *hLooseMuonEta;
    WrappedTH1 *hNumberOfTightMuons;
    WrappedTH1 *hNumberOfLooseMuons;
    WrappedTH1 *hMuonPt_matchingMCmuon;
    WrappedTH1 *hMuonEta_matchingMCmuon;
    WrappedTH1 *hMuonPt_matchingMCmuonFromW;
    WrappedTH1 *hMuonEta_matchingMCmuonFromW;
    WrappedTH1 *hMuonPt_BeforeIsolation;
    WrappedTH1 *hMuonEta_BeforeIsolation;
    WrappedTH1 *hMuonPt_InnerTrack_BeforeIsolation;
    WrappedTH1 *hMuonEta_InnerTrack_BeforeIsolation;
    WrappedTH1 *hMuonPt_GlobalTrack_BeforeIsolation;
    WrappedTH1 *hMuonEta_GlobalTrack_BeforeIsolation;
    WrappedTH1 *hMuonPt_AfterSelection;
    WrappedTH1 *hMuonEta_AfterSelection;
    WrappedTH1 *hMuonPt_InnerTrack_AfterSelection;
    WrappedTH1 *hMuonEta_InnerTrack_AfterSelection;
    WrappedTH1 *hMuonPt_GlobalTrack_AfterSelection;
    WrappedTH1 *hMuonEta_GlobalTrack_AfterSelection;
    WrappedTH1 *hMuonTransverseImpactParameter;
    WrappedTH1 *hMuonDeltaIPz;
    WrappedTH1 *hMuonRelIsol;
    WrappedTH2 *hMCMuonEtaPhiForPassedEvents;
    WrappedTH2 *hMuonEtaPhiForSelectedMuons;

  };
}

#endif
