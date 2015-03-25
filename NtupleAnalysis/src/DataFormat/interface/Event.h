// -*- c++ -*-
#ifndef DataFormat_Event_h
#define DataFormat_Event_h

#include "Framework/interface/ParameterSet.h"
#include "Tools/interface/BooleanOr.h"

#include "DataFormat/interface/EventID.h"
#include "DataFormat/interface/EventNPU.h"
#include "DataFormat/interface/Tau.h"
#include "DataFormat/interface/Jet.h"
#include "DataFormat/interface/GenJet.h"
#include "DataFormat/interface/Electron.h"
#include "DataFormat/interface/Muon.h"
#include "DataFormat/interface/MET.h"
#include "DataFormat/interface/GenParticle.h"

class BranchManager;

class Event {
public:
  explicit Event(const ParameterSet& config);
  ~Event();

  void setupBranches(BranchManager& mgr);

  bool isMC() const { return fIsMC; }
  bool isData() const { return !fIsMC; }

  bool configurableTriggerDecision() const {
    return fTriggerOr.value();
  }
  bool configurableTriggerDecision2() const {
    return fTriggerOr2.value();
  }
  const EventID& eventID() const { return fEventID; }
  const EventNPU& NPU() const { return fNPU; }
  const TauCollection& taus() const { return fTauCollection; }
  const JetCollection& jets() const { return fJetCollection; }
  const GenJetCollection& genjets() const { return fGenJetCollection; }
  const ElectronCollection& electrons() const { return fElectronCollection; }
  const MuonCollection& muons() const { return fMuonCollection; }
  const GenParticleCollection& genparticles() const { return fGenParticleCollection; }

  const MET& genMET() const { return fGenMET; }

  const MET& met() const { return met_Type1(); }
  const MET& met_Type1() const { return fMET_Type1; }

private:
  EventID fEventID;

  EventNPU fNPU;

  BooleanOr fTriggerOr;
  BooleanOr fTriggerOr2;

  TauCollection fTauCollection;
  JetCollection fJetCollection;
  GenJetCollection fGenJetCollection;
  ElectronCollection fElectronCollection;
  MuonCollection fMuonCollection;
  MET fGenMET;
  MET fMET_Type1;
  GenParticleCollection fGenParticleCollection;

  const bool fIsMC;
};

#endif
