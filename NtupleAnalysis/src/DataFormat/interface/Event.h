// -*- c++ -*-
#ifndef DataFormat_Event_h
#define DataFormat_Event_h

#include "Framework/interface/ParameterSet.h"
#include "Tools/interface/BooleanOr.h"

#include "DataFormat/interface/EventID.h"
#include "DataFormat/interface/VertexInfo.h"
#include "DataFormat/interface/METFilter.h"
#include "DataFormat/interface/L1Tau.h"
#include "DataFormat/interface/L1IsoTau.h"
#include "DataFormat/interface/L1Jet.h"
#include "DataFormat/interface/HLTTau.h"
#include "DataFormat/interface/HLTBJet.h"
#include "DataFormat/interface/Tau.h"
#include "DataFormat/interface/Jet.h"
#include "DataFormat/interface/GenJet.h"
#include "DataFormat/interface/Electron.h"
#include "DataFormat/interface/Muon.h"
#include "DataFormat/interface/MET.h"
#include "DataFormat/interface/GenWeight.h"
#include "DataFormat/interface/GenParticle.h"
#include "DataFormat/interface/PFCands.h"
// Marina
#include "DataFormat/interface/AK8Jet.h"
#include "DataFormat/interface/AK8JetsSoftDrop.h"

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
    if (!passL1Decision(fL1ETMThreshold)) return false;
    if (configurableTriggerIsEmpty() && configurableTrigger2IsEmpty())
      return true;
    if (configurableTrigger2IsEmpty())
      return configurableTriggerDecision();
    return configurableTriggerDecision() || configurableTriggerDecision2();
  }
  bool passL1Decision(float L1ETMcut = 0) const {
    if(L1ETMcut > 0){
      if(L1met().et() < L1ETMcut) return false;
    }
    return true;
  }  
  bool passHLTDecisionByName(std::string& trigger) const {
    return fTriggerOr.value_SearchBranches(trigger);
  }

  const EventID& eventID() const { return fEventID; }
  const VertexInfo& vertexInfo() const { return fVertexInfo; }
  const METFilter& metFilter() const { return fMETFilter; }
  const L1TauCollection& l1Taus() const { return fL1TauCollection; }
  const L1IsoTauCollection& l1IsoTaus() const { return fL1IsoTauCollection; }
  const L1JetCollection& l1Jets() const { return fL1JetCollection; }
  const HLTTauCollection& triggerTaus() const { return fTriggerTauCollection; }
  const HLTBJetCollection& triggerBJets() const { return fTriggerBJetCollection; }
  const TauCollection& taus() const { return fTauCollection; }
  const JetCollection& jets() const { return fJetCollection; }
  const GenJetCollection& genjets() const { return fGenJetCollection; }
  const ElectronCollection& electrons() const { return fElectronCollection; }
  const MuonCollection& muons() const { return fMuonCollection; }
  const GenParticleCollection& genparticles() const { return fGenParticleCollection; }
  const PFCandsCollection& pfCandidates() const { return fPFCandidates; }
  // Marina
  const AK8JetCollection& ak8jets() const { return fAK8JetCollection; }
  const AK8JetsSoftDropCollection& ak8jetsSoftDrop() const { return fAK8JetsSoftDropCollection; }

  const MET& genMET() const { return fGenMET; }
  const MET& met() const { return fMET; }
  const MET& met_Type1() const { return fMET_Type1; }
  const MET& calomet() const { return fCaloMET; }
  const MET& L1met() const { 
    ////    if(isMC()) return L1extramet(); // moved to stage2 l1etm, l1extra obsolete. 19082016/SL
    return fL1MET; 
  }
  const MET& L1extramet() const { return fL1extraMET; }

  const GenWeight& genWeight() const { return fGenWeight; }
  const GenWeight_T<float>& topPtWeight() const { return fTopPtWeight; }

private:
  EventID fEventID;

  VertexInfo fVertexInfo;
  METFilter fMETFilter;

  BooleanOr fTriggerOr;
  BooleanOr fTriggerOr2;

  L1TauCollection fL1TauCollection;
  L1IsoTauCollection fL1IsoTauCollection;
  L1JetCollection fL1JetCollection;
  HLTTauCollection fTriggerTauCollection;
  HLTBJetCollection fTriggerBJetCollection;
  TauCollection fTauCollection;
  JetCollection fJetCollection;
  GenJetCollection fGenJetCollection;
  ElectronCollection fElectronCollection;
  MuonCollection fMuonCollection;
  GenParticleCollection fGenParticleCollection;
  PFCandsCollection fPFCandidates;
  // Marina
  AK8JetCollection fAK8JetCollection;
  AK8JetsSoftDropCollection fAK8JetsSoftDropCollection;

  MET fGenMET;
  MET fMET_Type1;
  MET fMET;
  MET fCaloMET;
  MET fL1MET;
  MET fL1extraMET;

  GenWeight fGenWeight;
  GenWeight_T<float> fTopPtWeight;

  float fL1ETMThreshold;
  const bool fIsMC;
};

#endif
