// -*- c++ -*-
#ifndef DataFormat_Event_h
#define DataFormat_Event_h

#include "Framework/interface/ParameterSet.h"

#include "DataFormat/interface/EventID.h"
#include "DataFormat/interface/Tau.h"
#include "DataFormat/interface/Jet.h"
#include "DataFormat/interface/Electron.h"
#include "DataFormat/interface/Muon.h"
#include "DataFormat/interface/MET.h"

class BranchManager;

class Event {
public:
  Event();
  explicit Event(const ParameterSet& config);
  ~Event();

  void setupBranches(BranchManager& mgr);

  const EventID& eventID() const { return fEventID; }
  const TauCollection& taus() const { return fTauCollection; }
  const JetCollection& jets() const { return fJetCollection; }
  const ElectronCollection& electrons() const { return fElectronCollection; }
  const MuonCollection& muons() const { return fMuonCollection; }

  const MET& genMET() const { return fGenMET; }

  const MET& met() const { return met_Type1(); }
  const MET& met_Type1() const { return fMET_Type1; }

private:
  EventID fEventID;
  TauCollection fTauCollection;
  JetCollection fJetCollection;
  ElectronCollection fElectronCollection;
  MuonCollection fMuonCollection;
  MET fGenMET;
  MET fMET_Type1;
};

#endif
