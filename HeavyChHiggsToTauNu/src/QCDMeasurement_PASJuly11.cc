#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurement_PASJuly11.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/InvMassVetoOnJets.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

namespace HPlus {
  QCDMeasurement_PASJuly11::QCDMeasurement_PASJuly11(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    fAllCounter(eventCounter.addCounter("allEvents")),
    fTriggerAndHLTMetCutCounter(eventCounter.addCounter("Trigger_and_HLT_MET")),
    fPrimaryVertexCounter(eventCounter.addCounter("PrimaryVertex")),
    fOneProngTauSelectionCounter(eventCounter.addCounter("TauCandSelection")),
    fOneSelectedTauCounter(eventCounter.addCounter("TauCands==1")),
    fGlobalElectronVetoCounter(eventCounter.addCounter("GlobalElectronVeto")),
    fNonIsolatedElectronVetoCounter(eventCounter.addCounter("NonIsolatedElectronVeto")),
    fGlobalMuonVetoCounter(eventCounter.addCounter("GlobalMuonVeto")),
    fNonIsolatedMuonVetoCounter(eventCounter.addCounter("NonIsolatedMuonVeto")),
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
    fNonIsolatedElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("NonIsolatedElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fNonIsolatedMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("NonIsolatedMuonVeto"), eventCounter, eventWeight),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight, "MET"),
    fInvMassVetoOnJets(iConfig.getUntrackedParameter<edm::ParameterSet>("InvMassVetoOnJets"), eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, eventWeight),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, eventWeight),
    //fWeightedSelectedEventsAnalyzer("QCDm3p2_afterAllSelections_weighted"),
    //fNonWeightedSelectedEventsAnalyzer("QCDm3p2_afterAllSelections_nonWeighted"),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, eventWeight),
    fVertexWeight(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeight")),
    fTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiencyScaleFactor"), fEventWeight),
    fTree(iConfig.getUntrackedParameter<edm::ParameterSet>("Tree"), fBTagging.getDiscriminator()),
    fFactorizationTable(iConfig, "METTables")
    // fTriggerEmulationEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"))
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
   {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms
    hVerticesBeforeWeight = makeTH<TH1F>(*fs, "verticesBeforeWeight", "Number of vertices without weightingVertices;N_{events} / 1 Vertex", 30, 0, 30);
    hVerticesAfterWeight =  makeTH<TH1F>(*fs, "verticesAfterWeight", "Number of vertices with weighting; Vertices;N_{events} / 1 Vertex", 30, 0, 30);

    // Histograms in bins of another variable: in bins of tau pt /*
    /*createHistogramGroupByOtherVariableBins("QCD_MET_afterTauCandidateSelection_", fMETHistogramsByTauPtAfterTauCandidateSelection, 20, 0.0, 100.0, fFactorizationTable.getBinLowEdges(), "TauPt", "E_{T}^{miss}", "GeV");
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
    // MET-Tau Isolation Correlation check in tau pT bins
    createHistogramGroupByOtherVariableBins("QCD_MetInTauPtBins_AfterBigBox_withIsolation", fMetInTauPtBins_AfterBigBox_withIsolation, 20, 0.0, 100.0, fFactorizationTable.getBinLowEdges(), "TauPt", "E_{T}^{miss}", "GeV");
    createHistogramGroupByOtherVariableBins("QCD_MetInTauPtBins_AfterBigBox_withoutIsolation", fMetInTauPtBins_AfterBigBox_withoutIsolation, 20, 0.0, 100.0, fFactorizationTable.getBinLowEdges(), "TauPt", "E_{T}^{miss}", "GeV");
    // do-over with wider bins
    createHistogramGroupByOtherVariableBins("QCD_MetInWiderTauPtBins_AfterBigBox_withIsolation", fMetInWiderTauPtBins_AfterBigBox_withIsolation, 20, 0.0, 100.0, getWiderTauPtBins() , "TauPt", "E_{T}^{miss}", "GeV");
    createHistogramGroupByOtherVariableBins("QCD_MetInWiderTauPtBins_AfterBigBox_withoutIsolation", fMetInWiderTauPtBins_AfterBigBox_withoutIsolation, 20, 0.0, 100.0, getWiderTauPtBins(), "TauPt", "E_{T}^{miss}", "GeV");
    */
    // Histograms for later change of factorization map
    // MET factorization details
    int myCoefficientBinCount = fFactorizationTable.getCoefficientTableSize();
    /*hMETFactorizationNJetsBefore = makeTH<TH1F>(*fs, "QCD_METFactorization_NJetsBefore", "METFactorizationNJetsBefore;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationNJetsAfter = makeTH<TH1F>(*fs, "QCD_METFactorization_NJetsAfter", "METFactorizationNJetsAfter;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationNJets = makeTH<TH2F>(*fs, "QCD_METFactorization_NJets", "METFactorizationNJets;tau p_{T}, GeV/c;MET, GeV", 60, 0, 300., 60, 0., 300.);
    hMETFactorizationBJetsBefore = makeTH<TH1F>(*fs, "QCD_METFactorization_BJetsBefore", "METFactorizationBJetsBefore;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationBJetsAfter = makeTH<TH1F>(*fs, "QCD_METFactorization_BJetsAfter", "METFactorizationBJetsAfter;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hMETFactorizationBJets = makeTH<TH2F>(*fs, "QCD_METFactorization_BJets", "METFactorizationBJets;tau p_{T}, GeV/c;MET, GeV", 60, 0, 300., 60, 0., 300.);
*/

    // Correlation histograms
    /*hCorrelationMETAfterAllSelections = makeTH<TH1F>(*fs, "QCD_Correlation_TauPtAfterAllSelectionsAndMET", "NonWeightedTauPtAfterAllPlusMET;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
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
    */
    // Other control histograms
    hTauCandidateSelectionIsolatedPtMax = makeTH<TH1F>(*fs, "QCD_SelectedTauCandidateMaxIsolatedPt", "QCD_SelectedTauCandidateMaxIsolatedPt;Isol. track p_{T}, GeV/c; N_{jets} / 1 GeV/c", 100, 0., 100.);

    // Other histograms
    //hAlphaTAfterTauID = makeTH<TH1F>(*fs, "QCD_AlphaTAfterTauID", "QCD_hAlphaTAfterTauID;#alpha_{T};N_{events} / 0.1", 50, 0.0, 5.0);
    hTransverseMass_AfterBigBox = makeTH<TH1F>(*fs, "QCD_TransverseMass_AfterBigBox", "QCD_TransverseMass_AfterBigBox; m_{T}(#tau-cand, E_{T}^{miss}); N_{Events} / 10", 40, 0.0, 400.0); 
    hTransverseMass_AfterBigBoxAndMet = makeTH<TH1F>(*fs, "QCD_TransverseMass_AfterBigBoxAndMet", "QCD_TransverseMass_AfterBigBoxAndMet; m_{T}(#tau-cand, E_{T}^{miss}); N_{Events} / 10", 40, 0.0, 400.0); 
    hTransverseMass_AfterBigBoxAndBtag = makeTH<TH1F>(*fs, "QCD_TransverseMass_AfterBigBoxAndBtag", "QCD_TransverseMass_AfterBigBoxAndBtag; m_{T}(#tau-cand, E_{T}^{miss}); N_{Events} / 10", 40, 0.0, 400.0); 
    hTransverseMass_AfterBigBoxAndTauID = makeTH<TH1F>(*fs, "QCD_TransverseMass_AfterBigBoxAndTauID", "QCD_TransverseMass_AfterBigBoxAndTauID; m_{T}(#tau-cand, E_{T}^{miss}); N_{Events} / 10", 40, 0.0, 400.0); 


    hDeltaPhiMetTauCand_AfterBigBox = makeTH<TH1F>(*fs, "hDeltaPhiMetTauCand_AfterBigBox", "hDeltaPhiMetTauCand_AfterBigBox; #Delta#phi(#tau-cand, E_{T}^{miss}); N_{Events} / 5", 36, 0., 180.); 
    hDeltaPhiMetTauCand_AfterBigBoxAndMet = makeTH<TH1F>(*fs, "hDeltaPhiMetTauCand_AfterBigBoxAndMet", "hDeltaPhiMetTauCand_AfterBigBoxAndMet; #Delta#phi(#tau-cand, E_{T}^{miss}); N_{Events} / 5", 36, 0., 180.); 
    hDeltaPhiMetFirstLdgJet_AfterBigBox = makeTH<TH1F>(*fs, "hDeltaPhiMetFirstLdgJet_AfterBigBox", "hDeltaPhiMetFirstLdgJet_AfterBigBox; #Delta#phi(#tau-cand, E_{T}^{miss}); N_{Events} / 5", 36, 0., 180.); 
    hDeltaPhiMetSecondLdgJet_AfterBigBox = makeTH<TH1F>(*fs, "hDeltaPhiMetSecondLdgJet_AfterBigBox", "hDeltaPhiMetSecondLdgJet_AfterBigBox; #Delta#phi(#tau-cand, E_{T}^{miss}); N_{Events} / 5", 36, 0., 180.); 
    hDeltaPhiMetFirstLdgJet_AfterBigBoxAndMet = makeTH<TH1F>(*fs, "hDeltaPhiMetFirstLdgJet_AfterBigBoxAndMet", "hDeltaPhiMetFirstLdgJet_AfterBigBoxAndMet; #Delta#phi(#tau-cand, E_{T}^{miss}); N_{Events} / 5", 36, 0., 180.); 
    hDeltaPhiMetSecondLdgJet_AfterBigBoxAndMet = makeTH<TH1F>(*fs, "hDeltaPhiMetSecondLdgJet_AfterBigBoxAndMet", "hDeltaPhiMetSecondLdgJet_AfterBigBoxAndMet; #Delta#phi(#tau-cand, E_{T}^{miss}); N_{Events} / 5", 36, 0., 180.); 
    hRtau_AfterBigBox  = makeTH<TH1F>(*fs, "hRtau_AfterBigBox", "hRtau_AfterBigBox; R_{#tau}=p^{ldg.track}/E^{vis.#tau jet};N_{Events} / 0.02", 60, 0., 1.2);
    hRtauEfficiency_AfterBigBoxTauID = makeTH<TH1F>(*fs, "hRtauEfficiency_AfterBigBoxTauID", "hRtauEfficiency_AfterBigBoxTauID; pass;N_{Events}", 2, -0.5, 1.5);

    // Standard cut path
    TFileDirectory myDir = fs->mkdir("StdCutPath");
    hStdAfterNjets = makeTH<TH1F>(myDir, "After_Njets", "Njets;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdAfterMET = makeTH<TH1F>(myDir, "After_MET", "MET;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdAfterBjets = makeTH<TH1F>(myDir, "After_Bjets", "Bjets;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdAfterTauIDNoRtau = makeTH<TH1F>(myDir, "After_TauIDNoRtau", "tauIDNoRtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdAfterRtau = makeTH<TH1F>(myDir, "After_Rtau", "Rtau;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdFakeMETVeto = makeTH<TH1F>(myDir, "After_FakeMETVeto", "FakeMETVeto;tau p_{T} bin;N_{events}", myCoefficientBinCount, 0., myCoefficientBinCount);
    hStdTransverseMassAfterTauID = makeTH<TH1F>(myDir, "TransverseMass_AfterTauID", "TransverseMass_AfterTauID; m_{T}(#tau-jet, E_{T}^{miss}); N_{Events} / 10 GeV/c{^2}", 40, 0.0, 400.0);
    hStdTransverseMassAfterBTag = makeTH<TH1F>(myDir, "TransverseMass_AfterBTag", "TransverseMass_AfterBTag; m_{T}(#tau-jet, E_{T}^{miss}); N_{Events} / 10 GeV/c{^2}", 40, 0.0, 400.0);

    hSelectionFlow = makeTH<TH1F>(myDir, "QCD_SelectionFlow", "QCD_SelectionFlow;;N_{events}", 12, 0, 12);
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTrigger,"Trigger");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderVertexSelection,"Vertex");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTauCandidateSelection,"#tau candidate");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderElectronVeto,"Isol. e veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderMuonVeto,"Isol. #mu veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderJetSelection,"#geq 3 jets");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTauID,"#tau ID (no R_{#tau})");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderFakeMETVeto,"Further QCD rej.");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTopSelection,"Top mass");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderMETFactorized,"MET (factorized)");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderBTagFactorized,"#geq 1 b jet (factorized)");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderRtauFactorized,"R_{#tau} (factorized)");

    // PAS Control Plots
    /*hCtrlPlot_TauJetPt_AfterLeptonVeto_WithTauId = makeTH<TH1F>(*fs, "QCDCtrlPlot_TauJetPt_AfterLeptonVeto_WithTauId", "QCDCtrlPlot_TauJetPt_AfterLeptonVeto_WithTauId; #tau-jet p_{T} [GeV/c] ;N_{Events} / 5 GeV/c", 60, 0, 300);
    hCtrlPlot_TauJetLdgTrkPt_AfterLeptonVeto_WithTauId = makeTH<TH1F>(*fs, "QCDCtrlPlot_TauJetLdgTrkPt_AfterLeptonVeto_WithTauId", "QCDCtrlPlot_TauJetLdgTrkPt_AfterLeptonVeto_WithTauId; #tau-jet p_{T}^{LdgTrk} [GeV/c] ;N_{Events} / 5 GeV/c", 60, 0, 300);
    hCtrlPlot_Rtau_AfterLeptonVeto_WithTauId  = makeTH<TH1F>(*fs, "QCDCtrlPlot_Rtau_AfterLeptonVeto_WithTauId", "QCDCtrlPlot_Rtau_WithTauId; R_{#tau}=p^{ldg.track}/E^{vis.#tau jet};N_{Events} / 0.02", 60, 0., 1.2);
    hCtrlPlot_JetMultiplicity_AfterLeptonVeto_WithTauIdAndRtau = makeTH<TH1F>(*fs, "QCDCtrlPlot_JetMultiplicity_AfterLeptonVeto_WithTauIdAndRtau", "QCDCtrlPlot_JetMultiplicity_AfterLeptonVeto_WithTauIdAndRtau; Number of Selected Jets; N_{Events} / 1", 16, -0.5, 15.5);
    hCtrlPlot_MET_AfterLeptonVeto_WithTauIdAndRtau = makeTH<TH1F>(*fs, "QCDCtrlPlot_MET_AfterLeptonVeto_WithTauIdAndRtau", "QCDCtrlPlot_MET_AfterLeptonVeto_WithTauIdAndRtau; E_{T}^{miss} [GeV]; N_{Events} / 5 GeV", 60, 0.0, 300.0);
    hCtrlPlot_JetMultiplicity_AfterMET_WithTauIdAndRtau = makeTH<TH1F>(*fs, "QCDCtrlPlot_JetMultiplicity_AfterMET_WithTauIdAndRtau", "QCDCtrlPlot_JetMultiplicity_AfterMET_WithTauIdAndRtau; Number of Selected Jets; N_{Events} / 1", 16, -0.5, 15.5);
    hCtrlPlot_NBtags_AfterMET_WithTauIdAndRtau = makeTH<TH1F>(*fs, "QCDCtrlPlot_NBtags_AfterMET_WithTauIdAndRtau", "QCDCtrlPlot_NBtags_AfterMET_WithTauIdAndRtau; Number of B-tagged Jets; N_{Events} / 1", 16, -0.5, 15.5);
    hCtrlPlot_TransverseMass_AfterAllSelectionNoFakeMet = makeTH<TH1F>(*fs, "QCDCtrlPlot_TransverseMass_AfterAllSelectionNoFakeMet", "QCDCtrlPlot_TransverseMass_AfterAllSelectionNoFakeMet; m_{T}(#tau-jet, E_{T}^{miss}); N_{Events} / 1", 40, 0.0, 400.0);
    //attikis
    hCtrlPlot_TransverseMass_AfterJetSelection = makeTH<TH1F>(*fs, "QCDCtrlPlot_TransverseMass_AfterJetSelection", "QCDCtrlPlot_TransverseMass_AfterJetSelection; m_{T}(#tau-jet, E_{T}^{miss}); N_{Events} / 1", 40, 0.0, 400.0);
    hCtrlPlot_TransverseMass_AfterJetSelectionAndTauId = makeTH<TH1F>(*fs, "QCDCtrlPlot_TransverseMass_AfterJetSelectionAndTauId", "QCDCtrlPlot_TransverseMass_AfterJetSelectionAndTauId; m_{T}(#tau-jet, E_{T}^{miss}); N_{Events} / 1", 40, 0.0, 400.0);
    hCtrlPlot_TransverseMass_AfterJetSelectionMetAndBtag = makeTH<TH1F>(*fs, "QCDCtrlPlot_AfterJetSelectionMetAndBtag", "QCDCtrlPlot_TransverseMass_AfterJetSelectionMetAndBtag; m_{T}(#tau-jet, E_{T}^{miss}); N_{Events} / 1", 40, 0.0, 400.0);
    //
    hCtrlPlot_TauCandPt_AfterJetSelection = makeTH<TH1F>(*fs, "hCtrlPlot_TauCandPt_AfterJetSelection", "hCtrlPlot_TauCandPt_AfterJetSelection; #tau-cand p_{T} [GeV/c] ;N_{Events} / 5 GeV/c", 60, 0, 300);
    hCtrlPlot_JetMultiplicity_AfterMETNoJetSelection_WithTauIdAndRtau = makeTH<TH1F>(*fs, "QCDCtrlPlot_JetMultiplicity_AfterMETNoJetSelection_WithTauIdAndRtau", "QCDCtrlPlot_JetMultiplicity_AfterMETNoJetSelection_WithTauIdAndRtau; Number of Selected Jets; N_{Events} / 1", 16, -0.5, 15.5);

    createHistogramGroupByOtherVariableBins("QCDCtrlPlot_Counter_MetAndBtagEff_", fCtrlPlot_MetAndBtagEff_AfterJetSelection_ByTauPt, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "pass", "");
    //createHistogramGroupByOtherVariableBins("QCDCtrlPlot_Counter_MetAndBtagEffAfterFakeMet_", fCtrlPlot_MetAndBtagEff_AfterJetSelectionAndFakeMet_ByTauPt, 2, -0.5, 1.5, fFactorizationTable.getBinLowEdges(), "TauPt", "pass", "");
*/
    // Analysis variations
    //fAnalyses.push_back(AnalysisVariation(70., 10., myCoefficientBinCount));
    //fAnalyses.push_back(AnalysisVariation(70., 20., myCoefficientBinCount));
    /*fAnalyses.push_back(AnalysisVariation(70., 30., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(65., 10., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(65., 20., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(65., 30., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(60., 10., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(60., 20., myCoefficientBinCount));
    fAnalyses.push_back(AnalysisVariation(60., 30., myCoefficientBinCount));*/

    fTree.enableNonIsoLeptons(true);
    fTree.init(*fs);

   }

  QCDMeasurement_PASJuly11::~QCDMeasurement_PASJuly11() {}

  void QCDMeasurement_PASJuly11::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    analyze(iEvent, iSetup);
  }

  void QCDMeasurement_PASJuly11::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    // Read the prescale for the event and set the event weight as the prescale
    fEventWeight.updatePrescale(iEvent);
    fTree.setPrescaleWeight(fEventWeight.getWeight());
    increment(fAllCounter);

///////// Start vertex reweighting
    // Apply PU re-weighting (Vertex weight)
    std::pair<double, size_t> weightSize = fVertexWeight.getWeightAndSize(iEvent, iSetup);
    if(!iEvent.isRealData()) { 
      fEventWeight.multiplyWeight(weightSize.first);
      fTree.setPileupWeight(weightSize.first);
    }
    hVerticesBeforeWeight->Fill(weightSize.second);
    hVerticesAfterWeight->Fill(weightSize.second, fEventWeight.getWeight());
    fTree.setNvertices(weightSize.second);

///////// Start trigger
    // Trigger and HLT_MET cut; or trigger efficiency parametrisation
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup); 
    if(!triggerData.passedEvent()) return;
    increment(fTriggerAndHLTMetCutCounter);
    hSelectionFlow->Fill(kQCDOrderTrigger, fEventWeight.getWeight());

    // GenParticle analysis
    if(!iEvent.isRealData()) fGenparticleAnalysis.analyze(iEvent, iSetup);

///////// Start primary vertex
    // Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return;
    increment(fPrimaryVertexCounter);
    //hSelectionFlow->Fill(kQCDOrderVertexSelection, fEventWeight.getWeight());


///////// Tau candidate selection
    TauSelection::Data tauCandidateData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauCandidateData.passedEvent()) return;
    increment(fOneProngTauSelectionCounter);
    // Choose tau to be used throughout the event as the selected tau jet
    //edm::PtrVector<pat::Tau> mySelectedTau = chooseMostIsolatedTauCandidate(tauCandidateData.getSelectedTaus());
    // note: do not require here that only one tau has been found;
    // instead take first item from mySelectedTau as the tau in the event
    increment(fOneSelectedTauCounter);
    hSelectionFlow->Fill(kQCDOrderTauCandidateSelection,fEventWeight.getWeight());

    // FIXME (MK 20110921): not sure if this is the correct place to
    // apply the scale factor, but it is the same as if the scale
    // factor would be applied inside fOneProngTauSelection as before.
    // The offline tau which is used to derive the trigger scale
    // factor is required to pass the full tau ID, including isolation
    // etc, but the tau object here is not (yet) isolated.
    TriggerEfficiencyScaleFactor::Data triggerWeight = fTriggerEfficiencyScaleFactor.applyEventWeight(*(tauCandidateData.getCleanedTauCandidates()[0]));
    fTree.setTriggerWeight(triggerWeight.getEventWeight());

    double mySelectedTauPt = tauCandidateData.getCleanedTauCandidates()[0]->pt();
    int myFactorizationTableIndex = fFactorizationTable.getCoefficientTableIndexByPtAndEta(mySelectedTauPt,0.);


///////// Start global electron veto
    // ElectronVeto 
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return; 
    increment(fGlobalElectronVetoCounter);
    hSelectionFlow->Fill(kQCDOrderElectronVeto, fEventWeight.getWeight());

    // std::cout << "*** nonIsolatedElectronVetoData" << std::endl;
    NonIsolatedElectronVeto::Data nonIsolatedElectronVetoData = fNonIsolatedElectronVeto.analyze(iEvent, iSetup);
    if (!nonIsolatedElectronVetoData.passedEvent())  return;
    increment(fNonIsolatedElectronVetoCounter);
    // std::cout << "*** nonIsolatedElectronVetoData called" << std::endl;

///////// Start global muon veto
    // MuonVeto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return; 
    increment(fGlobalMuonVetoCounter);
    hSelectionFlow->Fill(kQCDOrderMuonVeto, fEventWeight.getWeight());

    NonIsolatedMuonVeto::Data nonIsolatedMuonVetoData = fNonIsolatedMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!nonIsolatedMuonVetoData.passedEvent()) return; 
    increment(fNonIsolatedMuonVetoCounter);


///////// Jet selection
    // Clean jet collection from selected tau and apply NJets>=3 cut
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauCandidateData.getCleanedTauCandidates()[0]);
    if (!jetData.passedEvent()) return;
    increment(fJetSelectionCounter);
    hSelectionFlow->Fill(kQCDOrderJetSelection, fEventWeight.getWeight());
    hStdAfterNjets->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
    
    // get the MET, but cut on it later
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);

    // alphaT - No cuts applied! Only produces plots
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauCandidateData.getCleanedTauCandidates()[0]), jetData.getSelectedJets());
    // increment(fEvtTopologyCounter);

    // It can happen (and happens) that mySelectedTau has more than 1
    // tau candidate, here we explicitly select only the first one
    // (with the hope that it is the correct one), because
    // SignalAnalysisTree accepts only one tau in the input container.
    // FIXME: how is jet selection affected by this? Sometimes there
    // is effectively a requirement of 5 jets?
    edm::PtrVector<pat::Tau> mySelectedTauFirst;
    mySelectedTauFirst.push_back(tauCandidateData.getCleanedTauCandidates()[0]);
    // FIXME: how to handle the top reco in QCD measurement?
    fTree.setFillWeight(fEventWeight.getWeight());
    fTree.setNonIsoLeptons(nonIsolatedMuonVetoData.getAllMuonswithTrkRef(), nonIsolatedElectronVetoData.getElectronswithGSFTrk());
    if(metData.getRawMET().isNonnull())
      fTree.setRawMET(metData.getRawMET());
    //    fTree.fill(iEvent, mySelectedTauFirst, jetData.getSelectedJets(), evtTopologyData.alphaT().fAlphaT);

///////// MET selection (factorise out)
    if (metData.passedEvent()) {
      increment(fMETCounter);
      hSelectionFlow->Fill(kQCDOrderMETFactorized, fEventWeight.getWeight());
      hStdAfterMET->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
    
      ///////// btag selection (factorise out)
      double myWeightWithoutBTagScale = fEventWeight.getWeight(); // needed because of btag scale factor 
      double EventWeightWithoutBTag = fEventWeight.getWeight(); // needed because of btag scale factor //attikis
      BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
      double EventWeightWithBTag = fEventWeight.getWeight(); // needed because of btag scale factor //attikis
      // Apply scale factor as weight to event
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
      if (btagData.passedEvent()) {
        increment(fMETCounter);
        hSelectionFlow->Fill(kQCDOrderBTagFactorized, fEventWeight.getWeight());
        hStdAfterBjets->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
        hStdTransverseMassAfterBTag->Fill(TransverseMass::reconstruct(*(tauCandidateData.getCleanedTauCandidates()[0]), *(metData.getSelectedMET())), fEventWeight.getWeight());
        // undo btag scale factor
        fEventWeight.multiplyWeight(myWeightWithoutBTagScale / fEventWeight.getWeight()); // needed because of btag scale factor
      }
    }
    
    /////////////////////    /////////////////////    /////////////////////
    /// BIG BOX: Produce plots
    METSelection::Data metDataBB  = fMETSelection.analyze(iEvent, iSetup);
    double EventWeightWithoutBTag = fEventWeight.getWeight(); // needed because of btag scale factor 
    BTagging::Data btagDataBB = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
    double EventWeightWithBTag = fEventWeight.getWeight(); // needed because of btag scale factor 
    TauSelection::Data tauDataForTauIDBB = fOneProngTauSelection.analyzeTauIDWithoutRtauOnCleanedTauCandidates(iEvent, iSetup, tauCandidateData.getCleanedTauCandidates()[0]);
    AfterBigBox(EventWeightWithBTag, EventWeightWithoutBTag, tauCandidateData, jetData, metDataBB, btagDataBB, tauDataForTauIDBB);
    /////////////////////    /////////////////////    /////////////////////

    // InvMassVeto - No cuts applied! Only produces plots 
//    InvMassVetoOnJets::Data invMassVetoOnJetsData =  fInvMassVetoOnJets.analyze( jetData.getSelectedJets() ); 
    // if(!invMassVetoOnJetsData.passedEvent()) return; 
    // increment(fInvMassVetoOnJetsCounter);


///////// Start parallel paths after big box

    // Apply non-standard cut paths
/*    analyzeCorrelation(metData, tauCandidateData.getCleanedTauCandidates()[0], tauCandidateData, tauDataForTauID, btagData, 
                       fakeMETData, forwardJetData, topSelectionData, myFactorizationTableIndex,
                       myEventWeightBeforeMetFactorization);
*/

    /* analysis variations cannot be done like this because of trigger scale factor!!!
      for(std::vector<AnalysisVariation>::iterator it = fAnalyses.begin(); it != fAnalyses.end(); ++it) {
      (*it).analyse(metData, tauCandidateData.getCleanedTauCandidates()[0], tauCandidateData, tauDataForTauID, btagData, 
                       fakeMETData, forwardJetData, topSelectionData, myFactorizationTableIndex,
                       myEventWeightBeforeMetFactorization);
    }*/

///////// Continue cut path to tau isolation and rtau

    // Apply rest of tauID without Rtau
    TauSelection::Data tauDataForTauID = fOneProngTauSelection.analyzeTauIDWithoutRtauOnCleanedTauCandidates(iEvent, iSetup, tauCandidateData.getCleanedTauCandidates()[0]);
    if(!tauDataForTauID.passedEvent()) return;
    increment(fOneProngTauIDWithoutRtauCounter);
    hSelectionFlow->Fill(kQCDOrderTauID, fEventWeight.getWeight());
    hStdAfterTauIDNoRtau->Fill(myFactorizationTableIndex, fEventWeight.getWeight());

    hStdTransverseMassAfterTauID->Fill(TransverseMass::reconstruct(*(tauCandidateData.getCleanedTauCandidates()[0]), *(metData.getSelectedMET())), fEventWeight.getWeight());

    // Factorize out Rtau
    if (tauDataForTauID.getBestTauCandidatePassedRtauStatus()) {
      increment(fOneProngTauIDWithRtauCounter);
      hSelectionFlow->Fill(kQCDOrderRtauFactorized, fEventWeight.getWeight());
      hStdAfterRtau->Fill(myFactorizationTableIndex, fEventWeight.getWeight());
    }

    // FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauCandidateData.getCleanedTauCandidates()[0], jetData.getSelectedJets());
    // ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    //TopSelection::Data topSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());


    /*
    // Apply FakeMETVeto
    hStdWeightedFakeMETVeto->Fill(fakeMETData.closestDeltaPhi(), fEventWeight.getWeight());
    hStdNonWeightedFakeMETVeto->Fill(fakeMETData.closestDeltaPhi(), myEventWeightBeforeMetFactorization);
    if (!fakeMETData.passedEvent()) return;
    increment(fFakeMETVetoCounter);
    //hSelectionFlow->Fill(kQCDOrderFakeMETVeto, fEventWeight.getWeight());
    hWeightedMETAfterFakeMETVeto->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterFakeMETVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterFakeMETVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);


    // Apply top mass reconstruction
    if (!topSelectionData.passedEvent()) return;
    increment(fTopSelectionCounter);
    //hSelectionFlow->Fill(kQCDOrderTopSelection, fEventWeight.getWeight());


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
    
    
    // Forward jet veto -- experimental
    if (!forwardJetData.passedEvent()) return;
    increment(fForwardJetVetoCounter);
    hWeightedMETAfterForwardJetVeto->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    hStdNonWeightedTauPtAfterForwardJetVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    if (metData.passedEvent())
      hMETPassProbabilityAfterForwardJetVeto->Fill(myFactorizationTableIndex, myEventWeightBeforeMetFactorization);
    
    */

  }



  edm::PtrVector<pat::Tau> QCDMeasurement_PASJuly11::chooseMostIsolatedTauCandidate(edm::PtrVector<pat::Tau> tauCandidates) {
    edm::PtrVector<pat::Tau> mySelectedTauCandidate;

    // TMP code starts - to be removed when all 42X pattuples are available
    //mySelectedTauCandidate.push_back(tauCandidates[0]); // take highest ET tau as the tau jet
    //return mySelectedTauCandidate;
    // TMP code ends
    
    edm::PtrVector<pat::Tau>::const_iterator myBestCandidate = tauCandidates.begin();
    double myBestPtMax = 9999.;
    for(edm::PtrVector<pat::Tau>::const_iterator iter = tauCandidates.begin(); iter != tauCandidates.end(); ++iter) {
      if (!(*iter)->isPFTau()) continue;
      const edm::Ptr<pat::Tau> iTau = *iter;
      double myValue = (*iter)->userFloat("byTightChargedMaxPt");
      if (myValue < myBestPtMax) {
        if (myValue < 0.5) {
          mySelectedTauCandidate.push_back(*iter);
          hTauCandidateSelectionIsolatedPtMax->Fill(myValue, fEventWeight.getWeight());
        } else {
          myBestPtMax = myValue;
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
  
  
  void QCDMeasurement_PASJuly11::AfterBigBox(double EventWeightWithBtag, double EventWeightWithoutBtag, const TauSelection::Data& tauCandidateDataBB, JetSelection::Data& jetDataBB, const METSelection::Data& metDataBB, const BTagging::Data& btagDataBB, const TauSelection::Data& tauDataForTauIDBB){
    
    double mt_TauCandAndMet = TransverseMass::reconstruct(*(tauDataForTauIDBB.getCleanedTauCandidates()[0]), *(metDataBB.getSelectedMET()) );
    double deltaPhiMetTauCand = reco::deltaPhi( *(tauDataForTauIDBB.getCleanedTauCandidates()[0]), *(metDataBB.getSelectedMET()) ) * 180./3.14159; 
    double deltaPhiMetFirstLdgJet = reco::deltaPhi( *(jetDataBB.getSelectedJets()[0]), *(metDataBB.getSelectedMET()) ) * 180./3.14159; 
    double deltaPhiMetSecondLdgJet = reco::deltaPhi( *(jetDataBB.getSelectedJets()[1]), *(metDataBB.getSelectedMET()) ) * 180./3.14159; 
    double BtagEventWeight = (EventWeightWithBtag)/(EventWeightWithoutBtag);
    fEventWeight.multiplyWeight( 1/BtagEventWeight); // undo btag scale factor, automaticall applied by  fBTagging.analyze(..);

    // Fill histograms: DeltaPhi(tauCand,MET)
    hDeltaPhiMetTauCand_AfterBigBox->Fill(deltaPhiMetTauCand, fEventWeight.getWeight());
    hDeltaPhiMetFirstLdgJet_AfterBigBox->Fill(deltaPhiMetFirstLdgJet, fEventWeight.getWeight());
    hDeltaPhiMetSecondLdgJet_AfterBigBox->Fill(deltaPhiMetSecondLdgJet, fEventWeight.getWeight());

    if(metDataBB.passedEvent() ){
      hDeltaPhiMetTauCand_AfterBigBoxAndMet->Fill(deltaPhiMetTauCand, fEventWeight.getWeight());
      hDeltaPhiMetFirstLdgJet_AfterBigBoxAndMet->Fill(deltaPhiMetFirstLdgJet, fEventWeight.getWeight());
      hDeltaPhiMetSecondLdgJet_AfterBigBoxAndMet->Fill(deltaPhiMetSecondLdgJet, fEventWeight.getWeight());
    }

    // Fill histograms: Transverse Mass
    hTransverseMass_AfterBigBox->Fill(mt_TauCandAndMet, fEventWeight.getWeight());

    // Standalone MET
    if(metDataBB.passedEvent() ){
      hTransverseMass_AfterBigBoxAndMet->Fill(mt_TauCandAndMet, fEventWeight.getWeight());
    }

    // Standalone Btaggig
    if(btagDataBB.passedEvent() ){
      fEventWeight.multiplyWeight(BtagEventWeight); // re-do btag scale factor
      hTransverseMass_AfterBigBoxAndBtag->Fill(mt_TauCandAndMet, fEventWeight.getWeight());
      fEventWeight.multiplyWeight( 1/BtagEventWeight); // re-undo btag scale factor
    }

    // Standalone TauID & Rtau
    if(tauDataForTauIDBB.passedEvent() ){
      hTransverseMass_AfterBigBoxAndTauID->Fill(mt_TauCandAndMet, fEventWeight.getWeight());
    
      // Rtau: If TauCandidate passes TauID (Loose) measure Rtau efficiency from data
      if (tauDataForTauIDBB.selectedTauPassedRtau()) {
	hRtau_AfterBigBox->Fill(tauDataForTauIDBB.getRtauOfSelectedTau() , fEventWeight.getWeight());
	hRtauEfficiency_AfterBigBoxTauID->Fill( 1.0, fEventWeight.getWeight());
      }else hRtauEfficiency_AfterBigBoxTauID->Fill( 0.0, fEventWeight.getWeight());
    }

    return;
}


  void QCDMeasurement_PASJuly11::createHistogramGroupByOtherVariableBins(std::string name, std::vector<TH1*>& histograms, const int nBins, double xMin, double xMax, std::vector<double> BinVariableBins, const TString BinVariableName, const TString VariableName, const TString VariableUnits ){

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

  void QCDMeasurement_PASJuly11::analyzeCorrelation(const METSelection::Data& METData, edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauCandidateData, const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data& forwardData, const TopSelection::Data& topSelectionData, int tauPtBin, double weightWithoutMET) {
    // Apply all selections of the standard cut path
    if (!tauData.passedEvent() || // Tau ID without Rtau
        !fakeMETData.passedEvent() || // fake MET veto
        !topSelectionData.passedEvent()) // top selection
      return;

    if (METData.passedEvent()) {
      //hCorrelationMETAfterAllSelections->Fill(tauPtBin, weightWithoutMET);
    }
    if (btagData.passedEvent()) {
      //hCorrelationBtagAfterAllSelections->Fill(tauPtBin, weightWithoutMET);
    }
    if (tauCandidateData.getBestTauCandidatePassedRtauStatus()) {
      //hCorrelationRtauAfterAllSelections->Fill(tauPtBin, weightWithoutMET);
      if (btagData.passedEvent()) {
        //hCorrelationBtagAndRtauAfterAllSelections->Fill(tauPtBin, weightWithoutMET);
      }
    }
    return;
  }

  void QCDMeasurement_PASJuly11::analyzePurities(const TauSelection::Data& tauDataForTauID, const JetSelection::Data &jetData, const METSelection::Data& METData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const int myTauPtIndex, double EventWeight, std::vector<TH1*> fPurityBeforeAfterJets, std::vector<TH1*> fPurityBeforeAfterJetsMet, std::vector<TH1*> fPurityBeforeAfterJetsMetBtag, std::vector<TH1*> fPurityBeforeAfterJetsFakeMet, std::vector<TH1*> fPurityBeforeAfterJetsTauIdNoRtau){
    
    
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
  

  QCDMeasurement_PASJuly11::AnalysisVariation::AnalysisVariation(double METcut, double fakeMETVetoCut, int nTauPtBins)
    : fMETCut(METcut),
      fFakeMETVetoCut(fakeMETVetoCut) {
    std::stringstream myName;
    myName << "QCDAnalysisVariation_METcut" << METcut << "_FakeMETCut" << fakeMETVetoCut;
    // Create histograms
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(myName.str());
    hAfterBigBox = makeTH<TH1F>(myDir, "AfterBigBox", "AfterBigBox", nTauPtBins, 0, nTauPtBins);
    hLeg1AfterBTagging = makeTH<TH1F>(myDir, "Leg1AfterBTagging", "Leg1AfterBTagging", nTauPtBins, 0, nTauPtBins);
    hLeg1AfterBTagging17 = makeTH<TH1F>(myDir, "Leg1AfterBTagging17", "Leg1AfterBTagging17", nTauPtBins, 0, nTauPtBins);
    hLeg1AfterBTagging33 = makeTH<TH1F>(myDir, "Leg1AfterBTagging33", "Leg1AfterBTagging33", nTauPtBins, 0, nTauPtBins);
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
  QCDMeasurement_PASJuly11::AnalysisVariation::~AnalysisVariation() { }
  void QCDMeasurement_PASJuly11::AnalysisVariation::analyse(const METSelection::Data& METData, edm::PtrVector<pat::Tau>& selectedTau, const TauSelection::Data& tauCandidateData, const TauSelection::Data& tauData, const BTagging::Data& btagData, const FakeMETVeto::Data& fakeMETData, const ForwardJetVeto::Data& forwardData, const TopSelection::Data& topSelectionData, int tauPtBin, double weightWithoutMET) {
    hAfterBigBox->Fill(tauPtBin, weightWithoutMET);
    // Leg 1
    if (METData.getSelectedMET()->et() > fMETCut) {
        hLeg1AfterMET->Fill(tauPtBin, weightWithoutMET);
      if (btagData.getMaxDiscriminatorValue() > 1.7)
        hLeg1AfterBTagging17->Fill(tauPtBin, weightWithoutMET);
      if (btagData.getMaxDiscriminatorValue() > 3.3)
        hLeg1AfterBTagging33->Fill(tauPtBin, weightWithoutMET);
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
      if (tauCandidateData.getBestTauCandidatePassedRtauStatus()) {
        hLeg2AfterRtau->Fill(tauPtBin, weightWithoutMET);
      }
      // Leg3
      hLeg3FakeMetVetoDistribution->Fill(fakeMETData.closestDeltaPhi(), weightWithoutMET);
      if (fakeMETData.closestDeltaPhi() > fFakeMETVetoCut) {
        hLeg3AfterFakeMETVeto->Fill(tauPtBin, weightWithoutMET);
      }
    }
  }

}

