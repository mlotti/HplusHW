#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementFactorised.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ConfigInfo.h"

#include "TNamed.h"
#include <iomanip>
#include <sstream>

namespace HPlus {
  QCDMeasurementFactorised::QCDMeasurementFactorised(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper):
    fEventWeight(eventWeight),
    fHistoWrapper(histoWrapper),
    // Input parameters
    fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
    fApplyNprongsCutForTauCandidate(iConfig.getUntrackedParameter<bool>("applyNprongsCutForTauCandidate")),
    fApplyRtauCutForTauCandidate(iConfig.getUntrackedParameter<bool>("applyRtauCutForTauCandidate")),
    // Counters - do not change order
    fAllCounter(eventCounter.addCounter("Offline selection begins")),
    fTopPtWeightCounter(eventCounter.addCounter("Top pt reweight")),
    fWJetsWeightCounter(eventCounter.addCounter("WJets inc+exl weight")),
    fMETFiltersCounter(eventCounter.addCounter("MET filters")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET")),
    fPrimaryVertexCounter(eventCounter.addCounter("PrimaryVertex")),
    fTausExistAfterCandidateSelectionCounter(eventCounter.addCounter("TauCandidate selection")),
    fTausExistAfterNprongsCutCounter(eventCounter.addCounter("TauCand+Nprong")),
    fTausExistAfterRtauCutCounter(eventCounter.addCounter("TauCand+Rtau")),
    fMultipleTausAfterTauSelection(eventCounter.addCounter("Multiple tau candidates exist")),
    fTausAfterScaleFactorsCounter(eventCounter.addCounter("Tau after scale factors")),
    fVetoTauCounter(eventCounter.addCounter("-> Killed by VetoTauSelection")),
    fElectronVetoCounter(eventCounter.addCounter("ElectronSelection")),
    fMuonVetoCounter(eventCounter.addCounter("MuonSelection")),
    fNJetsCounter(eventCounter.addCounter("JetSelection")),
    fPreMETCutCounter(eventCounter.addCounter("pre-MET cut")),
    fMETTriggerScaleFactorCounter(eventCounter.addCounter("Trg MET scale factor")),
    fQCDTailKillerCollinearCounter(eventCounter.addCounter("After collinear cuts")),
    fAfterStandardSelectionsCounter(eventCounter.addCounter("After std. selections")),
    fMetCounter(eventCounter.addCounter("MET cut")),
    fBTaggingCounter(eventCounter.addCounter("btagging")),
    fBTaggingScaleFactorCounter(eventCounter.addCounter("btagging with SF")),
    fQCDTailKillerBackToBackCounter(eventCounter.addCounter("After back-to-back cuts")),
    fTopSelectionCounter(eventCounter.addCounter("After top selection cuts")),
    fAfterLeg1Counter(eventCounter.addCounter("After leg1 selections")),
    fAfterLeg2Counter(eventCounter.addCounter("After leg2 selections")),
    fAfterLeg1AndLeg2Counter(eventCounter.addCounter("After leg1 and leg2 selections")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    fVetoTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("vetoTauSelection"),
                      iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"),
                      eventCounter, fHistoWrapper),
    fElectronSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("ElectronSelection"), fPrimaryVertexSelection.getSelectedSrc(), eventCounter, fHistoWrapper),
    fMuonSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MuonSelection"), eventCounter, fHistoWrapper),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, fHistoWrapper),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, fHistoWrapper, "MET", fTauSelection.getIsolationDiscriminator()),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, fHistoWrapper),
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, fHistoWrapper),
    fTopSelectionManager(iConfig, eventCounter, fHistoWrapper, iConfig.getUntrackedParameter<std::string>("topReconstruction")),
    fFullHiggsMassCalculator(iConfig.getUntrackedParameter<edm::ParameterSet>("invMassReco"), eventCounter, fHistoWrapper),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, fHistoWrapper),
    //fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, fHistoWrapper),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, fHistoWrapper),
    fTauTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("tauTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fMETTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("metTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fPrescaleWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("prescaleWeightReader"), fHistoWrapper, "PrescaleWeight"),
    fPileupWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("pileupWeightReader"), fHistoWrapper, "PileupWeight"),
    fWJetsWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("wjetsWeightReader"), fHistoWrapper, "WJetsWeight"),
    fTopPtWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("topPtWeightReader"), fHistoWrapper, "TopPtWeight"),
    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), fHistoWrapper, "TauCandidates"),
    fMETFilters(iConfig.getUntrackedParameter<edm::ParameterSet>("metFilters"), eventCounter),
    fQCDTailKiller(iConfig.getUntrackedParameter<edm::ParameterSet>("QCDTailKiller"), eventCounter, fHistoWrapper),
    fTree(iConfig.getUntrackedParameter<edm::ParameterSet>("Tree"), fBTagging.getDiscriminator()),
    fCommonPlots(iConfig.getUntrackedParameter<edm::ParameterSet>("commonPlotsSettings"), eventCounter, fHistoWrapper, CommonPlots::kQCDFactorised),
    fNormalizationSystematicsSignalRegion(iConfig.getUntrackedParameter<edm::ParameterSet>("commonPlotsSettings"), eventCounter, fHistoWrapper, CommonPlots::kQCDNormalizationSystematicsSignalRegion),
    fNormalizationSystematicsControlRegion(iConfig.getUntrackedParameter<edm::ParameterSet>("commonPlotsSettings"), eventCounter, fHistoWrapper, CommonPlots::kQCDNormalizationSystematicsControlRegion),
    fCommonPlotsAfterVertexSelection(fCommonPlots.createCommonPlotsFilledAtEveryStep("VertexSelection",false,"Vtx")),
    fCommonPlotsAfterTauSelection(fCommonPlots.createCommonPlotsFilledAtEveryStep("TauSelection",false,"TauID")),
    fCommonPlotsAfterTauWeight(fCommonPlots.createCommonPlotsFilledAtEveryStep("TauWeight",true,"Tau")),
    fCommonPlotsAfterElectronVeto(fCommonPlots.createCommonPlotsFilledAtEveryStep("ElectronVeto",true,"e veto")),
    fCommonPlotsAfterMuonVeto(fCommonPlots.createCommonPlotsFilledAtEveryStep("MuonVeto",true,"#mu veto")),
    fCommonPlotsAfterJetSelection(fCommonPlots.createCommonPlotsFilledAtEveryStep("JetSelection",true,"#geq3j")),
    fCommonPlotsAfterMETScaleFactor(fCommonPlots.createCommonPlotsFilledAtEveryStep("MET scale factor",true,"E_{T}^{miss} scale factor")),
    fCommonPlotsAfterStandardSelections(fCommonPlots.createCommonPlotsFilledAtEveryStep("Std. selections",false,"Std. selections")),
    fCommonPlotsAfterMET(fCommonPlots.createCommonPlotsFilledAtEveryStep("Std. selections+MET",false,"Std. selections+MET")),
    fCommonPlotsAfterMETAndBtag(fCommonPlots.createCommonPlotsFilledAtEveryStep("Std. selections+MET+btag",false,"Std. selections+MET+btag")),
    fCommonPlotsAfterMETAndBtagWithSF(fCommonPlots.createCommonPlotsFilledAtEveryStep("Std. selections+MET+btag with SF",false,"Std. selections+MET+btag with SF")),
    fCommonPlotsAfterMETAndBtagWithSFAndDeltaPhi(fCommonPlots.createCommonPlotsFilledAtEveryStep("Std. selections+MET+btag+deltaphi with SF",false,"Std. selections+MET+btag+deltaphi with SF")),
    fCommonPlotsAfterLeg1(fCommonPlots.createCommonPlotsFilledAtEveryStep("Leg1 (MET+btag+...)",false,"Leg1 (MET+btag+...)")),
    fCommonPlotsAfterLeg2(fCommonPlots.createCommonPlotsFilledAtEveryStep("Leg2 (tau isol.)",false,"Leg2 (tau isol.)"))
  {
    // Options
    std::string myAnalysisMode = iConfig.getUntrackedParameter<std::string>("analysisMode");
    if (myAnalysisMode == "traditional")
      fMethodType = QCDMeasurementFactorised::kQCDFactorisedTraditional;
    else if (myAnalysisMode == "ABCD")
      fMethodType = QCDMeasurementFactorised::kQCDFactorisedABCD;
    else
      throw cms::Exception("ConfigError") << "QCDfactorised parameter analysisMode unknown (valid options: 'traditional', 'ABCD')!";

    // Book histograms
    edm::Service<TFileService> fs;
    ConfigInfo::writeConfigInfo(iConfig, *fs);

    hVerticesBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesBeforeWeight", "Number of vertices without weighting;Vertices;N_{events} / 1 Vertex", 50, 0, 50);
    hVerticesAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesAfterWeight", "Number of vertices with weighting; Vertices;N_{events} / 1 Vertex", 50, 0, 50);

    std::string myDirTitle = "QCDfactorised";
    TFileDirectory myDir = fs->mkdir(myDirTitle.c_str());

    SplittedHistogramHandler& myHandler = fCommonPlots.getSplittedHistogramHandler();

    // Shape histograms (some needed for closure test)
    const int myMtBins = fCommonPlots.getMtBinSettings().bins();
    const double myMtMin = fCommonPlots.getMtBinSettings().min();
    const double myMtMax = fCommonPlots.getMtBinSettings().max();
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myDir, hMtShapesAfterStandardSelections, "MtAfterStandardSelections", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myDir, hMtShapesAfterStandardSelectionsAndIsolatedTau, "MtAfterStandardSelectionsAndIsolatedTau", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myDir, hMtShapesAfterStandardSelectionsAndNonIsolatedTau, "MtAfterStandardSelectionsAndNonIsolatedTau", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myDir, hMtShapesAfterLeg1, "MtAfterLeg1", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myDir, hMtShapesAfterLeg1WithoutBtag, "MtAfterLeg1WithoutBtag", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myDir, hMtShapesAfterLeg2, "MtAfterLeg2", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myDir, hMtShapesAfterLeg1AndLeg2, "MtAfterLeg1AndLeg2", "Transverse mass, GeV/c^{2}", myMtBins, myMtMin, myMtMax);
    const int myMassBins = fCommonPlots.getInvmassBinSettings().bins();
    const double myMassMin = fCommonPlots.getInvmassBinSettings().min();
    const double myMassMax = fCommonPlots.getInvmassBinSettings().max();
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myDir, hInvariantMassShapesAfterStandardSelections, "MassAfterStandardSelections", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myDir, hInvariantMassShapesAfterStandardSelectionsAndIsolatedTau, "InvariantMassAfterStandardSelectionsAndIsolatedTau", "Transverse mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myDir, hInvariantMassShapesAfterStandardSelectionsAndNonIsolatedTau, "InvariantMassAfterStandardSelectionsAndNonIsolatedTau", "Transverse mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myDir, hInvariantMassShapesAfterLeg1, "MassAfterLeg1", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myDir, hInvariantMassShapesAfterLeg1WithoutBtag, "MassAfterLeg1WithoutBtag", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    myHandler.createShapeHistogram(HistoWrapper::kSystematics, myDir, hInvariantMassShapesAfterLeg2, "MassAfterLeg2", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myDir, hInvariantMassShapesAfterLeg1AndLeg2, "MassAfterLeg1AndLeg2", "Invariant mass, GeV/c^{2}", myMassBins, myMassMin, myMassMax);
    // MET shapes (just for controlling, closure test comes from mT shapes)
    const int myMetBins = fCommonPlots.getMetBinSettings().bins();
    const double myMetMin = fCommonPlots.getMetBinSettings().min();
    const double myMetMax = fCommonPlots.getMetBinSettings().max();
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myDir, hMETAfterStandardSelections, "METAfterStandardSelections", "E_{T}^{miss}, GeV", myMetBins, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myDir, hMETAfterLeg1, "METAfterLeg1", "E_{T}^{miss}, GeV", myMetBins, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myDir, hMETAfterLeg2, "METAfterLeg2", "E_{T}^{miss}, GeV", myMetBins, myMetMin, myMetMax);
    myHandler.createShapeHistogram(HistoWrapper::kInformative, myDir, hMETAfterBJets, "METAfterBJets", "E_{T}^{miss}, GeV", myMetBins, myMetMin, myMetMax);
    // Shapes for closure test systematics for data-driven control plots are done via the extra Common plots objects
    fNormalizationSystematicsSignalRegion.disableCommonPlotsFilledAtEveryStep();
    fNormalizationSystematicsControlRegion.disableCommonPlotsFilledAtEveryStep();

    // Tree
    fTree.enableNonIsoLeptons(true);
    fTree.init(*fs);

    fTailTestAfterStdSel = new TailTest("AfterStdSel", fs, fHistoWrapper);
    fTailTestAfterTauLeg = new TailTest("AfterTauLeg", fs, fHistoWrapper);
  }

  QCDMeasurementFactorised::~QCDMeasurementFactorised() {}

  bool QCDMeasurementFactorised::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
//------ Read the prescale for the event and set the event weight as the prescale
    fEventWeight.beginEvent();
    const double prescaleWeight = fPrescaleWeightReader.getWeight(iEvent, iSetup);
    fEventWeight.multiplyWeight(prescaleWeight);
    fTree.setPrescaleWeight(prescaleWeight);


//------ Vertex weight
    double myWeightBeforePileupReweighting = fEventWeight.getWeight();
    if(!iEvent.isRealData()) {
      const double myPileupWeight = fPileupWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(myPileupWeight);
      fTree.setPileupWeight(myPileupWeight);
    }
    increment(fAllCounter);

//------ Top pT reweighting
    if(!iEvent.isRealData()) {
      const double topPtWeight = fTopPtWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(topPtWeight);
      fTree.setTopPtWeight(topPtWeight);
    }
    increment(fTopPtWeightCounter);

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
    const TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);
    if(triggerData.hasTriggerPath()) // protection if TriggerSelection is disabled
      fTree.setHltTaus(triggerData.getTriggerTaus());

//------ GenParticle analysis (must be done here when we effectively trigger all MC)
    if (!iEvent.isRealData()) {
      GenParticleAnalysis::Data genData = fGenparticleAnalysis.analyze(iEvent, iSetup);
      if(genData.isValid())
        fTree.setGenMET(genData.getGenMET());
    }

//------ Primary vertex selection
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if (!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    size_t nVertices = pvData.getNumberOfAllVertices();
    hVerticesBeforeWeight->Fill(nVertices, myWeightBeforePileupReweighting);
    hVerticesAfterWeight->Fill(nVertices);
    fTree.setNvertices(nVertices);
    // Setup common plots

    fCommonPlots.initialize(iEvent, iSetup, pvData, fTauSelection, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETTriggerEfficiencyScaleFactor, fMETSelection, fBTagging, fQCDTailKiller, fBjetSelection, fTopSelectionManager, fEvtTopology, fFullHiggsMassCalculator);

    fCommonPlotsAfterVertexSelection->fill();
    fCommonPlots.fillControlPlotsAfterVertexSelection(iEvent, pvData);

//------ Tau candidate selection
    // Do tau candidate selection
    TauSelection::Data tauCandidateDataTmp = fTauSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
    if (!tauCandidateDataTmp.passedEvent()) return false;
    increment(fTausExistAfterCandidateSelectionCounter);
    edm::PtrVector<pat::Tau> mySelectedTauList = tauCandidateDataTmp.getSelectedTausBeforeIsolation();
    // Apply nprongs if requested
    if (fApplyNprongsCutForTauCandidate) {
      edm::PtrVector<pat::Tau> myTmpVector;
      for (edm::PtrVector<pat::Tau>::iterator iTau = mySelectedTauList.begin(); iTau != mySelectedTauList.end(); ++iTau) {
        if (fTauSelection.getPassesNProngsStatusOfTauObject(*iTau))
          myTmpVector.push_back(*iTau);
      }
      mySelectedTauList = myTmpVector;
      myTmpVector.clear();
      if (!mySelectedTauList.size()) return false;
    }
    increment(fTausExistAfterNprongsCutCounter);
    // Apply Rtau cut if requested
    if (fApplyRtauCutForTauCandidate) {
      edm::PtrVector<pat::Tau> myTmpVector;
      for (edm::PtrVector<pat::Tau>::iterator iTau = mySelectedTauList.begin(); iTau != mySelectedTauList.end(); ++iTau) {
        if (fTauSelection.getPassesRtauStatusOfTauObject(*iTau))
          myTmpVector.push_back(*iTau);
      }
      mySelectedTauList = myTmpVector;
      myTmpVector.clear();
      if (!mySelectedTauList.size()) return false;
    }
    increment(fTausExistAfterRtauCutCounter);
    if (mySelectedTauList.size() > 1)
      increment(fMultipleTausAfterTauSelection);
    // Dirty hack to make code crash if tauCandidateData.getSelectedTau() is called
    const_cast<TauSelection::Data*>(&tauCandidateDataTmp)->invalidate();
    // Important NOTE: Beyond this line, use only 'mySelectedTau' as the tau object
    edm::Ptr<pat::Tau> mySelectedTau = fTauSelection.selectMostLikelyTau(mySelectedTauList, pvData.getSelectedVertex()->z());
    if (fMethodType == QCDMeasurementFactorised::kQCDFactorisedABCD) {
      // Check how many passed taus pass or fail isolation - one needs to choose tau depending on the isolation
      // because it will affect jet selection, MET value, delta phi, ...
      edm::PtrVector<pat::Tau> myPassedIsolationList;
      edm::PtrVector<pat::Tau> myFailedIsolationList;
      for (edm::PtrVector<pat::Tau>::iterator iTau = mySelectedTauList.begin(); iTau != mySelectedTauList.end(); ++iTau) {
        if (fTauSelection.getPassesIsolationStatusOfTauObject(*iTau)) {
          myPassedIsolationList.push_back(*iTau);
        } else {
          myFailedIsolationList.push_back(*iTau);
        }
      }
      // See if any tau passes isolation
      if (myPassedIsolationList.size() > 0) {
        mySelectedTau = fTauSelection.selectMostLikelyTau(myPassedIsolationList, pvData.getSelectedVertex()->z());
      } else {
        mySelectedTau = fTauSelection.selectMostLikelyTau(myFailedIsolationList, pvData.getSelectedVertex()->z());
      }
    }
    TauSelection::Data tauCandidateData = fTauSelection.setSelectedTau(mySelectedTau, true);
    // Obtain MC matching - for EWK without genuine taus
    FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, *(mySelectedTau));
    // note: do not require here that only one tau has been found (mySelectedTau is the selected tau in the event)
    // Now re-initialize common plots with the correct selection for tau (affects jet selection, b-tagging, type I MET, delta phi cuts)
    fCommonPlots.initialize(iEvent, iSetup, pvData, tauCandidateData, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETTriggerEfficiencyScaleFactor, fMETSelection, fBTagging, fQCDTailKiller, fBjetSelection, fTopSelectionManager, fEvtTopology, fFullHiggsMassCalculator);
    fCommonPlotsAfterTauSelection->fill();
    fCommonPlots.fillControlPlotsAfterTauSelection(iEvent, iSetup, tauCandidateData, tauMatchData, fJetSelection, fMETSelection, fBTagging, fQCDTailKiller);
    // Initialize also normalization systematics plotting
    fNormalizationSystematicsSignalRegion.initialize(iEvent, iSetup, pvData, tauCandidateData, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETTriggerEfficiencyScaleFactor, fMETSelection, fBTagging, fQCDTailKiller, fBjetSelection, fTopSelectionManager, fEvtTopology, fFullHiggsMassCalculator);
    fNormalizationSystematicsControlRegion.initialize(iEvent, iSetup, pvData, tauCandidateData, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETTriggerEfficiencyScaleFactor, fMETSelection, fBTagging, fQCDTailKiller, fBjetSelection, fTopSelectionManager, fEvtTopology, fFullHiggsMassCalculator);
    fNormalizationSystematicsSignalRegion.setSplittingOfPhaseSpaceInfoAfterTauSelection(iEvent, iSetup, tauCandidateData, fMETSelection);
    fNormalizationSystematicsControlRegion.setSplittingOfPhaseSpaceInfoAfterTauSelection(iEvent, iSetup, tauCandidateData, fMETSelection);

//------ Scale factors for tau fakes and for tau trigger
    // Apply scale factor for fake tau
    double myFakeTauScaleFactor = 1.0;
    if (!iEvent.isRealData()) {
      myFakeTauScaleFactor = fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), mySelectedTau->eta());
      fEventWeight.multiplyWeight(myFakeTauScaleFactor);
    }
    fTree.setTauFakeWeight(myFakeTauScaleFactor, fFakeTauIdentifier.getFakeTauSystematics(tauMatchData.getTauMatchType(), mySelectedTau->eta()));
    // Apply scale factor tau part of trigger
    const TauTriggerEfficiencyScaleFactor::Data tauTriggerWeightData = fTauTriggerEfficiencyScaleFactor.applyEventWeight(*(mySelectedTau), iEvent.isRealData(), fEventWeight);
    fTree.setTauTriggerWeight(tauTriggerWeightData.getEventWeight(), tauTriggerWeightData.getEventWeightAbsoluteUncertainty());
    increment(fTausAfterScaleFactorsCounter);
    fCommonPlotsAfterTauWeight->fill();
    fCommonPlots.fillControlPlotsAfterTauTriggerScaleFactor(iEvent);


//------ Veto against second tau in event
    const VetoTauSelection::Data vetoTauData = fVetoTauSelection.analyze(iEvent, iSetup, mySelectedTau, pvData.getSelectedVertex()->z());
    fCommonPlots.fillControlPlotsAtTauVetoSelection(iEvent, iSetup, vetoTauData);
    //    if (vetoTauData.passedEvent()) return false;
    if (!vetoTauData.passedEvent()) increment(fVetoTauCounter);
    // Note: no return statement should be added here


//------ Global electron veto
    const ElectronSelection::Data electronData = fElectronSelection.analyze(iEvent, iSetup);
    fCommonPlots.fillControlPlotsAtElectronSelection(iEvent, electronData);
    if (!electronData.passedEvent()) return false;
    increment(fElectronVetoCounter);
    fCommonPlotsAfterElectronVeto->fill();
    /*NonIsolatedElectronVeto::Data nonIsolatedElectronVetoData = fNonIsolatedElectronVeto.analyze(iEvent, iSetup);
    if (!nonIsolatedElectronVetoData.passedEvent())  return false;
    increment(fNonIsolatedElectronVetoCounter);*/
    // Control plot


//------ Global muon veto
    const MuonSelection::Data muonData = fMuonSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    fCommonPlots.fillControlPlotsAtMuonSelection(iEvent, muonData);
    if (!muonData.passedEvent()) return false;
    increment(fMuonVetoCounter);
    fCommonPlotsAfterMuonVeto->fill();
    /*NonIsolatedMuonVeto::Data nonIsolatedMuonVetoData = fNonIsolatedMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!nonIsolatedMuonVetoData.passedEvent()) return; 
    increment(fNonIsolatedMuonVetoCounter);*/
    // Control plot


//------ Jet selection
    const JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, mySelectedTau, nVertices);
    if (!jetData.passedEvent()) return false;
    fCommonPlots.fillControlPlotsAtJetSelection(iEvent, jetData);
    increment(fNJetsCounter);
    fCommonPlotsAfterJetSelection->fill();


//------ Scale factor for MET trigger
    const METSelection::Data metData = fMETSelection.analyzeWithPossiblyIsolatedTaus(iEvent, iSetup, nVertices, mySelectedTau, jetData.getAllJets());
    if(!metData.passedPreMetCut()) return false;
    increment(fPreMETCutCounter);
    if(iEvent.isRealData())
      fMETTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
    METTriggerEfficiencyScaleFactor::Data metTriggerWeight = fMETTriggerEfficiencyScaleFactor.applyEventWeight(*(metData.getSelectedMET()), iEvent.isRealData(), fEventWeight);
    fTree.setMETTriggerWeight(metTriggerWeight.getEventWeight(), metTriggerWeight.getEventWeightAbsoluteUncertainty());
    increment(fMETTriggerScaleFactorCounter);
    fCommonPlotsAfterMETScaleFactor->fill();
    fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(iEvent);

//------ Improved delta phi cut, a.k.a. QCD tail killer - collinear part
    const QCDTailKiller::Data qcdTailKillerDataCollinear = fQCDTailKiller.silentAnalyze(iEvent, iSetup, tauCandidateData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    fCommonPlots.fillControlPlotsAtCollinearDeltaPhiCuts(iEvent, qcdTailKillerDataCollinear);
    if (!qcdTailKillerDataCollinear.passedCollinearCuts()) return false;
    increment(fQCDTailKillerCollinearCounter);


//------ Standard selections are done, fill tree and quit if user asked for it
    if (fTree.isActive()) {
      doTreeFilling(iEvent, iSetup, pvData, mySelectedTau, electronData, muonData, jetData, metData);
      //return true;
    }


//----- Standard selections are done, now do analysis variations
    if (fMethodType == QCDMeasurementFactorised::kQCDFactorisedTraditional) {
      doTraditionalSelection(iEvent, iSetup, tauCandidateData, jetData, metData);
    } else if (fMethodType == QCDMeasurementFactorised::kQCDFactorisedABCD) {
      doABCDSelection(iEvent, iSetup, tauCandidateData, jetData, metData);
    }

    // Additional tests
    fTailTestAfterStdSel->Fill(iEvent, mySelectedTau, fTauSelection, qcdTailKillerDataCollinear, jetData, electronData, muonData, metData, iEvent.isRealData(), tauMatchData.isFakeTau());
    bool myLeg2PassedStatus = fTauSelection.getPassesIsolationStatusOfTauObject(mySelectedTau) &&
      fTauSelection.getPassesNProngsStatusOfTauObject(mySelectedTau) &&
      fTauSelection.getPassesRtauStatusOfTauObject(mySelectedTau);
    if (myLeg2PassedStatus) {
      fTailTestAfterTauLeg->Fill(iEvent, mySelectedTau, fTauSelection, qcdTailKillerDataCollinear, jetData, electronData, muonData, metData, iEvent.isRealData(), tauMatchData.isFakeTau());
    }

    //------ End of QCD measurement
    return true;
  }

  void QCDMeasurementFactorised::doTraditionalSelection(edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const JetSelection::Data& jetData, const METSelection::Data& metData) {
    bool myLeg2PassedStatus = fTauSelection.getPassesIsolationStatusOfTauObject(tauData.getSelectedTau()) &&
      fTauSelection.getPassesNProngsStatusOfTauObject(tauData.getSelectedTau()) &&
      fTauSelection.getPassesRtauStatusOfTauObject(tauData.getSelectedTau());
    double myMetValue = metData.getSelectedMET()->et();
    const double myTransverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()));
    const BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());
    double myFullMass = -1.0;
    FullHiggsMassCalculator::Data myFullHiggsMassData;
    if (btagDataTmp.passedEvent()) {
      FullHiggsMassCalculator::Data myFullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData.getSelectedTau(), btagDataTmp, metData);
      if (myFullHiggsMassData.passedEvent()) {
        myFullMass = myFullHiggsMassData.getHiggsMass();
      }
    }
    SplittedHistogramHandler& myHandler = fCommonPlots.getSplittedHistogramHandler();

    // Standard selections have been done, fill histograms
    increment(fAfterStandardSelectionsCounter);
    fCommonPlotsAfterStandardSelections->fill();
    myHandler.fillShapeHistogram(hMETAfterStandardSelections, myMetValue);
    myHandler.fillShapeHistogram(hMtShapesAfterStandardSelections, myTransverseMass);
    if (myFullMass > 0) myHandler.fillShapeHistogram(hInvariantMassShapesAfterStandardSelections, myFullMass);
    fNormalizationSystematicsControlRegion.fillAllControlPlots(iEvent, myTransverseMass);

    // Leg 2 (tau ID)
    if (myLeg2PassedStatus) {
      increment(fAfterLeg2Counter);
      fCommonPlotsAfterLeg2->fill();
      myHandler.fillShapeHistogram(hMETAfterLeg2, myMetValue);
      myHandler.fillShapeHistogram(hMtShapesAfterLeg2, myTransverseMass);
      myHandler.fillShapeHistogram(hMtShapesAfterStandardSelectionsAndIsolatedTau, myTransverseMass);
      fNormalizationSystematicsSignalRegion.fillAllControlPlots(iEvent, myTransverseMass);
      if (myFullMass > 0.) {
        myHandler.fillShapeHistogram(hInvariantMassShapesAfterLeg2, myFullMass);
        myHandler.fillShapeHistogram(hInvariantMassShapesAfterStandardSelectionsAndIsolatedTau, myFullMass);
      }
    } else {
      myHandler.fillShapeHistogram(hMtShapesAfterStandardSelectionsAndNonIsolatedTau, myTransverseMass);
      if (myFullMass > 0.) myHandler.fillShapeHistogram(hInvariantMassShapesAfterStandardSelectionsAndNonIsolatedTau, myFullMass);
    }

    // Leg 1 / MET cut
    fCommonPlots.fillControlPlotsAtMETSelection(iEvent, metData);
    if (!metData.passedEvent()) return;
    increment(fMetCounter);
    fCommonPlotsAfterMET->fill();

    double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();

    const QCDTailKiller::Data qcdTailKillerDataTmp = fQCDTailKiller.silentAnalyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    if (qcdTailKillerDataTmp.passedBackToBackCuts()) {
      myHandler.fillShapeHistogram(hMtShapesAfterLeg1WithoutBtag, myTransverseMass, myWeightWithBtagSF);
      if (myFullMass > 0.) myHandler.fillShapeHistogram(hInvariantMassShapesAfterLeg1WithoutBtag, myFullMass, myWeightWithBtagSF);
    }

    // Leg 1 / b tagging
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
    if (btagData.passedEvent()) {
      increment(fBTaggingCounter);
      fCommonPlotsAfterMETAndBtag->fill();
    }
    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
    // Beyond this point, the b tag scale factor has already been applied
    fCommonPlots.fillControlPlotsAtBtagging(iEvent, btagData);
    if (!btagData.passedEvent()) return;
    increment(fBTaggingScaleFactorCounter);
    fCommonPlotsAfterMETAndBtagWithSF->fill();
    myHandler.fillShapeHistogram(hMETAfterBJets, myMetValue);

    //------ Improved delta phi cut, a.k.a. QCD tail killer, back-to-back part
    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    fCommonPlots.fillControlPlotsAtBackToBackDeltaPhiCuts(iEvent, qcdTailKillerData);
    if (!qcdTailKillerData.passedBackToBackCuts()) return;
    increment(fQCDTailKillerBackToBackCounter);

    //------ Top selection
    BjetSelection::Data bjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());
    TopSelectionManager::Data topSelectionData = fTopSelectionManager.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), bjetSelectionData.getBjetTopSide(), bjetSelectionData.passedEvent());
    fCommonPlots.fillControlPlotsAtTopSelection(iEvent, topSelectionData);
    if (!(topSelectionData.passedEvent())) return;
    increment(fTopSelectionCounter);

    // Leg 1 passed
    increment(fAfterLeg1Counter);
    myHandler.fillShapeHistogram(hMETAfterLeg1, myMetValue);
    myHandler.fillShapeHistogram(hMtShapesAfterLeg1, myTransverseMass);
    if (myFullMass > 0.) myHandler.fillShapeHistogram(hInvariantMassShapesAfterLeg1, myFullMass);
    fCommonPlotsAfterLeg1->fill();
    fCommonPlots.fillControlPlotsAfterAllSelections(iEvent, myTransverseMass);
    if (myFullMass > 0.) fCommonPlots.fillControlPlotsAfterAllSelectionsWithFullMass(iEvent, myFullHiggsMassData);

    // Leg 1 and leg 2 passed (for control only)
    if (myLeg2PassedStatus) {
      increment(fAfterLeg1AndLeg2Counter);
      myHandler.fillShapeHistogram(hMtShapesAfterLeg1AndLeg2, myTransverseMass);
      if (myFullMass > 0.) myHandler.fillShapeHistogram(hInvariantMassShapesAfterLeg1AndLeg2, myFullMass);
    }
  }

  void QCDMeasurementFactorised::doABCDSelection(edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const JetSelection::Data& jetData, const METSelection::Data& metData) {
    // ABCD method with MET and tau isolation as variables
    // Obtain booleans
    bool myLeg2PassedStatus = fTauSelection.getPassesIsolationStatusOfTauObject(tauData.getSelectedTau()) &&
      fTauSelection.getPassesNProngsStatusOfTauObject(tauData.getSelectedTau()) &&
      fTauSelection.getPassesRtauStatusOfTauObject(tauData.getSelectedTau());
    double myMetValue = metData.getSelectedMET()->et();
    const double myTransverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()));
    const BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());
    const QCDTailKiller::Data qcdTailKillerDataTmp = fQCDTailKiller.silentAnalyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    BjetSelection::Data bjetSelectionData = fBjetSelection.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets(), btagDataTmp.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());
    TopSelectionManager::Data topSelectionData = fTopSelectionManager.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets(), btagDataTmp.getSelectedJets(), bjetSelectionData.getBjetTopSide(), bjetSelectionData.passedEvent());

    // Leg 1 passed
    double myFullMass = -1.0;
    FullHiggsMassCalculator::Data myFullHiggsMassData;
    if (btagDataTmp.passedEvent()) {
      FullHiggsMassCalculator::Data myFullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData.getSelectedTau(), btagDataTmp, metData);
      if (myFullHiggsMassData.passedEvent()) {
        myFullMass = myFullHiggsMassData.getHiggsMass();
      }
    }
    SplittedHistogramHandler& myHandler = fCommonPlots.getSplittedHistogramHandler();
    bool myLeg1PassedStatus = metData.passedEvent() && btagDataTmp.passedEvent() && qcdTailKillerDataTmp.passedEvent() && topSelectionData.passedEvent();

    // Fill inclusive histograms for syst. uncertainty
    if (myLeg2PassedStatus) {
      myHandler.fillShapeHistogram(hMtShapesAfterStandardSelectionsAndIsolatedTau, myTransverseMass);
      if (myFullMass > 0.) myHandler.fillShapeHistogram(hInvariantMassShapesAfterStandardSelectionsAndIsolatedTau, myFullMass);
    } else {
      myHandler.fillShapeHistogram(hMtShapesAfterStandardSelectionsAndNonIsolatedTau, myTransverseMass);
      if (myFullMass > 0.) myHandler.fillShapeHistogram(hInvariantMassShapesAfterStandardSelectionsAndNonIsolatedTau, myFullMass);
    }

    // Standard selections have been done, fill histograms
    if (!myLeg1PassedStatus && !myLeg2PassedStatus) { // Box A
      increment(fAfterStandardSelectionsCounter);
      fCommonPlotsAfterStandardSelections->fill();
      myHandler.fillShapeHistogram(hMETAfterStandardSelections, myMetValue);
      myHandler.fillShapeHistogram(hMtShapesAfterStandardSelections, myTransverseMass);
      if (myFullMass > 0) myHandler.fillShapeHistogram(hInvariantMassShapesAfterStandardSelections, myFullMass);
      fNormalizationSystematicsControlRegion.fillAllControlPlots(iEvent, myTransverseMass);
    }

    // Leg 2 (tau ID)
    if (!myLeg1PassedStatus && myLeg2PassedStatus) { // Box C
      increment(fAfterLeg2Counter);
      fCommonPlotsAfterLeg2->fill();
      myHandler.fillShapeHistogram(hMETAfterLeg2, myMetValue);
      myHandler.fillShapeHistogram(hMtShapesAfterLeg2, myTransverseMass);
      fNormalizationSystematicsSignalRegion.fillAllControlPlots(iEvent, myTransverseMass);
      if (myFullMass > 0.) myHandler.fillShapeHistogram(hInvariantMassShapesAfterLeg2, myFullMass);
    }

    if (!myLeg2PassedStatus) { // Box D
      // Leg 1 / MET cut
      fCommonPlots.fillControlPlotsAtMETSelection(iEvent, metData);
      if (!metData.passedEvent()) return;
      increment(fMetCounter);
      fCommonPlotsAfterMET->fill();

      double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();

      const QCDTailKiller::Data qcdTailKillerDataTmp = fQCDTailKiller.silentAnalyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
      if (qcdTailKillerDataTmp.passedBackToBackCuts()) {
        myHandler.fillShapeHistogram(hMtShapesAfterLeg1WithoutBtag, myTransverseMass, myWeightWithBtagSF);
        if (myFullMass > 0.) myHandler.fillShapeHistogram(hInvariantMassShapesAfterLeg1WithoutBtag, myFullMass, myWeightWithBtagSF);
      }

      // Leg 1 / b tagging
      BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
      if (btagData.passedEvent()) {
        increment(fBTaggingCounter);
        fCommonPlotsAfterMETAndBtag->fill();
      }
      if (!iEvent.isRealData()) {
        fBTagging.fillScaleFactorHistograms(btagData); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
        fEventWeight.multiplyWeight(btagData.getScaleFactor());
      }
      // Beyond this point, the b tag scale factor has already been applied
      fCommonPlots.fillControlPlotsAtBtagging(iEvent, btagData);
      if (!btagData.passedEvent()) return;
      increment(fBTaggingScaleFactorCounter);
      fCommonPlotsAfterMETAndBtagWithSF->fill();
      myHandler.fillShapeHistogram(hMETAfterBJets, myMetValue);

      //------ Improved delta phi cut, a.k.a. QCD tail killer, back-to-back part
      const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
      fCommonPlots.fillControlPlotsAtBackToBackDeltaPhiCuts(iEvent, qcdTailKillerData);
      if (!qcdTailKillerData.passedBackToBackCuts()) return;
      increment(fQCDTailKillerBackToBackCounter);

      //------ Top selection
      fCommonPlots.fillControlPlotsAtTopSelection(iEvent, topSelectionData);
      if (!(topSelectionData.passedEvent())) return;
      increment(fTopSelectionCounter);

      // Leg 1 passed
      increment(fAfterLeg1Counter);
      myHandler.fillShapeHistogram(hMETAfterLeg1, myMetValue);
      myHandler.fillShapeHistogram(hMtShapesAfterLeg1, myTransverseMass);
      if (myFullMass > 0.) myHandler.fillShapeHistogram(hInvariantMassShapesAfterLeg1, myFullMass);
      fCommonPlotsAfterLeg1->fill();
      fCommonPlots.fillControlPlotsAfterAllSelections(iEvent, myTransverseMass);
      if (myFullMass > 0.) fCommonPlots.fillControlPlotsAfterAllSelectionsWithFullMass(iEvent, myFullHiggsMassData);

    }

    // Leg 1 and leg 2 passed (for control only)
    if (myLeg1PassedStatus && myLeg2PassedStatus) { // Box D
      increment(fAfterLeg1AndLeg2Counter);
      myHandler.fillShapeHistogram(hMtShapesAfterLeg1AndLeg2, myTransverseMass);
      if (myFullMass > 0.) myHandler.fillShapeHistogram(hInvariantMassShapesAfterLeg1AndLeg2, myFullMass);
    }
  }

  void QCDMeasurementFactorised::doTreeFilling(edm::Event& iEvent, const edm::EventSetup& iSetup, const VertexSelection::Data& pvData, const edm::Ptr<pat::Tau>& selectedTau, const ElectronSelection::Data& electronData, const MuonSelection::Data& muonData, const JetSelection::Data& jetData, const METSelection::Data& metData) {
    // Obtain btagging data
    const BTagging::Data btagData = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());
    // Obtain QCD tail killer
    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.silentAnalyze(iEvent, iSetup, selectedTau, jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    // const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.analyze(iEvent, iSetup, selectedTau, jetData.getSelectedJets(), metData.getSelectedMET()); //testing
    // Obtain alphaT
    const EvtTopology::Data evtTopologyData = fEvtTopology.silentAnalyze(iEvent, iSetup, *(selectedTau), jetData.getSelectedJetsIncludingTau());

    // FIXME: Add filling of tree for QCD tail killer
    // FIXME: Add filling of weights (wjets ...)
    // Fill tree
    if(metData.getSelectedMET().isNonnull())
      fTree.setSelectedMet(metData.getSelectedMET());
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
    //if (!iEvent.isRealData()) {
    //  fEventWeight.multiplyWeight(btagData.getScaleFactor()); // needed to calculate the scale factor and the uncertainties
    //}
    fTree.setBTagging(btagData.passedEvent(), btagData.getScaleFactor(), btagData.getScaleFactorMaxAbsUncertainty());
    // Top reconstruction in different versions
    if (selectedTau.isNonnull() && btagData.passedEvent()) {
      BjetSelection::Data bjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), selectedTau, metData.getSelectedMET());
      TopSelectionManager::Data topSelectionData = fTopSelectionManager.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), bjetSelectionData.getBjetTopSide(), bjetSelectionData.passedEvent());
      fTree.setTop(topSelectionData.getTopP4());
    }
    // Sphericity, Aplanarity, Planarity, alphaT
    fTree.setDiJetMassesNoTau(evtTopologyData.alphaT().vDiJetMassesNoTau);
    fTree.setAlphaT(evtTopologyData.alphaT().fAlphaT);
    fTree.setSphericity(evtTopologyData.MomentumTensor().fSphericity);
    fTree.setAplanarity(evtTopologyData.MomentumTensor().fAplanarity);
    fTree.setPlanarity(evtTopologyData.MomentumTensor().fPlanarity);
    fTree.setCircularity(evtTopologyData.MomentumTensor().fCircularity);
    fTree.setMomentumTensorEigenvalues(evtTopologyData.MomentumTensor().fQOne, evtTopologyData.MomentumTensor().fQTwo, evtTopologyData.MomentumTensor().fQThree);
    fTree.setSpherocityTensorEigenvalues(evtTopologyData.SpherocityTensor().fQOne, evtTopologyData.SpherocityTensor().fQTwo, evtTopologyData.SpherocityTensor().fQThree);
    fTree.setCparameter(evtTopologyData.SpherocityTensor().fCparameter);
    fTree.setDparameter(evtTopologyData.SpherocityTensor().fDparameter);
    fTree.setJetThrust(evtTopologyData.SpherocityTensor().fJetThrust);
    fTree.setAllJets(jetData.getAllIdentifiedJets());
    fTree.setSelJets(jetData.getSelectedJets());
    fTree.setSelJetsInclTau(jetData.getSelectedJetsIncludingTau());
    fTree.setMHT(jetData.getMHTvector());
    fTree.setMHTSelJets(jetData.getSelectedJets());
    fTree.setMHTAllJets(jetData.getAllIdentifiedJets());
    //fTree.setDeltaPhi(fakeMETData.closestDeltaPhi());
    fTree.setNonIsoLeptons(muonData.getNonIsolatedMuons(), electronData.getNonIsolatedElectrons());
    if (selectedTau.isNonnull() && btagData.passedEvent()) {
      // FullH+ mass
      FullHiggsMassCalculator::Data FullHiggsMassDataTmp = fFullHiggsMassCalculator.silentAnalyze(iEvent, iSetup, selectedTau, btagData, metData);
      fTree.setHplusMassDiscriminant(FullHiggsMassDataTmp.getDiscriminant());
      fTree.setHplusMassHiggsMass(FullHiggsMassDataTmp.getHiggsMass());
      fTree.setHplusMassTopMass(FullHiggsMassDataTmp.getTopMass());
      fTree.setHplusMassSelectedNeutrinoPzSolution(FullHiggsMassDataTmp.getSelectedNeutrinoPzSolution());
      fTree.setHplusMassNeutrinoPtSolution(FullHiggsMassDataTmp.getNeutrinoPtSolution());
      fTree.setHplusMassMCNeutrinoPz(FullHiggsMassDataTmp.getMCNeutrinoPz());
    }
    fTree.setPassedTailKillerBackToBack(qcdTailKillerData.passedBackToBackCuts());
    fTree.setPassedTailKillerCollinear(qcdTailKillerData.passedCollinearCuts());

    for (int i = 0; i < qcdTailKillerData.getNConsideredJets(); ++i) {
      fTree.setRadiusFromBackToBackCornerJet(qcdTailKillerData.getRadiusFromBackToBackCorner(i));
      fTree.setRadiusFromCollinearCornerJet(qcdTailKillerData.getRadiusFromCollinearCorner(i));
      fTree.setTailKillerYaxisIntercept(qcdTailKillerData.getTailKillerYaxisIntercept(i));
    }

    fTree.fill(iEvent, selectedTau, jetData.getSelectedJets());
  }

  QCDMeasurementFactorised::TailTest::TailTest(std::string prefix, edm::Service<TFileService>& fs, HistoWrapper& histoWrapper) {
    std::string s = "TailTest_"+prefix;
    TFileDirectory myDir = fs->mkdir(s.c_str());
    fJetFakingTauGenuineTaus = new JetDetailHistograms(histoWrapper, myDir, "JetFakingTauGenuineTaus", true);
    fJetFakingTauFakeTaus = new JetDetailHistograms(histoWrapper, myDir, "JetFakingTauFakeTaus", true);
    fCollinearSystemJetsFakingTauGenuineTaus = new JetDetailHistograms(histoWrapper, myDir, "CollinearSystemJetsFakingTauGenuineTaus", true);
    fCollinearSystemJetsFakingTauFakeTaus = new JetDetailHistograms(histoWrapper, myDir, "CollinearSystemJetsFakingTauFakeTaus", true);
    fCollinearSystemJetsOppositeToTau = new JetDetailHistograms(histoWrapper, myDir, "CollinearSystemJetsOppositeToTau", true);
    fBackToBackSystemJetsFakingTauGenuineTaus = new JetDetailHistograms(histoWrapper, myDir, "BackToBackSystemJetsFakingTauGenuineTaus", true);
    fBackToBackSystemJetsFakingTauFakeTaus = new JetDetailHistograms(histoWrapper, myDir, "BackToBackSystemJetsFakingTauFakeTaus", true);
    fBackToBackSystemJetsOppositeToTau = new JetDetailHistograms(histoWrapper, myDir, "BackToBackSystemJetsOppositeToTau", true);
    // Delta phi experimental
    for (int i = 0; i < 4; ++i) {
      std::stringstream s1;
      std::stringstream s2;
      s1 << "TailTestByDeltaPhiJet" << i+1;
      s2 << "TailTestCollinearByDeltaPhi;#Delta#phi(#tau,MET),^{o};#Delta#phi(jet_{" << i+1 << "},MET),^{o}";
      hTailTestByDeltaPhi.push_back(histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, s1.str().c_str(), s2.str().c_str(), 36,0,180, 36,0,180));
      s1.str("");
      s2.str("");
      s1 << "TailTestByDeltaRJets" << i+1;
      s2 << "TailTestByDeltaRJets;#Delta#phi(#tau,MET),^{o};Sqrt((#eta_{jet_" << i+1 << "} + #eta_{#tau})^2 + (#phi_{jet_" << i+1 << "} + #phi_{#tau}))^2";
      hTailTestByDeltaRJets.push_back(histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, s1.str().c_str(), s2.str().c_str(), 36,0,180, 50,0,5.0));
      s1.str("");
      s2.str("");
      s1 << "TailTestByDeltaEtaJets" << i+1;
      s2 << "TailTestByDeltaEtaJets;#Delta#phi(#tau,MET),^{o};#eta_{jet_" << i+1 << "} + #eta_{#tau}";
      hTailTestByDeltaEtaJets.push_back(histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, s1.str().c_str(), s2.str().c_str(), 36,0,180, 50,0,5.0));
      s1.str("");
      s2.str("");
      s1 << "TailTestByDeltaPhiJets" << i+1;
      s2 << "TailTestByDeltaPhiJets;#Delta#phi(#tau,MET),^{o};#phi_{jet_" << i+1 << "} + #phi_{#tau}";
      hTailTestByDeltaPhiJets.push_back(histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, s1.str().c_str(), s2.str().c_str(), 36,0,180, 65,0,6.5));
      s1.str("");
      s2.str("");
      s1 << "TailTestDiffByDeltaEtaCollinearJet" << i+1;
      s2 << "TailTestDiffByDeltaEtaCollinear;#eta_{tau}+#eta_{jet" << i+1 << "};N_{jets}";
      hTailTestDiffByDeltaEtaCollinear.push_back(histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, s1.str().c_str(), s2.str().c_str(), 100,-5.0,5.0));
      s1.str("");
      s2.str("");
      s1 << "TailTestDiffByDeltaEtaBackToBackJet" << i+1;
      s2 << "TailTestDiffByDeltaEtaBackToBack;#eta_{tau}+#eta_{jet" << i+1 << "};N_{jets}";
      hTailTestDiffByDeltaEtaBackToBack.push_back(histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, s1.str().c_str(), s2.str().c_str(), 100,-5.0,5.0));
    }
    hTailTestMinDeltaR = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TailTestMinDeltaR","TailTestMinDeltaR;min #DeltaR;N_{events}", 50,0,5.0);
    hTailTestByDeltaPhiForMinDeltaR = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "TailTestByDeltaPhiForMinDeltaR", "TailTestByDeltaPhiForMinDeltaR;#Delta#phi(#tau,MET),^{o};#Delta#phi(jet_{min#DeltaR},MET),^{o}", 36,0,180, 36,0,180);
    hTailTestByDeltaPhiForMinDeltaR10 = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "TailTestByDeltaPhiForMinDeltaR10", "TailTestByDeltaPhiForMinDeltaR10;#Delta#phi(#tau,MET),^{o};#Delta#phi(jet_{min#DeltaR},MET),^{o}", 36,0,180, 36,0,180);
    hTailTestByDeltaPhiForMinDeltaR05 = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "TailTestByDeltaPhiForMinDeltaR05", "TailTestByDeltaPhiForMinDeltaR05;#Delta#phi(#tau,MET),^{o};#Delta#phi(jet_{min#DeltaR},MET),^{o}", 36,0,180, 36,0,180);
    hCollinearEtaPhi = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "CollinearEtaPhi", "CollinearEtaPhi;jet #eta; jet #phi, ^{o}", 58,-2.53073,2.53073, 72,-3.14159,3.14159);
    hBackToBackEtaPhi = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "BackToBackEtaPhi", "BackToBackEtaPhi;jet #eta; jet #phi, ^{o}", 58,-2.53073,2.53073, 72,-3.14159,3.14159);
    hCollinearEtaPhiForSelectedTau = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "CollinearEtaPhiForSelectedTau", "CollinearEtaPhiForSelectedTau;jet #eta; jet #phi, ^{o}", 58,-2.53073,2.53073, 72,-3.14159,3.14159);
    hBackToBackEtaPhiForSelectedTau = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "BackToBackEtaPhiForSelectedTau", "BackToBackEtaPhiForSelectedTau;jet #eta; jet #phi, ^{o}", 58,-2.53073,2.53073, 72,-3.14159,3.14159);
  }

  QCDMeasurementFactorised::TailTest::~TailTest() { }

  void QCDMeasurementFactorised::TailTest::Fill(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& selectedTau, const TauSelection& tauSelection, const QCDTailKiller::Data& qcdTailKillerData, const JetSelection::Data& jetData, const ElectronSelection::Data& eData, const MuonSelection::Data& muData, const METSelection::Data& metData, const bool isRealData, const bool isFakeTau) {
    // Obtain jet that is faking the tau
    edm::Ptr<pat::Jet> myJetFakingTheTau = jetData.getReferenceJetToTau();
    if (myJetFakingTheTau.isNull()) return;

    // Test effect of replacing deltaphi(jet_n,MET) with deltaR(jet_n,tau)
    size_t i = 0;
    double myDeltaPhiTauMET = DeltaPhi::reconstruct(*selectedTau, *(metData.getSelectedMET())) * 57.3;
    double myMinDeltaR = 999.;
    edm::Ptr<pat::Jet> myOppositeJet;
    while (i < jetData.getSelectedJetsIncludingTau().size() && i < 4) {
      //std::cout << i << std::endl;
      if (jetData.getSelectedJetsIncludingTau()[i] != myJetFakingTheTau) {
        double myDeltaPhiJetMET = DeltaPhi::reconstruct(*(jetData.getSelectedJetsIncludingTau()[i]), *(metData.getSelectedMET())) * 57.3;
        double myJetEta = jetData.getSelectedJetsIncludingTau()[i]->eta();
        double myJetPhi = jetData.getSelectedJetsIncludingTau()[i]->phi();
        hTailTestByDeltaPhi[i]->Fill(myDeltaPhiTauMET, myDeltaPhiJetMET);
        double myDeltaR = std::sqrt(std::pow(selectedTau->eta()+myJetEta,2) + std::pow(selectedTau->phi()+myJetPhi,2));
        //std::cout << "myJetPhi = " << myJetPhi << " myJetEta = " << myJetEta << std::endl;
        hTailTestByDeltaRJets[i]->Fill(myDeltaPhiTauMET, myDeltaR);
        hTailTestByDeltaEtaJets[i]->Fill(myDeltaPhiTauMET, selectedTau->eta()+myJetEta);
        hTailTestByDeltaPhiJets[i]->Fill(myDeltaPhiTauMET, selectedTau->phi()+myJetPhi);
        if (myDeltaR < myMinDeltaR) {
          myMinDeltaR = myDeltaR;
          myOppositeJet = jetData.getSelectedJetsIncludingTau()[i];
        }
        if (!qcdTailKillerData.passBackToBackCutForJet(i)) {
          hTailTestDiffByDeltaEtaBackToBack[i]->Fill(selectedTau->eta()-myJetEta);
          hBackToBackEtaPhi->Fill(myJetEta, myJetPhi);
          hBackToBackEtaPhiForSelectedTau->Fill(selectedTau->eta(),selectedTau->phi());
        } else if (!qcdTailKillerData.passCollinearCutForJet(i)) {
          hTailTestDiffByDeltaEtaCollinear[i]->Fill(selectedTau->eta()+myJetEta);
          hCollinearEtaPhi->Fill(myJetEta, myJetPhi);
          hCollinearEtaPhiForSelectedTau->Fill(selectedTau->eta(),selectedTau->phi());
        }
//       } else {
//         std::cout << "skipping genuine tau, phi = " << myJetFakingTheTau->phi() << " eta = " << myJetFakingTheTau->eta() << std::endl;
      }
      ++i;
    }
    if (!myOppositeJet.isNull()) {
      hTailTestMinDeltaR->Fill(myMinDeltaR);
      //std::cout << "min DeltaR=" << myMinDeltaR << std::endl;
      double myJetPhi = DeltaPhi::reconstruct(*(myOppositeJet), *(metData.getSelectedMET())) * 57.3;
      hTailTestByDeltaPhiForMinDeltaR->Fill(myDeltaPhiTauMET, myJetPhi);
      if (myMinDeltaR < 1.0)
        hTailTestByDeltaPhiForMinDeltaR10->Fill(myDeltaPhiTauMET, myJetPhi);
      if (myMinDeltaR < 0.5)
        hTailTestByDeltaPhiForMinDeltaR05->Fill(myDeltaPhiTauMET, myJetPhi);
    }
    //std::cout << "done" << std::endl;
    //std::cout << "QCD tail killer status: " << qcdTailKillerData.passedBackToBackCuts() << " " << qcdTailKillerData.passedCollinearCuts() << std::endl;
    if (qcdTailKillerData.passedBackToBackCuts() && !qcdTailKillerData.passedCollinearCuts()) {
      // Situation is that the jet faking tau is collinear with MET and the recoiling jet is back-to-back with MET
      // Why does rejecting these events make the mT closure test agree?
      // I.e. why is there a correlation between the collinear system and tau isolation?

      // Obtain jet that is back to back to the jet faking the tau
      edm::Ptr<pat::Jet> myJetOppositeToTau;
      for (int i = 0; i < qcdTailKillerData.getNConsideredJets(); ++i) {
        if (myJetOppositeToTau.isNull() && !qcdTailKillerData.passCollinearCutForJet(i)) {
          myJetOppositeToTau = jetData.getSelectedJetsIncludingTau()[i]; // sorted by Et
        }
      }
      if (myJetOppositeToTau.isNull()) return;

      // Fill jet detail histograms
      if (isFakeTau) {
        fCollinearSystemJetsFakingTauFakeTaus->fill(myJetFakingTheTau, isRealData);
        fCollinearSystemJetsFakingTauFakeTaus->fillLeptonDetails(iEvent, myJetFakingTheTau, eData, muData, isRealData);
      } else {
        fCollinearSystemJetsFakingTauGenuineTaus->fill(myJetFakingTheTau, isRealData);
        fCollinearSystemJetsFakingTauGenuineTaus->fillLeptonDetails(iEvent, myJetFakingTheTau, eData, muData, isRealData);
      }
      fCollinearSystemJetsOppositeToTau->fill(myJetOppositeToTau, isRealData);
      fCollinearSystemJetsOppositeToTau->fillLeptonDetails(iEvent, myJetOppositeToTau, eData, muData, isRealData);
    } else if (!qcdTailKillerData.passedBackToBackCuts() && qcdTailKillerData.passedCollinearCuts()) {
      // Situation is that the jet faking tau is back to back with MET and the recoiling jet is collinear with MET

      // Obtain jet that is back to back to the jet faking the tau
      edm::Ptr<pat::Jet> myJetOppositeToTau;
      for (int i = 0; i < qcdTailKillerData.getNConsideredJets(); ++i) {
        if (myJetOppositeToTau.isNull() && !qcdTailKillerData.passBackToBackCutForJet(i)) {
          myJetOppositeToTau = jetData.getSelectedJetsIncludingTau()[i]; // sorted by Et
        }
      }
      if (myJetOppositeToTau.isNull()) return;

      // Fill jet detail histograms
      if (isFakeTau) {
        fBackToBackSystemJetsFakingTauFakeTaus->fill(myJetFakingTheTau, isRealData);
        fBackToBackSystemJetsFakingTauFakeTaus->fillLeptonDetails(iEvent, myJetFakingTheTau, eData, muData, isRealData);
      } else {
        fBackToBackSystemJetsFakingTauGenuineTaus->fill(myJetFakingTheTau, isRealData);
        fBackToBackSystemJetsFakingTauGenuineTaus->fillLeptonDetails(iEvent, myJetFakingTheTau, eData, muData, isRealData);
      }
      fBackToBackSystemJetsOppositeToTau->fill(myJetOppositeToTau, isRealData);
      fBackToBackSystemJetsOppositeToTau->fillLeptonDetails(iEvent, myJetOppositeToTau, eData, muData, isRealData);
    }

    // For control, fill in all cases the jet faking tau details
    if (isFakeTau) {
      fJetFakingTauFakeTaus->fill(myJetFakingTheTau, isRealData);
    } else {
      fJetFakingTauGenuineTaus->fill(myJetFakingTheTau, isRealData);
    }

    // Answered by the detail histograms:
    // Multiplicity of PF charged particles in jet faking the tau
    // Multiplicity of PF charged particles for recoiling jet
    // Multiplicity of PF gammas in jet faking the tau
    // Multiplicity of PF gammas for recoiling jet
    // ET(RECO) / ET(GEN) for jet faking tau
    // ET(RECO) / ET(GEN) for recoiling jet
    // Flavor of the jet faking the tau (is it a b jet?)

    // Jet faking tau overlapping with electron or muon?
    // Jet faking tau overlapping with electron or muon from a b jet?

  }
}

