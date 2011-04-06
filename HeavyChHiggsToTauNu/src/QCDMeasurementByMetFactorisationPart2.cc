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
    fForwardJetVetoCounter(eventCounter.addCounter("forward jet veto")),
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
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, eventWeight),
    fFactorizationTable(iConfig, "METTables")
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
   {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms

    // Correlation histograms FIXME: move to separate class
    hTauIDMETCorrelationMETRightBeforeTauID = fs->make<TH1F>("QCDm3p2_METCorr_METRightBeforeTauID", "METRightBeforeTauID;MET, GeV;N / 5 GeV", 60, 0., 300.);
    hTauIDMETCorrelationMETRightBeforeTauID->Sumw2();
    hTauIDMETCorrelationMETRightAfterTauID = fs->make<TH1F>("QCDm3p2_METCorr_METRightAfterTauID", "METRightAfterTauID;MET, GeV;N / 5 GeV", 60, 0., 300.);
    hTauIDMETCorrelationMETRightAfterTauID->Sumw2();
    hTauIDMETCorrelationTauIDVsMETRightBeforeTauID = fs->make<TH2F>("QCDm3p2_METCorr_TauIDVsMETRightBeforeTauID", "TauID_Vs_MET;#tau-ID; MET, GeV ; N_{events} / 5 GeV", 3, -0.5, 1.5, 60, 0., 300. );
    hTauIDMETCorrelationTauIDVsMETRightBeforeTauID->Sumw2();
    // Histograms with weights
    hMETAfterJetSelection = fs->make<TH1F>("QCDm3p2_METctrl_METAfterJetSelection", "METAfterJetSelection;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hMETAfterJetSelection->Sumw2();
    hWeightedMETAfterJetSelection = fs->make<TH1F>("QCDm3p2_METctrl_METAfterJetSelectionWeighted", "METAfterJetSelectionWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterJetSelection->Sumw2();
    hWeightedMETAfterTauIDNoRtau = fs->make<TH1F>("QCDm3p2_METctrl_METAfterTauIDNoRtauWeighted", "METAfterTauIDNoRtauWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterTauIDNoRtau->Sumw2();
    hWeightedMETAfterTauID = fs->make<TH1F>("QCDm3p2_METctrl_METAfterTauIDWeighted", "METAfterTauIDWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterTauID->Sumw2();
    hWeightedMETAfterBTagging = fs->make<TH1F>("QCDm3p2_METctrl_METAfterBTaggingWeighted", "METAfterBTaggingWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterBTagging->Sumw2();
    hWeightedMETAfterFakeMETVeto = fs->make<TH1F>("QCDm3p2_METctrl_METAfterFakeMETVetoWeighted", "METAfterFakeMETVetoWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterFakeMETVeto->Sumw2();
    hWeightedMETAfterForwardJetVeto = fs->make<TH1F>("QCDm3p2_METctrl_METAfterForwardJetVetoWeighted", "METAfterForwardJetVetoWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterForwardJetVeto->Sumw2();
    // After all selections
    hWeightedTauPtAfterAllSelections = fs->make<TH1F>("QCDm3p2_weighted_TauPtAfterAllSelections", "TauPtAfterAllSelections;tau p_{T}, GeV/c;N_{events}/5", 60, 0., 300.);
    hWeightedTauPtAfterAllSelections->Sumw2();
    hWeightedTauEtaAfterAllSelections = fs->make<TH1F>("QCDm3p2_weighted_TauEtaAfterAllSelections", "TauEtaAfterAllSelections;tau #eta;N_{events}/0.1", 60, -3.0, 3.0);
    hWeightedTauEtaAfterAllSelections->Sumw2();
    hWeightedRTauAfterAllSelections = fs->make<TH1F>("QCDm3p2_weighted_RtauAfterAllSelections", "RTauAfterAllSelections;Rtau;N_{events}/0.02", 60, 0., 1.2);
    hWeightedRTauAfterAllSelections->Sumw2();
    hWeightedNJetsAfterAllSelections = fs->make<TH1F>("QCDm3p2_weighted_NJetsAfterAllSelections", "NJetsAfterAllSelections;N_{hadronic jets};N_{events}", 10, 0., 10.);
    hWeightedNJetsAfterAllSelections->Sumw2();
    hWeightedBJetsAfterAllSelections = fs->make<TH1F>("QCDm3p2_weighted_BJetsAfterAllSelections", "BJetsAfterAllSelections;N_{b-tagged jets};N_{events}", 10, 0., 10.);
    hWeightedBJetsAfterAllSelections->Sumw2();
    hWeightedMETAfterAllSelections = fs->make<TH1F>("QCDm3p2_weighted_METAfterAllSelections", "METAfterAllSelections;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterAllSelections->Sumw2();
    hWeightedFakeMETVetoAfterAllSelections = fs->make<TH1F>("QCDm3p2_weighted_FakeMETVetoAfterAllSelections", "FakeMETVetoAfterAllSelections;min(#Delta#phi(MET, jets)), degrees;N_{events} / 5 degrees", 36, 0., 180.);
    hWeightedFakeMETVetoAfterAllSelections->Sumw2();
    hWeightedDeltaPhiAfterAllSelections = fs->make<TH1F>("QCDm3p2_weighted_DeltaPhiAfterAllSelections", "DeltaPhiAfterAllSelections;#Delta#phi(MET, #tau), degrees;N_{events} / 5 degrees", 36, 0., 180.);
    hWeightedDeltaPhiAfterAllSelections->Sumw2();
    hWeightedTransverseMassAfterAllSelections = fs->make<TH1F>("QCDm3p2_weighted_TransverseMassAfterAllSelections", "TransverseMassAfterAllSelections;m_{T}(MET, #tau), GeV/c^{2};N_{events} / 5 GeV/c^{2}", 60, 0., 300.);
    hWeightedTransverseMassAfterAllSelections->Sumw2();

    // Histograms for later change of factorization map

    // MET factorization details
    createHistogramGroupByTauPt("QCDm3p2_METafterJetSelection");

    int myCoefficientBinCount = fFactorizationTable.getCoefficientTableSize();
    hMETFactorizationNJetsBefore = fs->make<TH1F>("QCDm3p2_METFactorization_NJetsBefore", "METFactorizationNJetsBefore;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationNJetsBefore->Sumw2();
    hMETFactorizationNJetsAfter = fs->make<TH1F>("QCDm3p2_METFactorization_NJetsAfter", "METFactorizationNJetsAfter;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationNJetsAfter->Sumw2();
    hMETFactorizationNJets = fs->make<TH2F>("QCDm3p2_METFactorization_NJets", "METFactorizationNJets;tau p_{T}, GeV/c;MET, GeV", 60, 0, 300., 60, 0., 300.);
    hMETFactorizationNJets->Sumw2();
    hMETFactorizationBJetsBefore = fs->make<TH1F>("QCDm3p2_METFactorization_BJetsBefore", "METFactorizationBJetsBefore;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationBJetsBefore->Sumw2();
    hMETFactorizationBJetsAfter = fs->make<TH1F>("QCDm3p2_METFactorization_BJetsAfter", "METFactorizationBJetsAfter;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationBJetsAfter->Sumw2();
    hMETFactorizationBJets = fs->make<TH2F>("QCDm3p2_METFactorization_BJets", "METFactorizationBJets;tau p_{T}, GeV/c;MET, GeV", 60, 0, 300., 60, 0., 300.);
    hMETFactorizationBJets->Sumw2();

    // Standard cut path
    hStdNonWeightedTauPtAfterJetSelection = fs->make<TH1F>("QCDm3p2_StdCutPath_TauPtAfterJetSelection", "NonWeightedTauPtAfterJetSelection;tau p_{T} bin;N_{events} after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterJetSelection->Sumw2();
    hStdNonWeightedTauPtAfterTauIDNoRtau = fs->make<TH1F>("QCDm3p2_StdCutPath_TauPtAfterTauIDNoRtau", "NonWeightedTauPtAfterTauIDNoRtau;tau p_{T} bin;N_{events} after TauIDNoRtau", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterTauIDNoRtau->Sumw2();
    hStdNonWeightedTauPtAfterTauID = fs->make<TH1F>("QCDm3p2_StdCutPath_TauPtAfterTauID", "NonWeightedTauPtAfterTauID;tau p_{T} bin;N_{events} after TauID", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterTauID->Sumw2();
    hStdNonWeightedTauPtAfterBTagging = fs->make<TH1F>("QCDm3p2_StdCutPath_TauPtAfterBTagging", "NonWeightedTauPtAfterBTagging;tau p_{T} bin;N_{events} after b tagging", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterBTagging->Sumw2();
    hStdNonWeightedTauPtAfterFakeMETVeto = fs->make<TH1F>("QCDm3p2_StdCutPath_TauPtAfterFakeMETVeto", "NonWeightedTauPtAfterFakeMETVeto;tau p_{T} bin;N_{events} after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterFakeMETVeto->Sumw2();
    hStdNonWeightedTauPtAfterForwardJetVeto = fs->make<TH1F>("QCDm3p2_StdCutPath_TauPtAfterForwardJetVeto", "NonWeightedTauPtAfterForwardJetVeto;tau p_{T} bin;N_{events} after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterForwardJetVeto->Sumw2();
    hStdWeightedRtau = fs->make<TH1F>("QCDm3p2_StdCutPath_weighted_Rtau", "Rtau;Rtau;N_{events}/0.02", 60, 0., 1.2);
    hStdWeightedRtau->Sumw2();
    hStdWeightedBjets = fs->make<TH1F>("QCDm3p2_StdCutPath_weighted_Bjets", "Bjets;N_{b-tagged jets};N_{events}", 10, 0., 10.);
    hStdWeightedBjets->Sumw2();
    hStdWeightedFakeMETVeto = fs->make<TH1F>("QCDm3p2_StdCutPath_weighted_FakeMETVeto", "FakeMETVeto;min(#Delta#phi(MET, jets)), degrees;N_{events} / 5 degrees", 36, 0., 180.);
    hStdWeightedFakeMETVeto->Sumw2();

    // Standard cuts with factorized rtau and b-tagging
    hFactRtauBNonWeightedTauPtAfterJetSelection = fs->make<TH1F>("QCDm3p2_FactRtauBCutPath_TauPtAfterJetSelection", "NonWeightedTauPtAfterJetSelection;tau p_{T} bin;N_{events} after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBNonWeightedTauPtAfterJetSelection->Sumw2();
    hFactRtauBNonWeightedTauPtAfterTauIDNoRtau = fs->make<TH1F>("QCDm3p2_FactRtauBCutPath_TauPtAfterTauIDNoRtau", "NonWeightedTauPtAfterTauIDNoRtau;tau p_{T} bin;N_{events} after TauIDNoRtau", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBNonWeightedTauPtAfterTauIDNoRtau->Sumw2();
    hFactRtauBNonWeightedTauPtAfterTauID = fs->make<TH1F>("QCDm3p2_FactRtauBCutPath_TauPtAfterTauID", "NonWeightedTauPtAfterTauID;tau p_{T} bin;N_{events} after TauID", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBNonWeightedTauPtAfterTauID->Sumw2();
    hFactRtauBNonWeightedTauPtAfterBTagging = fs->make<TH1F>("QCDm3p2_FactRtauBCutPath_TauPtAfterBTagging", "NonWeightedTauPtAfterBTagging;tau p_{T} bin;N_{events} after b tagging", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBNonWeightedTauPtAfterBTagging->Sumw2();
    hFactRtauBNonWeightedTauPtAfterFakeMETVeto = fs->make<TH1F>("QCDm3p2_FactRtauBCutPath_TauPtAfterFakeMETVeto", "NonWeightedTauPtAfterFakeMETVeto;tau p_{T} bin;N_{events} after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBNonWeightedTauPtAfterFakeMETVeto->Sumw2();
    hFactRtauBNonWeightedTauPtAfterForwardJetVeto = fs->make<TH1F>("QCDm3p2_FactRtauBCutPath_TauPtAfterForwardJetVeto", "NonWeightedTauPtAfterForwardJetVeto;tau p_{T} bin;N_{events} after forward jet veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBNonWeightedTauPtAfterForwardJetVeto->Sumw2();

    // Standard cuts with factorized rtau and b-tagging
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterJetSelection = fs->make<TH1F>("QCDm3p2_FactRtauBBeforeTauIDCutPath_TauPtAfterJetSelection", "NonWeightedTauPtAfterJetSelection;tau p_{T} bin;N_{events} after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterJetSelection->Sumw2();
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterTauIDNoRtau = fs->make<TH1F>("QCDm3p2_FactRtauBBeforeTauIDCutPath_TauPtAfterTauIDNoRtau", "NonWeightedTauPtAfterTauIDNoRtau;tau p_{T} bin;N_{events} after TauIDNoRtau", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterTauIDNoRtau->Sumw2();
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterTauID = fs->make<TH1F>("QCDm3p2_FactRtauBBeforeTauIDCutPath_TauPtAfterTauID", "NonWeightedTauPtAfterTauID;tau p_{T} bin;N_{events} after TauID", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterTauID->Sumw2();
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterBTagging = fs->make<TH1F>("QCDm3p2_FactRtauBBeforeTauIDCutPath_TauPtAfterBTagging", "NonWeightedTauPtAfterBTagging;tau p_{T} bin;N_{events} after b tagging", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterBTagging->Sumw2();
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterFakeMETVeto = fs->make<TH1F>("QCDm3p2_FactRtauBBeforeTauIDCutPath_TauPtAfterFakeMETVeto", "NonWeightedTauPtAfterFakeMETVeto;tau p_{T} bin;N_{events} after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterFakeMETVeto->Sumw2();
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterForwardJetVeto = fs->make<TH1F>("QCDm3p2_FactRtauBBeforeTauIDCutPath_TauPtAfterForwardJetVeto", "NonWeightedTauPtAfterForwardJetVeto;tau p_{T} bin;N_{events} after forward jet veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterForwardJetVeto->Sumw2();

    // ABCD(tau isol. vs. b-tag) cut path
    for (int i = 0; i < 4; i++) {
      std::string myRegion;
      if (i == 0) myRegion = "NegNeg";
      else if (i == 1) myRegion = "NegPos";
      else if (i == 2) myRegion = "PosNeg";
      else if (i == 3) myRegion = "PosPos";

      std::stringstream myLabel;
      myLabel << "QCDm3p2_ABCDTauIsolB_TauPtAfterJetSelection_" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterJetSelection[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterJetSelection;tau p_{T} bin;N_{events} after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBNonWeightedTauPtAfterJetSelection[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCDm3p2_ABCDTauIsolB_TauPtvsMET" << myRegion;
      hABCDTauIsolBNonWeightedTauPtVsMET[i] = fs->make<TH2F>(myLabel.str().c_str(), "NonWeightedTauPtvsMET;tau p_{T}, GeV/c;MET, GeV", 60, 0, 300., 60, 0., 300.);
      hABCDTauIsolBNonWeightedTauPtVsMET[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCDm3p2_ABCDTauIsolB_TauPtAfterMET" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterMET[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterMET;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBNonWeightedTauPtAfterMET[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCDm3p2_ABCDTauIsolB_TauPtAfterRtau" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterRtau[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBNonWeightedTauPtAfterRtau[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCDm3p2_ABCDTauIsolB_TauPtAfterFakeMETVeto" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterFakeMETVeto[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterFakeMETVeto;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBNonWeightedTauPtAfterFakeMETVeto[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCDm3p2_ABCDTauIsolB_TauPtAfterForwardJetVeto" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterForwardJetVeto[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterForwardJetVeto;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBNonWeightedTauPtAfterForwardJetVeto[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCDm3p2_ABCDTauIsolB_TauPtAfterFakeMETVetoWithFactorizedRtau" << myRegion;
      hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterFakeMETVeto[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterFakeMETVetoWithFactorizedRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterFakeMETVeto[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCDm3p2_ABCDTauIsolB_TauPtAfterForwardJetVetoWithFactorizedRtau" << myRegion;
      hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterForwardJetVeto[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterForwardJetVetoWithFactorizedRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterForwardJetVeto[i]->Sumw2();
    }

    // Control histograms for P(MET>70)
    hMETPassProbabilityAfterJetSelection = fs->make<TH1F>("QCDm3p2_NoWeight_METPassProbAfterJetSelection", "NonWeightedMETPassProbAfterJetSelection;tau p_{T} bin;N_{events} for MET after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterJetSelection->Sumw2();
    hMETPassProbabilityAfterTauIDNoRtau = fs->make<TH1F>("QCDm3p2_NoWeight_METPassProbAfterTauIDNoRtau", "NonWeightedMETPassProbAfterTauIDNoRtau;tau p_{T} bin;N_{events} for MET after TauIDNoRtau", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterTauIDNoRtau->Sumw2();
    hMETPassProbabilityAfterTauID = fs->make<TH1F>("QCDm3p2_NoWeight_METPassProbAfterTauID", "NonWeightedMETPassProbAfterTauID;tau p_{T} bin;N_{events} for MET after TauID", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterTauID->Sumw2();
    hMETPassProbabilityAfterBTagging = fs->make<TH1F>("QCDm3p2_NoWeight_METPassProbAfterBTagging", "NonWeightedMETPassProbAfterBTagging;tau p_{T} bin;N_{events} for MET after b tagging", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterBTagging->Sumw2();
    hMETPassProbabilityAfterFakeMETVeto = fs->make<TH1F>("QCDm3p2_NoWeight_METPassProbAfterFakeMETVeto", "NonWeightedMETPassProbAfterFakeMETVeto;tau p_{T} bin;N_{events} for MET after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterFakeMETVeto->Sumw2();
    hMETPassProbabilityAfterForwardJetVeto = fs->make<TH1F>("QCDm3p2_NoWeight_METPassProbAfterForwardJetVeto", "NonWeightedMETPassProbAfterForwardJetVeto;tau p_{T} bin;N_{events} for MET after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterForwardJetVeto->Sumw2();
   }

  QCDMeasurementByMetFactorisationPart2::~QCDMeasurementByMetFactorisationPart2() {}

  void QCDMeasurementByMetFactorisationPart2::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void QCDMeasurementByMetFactorisationPart2::createHistogramGroupByTauPt(std::string name) {
    // Get tau pt edge table
    fFactorizationBinLowEdges = fFactorizationTable.getBinLowEdges();
    // Make histograms
    edm::Service<TFileService> fs;
    size_t myTableSize = fFactorizationBinLowEdges.size(); 
    int myMETBins = 20; // number of bins for the histograms
    double myMETMin = 0.; // MET range minimum
    double myMETMax = 100.; // MET range maximum
    std::stringstream myHistoName;
    std::stringstream myHistoLabel;
    for (size_t i = 0; i < myTableSize; ++i) {
      myHistoName.str("");
      myHistoLabel.str("");
      if (i == 0) {
	// Treat first bin
	myHistoName << name << "TauPtRangeBelow" << fFactorizationBinLowEdges[0];
	myHistoLabel << name << "TauPtRangeBelow" << fFactorizationBinLowEdges[0] <<";MET, GeV;N/" 
		     << static_cast<int>((myMETMax-myMETMin)/myMETBins) << " GeV"; 
	fMETHistogramsByTauPt.push_back(fs->make<TH1F>(myHistoName.str().c_str(), 
						       myHistoLabel.str().c_str(), myMETBins, myMETMin, myMETMax));
      } else {
	myHistoName << name << "TauPtRange" << fFactorizationBinLowEdges[i-1] << "to" << fFactorizationBinLowEdges[i];
	myHistoLabel << name << "TauPtRange" << fFactorizationBinLowEdges[i-1] << "to" << fFactorizationBinLowEdges[i] << ";MET, GeV;N/" 
		     << static_cast<int>((myMETMax-myMETMin)/myMETBins) << " GeV"; 
	fMETHistogramsByTauPt.push_back(fs->make<TH1F>(myHistoName.str().c_str(), 
						       myHistoLabel.str().c_str(), myMETBins, myMETMin, myMETMax));
      }
    }
    // Treat last bin
    myHistoName.str("");
    myHistoLabel.str("");
    myHistoName << name << "TauPtRangeAbove" << fFactorizationBinLowEdges[myTableSize-1];
    myHistoLabel << name << "TauPtRangeAbove" << fFactorizationBinLowEdges[myTableSize-1] <<";MET, GeV;N/" 
		 << static_cast<int>((myMETMax-myMETMin)/myMETBins) << " GeV"; 
    fMETHistogramsByTauPt.push_back(fs->make<TH1F>(myHistoName.str().c_str(), 
						   myHistoLabel.str().c_str(), myMETBins, myMETMin, myMETMax));
    // Apply sumw2 on the histograms
    for (std::vector<TH1*>::iterator it = fMETHistogramsByTauPt.begin(); it != fMETHistogramsByTauPt.end(); ++it) {
      (*it)->Sumw2();
    }
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


    // Get MET just for reference; do not apply a MET cut but instead use P(MET>70 GeV) as weight
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    hMETAfterJetSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());


    // Apply tau candidate selection (with or without Rtau control region)
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return;
    increment(fOneProngTauSelectionCounter);
    edm::PtrVector<pat::Tau> mySelectedTau;
    mySelectedTau.push_back(tauData.getSelectedTaus()[0]);
    double mySelectedTauPt = mySelectedTau[0]->pt();
    int myFactorizationTableIndex = fFactorizationTable.getCoefficientTableIndexByPtAndEta(mySelectedTauPt,0.);


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

    // Fill factorization info into histogram
    fMETHistogramsByTauPt[myFactorizationTableIndex]->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hMETFactorizationNJetsBefore->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
    if (metData.passedEvent())
      hMETFactorizationNJetsAfter->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
    hMETFactorizationNJets->Fill(mySelectedTau[0]->pt(), metData.getSelectedMET()->et(), fEventWeight.getWeight());

    // Obtain weight for P(MET>70 GeV) and apply it
    double myEventWeightBeforeMetFactorization = fEventWeight.getWeight();
    fEventWeight.multiplyWeight(fFactorizationTable.getWeightByPtAndEta(mySelectedTauPt, 0.));
    hWeightedMETAfterJetSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterJetSelection->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterJetSelection->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);

    // alphaT - No cuts applied! Only produces plots
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(mySelectedTau[0]), jetData.getSelectedJets());
    // increment(fEvtTopologyCounter);


    // InvMassVeto - No cuts applied! Only produces plots 
    InvMassVetoOnJets::Data invMassVetoOnJetsData =  fInvMassVetoOnJets.analyze( jetData.getSelectedJets() ); 
    // if(!invMassVetoOnJetsData.passedEvent()) return; 
    // increment(fInvMassVetoOnJetsCounter);

    
    // Obtain btagging, fakeMETVeto, and forwardJetVeto data objects - internal plots will be wrong since they are not produced at the spot where the cut is applied
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets());
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, mySelectedTau, jetData.getSelectedJets());
    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    // Obtain tau ID data object
    TauSelection::Data tauDataForTauID = fOneProngTauSelection.analyzeTauIDWithoutRtauOnCleanedTauCandidates(iEvent, iSetup);
    
    // Obtain P(MET) after b-tagging; alternative for b-tag factorization
    if (btagData.passedEvent()) {
      hMETFactorizationBJetsBefore->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
      if (metData.passedEvent()) {
	hMETFactorizationBJetsAfter->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
      }
      hMETFactorizationBJets->Fill(mySelectedTau[0]->pt(), metData.getSelectedMET()->et(), myEventWeightBeforeMetFactorization);
    }

    // Apply non-standard cut paths
    analyzeABCDByTauIsolationAndBTagging(metData, mySelectedTau, tauDataForTauID, btagData, fakeMETData, forwardJetData, myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    analyzeFactorizedBTaggingAndRtau(tauDataForTauID, btagData, fakeMETData, forwardJetData, myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    analyzeFactorizedBTaggingBeforeTauIDAndRtau(tauDataForTauID, btagData, fakeMETData, forwardJetData, myFactorizationTableIndex, myEventWeightBeforeMetFactorization);

    // Continue standard cut path

    // Apply rest of tauID without Rtau
    hTauIDMETCorrelationTauIDVsMETRightBeforeTauID->Fill(tauDataForTauID.passedEvent(), metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hTauIDMETCorrelationMETRightBeforeTauID->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight()); // FIXME
    if(!tauDataForTauID.passedEvent()) return;
    increment(fOneProngTauIDWithoutRtauCounter);
    hWeightedMETAfterTauIDNoRtau->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterTauIDNoRtau->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterTauIDNoRtau->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);

    // Apply Rtau cut (but only if tau selection is not done in reversed Rtau control region)
    hStdWeightedRtau->Fill(tauDataForTauID.getRtauOfSelectedTau(), fEventWeight.getWeight());
    if(!tauDataForTauID.selectedTauPassedRtau()) return;
    increment(fOneProngTauIDWithRtauCounter);
    hWeightedMETAfterTauID->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterTauID->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterTauID->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    hTauIDMETCorrelationMETRightAfterTauID->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight()); // FIXME


    // BTagging
    hStdWeightedBjets->Fill(btagData.getBJetCount(), fEventWeight.getWeight());
    if(!btagData.passedEvent()) return;
    increment(fBTaggingCounter);
    hWeightedMETAfterBTagging->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterBTagging->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterBTagging->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);


    // FakeMETVeto
    hStdWeightedFakeMETVeto->Fill(fakeMETData.closestDeltaPhi(), fEventWeight.getWeight());
    if (!fakeMETData.passedEvent()) return;
    increment(fFakeMETVetoCounter);
    hWeightedMETAfterFakeMETVeto->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterFakeMETVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterFakeMETVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);


    // Do final histogramming
    hWeightedTauPtAfterAllSelections->Fill(mySelectedTau[0]->pt(), fEventWeight.getWeight());
    hWeightedTauEtaAfterAllSelections->Fill(mySelectedTau[0]->eta(), fEventWeight.getWeight());
    hWeightedRTauAfterAllSelections->Fill(tauDataForTauID.getRtauOfSelectedTau(), fEventWeight.getWeight());
    hWeightedNJetsAfterAllSelections->Fill(jetData.getHadronicJetCount(), fEventWeight.getWeight());
    hWeightedBJetsAfterAllSelections->Fill(btagData.getBJetCount(), fEventWeight.getWeight());
    hWeightedMETAfterAllSelections->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hWeightedFakeMETVetoAfterAllSelections->Fill(fakeMETData.closestDeltaPhi(), fEventWeight.getWeight());
    hWeightedDeltaPhiAfterAllSelections->Fill(fDeltaPhi.reconstruct(*(mySelectedTau[0]), *(metData.getSelectedMET()))*180.0/3.14159, fEventWeight.getWeight());
    hWeightedTransverseMassAfterAllSelections->Fill(fTransverseMass.reconstruct(*(mySelectedTau[0]), *(metData.getSelectedMET())), fEventWeight.getWeight());


    // Forward jet veto -- experimental
    if (!forwardJetData.passedEvent()) return;
    increment(fForwardJetVetoCounter);
    hWeightedMETAfterForwardJetVeto->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterForwardJetVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterForwardJetVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
  }

  void QCDMeasurementByMetFactorisationPart2::analyzeABCDByTauIsolationAndBTagging(const METSelection::Data& METData, edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data forwardData, int tauPtBin, double weightWithoutMET) {
    // Divide phase space into ABCD regions
    int myIndex = 0;
    if (!tauData.passedEvent()) {
      if (!btagData.passedEvent()) {
	myIndex = 0; // NegNeg
      } else {
	myIndex = 1; // NegPos
      }
    } else {
      if (!btagData.passedEvent()) {
	myIndex = 2; // PosNeg
      } else {
	myIndex = 3; // PosPos
      }
    }
    // Do cut flow in proper phase space
    hABCDTauIsolBNonWeightedTauPtAfterJetSelection[myIndex]->Fill(tauPtBin, weightWithoutMET);
    hABCDTauIsolBNonWeightedTauPtVsMET[myIndex]->Fill(selectedTau[0]->pt(), METData.getSelectedMET()->et());
    // ... obtain P(MET)
    if (METData.passedEvent()) hABCDTauIsolBNonWeightedTauPtAfterMET[myIndex]->Fill(tauPtBin, weightWithoutMET);
    // ... apply Rtau
    if (tauData.selectedTauPassedRtau()) {
      hABCDTauIsolBNonWeightedTauPtAfterRtau[myIndex]->Fill(tauPtBin, weightWithoutMET);
      if (fakeMETData.passedEvent()) {
        hABCDTauIsolBNonWeightedTauPtAfterFakeMETVeto[myIndex]->Fill(tauPtBin, weightWithoutMET);
	if (forwardData.passedEvent()) {
	  hABCDTauIsolBNonWeightedTauPtAfterForwardJetVeto[myIndex]->Fill(tauPtBin, weightWithoutMET);
	}
      }
    }
    // ... Apply fake MET veto for case where Rtau is factorized out
    if (fakeMETData.passedEvent()) {
      hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterFakeMETVeto[myIndex]->Fill(tauPtBin, weightWithoutMET);
      if (forwardData.passedEvent()) {
	hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterForwardJetVeto[myIndex]->Fill(tauPtBin, weightWithoutMET);
      }
    }
  }

  void QCDMeasurementByMetFactorisationPart2::analyzeFactorizedBTaggingAndRtau(const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data forwardData, int tauPtBin, double weightWithoutMET) {
    hFactRtauBNonWeightedTauPtAfterJetSelection->Fill(tauPtBin, weightWithoutMET);
    // Apply TauID isolation and N prongs
    if (!tauData.passedEvent()) return;
    hFactRtauBNonWeightedTauPtAfterTauIDNoRtau->Fill(tauPtBin, weightWithoutMET);

    // Handle Rtau
    if (tauData.selectedTauPassedRtau())
      hFactRtauBNonWeightedTauPtAfterTauID->Fill(tauPtBin, weightWithoutMET);

    // Handle btagging
    if (btagData.passedEvent())
      hFactRtauBNonWeightedTauPtAfterBTagging->Fill(tauPtBin, weightWithoutMET);
    
    // Apply Fake MET veto
    if (!fakeMETData.passedEvent()) return;
    hFactRtauBNonWeightedTauPtAfterFakeMETVeto->Fill(tauPtBin, weightWithoutMET);

    // Apply Forward jet veto
    if (!forwardData.passedEvent()) return;
    hFactRtauBNonWeightedTauPtAfterForwardJetVeto->Fill(tauPtBin, weightWithoutMET);
  }

  void QCDMeasurementByMetFactorisationPart2::analyzeFactorizedBTaggingBeforeTauIDAndRtau(const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data forwardData, int tauPtBin, double weightWithoutMET) {
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterJetSelection->Fill(tauPtBin, weightWithoutMET);

    // Handle btagging
    if (btagData.passedEvent())
      hFactRtauBBeforeTauIDNonWeightedTauPtAfterBTagging->Fill(tauPtBin, weightWithoutMET);

    // Apply TauID isolation and N prongs
    if (!tauData.passedEvent()) return;
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterTauIDNoRtau->Fill(tauPtBin, weightWithoutMET);

    // Handle Rtau
    if (tauData.selectedTauPassedRtau())
      hFactRtauBBeforeTauIDNonWeightedTauPtAfterTauID->Fill(tauPtBin, weightWithoutMET);
    
    // Apply Fake MET veto
    if (!fakeMETData.passedEvent()) return;
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterFakeMETVeto->Fill(tauPtBin, weightWithoutMET);

    // Apply Forward jet veto
    if (!forwardData.passedEvent()) return;
    hFactRtauBBeforeTauIDNonWeightedTauPtAfterForwardJetVeto->Fill(tauPtBin, weightWithoutMET);
  }

}
