#include "EventSelection/interface/PUDependencyPlots.h"

PUDependencyPlots::PUDependencyPlots(HistoWrapper& histoWrapper, bool isEnabled, const HistogramSettings& settings)
: CommonPlotsBase(histoWrapper, isEnabled),
  fHistoSettings(settings) { }

void PUDependencyPlots::book(TDirectory* dir, bool isData) {
  HistoLevel level = HistoLevel::kDebug;
  if (!isEnabled())
    level = HistoLevel::kNumberOfLevels;
  
  TDirectory* myDir = fHistoWrapper.mkdir(level, dir, "PUDependency");
  
  hNvtxTrg = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxTrg", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxVtx = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxVtx", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxTau = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxTau", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxAntiIsolatedTau = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxAntiIsolatedTau", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxElectronVeto = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxElectronVeto", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxMuonVeto = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxMuonVeto", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxJetSelection = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxJetSelection", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxAngularCutsCollinear = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxAngularCutsCollinear", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxMETSelection = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxMETSelection", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxBtagging = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxBtagging", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxAngularCutsBackToBack = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxAngularCutsBackToBack", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxAllSelections = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxAllSelections", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
  hNvtxAllSelectionsWithProbabilisticBtag = fHistoWrapper.makeTH<TH1F>(level, myDir, "NvtxAllSelectionsWithProbabilisticBtag", ";N_{vtx};N_{events}",
                                        fHistoSettings.bins(), fHistoSettings.min(), fHistoSettings.max());
}

void PUDependencyPlots::fillControlPlotsAfterTrigger(const Event& event) { 
  hNvtxTrg->Fill(fNvtx);
}

void PUDependencyPlots::fillControlPlotsAtVertexSelection(const Event& event) {
  hNvtxVtx->Fill(fNvtx);
}

void PUDependencyPlots::fillControlPlotsAfterTauSelection(const Event& event, const TauSelection::Data& data)  {
  hNvtxTau->Fill(fNvtx);
}

void PUDependencyPlots::fillControlPlotsAfterAntiIsolatedTauSelection(const Event& event, const TauSelection::Data& data) {
  hNvtxAntiIsolatedTau->Fill(fNvtx);
}

//void PUDependencyPlots::fillControlPlotsAtVetoTauSelection(const Event& event, const VetoTauSelection::Data& tauVetoData) { }

void PUDependencyPlots::fillControlPlotsAtElectronSelection(const Event& event, const ElectronSelection::Data& data)  {
  if (data.hasIdentifiedElectrons()) return;
  hNvtxElectronVeto->Fill(fNvtx);
}

void PUDependencyPlots::fillControlPlotsAtMuonSelection(const Event& event, const MuonSelection::Data& data)  {
  if (data.hasIdentifiedMuons()) return;
  hNvtxMuonVeto->Fill(fNvtx);
}

void PUDependencyPlots::fillControlPlotsAtJetSelection(const Event& event, const JetSelection::Data& data)  {
  if (!data.passedSelection()) return;
  hNvtxJetSelection->Fill(fNvtx);
}

void PUDependencyPlots::fillControlPlotsAtAngularCutsCollinear(const Event& event, const AngularCutsCollinear::Data& data)  {
  if (!data.passedSelection()) return;
  hNvtxAngularCutsCollinear->Fill(fNvtx);
}

void PUDependencyPlots::fillControlPlotsAtMETSelection(const Event& event, const METSelection::Data& data)  {
  if (!data.passedSelection()) return;
  hNvtxMETSelection->Fill(fNvtx);
}

void PUDependencyPlots::fillControlPlotsAtBtagging(const Event& event, const BJetSelection::Data& data)  {
  if (!data.passedSelection()) return;
  hNvtxBtagging->Fill(fNvtx);
}

void PUDependencyPlots::fillControlPlotsAtAngularCutsBackToBack(const Event& event, const AngularCutsBackToBack::Data& data)  {
  if (!data.passedSelection()) return;
  hNvtxAngularCutsBackToBack->Fill(fNvtx);
}

void PUDependencyPlots::fillControlPlotsAfterAllSelections(const Event& event)  {
  hNvtxAllSelections->Fill(fNvtx);
}

void PUDependencyPlots::fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(const Event& event, const METSelection::Data& metData, double btagWeight)  {
  hNvtxAllSelectionsWithProbabilisticBtag->Fill(fNvtx, btagWeight);
}
