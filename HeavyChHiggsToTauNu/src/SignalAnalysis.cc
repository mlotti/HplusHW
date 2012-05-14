#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TNamed.h"

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
    fFakeMETVetoCounter(eventCounter.addSubCounter(prefix,":fake MET veto")),
    fTopSelectionCounter(eventCounter.addSubCounter(prefix,":Top Selection cut")),
    //    fTopSelectionNarrowCounter(eventCounter.addSubCounter(prefix,":Top Selection small window")),
    fTopChiSelectionCounter(eventCounter.addSubCounter(prefix,":Top Chi Selection cut")),
    fTopWithBSelectionCounter(eventCounter.addSubCounter(prefix,":Top with B Selection cut")),
    fTopWithWSelectionCounter(eventCounter.addSubCounter(prefix,":Top with W Selection cut")),
    fSelectedEventsCounter(eventCounter.addCounter("EWKfaketaus:SelectedEvents")) { }
  SignalAnalysis::CounterGroup::~CounterGroup() { }

  SignalAnalysis::SignalAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
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
    fTauVetoAfterDeltaPhiCounter(eventCounter.addCounter("TauVeto after DeltaPhi cut")),
    fRealTauAfterDeltaPhiCounter(eventCounter.addCounter("Real tau after deltaPhi cut")),
    fRealTauAfterDeltaPhiTauVetoCounter(eventCounter.addCounter("Real tau after deltaPhi+tauveto cut")),
    fFakeMETVetoCounter(eventCounter.addCounter("fake MET veto")),
    fdeltaPhiTauMET160FakeMetCounter(eventCounter.addCounter("deltaPhi160 and fake MET veto")),
    fForwardJetVetoCounter(eventCounter.addCounter("forward jet veto")),
    ftransverseMassCut70Counter(eventCounter.addCounter("transverseMass > 70")),
    ftransverseMassCut80Counter(eventCounter.addCounter("transverseMass > 80")),
    ftransverseMass70TauVetoCounter(eventCounter.addCounter("transverseMass > 70 tau veto")),
    ftransverseMass80TauVetoCounter(eventCounter.addCounter("transverseMass > 80 tau veto")),
    ftransverseMass70TopChiSelCounter(eventCounter.addCounter("transverseMass > 70 TopChiSel")),
    ftransverseMass70TopWithBSelCounter(eventCounter.addCounter("transverseMass > 70 TopWithBSel")),
    ftransverseMass70TopWithWSelCounter(eventCounter.addCounter("transverseMass > 70 TopWithWSel")),
    ftransverseMass70TopSelCounter(eventCounter.addCounter("transverseMass > 70 TopSel")),
    ftransverseMass80TopChiSelCounter(eventCounter.addCounter("transverseMass > 80 TopChiSel")),
    ftransverseMass80TopWithBSelCounter(eventCounter.addCounter("transverseMass > 80 TopWithBSel")),
    ftransverseMass80TopWithWSelCounter(eventCounter.addCounter("transverseMass > 80 TopWithWSel")),
    ftransverseMass80TopSelCounter(eventCounter.addCounter("transverseMass > 80 TopSel")),
    ftransverseMassCut80NoRtauCounter(eventCounter.addCounter("transverseMass > 60 no Rtau")),
    ftransverseMassCut100NoRtauCounter(eventCounter.addCounter("transverseMass > 80 no Rtau")),
    fZmassVetoCounter(eventCounter.addCounter("ZmassVetoCounter")),
    fTopSelectionCounter(eventCounter.addCounter("Top Selection cut")),
    fTopChiSelectionCounter(eventCounter.addCounter("Top ChiSelection cut")),
    fTopChiSelectionNarrowCounter(eventCounter.addCounter("Top ChiSelection small window")),
    fTopWithBSelectionCounter(eventCounter.addCounter("Top with B Selection cut")),
    fTopWithWSelectionCounter(eventCounter.addCounter("Top with W Selection cut")),
    fSelectedEventsCounter(eventCounter.addCounter("Selected events")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight),
    fVetoTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("vetoTauSelection"), eventCounter, eventWeight),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight, "MET"),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, eventWeight),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, eventWeight),
    fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, eventWeight),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, eventWeight),
    fTopWithWSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithWSelection"), eventCounter, eventWeight),
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, eventWeight),
    //   ftransverseMassCut(iConfig.getUntrackedParameter<edm::ParameterSet>("transverseMassCut")),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, eventWeight),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, eventWeight),
    fCorrelationAnalysis(eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiencyScaleFactor"), eventWeight),
    fVertexWeight(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeight")),
    fVertexAssignmentAnalysis(eventCounter, eventWeight),
    fFakeTauIdentifier(fEventWeight, "TauID"),
    fTree(iConfig.getUntrackedParameter<edm::ParameterSet>("Tree"), fBTagging.getDiscriminator()),
    // Scale factor uncertainties
    fSFUncertaintiesAfterSelection("AfterSelection"),
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
    hVerticesBeforeWeight = makeTH<TH1F>(myVertexDir, "verticesBeforeWeight", "Number of vertices without weighting", 40, 0, 40);
    hVerticesAfterWeight = makeTH<TH1F>(myVertexDir, "verticesAfterWeight", "Number of vertices with weighting", 40, 0, 40);
    hVerticesTriggeredBeforeWeight = makeTH<TH1F>(myVertexDir, "verticesTriggeredBeforeWeight", "Number of vertices without weighting", 40, 0, 40);
    hVerticesTriggeredAfterWeight = makeTH<TH1F>(myVertexDir, "verticesTriggeredAfterWeight", "Number of vertices with weighting", 40, 0, 40);
    //    hmetAfterTrigger = makeTH<TH1F>(*fs, "metAfterTrigger", "metAfterTrigger", 50, 0., 200.);
    
    hTransverseMass = makeTH<TH1F>(*fs, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassTopSelection = makeTH<TH1F>(*fs, "transverseMassTopSelection", "transverseMassTopSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassTopChiSelection = makeTH<TH1F>(*fs, "transverseMassTopChiSelection", "transverseMassTopChiSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassTopBjetSelection = makeTH<TH1F>(*fs, "transverseMassTopBjetSelection", "transverseMassTopBjetSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassTopWithWSelection = makeTH<TH1F>(*fs, "transverseMassTopWithWSelection", "transverseMassTopWithWSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassTauVeto = makeTH<TH1F>(*fs, "transverseMassTauVeto", "transverseMassTauVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);

    hEWKFakeTausTransverseMass = makeTH<TH1F>(*fs, "EWKFakeTausTransverseMass", "EWKFakeTausTransverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    
    hDeltaPhi = makeTH<TH1F>(*fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 360, 0., 180.);
    hDeltaPhiJetMet = makeTH<TH1F>(*fs, "deltaPhiJetMet", "deltaPhiJetMet", 400, 0., 3.2);  
    hAlphaT = makeTH<TH1F>(*fs, "alphaT", "alphaT", 100, 0.0, 5.0);
    hAlphaTInvMass = makeTH<TH1F>(*fs, "alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);    
    hAlphaTVsRtau = makeTH<TH2F>(*fs, "alphaT(y)-Vs-Rtau(x)", "alphaT-Vs-Rtau",  120, 0.0, 1.2, 500, 0.0, 5.0);
    //    hMet_AfterTauSelection = makeTH<TH1F>(*fs, "met_AfterTauSelection", "met_AfterTauSelection", 100, 0.0, 400.0);
    //    hMet_BeforeTauSelection = makeTH<TH1F>(*fs, "met_BeforeTauSelection", "met_BeforeTauSelection", 100, 0.0, 400.0);
    
    TFileDirectory mySelectedTauDir = fs->mkdir("SelectedTau");
    hSelectedTauEt = makeTH<TH1F>(mySelectedTauDir, "SelectedTau_pT_AfterTauID", "SelectedTau_pT_AfterTauID;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    //    hSelectedTauEtMetCut = makeTH<TH1F>(*fs, "SelectedTau_pT_AfterTauID_MetCut", "SelectedTau_pT_AfterTauID_MetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEta = makeTH<TH1F>(mySelectedTauDir, "SelectedTau_eta_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.1", 300, -3.0, 3.0);
    hSelectedTauEtAfterCuts = makeTH<TH1F>(mySelectedTauDir, "SelectedTau_pT_AfterCuts", "SelectedTau_pT_AfterCuts;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 40, 0.0, 400.0);
    hSelectedTauEtaAfterCuts = makeTH<TH1F>(mySelectedTauDir, "SelectedTau_eta_AfterCuts", "SelectedTau_eta_AfterCuts;#tau #eta;N_{events} / 0.1", 30, -3.0, 3.0);
    hSelectedTauPhi = makeTH<TH1F>(mySelectedTauDir, "SelectedTau_phi_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtau = makeTH<TH1F>(mySelectedTauDir, "SelectedTau_Rtau_AfterTauID", "SelectedTau_Rtau_AfterTauID;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);
    hSelectedTauRtauAfterCuts = makeTH<TH1F>(mySelectedTauDir, "SelectedTau_Rtau_AfterCuts", "SelectedTau_Rtau_AfterCuts;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);
    hSelectedTauLeadingTrackPt = makeTH<TH1F>(mySelectedTauDir, "SelectedTau_TauLeadingTrackPt", "SelectedTau_TauLeadingTrackPt;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hEWKFakeTausSelectedTauEtAfterCuts = makeTH<TH1F>(mySelectedTauDir, "EWKFakeTaus_SelectedTau_pT_AfterCuts", "SelectedTau_pT_AfterCuts;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 40, 0.0, 400.0);
    hEWKFakeTausSelectedTauEtaAfterCuts = makeTH<TH1F>(mySelectedTauDir, "EWKFakeTaus_SelectedTau_eta_AfterCuts", "SelectedTau_eta_AfterCuts;#tau #eta;N_{events} / 0.1", 30, -3.0, 3.0);

    hMet = makeTH<TH1F>(*fs, "Met", "Met", 500, 0.0, 500.0);
    hMetAfterCuts = makeTH<TH1F>(*fs, "Met_AfterCuts", "Met_AfterCuts", 400, 0.0, 400.0);
    
    hSelectionFlow = makeTH<TH1F>(*fs, "SignalSelectionFlow", "SignalSelectionFlow;;N_{events}", 8, 0, 8);
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderTrigger,"Trigger");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderVertexSelection,"Vertex");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderTauID,"#tau ID");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderElectronVeto,"Isol. e veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderMuonVeto,"Isol. #mu veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderMETSelection,"MET");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderJetSelection,"jet sel.");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderBTagSelection,"b-jet sel.");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderDeltaPhiSelection,"#Delta#phi(#tau,MET) cut");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderFakeMETVeto,"Further QCD rej.");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderTopSelection,"Top mass");
    hSelectionFlowVsVertices = makeTH<TH2F>(*fs, "SignalSelectionFlowVsVertices", "SignalSelectionFlowVsVertices;N_{vertices};Step", 50, 0, 50, 9, 0, 9);
    hSelectionFlowVsVerticesFakeTaus = makeTH<TH2F>(*fs, "SignalSelectionFlowVsVerticesFakeTaus", "SignalSelectionFlowVsVerticesFakeTaus;N_{vertices};Step", 50, 0, 50, 9, 0, 9);
    for (int i = 0; i < 9; ++i) {
      hSelectionFlowVsVertices->GetYaxis()->SetBinLabel(i+1, hSelectionFlow->GetXaxis()->GetBinLabel(i+1));
      hSelectionFlowVsVerticesFakeTaus->GetYaxis()->SetBinLabel(i+1, hSelectionFlow->GetXaxis()->GetBinLabel(i+1));
    }

    hEMFractionAll = makeTH<TH1F>(*fs, "EWKFakeTaus_FakeTau_EMFraction_All", "FakeTau_EMFraction_All", 22, 0., 1.1);
    hEMFractionElectrons = makeTH<TH1F>(*fs, "EWKFakeTaus_FakeTau_EMFraction_Electrons", "FakeTau_EMFraction_Electrons", 22, 0., 1.1);

    // Control histograms
    TFileDirectory myCtrlDir = fs->mkdir("ControlPlots");
    hCtrlIdentifiedElectronPt = makeTH<TH1F>(myCtrlDir, "IdentifiedElectronPt", "IdentifiedElectronPt;Identified electron p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);
    hCtrlIdentifiedMuonPt = makeTH<TH1F>(myCtrlDir, "IdentifiedMuonPt", "IdentifiedMuonPt;Identified muon p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);
    hCtrlNjets = makeTH<TH1F>(myCtrlDir, "Njets", "Njets;Number of selected jets;N_{events}", 10, 0., 10.);
    hCtrlSelectedTauPtAfterStandardSelections = makeTH<TH1F>(myCtrlDir, "SelectedTau_pT_AfterStandardSelections", "SelectedTau_pT_AfterStandardSelections;#tau p_{T}, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlSelectedTauEtaAfterStandardSelections = makeTH<TH1F>(myCtrlDir, "SelectedTau_eta_AfterStandardSelections", "SelectedTau_eta_AfterStandardSelections;#tau #eta;N_{events} / 0.1", 60, -3.0, 3.0);
    hCtrlSelectedTauPhiAfterStandardSelections = makeTH<TH1F>(myCtrlDir, "SelectedTau_phi_AfterStandardSelections", "SelectedTau_eta_AfterStandardSelections;#tau #phi;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hCtrlSelectedTauEtaVsPhiAfterStandardSelections = makeTH<TH2F>(myCtrlDir, "SelectedTau_etavsphi_AfterStandardSelections", "SelectedTau_etavsphi_AfterStandardSelections;#tau #eta;#tau #phi", 60, -3.0, 3.0, 36, -3.1415926, 3.1415926);
    hCtrlSelectedTauLeadingTrkPtAfterStandardSelections = makeTH<TH1F>(myCtrlDir, "SelectedTau_LeadingTrackPt_AfterStandardSelections", "SelectedTau_LeadingTrackPt_AfterStandardSelections;#tau ldg.ch.particle p_{T}, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlSelectedTauRtauAfterStandardSelections = makeTH<TH1F>(myCtrlDir, "SelectedTau_Rtau_AfterStandardSelections", "SelectedTau_Rtau_AfterStandardSelections;R_{#tau};N_{events} / 0.1", 120, 0., 1.2);
    hCtrlSelectedTauPAfterStandardSelections = makeTH<TH1F>(myCtrlDir, "SelectedTau_p_AfterStandardSelections", "SelectedTau_p_AfterStandardSelections;#tau p, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlSelectedTauLeadingTrkPAfterStandardSelections = makeTH<TH1F>(myCtrlDir, "SelectedTau_LeadingTrackP_AfterStandardSelections", "SelectedTau_LeadingTrackP_AfterStandardSelections;#tau ldg.ch.particle p, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlIdentifiedElectronPtAfterStandardSelections = makeTH<TH1F>(myCtrlDir, "IdentifiedElectronPt_AfterStandardSelections", "IdentifiedElectronPt_AfterStandardSelections;Identified electron p_{T}, GeV/c;N_{events} / 1 GeV", 20, 0., 20.);;
    hCtrlIdentifiedMuonPtAfterStandardSelections = makeTH<TH1F>(myCtrlDir, "IdentifiedMuonPt_AfterStandardSelections", "IdentifiedMuonPt_AfterStandardSelections;Identified muon p_{T}, GeV/c;N_{events} / 1 GeV", 20, 0., 20.);
    hCtrlNjetsAfterStandardSelections = makeTH<TH1F>(myCtrlDir, "Njets_AfterStandardSelections", "Njets_AfterStandardSelections;Number of selected jets;N_{events}", 7, 3., 10.);
    hCtrlMET = makeTH<TH1F>(myCtrlDir, "MET", "MET;MET, GeV;N_{events} / 10 GeV", 100, 0., 500.);
    hCtrlNbjets = makeTH<TH1F>(myCtrlDir, "NBjets", "NBjets;Number of identified b-jets;N_{events}", 10, 0., 10.);

    fTree.init(*fs);
  }

  SignalAnalysis::~SignalAnalysis() { }

  void SignalAnalysis::produces(edm::EDFilter *producer) const {
    if(fProduce) {
      producer->produces<std::vector<pat::Tau> >("selectedTaus");
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
    std::pair<double, size_t> weightSize = fVertexWeight.getWeightAndSize(iEvent, iSetup);
    if(!iEvent.isRealData()) {
      fEventWeight.multiplyWeight(weightSize.first);
      fTree.setPileupWeight(weightSize.first);
    }
    int nVertices = weightSize.second;
    hVerticesBeforeWeight->Fill(nVertices);
    hVerticesAfterWeight->Fill(nVertices, fEventWeight.getWeight());
    fTree.setNvertices(nVertices);

    increment(fAllCounter);
    
//------ Apply trigger and HLT_MET cut or trigger parametrisation
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);
    hSelectionFlow->Fill(kSignalOrderTrigger, fEventWeight.getWeight());
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderTrigger, fEventWeight.getWeight());
    hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderTrigger, fEventWeight.getWeight());
    if(triggerData.hasTriggerPath()) // protection if TriggerSelection is disabled
      fTree.setHltTaus(triggerData.getTriggerTaus());

    hVerticesTriggeredBeforeWeight->Fill(weightSize.second);
    hVerticesTriggeredAfterWeight->Fill(weightSize.second, fEventWeight.getWeight());

//------ GenParticle analysis (must be done here when we effectively trigger all MC)
    if (!iEvent.isRealData()) {
      GenParticleAnalysis::Data genData = fGenparticleAnalysis.analyze(iEvent, iSetup);
      fTree.setGenMET(genData.getGenMET());
    }

//------ Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    //hSelectionFlow->Fill(kSignalOrderVertexSelection, fEventWeight.getWeight());

//------ TauID
    // Store weight of event
    // TauID
    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return false; // Require at least one tau
    // plot leading track without pt cut
    hSelectedTauLeadingTrackPt->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt(), fEventWeight.getWeight());
    increment(fTausExistCounter);
    if(tauData.getSelectedTaus().size() != 1) return false; // Require exactly one tau
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
    TriggerEfficiencyScaleFactor::Data triggerWeight = fTriggerEfficiencyScaleFactor.applyEventWeight(*(tauData.getSelectedTau()), iEvent.isRealData());
    fTree.setTriggerWeight(triggerWeight.getEventWeight(), triggerWeight.getEventWeightAbsoluteUncertainty());
    increment(fTriggerScaleFactorCounter);
    hSelectionFlow->Fill(kSignalOrderTauID, fEventWeight.getWeight());
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderTauID, fEventWeight.getWeight());
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderTauID, fEventWeight.getWeight());
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Tau> > saveTaus(new std::vector<pat::Tau>());
      copyPtrToVector(tauData.getSelectedTaus(), *saveTaus);
      iEvent.put(saveTaus, "selectedTaus");
    }
    //    hSelectedTauRtau->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());  
    if (!myFakeTauStatus)
      increment(fGenuineTauCounter);

    // For plotting Rtau
    //    if (!tauData.selectedTauPassedRtau()) return false;
    //    if (tauData.getRtauOfSelectedTau() < 0.7) return false;
    hSelectedTauLeadingTrackPt->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt(), fEventWeight.getWeight());
    hSelectedTauEt->Fill(tauData.getSelectedTau()->pt(), fEventWeight.getWeight());
    hSelectedTauEta->Fill(tauData.getSelectedTau()->eta(), fEventWeight.getWeight());
    hSelectedTauPhi->Fill(tauData.getSelectedTau()->phi(), fEventWeight.getWeight());


    fAllTausCounterGroup.incrementOneTauCounter();
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderTauID, tauData);
    if (myTauMatch == FakeTauIdentifier::kkElectronToTau)
      hEMFractionElectrons->Fill(tauData.getSelectedTau()->emFraction(), fEventWeight.getWeight());
    hEMFractionAll->Fill(tauData.getSelectedTau()->emFraction(), fEventWeight.getWeight());



  
//------ Veto against second tau in event
    VetoTauSelection::Data vetoTauData = fVetoTauSelection.analyze(iEvent, iSetup, tauData.getSelectedTau());
    //    if (vetoTauData.passedEvent()) return false;
    //    increment(fVetoTauCounter);
    if (!vetoTauData.passedEvent()) increment(fVetoTauCounter);

//------ Global electron veto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    hCtrlIdentifiedElectronPt->Fill(electronVetoData.getSelectedElectronPtBeforePtCut(), fEventWeight.getWeight());
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);   
    hSelectionFlow->Fill(kSignalOrderElectronVeto, fEventWeight.getWeight());
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderElectronVeto, fEventWeight.getWeight());
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderElectronVeto, fEventWeight.getWeight());
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderElectronVeto, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Electron> > saveElectrons(new std::vector<pat::Electron>());
      copyPtrToVector(electronVetoData.getSelectedElectrons(), *saveElectrons);
      iEvent.put(saveElectrons, "selectedVetoElectrons");
    }


//------ Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    hCtrlIdentifiedMuonPt->Fill(muonVetoData.getSelectedMuonPtBeforePtCut(), fEventWeight.getWeight());
    if (!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);
    hSelectionFlow->Fill(kSignalOrderMuonVeto, fEventWeight.getWeight());
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderMuonVeto, fEventWeight.getWeight());
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderMuonVeto, fEventWeight.getWeight());
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
    hCtrlNjets->Fill(jetData.getHadronicJetCount(), fEventWeight.getWeight());
    if(!jetData.passedEvent()) return false;
    increment(fNJetsCounter);
    hSelectionFlow->Fill(kSignalOrderJetSelection, fEventWeight.getWeight());
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderJetSelection, fEventWeight.getWeight());
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderJetSelection, fEventWeight.getWeight());
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
    hCtrlSelectedTauRtauAfterStandardSelections->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());
    hCtrlSelectedTauLeadingTrkPtAfterStandardSelections->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt(), fEventWeight.getWeight());
    hCtrlSelectedTauPtAfterStandardSelections->Fill(tauData.getSelectedTau()->pt(), fEventWeight.getWeight());
    hCtrlSelectedTauEtaAfterStandardSelections->Fill(tauData.getSelectedTau()->eta(), fEventWeight.getWeight());
    hCtrlSelectedTauPhiAfterStandardSelections->Fill(tauData.getSelectedTau()->phi(), fEventWeight.getWeight());
    hCtrlSelectedTauEtaVsPhiAfterStandardSelections->Fill(tauData.getSelectedTau()->eta(), tauData.getSelectedTau()->phi(), fEventWeight.getWeight());
    hCtrlSelectedTauPAfterStandardSelections->Fill(tauData.getSelectedTau()->p(), fEventWeight.getWeight());
    hCtrlSelectedTauLeadingTrkPAfterStandardSelections->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->p(), fEventWeight.getWeight());
    hCtrlIdentifiedElectronPtAfterStandardSelections->Fill(electronVetoData.getSelectedElectronPtBeforePtCut(), fEventWeight.getWeight());
    hCtrlIdentifiedMuonPtAfterStandardSelections->Fill(muonVetoData.getSelectedMuonPtBeforePtCut(), fEventWeight.getWeight());
    hCtrlNjetsAfterStandardSelections->Fill(jetData.getHadronicJetCount(), fEventWeight.getWeight());


//------ MET cut
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getAllJets());
    hMet->Fill(metData.getSelectedMET()->et(),fEventWeight.getWeight()); 
    hCtrlMET->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    if(!metData.passedEvent()) return false;
    increment(fMETCounter);
    hSelectionFlow->Fill(kSignalOrderMETSelection, fEventWeight.getWeight());
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderMETSelection, fEventWeight.getWeight());
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderMETSelection, fEventWeight.getWeight());
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderMETSelection, tauData);


//------ b tagging cut
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
    hCtrlNbjets->Fill(btagData.getBJetCount(), fEventWeight.getWeight());
    if(!btagData.passedEvent()) return false;
    increment(fBTaggingCounter);
    // Apply scale factor as weight to event
    if (!iEvent.isRealData()) {
      btagData.fillScaleFactorHistograms(); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
    increment(fBTaggingScaleFactorCounter);
    hSelectionFlow->Fill(kSignalOrderBTagSelection, fEventWeight.getWeight());
    hSelectionFlowVsVertices->Fill(nVertices, kSignalOrderBTagSelection, fEventWeight.getWeight());
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderBTagSelection, fEventWeight.getWeight());
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderBTagSelection, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveBJets(new std::vector<pat::Jet>());
      copyPtrToVector(btagData.getSelectedJets(), *saveBJets);
      iEvent.put(saveBJets, "selectedBJets");
    }


//------ Delta phi(tau,MET) cut
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    hDeltaPhi->Fill(deltaPhi, fEventWeight.getWeight());
    if (deltaPhi > fDeltaPhiCutValue) return false;
    increment(fDeltaPhiTauMETCounter);
    hSelectionFlow->Fill(kSignalOrderDeltaPhiSelection, fEventWeight.getWeight());
    if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderDeltaPhiSelection, fEventWeight.getWeight());
    fillEWKFakeTausCounters(myTauMatch, kSignalOrderDeltaPhiSelection, tauData);

    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()) );

//------ Top reconstruction

    // Top reco, no event cut

   // top mass with possible event cuts
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    if (TopSelectionData.passedEvent() ) {
      increment(fTopSelectionCounter);
      //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());
      //        if(transverseMass > 80 ) increment(ftransverseMassCut100TopCounter);
      hTransverseMassTopSelection->Fill(transverseMass, fEventWeight.getWeight());     
    }

    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    if (TopChiSelectionData.passedEvent() ) {
      double topmass = TopChiSelectionData.getTopMass();
      increment(fTopChiSelectionCounter);
      if (topmass < 220 ) increment(fTopChiSelectionNarrowCounter);
      //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
      hTransverseMassTopChiSelection->Fill(transverseMass, fEventWeight.getWeight());
    }

    bool myTopRecoWithWSelectionStatus = false;
    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());
    if (BjetSelectionData.passedEvent() ) {
      TopWithBSelection::Data TopWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());
      TopWithWSelection::Data TopWithWSelectionData = fTopWithWSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());
      if (TopWithBSelectionData.passedEvent() ) {
        increment(fTopWithBSelectionCounter);
        //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
        //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
        hTransverseMassTopBjetSelection->Fill(transverseMass, fEventWeight.getWeight()); 
        //if(transverseMass > 70 ) increment(ftransverseMass70TopWithBSelCounter); 
        //if(transverseMass > 80 ) increment(ftransverseMass80TopWithBSelCounter);   
      }

      if (TopWithWSelectionData.passedEvent() ) {
        myTopRecoWithWSelectionStatus = true;
        increment(fTopWithWSelectionCounter);
        //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
        //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
        hTransverseMassTopWithWSelection->Fill(transverseMass, fEventWeight.getWeight()); 
        //if(transverseMass > 70 ) increment(ftransverseMass70TopWithWSelCounter); 
        //if(transverseMass > 80 ) increment(ftransverseMass80TopWithWSelCounter);   
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
    hTransverseMass->Fill(transverseMass, fEventWeight.getWeight());
    if (myFakeTauStatus) hEWKFakeTausTransverseMass->Fill(transverseMass, fEventWeight.getWeight());
    fSFUncertaintiesAfterSelection.setScaleFactorUncertainties(fEventWeight.getWeight(),
                                                               triggerWeight.getEventWeight(), triggerWeight.getEventWeightAbsoluteUncertainty(),
                                                               btagData.getScaleFactor(), btagData.getScaleFactorAbsoluteUncertainty());

//------ Experimental cuts, counters, and histograms

    if (!iEvent.isRealData()) {
      edm::Handle <reco::GenParticleCollection> genParticles;
      iEvent.getByLabel("genParticles", genParticles);
      bool myTauFoundStatus = false;
      bool myLeptonVetoStatus = false;
      for (size_t i=0; i < genParticles->size(); ++i) {
	const reco::Candidate & p = (*genParticles)[i];
	if (std::abs(p.pdgId()) == 11 || std::abs(p.pdgId()) == 13 || std::abs(p.pdgId()) == 15) {
	  // Check match with tau
	  if (reco::deltaR(p, tauData.getSelectedTau()->p4()) < 0.3) {
	    if (p.pt() > 5.) {
              // match found
	      if (std::abs(p.pdgId()) == 11 || std::abs(p.pdgId()) == 13) {
		myLeptonVetoStatus = true;
		i = genParticles->size(); // finish loop
	      }
	      if (std::abs(p.pdgId()) == 15) myTauFoundStatus = true;
	    }
	  }
	}
      }
      if (myTauFoundStatus && !myLeptonVetoStatus) {
	increment(fRealTauAfterDeltaPhiCounter);
	if (!vetoTauData.passedEvent()) increment(fRealTauAfterDeltaPhiTauVetoCounter);
      }
    }

    if (!vetoTauData.passedEvent()) {
      increment(fTauVetoAfterDeltaPhiCounter);
      hTransverseMassTauVeto->Fill(transverseMass, fEventWeight.getWeight()); 
    }



    // plot deltaPhi(jet,met)
    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetData.getSelectedJets().begin(); iJet != jetData.getSelectedJets().end(); ++iJet) {
      double jetDeltaPhi = DeltaPhi::reconstruct(**iJet, *(metData.getSelectedMET()));
      hDeltaPhiJetMet->Fill(jetDeltaPhi*57.3, fEventWeight.getWeight());
    }


    // Calculate alphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTau()), jetData.getSelectedJets());   

    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());



     

/*    int njets30 = 0;
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jetData.getSelectedJets().begin(); iter != jetData.getSelectedJets().end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;
      if (iJet->pt() < 30) continue;
      njets30++;
    }*/




    /*   
    // Fake MET veto a.k.a. further QCD suppression
    //    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup,  tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());
    if (fakeMETData.passedEvent() ) {
      increment(fFakeMETVetoCounter);
      
    */
      
    //hSelectionFlow->Fill(kSignalOrderFakeMETVeto, fEventWeight.getWeight());

    //fillEWKFakeTausCounters(myTauMatch, kSignalOrderFakeMETVeto, tauData);


    //fillEWKFakeTausCounters(myTauMatch, kSignalOrderFakeMETVeto, tauData);
    
/*    if(transverseMass > 70 ) {
      increment(ftransverseMassCut70Counter);
      if (!vetoTauData.passedEvent()) increment(ftransverseMass70TauVetoCounter);
      if (TopChiSelectionData.passedEvent() )  increment(ftransverseMass70TopChiSelCounter);
      //      if (TopWithBSelectionData.passedEvent() )  increment(ftransverseMass70TopWithBSelCounter);
      if (TopSelectionData.passedEvent() )  increment(ftransverseMass70TopSelCounter);
    }
    if(transverseMass > 80 ) {
      increment(ftransverseMassCut80Counter);
      if (!vetoTauData.passedEvent()) increment(ftransverseMass80TauVetoCounter);
      if (TopChiSelectionData.passedEvent() )  increment(ftransverseMass80TopChiSelCounter);
      //      if (TopWithBSelectionData.passedEvent() )  increment(ftransverseMass80TopWithBSelCounter);
      if (TopSelectionData.passedEvent() )  increment(ftransverseMass80TopSelCounter);
    }
*/
    // Correlation analysis
    fCorrelationAnalysis.analyze(tauData.getSelectedTaus(), btagData.getSelectedJets());
    // Alpha T
    //if(!evtTopologyData.passedEvent()) return false;
    hAlphaT->Fill(evtTopologyData.alphaT().fAlphaT, fEventWeight.getWeight()); // FIXME: move this histogramming to evt topology

    // Forward jet veto
    //    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    //    if (!forwardJetData.passedEvent()) return false;
    //    increment(fForwardJetVetoCounter);

    //std::cout << "run=" << iEvent.id().run() << " lumiblock=" << iEvent.id().luminosityBlock() << " event=" << iEvent.id().event() << ", mT=" << transverseMass << std::endl;

//------- Control plots
    hSelectedTauRtauAfterCuts->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());
    hSelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt(), fEventWeight.getWeight());
    hSelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta(), fEventWeight.getWeight());
    hMetAfterCuts->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());

    return true;
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
        hEWKFakeTausSelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt(), fEventWeight.getWeight());
        hEWKFakeTausSelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta(), fEventWeight.getWeight());
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
}
