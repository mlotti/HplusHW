#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementFactorised.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "TNamed.h"
#include <iomanip>

namespace HPlus {
  QCDMeasurementFactorised::QCDMeasurementFactorised(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper):
    fEventWeight(eventWeight),
    fHistoWrapper(histoWrapper),
    fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
    fTopRecoName(iConfig.getUntrackedParameter<std::string>("topReconstruction")),
    fTauPtBinLowEdges(iConfig.getUntrackedParameter<std::vector<double> >("factorisationTauPtBinLowEdges")),
    fTauEtaBinLowEdges(iConfig.getUntrackedParameter<std::vector<double> >("factorisationTauEtaBinLowEdges")),
    fNVerticesBinLowEdges(iConfig.getUntrackedParameter<std::vector<int> >("factorisationNVerticesBinLowEdges")),
    fTransverseMassRange(iConfig.getUntrackedParameter<std::vector<double> >("factorisationTransverseMassRange")),
    fFullMassRange(iConfig.getUntrackedParameter<std::vector<double> >("factorisationFullMassRange")),
    fAllCounter(eventCounter.addCounter("Offline selection begins")),
    fVertexReweighting(eventCounter.addCounter("Vertex reweighting")),
    fWJetsWeightCounter(eventCounter.addCounter("WJets inc+exl weight")),
    fMETFiltersCounter(eventCounter.addCounter("MET filters")),
    fTriggerCounter(eventCounter.addCounter("Trigger_and_HLT_MET")),
    fPrimaryVertexCounter(eventCounter.addCounter("PrimaryVertex")),
    fTausExistCounter(eventCounter.addCounter("TauCandSelection")),
    fControlPlotsMultipleTausCounter(eventCounter.addCounter("Rejected in ctrl plots (multiple taus)")),
    fTauTriggerScaleFactorCounter(eventCounter.addCounter("Tau trg scale factor")),
    fVetoTauCounter(eventCounter.addCounter("VetoTauSelection")),
    fElectronVetoCounter(eventCounter.addCounter("ElectronSelection")),
    fMuonVetoCounter(eventCounter.addCounter("MuonSelection")),
    //fNonIsolatedElectronVetoCounter(eventCounter.addCounter("NonIsolatedElectronVeto")),
    //fNonIsolatedMuonVetoCounter(eventCounter.addCounter("NonIsolatedMuonVeto")),
    fNJetsCounter(eventCounter.addCounter("JetSelection")),
    fFullTauIDCounter(eventCounter.addCounter("FullTauIDCounter")),
    fMETCounter(eventCounter.addCounter("MET")),
    fBTaggingCounter(eventCounter.addCounter("bTagging")),
    fBTaggingScaleFactorCounter(eventCounter.addCounter("btag scale factor")),
    fQCDTailKillerCounter(eventCounter.addCounter("QCD tail killer")),
    fDeltaPhiTauMETCounter(eventCounter.addCounter("DeltaPhiTauMET")),
    fMaxDeltaPhiJetMETCounter(eventCounter.addCounter("maxDeltaPhiJetMET")),
    fTopSelectionCounter(eventCounter.addCounter("top selection")),
    fCoincidenceAfterMETCounter(eventCounter.addCounter("coincidence after MET")),
    fCoincidenceAfterBjetsCounter(eventCounter.addCounter("coincidence after Btag")),
    fCoincidenceAfterDeltaPhiCounter(eventCounter.addCounter("coincidence after Delta phi")),
    fCoincidenceAfterSelectionCounter(eventCounter.addCounter("coincidence after full selection")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    fVetoTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("vetoTauSelection"),
                      iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"),
                      eventCounter, fHistoWrapper),
    fElectronSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("ElectronSelection"), fPrimaryVertexSelection.getSelectedSrc(), eventCounter, fHistoWrapper),
    //fNonIsolatedElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("NonIsolatedElectronVeto"), eventCounter, fHistoWrapper),
    fMuonSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MuonSelection"), eventCounter, fHistoWrapper),
    //fNonIsolatedMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("NonIsolatedMuonVeto"), eventCounter, fHistoWrapper),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, fHistoWrapper),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, fHistoWrapper, "MET"),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, fHistoWrapper),
    //fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    //fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, fHistoWrapper),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, fHistoWrapper),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, fHistoWrapper),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, fHistoWrapper),
    fTopWithWSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithWSelection"), eventCounter, fHistoWrapper),
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, fHistoWrapper),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, fHistoWrapper),
    fFullHiggsMassCalculator(eventCounter, fHistoWrapper),
    fMETFilters(iConfig.getUntrackedParameter<edm::ParameterSet>("metFilters"), eventCounter),
    fQCDTailKiller(iConfig.getUntrackedParameter<edm::ParameterSet>("QCDTailKiller"), eventCounter, fHistoWrapper),
    fPrescaleWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("prescaleWeightReader"), fHistoWrapper, "PrescaleWeight"),
    fPileupWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("pileupWeightReader"), fHistoWrapper, "PileupWeight"),
    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), fHistoWrapper, "TauCandidates"),
    fTauTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("tauTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fMETTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("metTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fWJetsWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("wjetsWeightReader"), fHistoWrapper, "WJetsWeight"),
    fTree(iConfig.getUntrackedParameter<edm::ParameterSet>("Tree"), fBTagging.getDiscriminator()),
    fSFUncertaintyAfterStandardSelections(fHistoWrapper, "AfterStandardSelections")
    // fTriggerEmulationEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"))
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
   {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms
    hVerticesBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesBeforeWeight", "Number of vertices without weighting;Vertices;N_{events} / 1 Vertex", 50, 0, 50);
    hVerticesAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesAfterWeight", "Number of vertices with weighting; Vertices;N_{events} / 1 Vertex", 50, 0, 50);
    hVerticesTriggeredBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "verticesTriggeredBeforeWeight", "Number of vertices triggered without weighting;Vertices;N_{events} / 1 Vertex", 50, 0, 50);
    hVerticesTriggeredAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "verticesTriggeredAfterWeight", "Number of vertices triggered with weighting; Vertices;N_{events} / 1 Vertex", 50, 0, 50);

    hTauEtaVsPhiAfterBasicSelectionsCollinear = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterBasicSelectionsCollinear", "TauEtaVsPhiAfterBasicSelectionsCollinear; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterBasicSelectionsCollinearOpposite = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterBasicSelectionsCollinearOpposite", "TauEtaVsPhiAfterBasicSelectionsCollinearOpposite; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterBasicSelectionsBackToBack = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterBasicSelectionsBackToBack", "TauEtaVsPhiAfterBasicSelectionsBackToBack; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterBasicSelectionsBackToBackOpposite = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterBasicSelectionsBackToBackOpposite", "TauEtaVsPhiAfterBasicSelectionsBackToBackOpposite; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterBasicSelectionsCollinearTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterBasicSelectionsCollinearTight", "TauEtaVsPhiAfterBasicSelectionsCollinearTight; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterBasicSelectionsBackToBackTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterBasicSelectionsBackToBackTight", "TauEtaVsPhiAfterBasicSelectionsBackToBackTight; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterMETLegCollinear = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterMETLegCollinear", "TauEtaVsPhiAfterMETLegCollinear; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterMETLegCollinearOpposite = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterMETLegCollinearOpposite", "TauEtaVsPhiAfterMETLegCollinearOpposite; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterMETLegBackToBack = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterMETLegBackToBack", "TauEtaVsPhiAfterMETLegBackToBack; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterMETLegBackToBackOpposite = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterMETLegBackToBackOpposite", "TauEtaVsPhiAfterMETLegBackToBackOpposite; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterMETLegCollinearTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterMETLegCollinearTight", "TauEtaVsPhiAfterMETLegCollinearTight; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterMETLegBackToBackTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterMETLegBackToBackTight", "TauEtaVsPhiAfterMETLegBackToBackTight; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterTauLegCollinear = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterTauLegCollinear", "TauEtaVsPhiAfterTauLegCollinear; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterTauLegCollinearOpposite = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterTauLegCollinearOpposite", "TauEtaVsPhiAfterTauLegCollinearOpposite; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterTauLegBackToBack = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterTauLegBackToBack", "TauEtaVsPhiAfterTauLegBackToBack; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterTauLegBackToBackOpposite = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterTauLegBackToBackOpposite", "TauEtaVsPhiAfterTauLegBackToBackOpposite; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterTauLegCollinearTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterTauLegCollinearTight", "TauEtaVsPhiAfterTauLegCollinearTight; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hTauEtaVsPhiAfterTauLegBackToBackTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "TauEtaVsPhiAfterTauLegBackToBackTight", "TauEtaVsPhiAfterTauLegBackToBackTight; #tau #eta;#tau #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);

    hJetEtaVsPhiAfterBasicSelectionsCollinear = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterBasicSelectionsCollinear", "JetEtaVsPhiAfterBasicSelectionsCollinear; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hJetEtaVsPhiAfterBasicSelectionsCollinearTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterBasicSelectionsCollinearTight", "JetEtaVsPhiAfterBasicSelectionsCollinearTight; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hJetEtaVsPhiAfterBasicSelectionsBackToBack = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterBasicSelectionsBackToBack", "JetEtaVsPhiAfterBasicSelectionsBackToBack; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hJetEtaVsPhiAfterBasicSelectionsBackToBackTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterBasicSelectionsBackToBackTight", "JetEtaVsPhiAfterBasicSelectionsBackToBackTight; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hJetEtaVsPhiAfterMETLegCollinear = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterMETLegCollinear", "JetEtaVsPhiAfterMETLegCollinear; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hJetEtaVsPhiAfterMETLegCollinearTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterMETLegCollinearTight", "JetEtaVsPhiAfterMETLegCollinearTight; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hJetEtaVsPhiAfterMETLegBackToBack = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterMETLegBackToBack", "JetEtaVsPhiAfterMETLegBackToBack; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hJetEtaVsPhiAfterMETLegBackToBackTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterMETLegBackToBackTight", "JetEtaVsPhiAfterMETLegBackToBackTight; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hJetEtaVsPhiAfterTauLegCollinear = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterTauLegCollinear", "JetEtaVsPhiAfterTauLegCollinear; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hJetEtaVsPhiAfterTauLegCollinearTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterTauLegCollinearTight", "JetEtaVsPhiAfterTauLegCollinearTight; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hJetEtaVsPhiAfterTauLegBackToBack = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterTauLegBackToBack", "JetEtaVsPhiAfterTauLegBackToBack; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);
    hJetEtaVsPhiAfterTauLegBackToBackTight = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "JetEtaVsPhiAfterTauLegBackToBackTight", "JetEtaVsPhiAfterTauLegBackToBackTight; Jet #eta;Jet #phi", 60, -3.0, 3.0, 360, -3.1415926, 3.1415926);

    // Factorisation map
    int myTauPtBins = static_cast<int>(fTauPtBinLowEdges.size()) + 1;
    int myTauEtaBins = static_cast<int>(fTauEtaBinLowEdges.size()) + 1;
    int myNVerticesBins = static_cast<int>(fNVerticesBinLowEdges.size()) + 1;
    // Transverse mass bins
    if (fTransverseMassRange.size() != 3)
      throw cms::Exception("Configuration") << "QCDMeasurementFactorised: need to provide config param. factorisationTransverseMassRange = (nbins, min, max)!";
    double myDelta = (fTransverseMassRange[2]-fTransverseMassRange[1]) / fTransverseMassRange[0];
    for (double i = 0; i < fTransverseMassRange[0]; ++i) {
      fTransverseMassBinLowEdges.push_back(i * myDelta);
    }
    // Full mass bins
    if (fFullMassRange.size() != 3)
      throw cms::Exception("Configuration") << "QCDMeasurementFactorised: need to provide config param. factorisationFullMassRange = (nbins, min, max)!";
    myDelta = (fFullMassRange[2]-fFullMassRange[1]) / fFullMassRange[0];
    for (double i = 0; i < fFullMassRange[0]; ++i) {
      fFullMassRange.push_back(i * myDelta);
    }
    // Factorisation histograms
    TFileDirectory myDir = fs->mkdir("factorisation");
    hAfterJetSelection = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "AfterJetSelection", "AfterJetSelection", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hAfterJetSelection);
    hAfterJetSelectionMET20 = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "AfterJetSelectionMET20", "AfterJetSelectionMET20", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hAfterJetSelectionMET20);
    hAfterJetSelectionMET30 = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "AfterJetSelectionMET30", "AfterJetSelectionMET30", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hAfterJetSelectionMET30);
    hLeg1AfterMET = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg1AfterMET", "Leg1AfterMET", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hLeg1AfterMET);
    hLeg1AfterBTagging = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg1AfterBTagging", "Leg1AfterBTagging", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hLeg1AfterBTagging);
    hLeg1AfterDeltaPhiTauMET = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg1AfterDeltaPhiTauMET", "Leg1AfterDeltaPhiTauMET", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hLeg1AfterDeltaPhiTauMET);
    hLeg1AfterMaxDeltaPhiJetMET = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg1AfterMaxDeltaPhiJetMET", "Leg1AfterMaxDeltaPhiJetMET", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hLeg1AfterMaxDeltaPhiJetMET);
    hLeg1AfterTopSelection = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg1AfterTopSelection", "Leg1AfterTopSelection", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hLeg1AfterTopSelection);
    hLeg2AfterTauID = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg2AfterTauID", "Leg2AfterTauID", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hLeg2AfterTauID);
    hLeg2AfterTauIDMET20 = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg2AfterTauIDMET20", "Leg2AfterTauIDMET20", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hLeg2AfterTauIDMET20);
    hLeg2AfterTauIDMET30 = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg2AfterTauIDMET30", "Leg2AfterTauIDMET30", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hLeg2AfterTauIDMET30);
    hLeg2AfterTauIDNoRtau = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg2AfterTauIDNoRtau", "Leg2AfterTauIDNoRtau", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hLeg2AfterTauIDNoRtau);
    hLeg2AfterTauIDNoRtauMET20 = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg2AfterTauIDNoRtauMET20", "Leg2AfterTauIDNoRtauMET20", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hLeg2AfterTauIDNoRtauMET20);
    hLeg2AfterTauIDNoRtauMET30 = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg2AfterTauIDNoRtauMET30", "Leg2AfterTauIDNoRtauMET30", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hLeg2AfterTauIDNoRtauMET30);
    // ABCD factorisation
    hABCDAfterBasicSelection = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "ABCDAfterBasicSelection", "ABCDAfterBasicSelection", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hABCDAfterBasicSelection);
    hABCDAfterTauLeg = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "ABCDAfterTauLeg", "ABCDAfterTauLeg", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hABCDAfterTauLeg);
    hABCDAfterMETLeg = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "ABCDAfterMETLeg", "ABCDAfterMETLeg", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    setAxisLabelsForTH3(hABCDAfterMETLeg);

    // Mt and full mass shape histograms
    //createShapeHistograms(fs, hMtShapesAfterJetSelection, "MtShapesAfterJetSelection", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterStandardSelection, "MtShapesAfterStandardSelection", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterStandardSelectionMET20, "MtShapesAfterStandardSelectionMET20", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterStandardSelectionMET30, "MtShapesAfterStandardSelectionMET30", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterTauIDNoRtau, "MtShapesAfterTauIDNoRtau", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterTauID, "MtShapesAfterTauID", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterTauIDNoRtauMET20, "MtShapesAfterTauIDNoRtauMET20", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterTauIDMET20, "MtShapesAfterTauIDMET20", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterTauIDNoRtauMET30, "MtShapesAfterTauIDNoRtauMET30", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterTauIDMET30, "MtShapesAfterTauIDMET30", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterFullMETLeg, "MtShapesAfterFullMETLeg", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterMetLegNoBtagging, "MtShapesAfterMetLegNoBtagging", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterMet, "MtShapesAfterMet", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterMetAndBTagging, "MtShapesAfterMetAndBTagging", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    //createShapeHistograms(fs, hFullMassShapesAfterJetSelection, "FullMassShapesAfterJetSelection", fFullMassRange[0], fFullMassRange[1], fFullMassRange[2]);
    createShapeHistograms(fs, hFullMassShapesAfterFullMETLeg, "FullMassShapesAfterFullMETLeg", fFullMassRange[0], fFullMassRange[1], fFullMassRange[2]);
    //createShapeHistograms(fs, hFullMassShapesAfterMetLegNoBtagging, "FullMassShapesAfterMetLegNoBtagging", fFullMassRange[0], fFullMassRange[1], fFullMassRange[2]);

    createShapeHistograms(fs, hABCDMtShapesAfterBasicSelection, "ABCDMtShapesAfterBasicSelection", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hABCDMtShapesAfterTauLeg, "ABCDMtShapesAfterTauLeg", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hABCDMtShapesAfterMETLeg, "ABCDMtShapesAfterMETLeg", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hABCDMtShapesAfterMETLegNoBtag, "ABCDMtShapesAfterMETLegNoBtag", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);

    // Control plots
    createShapeHistograms(fs, hCtrlNjets, "CtrlLeg1AfterNjets", 10, 0., 10.);
    createShapeHistograms(fs, hCtrlNjetsMET20, "CtrlLeg1AfterNjetsMET20", 10, 0., 10.);
    createShapeHistograms(fs, hCtrlNjetsMET30, "CtrlLeg1AfterNjetsMET30", 10, 0., 10.);
    createShapeHistograms(fs, hCtrlNjetsAfterMET, "CtrlLeg1NJetsAfterMET", 10, 0., 10.);
    createShapeHistograms(fs, hCtrlMET, "CtrlLeg1AfterMET", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlMETAfterStandardSelections, "CtrlLeg1METAfterStandardSelections", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlMETAfterStandardSelectionsMET20, "CtrlLeg1METAfterStandardSelectionsMET20", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlMETAfterStandardSelectionsMET30, "CtrlLeg1METAfterStandardSelectionsMET30", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlMETAfterBtagging, "CtrlLeg1METAfterBtagging", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlMETAfterBtaggingAndDeltaPhi, "CtrlLeg1METAfterBtaggingAndDeltaPhi", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlMETAfterTauIDNoRtau, "CtrlLeg1METAfterTauIDNoRtau", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlMETAfterTauIDNoRtauMET20, "CtrlLeg1METAfterTauIDNoRtauMET20", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlMETAfterTauIDNoRtauMET30, "CtrlLeg1METAfterTauIDNoRtauMET30", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlMETAfterFullTauID, "CtrlLeg1METAfterFullTauID", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlMETAfterFullTauIDMET20, "CtrlLeg1METAfterFullTauIDMET20", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlMETAfterFullTauIDMET30, "CtrlLeg1METAfterFullTauIDMET30", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlNbjets, "CtrlLeg1AfterNbjets", 10, 0., 10.0);
    createShapeHistograms(fs, hCtrlDeltaPhiTauMET, "CtrlLeg1AfterDeltaPhiTauMET", 36, 0., 180.);
    createShapeHistograms(fs, hCtrlMaxDeltaPhiJetMET, "CtrlLeg1AfterMaxDeltaPhiJetMET", 36, 0., 180.);
    createShapeHistograms(fs, hCtrlTopMass, "CtrlLeg1AfterTopMass", 80, 0., 400.);

    createShapeHistograms(fs, hABCDCtrlNJets, "ABCDCtrlNJets", 10, 0., 10.);
    createShapeHistograms(fs, hABCDCtrlMET, "ABCDCtrlMET", 100, 0.0, 500.0);
    createShapeHistograms(fs, hABCDCtrlNbjets, "ABCDCtrlNbjets", 10, 0., 10.);
    createShapeHistograms(fs, hABCDCtrlDeltaPhiTauMET, "ABCDCtrlDeltaPhiTauMET", 36, 0., 180.);

    // Feature plots
    createShapeHistograms(fs, hFeatureMinEtaOfSelectedJetToGapAfterBasicSelection, "FeatureMinEtaOfSelectedJetToGapAfterBasicSelection", 30, 0, 3.0);
    createShapeHistograms(fs, hFeatureMinEtaOfSelectedJetToGapAfterMETLeg, "FeatureMinEtaOfSelectedJetToGapAfterMETLeg", 30, 0, 3.0);
    createShapeHistograms(fs, hFeatureMinEtaOfSelectedJetToGapAfterTauLeg, "FeatureMinEtaOfSelectedJetToGapAfterTauLeg", 30, 0, 3.0);
    createShapeHistograms(fs, hFeatureEtaSpreadOfSelectedJetsAfterBasicSelection, "FeatureEtaSpreadOfSelectedJetsAfterBasicSelection", 60, 0, 6.0);
    createShapeHistograms(fs, hFeatureEtaSpreadOfSelectedJetsAfterMETLeg, "FeatureEtaSpreadOfSelectedJetsAfterMETLeg", 60, 0, 6.0);
    createShapeHistograms(fs, hFeatureEtaSpreadOfSelectedJetsAfterTauLeg, "FeatureEtaSpreadOfSelectedJetsAfterTauLeg", 60, 0, 6.0);
    createShapeHistograms(fs, hFeatureAverageEtaOfSelectedJetsAfterBasicSelection, "FeatureAverageEtaOfSelectedJetsAfterBasicSelection", 60, 0, 6.0);
    createShapeHistograms(fs, hFeatureAverageEtaOfSelectedJetsAfterMETLeg, "FeatureAverageEtaOfSelectedJetsAfterMETLeg", 60, 0, 6.0);
    createShapeHistograms(fs, hFeatureAverageEtaOfSelectedJetsAfterTauLeg, "FeatureAverageEtaOfSelectedJetsAfterTauLeg", 60, 0, 6.0);
    createShapeHistograms(fs, hFeatureAverageSelectedJetsEtaDistanceToTauEtaAfterBasicSelection, "FeatureAverageSelectedJetsEtaDistanceToTauEtaAfterBasicSelection", 60, 0, 6.0);
    createShapeHistograms(fs, hFeatureAverageSelectedJetsEtaDistanceToTauEtaAfterMETLeg, "FeatureAverageSelectedJetsEtaDistanceToTauEtaAfterMETLeg", 60, 0, 6.0);
    createShapeHistograms(fs, hFeatureAverageSelectedJetsEtaDistanceToTauEtaAfterTauLeg, "FeatureAverageSelectedJetsEtaDistanceToTauEtaAfterTauLeg", 60, 0, 6.0);

    // Other control histograms

    // Selection flow histogram
    hSelectionFlow = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "QCD_SelectionFlow", "QCD_SelectionFlow;;N_{events}", 12, 0, 12);
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTrigger,"Trigger");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderVertexSelection,"Vertex");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTauCandidateSelection,"#tau cand.");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderElectronVeto,"Isol. e veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderMuonVeto,"Isol. #mu veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderJetSelection,"N_{jets}");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTauID,"tauID");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderMET,"MET");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderBTag,"N_{b jets}");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderDeltaPhiTauMET,"#Delta#phi(#tau,MET)");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderMaxDeltaPhiJetMET,"#Delta#phi(jet,MET)");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTopSelection,"top reco");

    fTree.enableNonIsoLeptons(true);
    fTree.init(*fs);

   }

  QCDMeasurementFactorised::~QCDMeasurementFactorised() {}

  bool QCDMeasurementFactorised::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    return analyze(iEvent, iSetup);
  }

  bool QCDMeasurementFactorised::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
//------ Read the prescale for the event and set the event weight as the prescale
    fEventWeight.beginEvent();
    const double prescaleWeight = fPrescaleWeightReader.getWeight(iEvent, iSetup);
    fEventWeight.multiplyWeight(prescaleWeight);
    fTree.setPrescaleWeight(prescaleWeight);

    increment(fAllCounter);

//------ Vertex weight
    double myWeightBeforePileupReweighting = fEventWeight.getWeight();
    if(!iEvent.isRealData()) {
      const double myPileupWeight = fPileupWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(myPileupWeight);
      fTree.setPileupWeight(myPileupWeight);
    }

    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    size_t nVertices = pvData.getNumberOfAllVertices();
    int myNVerticesBinIndex = getNVerticesBinIndex(nVertices);
    hVerticesBeforeWeight->Fill(nVertices, myWeightBeforePileupReweighting);
    hVerticesAfterWeight->Fill(nVertices);
    fTree.setNvertices(nVertices);
    hSelectionFlow->Fill(kQCDOrderVertexSelection);
    increment(fVertexReweighting);

//------ For combining W+Jets inclusive and exclusive samples, do an event weighting here
    if(!iEvent.isRealData()) {
      const double wjetsWeight = fWJetsWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(wjetsWeight);
    }
    increment(fWJetsWeightCounter);

//------ MET (noise) filters for data (reject events with instrumental fake MET)
    if(iEvent.isRealData()) {
      if(!fMETFilters.passedEvent(iEvent, iSetup)) return false;
    }
    increment(fMETFiltersCounter);

//------ Apply trigger and HLT_MET cut or trigger parametrisation
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);
    hSelectionFlow->Fill(kQCDOrderTrigger);
    if(triggerData.hasTriggerPath()) // protection if TriggerSelection is disabled
      fTree.setHltTaus(triggerData.getTriggerTaus());

    hVerticesTriggeredBeforeWeight->Fill(nVertices, myWeightBeforePileupReweighting);
    hVerticesTriggeredAfterWeight->Fill(nVertices);


//------ GenParticle analysis (must be done here when we effectively trigger all MC)
    if (!iEvent.isRealData()) {
      GenParticleAnalysis::Data genData = fGenparticleAnalysis.analyze(iEvent, iSetup);
      fTree.setGenMET(genData.getGenMET());
    }


//------ Primary vertex selection
    if (!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    //hSelectionFlow->Fill(kQCDOrderVertexSelection);


//------ Tau candidate selection
    // Do tau candidate selection
    TauSelection::Data tauCandidateData = fTauSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
    if (!tauCandidateData.passedEvent()) return false;
    // Obtain MC matching - for EWK without genuine taus
    FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, *(tauCandidateData.getSelectedTau()));
    // Apply scale factor for fake tau
    if (!iEvent.isRealData())
      fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauCandidateData.getSelectedTau()->eta()));
    // note: do not require here that only one tau has been found; instead take first item from mySelectedTau as the tau in the event
    increment(fTausExistCounter);
    // Apply trigger scale factor here, because it depends only on tau
    TauTriggerEfficiencyScaleFactor::Data tauTriggerWeight = fTauTriggerEfficiencyScaleFactor.applyEventWeight(*(tauCandidateData.getSelectedTau()), iEvent.isRealData(), fEventWeight);
    fTree.setTauTriggerWeight(tauTriggerWeight.getEventWeight(), tauTriggerWeight.getEventWeightAbsoluteUncertainty());
    increment(fTauTriggerScaleFactorCounter);
    hSelectionFlow->Fill(kQCDOrderTauCandidateSelection);
    // Obtain tau pT bin index
    int myTauPtBinIndex = getTauPtBinIndex(tauCandidateData.getSelectedTau()->pt());
    int myTauEtaBinIndex = getTauEtaBinIndex(tauCandidateData.getSelectedTau()->eta());

    // Obtain boolean for rest of tauID for control plots
    //bool myPassedTauIDStatus = tauCandidateData.selectedTauPassesFullTauID();
    // Count how many tau candidates actually pass tau ID
    /*
    if (myPassedTauIDStatus) {
      int myFullTauIDPassedCount = 0;
      for (edm::PtrVector<pat::Tau>::iterator it = tauCandidateData.getSelectedTaus().begin(); it != tauCandidateData.getSelectedTaus().end(); ++it) {
        if ((*it)->selectedTauPassesFullTauID())
          ++myFullTauIDPassedCount;
      }
      // Require exactly 1 tau
      if (myFullTauIDPassedCount > 1)
        myPassedTauIDStatus = false;
    }*/

//------ Veto against second tau in event
    VetoTauSelection::Data vetoTauData = fVetoTauSelection.analyze(iEvent, iSetup, tauCandidateData.getSelectedTau(), pvData.getSelectedVertex()->z());
    //    if (vetoTauData.passedEvent()) return false;
    if (!vetoTauData.passedEvent()) increment(fVetoTauCounter);
    // Note: no return statement should be added here


//------ Global electron veto
    ElectronSelection::Data electronVetoData = fElectronSelection.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);
    hSelectionFlow->Fill(kQCDOrderElectronVeto);
    /*NonIsolatedElectronVeto::Data nonIsolatedElectronVetoData = fNonIsolatedElectronVeto.analyze(iEvent, iSetup);
    if (!nonIsolatedElectronVetoData.passedEvent())  return false;
    increment(fNonIsolatedElectronVetoCounter);*/
    // Control plot


//------ Global muon veto
    MuonSelection::Data muonVetoData = fMuonSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);
    hSelectionFlow->Fill(kQCDOrderMuonVeto);
    /*NonIsolatedMuonVeto::Data nonIsolatedMuonVetoData = fNonIsolatedMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!nonIsolatedMuonVetoData.passedEvent()) return; 
    increment(fNonIsolatedMuonVetoCounter);*/
    // Control plot


//------ Jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauCandidateData.getSelectedTau(), nVertices);
    if (!jetData.passedEvent()) return false;
    hCtrlNjets[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getHadronicJetCount());
    increment(fNJetsCounter);
    hSelectionFlow->Fill(kQCDOrderJetSelection);
    hAfterJetSelection->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);

    hFeatureMinEtaOfSelectedJetToGapAfterBasicSelection[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getMinEtaOfSelectedJetToGap());
    hFeatureEtaSpreadOfSelectedJetsAfterBasicSelection[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getEtaSpreadOfSelectedJets());
    hFeatureAverageEtaOfSelectedJetsAfterBasicSelection[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getAverageEtaOfSelectedJets());
    hFeatureAverageSelectedJetsEtaDistanceToTauEtaAfterBasicSelection[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getAverageSelectedJetsEtaDistanceToTauEta());

//------ Improved delta phi cut, a.k.a. QCD tail killer // FIXME: place of cut still to be determined
    METSelection::Data metDataTmp = fMETSelection.silentAnalyze(iEvent, iSetup, tauCandidateData.getSelectedTau(), jetData.getAllJets());

    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.analyze(iEvent, iSetup, tauCandidateData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metDataTmp.getSelectedMET());
    if (!qcdTailKillerData.passedEvent()) return false;
    increment(fQCDTailKillerCounter);

//------ Standard selections is done, obtain data objects, fill tree, and loop over analysis variations
    if (fTree.isActive()) {
      // Obtain MET data
      METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauCandidateData.getSelectedTau(), jetData.getAllJets());
      // Obtain btagging data
      BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
      // Obtain alphaT
      EvtTopology::Data evtTopologyData = fEvtTopology.analyze(iEvent, iSetup, *(tauCandidateData.getSelectedTau()), jetData.getSelectedJetsIncludingTau());
      // Top reconstruction in different versions
      TopSelection::Data topSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
      BjetSelection::Data bjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauCandidateData.getSelectedTau(), metData.getSelectedMET());
      TopChiSelection::Data topChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
      TopWithBSelection::Data topWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), bjetSelectionData.getBjetTopSide());

      // Fill tree
      if(metData.getRawMET().isNonnull())
        fTree.setRawMET(metData.getRawMET());
      if(metData.getType1MET().isNonnull())
        fTree.setType1MET(metData.getType1MET());
      if(metData.getType2MET().isNonnull())
        fTree.setType2MET(metData.getType2MET());
      if(metData.getCaloMET().isNonnull())
        fTree.setCaloMET(metData.getCaloMET());
      if(metData.getTcMET().isNonnull())
        fTree.setTcMET(metData.getTcMET());
      fTree.setFillWeight(fEventWeight.getWeight());
      if (!iEvent.isRealData()) {
        fEventWeight.multiplyWeight(btagData.getScaleFactor()); // needed to calculate the scale factor and the uncertainties
      }
      fTree.setBTagging(btagData.passedEvent(), btagData.getScaleFactor(), btagData.getScaleFactorAbsoluteUncertainty());
      //fTree.setTop(TopSelectionData.getTopP4());
      //fTree.setAlphaT(evtTopologyData.alphaT().fAlphaT);
      //fTree.setDeltaPhi(fakeMETData.closestDeltaPhi());
      fTree.fill(iEvent, tauCandidateData.getSelectedTau(), jetData.getSelectedJets());
      return true;
    }

    // Obtain MET and Delta phi(tau,MET), but don't apply cuts on them yet
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauCandidateData.getSelectedTau(), jetData.getAllJets());
    double deltaPhi = DeltaPhi::reconstruct(*(tauCandidateData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    double myOppositePhi = tauCandidateData.getSelectedTau()->phi() - 3.1415926;
    if (myOppositePhi < -3.1415926) myOppositePhi += 2.0*3.1415926;
    double transverseMass = TransverseMass::reconstruct(*(tauCandidateData.getSelectedTau()), *(metData.getSelectedMET()));
    hCtrlMETAfterStandardSelections[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
    hMtShapesAfterStandardSelection[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
    if (metData.getSelectedMET()->et() > 20) {
        hCtrlNjetsMET20[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getHadronicJetCount());
        hCtrlMETAfterStandardSelectionsMET20[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
        hMtShapesAfterStandardSelectionMET20[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
      if (metData.getSelectedMET()->et() > 30) {
        hCtrlNjetsMET30[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getHadronicJetCount());
        hCtrlMETAfterStandardSelectionsMET30[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
        hMtShapesAfterStandardSelectionMET30[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
      }
    }
    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetData.getSelectedJets().begin(); iJet != jetData.getSelectedJets().end(); ++iJet) {
      if (deltaPhi < 90) {
        hJetEtaVsPhiAfterBasicSelectionsCollinear->Fill((*iJet)->eta(), (*iJet)->phi());
        if (deltaPhi < 30) hJetEtaVsPhiAfterBasicSelectionsCollinearTight->Fill((*iJet)->eta(), (*iJet)->phi());
      } else {
        hJetEtaVsPhiAfterBasicSelectionsBackToBack->Fill((*iJet)->eta(), (*iJet)->phi());
        if (deltaPhi > 150) hJetEtaVsPhiAfterBasicSelectionsBackToBackTight->Fill((*iJet)->eta(), (*iJet)->phi());
      }
    }

    if (deltaPhi < 90) {
      hTauEtaVsPhiAfterBasicSelectionsCollinear->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
      hTauEtaVsPhiAfterBasicSelectionsCollinearOpposite->Fill(-tauCandidateData.getSelectedTau()->eta(), myOppositePhi);
      if (deltaPhi < 30) {
        hTauEtaVsPhiAfterBasicSelectionsCollinearTight->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
      }
    } else {
      hTauEtaVsPhiAfterBasicSelectionsBackToBack->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
      hTauEtaVsPhiAfterBasicSelectionsBackToBackOpposite->Fill(-tauCandidateData.getSelectedTau()->eta(), myOppositePhi);
      if (deltaPhi > 150) {
        hTauEtaVsPhiAfterBasicSelectionsBackToBackTight->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
      }
    }


// ----- Tau ID leg (factorisation
    bool myPassedTauLegStatus = false;
    if (tauCandidateData.selectedTauPassesNProngs() && tauCandidateData.selectedTauPassesIsolation()) {
      hCtrlMETAfterTauIDNoRtau[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
      hLeg2AfterTauIDNoRtau->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
      hMtShapesAfterTauIDNoRtau[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
      if (metData.getSelectedMET()->et() > 20) {
        hLeg2AfterTauIDNoRtauMET20->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
        hMtShapesAfterTauIDNoRtauMET20[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
        hCtrlMETAfterTauIDNoRtauMET20[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
        if (metData.getSelectedMET()->et() > 30) {
          hLeg2AfterTauIDNoRtauMET30->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
          hMtShapesAfterTauIDNoRtauMET30[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
          hCtrlMETAfterTauIDNoRtauMET30[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
        }
      }
      if (tauCandidateData.selectedTauPassesRtau()) {
        hLeg2AfterTauID->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
        hSelectionFlow->Fill(kQCDOrderTauID);
        increment(fFullTauIDCounter);
        myPassedTauLegStatus = true;
        hCtrlMETAfterFullTauID[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
        hMtShapesAfterTauID[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
        if (metData.getSelectedMET()->et() > 20) {
          hMtShapesAfterTauIDMET20[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
          hCtrlMETAfterFullTauIDMET20[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
          hLeg2AfterTauIDMET20->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
          if (metData.getSelectedMET()->et() > 30) {
            hMtShapesAfterTauIDMET30[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
            hCtrlMETAfterFullTauIDMET30[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
            hLeg2AfterTauIDMET30->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
          }
        }
        hFeatureMinEtaOfSelectedJetToGapAfterTauLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getMinEtaOfSelectedJetToGap());
        hFeatureEtaSpreadOfSelectedJetsAfterTauLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getEtaSpreadOfSelectedJets());
        hFeatureAverageEtaOfSelectedJetsAfterTauLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getAverageEtaOfSelectedJets());
        hFeatureAverageSelectedJetsEtaDistanceToTauEtaAfterTauLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getAverageSelectedJetsEtaDistanceToTauEta());

        for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetData.getSelectedJets().begin(); iJet != jetData.getSelectedJets().end(); ++iJet) {
          if (deltaPhi < 90) {
            hJetEtaVsPhiAfterTauLegCollinear->Fill((*iJet)->eta(), (*iJet)->phi());
            if (deltaPhi < 30) hJetEtaVsPhiAfterTauLegCollinearTight->Fill((*iJet)->eta(), (*iJet)->phi());
          } else {
            hJetEtaVsPhiAfterTauLegBackToBack->Fill((*iJet)->eta(), (*iJet)->phi());
            if (deltaPhi > 150) hJetEtaVsPhiAfterTauLegBackToBackTight->Fill((*iJet)->eta(), (*iJet)->phi());
          }
        }

        if (deltaPhi < 90) {
          hTauEtaVsPhiAfterTauLegCollinear->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
          hTauEtaVsPhiAfterTauLegCollinearOpposite->Fill(-tauCandidateData.getSelectedTau()->eta(), myOppositePhi);
          if (deltaPhi < 30) {
            hTauEtaVsPhiAfterTauLegCollinearTight->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
          }
        } else {
          hTauEtaVsPhiAfterTauLegBackToBack->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
          hTauEtaVsPhiAfterTauLegBackToBackOpposite->Fill(-tauCandidateData.getSelectedTau()->eta(), myOppositePhi);
          if (deltaPhi > 150) {
            hTauEtaVsPhiAfterTauLegBackToBackTight->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
          }
        }
        // On purpose: No return statement for false (factorisation)
      }
    }
    // ABCD test
    // FIXME
/*    if (metData.getSelectedMET()->et() < metData.getCutValue()) {
      if (tauCandidateData.selectedTauPassesNProngs() && tauCandidateData.selectedTauPassesRtau()) {
        if (tauCandidateData.selectedTauPassesNProngsAndRtauButNotIsolation()) {
          // Basic point for ABCD
          hABCDAfterBasicSelection->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
          hABCDMtShapesAfterBasicSelection[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
          hABCDCtrlNJets[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getHadronicJetCount());
        } else {
          // Tau leg for ABCD
          hABCDAfterTauLeg->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
          hABCDMtShapesAfterTauLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
        }
      }
    }*/

// ----- MET, btag, deltaPhi(tau,MET), top reco leg
    // MET cut
    hCtrlMET[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
    if(!metData.passedEvent()) return false;
    increment(fMETCounter);
    hSelectionFlow->Fill(kQCDOrderMET);
    hLeg1AfterMET->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
    if (myPassedTauLegStatus) increment(fCoincidenceAfterMETCounter);
    hCtrlNjetsAfterMET[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getHadronicJetCount());

    if (deltaPhi < fDeltaPhiCutValue) {
      // Fill mT shape without btagging
      hMtShapesAfterMetLegNoBtagging[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
      if (tauCandidateData.selectedTauPassesNProngsAndRtauButNotIsolation()) {
        // MET leg point without btag for ABCD
        hABCDMtShapesAfterMETLegNoBtag[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
      }
    }
    hMtShapesAfterMet[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
    if (tauCandidateData.selectedTauPassesNProngsAndRtauButNotIsolation()) {
      hABCDCtrlMET[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
    }

    // b tagging cut
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    hCtrlNbjets[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(btagData.getBJetCount());
    if (tauCandidateData.selectedTauPassesNProngsAndRtauButNotIsolation()) {
      hABCDCtrlNbjets[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(btagData.getBJetCount());
    }
    if(!btagData.passedEvent()) return false;
    increment(fBTaggingCounter);
    // Apply scale factor as weight to event
    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
    increment(fBTaggingScaleFactorCounter);
    hSelectionFlow->Fill(kQCDOrderBTag);
    hLeg1AfterBTagging->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
    if (myPassedTauLegStatus) increment(fCoincidenceAfterBjetsCounter);
    hCtrlMETAfterBtagging[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
    hMtShapesAfterMetAndBTagging[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);

    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetData.getSelectedJets().begin(); iJet != jetData.getSelectedJets().end(); ++iJet) {
      if (deltaPhi < 90) {
        hJetEtaVsPhiAfterMETLegCollinear->Fill((*iJet)->eta(), (*iJet)->phi());
        if (deltaPhi < 30) hJetEtaVsPhiAfterMETLegCollinearTight->Fill((*iJet)->eta(), (*iJet)->phi());
      } else {
        hJetEtaVsPhiAfterMETLegBackToBack->Fill((*iJet)->eta(), (*iJet)->phi());
        if (deltaPhi > 150) hJetEtaVsPhiAfterMETLegBackToBackTight->Fill((*iJet)->eta(), (*iJet)->phi());
      }
    }

    if (deltaPhi < 90) {
      hTauEtaVsPhiAfterMETLegCollinear->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
      hTauEtaVsPhiAfterMETLegCollinearOpposite->Fill(-tauCandidateData.getSelectedTau()->eta(), myOppositePhi);
      if (deltaPhi < 30) {
        hTauEtaVsPhiAfterMETLegCollinearTight->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
      }
    } else {
      hTauEtaVsPhiAfterMETLegBackToBack->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
      hTauEtaVsPhiAfterMETLegBackToBackOpposite->Fill(-tauCandidateData.getSelectedTau()->eta(), myOppositePhi);
      if (deltaPhi > 150) {
        hTauEtaVsPhiAfterMETLegBackToBackTight->Fill(tauCandidateData.getSelectedTau()->eta(), tauCandidateData.getSelectedTau()->phi());
      }
    }

    // Delta phi(tau,MET) cut
    hCtrlDeltaPhiTauMET[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(deltaPhi);
    if (tauCandidateData.selectedTauPassesNProngsAndRtauButNotIsolation()) {
      hABCDCtrlDeltaPhiTauMET[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(deltaPhi);
    }
    if (deltaPhi > fDeltaPhiCutValue) return false;
    increment(fDeltaPhiTauMETCounter);
    hSelectionFlow->Fill(kQCDOrderDeltaPhiTauMET);
    hLeg1AfterDeltaPhiTauMET->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
    if (myPassedTauLegStatus) increment(fCoincidenceAfterDeltaPhiCounter);
    hCtrlMETAfterBtaggingAndDeltaPhi[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());

    // Max Delta phi(jet,MET) cut
    double myMaxDeltaPhiJetMET = 0.0;
    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetData.getSelectedJets().begin(); iJet != jetData.getSelectedJets().end(); ++iJet) {
      double jetDeltaPhi = DeltaPhi::reconstruct(**iJet, *(metData.getSelectedMET())) * 57.3;
      if (jetDeltaPhi > myMaxDeltaPhiJetMET)
        myMaxDeltaPhiJetMET = jetDeltaPhi;
    }
    hSelectionFlow->Fill(kQCDOrderMaxDeltaPhiJetMET);
    hCtrlMaxDeltaPhiJetMET[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(myMaxDeltaPhiJetMET);
    hLeg1AfterMaxDeltaPhiJetMET->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);

    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    bool myTopRecoWithWSelectionStatus = false;
    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauCandidateData.getSelectedTau(), metData.getSelectedMET());
    double myTopWithBSelectionTopMass = 0.0;
    if (BjetSelectionData.passedEvent() ) {
      TopWithBSelection::Data TopWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());
      TopWithWSelection::Data TopWithWSelectionData = fTopWithWSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());
      if (TopWithWSelectionData.passedEvent() ) {
        myTopRecoWithWSelectionStatus = true;
        myTopWithBSelectionTopMass = TopWithWSelectionData.getTopMass();
      }
    }
    // Select events depending on top resonctruction
    bool myPassedTopRecoStatus = false;
    double myTopMass = 0.0;
    if (fTopRecoName == "None") {
      myPassedTopRecoStatus = true;
    } else if (fTopRecoName == "std") {
      myPassedTopRecoStatus = TopSelectionData.passedEvent();
      myTopMass = TopSelectionData.getTopMass();
    } else if (fTopRecoName == "chi") {
      myPassedTopRecoStatus = TopChiSelectionData.passedEvent();
      myTopMass = TopChiSelectionData.getTopMass();
    } else if (fTopRecoName == "Wselection") {
      myPassedTopRecoStatus = myTopRecoWithWSelectionStatus;
      myTopMass = myTopWithBSelectionTopMass;
    }
    hCtrlTopMass[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(myTopMass);
    if (!myPassedTopRecoStatus)
      return false;
    increment(fTopSelectionCounter);
    hSelectionFlow->Fill(kQCDOrderTopSelection);
    hLeg1AfterTopSelection->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);

    // MET leg selection passed
    if (myPassedTauLegStatus) {
      increment(fCoincidenceAfterSelectionCounter);
      //std::cout << "first selected tau pt=" << tauCandidateData.getSelectedTau()->leadPFChargedHadrCand()->pt() << " trg SF=" << tauTriggerWeight.getEventWeight() << "\tnjets" << jetData.getHadronicJetCount() << std::endl;
    }

    hFeatureMinEtaOfSelectedJetToGapAfterMETLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getMinEtaOfSelectedJetToGap());
    hFeatureEtaSpreadOfSelectedJetsAfterMETLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getEtaSpreadOfSelectedJets());
    hFeatureAverageEtaOfSelectedJetsAfterMETLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getAverageEtaOfSelectedJets());
    hFeatureAverageSelectedJetsEtaDistanceToTauEtaAfterMETLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getAverageSelectedJetsEtaDistanceToTauEta());

    // Obtain transverseMass
    hMtShapesAfterFullMETLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
    // Obtain full mass
    FullHiggsMassCalculator::Data fullMassData =  fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauCandidateData, btagData, metData);
    hFullMassShapesAfterFullMETLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(fullMassData.getHiggsMass());


    // Uncertainties after standard selections // FIXME: is this needed?
    fSFUncertaintyAfterStandardSelections.setScaleFactorUncertainties(fEventWeight.getWeight(),
                                                                      fFakeTauIdentifier.isFakeTau(tauMatchData.getTauMatchType()),
                                                                      fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauCandidateData.getSelectedTau()->eta()),
                                                                      fFakeTauIdentifier.getFakeTauSystematics(tauMatchData.getTauMatchType(), tauCandidateData.getSelectedTau()->eta()),
                                                                      btagData.getScaleFactor(), btagData.getScaleFactorAbsoluteUncertainty());
    fSFUncertaintyAfterStandardSelections.setTauTriggerScaleFactorUncertainty(fEventWeight.getWeight(),
                                                                              tauTriggerWeight.getEventWeight(),
                                                                              tauTriggerWeight.getEventWeightAbsoluteUncertainty());

    if (tauCandidateData.selectedTauPassesNProngsAndRtauButNotIsolation()) {
      // MET leg point for ABCD
      hABCDAfterMETLeg->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
      hABCDMtShapesAfterMETLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
    }

//------ End of QCD measurement
    return true;
  }

  // Returns index to tau pT bin; 0 is underflow and size() is highest bin
  int QCDMeasurementFactorised::getTauPtBinIndex(double pt) {
    size_t mySize = fTauPtBinLowEdges.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (pt < fTauPtBinLowEdges[i])
        return static_cast<int>(i);
    }
    return static_cast<int>(mySize);
  }

  int QCDMeasurementFactorised::getTauEtaBinIndex(double eta) {
    size_t mySize = fTauEtaBinLowEdges.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (eta < fTauEtaBinLowEdges[i])
        return static_cast<int>(i);
    }
    return static_cast<int>(mySize);
  }

  int QCDMeasurementFactorised::getNVerticesBinIndex(int nvtx) {
    size_t mySize = fNVerticesBinLowEdges.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (nvtx < fNVerticesBinLowEdges[i])
        return static_cast<int>(i);
    }
    return static_cast<int>(mySize);
  }

  int QCDMeasurementFactorised::getMtBinIndex(double mt) {
    size_t mySize = fTransverseMassRange.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (mt < fTransverseMassRange[i])
        return static_cast<int>(i);
    }
    return static_cast<int>(mySize);
  }

  int QCDMeasurementFactorised::getFullMassBinIndex(double mass) {
    size_t mySize = fFullMassRange.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (mass < fFullMassRange[i])
        return static_cast<int>(i);
    }
    return static_cast<int>(mySize);
  }

  void QCDMeasurementFactorised::createShapeHistograms(edm::Service<TFileService>& fs, std::vector<WrappedTH1*>& container, std::string title, int nbins, double min, double max) {
    std::stringstream myLabel;
    int myTauPtBins = static_cast<int>(fTauPtBinLowEdges.size()) + 1;
    int myTauEtaBins = static_cast<int>(fTauEtaBinLowEdges.size()) + 1;
    int myNVerticesBins = static_cast<int>(fNVerticesBinLowEdges.size()) + 1;
    std::string myTitle = "shape_"+title;
    TFileDirectory myDir = fs->mkdir(myTitle.c_str());
    for (int i = 0; i < myTauPtBins; ++i) {
      for (int j = 0; j < myTauEtaBins; ++j) {
        for (int k = 0; k < myNVerticesBins; ++k) {
          myLabel.str("");
          myLabel << title << "_" << i << "_" << j << "_" << k;
          container.push_back(fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, myLabel.str().c_str(), myLabel.str().c_str(), nbins, min, max));
        }
      }
    }
  }

  int QCDMeasurementFactorised::getShapeBinIndex(int tauPtBin, int tauEtaBin, int nvtxBin) {
    int myTauEtaBins = static_cast<int>(fTauEtaBinLowEdges.size()) + 1;
    int myNVerticesBins = static_cast<int>(fNVerticesBinLowEdges.size()) + 1;
    //std::cout << " bin=" << tauPtBin << " taueta=" << tauEtaBin << " nvtx=" << nvtxBin << std::endl;
    //std::cout << "total index=" << nvtxBin + tauEtaBin*myNVerticesBins + tauPtBin*myNVerticesBins*myTauEtaBins << endl;
    return nvtxBin + tauEtaBin*myNVerticesBins + tauPtBin*myNVerticesBins*myTauEtaBins;
  }

  void QCDMeasurementFactorised::setAxisLabelsForTH3(WrappedTH3* h) {
    // Set axis titles and labels
    if (h->isActive()) {
      h->getHisto()->SetXTitle("#tau p_{T}, GeV/c");
      for (int i = 1; i <= h->getHisto()->GetNbinsX(); ++i) {
        std::stringstream s;
        if (i == 1) {
          if (fTauPtBinLowEdges.size() > 0)
            s << "<" << static_cast<int>(fTauPtBinLowEdges[0]);
          else
            s << "all";
          h->getHisto()->GetXaxis()->SetBinLabel(i, s.str().c_str());
        } else if (i ==  h->getHisto()->GetNbinsX()) {
          s << ">" << static_cast<int>(fTauPtBinLowEdges[fTauPtBinLowEdges.size()-1]);
          h->getHisto()->GetXaxis()->SetBinLabel(h->getHisto()->GetNbinsX(), s.str().c_str());
        } else {
          s << static_cast<int>(fTauPtBinLowEdges[i-2]) << "-" << static_cast<int>(fTauPtBinLowEdges[i-1]);
          h->getHisto()->GetXaxis()->SetBinLabel(i, s.str().c_str());
        }
      }
      h->getHisto()->SetYTitle("#tau #eta");
      for (int i = 1; i <= h->getHisto()->GetNbinsY(); ++i) {
        std::stringstream s;
        if (i == 1) {
          if (fTauEtaBinLowEdges.size() > 0)
            s << "<" << setprecision(2) << fTauEtaBinLowEdges[0];
          else
            s << "all";
          h->getHisto()->GetYaxis()->SetBinLabel(i, s.str().c_str());
        } else if (i == h->getHisto()->GetNbinsY()) {
          s << ">" << setprecision(2) << fTauEtaBinLowEdges[fTauEtaBinLowEdges.size()-1];
          h->getHisto()->GetYaxis()->SetBinLabel(h->getHisto()->GetNbinsY(), s.str().c_str());
        } else {
          s << setprecision(2) << fTauEtaBinLowEdges[i-2] << ".." << setprecision(2) << fTauEtaBinLowEdges[i-1];
          h->getHisto()->GetYaxis()->SetBinLabel(i, s.str().c_str());
        }
      }
      h->getHisto()->SetZTitle("N_{vertices}");
      for (int i = 1; i <= h->getHisto()->GetNbinsZ(); ++i) {
        std::stringstream s;
        if (i == 1) {
          if (fNVerticesBinLowEdges.size() > 0)
            s << "<" << static_cast<int>(fNVerticesBinLowEdges[0]);
          else
            s << "all";
          h->getHisto()->GetZaxis()->SetBinLabel(i, s.str().c_str());
        } else if (i == h->getHisto()->GetNbinsZ()) {
          s << ">" << static_cast<int>(fNVerticesBinLowEdges[fNVerticesBinLowEdges.size()-1]);
          h->getHisto()->GetZaxis()->SetBinLabel(h->getHisto()->GetNbinsZ(), s.str().c_str());
        } else {
          s << static_cast<int>(fNVerticesBinLowEdges[i-2]) << ".." << static_cast<int>(fNVerticesBinLowEdges[i-1]);
          h->getHisto()->GetZaxis()->SetBinLabel(i, s.str().c_str());
        }
      }
    }
  }
}

