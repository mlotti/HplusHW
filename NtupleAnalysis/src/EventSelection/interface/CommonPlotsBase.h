// -*- c++ -*-
#ifndef EventSelection_CommonPlotsBase_h
#define EventSelection_CommonPlotsBase_h

#include "EventSelection/interface/EventSelections.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/HistoSplitter.h"
#include "Framework/interface/HistogramSettings.h"

#include "TDirectory.h"

/// Base class for plotting routines needed at specific steps of the analysis
class CommonPlotsBase {
public:
  CommonPlotsBase(HistoWrapper& histoWrapper, bool isEnabled);
  virtual ~CommonPlotsBase();
  
  bool isEnabled() const { return bIsEnabled; }

  virtual void book(TDirectory* dir, bool isData);
  virtual void reset();
  //===== unique filling methods (to be called inside the event selection routine only, i.e. (before a passing decision is done))
  virtual void fillControlPlotsAtVertexSelection(const Event& event);
  //virtual void fillControlPlotsAtVetoTauSelection(const Event& event, const VetoTauSelection::Data& tauVetoData);
  virtual void fillControlPlotsAtElectronSelection(const Event& event, const ElectronSelection::Data& data);
  virtual void fillControlPlotsAtMuonSelection(const Event& event, const MuonSelection::Data& data);
  virtual void fillControlPlotsAtTauSelection(const Event& event, const TauSelection::Data& data);
  virtual void fillControlPlotsAtJetSelection(const Event& event, const JetSelection::Data& data);
  virtual void fillControlPlotsAtAngularCutsCollinear(const Event& event, const AngularCutsCollinear::Data& data);
  virtual void fillControlPlotsAtMETSelection(const Event& event, const METSelection::Data& data);
  virtual void fillControlPlotsAtBtagging(const Event& event, const BJetSelection::Data& data);
  virtual void fillControlPlotsAtAngularCutsBackToBack(const Event& event, const AngularCutsBackToBack::Data& data);
  //virtual void fillControlPlotsAtTopSelection(const Event& event, const TopSelectionManager::Data& data);
  //virtual void fillControlPlotsAtEvtTopology(const Event& event, const EvtTopology::Data& data);
  
  //===== unique filling methods (to be called AFTER return statement from analysis routine)
  virtual void fillControlPlotsAfterTrigger(const Event& event);
  virtual void fillControlPlotsAfterTauSelection(const Event& event, const TauSelection::Data& data);
  virtual void fillControlPlotsAfterAntiIsolatedTauSelection(const Event& event, const TauSelection::Data& data);
  virtual void fillControlPlotsAfterMETTriggerScaleFactor(const Event& event);
  virtual void fillControlPlotsAfterTopologicalSelections(const Event& event);
  virtual void fillControlPlotsAfterAllSelections(const Event& event);
  virtual void fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(const Event& event, const METSelection::Data& metData, double btagWeight);
  //virtual void fillControlPlotsAfterAllSelectionsWithFullMass(const Event& event, FullHiggsMassCalculator::Data& data);

protected:
  HistoWrapper fHistoWrapper;
  
private:
  bool bIsEnabled;
  
};

#endif
