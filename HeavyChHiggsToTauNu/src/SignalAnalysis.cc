#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"

#include "TLorentzVector.h"

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TNamed.h"

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
    fMETCounter(eventCounter.addCounter("EWKfaketaus:MET")),
    fNJetsCounter(eventCounter.addCounter("EWKfaketaus:njets")),
    fBTaggingCounter(eventCounter.addCounter("EWKfaketaus:btagging")),
    fDeltaPhiCounter(eventCounter.addCounter("EWKfaketaus:deltaphi")),
    fFakeMETVetoCounter(eventCounter.addCounter("EWKfaketaus:fake MET veto")),
    fTopSelectionCounter(eventCounter.addCounter("EWKfaketaus:Top Selection cut")),
    fTopChiSelectionCounter(eventCounter.addCounter("EWKfaketaus:Top Chi Selection cut")),
    //    fTopChiSelectionNarrowCounter(eventCounter.addCounter("EWKfaketaus:Top Chi Selection small window")),
    fTopWithBSelectionCounter(eventCounter.addCounter("EWKfaketaus:Top with B Selection cut")),
    fTopWithWSelectionCounter(eventCounter.addCounter("EWKfaketaus:Top with W Selection cut")),
    fSelectedEventsCounter(eventCounter.addCounter("EWKfaketaus:SelectedEvents")) { }
  SignalAnalysis::CounterGroup::CounterGroup(EventCounter& eventCounter, std::string prefix) :
    fOneTauCounter(eventCounter.addSubCounter(prefix,":taus == 1")),
    fElectronVetoCounter(eventCounter.addSubCounter(prefix,":electron veto")),
    fMuonVetoCounter(eventCounter.addSubCounter(prefix,":muon veto")),
    fMETCounter(eventCounter.addSubCounter(prefix,":MET")),
    fNJetsCounter(eventCounter.addSubCounter(prefix,":njets")),
    fBTaggingCounter(eventCounter.addSubCounter(prefix,":btagging")),
    fDeltaPhiCounter(eventCounter.addSubCounter(prefix,":deltaphi")),
    //    fHiggsMassCutCounter(eventCounter.addSubCounter(prefix,"HiggsMassCut")),
    fFakeMETVetoCounter(eventCounter.addSubCounter(prefix,":fake MET veto")),
    fTopSelectionCounter(eventCounter.addSubCounter(prefix,":Top Selection cut")),
    //fTopSelectionNarrowCounter(eventCounter.addSubCounter(prefix,":Top Selection small window")),
    fTopChiSelectionCounter(eventCounter.addSubCounter(prefix,":Top Chi Selection cut")),
    fTopWithBSelectionCounter(eventCounter.addSubCounter(prefix,":Top with B Selection cut")),
    fTopWithWSelectionCounter(eventCounter.addSubCounter(prefix,":Top with W Selection cut")),
    fSelectedEventsCounter(eventCounter.addSubCounter(prefix,"EWKfaketaus:SelectedEvents")) { }
  
  SignalAnalysis::CounterGroup::~CounterGroup() { }

  SignalAnalysis::SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    fHistoWrapper(fEventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
    bBlindAnalysisStatus(iConfig.getUntrackedParameter<bool>("blindAnalysisStatus")),
    fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
    fTopRecoName(iConfig.getUntrackedParameter<std::string>("topReconstruction")),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),
    fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
    fTausExistCounter(eventCounter.addCounter("taus > 0")),
    fOneTauCounter(eventCounter.addCounter("taus == 1")),
    fTriggerScaleFactorCounter(eventCounter.addCounter("trigger scale factor")),
    fGenuineTauCounter(eventCounter.addCounter("Tau is genuine")),
    fVetoTauCounter(eventCounter.addCounter("tau veto")),
    fElectronVetoCounter(eventCounter.addCounter("electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("muon veto")),
    fNJetsCounter(eventCounter.addCounter("njets")),
    fMETCounter(eventCounter.addCounter("MET")),
    fBTaggingCounter(eventCounter.addCounter("btagging")),
    fBTaggingScaleFactorCounter(eventCounter.addCounter("btagging scale factor")),
    fDeltaPhiTauMETCounter(eventCounter.addCounter("DeltaPhi(Tau,MET) upper limit")),
    fHiggsMassCutCounter(eventCounter.addCounter("HiggsMassCut")),
    fTauVetoAfterDeltaPhiCounter(eventCounter.addCounter("TauVeto after DeltaPhi cut")),
    fRealTauAfterDeltaPhiCounter(eventCounter.addCounter("Real tau after deltaPhi cut")),
    fRealTauAfterDeltaPhiTauVetoCounter(eventCounter.addCounter("Real tau after deltaPhi+tauveto cut")),


    fTauIsHadronFromHplusCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from H+ ->tau->hadrons")),
    fTauIsElectronFromHplusCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from H+ ->tau->electron")),
    fTauIsMuonFromHplusCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from H+ ->tau->muon")),
    fTauIsQuarkFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->qq")),
    fTauIsElectronFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->e")),
    fTauIsMuonFromWCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->mu")),
    fTauIsHadronFromWTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->tau->hadrons")),
    fTauIsElectronFromWTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->tau->e")),
    fTauIsMuonFromWTauCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from W->tau->mu")),
    fTauIsElectronFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from top->bottom->e")),
    fTauIsMuonFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from top->bottom->mu")),
    fTauIsHadronFromBottomCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from top->bottom->hadron")),
    fTauIsElectronFromJetCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from jet->e")),
    fTauIsMuonFromJetCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from jet->mu")),
    fTauIsHadronFromJetCounter(eventCounter.addSubCounter("MCinfo for selected events", "Tau from jet->hadron")),

    fTopSelectionCounter(eventCounter.addSubCounter("top", "Top selection")),
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
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, fHistoWrapper),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, fHistoWrapper),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    fVetoTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("vetoTauSelection"), eventCounter, fHistoWrapper),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, fHistoWrapper),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, fHistoWrapper, "MET"),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, fHistoWrapper),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, fHistoWrapper),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, fHistoWrapper),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, fHistoWrapper),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, fHistoWrapper),
    fTopWithWSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithWSelection"), eventCounter, fHistoWrapper),
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, fHistoWrapper),

    //   ftransverseMassCut(iConfig.getUntrackedParameter<edm::ParameterSet>("transverseMassCut")),
    fFullHiggsMassCalculator(eventCounter, fHistoWrapper),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, fHistoWrapper),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, fHistoWrapper),
    fCorrelationAnalysis(eventCounter, fHistoWrapper),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, fHistoWrapper),
    fTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiencyScaleFactor"), fHistoWrapper),
    fVertexWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeightReader")),
    fVertexAssignmentAnalysis(eventCounter, fHistoWrapper),
    fFakeTauIdentifier(fHistoWrapper, "TauID"),
    fTree(iConfig.getUntrackedParameter<edm::ParameterSet>("Tree"), fBTagging.getDiscriminator()),
    // Scale factor uncertainties
    fSFUncertaintiesAfterSelection(fHistoWrapper, "AfterSelection"),
    // Non-QCD Type II related
    fEWKFakeTausGroup(eventCounter),
    fAllTausCounterGroup(eventCounter, "All"),
    fElectronToTausCounterGroup(eventCounter, "e->tau"),
    fMuonToTausCounterGroup(eventCounter, "mu->tau"),
    fGenuineToTausCounterGroup(eventCounter, "tau->tau"),
    fJetToTausCounterGroup(eventCounter, "jet->tau"),
    fAllTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "All with tau outside acceptance"),
    fElectronToTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "e->tau with tau outside acceptance"),
    fMuonToTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "mu->tau with tau outside acceptance"),
    fGenuineToTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "tau->tau with tau outside acceptance"),
    fJetToTausAndTauOutsideAcceptanceCounterGroup(eventCounter, "jet->tau with tau outside acceptance"),
    fModuleLabel(iConfig.getParameter<std::string>("@module_label")),
    fProduce(iConfig.getUntrackedParameter<bool>("produceCollections", false)),
    fOnlyGenuineTaus(iConfig.getUntrackedParameter<bool>("onlyGenuineTaus", false))
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
    hVerticesTriggeredBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myVertexDir, "verticesTriggeredBeforeWeight", "Number of vertices without weighting", 40, 0, 40);
    hVerticesTriggeredAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myVertexDir, "verticesTriggeredAfterWeight", "Number of vertices with weighting", 40, 0, 40);
    //    hmetAfterTrigger = fHistoWrapper.makeTH<TH1F>(*fs, "metAfterTrigger", "metAfterTrigger", 50, 0., 200.);

    hTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTopSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopSelection", "transverseMassTopSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTopChiSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopChiSelection", "transverseMassTopChiSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTopBjetSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopBjetSelection", "transverseMassTopBjetSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTopWithWSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTopWithWSelection", "transverseMassTopWithWSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassTauVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassTauVeto", "transverseMassTauVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hEWKFakeTausTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "EWKFakeTausTransverseMass", "EWKFakeTausTransverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassFakeMetVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "transverseMassFakeMetVeto", "transverseMassFakeMetVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);

    
    hDeltaPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 180, 0., 180.);
    hDeltaPhiJetMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiJetMet", "deltaPhiJetMet", 180, 0., 180.);
    hMaxDeltaPhiJetMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "maxDeltaPhiJetMet", "maxDeltaPhiJetMet", 180, 0., 180.);
    hAlphaT = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "alphaT", "alphaT", 100, 0.0, 5.0);
    hAlphaTInvMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);
    hAlphaTVsRtau = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kDebug, *fs, "alphaT(y)-Vs-Rtau(x)", "alphaT-Vs-Rtau",  120, 0.0, 1.2, 500, 0.0, 5.0);
    //    hMet_AfterTauSelection = fHistoWrapper.makeTH<TH1F>(*fs, "met_AfterTauSelection", "met_AfterTauSelection", 100, 0.0, 400.0);
    //    hMet_BeforeTauSelection = fHistoWrapper.makeTH<TH1F>(*fs, "met_BeforeTauSelection", "met_BeforeTauSelection", 100, 0.0, 400.0);
    
    TFileDirectory mySelectedTauDir = fs->mkdir("SelectedTau");
    hSelectedTauEt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_pT_AfterTauID", "SelectedTau_pT_AfterTauID;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    //    hSelectedTauEtMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedTau_pT_AfterTauID_MetCut", "SelectedTau_pT_AfterTauID_MetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_eta_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.1", 250, -5.0, 5.0);
    hSelectedTauEtAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_pT_AfterCuts", "SelectedTau_pT_AfterCuts;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    hSelectedTauEtaAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_eta_AfterCuts", "SelectedTau_eta_AfterCuts;#tau #eta;N_{events} / 0.1", 250, -5.0, 5.0);
    hSelectedTauPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_phi_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_Rtau_AfterTauID", "SelectedTau_Rtau_AfterTauID;R_{#tau};N_{events} / 0.1", 240, 0., 1.2);
    hSelectedTauRtauAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_Rtau_AfterCuts", "SelectedTau_Rtau_AfterCuts;R_{#tau};N_{events} / 0.1", 240, 0., 1.2);
    hSelectedTauLeadingTrackPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "SelectedTau_TauLeadingTrackPt", "SelectedTau_TauLeadingTrackPt;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    hEWKFakeTausSelectedTauEtAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "EWKFakeTaus_SelectedTau_pT_AfterCuts", "SelectedTau_pT_AfterCuts;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    hEWKFakeTausSelectedTauEtaAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, mySelectedTauDir, "EWKFakeTaus_SelectedTau_eta_AfterCuts", "SelectedTau_eta_AfterCuts;#tau #eta;N_{events} / 0.1", 250, -5.0, 5.0);

    hMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "Met", "Met", 200, 0.0, 500.0);
    hMetAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "Met_AfterCuts", "Met_AfterCuts", 200, 0.0, 500.0);
    
    hSelectionFlow = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SignalSelectionFlow", "SignalSelectionFlow;;N_{events}", 12, 0, 12);
    hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderTrigger,"Trigger");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderVertexSelection,"Vertex");
    hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderTauID,"#tau ID");
    hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderElectronVeto,"Isol. e veto");
    hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderMuonVeto,"Isol. #mu veto");
    hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderMETSelection,"MET");
    hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderJetSelection,"jet sel.");
    hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderBTagSelection,"b-jet sel.");
    hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderDeltaPhiSelection,"#Delta#phi(#tau,MET) cut");
    hSelectionFlow->getHisto()->GetXaxis()->SetBinLabel(1+kSignalOrderSelectedEvents,"Selected events");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderFakeMETVeto,"Further QCD rej.");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderTopSelection,"Top mass");
    hSelectionFlowVsVertices = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "SignalSelectionFlowVsVertices", "SignalSelectionFlowVsVertices;N_{vertices};Step", 50, 0, 50, 12, 0, 12);
    hSelectionFlowVsVerticesFakeTaus = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "SignalSelectionFlowVsVerticesFakeTaus", "SignalSelectionFlowVsVerticesFakeTaus;N_{vertices};Step", 50, 0, 50, 9, 0, 9);
    for (int i = 0; i < 9; ++i) {
      hSelectionFlowVsVertices->getHisto()->GetYaxis()->SetBinLabel(i+1, hSelectionFlow->getHisto()->GetXaxis()->GetBinLabel(i+1));
      hSelectionFlowVsVerticesFakeTaus->getHisto()->GetYaxis()->SetBinLabel(i+1, hSelectionFlow->getHisto()->GetXaxis()->GetBinLabel(i+1));
    }

    hEMFractionAll = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "EWKFakeTaus_FakeTau_EMFraction_All", "FakeTau_EMFraction_All", 22, 0., 1.1);
    hEMFractionElectrons = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "EWKFakeTaus_FakeTau_EMFraction_Electrons", "FakeTau_EMFraction_Electrons", 22, 0., 1.1);

    // Control histograms
    TFileDirectory myCtrlDir = fs->mkdir("ControlPlots");
    hCtrlIdentifiedElectronPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "IdentifiedElectronPt", "IdentifiedElectronPt;Identified electron p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);
    hCtrlIdentifiedMuonPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "IdentifiedMuonPt", "IdentifiedMuonPt;Identified muon p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);
    hCtrlNjets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "Njets", "Njets;Number of selected jets;N_{events}", 10, 0., 10.);
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

    fTree.init(*fs);
  }

  SignalAnalysis::~SignalAnalysis() { }

  void SignalAnalysis::produces(edm::EDFilter *producer) const {
    if(fProduce) {
      producer->produces<std::vector<pat::Tau> >("selectedTaus");
      producer->produces<std::vector<pat::Tau> >("selectedVetoTaus");
      producer->produces<std::vector<pat::Jet> >("selectedJets");
      producer->produces<std::vector<pat::Jet> >("selectedBJets");
      producer->produces<std::vector<pat::Electron> >("selectedVetoElectrons");
      producer->produces<std::vector<pat::Muon> >("selectedVetoMuonsBeforeIsolationAndPtAndEtaCuts");
      producer->produces<std::vector<pat::Muon> >("selectedVetoMuonsBeforePtAndEtaCuts");
    }
  }

  bool SignalAnalysis::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    fEventWeight.updatePrescale(iEvent); // set prescale
    fTree.setPrescaleWeight(fEventWeight.getWeight());

//------ Vertex weight
    double myWeightBeforeVertexReweighting = fEventWeight.getWeight();
    if(!iEvent.isRealData()) {
      const double myVertexWeight = fVertexWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(myVertexWeight);
      fTree.setPileupWeight(myVertexWeight);
    }
    int nVertices = fVertexWeightReader.getNumberOfVertices(iEvent, iSetup);
    hVerticesBeforeWeight->Fill(nVertices, myWeightBeforeVertexReweighting);
    hVerticesAfterWeight->Fill(nVertices);
    fTree.setNvertices(nVertices);

    increment(fAllCounter);

//------ Apply trigger and HLT_MET cut or trigger parametrisation
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);
    hSelectionFlow->Fill(kSignalOrderTrigger);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderTrigger);
    hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderTrigger);
    if(triggerData.hasTriggerPath()) // protection if TriggerSelection is disabled
      fTree.setHltTaus(triggerData.getTriggerTaus());

    hVerticesTriggeredBeforeWeight->Fill(nVertices, myWeightBeforeVertexReweighting);
    hVerticesTriggeredAfterWeight->Fill(nVertices);

//------ GenParticle analysis (must be done here when we effectively trigger all MC)
    if (!iEvent.isRealData()) {
      GenParticleAnalysis::Data genData = fGenparticleAnalysis.analyze(iEvent, iSetup);
      fTree.setGenMET(genData.getGenMET());
    }

//------ Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    //hSelectionFlow->Fill(kSignalOrderVertexSelection);

 
   
    


//------ TauID
    // Store weight of event
    // TauID
    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return false; // Require at least one tau
    // plot leading track without pt cut
    hSelectedTauLeadingTrackPt->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt());
    increment(fTausExistCounter);
    //if(tauData.getSelectedTaus().size() != 1) return false; // Require exactly one tau
    increment(fOneTauCounter);
    // Obtain MC matching - for EWK without genuine taus
    FakeTauIdentifier::MCSelectedTauMatchType myTauMatch = fFakeTauIdentifier.matchTauToMC(iEvent, *(tauData.getSelectedTau()));
    bool myFakeTauStatus = fFakeTauIdentifier.isFakeTau(myTauMatch); // True if the selected tau is a fake
    if(fOnlyGenuineTaus && myFakeTauStatus) return false;
    // Primary vertex assignment analysis - diagnostics only
    fVertexAssignmentAnalysis.analyze(iEvent.isRealData(), pvData.getSelectedVertex(), tauData.getSelectedTau(), myTauMatch);
    // For data, set the current run number (needed for tau embedding
    // input, doesn't harm for normal data except by wasting small
    // amount of time)
    if(iEvent.isRealData())
      fTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
    // Apply trigger scale factor here, because it depends only on tau
    TriggerEfficiencyScaleFactor::Data triggerWeight = fTriggerEfficiencyScaleFactor.applyEventWeight(*(tauData.getSelectedTau()), iEvent.isRealData(), fEventWeight);
    fTree.setTriggerWeight(triggerWeight.getEventWeight(), triggerWeight.getEventWeightAbsoluteUncertainty());

    increment(fTriggerScaleFactorCounter);
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
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderTauID, tauData);
    if (myTauMatch == FakeTauIdentifier::kkElectronToTau)
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
    VetoTauSelection::Data vetoTauData = fVetoTauSelection.analyze(iEvent, iSetup, tauData.getSelectedTau());
    //    if (vetoTauData.passedEvent()) return false; // tau veto
    //    if (!vetoTauData.passedEvent()) return false; // select events with add. taus
    //    if (vetoTauData.getSelectedVetoTaus().size() > 0 ) return false;
    //    increment(fVetoTauCounter);
    if (!vetoTauData.passedEvent()) increment(fVetoTauCounter);




//------ Global electron veto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    //    NonIsolatedElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    hCtrlIdentifiedElectronPt->Fill(electronVetoData.getSelectedElectronPtBeforePtCut());
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);
    hSelectionFlow->Fill(kSignalOrderElectronVeto);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderElectronVeto);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderElectronVeto);
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderElectronVeto, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Electron> > saveElectrons(new std::vector<pat::Electron>());
      copyPtrToVector(electronVetoData.getSelectedElectrons(), *saveElectrons);
      iEvent.put(saveElectrons, "selectedVetoElectrons");
    }


//------ Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    hCtrlIdentifiedMuonPt->Fill(muonVetoData.getSelectedMuonPtBeforePtCut());
    if (!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);
    hSelectionFlow->Fill(kSignalOrderMuonVeto);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderMuonVeto);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderMuonVeto);
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderMuonVeto, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Muon> > saveMuons(new std::vector<pat::Muon>());
      copyPtrToVector(muonVetoData.getSelectedMuonsBeforeIsolationAndPtAndEtaCuts(), *saveMuons);
      iEvent.put(saveMuons, "selectedVetoMuonsBeforeIsolationAndPtAndEtaCuts");
      saveMuons.reset(new std::vector<pat::Muon>());
      copyPtrToVector(muonVetoData.getSelectedMuonsBeforePtAndEtaCuts(), *saveMuons);
      iEvent.put(saveMuons, "selectedVetoMuonsBeforePtAndEtaCuts");
    }

//------ Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), nVertices);
    hCtrlNjets->Fill(jetData.getHadronicJetCount());
    if(!jetData.passedEvent()) return false;
    increment(fNJetsCounter);
    hSelectionFlow->Fill(kSignalOrderJetSelection);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderJetSelection);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderJetSelection);
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderJetSelection, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveJets(new std::vector<pat::Jet>());
      copyPtrToVector(jetData.getSelectedJets(), *saveJets);
      iEvent.put(saveJets, "selectedJets");
    }

//------ Obtain rest of data objects      
    if (fTree.isActive()) {
      // MET
     
      METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getAllJets());
      // transverse mass
      //double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()) );
      // b tagging, no event cut
      BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
      // Top reco, no event cut
     
      TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
      BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());
  
      TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    
      // Calculate alphaT
      EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTau()), jetData.getSelectedJets());   
      
      FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());

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
      fTree.setAlphaT(evtTopologyData.alphaT().fAlphaT);
      fTree.setDeltaPhi(fakeMETData.closestDeltaPhi());
      fTree.fill(iEvent, tauData.getSelectedTaus(), jetData.getSelectedJets());
      return true;
    }

//------ Fill control plots for selected taus after standard selections
    hCtrlSelectedTauRtauAfterStandardSelections->Fill(tauData.getRtauOfSelectedTau());
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


//------ MET cut
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getAllJets());
    hMet->Fill(metData.getSelectedMET()->et(),fEventWeight.getWeight()); 
    hCtrlMET->Fill(metData.getSelectedMET()->et());
    if(!metData.passedEvent()) return false;
    increment(fMETCounter);
    hSelectionFlow->Fill(kSignalOrderMETSelection);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderMETSelection);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderMETSelection);
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderMETSelection, tauData);


//------ b tagging cut
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
    hCtrlNbjets->Fill(btagData.getBJetCount());
    if(!btagData.passedEvent()) return false;
    increment(fBTaggingCounter);

    // Apply scale factor as weight to event
    if (!iEvent.isRealData()) {
      btagData.fillScaleFactorHistograms(); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
   
    increment(fBTaggingScaleFactorCounter);
    hSelectionFlow->Fill(kSignalOrderBTagSelection);
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderBTagSelection);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderBTagSelection);
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderBTagSelection, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveBJets(new std::vector<pat::Jet>());
      copyPtrToVector(btagData.getSelectedJets(), *saveBJets);
      iEvent.put(saveBJets, "selectedBJets");
    }
   

//------ Delta phi(tau,MET) cut
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    hDeltaPhi->Fill(deltaPhi);
    if (deltaPhi > fDeltaPhiCutValue) return false;
    increment(fDeltaPhiTauMETCounter);
    hSelectionFlow->Fill(kSignalOrderDeltaPhiSelection);
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderDeltaPhiSelection);
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderDeltaPhiSelection, tauData);

    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()) );

//------ Top reconstruction

    // Top reco, no event cut

   // top mass with possible event cuts
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    if (TopSelectionData.passedEvent() ) {
      increment(fTopSelectionCounter);
      //      hSelectionFlow->Fill(kSignalOrderTopSelection);
      //        if(transverseMass > 80 ) increment(ftransverseMassCut100TopCounter);
      hTransverseMassTopSelection->Fill(transverseMass);     
    }
 
    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    if (TopChiSelectionData.passedEvent() ) {
      double topmass = TopChiSelectionData.getTopMass();
      increment(fTopChiSelectionCounter);
      double ptBjetInTop = TopChiSelectionData.getSelectedBjet()->pt();
      double etaBjetInTop = TopChiSelectionData.getSelectedBjet()->eta();
      //      double deltaRBjetTau = ROOT::Math::VectorUtil::DeltaR(TopChiSelectionData.getSelectedBjet()->p4(), tauData.getSelectedTau()->p4());
      //      std::cout << "B jet in Top mass:  myMinDeltaR " << deltaRBjetTau   << " pt " << ptBjetInTop  << " eta  " << etaBjetInTop << std::endl;

      //      fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData, metData, TopChiSelectionData);

      if (topmass < 250 ) increment(fTopChiSelection250Counter);
      if (topmass < 220 ) increment(fTopChiSelectionNarrowCounter);
      //      hSelectionFlow->Fill(kSignalOrderTopSelection);      
      hTransverseMassTopChiSelection->Fill(transverseMass);
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
        if (topmass < 220 ) increment(fTopWithBSelection220Counter);
        hTransverseMassTopBjetSelection->Fill(transverseMass); 
      }

      if (TopWithWSelectionData.passedEvent() ) {
        myTopRecoWithWSelectionStatus = true;
        increment(fTopWithWSelectionCounter);
        double topmass = TopWithWSelectionData.getTopMass();
        if (topmass < 250 ) increment(fTopWithWSelection250Counter);
        if (topmass < 220 ) increment(fTopWithWSelection220Counter);
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
    if (!myPassedTopRecoStatus)
      return false;

//------ Transverse mass and control plots
    increment(fSelectedEventsCounter);
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderSelectedEvents, tauData);
    hTransverseMass->Fill(transverseMass);
    if (myFakeTauStatus) hEWKFakeTausTransverseMass->Fill(transverseMass);
    fSFUncertaintiesAfterSelection.setScaleFactorUncertainties(fEventWeight.getWeight(),
                                                               triggerWeight.getEventWeight(), triggerWeight.getEventWeightAbsoluteUncertainty(),
                                                               btagData.getScaleFactor(), btagData.getScaleFactorAbsoluteUncertainty());


    FullHiggsMassCalculator::Data FullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData, metData);
    fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData, metData);
    double HiggsMass = FullHiggsMassData.getHiggsMass();
    if (HiggsMass > 100 && HiggsMass < 200 ) increment(fHiggsMassCutCounter);

//------ Experimental cuts, counters, and histograms
    doMCAnalysisOfSelectedEvents(iEvent, tauData, vetoTauData);



    if (!vetoTauData.passedEvent()) {
      increment(fTauVetoAfterDeltaPhiCounter);
      hTransverseMassTauVeto->Fill(transverseMass); 
    }

    // plot deltaPhi(jet,met)
    double myMaxDeltaPhiJetMET = 0.0;
    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetData.getSelectedJets().begin(); iJet != jetData.getSelectedJets().end(); ++iJet) {
      double jetDeltaPhi = DeltaPhi::reconstruct(**iJet, *(metData.getSelectedMET())) * 57.3;
      hDeltaPhiJetMet->Fill(jetDeltaPhi);
      if (jetDeltaPhi > myMaxDeltaPhiJetMET)
        myMaxDeltaPhiJetMET = jetDeltaPhi;
    }
    hMaxDeltaPhiJetMet->Fill(myMaxDeltaPhiJetMET);



    /*
<<<<<<< HEAD

    // Calculate alphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTau()), jetData.getSelectedJets());   

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

    // Fake MET veto a.k.a. further QCD suppression
    //    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup,  tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());
    if (fakeMETData.passedEvent() ) {
      increment(fFakeMETVetoCounter);
      hTransverseMassFakeMetVeto->Fill(transverseMass);
    }

    // Calculate alphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTau()), jetData.getSelectedJets());   
    // Correlation analysis
    fCorrelationAnalysis.analyze(tauData.getSelectedTaus(), btagData.getSelectedJets());
    // Alpha T
    //if(!evtTopologyData.passedEvent()) return false;
    hAlphaT->Fill(evtTopologyData.alphaT().fAlphaT); // FIXME: move this histogramming to evt topology

    // Forward jet veto
    //    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    //    if (!forwardJetData.passedEvent()) return false;
    //    increment(fForwardJetVetoCounter);

    //std::cout << "run=" << iEvent.id().run() << " lumiblock=" << iEvent.id().luminosityBlock() << " event=" << iEvent.id().event() << ", mT=" << transverseMass << std::endl;

//------- Control plots
    hSelectedTauRtauAfterCuts->Fill(tauData.getRtauOfSelectedTau());
    hSelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt());
    hSelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta());
    hMetAfterCuts->Fill(metData.getSelectedMET()->et());

    return true;
  }

  void SignalAnalysis::doMCAnalysisOfSelectedEvents(edm::Event& iEvent, const TauSelection::Data& tauData, const VetoTauSelection::Data& vetoTauData) {
    if (iEvent.isRealData()) return;

    // Origin and type of selected tau
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    bool myTauFoundStatus = false;
    bool myLeptonVetoStatus = false;

    
    reco::GenParticle parton;

    double minDeltaR = 99999;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (p.pt() > 5 && p.pdgId()!= std::abs(p.pdgId()) ) {
        if (reco::deltaR(p, tauData.getSelectedTau()->leadPFChargedHadrCand()->p4()) < 0.3) {
          if (std::abs(p.pdgId()) == 15) myTauFoundStatus = true;
        }

        double deltaR = reco::deltaR(p, tauData.getSelectedTau()->leadPFChargedHadrCand()->p4());
        if (deltaR < minDeltaR) {
          minDeltaR = deltaR;
          parton = (*genParticles)[i];
        }
      }
    }
  
    
    std::vector<const reco::GenParticle*> mothers = getMothers(parton);
    int motherId=9999;      
    bool wInMothers = false;
    bool topInMothers = false;
    bool bottomInMothers = false;
    bool tauInMothers = false;
    bool hplusInMothers = false;

    for(size_t d=0; d<mothers.size(); ++d) {
      const reco::GenParticle dparticle = *mothers[d];
      motherId = dparticle.pdgId();
      if( abs(motherId) == 24 ) wInMothers = true;
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
    
    if (bottomInMothers && !wInMothers  ) FromBottom = true;
    if (!bottomInMothers && !wInMothers && !hplusInMothers ) FromJet = true;
    if (hplusInMothers && tauInMothers ) FromHplusTau = true;
    if (wInMothers && tauInMothers ) FromWTau = true;
    if (wInMothers && !tauInMothers ) FromW = true;

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
    else if (tauMatch == FakeTauIdentifier::kkMuonToTau) return &fMuonToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkTauToTau) return &fGenuineToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkJetToTau) return &fJetToTausCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkElectronToTauAndTauOutsideAcceptance) return &fElectronToTausAndTauOutsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkMuonToTauAndTauOutsideAcceptance) return &fMuonToTausAndTauOutsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkTauToTauAndTauOutsideAcceptance) return &fGenuineToTausAndTauOutsideAcceptanceCounterGroup;
    else if (tauMatch == FakeTauIdentifier::kkJetToTauAndTauOutsideAcceptance) return &fJetToTausAndTauOutsideAcceptanceCounterGroup;
    return 0;
  }
  
  void SignalAnalysis::fillEWKFakeTausCounters(FakeTauIdentifier::MCSelectedTauMatchType tauMatch, HPlus::SignalAnalysis::SignalSelectionOrder selection, const HPlus::TauSelection::Data& tauData) {
    // Get out if no match has been found
    if (tauMatch == FakeTauIdentifier::kkNoMC) return;
    // Obtain status for main counter
    // Define event as type II if no genuine tau was identified as the selected tau
    bool myFakeTauStatus = fFakeTauIdentifier.isFakeTau(tauMatch);
    // Fill main and subcounter for the selection
    if (selection == kSignalOrderTauID) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementOneTauCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementOneTauCounter();
    } else if (selection == kSignalOrderMETSelection) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementMETCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementMETCounter();
    } else if (selection == kSignalOrderElectronVeto) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementElectronVetoCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementElectronVetoCounter();
    } else if (selection == kSignalOrderMuonVeto) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementMuonVetoCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementMuonVetoCounter();
    } else if (selection == kSignalOrderJetSelection) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementNJetsCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementNJetsCounter();
    } else if (selection == kSignalOrderBTagSelection) {
      if (myFakeTauStatus) {
        fEWKFakeTausGroup.incrementBTaggingCounter();
        // Fill histograms
        hEWKFakeTausSelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt());
        hEWKFakeTausSelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta());
      }
      getCounterGroupByTauMatch(tauMatch)->incrementBTaggingCounter();
/*    } else if (selection == kSignalOrderDeltaPhiSelection) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementDeltaPhiCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementDeltaPhiCounter();*/
    } else if (selection == kSignalOrderDeltaPhiSelection) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementDeltaPhiCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementDeltaPhiCounter();
    } else if (selection == kSignalOrderFakeMETVeto) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementFakeMETVetoCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementFakeMETVetoCounter();
    } else if (selection == kSignalOrderTopSelection) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementTopSelectionCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementTopSelectionCounter();
    } else if (selection == kSignalOrderSelectedEvents) {
      if (myFakeTauStatus) fEWKFakeTausGroup.incrementSelectedEventsCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementSelectedEventsCounter();
    }
  }

  double SignalAnalysis::calculateMuonTauSystemInvatiantMass(const TauSelection::Data& tauData, const GlobalMuonVeto::Data& muonData) const {
    return 0.0;
  }
}