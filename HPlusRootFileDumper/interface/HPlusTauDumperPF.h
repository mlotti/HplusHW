#ifndef HPLUSTAUDUMPERPF_H
#define HPLUSTAUDUMPERPF_H

#include "HiggsAnalysis/HPlusRootFileDumper/interface/HPlusTauDumperBase.h"

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
  
  bool refitThreeProng(reco::PFTauRef myPFTau, const edm::EventSetup& myEvtSetup); // method taken from HPSPFRecoTauAlgorithm
  bool refitFiveProng(reco::PFTauRef myPFTau, const edm::EventSetup& myEvtSetup); // method taken from HPSPFRecoTauAlgorithm
  
 private:
  int fCounterTest;
  int fCounter0pr; // FIXME: Please change name to more descriptive for self-documenting purposes
  int fCounter1pr;
  int fCounter2pr;
  int fCounter3pr;
  int fCounterXpr;
  int fCounterPFelectronsSignalCone;
  int fCounterPFNeutHadrsSignalCone;
  int fCounterPFelectronsIsolCone;
  int fCounterPFNeutHadrsIsolCone; 
};

}

#endif
