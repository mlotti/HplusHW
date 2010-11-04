// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_GlobalElectronVeto_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_GlobalElectronVeto_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

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

class TH1;
#include "TH2.h"

namespace HPlus {
  class GlobalElectronVeto {

  public:
    GlobalElectronVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    ~GlobalElectronVeto();

    bool analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Official Elecectron ID
    bool analyzeCustomElecID(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Requires General Tracks

    const float getSelectedElectronsPt() const {
      return fSelectedElectronsPt;
    }
    const float getSelectedElectronsEta() const {
      return fSelectedElectronsEta;
    }
   
  private:

    bool ElectronSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Official Elecectron ID
    bool CustomElectronSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup); // Requires General Tracks


    // Input parameters
    edm::InputTag fElecCollectionName;
    std::string fElecSelection;
    double fElecPtCut;
    double fElecEtaCut;
    
    /// Counter
    Count fGlobalElectronVetoCounter;
    /// Sub-Counter to Counter
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
    /// Sub-Counter (ElectronID) - just for my information
    Count fElecIDSubCountAllElectronCandidates;
    Count fElecIDSubCountElecIDRobustHighEnergy;
    Count fElecIDSubCountElecIDRobustLoose;
    Count fElecIDSubCountElecIDRobustTight;
    Count fElecIDSubCountElecIDLoose;
    Count fElecIDSubCountElecIDTight;

    Count fElecIDSubCountSimpleEleId95relIso;
    Count fElecIDSubCountSimpleEleId90relIso;
    Count fElecIDSubCountSimpleEleId85relIso;
    Count fElecIDSubCountSimpleEleId80relIso;
    Count fElecIDSubCountSimpleEleId70relIso;
    Count fElecIDSubCountSimpleEleId60relIso;
    
    // Histograms
    TH1 *hElectronPt;
    TH1 *hElectronEta;
    TH1 *hElectronPt_gsfTrack;
    TH1 *hElectronEta_gsfTrack;
    TH1 *hElectronPt_AfterSelection;
    TH1 *hElectronEta_AfterSelection;
    TH1 *hElectronPt_gsfTrack_AfterSelection;
    TH1 *hElectronEta_gsfTrack_AfterSelection;

    // Selected Electrons
    float fSelectedElectronsPt;
    float fSelectedElectronsEta;

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

  };
}

#endif
