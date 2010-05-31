#ifndef HPLUSANALYSISGLOBALMUONVETO_H
#define HPLUSANALYSISGLOBALMUONVETO_H

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

namespace HPlusAnalysis {

/**
Class for applying global muon veto, i.e. loop over all muons in the event
and reject the event, if any muon has pT greater than the cut value.

This selection method is aimed against the W->mu nu and W->tau nu->mu nu nu
decays, which might spoil the MET measurement for the fully hadronic
H+ -> tau nu decay channel 

	@author Lauri Wendland, Ritva Kinnunen
*/
class GlobalMuonVeto : public HPlusAnalysisBase, public HPlusSelectionBase {
 public:
  /// Default constructor
  GlobalMuonVeto();
  /// Default destructor
  ~GlobalMuonVeto();
  
  /// Method for parsing all necessary configuration things 
  void setup(const edm::ParameterSet& iConfig);
  /// Method for setting ROOT tree branches
  void setRootTreeBranches(TTree& tree);
  /// Applies the trigger selection; returns true if trigger was passed
  bool apply(const edm::Event& iEvent);
  /// Method for filling ROOT tree branches with data
  void fillRootTreeData(TTree& tree);
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
  int fPassedGlobalMuonVeto;

  int fAllMuonCandidates;
  int fAfterExcludedMuons;
  int fAfterTrackRefNonNull;
  int fFailedPtCut;
  // Values to be saved in ROOT tree or histograms
  /// pTmax of all reconstructed muons
  float fMaxMuonPt;
  /// Collection of valid global muon tracks for histogramming
  std::vector<reco::TrackRef> fMuonTracks;
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

}

#endif
