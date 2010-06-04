#ifndef HPLUSANALYSISHPLUSGLOBALELECTRONVETO_H
#define HPLUSANALYSISHPLUSGLOBALELECTRONVETO_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusAnalysisBase.h"
#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusSelectionBase.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "TH1F.h"

//namespace HPlusAnalysis {

/**
Class for applying global electron veto, i.e. loop over all electrons in the event
and reject the event, if any electron has pT greater than the cut value.
Electron identification can be required from the list of electrons analyzed. 

This selection method is aimed against the W->e nu and W->tau nu->e nu nu
decays, which might spoil the MET measurement for the fully hadronic
H+ -> tau nu decay channel 

	@author Lauri Wendland, Ritva Kinnunen
*/
class HPlusGlobalElectronVeto : public HPlusAnalysis::HPlusAnalysisBase, public HPlusAnalysis::HPlusSelectionBase {
  enum GlobalElectronIdentificationType {
    kNoElectronIdentification,
    kRobustElectronIdentification,
    kLooseElectronIdentification,
    kTightElectronIdentification
  };
 
 public:
  /// Default constructor
  HPlusGlobalElectronVeto(const edm::ParameterSet& iConfig);
  /// Default destructor
  ~HPlusGlobalElectronVeto();
  
  void beginJob();
  void endJob();
  /// Applies the trigger selection; returns true if trigger was passed
  bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  
 private:
  /// Name of electron collection
  edm::InputTag fElectronCollectionName;
  /// Type of electron identification
  GlobalElectronIdentificationType fElectronIdentificationType;
  /// Cut value for pTmax of muon
  float fCutValueMaxElectronPt;
  // Counter ID's
  /// IDs of the event counters
  int fGlobalElectronVetoInput;
  int fPassedGlobalElectronVeto;
  int fElectronCollectionHandleEmpty;
  int fAllElectronCandidates;
  int fAfterElectronID;
  int fAfterTrackRefNonNull;
  int fFailedPtCut;
  // Histograms
  /// Maximum muon pT in event (-1 if no muon in event)
  TH1F* hElectronMaxPt;
  /// eta of muon with highest pT in event (-4 if no muon in event)
  TH1F* hElectronEtaofHighest;
  /// pT of all muons (could be 0 or more per event)
  TH1F* hElectronPtAllElectrons;
  /// eta of all muons (could be 0 or more per event)
  TH1F* hElectronEtaAllElectrons;
};

//}

#endif
