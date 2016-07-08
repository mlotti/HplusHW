// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NormalisationWJetsEnriched.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Math/interface/LorentzVector.h"

namespace HPlus {
  NormalisationWJetsEnrichedWithGenuineTaus::NormalisationWJetsEnrichedWithGenuineTaus(EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(eventCounter, histoWrapper, "WJetsEnrichedWithGenuineTaus") { }

  NormalisationWJetsEnrichedWithGenuineTaus::NormalisationWJetsEnrichedWithGenuineTaus(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(iConfig, eventCounter, histoWrapper, "WJetsEnrichedWithGenuineTaus") { }

  NormalisationWJetsEnrichedWithGenuineTaus::~NormalisationWJetsEnrichedWithGenuineTaus() { }

  void NormalisationWJetsEnrichedWithGenuineTaus::analyse(const edm::Event& iEvent,
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
    // - reverse btagging
    // - if necessary, suppress QCD by increasing MET cut

    // Assume tau ID has been done already
    double myEventWeight = fHistoWrapper.getWeight();

    // Apply electron veto
    if (!electronData.passedEvent()) return;

    // Require exactly one isolated muon
    if (!muonData.passedEvent()) return;

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
    if (btagData.getBJetCount() != 0) return;

    // Obtain btagging scale factor
    if (!iEvent.isRealData()) {
      myEventWeight *= btagData.getScaleFactor();
    }

    // Do back-to-back tail killer
    //if (!tailKillerData.passedBackToBackCuts()) return;

    // Fill plots
    fillPlotsAfterSelection(fakeTauData.isFakeTau(), tauData, jetData, metData, btagData, myEventWeight);
  }

  NormalisationWJetsEnrichedBoostedWH::NormalisationWJetsEnrichedBoostedWH(EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(eventCounter, histoWrapper, "WJetsEnrichedBoostedWH") { }

  NormalisationWJetsEnrichedBoostedWH::NormalisationWJetsEnrichedBoostedWH(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(iConfig, eventCounter, histoWrapper, "WJetsEnrichedBoostedWH") { }

  NormalisationWJetsEnrichedBoostedWH::~NormalisationWJetsEnrichedBoostedWH() { }

  void NormalisationWJetsEnrichedBoostedWH::analyse(const edm::Event& iEvent,
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
    // - reverse b tagging
    // - calculate m(mu,tau) and require incompatibility with Z mass

    // Assume tau ID has been done already
    double myEventWeight = fHistoWrapper.getWeight();

    // Apply electron veto
    if (!electronData.passedEvent()) return;

    // Require exactly one isolated muons
    if (!muonData.passedEvent()) return;

    // Do jet selection
    if (!(jetData.getHadronicJetCount() == 3)) return;

    // Do MET preselection
    if(!metData.passedPreMetCut()) return;

    // Obtain MET trg SF
    if (!iEvent.isRealData()) {
      myEventWeight *= metTrgSF->getEventWeight(*(metData.getSelectedMET()));
    }

    // Do collinear tail killer
    //if (!tailKillerData.passedCollinearCuts()) return;

    // Do MET cut
    if (metData.getSelectedMET()->et() < 80.0) return;
    //if (!metData.passedEvent()) return;

    // Do btagging
    if (!(btagData.getMaxDiscriminatorValue() > 0.244 && btagData.getMaxDiscriminatorValue() < 0.898)) return;

    // Obtain btagging scale factor
    if (!iEvent.isRealData()) {
      myEventWeight *= btagData.getScaleFactor();
    }

    // Do back-to-back tail killer
    //if (!tailKillerData.passedBackToBackCuts()) return;

    // Cut on boost
    double myHiggsPt = getHiggsPt(tauData, metData);
    if (!(myHiggsPt > 120)) return;

    // Fill plots
    fillPlotsAfterSelection(fakeTauData.isFakeTau(), tauData, jetData, metData, btagData, myEventWeight);
  }

  NormalisationWJetsEnrichedWithFakeTaus::NormalisationWJetsEnrichedWithFakeTaus(EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(eventCounter, histoWrapper, "WJetsEnrichedWithFakeTaus") { }

  NormalisationWJetsEnrichedWithFakeTaus::NormalisationWJetsEnrichedWithFakeTaus(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(iConfig, eventCounter, histoWrapper, "WJetsEnrichedWithFakeTaus") { }

  NormalisationWJetsEnrichedWithFakeTaus::~NormalisationWJetsEnrichedWithFakeTaus() { }

  void NormalisationWJetsEnrichedWithFakeTaus::analyse(const edm::Event& iEvent,
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
    // - reverse b tagging
    // - calculate m(mu,tau) and require incompatibility with Z mass

    // Assume tau ID has been done already
    double myEventWeight = fHistoWrapper.getWeight();

    // Apply electron veto
    if (!electronData.passedEvent()) return;

    // Require exactly one isolated muons
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
    if (btagData.getBJetCount() != 0) return;

    // Obtain btagging scale factor
    if (!iEvent.isRealData()) {
      myEventWeight *= btagData.getScaleFactor();
    }

    // Do back-to-back tail killer
    //if (!tailKillerData.passedBackToBackCuts()) return;

    // Reconstruct Z mass from muon and tau
    double myZMass = (muonData.getSelectedTightMuons()[0]->p4() + tauData.getSelectedTau()->p4()).mass();
    // TODO: Add cut here ?

    // Fill plots
    fillPlotsAfterSelection(fakeTauData.isFakeTau(), tauData, jetData, metData, btagData, myEventWeight, myZMass);
  }
}
