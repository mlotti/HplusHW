#include "Branches.h"

#include<iostream>

//////////////////// EventInfo ////////////////////
EventInfo::EventInfo() {}
EventInfo::~EventInfo() {}

void EventInfo::setupBranches(TTree *tree) {
  fEvent.setupBranch(tree, "event");
  fLumi.setupBranch(tree, "lumi");
  fRun.setupBranch(tree, "run");
}


//////////////////// MuonCollection ////////////////////
MuonCollection::Muon::Muon(MuonCollection *mc, size_t i):
  fCollection(mc), fIndex(i)
{}
MuonCollection::Muon::~Muon() {}

MuonCollection::MuonCollection(const std::string prefix):
  fPrefix(prefix)
{}
MuonCollection::~MuonCollection() {}

void MuonCollection::setupBranches(TTree *tree, bool isMC) {
  fP4.setupBranch(tree, (fPrefix+"_p4").c_str());
  fDB.setupBranch(tree, (fPrefix+"_f_dB").c_str());

  fTrackIso.setupBranch(tree, (fPrefix+"_f_trackIso").c_str());
  fCaloIso.setupBranch(tree, (fPrefix+"_f_caloIso").c_str());

  fChargedHadronIso.setupBranch(tree, (fPrefix+"_f_chargedHadronIso").c_str());
  fPuChargedHadronIso.setupBranch(tree, (fPrefix+"_f_puChargedHadronIso").c_str());
  fNeutralHadronIso.setupBranch(tree, (fPrefix+"_f_neutralHadronIso").c_str());
  fPhotonIso.setupBranch(tree, (fPrefix+"_f_photonIso").c_str());

  if(isMC) {
    fPdgId.setupBranch(tree, (fPrefix+"_pdgid").c_str());
    fMotherPdgId.setupBranch(tree, (fPrefix+"_mother_pdgid").c_str());
    fGrandMotherPdgId.setupBranch(tree, (fPrefix+"_grandmother_pdgid").c_str());
  }
}

//////////////////// EmbeddingMuonCollection ////////////////////
EmbeddingMuonCollection::Muon::Muon(EmbeddingMuonCollection *mc, size_t i): MuonCollection::Muon(mc, i) {}
EmbeddingMuonCollection::Muon::~Muon() {}
EmbeddingMuonCollection::EmbeddingMuonCollection(const std::string& postfix): fPostfix(postfix) {}
EmbeddingMuonCollection::~EmbeddingMuonCollection() {}
void EmbeddingMuonCollection::setupBranches(TTree *tree, bool isMC) {
  MuonCollection::setupBranches(tree, isMC);

  fChargedHadronIsoEmb.setupBranch(tree, (fPrefix+"_f_chargedHadronIso"+fPostfix).c_str());
  fPuChargedHadronIsoEmb.setupBranch(tree, (fPrefix+"_f_puChargedHadronIso"+fPostfix).c_str());
  fNeutralHadronIsoEmb.setupBranch(tree, (fPrefix+"_f_neutralHadronIso"+fPostfix).c_str());
  fPhotonIsoEmb.setupBranch(tree, (fPrefix+"_f_photonIso"+fPostfix).c_str());
}


//////////////////// ElectronCollection ////////////////////
ElectronCollection::Electron::Electron(ElectronCollection *mc, size_t i):
  fCollection(mc), fIndex(i)
{}
ElectronCollection::Electron::~Electron() {}

ElectronCollection::ElectronCollection(const std::string prefix):
  fPrefix(prefix)
{}
ElectronCollection::~ElectronCollection() {}

void ElectronCollection::setupBranches(TTree *tree, bool isMC) {
  fP4.setupBranch(tree, (fPrefix+"_p4").c_str());

  fHasGsfTrack.setupBranch(tree, (fPrefix+"_hasGsfTrack").c_str());
  fHasSuperCluster.setupBranch(tree, (fPrefix+"_hasSuperCluster").c_str());
  fCutBasedIdVeto.setupBranch(tree, (fPrefix+"_cutBasedIdVeto").c_str());
  fCutBasedIdLoose.setupBranch(tree, (fPrefix+"_cutBasedIdLoose").c_str());
  fCutBasedIdMedium.setupBranch(tree, (fPrefix+"_cutBasedIdMedium").c_str());
  fCutBasedIdTight.setupBranch(tree, (fPrefix+"_cutBasedIdTight").c_str());

  fSuperClusterEta.setupBranch(tree, (fPrefix+"_f_superClusterEta").c_str());

  if(isMC) {
    fPdgId.setupBranch(tree, (fPrefix+"_pdgid").c_str());
    fMotherPdgId.setupBranch(tree, (fPrefix+"_mother_pdgid").c_str());
    fGrandMotherPdgId.setupBranch(tree, (fPrefix+"_grandmother_pdgid").c_str());
  }
}

//////////////////// JetCollection ////////////////////
JetCollection::Jet::Jet(JetCollection *mc, size_t i): 
  fCollection(mc), fIndex(i)
{}
JetCollection::Jet::~Jet() {}

JetCollection::JetCollection(const std::string prefix):
  fPrefix(prefix)
{}
JetCollection::~JetCollection() {}

void JetCollection::setupBranches(TTree *tree) {
  fP4.setupBranch(tree, (fPrefix+"_p4").c_str());
  fNumberOfDaughters.setupBranch(tree, (fPrefix+"_numberOfDaughters").c_str());
  fLooseId.setupBranch(tree, (fPrefix+"_looseId").c_str());
  fTightId.setupBranch(tree, (fPrefix+"_tightId").c_str());
}

//////////////////// JetDetailsCollection ////////////////////
JetDetailsCollection::Jet::Jet(JetDetailsCollection *jdc, size_t i): JetCollection::Jet(jdc, i) {}
JetDetailsCollection::Jet::~Jet() {}
JetDetailsCollection::JetDetailsCollection(const std::string prefix): JetCollection(prefix) {}
JetDetailsCollection::~JetDetailsCollection() {}
void JetDetailsCollection::setupBranches(TTree *tree) {
  fChm.setupBranch(tree, (fPrefix+"_chm").c_str());
  fNhm.setupBranch(tree, (fPrefix+"_nhm").c_str());
  fElm.setupBranch(tree, (fPrefix+"_elm").c_str());
  fPhm.setupBranch(tree, (fPrefix+"_phm").c_str());
  fMum.setupBranch(tree, (fPrefix+"_mum").c_str());
  fChf.setupBranch(tree, (fPrefix+"_chf").c_str());
  fNhf.setupBranch(tree, (fPrefix+"_nhf").c_str());
  fElf.setupBranch(tree, (fPrefix+"_elf").c_str());
  fPhf.setupBranch(tree, (fPrefix+"_phf").c_str());
  fMuf.setupBranch(tree, (fPrefix+"_muf").c_str());
}

//////////////////// TauCollection ////////////////////
TauCollection::Tau::Tau(TauCollection *mc, size_t i):
  fCollection(mc), fIndex(i)
{}
TauCollection::Tau::~Tau() {}

TauCollection::TauCollection(const std::string prefix):
  fPrefix(prefix)
{}
TauCollection::~TauCollection() {}

void TauCollection::setupBranches(TTree *tree) {
  fP4.setupBranch(tree, (fPrefix+"_p4").c_str());
  fLeadPFChargedHadrCandP4.setupBranch(tree, (fPrefix+"_leadPFChargedHadrCand_p4").c_str());
  fSignalPFChargedHadrCandsCount.setupBranch(tree, (fPrefix+"_signalPFChargedHadrCands_n").c_str());
  fDecayMode.setupBranch(tree, (fPrefix+"_decayMode").c_str());

  fDecayModeFinding.setupBranch(tree, (fPrefix+"_f_decayModeFinding").c_str());
  fAgainstMuonTight.setupBranch(tree, (fPrefix+"_f_againstMuonTight").c_str());
  fAgainstElectronLoose.setupBranch(tree, (fPrefix+"_f_againstElectronLoose").c_str());
  fAgainstElectronMedium.setupBranch(tree, (fPrefix+"_f_againstElectronMedium").c_str());
  fAgainstElectronTight.setupBranch(tree, (fPrefix+"_f_againstElectronTight").c_str());
  fAgainstElectronMVA.setupBranch(tree, (fPrefix+"_f_againstElectronMVA").c_str());
  fMediumCombinedIsolationDeltaBetaCorr.setupBranch(tree, (fPrefix+"_f_byMediumCombinedIsolationDeltaBetaCorr").c_str());
}
