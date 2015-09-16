// -*- c++ -*-
#ifndef DataFormat_Event_h
#define DataFormat_Event_h

#include "Framework/interface/ParameterSet.h"
#include "Tools/interface/BooleanOr.h"

#include "DataFormat/interface/EventID.h"
#include "DataFormat/interface/VertexInfo.h"
#include "DataFormat/interface/METFilter.h"
#include "DataFormat/interface/HLTTau.h"
#include "DataFormat/interface/Tau.h"
#include "DataFormat/interface/Jet.h"
#include "DataFormat/interface/GenJet.h"
#include "DataFormat/interface/Electron.h"
#include "DataFormat/interface/Muon.h"
#include "DataFormat/interface/MET.h"
#include "DataFormat/interface/GenWeight.h"
#include "DataFormat/interface/GenParticle.h"
#include "DataFormat/interface/PFCands.h"

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
  bool configurableTriggerIsEmpty() const {
    return fTriggerOr.isEmpty();
  }
  bool configurableTrigger2IsEmpty() const {
    return fTriggerOr2.isEmpty();
  }
  bool passTriggerDecision() const {
    if (configurableTriggerIsEmpty() && configurableTrigger2IsEmpty())
      return true;
    if (configurableTrigger2IsEmpty())
      return configurableTriggerDecision();
    return configurableTriggerDecision() || configurableTriggerDecision2();
  }
  
  const EventID& eventID() const { return fEventID; }
  const VertexInfo& NPU() const { return fNPU; }
  const METFilter& metFilter() const { return fMETFilter; }
  const HLTTauCollection& triggerTaus() const { return fTriggerTauCollection; }
  const TauCollection& taus() const { return fTauCollection; }
  const JetCollection& jets() const { return fJetCollection; }
  const GenJetCollection& genjets() const { return fGenJetCollection; }
  const ElectronCollection& electrons() const { return fElectronCollection; }
  const MuonCollection& muons() const { return fMuonCollection; }
  const GenParticleCollection& genparticles() const { return fGenParticleCollection; }
  const PFCandsCollection& pfCandidates() const { return fPFCandidates; }

  const MET& genMET() const { return fGenMET; }

  const MET& met() const { return met_Type1(); }
  const MET& met_Type1() const { return fMET_Type1; }
  const MET& calomet() const { return fCaloMET; }
  const MET& L1met() const { return fL1MET; }

  const GenWeight& genWeight() const { return fGenWeight; }

private:
  EventID fEventID;

  VertexInfo fNPU;
  METFilter fMETFilter;

  BooleanOr fTriggerOr;
  BooleanOr fTriggerOr2;

  HLTTauCollection fTriggerTauCollection;
  TauCollection fTauCollection;
  JetCollection fJetCollection;
  GenJetCollection fGenJetCollection;
  ElectronCollection fElectronCollection;
  MuonCollection fMuonCollection;
  GenParticleCollection fGenParticleCollection;
  PFCandsCollection fPFCandidates;
  MET fGenMET;
  MET fMET_Type1;
  MET fCaloMET;
  MET fL1MET;

  GenWeight fGenWeight;

  const bool fIsMC;
};

#endif
