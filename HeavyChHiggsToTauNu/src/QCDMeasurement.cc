 #include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurement.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"

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
    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight, 1),
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
    fFactorizationTable(iConfig, "METTables"),
    fTriggerEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiency")),
    fVertexWeight(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeight"))
    // fTriggerEmulationEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"))
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
   {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms
    hVerticesBeforeWeight = fs->make<TH1F>("verticesBeforeWeight", "Number of vertices without weightingVertices;N_{events} / 1 Vertex", 30, 0, 30);

    // Histograms with weights
    hVerticesAfterWeight =  fs->make<TH1F>("verticesAfterWeight", "Number of vertices with weighting; Vertices;N_{events} / 1 Vertex", 30, 0, 30);
    hMETAfterJetSelection = fs->make<TH1F>("QCD_METctrl_METAfterJetSelection", "METAfterJetSelection;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hMETAfterJetSelection->Sumw2();
    hWeightedMETAfterJetSelection = fs->make<TH1F>("QCD_METctrl_METAfterJetSelectionWeighted", "METAfterJetSelectionWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterJetSelection->Sumw2();
    hWeightedMETAfterTauIDNoRtau = fs->make<TH1F>("QCD_METctrl_METAfterTauIDNoRtauWeighted", "METAfterTauIDNoRtauWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterTauIDNoRtau->Sumw2();
    hWeightedMETAfterTauID = fs->make<TH1F>("QCD_METctrl_METAfterTauIDWeighted", "METAfterTauIDWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterTauID->Sumw2();
    hWeightedMETAfterBTagging = fs->make<TH1F>("QCD_METctrl_METAfterBTaggingWeighted", "METAfterBTaggingWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterBTagging->Sumw2();
    hWeightedMETAfterFakeMETVeto = fs->make<TH1F>("QCD_METctrl_METAfterFakeMETVetoWeighted", "METAfterFakeMETVetoWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterFakeMETVeto->Sumw2();
    hWeightedMETAfterForwardJetVeto = fs->make<TH1F>("QCD_METctrl_METAfterForwardJetVetoWeighted", "METAfterForwardJetVetoWeighted;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hWeightedMETAfterForwardJetVeto->Sumw2();

    createMETHistogramGroupByTauPt("QCD_MET_afterTauCandidateSelection", fMETHistogramsByTauPtAfterTauCandidateSelection);
    createMETHistogramGroupByTauPt("QCD_MET_afterJetSelection", fMETHistogramsByTauPtAfterJetSelection);
    createMETHistogramGroupByTauPt("QCD_MET_afterTauIsolation", fMETHistogramsByTauPtAfterTauIsolation);

    // Histograms for later change of factorization map

    // MET factorization details
    int myCoefficientBinCount = fFactorizationTable.getCoefficientTableSize();
    hMETFactorizationNJetsBefore = fs->make<TH1F>("QCD_METFactorization_NJetsBefore", "METFactorizationNJetsBefore;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationNJetsBefore->Sumw2();
    hMETFactorizationNJetsAfter = fs->make<TH1F>("QCD_METFactorization_NJetsAfter", "METFactorizationNJetsAfter;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationNJetsAfter->Sumw2();
    hMETFactorizationNJets = fs->make<TH2F>("QCD_METFactorization_NJets", "METFactorizationNJets;tau p_{T}, GeV/c;MET, GeV", 60, 0, 300., 60, 0., 300.);
    hMETFactorizationNJets->Sumw2();
    hMETFactorizationBJetsBefore = fs->make<TH1F>("QCD_METFactorization_BJetsBefore", "METFactorizationBJetsBefore;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationBJetsBefore->Sumw2();
    hMETFactorizationBJetsAfter = fs->make<TH1F>("QCD_METFactorization_BJetsAfter", "METFactorizationBJetsAfter;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationBJetsAfter->Sumw2();
    hMETFactorizationBJets = fs->make<TH2F>("QCD_METFactorization_BJets", "METFactorizationBJets;tau p_{T}, GeV/c;MET, GeV", 60, 0, 300., 60, 0., 300.);
    hMETFactorizationBJets->Sumw2();

    // Standard cut path
    hStdNonWeightedTauPtAfterJetSelection = fs->make<TH1F>("QCD_StdCutPath_TauPtAfterJetSelection", "NonWeightedTauPtAfterJetSelection;tau p_{T} bin;N_{events} after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterJetSelection->Sumw2();
    hStdNonWeightedTauPtAfterTauIDNoRtau = fs->make<TH1F>("QCD_StdCutPath_TauPtAfterTauIDNoRtau", "NonWeightedTauPtAfterTauIDNoRtau;tau p_{T} bin;N_{events} after TauIDNoRtau", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterTauIDNoRtau->Sumw2();
    hStdNonWeightedTauPtAfterTauID = fs->make<TH1F>("QCD_StdCutPath_TauPtAfterTauID", "NonWeightedTauPtAfterTauID;tau p_{T} bin;N_{events} after TauID", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterTauID->Sumw2();
    hStdNonWeightedTauPtAfterBTagging = fs->make<TH1F>("QCD_StdCutPath_TauPtAfterBTagging", "NonWeightedTauPtAfterBTagging;tau p_{T} bin;N_{events} after b tagging", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterBTagging->Sumw2();
    hStdNonWeightedTauPtAfterFakeMETVeto = fs->make<TH1F>("QCD_StdCutPath_TauPtAfterFakeMETVeto", "NonWeightedTauPtAfterFakeMETVeto;tau p_{T} bin;N_{events} after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterFakeMETVeto->Sumw2();
    hStdNonWeightedTauPtAfterForwardJetVeto = fs->make<TH1F>("QCD_StdCutPath_TauPtAfterForwardJetVeto", "NonWeightedTauPtAfterForwardJetVeto;tau p_{T} bin;N_{events} after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdNonWeightedTauPtAfterForwardJetVeto->Sumw2();
    hStdWeightedRtau = fs->make<TH1F>("QCD_StdCutPath_weighted_Rtau", "Rtau;Rtau;N_{events}/0.05", 24, 0., 1.2);
    hStdWeightedRtau->Sumw2();
    hStdWeightedBjets = fs->make<TH1F>("QCD_StdCutPath_weighted_Bjets", "Bjets;N_{b-tagged jets};N_{events}", 10, 0., 10.);
    hStdWeightedBjets->Sumw2();
    hStdWeightedFakeMETVeto = fs->make<TH1F>("QCD_StdCutPath_weighted_FakeMETVeto", "FakeMETVeto;min(#Delta#phi(MET, jets)), degrees;N_{events} / 5 degrees", 36, 0., 180.);
    hStdWeightedFakeMETVeto->Sumw2();
    hStdNonWeightedRtau = fs->make<TH1F>("QCD_StdCutPath_nonWeighted_Rtau", "Rtau;Rtau;N_{events}/0.05", 24, 0., 1.2);
    hStdNonWeightedRtau->Sumw2();
    hStdNonWeightedSelectedTauPt = fs->make<TH1F>("QCD_StdCutPath_nonWeighted_TauPtAfterTauID", "tau pT after tauID;#tau p_{T} after tauID;N_{events}/10 GeV/c", 30, 0., 300.);
    hStdNonWeightedSelectedTauPt->Sumw2();
    hStdNonWeightedSelectedTauEta = fs->make<TH1F>("QCD_StdCutPath_nonWeighted_TauEtaAfterTauID", "tau eta after tauID;#tau #eta after tauID;N_{events}/0.2", 30, -3., 3.);
    hStdNonWeightedSelectedTauEta->Sumw2();
    hStdNonWeightedBjets = fs->make<TH1F>("QCD_StdCutPath_nonWeighted_Bjets", "Bjets;N_{b-tagged jets};N_{events}", 10, 0., 10.);
    hStdNonWeightedBjets->Sumw2();
    hStdNonWeightedFakeMETVeto = fs->make<TH1F>("QCD_StdCutPath_nonWeighted_FakeMETVeto", "FakeMETVeto;min(#Delta#phi(MET, jets)), degrees;N_{events} / 5 degrees", 36, 0., 180.);
    hStdNonWeightedFakeMETVeto->Sumw2();


    // ABCD(tau isol. vs. b-tag) cut path
    for (int i = 0; i < 4; i++) {
      std::string myRegion;
      if (i == 0) myRegion = "NegNeg";
      else if (i == 1) myRegion = "NegPos";
      else if (i == 2) myRegion = "PosNeg";
      else if (i == 3) myRegion = "PosPos";

      std::stringstream myLabel;
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterJetSelection_" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterJetSelection[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterJetSelection;tau p_{T} bin;N_{events} after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBNonWeightedTauPtAfterJetSelection[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtvsMET" << myRegion;
      hABCDTauIsolBNonWeightedTauPtVsMET[i] = fs->make<TH2F>(myLabel.str().c_str(), "NonWeightedTauPtvsMET;tau p_{T}, GeV/c;MET, GeV", 60, 0, 300., 60, 0., 300.);
      hABCDTauIsolBNonWeightedTauPtVsMET[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterMET" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterMET[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterMET;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBNonWeightedTauPtAfterMET[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterRtau" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterRtau[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBNonWeightedTauPtAfterRtau[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterFakeMETVeto" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterFakeMETVeto[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterFakeMETVeto;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBNonWeightedTauPtAfterFakeMETVeto[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterForwardJetVeto" << myRegion;
      hABCDTauIsolBNonWeightedTauPtAfterForwardJetVeto[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterForwardJetVeto;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBNonWeightedTauPtAfterForwardJetVeto[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterFakeMETVetoWithFactorizedRtau" << myRegion;
      hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterFakeMETVeto[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterFakeMETVetoWithFactorizedRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterFakeMETVeto[i]->Sumw2();
      myLabel.str("");
      myLabel << "QCD_ABCDTauIsolB_TauPtAfterForwardJetVetoWithFactorizedRtau" << myRegion;
      hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterForwardJetVeto[i] = fs->make<TH1F>(myLabel.str().c_str(), "NonWeightedTauPtAfterForwardJetVetoWithFactorizedRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
      hABCDTauIsolBWithFactorizedRtauNonWeightedTauPtAfterForwardJetVeto[i]->Sumw2();
    }

    // Control histograms for P(MET>70)
    hMETPassProbabilityAfterJetSelection = fs->make<TH1F>("QCD_NoWeight_METPassProbAfterJetSelection", "NonWeightedMETPassProbAfterJetSelection;tau p_{T} bin;N_{events} for MET after jet selection", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterJetSelection->Sumw2();
    hMETPassProbabilityAfterTauIDNoRtau = fs->make<TH1F>("QCD_NoWeight_METPassProbAfterTauIDNoRtau", "NonWeightedMETPassProbAfterTauIDNoRtau;tau p_{T} bin;N_{events} for MET after TauIDNoRtau", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterTauIDNoRtau->Sumw2();
    hMETPassProbabilityAfterTauID = fs->make<TH1F>("QCD_NoWeight_METPassProbAfterTauID", "NonWeightedMETPassProbAfterTauID;tau p_{T} bin;N_{events} for MET after TauID", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterTauID->Sumw2();
    hMETPassProbabilityAfterBTagging = fs->make<TH1F>("QCD_NoWeight_METPassProbAfterBTagging", "NonWeightedMETPassProbAfterBTagging;tau p_{T} bin;N_{events} for MET after b tagging", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterBTagging->Sumw2();
    hMETPassProbabilityAfterFakeMETVeto = fs->make<TH1F>("QCD_NoWeight_METPassProbAfterFakeMETVeto", "NonWeightedMETPassProbAfterFakeMETVeto;tau p_{T} bin;N_{events} for MET after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterFakeMETVeto->Sumw2();
    hMETPassProbabilityAfterForwardJetVeto = fs->make<TH1F>("QCD_NoWeight_METPassProbAfterForwardJetVeto", "NonWeightedMETPassProbAfterForwardJetVeto;tau p_{T} bin;N_{events} for MET after fake MET veto", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETPassProbabilityAfterForwardJetVeto->Sumw2();
    
    // Other control histograms
    hTauCandidateSelectionIsolatedPtMax = fs->make<TH1F>("QCD_SelectedTauCandidateMaxIsolatedPt", "QCD_SelectedTauCandidateMaxIsolatedPt;Isol. track p_{T}, GeV/c; N_{jets} / 1 GeV/c", 100, 0., 100.);
    hTauCandidateSelectionIsolatedPtMax->Sumw2();

    // Other histograms
    hAlphaTAfterTauID = fs->make<TH1F>("QCD_AlphaTAfterTauID", "QCD_hAlphaTAfterTauID; #alpha_{T} , N_{events} / 0.1", 50, 0.0, 5.0);
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
	histograms.push_back(fs->make<TH1F>(myHistoName.str().c_str(), 
					    myHistoLabel.str().c_str(), myMETBins, myMETMin, myMETMax));
      } else {
	// Treat other bins
	myHistoName << name << "TauPtRange" << fFactorizationBinLowEdges[i-1] << "to" << fFactorizationBinLowEdges[i];
	myHistoLabel << name << "TauPtRange" << fFactorizationBinLowEdges[i-1] << "to" << fFactorizationBinLowEdges[i] << ";MET, GeV;N/" 
		     << static_cast<int>((myMETMax-myMETMin)/myMETBins) << " GeV"; 
	histograms.push_back(fs->make<TH1F>(myHistoName.str().c_str(), 
					    myHistoLabel.str().c_str(), myMETBins, myMETMin, myMETMax));
      }
    }
    // Treat last bin
    myHistoName.str("");
    myHistoLabel.str("");
    myHistoName << name << "TauPtRangeAbove" << fFactorizationBinLowEdges[myTableSize-1];
    myHistoLabel << name << "TauPtRangeAbove" << fFactorizationBinLowEdges[myTableSize-1] <<";MET, GeV;N/" 
		 << static_cast<int>((myMETMax-myMETMin)/myMETBins) << " GeV"; 
    histograms.push_back(fs->make<TH1F>(myHistoName.str().c_str(), 
						   myHistoLabel.str().c_str(), myMETBins, myMETMin, myMETMax));
    // Apply sumw2 on the histograms
    for (std::vector<TH1*>::iterator it = histograms.begin(); it != histograms.end(); ++it) {
      (*it)->Sumw2();
    }
  }

  void QCDMeasurement::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Read the prescale for the event and set the event weight as the prescale
    fEventWeight.updatePrescale(iEvent);
    increment(fAllCounter);
    // std::cout << "*** HERE" << std::endl;

    // Apply PU re-weighting (Vertex weight)
    std::pair<double, size_t> weightSize = fVertexWeight.getWeightAndSize(iEvent, iSetup);
    if(!iEvent.isRealData())
      fEventWeight.multiplyWeight(weightSize.first);
    hVerticesBeforeWeight->Fill(weightSize.second);
    hVerticesAfterWeight->Fill(weightSize.second, fEventWeight.getWeight());


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

    // Apply tau candidate selection (with or without Rtau control region)
    TauSelection::Data tauCandidateData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauCandidateData.passedEvent()) return;
    increment(fOneProngTauSelectionCounter);
    fPFTauIsolationCalculator.beginEvent(iEvent); // Set primary vertex to PF tau isolation calculation
    edm::PtrVector<pat::Tau> mySelectedTau = chooseMostIsolatedTauCandidate(tauCandidateData.getSelectedTaus());
    // Require that just one tau has been found
    if (mySelectedTau.size() != 1) return;
    increment(fOneSelectedTauCounter);
    
    double mySelectedTauPt = mySelectedTau[0]->pt();
    int myFactorizationTableIndex = fFactorizationTable.getCoefficientTableIndexByPtAndEta(mySelectedTauPt,0.);
    fMETHistogramsByTauPtAfterTauCandidateSelection[myFactorizationTableIndex]->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());


    // Apply Trigger efficiency parametrization weights (Right after calling Tau & MET functions)
    double triggerEfficiency = fTriggerEfficiency.efficiency(*(tauCandidateData.getSelectedTaus()[0]), *metData.getSelectedMET());
    //    if (!iEvent.isRealData() || fTauEmbeddingAnalysis.isEmbeddingInput()) {
    if (!iEvent.isRealData() ) {
      // Apply trigger efficiency as weight for simulated events, or if the input is from tau embedding
      fEventWeight.multiplyWeight(triggerEfficiency);
    }


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
    hMETAfterJetSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());

    // Fill factorization info into histogram
    fMETHistogramsByTauPtAfterJetSelection[myFactorizationTableIndex]->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hMETFactorizationNJetsBefore->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
    if (metData.passedEvent())
      hMETFactorizationNJetsAfter->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
    hMETFactorizationNJets->Fill(mySelectedTau[0]->pt(), metData.getSelectedMET()->et(), fEventWeight.getWeight());

    // Obtain weight for P(MET>70 GeV) and apply it
    double myEventWeightBeforeMetFactorization = fEventWeight.getWeight();
    // tmp fEventWeight.multiplyWeight(fFactorizationTable.getWeightByPtAndEta(mySelectedTauPt, 0.));
    hWeightedMETAfterJetSelection->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterJetSelection->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent()) {
      hMETPassProbabilityAfterJetSelection->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
      increment(fMETCounter);
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
    analyzeABCDByTauIsolationAndBTagging(metData, mySelectedTau, tauCandidateData, tauDataForTauID, btagData, fakeMETData, forwardJetData, myFactorizationTableIndex, myEventWeightBeforeMetFactorization);

    // Continue best cut path

    // Factorize out b-tagging
    hStdWeightedBjets->Fill(btagData.getBJetCount(), fEventWeight.getWeight());
    hStdNonWeightedBjets->Fill(btagData.getBJetCount(), myEventWeightBeforeMetFactorization);
    if (btagData.passedEvent()) {
      increment(fBTaggingCounter);
      hWeightedMETAfterBTagging->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      hStdNonWeightedTauPtAfterBTagging->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
      if (metData.passedEvent())
	hMETPassProbabilityAfterBTagging->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    }


    // Apply rest of tauID without Rtau
    if(!tauDataForTauID.passedEvent()) return;
    increment(fOneProngTauIDWithoutRtauCounter);
    hWeightedMETAfterTauIDNoRtau->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterTauIDNoRtau->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterTauIDNoRtau->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    fMETHistogramsByTauPtAfterTauIsolation[myFactorizationTableIndex]->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());


    // Factorize out Rtau cut
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


    // Has to be done after full TauID
    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    hAlphaTAfterTauID->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight());


    // Apply FakeMETVeto
    hStdWeightedFakeMETVeto->Fill(fakeMETData.closestDeltaPhi(), fEventWeight.getWeight());
    hStdNonWeightedFakeMETVeto->Fill(fakeMETData.closestDeltaPhi(), myEventWeightBeforeMetFactorization);
    if (!fakeMETData.passedEvent()) return;
    increment(fFakeMETVetoCounter);
    hWeightedMETAfterFakeMETVeto->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterFakeMETVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterFakeMETVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);

    // Apply TopMass reconstruction
    TopSelection::Data TopSelectionData = fTopSelection.analyze(jetData.getSelectedJets(), btagData.getSelectedJets());
    if (!TopSelectionData.passedEvent()) return;
    increment(fTopSelectionCounter);

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
      fPFTauIsolationCalculator.calculateHpsTight(**iter, &mySumPt, &myMaxPt, &myOccupancy);
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
    // FIXME: add code
    return mySelectedTauCandidate;
  }
  
  void QCDMeasurement::analyzeABCDByTauIsolationAndBTagging(const METSelection::Data& METData, edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauCandidateData, const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data forwardData, int tauPtBin, double weightWithoutMET) {
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

}
