#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ConfigInfo.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"

// #include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventClassification.h"

#include "TLorentzVector.h"

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace {
  template <typename T>
  void copyPtrToVector(const edm::PtrVector<T>& src, std::vector<T>& dst) {
    dst.reserve(src.size());
    for(typename edm::PtrVector<T>::const_iterator i = src.begin(); i != src.end(); ++i) {
      dst.push_back(**i);
    }
  }
}



namespace HPlus {
  SignalAnalysis::CounterGroup::CounterGroup(EventCounter& eventCounter) :
    fOneTauCounter(eventCounter.addCounter("EWKfaketaus:taus == 1")),
    fElectronVetoCounter(eventCounter.addCounter("EWKfaketaus:electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("EWKfaketaus:muon veto")),
    fNJetsCounter(eventCounter.addCounter("EWKfaketaus:njets")),
    fDeltaPhiCollinearCounter(eventCounter.addCounter("EWKfaketaus:deltaphi collinear")),
    fMETCounter(eventCounter.addCounter("EWKfaketaus:MET")),
    fBTaggingCounter(eventCounter.addCounter("EWKfaketaus:btagging")),
    fDeltaPhiBackToBackCounter(eventCounter.addCounter("EWKfaketaus:deltaphi backtoback")),
    fSelectedEventsCounter(eventCounter.addCounter("EWKfaketaus:SelectedEvents")),
    fSelectedEventsFullMassCounter(eventCounter.addCounter("EWKfaketaus:SelectedEventsFullMass")),
    fFakeMETVetoCounter(eventCounter.addCounter("EWKfaketaus:fake MET veto")) { }
  SignalAnalysis::CounterGroup::CounterGroup(EventCounter& eventCounter, std::string prefix) :
    fOneTauCounter(eventCounter.addSubCounter(prefix,":taus == 1")),
    fElectronVetoCounter(eventCounter.addSubCounter(prefix,":electron veto")),
    fMuonVetoCounter(eventCounter.addSubCounter(prefix,":muon veto")),
    fNJetsCounter(eventCounter.addSubCounter(prefix,":njets")),
    fDeltaPhiCollinearCounter(eventCounter.addSubCounter(prefix,":deltaphi collinear")),
    fMETCounter(eventCounter.addSubCounter(prefix,":MET")),
    fBTaggingCounter(eventCounter.addSubCounter(prefix,":btagging")),
    fDeltaPhiBackToBackCounter(eventCounter.addSubCounter(prefix,":deltaphi backtoback")),
    fSelectedEventsCounter(eventCounter.addSubCounter(prefix,"EWKfaketaus:SelectedEvents")),
    fSelectedEventsFullMassCounter(eventCounter.addSubCounter(prefix,"EWKfaketaus:SelectedEventsFullMass")),
    fFakeMETVetoCounter(eventCounter.addSubCounter(prefix,":fake MET veto")) { }
  SignalAnalysis::CounterGroup::~CounterGroup() { }

  SignalAnalysis::SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper):
    fEventWeight(eventWeight),
    fHistoWrapper(histoWrapper),
    bBlindAnalysisStatus(iConfig.getUntrackedParameter<bool>("blindAnalysisStatus")),
    bTauEmbeddingStatus(iConfig.getUntrackedParameter<bool>("tauEmbeddingStatus")),
    fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
    fTopRecoName(iConfig.getUntrackedParameter<std::string>("topReconstruction")),
    fOneAndThreeProngTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("oneAndThreeProngTauSrc")),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    // Main counters
    fAllCounter(eventCounter.addCounter("Offline selection begins")),
    fTopPtWeightCounter(eventCounter.addCounter("Top pt reweight")),
    fWJetsWeightCounter(eventCounter.addCounter("WJets inc+exl weight")),
    fEmbeddingGeneratorWeightCounter(eventCounter.addCounter("Embedding: generator weight")),
    fEmbeddingWTauMuWeightCounter(eventCounter.addCounter("Embedding: W->tau->mu weight")),
    fMETFiltersCounter(eventCounter.addCounter("MET filters")),
    fEmbeddingMuonTriggerEfficiencyCounter(eventCounter.addCounter("Embedding: muon trig eff weight")),
    fEmbeddingMuonIdEfficiencyCounter(eventCounter.addCounter("Embedding: muon ID eff weight")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),
    fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
    fTausExistCounter(eventCounter.addCounter("taus > 0")),
    fTauFakeScaleFactorCounter(eventCounter.addCounter("tau fake scale factor")),
    fOneTauCounter(eventCounter.addCounter("taus == 1")),
    fTauTriggerScaleFactorCounter(eventCounter.addCounter("tau trigger scale factor")),
    fGenuineTauCounter(eventCounter.addCounter("Tau is genuine")),
    fVetoTauCounter(eventCounter.addCounter("tau veto")),
    fElectronVetoCounter(eventCounter.addCounter("electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("muon veto")),
    fNJetsCounter(eventCounter.addCounter("njets")),
    fPreMETCutCounter(eventCounter.addCounter("pre-MET cut")),
    fMETTriggerScaleFactorCounter(eventCounter.addCounter("MET trigger scale factor")),
    fQCDTailKillerCollinearCounter(eventCounter.addCounter("QCD tail killer collinear")),
    fMETCounter(eventCounter.addCounter("MET")),
    fBTaggingCounter(eventCounter.addCounter("btagging")),

    fBTaggingScaleFactorCounter(eventCounter.addCounter("btagging scale factor")),
    fEmbeddingMTWeightCounter(eventCounter.addCounter("Embedding: mT weight")),
    fQCDTailKillerBackToBackCounter(eventCounter.addCounter("QCD tail killer back-to-back")),
    fTopReconstructionCounter(eventCounter.addCounter("Top reconstruction")),
    fSelectedEventsCounter(eventCounter.addCounter("Selected events")),
    fHiggsMassSelectionCounter(eventCounter.addCounter("HiggsMassSelection")),
    fFakeMETVetoCounter(eventCounter.addCounter("FakeMETVeto")),

    fTauVetoAfterDeltaPhiCounter(eventCounter.addCounter("TauVeto after DeltaPhi cut")),
    fRealTauAfterDeltaPhiCounter(eventCounter.addCounter("Real tau after deltaPhi cut")),
    fRealTauAfterDeltaPhiTauVetoCounter(eventCounter.addCounter("Real tau after deltaPhi+tauveto cut")),


    fSelectedEventsCounterWithGenuineBjets(eventCounter.addCounter("Selected events with genuine bjets")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
    fElectronSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("ElectronSelection"), fPrimaryVertexSelection.getSelectedSrc(), eventCounter, fHistoWrapper),
    fMuonSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MuonSelection"), eventCounter, fHistoWrapper),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    fVetoTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("vetoTauSelection"),
                      iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"),
                      eventCounter, fHistoWrapper),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, fHistoWrapper),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, fHistoWrapper, "MET", fTauSelection.getIsolationDiscriminator()),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, fHistoWrapper),
    fBTaggingEfficiencyInMC(eventCounter, fHistoWrapper),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, fHistoWrapper),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, fHistoWrapper),
/*    fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, fHistoWrapper),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, fHistoWrapper),
    fTopWithWSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithWSelection"), eventCounter, fHistoWrapper),
    //    fTopWithMHSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithMHSelection"), eventCounter, fHistoWrapper), */
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, fHistoWrapper),
    fMCAnalysisOfSelectedEvents(iConfig.getUntrackedParameter<edm::ParameterSet>("MCAnalysisOfSelectedEvents"), eventCounter, fHistoWrapper),     
    fTopSelectionManager(iConfig, eventCounter, fHistoWrapper, fTopRecoName),
    //   ftransverseMassCut(iConfig.getUntrackedParameter<edm::ParameterSet>("transverseMassCut")),
    fFullHiggsMassCalculator(iConfig.getUntrackedParameter<edm::ParameterSet>("invMassReco"), eventCounter, fHistoWrapper),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, fHistoWrapper),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, fHistoWrapper),
    fCorrelationAnalysis(eventCounter, fHistoWrapper, "HistoName"),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, fHistoWrapper),
    fTauTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("tauTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fMETTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("metTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fEmbeddingMuonTriggerEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("embeddingMuonTriggerEfficiency")),
    fEmbeddingMuonIdEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("embeddingMuonIdEfficiency")),
    fEmbeddingMTWeight(iConfig.getUntrackedParameter<edm::ParameterSet>("embeddingMTWeight")),
    fPrescaleWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("prescaleWeightReader"), fHistoWrapper, "PrescaleWeight"),
    fPileupWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("pileupWeightReader"), fHistoWrapper, "PileupWeight"),
    fWJetsWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("wjetsWeightReader"), fHistoWrapper, "WJetsWeight"),
    fTopPtWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("topPtWeightReader"), fHistoWrapper, "TopPtWeight"),
    fEmbeddingGeneratorWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("embeddingGeneratorWeightReader"), fHistoWrapper, "EmbeddingGeneratorWeight"),
    fEmbeddingWTauMuWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("embeddingWTauMuWeightReader"), fHistoWrapper, "EmbeddingWTauMuWeight"),
    fVertexAssignmentAnalysis(iConfig, eventCounter, fHistoWrapper),
    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), fHistoWrapper, "TauID"),
    fMETFilters(iConfig.getUntrackedParameter<edm::ParameterSet>("metFilters"), eventCounter),
    fQCDTailKiller(iConfig.getUntrackedParameter<edm::ParameterSet>("QCDTailKiller"), eventCounter, fHistoWrapper),
    fTauEmbeddingMuonIsolationQuantifier(eventCounter, fHistoWrapper),
    fTree(iConfig.getUntrackedParameter<edm::ParameterSet>("Tree"), fBTagging.getDiscriminator()),
    // Scale factor uncertainties
    fSFUncertaintiesAfterSelection(fHistoWrapper, "AfterSelection"),
    fEWKFakeTausSFUncertaintiesAfterSelection(fHistoWrapper, "EWKFakeTausAfterSelection"),
    // EKW+tt with fake taus (Non-QCD Type II) related
    fEWKFakeTausGroup(eventCounter),
    fAllTausCounterGroup(eventCounter, "All"),
    fElectronToTausCounterGroup(eventCounter, "e->tau"),
    fElectronFromTauDecayToTausCounterGroup(eventCounter, "tau_e->tau"),
    fMuonToTausCounterGroup(eventCounter, "mu->tau"),
    fMuonFromTauDecayToTausCounterGroup(eventCounter, "tau_mu->tau"),
    fGenuineToTausCounterGroup(eventCounter, "tau->tau"),
    fGenuineOneProngToTausCounterGroup(eventCounter, "1-prong tau->tau"),
    fJetToTausCounterGroup(eventCounter, "jet->tau"),
    fAllTausAndTauJetInsideAcceptanceCounterGroup(eventCounter, "All with tau jet inside acceptance"),
    fElectronToTausAndTauJetInsideAcceptanceCounterGroup(eventCounter, "e->tau with tau jet inside acceptance"),
    fElectronFromTauDecayToTausAndTauJetInsideAcceptanceCounterGroup(eventCounter, "tau_e->tau with tau jet inside acceptance"),
    fMuonToTausAndTauJetInsideAcceptanceCounterGroup(eventCounter, "mu->tau with tau jet inside acceptance"),
    fMuonFromTauDecayToTausAndTauJetInsideAcceptanceCounterGroup(eventCounter, "tau_mu->tau with tau jet inside acceptance"),
    fGenuineToTausAndTauJetInsideAcceptanceCounterGroup(eventCounter, "tau->tau with tau jet inside acceptance"),
    fGenuineOneProngToTausAndTauJetInsideAcceptanceCounterGroup(eventCounter, "1-prong tau->tau with tau jet inside acceptance"),
    fJetToTausAndTauJetInsideAcceptanceCounterGroup(eventCounter, "jet->tau with tau jet inside acceptance"),
    fModuleLabel(iConfig.getParameter<std::string>("@module_label")),
    fProduce(iConfig.getUntrackedParameter<bool>("produceCollections", false)),
    fOnlyEmbeddingGenuineTaus(iConfig.getUntrackedParameter<bool>("onlyEmbeddingGenuineTaus", false)),
    // Common plots
    fCommonPlots(iConfig.getUntrackedParameter<edm::ParameterSet>("commonPlotsSettings"), eventCounter, fHistoWrapper, CommonPlots::kSignalAnalysis, bTauEmbeddingStatus),
    fCommonPlotsAfterVertexSelection(fCommonPlots.createCommonPlotsFilledAtEveryStep("VertexSelection",false,"Vtx")),
    fCommonPlotsAfterTauSelection(fCommonPlots.createCommonPlotsFilledAtEveryStep("TauSelection",false,"TauID")),
    fCommonPlotsAfterTauWeight(fCommonPlots.createCommonPlotsFilledAtEveryStep("TauWeight",true,"Tau")),
    fCommonPlotsAfterElectronVeto(fCommonPlots.createCommonPlotsFilledAtEveryStep("ElectronVeto",true,"e veto")),
    fCommonPlotsAfterMuonVeto(fCommonPlots.createCommonPlotsFilledAtEveryStep("MuonVeto",true,"#mu veto")),
    fCommonPlotsAfterJetSelection(fCommonPlots.createCommonPlotsFilledAtEveryStep("JetSelection",true,"#geq3j")),
    fCommonPlotsAfterMET(fCommonPlots.createCommonPlotsFilledAtEveryStep("MET",true,"E_{T}^{miss}")),
    fCommonPlotsAfterMETWithPhiOscillationCorrection(fCommonPlots.createCommonPlotsFilledAtEveryStep("METPhiCorrected",false,"E_{T}^{miss} #phi corected")),
    fCommonPlotsAfterBTagging(fCommonPlots.createCommonPlotsFilledAtEveryStep("BTagging",true,"#geq1b tag")),
    fCommonPlotsAfterBackToBackDeltaPhi(fCommonPlots.createCommonPlotsFilledAtEveryStep("DeltaPhiBackToBack",true,"#Delta#phi b2b")),
    fCommonPlotsSelected(fCommonPlots.createCommonPlotsFilledAtEveryStep("Selected",true,"Selected")),
    fCommonPlotsSelectedMtTail(fCommonPlots.createCommonPlotsFilledAtEveryStep("SelectedMtTail",false,"SelectedMtTail")),
    fCommonPlotsSelectedFullMass(fCommonPlots.createCommonPlotsFilledAtEveryStep("SelectedFullMass",false,"SelectedFullMass")),
    // Probabilistic b tag as event weight (note: for invariant mass, b tag is needed!)
    fCommonPlotsProbabilisticBTagAfterBTagging(fCommonPlots.createCommonPlotsFilledAtEveryStep("ProbBtag_BTagging",false,"#geq1b tag")),
    fCommonPlotsProbabilisticBTagAfterBackToBackDeltaPhi(fCommonPlots.createCommonPlotsFilledAtEveryStep("ProbBtag_DeltaPhiBackToBack",false,"#Delta#phi b2b")),
    fCommonPlotsProbabilisticBTagSelected(fCommonPlots.createCommonPlotsFilledAtEveryStep("ProbBtag_Selected",false,"Selected")),
    fCommonPlotsProbabilisticBTagSelectedMtTail(fCommonPlots.createCommonPlotsFilledAtEveryStep("ProbBtag_SelectedMtTail",false,"SelectedMtTail")),
    // Common plots for EWK fake taus background
    fCommonPlotsAfterTauSelectionEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_TauSelection",false,"TauID")),
    fCommonPlotsAfterTauWeightEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_TauWeight",false,"Tau")),
    fCommonPlotsAfterElectronVetoEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_ElectronVeto",false,"e veto")),
    fCommonPlotsAfterMuonVetoEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_MuonVeto",false,"#mu veto")),
    fCommonPlotsAfterJetSelectionEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_JetSelection",false,"#geq3j")),
    fCommonPlotsAfterMETEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_MET",false,"E_{T}^{miss}")),
    fCommonPlotsAfterBTaggingEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_BTagging",false,"#geq1b tag")),
    fCommonPlotsAfterBackToBackDeltaPhiEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_DeltaPhiBackToBack",true,"#Delta#phi b2b")),
    fCommonPlotsSelectedEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_Selected",false,"Selected")),
    fCommonPlotsSelectedMtTailEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_SelectedMtTail",false,"SelectedMtTail")),
    fCommonPlotsSelectedFullMassEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_SelectedFullMass",false,"FakeTaus_SelectedFullMass")),
    // Probabilistic b tag as event weight (note: for invariant mass, b tag is needed!)
    fCommonPlotsProbabilisticBTagAfterBTaggingEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_ProbBtag_BTagging",false,"#geq1b tag")),
    fCommonPlotsProbabilisticBTagAfterBackToBackDeltaPhiEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_ProbBtag_DeltaPhiBackToBack",false,"#Delta#phi b2b")),
    fCommonPlotsProbabilisticBTagSelectedEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_ProbBtag_Selected",false,"Selected")),
    fCommonPlotsProbabilisticBTagSelectedMtTailEWKFakeTausBkg(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_ProbBtag_SelectedMtTail",false,"SelectedMtTail"))
  {
    // Check parameter initialisation
    if (fTopRecoName != "None" && fTopRecoName != "chi" && fTopRecoName != "std" && fTopRecoName != "Wselection" && fTopRecoName != "Bselection") {
      throw cms::Exception("config") << "selected topReconstruction is invalid! Valid options are: None, chi, std, Wselection, Bselection";
    }

    edm::Service<TFileService> fs;
    ConfigInfo::writeConfigInfo(iConfig, *fs);

    // Book histograms filled in the analysis body
    
    // Vertex histograms
    TFileDirectory myVertexDir = fs->mkdir("Vertices");
    hVerticesBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myVertexDir, "verticesBeforeWeight", "Number of vertices without weighting", 40, 0, 40);
    hVerticesAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myVertexDir, "verticesAfterWeight", "Number of vertices with weighting", 40, 0, 40);

    /*
    htransverseMassElectronFromTauFound = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassElectronFromTauFound", "transverseMassElectronFromTauFound", 200, 0., 400.);
    htransverseMassElectronFromWFound = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassElectronFromWFound", "transverseMassElectronFromWFound", 200, 0., 400.);
    htransverseMassElectronFromBottomFound = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassElectronFromBottomFound", "transverseMassElectronFromBottpmFound", 200, 0., 400.);
    htransverseMassElectronFound = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassElectronFound", "transverseMassElectronFound", 200, 0., 400.);

    htransverseMassMuonFromTauFound = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassMuonFromTauFound", "transverseMassMuonFromTauFound", 200, 0., 400.);
    htransverseMassMuonFromWFound = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassMuonFromWFound", "transverseMassMuonFromWFound", 200, 0., 400.);
    htransverseMassMuonFromBottomFound = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassMuonFromBottomFound", "transverseMassMuonFromBottpmFound", 200, 0., 400.);
    htransverseMassMuonFound = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassMuonFound", "transverseMassMuonFound", 200, 0., 400.);
    htransverseMassTauFromWFound = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassTauFromWFound", "transverseMassTauFromWFound", 200, 0., 400.);
    htransverseMassTauFound = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassTauFound", "transverseMassTauFound", 200, 0., 400.);
    */
    // Transverse mass for top algorithms
    hTransverseMassTopSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopSelection", "transverseMassTopSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTopChiSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopChiSelection", "transverseMassTopChiSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTopBjetSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopBjetSelection", "transverseMassTopBjetSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTopWithWSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopWithWSelection", "transverseMassTopWithWSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTauVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTauVeto", "transverseMassTauVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassFakeMetVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassFakeMetVeto", "transverseMassFakeMetVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);

    hTransverseMassVsNjets = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "transverseMassVsNjets", "transverseMassVsNjets;m_{T}(tau,MET), GeV/c^{2};N_{jets}", 200, 0., 400., 10, 0., 10.);
    hEWKFakeTausTransverseMassVsNjets = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "EWKFakeTausTransverseMassVsNjets", "EWKFakeTausTransverseMassVsNjets;m_{T}(tau,MET), GeV/c^{2};N_{jets}", 200, 0., 400., 10, 0., 10.);

    hDeltaPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 180, 0., 180.);

    hEWKFakeTausDeltaPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "EWKFakeTausDeltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 180, 0., 180.);
    hAlphaT = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "alphaT", "alphaT", 100, 0.0, 5.0);
    hAlphaTInvMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);
    hAlphaTVsRtau = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "alphaT(y)-Vs-Rtau(x)", "alphaT-Vs-Rtau",  120, 0.0, 1.2, 500, 0.0, 5.0);

    TFileDirectory mySelectedTauDir = fs->mkdir("SelectedTau");
    hSelectedTauEt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_pT_AfterTauID", "SelectedTau_pT_AfterTauID;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 300, 0.0, 600.0);
    //    hSelectedTauEtMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedTau_pT_AfterTauID_MetCut", "SelectedTau_pT_AfterTauID_MetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_eta_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.1", 250, -5.0, 5.0);
    hSelectedTauEtAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_pT_AfterCuts", "SelectedTau_pT_AfterCuts;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 300, 0.0, 600.0);
    hSelectedTauEtaAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_eta_AfterCuts", "SelectedTau_eta_AfterCuts;#tau #eta;N_{events} / 0.1", 250, -5.0, 5.0);
    hSelectedTauPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_phi_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_Rtau_AfterTauID", "SelectedTau_Rtau_AfterTauID;R_{#tau};N_{events} / 0.1", 240, 0., 1.2);
    hSelectedTauRtauAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_Rtau_AfterCuts", "SelectedTau_Rtau_AfterCuts;R_{#tau};N_{events} / 0.1", 240, 0., 1.2);
    hSelectedTauLeadingTrackPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_TauLeadingTrackPt", "SelectedTau_TauLeadingTrackPt;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    hEWKFakeTausSelectedTauEtAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "EWKFakeTaus_SelectedTau_pT_AfterCuts", "SelectedTau_pT_AfterCuts;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    hEWKFakeTausSelectedTauEtaAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "EWKFakeTaus_SelectedTau_eta_AfterCuts", "SelectedTau_eta_AfterCuts;#tau #eta;N_{events} / 0.1", 250, -5.0, 5.0);
    
    // Histograms used for jet flavour tagging efficiency calculation in MC
    TFileDirectory myBTagEffDir = fs->mkdir("BTaggingEfficiencyInMC");
    hGenuineBJetEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineBJetEta", "genuineBJetEta;b-jet #eta;N_{events} / 0.05", 200, -5.0, 5.0);
    hGenuineBJetWithBTagEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineBJetWithBTagEta", "genuineBJetWithBTagEta;b-jet #eta;N_{events} / 0.05", 200, -5.0, 5.0);
    hGenuineGJetEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineGJetEta", "genuineGJetEta;b-jet #eta;N_{events} / 0.05", 200, -5.0, 5.0);
    hGenuineGJetWithBTagEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineGJetWithBTagEta", "genuineGJetWithBTagEta;b-jet #eta;N_{events} / 0.05", 200, -5.0, 5.0);
    hGenuineUDSJetEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineUDSJetEta", "genuineUDSJetEta;b-jet #eta;N_{events} / 0.05", 200, -5.0, 5.0);
    hGenuineUDSJetWithBTagEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineUDSJetWithBTagEta", "genuineUDSJetWithBTagEta;b-jet #eta;N_{events} / 0.05", 200, -5.0, 5.0);
    hGenuineCJetEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineCJetEta", "genuineCJetEta;b-jet #eta;N_{events} / 0.05", 200, -5.0, 5.0);
    hGenuineCJetWithBTagEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineCJetWithBTagEta", "genuineCJetWithBTagEta;b-jet #eta;N_{events} / 0.05", 200, -5.0, 5.0);
    hGenuineLJetEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineLJetEta", "genuineLJetEta;b-jet #eta;N_{events} / 0.05", 200, -5.0, 5.0);
    hGenuineLJetWithBTagEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineLJetWithBTagEta", "genuineLJetWithBTagEta;b-jet #eta;N_{events} / 0.05", 200, -5.0, 5.0);
    
    hGenuineBJetPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineBJetPt", "genuineBJetPt;b-jet p_{T};N_{events} / 1 GeV", 500, 0.0, 500.0);
    hGenuineBJetWithBTagPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineBJetWithBTagPt", "genuineBJetWithBTagPt;b-jet p_{T};N_{events} / 1 GeV", 500, 0.0, 500.0);
    hGenuineGJetPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineGJetPt", "genuineGJetPt;b-jet p_{T};N_{events} / 1 GeV", 500, 0.0, 500.0);
    hGenuineGJetWithBTagPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineGJetWithBTagPt", "genuineGJetWithBTagPt;b-jet p_{T};N_{events} / 1 GeV", 500, 0.0, 500.0);
    hGenuineUDSJetPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineUDSJetPt", "genuineUDSJetPt;b-jet p_{T};N_{events} / 1 GeV", 500, 0.0, 500.0);
    hGenuineUDSJetWithBTagPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineUDSJetWithBTagPt", "genuineUDSJetWithBTagPt;b-jet p_{T};N_{events} / 1 GeV", 500, 0.0, 500.0);
    hGenuineCJetPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineCJetPt", "genuineCJetPt;b-jet p_{T};N_{events} / 1 GeV", 500, 0.0, 500.0);
    hGenuineCJetWithBTagPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineCJetWithBTagPt", "genuineCJetWithBTagPt;b-jet p_{T};N_{events} / 1 GeV", 500, 0.0, 500.0);
    hGenuineLJetPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineLJetPt", "genuineLJetPt;b-jet p_{T};N_{events} / 1 GeV", 500, 0.0, 500.0);
    hGenuineLJetWithBTagPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBTagEffDir, "genuineLJetWithBTagPt", "genuineLJetWithBTagPt;b-jet p_{T};N_{events} / 1 GeV", 500, 0.0, 500.0);

    hGenuineBJetPtAndEta = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myBTagEffDir, "genuineBJetPtAndEta", "genuineBJetPtAndEta;b-jet p_{T};b-jet #eta;N_{events}", 500, 0.0, 500.0, 200, -5.0, 5.0);
    hGenuineBJetWithBTagPtAndEta = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myBTagEffDir, "genuineBJetWithBTagPtAndEta", "genuineBJetWithBTagPtAndEta;b-jet p_{T};b-jet #eta;N_{events}", 500, 0.0, 500.0, 200, -5.0, 5.0);
    hGenuineGJetPtAndEta = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myBTagEffDir, "genuineGJetPtAndEta", "genuineGJetPtAndEta;b-jet p_{T};b-jet #eta;N_{events}", 500, 0.0, 500.0, 200, -5.0, 5.0);
    hGenuineGJetWithBTagPtAndEta = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myBTagEffDir, "genuineGJetWithBTagPtAndEta", "genuineGJetWithBTagPtAndEta;b-jet p_{T};b-jet #eta;N_{events}", 500, 0.0, 500.0, 200, -5.0, 5.0);
    hGenuineUDSJetPtAndEta = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myBTagEffDir, "genuineUDSJetPtAndEta", "genuineUDSJetPtAndEta;b-jet p_{T};b-jet #eta;N_{events}", 500, 0.0, 500.0, 200, -5.0, 5.0);
    hGenuineUDSJetWithBTagPtAndEta = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myBTagEffDir, "genuineUDSJetWithBTagPtAndEta", "genuineUDSJetWithBTagPtAndEta;b-jet p_{T};b-jet #eta;N_{events}", 500, 0.0, 500.0, 200, -5.0, 5.0);
    hGenuineCJetPtAndEta = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myBTagEffDir, "genuineCJetPtAndEta", "genuineCJetPtAndEta;b-jet p_{T};b-jet #eta;N_{events}", 500, 0.0, 500.0, 200, -5.0, 5.0);
    hGenuineCJetWithBTagPtAndEta = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myBTagEffDir, "genuineCJetWithBTagPtAndEta", "genuineCJetWithBTagPtAndEta;b-jet p_{T};b-jet #eta;N_{events}", 500, 0.0, 500.0, 200, -5.0, 5.0);
    hGenuineLJetPtAndEta = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myBTagEffDir, "genuineLJetPtAndEta", "genuineLJetPtAndEta;b-jet p_{T};b-jet #eta;N_{events}", 500, 0.0, 500.0, 200, -5.0, 5.0);
    hGenuineLJetWithBTagPtAndEta = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myBTagEffDir, "genuineLJetWithBTagPtAndEta", "genuineLJetWithBTagPtAndEta;b-jet p_{T};b-jet #eta;N_{events}", 500, 0.0, 500.0, 200, -5.0, 5.0);
    
    hSelectionFlow = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SignalSelectionFlow", "SignalSelectionFlow;;N_{events}", 15, 0, 15);
    hSelectionFlowVsVertices = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "SignalSelectionFlowVsVertices", "SignalSelectionFlowVsVertices;N_{vertices};Step", 50, 0, 50, 15, 0, 15);
    hSelectionFlowVsVerticesEWKFakeTausBkg = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "SignalSelectionFlowVsVerticesFakeTaus", "SignalSelectionFlowVsVerticesFakeTaus;N_{vertices};Step", 50, 0, 50, 15, 0, 15);
    if(hSelectionFlow->getHisto()) {
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderTrigger,"Trigger");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderVertexSelection,"PV selection");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderTauID,"#tau ID");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderElectronVeto,"Isol. e veto");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderMuonVeto,"Isol. #mu veto");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderJetSelection,"jet sel.");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderDeltaPhiCollinearSelection,"#Delta#phi collinear cuts");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderMETSelection,"MET");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderBTagSelection,"b-jet sel.");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderDeltaPhiBackToBackSelection,"#Delta#phi back-to-back cuts");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderFakeMETVeto,"Fake MET veto");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderBjetSelection,"B for Top selection");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderTopSelection,"Top selection");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderSelectedEvents,"Selected events");
      hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderSelectedEventsFullMass,"Selected events full mass");
      //hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderFakeMETVeto,"Further QCD rej.");
      //hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderTopSelection,"Top mass");

      for (int i = 0; i < 13; ++i) {
        hSelectionFlowVsVertices->getHisto()->GetYaxis()->SetBinLabel(i+1, hSelectionFlow->getHisto()->GetXaxis()->GetBinLabel(i+1));
        hSelectionFlowVsVerticesEWKFakeTausBkg->getHisto()->GetYaxis()->SetBinLabel(i+1, hSelectionFlow->getHisto()->GetXaxis()->GetBinLabel(i+1));
      }
    }

    hEMFractionAll = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "EWKFakeTaus_FakeTau_EMFraction_All", "FakeTau_EMFraction_All", 22, 0., 1.1);
    hEMFractionElectrons = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "EWKFakeTaus_FakeTau_EMFraction_Electrons", "FakeTau_EMFraction_Electrons", 22, 0., 1.1);

    hCtrlJetMatrixAfterJetSelection = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "JetMatrixAfterJetSelection", "JetMatrixAfterJetSelection;Number of selected jets;Number of selected b jets", 7, 3., 10.,7, 0., 7.);
    hCtrlJetMatrixAfterMET = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "JetMatrixAfterMET", "JetMatrixAfterMET;Number of selected jets;Number of selected b jets", 7, 3., 10.,7, 0., 7.);
    hCtrlJetMatrixAfterMET100 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "JetMatrixAfterMET100", "JetMatrixAfterMET100;Number of selected jets;Number of selected b jets", 7, 3., 10.,7, 0., 7.);

    fTree.init(*fs);

    hReferenceJetToTauDeltaPtDecayMode0 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "DeltaPtDecayMode0", "ReferenceJetToTauDeltaPtDecayMode0;#tau p_{T} - ref.jet p_{T}, GeV/c;N_{events}", 200, -200., 200.);
    hReferenceJetToTauDeltaPtDecayMode1 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "DeltaPtDecayMode1", "ReferenceJetToTauDeltaPtDecayMode1;#tau p_{T} - ref.jet p_{T}, GeV/c;N_{events}", 200, -200., 200.);
    hReferenceJetToTauDeltaPtDecayMode2 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "DeltaPtDecayMode2", "ReferenceJetToTauDeltaPtDecayMode2;#tau p_{T} - ref.jet p_{T}, GeV/c;N_{events}", 200, -200., 200.);
    hReferenceJetToTauDeltaPtDecayMode0NoNeutralHadrons = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "DeltaPtDecayMode0NoNeutralHadrons", "ReferenceJetToTauDeltaPtDecayMode0NoNeutralHadrons;#tau p_{T} - ref.jet p_{T}, GeV/c;N_{events}", 200, -200., 200.);
    hReferenceJetToTauDeltaPtDecayMode1NoNeutralHadrons = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "DeltaPtDecayMode1NoNeutralHadrons", "ReferenceJetToTauDeltaPtDecayMode1NoNeutralHadrons;#tau p_{T} - ref.jet p_{T}, GeV/c;N_{events}", 200, -200., 200.);
    hReferenceJetToTauDeltaPtDecayMode2NoNeutralHadrons = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "DeltaPtDecayMode2NoNeutralHadrons", "ReferenceJetToTauDeltaPtDecayMode2NoNeutralHadrons;#tau p_{T} - ref.jet p_{T}, GeV/c;N_{events}", 200, -200., 200.);

    TFileDirectory ttbarDir = fs->mkdir("TTBarDecayMode");
    hTTBarDecayModeAfterVertexSelection = GenParticleAnalysis::bookTTBarDecayModeHistogram(fHistoWrapper, HistoWrapper::kVital, ttbarDir, "ttbarDecayMode_AfterVertexSelection");
    hTTBarDecayModeAfterVertexSelectionUnweighted = GenParticleAnalysis::bookTTBarDecayModeHistogram(fHistoWrapper, HistoWrapper::kVital, ttbarDir, "ttbarDecayModeUnweighted_AfterVertexSelection");
    hTTBarDecayModeAfterStandardSelections = GenParticleAnalysis::bookTTBarDecayModeHistogram(fHistoWrapper, HistoWrapper::kVital, ttbarDir, "ttbarDecayMode_AfterStandardSelections");
    hTTBarDecayModeAfterStandardSelectionsUnweighted = GenParticleAnalysis::bookTTBarDecayModeHistogram(fHistoWrapper, HistoWrapper::kVital, ttbarDir, "ttbarDecayModeUnweighted_AfterStandardSelections");
    hTTBarDecayModeAfterMtSelections = GenParticleAnalysis::bookTTBarDecayModeHistogram(fHistoWrapper, HistoWrapper::kVital, ttbarDir, "ttbarDecayMode_AfterMtSelections");
    hTTBarDecayModeAfterMtSelectionsUnweighted = GenParticleAnalysis::bookTTBarDecayModeHistogram(fHistoWrapper, HistoWrapper::kVital, ttbarDir, "ttbarDecayModeUnweighted_AfterMtSelections");



    // Print info about number of booked histograms
    std::string myModuleLabel = iConfig.getParameter<std::string>("@module_label");
    
    if (myModuleLabel.find("SystVar") == std::string::npos && myModuleLabel.find("Opt") == std::string::npos) {
      std::cout << "Histogram breakdown for module " << myModuleLabel << std::endl;
      fHistoWrapper.printHistoStatistics();
    }
  }

  SignalAnalysis::~SignalAnalysis() { }

  void SignalAnalysis::produces(edm::EDFilter *producer) const {
    if(fProduce) {
      producer->produces<std::vector<pat::Tau> >("selectedTaus");
      producer->produces<std::vector<pat::Tau> >("selectedVetoTaus");
      producer->produces<std::vector<pat::Jet> >("selectedJets");
      producer->produces<std::vector<pat::Jet> >("selectedBJets");
      producer->produces<std::vector<pat::Electron> >("selectedVetoElectronsBeforePtAndEtaCuts");
      producer->produces<std::vector<pat::Muon> >("selectedVetoMuonsBeforeIsolationAndPtAndEtaCuts");
      producer->produces<std::vector<pat::Muon> >("selectedVetoMuonsBeforePtAndEtaCuts");
    }
  }

  bool SignalAnalysis::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    fEventWeight.beginEvent();

    if (bTauEmbeddingStatus)
      fTauEmbeddingMuonIsolationQuantifier.analyzeAfterTrigger(iEvent, iSetup);

//------ Set prescale
    const double prescaleWeight = fPrescaleWeightReader.getWeight(iEvent, iSetup);
    fEventWeight.multiplyWeight(prescaleWeight);
    fTree.setPrescaleWeight(prescaleWeight);

//------ Pileup weight
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
      fTree.setWjetsWeight(wjetsWeight);
    }
    increment(fWJetsWeightCounter);

//------ For embedding, incorporate generator weight here (N(vispt > cut)/Nall)
    if(bTauEmbeddingStatus) {
      double embeddingWeight = fEmbeddingGeneratorWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(embeddingWeight);
      fTree.setEmbeddingGeneratorWeight(embeddingWeight);
    }
    increment(fEmbeddingGeneratorWeightCounter);

    if(bTauEmbeddingStatus) {
      double embeddingWeight = fEmbeddingWTauMuWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(embeddingWeight);
      fTree.setEmbeddingWTauMuWeight(embeddingWeight);
    }
    increment(fEmbeddingWTauMuWeightCounter);


//------ MET (noise) filters for data (reject events with instrumental fake MET)
    if(iEvent.isRealData()) {
      if(!fMETFilters.passedEvent(iEvent, iSetup)) return false;
    }
    increment(fMETFiltersCounter);

//------ For embedding, apply the muon ID efficiency at this stage
    EmbeddingMuonEfficiency::Data embeddingMuonTriggerData;
    EmbeddingMuonEfficiency::Data embeddingMuonIdData;
    if(bTauEmbeddingStatus) {
      embeddingMuonTriggerData = fEmbeddingMuonTriggerEfficiency.getEventWeight(iEvent);
      fEventWeight.multiplyWeight(embeddingMuonTriggerData.getEventWeight());
    }
    increment(fEmbeddingMuonTriggerEfficiencyCounter);
    if(bTauEmbeddingStatus) {
      embeddingMuonIdData = fEmbeddingMuonIdEfficiency.getEventWeight(iEvent);
      fEventWeight.multiplyWeight(embeddingMuonIdData.getEventWeight());
    }
    increment(fEmbeddingMuonIdEfficiencyCounter);

//------ Apply trigger and HLT_MET cut or trigger parametrisation
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);
    hSelectionFlow->Fill(kSignalOrderTrigger);
    if(triggerData.hasTriggerPath()) // protection if TriggerSelection is disabled
      fTree.setHltTaus(triggerData.getTriggerTaus());

//------ GenParticle analysis (must be done here when we effectively trigger all MC)
    GenParticleAnalysis::Data genData;
    if(!iEvent.isRealData()) {
      genData = fGenparticleAnalysis.analyze(iEvent, iSetup);
      if(genData.isValid())
        fTree.setGenMET(genData.getGenMET());
    }

//------ Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    size_t nVertices = pvData.getNumberOfAllVertices();
    hSelectionFlow->Fill(kSignalOrderVertexSelection);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderVertexSelection);
    hVerticesBeforeWeight->Fill(nVertices, myWeightBeforePileupReweighting);
    hVerticesAfterWeight->Fill(nVertices);
    fTree.setNvertices(nVertices);

    // Setup common plots
    fCommonPlots.initialize(iEvent, iSetup, pvData, fTauSelection, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETTriggerEfficiencyScaleFactor, fMETSelection, fBTagging, fQCDTailKiller, fBjetSelection, fTopSelectionManager, fEvtTopology, fFullHiggsMassCalculator);

    //fCommonPlotsAfterVertexSelection->fill();
    fCommonPlots.fillControlPlotsAfterVertexSelection(iEvent, pvData);
    if(genData.isValid()) {
      hTTBarDecayModeAfterVertexSelection->Fill(genData.getTTBarDecayMode());
      hTTBarDecayModeAfterVertexSelectionUnweighted->Fill(genData.getTTBarDecayMode(), 1.0);
    }

//------ Apply filter (if chosen) to select tail events
    //if (!selectTailEvents(iEvent, iSetup, pvData)) return false;


//------ TauID
    /*
    // Test transverse mass regions for embedded events
    if(bTauEmbeddingStatus) {
      TauSelection::Data tauDataTmp = fTauSelection.silentAnalyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
      if(tauDataTmp.getAllTauObjects().size() == 0)
        return false;
      if(tauDataTmp.getAllTauObjects().size() != 1)
        throw cms::Exception("Assert") << "There should be only one embedded tau, got " << tauDataTmp.getAllTauObjects().size();
      edm::Ptr<pat::Tau> theTau = tauDataTmp.getAllTauObjects()[0];
      JetSelection::Data jetDataTmp = fJetSelection.silentAnalyze(iEvent, iSetup, theTau, nVertices);
      METSelection::Data metDataTmp = fMETSelection.silentAnalyze(iEvent, iSetup, nVertices, theTau, jetDataTmp.getAllJets());
      double transverseMass = TransverseMass::reconstruct(*theTau, *(metDataTmp.getSelectedMET()));
      if(!(transverseMass < 120))
        //if(!(transverseMass >= 120))
        return false;
    }
    */

    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
    fTauSelection.analyseFakeTauComposition(fFakeTauIdentifier,iEvent);
    if(!tauData.passedEvent()) return false; // Require at least one tau
    if (!fTauSelection.passesDecayModeFilter(tauData.getSelectedTau())) return false;
    //    std::cout << "taus  " << tauData.getSelectedTaus().size() << std::endl;

    // Obtain MC matching - for EWK without genuine taus
    FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, *(tauData.getSelectedTau()));
    bool mySelectedToEWKFakeTauBackgroundStatus = tauMatchData.isEWKFakeTauLike();
    fCommonPlotsAfterTauSelection->fill();
    fCommonPlots.fillControlPlotsAfterTauSelection(iEvent, iSetup, tauData, tauMatchData, fJetSelection, fMETSelection, fBTagging, fQCDTailKiller);
    fTree.setTauIsFake(mySelectedToEWKFakeTauBackgroundStatus);
    if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsAfterTauSelectionEWKFakeTausBkg->fill();
    // Below "genuine tau" is in the context of embedding (i.e. irrespective of the tau decay)
    if (fOnlyEmbeddingGenuineTaus && !tauMatchData.isEmbeddingGenuineTauLike()) return false;
    increment(fTausExistCounter);
    // Apply scale factor for fake tau
    if (!iEvent.isRealData())
      fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauData.getSelectedTau()->eta()));
    // plot leading track without pt cut
    hSelectedTauLeadingTrackPt->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt());
    increment(fTauFakeScaleFactorCounter);
    if (tauData.getSelectedTaus().size() == 1) increment(fOneTauCounter);
    // Primary vertex assignment analysis - diagnostics only
    fVertexAssignmentAnalysis.analyze(iEvent, iSetup, iEvent.isRealData(), pvData.getSelectedVertex(), tauData.getSelectedTau(), tauMatchData.getTauMatchType());
    // For data, set the current run number (needed for tau embedding
    // input, doesn't harm for normal data except by wasting small
    // amount of time)
    if(iEvent.isRealData())
      fTauTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
    // Apply trigger scale factor here, because it depends only on tau
    TauTriggerEfficiencyScaleFactor::Data tauTriggerWeight = fTauTriggerEfficiencyScaleFactor.applyEventWeight(*(tauData.getSelectedTau()), iEvent.isRealData(), fEventWeight);
    fTree.setTauTriggerWeight(tauTriggerWeight.getEventWeight(), tauTriggerWeight.getEventWeightAbsoluteUncertainty());
    increment(fTauTriggerScaleFactorCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderTauID, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Tau> > saveTaus(new std::vector<pat::Tau>());
      copyPtrToVector(tauData.getSelectedTaus(), *saveTaus);
      iEvent.put(saveTaus, "selectedTaus");
    }
    fCommonPlotsAfterTauWeight->fill();
    if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsAfterTauWeightEWKFakeTausBkg->fill();
    fCommonPlots.fillControlPlotsAfterTauTriggerScaleFactor(iEvent);
    //    hSelectedTauRtau->Fill(tauData.getRtauOfSelectedTau());  
    if (!tauMatchData.isGenuineTau())
      increment(fGenuineTauCounter);

    // For plotting Rtau
    //    if (!tauData.selectedTauPassedRtau()) return false;
    //    if (tauData.getRtauOfSelectedTau() < 0.7) return false;
    hSelectedTauLeadingTrackPt->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt());
    hSelectedTauEt->Fill(tauData.getSelectedTau()->pt());
    hSelectedTauEta->Fill(tauData.getSelectedTau()->eta());
    hSelectedTauPhi->Fill(tauData.getSelectedTau()->phi());

    fAllTausCounterGroup.incrementOneTauCounter();
    if (tauMatchData.getTauMatchType() == FakeTauIdentifier::kkElectronToTau)
      hEMFractionElectrons->Fill(tauData.getSelectedTau()->emFraction());
    hEMFractionAll->Fill(tauData.getSelectedTau()->emFraction());


//------ Veto against second tau in event
    VetoTauSelection::Data vetoTauData = fVetoTauSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), pvData.getSelectedVertex()->z());
    fCommonPlots.fillControlPlotsAtTauVetoSelection(iEvent, iSetup, vetoTauData);
    //    if (vetoTauData.passedEvent()) return false; // tau veto
    //    if (!vetoTauData.passedEvent()) return false; // select events with add. taus
    //    if (vetoTauData.getSelectedVetoTaus().size() > 0 ) return false;
    //    increment(fVetoTauCounter);
    if (vetoTauData.passedEvent()) increment(fVetoTauCounter);


//------ Global electron veto
    ElectronSelection::Data electronVetoData = fElectronSelection.analyze(iEvent, iSetup);
    fCommonPlots.fillControlPlotsAtElectronSelection(iEvent, electronVetoData);
    //    NonIsolatedElectronVeto::Data electronVetoData = fNonIsolatedElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false;
    fCommonPlotsAfterElectronVeto->fill();
    if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsAfterElectronVetoEWKFakeTausBkg->fill();
    increment(fElectronVetoCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderElectronVeto, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Electron> > saveElectrons(new std::vector<pat::Electron>());
      copyPtrToVector(electronVetoData.getSelectedElectronsBeforePtAndEtaCuts(), *saveElectrons);
      iEvent.put(saveElectrons, "selectedVetoElectronsBeforePtAndEtaCuts");
    }


//------ Global muon veto
    MuonSelection::Data muonVetoData = fMuonSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    fCommonPlots.fillControlPlotsAtMuonSelection(iEvent, muonVetoData);
    if (!muonVetoData.passedEvent()) return false;
    fCommonPlotsAfterMuonVeto->fill();
    if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsAfterMuonVetoEWKFakeTausBkg->fill();
    increment(fMuonVetoCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderMuonVeto, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Muon> > saveMuons(new std::vector<pat::Muon>());
      copyPtrToVector(muonVetoData.getSelectedMuonsBeforePtAndEtaCuts(), *saveMuons);
      iEvent.put(saveMuons, "selectedVetoMuonsBeforePtAndEtaCuts");
    }





//------ Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), nVertices);
    fCommonPlots.fillControlPlotsAtJetSelection(iEvent, jetData);

    if (jetData.getReferenceJetToTau().isNonnull() && tauMatchData.isJetToTau()) {
      double myDeltaPtWithoutNeutralHadrons = tauData.getSelectedTau()->pt() - jetData.getReferenceJetToTau()->pt() * (1.0-jetData.getReferenceJetToTau()->neutralHadronEnergyFraction());
      if (tauData.getSelectedTau()->decayMode() == 0) {
        hReferenceJetToTauDeltaPtDecayMode0->Fill(jetData.getReferenceJetToTauDeltaPt());
        hReferenceJetToTauDeltaPtDecayMode0NoNeutralHadrons->Fill(myDeltaPtWithoutNeutralHadrons);
      } else if (tauData.getSelectedTau()->decayMode() == 1) {
        hReferenceJetToTauDeltaPtDecayMode1->Fill(jetData.getReferenceJetToTauDeltaPt());
        hReferenceJetToTauDeltaPtDecayMode1NoNeutralHadrons->Fill(myDeltaPtWithoutNeutralHadrons);
      } else if (tauData.getSelectedTau()->decayMode() == 2) {
        hReferenceJetToTauDeltaPtDecayMode2->Fill(jetData.getReferenceJetToTauDeltaPt());
        hReferenceJetToTauDeltaPtDecayMode2NoNeutralHadrons->Fill(myDeltaPtWithoutNeutralHadrons);
      }
    }

    if(!jetData.passedEvent()) return false;
    increment(fNJetsCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderJetSelection, tauData);
    fCommonPlotsAfterJetSelection->fill();
    if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsAfterJetSelectionEWKFakeTausBkg->fill();
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveJets(new std::vector<pat::Jet>());
      copyPtrToVector(jetData.getSelectedJets(), *saveJets);
      iEvent.put(saveJets, "selectedJets");
    }
    if (bTauEmbeddingStatus)
      fTauEmbeddingMuonIsolationQuantifier.analyzeAfterJets(iEvent, iSetup);


//------ MET trigger scale factor
    // For data, set the current run number (needed for tau embedding
    // input, doesn't harm for normal data except by wasting small
    // amount of time)
    METSelection::Data metDataTmp = fMETSelection.silentAnalyze(iEvent, iSetup, nVertices, tauData.getSelectedTau(), jetData.getAllJets());


    if(!metDataTmp.passedPreMetCut()) return false;
    increment(fPreMETCutCounter);
    if(iEvent.isRealData())
      fMETTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
    // Apply trigger scale factor here for now, SF calculated for tau+3 jets events
    METTriggerEfficiencyScaleFactor::Data metTriggerWeight = fMETTriggerEfficiencyScaleFactor.applyEventWeight(*(metDataTmp.getSelectedMET()), iEvent.isRealData(), fEventWeight);
    fTree.setMETTriggerWeight(metTriggerWeight.getEventWeight(), metTriggerWeight.getEventWeightAbsoluteUncertainty());
    increment(fMETTriggerScaleFactorCounter);
    fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(iEvent);

//------ Improved delta phi cut, a.k.a. QCD tail killer - collinear part
    const QCDTailKiller::Data qcdTailKillerDataCollinear = fQCDTailKiller.silentAnalyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metDataTmp.getSelectedMET());
    fCommonPlots.fillControlPlotsAtCollinearDeltaPhiCuts(iEvent, qcdTailKillerDataCollinear);
    if (!qcdTailKillerDataCollinear.passedCollinearCuts()) return false;
    increment(fQCDTailKillerCollinearCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderDeltaPhiCollinearSelection, tauData);


//------ Fill TTree, if it is active
    if (fTree.isActive()) {
      doTreeFilling(iEvent, iSetup, pvData, tauData.getSelectedTau(), electronVetoData, muonVetoData, jetData);
      //return true;
    }

    // BTagging::silentAnalyze() needs to be called before the first call to BTaggingEfficiencyInMC::silentAnalyze()
    BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());

    BTaggingEfficiencyInMC::Data bTagEffData_afterCollinearCut = fBTaggingEfficiencyInMC.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets(), btagDataTmp);
    for (edm::PtrVector<pat::Jet>::iterator jet = bTagEffData_afterCollinearCut.getGenuineBJets().begin(); jet != bTagEffData_afterCollinearCut.getGenuineBJets().end(); ++jet) {
      hGenuineBJetPt->Fill((*jet)->pt());
      hGenuineBJetEta->Fill((*jet)->eta());
      hGenuineBJetPtAndEta->Fill((*jet)->pt(),(*jet)->eta());
    }
    for (edm::PtrVector<pat::Jet>::iterator jet = bTagEffData_afterCollinearCut.getGenuineBJetsWithBTag().begin(); jet != bTagEffData_afterCollinearCut.getGenuineBJetsWithBTag().end(); ++jet) {
      hGenuineBJetWithBTagPt->Fill((*jet)->pt());
      hGenuineBJetWithBTagEta->Fill((*jet)->eta());
      hGenuineBJetWithBTagPtAndEta->Fill((*jet)->pt(),(*jet)->eta());
    }
    for (edm::PtrVector<pat::Jet>::iterator jet = bTagEffData_afterCollinearCut.getGenuineGJets().begin(); jet != bTagEffData_afterCollinearCut.getGenuineGJets().end(); ++jet) {
      hGenuineGJetPt->Fill((*jet)->pt());
      hGenuineGJetEta->Fill((*jet)->eta());
      hGenuineGJetPtAndEta->Fill((*jet)->pt(),(*jet)->eta());
    }
    for (edm::PtrVector<pat::Jet>::iterator jet = bTagEffData_afterCollinearCut.getGenuineGJetsWithBTag().begin(); jet != bTagEffData_afterCollinearCut.getGenuineGJetsWithBTag().end(); ++jet) {
      hGenuineGJetWithBTagPt->Fill((*jet)->pt());
      hGenuineGJetWithBTagEta->Fill((*jet)->eta());
      hGenuineGJetWithBTagPtAndEta->Fill((*jet)->pt(),(*jet)->eta());
    }
    for (edm::PtrVector<pat::Jet>::iterator jet = bTagEffData_afterCollinearCut.getGenuineUDSJets().begin(); jet != bTagEffData_afterCollinearCut.getGenuineUDSJets().end(); ++jet) {
      hGenuineUDSJetPt->Fill((*jet)->pt());
      hGenuineUDSJetEta->Fill((*jet)->eta());
      hGenuineUDSJetPtAndEta->Fill((*jet)->pt(),(*jet)->eta());
    }
    for (edm::PtrVector<pat::Jet>::iterator jet = bTagEffData_afterCollinearCut.getGenuineUDSJetsWithBTag().begin(); jet != bTagEffData_afterCollinearCut.getGenuineUDSJetsWithBTag().end(); ++jet) {
      hGenuineUDSJetWithBTagPt->Fill((*jet)->pt());
      hGenuineUDSJetWithBTagEta->Fill((*jet)->eta());
      hGenuineUDSJetWithBTagPtAndEta->Fill((*jet)->pt(),(*jet)->eta());
    }
    for (edm::PtrVector<pat::Jet>::iterator jet = bTagEffData_afterCollinearCut.getGenuineCJets().begin(); jet != bTagEffData_afterCollinearCut.getGenuineCJets().end(); ++jet) {
      hGenuineCJetPt->Fill((*jet)->pt());
      hGenuineCJetEta->Fill((*jet)->eta());
      hGenuineCJetPtAndEta->Fill((*jet)->pt(),(*jet)->eta());
    }
    for (edm::PtrVector<pat::Jet>::iterator jet = bTagEffData_afterCollinearCut.getGenuineCJetsWithBTag().begin(); jet != bTagEffData_afterCollinearCut.getGenuineCJetsWithBTag().end(); ++jet) {
      hGenuineCJetWithBTagPt->Fill((*jet)->pt());
      hGenuineCJetWithBTagEta->Fill((*jet)->eta());
      hGenuineCJetWithBTagPtAndEta->Fill((*jet)->pt(),(*jet)->eta());
    }
    for (edm::PtrVector<pat::Jet>::iterator jet = bTagEffData_afterCollinearCut.getGenuineLJets().begin(); jet != bTagEffData_afterCollinearCut.getGenuineLJets().end(); ++jet) {
      hGenuineLJetPt->Fill((*jet)->pt());
      hGenuineLJetEta->Fill((*jet)->eta());
      hGenuineLJetPtAndEta->Fill((*jet)->pt(),(*jet)->eta());
    }
    for (edm::PtrVector<pat::Jet>::iterator jet = bTagEffData_afterCollinearCut.getGenuineLJetsWithBTag().begin(); jet != bTagEffData_afterCollinearCut.getGenuineLJetsWithBTag().end(); ++jet) {
      hGenuineLJetWithBTagPt->Fill((*jet)->pt());
      hGenuineLJetWithBTagEta->Fill((*jet)->eta());
      hGenuineLJetWithBTagPtAndEta->Fill((*jet)->pt(),(*jet)->eta());
    }


    // Obtain delta phi and transverse mass here, but do not yet cut on them
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metDataTmp.getSelectedMET())) * 57.3; // converted to degrees
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metDataTmp.getSelectedMET()));

//------ b tagging cut
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
    // Apply btag pass probability as weight to event (to get better stats. for W+jets and DY)
    if (!iEvent.isRealData()) {
      double myBTagPassProbability = btagData.getProbabilityToPassBtagging();
      fEventWeight.multiplyWeight(myBTagPassProbability);
      fCommonPlotsProbabilisticBTagAfterBTagging->fill();
      if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsProbabilisticBTagAfterBTaggingEWKFakeTausBkg->fill();
      METSelection::Data metDataTmp = fMETSelection.silentAnalyze(iEvent, iSetup, nVertices, tauData.getSelectedTau(), jetData.getAllJets());
      if (metDataTmp.passedEvent() && qcdTailKillerDataCollinear.passedBackToBackCuts()) {
        fCommonPlotsProbabilisticBTagAfterBackToBackDeltaPhi->fill();
        fCommonPlotsProbabilisticBTagSelected->fill();
        if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsProbabilisticBTagAfterBackToBackDeltaPhiEWKFakeTausBkg->fill();
        if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsProbabilisticBTagSelectedEWKFakeTausBkg->fill();
        fCommonPlots.fillControlPlotsAfterAllSelectionsWithProbabilisticBtag(iEvent, transverseMass);
        if (transverseMass > 120) {
          fCommonPlotsProbabilisticBTagSelectedMtTail->fill();
          if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsProbabilisticBTagSelectedMtTailEWKFakeTausBkg->fill();
        }
      }
      // Undo btag pass probability weight and continue selection as usual
      fEventWeight.multiplyWeight(1.0/myBTagPassProbability);
    }
    if(btagData.passedEvent()) increment(fBTaggingCounter);
    // Apply scale factor as weight to event
    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
    fCommonPlots.fillControlPlotsAtBtagging(iEvent, btagData);
    if(!btagData.passedEvent()) return false;
    increment(fBTaggingScaleFactorCounter);
    fCommonPlotsAfterBTagging->fill();
    if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsAfterBTaggingEWKFakeTausBkg->fill();
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderBTagSelection, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveBJets(new std::vector<pat::Jet>());
      copyPtrToVector(btagData.getSelectedJets(), *saveBJets);
      iEvent.put(saveBJets, "selectedBJets");
    }

    // For embedding, performt mT weighting
    if(bTauEmbeddingStatus) {
      EmbeddingMTWeightFit::Data data = fEmbeddingMTWeight.getEventWeight(transverseMass);
      fEventWeight.multiplyWeight(data.getEventWeight());
    }
    increment(fEmbeddingMTWeightCounter);


//------ ttbar topology selected
    fCommonPlots.fillControlPlotsAfterTopologicalSelections(iEvent);
    if(genData.isValid()) {
      hTTBarDecayModeAfterStandardSelections->Fill(genData.getTTBarDecayMode());
      hTTBarDecayModeAfterStandardSelectionsUnweighted->Fill(genData.getTTBarDecayMode(), 1.0);
    }


//------ MET cut
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, nVertices, tauData.getSelectedTau(), jetData.getAllJets());
    fCommonPlots.fillControlPlotsAtMETSelection(iEvent, metData);
    if (transverseMass > 40 && transverseMass < 100)
      hCtrlJetMatrixAfterJetSelection->Fill(jetData.getHadronicJetCount(), btagDataTmp.getBJetCount());
    // Now cut on MET
    if (metData.getPhiCorrectedSelectedMET()->et() > 50.0) fCommonPlotsAfterMETWithPhiOscillationCorrection->fill(); // FIXME: temp
    if(!metData.passedEvent()) return false;
    fCommonPlotsAfterMET->fill();
    if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsAfterMETEWKFakeTausBkg->fill();
    increment(fMETCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderMETSelection, tauData);

    // Plot jet matrix
    if (transverseMass > 40 && transverseMass < 100) {
      hCtrlJetMatrixAfterMET->Fill(jetData.getHadronicJetCount(), btagDataTmp.getBJetCount());
      if (metData.getSelectedMET()->et() > 100.0)
        hCtrlJetMatrixAfterMET100->Fill(jetData.getHadronicJetCount(), btagDataTmp.getBJetCount());
    }


//------ Improved delta phi cut, a.k.a. QCD tail killer, back-to-back part
    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    fCommonPlots.fillControlPlotsAtBackToBackDeltaPhiCuts(iEvent, qcdTailKillerData);
    if (!qcdTailKillerData.passedBackToBackCuts()) return false;
    increment(fQCDTailKillerBackToBackCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderDeltaPhiBackToBackSelection, tauData);
    fCommonPlotsAfterBackToBackDeltaPhi->fill();
    if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsAfterBackToBackDeltaPhiEWKFakeTausBkg->fill();


//------ Delta phi(tau,MET) after delta phi cuts
    hDeltaPhi->Fill(deltaPhi);
    if (mySelectedToEWKFakeTauBackgroundStatus) hEWKFakeTausDeltaPhi->Fill(deltaPhi);


    if (!iEvent.isRealData() && genData.isValid()) {
      fMCAnalysisOfSelectedEvents.analyze(iEvent, iSetup, tauData, metData, genData);
      // doMCAnalysisOfSelectedEvents(iEvent, tauData, vetoTauData, metData, genData);
      hTTBarDecayModeAfterMtSelections->Fill(genData.getTTBarDecayMode());
      hTTBarDecayModeAfterMtSelectionsUnweighted->Fill(genData.getTTBarDecayMode(), 1.0);
    }

//------ Top reconstruction
    BjetSelection::Data bjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());
    TopSelectionManager::Data topSelectionData = fTopSelectionManager.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), bjetSelectionData.getBjetTopSide(), bjetSelectionData.passedEvent());
    fCommonPlots.fillControlPlotsAtTopSelection(iEvent, topSelectionData);
    if (!(topSelectionData.passedEvent())) return false;
    increment(fTopReconstructionCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderTopSelection, tauData);


//------ Calculate alphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(iEvent, iSetup, *(tauData.getSelectedTau()), jetData.getSelectedJetsIncludingTau());
    fCommonPlots.fillControlPlotsAtEvtTopology(iEvent, evtTopologyData);


//------ Transverse mass and control plots
    fCommonPlots.fillControlPlotsAfterAllSelections(iEvent, transverseMass);
    increment(fSelectedEventsCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderSelectedEvents, tauData);
    if (btagData.hasGenuineBJets()) increment(fSelectedEventsCounterWithGenuineBjets);
    hTransverseMassVsNjets->Fill(transverseMass, jetData.getHadronicJetCount());
    fCommonPlotsSelected->fill();
    if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsSelectedEWKFakeTausBkg->fill();
    if (transverseMass > 120) {
      fCommonPlotsSelectedMtTail->fill();
      if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsSelectedMtTailEWKFakeTausBkg->fill();
    }

    hSelectedTauRtauAfterCuts->Fill(tauData.getSelectedTauRtauValue());
    hSelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt());
    hSelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta());


//------ Syst. uncertainties handling FIXME: to be phased out
    fSFUncertaintiesAfterSelection.setScaleFactorUncertainties(mySelectedToEWKFakeTauBackgroundStatus,
                                                            fEventWeight.getWeight(),
                                                            fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauData.getSelectedTau()->eta()),
                                                            fFakeTauIdentifier.getFakeTauSystematics(tauMatchData.getTauMatchType(), tauData.getSelectedTau()->eta()),
							       btagData.getScaleFactor(), btagData.getScaleFactorMaxAbsUncertainty());
    fSFUncertaintiesAfterSelection.setTauTriggerScaleFactorUncertainty(fEventWeight.getWeight(),
                                                                       tauTriggerWeight.getEventWeight(),
                                                                       tauTriggerWeight.getEventWeightAbsoluteUncertainty());
    fSFUncertaintiesAfterSelection.setMETTriggerScaleFactorUncertainty(fEventWeight.getWeight(),
                                                                       metTriggerWeight.getEventWeight(),
                                                                       metTriggerWeight.getEventWeightAbsoluteUncertainty());

    if(bTauEmbeddingStatus) // FIXME: add trigger efficiency too
      fSFUncertaintiesAfterSelection.setEmbeddingMuonEfficiencyUncertainty(fEventWeight.getWeight(),
                                                                           embeddingMuonIdData.getEventWeight(),
                                                                           embeddingMuonIdData.getEventWeightAbsoluteUncertainty());

    if (mySelectedToEWKFakeTauBackgroundStatus) {
      hEWKFakeTausTransverseMassVsNjets->Fill(transverseMass, jetData.getHadronicJetCount());
      fEWKFakeTausSFUncertaintiesAfterSelection.setScaleFactorUncertainties(mySelectedToEWKFakeTauBackgroundStatus,
                                                                            fEventWeight.getWeight(),
                                                                            fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauData.getSelectedTau()->eta()),
                                                                            fFakeTauIdentifier.getFakeTauSystematics(tauMatchData.getTauMatchType(), tauData.getSelectedTau()->eta()),
                                                                            btagData.getScaleFactor(), btagData.getScaleFactorMaxAbsUncertainty());
      fEWKFakeTausSFUncertaintiesAfterSelection.setTauTriggerScaleFactorUncertainty(fEventWeight.getWeight(),
                                                                                    tauTriggerWeight.getEventWeight(),
                                                                                    tauTriggerWeight.getEventWeightAbsoluteUncertainty());
      fEWKFakeTausSFUncertaintiesAfterSelection.setMETTriggerScaleFactorUncertainty(fEventWeight.getWeight(),
                                                                                    metTriggerWeight.getEventWeight(),
                                                                                    metTriggerWeight.getEventWeightAbsoluteUncertainty());
    }


//------ Full Higgs mass reconstruction
    FullHiggsMassCalculator::Data fullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData,
										       metData, &genData);
    if (!fullHiggsMassData.passedEvent()) return true; // this is currently optional selection step, so we want to include events failing these cuts to be included in pickEvents.txt
    fCommonPlots.fillControlPlotsAfterAllSelectionsWithFullMass(iEvent, fullHiggsMassData);
    //double myHiggsMass = fullHiggsMassData.getHiggsMass();
    increment(fHiggsMassSelectionCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderSelectedEventsFullMass, tauData);
    fCommonPlotsSelectedFullMass->fill();
    if (mySelectedToEWKFakeTauBackgroundStatus) fCommonPlotsSelectedFullMassEWKFakeTausBkg->fill();


/*
//------ Experimental cuts, counters, and histograms
    if (!iEvent.isRealData()) {
      doMCAnalysisOfSelectedEvents(iEvent, tauData, vetoTauData, metData, genData);
    }
*/

   // transverse mass and inv mass with tau veto
    if (vetoTauData.passedEvent()) {
      increment(fTauVetoAfterDeltaPhiCounter);
      hTransverseMassTauVeto->Fill(transverseMass);
      //      hHiggsMassTauVeto->Fill(HiggsMass); 
    }


    /*

    // Calculate alphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(iEvent, iSetup, *(tauData.getSelectedTau()), jetData.getSelectedJetsIncludingTau());

    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());



    if (TopChiSelectionData.passedEvent() ) {
      double topmass = TopChiSelectionData.getTopMass();
      //      increment(fTopChiSelectionCounter);
      if (topmass < 250 ) increment(fTopChiSelection250Counter);
      if (topmass < 220 ) increment(fTopChiSelection220Counter);
      //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
      if (!(bBlindAnalysisStatus && iEvent.isRealData())) {
        hTransverseMassTopChiSelection->Fill(transverseMass, fEventWeight.getWeight());
      }
    } 




    if (BjetSelectionData.passedEvent() ) {
        
      TopWithBSelection::Data TopWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());
      TopWithWSelection::Data TopWithWSelectionData = fTopWithWSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());    
      if (TopWithBSelectionData.passedEvent() ) {
	//        increment(fTopWithBSelectionCounter);
	double topmass = TopWithBSelectionData.getTopMass();
	if (topmass < 250 ) increment(fTopWithBSelection250Counter);
	if (topmass < 220 ) increment(fTopWithBSelection220Counter);
        //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
        if (!(bBlindAnalysisStatus && iEvent.isRealData())) {
	  //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
	  hTransverseMassTopBjetSelection->Fill(transverseMass, fEventWeight.getWeight()); 
	  if(transverseMass > 70 ) increment(ftransverseMass70TopWithBSelCounter); 
	  if(transverseMass > 80 ) increment(ftransverseMass80TopWithBSelCounter);   
	}    
      }
      
      if (TopWithWSelectionData.passedEvent() ) {
	//        increment(fTopWithWSelectionCounter);
	double topmass = TopWithBSelectionData.getTopMass();
	if (topmass < 250 ) increment(fTopWithWSelection250Counter);
	if (topmass < 220 ) increment(fTopWithWSelection220Counter);
        //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
        if (!(bBlindAnalysisStatus && iEvent.isRealData())) {
	  //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
	  hTransverseMassTopWithWSelection->Fill(transverseMass, fEventWeight.getWeight()); 
	  if(transverseMass > 70 ) increment(ftransverseMass70TopWithWSelCounter); 
	  if(transverseMass > 80 ) increment(ftransverseMass80TopWithWSelCounter);   
	}    
      }
     
    }

    
*/
    /*

    // Fake MET veto a.k.a. further QCD suppression
    //    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup,  tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());
    if (fakeMETData.passedEvent() ) {
      increment(fFakeMETVetoCounter);
      fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, mySelectedToEWKFakeTauBackgroundStatus, kSignalOrderFakeMETVeto, tauData);
      hTransverseMassFakeMetVeto->Fill(transverseMass);
    }

    */

    // Correlation analysis
    fCorrelationAnalysis.analyze(iEvent, iSetup, tauData.getSelectedTaus(), btagData.getSelectedJets(),"BCorrelationAnalysis");
    // Alpha T
    //if(!evtTopologyData.passedEvent()) return false;
    hAlphaT->Fill(evtTopologyData.alphaT().fAlphaT); // FIXME: move this histogramming to evt topology

    // Forward jet veto
    //    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    //    if (!forwardJetData.passedEvent()) return false;
    //    increment(fForwardJetVetoCounter);

    //std::cout << "run=" << iEvent.id().run() << " lumiblock=" << iEvent.id().luminosityBlock() << " event=" << iEvent.id().event() << ", mT=" << transverseMass << std::endl;

    return true;
  }

  void SignalAnalysis::doTreeFilling(edm::Event& iEvent, const edm::EventSetup& iSetup, const VertexSelection::Data& pvData, const edm::Ptr<pat::Tau>& selectedTau, const ElectronSelection::Data& electronVetoData, const MuonSelection::Data& muonVetoData, const JetSelection::Data& jetData) {
    // MET
   
    METSelection::Data metData = fMETSelection.silentAnalyze(iEvent, iSetup, pvData.getNumberOfAllVertices(), selectedTau, jetData.getAllJets());
    // transverse mass
    //double transverseMass = TransverseMass::reconstruct(*(selectedTau), *(metData.getSelectedMET()) );
    // b tagging, no event cut
    BTagging::Data btagData = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets());

    // Top reco, no event cut 
    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());
    TopSelectionManager::Data TopSelectionData = fTopSelectionManager.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), BjetSelectionData.getBjetTopSide(), BjetSelectionData.passedEvent());
  
    // Calculate event topology variables (alphaT, sphericity, aplanarity etc..)
    EvtTopology::Data evtTopologyData = fEvtTopology.silentAnalyze(iEvent, iSetup, *(selectedTau), jetData.getSelectedJetsIncludingTau());
    
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.silentAnalyze(iEvent, iSetup, selectedTau, jetData.getSelectedJets(), metData.getSelectedMET());

    //------ Fill tree 
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
    fTree.setBTagging(btagData.passedEvent(), btagData.getScaleFactor(), btagData.getScaleFactorMaxAbsUncertainty());
    fTree.setTop(TopSelectionData.getTopP4());
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
    fTree.setDeltaPhi(fakeMETData.closestDeltaPhi());
    fTree.setNonIsoLeptons(muonVetoData.getNonIsolatedMuons(), electronVetoData.getNonIsolatedElectrons());
    if (btagData.passedEvent()) {
      // FullH+ mass
      FullHiggsMassCalculator::Data FullHiggsMassDataTmp = fFullHiggsMassCalculator.silentAnalyze(iEvent, iSetup, selectedTau, btagData, metData);
      if (FullHiggsMassDataTmp.passedEvent()) {
        fTree.setHplusMassDiscriminant(FullHiggsMassDataTmp.getDiscriminant());
        fTree.setHplusMassHiggsMass(FullHiggsMassDataTmp.getHiggsMass());
        fTree.setHplusMassTopMass(FullHiggsMassDataTmp.getTopMass());
        fTree.setHplusMassSelectedNeutrinoPzSolution(FullHiggsMassDataTmp.getSelectedNeutrinoPzSolution());
        fTree.setHplusMassNeutrinoPtSolution(FullHiggsMassDataTmp.getNeutrinoPtSolution());
        fTree.setHplusMassMCNeutrinoPz(FullHiggsMassDataTmp.getMCNeutrinoPz());
      }
    }

    fTree.fill(iEvent, selectedTau, jetData.getSelectedJets());
  }


  SignalAnalysis::CounterGroup* SignalAnalysis::getCounterGroupByTauMatch(FakeTauIdentifier::MCSelectedTauMatchType tauMatch) {
    if (tauMatch == FakeTauIdentifier::kkElectronToTau) return &fElectronToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkElectronFromTauDecayToTau) return &fElectronFromTauDecayToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkMuonToTau) return &fMuonToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkMuonFromTauDecayToTau) return &fMuonFromTauDecayToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkTauToTau) return &fGenuineToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkOneProngTauToTau) return &fGenuineToTausCounterGroup; // Handle separation in filling
    else if (tauMatch == FakeTauIdentifier::kkJetToTau) return &fJetToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkElectronToTauAndTauJetInsideAcceptance) return &fElectronToTausAndTauJetInsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkElectronFromTauDecayToTauAndTauJetInsideAcceptance) return &fElectronFromTauDecayToTausAndTauJetInsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkMuonToTauAndTauJetInsideAcceptance) return &fMuonToTausAndTauJetInsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkMuonFromTauDecayToTauAndTauJetInsideAcceptance) return &fMuonFromTauDecayToTausAndTauJetInsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkTauToTauAndTauJetInsideAcceptance) return &fGenuineToTausAndTauJetInsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkOneProngTauToTauAndTauJetInsideAcceptance) return &fGenuineToTausAndTauJetInsideAcceptanceCounterGroup; // Handle separation in filling
    else if (tauMatch == FakeTauIdentifier::kkJetToTauAndTauJetInsideAcceptance) return &fJetToTausAndTauJetInsideAcceptanceCounterGroup;
    return 0;
  }

  void SignalAnalysis::fillSelectionFlowAndCounterGroups(int nVertices, FakeTauIdentifier::Data& tauMatchData, bool selectedToEWKFakeTauBackgroundStatus, SignalSelectionOrder selection, const TauSelection::Data& tauData) {
    hSelectionFlow->Fill(selection);
    hSelectionFlowVsVertices->Fill(nVertices, selection);
    if (selectedToEWKFakeTauBackgroundStatus) {
      hSelectionFlowVsVerticesEWKFakeTausBkg->Fill(nVertices, selection);
      fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), selectedToEWKFakeTauBackgroundStatus, selection, tauData);
    }
  }

  void SignalAnalysis::fillEWKFakeTausCounters(FakeTauIdentifier::MCSelectedTauMatchType tauMatch, bool selectedToEWKFakeTauBackgroundStatus, HPlus::SignalAnalysis::SignalSelectionOrder selection, const HPlus::TauSelection::Data& tauData) {
    // Get out if no match has been found
    if (tauMatch == FakeTauIdentifier::kkNoMC) return;
    // Obtain status for main counter
    // Fill main and subcounter for the selection
    SignalAnalysis::CounterGroup* myCounterGroup = getCounterGroupByTauMatch(tauMatch);
    if (selection == kSignalOrderTauID) {
      if (selectedToEWKFakeTauBackgroundStatus) fEWKFakeTausGroup.incrementOneTauCounter();
      myCounterGroup->incrementOneTauCounter();
    } else if (selection == kSignalOrderMETSelection) {
      if (selectedToEWKFakeTauBackgroundStatus) fEWKFakeTausGroup.incrementMETCounter();
      myCounterGroup->incrementMETCounter();
    } else if (selection == kSignalOrderElectronVeto) {
      if (selectedToEWKFakeTauBackgroundStatus) fEWKFakeTausGroup.incrementElectronVetoCounter();
      myCounterGroup->incrementElectronVetoCounter();
    } else if (selection == kSignalOrderMuonVeto) {
      if (selectedToEWKFakeTauBackgroundStatus) fEWKFakeTausGroup.incrementMuonVetoCounter();
      myCounterGroup->incrementMuonVetoCounter();
    } else if (selection == kSignalOrderJetSelection) {
      if (selectedToEWKFakeTauBackgroundStatus) fEWKFakeTausGroup.incrementNJetsCounter();
      myCounterGroup->incrementNJetsCounter();
    } else if (selection == kSignalOrderBTagSelection) {
      if (selectedToEWKFakeTauBackgroundStatus) {
        fEWKFakeTausGroup.incrementBTaggingCounter();
        // Fill histograms
        hEWKFakeTausSelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt());
        hEWKFakeTausSelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta());
      }
      myCounterGroup->incrementBTaggingCounter();
    } else if (selection == kSignalOrderDeltaPhiBackToBackSelection) {
      if (selectedToEWKFakeTauBackgroundStatus) fEWKFakeTausGroup.incrementDeltaPhiBackToBackCounter();
      myCounterGroup->incrementDeltaPhiBackToBackCounter();
    } else if (selection == kSignalOrderFakeMETVeto) {
      if (selectedToEWKFakeTauBackgroundStatus) fEWKFakeTausGroup.incrementFakeMETVetoCounter();
      myCounterGroup->incrementFakeMETVetoCounter();
    } else if (selection == kSignalOrderTopSelection) {
      //if (selectedToEWKFakeTauBackgroundStatus) fEWKFakeTausGroup.incrementTopSelectionCounter();
      //myCounterGroup->incrementTopSelectionCounter();
    } else if (selection == kSignalOrderDeltaPhiCollinearSelection) {
      if (selectedToEWKFakeTauBackgroundStatus) fEWKFakeTausGroup.incrementDeltaPhiCollinearCounter();
      myCounterGroup->incrementDeltaPhiCollinearCounter();
    } else if (selection == kSignalOrderSelectedEvents) {
      if (selectedToEWKFakeTauBackgroundStatus) fEWKFakeTausGroup.incrementSelectedEventsCounter();
      myCounterGroup->incrementSelectedEventsCounter();
    } else if (selection == kSignalOrderSelectedEventsFullMass) {
      if (selectedToEWKFakeTauBackgroundStatus) fEWKFakeTausGroup.incrementSelectedEventsFullMassCounter();
      myCounterGroup->incrementSelectedEventsFullMassCounter();
    }
    // Check status for genuine one prong taus
    if (fFakeTauIdentifier.isGenuineOneProngTau(tauMatch)) {
      SignalAnalysis::CounterGroup* mySpecialGroup = &fGenuineOneProngToTausCounterGroup;
      if (tauMatch == FakeTauIdentifier::kkOneProngTauToTauAndTauJetInsideAcceptance) {
        mySpecialGroup = &fGenuineOneProngToTausAndTauJetInsideAcceptanceCounterGroup;
      }
      if (selection == kSignalOrderTauID) {
        mySpecialGroup->incrementOneTauCounter();
      } else if (selection == kSignalOrderElectronVeto) {
        mySpecialGroup->incrementElectronVetoCounter();
      } else if (selection == kSignalOrderMuonVeto) {
        mySpecialGroup->incrementMuonVetoCounter();
      } else if (selection == kSignalOrderJetSelection) {
        mySpecialGroup->incrementNJetsCounter();
      } else if (selection == kSignalOrderDeltaPhiCollinearSelection) {
        mySpecialGroup->incrementDeltaPhiCollinearCounter();
      } else if (selection == kSignalOrderMETSelection) {
        mySpecialGroup->incrementMETCounter();
      } else if (selection == kSignalOrderBTagSelection) {
        mySpecialGroup->incrementBTaggingCounter();
      } else if (selection == kSignalOrderDeltaPhiBackToBackSelection) {
        mySpecialGroup->incrementDeltaPhiBackToBackCounter();
      } else if (selection == kSignalOrderFakeMETVeto) {
        mySpecialGroup->incrementFakeMETVetoCounter();
      } else if (selection == kSignalOrderTopSelection) {
        //mySpecialGroup->incrementTopSelectionCounter();
      } else if (selection == kSignalOrderSelectedEvents) {
        mySpecialGroup->incrementSelectedEventsCounter();
      } else if (selection == kSignalOrderSelectedEventsFullMass) {
        mySpecialGroup->incrementSelectedEventsFullMassCounter();
      }
    }
  }

  bool SignalAnalysis::selectTailEvents(edm::Event& iEvent, const edm::EventSetup& iSetup, const VertexSelection::Data& pvData) {
    TauSelection::Data tauData = fTauSelection.silentAnalyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
    if (!tauData.passedEvent()) return false; // Require at least one tau
    JetSelection::Data jetData = fJetSelection.silentAnalyze(iEvent, iSetup, tauData.getSelectedTau(), 0);
    if (jetData.getHadronicJetCount() == 0) return false;
    METSelection::Data metData = fMETSelection.silentAnalyze(iEvent, iSetup, pvData.getNumberOfAllVertices(), tauData.getSelectedTau(), jetData.getAllJets());
    if (!(metData.getSelectedMET()->et() > 30)) return false;

    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()));
    if (deltaPhi < 90) return false;
    if (transverseMass < 80) return false;
    return true;
  }

}
