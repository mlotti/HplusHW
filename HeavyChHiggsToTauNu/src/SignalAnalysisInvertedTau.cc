#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisInvertedTau.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

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
  SignalAnalysisInvertedTau::CounterGroup::CounterGroup(EventCounter& eventCounter) :
    fOneTauCounter(eventCounter.addCounter("nonQCDType2:taus == 1")),
    fElectronVetoCounter(eventCounter.addCounter("nonQCDType2:electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("nonQCDType2:muon veto")),
    fMETCounter(eventCounter.addCounter("nonQCDType2:MET")),
    fNJetsCounter(eventCounter.addCounter("nonQCDType2:njets")),
    fBTaggingCounter(eventCounter.addCounter("nonQCDType2:btagging")),
    fFakeMETVetoCounter(eventCounter.addCounter("nonQCDType2:fake MET veto")),
    fTopSelectionCounter(eventCounter.addCounter("nonQCDType2:Top Selection cut")),
    fTopChiSelectionCounter(eventCounter.addCounter("nonQCDType2:Top ChiSelection cut")),
    fTopWithBSelectionCounter(eventCounter.addCounter("nonQCDType2:Top WithBSelection cut")) { }
  SignalAnalysisInvertedTau::CounterGroup::CounterGroup(EventCounter& eventCounter, std::string prefix) :
    fOneTauCounter(eventCounter.addSubCounter(prefix,":taus == 1")),
    fElectronVetoCounter(eventCounter.addSubCounter(prefix,":electron veto")),
    fMuonVetoCounter(eventCounter.addSubCounter(prefix,":muon veto")),
    fMETCounter(eventCounter.addSubCounter(prefix,":MET")),
    fNJetsCounter(eventCounter.addSubCounter(prefix,":njets")),
    fBTaggingCounter(eventCounter.addSubCounter(prefix,":btagging")),
    fFakeMETVetoCounter(eventCounter.addSubCounter(prefix,":fake MET veto")),
    fTopSelectionCounter(eventCounter.addSubCounter(prefix,":Top Selection cut")),
    fTopChiSelectionCounter(eventCounter.addSubCounter(prefix,":Top ChiSelection cut")),
    fTopWithBSelectionCounter(eventCounter.addSubCounter(prefix,":Top WithBSelection cut")) { }
  SignalAnalysisInvertedTau::CounterGroup::~CounterGroup() { }

  SignalAnalysisInvertedTau::SignalAnalysisInvertedTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    fHistoWrapper(eventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
    bBlindAnalysisStatus(iConfig.getUntrackedParameter<bool>("blindAnalysisStatus")),
    fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fAllCounter(eventCounter.addCounter("All events")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),
    fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
    fTausExistCounter(eventCounter.addCounter("taus > 0")),
    fBaselineTauIDCounter(eventCounter.addCounter("Baseline,taus == 1")),
    fBaselineEvetoCounter(eventCounter.addCounter("Baseline,electron veto")),
    fBaselineMuvetoCounter(eventCounter.addCounter("Baseline,muon veto")),
    fBaselineJetsCounter(eventCounter.addCounter("Baseline, njets")),
    fBaselineMetCounter(eventCounter.addCounter("Baseline, MET")),
    fBaselineBtagCounter(eventCounter.addCounter("Baseline, btagging")),
    fBaselineDeltaPhiTauMETCounter(eventCounter.addCounter("Baseline,DeltaPhi(Tau,MET) upper limit")),
    fBaselineDphi160Counter(eventCounter.addCounter("Baseline, deltaPhi160")),
    fBaselineDphi130Counter(eventCounter.addCounter("Baseline, deltaPhi130")),
    fBaselineTopChiSelectionCounter(eventCounter.addCounter("Top BaselineChiSelection cut")),
    fOneTauCounter(eventCounter.addCounter("taus == 1")),
    fTriggerScaleFactorCounter(eventCounter.addCounter("trigger scale factor")),
    fTauVetoAfterTauIDCounter(eventCounter.addCounter("Veto on isolated taus")),
    fNprongsAfterTauIDCounter(eventCounter.addCounter("Nprongs for best candidate")),
    fRtauAfterTauIDCounter(eventCounter.addCounter("RtauAfterTauID")),
    fElectronVetoCounter(eventCounter.addCounter("electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("muon veto")),
    fNJetsCounter(eventCounter.addCounter("njets")),
    fBTaggingBeforeMETCounter(eventCounter.addCounter("btagging before MET")),
    fMETCounter(eventCounter.addCounter("MET")),
    fBjetVetoCounter(eventCounter.addCounter("Veto on hard b jets")),
    fBTaggingCounter(eventCounter.addCounter("btagging")),
    fdeltaPhiTauMET10Counter(eventCounter.addCounter("deltaPhiTauMET lower limit")),
    fDeltaPhiTauMETCounter(eventCounter.addCounter("DeltaPhi(Tau,MET) upper limit")),
    //    fDeltaPhiTauMET140Counter(eventCounter.addCounter("DeltaPhi(Tau,MET) upper limit 140")),
    fHiggsMassCutCounter(eventCounter.addCounter("HiggsMassCut")),
    fdeltaPhiTauMET160Counter(eventCounter.addCounter("deltaPhiTauMET160 limit")),
    fdeltaPhiTauMET130Counter(eventCounter.addCounter("deltaPhiTauMET130 limit")),
    fFakeMETVetoCounter(eventCounter.addCounter("fake MET veto")),
    fdeltaPhiTauMET160FakeMetCounter(eventCounter.addCounter("deltaPhi160 and fake MET veto")),
    fTopRtauDeltaPhiFakeMETCounter(eventCounter.addCounter("TopRtauDeltaPhiFakeMET cuts")),
    fRtauAfterCutsCounter(eventCounter.addCounter("RtauAfterCuts")),
    fForwardJetVetoCounter(eventCounter.addCounter("forward jet veto")),
    ftransverseMassCut80Counter(eventCounter.addCounter("transverseMass > 60")),
    ftransverseMassCut100Counter(eventCounter.addCounter("transverseMass > 80")),
    ftransverseMassCut80NoRtauCounter(eventCounter.addCounter("transverseMass > 60 no Rtau")),
    ftransverseMassCut100NoRtauCounter(eventCounter.addCounter("transverseMass > 80 no Rtau")),
    fZmassVetoCounter(eventCounter.addCounter("ZmassVetoCounter")),
    fTopSelectionCounter(eventCounter.addCounter("Top Selection cut")),
    fTopChiSelectionCounter(eventCounter.addCounter("Top ChiSelection cut")),
    fTopWithBSelectionCounter(eventCounter.addCounter("Top with B Selection cut")),
    ftransverseMassCut100TopCounter(eventCounter.addCounter("transverseMass > 100 top cut")),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, fHistoWrapper),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, fHistoWrapper),
    /////////////    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, fHistoWrapper),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, fHistoWrapper, "MET"),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, fHistoWrapper),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, fHistoWrapper),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, fHistoWrapper),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, fHistoWrapper),
    fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, fHistoWrapper),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, fHistoWrapper),
    fFullHiggsMassCalculator(eventCounter, fHistoWrapper),
    //    ftransverseMassCut(iConfig.getUntrackedParameter<edm::ParameterSet>("transverseMassCut")),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, fHistoWrapper),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, fHistoWrapper),
    fCorrelationAnalysis(eventCounter, fHistoWrapper),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, fHistoWrapper),
    fTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiencyScaleFactor"), fHistoWrapper),
    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), fHistoWrapper, "TauID"),
    fVertexWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeightReader")),
    fTree(iConfig.getUntrackedParameter<edm::ParameterSet>("Tree"), fBTagging.getDiscriminator()),
    // Non-QCD Type II related
    fNonQCDTypeIIGroup(eventCounter),
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
    fProduce(iConfig.getUntrackedParameter<bool>("produceCollections", false))
  {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms filled in the analysis body

    hVerticesBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesBeforeWeight", "Number of vertices without weighting", 30, 0, 30);
    hVerticesAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesAfterWeight", "Number of vertices with weighting", 30, 0, 30);
    hVerticesTriggeredBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesTriggeredBeforeWeight", "Number of vertices without weighting", 30, 0, 30);
    hVerticesTriggeredAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesTriggeredAfterWeight", "Number of vertices with weighting", 30, 0, 30);
    //    hmetAfterTrigger = fHistoWrapper.makeTH<TH1F>(*fs, "metAfterTrigger", "metAfterTrigger", 50, 0., 200.);
    hTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassWithTopCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassWithTopCut", "transverseMassWithTopCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassAfterVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassAfterVeto", "transverseMassAfterVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassBeforeVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassBeforeVeto", "transverseMassBeforeVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassNoMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassNoMet", "transverseMassNoMet;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassNoMetBtag = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassNoMetBtag", "transverseMassNoMetBtag;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassBeforeFakeMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassBeforeFakeMet", "transverseMassBeforeFakeMet;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassDeltaPhiUpperCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassDeltaPhiUpperCut", "transverseMassDeltaPhiUpperCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);


    hTransverseMassDeltaPhi160 =  fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassDeltaPhi160", "transverseMassDeltaPhi160;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.); 
    hTransverseMassDeltaPhi130 =  fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMassDeltaPhi130", "transverseMassDeltaPhi130;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassFakeMET =  fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassFakeMET", "transverseMassFakeMET;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassTopChiSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassTopChiSelection", "transverseMassTopChiSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassTopBjetSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassTopBjetSelection", "transverseMassTopBjetSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hDeltaPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 360, 0., 180.);
    hDeltaPhiJetMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "deltaPhiJetMet", "deltaPhiJetMet", 400, 0., 3.2);  
    hAlphaT = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "alphaT", "alphaT", 100, 0.0, 5.0);
    hAlphaTInvMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);    
    hAlphaTVsRtau = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kDebug, *fs, "alphaT(y)-Vs-Rtau(x)", "alphaT-Vs-Rtau",  120, 0.0, 1.2, 500, 0.0, 5.0);
    hMet_AfterBTagging = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "MET_AfterBTagging", "MET_AfterBTagging;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);

    
    hMETBeforeMETCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BeforeMETCut", "MET_BeforeMETCut;PF MET, GeV;N_{events} / 10 GeV", 80, 0.0, 400.0);
    hSelectedTauEt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_pT_AfterTauID", "SelectedTau_pT_AfterTauID;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    //    hSelectedTauEtMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_pT_AfterTauID_MetCut", "SelectedTau_pT_AfterTauID_MetCut;#tau p_{T}, GeV/c;N_{events / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_eta_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.1", 300, -3.0, 3.0);
    hSelectedTauEtAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_pT_AfterCuts", "SelectedTau_pT_AfterCuts;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 40, 0.0, 400.0);
    hSelectedTauEtaAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_eta_AfterCuts", "SelectedTau_eta_AfterCuts;#tau #eta;N_{events} / 0.1", 30, -3.0, 3.0);
    hSelectedTauPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_phi_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_Rtau_AfterTauID", "SelectedTau_Rtau_AfterTauID;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);
    hSelectedTauRtauAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_Rtau_AfterCuts", "SelectedTau_Rtau_AfterCuts;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);
    hSelectedTauLeadingTrackPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_TauLeadingTrackPt", "SelectedTau_TauLeadingTrackPt;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauLeadingTrackPtMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_TauLeadingTrackPt_MetCut", "SelectedTau_TauLeadingTrackPt_MetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);

    hMetAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "Met_AfterCuts", "Met_AfterCuts", 500, 0.0, 500.0);
    hMETBeforeTauId = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "Met_BeforeTauId", "Met_BeforeTauId", 500, 0.0, 500.0);
    hMETBaselineTauId = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs,"MET_BaseLineTauId", "MET_BaseLineTauId;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauId = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauId", "MET_InvertedTauId;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    //    TauIdJets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets", "MET_BaseLineTauIdJets;PF MET", 400, 0.0, 400.0);

    hMETBaselineTauIdJets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets", "MET_BaseLineTauIdJets", 400, 0.0, 400.0);
    hMETBaselineTauIdJets120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets120", "MET_BaseLineTauIdJets120", 400, 0.0, 400.0);
    hMETBaselineTauIdJets150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets150", "MET_BaseLineTauIdJets150", 400, 0.0, 400.0);
    hMETBaselineTauIdJets120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets120150", "MET_BaseLineTauIdJets120150;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets100120", "MET_BaseLineTauIdJets100120;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets80100", "MET_BaseLineTauIdJets80100;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets7080", "MET_BaseLineTauIdJets7080;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets6070", "MET_BaseLineTauIdJets6070;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets5060", "MET_BaseLineTauIdJets5060;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets4050", "MET_BaseLineTauIdJets4050;PF MET", 400, 0.0, 400.0);
    
    hMETBaselineTauIdBtag = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag", "MET_BaseLineTauIdBtag;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag150", "MET_BaseLineTauIdBtag150;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag120", "MET_BaseLineTauIdBtag120;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag120150", "MET_BaseLineTauIdBtag120150;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag100120", "MET_BaseLineTauIdBtag100120;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag80100", "MET_BaseLineTauIdBtag80100;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag7080", "MET_BaseLineTauIdBtag7080;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag6070", "MET_BaseLineTauIdBtag6070;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag5060", "MET_BaseLineTauIdBtag5060;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag4050", "MET_BaseLineTauIdBtag4050;PF MET", 400, 0.0, 400.0);


    hMETBaselineTauIdBveto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto", "MET_BaseLineTauIdBveto;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBveto150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto150", "MET_BaseLineTauIdBveto150;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBveto120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto120", "MET_BaseLineTauIdBveto120;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBveto120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto120150", "MET_BaseLineTauIdBveto120150;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBveto100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto100120", "MET_BaseLineTauIdBveto100120;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBveto80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto80100", "MET_BaseLineTauIdBveto80100;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBveto7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto7080", "MET_BaseLineTauIdBveto7080;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBveto6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto6070", "MET_BaseLineTauIdBveto6070;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBveto5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto5060", "MET_BaseLineTauIdBveto5060;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBveto4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto4050", "MET_BaseLineTauIdBveto4050;PF MET", 400, 0.0, 400.0);
  
    hMTBaselineTauIdJet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdJet", "MTBaseLineTauIdJet", 400, 0., 400.);
    hMTBaselineTauIdJet150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdJet150", "MTBaseLineTauIdJet150", 400, 0., 400.);
    hMTBaselineTauIdJet120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdJet120", "MTBaseLineTauIdJet120", 400, 0., 400.);
    hMTBaselineTauIdJet120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdJet120150", "MTBaseLineTauIdJet120150", 400, 0., 400.);
    hMTBaselineTauIdJet100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdJet100120", "MTBaseLineTauIdJet100120", 400, 0., 400.);
    hMTBaselineTauIdJet80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdJet80100", "MTBaseLineTauIdJet80100", 400, 0., 400.);
    hMTBaselineTauIdJet7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdJet7080", "MTBaseLineTauIdJet7080", 400, 0., 400.);
    hMTBaselineTauIdJet6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdJet6070", "MTBaseLineTauIdJet6070", 400, 0., 400.);
    hMTBaselineTauIdJet5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdJet5060", "MTBaseLineTauIdJet5060", 400, 0., 400.);
    hMTBaselineTauIdJet4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdJet4050", "MTBaseLineTauIdJet4050", 400, 0., 400.);
  
     hMTBaselineTauIdBtag = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBtag", "MTBaseLineTauIdBtag;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMTBaselineTauIdBtag150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBtag150", "MTBaseLineTauIdBtag150", 400, 0., 400.);
    hMTBaselineTauIdBtag120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBtag120", "MTBaseLineTauIdBtag120", 400, 0., 400.);
    hMTBaselineTauIdBtag120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBtag120150", "MTBaseLineTauIdBtag120150", 400, 0., 400.);
    hMTBaselineTauIdBtag100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBtag100120", "MTBaseLineTauIdBtag100120", 400, 0., 400.);
    hMTBaselineTauIdBtag80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBtag80100", "MTBaseLineTauIdBtag80100", 400, 0., 400.);
    hMTBaselineTauIdBtag7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBtag7080", "MTBaseLineTauIdBtag7080", 400, 0., 400.);
    hMTBaselineTauIdBtag6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBtag6070", "MTBaseLineTauIdBtag6070", 400, 0., 400.);
    hMTBaselineTauIdBtag5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBtag5060", "MTBaseLineTauIdBtag5060", 400, 0., 400.);
    hMTBaselineTauIdBtag4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBtag4050", "MTBaseLineTauIdBtag4050", 400, 0., 400.);

    hMTBaselineTauIdPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdPhi", "MTBaseLineTauIdPhi;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMTBaselineTauIdPhi150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdPhi150", "MTBaseLineTauIdPhi150", 400, 0., 400.);
    hMTBaselineTauIdPhi120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdPhi120", "MTBaseLineTauIdPhi120", 400, 0., 400.);
    hMTBaselineTauIdPhi120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdPhi120150", "MTBaseLineTauIdPhi120150", 400, 0., 400.);
    hMTBaselineTauIdPhi100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdPhi100120", "MTBaseLineTauIdPhi100120", 400, 0., 400.);
    hMTBaselineTauIdPhi80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdPhi80100", "MTBaseLineTauIdPhi80100", 400, 0., 400.);
    hMTBaselineTauIdPhi7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdPhi7080", "MTBaseLineTauIdPhi7080", 400, 0., 400.);
    hMTBaselineTauIdPhi6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdPhi6070", "MTBaseLineTauIdPhi6070", 400, 0., 400.);
    hMTBaselineTauIdPhi5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdPhi5060", "MTBaseLineTauIdPhi5060", 400, 0., 400.);
    hMTBaselineTauIdPhi4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdPhi4050", "MTBaseLineTauIdPhi4050", 400, 0., 400.);

    hMTBaselineTauIdTopMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdTopMass", "MTBaseLineTauIdTopMass", 400, 0., 400.);
    hMTBaselineTauIdTopMass150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdTopMass150", "MTBaseLineTauIdTopMass150", 400, 0., 400.);
    hMTBaselineTauIdTopMass120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdTopMass120", "MTBaseLineTauIdTopMass120", 400, 0., 400.);
    hMTBaselineTauIdTopMass120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdTopMass120150", "MTBaseLineTauIdTopMass120150", 400, 0., 400.);
    hMTBaselineTauIdTopMass100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdTopMass100120", "MTBaseLineTauIdTopMass100120", 400, 0., 400.);
    hMTBaselineTauIdTopMass80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdTopMass80100", "MTBaseLineTauIdTopMass80100", 400, 0., 400.);
    hMTBaselineTauIdTopMass7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdTopMass7080", "MTBaseLineTauIdTopMass7080", 400, 0., 400.);
    hMTBaselineTauIdTopMass6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdTopMass6070", "MTBaseLineTauIdTopMass6070", 400, 0., 400.);
    hMTBaselineTauIdTopMass5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdTopMass5060", "MTBaseLineTauIdTopMass5060", 400, 0., 400.);
    hMTBaselineTauIdTopMass4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdTopMass4050", "MTBaseLineTauIdTopMass4050", 400, 0., 400.);

   
    hMTInvertedTauIdJet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJet", "MTInvertedTauIdJet", 400, 0., 400.);
    hMTInvertedTauIdJet150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJet150", "MTInvertedTauIdJet150", 400, 0., 400.);
    hMTInvertedTauIdJet120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJet120", "MTInvertedTauIdJet120", 400, 0., 400.);
    hMTInvertedTauIdJet120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJet120150", "MTInvertedTauIdJet120150", 400, 0., 400.);
    hMTInvertedTauIdJet100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJet100120", "MTInvertedTauIdJet100120", 400, 0., 400.);
    hMTInvertedTauIdJet80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJet80100", "MTInvertedTauIdJet80100", 400, 0., 400.);
    hMTInvertedTauIdJet7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJet7080", "MTInvertedTauIdJet7080", 400, 0., 400.);
    hMTInvertedTauIdJet6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJet6070", "MTInvertedTauIdJet6070", 400, 0., 400.);
    hMTInvertedTauIdJet5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJet5060", "MTInvertedTauIdJet5060", 400, 0., 400.);
    hMTInvertedTauIdJet4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJet4050", "MTInvertedTauIdJet4050", 400, 0., 400.);

    hMTInvertedTauIdBtag = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBtag", "MTInvertedTauIdBtag", 400, 0., 400.);
    hMTInvertedTauIdBtag150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBtag150", "MTInvertedTauIdBtag150", 400, 0., 400.);
    hMTInvertedTauIdBtag120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBtag120", "MTInvertedTauIdBtag120", 400, 0., 400.);
    hMTInvertedTauIdBtag120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBtag120150", "MTInvertedTauIdBtag120150", 400, 0., 400.);
    hMTInvertedTauIdBtag100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBtag100120", "MTInvertedTauIdBtag100120", 400, 0., 400.);
    hMTInvertedTauIdBtag80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBtag80100", "MTInvertedTauIdBtag80100", 400, 0., 400.);
    hMTInvertedTauIdBtag7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBtag7080", "MTInvertedTauIdBtag7080", 400, 0., 400.);
    hMTInvertedTauIdBtag6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBtag6070", "MTInvertedTauIdBtag6070", 400, 0., 400.);
    hMTInvertedTauIdBtag5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBtag5060", "MTInvertedTauIdBtag5060", 400, 0., 400.);
    hMTInvertedTauIdBtag4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBtag4050", "MTInvertedTauIdBtag4050", 400, 0., 400.);

    hMTInvertedTauIdMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdMet", "MTInvertedTauIdMet", 400, 0., 400.);
    hMTInvertedTauIdMet150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdMet150", "MTInvertedTauIdMet150", 400, 0., 400.);
    hMTInvertedTauIdMet120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdMet120", "MTInvertedTauIdMet120", 400, 0., 400.);
    hMTInvertedTauIdMet120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdMet120150", "MTInvertedTauIdMet120150", 400, 0., 400.);
    hMTInvertedTauIdMet100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdMet100120", "MTInvertedTauIdMet100120", 400, 0., 400.);
    hMTInvertedTauIdMet80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdMet80100", "MTInvertedTauIdMet80100", 400, 0., 400.);
    hMTInvertedTauIdMet7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdMet7080", "MTInvertedTauIdMet7080", 400, 0., 400.);
    hMTInvertedTauIdMet6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdMet6070", "MTInvertedTauIdMet6070", 400, 0., 400.);
    hMTInvertedTauIdMet5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdMet5060", "MTInvertedTauIdMet5060", 400, 0., 400.);
    hMTInvertedTauIdMet4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdMet4050", "MTInvertedTauIdMet4050", 400, 0., 400.);

    hMTInvertedTauIdJetPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdPhi", "MTInvertedTauIdPhi", 400, 0., 400.);
    hMTInvertedTauIdJetPhi150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdPhi150", "MTInvertedTauIdPhi150", 400, 0., 400.);
    hMTInvertedTauIdJetPhi120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdPhi120", "MTInvertedTauIdPhi120", 400, 0., 400.);
    hMTInvertedTauIdJetPhi120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdPhi120150", "MTInvertedTauIdPhi120150", 400, 0., 400.);
    hMTInvertedTauIdJetPhi100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdPhi100120", "MTInvertedTauIdPhi100120", 400, 0., 400.);
    hMTInvertedTauIdJetPhi80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdPhi80100", "MTInvertedTauIdPhi80100", 400, 0., 400.);
    hMTInvertedTauIdJetPhi7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdPhi7080", "MTInvertedTauIdPhi7080", 400, 0., 400.);
    hMTInvertedTauIdJetPhi6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdPhi6070", "MTInvertedTauIdPhi6070", 400, 0., 400.);
    hMTInvertedTauIdJetPhi5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdPhi5060", "MTInvertedTauIdPhi5060", 400, 0., 400.);
    hMTInvertedTauIdJetPhi4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdPhi4050", "MTInvertedTauIdPhi4050", 400, 0., 400.);

    hTopMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TopMass", "TopMass", 400, 0., 400.);
    hTopMass150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TopMass150", "TopMass150", 400, 0., 400.);
    hTopMass120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TopMass120", "TopMass120", 400, 0., 400.);
    hTopMass120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TopMass120150", "TopMass120150", 400, 0., 400.);
    hTopMass100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TopMass100120", "TopMass100120", 400, 0., 400.);
    hTopMass80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TopMass80100", "TopMass80100", 400, 0., 400.);
    hTopMass7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TopMass7080", "TopMass7080", 400, 0., 400.);
    hTopMass6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TopMass6070", "TopMass6070", 400, 0., 400.);
    hTopMass5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TopMass5060", "TopMass5060", 400, 0., 400.);
    hTopMass4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TopMass4050", "TopMass4050", 400, 0., 400.);

    hHiggsMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass", "HiggsMass", 400, 0., 400.);
    hHiggsMass150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass150", "HiggsMass150", 400, 0., 400.);
    hHiggsMass120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass120", "HiggsMass120", 400, 0., 400.);
    hHiggsMass120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass120150", "HiggsMass120150", 400, 0., 400.);
    hHiggsMass100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass100120", "HiggsMass100120", 400, 0., 400.);
    hHiggsMass80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass80100", "HiggsMass80100", 400, 0., 400.);
    hHiggsMass7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggMass7080", "HiggsMass7080", 400, 0., 400.);
    hHiggsMass6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass6070", "HiggsMass6070", 400, 0., 400.);
    hHiggsMass5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass5060", "HiggsMass5060", 400, 0., 400.);
    hHiggsMass4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass4050", "HiggsMass4050", 400, 0., 400.);

    hHiggsMassPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi", "HiggsMassPhi", 400, 0., 400.);
    hHiggsMassPhi150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi150", "HiggsMassPhi150", 400, 0., 400.);
    hHiggsMassPhi120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi120", "HiggsMassPhi120", 400, 0., 400.);
    hHiggsMassPhi120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi120150", "HiggsMassPhi120150", 400, 0., 400.);
    hHiggsMassPhi100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi100120", "HiggsMassPhi100120", 400, 0., 400.);
    hHiggsMassPhi80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi80100", "HiggsMassPhi80100", 400, 0., 400.);
    hHiggsMassPhi7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi7080", "HiggsMassPhi7080", 400, 0., 400.);
    hHiggsMassPhi6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi6070", "HiggsMassPhi6070", 400, 0., 400.);
    hHiggsMassPhi5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi5060", "HiggsMassPhi5060", 400, 0., 400.);
    hHiggsMassPhi4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi4050", "HiggsMassPhi4050", 400, 0., 400.);

    hMTInvertedTauIdTopMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdTopMass", "MTInvertedTauIdTopMass", 400, 0., 400.);
    hMTInvertedTauIdTopMass150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdTopMass150", "MTInvertedTauIdTopMass150", 400, 0., 400.);
    hMTInvertedTauIdTopMass120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdTopMass120", "MTInvertedTauIdTopMass120", 400, 0., 400.);
    hMTInvertedTauIdTopMass120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdTopMass120150", "MTInvertedTauIdTopMass120150", 400, 0., 400.);
    hMTInvertedTauIdTopMass100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdTopMass100120", "MTInvertedTauIdTopMass100120", 400, 0., 400.);
    hMTInvertedTauIdTopMass80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdTopMass80100", "MTInvertedTauIdTopMass80100", 400, 0., 400.);
    hMTInvertedTauIdTopMass7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdTopMass7080", "MTInvertedTauIdTopMass7080", 400, 0., 400.);
    hMTInvertedTauIdTopMass6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdTopMass6070", "MTInvertedTauIdTopMass6070", 400, 0., 400.);
    hMTInvertedTauIdTopMass5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdTopMass5060", "MTInvertedTauIdTopMass5060", 400, 0., 400.);
    hMTInvertedTauIdTopMass4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdTopMass4050", "MTInvertedTauIdTopMass4050", 400, 0., 400.);

    hDeltaPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events", 360, 0.0, 360.0);
    //    hMTBaselineTauIdJet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MT_BaseLineTauIdJets", "MT_BaseLineTauIdJets;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);

    hMETInvertedTauIdJets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets", "MET_InvertedTauIdJets;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdJets150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets150", "MET_InvertedTauIdJets150", 400, 0.0, 400.0);
    hMETInvertedTauIdJets120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets120", "MET_InvertedTauIdJets120", 400, 0.0, 400.0);
    hMETInvertedTauIdJets120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets120150", "MET_InvertedTauIdJets120150", 400, 0.0, 400.0);
    hMETInvertedTauIdJets100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets100120", "MET_InvertedTauIdJets100120", 400, 0.0, 400.0); 
    hMETInvertedTauIdJets80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets80100", "MET_InvertedTauIdJets80100", 400, 0.0, 400.0); 
    hMETInvertedTauIdJets7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets7080", "MET_InvertedTauIdJets7080", 400, 0.0, 400.0); 
    hMETInvertedTauIdJets6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets6070", "MET_InvertedTauIdJets6070", 400, 0.0, 400.0); 
    hMETInvertedTauIdJets5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets5060", "MET_InvertedTauIdJets5060", 400, 0.0, 400.0); 
    hMETInvertedTauIdJets4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets4050", "MET_InvertedTauIdJets4050", 400, 0.0, 400.0); 

   
    hMETInvertedTauIdBtag = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag", "MET_InvertedTauIdBtag", 400, 0.0, 400.0);
    hMETInvertedTauIdBtag150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag150", "MET_InvertedTauIdBtag150", 400, 0.0, 400.0);
    hMETInvertedTauIdBtag120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag120", "MET_InvertedTauIdBtag120", 400, 0.0, 400.0);
    hMETInvertedTauIdBtag120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag120150", "MET_InvertedTauIdBtag120150", 400, 0.0, 400.0);
    hMETInvertedTauIdBtag100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag100120", "MET_InvertedTauIdBtag100120", 400, 0.0, 400.0); 
    hMETInvertedTauIdBtag80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag80100", "MET_InvertedTauIdBtag80100", 400, 0.0, 400.0); 
    hMETInvertedTauIdBtag7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag7080", "MET_InvertedTauIdBtag7080", 400, 0.0, 400.0); 
    hMETInvertedTauIdBtag6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag6070", "MET_InvertedTauIdBtag6070", 400, 0.0, 400.0); 
    hMETInvertedTauIdBtag5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag5060", "MET_InvertedTauIdBtag5060", 400, 0.0, 400.0); 
    hMETInvertedTauIdBtag4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag4050", "MET_InvertedTauIdBtag4050", 400, 0.0, 400.0); 

    hMETInvertedTauIdBveto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto", "MET_InvertedTauIdBveto", 400, 0.0, 400.0);
    hMETInvertedTauIdBveto150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto150", "MET_InvertedTauIdBveto150", 400, 0.0, 400.0);
    hMETInvertedTauIdBveto120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto120", "MET_InvertedTauIdBveto120", 400, 0.0, 400.0);
    hMETInvertedTauIdBveto120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto120150", "MET_InvertedTauIdBveto120150", 400, 0.0, 400.0);
    hMETInvertedTauIdBveto100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto100120", "MET_InvertedTauIdBveto100120", 400, 0.0, 400.0); 
    hMETInvertedTauIdBveto80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto80100", "MET_InvertedTauIdBveto80100", 400, 0.0, 400.0); 
    hMETInvertedTauIdBveto7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto7080", "MET_InvertedTauIdBveto7080", 400, 0.0, 400.0); 
    hMETInvertedTauIdBveto6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto6070", "MET_InvertedTauIdBveto6070", 400, 0.0, 400.0); 
    hMETInvertedTauIdBveto5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto5060", "MET_InvertedTauIdBveto5060", 400, 0.0, 400.0); 
    hMETInvertedTauIdBveto4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto4050", "MET_InvertedTauIdBveto4050", 400, 0.0, 400.0); 

    hDeltaPhiInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInverted", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 360, 0., 180.);
    hDeltaPhiInverted150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInverted150", "deltaPhi;#Delta#phi(tau,MET) 150", 360, 0., 180.);
    hDeltaPhiInverted120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInverted120", "deltaPhi;#Delta#phi(tau,MET) 120", 360, 0., 180.);

    hDeltaPhiInverted120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInverted120150", "deltaPhi;#Delta#phi(tau,MET) 120150", 360, 0., 180.);

    hDeltaPhiInverted100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInverted100120", "deltaPhi;#Delta#phi(tau,MET) 100120", 360, 0., 180.);

    hDeltaPhiInverted80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInverted80100", "deltaPhi;#Delta#phi(tau,MET) 80100", 360, 0., 180.);

    hDeltaPhiInverted7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInverted7080", "deltaPhi;#Delta#phi(tau,MET) 7080", 360, 0., 180.);

    hDeltaPhiInverted6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInverted6070", "deltaPhi;#Delta#phi(tau,MET) 6070", 360, 0., 180.);

    hDeltaPhiInverted5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInverted5060", "deltaPhi;#Delta#phi(tau,MET) 5060", 360, 0., 180.);

    hDeltaPhiInverted4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInverted4050", "deltaPhi;#Delta#phi(tau,MET) 4050", 360, 0., 180.);


    //   hMTInvertedTauIdJets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MT_InvertedTauIdJets", "MT_InvertedTauIdJets;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    //    hMETInvertedTauIdLoose = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdLoose", "MET_InvertedTauIdLoose;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    //    hMETInvertedTauIdLoose150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdLoose150", "MET_InvertedTauIdLoose150;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    //    hMETInvertedTauIdLoose4070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJLoose4070", "MET_InvertedTauIdLoose4070;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    //   hMETInvertedTauIdLoose70150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdLoose70150", "MET_InvertedTauIdLoose70150;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0); 
    //    hMTInvertedTauIdLoose = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MT_InvertedTauIdLoose", "MT_InvertedTauIdLoose;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
   
    hMETInvertedTauIdBtagDphi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtagDphi", "MET_InvertedTauIdBtagDphi;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETBaselineTauIdBtagDphi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtagDphi", "MET_BaseLineTauIdBtagDphi;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);

    
    hSelectedTauEtMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_pT_AfterMetCut", "SelectedTau_pT_AfterMetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEtaMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_eta_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.1", 300, -3.0, 3.0);
    hSelectedTauPhiMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_phi_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtauMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_Rtau_AfterMetCut", "SelectedTau_Rtau_AfterMetCut;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);

    hSelectionFlow = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SignalSelectionFlow", "SignalSelectionFlow;;N_{events}", 7, 0, 7);
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderTrigger,"Trigger");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderVertexSelection,"Vertex");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderTauID,"#tau ID");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderElectronVeto,"Isol. e veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderMuonVeto,"Isol. #mu veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderMETSelection,"MET");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderJetSelection,"#geq 3 jets");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderBTagSelection,"#geq 1 b jet");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderFakeMETVeto,"Further QCD rej.");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kSignalOrderTopSelection,"Top mass");

    hEMFractionAll = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "NonQCDTypeII_FakeTau_EMFraction_All", "FakeTau_EMFraction_All", 22, 0., 1.1);
    hEMFractionElectrons = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "NonQCDTypeII_FakeTau_EMFraction_Electrons", "FakeTau_EMFraction_Electrons", 22, 0., 1.1);
    
    hNonQCDTypeIISelectedTauEtAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NonQCDTypeII_SelectedTau_pT_AfterCuts", "SelectedTau_pT_AfterCuts;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 40, 0.0, 400.0);
    hNonQCDTypeIISelectedTauEtaAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NonQCDTypeII_SelectedTau_eta_AfterCuts", "SelectedTau_eta_AfterCuts;#tau #eta;N_{events} / 0.1", 30, -3.0, 3.0);

    fTree.init(*fs);
  }

  SignalAnalysisInvertedTau::~SignalAnalysisInvertedTau() { }

  void SignalAnalysisInvertedTau::produces(edm::EDFilter *producer) const {
    if(fProduce) {
      producer->produces<std::vector<pat::Tau> >("selectedTaus");
      producer->produces<std::vector<pat::Jet> >("selectedJets");
      producer->produces<std::vector<pat::Jet> >("selectedBJets");
      producer->produces<std::vector<pat::Electron> >("selectedVetoElectrons");
      producer->produces<std::vector<pat::Muon> >("selectedVetoMuonsBeforeIsolation");
      producer->produces<std::vector<pat::Muon> >("selectedVetoMuons");
    }
  }





  bool SignalAnalysisInvertedTau::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    fEventWeight.updatePrescale(iEvent); // set prescale
    fTree.setPrescaleWeight(fEventWeight.getWeight());

 

    // Vertex weight
    if(!iEvent.isRealData()) {
      const double myVertexWeight = fVertexWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(myVertexWeight);
      fTree.setPileupWeight(myVertexWeight);
    }
    int nVertices = fVertexWeightReader.getNumberOfVertices(iEvent, iSetup);
    hVerticesBeforeWeight->Fill(nVertices);
    hVerticesAfterWeight->Fill(nVertices);
    fTree.setNvertices(nVertices);
    increment(fAllCounter);
    
    // Apply trigger and HLT_MET cut or trigger parametrisation
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);
    hSelectionFlow->Fill(kSignalOrderTrigger);
    if(triggerData.hasTriggerPath()) // protection if TriggerSelection is disabled
      fTree.setHltTaus(triggerData.getTriggerTaus());

    hVerticesTriggeredBeforeWeight->Fill(nVertices);
    hVerticesTriggeredAfterWeight->Fill(nVertices);

    // GenParticle analysis (must be done here when we effectively trigger all MC)
    if (!iEvent.isRealData()) fGenparticleAnalysis.analyze(iEvent, iSetup);

    // Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    //hSelectionFlow->Fill(kSignalOrderVertexSelection);

  // Get MET object 
    //    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    //double Met = metData.getSelectedMET()->et();
    //    std::cout << " weight before  = " << fEventWeight.getWeight() << " met " << Met <<  std::endl;
    //    hMETBeforeTauId->Fill(metData.getSelectedMET()->et());  



  
    // TauID
    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup); 
    //    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    edm::PtrVector<pat::Tau> myBestTauCandidate;
    if (tauData.getSelectedTaus().size())
      myBestTauCandidate.push_back(tauData.getSelectedTau());
    // Obtain MC matching - for EWK without genuine taus
    FakeTauIdentifier::MCSelectedTauMatchType myMatch = fFakeTauIdentifier.matchTauToMC(iEvent, *(tauData.getSelectedTau()));
    // Apply scale factor for fake tau
    if (!iEvent.isRealData())
      fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(myMatch, tauData.getSelectedTau()->eta()));

    //if(tauData.getSelectedTaus().size() == 0) return false; // at least one tau candidate
    increment(fTausExistCounter);

    // nprongs
    if (!tauData.selectedTauPassesNProngs()) return false;
    increment(fNprongsAfterTauIDCounter);

    hSelectedTauLeadingTrackPt->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt());

    // rtau
    hSelectedTauRtau->Fill(tauData.getRtauOfSelectedTau());
    if (!tauData.selectedTauPassesRtau()) return false;
    increment(fRtauAfterTauIDCounter);
    // now tau ID has been applied


    if(iEvent.isRealData())
      fTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
    // Apply trigger scale factor here, because it depends only on tau
    TriggerEfficiencyScaleFactor::Data triggerWeight = fTriggerEfficiencyScaleFactor.applyEventWeight(*(tauData.getSelectedTau()), iEvent.isRealData(), fEventWeight);
    fTree.setTriggerWeight(triggerWeight.getEventWeight(), triggerWeight.getEventWeightAbsoluteUncertainty());
    increment(fTriggerScaleFactorCounter);
    hSelectionFlow->Fill(kSignalOrderTauID);




    //    std::string myTauIsolation = "byTightIsolation";
    std::string myTauIsolation = "byMediumCombinedIsolationDeltaBetaCorr";


    // Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup,  tauData.getSelectedTau(),  nVertices); 

 // Get MET object 
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getAllJets());
    //double Met = metData.getSelectedMET()->et();
    //    std::cout << " weight before  = " << fEventWeight.getWeight() << " met " << Met <<  std::endl;
    hMETBeforeTauId->Fill(metData.getSelectedMET()->et());  


    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    // Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());


    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    //    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());

    //    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());

    //    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
   double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
   
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()) );
   
    //    FullHiggsMassCalculator::Data FullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData, metData);



  // baseline tau-id


    if (tauData.selectedTauPassesDiscriminator(myTauIsolation, 0.5)  && tauData.selectedTauPassesNProngs() && tauData.selectedTauPassesRtau() ) {


      hMETBaselineTauId->Fill(metData.getSelectedMET()->et());

      increment(fBaselineTauIDCounter);
      if (electronVetoData.passedEvent()) {
	increment(fBaselineEvetoCounter);
	if (muonVetoData.passedEvent()) {
	  increment(fBaselineMuvetoCounter);
	  if(jetData.passedEvent()) {
	    increment(fBaselineJetsCounter);
	    // Count baseline events
	    if(btagData.passedEvent()) hMet_AfterBTagging->Fill(metData.getSelectedMET()->et());
	    if(metData.passedEvent()) {	
	      increment(fBaselineMetCounter); 
	      hMTBaselineTauIdJet->Fill(transverseMass);  
	      if ( tauData.getSelectedTau()->pt() > 150  ) hMTBaselineTauIdJet150->Fill(transverseMass);
	      if ( tauData.getSelectedTau()->pt() > 120  ) hMTBaselineTauIdJet120->Fill(transverseMass);
	      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTBaselineTauIdJet120150->Fill(transverseMass);
	      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTBaselineTauIdJet100120->Fill(transverseMass);
	      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100  ) hMTBaselineTauIdJet80100->Fill(transverseMass);
	      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTBaselineTauIdJet7080->Fill(transverseMass);
	      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTBaselineTauIdJet6070->Fill(transverseMass);
	      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTBaselineTauIdJet5060->Fill(transverseMass);
	      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTBaselineTauIdJet4050->Fill(transverseMass);
	   
	      if(btagData.passedEvent()) {
		increment(fBaselineBtagCounter);
		if ( deltaPhi < 160) {
		  increment(fBaselineDphi160Counter);
		  //		  fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData, metData);

		if ( deltaPhi < 130) increment(fBaselineDphi130Counter);
		//		  hMETBaselineTauIdBtagDphi->Fill(metData.getSelectedMET()->et()); 
		//		  if (TopChiSelectionData.passedEvent() ) {
		//		    increment(fBaselineTopChiSelectionCounter);    
		    //		    hTransverseMassTopChiSelection->Fill(transverseMass);  
		//		  }  	      
		}
	      }
	    }
	    //	    if(metData.passedEvent()) hMTBaselineTauIdJet->Fill(transverseMass); 
	 
	    if(btagData.passedEvent()) {
	      hMETBaselineTauIdBtag->Fill(metData.getSelectedMET()->et()); 
	      if ( tauData.getSelectedTau()->pt() > 150  ) hMETBaselineTauIdBtag150->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 120  ) hMETBaselineTauIdBtag120->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMETBaselineTauIdBtag120150->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMETBaselineTauIdBtag100120->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100  ) hMETBaselineTauIdBtag80100->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMETBaselineTauIdBtag7080->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMETBaselineTauIdBtag6070->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMETBaselineTauIdBtag5060->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMETBaselineTauIdBtag4050->Fill(metData.getSelectedMET()->et());
	      

   
	     
	      // mT with b tagging and met cut
	      if(metData.passedEvent()) {
		hMTBaselineTauIdBtag->Fill(transverseMass);   
		if ( tauData.getSelectedTau()->pt() > 150  ) hMTBaselineTauIdBtag150->Fill(transverseMass); 
		if ( tauData.getSelectedTau()->pt() > 120  ) hMTBaselineTauIdBtag120->Fill(transverseMass); 
		if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTBaselineTauIdBtag120150->Fill(transverseMass); 
		if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTBaselineTauIdBtag100120->Fill(transverseMass); 
		if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTBaselineTauIdBtag80100->Fill(transverseMass); 
		if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTBaselineTauIdBtag7080->Fill(transverseMass); 
		if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTBaselineTauIdBtag6070->Fill(transverseMass); 
		if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTBaselineTauIdBtag5060->Fill(transverseMass); 
		if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTBaselineTauIdBtag4050->Fill(transverseMass);

		if ( deltaPhi < 160) {
		  hMTBaselineTauIdPhi->Fill(transverseMass);   
		  if ( tauData.getSelectedTau()->pt() > 150  ) hMTBaselineTauIdPhi150->Fill(transverseMass);
		  if ( tauData.getSelectedTau()->pt() > 120  ) hMTBaselineTauIdPhi120->Fill(transverseMass); 
		  if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTBaselineTauIdPhi120150->Fill(transverseMass); 
		  if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTBaselineTauIdPhi100120->Fill(transverseMass); 
		  if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTBaselineTauIdPhi80100->Fill(transverseMass); 
		  if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTBaselineTauIdPhi7080->Fill(transverseMass); 
		  if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTBaselineTauIdPhi6070->Fill(transverseMass); 
		  if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTBaselineTauIdPhi5060->Fill(transverseMass); 
		  if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTBaselineTauIdPhi4050->Fill(transverseMass);
	       

		}
		
	      }
	    }
	   
	    hMETBaselineTauIdJets->Fill(metData.getSelectedMET()->et());  
	    if ( tauData.getSelectedTau()->pt() > 150  ) hMETBaselineTauIdJets150->Fill(metData.getSelectedMET()->et());
	    if ( tauData.getSelectedTau()->pt() > 120  ) hMETBaselineTauIdJets120->Fill(metData.getSelectedMET()->et());
	    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMETBaselineTauIdJets120150->Fill(metData.getSelectedMET()->et());
	    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMETBaselineTauIdJets100120->Fill(metData.getSelectedMET()->et());
	    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100  ) hMETBaselineTauIdJets80100->Fill(metData.getSelectedMET()->et());
	    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMETBaselineTauIdJets7080->Fill(metData.getSelectedMET()->et());
	    if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMETBaselineTauIdJets6070->Fill(metData.getSelectedMET()->et());
	    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMETBaselineTauIdJets5060->Fill(metData.getSelectedMET()->et());
	    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMETBaselineTauIdJets4050->Fill(metData.getSelectedMET()->et());

	    if( btagData.getSelectedJets().size() < 1 ) {
	      hMETBaselineTauIdBveto->Fill(metData.getSelectedMET()->et());  
	      if ( tauData.getSelectedTau()->pt() > 150  ) hMETBaselineTauIdBveto150->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 120  ) hMETBaselineTauIdBveto120->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMETBaselineTauIdBveto120150->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMETBaselineTauIdBveto100120->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100  ) hMETBaselineTauIdBveto80100->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMETBaselineTauIdBveto7080->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMETBaselineTauIdBveto6070->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMETBaselineTauIdBveto5060->Fill(metData.getSelectedMET()->et());
	      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMETBaselineTauIdBveto4050->Fill(metData.getSelectedMET()->et());	   
	    }
	  }
	}
      }
    }
   

    // TauID, inverted TauID, veto on isolated tau
    if(!tauData.selectedTausDoNotPassIsolation())  return false; 
    // veto was successfull
    increment(fTauVetoAfterTauIDCounter);

    hMETInvertedTauId->Fill(metData.getSelectedMET()->et());  


    hSelectionFlow->Fill(kSignalOrderTauID);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Tau> > saveTaus(new std::vector<pat::Tau>());
      copyPtrToVector(tauData.getSelectedTaus(), *saveTaus);
      iEvent.put(saveTaus, "selectedTaus");
    }

 
    hSelectedTauEt->Fill(tauData.getSelectedTau()->pt());
    hSelectedTauEta->Fill(tauData.getSelectedTau()->eta());
    hSelectedTauPhi->Fill(tauData.getSelectedTau()->phi());
    //    hSelectedTauRtau->Fill(tauData.getRtauOfBestTauCandidate());
    if(metData.passedEvent()) {
      //      hSelectedTauEtMetCut->Fill(tauData.getSelectedTau()->pt());
      hSelectedTauLeadingTrackPtMetCut->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt());
    }

    // Obtain MC matching
    MCSelectedTauMatchType myTauMatch = matchTauToMC(iEvent, tauData.getSelectedTau());
    fAllTausCounterGroup.incrementOneTauCounter();
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderTauID, tauData);
    if (myTauMatch == kkElectronToTau)
      hEMFractionElectrons->Fill(tauData.getSelectedTau()->emFraction());
    hEMFractionAll->Fill(tauData.getSelectedTau()->emFraction());

    hTransverseMassBeforeVeto->Fill(transverseMass);
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderMETSelection, tauData);

    //    Global electron veto
    //    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);
    hSelectionFlow->Fill(kSignalOrderElectronVeto);
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderElectronVeto, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Electron> > saveElectrons(new std::vector<pat::Electron>());
      copyPtrToVector(electronVetoData.getSelectedElectrons(), *saveElectrons);
      iEvent.put(saveElectrons, "selectedVetoElectrons");
    }

    // Global muon veto
    //    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);
    hSelectionFlow->Fill(kSignalOrderMuonVeto);
    hTransverseMassAfterVeto->Fill(transverseMass);
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderMuonVeto, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Muon> > saveMuons(new std::vector<pat::Muon>());
      copyPtrToVector(muonVetoData.getSelectedMuonsBeforeIsolation(), *saveMuons);
      iEvent.put(saveMuons, "selectedVetoMuonsBeforeIsolation");
      saveMuons.reset(new std::vector<pat::Muon>());
      copyPtrToVector(muonVetoData.getSelectedMuons(), *saveMuons);
      iEvent.put(saveMuons, "selectedVetoMuons");
    }

   
    if (tauData.getSelectedTaus().size())
      myBestTauCandidate.push_back(tauData.getSelectedTau());


    // Hadronic jet selection
    //    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup,  tauData.getSelectedTau()); 
    if(!jetData.passedEvent()) return false;
    increment(fNJetsCounter);
    hSelectionFlow->Fill(kSignalOrderJetSelection);
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderJetSelection, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveJets(new std::vector<pat::Jet>());
      copyPtrToVector(jetData.getSelectedJets(), *saveJets);
      iEvent.put(saveJets, "selectedJets");
    }
   
  // b tagging, no event cut
    //   BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());

   
// plots for inverted isolation

    // inverted MET before b tagging
    hMETInvertedTauIdJets->Fill(metData.getSelectedMET()->et());
    if ( tauData.getSelectedTau()->pt() > 150  ) hMETInvertedTauIdJets150->Fill(metData.getSelectedMET()->et());
    if ( tauData.getSelectedTau()->pt() > 120  ) hMETInvertedTauIdJets120->Fill(metData.getSelectedMET()->et());
    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMETInvertedTauIdJets120150->Fill(metData.getSelectedMET()->et());
    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMETInvertedTauIdJets100120->Fill(metData.getSelectedMET()->et());
    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMETInvertedTauIdJets80100->Fill(metData.getSelectedMET()->et());
    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMETInvertedTauIdJets7080->Fill(metData.getSelectedMET()->et());     
    if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMETInvertedTauIdJets6070->Fill(metData.getSelectedMET()->et());
    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMETInvertedTauIdJets5060->Fill(metData.getSelectedMET()->et()); 
    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMETInvertedTauIdJets4050->Fill(metData.getSelectedMET()->et());																		


 // Get MET object 
    //    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    //double Met = metData.getSelectedMET()->et();
    //    std::cout << " weight before  = " << fEventWeight.getWeight() << " met " << Met <<  std::endl;
    //    hMETBeforeTauId->Fill(metData.getSelectedMET()->et());  
															      

    if(btagData.passedEvent()) {
      hMETInvertedTauIdBtag->Fill(metData.getSelectedMET()->et());
     
      if ( tauData.getSelectedTau()->pt() > 150  ) hMETInvertedTauIdBtag150->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 120  ) hMETInvertedTauIdBtag120->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMETInvertedTauIdBtag120150->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMETInvertedTauIdBtag100120->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMETInvertedTauIdBtag80100->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMETInvertedTauIdBtag7080->Fill(metData.getSelectedMET()->et());     	
      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMETInvertedTauIdBtag6070->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMETInvertedTauIdBtag5060->Fill(metData.getSelectedMET()->et()); 
      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMETInvertedTauIdBtag4050->Fill(metData.getSelectedMET()->et());																		
    }


    // Veto on hard b jets  
    if( btagData.getSelectedJets().size() < 1) {
      increment(fBjetVetoCounter);
      hMETInvertedTauIdBveto->Fill(metData.getSelectedMET()->et());
     
      if ( tauData.getSelectedTau()->pt() > 150  ) hMETInvertedTauIdBveto150->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 120  ) hMETInvertedTauIdBveto120->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMETInvertedTauIdBveto120150->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMETInvertedTauIdBveto100120->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMETInvertedTauIdBveto80100->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMETInvertedTauIdBveto7080->Fill(metData.getSelectedMET()->et());     	
      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMETInvertedTauIdBveto6070->Fill(metData.getSelectedMET()->et());
      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMETInvertedTauIdBveto5060->Fill(metData.getSelectedMET()->et()); 
      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMETInvertedTauIdBveto4050->Fill(metData.getSelectedMET()->et());																		
    }
  

    //    fTree.setFillWeight(fEventWeight.getWeight());
    //    fTree.setBTagging(btagData.passedEvent(), btagData.getScaleFactor());
    //    fTree.setTop(TopSelectionData.getTopP4());
    //    fTree.fill(iEvent, tauData.getSelectedTaus(), jetData.getSelectedJets(), metData.getSelectedMET(),
    //               evtTopologyData.alphaT().fAlphaT, fakeMETData.closestDeltaPhi() );

 
    
    hTransverseMassNoMet->Fill(transverseMass);
    if(btagData.passedEvent())   {
      increment(fBTaggingBeforeMETCounter);
      hTransverseMassNoMetBtag->Fill(transverseMass);
    } 

    // MET cut
    hMETBeforeMETCut->Fill(metData.getSelectedMET()->et());
    if(!metData.passedEvent()) return false;
    increment(fMETCounter);
    hSelectionFlow->Fill(kSignalOrderMETSelection);

    hSelectedTauEtMetCut->Fill(tauData.getSelectedTau()->pt());
    hSelectedTauEtaMetCut->Fill(tauData.getSelectedTau()->eta());
    hSelectedTauPhiMetCut->Fill(tauData.getSelectedTau()->phi());
    hSelectedTauRtauMetCut->Fill(tauData.getRtauOfSelectedTau());  
 
  
   // mt for inverted tau before b tagging
    hMTInvertedTauIdJet->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 150  ) hMTInvertedTauIdJet150->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 120  ) hMTInvertedTauIdJet120->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTInvertedTauIdJet120150->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTInvertedTauIdJet100120->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTInvertedTauIdJet80100->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTInvertedTauIdJet7080->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTInvertedTauIdJet6070->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTInvertedTauIdJet5060->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTInvertedTauIdJet4050->Fill(transverseMass); 

 
 

    // b tagging cut
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderBTagSelection, tauData, btagData.passedEvent(),btagData.getMaxDiscriminatorValue());
    if(!btagData.passedEvent()) return false;
    // Apply scale factor as weight to event
    fEventWeight.multiplyWeight(btagData.getScaleFactor());
    increment(fBTaggingCounter);
    hSelectionFlow->Fill(kSignalOrderBTagSelection);
    hMet_AfterBTagging->Fill(metData.getSelectedMET()->et());

    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveBJets(new std::vector<pat::Jet>());
      copyPtrToVector(btagData.getSelectedJets(), *saveBJets);
      iEvent.put(saveBJets, "selectedBJets");
    }

   // mt for inverted tau with b tagging
    
    hMTInvertedTauIdBtag->Fill(transverseMass);
    if ( tauData.getSelectedTau()->pt() > 150  ) hMTInvertedTauIdBtag150->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 120  ) hMTInvertedTauIdBtag120->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTInvertedTauIdBtag120150->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTInvertedTauIdBtag100120->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTInvertedTauIdBtag80100->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTInvertedTauIdBtag7080->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTInvertedTauIdBtag6070->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTInvertedTauIdBtag5060->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTInvertedTauIdBtag4050->Fill(transverseMass); 

    hDeltaPhiInverted->Fill(deltaPhi);  
    if ( tauData.getSelectedTau()->pt() > 150  ) hDeltaPhiInverted150->Fill(deltaPhi); 
    if ( tauData.getSelectedTau()->pt() > 120  ) hDeltaPhiInverted120->Fill(deltaPhi); 
    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hDeltaPhiInverted120150->Fill(deltaPhi); 
    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hDeltaPhiInverted100120->Fill(deltaPhi); 
    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hDeltaPhiInverted80100->Fill(deltaPhi); 
    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hDeltaPhiInverted7080->Fill(deltaPhi); 
    if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hDeltaPhiInverted6070->Fill(deltaPhi); 
    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hDeltaPhiInverted5060->Fill(deltaPhi); 
    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hDeltaPhiInverted4050->Fill(deltaPhi); 

   //    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    hDeltaPhi->Fill(deltaPhi);
    if (deltaPhi > fDeltaPhiCutValue) return false;    
    increment(fDeltaPhiTauMETCounter);
   

    FullHiggsMassCalculator::Data FullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData, metData);
    //    fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData, metData);
    double HiggsMass = FullHiggsMassData.getHiggsMass();
    if (HiggsMass > 100 && HiggsMass < 200 ) increment(fHiggsMassCutCounter);


    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());

    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    // Calculate alphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTau()), jetData.getSelectedJets()); 
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());

    double topMass = TopChiSelectionData.getTopMass();
    hTopMass->Fill(topMass);
    // top mass with binning    
    if ( tauData.getSelectedTau()->pt() > 150  ) hTopMass150->Fill(topMass); 
    if ( tauData.getSelectedTau()->pt() > 120  ) hTopMass120->Fill(topMass); 
    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hTopMass120150->Fill(topMass); 
    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hTopMass100120->Fill(topMass); 
    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hTopMass80100->Fill(topMass); 
    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hTopMass7080->Fill(topMass); 
    if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hTopMass6070->Fill(topMass); 
    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hTopMass5060->Fill(topMass); 
    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hTopMass4050->Fill(topMass); 

 
  
    // Inv mass mass with binning  
    hHiggsMass->Fill(HiggsMass);   
    if ( tauData.getSelectedTau()->pt() > 150  ) hHiggsMass150->Fill(HiggsMass); 
    if ( tauData.getSelectedTau()->pt() > 120  ) hHiggsMass120->Fill(HiggsMass); 
    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hHiggsMass120150->Fill(HiggsMass); 
    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hHiggsMass100120->Fill(HiggsMass); 
    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hHiggsMass80100->Fill(HiggsMass); 
    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hHiggsMass7080->Fill(HiggsMass); 
    if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hHiggsMass6070->Fill(HiggsMass); 
    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hHiggsMass5060->Fill(HiggsMass); 
    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hHiggsMass4050->Fill(HiggsMass); 

    if (deltaPhi<  140 ) {
      //      increment(fDeltaPhiTauMET140Counter);

      // Inv mass mass with binning  
      hHiggsMassPhi->Fill(HiggsMass);   
      if ( tauData.getSelectedTau()->pt() > 150  ) hHiggsMassPhi150->Fill(HiggsMass);
      if ( tauData.getSelectedTau()->pt() > 120  ) hHiggsMassPhi120->Fill(HiggsMass);  
      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hHiggsMassPhi120150->Fill(HiggsMass); 
      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hHiggsMassPhi100120->Fill(HiggsMass); 
      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hHiggsMassPhi80100->Fill(HiggsMass); 
      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hHiggsMassPhi7080->Fill(HiggsMass); 
      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hHiggsMassPhi6070->Fill(HiggsMass); 
      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hHiggsMassPhi5060->Fill(HiggsMass); 
      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hHiggsMassPhi4050->Fill(HiggsMass); 

 


    // for inverted tau with MET>70 cut   
 //    if (metData.getSelectedMET()->et() > 70) {
      hMTInvertedTauIdMet->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 150  ) hMTInvertedTauIdJet150->Fill(transverseMass);
      if ( tauData.getSelectedTau()->pt() > 120  ) hMTInvertedTauIdJet120->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTInvertedTauIdMet120150->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTInvertedTauIdMet100120->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTInvertedTauIdMet80100->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTInvertedTauIdMet7080->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTInvertedTauIdMet6070->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTInvertedTauIdMet5060->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTInvertedTauIdMet4050->Fill(transverseMass);
    }
   // mt for inverted tau with deltaphi cut


    hTransverseMass->Fill(transverseMass); 

    hMTInvertedTauIdJetPhi->Fill(transverseMass); 
    increment(fdeltaPhiTauMET160Counter);
    if ( tauData.getSelectedTau()->pt() > 150  ) hMTInvertedTauIdJetPhi150->Fill(transverseMass);
    if ( tauData.getSelectedTau()->pt() > 120  ) hMTInvertedTauIdJetPhi120->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTInvertedTauIdJetPhi120150->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTInvertedTauIdJetPhi100120->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTInvertedTauIdJetPhi80100->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTInvertedTauIdJetPhi7080->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTInvertedTauIdJetPhi6070->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTInvertedTauIdJetPhi5060->Fill(transverseMass); 
    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTInvertedTauIdJetPhi4050->Fill(transverseMass); 
 
  
  

  //    if ( deltaPhi < 130 ) {
    if (TopChiSelectionData.passedEvent() ) {
      hMTInvertedTauIdTopMass->Fill(transverseMass);
      increment(fdeltaPhiTauMET130Counter); 
      if ( tauData.getSelectedTau()->pt() > 150  ) hMTInvertedTauIdTopMass150->Fill(transverseMass);
      if ( tauData.getSelectedTau()->pt() > 120  ) hMTInvertedTauIdTopMass120->Fill(transverseMass);  
      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTInvertedTauIdTopMass120150->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTInvertedTauIdTopMass100120->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTInvertedTauIdTopMass80100->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTInvertedTauIdTopMass7080->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTInvertedTauIdTopMass6070->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTInvertedTauIdTopMass5060->Fill(transverseMass); 
      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTInvertedTauIdTopMass4050->Fill(transverseMass); 
    }


    hDeltaPhi->Fill(deltaPhi);
    if ( deltaPhi > 10) increment(fdeltaPhiTauMET10Counter); 


     

    // plot deltaPhi(jet,met)
    double deltaPhiJetMet = -999;
    double deltaPhiMin = 999;
    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetData.getSelectedJets().begin(); iJet != jetData.getSelectedJets().end(); ++iJet) {
      deltaPhiJetMet = DeltaPhi::reconstruct(**iJet, *(metData.getSelectedMET()));
      if (deltaPhiMin < deltaPhiJetMet ) deltaPhiMin = deltaPhiJetMet;
      hDeltaPhiJetMet->Fill(deltaPhiJetMet*57.3);
    }

    hSelectedTauRtauAfterCuts->Fill(tauData.getRtauOfSelectedTau());
    hSelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt());
    hSelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta());
    hMetAfterCuts->Fill(metData.getSelectedMET()->et());


   
    if (TopChiSelectionData.passedEvent() ) {
         increment(fTopChiSelectionCounter);
      //      hSelectionFlow->Fill(kSignalOrderTopSelection);      
	 hTransverseMassTopChiSelection->Fill(transverseMass);     
    } 

    if (BjetSelectionData.passedEvent() ) {
        
      TopWithBSelection::Data TopWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());

      if (TopWithBSelectionData.passedEvent() ) {
	increment(fTopWithBSelectionCounter);
	//      hSelectionFlow->Fill(kSignalOrderTopSelection);      
	hTransverseMassTopBjetSelection->Fill(transverseMass);     
      }    
    }


    //    return false;

   // top mass with possible event cuts
    if (TopSelectionData.passedEvent() ) {
      increment(fTopSelectionCounter);
      //      hSelectionFlow->Fill(kSignalOrderTopSelection);      
      hTransverseMassWithTopCut->Fill(transverseMass);
      if(transverseMass > 80 ) increment(ftransverseMassCut100TopCounter);   
    } 


    if (fakeMETData.passedEvent() ) {
      increment(fFakeMETVetoCounter);
      //      hTransverseMass->Fill(transverseMass);
      //     if ( deltaPhiJetMet*57.3 < 135) {
	//	increment(fdeltaPhiTauMET160FakeMetCounter);
	hTransverseMassFakeMET->Fill(transverseMass);  
      //      } 
    }
    //hSelectionFlow->Fill(kSignalOrderFakeMETVeto);
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderFakeMETVeto, tauData);




    if(transverseMass > 60 ) increment(ftransverseMassCut80NoRtauCounter);
    if(transverseMass > 80 ) increment(ftransverseMassCut100NoRtauCounter);

 

    if(transverseMass < 60 ) return false;
    increment(ftransverseMassCut80Counter);

    if(transverseMass < 80 ) return false;
    increment(ftransverseMassCut100Counter);

    
    // Fake MET veto a.k.a. further QCD suppression
    //    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTaus(), jetData.getSelectedJets());
    //    if (!fakeMETData.passedEvent()) return true;
    //    increment(fFakeMETVetoCounter);
    //hSelectionFlow->Fill(kSignalOrderFakeMETVeto);
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderFakeMETVeto, tauData);

    // Correlation analysis
    fCorrelationAnalysis.analyze(tauData.getSelectedTaus(), btagData.getSelectedJets());
    // Alpha T
    //if(!evtTopologyData.passedEvent()) return false;
    //    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    //    hAlphaT->Fill(sAlphaT.fAlphaT); // FIXME: move this histogramming to evt topology


   
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderTopSelection, tauData);

 
                               
    // Forward jet veto                                                                                                                                                                                                           
    //    ForwardJetVeto::Data forwardJetData = fForwardJetVeto.analyze(iEvent, iSetup);
    //    if (!forwardJetData.passedEvent()) return false;
    //    increment(fForwardJetVetoCounter);
    


    return true;
  }

  SignalAnalysisInvertedTau::MCSelectedTauMatchType SignalAnalysisInvertedTau::matchTauToMC(const edm::Event& iEvent, const edm::Ptr<pat::Tau> tau) {
    if (iEvent.isRealData()) return kkNoMC;
    bool foundMCTauOutsideAcceptanceStatus = false;
    bool isMCTau = false;
    bool isMCElectron = false;
    bool isMCMuon = false;

    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    //std::cout << "matchfinding:" << std::endl;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (std::abs(p.pdgId()) == 11 || std::abs(p.pdgId()) == 13 || std::abs(p.pdgId()) == 15) {
        // Check match with tau
        if (reco::deltaR(p, tau->p4()) < 0.1) {
          if (p.pt() > 10.) {
            //std::cout << "  match found, pid=" << p.pdgId() << " eta=" << std::abs(p.eta()) << " pt=" << p.pt() << std::endl;
            if (std::abs(p.pdgId()) == 11) isMCElectron = true;
            if (std::abs(p.pdgId()) == 13) isMCMuon = true;
            if (std::abs(p.pdgId()) == 15) isMCTau = true;
          }
        }
        // Check if there is a tau outside the acceptance in the event
        if (!foundMCTauOutsideAcceptanceStatus && std::abs(p.pdgId()) == 15) {
          if (p.pt() < 40 || abs(p.eta()) > 2.1)
            foundMCTauOutsideAcceptanceStatus = true;
        }
      }
    }
    if (!foundMCTauOutsideAcceptanceStatus) {
      if (isMCElectron) return kkElectronToTau;
      if (isMCMuon) return kkMuonToTau;
      if (isMCTau) return kkTauToTau;
      return kkJetToTau;
    }
    if (isMCElectron) return kkElectronToTauAndTauOutsideAcceptance;
    if (isMCMuon) return kkMuonToTauAndTauOutsideAcceptance;
    if (isMCTau) return kkTauToTauAndTauOutsideAcceptance;
    return kkJetToTauAndTauOutsideAcceptance;
  }

  SignalAnalysisInvertedTau::CounterGroup* SignalAnalysisInvertedTau::getCounterGroupByTauMatch(MCSelectedTauMatchType tauMatch) {
    if (tauMatch == kkElectronToTau) return &fElectronToTausCounterGroup;
    else if (tauMatch == kkMuonToTau) return &fMuonToTausCounterGroup;
    else if (tauMatch == kkTauToTau) return &fGenuineToTausCounterGroup;
    else if (tauMatch == kkJetToTau) return &fJetToTausCounterGroup;
    else if (tauMatch == kkElectronToTauAndTauOutsideAcceptance) return &fElectronToTausAndTauOutsideAcceptanceCounterGroup;
    else if (tauMatch == kkMuonToTauAndTauOutsideAcceptance) return &fMuonToTausAndTauOutsideAcceptanceCounterGroup;
    else if (tauMatch == kkTauToTauAndTauOutsideAcceptance) return &fGenuineToTausAndTauOutsideAcceptanceCounterGroup;
    else if (tauMatch == kkJetToTauAndTauOutsideAcceptance) return &fJetToTausAndTauOutsideAcceptanceCounterGroup;
    return 0;
  }
  
  void SignalAnalysisInvertedTau::fillNonQCDTypeIICounters(MCSelectedTauMatchType tauMatch, SignalSelectionOrder selection, const TauSelection::Data& tauData, bool passedStatus, double value) {
    // Get out if no match has been found
    if (tauMatch == kkNoMC) return;
    // Obtain status for main counter
    bool myTypeIIStatus = true;
    if (tauMatch == kkTauToTau || tauMatch == kkTauToTauAndTauOutsideAcceptance)
        myTypeIIStatus = false;
    // Fill main and subcounter for the selection
    if (selection == kSignalOrderTauID) {
      if (myTypeIIStatus) fNonQCDTypeIIGroup.incrementOneTauCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementOneTauCounter();
    } else if (selection == kSignalOrderMETSelection) {
      if (myTypeIIStatus) fNonQCDTypeIIGroup.incrementMETCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementMETCounter();
    } else if (selection == kSignalOrderElectronVeto) {
      if (myTypeIIStatus) fNonQCDTypeIIGroup.incrementElectronVetoCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementElectronVetoCounter();
    } else if (selection == kSignalOrderMuonVeto) {
      if (myTypeIIStatus) fNonQCDTypeIIGroup.incrementMuonVetoCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementMuonVetoCounter();
    } else if (selection == kSignalOrderJetSelection) {
      if (myTypeIIStatus) fNonQCDTypeIIGroup.incrementNJetsCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementNJetsCounter();
    } else if (selection == kSignalOrderBTagSelection) {
      if (myTypeIIStatus) {
        fNonQCDTypeIIGroup.incrementBTaggingCounter();
        // Fill histograms
        hNonQCDTypeIISelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt());
        hNonQCDTypeIISelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta());
      }
      getCounterGroupByTauMatch(tauMatch)->incrementBTaggingCounter();
    } else if (selection == kSignalOrderFakeMETVeto) {
      if (myTypeIIStatus) fNonQCDTypeIIGroup.incrementFakeMETVetoCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementFakeMETVetoCounter();
    } else if (selection == kSignalOrderTopSelection) {
      if (myTypeIIStatus) fNonQCDTypeIIGroup.incrementTopSelectionCounter();
      getCounterGroupByTauMatch(tauMatch)->incrementTopSelectionCounter();
    }
  }
}
