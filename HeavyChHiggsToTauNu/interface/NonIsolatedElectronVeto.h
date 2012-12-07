// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_NonIsolatedElectronVeto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_NonIsolatedElectronVeto_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include <DataFormats/BeamSpot/interface/BeamSpot.h>
#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "RecoEgamma/EgammaTools/interface/ConversionFinder.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include <MagneticField/Engine/interface/MagneticField.h>
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h" 

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  
  class NonIsolatedElectronVeto: public BaseSelection {
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
      Data(const NonIsolatedElectronVeto *nonIsolatedElectronVeto, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      const edm::PtrVector<pat::Electron>& getElectronswithGSFTrk() { return fNonIsolatedElectronVeto->fElectronsWithGSFTrk; }
      const float getSelectedElectronPt() const { return fNonIsolatedElectronVeto->fSelectedElectronPt; }
      const float getSelectedElectronEta() const { return fNonIsolatedElectronVeto->fSelectedElectronEta; }

      const edm::PtrVector<pat::Electron>& getSelectedElectrons() { return fNonIsolatedElectronVeto->fSelectedElectrons; }

    private:
      const NonIsolatedElectronVeto *fNonIsolatedElectronVeto;
      const bool fPassedEvent;
    };

    NonIsolatedElectronVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~NonIsolatedElectronVeto();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Official Electron ID
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Official Electron ID
    Data analyzeCustomElecID(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Requires General Tracks
   
  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Official Electron ID
    
    bool ElectronSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Official Electron ID
    bool CustomElectronSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Requires General Tracks

    // Input parameters
    edm::InputTag fElecCollectionName;
    const std::string fElecSelection;
    const double fElecPtCut;
    const double fElecEtaCut;
    
    // Counters
    Count fNonIsolatedElectronVetoCounter;
    Count fElecSelectionSubCountElectronPresent;
    Count fElecSelectionSubCountElectronHasGsfTrkOrTrk;
    Count fElecSelectionSubCountPtCut;
    Count fElecSelectionSubCountEtaCut;
    Count fElecSelectionSubCountFiducialVolumeCut;
    Count fElecSelectionSubCountMatchingMCelectron;
    Count fElecSelectionSubCountMatchingMCelectronFromW;
    Count fElecSelectionSubCountElectronSelection;
    Count fElecSelectionSubCountNLostHitsInTrkerCut;
    Count fElecSelectionSubCountmyElectronDeltaCotThetaCut;
    Count fElecSelectionSubCountmyElectronDistanceCut;
    Count fElecSelectionSubCountTransvImpactParCut;
    Count fElecSelectionSubCountDeltaRFromGlobalOrTrkerMuonCut;
    Count fElecSelectionSubCountRelIsolationR03Cut;
    // Sub-Counters (ElectronID) - just for my information
    Count fElecIDSubCountAllElectronCandidates;
    Count fElecIDSubCountElecIDLoose;
    Count fElecIDSubCountElecIDRobustLoose;
    Count fElecIDSubCountElecIDTight;
    Count fElecIDSubCountElecIDRobustTight;
    Count fElecIDSubCountElecIDRobustHighEnergy;
    Count fElecIDSubCountSimpleEleId95relIso;
    Count fElecIDSubCountSimpleEleId90relIso;
    Count fElecIDSubCountSimpleEleId85relIso;
    Count fElecIDSubCountSimpleEleId80relIso;
    Count fElecIDSubCountSimpleEleId70relIso;
    Count fElecIDSubCountSimpleEleId60relIso;

    // Histograms
    WrappedTH1 *hElectronPt;
    WrappedTH1 *hElectronEta;
    WrappedTH1 *hElectronPt_matchingMCelectron;
    WrappedTH1 *hElectronEta_matchingMCelectron;
    WrappedTH1 *hElectronPt_matchingMCelectronFromW;
    WrappedTH1 *hElectronEta_matchingMCelectronFromW;
    WrappedTH1 *hElectronPt_gsfTrack;
    WrappedTH1 *hElectronEta_gsfTrack;
    WrappedTH1 *hElectronPt_AfterSelection;
    WrappedTH1 *hElectronEta_AfterSelection;
    WrappedTH1 *hElectronPt_gsfTrack_AfterSelection;
    WrappedTH1 *hElectronEta_gsfTrack_AfterSelection;
    WrappedTH1 *hElectronImpactParameter;
    WrappedTH1 *hElectronEta_superCluster;

    // pt and eta of highest pt electron passing the selection
    float fSelectedElectronPt;
    float fSelectedElectronEta;

    // for Electron-ID Selection
    bool bDecision;
    bool bPassedElecID;
    bool bUseLooseID;
    bool bUseRobustLooseID;
    bool bUseTightID;
    bool bUseRobustTightID;
    bool bUseRobustHighEnergyID;
    bool bUseSimpleEleId95relIsoID;
    bool bUseSimpleEleId90relIsoID;
    bool bUseSimpleEleId85relIsoID;
    bool bUseSimpleEleId80relIsoID;
    bool bUseSimpleEleId70relIsoID;
    bool bUseSimpleEleId60relIsoID;
    bool bUseCustomElectronID;

    // Selected electrons
    edm::PtrVector<pat::Electron> fElectronsWithGSFTrk;
    edm::PtrVector<pat::Electron> fSelectedElectrons;
  };
}

#endif
