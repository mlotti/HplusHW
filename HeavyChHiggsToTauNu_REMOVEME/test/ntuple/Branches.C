#include "Branches.h"

#include<limits>
#include<iostream>
#include<stdexcept>

//////////////////// EventInfo ////////////////////
EventInfo::EventInfo() {}
EventInfo::~EventInfo() {}

void EventInfo::setupBranches(BranchManager& branchManager) {
  branchManager.book("event", &fEvent);
  branchManager.book("lumi", &fLumi);
  branchManager.book("run", &fRun);
}

//////////////////// Particle ////////////////////

namespace Impl {
  ParticleBase::ParticleBase(): fIndex(std::numeric_limits<size_t>::max()) {}
  ParticleBase::~ParticleBase() {}
}

//////////////////// MuonCollection ////////////////////
MuonCollection::Muon::~Muon() {}
void MuonCollection::Muon::ensureValidity() const {
  if(!isValid())
    throw std::logic_error("Muon is not valid (fCollection is NULL)");
}
void MuonCollection::Muon::assignP4() {
  if(correctedP4().Pt() < 200 && std::sqrt(tunePP3().Perp2()) < 200) {
    setP4(correctedP4());
    fCorrectionType = kCorrected;
  }
  else {
    math::XYZTLorentzVector p = correctedP4();
    p.SetPx(tunePP3().X());
    p.SetPy(tunePP3().Y());
    p.SetPz(tunePP3().Z());
    setP4(p);
    fCorrectionType = kTuneP;
  }
}

MuonCollection::MuonCollection(const std::string prefix):
  fPrefix(prefix)
{}
MuonCollection::~MuonCollection() {}

void MuonCollection::setupBranches(BranchManager& branchManager, bool isMC) {
  branchManager.book(fPrefix+"_p4", &fP4);
  branchManager.book(fPrefix+"_correctedP4", &fCorrectedP4);

  branchManager.book(fPrefix+"_tunePP3", &fTunePP3);
  branchManager.book(fPrefix+"_tunePPtError", &fTunePPtError);

  branchManager.book(fPrefix+"_charge", &fCharge);
  branchManager.book(fPrefix+"_f_dB", &fDB);
  branchManager.book(fPrefix+"_globalTrack_normalizedChi2", &fNormalizedChi2);

  branchManager.book(fPrefix+"_f_trackIso", &fTrackIso);
  branchManager.book(fPrefix+"_f_caloIso", &fCaloIso);

  branchManager.book(fPrefix+"_f_chargedHadronIso", &fChargedHadronIso);
  branchManager.book(fPrefix+"_f_puChargedHadronIso", &fPuChargedHadronIso);
  branchManager.book(fPrefix+"_f_neutralHadronIso", &fNeutralHadronIso);
  branchManager.book(fPrefix+"_f_photonIso", &fPhotonIso);

  if(!fIdEfficiencyName.empty()) {
    branchManager.book(fPrefix+"_"+fIdEfficiencyName, &fIdEfficiency);
  }
  if(!fTriggerEfficiencyName.empty()) {
    branchManager.book(fPrefix+"_"+fIdEfficiencyName, &fTriggerEfficiency);
  }

  branchManager.book(fPrefix+"_triggerMatched", &fTriggerMatched);

  if(isMC) {
    branchManager.book(fPrefix+"_genmatch_p4", &fGenMatchP4);
    branchManager.book(fPrefix+"_genmatch_pdgid", &fPdgId);
    branchManager.book(fPrefix+"_genmatch_mother_pdgid", &fMotherPdgId);
    branchManager.book(fPrefix+"_genmatch_grandmother_pdgid", &fGrandMotherPdgId);
  }
}

//////////////////// EmbeddingMuonCollection ////////////////////
EmbeddingMuonCollection::Muon::Muon(): MuonCollection::Muon() {}
EmbeddingMuonCollection::Muon::Muon(EmbeddingMuonCollection *mc, size_t i): MuonCollection::Muon(mc, i) {}
EmbeddingMuonCollection::Muon::~Muon() {}
EmbeddingMuonCollection::EmbeddingMuonCollection(const std::string& postfix): fPostfix(postfix) {}
EmbeddingMuonCollection::~EmbeddingMuonCollection() {}
void EmbeddingMuonCollection::setupBranches(BranchManager& branchManager, bool isMC) {
  MuonCollection::setupBranches(branchManager, isMC);

  branchManager.book(fPrefix+"_f_chargedHadronIso", &fChargedHadronIsoEmb);
  branchManager.book(fPrefix+"_f_puChargedHadronIso", &fPuChargedHadronIsoEmb);
  branchManager.book(fPrefix+"_f_neutralHadronIso", &fNeutralHadronIsoEmb);
  branchManager.book(fPrefix+"_f_photonIso", &fPhotonIsoEmb);
}


//////////////////// ElectronCollection ////////////////////
ElectronCollection::Electron::~Electron() {}

ElectronCollection::ElectronCollection(const std::string prefix):
  fPrefix(prefix)
{}
ElectronCollection::~ElectronCollection() {}

void ElectronCollection::setupBranches(BranchManager& branchManager, bool isMC) {
  branchManager.book(fPrefix+"_p4", &fP4);

  branchManager.book(fPrefix+"_hasGsfTrack", &fHasGsfTrack     );
  branchManager.book(fPrefix+"_hasSuperCluster", &fHasSuperCluster );
  branchManager.book(fPrefix+"_cutBasedIdVeto", &fCutBasedIdVeto  );
  branchManager.book(fPrefix+"_cutBasedIdLoose", &fCutBasedIdLoose );
  branchManager.book(fPrefix+"_cutBasedIdMedium", &fCutBasedIdMedium);
  branchManager.book(fPrefix+"_cutBasedIdTight", &fCutBasedIdTight );

  branchManager.book(fPrefix+"_f_superClusterEta", &fSuperClusterEta);

  if(isMC) {
    branchManager.book(fPrefix+"_genmatch_p4", &fGenMatchP4);
    branchManager.book(fPrefix+"_genmatch_pdgid", &fPdgId);
    branchManager.book(fPrefix+"_genmatch_mother_pdgid", &fMotherPdgId);
    branchManager.book(fPrefix+"_genmatch_grandmother_pdgid", &fGrandMotherPdgId);
  }
}

//////////////////// JetCollection ////////////////////
JetCollection::Jet::~Jet() {}

JetCollection::JetCollection(const std::string prefix):
  fPrefix(prefix)
{}
JetCollection::~JetCollection() {}

void JetCollection::setupBranches(BranchManager& branchManager) {
  branchManager.book(fPrefix+"_p4", &fP4);
  branchManager.book(fPrefix+"_numberOfDaughters", &fNumberOfDaughters);
  branchManager.book(fPrefix+"_looseId", &fLooseId);
  branchManager.book(fPrefix+"_tightId", &fTightId);
  branchManager.book(fPrefix+"_f_csv", &fCSV);
  branchManager.book(fPrefix+"_btagged", &fBTagged);
  branchManager.book(fPrefix+"_btagScaleFactor", &fBTagSF);
  branchManager.book(fPrefix+"_btagScaleFactorUncertainty", &fBTagSFUnc);
}

//////////////////// JetDetailsCollection ////////////////////
JetDetailsCollection::Jet::Jet(JetDetailsCollection *jdc, size_t i): JetCollection::Jet(jdc, i) {}
JetDetailsCollection::Jet::~Jet() {}
JetDetailsCollection::JetDetailsCollection(const std::string prefix): JetCollection(prefix) {}
JetDetailsCollection::~JetDetailsCollection() {}
void JetDetailsCollection::setupBranches(BranchManager& branchManager) {
  branchManager.book(fPrefix+"_chm", &fChm);
  branchManager.book(fPrefix+"_nhm", &fNhm);
  branchManager.book(fPrefix+"_elm", &fElm);
  branchManager.book(fPrefix+"_phm", &fPhm);
  branchManager.book(fPrefix+"_mum", &fMum);
  branchManager.book(fPrefix+"_chf", &fChf);
  branchManager.book(fPrefix+"_nhf", &fNhf);
  branchManager.book(fPrefix+"_elf", &fElf);
  branchManager.book(fPrefix+"_phf", &fPhf);
  branchManager.book(fPrefix+"_muf", &fMuf);
}

//////////////////// TauCollection ////////////////////
TauCollection::Tau::~Tau() {}

TauCollection::TauCollection(const std::string prefix):
  fPrefix(prefix)
{}
TauCollection::~TauCollection() {}

void TauCollection::setupBranches(BranchManager& branchManager, bool isMC) {
  branchManager.book(fPrefix+"_p4", &fP4);
  branchManager.book(fPrefix+"_leadPFChargedHadrCand_p4", &fLeadPFChargedHadrCandP4);
  branchManager.book(fPrefix+"_signalPFChargedHadrCands_n", &fSignalPFChargedHadrCandsCount);
  branchManager.book(fPrefix+"_decayMode", &fDecayMode);

  branchManager.book(fPrefix+"_f_decayModeFinding", &fDecayModeFinding);
  branchManager.book(fPrefix+"_f_againstMuonTight", &fAgainstMuonTight);
  branchManager.book(fPrefix+"_f_againstMuonTight2", &fAgainstMuonTight2);
  branchManager.book(fPrefix+"_f_againstElectronLoose", &fAgainstElectronLoose);
  branchManager.book(fPrefix+"_f_againstElectronMedium", &fAgainstElectronMedium);
  branchManager.book(fPrefix+"_f_againstElectronTight", &fAgainstElectronTight);
  branchManager.book(fPrefix+"_f_againstElectronMVA", &fAgainstElectronMVA);
  branchManager.book(fPrefix+"_f_againstElectronTightMVA3", &fAgainstElectronTightMVA3);
  branchManager.book(fPrefix+"_f_byMediumCombinedIsolationDeltaBetaCorr", &fMediumCombinedIsolationDeltaBetaCorr);
  branchManager.book(fPrefix+"_f_byMediumCombinedIsolationDeltaBetaCorr3Hits", &fMediumCombinedIsolationDeltaBetaCorr3Hits);

  if(isMC) {
    branchManager.book(fPrefix+"_genmatch_p4", &fGenMatchP4);
    branchManager.book(fPrefix+"_genmatch_visible_p4", &fGenMatchVisibleP4);
    branchManager.book(fPrefix+"_genmatch_pdgid", &fPdgId);
    branchManager.book(fPrefix+"_genmatch_mother_pdgid", &fMotherPdgId);
    branchManager.book(fPrefix+"_genmatch_grandmother_pdgid", &fGrandMotherPdgId);
    branchManager.book(fPrefix+"_genmatch_daughter_pdgid", &fDaughterPdgId);
  }
}

//////////////////// GenParticleCollection ////////////////////
GenParticleCollection::GenParticle::GenParticle():  Base(0, std::numeric_limits<size_t>::max()) {}
GenParticleCollection::GenParticle::~GenParticle() {}

GenParticleCollection::GenParticleCollection(const std::string& prefix, bool isTau):
  fPrefix(prefix), fIsTau(isTau)
{}
GenParticleCollection::~GenParticleCollection() {}

void GenParticleCollection::setupBranches(BranchManager& branchManager) {
  branchManager.book(fPrefix+"_p4", &fP4);
  branchManager.book(fPrefix+"_pdgid", &fPdgId);
  branchManager.book(fPrefix+"_mother_pdgid", &fMotherPdgId);
  branchManager.book(fPrefix+"_grandmother_pdgid", &fGrandMotherPdgId);

  if(fIsTau) {
    branchManager.book(fPrefix+"_daughter_pdgid", &fDaughterPdgId);
    branchManager.book(fPrefix+"_visible_p4", &fVisibleP4);
  }
}
