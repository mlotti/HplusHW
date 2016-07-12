// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NormalisationDYEnriched.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Math/interface/LorentzVector.h"

namespace HPlus {
  NormalisationDYEnrichedWithGenuineTaus::NormalisationDYEnrichedWithGenuineTaus(EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(eventCounter, histoWrapper, "DYEnrichedWithGenuineTaus") { }

  NormalisationDYEnrichedWithGenuineTaus::NormalisationDYEnrichedWithGenuineTaus(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(iConfig, eventCounter, histoWrapper, "DYEnrichedWithGenuineTaus") { }

  NormalisationDYEnrichedWithGenuineTaus::~NormalisationDYEnrichedWithGenuineTaus() { }

  void NormalisationDYEnrichedWithGenuineTaus::analyse(const edm::Event& iEvent,
                                                       const TauSelection::Data& tauData,
                                                       const FakeTauIdentifier::Data& fakeTauData,
                                                       const ElectronSelection::Data& electronData,
                                                       const MuonSelection::Data& muonData,
                                                       const JetSelection::Data& jetData,
                                                       METTriggerEfficiencyScaleFactor* metTrgSF,
                                                       const QCDTailKiller::Data& tailKillerData,
                                                       const METSelection::Data& metData,
                                                       const BTagging::Data& btagData) {
    // Apply signal analysis with following exceptions to select a DY enriched sample:
    // - instead of mu veto require one isolated muon
    // - require opposite sign of muon and tau
    // - calculate m(mu,tau) and apply a mass window

    // Assume tau ID has been done already
    double myEventWeight = fHistoWrapper.getWeight();

    // Apply electron veto
    if (!electronData.passedEvent()) return;

    // Require exactly one isolated muon
    if (muonData.getSelectedTightMuons().size() != 1) return;

    // Do jet selection
    if (!jetData.passedEvent()) return;

    // Do MET preselection
    if(!metData.passedPreMetCut()) return;

    // Obtain MET trg SF
    if (!iEvent.isRealData()) {
      myEventWeight *= metTrgSF->getEventWeight(*(metData.getSelectedMET()));
    }

    // Do collinear tail killer
    //if (!tailKillerData.passedCollinearCuts()) return;

    // Do MET cut
    if (!metData.passedEvent()) return;

    // Do btagging
    if (!btagData.passedEvent()) return;

    // Obtain btagging scale factor
    if (!iEvent.isRealData()) {
      myEventWeight *= btagData.getScaleFactor();
    }

    // Do back-to-back tail killer
    //if (!tailKillerData.passedBackToBackCuts()) return;

    // Require opposite sign of muon and tau
    if (muonData.getSelectedTightMuons()[0]->charge() == tauData.getSelectedTau()->charge()) return;

    // Reconstruct Z mass from muon and tau
    double myZMass = (muonData.getSelectedTightMuons()[0]->p4() + tauData.getSelectedTau()->p4()).mass();
    //InvariantMass::InvariantMass<LorentzVector>(muonData.getSelectedTightMuons()[0]->p4(), tauData.getSelectedTau()->p4());
    // TODO: Add cut here


    // Fill plots
    fillPlotsAfterSelection(fakeTauData.isFakeTau(), tauData, jetData, metData, btagData, myEventWeight, myZMass);
  }
    NormalisationDYEnrichedWithFakeTaus::NormalisationDYEnrichedWithFakeTaus(EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(eventCounter, histoWrapper, "DYEnrichedWithFakeTaus") { }

  NormalisationDYEnrichedWithFakeTaus::NormalisationDYEnrichedWithFakeTaus(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(iConfig, eventCounter, histoWrapper, "DYEnrichedWithFakeTaus") { }

  NormalisationDYEnrichedWithFakeTaus::~NormalisationDYEnrichedWithFakeTaus() { }

  void NormalisationDYEnrichedWithFakeTaus::analyse(const edm::Event& iEvent,
                                                    const TauSelection::Data& tauData,
                                                    const FakeTauIdentifier::Data& fakeTauData,
                                                    const ElectronSelection::Data& electronData,
                                                    const MuonSelection::Data& muonData,
                                                    const JetSelection::Data& jetData,
                                                    METTriggerEfficiencyScaleFactor* metTrgSF,
                                                    const QCDTailKiller::Data& tailKillerData,
                                                    const METSelection::Data& metData,
                                                    const BTagging::Data& btagData) {
    // Apply signal analysis with following exceptions to select a DY enriched sample:
    // - instead of mu veto require one isolated muon
    // - require opposite sign of muon and tau
    // - calculate m(mu,tau) and apply a mass window

    // Assume tau ID has been done already
    double myEventWeight = fHistoWrapper.getWeight();

    // Apply electron veto
    if (!electronData.passedEvent()) return;

    // Require exactly two isolated muons
    if (muonData.getSelectedTightMuons().size() != 2) return;

    // Do jet selection
    if (!jetData.passedEvent()) return;

    // Do MET preselection
    if(!metData.passedPreMetCut()) return;

    // Obtain MET trg SF
    if (!iEvent.isRealData()) {
      myEventWeight *= metTrgSF->getEventWeight(*(metData.getSelectedMET()));
    }

    // Do collinear tail killer
    //if (!tailKillerData.passedCollinearCuts()) return;

    // Do MET cut
    if (!metData.passedEvent()) return;

    // Do btagging
    if (!btagData.passedEvent()) return;

    // Obtain btagging scale factor
    if (!iEvent.isRealData()) {
      myEventWeight *= btagData.getScaleFactor();
    }

    // Do back-to-back tail killer
    //if (!tailKillerData.passedBackToBackCuts()) return;

    // Require opposite sign of muon and tau
    if (muonData.getSelectedTightMuons()[0]->charge() == muonData.getSelectedTightMuons()[1]->charge()) return;

    // Reconstruct Z mass from muon and tau
    double myZMass = (muonData.getSelectedTightMuons()[0]->p4() + muonData.getSelectedTightMuons()[1]->p4()).mass();
    // TODO: Add cut here (80-100) ?

    // Fill plots
    fillPlotsAfterSelection(fakeTauData.isFakeTau(), tauData, jetData, metData, btagData, myEventWeight, myZMass);
  }
}
