// -*- c++ -*-
#ifndef EventSelection_PUDependencyPlots_h
#define EventSelection_PUDependencyPlots_h

#include "EventSelection/interface/CommonPlotsBase.h"

class PUDependencyPlots : public CommonPlotsBase {
public:
  PUDependencyPlots(HistoWrapper& histoWrapper, bool isEnabled, const HistogramSettings& settings);
  ~PUDependencyPlots() { }
  
  void setNvtx(int nvtx) { fNvtx = nvtx; }
  
  void book(TDirectory* dir, bool isData);
  void reset() { fNvtx = -1; }
  
  void fillControlPlotsAfterTrigger(const Event& event);
  void fillControlPlotsAtVertexSelection(const Event& event);
  void fillControlPlotsAfterTauSelection(const Event& event, const TauSelection::Data& data);
  void fillControlPlotsAfterAntiIsolatedTauSelection(const Event& event, const TauSelection::Data& data);
  //void fillControlPlotsAtVetoTauSelection(const Event& event, const VetoTauSelection::Data& tauVetoData);
  void fillControlPlotsAtElectronSelection(const Event& event, const ElectronSelection::Data& data);
  void fillControlPlotsAtMuonSelection(const Event& event, const MuonSelection::Data& data);
  void fillControlPlotsAtJetSelection(const Event& event, const JetSelection::Data& data);
  void fillControlPlotsAtAngularCutsCollinear(const Event& event, const AngularCutsCollinear::Data& data);
  void fillControlPlotsAtMETSelection(const Event& event, const METSelection::Data& data);
  void fillControlPlotsAtBtagging(const Event& event, const BJetSelection::Data& data);
  void fillControlPlotsAtAngularCutsBackToBack(const Event& event, const AngularCutsBackToBack::Data& data);
  void fillControlPlotsAfterAllSelections(const Event& event);
  void fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(const Event& event, const METSelection::Data& metData, double btagWeight);

private:
  const HistogramSettings& fHistoSettings;
  
  int fNvtx;
  
  WrappedTH1* hNvtxTrg;
  WrappedTH1* hNvtxVtx;
  WrappedTH1* hNvtxTau;
  WrappedTH1* hNvtxAntiIsolatedTau;
  WrappedTH1* hNvtxElectronVeto;
  WrappedTH1* hNvtxMuonVeto;
  WrappedTH1* hNvtxJetSelection;
  WrappedTH1* hNvtxAngularCutsCollinear;
  WrappedTH1* hNvtxMETSelection;
  WrappedTH1* hNvtxBtagging;
  WrappedTH1* hNvtxAngularCutsBackToBack;
  WrappedTH1* hNvtxAllSelections;
  WrappedTH1* hNvtxAllSelectionsWithProbabilisticBtag;
};

#endif