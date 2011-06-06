#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurement.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  QCDMeasurement::QCDMeasurement(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    fAllCounter(eventCounter.addCounter("allEvents")),
    fTriggerAndHLTMetCutCounter(eventCounter.addCounter("Trigger_and_HLT_MET")),
    fPrimaryVertexCounter(eventCounter.addCounter("PrimaryVertex")),
    fOneProngTauSelectionCounter(eventCounter.addCounter("TauCandSelection")),
    fOneSelectedTauCounter(eventCounter.addCounter("TauCands==1")),
    fGlobalElectronVetoCounter(eventCounter.addCounter("GlobalElectronVeto")),
    fGlobalMuonVetoCounter(eventCounter.addCounter("GlobalMuonVeto")),
    fJetSelectionCounter2(eventCounter.addCounter("Njets==2")),
    fJetSelectionCounter(eventCounter.addCounter("JetSelection")),
    fMETCounter(eventCounter.addCounter("MET")),
    fOneProngTauIDWithoutRtauCounter(eventCounter.addCounter("TauID_noRtau")),
    fOneProngTauIDWithRtauCounter(eventCounter.addCounter("TauID_withRtau")),
    fInvMassVetoOnJetsCounter(eventCounter.addCounter("InvMassVetoOnJets")), // dumbie
    fEvtTopologyCounter(eventCounter.addCounter("EvtTopology")),             // dumbie
    fBTaggingCounter(eventCounter.addCounter("bTagging")),
    fFakeMETVetoCounter(eventCounter.addCounter("FakeMETVeto")),
    fTopSelectionCounter(eventCounter.addCounter("Top Selection cut")),
    fForwardJetVetoCounter(eventCounter.addCounter("forward jet veto")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    //fTriggerTauMETEmulation(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"), eventCounter, eventWeight),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, eventWeight),
    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, 1, "tauCandidate"),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight, "MET"),
    fInvMassVetoOnJets(iConfig.getUntrackedParameter<edm::ParameterSet>("InvMassVetoOnJets"), eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, eventWeight),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, eventWeight),
    fWeightedSelectedEventsAnalyzer("QCDm3p2_afterAllSelections_weighted"),
    fNonWeightedSelectedEventsAnalyzer("QCDm3p2_afterAllSelections_nonWeighted"),
    fPFTauIsolationCalculator(iConfig.getUntrackedParameter<edm::ParameterSet>("tauIsolationCalculator")),
    fGenparticleAnalysis(eventCounter, eventWeight),
    fVertexWeight(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeight")),
    fFactorizationTable(iConfig, "METTables")
    // fTriggerEmulationEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"))
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
   {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms
    hVerticesBeforeWeight = makeTH<TH1F>(*fs, "verticesBeforeWeight", "Number of vertices without weightingVertices;N_{events} / 1 Vertex", 30, 0, 30);

    // Histograms with weights
    hVerticesAfterWeight =  makeTH<TH1F>(*fs, "verticesAfterWeight", "Number of vertices with weighting; Vertices;N_{events} / 1 Vertex", 30, 0, 30);
    hMETAfterJetSelection = makeTH<TH1F>(*fs, "QCD_METctrl_METAfterJetSelection", "METAfterJetSelection;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterJetSelection = makeTH<TH1F>(*fs, "QCD_METctrl_METAfterJetSelectionWeighted", "METAfterJetSelectionWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterTauIDNoRtau = makeTH<TH1F>(*fs, "QCD_METctrl_METAfterTauIDNoRtauWeighted", "METAfterTauIDNoRtauWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterTauID = makeTH<TH1F>(*fs, "QCD_METctrl_METAfterTauIDWeighted", "METAfterTauIDWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterBTagging = makeTH<TH1F>(*fs, "QCD_METctrl_METAfterBTaggingWeighted", "METAfterBTaggingWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterFakeMETVeto = makeTH<TH1F>(*fs, "QCD_METctrl_METAfterFakeMETVetoWeighted", "METAfterFakeMETVetoWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterForwardJetVeto = makeTH<TH1F>(*fs, "QCD_METctrl_METAfterForwardJetVetoWeighted", "METAfterForwardJetVetoWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);

    // Histograms in bins of another variable: in bins of tau pt
    createHistogramGroupByOtherVariableBins("QCD_MET_afterTauCandidateSelection_", fMETHistogramsByTauPtAfterTauCandidateSelection, 20, 0.0, 100.0, fFactorizationTable.getBinLowEdges(), "TauPt", "E_{T}^{miss}", "GeV");
    createHistogramGroupByOtherVariableBins("QCD_Counter_afterJetsMetBtag_", fCounterAfterJetsMetBtagByTauPt, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "pass", "");
    createHistogramGroupByOtherVariableBins("QCD_Counter_afterJetsMetBtagFakeMet_", fCounterAfterJetsMetBtagFakeMetByTauPt, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "pass", "");
    createHistogramGroupByOtherVariableBins("QCD_Counter_afterJetsTauIdNoRtau_", fCounterAfterJetsTauIdNoRtauByTauPt, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "pass", "");
    createHistogramGroupByOtherVariableBins("QCD_Counter_afterJetsTauIdNoRtauFakeMet_", fCounterAfterJetsTauIdNoRtauFakeMetByTauPt, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "pass", "");
    createHistogramGroupByOtherVariableBins("QCD_MET_afterJetSelection_", fMETHistogramsByTauPtAfterJetSelection, 20, 0.0, 100.0, fFactorizationTable.getBinLowEdges(), "TauPt", "E_{T}^{miss}", "GeV");
    createHistogramGroupByOtherVariableBins("QCD_MET_afterTauIsolation_", fMETHistogramsByTauPtAfterTauIsolation, 20, 0.0, 100.0, fFactorizationTable.getBinLowEdges(), "TauPt", "E_{T}^{miss}", "GeV");
    createHistogramGroupByOtherVariableBins("QCD_NBtags_afterJetSelection_", fNBtagsHistogramsByTauPtAfterJetSelection, 16, -0.5, 15.5, fFactorizationTable.getBinLowEdges(), "TauPt", "NBtags", "");
    createHistogramGroupByOtherVariableBins("QCD_NBtags_afterTauIdNoRtau_", fNBtagsHistogramsByTauPtAfterTauIdNoRtau, 16, -0.5, 15.5, fFactorizationTable.getBinLowEdges(), "TauPt", "NBtags", "");
    createHistogramGroupByOtherVariableBins("QCD_NBtags_afterTauIdAndRtau_", fNBtagsHistogramsByTauPtAfterTauIdAndRtau, 16, -0.5, 15.5, fFactorizationTable.getBinLowEdges(), "TauPt", "NBtags", "");

    //  Histograms in bins of another variable: in bins of MET
    createHistogramGroupByOtherVariableBins("QCD_LdgJetPt_afterJetSelection_", fLdgJetPtHistogramGroupByMET, 100, 0.0, 500.0, getMetBins(), "MET", "E_{T}^{LdgJet}", "GeV");
    createHistogramGroupByOtherVariableBins("QCD_NBtags_afterJetSelection_", fNBtagsHistogramGroupByMET, 16, -0.5, 15.5, getMetBins(), "MET", "NBtags", "");
    createHistogramGroupByOtherVariableBins("QCD_FakeMETVeto_afterJetSelection_", fFakeMETVetoHistogramGroupByMET, 36, 0.0, 180.0, getMetBins(), "MET", "#Delta#phi(MET, jets)_{min}", "degrees");
    createHistogramGroupByOtherVariableBins("QCD_NBquarks_afterJetSelection_", fNBquarksHistogramGroupByMET, 16, -0.5, 15.5, getMetBins(), "MET", "NBquarks", "");
    createHistogramGroupByOtherVariableBins("QCD_NBquarksStatus2_afterJetSelection_", fNBquarksStatus2HistogramGroupByMET, 16, -0.5, 15.5, getMetBins(), "MET", "NBquarks(st=2)", "");
    createHistogramGroupByOtherVariableBins("QCD_NBquarksStatus3_afterJetSelection_", fNBquarksStatus3HistogramGroupByMET, 16, -0.5, 15.5, getMetBins(), "MET", "NBquarks(st=3)", "");
    //  Histograms in bins of another variable: in  bins of Ldg Jet Pt 
    createHistogramGroupByOtherVariableBins("QCD_MET_afterJetSelection_", fMETHistogramGroupByLdgJetPt, 50, 0.0, 250.0, getJetPtBins(), "LdgJetPt", "MET", "GeV");

    // Purity
    createHistogramGroupByOtherVariableBins("QCD_Purity_BeforeAfterJets_", fPurityBeforeAfterJets, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "GeV/c", "passCut");
    createHistogramGroupByOtherVariableBins("QCD_Purity_BeforeAfterJetsMet_",fPurityBeforeAfterJetsMet , 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "GeV/c", "passCut");
    createHistogramGroupByOtherVariableBins("QCD_Purity_BeforeAfterJetsMetBtag_", fPurityBeforeAfterJetsMetBtag, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "GeV/c", "passCut");
    createHistogramGroupByOtherVariableBins("QCD_Purity_BeforeAfterJetsFakeMet_", fPurityBeforeAfterJetsFakeMet, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "GeV/c", "passCut");
    createHistogramGroupByOtherVariableBins("QCD_Purity_BeforeAfterJetsTauIdNoRtau_", fPurityBeforeAfterJetsTauIdNoRtau, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "GeV/c", "passCut");
        
    // Histograms for later change of factorization map
    // MET factorization details
    int myCoefficientBinCount = fFactorizationTable.getCoefficientTableSize();
    hMETFactorizationNJetsBefore = makeTH<TH1F>(*fs, "QCD_METFactorization_NJetsBefore", "METFactorizationNJetsBefore;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationNJetsAfter = makeTH<TH1F>(*fs, "QCD_METFactorization_NJetsAfter", "METFactorizationNJetsAfter;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationNJets = makeTH<TH2F>(*fs, "QCD_METFactorization_NJets", "METFactorizationNJets;tau p_{T}, GeV/c;MET, GeV", 60, 0, 300., 60, 0., 300.);
    hMETFactorizationBJetsBefore = makeTH<TH1F>(*fs, "QCD_METFactorization_BJetsBefore", "METFactorizationBJetsBefore;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationBJetsAfter = makeTH<TH1F>(*fs, "QCD_METFactorization_BJetsAfter", "METFactorizationBJetsAfter;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationBJets = makeTH<TH2F>(*fs, "QCD_METFactorization_BJets", "METFactorizationBJets;tau p_{T}, GeV/c;MET, GeV", 60, 0, 300., 60, 0., 300.);

    // Standard cut path
    hStdNonWeightedTauPtAfterJetSelection = makeTH<TH1F>(*fs, "QCD_StdCutPath_TauPtAfterJetSelection", "NonWeightedTauPtAfterJetSelection;tau p_{T} bin;N_{events} after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterTauIDNoRtau = makeTH<TH1F>(*fs, "QCD_StdCutPath_TauPtAfterTauIDNoRtau", "NonWeightedTauPtAfterTauIDNoRtau;tau p_{T} bin;N_{events} after TauIDNoRtau", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterTauID = makeTH<TH1F>(*fs, "QCD_StdCutPath_TauPtAfterTauID", "NonWeightedTauPtAfterTauID;tau p_{T} bin;N_{events} after TauID", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterBTagging = makeTH<TH1F>(*fs, "QCD_StdCutPath_TauPtAfterBTagging", "NonWeightedTauPtAfterBTagging;tau p_{T} bin;N_{events} after b tagging", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterFakeMETVeto = makeTH<TH1F>(*fs, "QCD_StdCutPath_TauPtAfterFakeMETVeto", "NonWeightedTauPtAfterFakeMETVeto;tau p_{T} bin;N_{events} after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterForwardJetVeto = makeTH<TH1F>(*fs, "QCD_StdCutPath_TauPtAfterForwardJetVeto", "NonWeightedTauPtAfterForwardJetVeto;tau p_{T} bin;N_{events} after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterRtauWithoutNjetsBeforeCut = makeTH<TH1F>(*fs, "QCD_StdCutPath_TauPtAfter_noNjets_Rtau_before", "Rtau;tau pT bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterRtauWithoutNjetsAfterCut = makeTH<TH1F>(*fs, "QCD_StdCutPath_TauPtAfter_noNjets_Rtau_after", "Rtau;tau pT bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdWeightedRtau = makeTH<TH1F>(*fs, "QCD_StdCutPath_weighted_Rtau", "Rtau;Rtau;N_{events}/0.05", 24, 0., 1.2);
    hStdWeightedBjets = makeTH<TH1F>(*fs, "QCD_StdCutPath_weighted_Bjets", "Bjets;N_{b-tagged jets};N_{events}", 10, 0., 10.);
    hStdWeightedFakeMETVeto = makeTH<TH1F>(*fs, "QCD_StdCutPath_weighted_FakeMETVeto", "FakeMETVeto;min(#Delta#phi(MET, jets)), degrees;N_{events} / 5 degrees", 36, 0., 180.);
    hStdNonWeightedRtau = makeTH<TH1F>(*fs, "QCD_StdCutPath_nonWeighted_Rtau", "Rtau;Rtau;N_{events}/0.05", 24, 0., 1.2);
    hStdNonWeightedSelectedTauPt = makeTH<TH1F>(*fs, "QCD_StdCutPath_nonWeighted_TauPtAfterTauID", "tau pT after tauID;#tau p_{T} after tauID;N_{events}/10 GeV/c", 30, 0., 300.);
    hStdNonWeightedSelectedTauEta = makeTH<TH1F>(*fs, "QCD_StdCutPath_nonWeighted_TauEtaAfterTauID", "tau eta after tauID;#tau #eta after tauID;N_{events}/0.2", 30, -3., 3.);
    hStdNonWeightedBjets = makeTH<TH1F>(*fs, "QCD_StdCutPath_nonWeighted_Bjets", "Bjets;N_{b-tagged jets};N_{events}", 10, 0., 10.);
    hStdNonWeightedFakeMETVeto = makeTH<TH1F>(*fs, "QCD_StdCutPath_nonWeighted_FakeMETVeto", "FakeMETVeto;min(#Delta#phi(MET, jets)), degrees;N_{events} / 5 degrees", 36, 0., 180.);

    // ABCD(tau isol. vs. b-tag) cut path
    for (int i = 0; i < 4; i++) {
      std::string myRegion;
      if (i == 0) myRegion = "NegNeg";
      else if (i == 1) myRegion = "NegPos";
      else if (i == 2) myRegion = "PosNeg";
      else if (i == 3) myRegion = "PosPos";

      std::stringstream myLabel;
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterJetSelection_" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterJetSelection[i] = makeTH<TH1F>(*fs, myLabel.str().c_str(), "NonWeightedTauPtAfterJetSelection;tau p_{T} bin;N_{events} after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtvsMET" << myRegion;
      hABCDTauIsolBNonWeightedTauPtVsMET[i] = makeTH<TH2F>(*fs, myLabel.str().c_str(), "NonWeightedTauPtvsMET;tau p_{T}, GeV/c;MET, GeV", 60, 0, 300., 60, 0., 300.);
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterMET" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterMET[i] = makeTH<TH1F>(*fs, myLabel.str().c_str(), "NonWeightedTauPtAfterMET;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterRtau" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterRtau[i] = makeTH<TH1F>(*fs, myLabel.str().c_str(), "NonWeightedTauPtAfterRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterFakeMETVeto" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterFakeMETVeto[i] = makeTH<TH1F>(*fs, myLabel.str().c_str(), "NonWeightedTauPtAfterFakeMETVeto;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterForwardJetVeto" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterForwardJetVeto[i] = makeTH<TH1F>(*fs, myLabel.str().c_str(), "NonWeightedTauPtAfterForwardJetVeto;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterFakeMETVetoWithFactorizedRtau" << myRegion;
      hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterFakeMETVeto[i] = makeTH<TH1F>(*fs, myLabel.str().c_str(), "NonWeightedTauPtAfterFakeMETVetoWithFactorizedRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterForwardJetVetoWithFactorizedRtau" << myRegion;
      hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterForwardJetVeto[i] = makeTH<TH1F>(*fs, myLabel.str().c_str(), "NonWeightedTauPtAfterForwardJetVetoWithFactorizedRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    }

    // Correlation histograms
    hCorrelationMETAfterAllSelections = makeTH<TH1F>(*fs, "QCD_Correlation_TauPtAfterAllSelectionsAndMET", "NonWeightedTauPtAfterAllPlusMET;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hCorrelationBtagAfterAllSelections = makeTH<TH1F>(*fs, "QCD_Correlation_TauPtAfterAllSelectionsAndBtag", "NonWeightedTauPtAfterAllPlusBtag;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hCorrelationRtauAfterAllSelections = makeTH<TH1F>(*fs, "QCD_Correlation_TauPtAfterAllSelectionsAndRtau", "NonWeightedTauPtAfterAllPlusRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hCorrelationBtagAndRtauAfterAllSelections = makeTH<TH1F>(*fs, "QCD_Correlation_TauPtAfterAllSelectionsAndBtagAndRtau", "NonWeightedTauPtAfterAllPlusBtagAndRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);

    // Control histograms for P(MET>70)
    hMETPassProbabilityAfterJetSelection = makeTH<TH1F>(*fs, "QCD_NoWeight_METPassProbAfterJetSelection", "NonWeightedMETPassProbAfterJetSelection;tau p_{T} bin;N_{events} for MET after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterTauIDNoRtau = makeTH<TH1F>(*fs, "QCD_NoWeight_METPassProbAfterTauIDNoRtau", "NonWeightedMETPassProbAfterTauIDNoRtau;tau p_{T} bin;N_{events} for MET after TauIDNoRtau", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterTauID = makeTH<TH1F>(*fs, "QCD_NoWeight_METPassProbAfterTauID", "NonWeightedMETPassProbAfterTauID;tau p_{T} bin;N_{events} for MET after TauID", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterBTagging = makeTH<TH1F>(*fs, "QCD_NoWeight_METPassProbAfterBTagging", "NonWeightedMETPassProbAfterBTagging;tau p_{T} bin;N_{events} for MET after b tagging", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterFakeMETVeto = makeTH<TH1F>(*fs, "QCD_NoWeight_METPassProbAfterFakeMETVeto", "NonWeightedMETPassProbAfterFakeMETVeto;tau p_{T} bin;N_{events} for MET after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterForwardJetVeto = makeTH<TH1F>(*fs, "QCD_NoWeight_METPassProbAfterForwardJetVeto", "NonWeightedMETPassProbAfterForwardJetVeto;tau p_{T} bin;N_{events} for MET after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    
    // Other control histograms
    hTauCandidateSelectionIsolatedPtMax = makeTH<TH1F>(*fs, "QCD_SelectedTauCandidateMaxIsolatedPt", "QCD_SelectedTauCandidateMaxIsolatedPt;Isol. track p_{T}, GeV/c; N_{jets} / 1 GeV/c", 100, 0., 100.);

    // Other histograms
    hAlphaTAfterTauID = makeTH<TH1F>(*fs, "QCD_AlphaTAfterTauID", "QCD_hAlphaTAfterTauID;#alpha_{T};N_{events} / 0.1", 50, 0.0, 5.0);
    hSelectionFlow = makeTH<TH1F>(*fs, "QCD_SelectionFlow", "QCD_SelectionFlow;;N_{events}", 12, 0, 12);
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTrigger,"Trigger");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderVertexSelection,"Vertex");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTauCandidateSelection,"#tau candidate");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderElectronVeto,"Isol. e veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderMuonVeto,"Isol. #mu veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderJetSelection,"#geq 3 jets");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTauID,"#tau ID (no R_{#tau})");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderFakeMETVeto,"Further QCD rej.");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTopSelection,"Top mass");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderMETFactorized,"MET (factorized)");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderBTagFactorized,"#geq 1 b jet (factorized)");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderRtauFactorized,"R_{#tau} (factorized)");

    // PAS Control Plots
    hCtrlPlot_TauJetPt_AfterLeptonVeto_WithTauId = makeTH<TH1F>(*fs, "QCDCtrlPlot_TauJetPt_AfterLeptonVeto_WithTauId", "QCDCtrlPlot_TauJetPt_AfterLeptonVeto_WithTauId; #tau-jet p_{T} [GeV/c] ;N_{events} / 5 GeV/c", 60, 0, 300);
    hCtrlPlot_TauJetLdgTrkPt_AfterLeptonVeto_WithTauId = makeTH<TH1F>(*fs, "QCDCtrlPlot_TauJetLdgTrkPt_AfterLeptonVeto_WithTauId", "QCDCtrlPlot_TauJetLdgTrkPt_AfterLeptonVeto_WithTauId; #tau-jet p_{T}^{LdgTrk} [GeV/c] ;N_{events} / 5 GeV/c", 60, 0, 300);
    hCtrlPlot_Rtau_AfterLeptonVeto_WithTauId  = makeTH<TH1F>(*fs, "QCDCtrlPlot_Rtau_AfterLeptonVeto_WithTauId", "QCDCtrlPlot_Rtau_WithTauId; R_{#tau}=p^{ldg.track}/E^{vis.#tau jet};N_{events} / 0.02", 60, 0., 1.2);
    hCtrlPlot_JetMultiplicity_AfterLeptonVeto_WithTauIdAndRtau = makeTH<TH1F>(*fs, "QCDCtrlPlot_JetMultiplicity_AfterLeptonVeto_WithTauIdAndRtau", "QCDCtrlPlot_JetMultiplicity_AfterLeptonVeto_WithTauIdAndRtau; Number of Selected Jets; N_{events} / 1", 16, -0.5, 15.5);
    hCtrlPlot_MET_AfterLeptonVeto_WithTauIdAndRtau = makeTH<TH1F>(*fs, "QCDCtrlPlot_MET_AfterLeptonVeto_WithTauIdAndRtau", "QCDCtrlPlot_MET_AfterLeptonVeto_WithTauIdAndRtau; E_{T}^{miss} [GeV]; N_{events} / 5 GeV", 60, 0.0, 300.0);
    hCtrlPlot_JetMultiplicity_AfterMET_WithTauIdAndRtau = makeTH<TH1F>(*fs, "QCDCtrlPlot_JetMultiplicity_AfterMET_WithTauIdAndRtau", "QCDCtrlPlot_JetMultiplicity_AfterMET_WithTauIdAndRtau; Number of Selected Jets; N_{events} / 1", 16, -0.5, 15.5);
    hCtrlPlot_NBtags_AfterMET_WithTauIdAndRtau = makeTH<TH1F>(*fs, "QCDCtrlPlot_NBtags_AfterMET_WithTauIdAndRtau", "QCDCtrlPlot_NBtags_AfterMET_WithTauIdAndRtau; Number of B-tagged Jets; N_{events} / 1", 16, -0.5, 15.5);
    hCtrlPlot_TransverseMass_AfterAllSelectionNoFakeMet = makeTH<TH1F>(*fs, "QCDCtrlPlot_TransverseMass_AfterAllSelectionNoFakeMet", "QCDCtrlPlot_TransverseMass_AfterAllSelectionNoFakeMet; m_{T}(#tau-jet, E_{T}^{miss}); N_{events} / 1", 40, 0.0, 400.0); // attikis
    createHistogramGroupByOtherVariableBins("QCDCtrlPlot_Counter_MetAndBtagEff_", fCtrlPlot_MetAndBtagEff_AfterJetSelection_ByTauPt, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "pass", "");
    createHistogramGroupByOtherVariableBins("QCDCtrlPlot_Counter_MetAndBtagEffAfterFakeMet_", fCtrlPlot_MetAndBtagEff_AfterJetSelectionAndFakeMet_ByTauPt, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "pass", ""); // attikis

 
    // Analysis variations
    fAnalyses.push_back(AnalysisVariation(70., 10., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(70., 20., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(70., 30., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(65., 10., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(65., 20., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(65., 30., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(60., 10., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(60., 20., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(60., 30., myCoefficientBinCount));
   }

  QCDMeasurement::~QCDMeasurement() {}

  void QCDMeasurement::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }


  
  const int QCDMeasurement::getMetIndex(double met){
    
    if( (met < 10.0) ) return 0;
    else if( (met >= 10.0) && (met < 20.0 ) )  return 1;
    else if( (met >= 20.0) && (met < 30.0 ) )  return 2;
    else if( (met >= 30.0) && (met < 40.0 ) )  return 3;
    else if( (met >= 40.0) && (met < 50.0 ) )  return 4;
    else if( (met >= 50.0) && (met < 60.0 ) )  return 5;
    else if( (met >= 60.0) && (met < 70.0 ) )  return 6;
    else if( (met >= 70.0) && (met < 80.0 ) )  return 7;
    else if( (met >= 80.0) && (met < 90.0 ) )  return 8;
    else if( (met >= 90.0) && (met < 100.0 ) ) return 9;
    else if( (met >= 100.0) ) return 10;
    else throw cms::Exception("Configuration") << "QCDMeasruement: Cannot determine the index for MET factorization histograms for MET = " << met << ". Please check the function getMETFactorizationindex(const double met)" << std::endl;
  
    return -1;
  }


  std::vector<double> QCDMeasurement::getMetBins(void){

    std::vector<double> fMetBinLowEdges;
    fMetBinLowEdges.push_back(10);
    fMetBinLowEdges.push_back(20);
    fMetBinLowEdges.push_back(30);
    fMetBinLowEdges.push_back(40);
    fMetBinLowEdges.push_back(50);
    fMetBinLowEdges.push_back(60);
    fMetBinLowEdges.push_back(70);
    fMetBinLowEdges.push_back(80);
    fMetBinLowEdges.push_back(90);
    fMetBinLowEdges.push_back(100);

    return fMetBinLowEdges;;
  }



  const int QCDMeasurement::getJetPtIndex(double JetPt){
  
    if( (JetPt < 30.0) ) return 0;
    else if( (JetPt >= 30.0) && (JetPt < 40.0 ) )  return 1;
    else if( (JetPt >= 40.0) && (JetPt < 50.0 ) )  return 2;
    else if( (JetPt >= 50.0) && (JetPt < 60.0 ) )  return 3;
    else if( (JetPt >= 60.0) && (JetPt < 70.0 ) )  return 4;
    else if( (JetPt >= 70.0) && (JetPt < 80.0 ) )  return 5;
    else if( (JetPt >= 80.0) && (JetPt < 90.0 ) )  return 6;
    else if( (JetPt >= 90.0) && (JetPt < 100.0 ) ) return 7;
    else if( (JetPt >= 100.0) && (JetPt < 120.0 ) ) return 8;
    else if( (JetPt >= 120.0) && (JetPt < 150.0 ) ) return 9;
    else if( (JetPt >= 150.0) ) return 10;
    else throw cms::Exception("Configuration") << "QCDMeasruement: Cannot determine the index of histogram for event with JetPt = " << JetPt << ". Please check the function getMETFactorizationindex(const double met)" << std::endl;
  
    return -1;
  }


  std::vector<double> QCDMeasurement::getJetPtBins(void){

    std::vector<double> fJetPtBinLowEdges;
    fJetPtBinLowEdges.push_back(30);
    fJetPtBinLowEdges.push_back(40);
    fJetPtBinLowEdges.push_back(50);
    fJetPtBinLowEdges.push_back(60);
    fJetPtBinLowEdges.push_back(70);
    fJetPtBinLowEdges.push_back(80);
    fJetPtBinLowEdges.push_back(90);
    fJetPtBinLowEdges.push_back(100);
    fJetPtBinLowEdges.push_back(120);
    fJetPtBinLowEdges.push_back(150);

    return fJetPtBinLowEdges;;
  }


  void QCDMeasurement::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Read the prescale for the event and set the event weight as the prescale
    fEventWeight.updatePrescale(iEvent);
    increment(fAllCounter);

    // Apply PU re-weighting (Vertex weight)
    std::pair<double, size_t> weightSize = fVertexWeight.getWeightAndSize(iEvent, iSetup);
    if(!iEvent.isRealData()) fEventWeight.multiplyWeight(weightSize.first);
    hVerticesBeforeWeight->Fill(weightSize.second);
    hVerticesAfterWeight->Fill(weightSize.second, fEventWeight.getWeight());

    // Trigger and HLT_MET cut; or trigger efficiency parametrisation
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup); 
    if(!triggerData.passedEvent()) return;
    increment(fTriggerAndHLTMetCutCounter);
    hSelectionFlow->Fill(kQCDOrderTrigger, fEventWeight.getWeight());

    // GenParticle analysis
    if(!iEvent.isRealData()) fGenparticleAnalysis.analyze(iEvent, iSetup);

    
    // Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return;
    increment(fPrimaryVertexCounter);
    hSelectionFlow->Fill(kQCDOrderVertexSelection, fEventWeight.getWeight());


    // Apply pre-MET cut to see if MC Normalization is better.
    //if(metData.getSelectedMET()->et() < 30 ) return;

    // Apply tau candidate selection (with or without Rtau control region)
    TauSelection::Data tauCandidateData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauCandidateData.passedEvent()) return;
    increment(fOneProngTauSelectionCounter);
    fPFTauIsolationCalculator.beginEvent(iEvent); // Set primary vertex to PF tau isolation calculation
    edm::PtrVector<pat::Tau> mySelectedTau = chooseMostIsolatedTauCandidate(tauCandidateData.getSelectedTaus());
    // Require that just one tau has been found
    if (mySelectedTau.size() != 1) return;
    increment(fOneSelectedTauCounter);
    hSelectionFlow->Fill(kQCDOrderTauCandidateSelection,fEventWeight.getWeight());

    double mySelectedTauPt = mySelectedTau[0]->pt();
    int myFactorizationTableIndex = fFactorizationTable.getCoefficientTableIndexByPtAndEta(mySelectedTauPt,0.);
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    fMETHistogramsByTauPtAfterTauCandidateSelection[myFactorizationTableIndex]->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());


    // GlobalElectronVeto 
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return; 
    increment(fGlobalElectronVetoCounter);
    hSelectionFlow->Fill(kQCDOrderElectronVeto, fEventWeight.getWeight());


    // GlobalMuonVeto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return; 
    increment(fGlobalMuonVetoCounter);
    hSelectionFlow->Fill(kQCDOrderMuonVeto, fEventWeight.getWeight());
    

    // Factorized out Rtau (after full tauID, but without Njets; assume that Njets cut does not correlate with Rtau)
    // Obtain tau ID data object
    TauSelection::Data tauDataForTauID = fOneProngTauSelection.analyzeTauIDWithoutRtauOnCleanedTauCandidates(iEvent, iSetup);
    if (tauDataForTauID.passedEvent()) {
      hStdNonWeightedTauPtAfterRtauWithoutNjetsBeforeCut->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
      if (tauDataForTauID.selectedTauPassedRtau()) {
        hStdNonWeightedTauPtAfterRtauWithoutNjetsAfterCut->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
        hSelectionFlow->Fill(kQCDOrderRtauFactorized, fEventWeight.getWeight());
      }
    }


    // PAS Control Plots: After Tr, PV, e/mu veto (Before Jet Selection)
    if( tauDataForTauID.passedEvent() ){
//       double myTauPtValue = tauDataForTauID.getSelectedTaus()[0]->pt(); // value 1 goes in the bin below 1 in the histogram
//       double myTauLdgTrkPtValue = tauDataForTauID.getSelectedTaus()[0]->leadPFChargedHadrCand()->pt() / tauDataForTauID.getSelectedTaus()[0]->p() - 1.0e-10; // value 1 goes in the bin below 1 in the histogram
//       double myRtauValue = tauDataForTauID.getSelectedTaus()[0]->leadPFChargedHadrCand()->p() / tauDataForTauID.getSelectedTaus()[0]->p() - 1.0e-10; // value 1 goes in the bin below 1 in the histogram
      
      double myTauPValue = tauDataForTauID.getSelectedTaus()[0]->p();
      double myTauPtValue = tauDataForTauID.getSelectedTaus()[0]->pt();
      double myTauLdgTrkPtValue = tauDataForTauID.getSelectedTaus()[0]->leadPFChargedHadrCand()->pt();
      double myRtauValue = myTauLdgTrkPtValue / myTauPValue - 1.0e-10; // value 1 goes in the bin below 1 in the histogram


      // After Tr, PV, e/mu veto (Before Jet Selection) with TauId (no Rtau or LdgTrk pt) -> get from parallel tauid analysis
      hCtrlPlot_TauJetPt_AfterLeptonVeto_WithTauId->Fill(myTauPtValue,fEventWeight.getWeight());
      hCtrlPlot_TauJetLdgTrkPt_AfterLeptonVeto_WithTauId->Fill(myTauLdgTrkPtValue, fEventWeight.getWeight() );
      
      // After Tr, PV, e/mu veto (Before Jet Selection) with TauId (no Rtau)
      hCtrlPlot_Rtau_AfterLeptonVeto_WithTauId->Fill(myRtauValue, fEventWeight.getWeight() );

      // After Tr, PV, e/mu veto (Before Jet Selection) with TauId
      JetSelection::Data jetDataTmp = fJetSelection.analyze(iEvent, iSetup, mySelectedTau);
      if (tauDataForTauID.selectedTauPassedRtau()) {
	hCtrlPlot_JetMultiplicity_AfterLeptonVeto_WithTauIdAndRtau->Fill(jetDataTmp.getHadronicJetCount(), fEventWeight.getWeight());
	hCtrlPlot_MET_AfterLeptonVeto_WithTauIdAndRtau->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      }

    }
    
    // Clean jet collection from selected tau and apply NJets>=3 cut
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, mySelectedTau);
    if (jetData.getHadronicJetCount() >= 2) {
      increment(fJetSelectionCounter2);
    }
    if (!jetData.passedEvent()) return;
    
    ///////////////////////////////// After Jet Selection /////////////////////////////////
    increment(fJetSelectionCounter);
    hSelectionFlow->Fill(kQCDOrderJetSelection, fEventWeight.getWeight());
    hMETAfterJetSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    
    // Fill factorization info into histogram
    fMETHistogramsByTauPtAfterJetSelection[myFactorizationTableIndex]->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hMETFactorizationNJetsBefore->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
    if (metData.passedEvent())
      hMETFactorizationNJetsAfter->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
    hMETFactorizationNJets->Fill(mySelectedTau[0]->pt(), metData.getSelectedMET()->et(), fEventWeight.getWeight());

    // Check BTag-MET correlations
    edm::PtrVector<pat::Jet> selectedJets = jetData.getSelectedJets();
    const int myMetIndex =  getMetIndex( metData.getSelectedMET()->et() );
    const int myJetPtIndex =  getJetPtIndex( selectedJets[0]->et() );
    fLdgJetPtHistogramGroupByMET[myMetIndex]->Fill( selectedJets[0]->et(), fEventWeight.getWeight());
    
    // FIXME: put inside a method
    // Perform GenParticle Level Analysis
    if( !(iEvent.isRealData()) ) {
      std::vector<const reco::Candidate*> myBquarks = fGenparticleAnalysis.doQCDmAnalysis(iEvent, iSetup);
      const int nBquarks = myBquarks.size();
      int nBquarksStatus2 = 0;
      int nBquarksStatus3 = 0;
      std::vector<const reco::Candidate*>::iterator iBquark;
      // Loop over all bquarks
      for(iBquark = myBquarks.begin(); iBquark < myBquarks.end(); iBquark++){
	if ( (*iBquark)->pt() < 30 || (*iBquark)->eta() > 2.5 ) continue;
	const int st = (*iBquark)->status();
	bool bHasBquarkDaughter = false;
	// Check whether the GenParticle decays to itself. If yes do not consider in counting
	if ( (*iBquark)->numberOfDaughters() != 0 ){
	  // Loop over all 1st daughters of genParticle    
	  for(size_t j = 0; j < (*iBquark)->numberOfDaughters() ; ++ j) {
	    const reco::Candidate *d = (*iBquark)->daughter( j );
	    if( (*iBquark)->pdgId() == d->pdgId() ) bHasBquarkDaughter = true;
	  }
	}
	if(bHasBquarkDaughter) continue;
	if(st == 2) nBquarksStatus2++;
	else if (st == 3) nBquarksStatus3++;
	else std::cout << "*** WARNING! Found Bquark with status = " << st << std::endl;
      } //eof: Loop over all bquarks
      fNBquarksHistogramGroupByMET[myMetIndex]->Fill(nBquarks, fEventWeight.getWeight());
      fNBquarksStatus2HistogramGroupByMET[myMetIndex]->Fill(nBquarksStatus2, fEventWeight.getWeight());
      fNBquarksStatus3HistogramGroupByMET[myMetIndex]->Fill(nBquarksStatus3 , fEventWeight.getWeight());
    } // eof: if(!iEvent.isRealData()){
    // FIXME: end of put to separate method

    fMETHistogramGroupByLdgJetPt[myJetPtIndex]->Fill( metData.getSelectedMET()->et(), fEventWeight.getWeight());
  
    // Factorize out MET cut
    double myEventWeightBeforeMetFactorization = fEventWeight.getWeight();
    hWeightedMETAfterJetSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterJetSelection->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent()) {
      hMETPassProbabilityAfterJetSelection->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
      increment(fMETCounter);
      hSelectionFlow->Fill(kQCDOrderMETFactorized, fEventWeight.getWeight());
    }


    // alphaT - No cuts applied! Only produces plots
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(mySelectedTau[0]), jetData.getSelectedJets());
    // increment(fEvtTopologyCounter);


    // InvMassVeto - No cuts applied! Only produces plots 
    InvMassVetoOnJets::Data invMassVetoOnJetsData =  fInvMassVetoOnJets.analyze( jetData.getSelectedJets() ); 
    // if(!invMassVetoOnJetsData.passedEvent()) return; 
    // increment(fInvMassVetoOnJetsCounter);


    // Obtain btagging, fakeMETVeto, and forwardJetVeto data objects - internal plots will be wrong since they are not produced at the spot where the cut is applied
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
    fNBtagsHistogramsByTauPtAfterJetSelection[myFactorizationTableIndex]->Fill(btagData.getBJetCount(), fEventWeight.getWeight());
    fNBtagsHistogramGroupByMET[myMetIndex]->Fill(btagData.getBJetCount(), fEventWeight.getWeight());
      
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, mySelectedTau, jetData.getSelectedJets());
    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    TopSelection::Data topSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());

    // Save histograms to enable QCD purity evaluation
    analyzePurities( tauDataForTauID, jetData, metData, btagData, fakeMETData, myFactorizationTableIndex, fEventWeight.getWeight(), fPurityBeforeAfterJets, fPurityBeforeAfterJetsMet, fPurityBeforeAfterJetsMetBtag, fPurityBeforeAfterJetsFakeMet, fPurityBeforeAfterJetsTauIdNoRtau);


    // PAS Control Plots: After Tr, PV, e/mu veto and Jet Selection
    if(btagData.passedEvent() && metData.passedEvent()) fCtrlPlot_MetAndBtagEff_AfterJetSelection_ByTauPt[myFactorizationTableIndex]->Fill(1.0, fEventWeight.getWeight());
    else fCtrlPlot_MetAndBtagEff_AfterJetSelection_ByTauPt[myFactorizationTableIndex]->Fill(0.0, fEventWeight.getWeight());

    // Now repeat but do it also after FakeMET 
    if(btagData.passedEvent() && metData.passedEvent() && fakeMETData.passedEvent() ) fCtrlPlot_MetAndBtagEff_AfterJetSelectionAndFakeMet_ByTauPt[myFactorizationTableIndex]->Fill(1.0, fEventWeight.getWeight());
    else fCtrlPlot_MetAndBtagEff_AfterJetSelectionAndFakeMet_ByTauPt[myFactorizationTableIndex]->Fill(0.0, fEventWeight.getWeight());

    // Check FakeMETVeto-MET Correlations
    if(metData.passedEvent() && btagData.passedEvent() ) fCounterAfterJetsMetBtagByTauPt[myFactorizationTableIndex]->Fill(1.0, fEventWeight.getWeight());
    else fCounterAfterJetsMetBtagByTauPt[myFactorizationTableIndex]->Fill(0.0, fEventWeight.getWeight());

    if( metData.passedEvent() && btagData.passedEvent() && fakeMETData.passedEvent() ) fCounterAfterJetsMetBtagFakeMetByTauPt[myFactorizationTableIndex]->Fill( 1.0, fEventWeight.getWeight());
    else fCounterAfterJetsMetBtagFakeMetByTauPt[myFactorizationTableIndex]->Fill( 0.0, fEventWeight.getWeight());

    if( tauDataForTauID.passedEvent() ) fCounterAfterJetsTauIdNoRtauByTauPt[myFactorizationTableIndex]->Fill( 1.0, fEventWeight.getWeight());
    else fCounterAfterJetsTauIdNoRtauByTauPt[myFactorizationTableIndex]->Fill( 0.0, fEventWeight.getWeight());

    if( tauDataForTauID.passedEvent() && fakeMETData.passedEvent() ) fCounterAfterJetsTauIdNoRtauFakeMetByTauPt[myFactorizationTableIndex]->Fill( 1.0, fEventWeight.getWeight());
    else fCounterAfterJetsTauIdNoRtauFakeMetByTauPt[myFactorizationTableIndex]->Fill( 0.0, fEventWeight.getWeight());


    // Factorize out b-tagging
    hStdWeightedBjets->Fill(btagData.getBJetCount(), fEventWeight.getWeight());
    hStdNonWeightedBjets->Fill(btagData.getBJetCount(), myEventWeightBeforeMetFactorization);
    if (btagData.passedEvent()) {
      increment(fBTaggingCounter);
      hWeightedMETAfterBTagging->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      hSelectionFlow->Fill(kQCDOrderBTagFactorized, fEventWeight.getWeight());
      // Check MET and btagging - is it necessary?
      hStdNonWeightedTauPtAfterBTagging->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
      if (metData.passedEvent())
        hMETPassProbabilityAfterBTagging->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
      hMETFactorizationBJets->Fill(mySelectedTau[0]->pt(), metData.getSelectedMET()->et(), myEventWeightBeforeMetFactorization);
    }

    // Apply non-standard cut paths
    analyzeABCDByTauIsolationAndBTagging(metData, mySelectedTau, tauCandidateData, tauDataForTauID, btagData,
                                         fakeMETData, forwardJetData, topSelectionData, myFactorizationTableIndex, 
                                         myEventWeightBeforeMetFactorization);
    analyzeCorrelation(metData, mySelectedTau, tauCandidateData, tauDataForTauID, btagData, 
                       fakeMETData, forwardJetData, topSelectionData, myFactorizationTableIndex,
                       myEventWeightBeforeMetFactorization);
    for(std::vector<AnalysisVariation>::iterator it = fAnalyses.begin(); it != fAnalyses.end(); ++it) {
      (*it).analyse(metData, mySelectedTau, tauCandidateData, tauDataForTauID, btagData, 
                       fakeMETData, forwardJetData, topSelectionData, myFactorizationTableIndex,
                       myEventWeightBeforeMetFactorization);
    }

    
    // Continue best cut path

    /// FakeMETVeto and MET Correlations
    fFakeMETVetoHistogramGroupByMET[myMetIndex]->Fill(fakeMETData.closestDeltaPhi(), fEventWeight.getWeight() );
    

    // Apply rest of tauID without Rtau
    if(!tauDataForTauID.passedEvent()) return;
    increment(fOneProngTauIDWithoutRtauCounter);
    hSelectionFlow->Fill(kQCDOrderTauID, fEventWeight.getWeight());
    hWeightedMETAfterTauIDNoRtau->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterTauIDNoRtau->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterTauIDNoRtau->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    fMETHistogramsByTauPtAfterTauIsolation[myFactorizationTableIndex]->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());

    // PAS Control Plots: After Tr, PV, e/mu veto, Jet Selection, MET and Full TauId 
    if( tauDataForTauID.selectedTauPassedRtau() && metData.passedEvent()  ){
      hCtrlPlot_JetMultiplicity_AfterMET_WithTauIdAndRtau->Fill(jetData.getHadronicJetCount(), fEventWeight.getWeight());
      hCtrlPlot_NBtags_AfterMET_WithTauIdAndRtau->Fill(btagData.getBJetCount(), fEventWeight.getWeight());
    }
    
    // PAS Control Plots: Transverse Mass distribution
    double transverseMass = TransverseMass::reconstruct(*(tauDataForTauID.getSelectedTaus()[0]), *(metData.getSelectedMET()) );
    if( btagData.passedEvent() && metData.passedEvent() ) hCtrlPlot_TransverseMass_AfterAllSelectionNoFakeMet->Fill(transverseMass, fEventWeight.getWeight());

    // Fill Btagging-TauID correlation histos (in tau pT bins)
    fNBtagsHistogramsByTauPtAfterTauIdNoRtau[myFactorizationTableIndex]->Fill(btagData.getBJetCount(), fEventWeight.getWeight());
    if( tauDataForTauID.selectedTauPassedRtau() ) fNBtagsHistogramsByTauPtAfterTauIdAndRtau[myFactorizationTableIndex]->Fill(btagData.getBJetCount(), fEventWeight.getWeight()); 

    // Factorize out Rtau cut - check if it can be done without Njets
    hStdWeightedRtau->Fill(tauDataForTauID.getRtauOfSelectedTau(), fEventWeight.getWeight());
    hStdNonWeightedRtau->Fill(tauDataForTauID.getRtauOfSelectedTau(), myEventWeightBeforeMetFactorization);
    if (tauDataForTauID.selectedTauPassedRtau()) {
      increment(fOneProngTauIDWithRtauCounter);
      hWeightedMETAfterTauID->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      hStdNonWeightedTauPtAfterTauID->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
      if (metData.passedEvent())
	hMETPassProbabilityAfterTauID->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
      hStdNonWeightedSelectedTauPt->Fill(mySelectedTau[0]->pt(), myEventWeightBeforeMetFactorization);
      hStdNonWeightedSelectedTauEta->Fill(mySelectedTau[0]->eta(), myEventWeightBeforeMetFactorization);
    }

    // Apply FakeMETVeto
    hStdWeightedFakeMETVeto->Fill(fakeMETData.closestDeltaPhi(), fEventWeight.getWeight());
    hStdNonWeightedFakeMETVeto->Fill(fakeMETData.closestDeltaPhi(), myEventWeightBeforeMetFactorization);
    if (!fakeMETData.passedEvent()) return;
    increment(fFakeMETVetoCounter);
    hSelectionFlow->Fill(kQCDOrderFakeMETVeto, fEventWeight.getWeight());
    hWeightedMETAfterFakeMETVeto->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterFakeMETVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterFakeMETVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);


    // Apply top mass reconstruction
    if (!topSelectionData.passedEvent()) return;
    increment(fTopSelectionCounter);
    hSelectionFlow->Fill(kQCDOrderTopSelection, fEventWeight.getWeight());


    // AlphaT
    // Has to be done after full TauID
    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    hAlphaTAfterTauID->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());

    // hTransverseMassWithTopCut->Fill(transverseMass, fEventWeight.getWeight());

    //     //    if(transverseMass < ftransverseMassCut-20.0 ) return false;
    //     if(transverseMass < 80 ) return false;
    //     increment(ftransverseMassCut80Counter);
    
    //     if(transverseMass < 100 ) return false;
    //     increment(ftransverseMassCut100Counter);
    

    // Do final histogramming
    fWeightedSelectedEventsAnalyzer.fill(mySelectedTau,
					 tauCandidateData,
					 electronVetoData,
					 muonVetoData,
					 jetData,
					 btagData,
					 metData,
					 fakeMETData,
					 forwardJetData,
					 fEventWeight.getWeight());
    fNonWeightedSelectedEventsAnalyzer.fill(mySelectedTau,
					    tauCandidateData,
					    electronVetoData,
					    muonVetoData,
					    jetData,
					    btagData,
					    metData,
					    fakeMETData,
					    forwardJetData,
					    myEventWeightBeforeMetFactorization);
    
    // Forward jet veto -- experimental
    if (!forwardJetData.passedEvent()) return;
    increment(fForwardJetVetoCounter);
    hWeightedMETAfterForwardJetVeto->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterForwardJetVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterForwardJetVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
  }



  edm::PtrVector<pat::Tau> QCDMeasurement::chooseMostIsolatedTauCandidate(edm::PtrVector<pat::Tau> tauCandidates) {
    edm::PtrVector<pat::Tau> mySelectedTauCandidate;
    edm::PtrVector<pat::Tau>::const_iterator myBestCandidate = tauCandidates.begin();
    double myBestPtMax = 9999.;
    for(edm::PtrVector<pat::Tau>::const_iterator iter = tauCandidates.begin(); iter != tauCandidates.end(); ++iter) {
      if (!(*iter)->isPFTau()) continue;
      //const edm::Ptr<pat::Tau> iTau = *iter;
      double mySumPt = 999.;
      double myMaxPt = 999.;
      size_t myOccupancy = 999.;
      // TMP //fPFTauIsolationCalculator.calculateHpsTight(**iter, &mySumPt, &myMaxPt, &myOccupancy);
      myMaxPt = 0.; // TMP
      if (myMaxPt < myBestPtMax) {
        if (myMaxPt < 0.5) {
          mySelectedTauCandidate.push_back(*iter);
          hTauCandidateSelectionIsolatedPtMax->Fill(myMaxPt, fEventWeight.getWeight());
        } else {
          myBestPtMax = myMaxPt;
          myBestCandidate = iter;
        }
      }
    }
    // Save best candidate if list is empty 
    if (!mySelectedTauCandidate.size() && tauCandidates.size()) {
      mySelectedTauCandidate.push_back(*myBestCandidate);
      hTauCandidateSelectionIsolatedPtMax->Fill(myBestPtMax, fEventWeight.getWeight());
    }
    // If more than 1 jets are chosen, then take the one with higher ET
    // No need for code, should be the first in list
    return mySelectedTauCandidate;
  }
  


  void QCDMeasurement::createHistogramGroupByOtherVariableBins(std::string name, std::vector<TH1*>& histograms, const int nBins, double xMin, double xMax, std::vector<double> BinVariableBins, const TString BinVariableName, const TString VariableName, const TString VariableUnits ){

    // Make histograms
    edm::Service<TFileService> fs;
    size_t myTableSize = BinVariableBins.size(); 
    std::stringstream myHistoName;
    std::stringstream myHistoLabel;

    /// Loop ofver all tau pT bins
    for (size_t i = 0; i < myTableSize; ++i) {
      myHistoName.str("");
      myHistoLabel.str("");
      if (i == 0) {
	// Treat first bin
	myHistoName << name <<  BinVariableName << "RangeBelow" << BinVariableBins[0];
	// myHistoLabel << name << BinVariableName << "RangeBelow" << BinVariableBins[0] <<";Pass;N";
	myHistoLabel << name << BinVariableName << "RangeBelow" << BinVariableBins[0] <<"; "<< VariableName << "[" << VariableUnits << "]" << ";N/" << static_cast<int>((xMax-xMin)/nBins) << VariableUnits; 
	histograms.push_back( fs->make<TH1F>(myHistoName.str().c_str(), myHistoLabel.str().c_str(), nBins, xMin, xMax) );
      } else {
	// Treat other bins
	myHistoName << name << BinVariableName << "Range" << BinVariableBins[i-1] << "to" << BinVariableBins[i];
	// myHistoLabel << name << "TauPtRange" << BinVariableBins[i-1] << "to" << BinVariableBins[i] << ";Pass;N"; 
	myHistoLabel << name << BinVariableName << "Range" << BinVariableBins[i-1] << "to" << BinVariableBins[i] << "; "<< VariableName << "[" << VariableUnits << "]" << ";N/" << static_cast<int>((xMax-xMin)/nBins) << VariableUnits; 
	histograms.push_back(fs->make<TH1F>(myHistoName.str().c_str(), myHistoLabel.str().c_str(), nBins, xMin, xMax));
      }
    }
    // Treat last bin
    myHistoName.str("");
    myHistoLabel.str("");
    myHistoName << name << BinVariableName << "RangeAbove" << BinVariableBins[myTableSize-1];
    // myHistoLabel << name << BinVariableName << "RangeAbove" << BinVariableBins[myTableSize-1] <<";Pass;N"; 
    myHistoLabel << name << BinVariableName << "RangeAbove" << BinVariableBins[myTableSize-1] << "; "<< VariableName << "[" << VariableUnits << "]" << ";N/" << static_cast<int>((xMax-xMin)/nBins) << VariableUnits; 
    histograms.push_back(fs->make<TH1F>(myHistoName.str().c_str(), myHistoLabel.str().c_str(), nBins, xMin, xMax));
    // Apply sumw2 on the histograms
    for (std::vector<TH1*>::iterator it = histograms.begin(); it != histograms.end(); ++it) {
      (*it)->Sumw2();
    }
    return;
}



  void QCDMeasurement::analyzeABCDByTauIsolationAndBTagging(const METSelection::Data& METData, edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauCandidateData, const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data& forwardData, const TopSelection::Data& topSelectionData, int tauPtBin, double weightWithoutMET) {
    // Divide phase space into ABCD regions
    int myIndex = 0;
    if (!tauData.passedEvent()) { // this is just isolation and nprongs == 1
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
    if (tauCandidateData.selectedTauCandidatePassedRtau()) {
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
    return;
  }


  void QCDMeasurement::analyzeCorrelation(const METSelection::Data& METData, edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauCandidateData, const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data& forwardData, const TopSelection::Data& topSelectionData, int tauPtBin, double weightWithoutMET) {
    // Apply all selections of the standard cut path
    if (!tauData.passedEvent() || // Tau ID without Rtau
        !fakeMETData.passedEvent() || // fake MET veto
        !topSelectionData.passedEvent()) // top selection
      return;

    if (METData.passedEvent()) {
      hCorrelationMETAfterAllSelections->Fill(tauPtBin, weightWithoutMET);
    }
    if (btagData.passedEvent()) {
      hCorrelationBtagAfterAllSelections->Fill(tauPtBin, weightWithoutMET);
    }
    if (tauCandidateData.selectedTauCandidatePassedRtau()) {
      hCorrelationRtauAfterAllSelections->Fill(tauPtBin, weightWithoutMET);
      if (btagData.passedEvent()) {
        hCorrelationBtagAndRtauAfterAllSelections->Fill(tauPtBin, weightWithoutMET);
      }
    }
    return;
  }


  
  void QCDMeasurement::analyzePurities(const TauSelection::Data& tauDataForTauID, const JetSelection::Data &jetData, const METSelection::Data& METData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const int myTauPtIndex, double EventWeight, std::vector<TH1*> fPurityBeforeAfterJets, std::vector<TH1*> fPurityBeforeAfterJetsMet, std::vector<TH1*> fPurityBeforeAfterJetsMetBtag, std::vector<TH1*> fPurityBeforeAfterJetsFakeMet, std::vector<TH1*> fPurityBeforeAfterJetsTauIdNoRtau){
    
    
    // Purity histograms
    // JetSelection has probably already been passed but it matters not. I will get a histo with only entries on 1.0. Still can calculate Purity after Jet Selection.
    if( jetData.passedEvent() ) fPurityBeforeAfterJets[myTauPtIndex]->Fill( 1.0, EventWeight);
    else fPurityBeforeAfterJets[myTauPtIndex]->Fill( 0.0, EventWeight);
    
    // Exit if jet-Selection is not satisfied  
    if( !jetData.passedEvent() ) return;
    
    if( METData.passedEvent() ) fPurityBeforeAfterJetsMet[myTauPtIndex]->Fill( 1.0, EventWeight);
    else fPurityBeforeAfterJetsMet[myTauPtIndex]->Fill( 0.0, EventWeight);


    if( METData.passedEvent() && btagData.passedEvent() ) fPurityBeforeAfterJetsMetBtag[myTauPtIndex]->Fill( 1.0, EventWeight);
    else fPurityBeforeAfterJetsMetBtag[myTauPtIndex]->Fill( 0.0, EventWeight);


    if( fakeMETData.passedEvent() ) fPurityBeforeAfterJetsFakeMet[myTauPtIndex]->Fill( 1.0, EventWeight);
    else fPurityBeforeAfterJetsFakeMet[myTauPtIndex]->Fill( 0.0, EventWeight);


    //if (tauDataForTauID.selectedTauPassedRtau())
    if (tauDataForTauID.passedEvent() ) fPurityBeforeAfterJetsTauIdNoRtau[myTauPtIndex]->Fill( 1.0, EventWeight);
    else fPurityBeforeAfterJetsTauIdNoRtau[myTauPtIndex]->Fill( 0.0, EventWeight);

    return;
  }
  

  QCDMeasurement::AnalysisVariation::AnalysisVariation(double METcut, double fakeMETVetoCut, int nTauPtBins)
    : fMETCut(METcut),
      fFakeMETVetoCut(fakeMETVetoCut) {
    std::stringstream myName;
    myName << "QCDAnalysisVariation_METcut" << METcut << "_FakeMETCut" << fakeMETVetoCut;
    // Create histograms
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(myName.str());
    hAfterBigBox = makeTH<TH1F>(myDir, "AfterBigBox", "AfterBigBox", nTauPtBins, 0, nTauPtBins);
    hLeg1AfterBTagging = makeTH<TH1F>(myDir, "Leg1AfterBTagging", "Leg1AfterBTagging", nTauPtBins, 0, nTauPtBins);
    hLeg1AfterMET = makeTH<TH1F>(myDir, "Leg1AfterMET", "Leg1AfterMET", nTauPtBins, 0, nTauPtBins);
    hLeg1AfterFakeMETVeto = makeTH<TH1F>(myDir, "Leg1AfterFakeMETVeto", "Leg1AfterFakeMETVeto", nTauPtBins, 0, nTauPtBins);
    hLeg1AfterTopSelection = makeTH<TH1F>(myDir, "Leg1AfterTopSelection", "Leg1AfterTopSelection", nTauPtBins, 0, nTauPtBins);
    hLeg1AfterAntiTopSelection = makeTH<TH1F>(myDir, "Leg1AfterAntiTopSelection", "Leg1AfterAntiTopSelection", nTauPtBins, 0, nTauPtBins);
    hAfterBigBoxAndTauIDNoRtau = makeTH<TH1F>(myDir, "AfterBigBoxAndTauIDNoRtau", "AfterBigBoxAndTauIDNoRtau", nTauPtBins, 0, nTauPtBins);
    hLeg2AfterRtau = makeTH<TH1F>(myDir, "Leg2AfterRtau", "Leg2AfterRtau", nTauPtBins, 0, nTauPtBins);
    hLeg3AfterFakeMETVeto = makeTH<TH1F>(myDir, "Leg3AfterFakeMETVeto", "Leg3AfterFakeMETVeto", nTauPtBins, 0, nTauPtBins);
    hLeg1FakeMetVetoDistribution = makeTH<TH1F>(myDir, "Leg1_Closest_DeltaPhi_of_MET_and_selected_jets_or_taus", "min DeltaPhi(MET,selected jets or taus);min(#Delta#phi(MET,jets)), degrees;N / 5", 36, 0., 180.);
    hLeg3FakeMetVetoDistribution = makeTH<TH1F>(myDir, "Leg3_Closest_DeltaPhi_of_MET_and_selected_jets_or_taus", "min DeltaPhi(MET,selected jets or taus);min(#Delta#phi(MET,jets)), degrees;N / 5", 36, 0., 180.);
    hTopMassDistribution = makeTH<TH1F>(myDir, "TopMass_jjbMax", "Mass_jjbMax;;N_{Events} / 5 GeV/c^{2}", 160, 0., 800.);
  }
  QCDMeasurement::AnalysisVariation::~AnalysisVariation() { }
  void QCDMeasurement::AnalysisVariation::analyse(const METSelection::Data& METData, edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauCandidateData, const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data& forwardData, const TopSelection::Data& topSelectionData, int tauPtBin, double weightWithoutMET) {
    hAfterBigBox->Fill(tauPtBin, weightWithoutMET);
    // Leg 1
    if (METData.getSelectedMET()->et() > fMETCut) {
        hLeg1AfterMET->Fill(tauPtBin, weightWithoutMET);
      if (btagData.passedEvent()) {
        hLeg1AfterBTagging->Fill(tauPtBin, weightWithoutMET);
        hTopMassDistribution->Fill(topSelectionData.getTopMass(), weightWithoutMET);
        if (topSelectionData.passedEvent()) {
          hLeg1AfterTopSelection->Fill(tauPtBin, weightWithoutMET);
        } else {
          hLeg1AfterAntiTopSelection->Fill(tauPtBin, weightWithoutMET);
        }
      }
      hLeg1FakeMetVetoDistribution->Fill(fakeMETData.closestDeltaPhi(), weightWithoutMET);
      if (fakeMETData.closestDeltaPhi() > fFakeMETVetoCut) {
        hLeg1AfterFakeMETVeto->Fill(tauPtBin, weightWithoutMET);
      }
    }
    // TauID without Rtau
    if (tauData.passedEvent()) {
      hAfterBigBoxAndTauIDNoRtau->Fill(tauPtBin, weightWithoutMET);
      // Leg2
      if (tauCandidateData.selectedTauCandidatePassedRtau()) {
        hLeg2AfterRtau->Fill(tauPtBin, weightWithoutMET);
      }
      // Leg3
      hLeg3FakeMetVetoDistribution->Fill(fakeMETData.closestDeltaPhi(), weightWithoutMET);
      if (fakeMETData.closestDeltaPhi() > fFakeMETVetoCut) {
        hLeg3AfterFakeMETVeto->Fill(tauPtBin, weightWithoutMET);
      }
    }
    return;
  }

}

