// -*- c++ -*-
#ifndef DataFormat_Event_h
#define DataFormat_Event_h

#include "DataFormat/interface/EventID.h"
#include "DataFormat/interface/Tau.h"
#include "DataFormat/interface/Jet.h"
#include "DataFormat/interface/Electron.h"
#include "DataFormat/interface/Muon.h"
#include "DataFormat/interface/MET.h"

#include "boost/property_tree/ptree.hpp"

class BranchManager;

class Event {
public:
  Event();
  explicit Event(const boost::property_tree::ptree& config);
  ~Event();

  void setupBranches(BranchManager& mgr);

  EventID& eventID() { return fEventID; }
  TauCollection& taus() { return fTauCollection; }
  JetCollection& jets() { return fJetCollection; }
  ElectronCollection& electrons() { return fElectronCollection; }
  MuonCollection& muons() { return fMuonCollection; }

  MET& genMET() { return fGenMET; }

  MET& met() { return met_Type1(); }
  MET& met_Type1() { return fMET_Type1; }

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
