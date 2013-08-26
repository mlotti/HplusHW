#ifndef HPLUSTAUDUMPERPF_H
#define HPLUSTAUDUMPERPF_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTauDumperBase.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoBTag/SecondaryVertex/interface/SecondaryVertex.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

/**
Class for dumping the relevant PF tau information to a root file

	@author Alexandros Attikis, Lauri Wendland
*/

namespace HPlusAnalysis {

class HPlusTauDumperPF : public HPlusTauDumperBase {
 public:
  /// Default constructor (takes a pointer to the ROOT tree object containing the data)
  HPlusTauDumperPF(edm::EDProducer& producer, edm::ParameterSet& aTauCollectionParameterSet,
                   Counter* counter);
  /// Default destructor
  ~HPlusTauDumperPF();

  typedef reco::Candidate::LorentzVector LorentzVector; // can be saved to edm 

  /// Sets the data specific to this tau collection; returns true if something was saved
  bool setData(edm::Event& iEvent, const edm::EventSetup& iSetup);
  reco::Vertex threeProng(reco::PFTauRef myPFTau, edm::Event& myEvent, const edm::EventSetup& myEvtSetup);
  reco::Vertex fiveProng(reco::PFTauRef myPFTau, edm::Event& myEvent, const edm::EventSetup& myEvtSetup); 

 private:
  // counters
  int fCounter0pr; // Counter for 0-prong PFTaus (no selection cuts)
  int fCounter1pr; // Counter for 1-prong PFTaus (no selection cuts)
  int fCounter2pr; // Counter for 2-prong PFTaus (no selection cuts)
  int fCounter3pr; // Counter for 3-prong PFTaus (no selection cuts)
  int fCounterXpr; // Counter for Any-prong PFTaus (no selection cuts)
  int fCounterPFelectronsSignalCone;   // Counter for PFelectrons found inside signal cone (no selection cuts)
  int fCounterPFNeutHadrsSignalCone;   // Counter for PFNeutralHadrons found inside signal cone (no selection cuts)
  int fCounterPFelectronsIsolCone;     // Counter for PFelectrons found inside isolation cone (no selection cuts)
  int fCounterPFNeutHadrsIsolCone;     // Counter for PFNeutralHadrons found inside isolation cone (no selection cuts)
};

}

#endif
