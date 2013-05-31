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
    fFakeMETVetoCounter(eventCounter.addCounter("EWKfaketaus:fake MET veto")),
    fTopSelectionCounter(eventCounter.addCounter("EWKfaketaus:Top Selection cut")),
    fTopChiSelectionCounter(eventCounter.addCounter("EWKfaketaus:Top Chi Selection cut")),
    //fTopWithMHSelectionCounter(eventCounter.addCounter("EWKfaketaus:Top Higgs mass Selection cut")),
    //    fTopChiSelectionNarrowCounter(eventCounter.addCounter("EWKfaketaus:Top Chi Selection small window")),
    //fTopWithBSelectionCounter(eventCounter.addCounter("EWKfaketaus:Top with B Selection cut")),
    //fTopWithWSelectionCounter(eventCounter.addCounter("EWKfaketaus:Top with W Selection cut")),
    fSelectedEventsCounter(eventCounter.addCounter("EWKfaketaus:SelectedEvents")),
    fSelectedEventsFullMassCounter(eventCounter.addCounter("EWKfaketaus:SelectedEventsFullMass")) { }
  SignalAnalysis::CounterGroup::CounterGroup(EventCounter& eventCounter, std::string prefix) :
    fOneTauCounter(eventCounter.addSubCounter(prefix,":taus == 1")),
    fElectronVetoCounter(eventCounter.addSubCounter(prefix,":electron veto")),
    fMuonVetoCounter(eventCounter.addSubCounter(prefix,":muon veto")),
    fNJetsCounter(eventCounter.addSubCounter(prefix,":njets")),
    fDeltaPhiCollinearCounter(eventCounter.addSubCounter(prefix,":deltaphi collinear")),
    fMETCounter(eventCounter.addSubCounter(prefix,":MET")),
    fBTaggingCounter(eventCounter.addSubCounter(prefix,":btagging")),
    fDeltaPhiBackToBackCounter(eventCounter.addSubCounter(prefix,":deltaphi backtoback")),
    //    fHiggsMassSelectionCounter(eventCounter.addSubCounter(prefix,"HiggsMassSelection")),
    fFakeMETVetoCounter(eventCounter.addSubCounter(prefix,":fake MET veto")),
    fTopSelectionCounter(eventCounter.addSubCounter(prefix,":Top Selection cut")),
    //fTopSelectionNarrowCounter(eventCounter.addSubCounter(prefix,":Top Selection small window")),
    fTopChiSelectionCounter(eventCounter.addSubCounter(prefix,":Top Chi Selection cut")),
    //fTopWithMHSelectionCounter(eventCounter.addSubCounter(prefix,":Top after Inv Mass Selection cut")),
    //fTopWithBSelectionCounter(eventCounter.addSubCounter(prefix,":Top with B Selection cut")),
    //fTopWithWSelectionCounter(eventCounter.addSubCounter(prefix,":Top with W Selection cut")),
    fSelectedEventsCounter(eventCounter.addSubCounter(prefix,"EWKfaketaus:SelectedEvents")),
    fSelectedEventsFullMassCounter(eventCounter.addSubCounter(prefix,"EWKfaketaus:SelectedEventsFullMass")) { }

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
    fQCDTailKillerCollinearCounter(eventCounter.addCounter("QCD tail killer collinear")),
    fMETTriggerScaleFactorCounter(eventCounter.addCounter("MET trigger scale factor")),
    fMETCounter(eventCounter.addCounter("MET")),
    fBTaggingCounter(eventCounter.addCounter("btagging")),
    fBTaggingScaleFactorCounter(eventCounter.addCounter("btagging scale factor")),
    fQCDTailKillerBackToBackCounter(eventCounter.addCounter("QCD tail killer back-to-back")),
    fDeltaPhiTauMETCounter(eventCounter.addCounter("DeltaPhi(Tau,MET) upper limit")),
    fDeltaPtJetTauCounter(eventCounter.addCounter("DeltaPt(Jet,Tau) < 5")),
    fBjetVetoCounter(eventCounter.addCounter("Veto on second b jet")),
    fMetCut80Counter(eventCounter.addCounter("MET>80")),
    fMetCut100Counter(eventCounter.addCounter("MET>100")),
    fHiggsMassSelectionCounter(eventCounter.addCounter("HiggsMassSelection")),
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

    fTopSelectionCounter(eventCounter.addSubCounter("top", "Top selection")),
    fTopWithMHSelectionCounter(eventCounter.addCounter("Top after Inv Mass selection")),
    fTopChiSelectionCounter(eventCounter.addSubCounter("top", "Top ChiSelection 120-300")),
    fTopChiSelection250Counter(eventCounter.addSubCounter("top", "Top ChiSelection 120-250")),
    fTopChiSelection220Counter(eventCounter.addSubCounter("top", "Top ChiSelection 120-220")),
    fTopWithBSelectionCounter(eventCounter.addSubCounter("top", "Top with B Selection 120-300")),
    fTopWithBSelection250Counter(eventCounter.addSubCounter("top", "Top with B Selection 120-250")),
    fTopWithBSelection220Counter(eventCounter.addSubCounter("top", "Top with B Selection 120-220")),
    fTopWithWSelectionCounter(eventCounter.addSubCounter("top", "Top with W Selection 120-300")),
    fTopWithWSelection250Counter(eventCounter.addSubCounter("top", "Top with W Selection 120-250")),
    fTopWithWSelection220Counter(eventCounter.addSubCounter("top", "Top with W Selection 120-220")),
    //fTopSelectionCounter(eventCounter.addSubCounter("top", "Top Selection cut")),
    //fTopChiSelectionCounter(eventCounter.addSubCounter("top", "Top ChiSelection cut")),
    fTopChiSelectionNarrowCounter(eventCounter.addSubCounter("top", "Top ChiSelection small window")),
    //fTopWithBSelectionCounter(eventCounter.addSubCounter("top", "Top with B Selection cut")),
    //fTopWithWSelectionCounter(eventCounter.addSubCounter("top", "Top with W Selection cut")),
    fFakeMETVetoCounter(eventCounter.addCounter("FakeMETVeto")),
    fSelectedEventsCounter(eventCounter.addCounter("Selected events")),
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
    //STEFAN    fEventClassification()
    fMETFilters(iConfig.getUntrackedParameter<edm::ParameterSet>("metFilters"), eventCounter),
    fQCDTailKiller(iConfig.getUntrackedParameter<edm::ParameterSet>("QCDTailKiller"), eventCounter, fHistoWrapper),
    fTauEmbeddingMuonIsolationQuantifier(eventCounter, fHistoWrapper),
    fTree(iConfig.getUntrackedParameter<edm::ParameterSet>("Tree"), fBTagging.getDiscriminator()),
    // Scale factor uncertainties
    fSFUncertaintiesAfterSelection(fHistoWrapper, "AfterSelection"),
    fEWKFakeTausSFUncertaintiesAfterSelection(fHistoWrapper, "EWKFakeTausAfterSelection"),
    // Non-QCD Type II related
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
    fCommonPlots(eventCounter, fHistoWrapper),
    fCommonPlotsAfterVertexSelection(fCommonPlots.createCommonPlotsFilledAtEveryStep("VertexSelection",false,"Vtx")),
    fCommonPlotsAfterTauSelection(fCommonPlots.createCommonPlotsFilledAtEveryStep("TauSelection",false,"TauID")),
    fCommonPlotsAfterTauWeight(fCommonPlots.createCommonPlotsFilledAtEveryStep("TauWeight",true,"Tau")),
    fCommonPlotsAfterElectronVeto(fCommonPlots.createCommonPlotsFilledAtEveryStep("ElectronVeto",true,"e veto")),
    fCommonPlotsAfterMuonVeto(fCommonPlots.createCommonPlotsFilledAtEveryStep("MuonVeto",true,"#mu veto")),
    fCommonPlotsAfterJetSelection(fCommonPlots.createCommonPlotsFilledAtEveryStep("JetSelection",true,"#geq3j")),
    fCommonPlotsAfterMET(fCommonPlots.createCommonPlotsFilledAtEveryStep("MET",true,"E_{T}^{miss}")),
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

    hTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kSystematics, *fs, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassDeltaPtCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassDeltaPtCut", "transverseMassDeltaPtCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassSecondBveto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassSecondBveto", "transverseMassSecondBveto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassMet80 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassMet80", "transverseMassMet80;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassMet100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassMet100", "transverseMassMet100;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassNoBtagging = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassNoBtagging", "transverseMassNoBtagging;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassNoBtaggingWithRtau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassNoBtaggingWithRtau", "transverseMassNoBtaggingWithRtau;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTopSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopSelection", "transverseMassTopSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
   hTransverseMassWmassCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassWmassCut", "transverseMassWmassCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTopChiSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopChiSelection", "transverseMassTopChiSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTopBjetSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopBjetSelection", "transverseMassTopBjetSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTopWithWSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopWithWSelection", "transverseMassTopWithWSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTauVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTauVeto", "transverseMassTauVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hEWKFakeTausTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "EWKFakeTausTransverseMass", "EWKFakeTausTransverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassFakeMetVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassFakeMetVeto", "transverseMassFakeMetVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);

    hDeltaPhiVsTransverseMass = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "DeltaPhiVsTransverseMass", "DeltaPhiVsTransverseMass",  180, 0., 180.,200, 0., 400.);


    hFullMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "fullMass", "fullMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 5 GeV/c^{2}", 100, 0., 500.);
    hEWKFakeTausFullMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "EWKFakeTausFullMass", "EWKFakeTausFullMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 5 GeV/c^{2}", 100, 0., 500.);

    hTransverseMassVsNjets = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "transverseMassVsNjets", "transverseMassVsNjets;m_{T}(tau,MET), GeV/c^{2};N_{jets}", 200, 0., 400., 10, 0., 10.);
    hEWKFakeTausTransverseMassVsNjets = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "EWKFakeTausTransverseMassVsNjets", "EWKFakeTausTransverseMassVsNjets;m_{T}(tau,MET), GeV/c^{2};N_{jets}", 200, 0., 400., 10, 0., 10.);

    hDeltaPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 180, 0., 180.);

    hDeltaPhiNoBtagging = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "deltaPhiNoBtagging", "deltaPhiNoBtagging;#Delta#phi(tau,MET);N_{events} / 10 degrees", 180, 0., 180.);

    hEWKFakeTausDeltaPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "EWKFakeTausDeltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 180, 0., 180.);
    hDeltaPhiJetMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "deltaPhiJetMet", "deltaPhiJetMet", 180, 0., 180.);
    hMaxDeltaPhiJetMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "maxDeltaPhiJetMet", "maxDeltaPhiJetMet", 180, 0., 180.);
    hAlphaT = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "alphaT", "alphaT", 100, 0.0, 5.0);
    hAlphaTInvMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);
    hAlphaTVsRtau = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "alphaT(y)-Vs-Rtau(x)", "alphaT-Vs-Rtau",  120, 0.0, 1.2, 500, 0.0, 5.0);
    //    hMet_AfterTauSelection = fHistoWrapper.makeTH<TH1F>(*fs, "met_AfterTauSelection", "met_AfterTauSelection", 100, 0.0, 400.0);
    hDeltaPtJetTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "DeltaPtJetTau", "DeltaPtJetTau", 200, -100., 100.);  
    hDeltaRJetTau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "DeltaRJetTau", "DeltaRJetTau", 100, 0., 2.); 
    //    hMet_BeforeTauSelection = fHistoWrapper.makeTH<TH1F>(*fs, "met_BeforeTauSelection", "met_BeforeTauSelection", 100, 0.0, 400.0);

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

    hMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "Met", "Met", 200, 0.0, 500.0);
    hMetWithBtagging = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "MetWithBtagging", "MetWithBtagging", 200, 0.0, 500.0);
    hMet_beforeJetCut  = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "Met_beforeJetCut", "Met_beforeJetCut", 200, 0.0, 500.0);  
    hMetAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "Met_AfterCuts", "Met_AfterCuts", 200, 0.0, 500.0);

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

    // Control histograms
    TFileDirectory myCtrlDir = fs->mkdir("ControlPlots");
    hCtrlIdentifiedElectronPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "IdentifiedElectronPt", "IdentifiedElectronPt;Identified electron p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);
    hCtrlIdentifiedMuonPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "IdentifiedMuonPt", "IdentifiedMuonPt;Identified muon p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);
    hCtrlNjets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "Njets", "Njets;Number of selected jets;N_{events}", 20, 0., 20.);
    hCtrlNjetsBeforeCollinearCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "NjetsBeforeCollinearCuts", "NjetsBeforeCollinearCuts;Number of selected jets;N_{events}", 20, 0., 20.);
    hCtrlNjetsAfterMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "NjetsAfterMET", "Njets after MET;Number of selected jets;N_{events}", 20, 0., 20.);
    hCtrlSelectedTauPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "SelectedTau_pT_AfterStandardSelections", "SelectedTau_pT_AfterStandardSelections;#tau p_{T}, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlSelectedTauEtaAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "SelectedTau_eta_AfterStandardSelections", "SelectedTau_eta_AfterStandardSelections;#tau #eta;N_{events} / 0.1", 60, -3.0, 3.0);
    hCtrlSelectedTauPhiAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "SelectedTau_phi_AfterStandardSelections", "SelectedTau_eta_AfterStandardSelections;#tau #phi;N_{events} / 0.087", 72, -3.1415926, 3.1415926);
    hCtrlSelectedTauEtaVsPhiAfterStandardSelections = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, myCtrlDir, "SelectedTau_etavsphi_AfterStandardSelections", "SelectedTau_etavsphi_AfterStandardSelections;#tau #eta;#tau #phi", 60, -3.0, 3.0, 36, -3.1415926, 3.1415926);
    hCtrlSelectedTauLeadingTrkPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "SelectedTau_LeadingTrackPt_AfterStandardSelections", "SelectedTau_LeadingTrackPt_AfterStandardSelections;#tau ldg.ch.particle p_{T}, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlSelectedTauRtauAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "SelectedTau_Rtau_AfterStandardSelections", "SelectedTau_Rtau_AfterStandardSelections;R_{#tau};N_{events} / 0.1", 120, 0., 1.2);
    hCtrlSelectedTauPAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "SelectedTau_p_AfterStandardSelections", "SelectedTau_p_AfterStandardSelections;#tau p, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlSelectedTauLeadingTrkPAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "SelectedTau_LeadingTrackP_AfterStandardSelections", "SelectedTau_LeadingTrackP_AfterStandardSelections;#tau ldg.ch.particle p, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlIdentifiedElectronPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "IdentifiedElectronPt_AfterStandardSelections", "IdentifiedElectronPt_AfterStandardSelections;Identified electron p_{T}, GeV/c;N_{events} / 1 GeV", 20, 0., 20.);;
    hCtrlIdentifiedMuonPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "IdentifiedMuonPt_AfterStandardSelections", "IdentifiedMuonPt_AfterStandardSelections;Identified muon p_{T}, GeV/c;N_{events} / 1 GeV", 20, 0., 20.);
    hCtrlNjetsAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "Njets_AfterStandardSelections", "Njets_AfterStandardSelections;Number of selected jets;N_{events}", 7, 3., 10.);
    hCtrlMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "MET", "MET;MET, GeV;N_{events} / 10 GeV", 100, 0., 500.);
    hCtrlNbjets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "NBjets", "NBjets;Number of identified b-jets;N_{events}", 10, 0., 10.);
    for (int i = 0; i < 4; ++i) {
      std::stringstream sName;
      std::stringstream sTitle;
      sName << "QCDTailKillerJet" << i << "BackToBack";
      sTitle << "QCDTailKillerJet" << i << "BackToBack;#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{" << i << "},MET)^{2}}, ^{o};N_{events}";
      hCtrlQCDTailKillerBackToBack.push_back(fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, sName.str().c_str(), sTitle.str().c_str(), 52, 0., 260.));
      sName.str("");
      sTitle.str("");
      sName << "QCDTailKillerJet" << i << "Collinear";
      sTitle << "QCDTailKillerJet" << i << "Collinear;#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{" << i << "},MET))^{2}}, ^{o};N_{events}";
      hCtrlQCDTailKillerCollinear.push_back(fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, sName.str().c_str(), sTitle.str().c_str(), 52, 0., 260.));
    }
    // Control histograms for EWKFakeTaus
    TFileDirectory myCtrlEWKFakeTausDir = fs->mkdir("ControlPlotsEWKFakeTaus");
    hCtrlEWKFakeTausIdentifiedElectronPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "IdentifiedElectronPt", "IdentifiedElectronPt;Identified electron p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);
    hCtrlEWKFakeTausIdentifiedMuonPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "IdentifiedMuonPt", "IdentifiedMuonPt;Identified muon p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);
    hCtrlEWKFakeTausNjets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "Njets", "Njets;Number of selected jets;N_{events}", 20, 0., 20.);
    hCtrlEWKFakeTausNjetsBeforeCollinearCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "NjetsBeforeCollinearCut", "NjetsBeforeCollinearCut;Number of selected jets;N_{events}", 20, 0., 20.);
    hCtrlEWKFakeTausNjetsAfterMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "NjetsAfterMET", "NjetsAfterMET;Number of selected jets;N_{events}", 20, 0., 20.);
    hCtrlEWKFakeTausSelectedTauPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "SelectedTau_pT_AfterStandardSelections", "SelectedTau_pT_AfterStandardSelections;#tau p_{T}, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlEWKFakeTausSelectedTauEtaAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "SelectedTau_eta_AfterStandardSelections", "SelectedTau_eta_AfterStandardSelections;#tau #eta;N_{events} / 0.1", 60, -3.0, 3.0);
    hCtrlEWKFakeTausSelectedTauPhiAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "SelectedTau_phi_AfterStandardSelections", "SelectedTau_eta_AfterStandardSelections;#tau #phi;N_{events} / 0.087", 72, -3.1415926, 3.1415926);
    hCtrlEWKFakeTausSelectedTauEtaVsPhiAfterStandardSelections = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "SelectedTau_etavsphi_AfterStandardSelections", "SelectedTau_etavsphi_AfterStandardSelections;#tau #eta;#tau #phi", 60, -3.0, 3.0, 36, -3.1415926, 3.1415926);
    hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "SelectedTau_LeadingTrackPt_AfterStandardSelections", "SelectedTau_LeadingTrackPt_AfterStandardSelections;#tau ldg.ch.particle p_{T}, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlEWKFakeTausSelectedTauRtauAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "SelectedTau_Rtau_AfterStandardSelections", "SelectedTau_Rtau_AfterStandardSelections;R_{#tau};N_{events} / 0.1", 120, 0., 1.2);
    hCtrlEWKFakeTausSelectedTauPAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "SelectedTau_p_AfterStandardSelections", "SelectedTau_p_AfterStandardSelections;#tau p, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "SelectedTau_LeadingTrackP_AfterStandardSelections", "SelectedTau_LeadingTrackP_AfterStandardSelections;#tau ldg.ch.particle p, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlEWKFakeTausIdentifiedElectronPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "IdentifiedElectronPt_AfterStandardSelections", "IdentifiedElectronPt_AfterStandardSelections;Identified electron p_{T}, GeV/c;N_{events} / 1 GeV", 20, 0., 20.);;
    hCtrlEWKFakeTausIdentifiedMuonPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "IdentifiedMuonPt_AfterStandardSelections", "IdentifiedMuonPt_AfterStandardSelections;Identified muon p_{T}, GeV/c;N_{events} / 1 GeV", 20, 0., 20.);
    hCtrlEWKFakeTausNjetsAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "Njets_AfterStandardSelections", "Njets_AfterStandardSelections;Number of selected jets;N_{events}", 7, 3., 10.);
    hCtrlEWKFakeTausMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "MET", "MET;MET, GeV;N_{events} / 10 GeV", 100, 0., 500.);
    hCtrlEWKFakeTausNbjets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "NBjets", "NBjets;Number of identified b-jets;N_{events}", 10, 0., 10.);
    for (int i = 0; i < 4; ++i) {
      std::stringstream sName;
      std::stringstream sTitle;
      sName << "QCDTailKillerJet" << i << "BackToBack";
      sTitle << "QCDTailKillerJet" << i << "BackToBack;#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{" << i << "},MET)^{2}}, ^{o};N_{events}";
      hCtrlEWKFakeTausQCDTailKillerBackToBack.push_back(fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, sName.str().c_str(), sTitle.str().c_str(), 52, 0., 260.));
      sName.str("");
      sTitle.str("");
      sName << "QCDTailKillerJet" << i << "Collinear";
      sTitle << "QCDTailKillerJet" << i << "Collinear;#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{" << i << "},MET))^{2}}, ^{o};N_{events}";
      hCtrlEWKFakeTausQCDTailKillerCollinear.push_back(fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, sName.str().c_str(), sTitle.str().c_str(), 52, 0., 260.));
    }

    hCtrlJetMatrixAfterJetSelection = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myCtrlDir, "JetMatrixAfterJetSelection", "JetMatrixAfterJetSelection;Number of selected jets;Number of selected b jets", 7, 3., 10.,7, 0., 7.);
    hCtrlJetMatrixAfterMET = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myCtrlDir, "JetMatrixAfterMET", "JetMatrixAfterMET;Number of selected jets;Number of selected b jets", 7, 3., 10.,7, 0., 7.);
    hCtrlJetMatrixAfterMET100 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myCtrlDir, "JetMatrixAfterMET100", "JetMatrixAfterMET100;Number of selected jets;Number of selected b jets", 7, 3., 10.,7, 0., 7.);

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
    edm::Ptr<pat::Tau> myZeroTauPointer; // to force common plots to use tau from TauSelection::Data::getSelectedTau()
    fCommonPlots.initialize(iEvent, iSetup, pvData, fTauSelection, myZeroTauPointer, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETSelection, fBTagging, fTopChiSelection, fEvtTopology, fFullHiggsMassCalculator);
    fCommonPlotsAfterVertexSelection->fill();
    fCommonPlots.fillControlPlots(iEvent, pvData);

//------ Apply filter (if chosen) to select tail events
    //if (!selectTailEvents(iEvent, iSetup, pvData)) return false;


//------ TauID
    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
    fTauSelection.analyseFakeTauComposition(fFakeTauIdentifier,iEvent);
    if(!tauData.passedEvent()) return false; // Require at least one tau
    // Obtain MC matching - for EWK without genuine taus
    FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, *(tauData.getSelectedTau()));
    bool myFakeTauStatus = fFakeTauIdentifier.isFakeTau(tauMatchData.getTauMatchType()); // True if the selected tau is a fake
    fCommonPlotsAfterTauSelection->fill();
    fTree.setTauIsFake(myFakeTauStatus);
    if (myFakeTauStatus) fCommonPlotsAfterTauSelectionFakeTaus->fill();
    // Below "genuine tau" is in the context of embedding (i.e. irrespective of the tau decay)
    if(fOnlyGenuineTaus && !fFakeTauIdentifier.isEmbeddingGenuineTau(tauMatchData.getTauMatchType())) return false;
    increment(fTausExistCounter);
    // Apply scale factor for fake tau
    if (!iEvent.isRealData())
      fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauData.getSelectedTau()->eta()));
    fCommonPlotsAfterTauWeight->fill();
    if (myFakeTauStatus) fCommonPlotsAfterTauWeightFakeTaus->fill();
    fCommonPlots.fillControlPlots(iEvent, iSetup, tauData, tauMatchData, tauData.getSelectedTau(), fMETSelection);
    // plot leading track without pt cut
    hSelectedTauLeadingTrackPt->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt());
    increment(fTauFakeScaleFactorCounter);
    //if(tauData.getSelectedTaus().size() != 1) return false; // Require exactly one tau
    increment(fOneTauCounter);
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
    hSelectionFlow->Fill(kSignalOrderTauID);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderTauID);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderTauID);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Tau> > saveTaus(new std::vector<pat::Tau>());
      copyPtrToVector(tauData.getSelectedTaus(), *saveTaus);
      iEvent.put(saveTaus, "selectedTaus");
    }
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
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), kSignalOrderTauID, tauData);
    if (tauMatchData.getTauMatchType() == FakeTauIdentifier::kkElectronToTau)
      hEMFractionElectrons->Fill(tauData.getSelectedTau()->emFraction());
    hEMFractionAll->Fill(tauData.getSelectedTau()->emFraction());

    /*
    // for testing
 // MET
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), nVertices);
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getAllJets());
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());

    if(metData.passedEvent()) {
      // transverse mass
      double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()) );
      hmtTest_metcut->Fill(transverseMass, fEventWeight.getWeight());
      if(jetData.passedEvent()) {
	hmtTest_jetcut->Fill(transverseMass, fEventWeight.getWeight());
	// b tagging, no event cut
	if(btagData.passedEvent()) {
	  hmtTest_btagcut->Fill(transverseMass, fEventWeight.getWeight());
	}
      }
    }
    */  
//------ Veto against second tau in event
    VetoTauSelection::Data vetoTauData = fVetoTauSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), pvData.getSelectedVertex()->z());
    //    if (vetoTauData.passedEvent()) return false; // tau veto
    //    if (!vetoTauData.passedEvent()) return false; // select events with add. taus
    //    if (vetoTauData.getSelectedVetoTaus().size() > 0 ) return false;
    //    increment(fVetoTauCounter);
    if (vetoTauData.passedEvent()) increment(fVetoTauCounter);

    //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! temporary place !!!!!!!!!!!!!!!!!!
    /*
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), nVertices);

    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getAllJets());
    hMet_beforeJetCut->Fill(metData.getSelectedMET()->et());  
//------ Experimental cuts, counters, and histograms
    if (!iEvent.isRealData()) {
      doMCAnalysisOfSelectedEvents(iEvent, tauData, vetoTauData, metData, genData);
    }
    */

//------ Global electron veto
    ElectronSelection::Data electronVetoData = fElectronSelection.analyze(iEvent, iSetup);
    //    NonIsolatedElectronVeto::Data electronVetoData = fNonIsolatedElectronVeto.analyze(iEvent, iSetup);
    hCtrlIdentifiedElectronPt->Fill(electronVetoData.getSelectedElectronPtBeforePtCut());

    if (myFakeTauStatus) hCtrlEWKFakeTausIdentifiedElectronPt->Fill(electronVetoData.getSelectedElectronPtBeforePtCut());

    if (!electronVetoData.passedEvent()) return false;
    fCommonPlotsAfterElectronVeto->fill();
    fCommonPlots.fillControlPlots(iEvent, electronVetoData);
    if (myFakeTauStatus) fCommonPlotsAfterElectronVetoFakeTaus->fill();
    increment(fElectronVetoCounter);
    hSelectionFlow->Fill(kSignalOrderElectronVeto);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderElectronVeto);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderElectronVeto);
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), kSignalOrderElectronVeto, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Electron> > saveElectrons(new std::vector<pat::Electron>());
      copyPtrToVector(electronVetoData.getSelectedElectronsBeforePtAndEtaCuts(), *saveElectrons);
      iEvent.put(saveElectrons, "selectedVetoElectronsBeforePtAndEtaCuts");
    }


//------ Global muon veto
    MuonSelection::Data muonVetoData = fMuonSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    hCtrlIdentifiedMuonPt->Fill(muonVetoData.getSelectedMuonPtBeforePtCut());
    if (myFakeTauStatus) hCtrlEWKFakeTausIdentifiedMuonPt->Fill(muonVetoData.getSelectedMuonPtBeforePtCut());
    if (!muonVetoData.passedEvent()) return false;
    fCommonPlotsAfterMuonVeto->fill();
    fCommonPlots.fillControlPlots(iEvent, muonVetoData);
    if (myFakeTauStatus) fCommonPlotsAfterMuonVetoFakeTaus->fill();
    increment(fMuonVetoCounter);
    hSelectionFlow->Fill(kSignalOrderMuonVeto);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderMuonVeto);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderMuonVeto);
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), kSignalOrderMuonVeto, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Muon> > saveMuons(new std::vector<pat::Muon>());
      copyPtrToVector(muonVetoData.getSelectedMuonsBeforePtAndEtaCuts(), *saveMuons);
      iEvent.put(saveMuons, "selectedVetoMuonsBeforePtAndEtaCuts");
    }


//------ Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), nVertices);

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

    hCtrlNjetsBeforeCollinearCuts->Fill(jetData.getHadronicJetCount());
    if (myFakeTauStatus) hCtrlEWKFakeTausNjetsBeforeCollinearCuts->Fill(jetData.getHadronicJetCount());
    if(!jetData.passedEvent()) return false;
    increment(fNJetsCounter);
    // For data, set the current run number (needed for tau embedding
    // input, doesn't harm for normal data except by wasting small
    // amount of time)
    if(iEvent.isRealData())
      fMETTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
    METSelection::Data metDataTmp = fMETSelection.silentAnalyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getAllJets());
    // Apply trigger scale factor here for now, SF calculated for tau+3 jets events
    METTriggerEfficiencyScaleFactor::Data metTriggerWeight = fMETTriggerEfficiencyScaleFactor.applyEventWeight(*(metDataTmp.getSelectedMET()), iEvent.isRealData(), fEventWeight);
    fTree.setMETTriggerWeight(metTriggerWeight.getEventWeight(), metTriggerWeight.getEventWeightAbsoluteUncertainty());
    increment(fMETTriggerScaleFactorCounter);

    fCommonPlotsAfterJetSelection->fill();
    fCommonPlots.fillControlPlots(iEvent, jetData);
    if (myFakeTauStatus) fCommonPlotsAfterJetSelectionFakeTaus->fill();

    hSelectionFlow->Fill(kSignalOrderJetSelection);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderJetSelection);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderJetSelection);
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), kSignalOrderJetSelection, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveJets(new std::vector<pat::Jet>());
      copyPtrToVector(jetData.getSelectedJets(), *saveJets);
      iEvent.put(saveJets, "selectedJets");
    }
    if (bTauEmbeddingStatus)
      fTauEmbeddingMuonIsolationQuantifier.analyzeAfterJets(iEvent, iSetup);


//------ Improved delta phi cut, a.k.a. QCD tail killer - collinear part
    METSelection::Data metDataForCollinearCut = fMETSelection.silentAnalyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getAllJets());
    const QCDTailKiller::Data qcdTailKillerDataCollinear = fQCDTailKiller.silentAnalyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metDataForCollinearCut.getSelectedMET());
    for (int i = 0; i < qcdTailKillerDataCollinear.getNConsideredJets(); ++i) {
      if (i < 4) { // protection
        hCtrlQCDTailKillerCollinear[i]->Fill(qcdTailKillerDataCollinear.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (myFakeTauStatus)
          hCtrlEWKFakeTausQCDTailKillerCollinear[i]->Fill(qcdTailKillerDataCollinear.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (!qcdTailKillerDataCollinear.passCollinearCutForJet(i)) return false;
      }
    }
    increment(fQCDTailKillerCollinearCounter);
    hSelectionFlow->Fill(kSignalOrderDeltaPhiCollinearSelection);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderDeltaPhiCollinearSelection);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderDeltaPhiCollinearSelection);
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), kSignalOrderDeltaPhiCollinearSelection, tauData);

    hCtrlNjets->Fill(jetData.getHadronicJetCount());
    if (myFakeTauStatus) hCtrlEWKFakeTausNjets->Fill(jetData.getHadronicJetCount());

//------ Fill control plots for selected taus after standard selections
    hCtrlSelectedTauRtauAfterStandardSelections->Fill(tauData.getSelectedTauRtauValue());
    hCtrlSelectedTauLeadingTrkPtAfterStandardSelections->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt());
    hCtrlSelectedTauPtAfterStandardSelections->Fill(tauData.getSelectedTau()->pt());
    hCtrlSelectedTauEtaAfterStandardSelections->Fill(tauData.getSelectedTau()->eta());
    hCtrlSelectedTauPhiAfterStandardSelections->Fill(tauData.getSelectedTau()->phi());
    hCtrlSelectedTauEtaVsPhiAfterStandardSelections->Fill(tauData.getSelectedTau()->eta(), tauData.getSelectedTau()->phi());
    hCtrlSelectedTauPAfterStandardSelections->Fill(tauData.getSelectedTau()->p());
    hCtrlSelectedTauLeadingTrkPAfterStandardSelections->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->p());
    hCtrlIdentifiedElectronPtAfterStandardSelections->Fill(electronVetoData.getSelectedElectronPtBeforePtCut());
    hCtrlIdentifiedMuonPtAfterStandardSelections->Fill(muonVetoData.getSelectedMuonPtBeforePtCut());
    hCtrlNjetsAfterStandardSelections->Fill(jetData.getHadronicJetCount());

    if (myFakeTauStatus) {
      hCtrlEWKFakeTausSelectedTauRtauAfterStandardSelections->Fill(tauData.getSelectedTauRtauValue());
      hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterStandardSelections->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt());
      hCtrlEWKFakeTausSelectedTauPtAfterStandardSelections->Fill(tauData.getSelectedTau()->pt());
      hCtrlEWKFakeTausSelectedTauEtaAfterStandardSelections->Fill(tauData.getSelectedTau()->eta());
      hCtrlEWKFakeTausSelectedTauPhiAfterStandardSelections->Fill(tauData.getSelectedTau()->phi());
      hCtrlEWKFakeTausSelectedTauEtaVsPhiAfterStandardSelections->Fill(tauData.getSelectedTau()->eta(), tauData.getSelectedTau()->phi());
      hCtrlEWKFakeTausSelectedTauPAfterStandardSelections->Fill(tauData.getSelectedTau()->p());
      hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterStandardSelections->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->p());
      hCtrlEWKFakeTausIdentifiedElectronPtAfterStandardSelections->Fill(electronVetoData.getSelectedElectronPtBeforePtCut());
      hCtrlEWKFakeTausIdentifiedMuonPtAfterStandardSelections->Fill(muonVetoData.getSelectedMuonPtBeforePtCut());
      hCtrlEWKFakeTausNjetsAfterStandardSelections->Fill(jetData.getHadronicJetCount());
    }

//------ Fill TTree, if it is active
    if (fTree.isActive()) {
      doTreeFilling(iEvent, iSetup, pvData, tauData.getSelectedTau(), electronVetoData, muonVetoData, jetData);
      //return true;
    }


//------ MET cut
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getAllJets());
    hMet->Fill(metData.getSelectedMET()->et());
    hCtrlMET->Fill(metData.getSelectedMET()->et());
    if (myFakeTauStatus) hCtrlEWKFakeTausMET->Fill(metData.getSelectedMET()->et());
    // Obtain delta phi and transverse mass here, but do not yet cut on them
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()));
    BTagging::Data btagData = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    if (transverseMass > 40 && transverseMass < 100)
      hCtrlJetMatrixAfterJetSelection->Fill(jetData.getHadronicJetCount(), btagData.getBJetCount());
    // Now cut on MET
    if(!metData.passedEvent()) return false;
    fCommonPlotsAfterMET->fill();
    if (myFakeTauStatus) fCommonPlotsAfterMETFakeTaus->fill();
    increment(fMETCounter);
    hSelectionFlow->Fill(kSignalOrderMETSelection);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderMETSelection);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderMETSelection);
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), kSignalOrderMETSelection, tauData);


	  //    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()) );
    hTransverseMassNoBtagging->Fill(transverseMass);
//------ Delta phi(tau,MET) cut
//    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    hDeltaPhiNoBtagging->Fill(deltaPhi);
    if (tauData.selectedTauPassesRtau()) hTransverseMassNoBtaggingWithRtau->Fill(transverseMass); 

    // Plot jet matrix
    if (transverseMass > 40 && transverseMass < 100) {
      hCtrlJetMatrixAfterMET->Fill(jetData.getHadronicJetCount(), btagData.getBJetCount());
      if (metData.getSelectedMET()->et() > 100.0)
        hCtrlJetMatrixAfterMET100->Fill(jetData.getHadronicJetCount(), btagData.getBJetCount());

    }
    hCtrlNjetsAfterMET->Fill(jetData.getHadronicJetCount());
    if (myFakeTauStatus) hCtrlEWKFakeTausNjetsAfterMET->Fill(jetData.getHadronicJetCount());



                                          
    //    if (electronTauMatch ) return false;      
//------ b tagging cut

//    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
    btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    hCtrlNbjets->Fill(btagData.getBJetCount());
    if (myFakeTauStatus) hCtrlEWKFakeTausNbjets->Fill(btagData.getBJetCount());
    if(!btagData.passedEvent()) return false;
    fCommonPlotsAfterBTagging->fill();
    if (myFakeTauStatus) fCommonPlotsAfterBTaggingFakeTaus->fill();
    increment(fBTaggingCounter);

    // Apply scale factor as weight to event
    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
   
    increment(fBTaggingScaleFactorCounter);
    hSelectionFlow->Fill(kSignalOrderBTagSelection);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderBTagSelection);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderBTagSelection);
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), kSignalOrderBTagSelection, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveBJets(new std::vector<pat::Jet>());
      copyPtrToVector(btagData.getSelectedJets(), *saveBJets);
      iEvent.put(saveBJets, "selectedBJets");
    }


//------ Improved delta phi cut, a.k.a. QCD tail killer, back-to-back part
    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    for (int i = 0; i < qcdTailKillerData.getNConsideredJets(); ++i) {
      if (i < 4) { // protection
        hCtrlQCDTailKillerBackToBack[i]->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (myFakeTauStatus)
          hCtrlEWKFakeTausQCDTailKillerBackToBack[i]->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (!qcdTailKillerData.passBackToBackCutForJet(i)) return false;
      }
    }
    increment(fQCDTailKillerBackToBackCounter);
    hSelectionFlow->Fill(kSignalOrderDeltaPhiBackToBackSelection);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderDeltaPhiBackToBackSelection);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderDeltaPhiBackToBackSelection);
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), kSignalOrderDeltaPhiBackToBackSelection, tauData);

//------ Delta phi(tau,MET) cut / obsolete

    hDeltaPhi->Fill(deltaPhi);
    //if (myFakeTauStatus) hEWKFakeTausDeltaPhi->Fill(deltaPhi);
    //if (deltaPhi > fDeltaPhiCutValue) return false;
    //increment(fDeltaPhiTauMETCounter);

    // plot deltaPhi(jet,met)
    double myMaxDeltaPhiJetMET = 0.0;
    double minDeltaRTauJet = 9999;
    edm::Ptr<pat::Jet> closestJetToTau; 
    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetData.getSelectedJets().begin(); iJet != jetData.getSelectedJets().end(); ++iJet) {
      double jetDeltaPhi = DeltaPhi::reconstruct(**iJet, *(metData.getSelectedMET())) * 57.3;
      hDeltaPhiJetMet->Fill(jetDeltaPhi);
      if (jetDeltaPhi > myMaxDeltaPhiJetMET) myMaxDeltaPhiJetMET = jetDeltaPhi;
      double deltaRTauJet = ROOT::Math::VectorUtil::DeltaR(tauData.getSelectedTau()->p4(), (*iJet)->p4());
      if ( deltaRTauJet < minDeltaRTauJet) {
	closestJetToTau = *iJet;
	minDeltaRTauJet = deltaRTauJet;
      }
    }
    double DeltaPtJetTau = 9999;
    if ( minDeltaRTauJet < 5) {
      DeltaPtJetTau = closestJetToTau->pt()- tauData.getSelectedTau()->pt();
      hDeltaPtJetTau->Fill(DeltaPtJetTau);
      hDeltaRJetTau->Fill(minDeltaRTauJet);
    }
    hMaxDeltaPhiJetMet->Fill(myMaxDeltaPhiJetMET);

    if (jetData.getDeltaPtJetTau() < 10 ) {
      hTransverseMassDeltaPtCut->Fill(transverseMass);
      increment(fDeltaPtJetTauCounter);
    }

    // test second b jet veto
    if( btagData.getSelectedJets().size() < 2) {
      increment(fBjetVetoCounter);  
      hTransverseMassSecondBveto->Fill(transverseMass);
    }


    // Met test
    if (metData.getSelectedMET()->et() > 80 ) {
      increment(fMetCut80Counter);
      hTransverseMassMet80->Fill(transverseMass);
    }      
    if (metData.getSelectedMET()->et() > 100 ) {
      increment(fMetCut100Counter);
      hTransverseMassMet100->Fill(transverseMass);
    } 

//------ Top reconstruction

    // Top reco, no event cut

   // top mass with possible event cuts
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    if (TopSelectionData.passedEvent() ) {
      increment(fTopSelectionCounter);
      //        if(transverseMass > 80 ) increment(ftransverseMassCut100TopCounter);
      hTransverseMassTopSelection->Fill(transverseMass);     
    }
 
    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    if (TopChiSelectionData.passedEvent() ) {
      double topmass = TopChiSelectionData.getTopMass();
      double wmass = TopChiSelectionData.getWMass();
      increment(fTopChiSelectionCounter);
      //double ptBjetInTop = TopChiSelectionData.getSelectedBjet()->pt();
      //double etaBjetInTop = TopChiSelectionData.getSelectedBjet()->eta();
      //      double deltaRBjetTau = ROOT::Math::VectorUtil::DeltaR(TopChiSelectionData.getSelectedBjet()->p4(), tauData.getSelectedTau()->p4());
      //      std::cout << "B jet in Top mass:  myMinDeltaR " << deltaRBjetTau   << " pt " << ptBjetInTop  << " eta  " << etaBjetInTop << std::endl;

      //      fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData, metData, TopChiSelectionData);

      if (topmass < 250 ) increment(fTopChiSelection250Counter);
      if (topmass < 220 ) {
	increment(fTopChiSelectionNarrowCounter);
	hTransverseMassTopChiSelection->Fill(transverseMass);
      }
      if (wmass < 180 && wmass > 50 ) hTransverseMassWmassCut->Fill(transverseMass);
    }

    bool myTopRecoWithWSelectionStatus = false;
    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());
    if (BjetSelectionData.passedEvent() ) {
      TopWithBSelection::Data TopWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());
      TopWithWSelection::Data TopWithWSelectionData = fTopWithWSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());
      if (TopWithBSelectionData.passedEvent() ) {
        increment(fTopWithBSelectionCounter);
        double topmass = TopWithBSelectionData.getTopMass();
        if (topmass < 250 ) increment(fTopWithBSelection250Counter);
        if (topmass < 220 ) {
	  increment(fTopWithBSelection220Counter);
	  hTransverseMassTopBjetSelection->Fill(transverseMass);
	} 
      }

      if (TopWithWSelectionData.passedEvent() ) {
        myTopRecoWithWSelectionStatus = true;
        increment(fTopWithWSelectionCounter);
        double topmass = TopWithWSelectionData.getTopMass();
        if (topmass < 250 ) increment(fTopWithWSelection250Counter);
        if (topmass < 220 ) {
	  increment(fTopWithWSelection220Counter);
	  hTransverseMassTopWithWSelection->Fill(transverseMass);
	} 
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
    if (!myPassedTopRecoStatus)
      return false;
    hSelectionFlow->Fill(kSignalOrderTopSelection);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderTopSelection);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderTopSelection);
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), kSignalOrderTopSelection, tauData);

//------ Transverse mass and control plots
    increment(fSelectedEventsCounter);
    if (btagData.hasGenuineBJets()) increment(fSelectedEventsCounterWithGenuineBjets);
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), kSignalOrderSelectedEvents, tauData);
    hTransverseMass->Fill(transverseMass);
    hTransverseMassVsNjets->Fill(transverseMass, jetData.getHadronicJetCount());
    hSelectionFlow->Fill(kSignalOrderSelectedEvents);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderSelectedEvents);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderSelectedEvents);
    fCommonPlotsSelected->fill();
    if (myFakeTauStatus) fCommonPlotsSelectedFakeTaus->fill();
    if (transverseMass > 120) {
      fCommonPlotsSelectedMtTail->fill();
      if (myFakeTauStatus) fCommonPlotsSelectedMtTailFakeTaus->fill();
    }
    fCommonPlots.fillFinalPlots();
    if (myFakeTauStatus) fCommonPlots.fillFinalPlotsForFakeTaus();

    hSelectedTauRtauAfterCuts->Fill(tauData.getSelectedTauRtauValue());
    hSelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt());
    hSelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta());
    hMetAfterCuts->Fill(metData.getSelectedMET()->et());


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
      hEWKFakeTausTransverseMass->Fill(transverseMass);
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
    FullHiggsMassCalculator::Data FullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData,
										       metData, &genData);
    if (!FullHiggsMassData.passedEvent()) return false;
    double HiggsMass = FullHiggsMassData.getHiggsMass();
    increment(fHiggsMassSelectionCounter);
    fillEWKFakeTausCounters(tauMatchData.getTauMatchType(), kSignalOrderSelectedEventsFullMass, tauData);
    hFullMass->Fill(HiggsMass);
    fCommonPlotsSelectedFullMass->fill();
    if (myFakeTauStatus) {
      hEWKFakeTausFullMass->Fill(HiggsMass);
      fCommonPlotsSelectedFullMassFakeTaus->fill();
    }
    hSelectionFlow->Fill(kSignalOrderSelectedEventsFullMass);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderSelectedEventsFullMass);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderSelectedEventsFullMass);


//------ Experimental cuts, counters, and histograms
    if (!iEvent.isRealData()) {
      ///      doMCAnalysisOfSelectedEvents(iEvent, tauData, vetoTauData, metData, genData);
    }

   // transverse mass and inv mass with tau veto
    if (vetoTauData.passedEvent()) {
      increment(fTauVetoAfterDeltaPhiCounter);
      hTransverseMassTauVeto->Fill(transverseMass);
      //      hHiggsMassTauVeto->Fill(HiggsMass); 
    }

    // Fake MET veto a.k.a. further QCD suppression
    //    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup,  tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());
    if (fakeMETData.passedEvent() ) {
      increment(fFakeMETVetoCounter);
      hTransverseMassFakeMetVeto->Fill(transverseMass);
    }

    hDeltaPhiVsTransverseMass->Fill(fakeMETData.closestDeltaPhi(),transverseMass); 

    // Calculate alphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(iEvent, iSetup, *(tauData.getSelectedTau()), jetData.getSelectedJetsIncludingTau());
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
   
    METSelection::Data metData = fMETSelection.silentAnalyze(iEvent, iSetup, selectedTau, jetData.getAllJets());
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

  void SignalAnalysis::doMCAnalysisOfSelectedEvents(edm::Event& iEvent, const TauSelection::Data& tauData, const VetoTauSelection::Data& vetoTauData, const METSelection::Data& metData, const GenParticleAnalysis::Data& genData) {
    if (iEvent.isRealData()) return;

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
		if( abs(dparticle.pdgId()) == 24 ) increment(fTauNotInTauFromWCounter);
		//		if( abs(dparticle.pdgId()) == 24 ) std::cout << " W mass " << dparticle.mass() << std::endl;
		if( abs(dparticle.pdgId()) == 24 ) hgenWmass->Fill(dparticle.mass());
		if( abs(dparticle.pdgId()) == 5 ) increment(fTauNotInTauFromBottomCounter);
		if( abs(dparticle.pdgId()) == 37 ) increment(fTauNotInTauFromHplusCounter); 	
	      }
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
	      if( abs(dparticle.pdgId()) == 24 ) increment(fElectronNotInTauFromWCounter);
	      if( abs(dparticle.pdgId()) == 5 ) increment(fElectronNotInTauFromBottomCounter);
	      if( abs(dparticle.pdgId()) == 15 ) increment(fElectronNotInTauFromTauCounter); 	
	     
	    }
	    if ( p.pt() < 15 || fabs(p.eta()) > 2.4 ) continue;
	    increment(fObservableElectronsCounter);
	    observableElectronFound = true;
	  }

	  // muons
          if (std::abs(p.pdgId()) == 13 && !hasImmediateMother(p,13) && !hasImmediateMother(p,-13) ) {
	    increment(fMuonNotInTauCounter);
	    muonFound = true;
	    muon = (*genParticles)[i];
	    std::vector<const reco::GenParticle*> muonMothers = getMothers(muon);
	    
	    for(size_t d=0; d< muonMothers.size(); ++d) {
	      const reco::GenParticle dparticle = *muonMothers[d];
	      if( abs(dparticle.pdgId()) == 24 ) increment(fMuonNotInTauFromWCounter);
	      if( abs(dparticle.pdgId()) == 5 ) increment(fMuonNotInTauFromBottomCounter);
	      if( abs(dparticle.pdgId()) == 15 ) increment(fMuonNotInTauFromTauCounter); 	
	    }
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
    if (otherTauFound || electronFound || muonFound ) {
      //      increment(fTauNotInTauCounter);
      htransverseMassLeptonNotInTau->Fill(transverseMass);
      if (myTauFoundStatus ) htransverseMassLeptonRealSignalTau->Fill(transverseMass);
      if (!myTauFoundStatus ) htransverseMassLeptonFakeSignalTau->Fill(transverseMass); 
    }

    if (!otherTauFound && !electronFound && !muonFound ) {
      //      increment(fTauNotInTauCounter);
      htransverseMassNoLeptonNotInTau->Fill(transverseMass);
    }

    if (observableOtherTauFound || observableElectronFound || observableMuonFound ) {
      //      increment(fTauNotInTauCounter);
      htransverseMassObservableLeptons->Fill(transverseMass);
    }

    if (!observableOtherTauFound && !observableElectronFound && !observableMuonFound ) {
      //      increment(fTauNotInTauCounter);                                                                                                                                               
      htransverseMassNoObservableLeptons->Fill(transverseMass);
    }

    if ((fabs(genData.getGenMET()->pt() - metData.getSelectedMET()->pt())/genData.getGenMET()->pt()) < 0.2) {
      if (!otherTauFound && !electronFound && !muonFound ) {
	//      increment(fTauNotInTauCounter);
	htransverseMassNoLeptonGoodMet->Fill(transverseMass);
	if (myTauFoundStatus ) {
	  //      increment(fTauNotInTauCounter);
	  htransverseMassNoLeptonGoodMetGoodTau->Fill(transverseMass);
	}
      }
    }

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
    METSelection::Data metData = fMETSelection.silentAnalyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getAllJets());
    if (!(metData.getSelectedMET()->et() > 30)) return false;
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()));
    if (deltaPhi < 90) return false;
    if (transverseMass < 80) return false;
    return true;
  }

}
