#include "EventSelection/interface/CommonPlotsBase.h"

#include "EventSelection/interface/TransverseMass.h"

#include "DataFormat/interface/Event.h"

CommonPlotsBase::CommonPlotsBase(HistoWrapper& histoWrapper, bool isEnabled)
: fHistoWrapper(histoWrapper),
  bIsEnabled(isEnabled) { }
CommonPlotsBase::~CommonPlotsBase() { }
  
void CommonPlotsBase::book(TDirectory* dir, bool isData) { }
void CommonPlotsBase::reset() { }

//===== unique filling methods (to be called inside the event selection routine only, i.e. (before a passing decision is done))
//void CommonPlotsBase::fillControlPlotsAtVetoTauSelection(const Event& event, const VetoTauSelection::Data& tauVetoData) { }
void CommonPlotsBase::fillControlPlotsAtVertexSelection(const Event& event) { }
void CommonPlotsBase::fillControlPlotsAtElectronSelection(const Event& event, const ElectronSelection::Data& data) { }
void CommonPlotsBase::fillControlPlotsAtMuonSelection(const Event& event, const MuonSelection::Data& data) { }
void CommonPlotsBase::fillControlPlotsAtTauSelection(const Event& event, const TauSelection::Data& data) { }
void CommonPlotsBase::fillControlPlotsAtJetSelection(const Event& event, const JetSelection::Data& data) { }
void CommonPlotsBase::fillControlPlotsAtAngularCutsCollinear(const Event& event, const AngularCutsCollinear::Data& data) { }
void CommonPlotsBase::fillControlPlotsAtMETSelection(const Event& event, const METSelection::Data& data) { }
void CommonPlotsBase::fillControlPlotsAtBtagging(const Event& event, const BJetSelection::Data& data) { }
void CommonPlotsBase::fillControlPlotsAtAngularCutsBackToBack(const Event& event, const AngularCutsBackToBack::Data& data) { }
//void CommonPlotsBase::fillControlPlotsAtTopSelection(const Event& event, const TopSelectionManager::Data& data) { }
//void CommonPlotsBase::fillControlPlotsAtEvtTopology(const Event& event, const EvtTopology::Data& data) { }

//===== unique filling methods (to be called AFTER return statement from analysis routine)
void CommonPlotsBase::fillControlPlotsAfterAntiIsolatedTauSelection(const Event& event, const TauSelection::Data& data) { }
void CommonPlotsBase::fillControlPlotsAfterTrigger(const Event& event) { }
void CommonPlotsBase::fillControlPlotsAfterTauSelection(const Event& event, const TauSelection::Data& data) { }
void CommonPlotsBase::fillControlPlotsAfterMETTriggerScaleFactor(const Event& event) { }
void CommonPlotsBase::fillControlPlotsAfterTopologicalSelections(const Event& event) { }
void CommonPlotsBase::fillControlPlotsAfterAllSelections(const Event& event) { }
void CommonPlotsBase::fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(const Event& event, const METSelection::Data& metData, double btagWeight) { }
//void CommonPlotsBase::fillControlPlotsAfterAllSelectionsWithFullMass(const Event& event, FullHiggsMassCalculator::Data& data) { }
