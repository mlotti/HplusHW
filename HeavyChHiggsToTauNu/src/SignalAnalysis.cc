#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"

// #include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventClassification.h"

#include "TLorentzVector.h"

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TNamed.h"

bool  hasImmediateMother(const reco::Candidate& p, int id);
bool  hasImmediateDaughter(const reco::Candidate& p, int id);
void  printImmediateMothers(const reco::Candidate& p);
void  printImmediateDaughters(const reco::Candidate& p);
std::vector<const reco::GenParticle*>   getMothers(const reco::Candidate& p);

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
    fTopSelectionCounter(eventCounter.addCounter("EWKfaketaus:Top Selection cut")),
    fTopChiSelectionCounter(eventCounter.addCounter("EWKfaketaus:Top Chi Selection cut")),
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
    fTopSelectionCounter(eventCounter.addSubCounter(prefix,":Top Selection cut")),
    fTopChiSelectionCounter(eventCounter.addSubCounter(prefix,":Top Chi Selection cut")),
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
    fWJetsWeightCounter(eventCounter.addCounter("WJets inc+exl weight")),
    fMETFiltersCounter(eventCounter.addCounter("MET filters")),
    fEmbeddingMuonEfficiencyCounter(eventCounter.addCounter("Embedding: muon eff weight")),
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
    fQCDTailKillerBackToBackCounter(eventCounter.addCounter("QCD tail killer back-to-back")),
    fTopReconstructionCounter(eventCounter.addCounter("Top reconstruction")),
    fSelectedEventsCounter(eventCounter.addCounter("Selected events")),
    fHiggsMassSelectionCounter(eventCounter.addCounter("HiggsMassSelection")),
    fFakeMETVetoCounter(eventCounter.addCounter("FakeMETVeto")),

    fTauVetoAfterDeltaPhiCounter(eventCounter.addCounter("TauVeto after DeltaPhi cut")),
    fRealTauAfterDeltaPhiCounter(eventCounter.addCounter("Real tau after deltaPhi cut")),
    fRealTauAfterDeltaPhiTauVetoCounter(eventCounter.addCounter("Real tau after deltaPhi+tauveto cut")),

    fElectronNotInTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Electron not in tau")),
    fElectronNotInTauFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "W->Electron not in tau")),
    fElectronNotInTauFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Bottom->Electron not in tau")),
    fElectronNotInTauFromTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau->Electron not in tau")),

    fMuonNotInTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Muon not in tau")),
    fMuonNotInTauFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "W->Muon not in tau")),
    fMuonNotInTauFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Bottom->Muon not in tau")),
    fMuonNotInTauFromTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau->Muon not in tau")),

    fTauNotInTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau not in tau")),
    fTauNotInTauFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "W->Tau not in tau")),
    fTauNotInTauFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Bottom->Tau not in tau")),
    fTauNotInTauFromHplusCounter(eventCounter.addSubCounter("MCinfo for selected events", "Hplus->tau not in tau")),

    fObservableMuonsCounter(eventCounter.addSubCounter("MCinfo for selected events", "Observable associated muons")),
    fObservableElectronsCounter(eventCounter.addSubCounter("MCinfo for selected events", "Observable associated electrons")),
    fObservableTausCounter(eventCounter.addSubCounter("MCinfo for selected events", "Observable associated taus")),

    fTauIsHadronFromHplusCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from H+ ->tau->hadrons")),
    fTauIsElectronFromHplusCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from H+ ->tau->electron")),
    fTauIsMuonFromHplusCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from H+ ->tau->muon")),
    fTauIsQuarkFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->qq")),
    fTauIsQuarkFromZCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->qq")),
    fTauIsElectronFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->e")),
    fTauIsElectronFromZCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->e")),
    fTauIsMuonFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->mu")),
    fTauIsHadronFromWTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->tau->hadrons")),
    fTauIsElectronFromWTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->tau->e")),
    fTauIsMuonFromWTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->tau->mu")),
    fTauIsMuonFromZCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->mu")),
    fTauIsHadronFromZTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->tau->hadrons")),
    fTauIsElectronFromZTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->tau->e")),
    fTauIsMuonFromZTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from Z->tau->mu")),
    fTauIsElectronFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from top->bottom->e")),
    fTauIsMuonFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from top->bottom->mu")),
    fTauIsHadronFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from top->bottom->hadron")),
    fTauIsElectronFromJetCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from jet->e")),
    fTauIsMuonFromJetCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from jet->mu")),
    fTauIsHadronFromJetCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from jet->hadron")),
    // Counters for different top algorithms
    fTopSelectionCounter(eventCounter.addSubCounter("top", "Top selection")),
    fTopChiSelectionCounter(eventCounter.addSubCounter("top", "Top Chi Selection")),
    fTopWithMHSelectionCounter(eventCounter.addCounter("Top after Inv Mass selection")),
    fTopWithBSelectionCounter(eventCounter.addSubCounter("top", "Top with B Selection")),
    fTopWithWSelectionCounter(eventCounter.addSubCounter("top", "Top with W Selection")),

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
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, fHistoWrapper),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, fHistoWrapper),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, fHistoWrapper),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, fHistoWrapper),
    fTopWithWSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithWSelection"), eventCounter, fHistoWrapper),
    //    fTopWithMHSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithMHSelection"), eventCounter, fHistoWrapper),
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, fHistoWrapper),

    //   ftransverseMassCut(iConfig.getUntrackedParameter<edm::ParameterSet>("transverseMassCut")),
    fFullHiggsMassCalculator(iConfig.getUntrackedParameter<edm::ParameterSet>("invMassReco"), eventCounter, fHistoWrapper),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, fHistoWrapper),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, fHistoWrapper),
    fCorrelationAnalysis(eventCounter, fHistoWrapper, "HistoName"),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, fHistoWrapper),
    fTauTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("tauTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fMETTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("metTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fEmbeddingMuonEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("embeddingMuonEfficiency")),
    fPrescaleWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("prescaleWeightReader"), fHistoWrapper, "PrescaleWeight"),
    fPileupWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("pileupWeightReader"), fHistoWrapper, "PileupWeight"),
    fWJetsWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("wjetsWeightReader"), fHistoWrapper, "WJetsWeight"),
    fVertexAssignmentAnalysis(iConfig, eventCounter, fHistoWrapper),
    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), fHistoWrapper, "TauID"),
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
    fAllTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "All with tau outside acceptance"),
    fElectronToTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "e->tau with tau outside acceptance"),
    fElectronFromTauDecayToTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "tau_e->tau with tau outside acceptance"),
    fMuonToTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "mu->tau with tau outside acceptance"),
    fMuonFromTauDecayToTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "tau_mu->tau with tau outside acceptance"),
    fGenuineToTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "tau->tau with tau outside acceptance"),
    fGenuineOneProngToTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "1-prong tau->tau with tau outside acceptance"),
    fJetToTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "jet->tau with tau outside acceptance"),
    fModuleLabel(iConfig.getParameter<std::string>("@module_label")),
    fProduce(iConfig.getUntrackedParameter<bool>("produceCollections", false)),
    fOnlyGenuineTaus(iConfig.getUntrackedParameter<bool>("onlyGenuineTaus", false)),
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
    fCommonPlotsSelected(fCommonPlots.createCommonPlotsFilledAtEveryStep("Selected",true,"Selected")),
    fCommonPlotsSelectedMtTail(fCommonPlots.createCommonPlotsFilledAtEveryStep("SelectedMtTail",false,"SelectedMtTail")),
    fCommonPlotsSelectedFullMass(fCommonPlots.createCommonPlotsFilledAtEveryStep("SelectedFullMass",false,"SelectedFullMass")),
    fCommonPlotsAfterTauSelectionFakeTaus(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_TauSelection",false,"TauID")),
    fCommonPlotsAfterTauWeightFakeTaus(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_TauWeight",false,"Tau")),
    fCommonPlotsAfterElectronVetoFakeTaus(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_ElectronVeto",false,"e veto")),
    fCommonPlotsAfterMuonVetoFakeTaus(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_MuonVeto",false,"#mu veto")),
    fCommonPlotsAfterJetSelectionFakeTaus(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_JetSelection",false,"#geq3j")),
    fCommonPlotsAfterMETFakeTaus(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_MET",false,"E_{T}^{miss}")),
    fCommonPlotsAfterBTaggingFakeTaus(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_BTagging",false,"#geq1b tag")),
    fCommonPlotsSelectedFakeTaus(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_Selected",false,"Selected")),
    fCommonPlotsSelectedMtTailFakeTaus(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_SelectedMtTail",false,"SelectedMtTail")),
    fCommonPlotsSelectedFullMassFakeTaus(fCommonPlots.createCommonPlotsFilledAtEveryStep("FakeTaus_SelectedFullMass",false,"FakeTaus_SelectedFullMass"))
  {
    // Check parameter initialisation
    if (fTopRecoName != "None" && fTopRecoName != "chi" && fTopRecoName != "std" && fTopRecoName != "Wselection") {
      throw cms::Exception("config") << "selected topReconstruction is invalid! Valid options are: None, chi, std, Wselection";
    }

    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms filled in the analysis body
    
    // Vertex histograms
    TFileDirectory myVertexDir = fs->mkdir("Vertices");
    hVerticesBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myVertexDir, "verticesBeforeWeight", "Number of vertices without weighting", 40, 0, 40);
    hVerticesAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myVertexDir, "verticesAfterWeight", "Number of vertices with weighting", 40, 0, 40);

    // MET histograms

    hGenMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "genMET", "genMET", 200, 0., 400.);
    hdeltaPhiMetGenMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "deltaPhiMetGenMet", "deltaPhiMetGenMet", 180, 0., 180.); 
    hdeltaEtMetGenMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "deltaEtMetGenMet", "deltaEtMetGenMet", 200, -1., 1.);
    hgenWmass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "genWmass", "genWmass", 200, 0.,400.); 
    htransverseMassMuonNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassMuonNotInTau", "transverseMassMuonNotInTau;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    htransverseMassElectronNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassElectronNotInTau", "transverseMassElectronNotInTau;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    htransverseMassTauNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTauNotInTau", "transverseMassTauNotInTau;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    htransverseMassMetReso02 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassMetReso02", "transverseMassMetReso02;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    htransverseMassLeptonNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassLeptonNotInTau", "transverseMassLeptonNotInTau", 200, 0., 400.);
    htransverseMassNoLeptonNotInTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassNoLeptonNotInTau", "transverseMassNoLeptonNotInTau", 200, 0., 400.);
    htransverseMassLeptonRealSignalTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassLeptonRealSignalTau", "transverseMassLeptonRealSignalTau", 200, 0., 400.);
    htransverseMassLeptonFakeSignalTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassLeptonFakeSignalTau", "transverseMassLeptonFakeSignalTau", 200, 0., 400.);
    htransverseMassNoLeptonGoodMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassNoLeptonGoodMet", "transverseMassNoLeptonGoodMet", 200, 0., 400.);
    htransverseMassNoLeptonGoodMetGoodTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassNoLeptonGoodMetGoodTau", "transverseMassNoLeptonGoodMetGoodTau", 200, 0., 400.);
    htransverseMassNoObservableLeptons= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseNoMassObservableLeptons", "transverseMassNoObservableLeptons", 200, 0., 400.);
    htransverseMassObservableLeptons= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassObservableLeptons", "transverseMassObservableLeptons", 200, 0., 400.);


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

    hSelectionFlow = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SignalSelectionFlow", "SignalSelectionFlow;;N_{events}", 15, 0, 15);
    hSelectionFlowVsVertices = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "SignalSelectionFlowVsVertices", "SignalSelectionFlowVsVertices;N_{vertices};Step", 50, 0, 50, 15, 0, 15);
    hSelectionFlowVsVerticesFakeTaus = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "SignalSelectionFlowVsVerticesFakeTaus", "SignalSelectionFlowVsVerticesFakeTaus;N_{vertices};Step", 50, 0, 50, 15, 0, 15);
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
        hSelectionFlowVsVerticesFakeTaus->getHisto()->GetYaxis()->SetBinLabel(i+1, hSelectionFlow->getHisto()->GetXaxis()->GetBinLabel(i+1));
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

//------ For combining W+Jets inclusive and exclusive samples, do an event weighting here
    if(!iEvent.isRealData()) {
      const double wjetsWeight = fWJetsWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(wjetsWeight);
      fTree.setWjetsWeight(wjetsWeight);
    }
    increment(fWJetsWeightCounter);

//------ MET (noise) filters for data (reject events with instrumental fake MET)
    if(iEvent.isRealData()) {
      if(!fMETFilters.passedEvent(iEvent, iSetup)) return false;
    }
    increment(fMETFiltersCounter);

//------ For embedding, apply the muon ID efficiency at this stage
    EmbeddingMuonEfficiency::Data embeddingMuonData;
    if(bTauEmbeddingStatus) {
      embeddingMuonData = fEmbeddingMuonEfficiency.getEventWeight(iEvent);
      fEventWeight.multiplyWeight(embeddingMuonData.getEventWeight());
    }
    increment(fEmbeddingMuonEfficiencyCounter);

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
    fCommonPlots.initialize(iEvent, iSetup, pvData, fTauSelection, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETSelection, fBTagging, fQCDTailKiller, fTopChiSelection, fEvtTopology, fFullHiggsMassCalculator);
    fCommonPlotsAfterVertexSelection->fill();
    fCommonPlots.fillControlPlotsAfterVertexSelection(iEvent, pvData);

//------ Apply filter (if chosen) to select tail events
    //if (!selectTailEvents(iEvent, iSetup, pvData)) return false;


//------ TauID
    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
    fTauSelection.analyseFakeTauComposition(fFakeTauIdentifier,iEvent);
    if(!tauData.passedEvent()) return false; // Require at least one tau
    //    std::cout << "taus  " << tauData.getSelectedTaus().size() << std::endl;

    // Obtain MC matching - for EWK without genuine taus
    FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, *(tauData.getSelectedTau()));
    bool myFakeTauStatus = fFakeTauIdentifier.isFakeTau(tauMatchData.getTauMatchType()); // True if the selected tau is a fake
    fCommonPlotsAfterTauSelection->fill();
    fCommonPlots.fillControlPlotsAfterTauSelection(iEvent, iSetup, tauData, tauMatchData, fMETSelection);
    fTree.setTauIsFake(myFakeTauStatus);
    if (myFakeTauStatus) fCommonPlotsAfterTauSelectionFakeTaus->fill();
    // Below "genuine tau" is in the context of embedding (i.e. irrespective of the tau decay)
    if(fOnlyGenuineTaus && !fFakeTauIdentifier.isEmbeddingGenuineTau(tauMatchData.getTauMatchType())) return false;
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
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderTauID, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Tau> > saveTaus(new std::vector<pat::Tau>());
      copyPtrToVector(tauData.getSelectedTaus(), *saveTaus);
      iEvent.put(saveTaus, "selectedTaus");
    }
    fCommonPlotsAfterTauWeight->fill();
    if (myFakeTauStatus) fCommonPlotsAfterTauWeightFakeTaus->fill();
    fCommonPlots.fillControlPlotsAfterTauTriggerScaleFactor(iEvent);
    //    hSelectedTauRtau->Fill(tauData.getRtauOfSelectedTau());  
    if (!myFakeTauStatus)
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
    if (myFakeTauStatus) fCommonPlotsAfterElectronVetoFakeTaus->fill();
    increment(fElectronVetoCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderElectronVeto, tauData);
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
    if (myFakeTauStatus) fCommonPlotsAfterMuonVetoFakeTaus->fill();
    increment(fMuonVetoCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderMuonVeto, tauData);
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
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderJetSelection, tauData);
    fCommonPlotsAfterJetSelection->fill();
    if (myFakeTauStatus) fCommonPlotsAfterJetSelectionFakeTaus->fill();
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
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderDeltaPhiCollinearSelection, tauData);


//------ Fill TTree, if it is active
    if (fTree.isActive()) {
      doTreeFilling(iEvent, iSetup, pvData, tauData.getSelectedTau(), electronVetoData, muonVetoData, jetData);
      //return true;
    }


//------ MET cut
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, nVertices, tauData.getSelectedTau(), jetData.getAllJets());
    fCommonPlots.fillControlPlotsAtMETSelection(iEvent, metData);
    // Obtain delta phi and transverse mass here, but do not yet cut on them
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()));
    BTagging::Data btagData = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    if (transverseMass > 40 && transverseMass < 100)
      hCtrlJetMatrixAfterJetSelection->Fill(jetData.getHadronicJetCount(), btagData.getBJetCount());
    // Now cut on MET
    if (metData.getPhiCorrectedSelectedMET()->et() > 50.0) fCommonPlotsAfterMETWithPhiOscillationCorrection->fill(); // FIXME: temp
    if(!metData.passedEvent()) return false;
    fCommonPlotsAfterMET->fill();
    if (myFakeTauStatus) fCommonPlotsAfterMETFakeTaus->fill();
    increment(fMETCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderMETSelection, tauData);

    // Plot jet matrix
    if (transverseMass > 40 && transverseMass < 100) {
      hCtrlJetMatrixAfterMET->Fill(jetData.getHadronicJetCount(), btagData.getBJetCount());
      if (metData.getSelectedMET()->et() > 100.0)
        hCtrlJetMatrixAfterMET100->Fill(jetData.getHadronicJetCount(), btagData.getBJetCount());

    }


//------ b tagging cut

//    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
    btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    if(btagData.passedEvent())
      increment(fBTaggingCounter);
    // Apply scale factor as weight to event
    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
    fCommonPlots.fillControlPlotsAtBtagging(iEvent, btagData);
    if(!btagData.passedEvent()) return false;
    increment(fBTaggingScaleFactorCounter);
    fCommonPlotsAfterBTagging->fill();
    if (myFakeTauStatus) fCommonPlotsAfterBTaggingFakeTaus->fill();

   
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderBTagSelection, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveBJets(new std::vector<pat::Jet>());
      copyPtrToVector(btagData.getSelectedJets(), *saveBJets);
      iEvent.put(saveBJets, "selectedBJets");
    }


//------ Improved delta phi cut, a.k.a. QCD tail killer, back-to-back part
//------ Improved delta phi cut, a.k.a. QCD tail killer // FIXME: place of cut still to be determined
    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    fCommonPlots.fillControlPlotsAtBackToBackDeltaPhiCuts(iEvent, qcdTailKillerData);
    if (!qcdTailKillerData.passedBackToBackCuts()) return false;
    increment(fQCDTailKillerBackToBackCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderDeltaPhiBackToBackSelection, tauData);


//------ Delta phi(tau,MET) after delta phi cuts
    hDeltaPhi->Fill(deltaPhi);
    if (myFakeTauStatus) hEWKFakeTausDeltaPhi->Fill(deltaPhi);

//------ Top reconstruction

    // Top reco, no event cut

   // top mass with possible event cuts
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    if (TopSelectionData.passedEvent() ) {
      increment(fTopSelectionCounter);
      hTransverseMassTopSelection->Fill(transverseMass);
    }

    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    if (TopChiSelectionData.passedEvent() ) {
      increment(fTopChiSelectionCounter);
      hTransverseMassTopChiSelection->Fill(transverseMass);
    }

    bool myTopRecoWithWSelectionStatus = false;
    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());
    if (BjetSelectionData.passedEvent() ) {
      TopWithBSelection::Data TopWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());
      if (TopWithBSelectionData.passedEvent() ) {
        increment(fTopWithBSelectionCounter);
        hTransverseMassTopBjetSelection->Fill(transverseMass);
      }
      TopWithWSelection::Data TopWithWSelectionData = fTopWithWSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());
      if (TopWithWSelectionData.passedEvent() ) {
        myTopRecoWithWSelectionStatus = true;
        increment(fTopWithWSelectionCounter);
        hTransverseMassTopWithWSelection->Fill(transverseMass);
      }
    }
    // Select events depending on top resonctruction
    bool myPassedTopRecoStatus = false;
    if (fTopRecoName == "None")
      myPassedTopRecoStatus = true;
    else if (fTopRecoName == "std")
      myPassedTopRecoStatus = TopSelectionData.passedEvent();
    else if (fTopRecoName == "chi")
      myPassedTopRecoStatus = TopChiSelectionData.passedEvent();
    else if (fTopRecoName == "Wselection")
      myPassedTopRecoStatus = myTopRecoWithWSelectionStatus;
    fCommonPlots.fillControlPlotsAtTopSelection(iEvent, TopChiSelectionData);
    if (!myPassedTopRecoStatus)
      return false;
    increment(fTopReconstructionCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderTopSelection, tauData);


//------ Calculate alphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(iEvent, iSetup, *(tauData.getSelectedTau()), jetData.getSelectedJetsIncludingTau());
    fCommonPlots.fillControlPlotsAtEvtTopology(iEvent, evtTopologyData);


//------ Transverse mass and control plots
    fCommonPlots.fillControlPlotsAfterAllSelections(iEvent, transverseMass);
    increment(fSelectedEventsCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderSelectedEvents, tauData);
    if (btagData.hasGenuineBJets()) increment(fSelectedEventsCounterWithGenuineBjets);
    hTransverseMassVsNjets->Fill(transverseMass, jetData.getHadronicJetCount());
    fCommonPlotsSelected->fill();
    if (myFakeTauStatus) fCommonPlotsSelectedFakeTaus->fill();
    if (transverseMass > 120) {
      fCommonPlotsSelectedMtTail->fill();
      if (myFakeTauStatus) fCommonPlotsSelectedMtTailFakeTaus->fill();
    }

    hSelectedTauRtauAfterCuts->Fill(tauData.getSelectedTauRtauValue());
    hSelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt());
    hSelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta());


//------ Syst. uncertainties handling FIXME: to be phased out
    fSFUncertaintiesAfterSelection.setScaleFactorUncertainties(myFakeTauStatus,
                                                            fEventWeight.getWeight(),
                                                            fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauData.getSelectedTau()->eta()),
                                                            fFakeTauIdentifier.getFakeTauSystematics(tauMatchData.getTauMatchType(), tauData.getSelectedTau()->eta()),
                                                            btagData.getScaleFactor(), btagData.getScaleFactorAbsoluteUncertainty());
    fSFUncertaintiesAfterSelection.setTauTriggerScaleFactorUncertainty(fEventWeight.getWeight(),
                                                                       tauTriggerWeight.getEventWeight(),
                                                                       tauTriggerWeight.getEventWeightAbsoluteUncertainty());
    fSFUncertaintiesAfterSelection.setMETTriggerScaleFactorUncertainty(fEventWeight.getWeight(),
                                                                       metTriggerWeight.getEventWeight(),
                                                                       metTriggerWeight.getEventWeightAbsoluteUncertainty());

    if(bTauEmbeddingStatus)
      fSFUncertaintiesAfterSelection.setEmbeddingMuonEfficiencyUncertainty(fEventWeight.getWeight(),
                                                                           embeddingMuonData.getEventWeight(),
                                                                           embeddingMuonData.getEventWeightAbsoluteUncertainty());

    if (myFakeTauStatus) {
      hEWKFakeTausTransverseMassVsNjets->Fill(transverseMass, jetData.getHadronicJetCount());
      fEWKFakeTausSFUncertaintiesAfterSelection.setScaleFactorUncertainties(myFakeTauStatus,
                                                                            fEventWeight.getWeight(),
                                                                            fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauData.getSelectedTau()->eta()),
                                                                            fFakeTauIdentifier.getFakeTauSystematics(tauMatchData.getTauMatchType(), tauData.getSelectedTau()->eta()),
                                                                            btagData.getScaleFactor(), btagData.getScaleFactorAbsoluteUncertainty());
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
    if (!fullHiggsMassData.passedEvent()) return false;
    fCommonPlots.fillControlPlotsAfterAllSelectionsWithFullMass(iEvent, fullHiggsMassData);
    //double myHiggsMass = fullHiggsMassData.getHiggsMass();
    increment(fHiggsMassSelectionCounter);
    fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderSelectedEventsFullMass, tauData);
    fCommonPlotsSelectedFullMass->fill();
    if (myFakeTauStatus) fCommonPlotsSelectedFullMassFakeTaus->fill();


//------ Experimental cuts, counters, and histograms
    if (!iEvent.isRealData()) {
      doMCAnalysisOfSelectedEvents(iEvent, tauData, vetoTauData, metData, genData);
    }

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
      fillSelectionFlowAndCounterGroups(nVertices, tauMatchData, kSignalOrderFakeMETVeto, tauData);
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
   
    TopSelection::Data TopSelectionData = fTopSelection.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    BjetSelection::Data BjetSelectionData = fBjetSelection.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), selectedTau, metData.getSelectedMET());

    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.silentAnalyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
  
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
    fTree.setBTagging(btagData.passedEvent(), btagData.getScaleFactor(), btagData.getScaleFactorAbsoluteUncertainty());
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

  // FIXME: Move as its own class
  void SignalAnalysis::doMCAnalysisOfSelectedEvents(edm::Event& iEvent, const TauSelection::Data& tauData, const VetoTauSelection::Data& vetoTauData, const METSelection::Data& metData, const GenParticleAnalysis::Data& genData) {
    if (iEvent.isRealData() || !genData.isValid()) return;

    // Origin and type of selected tau
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);

    typedef math::XYZTLorentzVectorD LorentzVector;
    typedef std::vector<LorentzVector> LorentzVectorCollection;


    edm::Handle <std::vector<LorentzVector> > oneProngTaus;
    iEvent.getByLabel(fOneProngTauSrc, oneProngTaus); // FIXME: fOneProngTauSrc is not initialized!

    edm::Handle <std::vector<LorentzVector> > oneAndThreeProngTaus;
    iEvent.getByLabel(fOneAndThreeProngTauSrc,oneAndThreeProngTaus);

    edm::Handle <std::vector<LorentzVector> > threeProngTaus;
    iEvent.getByLabel(fThreeProngTauSrc, threeProngTaus); // FIXME: fThreeProngTauSrc is not initialized!

    bool myTauFoundStatus = false;
    bool myLeptonVetoStatus = false;
    bool otherTauFound = false;
    bool electronFound = false;
    bool muonFound = false;
    bool observableOtherTauFound = false;
    bool observableElectronFound = false;
    bool observableMuonFound = false;
    bool electronFromBottomFound = false;
    bool electronFromWFound  = false;
    bool electronFromTauFound  = false;
    bool muonFromBottomFound = false;
    bool muonFromWFound  = false;
    bool muonFromTauFound  = false;
    bool tauFromWFound  = false;

    hGenMET->Fill(genData.getGenMET()->pt());
    double deltaPhiMetGenMet = DeltaPhi::reconstruct(*(genData.getGenMET()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    hdeltaPhiMetGenMet->Fill(deltaPhiMetGenMet);
    hdeltaEtMetGenMet->Fill((genData.getGenMET()->pt() - metData.getSelectedMET()->pt())/genData.getGenMET()->pt());

    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()));
    if ((fabs(genData.getGenMET()->pt() - metData.getSelectedMET()->pt())/genData.getGenMET()->pt()) > 0.2) {
      htransverseMassMetReso02->Fill(transverseMass);
    }

    
    reco::GenParticle parton;
    reco::GenParticle otherTau;
    reco::GenParticle electron;
    reco::GenParticle muon;

    double minDeltaR = 99999;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      //      std::cout << "p.pdgId() " <<  p.pdgId() << " atatus " << p.status() << std::endl;
      //      if (p.pt() > 5 && p.pdgId()!= std::abs(p.pdgId()) ) {
      if (p.pt() > 5 ) {
        if (reco::deltaR(p, tauData.getSelectedTau()->leadPFChargedHadrCand()->p4()) < 0.3) {
          if (std::abs(p.pdgId()) == 15) myTauFoundStatus = true;
        }
	if (reco::deltaR(p, tauData.getSelectedTau()->leadPFChargedHadrCand()->p4()) > 0.5 ) {

	  // non-signal taus
          if (std::abs(p.pdgId()) == 15 && !hasImmediateMother(p,15) && !hasImmediateMother(p,-15) ) {
	    // hadronic taus
	    for( LorentzVectorCollection::const_iterator tau = oneAndThreeProngTaus->begin();tau!=oneAndThreeProngTaus->end();++tau) {
	      double deltaR = ROOT::Math::VectorUtil::DeltaR( p.p4() ,*tau );
	      if ( deltaR > 0.3) continue;
	      // if (hasImmediateDaughter(p,11) || !hasImmediateDaughter(p,-13) ) continue;	
	      increment(fTauNotInTauCounter);
	      otherTau = (*genParticles)[i]; 
	      otherTauFound = true;
	      std::vector<const reco::GenParticle*> tauMothers = getMothers(otherTau); 
	      for(size_t d=0; d< tauMothers.size(); ++d) {
		const reco::GenParticle dparticle = *tauMothers[d];
		//		if (dparticle.status() == 2) {
		  if( abs(dparticle.pdgId()) == 24 ) {
		    tauFromWFound = true;
		    increment(fTauNotInTauFromWCounter);
		  }
		  //		if( abs(dparticle.pdgId()) == 24 ) std::cout << " W mass " << dparticle.mass() << std::endl;
		  if( abs(dparticle.pdgId()) == 24 ) hgenWmass->Fill(dparticle.mass());
		  if( abs(dparticle.pdgId()) == 5 ) increment(fTauNotInTauFromBottomCounter);
		  if( abs(dparticle.pdgId()) == 37 ) increment(fTauNotInTauFromHplusCounter); 	
		}
	      //	      }
	      if ( tau->pt() < 15 || fabs(tau->eta()) > 2.4 ) continue;
	      increment(fObservableTausCounter);
	      observableOtherTauFound = true;
	    }
	  }


	  // electrons 
          if (std::abs(p.pdgId()) == 11 && !hasImmediateMother(p,11) && !hasImmediateMother(p,-11)) {
	    increment(fElectronNotInTauCounter);
	    electronFound = true;
	    electron = (*genParticles)[i]; 
	    std::vector<const reco::GenParticle*> electronMothers = getMothers(electron); 
	    for(size_t d=0; d<electronMothers.size(); ++d) {
	      const reco::GenParticle dparticle = *electronMothers[d];
	      //	      if (dparticle.status() == 2) {
		if( abs(dparticle.pdgId()) == 24 ) {
		  electronFromWFound = true;
		  increment(fElectronNotInTauFromWCounter);
		}
		if( abs(dparticle.pdgId()) == 5 ) {
		  electronFromBottomFound = true;
		  increment(fElectronNotInTauFromBottomCounter);
		}
		if( abs(dparticle.pdgId()) == 15 ) {
		  electronFromTauFound = true;
		  increment(fElectronNotInTauFromTauCounter); 
		}	
		
		//	      }
	      if ( p.pt() < 15 || fabs(p.eta()) > 2.4 ) continue;
	      increment(fObservableElectronsCounter);
	      observableElectronFound = true;
	    }
	  }
	  // muons
          if (std::abs(p.pdgId()) == 13 && !hasImmediateMother(p,13) && !hasImmediateMother(p,-13) ) {
	    increment(fMuonNotInTauCounter);
	    muonFound = true;
	    muon = (*genParticles)[i];
	    std::vector<const reco::GenParticle*> muonMothers = getMothers(muon);
	    
	    for(size_t d=0; d< muonMothers.size(); ++d) {
	      const reco::GenParticle dparticle = *muonMothers[d];
	      if (dparticle.status() == 2) {
		//	      std::cout << "dparticle.pdgId() " <<  dparticle.pdgId() << " atatus " << dparticle.status() << std::endl;
		//		if( abs(dparticle.pdgId()) == 24 ) {
		  muonFromWFound = true;
		  increment(fMuonNotInTauFromWCounter);
		}
		if( abs(dparticle.pdgId()) == 5 ) {
		  muonFromBottomFound = true;
		  increment(fMuonNotInTauFromBottomCounter);
		}
		if( abs(dparticle.pdgId()) == 15 ) {
		  muonFromTauFound = true;
		  increment(fMuonNotInTauFromTauCounter); 
		}	
	      }
	    //	    }
	    if ( p.pt() < 15 || fabs(p.eta()) > 2.4 ) continue;
	    increment(fObservableMuonsCounter);
	    observableMuonFound = true;
	  }
	}
	
        double deltaR = reco::deltaR(p, tauData.getSelectedTau()->leadPFChargedHadrCand()->p4());
        if (deltaR < minDeltaR) {
          minDeltaR = deltaR;
          parton = (*genParticles)[i];
        }
      }
    }
  
    // origin of leptons (not in tau)
    if (electronFound) {
      //      increment(fElectronNotInTauCounter);
      htransverseMassElectronNotInTau->Fill(transverseMass);
    }

    if (muonFound) {
      //      increment(fMuonNotInTauCounter);
      htransverseMassMuonNotInTau->Fill(transverseMass);
    }

    if (otherTauFound) {
      //      increment(fTauNotInTauCounter);
      htransverseMassTauNotInTau->Fill(transverseMass);
    }

    if (otherTauFound  ) {
      htransverseMassTauFound->Fill(transverseMass);
      if(tauFromWFound) htransverseMassTauFromWFound->Fill(transverseMass);
    }
    if ( electronFound  ) {
      htransverseMassElectronFound->Fill(transverseMass);
      if(electronFromWFound) htransverseMassElectronFromWFound->Fill(transverseMass);
      if(electronFromBottomFound) htransverseMassElectronFromBottomFound->Fill(transverseMass);
      if(electronFromTauFound) htransverseMassElectronFromTauFound->Fill(transverseMass);
    }
    if ( muonFound  ) {
      htransverseMassMuonFound->Fill(transverseMass);
      if(muonFromWFound) htransverseMassMuonFromWFound->Fill(transverseMass);
      if(muonFromBottomFound) htransverseMassMuonFromBottomFound->Fill(transverseMass);
      if(muonFromTauFound) htransverseMassMuonFromTauFound->Fill(transverseMass);
    }


    if (otherTauFound || electronFound || muonFound ) {
      //      increment(fTauNotInTauCounter);
      htransverseMassLeptonNotInTau->Fill(transverseMass);
      if (myTauFoundStatus ) htransverseMassLeptonRealSignalTau->Fill(transverseMass);
      if (!myTauFoundStatus ) htransverseMassLeptonFakeSignalTau->Fill(transverseMass); 
    }

    if (!otherTauFound && !electronFound && !muonFound ) {
      //      increment(fTauNotInTauCounter);
      htransverseMassNoLeptonNotInTau->Fill(transverseMass);
      if (myTauFoundStatus ) htransverseMassNoLeptonGoodMet->Fill(transverseMass);
      if (!myTauFoundStatus ) htransverseMassNoLeptonGoodMetGoodTau->Fill(transverseMass); 
    }

    if (observableOtherTauFound || observableElectronFound || observableMuonFound ) {
      //      increment(fTauNotInTauCounter);
      htransverseMassObservableLeptons->Fill(transverseMass);
    }

    if (!observableOtherTauFound && !observableElectronFound && !observableMuonFound ) {
      //      increment(fTauNotInTauCounter);                                                                                                                                               
      htransverseMassNoObservableLeptons->Fill(transverseMass);
    }
    /*
    if ((fabs(genData.getGenMET()->pt() - metData.getSelectedMET()->pt())/genData.getGenMET()->pt()) < 0.2) {
      if (!otherTauFound && !electronFound && !muonFound ) {
	//      increment(fTauNotInTauCounter);
	//	htransverseMassNoLeptonGoodMet->Fill(transverseMass);
	if (myTauFoundStatus ) {
	  //      increment(fTauNotInTauCounter);
	  htransverseMassNoLeptonGoodMetGoodTau->Fill(transverseMass);
	}
      }
    }
    */


    std::vector<const reco::GenParticle*> mothers = getMothers(parton);
    int motherId=9999;      
    bool wInMothers = false;
    bool zInMothers = false;
    bool topInMothers = false;
    bool bottomInMothers = false;
    bool tauInMothers = false;
    bool hplusInMothers = false;

    for(size_t d=0; d<mothers.size(); ++d) {
      const reco::GenParticle dparticle = *mothers[d];
      motherId = dparticle.pdgId();
      if( abs(motherId) == 24 ) wInMothers = true; 
      if( abs(motherId) == 23 ) zInMothers = true; 
      if( abs(motherId) == 6 ) topInMothers = true;
      if( abs(motherId) == 5 ) bottomInMothers = true;
      if( abs(motherId) == 15 ) tauInMothers = true;
      if( abs(motherId) == 37 ) hplusInMothers = true;
            
    }

    bool FromBottom = false;
    bool FromJet = false;    
    bool FromHplusTau = false;
    bool FromWTau = false;
    bool FromW = false;
    bool FromZTau = false;
    bool FromZ = false;
    
    if (bottomInMothers && !wInMothers && !zInMothers  ) FromBottom = true;
    if (!bottomInMothers && !wInMothers && !hplusInMothers && !zInMothers ) FromJet = true;
    if (hplusInMothers && tauInMothers ) FromHplusTau = true;
    if (wInMothers && tauInMothers ) FromWTau = true;
    if (zInMothers && tauInMothers ) FromZTau = true;
    if (wInMothers && !tauInMothers ) FromW = true;
    if (zInMothers && !tauInMothers ) FromZ = true;

    if (FromBottom && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromBottomCounter);
    if (FromBottom && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromBottomCounter);
    if (FromBottom && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsHadronFromBottomCounter);
    

    if (FromJet && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromJetCounter); 
    if (FromJet && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromJetCounter);
    if (FromJet && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11)  increment(fTauIsHadronFromJetCounter);

    //      if (hplusInMothers && std::abs(parton.pdgId()) == 15 ) tauFromHplus = true;
    if (hplusInMothers && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromHplusCounter);
    if (hplusInMothers && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromHplusCounter);
    if (hplusInMothers && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsHadronFromHplusCounter);

    if (FromW && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromWCounter);
    if (FromW && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromWCounter);
    if (FromW && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsQuarkFromWCounter);

    if (FromWTau && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromWTauCounter);
    if (FromWTau && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromWTauCounter);
    if (FromWTau && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsHadronFromWTauCounter);

    if (FromZ && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromZCounter);
    if (FromZ && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromZCounter);
    if (FromZ && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsQuarkFromZCounter);

    if (FromZTau && std::abs(parton.pdgId()) == 11 ) increment(fTauIsElectronFromZTauCounter);
    if (FromZTau && std::abs(parton.pdgId()) == 13 ) increment(fTauIsMuonFromZTauCounter);
    if (FromZTau && std::abs(parton.pdgId()) != 13 && std::abs(parton.pdgId()) != 11 ) increment(fTauIsHadronFromZTauCounter);

    //      if (wInMothers && std::abs(parton.pdgId()) == 15 ) tauFromW = true; 


    if (myTauFoundStatus && !myLeptonVetoStatus) {
      increment(fRealTauAfterDeltaPhiCounter);
      if (!vetoTauData.passedEvent()) increment(fRealTauAfterDeltaPhiTauVetoCounter);
    }

    /*
    if (electronFromW ) increment(fTauIsElectronFromWCounter);
    //      if (electronFound ) increment(fTauIsElectronFromWCounter);
    if (muonFromW ) increment(fTauIsMuonFromWCounter);  
    if (quarkFromW ) increment(fTauIsQuarkFromWCounter);
    if (FromBottom && electronFound ) increment(fTauIsElectronFromBottomCounter);
    if (FromBottom  &&  muonFound) increment(fTauIsMuonFromBottomCounter);  
    if (FromBottom && !electronFound &&  !muonFound &&  !tauFound ) increment(fTauIsHadronFromBottomCounter);
    if (FromJet && electronFound ) increment(fTauIsElectronFromJetCounter);
    if (FromJet &&  muonFound ) increment(fTauIsMuonFromJetCounter);  
    if (FromJet && !electronFound &&  !muonFound &&  !tauFound) increment(fTauIsHadronFromJetCounter);
    //      if (tauFromHplus && !electronFound &&  !muonFound) increment(fTauIsHadronFromHplusCounter);
    if (tauFromW && !electronFound &&  !muonFound) increment(fTauIsHadronFromWCounter);
    if (electronFound &&  tauFound) increment(fTauIsElectronFromTauCounter);
    */
  }

  SignalAnalysis::CounterGroup* SignalAnalysis::getCounterGroupByTauMatch(FakeTauIdentifier::MCSelectedTauMatchType tauMatch) {
    if (tauMatch == FakeTauIdentifier::kkElectronToTau) return &fElectronToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkElectronFromTauDecayToTau) return &fElectronFromTauDecayToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkMuonToTau) return &fMuonToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkMuonFromTauDecayToTau) return &fMuonFromTauDecayToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkTauToTau) return &fGenuineToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkOneProngTauToTau) return &fGenuineToTausCounterGroup; // Handle separation in filling
    else if (tauMatch == FakeTauIdentifier::kkJetToTau) return &fJetToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkElectronToTauAndTauOutsideAcceptance) return &fElectronToTausAndTauOutsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkElectronFromTauDecayToTauAndTauOutsideAcceptance) return &fElectronFromTauDecayToTausAndTauOutsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkMuonToTauAndTauOutsideAcceptance) return &fMuonToTausAndTauOutsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkMuonFromTauDecayToTauAndTauOutsideAcceptance) return &fMuonFromTauDecayToTausAndTauOutsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkTauToTauAndTauOutsideAcceptance) return &fGenuineToTausAndTauOutsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkOneProngTauToTauAndTauOutsideAcceptance) return &fGenuineToTausAndTauOutsideAcceptanceCounterGroup; // Handle separation in filling
    else if (tauMatch == FakeTauIdentifier::kkJetToTauAndTauOutsideAcceptance) return &fJetToTausAndTauOutsideAcceptanceCounterGroup;
    return 0;
  }

  void SignalAnalysis::fillSelectionFlowAndCounterGroups(int nVertices, FakeTauIdentifier::Data& tauMatchData, SignalSelectionOrder selection, const TauSelection::Data& tauData) {
    hSelectionFlow->Fill(selection);
    hSelectionFlowVsVertices->Fill(nVertices, selection);
    if (tauMatchData.isFakeTau())
      hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, selection);
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), selection, tauData);
  }

  void SignalAnalysis::fillEWKFakeTausCounters(FakeTauIdentifier::MCSelectedTauMatchType tauMatch, HPlus::SignalAnalysis::SignalSelectionOrder selection, const HPlus::TauSelection::Data& tauData) {
    // Get out if no match has been found
    if (tauMatch == FakeTauIdentifier::kkNoMC) return;
    // Obtain status for main counter
    // Define event as type II if no genuine tau was identified as the selected tau
    bool myFakeTauStatus = fFakeTauIdentifier.isFakeTau(tauMatch); // FIXME: think here if the tau_e -> tau  and tau_mu -> tau should be excluded
    // Fill main and subcounter for the selection
    SignalAnalysis::CounterGroup* myCounterGroup = getCounterGroupByTauMatch(tauMatch);
    if (selection == kSignalOrderTauID) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementOneTauCounter();
      myCounterGroup->incrementOneTauCounter();
    } else if (selection == kSignalOrderMETSelection) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementMETCounter();
      myCounterGroup->incrementMETCounter();
    } else if (selection == kSignalOrderElectronVeto) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementElectronVetoCounter();
      myCounterGroup->incrementElectronVetoCounter();
    } else if (selection == kSignalOrderMuonVeto) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementMuonVetoCounter();
      myCounterGroup->incrementMuonVetoCounter();
    } else if (selection == kSignalOrderJetSelection) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementNJetsCounter();
      myCounterGroup->incrementNJetsCounter();
    } else if (selection == kSignalOrderBTagSelection) {
      if (myFakeTauStatus) {
        fEWKFakeTausGroup.incrementBTaggingCounter();
        // Fill histograms
        hEWKFakeTausSelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt());
        hEWKFakeTausSelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta());
      }
      myCounterGroup->incrementBTaggingCounter();
    } else if (selection == kSignalOrderDeltaPhiBackToBackSelection) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementDeltaPhiBackToBackCounter();
      myCounterGroup->incrementDeltaPhiBackToBackCounter();
    } else if (selection == kSignalOrderFakeMETVeto) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementFakeMETVetoCounter();
      myCounterGroup->incrementFakeMETVetoCounter();
    } else if (selection == kSignalOrderTopSelection) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementTopSelectionCounter();
      myCounterGroup->incrementTopSelectionCounter();
    } else if (selection == kSignalOrderDeltaPhiCollinearSelection) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementDeltaPhiCollinearCounter();
      myCounterGroup->incrementDeltaPhiCollinearCounter();
    } else if (selection == kSignalOrderSelectedEvents) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementSelectedEventsCounter();
      myCounterGroup->incrementSelectedEventsCounter();
    } else if (selection == kSignalOrderSelectedEventsFullMass) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementSelectedEventsFullMassCounter();
      myCounterGroup->incrementSelectedEventsFullMassCounter();
    }
    // Check status for genuine one prong taus
    if (fFakeTauIdentifier.isGenuineOneProngTau(tauMatch)) {
      SignalAnalysis::CounterGroup* mySpecialGroup = &fGenuineOneProngToTausCounterGroup;
      if (tauMatch == FakeTauIdentifier::kkOneProngTauToTauAndTauOutsideAcceptance) {
        mySpecialGroup = &fGenuineOneProngToTausAndTauOutsideAcceptanceCounterGroup;
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
        mySpecialGroup->incrementTopSelectionCounter();
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
