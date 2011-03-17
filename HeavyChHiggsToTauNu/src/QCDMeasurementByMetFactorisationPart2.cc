#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementByMetFactorisationPart2.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  QCDMeasurementByMetFactorisationPart2::QCDMeasurementByMetFactorisationPart2(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    fAllCounter(eventCounter.addCounter("allEvents")),
    fTriggerAndHLTMetCutCounter(eventCounter.addCounter("Trigger_and_HLT_MET")),
    fPrimaryVertexCounter(eventCounter.addCounter("PrimaryVertex")),
    fOneProngTauSelectionCounter(eventCounter.addCounter("TauSelection")),
    fGlobalElectronVetoCounter(eventCounter.addCounter("GlobalElectronVeto")),
    fGlobalMuonVetoCounter(eventCounter.addCounter("GlobalMuonVeto")),
    fJetSelectionCounter2(eventCounter.addCounter("JetSelection2")),
    fJetSelectionCounter(eventCounter.addCounter("JetSelection")),
    fMETCounter(eventCounter.addCounter("MET")),
    fOneProngTauIDWithoutRtauCounter(eventCounter.addCounter("TauID_noRtau")),
    fOneProngTauIDWithRtauCounter(eventCounter.addCounter("TauID_withRtau")),
    fInvMassVetoOnJetsCounter(eventCounter.addCounter("InvMassVetoOnJets")), // dumbie
    fEvtTopologyCounter(eventCounter.addCounter("EvtTopology")),             // dumbie
    fBTaggingCounter(eventCounter.addCounter("bTagging")),
    fFakeMETVetoCounter(eventCounter.addCounter("FakeMETVeto")),
    fABCDNegativeRtauNegativeBTagCounter(eventCounter.addCounter("ABCD_NegRtau_NegBtag")),
    fABCDNegativeRtauPositiveBTagCounter(eventCounter.addCounter("ABCD_NegRtau_PosBtag")),
    fABCDPositiveRtauNegativeBTagCounter(eventCounter.addCounter("ABCD_PosRtau_NegBtag")),
    fABCDPositiveRtauPositiveBTagCounter(eventCounter.addCounter("ABCD_PosRtau_PosBtag")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    //fTriggerTauMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"), eventCounter, eventWeight),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, eventWeight),
    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, 1),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight),
    fInvMassVetoOnJets(iConfig.getUntrackedParameter<edm::ParameterSet>("InvMassVetoOnJets"), eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight),
    fFactorizationTable(iConfig, "METTables")
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
   {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms 
    hMETAfterJetSelection = fs->make<TH1F>("METAfterJetSelection", "METAfterJetSelection;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hMETAfterJetSelection->Sumw2();
    hWeightedMETAfterJetSelection = fs->make<TH1F>("METAfterJetSelectionWeighted", "METAfterJetSelectionWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterJetSelection->Sumw2();
    hWeightedMETAfterTauIDNoRtau = fs->make<TH1F>("METAfterTauIDNoRtauWeighted", "METAfterTauIDNoRtauWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterTauIDNoRtau->Sumw2();
    hWeightedMETAfterTauID = fs->make<TH1F>("METAfterTauIDWeighted", "METAfterTauIDWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterTauID->Sumw2();
    hWeightedMETAfterBTagging = fs->make<TH1F>("METAfterBTaggingWeighted", "METAfterBTaggingWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterBTagging->Sumw2();
    hWeightedMETAfterFakeMETVeto = fs->make<TH1F>("METAfterFakeMETVetoWeighted", "METAfterFakeMETVetoWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterFakeMETVeto->Sumw2();    
    hRTauAfterAllSelections = fs->make<TH1F>("RTauAfterAllSelections", "RTauAfterAllSelections;Rtau;N_{events}/0.02", 60, 0., 1.2);
    hRTauAfterAllSelections->Sumw2();

    // Histograms for later change of factorization map
    int myCoefficientBinCount = fFactorizationTable.getCoefficientTableSize();
    hNonWeightedTauPtAfterJetSelection = fs->make<TH1F>("NonWeightedTauPtAfterJetSelection", "NonWeightedTauPtAfterJetSelection;tau p_{T} bin;N_{events} after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
    hNonWeightedTauPtAfterJetSelection->Sumw2();
    hNonWeightedTauPtAfterTauIDNoRtau = fs->make<TH1F>("NonWeightedTauPtAfterTauIDNoRtau", "NonWeightedTauPtAfterTauIDNoRtau;tau p_{T} bin;N_{events} after TauIDNoRtau", myCoefficientBinCount, 0., myCoefficientBinCount);
    hNonWeightedTauPtAfterTauIDNoRtau->Sumw2();
    hNonWeightedTauPtAfterTauID = fs->make<TH1F>("NonWeightedTauPtAfterTauID", "NonWeightedTauPtAfterTauID;tau p_{T} bin;N_{events} after TauID", myCoefficientBinCount, 0., myCoefficientBinCount);
    hNonWeightedTauPtAfterTauID->Sumw2();
    hNonWeightedTauPtAfterBTagging = fs->make<TH1F>("NonWeightedTauPtAfterBTagging", "NonWeightedTauPtAfterBTagging;tau p_{T} bin;N_{events} after b tagging", myCoefficientBinCount, 0., myCoefficientBinCount);
    hNonWeightedTauPtAfterBTagging->Sumw2();
    hNonWeightedTauPtAfterFakeMETVeto = fs->make<TH1F>("NonWeightedTauPtAfterFakeMETVeto", "NonWeightedTauPtAfterFakeMETVeto;tau p_{T} bin;N_{events} after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hNonWeightedTauPtAfterFakeMETVeto->Sumw2();
    fNonWeightedABCDNegativeRtauNegativeBTag = fs->make<TH1F>("NonWeightedTauPtABCDNegRtauNegBTag", "NonWeightedTauPtABCDNegRtauNegBTag;tau p_{T} bin;N_{events} for ABCDNegRtauNegBTag", myCoefficientBinCount, 0., myCoefficientBinCount);
    fNonWeightedABCDNegativeRtauNegativeBTag->Sumw2();
    fNonWeightedABCDNegativeRtauPositiveBTag = fs->make<TH1F>("NonWeightedTauPtABCDNegRtauPosBTag", "NonWeightedTauPtABCDNegRtauPosBTag;tau p_{T} bin;N_{events} for ABCDNegRtauPosBTag", myCoefficientBinCount, 0., myCoefficientBinCount);
    fNonWeightedABCDNegativeRtauPositiveBTag->Sumw2();
    fNonWeightedABCDPositiveRtauNegativeBTag = fs->make<TH1F>("NonWeightedTauPtABCDPosRtauNegBTag", "NonWeightedTauPtABCDPosRtauNegBTag;tau p_{T} bin;N_{events} for ABCDPosRtauNegBTag", myCoefficientBinCount, 0., myCoefficientBinCount);
    fNonWeightedABCDPositiveRtauNegativeBTag->Sumw2();
    fNonWeightedABCDPositiveRtauPositiveBTag = fs->make<TH1F>("NonWeightedTauPtABCDPosRtauPosBTag", "NonWeightedTauPtABCDPosRtauPosBTag;tau p_{T} bin;N_{events} for ABCDPosRtauPosBTag", myCoefficientBinCount, 0., myCoefficientBinCount);
    fNonWeightedABCDPositiveRtauPositiveBTag->Sumw2();

    // Control histograms for P(MET>70)
    hMETPassProbabilityAfterJetSelection = fs->make<TH1F>("NonWeightedMETPassProbAfterJetSelection", "NonWeightedMETPassProbAfterJetSelection;tau p_{T} bin;N_{events} for MET after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterJetSelection->Sumw2();
    hMETPassProbabilityAfterTauIDNoRtau = fs->make<TH1F>("NonWeightedMETPassProbAfterTauIDNoRtau", "NonWeightedMETPassProbAfterTauIDNoRtau;tau p_{T} bin;N_{events} for MET after TauIDNoRtau", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterTauIDNoRtau->Sumw2();
    hMETPassProbabilityAfterTauID = fs->make<TH1F>("NonWeightedMETPassProbAfterTauID", "NonWeightedMETPassProbAfterTauID;tau p_{T} bin;N_{events} for MET after TauID", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterTauID->Sumw2();
    hMETPassProbabilityAfterBTagging = fs->make<TH1F>("NonWeightedMETPassProbAfterBTagging", "NonWeightedMETPassProbAfterBTagging;tau p_{T} bin;N_{events} for MET after b tagging", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterBTagging->Sumw2();
    hMETPassProbabilityAfterFakeMETVeto = fs->make<TH1F>("NonWeightedMETPassProbAfterFakeMETVeto", "NonWeightedMETPassProbAfterFakeMETVeto;tau p_{T} bin;N_{events} for MET after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterFakeMETVeto->Sumw2();
   }

  QCDMeasurementByMetFactorisationPart2::~QCDMeasurementByMetFactorisationPart2() {}

  void QCDMeasurementByMetFactorisationPart2::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void QCDMeasurementByMetFactorisationPart2::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Read the prescale for the event and set the event weight as the prescale
    fEventWeight.updatePrescale(iEvent);
    increment(fAllCounter);


    // Trigger and HLT_MET cut
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup); 
    if(!triggerData.passedEvent()) return;
    increment(fTriggerAndHLTMetCutCounter);


    // Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return;
    increment(fPrimaryVertexCounter);


    // Apply tau candidate selection (with or without Rtau control region)
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return;
    increment(fOneProngTauSelectionCounter);
    edm::PtrVector<pat::Tau> mySelectedTau;
    mySelectedTau.push_back(tauData.getSelectedTaus()[0]);
    double mySelectedTauPt = mySelectedTau[0]->pt();


    // GlobalElectronVeto 
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return; 
    increment(fGlobalElectronVetoCounter);


    // GlobalMuonVeto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return; 
    increment(fGlobalMuonVetoCounter);


    // Clean jet collection from selected tau and apply NJets>=3 cut
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, mySelectedTau);    
    if (jetData.getHadronicJetCount() >= 2) {
      increment(fJetSelectionCounter2);
    }
    if(!jetData.passedEvent()) return;
    increment(fJetSelectionCounter);

    // Get MET just for reference; do not apply a MET cut but instead use P(MET>70 GeV) as weight
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    hMETAfterJetSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());


    // Obtain weight for P(MET>70 GeV) and apply it
    double myEventWeightBeforeMetFactorization = fEventWeight.getWeight();
    fEventWeight.multiplyWeight(fFactorizationTable.getWeightByPtAndEta(mySelectedTauPt, 0.));
    int myFactorizationTableIndex = fFactorizationTable.getCoefficientTableIndexByPtAndEta(mySelectedTauPt,0.);
    hWeightedMETAfterJetSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hNonWeightedTauPtAfterJetSelection->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterJetSelection->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);


    // alphaT - No cuts applied! Only produces plots
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTaus()[0]), jetData.getSelectedJets());
    // increment(fEvtTopologyCounter);


    // InvMassVeto - No cuts applied! Only produces plots 
    InvMassVetoOnJets::Data invMassVetoOnJetsData =  fInvMassVetoOnJets.analyze( jetData.getSelectedJets() ); 
    // if(!invMassVetoOnJetsData.passedEvent()) return; 
    // increment(fInvMassVetoOnJetsCounter);

    
    // Obtain btagging and "fake MET veto" data objects
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets());
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, mySelectedTau, jetData.getSelectedJets());


    // Apply rest of tauID without Rtau
    TauSelection::Data tauDataForTauID = fOneProngTauSelection.analyzeTauIDWithoutRtauOnCleanedTauCandidates(iEvent, iSetup);
    if(!tauDataForTauID.passedEvent()) return;
    increment(fOneProngTauIDWithoutRtauCounter);
    hWeightedMETAfterTauIDNoRtau->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hNonWeightedTauPtAfterTauIDNoRtau->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterTauIDNoRtau->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    
    // Plot ABCD of btagging vs. rtau
    if (!btagData.passedEvent()) {
      if (!tauDataForTauID.selectedTauPassedRtau()) {
        fNonWeightedABCDNegativeRtauNegativeBTag->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
        increment(fABCDNegativeRtauNegativeBTagCounter);
      } else {
        fNonWeightedABCDPositiveRtauNegativeBTag->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
        increment(fABCDPositiveRtauNegativeBTagCounter);
      }
    } else {
      if (!tauDataForTauID.selectedTauPassedRtau()) {
        fNonWeightedABCDNegativeRtauPositiveBTag->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
        increment(fABCDNegativeRtauPositiveBTagCounter);
      } else {
        fNonWeightedABCDPositiveRtauPositiveBTag->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
        increment(fABCDPositiveRtauPositiveBTagCounter);
      }
    }

    // Apply Rtau cut (but only if tau selection is not done in reversed Rtau control region)
    if(!(tauDataForTauID.selectedTauPassedRtau() || !tauDataForTauID.shouldRtauBeAppliedOnSelectedTau())) 
      return;
    increment(fOneProngTauIDWithRtauCounter);
    hWeightedMETAfterTauID->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hNonWeightedTauPtAfterTauID->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterTauID->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);


    // BTagging
    if(!btagData.passedEvent()) return;
    increment(fBTaggingCounter);
    hWeightedMETAfterBTagging->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hNonWeightedTauPtAfterBTagging->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterBTagging->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);


    // FakeMETVeto
    if (!fakeMETData.passedEvent()) return;
    increment(fFakeMETVetoCounter);
    hWeightedMETAfterFakeMETVeto->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hNonWeightedTauPtAfterFakeMETVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterFakeMETVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);


    // Do final histogramming
    hRTauAfterAllSelections->Fill(tauDataForTauID.getRtauOfSelectedTau());
  }
}
