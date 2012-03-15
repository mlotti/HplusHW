#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisInvertedTau.h"
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
    fMETCounter(eventCounter.addCounter("MET")),
    fBTaggingCounter(eventCounter.addCounter("btagging")),
    fdeltaPhiTauMET10Counter(eventCounter.addCounter("deltaPhiTauMET lower limit")),
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
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, eventWeight),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, eventWeight),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
    fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight, "MET"),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, eventWeight),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, eventWeight),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, eventWeight),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, eventWeight),
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, eventWeight),
    fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, eventWeight),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, eventWeight),
    //    ftransverseMassCut(iConfig.getUntrackedParameter<edm::ParameterSet>("transverseMassCut")),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, eventWeight),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, eventWeight),
    fCorrelationAnalysis(eventCounter, eventWeight),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, eventWeight),
    fTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiencyScaleFactor"), fEventWeight),
    fVertexWeight(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeight")),
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
    hVerticesBeforeWeight = makeTH<TH1F>(*fs, "verticesBeforeWeight", "Number of vertices without weighting", 30, 0, 30);
    hVerticesAfterWeight = makeTH<TH1F>(*fs, "verticesAfterWeight", "Number of vertices with weighting", 30, 0, 30);
    hVerticesTriggeredBeforeWeight = makeTH<TH1F>(*fs, "verticesTriggeredBeforeWeight", "Number of vertices without weighting", 30, 0, 30);
    hVerticesTriggeredAfterWeight = makeTH<TH1F>(*fs, "verticesTriggeredAfterWeight", "Number of vertices with weighting", 30, 0, 30);
    //    hmetAfterTrigger = makeTH<TH1F>(*fs, "metAfterTrigger", "metAfterTrigger", 50, 0., 200.);
    hTransverseMass = makeTH<TH1F>(*fs, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassWithTopCut = makeTH<TH1F>(*fs, "transverseMassWithTopCut", "transverseMassWithTopCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassAfterVeto = makeTH<TH1F>(*fs, "transverseMassAfterVeto", "transverseMassAfterVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassBeforeVeto = makeTH<TH1F>(*fs, "transverseMassBeforeVeto", "transverseMassBeforeVeto;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassNoMet = makeTH<TH1F>(*fs, "transverseMassNoMet", "transverseMassNoMet;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassNoMetBtag = makeTH<TH1F>(*fs, "transverseMassNoMetBtag", "transverseMassNoMetBtag;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassBeforeFakeMet = makeTH<TH1F>(*fs, "transverseMassBeforeFakeMet", "transverseMassBeforeFakeMet;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassDeltaPhiUpperCut = makeTH<TH1F>(*fs, "transverseMassDeltaPhiUpperCut", "transverseMassDeltaPhiUpperCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);


    hTransverseMassDeltaPhi160 =  makeTH<TH1F>(*fs, "transverseMassDeltaPhi160", "transverseMassDeltaPhi160;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.); 
    hTransverseMassDeltaPhi130 =  makeTH<TH1F>(*fs, "transverseMassDeltaPhi130", "transverseMassDeltaPhi130;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassTopDeltaPhiFakeMET =  makeTH<TH1F>(*fs, "transverseMassTopDeltaPhiFakeMET", "transverseMassTopDeltaPhiFakeMET;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassTopChiSelection = makeTH<TH1F>(*fs, "transverseMassTopChiSelection", "transverseMassTopChiSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hTransverseMassTopBjetSelection = makeTH<TH1F>(*fs, "transverseMassTopBjetSelection", "transverseMassTopBjetSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 400, 0., 400.);
    hDeltaPhi = makeTH<TH1F>(*fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 360, 0., 180.);
    hDeltaPhiJetMet = makeTH<TH1F>(*fs, "deltaPhiJetMet", "deltaPhiJetMet", 400, 0., 3.2);  
    hAlphaT = makeTH<TH1F>(*fs, "alphaT", "alphaT", 100, 0.0, 5.0);
    hAlphaTInvMass = makeTH<TH1F>(*fs, "alphaT-InvMass", "alphaT-InvMass", 100, 0.0, 1000.0);    
    hAlphaTVsRtau = makeTH<TH2F>(*fs, "alphaT(y)-Vs-Rtau(x)", "alphaT-Vs-Rtau",  120, 0.0, 1.2, 500, 0.0, 5.0);
    hMet_AfterBTagging = makeTH<TH1F>(*fs, "MET_AfterBTagging", "MET_AfterBTagging;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    
    hMETBeforeMETCut = makeTH<TH1F>(*fs, "MET_BeforeMETCut", "MET_BeforeMETCut;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hSelectedTauEt = makeTH<TH1F>(*fs, "SelectedTau_pT_AfterTauID", "SelectedTau_pT_AfterTauID;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    //    hSelectedTauEtMetCut = makeTH<TH1F>(*fs, "SelectedTau_pT_AfterTauID_MetCut", "SelectedTau_pT_AfterTauID_MetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEta = makeTH<TH1F>(*fs, "SelectedTau_eta_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.1", 300, -3.0, 3.0);
    hSelectedTauEtAfterCuts = makeTH<TH1F>(*fs, "SelectedTau_pT_AfterCuts", "SelectedTau_pT_AfterCuts;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 40, 0.0, 400.0);
    hSelectedTauEtaAfterCuts = makeTH<TH1F>(*fs, "SelectedTau_eta_AfterCuts", "SelectedTau_eta_AfterCuts;#tau #eta;N_{events} / 0.1", 30, -3.0, 3.0);
    hSelectedTauPhi = makeTH<TH1F>(*fs, "SelectedTau_phi_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtau = makeTH<TH1F>(*fs, "SelectedTau_Rtau_AfterTauID", "SelectedTau_Rtau_AfterTauID;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);
    hSelectedTauRtauAfterCuts = makeTH<TH1F>(*fs, "SelectedTau_Rtau_AfterCuts", "SelectedTau_Rtau_AfterCuts;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);
    hSelectedTauLeadingTrackPt = makeTH<TH1F>(*fs, "SelectedTau_TauLeadingTrackPt", "SelectedTau_TauLeadingTrackPt;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauLeadingTrackPtMetCut = makeTH<TH1F>(*fs, "SelectedTau_TauLeadingTrackPt_MetCut", "SelectedTau_TauLeadingTrackPt_MetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);

    hMetAfterCuts = makeTH<TH1F>(*fs, "Met_AfterCuts", "Met_AfterCuts", 500, 0.0, 500.0);
    hMETBeforeTauId = makeTH<TH1F>(*fs, "Met_BeforeTauId", "Met_BeforeTauId", 500, 0.0, 500.0);
    hMETBaselineTauId = makeTH<TH1F>(*fs,"MET_BaseLineTauId", "MET_BaseLineTauId;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauId = makeTH<TH1F>(*fs, "MET_InvertedTauId", "MET_InvertedTauId;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETBaselineTauIdJets = makeTH<TH1F>(*fs, "MET_BaseLineTauIdJets", "MET_BaseLineTauIdJets;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETBaselineTauIdJets150 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdJets150", "MET_BaseLineTauIdJets150;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETBaselineTauIdJets120150 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdJets120150", "MET_BaseLineTauIdJets120150;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets100120 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdJets100120", "MET_BaseLineTauIdJets100120;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets80100 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdJets80100", "MET_BaseLineTauIdJets80100;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets7080 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdJets7080", "MET_BaseLineTauIdJets7080;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets6070 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdJets6070", "MET_BaseLineTauIdJets6070;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets5060 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdJets5060", "MET_BaseLineTauIdJets5060;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdJets4050 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdJets4050", "MET_BaseLineTauIdJets4050;PF MET", 400, 0.0, 400.0);

    hMETBaselineTauIdBtag = makeTH<TH1F>(*fs, "MET_BaseLineTauIdBtag", "MET_BaseLineTauIdBtag;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag150 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdBtag150", "MET_BaseLineTauIdBtag150;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag120150 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdBtag120150", "MET_BaseLineTauIdBtag120150;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag100120 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdBtag100120", "MET_BaseLineTauIdBtag100120;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag80100 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdBtag80100", "MET_BaseLineTauIdBtag80100;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag7080 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdBtag7080", "MET_BaseLineTauIdBtag7080;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag6070 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdBtag6070", "MET_BaseLineTauIdBtag6070;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag5060 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdBtag5060", "MET_BaseLineTauIdBtag5060;PF MET", 400, 0.0, 400.0);
    hMETBaselineTauIdBtag4050 = makeTH<TH1F>(*fs, "MET_BaseLineTauIdBtag4050", "MET_BaseLineTauIdBtag4050;PF MET", 400, 0.0, 400.0);

    hMTBaselineTauIdJet150 = makeTH<TH1F>(*fs, "MTBaselineTauIdJet150", "MTBaselineTauIdJet150", 400, 0., 400.);
    hMTBaselineTauIdJet120150 = makeTH<TH1F>(*fs, "MTBaselineTauIdJet120150", "MTBaselineTauIdJet120150", 400, 0., 400.);
    hMTBaselineTauIdJet100120 = makeTH<TH1F>(*fs, "MTBaselineTauIdJet100120", "MTBaselineTauIdJet100120", 400, 0., 400.);
    hMTBaselineTauIdJet80100 = makeTH<TH1F>(*fs, "MTBaselineTauIdJet80100", "MTBaselineTauIdJet80100", 400, 0., 400.);
    hMTBaselineTauIdJet7080 = makeTH<TH1F>(*fs, "MTBaselineTauIdJet7080", "MTBaselineTauIdJet7080", 400, 0., 400.);
    hMTBaselineTauIdJet6070 = makeTH<TH1F>(*fs, "MTBaselineTauIdJet6070", "MTBaselineTauIdJet6070", 400, 0., 400.);
    hMTBaselineTauIdJet5060 = makeTH<TH1F>(*fs, "MTBaselineTauIdJet5060", "MTBaselineTauIdJet5060", 400, 0., 400.);
    hMTBaselineTauIdJet4050 = makeTH<TH1F>(*fs, "MTBaselineTauIdJet4050", "MTBaselineTauIdJet4050", 400, 0., 400.);

    hMTInvertedTauIdJet = makeTH<TH1F>(*fs, "MTInvertedTauIdJet", "MTInvertedTauIdJet", 400, 0., 400.);
    hMTInvertedTauIdJet150 = makeTH<TH1F>(*fs, "MTInvertedTauIdJet150", "MTInvertedTauIdJet150", 400, 0., 400.);
    hMTInvertedTauIdJet120150 = makeTH<TH1F>(*fs, "MTInvertedTauIdJet120150", "MTInvertedTauIdJet120150", 400, 0., 400.);
    hMTInvertedTauIdJet100120 = makeTH<TH1F>(*fs, "MTInvertedTauIdJet100120", "MTInvertedTauIdJet100120", 400, 0., 400.);
    hMTInvertedTauIdJet80100 = makeTH<TH1F>(*fs, "MTInvertedTauIdJet80100", "MTInvertedTauIdJet80100", 400, 0., 400.);
    hMTInvertedTauIdJet7080 = makeTH<TH1F>(*fs, "MTInvertedTauIdJet7080", "MTInvertedTauIdJet7080", 400, 0., 400.);
    hMTInvertedTauIdJet6070 = makeTH<TH1F>(*fs, "MTInvertedTauIdJet6070", "MTInvertedTauIdJet6070", 400, 0., 400.);
    hMTInvertedTauIdJet5060 = makeTH<TH1F>(*fs, "MTInvertedTauIdJet5060", "MTInvertedTauIdJet5060", 400, 0., 400.);
    hMTInvertedTauIdJet4050 = makeTH<TH1F>(*fs, "MTInvertedTauIdJet4050", "MTInvertedTauIdJet4050", 400, 0., 400.);

    hMTInvertedTauIdMet = makeTH<TH1F>(*fs, "MTInvertedTauIdMet", "MTInvertedTauIdMet", 400, 0., 400.);
    hMTInvertedTauIdMet150 = makeTH<TH1F>(*fs, "MTInvertedTauIdMet150", "MTInvertedTauIdMet150", 400, 0., 400.);
    hMTInvertedTauIdMet120150 = makeTH<TH1F>(*fs, "MTInvertedTauIdMet120150", "MTInvertedTauIdMet120150", 400, 0., 400.);
    hMTInvertedTauIdMet100120 = makeTH<TH1F>(*fs, "MTInvertedTauIdMet100120", "MTInvertedTauIdMet100120", 400, 0., 400.);
    hMTInvertedTauIdMet80100 = makeTH<TH1F>(*fs, "MTInvertedTauIdMet80100", "MTInvertedTauIdMet80100", 400, 0., 400.);
    hMTInvertedTauIdMet7080 = makeTH<TH1F>(*fs, "MTInvertedTauIdMet7080", "MTInvertedTauIdMet7080", 400, 0., 400.);
    hMTInvertedTauIdMet6070 = makeTH<TH1F>(*fs, "MTInvertedTauIdMet6070", "MTInvertedTauIdMet6070", 400, 0., 400.);
    hMTInvertedTauIdMet5060 = makeTH<TH1F>(*fs, "MTInvertedTauIdMet5060", "MTInvertedTauIdMet5060", 400, 0., 400.);
    hMTInvertedTauIdMet4050 = makeTH<TH1F>(*fs, "MTInvertedTauIdMet4050", "MTInvertedTauIdMet4050", 400, 0., 400.);

    hMTInvertedTauIdJetPhi = makeTH<TH1F>(*fs, "MTInvertedTauIdJetPhi", "MTInvertedTauIdJetPhi", 400, 0., 400.);
    hMTInvertedTauIdJetPhi150 = makeTH<TH1F>(*fs, "MTInvertedTauIdJetPhi150", "MTInvertedTauIdJetPhi150", 400, 0., 400.);
    hMTInvertedTauIdJetPhi120150 = makeTH<TH1F>(*fs, "MTInvertedTauIdJetPhi120150", "MTInvertedTauIdJetPhi120150", 400, 0., 400.);
    hMTInvertedTauIdJetPhi100120 = makeTH<TH1F>(*fs, "MTInvertedTauIdJetPhi100120", "MTInvertedTauIdJetPhi100120", 400, 0., 400.);
    hMTInvertedTauIdJetPhi80100 = makeTH<TH1F>(*fs, "MTInvertedTauIdJetPhi80100", "MTInvertedTauIdJetPhi80100", 400, 0., 400.);
    hMTInvertedTauIdJetPhi7080 = makeTH<TH1F>(*fs, "MTInvertedTauIdJetPhi7080", "MTInvertedTauIdJetPhi7080", 400, 0., 400.);
    hMTInvertedTauIdJetPhi6070 = makeTH<TH1F>(*fs, "MTInvertedTauIdJetPhi6070", "MTInvertedTauIdJetPhi6070", 400, 0., 400.);
    hMTInvertedTauIdJetPhi5060 = makeTH<TH1F>(*fs, "MTInvertedTauIdJetPhi5060", "MTInvertedTauIdJetPhi5060", 400, 0., 400.);
    hMTInvertedTauIdJetPhi4050 = makeTH<TH1F>(*fs, "MTInvertedTauIdJetPhi4050", "MTInvertedTauIdJetPhi4050", 400, 0., 400.);

    hTopMass = makeTH<TH1F>(*fs, "TopMass", "TopMass", 400, 0., 400.);
    hTopMass150 = makeTH<TH1F>(*fs, "TopMass150", "TopMass150", 400, 0., 400.);
    hTopMass120150 = makeTH<TH1F>(*fs, "TopMass120150", "TopMass120150", 400, 0., 400.);
    hTopMass100120 = makeTH<TH1F>(*fs, "TopMass100120", "TopMass100120", 400, 0., 400.);
    hTopMass80100 = makeTH<TH1F>(*fs, "TopMass80100", "TopMass80100", 400, 0., 400.);
    hTopMass7080 = makeTH<TH1F>(*fs, "TopMass7080", "TopMass7080", 400, 0., 400.);
    hTopMass6070 = makeTH<TH1F>(*fs, "TopMass6070", "TopMass6070", 400, 0., 400.);
    hTopMass5060 = makeTH<TH1F>(*fs, "TopMass5060", "TopMass5060", 400, 0., 400.);
    hTopMass4050 = makeTH<TH1F>(*fs, "TopMass4050", "TopMass4050", 400, 0., 400.);

    hMTInvertedTauIdTopMass = makeTH<TH1F>(*fs, "MTInvertedTauIdTopMass", "MTInvertedTauIdTopMass", 400, 0., 400.);
    hMTInvertedTauIdTopMass150 = makeTH<TH1F>(*fs, "MTInvertedTauIdTopMass150", "MTInvertedTauIdTopMass150", 400, 0., 400.);
    hMTInvertedTauIdTopMass120150 = makeTH<TH1F>(*fs, "MTInvertedTauIdTopMass120150", "MTInvertedTauIdTopMass120150", 400, 0., 400.);
    hMTInvertedTauIdTopMass100120 = makeTH<TH1F>(*fs, "MTInvertedTauIdTopMass100120", "MTInvertedTauIdTopMass100120", 400, 0., 400.);
    hMTInvertedTauIdTopMass80100 = makeTH<TH1F>(*fs, "MTInvertedTauIdTopMass80100", "MTInvertedTauIdTopMass80100", 400, 0., 400.);
    hMTInvertedTauIdTopMass7080 = makeTH<TH1F>(*fs, "MTInvertedTauIdTopMass7080", "MTInvertedTauIdTopMass7080", 400, 0., 400.);
    hMTInvertedTauIdTopMass6070 = makeTH<TH1F>(*fs, "MTInvertedTauIdTopMass6070", "MTInvertedTauIdTopMass6070", 400, 0., 400.);
    hMTInvertedTauIdTopMass5060 = makeTH<TH1F>(*fs, "MTInvertedTauIdTopMass5060", "MTInvertedTauIdTopMass5060", 400, 0., 400.);
    hMTInvertedTauIdTopMass4050 = makeTH<TH1F>(*fs, "MTInvertedTauIdTopMass4050", "MTInvertedTauIdTopMass4050", 400, 0., 400.);

    hDeltaPhi = makeTH<TH1F>(*fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events", 360, 0.0, 360.0);
    hMTBaselineTauIdJet = makeTH<TH1F>(*fs, "MT_BaseLineTauIdJets", "MT_BaseLineTauIdJets;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdJets = makeTH<TH1F>(*fs, "MET_InvertedTauIdJets", "MET_InvertedTauIdJets;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdJets150 = makeTH<TH1F>(*fs, "MET_InvertedTauIdJets150", "MET_InvertedTauIdJets150;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdJets120150 = makeTH<TH1F>(*fs, "MET_InvertedTauIdJets120150", "MET_InvertedTauIdJets120150", 400, 0.0, 400.0);
    hMETInvertedTauIdJets100120 = makeTH<TH1F>(*fs, "MET_InvertedTauIdJets100120", "MET_InvertedTauIdJets100120", 400, 0.0, 400.0); 
    hMETInvertedTauIdJets80100 = makeTH<TH1F>(*fs, "MET_InvertedTauIdJets80100", "MET_InvertedTauIdJets80100", 400, 0.0, 400.0); 
    hMETInvertedTauIdJets7080 = makeTH<TH1F>(*fs, "MET_InvertedTauIdJets7080", "MET_InvertedTauIdJets7080", 400, 0.0, 400.0); 
    hMETInvertedTauIdJets6070 = makeTH<TH1F>(*fs, "MET_InvertedTauIdJets6070", "MET_InvertedTauIdJets6070", 400, 0.0, 400.0); 
    hMETInvertedTauIdJets5060 = makeTH<TH1F>(*fs, "MET_InvertedTauIdJets5060", "MET_InvertedTauIdJets5060", 400, 0.0, 400.0); 
    hMETInvertedTauIdJets4050 = makeTH<TH1F>(*fs, "MET_InvertedTauIdJets4050", "MET_InvertedTauIdJets4050", 400, 0.0, 400.0); 

   
    hMETInvertedTauIdBtag = makeTH<TH1F>(*fs, "MET_InvertedTauIdBtag", "MET_InvertedTauIdBtag;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMTInvertedTauIdBtag = makeTH<TH1F>(*fs, "MT_InvertedTauIdBtag", "MT_InvertedTauIdBtag;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdBtag150 = makeTH<TH1F>(*fs, "MET_InvertedTauIdBtag150", "MET_InvertedTauIdBtag150;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdBtag120150 = makeTH<TH1F>(*fs, "MET_InvertedTauIdBtag120150", "MET_InvertedTauIdBtag120150", 400, 0.0, 400.0);
    hMETInvertedTauIdBtag100120 = makeTH<TH1F>(*fs, "MET_InvertedTauIdBtag100120", "MET_InvertedTauIdBtag100120", 400, 0.0, 400.0); 
    hMETInvertedTauIdBtag80100 = makeTH<TH1F>(*fs, "MET_InvertedTauIdBtag80100", "MET_InvertedTauIdBtag80100", 400, 0.0, 400.0); 
    hMETInvertedTauIdBtag7080 = makeTH<TH1F>(*fs, "MET_InvertedTauIdBtag7080", "MET_InvertedTauIdBtag7080", 400, 0.0, 400.0); 
    hMETInvertedTauIdBtag6070 = makeTH<TH1F>(*fs, "MET_InvertedTauIdBtag6070", "MET_InvertedTauIdBtag6070", 400, 0.0, 400.0); 
    hMETInvertedTauIdBtag5060 = makeTH<TH1F>(*fs, "MET_InvertedTauIdBtag5060", "MET_InvertedTauIdBtag5060", 400, 0.0, 400.0); 
    hMETInvertedTauIdBtag4050 = makeTH<TH1F>(*fs, "MET_InvertedTauIdBtag4050", "MET_InvertedTauIdBtag4050", 400, 0.0, 400.0); 

    hMTInvertedTauIdJets = makeTH<TH1F>(*fs, "MT_InvertedTauIdJets", "MT_InvertedTauIdJets;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdLoose = makeTH<TH1F>(*fs, "MET_InvertedTauIdLoose", "MET_InvertedTauIdLoose;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdLoose150 = makeTH<TH1F>(*fs, "MET_InvertedTauIdLoose150", "MET_InvertedTauIdLoose150;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdLoose4070 = makeTH<TH1F>(*fs, "MET_InvertedTauIdJLoose4070", "MET_InvertedTauIdLoose4070;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdLoose70150 = makeTH<TH1F>(*fs, "MET_InvertedTauIdLoose70150", "MET_InvertedTauIdLoose70150;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0); 
    hMTInvertedTauIdLoose = makeTH<TH1F>(*fs, "MT_InvertedTauIdLoose", "MT_InvertedTauIdLoose;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    //    hMETBaselineTauIdBtag = makeTH<TH1F>(*fs, "MET_BaseLineTauIdBtag", "MET_BaseLineTauIdBtag;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMTBaselineTauIdBtag = makeTH<TH1F>(*fs, "MT_BaseLineTauIdBtag", "MT_BaseLineTauIdBtag;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdBtag = makeTH<TH1F>(*fs, "MET_InvertedTauIdBtag", "MET_InvertedTauIdBtag;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMTInvertedTauIdBtag = makeTH<TH1F>(*fs, "MT_InvertedTauIdBtag", "MT_InvertedTauIdBtag;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETInvertedTauIdBtagDphi = makeTH<TH1F>(*fs, "MET_InvertedTauIdBtagDphi", "MET_InvertedTauIdBtagDphi;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);
    hMETBaselineTauIdBtagDphi = makeTH<TH1F>(*fs, "MET_BaseLineTauIdBtagDphi", "MET_BaseLineTauIdBtagDphi;PF MET, GeV;N_{events} / 10 GeV", 400, 0.0, 400.0);

    
    hSelectedTauEtMetCut = makeTH<TH1F>(*fs, "SelectedTau_pT_AfterMetCut", "SelectedTau_pT_AfterMetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 400, 0.0, 400.0);
    hSelectedTauEtaMetCut = makeTH<TH1F>(*fs, "SelectedTau_eta_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.1", 300, -3.0, 3.0);
    hSelectedTauPhiMetCut = makeTH<TH1F>(*fs, "SelectedTau_phi_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.087", 360, -3.1415926, 3.1415926);
    hSelectedTauRtauMetCut = makeTH<TH1F>(*fs, "SelectedTau_Rtau_AfterMetCut", "SelectedTau_Rtau_AfterMetCut;R_{#tau};N_{events} / 0.1", 360, 0., 1.2);

    hSelectionFlow = makeTH<TH1F>(*fs, "SignalSelectionFlow", "SignalSelectionFlow;;N_{events}", 7, 0, 7);
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

    hEMFractionAll = makeTH<TH1F>(*fs, "NonQCDTypeII_FakeTau_EMFraction_All", "FakeTau_EMFraction_All", 22, 0., 1.1);
    hEMFractionElectrons = makeTH<TH1F>(*fs, "NonQCDTypeII_FakeTau_EMFraction_Electrons", "FakeTau_EMFraction_Electrons", 22, 0., 1.1);
    
    hNonQCDTypeIISelectedTauEtAfterCuts = makeTH<TH1F>(*fs, "NonQCDTypeII_SelectedTau_pT_AfterCuts", "SelectedTau_pT_AfterCuts;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 40, 0.0, 400.0);
    hNonQCDTypeIISelectedTauEtaAfterCuts = makeTH<TH1F>(*fs, "NonQCDTypeII_SelectedTau_eta_AfterCuts", "SelectedTau_eta_AfterCuts;#tau #eta;N_{events} / 0.1", 30, -3.0, 3.0);

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
    std::pair<double, size_t> weightSize = fVertexWeight.getWeightAndSize(iEvent, iSetup);
    if(!iEvent.isRealData()) {
      fEventWeight.multiplyWeight(weightSize.first);
      fTree.setPileupWeight(weightSize.first);
    }
    hVerticesBeforeWeight->Fill(weightSize.second);
    hVerticesAfterWeight->Fill(weightSize.second, fEventWeight.getWeight());
    fTree.setNvertices(weightSize.second);
    //    std::cout << " weight before  = " << fEventWeight.getWeight() << std::endl;
    // QCD fraction from fit
    //    double QCDfraction = 0.86;
    //    fEventWeight.multiplyWeight(QCDfraction);
    //     std::cout << " weight after  = " << fEventWeight.getWeight() <<  std::endl;
    increment(fAllCounter);
    
    // Apply trigger and HLT_MET cut or trigger parametrisation
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);
    hSelectionFlow->Fill(kSignalOrderTrigger, fEventWeight.getWeight());

    hVerticesTriggeredBeforeWeight->Fill(weightSize.second);
    hVerticesTriggeredAfterWeight->Fill(weightSize.second, fEventWeight.getWeight());

    // GenParticle analysis (must be done here when we effectively trigger all MC)
    if (!iEvent.isRealData()) fGenparticleAnalysis.analyze(iEvent, iSetup);

    // Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    //hSelectionFlow->Fill(kSignalOrderVertexSelection, fEventWeight.getWeight());

  // Get MET object 
    //    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    //double Met = metData.getSelectedMET()->et();
    //    std::cout << " weight before  = " << fEventWeight.getWeight() << " met " << Met <<  std::endl;
    //    hMETBeforeTauId->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());  



  
    // TauID 
    TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    edm::PtrVector<pat::Tau> myBestTauCandidate;
    if (tauData.getSelectedTaus().size())
      myBestTauCandidate.push_back(tauData.getSelectedTau());

   
    if(tauData.getSelectedTaus().size() == 0) return false; // Require exactly one tau
    increment(fTausExistCounter);
    
    // nprongs
    if (tauData.selectedTauPassesNProngs()) return false;
    increment(fNprongsAfterTauIDCounter);

    hSelectedTauLeadingTrackPt->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt(), fEventWeight.getWeight());

    // rtau
    hSelectedTauRtau->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());
    if (!tauData.selectedTauPassesRtau()) return false;
    increment(fRtauAfterTauIDCounter);
    // now tau ID has been applied


    if(iEvent.isRealData())
      fTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
    // Apply trigger scale factor here, because it depends only on tau
    TriggerEfficiencyScaleFactor::Data triggerWeight = fTriggerEfficiencyScaleFactor.applyEventWeight(*(tauData.getSelectedTau()), iEvent.isRealData());
    fTree.setTriggerWeight(triggerWeight.getEventWeight(), triggerWeight.getEventWeightAbsoluteUncertainty());
    increment(fTriggerScaleFactorCounter);
    hSelectionFlow->Fill(kSignalOrderTauID, fEventWeight.getWeight());




    std::string myTauIsolation = "byTightIsolation";


 // Get MET object 
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    //double Met = metData.getSelectedMET()->et();
    //    std::cout << " weight before  = " << fEventWeight.getWeight() << " met " << Met <<  std::endl;
    hMETBeforeTauId->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());  


    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    // Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    // Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup,  tauData.getSelectedTau()); 
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());

    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());

    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()));
    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()) );
   
      

  // baseline tau-id
    if (tauData.selectedTauPassesDiscriminator(myTauIsolation, 0.5)) {
      hMETBaselineTauId->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      increment(fBaselineTauIDCounter);
      if (electronVetoData.passedEvent()) {
	increment(fBaselineEvetoCounter);
	if (muonVetoData.passedEvent()) {
	  increment(fBaselineMuvetoCounter);
	  if(jetData.passedEvent()) {
	    increment(fBaselineJetsCounter);
	    // Count baseline events
	    if(metData.passedEvent()) {	
	      increment(fBaselineMetCounter);   
	      if(btagData.passedEvent()) {
		increment(fBaselineBtagCounter);
		if ( deltaPhi*57.3 < 160) {
		  increment(fBaselineDphi160Counter);
		if ( deltaPhi*57.3 < 130) increment(fBaselineDphi130Counter);
		  hMETBaselineTauIdBtagDphi->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight()); 
		  if (TopChiSelectionData.passedEvent() ) {
		    increment(fBaselineTopChiSelectionCounter);    
		    hTransverseMassTopChiSelection->Fill(transverseMass, fEventWeight.getWeight());  
		  }  	      
		}
	      }
	    }
	    if(btagData.passedEvent()) {
	      hMETBaselineTauIdBtag->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight()); 
	      if ( tauData.getSelectedTau()->pt() > 150  ) hMETBaselineTauIdBtag150->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMETBaselineTauIdBtag120150->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMETBaselineTauIdBtag100120->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100  ) hMETBaselineTauIdBtag80100->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMETBaselineTauIdBtag7080->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMETBaselineTauIdBtag6070->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMETBaselineTauIdBtag5060->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMETBaselineTauIdBtag4050->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	      


	      hMTBaselineTauIdBtag->Fill(transverseMass, fEventWeight.getWeight());   
	     
	      hMTBaselineTauIdJet->Fill(transverseMass, fEventWeight.getWeight()); 
	      // mT with b tagging and met cut
	      if(metData.passedEvent()) {
		if ( tauData.getSelectedTau()->pt() > 150  ) hMTBaselineTauIdJet150->Fill(transverseMass, fEventWeight.getWeight()); 
		if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTBaselineTauIdJet120150->Fill(transverseMass, fEventWeight.getWeight()); 
		if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTBaselineTauIdJet100120->Fill(transverseMass, fEventWeight.getWeight()); 
		if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTBaselineTauIdJet80100->Fill(transverseMass, fEventWeight.getWeight()); 
		if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTBaselineTauIdJet7080->Fill(transverseMass, fEventWeight.getWeight()); 
		if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTBaselineTauIdJet6070->Fill(transverseMass, fEventWeight.getWeight()); 
		if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTBaselineTauIdJet5060->Fill(transverseMass, fEventWeight.getWeight()); 
		if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTBaselineTauIdJet4050->Fill(transverseMass, fEventWeight.getWeight());
	      }
	    }


	    hMETBaselineTauIdJets->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());  
	    if ( tauData.getSelectedTau()->pt() > 150  ) hMETBaselineTauIdJets150->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMETBaselineTauIdJets120150->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMETBaselineTauIdJets100120->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100  ) hMETBaselineTauIdJets80100->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMETBaselineTauIdJets7080->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	    if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMETBaselineTauIdJets6070->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMETBaselineTauIdJets5060->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMETBaselineTauIdJets4050->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
	  }
	}
      }
    }

    // TauID, inverted TauID, veto on isolated taus
    if(!tauData.selectedTausDoNotPassIsolation())  return false; 
    // veto was successfull
    increment(fTauVetoAfterTauIDCounter);

    hMETInvertedTauId->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());  

    //    if(!tauData.passedEvent()) return false; // Require at least one tau candidate
    // plot leading track without pt cut
    //    hSelectedTauLeadingTrackPt->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt(), fEventWeight.getWeight());
    //    if (tauData.getSelectedTau()->leadPFChargedHadrCand()->pt() < 20.0) return false;

    //    increment(fTausExistCounter);
    //    if(tauData.getSelectedTaus().size() == 0) return false; // Require exactly one tau
    // Apply trigger scale factor here, because it depends only on tau
    //    TriggerEfficiencyScaleFactor::Data triggerWeight = fTriggerEfficiencyScaleFactor.applyEventWeight(*(tauData.getSelectedTau()), iEvent.isRealData());
    //    fTree.setTriggerWeight(triggerWeight.getEventWeight(), triggerWeight.getEventWeightAbsoluteUncertainty());
    //    increment(fOneTauCounter);
    hSelectionFlow->Fill(kSignalOrderTauID, fEventWeight.getWeight());
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Tau> > saveTaus(new std::vector<pat::Tau>());
      copyPtrToVector(tauData.getSelectedTaus(), *saveTaus);
      iEvent.put(saveTaus, "selectedTaus");
    }

  
    
    //    hSelectedTauRtau->Fill(tauData.getRtauOfBestTauCandidate(), fEventWeight.getWeight());  
    //    if(tauData.getRtauOfBestTauCandidate() < 0.8 ) return false;
    //    increment(fRtauAfterTauIDCounter);

    //    hSelectedTauLeadingTrackPt->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt(), fEventWeight.getWeight());
    //    if (tauData.getSelectedTau()->leadPFChargedHadrCand()->pt() < 20.0) return false;                             
  
    hSelectedTauEt->Fill(tauData.getSelectedTau()->pt(), fEventWeight.getWeight());
    hSelectedTauEta->Fill(tauData.getSelectedTau()->eta(), fEventWeight.getWeight());
    hSelectedTauPhi->Fill(tauData.getSelectedTau()->phi(), fEventWeight.getWeight());
    //    hSelectedTauRtau->Fill(tauData.getRtauOfBestTauCandidate(), fEventWeight.getWeight());
    if(metData.passedEvent()) {
      //      hSelectedTauEtMetCut->Fill(tauData.getSelectedTau()->pt(), fEventWeight.getWeight());
      hSelectedTauLeadingTrackPtMetCut->Fill(tauData.getSelectedTau()->leadPFChargedHadrCand()->pt(), fEventWeight.getWeight());
    }

    // Obtain MC matching
    MCSelectedTauMatchType myTauMatch = matchTauToMC(iEvent, tauData.getSelectedTau());
    fAllTausCounterGroup.incrementOneTauCounter();
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderTauID, tauData);
    if (myTauMatch == kkElectronToTau)
      hEMFractionElectrons->Fill(tauData.getSelectedTau()->emFraction());
    hEMFractionAll->Fill(tauData.getSelectedTau()->emFraction());


    //    double transverseMass = TransverseMass::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()) );
    // hTransverseMassBeforeVeto->Fill(transverseMass);
    // Hadronic jet selection                                                                                                                                      
    //    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauData.getSelectedTaus());


    hTransverseMassBeforeVeto->Fill(transverseMass, fEventWeight.getWeight());
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderMETSelection, tauData);

    //    Global electron veto
    //    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);
    hSelectionFlow->Fill(kSignalOrderElectronVeto, fEventWeight.getWeight());
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
    hSelectionFlow->Fill(kSignalOrderMuonVeto, fEventWeight.getWeight());
    hTransverseMassAfterVeto->Fill(transverseMass, fEventWeight.getWeight());
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
    hSelectionFlow->Fill(kSignalOrderJetSelection, fEventWeight.getWeight());
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
    hMETInvertedTauIdJets->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    if ( tauData.getSelectedTau()->pt() > 150  ) hMETInvertedTauIdJets150->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMETInvertedTauIdJets120150->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMETInvertedTauIdJets100120->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMETInvertedTauIdJets80100->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMETInvertedTauIdJets7080->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());  																	     																	     
    if ( tauData.getSelectedTaus()
[0]->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMETInvertedTauIdJets6070->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMETInvertedTauIdJets5060->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMETInvertedTauIdJets4050->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());																		


 // Get MET object 
    //    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup);
    //double Met = metData.getSelectedMET()->et();
    //    std::cout << " weight before  = " << fEventWeight.getWeight() << " met " << Met <<  std::endl;
    //    hMETBeforeTauId->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());  
															      


    // Inverted MET with loose isolation
    if (tauData.selectedTauPassesDiscriminator("byLooseIsolation", 0.5)) {
      hMETInvertedTauIdLoose->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      if ( tauData.getSelectedTau()->pt() > 150  ) hMETInvertedTauIdLoose150->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 70 ) hMETInvertedTauIdLoose4070->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 150 ) hMETInvertedTauIdLoose70150->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      hMTInvertedTauIdLoose->Fill(transverseMass, fEventWeight.getWeight());
    }
    
  
    if(!btagData.passedEvent()) {
      hMETInvertedTauIdBtag->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      //      hMTInvertedTauIdBtag->Fill(transverseMass, fEventWeight.getWeight());
     
      if ( tauData.getSelectedTau()->pt() > 150  ) hMETInvertedTauIdBtag150->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMETInvertedTauIdBtag120150->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMETInvertedTauIdBtag100120->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMETInvertedTauIdBtag80100->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());


      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMETInvertedTauIdBtag7080->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());  															  															     
      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMETInvertedTauIdBtag6070->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMETInvertedTauIdBtag5060->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMETInvertedTauIdBtag4050->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());																		
    }
  
 
    // b tagging, no event cut
    //    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
    // Top reco, no event cut
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    // Calculate alphaT
    EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauData.getSelectedTau()), jetData.getSelectedJets()); 
    FakeMETVeto::Data fakeMETData = fFakeMETVeto.analyze(iEvent, iSetup, tauData.getSelectedTau(), jetData.getSelectedJets(), metData.getSelectedMET());
    // Write the stuff to the tree 
    //    fTree.setFillWeight(fEventWeight.getWeight());
    //    fTree.setBTagging(btagData.passedEvent(), btagData.getScaleFactor());
    //    fTree.setTop(TopSelectionData.getTopP4());
    //    fTree.fill(iEvent, tauData.getSelectedTaus(), jetData.getSelectedJets(), metData.getSelectedMET(),
    //               evtTopologyData.alphaT().fAlphaT, fakeMETData.closestDeltaPhi() );

 

 
    
    hTransverseMassNoMet->Fill(transverseMass, fEventWeight.getWeight());
    if(btagData.passedEvent())   {
      hTransverseMassNoMetBtag->Fill(transverseMass, fEventWeight.getWeight());
    } 

    // MET cut
    hMETBeforeMETCut->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());
    if(!metData.passedEvent()) return false;
    increment(fMETCounter);
    hSelectionFlow->Fill(kSignalOrderMETSelection, fEventWeight.getWeight());

    hSelectedTauEtMetCut->Fill(tauData.getSelectedTau()->pt(), fEventWeight.getWeight());
    hSelectedTauEtaMetCut->Fill(tauData.getSelectedTau()->eta(), fEventWeight.getWeight());
    hSelectedTauPhiMetCut->Fill(tauData.getSelectedTau()->phi(), fEventWeight.getWeight());
    hSelectedTauRtauMetCut->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());   

    // b tagging cut
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderBTagSelection, tauData, btagData.passedEvent(),btagData.getMaxDiscriminatorValue());
    if(!btagData.passedEvent()) return false;
    // Apply scale factor as weight to event
    fEventWeight.multiplyWeight(btagData.getScaleFactor());
    increment(fBTaggingCounter);
    hSelectionFlow->Fill(kSignalOrderBTagSelection, fEventWeight.getWeight());
    hMet_AfterBTagging->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());

    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveBJets(new std::vector<pat::Jet>());
      copyPtrToVector(btagData.getSelectedJets(), *saveBJets);
      iEvent.put(saveBJets, "selectedBJets");
    }


    double topMass = TopChiSelectionData.getTopMass();
    hTopMass->Fill(topMass, fEventWeight.getWeight());
    // top mass with binning    
    if ( tauData.getSelectedTau()->pt() > 150  ) hMTInvertedTauIdJet150->Fill(transverseMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hTopMass120150->Fill(topMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hTopMass100120->Fill(topMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hTopMass80100->Fill(topMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hTopMass7080->Fill(topMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hTopMass6070->Fill(topMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hTopMass5060->Fill(topMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hTopMass4050->Fill(topMass, fEventWeight.getWeight()); 


    // mt for inverted tau with Met and b tagging
    hMTInvertedTauIdJet->Fill(transverseMass, fEventWeight.getWeight()); 
    hMTInvertedTauIdBtag->Fill(transverseMass, fEventWeight.getWeight());
    if ( tauData.getSelectedTau()->pt() > 150  ) hMTInvertedTauIdJet150->Fill(transverseMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTInvertedTauIdJet120150->Fill(transverseMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTInvertedTauIdJet100120->Fill(transverseMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTInvertedTauIdJet80100->Fill(transverseMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTInvertedTauIdJet7080->Fill(transverseMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTInvertedTauIdJet6070->Fill(transverseMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTInvertedTauIdJet5060->Fill(transverseMass, fEventWeight.getWeight()); 
    if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTInvertedTauIdJet4050->Fill(transverseMass, fEventWeight.getWeight()); 


   // mt for inverted tau with MET>70 cut   
    if (metData.getSelectedMET()->et() > 70) {
      hMTInvertedTauIdMet->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 150  ) hMTInvertedTauIdJet150->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTInvertedTauIdMet120150->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTInvertedTauIdMet100120->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTInvertedTauIdMet80100->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTInvertedTauIdMet7080->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTInvertedTauIdMet6070->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTInvertedTauIdMet5060->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTInvertedTauIdMet4050->Fill(transverseMass, fEventWeight.getWeight());
    }
   // mt for inverted tau with deltaphi cut

    if ( deltaPhi*57.3 < 160 ) {
      hMTInvertedTauIdJetPhi->Fill(transverseMass, fEventWeight.getWeight()); 
      increment(fdeltaPhiTauMET160Counter);
      if ( tauData.getSelectedTau()->pt() > 150  ) hMTInvertedTauIdJetPhi150->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTInvertedTauIdJetPhi120150->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTInvertedTauIdJetPhi100120->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTInvertedTauIdJetPhi80100->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTInvertedTauIdJetPhi7080->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTInvertedTauIdJetPhi6070->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTInvertedTauIdJetPhi5060->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTInvertedTauIdJetPhi4050->Fill(transverseMass, fEventWeight.getWeight()); 
    }

       

    //    if ( deltaPhi*57.3 < 130 ) {
    if (TopChiSelectionData.passedEvent()  &&  deltaPhi*57.3 < 160 ) {
      hMTInvertedTauIdTopMass->Fill(transverseMass, fEventWeight.getWeight());
      increment(fdeltaPhiTauMET130Counter); 
      if ( tauData.getSelectedTau()->pt() > 150  ) hMTInvertedTauIdJetPhi150->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 120 && tauData.getSelectedTau()->pt() < 150 ) hMTInvertedTauIdTopMass120150->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 100 && tauData.getSelectedTau()->pt() < 120 ) hMTInvertedTauIdTopMass100120->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 80 && tauData.getSelectedTau()->pt() < 100 ) hMTInvertedTauIdTopMass80100->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 70 && tauData.getSelectedTau()->pt() < 80 ) hMTInvertedTauIdTopMass7080->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 60 && tauData.getSelectedTau()->pt() < 70 ) hMTInvertedTauIdTopMass6070->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 50 && tauData.getSelectedTau()->pt() < 60 ) hMTInvertedTauIdTopMass5060->Fill(transverseMass, fEventWeight.getWeight()); 
      if ( tauData.getSelectedTau()->pt() > 40 && tauData.getSelectedTau()->pt() < 50 ) hMTInvertedTauIdTopMass4050->Fill(transverseMass, fEventWeight.getWeight()); 
    }




    //    double deltaPhi = DeltaPhi::reconstruct(*(tauData.getSelectedTau()), *(metData.getSelectedMET()));
    hDeltaPhi->Fill(deltaPhi*57.3, fEventWeight.getWeight());
    if ( deltaPhi*57.3 > 10) increment(fdeltaPhiTauMET10Counter); 


 
    if ( deltaPhi*57.3 > 160) return false;
    hTransverseMassDeltaPhiUpperCut->Fill(transverseMass, fEventWeight.getWeight());  
     

    // plot deltaPhi(jet,met)
    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetData.getSelectedJets().begin(); iJet != jetData.getSelectedJets().end(); ++iJet) {
      deltaPhi = DeltaPhi::reconstruct(**iJet, *(metData.getSelectedMET()));
      hDeltaPhiJetMet->Fill(deltaPhi*57.3, fEventWeight.getWeight());
    }

    hSelectedTauRtauAfterCuts->Fill(tauData.getRtauOfSelectedTau(), fEventWeight.getWeight());
    hSelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt(), fEventWeight.getWeight());
    hSelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta(), fEventWeight.getWeight());
    hMetAfterCuts->Fill(metData.getSelectedMET()->et(), fEventWeight.getWeight());


   
    if (TopChiSelectionData.passedEvent() ) {
         increment(fTopChiSelectionCounter);
      //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
	 hTransverseMassTopChiSelection->Fill(transverseMass, fEventWeight.getWeight());     
    } 

    if (BjetSelectionData.passedEvent() ) {
        
      TopWithBSelection::Data TopWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());

      if (TopWithBSelectionData.passedEvent() ) {
	increment(fTopWithBSelectionCounter);
	//      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
	hTransverseMassTopBjetSelection->Fill(transverseMass, fEventWeight.getWeight());     
      }    
    }


    //    return false;

   // top mass with possible event cuts
    if (TopSelectionData.passedEvent() ) {
      increment(fTopSelectionCounter);
      //      hSelectionFlow->Fill(kSignalOrderTopSelection, fEventWeight.getWeight());      
      hTransverseMassWithTopCut->Fill(transverseMass, fEventWeight.getWeight());
      if(transverseMass > 80 ) increment(ftransverseMassCut100TopCounter);   
    } 


    if (fakeMETData.passedEvent() ) {
      increment(fFakeMETVetoCounter);
      hTransverseMass->Fill(transverseMass, fEventWeight.getWeight());
      if ( deltaPhi*57.3 < 135) {
	increment(fdeltaPhiTauMET160FakeMetCounter);
	//	hTransverseMassDeltaPhiUpperCutFakeMet->Fill(transverseMass, fEventWeight.getWeight());  
      } 
    }
    //hSelectionFlow->Fill(kSignalOrderFakeMETVeto, fEventWeight.getWeight());
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
    //hSelectionFlow->Fill(kSignalOrderFakeMETVeto, fEventWeight.getWeight());
    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderFakeMETVeto, tauData);

    // Correlation analysis
    fCorrelationAnalysis.analyze(tauData.getSelectedTaus(), btagData.getSelectedJets());
    // Alpha T
    //if(!evtTopologyData.passedEvent()) return false;
    //    EvtTopology::AlphaStruc sAlphaT = evtTopologyData.alphaT();
    //    hAlphaT->Fill(sAlphaT.fAlphaT, fEventWeight.getWeight()); // FIXME: move this histogramming to evt topology


   
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
        hNonQCDTypeIISelectedTauEtAfterCuts->Fill(tauData.getSelectedTau()->pt(), fEventWeight.getWeight());
        hNonQCDTypeIISelectedTauEtaAfterCuts->Fill(tauData.getSelectedTau()->eta(), fEventWeight.getWeight());
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
