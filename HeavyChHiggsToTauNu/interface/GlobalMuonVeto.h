// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_GlobalMuonVeto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_GlobalMuonVeto_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h" 
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

/// The class is designed so that when the methond analyze is called it returns FALSE if a Global Muon is found passing all criteria. 
/// It returns TRUE if no muons are found or if the muons present do NOT satisfy the "Selection of muons" as chosen by TTbar analyses.
namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
#include "TH2.h"

namespace HPlus {
  class GlobalMuonVeto {
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
      Data(const GlobalMuonVeto *globalMuonVeto, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      const float getSelectedMuonPt() const { return fGlobalMuonVeto->fSelectedMuonPt; }
      const float getSelectedMuonEta() const { return fGlobalMuonVeto->fSelectedMuonEta; }
    
    private:
      const GlobalMuonVeto *fGlobalMuonVeto;
      const bool fPassedEvent;
    };
    
    GlobalMuonVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~GlobalMuonVeto();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex);
    void debug(void);

  private:
    bool MuonSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<reco::Vertex>& primaryVertex);

    // Input parameters
    edm::InputTag fMuonCollectionName;
    const std::string fMuonSelection;
    const double fMuonPtCut;
    const double fMuonEtaCut;
    const bool fMuonApplyIpz;
    
    /// Counter
    Count fGlobalMuonVetoCounter;
    /// Sub-Counter to Counter
    Count fMuonSelectionSubCountMuonPresent;
    Count fMuonSelectionSubCountMuonHasGlobalOrInnerTrk;
    Count fMuonSelectionSubCountPtCut;
    Count fMuonSelectionSubCountEtaCut;
    Count fMuonSelectionSubCountMuonGlobalMuonOrTrkerMuon;
    Count fMuonSelectionSubCountMuonSelection;
    Count fMuonSelectionSubCountNTrkerHitsCut;
    Count fMuonSelectionSubCountNPixelHitsCut;
    Count fMuonSelectionSubCountNMuonlHitsCut;
    Count fMuonSelectionSubCountGlobalTrkChiSqCut;
    Count fMuonSelectionSubCountImpactParCut;
    Count fMuonSelectionSubCountRelIsolationR03Cut;
    Count fMuonSelectionSubCountGoodPVCut;
    Count fMuonSelectionSubCountMatchingMCmuon;
    Count fMuonSelectionSubCountMatchingMCmuonFromW;
    /// Sub-Counter (MuonID) - just for my information
    Count fMuonIDSubCountAllMuonCandidates;
    Count fMuonIDSubCountAll;
    Count fMuonIDSubCountAllGlobalMuons;
    Count fMuonIDSubCountAllStandAloneMuons;
    Count fMuonIDSubCountAllTrackerMuons;
    Count fMuonIDSubCountTrackerMuonArbitrated;
    Count fMuonIDSubCountAllArbitrated;
    Count fMuonIDSubCountGlobalMuonPromptTight;
    Count fMuonIDSubCountTMLastStationLoose;
    Count fMuonIDSubCountTMLastStationTight;
    Count fMuonIDSubCountTMOneStationLoose;
    Count fMuonIDSubCountTMLastStationOptimizedLowPtLoose;
    Count fMuonIDSubCountTMLastStationOptimizedLowPtTight;
    Count fMuonIDSubCountGMTkChiCompatibility;
    Count fMuonIDSubCountGMTkKinkTight;
    Count fMuonIDSubCountTMLastStationAngLoose;
    Count fMuonIDSubCountTMLastStationAngTight;
    Count fMuonIDSubCountTMLastStationOptimizedBarrelLowPtLoose;
    Count fMuonIDSubCountTMLastStationOptimizedBarrelLowPtTight;
    Count fMuonIDSubCountOther;

    // EventWeight object
    EventWeight& fEventWeight;

    // Histograms
    TH1 *hMuonPt;
    TH1 *hMuonEta;
    TH1 *hMuonPt_matchingMCmuon;
    TH1 *hMuonEta_matchingMCmuon;
    TH1 *hMuonPt_matchingMCmuonFromW;
    TH1 *hMuonEta_matchingMCmuonFromW;
    TH1 *hMuonPt_InnerTrack;
    TH1 *hMuonEta_InnerTrack;
    TH1 *hMuonPt_GlobalTrack;
    TH1 *hMuonEta_GlobalTrack;
    TH1 *hMuonPt_AfterSelection;
    TH1 *hMuonEta_AfterSelection;
    TH1 *hMuonPt_InnerTrack_AfterSelection;
    TH1 *hMuonEta_InnerTrack_AfterSelection;
    TH1 *hMuonPt_GlobalTrack_AfterSelection;
    TH1 *hMuonEta_GlobalTrack_AfterSelection;
    TH1 *hMuonImpactParameter;
    TH1 *hMuonZdiff;
    // pt and eta of muon with highest pt passing the selections
    float fSelectedMuonPt;
    float fSelectedMuonEta;

    // booleans
    bool bMuonPresent;
    bool bDecision;
    bool bMuonHasGlobalOrInnerTrk;
    bool bMuonPtCut;
    bool bMuonEtaCut;
    bool bMuonGlobalMuonOrTrkerMuon;
    bool bMuonSelection;
    bool bMuonNTrkerHitsCut;
    bool bMuonNPixelHitsCut;
    bool bMuonNMuonlHitsCut;
    bool bMuonGlobalTrkChiSqCut;
    bool bMuonImpactParCut;
    bool bMuonRelIsolationR03Cut;
    bool bMuonGoodPVCut;
    bool bMuonMatchingMCmuon;
    bool bMuonMatchingMCmuonFromW;
    
  };
}

#endif
