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
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight),
    fInvMassVetoOnJets(iConfig.getUntrackedParameter<edm::ParameterSet>("InvMassVetoOnJets"), eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, eventWeight),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, eventWeight),
    fWeightedSelectedEventsAnalyzer("QCDm3p2_afterAllSelections_weighted"),
    fNonWeightedSelectedEventsAnalyzer("QCDm3p2_afterAllSelections_nonWeighted"),
    fPFTauIsolationCalculator(iConfig.getUntrackedParameter<edm::ParameterSet>("tauIsolationCalculator")),
    fTriggerEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiency")),
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

    createMETHistogramGroupByTauPt("QCD_MET_afterTauCandidateSelection", fMETHistogramsByTauPtAfterTauCandidateSelection);
    createMETHistogramGroupByTauPt("QCD_MET_afterJetSelection", fMETHistogramsByTauPtAfterJetSelection);
    createMETHistogramGroupByTauPt("QCD_MET_afterTauIsolation", fMETHistogramsByTauPtAfterTauIsolation);
    createNBtagsHistogramGroupByTauPt("QCD_NBtags_afterJetSelection", fNBtagsHistogramsByTauPtAfterJetSelection);

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
   }

  QCDMeasurement::~QCDMeasurement() {}

  void QCDMeasurement::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void QCDMeasurement::createMETHistogramGroupByTauPt(std::string name, std::vector<TH1*>& histograms) {
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
        histograms.push_back(makeTH<TH1F>(*fs, myHistoName.str().c_str(),
          myHistoLabel.str().c_str(), myMETBins, myMETMin, myMETMax));
        } else {
          // Treat other bins
          myHistoName << name << "TauPtRange" << fFactorizationBinLowEdges[i-1] << "to" << fFactorizationBinLowEdges[i];
          myHistoLabel << name << "TauPtRange" << fFactorizationBinLowEdges[i-1] << "to" << fFactorizationBinLowEdges[i] << ";MET, GeV;N/"
            << static_cast<int>((myMETMax-myMETMin)/myMETBins) << " GeV";
          histograms.push_back(makeTH<TH1F>(*fs, myHistoName.str().c_str(),
            myHistoLabel.str().c_str(), myMETBins, myMETMin, myMETMax));
      }
    }
    // Treat last bin
    myHistoName.str("");
    myHistoLabel.str("");
    myHistoName << name << "TauPtRangeAbove" << fFactorizationBinLowEdges[myTableSize-1];
    myHistoLabel << name << "TauPtRangeAbove" << fFactorizationBinLowEdges[myTableSize-1] <<";MET, GeV;N/" 
      << static_cast<int>((myMETMax-myMETMin)/myMETBins) << " GeV"; 
    histograms.push_back(makeTH<TH1F>(*fs, myHistoName.str().c_str(),
      myHistoLabel.str().c_str(), myMETBins, myMETMin, myMETMax));
  }




  void QCDMeasurement::createNBtagsHistogramGroupByTauPt(std::string name, std::vector<TH1*>& histograms) {
    // Get tau pt edge table
    fFactorizationBinLowEdges = fFactorizationTable.getBinLowEdges();
    // Make histograms
    edm::Service<TFileService> fs;
    size_t myTableSize = fFactorizationBinLowEdges.size(); 
    int nBins = 10; // number of bins for the histograms
    double xMin = 0.0; // x range minimum
    double xMax = 10.0; // x range maximum
    std::stringstream myHistoName;
    std::stringstream myHistoLabel;

    /// Loop ofver all tau pT bins
    for (size_t i = 0; i < myTableSize; ++i) {
      myHistoName.str("");
      myHistoLabel.str("");
      if (i == 0) {
	// Treat first bin
	myHistoName << name << "TauPtRangeBelow" << fFactorizationBinLowEdges[0];
	myHistoLabel << name << "TauPtRangeBelow" << fFactorizationBinLowEdges[0] <<";NBtags;N/" << static_cast<int>((xMax-xMin)/nBins) << " BTag"; 
	histograms.push_back( fs->make<TH1F>(myHistoName.str().c_str(), myHistoLabel.str().c_str(), nBins, xMin, xMax) );
      } else {
	// Treat other bins
	myHistoName << name << "TauPtRange" << fFactorizationBinLowEdges[i-1] << "to" << fFactorizationBinLowEdges[i];
	myHistoLabel << name << "TauPtRange" << fFactorizationBinLowEdges[i-1] << "to" << fFactorizationBinLowEdges[i] << ";NBtags;N/"  << static_cast<int>((xMax-xMin)/nBins) << " BTag"; 
	histograms.push_back(fs->make<TH1F>(myHistoName.str().c_str(), myHistoLabel.str().c_str(), nBins, xMin, xMax));
      }
    }
    // Treat last bin
    myHistoName.str("");
    myHistoLabel.str("");
    myHistoName << name << "TauPtRangeAbove" << fFactorizationBinLowEdges[myTableSize-1];
    myHistoLabel << name << "TauPtRangeAbove" << fFactorizationBinLowEdges[myTableSize-1] <<";NBtags;N/"  << static_cast<int>((xMax-xMin)/nBins) << " BTag"; 
    histograms.push_back(fs->make<TH1F>(myHistoName.str().c_str(), myHistoLabel.str().c_str(), nBins, xMin, xMax));
    // Apply sumw2 on the histograms
    for (std::vector<TH1*>::iterator it = histograms.begin(); it != histograms.end(); ++it) {
      (*it)->Sumw2();
    }
    return;
  }




  void QCDMeasurement::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Read the prescale for the event and set the event weight as the prescale
    fEventWeight.updatePrescale(iEvent);
    increment(fAllCounter);

    // Apply PU re-weighting (Vertex weight)
    std::pair<double, size_t> weightSize = fVertexWeight.getWeightAndSize(iEvent, iSetup);
    if(!iEvent.isRealData())
      fEventWeight.multiplyWeight(weightSize.first);
    hVerticesBeforeWeight->Fill(weightSize.second);
    hVerticesAfterWeight->Fill(weightSize.second, fEventWeight.getWeight());

    // Trigger and HLT_MET cut (only applied to REAL data)
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup); 
// tmp    if (iEvent.isRealData()) {
      // Trigger is applied only if the data sample is real data
      // std::cout <<"*** QCDMeasurement.cc ***  isRealData = " << iEvent.isRealData() << std::endl;
      if(!triggerData.passedEvent()) return;
// tmp    }
    increment(fTriggerAndHLTMetCutCounter);
    hSelectionFlow->Fill(kQCDOrderTrigger, fEventWeight.getWeight());
//     if(!triggerData.passedEvent()) return;
//     increment(fTriggerAndHLTMetCutCounter);


    // Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return;
    increment(fPrimaryVertexCounter);
    hSelectionFlow->Fill(kQCDOrderVertexSelection, fEventWeight.getWeight());

    // Get MET just for reference; do not apply a MET cut but instead use P(MET>70 GeV) as weight
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);

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
    fMETHistogramsByTauPtAfterTauCandidateSelection[myFactorizationTableIndex]->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());


    // Apply Trigger efficiency parametrization weights (Right after calling Tau & MET functions)
    double triggerEfficiency = fTriggerEfficiency.efficiency(*(tauCandidateData.getSelectedTaus()[0]), *metData.getSelectedMET());
    //    if (!iEvent.isRealData() || fTauEmbeddingAnalysis.isEmbeddingInput()) {
/* tmp    if (!iEvent.isRealData() ) {
      // Apply trigger efficiency as weight for simulated events, or if the input is from tau embedding
      fEventWeight.multiplyWeight(triggerEfficiency);
  } tmp */


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


    // Clean jet collection from selected tau and apply NJets>=3 cut
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, mySelectedTau);
    if (jetData.getHadronicJetCount() >= 2) {
      increment(fJetSelectionCounter2);
    }
    if (!jetData.passedEvent()) return;
    increment(fJetSelectionCounter);
    hSelectionFlow->Fill(kQCDOrderJetSelection, fEventWeight.getWeight());
    hMETAfterJetSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());

    // Fill factorization info into histogram
    fMETHistogramsByTauPtAfterJetSelection[myFactorizationTableIndex]->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hMETFactorizationNJetsBefore->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
    if (metData.passedEvent())
      hMETFactorizationNJetsAfter->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
    hMETFactorizationNJets->Fill(mySelectedTau[0]->pt(), metData.getSelectedMET()->et(), fEventWeight.getWeight());


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
    BTagging::Data btagData = fBTagging.analyze(jetData.getSelectedJets());
    fNBtagsHistogramsByTauPtAfterJetSelection[myFactorizationTableIndex]->Fill(btagData.getBJetCount(), fEventWeight.getWeight());
    
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, mySelectedTau, jetData.getSelectedJets());
    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    TopSelection::Data topSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());

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
    // Continue best cut path


    // Apply rest of tauID without Rtau
    if(!tauDataForTauID.passedEvent()) return;
    increment(fOneProngTauIDWithoutRtauCounter);
    hSelectionFlow->Fill(kQCDOrderTauID, fEventWeight.getWeight());
    hWeightedMETAfterTauIDNoRtau->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterTauIDNoRtau->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterTauIDNoRtau->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    fMETHistogramsByTauPtAfterTauIsolation[myFactorizationTableIndex]->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());


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
  }
}
