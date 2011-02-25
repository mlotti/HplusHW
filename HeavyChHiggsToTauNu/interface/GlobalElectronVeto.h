// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_GlobalElectronVeto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_GlobalElectronVeto_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

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

class TH1;
#include "TH2.h"

namespace HPlus {
  class GlobalElectronVeto {
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
      Data(const GlobalElectronVeto *globalElectronVeto, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      const float getSelectedElectronPt() const { return fGlobalElectronVeto->fSelectedElectronPt; }
      const float getSelectedElectronEta() const { return fGlobalElectronVeto->fSelectedElectronEta; }

    private:
      const GlobalElectronVeto *fGlobalElectronVeto;
      const bool fPassedEvent;
    };

    GlobalElectronVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);
    ~GlobalElectronVeto();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Official Electron ID
    Data analyzeCustomElecID(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Requires General Tracks
   
  private:

    bool ElectronSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Official Electron ID
    bool CustomElectronSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Requires General Tracks

    // Input parameters
    edm::InputTag fElecCollectionName;
    const std::string fElecSelection;
    const double fElecPtCut;
    const double fElecEtaCut;
    
    // Counters
    Count fGlobalElectronVetoCounter;
    Count fElecSelectionSubCountElectronPresent;
    Count fElecSelectionSubCountElectronHasGsfTrkOrTrk;
    Count fElecSelectionSubCountPtCut;
    Count fElecSelectionSubCountEtaCut;
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
    
    // EventWeight object
    EventWeight& fEventWeight;

    // Histograms
    TH1 *hElectronPt;
    TH1 *hElectronEta;
    TH1 *hElectronPt_gsfTrack;
    TH1 *hElectronEta_gsfTrack;
    TH1 *hElectronPt_AfterSelection;
    TH1 *hElectronEta_AfterSelection;
    TH1 *hElectronPt_gsfTrack_AfterSelection;
    TH1 *hElectronEta_gsfTrack_AfterSelection;
    TH1 *hElectronImpactParameter;

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
  };
}

#endif
