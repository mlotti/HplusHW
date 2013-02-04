// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_GlobalElectronVeto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_GlobalElectronVeto_h

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

  class GlobalElectronVeto: public BaseSelection {
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

      const bool passedEvent() const { return fPassedEvent; }
      const float getSelectedElectronPt() const { return fSelectedElectronPt; }
      const float getSelectedElectronEta() const { return fSelectedElectronEta; }
      const float getSelectedElectronPtBeforePtCut() const { return fSelectedElectronPtBeforePtCut; }
      const edm::PtrVector<pat::Electron>& getSelectedElectrons() { return fSelectedElectrons; }
      const edm::PtrVector<pat::Electron>& getSelectedElectronsBeforePtAndEtaCuts() { return fSelectedElectronsBeforePtAndEtaCuts; }

      friend class GlobalElectronVeto;

    private:
      bool fPassedEvent;
      // pt and eta of highest pt electron passing the selection
      float fSelectedElectronPt;
      float fSelectedElectronEta;
      float fSelectedElectronPtBeforePtCut;

      // Selected electrons
      edm::PtrVector<pat::Electron> fSelectedElectrons;
      edm::PtrVector<pat::Electron> fSelectedElectronsBeforePtAndEtaCuts;

    };

    GlobalElectronVeto(const edm::ParameterSet& iConfig, const edm::InputTag& vertexSrc, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~GlobalElectronVeto();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    // Input parameters
    edm::InputTag fElecCollectionName;
    edm::InputTag fVertexSrc;
    edm::InputTag fConversionSrc;
    edm::InputTag fBeamspotSrc;
    edm::InputTag fRhoSrc;
    const std::string fElecSelection;
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
    Count fElecSelectionSubCountSelected;
    Count fElecSelectionSubCountMatchingMCelectron;
    Count fElecSelectionSubCountMatchingMCelectronFromW;

    // Histograms
    WrappedTH1 *hElectronPt;
    WrappedTH1 *hElectronEta;
    WrappedTH1 *hNumberOfSelectedElectrons;
    WrappedTH1 *hElectronPt_identified;
    WrappedTH1 *hElectronEta_identified;
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

    WrappedTH2 *hElectronEtaPhiForSelectedElectrons;
    WrappedTH2 *hMCElectronEtaPhiForPassedEvents;

    // for Electron-ID Selection
    EgammaCutBasedEleId::WorkingPoint fElectronIdEnumerator;

  };
}

#endif
