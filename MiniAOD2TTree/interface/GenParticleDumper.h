#ifndef GenParticleDumper_h
#define GenParticleDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include <string>
#include <vector>

#include "TTree.h"

#include "DataFormats/Math/interface/LorentzVector.h"

#include "HiggsAnalysis/MiniAOD2TTree/interface/BaseDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/FourVectorDumper.h"

class GenParticleDumper : public BaseDumper {
public:
  GenParticleDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets);
  ~GenParticleDumper();

  void book(TTree*);
  bool fill(edm::Event&, const edm::EventSetup&);
  void reset();
   
private:
  bool filter();
  /// Saves lepton four-momenta
  void saveLeptons(edm::Handle<reco::GenParticleCollection>& handle, FourVectorDumper& dumper, int pID);
  /// Saves tau helicity related information
  void saveHelicityInformation(math::XYZTLorentzVector& visibleTau, const std::vector<const reco::Candidate*>& offspring, const size_t index);
  /// Prints the descendants
  void printDescendants(edm::Handle<reco::GenParticleCollection>& handle, const reco::Candidate* p);
  
private:  
  //edm::Handle<reco::GenParticleCollection> *handle;
  edm::EDGetTokenT<reco::GenParticleCollection> *token;
  
  // General particle list
  std::vector<int> *collisionId;
  // std::vector<short> *mother;
  std::vector< std::vector<short> > *mothers;
  std::vector< std::vector<short> > *daughters;

  // Booleans
  std::vector<bool> *fromHardProcessBeforeFSR;
  std::vector<bool> *fromHardProcessDecayed;
  std::vector<bool> *fromHardProcessFinalState;
  std::vector<bool> *isDirectHardProcessTauDecayProductFinalState;
  std::vector<bool> *isDirectPromptTauDecayProductFinalState;
  std::vector<bool> *isHardProcess;
  std::vector<bool> *isLastCopy;
  std::vector<bool> *isLastCopyBeforeFSR;
  // std::vector<bool> *isMostlyLikePythia6Status3;
  std::vector<bool> *isPromptDecayed;
  std::vector<bool> *isPromptFinalState;

  // Flags
  std::vector<bool> *fromHardProcess;
  std::vector<bool> *isDecayedLeptonHadron;
  std::vector<bool> *isDirectHadronDecayProduct;
  std::vector<bool> *isDirectHardProcessTauDecayProduct;
  std::vector<bool> *isDirectPromptTauDecayProduct;
  std::vector<bool> *isDirectTauDecayProduct;
  std::vector<bool> *isFirstCopy;
  std::vector<bool> *isHardProcessTauDecayProduct;
  std::vector<bool> *isPrompt;
  std::vector<bool> *isPromptTauDecayProduct;
  std::vector<bool> *isTauDecayProduct;

  // MC electrons
  FourVectorDumper *electrons;
  
  // MC muons
  FourVectorDumper *muons;
  
  // MC taus
  FourVectorDumper *taus;
  FourVectorDumper *visibleTaus;
  std::vector<short> *tauNcharged;
  std::vector<short> *tauNPi0;
  std::vector<double> *tauRtau;
  short *tauAssociatedWithHpm;
  std::vector<short> *tauMother;
  std::vector<bool> *tauDecaysToElectron;
  std::vector<bool> *tauDecaysToMuon;
  std::vector<double> *tauSpinEffects;
  FourVectorDumper *tauNeutrinos;
  
  // Neutrinos
  FourVectorDumper *neutrinos;
  
  // Top info
  FourVectorDumper *top;
  std::vector<short> *topDecayMode;
  FourVectorDumper *topBQuark;
  std::vector<bool> *topBJetContainsLeptons;
  FourVectorDumper *topBNeutrinos;
  
  // W info
  FourVectorDumper *W;
  std::vector<short> *WDecayMode;
  FourVectorDumper *WNeutrinos;
  
  // H+ info
  FourVectorDumper *Hplus;
  FourVectorDumper *HplusNeutrinos;
};
#endif
