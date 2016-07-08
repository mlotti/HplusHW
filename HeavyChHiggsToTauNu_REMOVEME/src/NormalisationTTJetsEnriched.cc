// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NormalisationTTJetsEnriched.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Math/interface/LorentzVector.h"

namespace HPlus {
  NormalisationTTJetsEnrichedWithGenuineTaus::NormalisationTTJetsEnrichedWithGenuineTaus(EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(eventCounter, histoWrapper, "TTJetsEnrichedWithGenuineTaus") { }

  NormalisationTTJetsEnrichedWithGenuineTaus::NormalisationTTJetsEnrichedWithGenuineTaus(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(iConfig, eventCounter, histoWrapper, "TTJetsEnrichedWithGenuineTaus") { }

  NormalisationTTJetsEnrichedWithGenuineTaus::~NormalisationTTJetsEnrichedWithGenuineTaus() { }

  void NormalisationTTJetsEnrichedWithGenuineTaus::analyse(const edm::Event& iEvent,
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
    // - increase MET cut and/or tau pT cut to suppress QCD
    // - if necessary, remove signal region by cut on mT
    // - if necessary, require one more b tagged jet

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

    // Do MET cut, require MET>80
    if (!metData.passedEvent()) return;
    if (metData.getSelectedMET()->et() < 80.0) return;

    // Do btagging
    if (!btagData.passedEvent()) return;

    // Obtain btagging scale factor
    if (!iEvent.isRealData()) {
      myEventWeight *= btagData.getScaleFactor();
    }

    // Do back-to-back tail killer
    // if (!tailKillerData.passedBackToBackCuts()) return;

    // Fill plots
    fillPlotsAfterSelection(fakeTauData.isFakeTau(), tauData, jetData, metData, btagData, myEventWeight);
  }

  NormalisationTTJetsEnrichedBoostedWH::NormalisationTTJetsEnrichedBoostedWH(EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(eventCounter, histoWrapper, "TTJetsEnrichedBoostedWH") { }

  NormalisationTTJetsEnrichedBoostedWH::NormalisationTTJetsEnrichedBoostedWH(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(iConfig, eventCounter, histoWrapper, "TTJetsEnrichedBoostedWH") { }

  NormalisationTTJetsEnrichedBoostedWH::~NormalisationTTJetsEnrichedBoostedWH() { }

  void NormalisationTTJetsEnrichedBoostedWH::analyse(const edm::Event& iEvent,
                                                       const TauSelection::Data& tauData,
                                                       const FakeTauIdentifier::Data& fakeTauData,
                                                       const ElectronSelection::Data& electronData,
                                                       const MuonSelection::Data& muonData,
                                                       const JetSelection::Data& jetData,
                                                       METTriggerEfficiencyScaleFactor* metTrgSF,
                                                       const QCDTailKiller::Data& tailKillerData,
                                                       const METSelection::Data& metData,
                                                       const BTagging::Data& btagData) {
    // Apply signal analysis with following exceptions to select a TTJets enriched sample in style of AN2013/067

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

    // Do MET cut, require MET>80
    if (!metData.passedEvent()) return;
    if (metData.getSelectedMET()->et() < 80.0) return;

    // Do btagging
    if (!btagData.passedEvent()) return;
    if (!(btagData.getBJetCount() == 2)) return;

    // Obtain btagging scale factor
    if (!iEvent.isRealData()) {
      myEventWeight *= btagData.getScaleFactor();
    }

    // Do back-to-back tail killer
    // if (!tailKillerData.passedBackToBackCuts()) return;

    // Cut on boost
    double myHiggsPt = getHiggsPt(tauData, metData);
    if (!(myHiggsPt > 120)) return;

    // Fill plots
    fillPlotsAfterSelection(fakeTauData.isFakeTau(), tauData, jetData, metData, btagData, myEventWeight);
  }


    NormalisationTTJetsEnrichedWithFakeTaus::NormalisationTTJetsEnrichedWithFakeTaus(EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(eventCounter, histoWrapper, "TTJetsEnrichedWithFakeTaus") { }

  NormalisationTTJetsEnrichedWithFakeTaus::NormalisationTTJetsEnrichedWithFakeTaus(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper)
  : NormalisationAnalysis(iConfig, eventCounter, histoWrapper, "TTJetsEnrichedWithFakeTaus") { }

  NormalisationTTJetsEnrichedWithFakeTaus::~NormalisationTTJetsEnrichedWithFakeTaus() { }

  void NormalisationTTJetsEnrichedWithFakeTaus::analyse(const edm::Event& iEvent,
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
    // - instead of mu veto require two isolated muons
    // - require opposite sign of muons
    // - calculate m(mu,tau) and require incompatilibity with Z mass

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

    // Do back-to-back tail killer
    //if (!tailKillerData.passedBackToBackCuts()) return;

    // Require opposite sign of muon and tau
    if (muonData.getSelectedTightMuons()[0]->charge() == muonData.getSelectedTightMuons()[1]->charge()) return;

    // Reconstruct Z mass from muon and tau
    double myZMass = (muonData.getSelectedTightMuons()[0]->p4() + tauData.getSelectedTau()->p4()).mass();
    // TODO: Add cut here 

    // Fill plots
    fillPlotsAfterSelection(fakeTauData.isFakeTau(), tauData, jetData, metData, btagData, myEventWeight, myZMass);
  }
}
