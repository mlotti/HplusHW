#ifndef HPLUSANALYSISHPLUSGLOBALMUONVETO_H
#define HPLUSANALYSISHPLUSGLOBALMUONVETO_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusAnalysisBase.h"
#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusSelectionBase.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"

#include "TH1F.h"

#include <vector>

//namespace HPlusAnalysis {

/**
Class for applying global muon veto, i.e. loop over all muons in the event
and reject the event, if any muon has pT greater than the cut value.

This selection method is aimed against the W->mu nu and W->tau nu->mu nu nu
decays, which might spoil the MET measurement for the fully hadronic
H+ -> tau nu decay channel 

	@author Lauri Wendland, Ritva Kinnunen
*/
class HPlusGlobalMuonVeto : public HPlusAnalysis::HPlusAnalysisBase, public HPlusAnalysis::HPlusSelectionBase {
 public:
  /// Default constructor
  HPlusGlobalMuonVeto(const edm::ParameterSet& iConfig);
  /// Default destructor
  ~HPlusGlobalMuonVeto();
  
  void beginJob();
  void endJob();
  /// Applies the trigger selection; returns true if trigger was passed
  bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  /// Setter for excluded muons
  void addExcludedMuon(const reco::Muon* muon) { fExcludedMuons.push_back(muon); }
  
 private:
  /// Name of muon collection
  edm::InputTag fMuonCollectionName;
  /// Cut value for pTmax of muon
  float fCutValueMaxMuonPt;
  /// Collection of excluded muons
  std::vector<const reco::Muon*> fExcludedMuons;
  
  // Counter ID's
  /// IDs of the event counters
  int fGlobalMuonVetoInput;
  int fPassedGlobalMuonVeto;
  int fMuonCollectionHandleEmpty;
  int fAllMuonCandidates;
  int fAfterExcludedMuons;
  int fAfterTrackRefNonNull;
  int fFailedPtCut;
  // Histograms
  /// Maximum muon pT in event (-1 if no muon in event)
  TH1F* hMuonMaxPt;
  /// eta of muon with highest pT in event (-4 if no muon in event)
  TH1F* hMuonEtaofHighest;
  /// pT of all muons (could be 0 or more per event)
  TH1F* hMuonPtAllMuons;
  /// eta of all muons (could be 0 or more per event)
  TH1F* hMuonEtaAllMuons;
};

//}

#endif
