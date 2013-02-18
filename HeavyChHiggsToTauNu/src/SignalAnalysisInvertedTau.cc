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
    fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
    bBlindAnalysisStatus(iConfig.getUntrackedParameter<bool>("blindAnalysisStatus")),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fAllCounter(eventCounter.addCounter("All events")),
    fWJetsWeightCounter(eventCounter.addCounter("WJets inc+exl weight")),
    fVertexFilterCounter(eventCounter.addCounter("Vertex number filter")),
    fMETFiltersCounter(eventCounter.addCounter("MET filters")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),  
    fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
    fTauCandidateCounter(eventCounter.addCounter("Baseline, tau candidates found")),
    fNprongsAfterTauIDCounter(eventCounter.addCounter("Nprongs, all tau candidates")),
    fRtauAfterTauIDCounter(eventCounter.addCounter("Rtau, all tau candidates")),
    fTausExistCounter(eventCounter.addCounter("Baseline, isolation, all cands")),
    fTauFakeScaleFactorCounter(eventCounter.addCounter("Baseline, tau fake scale factor, all cands")),
    fTriggerScaleFactorCounter(eventCounter.addCounter("Baseline, trigger scale factor, all cands")),  
    fBaselineTauIDCounter(eventCounter.addCounter("Baseline, at least one tau")),
    fBaselineEvetoCounter(eventCounter.addCounter("Baseline,electron veto")),
    fBaselineMuvetoCounter(eventCounter.addCounter("Baseline,muon veto")),
    fBaselineJetsCounter(eventCounter.addCounter("Baseline, njets")),
    fBaselineMetCounter(eventCounter.addCounter("Baseline, MET")),
    fBaselineBtagCounter(eventCounter.addCounter("Baseline, btagging")),
    fBTaggingScaleFactorCounter(eventCounter.addCounter("btagging scale factor")),
    fBaselineDeltaPhiTauMETCounter(eventCounter.addCounter("Baseline,DeltaPhi(Tau,MET) upper limit")),
    fBaselineDphi160Counter(eventCounter.addCounter("Baseline, deltaPhi160")),
    fBaselineDeltaPhiMHTJet1CutCounter(eventCounter.addCounter("Baseline,DeltaPhi(Jet1,MHT) lower limit")),
    fBaselineDeltaPhiVSDeltaPhiMHTJet1CutCounter(eventCounter.addCounter("Baseline,DeltaPhi(Jet1,MHT) vs DeltaPhi cut")),
    fOneTauCounter(eventCounter.addCounter("Baseline, taus = 1")),
    fBaselineDphi130Counter(eventCounter.addCounter("Baseline, deltaPhi130")),
    fBaselineTopChiSelectionCounter(eventCounter.addCounter("Top BaselineChiSelection cut")),
    fTauVetoAfterTauIDCounter(eventCounter.addCounter("Veto on isolated taus")),
    fElectronVetoCounter(eventCounter.addCounter("electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("muon veto")),
    fNJetsCounter(eventCounter.addCounter("njets")),
    fBTaggingBeforeMETCounter(eventCounter.addCounter("btagging before MET")),
    fMETCounter(eventCounter.addCounter("MET")),
    fRtauAfterMETCounter(eventCounter.addCounter("Rtau after MET cut")),
    fBjetVetoCounter(eventCounter.addCounter("Veto on hard b jets")),
    fBvetoCounter(eventCounter.addCounter("Veto on b jets after MET")),
    fBvetoDeltaPhiCounter(eventCounter.addCounter("Veto on b jets after MET and Dphi")),
    fBTaggingCounter(eventCounter.addCounter("btagging")),
    fBTaggingScaleFactorInvertedCounter(eventCounter.addCounter("btagging scale factor inverted")),
    fDeltaPhiTauMETCounter(eventCounter.addCounter("DeltaPhi(Tau,MET) upper limit")),
    fDeltaPhiVSDeltaPhiMetJetCutCounter(eventCounter.addCounter("DeltaPhi(Jet,MET) vs DeltaPhi cut")),
    fDeltaPhiVSDeltaPhiMHTJet1CutCounter(eventCounter.addCounter("DeltaPhi(Jet1,MHT) vs DeltaPhi cut")),
    fDeltaPhiVSDeltaPhiMHTJet2CutCounter(eventCounter.addCounter("DeltaPhi(Jet2,MHT) vs DeltaPhi cut")),
    fDeltaPhiVSDeltaPhiMHTJet3CutCounter(eventCounter.addCounter("DeltaPhi(Jet3,MHT) vs DeltaPhi cut")),
    fdeltaPhiTauMET10Counter(eventCounter.addCounter("deltaPhiTauMET lower limit")),
    //    fDeltaPhiTauMET140Counter(eventCounter.addCounter("DeltaPhi(Tau,MET) upper limit 140")),
    //    fdeltaPhiTauMET10Counter(eventCounter.addCounter("deltaPhiTauMET lower limit")),
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


    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), fPrimaryVertexSelection.getSrc(), eventCounter, fHistoWrapper),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, fHistoWrapper),
    //    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    /////////////    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, fHistoWrapper),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, fHistoWrapper, "MET"),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, fHistoWrapper),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, fHistoWrapper),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, fHistoWrapper),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, fHistoWrapper),
    fFullHiggsMassCalculator(eventCounter, fHistoWrapper),
    fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, fHistoWrapper),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, fHistoWrapper),
    //    ftransverseMassCut(iConfig.getUntrackedParameter<edm::ParameterSet>("transverseMassCut")),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, fHistoWrapper),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, fHistoWrapper),
    fCorrelationAnalysis(eventCounter, fHistoWrapper, "HistoName"),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, fHistoWrapper),
    fTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiencyScaleFactor"), fHistoWrapper),
    //    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), fHistoWrapper, "TauID"),
    fVertexWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeightReader")),
    fMETFilters(iConfig.getUntrackedParameter<edm::ParameterSet>("metFilters"), eventCounter),
    fWJetsWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("wjetsWeightReader")),
    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), fHistoWrapper, "TauID"),
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
    fProduce(iConfig.getUntrackedParameter<bool>("produceCollections", false)),
    fOnlyGenuineTaus(iConfig.getUntrackedParameter<bool>("onlyGenuineTaus", false))
  {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms filled in the analysis body
    hOneProngRtauPassedInvertedTaus= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "OneProngRtauPassedInvertedTaus", "OneProngRtauPassedInvertedTaus", 10, 0, 10);
    hTauDiscriminator= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TauDiscriminator", "TauDiscriminator", 100, 0, 2);

    hVerticesBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesBeforeWeight", "Number of vertices without weighting", 30, 0, 30);
    hVerticesAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesAfterWeight", "Number of vertices with weighting", 30, 0, 30);
    hVerticesTriggeredBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesTriggeredBeforeWeight", "Number of vertices without weighting", 30, 0, 30);
    hVerticesTriggeredAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesTriggeredAfterWeight", "Number of vertices with weighting", 30, 0, 30);
    //    hmetAfterTrigger = fHistoWrapper.makeTH<TH1F>(*fs, "metAfterTrigger", "metAfterTrigger", 50, 0., 200.);
    hTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassWithTopCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassWithTopCut", "transverseMassWithTopCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassAfterVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassAfterVeto", "transverseMassAfterVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassBeforeVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassBeforeVeto", "transverseMassBeforeVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassNoMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassNoMet", "transverseMassNoMet;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassNoMetBtag = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassNoMetBtag", "transverseMassNoMetBtag;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);

 
    hTransverseMassFakeMET =  fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassFakeMET", "transverseMassFakeMET;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassTopChiSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassTopChiSelection", "transverseMassTopChiSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassTopBjetSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassTopBjetSelection", "transverseMassTopBjetSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hDeltaPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 360, 0., 180.);
    hDeltaPhiBeforeVeto= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiBeforeVeto", "deltaPhiBeforeVeto", 360, 0., 180.);
    hDeltaPhiAfterVeto= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiAfterVeto", "deltaPhiAfterVeto", 360, 0., 180.);
    hDeltaPhiAfterJets= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiAfterJets", "deltaPhiAfterJets", 360, 0., 180.);
    hDeltaPhiJetMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "deltaPhiJetMet", "deltaPhiJetMet", 320, 0., 3.2);  
    hMet_AfterBTagging = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "MET_AfterBTagging", "MET_AfterBTagging;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);

    
    hMETBeforeMETCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BeforeMETCut", "MET_BeforeMETCut;PF MET, GeV;N_{events} / 10 GeV", 80, 0.0, 400.0);
    hSelectedTauEt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_pT_AfterTauID", "SelectedTau_pT_AfterTauID;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    //    hSelectedTauEtMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_pT_AfterTauID_MetCut", "SelectedTau_pT_AfterTauID_MetCut;#tau p_{T}, GeV/c;N_{events / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_eta_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.1", 300, -3.0, 3.0);
    hSelectedTauEtaBackToBack = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_eta_BackToBack","SelectedtedTau_eta_BackToBack", 300, -3.0, 3.0);
    hSelectedTauEtaNoBackToBack = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_eta_NoBackToBack", "SelectedTau_eta_NoBackToBack", 300, -3.0, 3.0);
    hSelectedTauEtaCollinear = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_eta_Collinear", "SelectedTau_eta_Collinear", 300, -3.0, 3.0);
    hSelectedTauPhiBackToBack = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_phi_BackToBack","SelectedtedTau_phi_BackToBack", 60, -3.1415926, 3.1415926);
    hSelectedTauPhiNoBackToBack = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_phi_NoBackToBack", "SelectedTau_phi_NoBackToBack;", 60, -3.1415926, 3.1415926);

    hSelectedTauPhiCollinear = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_phi_Collinear", "SelectedTau_eta_Collinear", 60, -3.1415926, 3.1415926);
    hPtTauVsMetBackToBack = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "PtTauBackToBack", "MetBackToBack", 60, 0.0, 300.0, 60, 0.0, 300.0);
    hPtTauVsMetNoBackToBack = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "PtTauNoBackToBack", "MetNoBackToBack", 60, 0.0, 300.0, 60, 0.0, 300.0);
    hSelectedTauEtAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_pT_AfterCuts", "SelectedTau_pT_AfterCuts;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 40, 0.0, 400.0);
    hSelectedTauEtaAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_eta_AfterCuts", "SelectedTau_eta_AfterCuts;#tau #eta;N_{events} / 0.1", 30, -3.0, 3.0);
    hSelectedTauPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_phi_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_Rtau_AfterTauID", "SelectedTau_Rtau_AfterTauID;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);

    hSelectedTauLeadingTrackPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_TauLeadingTrackPt", "SelectedTau_TauLeadingTrackPt;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
  
    hMetAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "Met_AfterCuts", "Met_AfterCuts", 400, 0.0, 500.0);
    hMETBeforeTauId = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "Met_BeforeTauId", "Met_BeforeTauId", 400, 0.0, 500.0);


    hNBBaselineTauIdJet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBBaselineTauIdJet", "NBBaselineTauIdJet", 10, 0., 10.);
    hNJetBaselineTauIdMet= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetBaselineTauIdJetMet", "NJetBaselineTauIdJetMett", 10, 0., 10.);
    hNJetBaselineTauId = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetBaselineTauIdJet", "NJetBaselineTauIdJet", 20, 0., 20.);
    hDeltaPhiBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiBaseline", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 360, 0., 180.);


    hMETBaselineTauId = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauId", "MET_BaseLineTauId", 400, 0.0, 500.0);
    hMETBaselineTauId120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauId120", "MET_BaseLineTauId120", 400, 0.0, 500.0);
    hMETBaselineTauId150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauId150", "MET_BaseLineTauId150", 400, 0.0, 500.0);
    hMETBaselineTauId120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauId120150", "MET_BaseLineTauId120150;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauId100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauId100120", "MET_BaseLineTauId100120;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauId80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauId80100", "MET_BaseLineTauId80100;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauId7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauId7080", "MET_BaseLineTauId7080;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauId6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauId6070", "MET_BaseLineTauId6070;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauId5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauId5060", "MET_BaseLineTauId5060;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauId4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauId4050", "MET_BaseLineTauId4050;PF MET", 400, 0.0, 500.0);
    
    hMETBaselineTauIdJets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets", "MET_BaseLineTauIdJets", 400, 0.0, 500.0);
    hMETBaselineTauIdJets120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets120", "MET_BaseLineTauIdJets120", 400, 0.0, 500.0);
    hMETBaselineTauIdJets150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets150", "MET_BaseLineTauIdJets150", 400, 0.0, 500.0);
    hMETBaselineTauIdJets120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets120150", "MET_BaseLineTauIdJets120150;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdJets100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets100120", "MET_BaseLineTauIdJets100120;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdJets80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets80100", "MET_BaseLineTauIdJets80100;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdJets7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets7080", "MET_BaseLineTauIdJets7080;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdJets6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets6070", "MET_BaseLineTauIdJets6070;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdJets5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets5060", "MET_BaseLineTauIdJets5060;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdJets4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdJets4050", "MET_BaseLineTauIdJets4050;PF MET", 400, 0.0, 500.0);
       
    hMETBaselineTauIdBtag = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag", "MET_BaseLineTauIdBtag;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBtag150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag150", "MET_BaseLineTauIdBtag150;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBtag120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag120", "MET_BaseLineTauIdBtag120;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBtag120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag120150", "MET_BaseLineTauIdBtag120150;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBtag100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag100120", "MET_BaseLineTauIdBtag100120;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBtag80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag80100", "MET_BaseLineTauIdBtag80100;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBtag7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag7080", "MET_BaseLineTauIdBtag7080;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBtag6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag6070", "MET_BaseLineTauIdBtag6070;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBtag5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag5060", "MET_BaseLineTauIdBtag5060;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBtag4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBtag4050", "MET_BaseLineTauIdBtag4050;PF MET", 400, 0.0, 500.0);


    hMETBaselineTauIdBveto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto", "MET_BaseLineTauIdBveto;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBveto150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto150", "MET_BaseLineTauIdBveto150;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBveto120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto120", "MET_BaseLineTauIdBveto120;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBveto120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto120150", "MET_BaseLineTauIdBveto120150;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBveto100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto100120", "MET_BaseLineTauIdBveto100120;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBveto80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto80100", "MET_BaseLineTauIdBveto80100;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBveto7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto7080", "MET_BaseLineTauIdBveto7080;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBveto6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto6070", "MET_BaseLineTauIdBveto6070;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBveto5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto5060", "MET_BaseLineTauIdBveto5060;PF MET", 400, 0.0, 500.0);
    hMETBaselineTauIdBveto4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_BaseLineTauIdBveto4050", "MET_BaseLineTauIdBveto4050;PF MET", 400, 0.0, 500.0);
  
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

    hMTBaselineTauIdBveto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBveto", "MTBaseLineTauIdBveto", 400, 0.0, 400.0);
    hMTBaselineTauIdBveto150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBveto150", "MTBaseLineTauIdBveto150", 400, 0., 400.);
    hMTBaselineTauIdBveto120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBveto120", "MTBaseLineTauIdBveto120", 400, 0., 400.);
    hMTBaselineTauIdBveto120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBveto120150", "MTBaseLineTauIdBveto120150", 400, 0., 400.);
    hMTBaselineTauIdBveto100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBveto100120", "MTBaseLineTauIdBveto100120", 400, 0., 400.);
    hMTBaselineTauIdBveto80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBveto80100", "MTBaseLineTauIdBveto80100", 400, 0., 400.);
    hMTBaselineTauIdBveto7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBveto7080", "MTBaseLineTauIdBveto7080", 400, 0., 400.);
    hMTBaselineTauIdBveto6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBveto6070", "MTBaseLineTauIdBveto6070", 400, 0., 400.);
    hMTBaselineTauIdBveto5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBveto5060", "MTBaseLineTauIdBveto5060", 400, 0., 400.);
    hMTBaselineTauIdBveto4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBveto4050", "MTBaseLineTauIdBveto4050", 400, 0., 400.);

    hMTBaselineTauIdBvetoDphi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBvetoDphi", "MTBaseLineTauIdBvetoDphi", 400, 0.0, 400.0);
    hMTBaselineTauIdBvetoDphi150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBvetoDphi150", "MTBaseLineTauIdBvetoDphi150", 400, 0., 400.);
    hMTBaselineTauIdBvetoDphi120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBvetoDphi120", "MTBaseLineTauIdBvetoDphi120", 400, 0., 400.);
    hMTBaselineTauIdBvetoDphi120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBvetoDphi120150", "MTBaseLineTauIdBvetoDphi120150", 400, 0., 400.);
    hMTBaselineTauIdBvetoDphi100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBvetoDphi100120", "MTBaseLineTauIdBvetoDphi100120", 400, 0., 400.);
    hMTBaselineTauIdBvetoDphi80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBvetoDphi80100", "MTBaseLineTauIdBvetoDphi80100", 400, 0., 400.);
    hMTBaselineTauIdBvetoDphi7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBvetoDphi7080", "MTBaseLineTauIdBvetoDphi7080", 400, 0., 400.);
    hMTBaselineTauIdBvetoDphi6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBvetoDphi6070", "MTBaseLineTauIdBveto6Dphi070", 400, 0., 400.);
    hMTBaselineTauIdBvetoDphi5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBvetoDphi5060", "MTBaseLineTauIdBvetoDphi5060", 400, 0., 400.);
    hMTBaselineTauIdBvetoDphi4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTBaseLineTauIdBvetoDphi4050", "MTBaseLineTauIdBvetoDphi4050", 400, 0., 400.);

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

    hMTInvertedTauIdJetWithRtau  = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJetWithRtau", "MTInvertedTauIdJetWithRtau", 400, 0., 400.);
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


    // before b tagging for factorised b tagging
    hMTInvertedTauIdJetDphi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJetDphi", "MTInvertedTauIdJetDphi", 400, 0., 400.);
    hMTInvertedTauIdJetDphi150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJetDphi150", "MTInvertedTauIdJet150Dphi", 400, 0., 400.);
    hMTInvertedTauIdJetDphi120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJetDphi120", "MTInvertedTauIdJet120Dphi", 400, 0., 400.);
    hMTInvertedTauIdJetDphi120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJetDphi120150", "MTInvertedTauIdJet120150Dphi", 400, 0., 400.);
    hMTInvertedTauIdJetDphi100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJetDphi100120", "MTInvertedTauIdJet100120Dphi", 400, 0., 400.);
    hMTInvertedTauIdJetDphi80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJetDphi80100", "MTInvertedTauIdJet80100Dphi", 400, 0., 400.);
    hMTInvertedTauIdJetDphi7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJetDphi7080", "MTInvertedTauIdJet7080Dphi", 400, 0., 400.);
    hMTInvertedTauIdJetDphi6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJetDphi6070", "MTInvertedTauIdJet6070Dphi", 400, 0., 400.);
    hMTInvertedTauIdJetDphi5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJetDphi5060", "MTInvertedTauIdJet5060Dphi", 400, 0., 400.);
    hMTInvertedTauIdJetDphi4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdJetDphi4050", "MTInvertedTauIdJet4050Dphi", 400, 0., 400.);

    hNBInvertedTauIdJetDphi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJetDphi", "NBInvertedTauIdJetDphi", 10, 0., 10.);
    hNBInvertedTauIdJetDphi150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJetDphi150", "NBInvertedTauIdJet150Dphi", 10, 0., 10.);
    hNBInvertedTauIdJetDphi120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJetDphi120", "NBInvertedTauIdJet120Dphi", 10, 0., 10.);
    hNBInvertedTauIdJetDphi120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJetDphi120150", "NBInvertedTauIdJet120150Dphi", 10, 0., 10.);
    hNBInvertedTauIdJetDphi100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJetDphi100120", "NBInvertedTauIdJet100120Dphi", 10, 0., 10.);
    hNBInvertedTauIdJetDphi80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJetDphi80100", "NBInvertedTauIdJet80100Dphi", 10, 0., 10.);
    hNBInvertedTauIdJetDphi7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJetDphi7080", "NBInvertedTauIdJet7080Dphi", 10, 0., 10.);
    hNBInvertedTauIdJetDphi6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJetDphi6070", "NBInvertedTauIdJet6070Dphi", 10, 0., 10.);
    hNBInvertedTauIdJetDphi5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJetDphi5060", "NBInvertedTauIdJet5060Dphi", 10, 0., 10.);
    hNBInvertedTauIdJetDphi4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJetDphi4050", "NBInvertedTauIdJet4050Dphi", 10, 0., 10.);

    hNBInvertedTauIdJet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJet", "NBInvertedTauIdJet", 10, 0., 10.);
    hNBInvertedTauIdJet150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJet150", "NBInvertedTauIdJet150", 10, 0., 10.);
    hNBInvertedTauIdJet120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJet120", "NBInvertedTauIdJet120", 10, 0., 10.);
    hNBInvertedTauIdJet120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJet120150", "NBInvertedTauIdJet120150", 10, 0., 10.);
    hNBInvertedTauIdJet100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJet100120", "NBInvertedTauIdJet100120", 10, 0., 10.);
    hNBInvertedTauIdJet80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJet80100", "NBInvertedTauIdJet80100", 10, 0., 10.);
    hNBInvertedTauIdJet7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJet7080", "NBInvertedTauIdJet7080", 10, 0., 10.);
    hNBInvertedTauIdJet6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJet6070", "NBInvertedTauIdJet6070", 10, 0., 10.);
    hNBInvertedTauIdJet5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJet5060", "NBInvertedTauIdJet5060", 10, 0., 10.);
    hNBInvertedTauIdJet4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NBInvertedTauIdJet4050", "NBInvertedTauIdJet4050", 10, 0., 10.);

    hNJetInvertedTauId = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJet", "NJetInvertedTauIdJet", 10, 0., 10.);
    hNJetInvertedTauId150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJet150", "NJetInvertedTauIdJet150", 10, 0., 10.);
    hNJetInvertedTauId120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJet120", "NJetInvertedTauIdJet120", 10, 0., 10.);
    hNJetInvertedTauId120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJet120150", "NJetInvertedTauIdJet120150", 10, 0., 10.);
    hNJetInvertedTauId100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJet100120", "NJetInvertedTauIdJet100120", 10, 0., 10.);
    hNJetInvertedTauId80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJet80100", "NJetInvertedTauIdJet80100", 10, 0., 10.);
    hNJetInvertedTauId7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJet7080", "NJetInvertedTauIdJet7080", 10, 0., 10.);
    hNJetInvertedTauId6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJet6070", "NJetInvertedTauIdJet6070", 10, 0., 10.);
    hNJetInvertedTauId5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJet5060", "NJetInvertedTauIdJet5060", 10, 0., 10.);
    hNJetInvertedTauId4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJet4050", "NJetInvertedTauIdJet4050", 10, 0., 10.);

    hNJetInvertedTauIdMet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJetMet", "NJetInvertedTauIdJetMet", 10, 0., 10.);
    hNJetInvertedTauIdMet150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJetMet150", "NJetInvertedTauIdJetMet150",10, 0., 10.);
    hNJetInvertedTauIdMet120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJetMet120", "NJetInvertedTauIdJetMet120", 10, 0., 10.);
    hNJetInvertedTauIdMet120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJetMet120150", "NJetInvertedTauIdJetMet120150", 10, 0., 10.);
    hNJetInvertedTauIdMet100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJetMet100120", "NJetInvertedTauIdJetMet100120", 10, 0., 10.);
    hNJetInvertedTauIdMet80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJetMet80100", "NJetInvertedTauIdJetMet80100", 10, 0., 10.);
    hNJetInvertedTauIdMet7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJetMet7080", "NJetInvertedTauIdJetMet7080", 10, 0., 10.);
    hNJetInvertedTauIdMet6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJetMet6070", "NJetInvertedTauIdJetMet6070", 10, 0., 10.);
    hNJetInvertedTauIdMet5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJetMet5060", "NJetInvertedTauIdJetMet5060", 10, 0., 10.);
    hNJetInvertedTauIdMet4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "NJetInvertedTauIdJetMet4050", "NJetInvertedTauIdJet4Met050", 10, 0., 10.);

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

    hMTInvertedTauIdBveto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBveto", "MTInvertedTauIdBveto", 400, 0., 400.);
    hMTInvertedTauIdBveto150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBveto150", "MTInvertedTauIdBveto150", 400, 0., 400.);
    hMTInvertedTauIdBveto120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBveto120", "MTInvertedTauIdBveto120", 400, 0., 400.);
    hMTInvertedTauIdBveto120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBveto120150", "MTInvertedTauIdBveto120150", 400, 0., 400.);
    hMTInvertedTauIdBveto100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBveto100120", "MTInvertedTauIdBveto100120", 400, 0., 400.);
    hMTInvertedTauIdBveto80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBveto80100", "MTInvertedTauIdBveto80100", 400, 0., 400.);
    hMTInvertedTauIdBveto7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBveto7080", "MTInvertedTauIdBveto7080", 400, 0., 400.);
    hMTInvertedTauIdBveto6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBveto6070", "MTInvertedTauIdBveto6070", 400, 0., 400.);
    hMTInvertedTauIdBveto5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBveto5060", "MTInvertedTauIdBveto5060", 400, 0., 400.);
    hMTInvertedTauIdBveto4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBveto4050", "MTInvertedTauIdBveto4050", 400, 0., 400.);

    hMTInvertedTauIdBvetoDphi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBvetoDphi", "MTInvertedTauIdBvetoDphi", 400, 0., 400.);
    hMTInvertedTauIdBvetoDphi150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBvetoDphi150", "MTInvertedTauIdBvetoDphi150", 400, 0., 400.);
    hMTInvertedTauIdBvetoDphi120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBvetoDphi120", "MTInvertedTauIdBvetoDphi120", 400, 0., 400.);
    hMTInvertedTauIdBvetoDphi120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBvetoDphi120150", "MTInvertedTauIdBvetoDphi120150", 400, 0., 400.);
    hMTInvertedTauIdBvetoDphi100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBvetoDphi100120", "MTInvertedTauIdBvetoDphi100120", 400, 0., 400.);
    hMTInvertedTauIdBvetoDphi80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBvetoDphi80100", "MTInvertedTauIdBvetoDphi80100", 400, 0., 400.);
    hMTInvertedTauIdBvetoDphi7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBvetoDphi7080", "MTInvertedTauIdBvetoDphi7080", 400, 0., 400.);
    hMTInvertedTauIdBvetoDphi6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBvetoDphi6070", "MTInvertedTauIdBvetoDphi6070", 400, 0., 400.);
    hMTInvertedTauIdBvetoDphi5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBvetoDphi5060", "MTInvertedTauIdBvetoDphi5060", 400, 0., 400.);
    hMTInvertedTauIdBvetoDphi4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MTInvertedTauIdBvetoDphi4050", "MTInvertedTauIdBvetoDphi4050", 400, 0., 400.);

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
// after b tagging 
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

    hHiggsMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass", "HiggsMass", 400, 0., 500.);
    hHiggsMass150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass150", "HiggsMass150", 400, 0., 500.);
    hHiggsMass120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass120", "HiggsMass120", 400, 0., 500.);
    hHiggsMass120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass120150", "HiggsMass120150", 400, 0., 500.);
    hHiggsMass100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass100120", "HiggsMass100120", 400, 0., 500.);
    hHiggsMass80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass80100", "HiggsMass80100", 400, 0., 500.);
    hHiggsMass7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggMass7080", "HiggsMass7080", 400, 0., 500.);
    hHiggsMass6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass6070", "HiggsMass6070", 400, 0., 500.);
    hHiggsMass5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass5060", "HiggsMass5060", 400, 0., 500.);
    hHiggsMass4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMass4050", "HiggsMass4050", 400, 0., 500.);

    hHiggsMassPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi", "HiggsMassPhi", 400, 0., 500.);
    hHiggsMassPhi150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi150", "HiggsMassPhi150", 400, 0., 500.);
    hHiggsMassPhi120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi120", "HiggsMassPhi120", 400, 0., 500.);
    hHiggsMassPhi120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi120150", "HiggsMassPhi120150", 400, 0., 500.);
    hHiggsMassPhi100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi100120", "HiggsMassPhi100120", 400, 0., 500.);
    hHiggsMassPhi80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi80100", "HiggsMassPhi80100", 400, 0., 500.);
    hHiggsMassPhi7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi7080", "HiggsMassPhi7080", 400, 0., 500.);
    hHiggsMassPhi6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi6070", "HiggsMassPhi6070", 400, 0., 500.);
    hHiggsMassPhi5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi5060", "HiggsMassPhi5060", 400, 0., 500.);
    hHiggsMassPhi4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "HiggsMassPhi4050", "HiggsMassPhi4050", 400, 0., 500.);

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


    //    hMTBaselineTauIdJet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MT_BaseLineTauIdJets", "MT_BaseLineTauIdJets;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);

    hMETInvertedTauId = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauId", "MET_InvertedTauId;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0,500.0);
    hMETInvertedTauId150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauId150", "MET_InvertedTauId150", 400, 0.0, 500.0);
    hMETInvertedTauId120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauId120", "MET_InvertedTauId120", 400, 0.0, 500.0);
    hMETInvertedTauId120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauId120150", "MET_InvertedTauId120150", 400, 0.0, 500.0);
    hMETInvertedTauId100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauId100120", "MET_InvertedTauId100120", 400, 0.0, 500.0); 
    hMETInvertedTauId80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauId80100", "MET_InvertedTauId80100", 400, 0.0, 500.0); 
    hMETInvertedTauId7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauId7080", "MET_InvertedTauId7080", 400, 0.0, 500.0); 
    hMETInvertedTauId6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauId6070", "MET_InvertedTauId6070", 400, 0.0, 500.0); 
    hMETInvertedTauId5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauId5060", "MET_InvertedTauId5060", 400, 0.0, 500.0); 
    hMETInvertedTauId4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauId4050", "MET_InvertedTauId4050", 400, 0.0, 500.0); 

    hMETInvertedTauIdJets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets", "MET_InvertedTauIdJets;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 500.0);
    hMETInvertedTauIdJets150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets150", "MET_InvertedTauIdJets150", 400, 0.0, 500.0);
    hMETInvertedTauIdJets120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets120", "MET_InvertedTauIdJets120", 400, 0.0, 500.0);
    hMETInvertedTauIdJets120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets120150", "MET_InvertedTauIdJets120150", 400, 0.0, 500.0);
    hMETInvertedTauIdJets100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets100120", "MET_InvertedTauIdJets100120", 400, 0.0, 500.0); 
    hMETInvertedTauIdJets80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets80100", "MET_InvertedTauIdJets80100", 400, 0.0, 500.0); 
    hMETInvertedTauIdJets7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets7080", "MET_InvertedTauIdJets7080", 400, 0.0, 500.0); 
    hMETInvertedTauIdJets6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets6070", "MET_InvertedTauIdJets6070", 400, 0.0, 500.0); 
    hMETInvertedTauIdJets5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets5060", "MET_InvertedTauIdJets5060", 400, 0.0, 500.0); 
    hMETInvertedTauIdJets4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdJets4050", "MET_InvertedTauIdJets4050", 400, 0.0, 500.0);
   
    hMETInvertedTauIdBtag = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag", "MET_InvertedTauIdBtag", 400, 0.0, 500.0);
    hMETInvertedTauIdBtag150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag150", "MET_InvertedTauIdBtag150", 400, 0.0, 500.0);
    hMETInvertedTauIdBtag120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag120", "MET_InvertedTauIdBtag120", 400, 0.0, 500.0);
    hMETInvertedTauIdBtag120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag120150", "MET_InvertedTauIdBtag120150", 400, 0.0, 500.0);
    hMETInvertedTauIdBtag100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag100120", "MET_InvertedTauIdBtag100120", 400, 0.0, 500.0); 
    hMETInvertedTauIdBtag80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag80100", "MET_InvertedTauIdBtag80100", 400, 0.0, 500.0); 
    hMETInvertedTauIdBtag7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag7080", "MET_InvertedTauIdBtag7080", 400, 0.0, 500.0); 
    hMETInvertedTauIdBtag6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag6070", "MET_InvertedTauIdBtag6070", 400, 0.0, 500.0); 
    hMETInvertedTauIdBtag5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag5060", "MET_InvertedTauIdBtag5060", 400, 0.0, 500.0); 
    hMETInvertedTauIdBtag4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBtag4050", "MET_InvertedTauIdBtag4050", 400, 0.0, 500.0); 

    hMETInvertedTauIdBveto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto", "MET_InvertedTauIdBveto", 400, 0.0, 500.0);
    hMETInvertedTauIdBveto150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto150", "MET_InvertedTauIdBveto150", 400, 0.0, 500.0);
    hMETInvertedTauIdBveto120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto120", "MET_InvertedTauIdBveto120", 400, 0.0, 400.0);
    hMETInvertedTauIdBveto120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto120150", "MET_InvertedTauIdBveto120150", 400, 0.0, 500.0);
    hMETInvertedTauIdBveto100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto100120", "MET_InvertedTauIdBveto100120", 400, 0.0, 500.0); 
    hMETInvertedTauIdBveto80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto80100", "MET_InvertedTauIdBveto80100", 400, 0.0, 500.0); 
    hMETInvertedTauIdBveto7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto7080", "MET_InvertedTauIdBveto7080", 400, 0.0, 500.0); 
    hMETInvertedTauIdBveto6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto6070", "MET_InvertedTauIdBveto6070", 400, 0.0, 500.0); 
    hMETInvertedTauIdBveto5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto5060", "MET_InvertedTauIdBveto5060", 400, 0.0, 500.0); 
    hMETInvertedTauIdBveto4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "MET_InvertedTauIdBveto4050", "MET_InvertedTauIdBveto4050", 400, 0.0, 500.0); 

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

    hDeltaPhiInvertedNoB = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInvertedNoB", "deltaPhiNoB;#Delta#phi(tau,MET)", 360, 0., 180.);
    hDeltaPhiInvertedNoB150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInvertedNoB150", "deltaPhiNoB;#Delta#phi(tau,MET) 150", 360, 0., 180.);
    hDeltaPhiInvertedNoB120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInvertedNoB120", "deltaPhiNoB;#Delta#phi(tau,MET) 120", 360, 0., 180.);
    hDeltaPhiInvertedNoB120150 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInvertedNoB120150", "deltaPhiNoB;#Delta#phi(tau,MET) 120150", 360, 0., 180.);
    hDeltaPhiInvertedNoB100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInvertedNoB100120", "deltaPhiNoB;#Delta#phi(tau,MET) 100120", 360, 0., 180.);
    hDeltaPhiInvertedNoB80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInvertedNoB80100", "deltaPhiNoB;#Delta#phi(tau,MET) 80100", 360, 0., 180.);
    hDeltaPhiInvertedNoB7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInvertedNoB7080", "deltaPhiNoB;#Delta#phi(tau,MET) 7080", 360, 0., 180.);
    hDeltaPhiInvertedNoB6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInvertedNoB6070", "deltaPhiNoB;#Delta#phi(tau,MET) 6070", 360, 0., 180.);
    hDeltaPhiInvertedNoB5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInvertedNoB5060", "deltaPhiNoB;#Delta#phi(tau,MET) 5060", 360, 0., 180.);
    hDeltaPhiInvertedNoB4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhiInvertedNoB4050", "deltaPhiNoB;#Delta#phi(tau,MET) 4050", 360, 0., 180.);
    hClosestDeltaPhiInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiInverted", "ClosestDeltaPhiInverted(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiInverted120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiInverted120", "ClosestDeltaPhiInverted120(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiInverted100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiInverted100120", "ClosestDeltaPhiInverted100120(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiInverted80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiInverted80100", "ClosestDeltaPhiInverted80100(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiInverted7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiInverted7080", "ClosestDeltaPhiInverted7080(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiInverted6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiInverted6070", "ClosestDeltaPhiInverted6070(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiInverted5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiInverted5060", "ClosestDeltaPhiInverted5060(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiInverted4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiInverted4050", "ClosestDeltaPhiInverted4050(jet,MET)", 360, 0., 180.);



    hDeltaPhiMHTJet1Inverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "DeltaPhiMHTJet1Inverted","DeltaPhiMHTJet1Inverted", 180, 0., 180. );
    hDeltaPhiMHTJet1Inverted120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "DeltaPhiMHTJet1Inverted120","DeltaPhiMHTJet1Inverted120", 180, 0., 180. );
    hDeltaPhiMHTJet1Inverted100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "DeltaPhiMHTJet1Inverted100120","DeltaPhiMHTJet1Inverted100120", 180, 0., 180. );
    hDeltaPhiMHTJet1Inverted80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "DeltaPhiMHTJet1Inverted80100","DeltaPhiMHTJet1Inverted80100", 180, 0., 180. );
    hDeltaPhiMHTJet1Inverted7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "DeltaPhiMHTJet1Inverted7080","DeltaPhiMHTJet1Inverted7080", 180,0,180. );
    hDeltaPhiMHTJet1Inverted6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "DeltaPhiMHTJet1Inverted6070","DeltaPhiMHTJet1Inverted6070", 180,0,180. );
    hDeltaPhiMHTJet1Inverted5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "DeltaPhiMHTJet1Inverted5060","DeltaPhiMHTJet1Inverted5060", 180,0,180. );
    hDeltaPhiMHTJet1Inverted4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "DeltaPhiMHTJet1Inverted4050","DeltaPhiMHTJet1Inverted4050", 180,0,180. );

    hDeltaPhiVsDeltaPhiMHTJet1Inverted = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet1Inverted","DeltaPhiVsDeltaPhiMHTJet1Inverted", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet1Inverted120 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet1Inverted120","DeltaPhiVsDeltaPhiMHTJet1Inverted120", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet1Inverted100120 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet1Inverted100120","DeltaPhiVsDeltaPhiMHTJet1Inverted100120", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet1Inverted80100 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet1Inverted80100","DeltaPhiVsDeltaPhiMHTJet1Inverted80100", 180, 0., 180., 180,0,180. );
  
    hDeltaPhiVsDeltaPhiMHTJet1Inverted7080 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet1Inverted7080","DeltaPhiVsDeltaPhiMHTJet1Inverted7080", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet1Inverted6070 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet1Inverted6070","DeltaPhiVsDeltaPhiMHTJet1Inverted6070", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet1Inverted5060 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet1Inverted5060","DeltaPhiVsDeltaPhiMHTJet1Inverted5060", 180, 0., 180., 180,0,180. );

    hDeltaPhiVsDeltaPhiMHTJet1Inverted4050 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet1Inverted4050","DeltaPhiVsDeltaPhiMHTJet1Inverted4050", 180, 0., 180., 180,0,180. );


    hDeltaPhiVsDeltaPhiMHTJet2Inverted = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet2Inverted","DeltaPhiVsDeltaPhiMHTJet2Inverted", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet2Inverted120 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet2Inverted120","DeltaPhiVsDeltaPhiMHTJet2Inverted120", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet2Inverted100120 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet2Inverted100120","DeltaPhiVsDeltaPhiMHTJet2Inverted100120", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet2Inverted80100 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet2Inverted80100","DeltaPhiVsDeltaPhiMHTJet2Inverted80100", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet2Inverted7080 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet2Inverted7080","DeltaPhiVsDeltaPhiMHTJet2Inverted7080", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet2Inverted6070 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet2Inverted6070","DeltaPhiVsDeltaPhiMHTJet2Inverted6070", 180, 0., 180., 180,0.,180 );
    hDeltaPhiVsDeltaPhiMHTJet2Inverted5060 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet2Inverted5060","DeltaPhiVsDeltaPhiMHTJet2Inverted5060", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet2Inverted4050 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet2Inverted4050","DeltaPhiVsDeltaPhiMHTJet2Inverted4050", 180, 0., 180., 180,0,180. );


    hDeltaPhiVsDeltaPhiMHTJet3Inverted = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet3Inverted","DeltaPhiVsDeltaPhiMHTJet3Inverted", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet3Inverted120 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet3Inverted120","DeltaPhiVsDeltaPhiMHTJet3Inverted120", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet3Inverted100120 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet3Inverted100120","DeltaPhiVsDeltaPhiMHTJet3Inverted100120", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet3Inverted80100 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet3Inverted80100","DeltaPhiVsDeltaPhiMHTJet3Inverted80100", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet3Inverted80100 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet3Inverted80100","DeltaPhiVsDeltaPhiMHTJet3Inverted80100", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet3Inverted7080 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet3Inverted7080","DeltaPhiVsDeltaPhiMHTJet3Inverted7080", 180, 0., 180., 180,0,180. );
    hDeltaPhiVsDeltaPhiMHTJet3Inverted6070 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet3Inverted6070","DeltaPhiVsDeltaPhiMHTJet3Inverted6070", 180, 0., 180., 180,0.,180 );
    hDeltaPhiVsDeltaPhiMHTJet3Inverted5060 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet3Inverted5060","DeltaPhiVsDeltaPhiMHTJet3Inverted5060", 180, 0., 180., 180,0,180. );

    hDeltaPhiVsDeltaPhiMHTJet3Inverted4050 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiVsDeltaPhiMHTJet3Inverted4050","DeltaPhiVsDeltaPhiMHTJet3Inverted4050", 180, 0., 180., 180,0,180. );

    hDeltaPhiMHTTauVsDeltaPhiMHTJet1Inverted = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiMHTTauVsDeltaPhiMHTJet1Inverted","DeltaPhiMHTTauVsDeltaPhiMHTJet1Inverted", 180, 0., 180., 180,0,180. );
    hDeltaPhiMHTTauVsDeltaPhiMHTJet2Inverted = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiMHTTauVsDeltaPhiMHTJet2Inverted","DeltaPhiMHTTauVsDeltaPhiMHTJet2Inverted", 180, 0., 180., 180,0,180. );
    hDeltaPhiMHTTauVsDeltaPhiMHTJet3Inverted = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "DeltaPhiMHTTauVsDeltaPhiMHTJet3Inverted","DeltaPhiMHTTauVsDeltaPhiMHTJet3Inverted", 180, 0., 180., 180,0,180. );



    hDeltaPhiTauVSJetInvertedAfterCut  = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiTauVSMetInvertedAfterCut", "ClosestDeltaPhiTauVSMetInvertedAfterCut(jet,MET)", 180, 0., 180.,180, 0., 180.); 

    hDeltaPhiTauVSJetInverted  = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiTauVSMetInverted", "ClosestDeltaPhiTauVSMetInverted(jet,MET)", 180, 0., 180.,180, 0., 180.);  
    hDeltaPhiTauVSJetInverted120  = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiTauVSMetInverted120", "ClosestDeltaPhiTauVSMetInverted120(jet,MET)", 180, 0., 180.,180, 0., 180.);  
    hDeltaPhiTauVSJetInverted100120 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiTauVSMetInverted100120", "ClosestDeltaPhiTauVSMetInverted100120(jet,MET)", 180, 0., 180.,180, 0., 180.);  
    hDeltaPhiTauVSJetInverted80100 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiTauVSMetInverted80100", "ClosestDeltaPhiTauVSMetInverted80100(jet,MET)", 180, 0., 180.,180, 0., 180.);  
    hDeltaPhiTauVSJetInverted7080 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiTauVSMetInverted7080", "ClosestDeltaPhiTauVSMetInverted7080(jet,MET)", 180, 0., 180.,180, 0., 180.);  
    hDeltaPhiTauVSJetInverted6070 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiTauVSMetInverted6070", "ClosestDeltaPhiTauVSMetInverted6070(jet,MET)", 180, 0., 180.,180, 0., 180.);  
    hDeltaPhiTauVSJetInverted5060 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiTauVSMetInverted5060", "ClosestDeltaPhiTauVSMetInverted5060(jet,MET)", 180, 0., 180.,180, 0., 180.);  
    hDeltaPhiTauVSJetInverted4050 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiTauVSMetInverted4050", "ClosestDeltaTauVSMetPhiInverted4050(jet,MET)", 180, 0., 180.,180, 0., 180.);
   
    hClosestDeltaPhiBase = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiBase", "ClosestDeltaPhiBase(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiBase120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiBase120", "ClosestDeltaPhiBase120(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiBase100120 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiBase100120", "ClosestDeltaPhiBase100120(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiBase80100 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiBase80100", "ClosestDeltaPhiBase80100(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiBase7080 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiBase7080", "ClosestDeltaPhiBase7080(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiBase6070 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiBase6070", "ClosestDeltaPhiBase6070(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiBase5060 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiBase5060", "ClosestDeltaPhiBase5060(jet,MET)", 360, 0., 180.);  
    hClosestDeltaPhiBase4050 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "ClosestDeltaPhiBase4050", "ClosestDeltaPhiBase4050(jet,MET)", 360, 0., 180.);
          
    hSelectedTauEtMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_pT_AfterMetCut", "SelectedTau_pT_AfterMetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEtaMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_eta_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.1", 300, -3.0, 3.0);
    hSelectedTauPhiMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_phi_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtauMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_Rtau_AfterMetCut", "SelectedTau_Rtau_AfterMetCut;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);


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
      //      producer->produces<std::vector<pat::Muon> >("selectedVetoMuonsBeforeIsolation");
      //      producer->produces<std::vector<pat::Muon> >("selectedVetoMuons");
      producer->produces<std::vector<pat::Muon> >("selectedVetoMuonsBeforeIsolationAndPtAndEtaCuts");
      producer->produces<std::vector<pat::Muon> >("selectedVetoMuonsBeforePtAndEtaCuts");
    }
  }



  bool SignalAnalysisInvertedTau::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    fEventWeight.updatePrescale(iEvent); // set prescale
    fTree.setPrescaleWeight(fEventWeight.getWeight());

 

    // Vertex weight
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
    hSelectionFlow->Fill(kQCDOrderVertexSelection);
    
    // test for pile-up dependence
    //    if (nVertices > 12 )  return false;
    //    if (nVertices < 13 || nVertices > 18 )  return false;
    //    if (nVertices < 19 )  return false;
    increment(fVertexFilterCounter);

      
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
        
    
    // Apply trigger and HLT_MET cut or trigger parametrisation
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);
    hSelectionFlow->Fill(kQCDOrderTrigger);
  
    if(triggerData.hasTriggerPath()) // protection if TriggerSelection is disabled
      fTree.setHltTaus(triggerData.getTriggerTaus());

    hVerticesTriggeredBeforeWeight->Fill(nVertices, myWeightBeforeVertexReweighting);
    hVerticesTriggeredAfterWeight->Fill(nVertices);

//------ GenParticle analysis (must be done here when we effectively trigger all MC)
    GenParticleAnalysis::Data genData;
    if (!iEvent.isRealData()) {
      genData = fGenparticleAnalysis.analyze(iEvent, iSetup);
      fTree.setGenMET(genData.getGenMET());
    }
   

    // Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    //hSelectionFlow->Fill(kSignalOrderVertexSelection);


  
    // TauID
    //    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
    //   TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup);
    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
  
    //    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    if(!tauData.passedEvent()) return false; // Require at least one tau

    increment(fTauCandidateCounter);

    // tauID cuts applied to inverted and baseline taus    
    // nprongs
    hSelectionFlow->Fill(kQCDOrderTauCandidateSelection);

   
    //   std::cout << "taus  " << tauData.getSelectedTausBeforeIsolation().size() << std::endl;

    edm::PtrVector<pat::Tau> myOneProngTaus;
    edm::PtrVector<pat::Tau> myOneProngRtauPassedTaus;    
    for(edm::PtrVector<pat::Tau>::const_iterator iTau = tauData.getSelectedTausBeforeIsolation().begin(); iTau != tauData.getSelectedTausBeforeIsolation().end(); ++iTau) {
      //      std::cout << "tracks  " << (*iTau)->signalPFChargedHadrCands().size() << std::endl;
      if((*iTau)->signalPFChargedHadrCands().size() == 1) {
	//std::cout << "tracks  " << (*iTau)->signalPFChargedHadrCands().size() << std::endl;
         myOneProngTaus.push_back(*iTau);
	 hSelectedTauLeadingTrackPt->Fill((*iTau)->leadPFChargedHadrCand()->pt());
	 hSelectedTauRtau->Fill((*iTau)->leadPFChargedHadrCand()->p() / (*iTau)->p() );
     
	 if((*iTau)->leadPFChargedHadrCand()->p() / (*iTau)->p()  > 0.7 )
	   myOneProngRtauPassedTaus.push_back(*iTau);
      }
    }
 

 

    //  Nprongs cut
    if (myOneProngTaus.size() == 0) return false; 
    increment(fNprongsAfterTauIDCounter);
    //    if (!tauData.selectedTauPassesNProngs()) return false;
    
   
    // Rtau cut
    if (myOneProngRtauPassedTaus.size() == 0) return false;
    increment(fRtauAfterTauIDCounter);
    //    if (!tauData.selectedTauPassesRtau()) return false;
    
    
    std::string myTauIsolation = "byMediumCombinedIsolationDeltaBetaCorr";
    
    /*    edm::PtrVector<pat::Tau> myBestTauCandidate;    
    if (myOneProngRtauPassedTaus.size())
      myBestTauCandidate.push_back(myOneProngRtauPassedTaus);
    */



    // Common for baseline and inverted
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    // Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());



    ////////////////////////////////////////////////////////////////////////////////////////////////
  // baseline tau-id and selection starts 

  //    if (tauData.selectedTauPassesDiscriminator(myTauIsolation, 0.5)  && tauData.selectedTauPassesNProngs() && tauData.selectedTauPassesRtau() ) {
  
    edm::PtrVector<pat::Tau> myOneProngRtauPassedIsolatedTaus;  
    edm::Ptr<pat::Tau> selectedTau;
    //    bool isolatedTauFound = false;
    //    double maxTauDiscriminator = 0;

    
    for(edm::PtrVector<pat::Tau>::const_iterator iTau = myOneProngRtauPassedTaus.begin(); iTau != myOneProngRtauPassedTaus.end(); ++iTau) {
      
      
      if ( (*iTau)->tauID(myTauIsolation) < 0.5 ) continue;
	//	std::cout <<"PASSES TAU DISCR" << std::endl;
      hTauDiscriminator->Fill((*iTau)->tauID("byRawCombinedIsolationDeltaBetaCorr"));
      increment(fTausExistCounter);
  
      FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, (**iTau));
      //        FakeTauIdentifier::MCSelectedTauMatchType tauMatchData.getTauMatchType() = fFakeTauIdentifier.matchTauToMC(iEvent, (**iTau));
      //      bool myFakeTauStatus = fFakeTauIdentifier.isFakeTau(tauMatchData.getTauMatchType()); // True if the selected tau is a fake
      // Below "genuine tau" is in the context of embedding (i.e. irrespective of the tau decay)
      if((fOnlyGenuineTaus && !fFakeTauIdentifier.isEmbeddingGenuineTau(tauMatchData.getTauMatchType()))) continue;
    
	
      // Apply scale factor for fake tau
      if (!iEvent.isRealData())
	//	fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(myTauMatch, (*iTau)->eta()));
      fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), (*iTau)->eta()));

      // plot leading track without pt cut
      increment(fTauFakeScaleFactorCounter);

      
      if(iEvent.isRealData())
	fTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
      // Apply trigger scale factor here, because it depends only on tau
      TriggerEfficiencyScaleFactor::Data triggerWeight = fTriggerEfficiencyScaleFactor.applyEventWeight((**iTau), iEvent.isRealData(), fEventWeight);
      increment(fTriggerScaleFactorCounter);
      
      if(fProduce) {
	std::auto_ptr<std::vector<pat::Tau> > saveTaus(new std::vector<pat::Tau>());
	copyPtrToVector(tauData.getSelectedTaus(), *saveTaus);
	iEvent.put(saveTaus, "selectedTaus");
      }

      myOneProngRtauPassedIsolatedTaus.push_back(*iTau);
      
      /*   
      if ( (*iTau)->tauID(myTauIsolation) > maxTauDiscriminator ) {
	maxTauDiscriminator  = (*iTau)->tauID(myTauIsolation);
	selectedTau = *iTau;
	isolatedTauFound = true;
	}  
      */    
    }
  
  
    if ( myOneProngRtauPassedIsolatedTaus.size() > 0) {
      
      selectedTau = *(myOneProngRtauPassedIsolatedTaus.begin());
      increment(fBaselineTauIDCounter);
      //      hSelectionFlow->Fill(kSignalOrderTauID);
    
      //      if (myFakeTauStatus) hSelectionFlowVsVerticesFakeTaus->Fill(nVertices, kSignalOrderTauID);    

      if (electronVetoData.passedEvent()) {
	increment(fBaselineEvetoCounter); 
	
	if (muonVetoData.passedEvent()) {
	  increment(fBaselineMuvetoCounter);
	  
	 

	  JetSelection::Data jetDataBase = fJetSelection.analyze(iEvent, iSetup,  selectedTau,  nVertices); 
	  METSelection::Data metDataBase = fMETSelection.analyze(iEvent, iSetup, selectedTau, jetDataBase.getAllJets());

	  hNJetBaselineTauId->Fill(jetDataBase.getSelectedJets().size());  
	  if(metDataBase.passedEvent()) hNJetBaselineTauIdMet->Fill(jetDataBase.getSelectedJets().size()); 

	  hMETBaselineTauId->Fill(metDataBase.getSelectedMET()->et());  
	  if ( selectedTau->pt() > 150  ) hMETBaselineTauId150->Fill(metDataBase.getSelectedMET()->et());
	  if ( selectedTau->pt() > 120  ) hMETBaselineTauId120->Fill(metDataBase.getSelectedMET()->et());
	  if ( selectedTau->pt() > 120 && selectedTau->pt() < 150 ) hMETBaselineTauId120150->Fill(metDataBase.getSelectedMET()->et());
	  if ( selectedTau->pt() > 100 && selectedTau->pt() < 120 ) hMETBaselineTauId100120->Fill(metDataBase.getSelectedMET()->et());
	  if ( selectedTau->pt() > 80 && selectedTau->pt() < 100  ) hMETBaselineTauId80100->Fill(metDataBase.getSelectedMET()->et());
	  if ( selectedTau->pt() > 70 && selectedTau->pt() < 80 ) hMETBaselineTauId7080->Fill(metDataBase.getSelectedMET()->et());
	  if ( selectedTau->pt() > 60 && selectedTau->pt() < 70 ) hMETBaselineTauId6070->Fill(metDataBase.getSelectedMET()->et());
	  if ( selectedTau->pt() > 50 && selectedTau->pt() < 60 ) hMETBaselineTauId5060->Fill(metDataBase.getSelectedMET()->et());
	  if ( selectedTau->pt() > 40 && selectedTau->pt() < 50 ) hMETBaselineTauId4050->Fill(metDataBase.getSelectedMET()->et());
	  	  

	  if(jetDataBase.passedEvent()) {
	    increment(fBaselineJetsCounter);

	    //	    METSelection::Data metDataBase = fMETSelection.analyze(iEvent, iSetup, selectedTau, jetDataBase.getAllJets());

	    
	    // Met with after jets
	    hMETBaselineTauIdJets->Fill(metDataBase.getSelectedMET()->et());  
	    if ( selectedTau->pt() > 150  ) hMETBaselineTauIdJets150->Fill(metDataBase.getSelectedMET()->et());
	    if ( selectedTau->pt() > 120  ) hMETBaselineTauIdJets120->Fill(metDataBase.getSelectedMET()->et());
	    if ( selectedTau->pt() > 120 && selectedTau->pt() < 150 ) hMETBaselineTauIdJets120150->Fill(metDataBase.getSelectedMET()->et());
	    if ( selectedTau->pt() > 100 && selectedTau->pt() < 120 ) hMETBaselineTauIdJets100120->Fill(metDataBase.getSelectedMET()->et());
	    if ( selectedTau->pt() > 80 && selectedTau->pt() < 100  ) hMETBaselineTauIdJets80100->Fill(metDataBase.getSelectedMET()->et());
	    if ( selectedTau->pt() > 70 && selectedTau->pt() < 80 ) hMETBaselineTauIdJets7080->Fill(metDataBase.getSelectedMET()->et());
	    if ( selectedTau->pt() > 60 && selectedTau->pt() < 70 ) hMETBaselineTauIdJets6070->Fill(metDataBase.getSelectedMET()->et());
	    if ( selectedTau->pt() > 50 && selectedTau->pt() < 60 ) hMETBaselineTauIdJets5060->Fill(metDataBase.getSelectedMET()->et());
	    if ( selectedTau->pt() > 40 && selectedTau->pt() < 50 ) hMETBaselineTauIdJets4050->Fill(metDataBase.getSelectedMET()->et());
	    
	    
	    BTagging::Data btagDataBase = fBTagging.analyze(iEvent, iSetup, jetDataBase.getSelectedJetsPt20());

	    hNBBaselineTauIdJet->Fill(btagDataBase.getSelectedJets().size());
	    
	    if(btagDataBase.passedEvent()) {
	      // Met with b tagging	
	      hMETBaselineTauIdBtag->Fill(metDataBase.getSelectedMET()->et()); 
	      if ( selectedTau->pt() > 150  ) hMETBaselineTauIdBtag150->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 120  ) hMETBaselineTauIdBtag120->Fill(metDataBase.getSelectedMET()->et());
	      
	      if ( selectedTau->pt() > 120 && selectedTau->pt() < 150 ) hMETBaselineTauIdBtag120150->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 100 && selectedTau->pt() < 120 ) hMETBaselineTauIdBtag100120->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 80 && selectedTau->pt() < 100  ) hMETBaselineTauIdBtag80100->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 70 && selectedTau->pt() < 80 ) hMETBaselineTauIdBtag7080->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 60 && selectedTau->pt() < 70 ) hMETBaselineTauIdBtag6070->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 50 && selectedTau->pt() < 60 ) hMETBaselineTauIdBtag5060->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 40 && selectedTau->pt() < 50 ) hMETBaselineTauIdBtag4050->Fill(metDataBase.getSelectedMET()->et());	  
	    }
	    // Met with b veto
	    if( btagDataBase.getSelectedJets().size() < 1 ) {
	      hMETBaselineTauIdBveto->Fill(metDataBase.getSelectedMET()->et());  
	      if ( selectedTau->pt() > 150  ) hMETBaselineTauIdBveto150->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 120  ) hMETBaselineTauIdBveto120->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 120 && selectedTau->pt() < 150 ) hMETBaselineTauIdBveto120150->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 100 && selectedTau->pt() < 120 ) hMETBaselineTauIdBveto100120->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 80 && selectedTau->pt() < 100  ) hMETBaselineTauIdBveto80100->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 70 && selectedTau->pt() < 80 ) hMETBaselineTauIdBveto7080->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 60 && selectedTau->pt() < 70 ) hMETBaselineTauIdBveto6070->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 50 && selectedTau->pt() < 60 ) hMETBaselineTauIdBveto5060->Fill(metDataBase.getSelectedMET()->et());
	      if ( selectedTau->pt() > 40 && selectedTau->pt() < 50 ) hMETBaselineTauIdBveto4050->Fill(metDataBase.getSelectedMET()->et());	   
	    }


	    if(metDataBase.passedEvent()) {
	      increment(fBaselineMetCounter);
	      
	      double transverseMass = TransverseMass::reconstruct(*(selectedTau), *(metDataBase.getSelectedMET()) );
	      double deltaPhiBaseline = DeltaPhi::reconstruct(*(selectedTau), *(metDataBase.getSelectedMET())) * 57.3; // converted to degrees 
	      FakeMETVeto::Data fakeMETDataBase = fFakeMETVeto.analyze(iEvent, iSetup, selectedTau, jetDataBase.getSelectedJets(), metDataBase.getSelectedMET()); 
 
	      // New cut !!!!!!!!!!!
	      // deltaPhi cut as a function of deltaPhiJetMet
	      double deltaPhiTauMetCut = 130;
	      double deltaPhiJetMetCut = 30; 
	      double deltaPhiCutValue2Dim = 180 - (deltaPhiJetMetCut - fakeMETDataBase.closestDeltaPhi())*(180 - deltaPhiTauMetCut) / deltaPhiJetMetCut;
	      //    std::cout << "  new cut value " << cutValue << " deltaPhi " << deltaPhi <<   " closestDeltaPhi  " << fakeMETData.closestDeltaPhi() << std::endl;

//------ Delta phi(tau,MET) cut
	      
	      
	      hMTBaselineTauIdJet->Fill(transverseMass);  
	      if ( selectedTau->pt() > 150  ) hMTBaselineTauIdJet150->Fill(transverseMass);
	      if ( selectedTau->pt() > 120  ) hMTBaselineTauIdJet120->Fill(transverseMass);
	      if ( selectedTau->pt() > 120 && selectedTau->pt() < 150 ) hMTBaselineTauIdJet120150->Fill(transverseMass);
	      if ( selectedTau->pt() > 100 && selectedTau->pt() < 120 ) hMTBaselineTauIdJet100120->Fill(transverseMass);
	      if ( selectedTau->pt() > 80 && selectedTau->pt() < 100  ) hMTBaselineTauIdJet80100->Fill(transverseMass);
	      if ( selectedTau->pt() > 70 && selectedTau->pt() < 80 ) hMTBaselineTauIdJet7080->Fill(transverseMass);
	      if ( selectedTau->pt() > 60 && selectedTau->pt() < 70 ) hMTBaselineTauIdJet6070->Fill(transverseMass);
	      if ( selectedTau->pt() > 50 && selectedTau->pt() < 60 ) hMTBaselineTauIdJet5060->Fill(transverseMass);
	      if ( selectedTau->pt() > 40 && selectedTau->pt() < 50 ) hMTBaselineTauIdJet4050->Fill(transverseMass);

	      if( btagDataBase.getSelectedJets().size() < 1) {
		// mT with b veto and met cut      
		hMTBaselineTauIdBveto->Fill(transverseMass);   
		if ( selectedTau->pt() > 150  ) hMTBaselineTauIdBveto150->Fill(transverseMass); 
		if ( selectedTau->pt() > 120  ) hMTBaselineTauIdBveto120->Fill(transverseMass); 
		if ( selectedTau->pt() > 120 && selectedTau->pt() < 150 ) hMTBaselineTauIdBveto120150->Fill(transverseMass); 
		if ( selectedTau->pt() > 100 && selectedTau->pt() < 120 ) hMTBaselineTauIdBveto100120->Fill(transverseMass); 
		if ( selectedTau->pt() > 80 && selectedTau->pt() < 100 ) hMTBaselineTauIdBveto80100->Fill(transverseMass); 
		if ( selectedTau->pt() > 70 && selectedTau->pt() < 80 ) hMTBaselineTauIdBveto7080->Fill(transverseMass); 
		if ( selectedTau->pt() > 60 && selectedTau->pt() < 70 ) hMTBaselineTauIdBveto6070->Fill(transverseMass); 
		if ( selectedTau->pt() > 50 && selectedTau->pt() < 60 ) hMTBaselineTauIdBveto5060->Fill(transverseMass); 
		if ( selectedTau->pt() > 40 && selectedTau->pt() < 50 ) hMTBaselineTauIdBveto4050->Fill(transverseMass);
		//		if ( deltaPhiBaseline < fDeltaPhiCutValue) {
		if ( deltaPhiBaseline < deltaPhiCutValue2Dim) {
		  hMTBaselineTauIdBvetoDphi->Fill(transverseMass);   
		  if ( selectedTau->pt() > 150  ) hMTBaselineTauIdBvetoDphi150->Fill(transverseMass); 
		  if ( selectedTau->pt() > 120  ) hMTBaselineTauIdBvetoDphi120->Fill(transverseMass); 
		  if ( selectedTau->pt() > 120 && selectedTau->pt() < 150 ) hMTBaselineTauIdBvetoDphi120150->Fill(transverseMass); 
		  if ( selectedTau->pt() > 100 && selectedTau->pt() < 120 ) hMTBaselineTauIdBvetoDphi100120->Fill(transverseMass); 
		  if ( selectedTau->pt() > 80 && selectedTau->pt() < 100 ) hMTBaselineTauIdBvetoDphi80100->Fill(transverseMass); 
		  if ( selectedTau->pt() > 70 && selectedTau->pt() < 80 ) hMTBaselineTauIdBvetoDphi7080->Fill(transverseMass); 
		  if ( selectedTau->pt() > 60 && selectedTau->pt() < 70 ) hMTBaselineTauIdBvetoDphi6070->Fill(transverseMass); 
		  if ( selectedTau->pt() > 50 && selectedTau->pt() < 60 ) hMTBaselineTauIdBvetoDphi5060->Fill(transverseMass); 
		  if ( selectedTau->pt() > 40 && selectedTau->pt() < 50 ) hMTBaselineTauIdBvetoDphi4050->Fill(transverseMass);
		}
	      }
	      if(btagDataBase.passedEvent()) {
		increment(fBaselineBtagCounter);
		
		// Apply scale factor as weight to event 
		if (!iEvent.isRealData()) {
		  fBTagging.fillScaleFactorHistograms(btagDataBase); 	      // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
		  fEventWeight.multiplyWeight(btagDataBase.getScaleFactor());
		}   
		increment(fBTaggingScaleFactorCounter);
		
		
		// mT with b tagging and met cut      
		hMTBaselineTauIdBtag->Fill(transverseMass);   
		if ( selectedTau->pt() > 150  ) hMTBaselineTauIdBtag150->Fill(transverseMass); 
		if ( selectedTau->pt() > 120  ) hMTBaselineTauIdBtag120->Fill(transverseMass); 
		if ( selectedTau->pt() > 120 && selectedTau->pt() < 150 ) hMTBaselineTauIdBtag120150->Fill(transverseMass); 
		if ( selectedTau->pt() > 100 && selectedTau->pt() < 120 ) hMTBaselineTauIdBtag100120->Fill(transverseMass); 
		if ( selectedTau->pt() > 80 && selectedTau->pt() < 100 ) hMTBaselineTauIdBtag80100->Fill(transverseMass); 
		if ( selectedTau->pt() > 70 && selectedTau->pt() < 80 ) hMTBaselineTauIdBtag7080->Fill(transverseMass); 
		if ( selectedTau->pt() > 60 && selectedTau->pt() < 70 ) hMTBaselineTauIdBtag6070->Fill(transverseMass); 
		if ( selectedTau->pt() > 50 && selectedTau->pt() < 60 ) hMTBaselineTauIdBtag5060->Fill(transverseMass); 
		if ( selectedTau->pt() > 40 && selectedTau->pt() < 50 ) hMTBaselineTauIdBtag4050->Fill(transverseMass);
		
		hDeltaPhiBaseline->Fill(deltaPhiBaseline);
 	   


		if ( deltaPhiBaseline < fDeltaPhiCutValue) {
		//		if ( deltaPhiBaseline < deltaPhiCutValue2Dim ) {
		//		if ( deltaPhiBaseline < fDeltaPhiCutValue) {
		  increment(fBaselineDphi160Counter);
		}

		 

		  
		if ( deltaPhiBaseline < 120 || jetDataBase.getDeltaPhiMHTJet1() > 60 ) {
		  increment(fBaselineDeltaPhiMHTJet1CutCounter); 

		  if( deltaPhiBaseline <  150 || jetDataBase.getDeltaPhiMHTJet2() > 30 ) {
		    increment(fBaselineDeltaPhiVSDeltaPhiMHTJet1CutCounter); 
		    
		    
		    increment(fOneTauCounter);
		    //		  fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData, metDataBase);
		    if ( deltaPhiBaseline < 130) increment(fBaselineDphi130Counter);
		    hMTBaselineTauIdPhi->Fill(transverseMass);   
		    if ( selectedTau->pt() > 150  ) hMTBaselineTauIdPhi150->Fill(transverseMass);
		    if ( selectedTau->pt() > 120  ) hMTBaselineTauIdPhi120->Fill(transverseMass); 
		    if ( selectedTau->pt() > 120 && selectedTau->pt() < 150 ) hMTBaselineTauIdPhi120150->Fill(transverseMass); 
		    if ( selectedTau->pt() > 100 && selectedTau->pt() < 120 ) hMTBaselineTauIdPhi100120->Fill(transverseMass); 
		    if ( selectedTau->pt() > 80 && selectedTau->pt() < 100 ) hMTBaselineTauIdPhi80100->Fill(transverseMass); 
		    if ( selectedTau->pt() > 70 && selectedTau->pt() < 80 ) hMTBaselineTauIdPhi7080->Fill(transverseMass); 
		    if ( selectedTau->pt() > 60 && selectedTau->pt() < 70 ) hMTBaselineTauIdPhi6070->Fill(transverseMass); 
		    if ( selectedTau->pt() > 50 && selectedTau->pt() < 60 ) hMTBaselineTauIdPhi5060->Fill(transverseMass); 
		    if ( selectedTau->pt() > 40 && selectedTau->pt() < 50 ) hMTBaselineTauIdPhi4050->Fill(transverseMass);
		    
		    //		  FakeMETVeto::Data fakeMETDataBase = fFakeMETVeto.analyze(iEvent, iSetup, selectedTau, jetDataBase.getSelectedJets(), metDataBase.getSelectedMET());	     
		    hClosestDeltaPhiBase->Fill(fakeMETDataBase.closestDeltaPhi());
		    if ( selectedTau->pt() > 120 ) hClosestDeltaPhiBase120->Fill(fakeMETDataBase.closestDeltaPhi()); 
		    if ( selectedTau->pt() > 100 && selectedTau->pt() < 120 ) hClosestDeltaPhiBase100120->Fill(fakeMETDataBase.closestDeltaPhi()); 
		    if ( selectedTau->pt() > 80 && selectedTau->pt() < 100 ) hClosestDeltaPhiBase80100->Fill(fakeMETDataBase.closestDeltaPhi()); 
		    if ( selectedTau->pt() > 70 && selectedTau->pt() < 80 ) hClosestDeltaPhiBase7080->Fill(fakeMETDataBase.closestDeltaPhi()); 
		    if ( selectedTau->pt() > 60 && selectedTau->pt() < 70 ) hClosestDeltaPhiBase6070->Fill(fakeMETDataBase.closestDeltaPhi()); 
		    if ( selectedTau->pt() > 50 && selectedTau->pt() < 60 ) hClosestDeltaPhiBase5060->Fill(fakeMETDataBase.closestDeltaPhi()); 
		    if ( selectedTau->pt() > 40 && selectedTau->pt() < 50 ) hClosestDeltaPhiBase4050->Fill(fakeMETDataBase.closestDeltaPhi());		 		  
		  }      
		} 
	      }
	    }
	  }
	}
      }
    }
    ///////////////////////////////////////////////////////////////////
    // end baseline tauid and selection
    
    // Continue inverted tau selection
    /*    
	  if(metData.passedEvent()) {
	  hTransverseMassBeforeVeto->Fill(transverseMass);
	  hDeltaPhiBeforeVeto->Fill(deltaPhi);
	  } 
    */  
    
    edm::PtrVector<pat::Tau> myOneProngRtauPassedInvertedTaus;    
    for(edm::PtrVector<pat::Tau>::const_iterator iTau = myOneProngRtauPassedTaus.begin(); iTau != myOneProngRtauPassedTaus.end(); ++iTau) {
      
      if ( (*iTau)->tauID(myTauIsolation) < 0.5 ){
	//	std::cout <<"Fails TAU DISCR" << std::endl;
	myOneProngRtauPassedInvertedTaus.push_back(*iTau);
      }	
    }
    
    if (myOneProngRtauPassedIsolatedTaus.size() > 0)  return false; 
    if ( myOneProngRtauPassedInvertedTaus.size() == 0 )  return false;   
    
    hOneProngRtauPassedInvertedTaus->Fill(myOneProngRtauPassedInvertedTaus.size());
    
    edm::Ptr<pat::Tau> selectedInvertedTau;
    selectedInvertedTau  = *(myOneProngRtauPassedInvertedTaus.begin());
      
    //    if (tauData.selectedTauPassesDiscriminator(myTauIsolation, 0.5)) return false;    
    
    //    hSelectionFlow->Fill(kQCDOrderTauCandidateSelection);
    hSelectionFlow->Fill(kQCDOrderTauID);    
    // veto was successfull
    increment(fTauVetoAfterTauIDCounter); 
        
    JetSelection::Data jetDataInverted = fJetSelection.analyze(iEvent, iSetup,  selectedInvertedTau,  nVertices); 
    // Get MET object 
    METSelection::Data metDataInverted = fMETSelection.analyze(iEvent, iSetup, selectedInvertedTau, jetDataInverted.getAllJets());
    BTagging::Data btagDataInverted = fBTagging.analyze(iEvent, iSetup, jetDataInverted.getSelectedJetsPt20());
    
    double deltaPhi = DeltaPhi::reconstruct(*(selectedInvertedTau), *(metDataInverted.getSelectedMET())) * 57.3; // converted to degrees   
    double transverseMass = TransverseMass::reconstruct(*(selectedInvertedTau), *(metDataInverted.getSelectedMET()) );
    FakeMETVeto::Data fakeMETDataInverted = fFakeMETVeto.analyze(iEvent, iSetup, selectedInvertedTau, jetDataInverted.getSelectedJets(), metDataInverted.getSelectedMET());   
 
    // New cut !!!!!!!!!!!
    // deltaPhi cut as a function of deltaPhiJetMet
    double deltaPhiTauMetCut = 130;
    double deltaPhiJetMetCut = 30; 
    double deltaPhiCutValue2Dim = 180 - (deltaPhiJetMetCut - fakeMETDataInverted.closestDeltaPhi())*(180 - deltaPhiTauMetCut) / deltaPhiJetMetCut;
    //    std::cout << "  new cut value " << cutValue << " deltaPhi " << deltaPhi <<   " closestDeltaPhi  " << fakeMETData.closestDeltaPhi() << std::endl;  
  
    hSelectionFlow->Fill(kSignalOrderTauID);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Tau> > saveTaus(new std::vector<pat::Tau>());
      copyPtrToVector(tauData.getSelectedTaus(), *saveTaus);
      iEvent.put(saveTaus, "selectedTaus");
    }
  
 
    hSelectedTauEt->Fill(selectedInvertedTau->pt());
    hSelectedTauEta->Fill(selectedInvertedTau->eta());
    hSelectedTauPhi->Fill(selectedInvertedTau->phi());
    if(metDataInverted.passedEvent()) {
      //      hSelectedTauEtMetCut->Fill(selectedInvertedTau->pt());
      hTransverseMassBeforeVeto->Fill(transverseMass);
      hDeltaPhiAfterVeto->Fill(deltaPhi);
    }

    
 
    // Obtain MC matching
    MCSelectedTauMatchType myTauMatch = matchTauToMC(iEvent, selectedInvertedTau);
 
  
    //    Global electron veto
    //    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);
    hSelectionFlow->Fill(kQCDOrderElectronVeto);  

  
        
    //    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderElectronVeto, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Electron> > saveElectrons(new std::vector<pat::Electron>());
      copyPtrToVector(electronVetoData.getSelectedElectrons(), *saveElectrons);
      iEvent.put(saveElectrons, "selectedVetoElectrons");
    }

    // Global muon veto
    //    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);
    hSelectionFlow->Fill(kQCDOrderMuonVeto);
    
    if(metDataInverted.passedEvent()) hTransverseMassAfterVeto->Fill(transverseMass);
    //    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderMuonVeto, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Muon> > saveMuons(new std::vector<pat::Muon>());
      copyPtrToVector(muonVetoData.getSelectedMuonsBeforeIsolation(), *saveMuons);
      iEvent.put(saveMuons, "selectedVetoMuonsBeforeIsolation");
      saveMuons.reset(new std::vector<pat::Muon>());
      copyPtrToVector(muonVetoData.getSelectedMuons(), *saveMuons);
      iEvent.put(saveMuons, "selectedVetoMuons");
    }

    hMETInvertedTauId->Fill(metDataInverted.getSelectedMET()->et());  
    if ( selectedInvertedTau->pt() > 150  ) hMETInvertedTauId150->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 120  ) hMETInvertedTauId120->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMETInvertedTauId120150->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMETInvertedTauId100120->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMETInvertedTauId80100->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMETInvertedTauId7080->Fill(metDataInverted.getSelectedMET()->et());     
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMETInvertedTauId6070->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMETInvertedTauId5060->Fill(metDataInverted.getSelectedMET()->et()); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMETInvertedTauId4050->Fill(metDataInverted.getSelectedMET()->et());
						
        
    hNJetInvertedTauId->Fill(jetDataInverted.getSelectedJets().size());  
    if ( selectedInvertedTau->pt() > 150  ) hNJetInvertedTauId150->Fill(jetDataInverted.getSelectedJets().size());
    if ( selectedInvertedTau->pt() > 120  ) hNJetInvertedTauId120->Fill(jetDataInverted.getSelectedJets().size());
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hNJetInvertedTauId120150->Fill(jetDataInverted.getSelectedJets().size());
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hNJetInvertedTauId100120->Fill(jetDataInverted.getSelectedJets().size());
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hNJetInvertedTauId80100->Fill(jetDataInverted.getSelectedJets().size());
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hNJetInvertedTauId7080->Fill(jetDataInverted.getSelectedJets().size());     
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hNJetInvertedTauId6070->Fill(jetDataInverted.getSelectedJets().size());
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hNJetInvertedTauId5060->Fill(jetDataInverted.getSelectedJets().size()); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hNJetInvertedTauId4050->Fill(jetDataInverted.getSelectedJets().size());

    if(metDataInverted.passedEvent()) {
      hNJetInvertedTauIdMet->Fill(jetDataInverted.getSelectedJets().size());  
      if ( selectedInvertedTau->pt() > 150  ) hNJetInvertedTauIdMet150->Fill(jetDataInverted.getSelectedJets().size());
      if ( selectedInvertedTau->pt() > 120  ) hNJetInvertedTauIdMet120->Fill(jetDataInverted.getSelectedJets().size());
      if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hNJetInvertedTauIdMet120150->Fill(jetDataInverted.getSelectedJets().size());
      if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hNJetInvertedTauIdMet100120->Fill(jetDataInverted.getSelectedJets().size());
      if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hNJetInvertedTauIdMet80100->Fill(jetDataInverted.getSelectedJets().size());
      if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hNJetInvertedTauIdMet7080->Fill(jetDataInverted.getSelectedJets().size());     
      if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hNJetInvertedTauIdMet6070->Fill(jetDataInverted.getSelectedJets().size());
      if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hNJetInvertedTauIdMet5060->Fill(jetDataInverted.getSelectedJets().size()); 
      if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hNJetInvertedTauIdMet4050->Fill(jetDataInverted.getSelectedJets().size());
    }


    // Hadronic jet selection
    //    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup,  tauData.getSelectedTau()); 
    if(!jetDataInverted.passedEvent()) return false;
    increment(fNJetsCounter);
    hSelectionFlow->Fill(kQCDOrderJetSelection);
    //    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderJetSelection, tauData);
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveJets(new std::vector<pat::Jet>());
      copyPtrToVector(jetDataInverted.getSelectedJets(), *saveJets);
      iEvent.put(saveJets, "selectedJets");
    }
   

// plots for inverted isolation

    // inverted MET before b tagging
    hMETInvertedTauIdJets->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 150  ) hMETInvertedTauIdJets150->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 120  ) hMETInvertedTauIdJets120->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMETInvertedTauIdJets120150->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMETInvertedTauIdJets100120->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMETInvertedTauIdJets80100->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMETInvertedTauIdJets7080->Fill(metDataInverted.getSelectedMET()->et());     
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMETInvertedTauIdJets6070->Fill(metDataInverted.getSelectedMET()->et());
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMETInvertedTauIdJets5060->Fill(metDataInverted.getSelectedMET()->et()); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMETInvertedTauIdJets4050->Fill(metDataInverted.getSelectedMET()->et());																		
															      

    if(btagDataInverted.passedEvent()) {
      hMETInvertedTauIdBtag->Fill(metDataInverted.getSelectedMET()->et());
     
      if ( selectedInvertedTau->pt() > 150  ) hMETInvertedTauIdBtag150->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 120  ) hMETInvertedTauIdBtag120->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMETInvertedTauIdBtag120150->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMETInvertedTauIdBtag100120->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMETInvertedTauIdBtag80100->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMETInvertedTauIdBtag7080->Fill(metDataInverted.getSelectedMET()->et());    	
      if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMETInvertedTauIdBtag6070->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMETInvertedTauIdBtag5060->Fill(metDataInverted.getSelectedMET()->et()); 
      if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMETInvertedTauIdBtag4050->Fill(metDataInverted.getSelectedMET()->et());																		
    }


    // Veto on hard b jets  
    if( btagDataInverted.getSelectedJets().size() < 1) {
      increment(fBjetVetoCounter);
      hMETInvertedTauIdBveto->Fill(metDataInverted.getSelectedMET()->et());
     
      if ( selectedInvertedTau->pt() > 150  ) hMETInvertedTauIdBveto150->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 120  ) hMETInvertedTauIdBveto120->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMETInvertedTauIdBveto120150->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMETInvertedTauIdBveto100120->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMETInvertedTauIdBveto80100->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMETInvertedTauIdBveto7080->Fill(metDataInverted.getSelectedMET()->et());     	
      if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMETInvertedTauIdBveto6070->Fill(metDataInverted.getSelectedMET()->et());
      if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMETInvertedTauIdBveto5060->Fill(metDataInverted.getSelectedMET()->et()); 
      if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMETInvertedTauIdBveto4050->Fill(metDataInverted.getSelectedMET()->et());																		
    }
  
 
    if(metDataInverted.passedEvent()) hDeltaPhiAfterJets->Fill(deltaPhi);   
      
    hTransverseMassNoMet->Fill(transverseMass);
    if(btagDataInverted.passedEvent())   {
      increment(fBTaggingBeforeMETCounter);
      hTransverseMassNoMetBtag->Fill(transverseMass);
    } 

    // MET cut
    hMETBeforeMETCut->Fill(metDataInverted.getSelectedMET()->et());
    if(!metDataInverted.passedEvent()) return false;
    increment(fMETCounter);
    hSelectionFlow->Fill(kQCDOrderMET);
    hSelectedTauEtMetCut->Fill(selectedInvertedTau->pt());
    hSelectedTauEtaMetCut->Fill(selectedInvertedTau->eta());
    hSelectedTauPhiMetCut->Fill(selectedInvertedTau->phi());  
 


  // Nbjets for inverted tau before b tagging
    hNBInvertedTauIdJet->Fill(btagDataInverted.getSelectedJets().size()); 
    if ( selectedInvertedTau->pt() > 150  ) hNBInvertedTauIdJet150->Fill(btagDataInverted.getSelectedJets().size()); 
    if ( selectedInvertedTau->pt() > 120  ) hNBInvertedTauIdJet120->Fill(btagDataInverted.getSelectedJets().size()); 
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hNBInvertedTauIdJet120150->Fill(btagDataInverted.getSelectedJets().size()); 
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hNBInvertedTauIdJet100120->Fill(btagDataInverted.getSelectedJets().size()); 
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hNBInvertedTauIdJet80100->Fill(btagDataInverted.getSelectedJets().size()); 
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hNBInvertedTauIdJet7080->Fill(btagDataInverted.getSelectedJets().size()); 
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hNBInvertedTauIdJet6070->Fill(btagDataInverted.getSelectedJets().size()); 
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hNBInvertedTauIdJet5060->Fill(btagDataInverted.getSelectedJets().size()); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hNBInvertedTauIdJet4050->Fill(btagDataInverted.getSelectedJets().size()); 

   // mt for inverted tau before b tagging
    hMTInvertedTauIdJet->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdJet150->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdJet120->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdJet120150->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdJet100120->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdJet80100->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdJet7080->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdJet6070->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdJet5060->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdJet4050->Fill(transverseMass);
 
    hDeltaPhiInvertedNoB->Fill(deltaPhi);  
    if ( selectedInvertedTau->pt() > 150  ) hDeltaPhiInvertedNoB150->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiInvertedNoB120->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hDeltaPhiInvertedNoB120150->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiInvertedNoB100120->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiInvertedNoB80100->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiInvertedNoB7080->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiInvertedNoB6070->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiInvertedNoB5060->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiInvertedNoB4050->Fill(deltaPhi); 

    //   if (deltaPhi < fDeltaPhiCutValue) {
    //    if (deltaPhi < deltaPhiCutValue2Dim) {
    if ( deltaPhi < 120 || jetDataInverted.getDeltaPhiMHTJet1() < 60 ) {
      /*
// moved to deltaPhi
      hMTInvertedTauIdJetDphi->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdJetDphi150->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdJetDphi120->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdJetDphi120150->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdJetDphi100120->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdJetDphi80100->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdJetDphi7080->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdJetDphi6070->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdJetDphi5060->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdJetDphi4050->Fill(transverseMass); 
      */


      hNBInvertedTauIdJetDphi->Fill(btagDataInverted.getSelectedJets().size()); 
      if ( selectedInvertedTau->pt() > 150  ) hNBInvertedTauIdJetDphi150->Fill(btagDataInverted.getSelectedJets().size()); 
      if ( selectedInvertedTau->pt() > 120  ) hNBInvertedTauIdJetDphi120->Fill(btagDataInverted.getSelectedJets().size()); 
      if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hNBInvertedTauIdJetDphi120150->Fill(btagDataInverted.getSelectedJets().size()); 
      if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hNBInvertedTauIdJetDphi100120->Fill(btagDataInverted.getSelectedJets().size()); 
      if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hNBInvertedTauIdJetDphi80100->Fill(btagDataInverted.getSelectedJets().size()); 
      if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hNBInvertedTauIdJetDphi7080->Fill(btagDataInverted.getSelectedJets().size()); 
      if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hNBInvertedTauIdJetDphi6070->Fill(btagDataInverted.getSelectedJets().size()); 
      if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hNBInvertedTauIdJetDphi5060->Fill(btagDataInverted.getSelectedJets().size()); 
      if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hNBInvertedTauIdJetDphi4050->Fill(btagDataInverted.getSelectedJets().size());
    }


  // mt for inverted tau with b veto
    if( btagDataInverted.getSelectedJets().size() < 1) { 
      increment(fBvetoCounter); 
      // moved to phi!!!!!!!!!!!!
      /*
      hMTInvertedTauIdBveto->Fill(transverseMass);
      if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdBveto150->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdBveto120->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdBveto120150->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdBveto100120->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdBveto80100->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdBveto7080->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdBveto6070->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdBveto5060->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdBveto4050->Fill(transverseMass);
      */

      //      if (deltaPhi < fDeltaPhiCutValue) {
      if (deltaPhi < deltaPhiCutValue2Dim) {
	increment(fBvetoDeltaPhiCounter); 
	hMTInvertedTauIdBvetoDphi->Fill(transverseMass);
	if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdBvetoDphi150->Fill(transverseMass); 
	if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdBvetoDphi120->Fill(transverseMass); 
	if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdBvetoDphi120150->Fill(transverseMass); 
	if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdBvetoDphi100120->Fill(transverseMass); 
	if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdBvetoDphi80100->Fill(transverseMass); 
	if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdBvetoDphi7080->Fill(transverseMass); 
	if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdBvetoDphi6070->Fill(transverseMass); 
	if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdBvetoDphi5060->Fill(transverseMass); 
	if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdBvetoDphi4050->Fill(transverseMass);
      }
    }


    // b tagging cut
    //    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderBTagSelection, tauData, btagDataInverted.passedEvent(),btagData.getMaxDiscriminatorValue());
    if(!btagDataInverted.passedEvent()) return false;
    // Apply scale factor as weight to event 
    increment(fBTaggingCounter);
    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagDataInverted); //    Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagDataInverted.getScaleFactor());
    }   
    increment(fBTaggingScaleFactorInvertedCounter);
		

    hSelectionFlow->Fill(kQCDOrderBTag);
   
    hMet_AfterBTagging->Fill(metDataInverted.getSelectedMET()->et());

    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveBJets(new std::vector<pat::Jet>());
      copyPtrToVector(btagDataInverted.getSelectedJets(), *saveBJets);
      iEvent.put(saveBJets, "selectedBJets");
    }

   // mt for inverted tau with b tagging
    
    hMTInvertedTauIdBtag->Fill(transverseMass);
    if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdBtag150->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdBtag120->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdBtag120150->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdBtag100120->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdBtag80100->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdBtag7080->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdBtag6070->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdBtag5060->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdBtag4050->Fill(transverseMass); 

    hDeltaPhiInverted->Fill(deltaPhi);  
    if ( selectedInvertedTau->pt() > 150  ) hDeltaPhiInverted150->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiInverted120->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hDeltaPhiInverted120150->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiInverted100120->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiInverted80100->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiInverted7080->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiInverted6070->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiInverted5060->Fill(deltaPhi); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiInverted4050->Fill(deltaPhi); 






  /// test !!!!!!!!!!!!!

    int ijet = 0;
    double deltaPhiMetJet1 = -999;
    double deltaPhiMetJet2 = -999;
    double deltaPhiMetJet3 = -999;
    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetDataInverted.getSelectedJets().begin(); iJet != jetDataInverted.getSelectedJets().end(); ++iJet) {
      double jetDeltaPhi = DeltaPhi::reconstruct(**iJet, *(metDataInverted.getSelectedMET())) * 57.3;
      ijet++;
      if (ijet == 1) deltaPhiMetJet1 = jetDeltaPhi;
      if (ijet == 2) deltaPhiMetJet2 = jetDeltaPhi;
      if (ijet == 3) deltaPhiMetJet3 = jetDeltaPhi;
    }




    //fCorrelationAnalysis.analyze(iEvent, iSetup, tauData.getSelectedTaus(), btagData.getSelectedJets(), "BCorrelationAnalysis");

    //    FakeMETVeto::Data fakeMETDataInverted = fFakeMETVeto.analyze(iEvent, iSetup, selectedInvertedTau, jetDataInverted.getSelectedJets(), metDataInverted.getSelectedMET());
    hDeltaPhiTauVSJetInverted->Fill(deltaPhi, fakeMETDataInverted.closestDeltaPhi());   
    if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiTauVSJetInverted120->Fill(deltaPhi,fakeMETDataInverted.closestDeltaPhi());  
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiTauVSJetInverted100120->Fill(deltaPhi,fakeMETDataInverted.closestDeltaPhi()); 
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiTauVSJetInverted80100->Fill(deltaPhi,fakeMETDataInverted.closestDeltaPhi()); 
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiTauVSJetInverted7080->Fill(deltaPhi,fakeMETDataInverted.closestDeltaPhi()); 
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiTauVSJetInverted6070->Fill(deltaPhi, fakeMETDataInverted.closestDeltaPhi()); 
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiTauVSJetInverted5060->Fill(deltaPhi,fakeMETDataInverted.closestDeltaPhi()); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiTauVSJetInverted4050->Fill(deltaPhi,fakeMETDataInverted.closestDeltaPhi()); 

    /*
    hDeltaPhiVsDeltaPhiMHTJet1Inverted->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiVsDeltaPhiMHTJet1Inverted->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted100120->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted80100->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted7080->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted6070->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted5060->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted4050->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet1());
    */
    // test !!!!!!!!!!
    hDeltaPhiVsDeltaPhiMHTJet1Inverted->Fill(deltaPhi,deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiVsDeltaPhiMHTJet1Inverted->Fill(deltaPhi,deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted100120->Fill(deltaPhi,deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted80100->Fill(deltaPhi,deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted7080->Fill(deltaPhi,deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted6070->Fill(deltaPhi,deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted5060->Fill(deltaPhi,deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiVsDeltaPhiMHTJet1Inverted4050->Fill(deltaPhi,deltaPhiMetJet1);

    hDeltaPhiMHTJet1Inverted->Fill(deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiMHTJet1Inverted120->Fill(deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiMHTJet1Inverted100120->Fill(deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiMHTJet1Inverted80100->Fill(deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiMHTJet1Inverted7080->Fill(deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiMHTJet1Inverted6070->Fill(deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiMHTJet1Inverted5060->Fill(deltaPhiMetJet1);
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiMHTJet1Inverted4050->Fill(deltaPhiMetJet1);
    /*
    hDeltaPhiVsDeltaPhiMHTJet2Inverted->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
    if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiVsDeltaPhiMHTJet2Inverted->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted100120->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted80100->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted7080->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted6070->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted5060->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted4050->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());

    hDeltaPhiVsDeltaPhiMHTJet3Inverted->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
    if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiVsDeltaPhiMHTJet3Inverted->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted100120->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted80100->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted7080->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted6070->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted5060->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted4050->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());

   

    hDeltaPhiMHTJet1Inverted->Fill(jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiMHTJet1Inverted120->Fill(jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiMHTJet1Inverted100120->Fill(jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiMHTJet1Inverted80100->Fill(jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiMHTJet1Inverted7080->Fill(jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiMHTJet1Inverted6070->Fill(jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiMHTJet1Inverted5060->Fill(jetDataInverted.getDeltaPhiMHTJet1());
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiMHTJet1Inverted4050->Fill(jetDataInverted.getDeltaPhiMHTJet1());
*/


    hDeltaPhiMHTTauVsDeltaPhiMHTJet1Inverted->Fill(jetDataInverted.getDeltaPhiMHTTau(),jetDataInverted.getDeltaPhiMHTJet1());
    hDeltaPhiMHTTauVsDeltaPhiMHTJet2Inverted->Fill(jetDataInverted.getDeltaPhiMHTTau(),jetDataInverted.getDeltaPhiMHTJet2());
    hDeltaPhiMHTTauVsDeltaPhiMHTJet3Inverted->Fill(jetDataInverted.getDeltaPhiMHTTau(),jetDataInverted.getDeltaPhiMHTJet3());




    hDeltaPhi->Fill(deltaPhi);
    if ( deltaPhi > 150 ) {
       hSelectedTauEtaBackToBack->Fill(selectedInvertedTau->eta()); 
       hSelectedTauPhiBackToBack->Fill(selectedInvertedTau->phi());
       hPtTauVsMetBackToBack->Fill(selectedInvertedTau->pt(),metDataInverted.getSelectedMET()->et()); 
       //       fCorrelationAnalysis.analyze(tauData.getSelectedTaus(), btagData.getSelectedJets(), "BCorrelationAnalysisDeltaPhi");                
    }
    /*
    if ( deltaPhi < 150 && deltaPhi > 30 ) {                                                                                                                                                                    
       hSelectedTauEtaNoBackToBack->Fill(selectedInvertedTau->eta()); 
       hSelectedTauPhiNoBackToBack->Fill(selectedInvertedTau->phi()); 
       hPtTauVsMetNoBackToBack->Fill(selectedInvertedTau->pt(),metDataInverted.getSelectedMET()->et());                                                                                                                   
    } 
    */ 
    if ( deltaPhi < 30 ) {                                                                                                                                                                   
       hSelectedTauEtaCollinear->Fill(selectedInvertedTau->eta()); 
       hSelectedTauPhiCollinear->Fill(selectedInvertedTau->phi());                                                                                                                           
    }

     if (deltaPhi < fDeltaPhiCutValue) {
       hMTInvertedTauIdJetDphi->Fill(transverseMass); 
       if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdJetDphi150->Fill(transverseMass); 
       if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdJetDphi120->Fill(transverseMass); 
       if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdJetDphi120150->Fill(transverseMass); 
       if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdJetDphi100120->Fill(transverseMass); 
       if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdJetDphi80100->Fill(transverseMass); 
       if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdJetDphi7080->Fill(transverseMass); 
       if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdJetDphi6070->Fill(transverseMass); 
       if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdJetDphi5060->Fill(transverseMass); 
       if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdJetDphi4050->Fill(transverseMass); 
       
       increment(fDeltaPhiTauMETCounter);
     }
     // test deltaPhi(jet,Met) !!!!!!!!!!!!!!!!!!!!!
     //     if( (deltaPhi < 120 || deltaPhiMetJet1  > 60) && (deltaPhi < 150 || deltaPhiMetJet2  > 30) && (deltaPhi < 150 || deltaPhiMetJet3  > 30) ) {
     if( !(deltaPhi > 100 &&  deltaPhiMetJet1  < 80) ) {
       if( !(deltaPhi > 150 &&  deltaPhiMetJet2  < 30) ) {
	 if( !(deltaPhi > 150 &&  deltaPhiMetJet3  < 30) ) {
	   increment(fDeltaPhiVSDeltaPhiMetJetCutCounter);
	   hMTInvertedTauIdBveto->Fill(transverseMass);
	   if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdBveto150->Fill(transverseMass); 
	   if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdBveto120->Fill(transverseMass); 
	   if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdBveto120150->Fill(transverseMass); 
	   if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdBveto100120->Fill(transverseMass); 
	   if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdBveto80100->Fill(transverseMass); 
	   if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdBveto7080->Fill(transverseMass); 
	   if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdBveto6070->Fill(transverseMass); 
	   if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdBveto5060->Fill(transverseMass); 
	   if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdBveto4050->Fill(transverseMass);
	 }
       }
     }
     
     // cut in  DeltaPhiMHTJet1 
     //     if ( deltaPhi > 120 &&  jetDataInverted.getDeltaPhiMHTJet1() < 60 ) return false;
     if ( deltaPhi > 120 &&  deltaPhiMetJet1  < 60 ) return false;
     increment(fDeltaPhiVSDeltaPhiMHTJet1CutCounter);
     hMTInvertedTauIdMet->Fill(transverseMass); 
     if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdJet150->Fill(transverseMass);
     if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdJet120->Fill(transverseMass); 
     if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdMet120150->Fill(transverseMass); 
     if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdMet100120->Fill(transverseMass); 
     if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdMet80100->Fill(transverseMass); 
     if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdMet7080->Fill(transverseMass); 
     if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdMet6070->Fill(transverseMass); 
     if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdMet5060->Fill(transverseMass); 
     if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdMet4050->Fill(transverseMass);     
     

     //test !!!!!!!!!!!!!!!     
     hDeltaPhiVsDeltaPhiMHTJet2Inverted->Fill(deltaPhi,deltaPhiMetJet2);
     if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiVsDeltaPhiMHTJet2Inverted->Fill(deltaPhi,deltaPhiMetJet2);
     if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted100120->Fill(deltaPhi,deltaPhiMetJet2);
     if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted80100->Fill(deltaPhi,deltaPhiMetJet2);
     if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted7080->Fill(deltaPhi,deltaPhiMetJet2);
     if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted6070->Fill(deltaPhi,deltaPhiMetJet2);
     if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted5060->Fill(deltaPhi,deltaPhiMetJet2);
     if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted4050->Fill(deltaPhi,deltaPhiMetJet2);
     
 
     
     /*     
     hDeltaPhiVsDeltaPhiMHTJet2Inverted->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
     if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiVsDeltaPhiMHTJet2Inverted->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
     if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted100120->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
     if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted80100->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
     if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted7080->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
     if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted6070->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
     if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted5060->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
     if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiVsDeltaPhiMHTJet2Inverted4050->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet2());
     
     hDeltaPhiVsDeltaPhiMHTJet3Inverted->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
     if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiVsDeltaPhiMHTJet3Inverted->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
     if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted100120->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
     if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted80100->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
     if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted7080->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
     if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted6070->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
     if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted5060->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
     if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted4050->Fill(deltaPhi,jetDataInverted.getDeltaPhiMHTJet3());
     */     



     
     // add cut in  DeltaPhiMHTJet2     
     //     if( deltaPhi > 150 && jetDataInverted.getDeltaPhiMHTJet2() < 30 ) return false; 
    if( deltaPhi > 120 && deltaPhiMetJet2  < 60 ) return false;   
     increment(fDeltaPhiVSDeltaPhiMHTJet2CutCounter);

     hDeltaPhiVsDeltaPhiMHTJet3Inverted->Fill(deltaPhi,deltaPhiMetJet3);
     if ( selectedInvertedTau->pt() > 120  ) hDeltaPhiVsDeltaPhiMHTJet3Inverted->Fill(deltaPhi,deltaPhiMetJet3);
     if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted100120->Fill(deltaPhi,deltaPhiMetJet3);
     if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted80100->Fill(deltaPhi,deltaPhiMetJet3);
     if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted7080->Fill(deltaPhi,deltaPhiMetJet3);
     if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted6070->Fill(deltaPhi,deltaPhiMetJet3);
     if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted5060->Fill(deltaPhi,deltaPhiMetJet3);
     if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hDeltaPhiVsDeltaPhiMHTJet3Inverted4050->Fill(deltaPhi,deltaPhiMetJet3);     
     
     //    if (deltaPhi > fDeltaPhiCutValue) return false;
     //    if (deltaPhi > deltaPhiCutValue2Dim) return false;
     
     
     hDeltaPhiTauVSJetInvertedAfterCut->Fill(deltaPhi, fakeMETDataInverted.closestDeltaPhi());   



    increment(fDeltaPhiTauMETCounter);
    hSelectionFlow->Fill(kQCDOrderDeltaPhiTauMET);   
    hTransverseMass->Fill(transverseMass); 

    hMTInvertedTauIdJetPhi->Fill(transverseMass); 
    increment(fdeltaPhiTauMET160Counter);
    if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdJetPhi150->Fill(transverseMass);
    if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdJetPhi120->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdJetPhi120150->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdJetPhi100120->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdJetPhi80100->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdJetPhi7080->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdJetPhi6070->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdJetPhi5060->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdJetPhi4050->Fill(transverseMass); 
 

  //    if( deltaPhi > 150 && jetDataInverted.getDeltaPhiMHTJet3() < 30 ) return false; 
     if( deltaPhi > 120 && deltaPhiMetJet3  < 60 ) return false;  
    increment(fDeltaPhiVSDeltaPhiMHTJet3CutCounter);
    // Moved !!!
    hMTInvertedTauIdTopMass->Fill(transverseMass);
    increment(fdeltaPhiTauMET130Counter); 
    if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdTopMass150->Fill(transverseMass);
    if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdTopMass120->Fill(transverseMass);  
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdTopMass120150->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdTopMass100120->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdTopMass80100->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdTopMass7080->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdTopMass6070->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdTopMass5060->Fill(transverseMass); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdTopMass4050->Fill(transverseMass); 
   
     




    FullHiggsMassCalculator::Data FullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagDataInverted, metDataInverted);
    //    fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData, metDataInverted);
    double HiggsMass = FullHiggsMassData.getHiggsMass();
    if (HiggsMass > 100 && HiggsMass < 200 ) increment(fHiggsMassCutCounter);

    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetDataInverted.getSelectedJets(), btagDataInverted.getSelectedJets());
    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetDataInverted.getSelectedJets(), btagDataInverted.getSelectedJets(), selectedInvertedTau, metDataInverted.getSelectedMET());

    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetDataInverted.getSelectedJets(), btagDataInverted.getSelectedJets());
    // Calculate alphaT

    //    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(selectedInvertedTau), jetDataInverted.getSelectedJets()); 
    //    FakeMETVeto::Data fakeMETDataInverted = fFakeMETVeto.analyze(iEvent, iSetup, selectedInvertedTau, jetDataInverted.getSelectedJets(), metDataInverted.getSelectedMET());
    //    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(iEvent, iSetup, *(tauData.getSelectedTau()), jetData.getSelectedJets()); 
      //    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());

   
    hClosestDeltaPhiInverted->Fill(fakeMETDataInverted.closestDeltaPhi());
    if ( selectedInvertedTau->pt() > 120 ) hClosestDeltaPhiInverted120->Fill(fakeMETDataInverted.closestDeltaPhi()); 
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hClosestDeltaPhiInverted100120->Fill(fakeMETDataInverted.closestDeltaPhi()); 
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hClosestDeltaPhiInverted80100->Fill(fakeMETDataInverted.closestDeltaPhi()); 
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hClosestDeltaPhiInverted7080->Fill(fakeMETDataInverted.closestDeltaPhi()); 
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hClosestDeltaPhiInverted6070->Fill(fakeMETDataInverted.closestDeltaPhi()); 
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hClosestDeltaPhiInverted5060->Fill(fakeMETDataInverted.closestDeltaPhi()); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hClosestDeltaPhiInverted4050->Fill(fakeMETDataInverted.closestDeltaPhi());

    double topMass = TopChiSelectionData.getTopMass();    
    hTopMass->Fill(topMass);
    // top mass with binning    
    if ( selectedInvertedTau->pt() > 150  ) hTopMass150->Fill(topMass); 
    if ( selectedInvertedTau->pt() > 120  ) hTopMass120->Fill(topMass); 
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hTopMass120150->Fill(topMass); 
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hTopMass100120->Fill(topMass); 
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hTopMass80100->Fill(topMass); 
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hTopMass7080->Fill(topMass); 
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hTopMass6070->Fill(topMass); 
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hTopMass5060->Fill(topMass); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hTopMass4050->Fill(topMass); 

  
    // Inv mass mass with binning  
    hHiggsMass->Fill(HiggsMass);   
    if ( selectedInvertedTau->pt() > 150  ) hHiggsMass150->Fill(HiggsMass); 
    if ( selectedInvertedTau->pt() > 120  ) hHiggsMass120->Fill(HiggsMass); 
    if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hHiggsMass120150->Fill(HiggsMass); 
    if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hHiggsMass100120->Fill(HiggsMass); 
    if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hHiggsMass80100->Fill(HiggsMass); 
    if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hHiggsMass7080->Fill(HiggsMass); 
    if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hHiggsMass6070->Fill(HiggsMass); 
    if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hHiggsMass5060->Fill(HiggsMass); 
    if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hHiggsMass4050->Fill(HiggsMass); 


    if (deltaPhi <  130 ) {
      
      hHiggsMassPhi->Fill(HiggsMass);   
      if ( selectedInvertedTau->pt() > 150  ) hHiggsMassPhi150->Fill(HiggsMass);
      if ( selectedInvertedTau->pt() > 120  ) hHiggsMassPhi120->Fill(HiggsMass);  
      if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hHiggsMassPhi120150->Fill(HiggsMass); 
      if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hHiggsMassPhi100120->Fill(HiggsMass); 
      if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hHiggsMassPhi80100->Fill(HiggsMass); 
      if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hHiggsMassPhi7080->Fill(HiggsMass); 
      if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hHiggsMassPhi6070->Fill(HiggsMass); 
      if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hHiggsMassPhi5060->Fill(HiggsMass); 
      if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hHiggsMassPhi4050->Fill(HiggsMass); 

      /*
// moved to deltaPhi 
      hMTInvertedTauIdMet->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdJet150->Fill(transverseMass);
      if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdJet120->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdMet120150->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdMet100120->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdMet80100->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdMet7080->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdMet6070->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdMet5060->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdMet4050->Fill(transverseMass);
      */
    }

  

 
    if (TopChiSelectionData.passedEvent() ) {
      /*
      hMTInvertedTauIdTopMass->Fill(transverseMass);
      increment(fdeltaPhiTauMET130Counter); 
      if ( selectedInvertedTau->pt() > 150  ) hMTInvertedTauIdTopMass150->Fill(transverseMass);
      if ( selectedInvertedTau->pt() > 120  ) hMTInvertedTauIdTopMass120->Fill(transverseMass);  
      if ( selectedInvertedTau->pt() > 120 && selectedInvertedTau->pt() < 150 ) hMTInvertedTauIdTopMass120150->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 100 && selectedInvertedTau->pt() < 120 ) hMTInvertedTauIdTopMass100120->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 80 && selectedInvertedTau->pt() < 100 ) hMTInvertedTauIdTopMass80100->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 70 && selectedInvertedTau->pt() < 80 ) hMTInvertedTauIdTopMass7080->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 60 && selectedInvertedTau->pt() < 70 ) hMTInvertedTauIdTopMass6070->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 50 && selectedInvertedTau->pt() < 60 ) hMTInvertedTauIdTopMass5060->Fill(transverseMass); 
      if ( selectedInvertedTau->pt() > 40 && selectedInvertedTau->pt() < 50 ) hMTInvertedTauIdTopMass4050->Fill(transverseMass); 
      */
    }
    

    hDeltaPhi->Fill(deltaPhi);
    if ( deltaPhi > 10) increment(fdeltaPhiTauMET10Counter); 


     

    // plot deltaPhi(jet,met)
    double deltaPhiJetMet = -999;
    double deltaPhiMin = 999;
    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetDataInverted.getSelectedJets().begin(); iJet != jetDataInverted.getSelectedJets().end(); ++iJet) {
      deltaPhiJetMet = DeltaPhi::reconstruct(**iJet, *(metDataInverted.getSelectedMET()));
      if (deltaPhiMin < deltaPhiJetMet ) deltaPhiMin = deltaPhiJetMet;
      hDeltaPhiJetMet->Fill(deltaPhiJetMet*57.3);
    }

    hSelectedTauEtAfterCuts->Fill(selectedInvertedTau->pt());
    hSelectedTauEtaAfterCuts->Fill(selectedInvertedTau->eta());
    hMetAfterCuts->Fill(metDataInverted.getSelectedMET()->et());


   
    if (TopChiSelectionData.passedEvent() ) {
         increment(fTopChiSelectionCounter);     
	 hTransverseMassTopChiSelection->Fill(transverseMass);     
    } 

    if (BjetSelectionData.passedEvent() ) {
        
      TopWithBSelection::Data TopWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetDataInverted.getSelectedJets(), BjetSelectionData.getBjetTopSide());

      if (TopWithBSelectionData.passedEvent() ) {
	increment(fTopWithBSelectionCounter);
	//      hSelectionFlow->Fill(kSignalOrderTopSelection);      
	hTransverseMassTopBjetSelection->Fill(transverseMass);     
      }    
    }


   // top mass with possible event cuts
    if (TopSelectionData.passedEvent() ) {
      increment(fTopSelectionCounter);      
      hTransverseMassWithTopCut->Fill(transverseMass);
      if(transverseMass > 80 ) increment(ftransverseMassCut100TopCounter);   
    } 


    if (fakeMETDataInverted.passedEvent() ) {
      increment(fFakeMETVetoCounter);
	hTransverseMassFakeMET->Fill(transverseMass);  
    }
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderFakeMETVeto, tauData);

    if(transverseMass > 60 ) increment(ftransverseMassCut80NoRtauCounter);
    if(transverseMass > 80 ) increment(ftransverseMassCut100NoRtauCounter);

 
    if(transverseMass < 60 ) return false;
    increment(ftransverseMassCut80Counter);

    if(transverseMass < 80 ) return false;
    increment(ftransverseMassCut100Counter);


    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderFakeMETVeto, tauData);   
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
