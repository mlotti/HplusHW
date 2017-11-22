#include "DataFormat/interface/Event.h"

#include "boost/optional.hpp"

#include <stdexcept>

Event::Event(const ParameterSet& config):
  fJetCollection(config.getParameter<std::string>("JetSelection.jetType", "Jets")),
  fGenMET("GenMET"),
  fMET_Type1("MET_Type1"),
  fMET(config.getParameter<std::string>("METSelection.METType", "MET_Type1")),
  fCaloMET("CaloMET"),
  fL1MET("L1MET_pat"),
  fL1extraMET("L1MET_l1extra"),
  fGenWeight("GenWeight"),
  fTopPtWeight("topPtWeight"),
  fIsMC(config.isMC())
{
  // Trigger
  boost::optional<float> fL1ETM = config.getParameterOptional<float>("Trigger.L1ETM");
  fL1ETMThreshold = 0;
  if(fL1ETM) fL1ETMThreshold = static_cast<float>(*fL1ETM);
  boost::optional<std::vector<std::string>> triggerOR = config.getParameterOptional<std::vector<std::string>>("Trigger.triggerOR", std::vector<std::string>{});
  if(triggerOR) {
    if (triggerOR->size())
      fTriggerOr.setBranchNames(*triggerOR);
  }
  boost::optional<std::vector<std::string>> triggerOR2 = config.getParameterOptional<std::vector<std::string>>("Trigger.triggerOR2", std::vector<std::string>{});
  if(triggerOR2) {
    if (triggerOR2->size())
      fTriggerOr2.setBranchNames(*triggerOR2);
  }
 
  bool variationAssigned = false;
  // Systematics
  boost::optional<std::string> jetSyst = config.getParameterOptional<std::string>("JetSelection.systematicVariation");
  if(jetSyst) {
    fJetCollection.setEnergySystematicsVariation(*jetSyst);
    fMET_Type1.setEnergySystematicsVariation(*jetSyst);
    variationAssigned = true;
  }

  boost::optional<std::string> tauSyst = config.getParameterOptional<std::string>("TauSelection.systematicVariation");
  if(tauSyst) {
    if(variationAssigned) {
      throw std::runtime_error("Trying to set systematicVariation for taus, but a variation has already been set for jets! Only one variation per analyzer is allowed");
    }
    fTauCollection.setEnergySystematicsVariation(*tauSyst);
    fMET_Type1.setEnergySystematicsVariation(*tauSyst);
    variationAssigned = true;
  }

  // MET filter discriminators
  boost::optional<std::vector<std::string> > metFilterDiscr = config.getParameterOptional<std::vector<std::string> >("METFilter.discriminators", std::vector<std::string>{});
  if (metFilterDiscr) {
    fMETFilter.setConfigurableDiscriminators(*metFilterDiscr);
  }
  
  // Tau discriminators
  boost::optional<std::vector<std::string> > tauDiscr = config.getParameterOptional<std::vector<std::string> >("TauSelection.discriminators", std::vector<std::string>{});
  if(tauDiscr) {
    fTauCollection.setConfigurableDiscriminators(*tauDiscr);
  }
  boost::optional<std::string> tauAgainstElectronDiscr = config.getParameterOptional<std::string>("TauSelection.againstElectronDiscr");
  if (tauAgainstElectronDiscr)
    fTauCollection.setAgainstElectronDiscriminator(*tauAgainstElectronDiscr);
  boost::optional<std::string> tauAgainstMuonDiscr = config.getParameterOptional<std::string>("TauSelection.againstMuonDiscr");
  if (tauAgainstMuonDiscr)
    fTauCollection.setAgainstMuonDiscriminator(*tauAgainstMuonDiscr);
  boost::optional<std::string> tauIsolationDiscr = config.getParameterOptional<std::string>("TauSelection.isolationDiscr");
  if (tauIsolationDiscr)
    fTauCollection.setIsolationDiscriminator(*tauIsolationDiscr);
  
  // Muon discriminators
  boost::optional<std::string> muIDDiscr = config.getParameterOptional<std::string>("MuonSelection.muonID");
  if (muIDDiscr)
    fMuonCollection.setMuonIDDiscriminator(*muIDDiscr);
  
  // Electron discriminators
  boost::optional<std::string> eIDDiscr = config.getParameterOptional<std::string>("ElectronSelection.electronID");
  if (eIDDiscr)
    fElectronCollection.setElectronIDDiscriminator(*eIDDiscr);
  
  // Jet discriminators
  boost::optional<std::string> jetIDDiscr = config.getParameterOptional<std::string>("JetSelection.jetIDDiscr");
  if (jetIDDiscr)
    fJetCollection.setJetIDDiscriminator(*jetIDDiscr);
  boost::optional<std::string> jetPUIDDiscr = config.getParameterOptional<std::string>("JetSelection.jetPUIDDiscr");
  if (jetPUIDDiscr)
    fJetCollection.setJetPUIDDiscriminator(*jetPUIDDiscr);

  // B jet discriminators
  boost::optional<std::string> bjetDiscr = config.getParameterOptional<std::string>("BJetSelection.bjetDiscr");
  if (bjetDiscr)
    fJetCollection.setBJetDiscriminator(*bjetDiscr);
  
}

Event::~Event() {}

void Event::setupBranches(BranchManager& mgr) {
  fEventID.setupBranches(mgr);

  fVertexInfo.setupBranches(mgr);
  fMETFilter.setupBranches(mgr);

  fTriggerOr.setupBranchesAutoScanVersion(mgr);
  fTriggerOr2.setupBranchesAutoScanVersion(mgr);

  fL1TauCollection.setupBranches(mgr);
  fL1IsoTauCollection.setupBranches(mgr);
  fL1JetCollection.setupBranches(mgr);
  fTriggerTauCollection.setupBranches(mgr);
  fTriggerBJetCollection.setupBranches(mgr);
  fTauCollection.setupBranches(mgr);
  fJetCollection.setupBranches(mgr);
  fGenJetCollection.setupBranches(mgr);
  fMuonCollection.setupBranches(mgr);
  fElectronCollection.setupBranches(mgr);
  fGenParticleCollection.setupBranches(mgr);
  fGenMET.setupBranches(mgr);
  fGenWeight.setupBranches(mgr);
  fTopPtWeight.setupBranches(mgr);
  fMET_Type1.setupBranches(mgr);
  fMET.setupBranches(mgr);
  fCaloMET.setupBranches(mgr);
  fL1MET.setupBranches(mgr);
  fL1extraMET.setupBranches(mgr);
  fPFCandidates.setupBranches(mgr);
}
