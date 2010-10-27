// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_GlobalMuonVeto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_GlobalMuonVeto_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h" 

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

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
    GlobalMuonVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    ~GlobalMuonVeto();

    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    const float getSelectedMuonsPt() const {
      return fSelectedMuonsPt;
    }
    const float getSelectedMuonsEta() const {
      return fSelectedMuonsEta;
    }
    
  private:

    bool MuonSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup);


    // Input parameters
    edm::InputTag fMuonCollectionName;
    std::string fMuonSelection;
    double fMuonPtCut;
    double fMuonEtaCut;
    
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

    // Histograms
    TH1 *hMuonPt_InnerTrack;
    TH1 *hMuonEta_InnerTrack;
    TH1 *hMuonPt_GlobalTrack;
    TH1 *hMuonEta_GlobalTrack;
    TH1 *hMuonPt_InnerTrack_AfterSelection;
    TH1 *hMuonEta_InnerTrack_AfterSelection;
    TH1 *hMuonPt_GlobalTrack_AfterSelection;
    TH1 *hMuonEta_GlobalTrack_AfterSelection;

    // Selected Muons
    float fSelectedMuonsPt;
    float fSelectedMuonsEta;
  };
}

#endif
