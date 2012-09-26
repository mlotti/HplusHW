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
    fMotherPdgId.setupBranch(tree, (fPrefix+"_grandmother_pdgid").c_str());
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
}
