// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ElectronSelection_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ElectronSelection_h

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
//#include "DataFormats/PatCandidates/interface/Muon.h"
//#include "DataFormats/MuonReco/interface/MuonSelectors.h" 
#include "EGamma/EGammaAnalysisTools/interface/EGammaCutBasedEleId.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class WrappedTH2;

  class ElectronSelection: public BaseSelection {
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

      const bool passedEvent() const { return passedElectronVeto(); }
      const bool passedElectronVeto() const { return (fSelectedElectronsVeto.size() == 0); }
      const float getSelectedElectronPt() const { return fSelectedElectronPt; }
      const float getSelectedElectronEta() const { return fSelectedElectronEta; }
      const float getSelectedElectronPtBeforePtCut() const { return fSelectedElectronPtBeforePtCut; }
      const bool foundTightElectron() const { return (fSelectedElectronsTight.size() > 0); }
      const bool foundMediumElectron() const { return (fSelectedElectronsMedium.size() > 0); }
      const bool eventContainsElectronFromCJet() const { return fHasElectronFromCjetStatus; }
      const bool eventContainsElectronFromBJet() const { return fHasElectronFromBjetStatus; }
      const bool eventContainsElectronFromCorBJet() const { return eventContainsElectronFromCJet() || eventContainsElectronFromBJet(); }
      const edm::PtrVector<pat::Electron>& getSelectedElectrons() const { return fSelectedElectronsVeto; }
      const edm::PtrVector<pat::Electron>& getSelectedElectronsVeto() const { return fSelectedElectronsVeto; }
      const edm::PtrVector<pat::Electron>& getSelectedElectronsMedium() const { return fSelectedElectronsMedium; }
      const edm::PtrVector<pat::Electron>& getSelectedElectronsTight() const { return fSelectedElectronsTight; }
      const edm::PtrVector<pat::Electron>& getNonIsolatedElectrons() const { return fSelectedNonIsolatedElectrons; }
      const edm::PtrVector<pat::Electron>& getSelectedElectronsBeforePtAndEtaCuts() const { return fSelectedElectronsBeforePtAndEtaCuts; }

      friend class ElectronSelection;

    private:
      /// pt and eta of highest pt electron passing the selection
      float fSelectedElectronPt;
      float fSelectedElectronEta;
      float fSelectedElectronPtBeforePtCut;
      /// MC info about non-isolated electrons
      bool fHasElectronFromCjetStatus;
      bool fHasElectronFromBjetStatus;
      /// Electron collections after all selections
      edm::PtrVector<pat::Electron> fSelectedElectronsVeto;
      edm::PtrVector<pat::Electron> fSelectedElectronsTight;
      edm::PtrVector<pat::Electron> fSelectedElectronsMedium;
      edm::PtrVector<pat::Electron> fSelectedNonIsolatedElectrons;
      edm::PtrVector<pat::Electron> fSelectedElectronsBeforePtAndEtaCuts;

    };

    ElectronSelection(const edm::ParameterSet& iConfig, const edm::InputTag& vertexSrc, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~ElectronSelection();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    EgammaCutBasedEleId::WorkingPoint translateWorkingPoint(const std::string& wp);
    
    // Input parameters
    const edm::InputTag fGenParticleSrc;
    const edm::InputTag fElecCollectionName;
    const edm::InputTag fVertexSrc;
    const edm::InputTag fConversionSrc;
    const edm::InputTag fBeamspotSrc;
    const edm::InputTag fRhoSrc;
    const std::string fElecSelectionVeto;
    const std::string fElecSelectionMedium;
    const std::string fElecSelectionTight;
    const double fElecPtCut;
    const double fElecEtaCut;
    
    // Counters
    Count fElecSelectionSubCountAllEvents;
    Count fElecSelectionSubCountElectronPresent;
    Count fElecSelectionSubCountElectronHasGsfTrkOrTrk;
    Count fElecSelectionSubCountFiducialVolumeCut;
    Count fElecSelectionSubCountId;
    Count fElecSelectionSubCountEtaCut;
    Count fElecSelectionSubCountPtCut;
    Count fElecSelectionSubCountSelectedVeto;
    Count fElecSelectionSubCountMatchingMCelectron;
    Count fElecSelectionSubCountMatchingMCelectronFromW;
    Count fElecSelectionSubCountSelectedMedium;
    Count fElecSelectionSubCountSelectedTight;
    Count fElecSelectionSubCountPassedVeto;
    Count fElecSelectionSubCountPassedVetoAndElectronFromCjet;
    Count fElecSelectionSubCountPassedVetoAndElectronFromBjet;

    // Histograms
    // all candidates
    WrappedTH1 *hElectronPt_all;
    WrappedTH1 *hElectronEta_all;
    WrappedTH1 *hElectronPt_gsfTrack_all;
    WrappedTH1 *hElectronEta_gsfTrack_all;
    WrappedTH1 *hElectronEta_superCluster;
    // Selected electrons for veto
    WrappedTH1 *hNumberOfVetoElectrons;
    WrappedTH1 *hElectronPt_veto;
    WrappedTH1 *hElectronEta_veto;
    WrappedTH1 *hElectronPt_matchingMCelectron;
    WrappedTH1 *hElectronEta_matchingMCelectron;
    WrappedTH1 *hElectronPt_matchingMCelectronFromW;
    WrappedTH1 *hElectronEta_matchingMCelectronFromW;
    WrappedTH1 *hElectronPt_AfterSelection;
    WrappedTH1 *hElectronEta_AfterSelection;
    WrappedTH1 *hElectronPt_gsfTrack_AfterSelection;
    WrappedTH1 *hElectronEta_gsfTrack_AfterSelection;
    WrappedTH2 *hElectronEtaPhiForSelectedElectrons;
    WrappedTH2 *hMCElectronEtaPhiForPassedEvents;
    // Selected electrons for medium
    WrappedTH1 *hNumberOfMediumElectrons;
    WrappedTH1 *hElectronPt_medium;
    WrappedTH1 *hElectronEta_medium;    
    // Selected electrons for tight
    WrappedTH1 *hNumberOfTightElectrons;
    WrappedTH1 *hElectronPt_tight;
    WrappedTH1 *hElectronEta_tight;
    
    // for Electron-ID Selection
    EgammaCutBasedEleId::WorkingPoint fElectronIdEnumeratorVeto;
    EgammaCutBasedEleId::WorkingPoint fElectronIdEnumeratorMedium;
    EgammaCutBasedEleId::WorkingPoint fElectronIdEnumeratorTight;
  };
}

#endif
