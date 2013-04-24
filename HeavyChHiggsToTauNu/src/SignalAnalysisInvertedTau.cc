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

  SignalAnalysisInvertedTau::SignalAnalysisInvertedTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper):
    fEventWeight(eventWeight),
    fHistoWrapper(histoWrapper),
    fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
    bBlindAnalysisStatus(iConfig.getUntrackedParameter<bool>("blindAnalysisStatus")),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fAllCounter(eventCounter.addCounter("All events")),
    fWJetsWeightCounter(eventCounter.addCounter("WJets inc+exl weight")),
    fVertexFilterCounter(eventCounter.addCounter("Vertex number filter")),
    fMETFiltersCounter(eventCounter.addCounter("MET filters")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),  
    fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
    fTauCandidateCounter(eventCounter.addCounter("Tau candidates found")),
    fNprongsAfterTauIDCounter(eventCounter.addCounter("Nprongs cut, all tau candidates")),
    fRtauAfterTauIDCounter(eventCounter.addCounter("Rtau cut, all tau candidates")),
    fTausExistCounter(eventCounter.addCounter("Baseline: isolation, all passed taus")),
    fTauFakeScaleFactorBaselineCounter(eventCounter.addCounter("Baseline:tau fake scale factor, all passed taus")),
    fTauTriggerScaleFactorBaselineCounter(eventCounter.addCounter("Baseline:tau trig scale factor, all passed taus")),  
    fBaselineTauIDCounter(eventCounter.addCounter("Baseline: at least one tau")),
    fBaselineEvetoCounter(eventCounter.addCounter("Baseline: electron veto")),
    fBaselineMuvetoCounter(eventCounter.addCounter("Baseline: muon veto")),
    fBaselineJetsCounter(eventCounter.addCounter("Baseline:  njets")),
    fBaselineMetCounter(eventCounter.addCounter("Baseline: MET")),
    fBaselineBtagCounter(eventCounter.addCounter("Baseline: btagging")),
    fBTaggingScaleFactorCounter(eventCounter.addCounter("Baseline: btagging scale factor")),
    fBaselineDeltaPhiTauMETCounter(eventCounter.addCounter("Baseline: DeltaPhi(Tau,MET) upper limit")),
    fBaselineDeltaPhiVSDeltaPhiMHTJet1CutCounter(eventCounter.addCounter("Baseline: DeltaPhi(Jets,MET) vs DeltaPhi cut")),
    fOneTauCounter(eventCounter.addCounter("Baseline, taus = 1")),
    // confligt starts
    fTauFakeScaleFactorCounter(eventCounter.addCounter("Inverted: tau fake scale factor, all cands")),
    fTauTriggerScaleFactorCounter(eventCounter.addCounter("Inverted: tau trigger scale factor, all cands")),
    fTauVetoAfterTauIDCounter(eventCounter.addCounter("Inverted: Taus found")),
    fElectronVetoCounter(eventCounter.addCounter("Inverted: electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("Inverted: muon veto")),
    fNJetsCounter(eventCounter.addCounter("Inverted: njets")),
    fBTaggingBeforeMETCounter(eventCounter.addCounter("Inverted: btagging before MET")),
    fMETCounter(eventCounter.addCounter("Inverted: MET")),
    fBjetVetoCounter(eventCounter.addCounter("Inverted: Veto on b jets before MET")),
    fBvetoCounter(eventCounter.addCounter("Inverted: Veto on b jets after MET")),
    fBvetoDeltaPhiCounter(eventCounter.addCounter("Inverted: Veto on b jets after MET and Dphi")),
    fBTaggingCounter(eventCounter.addCounter("Inverted: btagging")),
    fBTaggingScaleFactorInvertedCounter(eventCounter.addCounter("Inverted: btagging scale factor")),
    fQCDTailKillerCounter(eventCounter.addCounter("QCD tail killer")),
    fDeltaPhiTauMETCounter(eventCounter.addCounter("Inverted: DeltaPhi(Tau,MET) upper limit")),
    fDeltaPhiVSDeltaPhiMETJet1CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet1,MET) vs DeltaPhi cut")),
    fDeltaPhiVSDeltaPhiMETJet2CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet2,MET) vs DeltaPhi cut")),
    fDeltaPhiVSDeltaPhiMETJet3CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet3,MET) vs DeltaPhi cut")),
    fDeltaPhiVSDeltaPhiMETJet4CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet4,MET) vs DeltaPhi cut")), 
    fDeltaPhiAgainstTTCutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet1,MET) cut against TT")), 
    fHiggsMassCutCounter(eventCounter.addCounter("Inverted: HiggsMassCut")),
    ftransverseMassCut80Counter(eventCounter.addCounter("Inverted: transverseMass > 60")),
    ftransverseMassCut100Counter(eventCounter.addCounter("Inverted: transverseMass > 80")),
    fTopSelectionCounter(eventCounter.addCounter("Inverted: Top Selection cut")),
    fTopChiSelectionCounter(eventCounter.addCounter("Inverted: Top ChiSelection cut")),
    fTopWithBSelectionCounter(eventCounter.addCounter("Inverted: Top with B Selection cut")),
    ftransverseMassCut100TopCounter(eventCounter.addCounter("Inverted: transverseMass > 100 top cut")),
    

    /*
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
    fQCDTailKillerCounter(eventCounter.addCounter("QCD tail killer")),
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
    */


    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
    fElectronSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("ElectronSelection"), fPrimaryVertexSelection.getSelectedSrc(), eventCounter, fHistoWrapper),
    fMuonSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MuonSelection"), eventCounter, fHistoWrapper),
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
    //    fHistogramsInBins(eventCounter, fHistoWrapper, "DirectoryName","HistoName", 250, double , double ),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, fHistoWrapper),
    fTauTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("tauTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fMETTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("metTriggerEfficiencyScaleFactor"), fHistoWrapper),
    //    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), fHistoWrapper, "TauID"),
    fPrescaleWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("prescaleWeightReader"), fHistoWrapper, "PrescaleWeight"),
    fPileupWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("pileupWeightReader"), fHistoWrapper, "PileupWeight"),
    fMETFilters(iConfig.getUntrackedParameter<edm::ParameterSet>("metFilters"), eventCounter),
    fQCDTailKiller(iConfig.getUntrackedParameter<edm::ParameterSet>("QCDTailKiller"), eventCounter, fHistoWrapper),
    fWJetsWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("wjetsWeightReader"), fHistoWrapper, "WjetsWeight"),
    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), fHistoWrapper, "TauID"),
    fTree(iConfig.getUntrackedParameter<edm::ParameterSet>("Tree"), fBTagging.getDiscriminator()),
    fVertexAssignmentAnalysis(iConfig, eventCounter, fHistoWrapper),
    fMETPhiOscillationCorrection(iConfig, eventCounter, fHistoWrapper),
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
 
 
    TFileDirectory myInverted = fs->mkdir("Inverted");
    TFileDirectory myBaseline = fs->mkdir("BaseLine");    
    // Book histograms filled in the analysis body
    hOneProngRtauPassedInvertedTaus= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "OneProngRtauPassedInvertedTaus", "OneProngRtauPassedInvertedTaus", 10, 0, 10);
    hTauDiscriminator= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "TauDiscriminator", "TauDiscriminator", 100, 0, 2);

    hVerticesBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesBeforeWeight", "Number of vertices without weighting", 30, 0, 30);
    hVerticesAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesAfterWeight", "Number of vertices with weighting", 30, 0, 30);
    hVerticesTriggeredBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesTriggeredBeforeWeight", "Number of vertices without weighting", 30, 0, 30);
    hVerticesTriggeredAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesTriggeredAfterWeight", "Number of vertices with weighting", 30, 0, 30);    
    hTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kSystematics, *fs, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
    hTransverseMassWithTopCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassWithTopCut", "transverseMassWithTopCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassTopChiSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassTopChiSelection", "transverseMassTopChiSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassTopBjetSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassTopBjetSelection", "transverseMassTopBjetSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
   
    hDeltaPhiAfterJets= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted , "deltaPhiAfterJets", "deltaPhiAfterJets", 180, 0., 180.);
    
    hTransverseMassVsDphi = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, *fs, "transverseMassVsDphi", "transverseMassVsDphi;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.,180,0.,180.);
    hSelectedTauEt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_pT_AfterTauID", "SelectedTau_pT_AfterTauID;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);    
    hSelectedTauEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_eta_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.1", 150, -3.0, 3.0);   
    hSelectedTauEtAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedInvertedTauAfterCuts", "SelectedInvertedTauAfterCuts", 100, 0.0, 400.0);
    hSelectedTauEtaAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedInvertedTau_eta_AfterCuts", "SelectedInvertedTau_eta_AfterCuts", 60, -3.0, 3.0);
    hSelectedTauPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_phi_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.087", 180, -3.1415926, 3.1415926);
    hSelectedTauRtau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_Rtau_AfterTauID", "SelectedTau_Rtau_AfterTauID;R_{#tau};N_{events} / 0.1", 240, 0., 1.2);

    hSelectedTauLeadingTrackPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_TauLeadingTrackPt", "SelectedTau_TauLeadingTrackPt;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    //    hTransverseMassTailKiller = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kSystematics, *fs, "transverseMassTailKiller", "transverseMassTailKiller", 200, 0., 400.);   

    hMETBaselineTauId =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MET_BaseLineTauId", 250, 0.0 , 500.0 );
    hMETBaselineTauIdJets =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MET_BaseLineTauIdJets", 250, 0.0 , 500.0 );
    hMETBaselineTauIdBtag =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MET_BaseLineTauIdBtag", 250, 0.0 , 500.0 );
    hMETBaselineTauIdBveto =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MET_BaseLineTauIdBveto", 250, 0.0 , 500.0 );

    hMTBaselineTauIdJet =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdJet", 200, 0.0, 400.0 );
    hMTBaselineTauIdBveto =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdBveto", 200, 0.0, 400.0 );
    hMTBaselineTauIdBvetoTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdBvetoTailKiller", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoBtagging = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTaudNoBtagging", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoBtaggingTailKiller= new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTaudNoBtaggingTailKiller", 200, 0.0, 400.0 );
    //    hMTBaselineTauIdJetTailKiller = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdJetTailKiller", 200, 0.0, 400.0 );
    hMTBaselineTauIdBtag =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdBtag", 200, 0.0, 400.0 );
    //    hMTBaselineTauIdBvetoDphi =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdBvetoDphi", 200, 0.0, 400.0 );
    //    hMTBaselineTauIdPhi =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdPhi", 200, 0.0, 400.0 );

    hMTBaselineTauIdAllCutsTailKiller =  new HistogramsInBins(HistoWrapper::kSystematics, eventCounter, fHistoWrapper, "BaseLine","MTBaselineTauIdAllCutsTailKiller", 200, 0.0, 400.0 ); 

    hMTBaselineTauIdNoMetBveto =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaselineTauIdNoMetBveto", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoMetBvetoTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaselineTauIdNoMetBvetoTailKiller", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoMetBtag =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaselineTauIdNoMetBtag", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoMetBtagTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaselineTauIdNoMetBtagTailKiller", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoMetNoBtagging=  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaselineTauIdNoMetBtagging", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoMetNoBtaggingTailKiller=  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaselineTauIdNoMetBtaggingTailKiller", 200, 0.0, 400.0 );
    hMTInvertedTauIdJet =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdJet", 200, 0.0, 400.0 );
    hMTInvertedTauIdJetTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdJetTailKiller", 200, 0.0, 400.0 );
    hMTInvertedTauIdJetDphi =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdJetDphi", 200, 0.0, 400.0 ); 
    hMTInvertedTauIdBtag =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBtag", 200, 0.0, 400.0 ); 
    hMTInvertedTauIdNoBtagging=  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdNoBtagging", 200, 0.0, 400.0 ); 
    hMTInvertedTauIdBveto =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBveto", 200, 0.0, 400.0 ); 
    hMTInvertedTauIdBvetoDphi =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBvetoDphi", 200, 0.0, 400.0 );
 
    hMTInvertedAllCutsTailKiller =  new HistogramsInBins(HistoWrapper::kSystematics, eventCounter, fHistoWrapper, "Inverted","MTInvertedAllCutsTailKiller", 200, 0.0, 400.0 );

    hMTInvertedNoBtagging = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedNoBtagging", 200, 0.0, 400.0 );    
    hMTInvertedNoBtaggingTailKiller = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedNoBtaggingTailKiller", 200, 0.0, 400.0 );

    hTopMass =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","TopMass", 200, 0.0, 400.0 );
    hHiggsMass =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","HiggsMass", 250, 0.0 , 500.0 );
    //    hHiggsMassTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","HiggsMassTailKiller", 250, 0.0 , 500.0 );

    hMTInvertedTauIdBtagNoMetCut =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBtagNoMetCut", 200, 0.0, 400.0 );
    hMTInvertedTauIdBvetoNoMetCut =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBvetoNoMetCut", 200, 0.0, 400.0 );
    hMTInvertedTauIdBvetoNoMetCutTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBvetoNoMetCutTailKiller", 200, 0.0, 400.0 );
    hMTInvertedTauIdBtagNoMetCutTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBtagNoMetCutTailKiller", 200,0.0, 400.0 );
    hNBInvertedTauIdJet =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","NBInvertedTauIdJet", 10, 0.0 , 10.0 );
    hNBInvertedTauIdJetDphi =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","NBInvertedTauIdJetDphi", 10, 0.0 , 10.0 );
    hNJetInvertedTauId =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","NJetInvertedTauId", 10, 0.0 , 10.0 );
    hNJetInvertedTauIdMet =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","NJetInvertedTauIdMet", 10, 0.0 , 10.0 );
    hDeltaPhiInverted =   new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","DeltaPhiInverted", 180, 0., 180.);
    hDeltaPhiInvertedNoB =   new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","DeltaPhiInvertedNoB", 180, 0., 180.);
  
    hMETInvertedTauId = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MET_InvertedTauId", 250, 0.0 , 500.0 );
    hMETInvertedTauIdJets = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MET_InvertedTauIdJets", 250, 0.0 , 500.0 );
    hMETInvertedTauIdBtag = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MET_InvertedTauIdBtag", 250, 0.0 , 500.0 );
    hMETInvertedTauIdBveto = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MET_InvertedTauIdBveto", 250, 0.0 , 500.0 );
    hMETInvertedAllCutsTailKiller = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MET_InvertedAllCutsTailKiller", 250, 0.0 , 500.0 );

    hNBBaselineTauIdJet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myBaseline, "NBBaselineTauIdJet", "NBBaselineTauIdJet", 10, 0., 10.);
    hNJetBaselineTauIdMet= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myBaseline, "NJetBaselineTauIdJetMet", "NJetBaselineTauIdJetMet", 10, 0., 10.);
    hNJetBaselineTauId = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myBaseline, "NJetBaselineTauIdJet", "NJetBaselineTauIdJet", 20, 0., 20.);
    hDeltaPhiBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myBaseline , "deltaPhiBaseline", "deltaPhi;#Delta#phi", 180, 0., 180.);


    hSelectedTauEt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "SelectedTau_pT_AfterRtauCut", "SelectedTau_pT_AfterRtauCut", 200, 0.0, 400.0);
    hSelectedTauEtTauVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "SelectedTau_pT_AfterTauVeto", "SelectedTau_pT_AfterTauVeto", 200, 0.0, 400.0);     
    hSelectedTauEtJetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "SelectedTau_pT_AfterJetCut", "SelectedTau_pT_AfterJetCut", 200, 0.0, 400.0);
    hSelectedTauEtMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "SelectedTau_pT_AfterMetCut", "SelectedTau_pT_AfterMetCut", 200, 0.0, 400.0);
    hSelectedTauEtBtagging = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "SelectedTau_pT_AfterBtagging", "SelectedTau_pT_AfterBtagging", 200, 0.0, 400.0);
    hSelectedTauEtBjetVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "SelectedTau_pT_AfterBveto", "SelectedTau_pT_AfterBveto", 200, 0.0, 400.0);
    hSelectedTauEtBjetVetoPhiCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "SelectedTau_pT_AfterBvetoPhiCuts", "SelectedTau_pT_AfterBvetoPhiCuts", 200, 0.,400.0);
    hSelectedTauEtTailKiller = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "SelectedTau_pT_TailKiller", "SelectedTau_pT_TailKiller", 200, 0.0, 400.0);
    
    hSelectedTauEtDeltaPhiJet123Cut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "SelectedTau_pT_AfterDeltaPhiJet123Cut", "SelectedTau_pT_AfterDeltaPhiJet123Cut", 200,0, 400.0);
    hSelectedTauEtDeltaPhiJetsAgainstTTCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "SelectedTau_pT_AfterDeltaPhiJetsAgainstTTCut", "SelectedTau_pT_AfterDeltaPhiJetsAgainstTTCut", 200, 0.0, 400.0);
				  
          
    //    hSelectedTauEtMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_pT_AfterMetCut", "SelectedTau_pT_AfterMetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    hSelectedTauEtaMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_eta_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.1", 150, -3.0, 3.0);
    hSelectedTauPhiMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_phi_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.087", 180, -3.1415926, 3.1415926);
    hSelectedTauRtauMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "SelectedTau_Rtau_AfterMetCut", "SelectedTau_Rtau_AfterMetCut;R_{#tau};N_{events} / 0.1", 180, 0., 1.2);

   hDeltaR_TauMETJet1MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "DeltaR_TauMETJet1MET", "DeltaR_TauMETJet1MET ", 65, 0., 260.);
   hDeltaR_TauMETJet2MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "DeltaR_TauMETJet2MET", "DeltaR_TauMETJet2MET ", 65, 0., 260.);
   hDeltaR_TauMETJet3MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "DeltaR_TauMETJet3MET", "DeltaR_TauMETJet3MET ", 65, 0., 260.);
   hDeltaR_TauMETJet4MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myInverted, "DeltaR_TauMETJet4MET", "DeltaR_TauMETJet4MET ", 65, 0., 260.);

   
   /*
   // Selection flow histogram
    hSelectionFlow = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "QCD_SelectionFlow", "QCD_SelectionFlow;;N_{events}", 12, 0, 12);
    if(hSelectionFlow.isActive()) {
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
    }
   */
   
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
      producer->produces<std::vector<pat::Muon> >("selectedVetoMuonsBeforeIsolationAndPtAndEtaCuts");
      producer->produces<std::vector<pat::Muon> >("selectedVetoMuonsBeforePtAndEtaCuts");
    }
  }

 

  bool SignalAnalysisInvertedTau::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    fEventWeight.beginEvent();

    // set prescale
    const double prescaleWeight = fPrescaleWeightReader.getWeight(iEvent, iSetup);
    fEventWeight.multiplyWeight(prescaleWeight);
    fTree.setPrescaleWeight(prescaleWeight);



    // Pileup weight
    double myWeightBeforePileupReweighting = fEventWeight.getWeight();
    if(!iEvent.isRealData()) {
      const double myPileupWeight = fPileupWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(myPileupWeight);
      fTree.setPileupWeight(myPileupWeight);
    }
 

    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    size_t nVertices = pvData.getNumberOfAllVertices();
    hVerticesBeforeWeight->Fill(nVertices, myWeightBeforePileupReweighting);
    hVerticesAfterWeight->Fill(nVertices);
    fTree.setNvertices(nVertices);
    increment(fAllCounter);
    //hSelectionFlow->Fill(kQCDOrderVertexSelection);
    
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
    //hSelectionFlow->Fill(kQCDOrderTrigger);
  
    if(triggerData.hasTriggerPath()) // protection if TriggerSelection is disabled
      fTree.setHltTaus(triggerData.getTriggerTaus());

    hVerticesTriggeredBeforeWeight->Fill(nVertices, myWeightBeforePileupReweighting);
    hVerticesTriggeredAfterWeight->Fill(nVertices);

//------ GenParticle analysis (must be done here when we effectively trigger all MC)
    GenParticleAnalysis::Data genData;
    if (!iEvent.isRealData()) {
      genData = fGenparticleAnalysis.analyze(iEvent, iSetup);
      fTree.setGenMET(genData.getGenMET());
    }
   

    // Primary vertex
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    ////hSelectionFlow->Fill(kSignalOrderVertexSelection);

   
  
    // Tau-candidate selection
   
    TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
 
    if(!tauData.passedEvent()) return false; // Require at least one tau

    increment(fTauCandidateCounter);

    // tauID cuts applied to inverted and baseline taus    
    // nprongs
    //hSelectionFlow->Fill(kQCDOrderTauCandidateSelection);

  

    edm::PtrVector<pat::Tau> myOneProngTaus;
    edm::PtrVector<pat::Tau> myOneProngRtauPassedTaus;    
    for(edm::PtrVector<pat::Tau>::const_iterator iTau = tauData.getSelectedTausBeforeIsolation().begin(); iTau != tauData.getSelectedTausBeforeIsolation().end(); ++iTau) {
      if((*iTau)->signalPFChargedHadrCands().size() == 1) {
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
    
    
    std::string myTauIsolation = "byMediumCombinedIsolationDeltaBetaCorr3Hits";
    
  
  

    ////////////////////////////////////////////////////////////////////////////////////////////////
  // baseline tau-id (full tauID) and selection starts 

  
    edm::PtrVector<pat::Tau> myOneProngRtauPassedIsolatedTaus;  
     
    for(edm::PtrVector<pat::Tau>::const_iterator iTau = myOneProngRtauPassedTaus.begin(); iTau != myOneProngRtauPassedTaus.end(); ++iTau) {
      
      // tau isolation
      if ( (*iTau)->tauID(myTauIsolation) < 0.5 ) continue;
      //<<<<<<< HEAD
      //=======
	//	std::cout <<"PASSES TAU DISCR" << std::endl;
      hTauDiscriminator->Fill((*iTau)->tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits"));
      increment(fTausExistCounter);
  
	
      FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, (**iTau));
      //	FakeTauIdentifier::MCSelectedTauMatchType tauMatchData.getTauMatchType() = fFakeTauIdentifier.matchTauToMC(iEvent, (**iTau));
      //      bool myFakeTauStatus = fFakeTauIdentifier.isFakeTau(tauMatchData.getTauMatchType()); // True if the selected tau is a fake
      // Below "genuine tau" is in the context of embedding (i.e. irrespective of the tau decay)
      if((fOnlyGenuineTaus && !fFakeTauIdentifier.isEmbeddingGenuineTau(tauMatchData.getTauMatchType()))) continue;
	
      // Apply scale factor for fake tau
      if (!iEvent.isRealData())
	fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), (*iTau)->eta()));
      // plot leading track without pt cut
      increment(fTauFakeScaleFactorCounter);

      //>>>>>>> sami2011/2011
      
      hTauDiscriminator->Fill((*iTau)->tauID("byRawCombinedIsolationDeltaBetaCorr"));
      increment(fTausExistCounter);  
      
      if(fProduce) {
	std::auto_ptr<std::vector<pat::Tau> > saveTaus(new std::vector<pat::Tau>());
	copyPtrToVector(tauData.getSelectedTaus(), *saveTaus);
	iEvent.put(saveTaus, "selectedTaus");
      }

      myOneProngRtauPassedIsolatedTaus.push_back(*iTau);          
    }
   



    if ( myOneProngRtauPassedIsolatedTaus.size() > 0) {
      const edm::Ptr<pat::Tau> selectedTau = fTauSelection.selectMostLikelyTau(myOneProngRtauPassedIsolatedTaus,pvData.getSelectedVertex()->z());

      increment(fBaselineTauIDCounter);
      FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, (*selectedTau));
      if (!iEvent.isRealData())
	fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), selectedTau->eta()));
      increment(fTauFakeScaleFactorBaselineCounter);

      fVertexAssignmentAnalysis.analyze(iEvent, iSetup, iEvent.isRealData(), pvData.getSelectedVertex(), tauData.getSelectedTau(), tauMatchData.getTauMatchType());
      
      if(iEvent.isRealData())
	fTauTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
      // Apply trigger scale factor here, because it depends only on tau
      TauTriggerEfficiencyScaleFactor::Data tauTriggerWeight = fTauTriggerEfficiencyScaleFactor.applyEventWeight((*selectedTau), iEvent.isRealData(), fEventWeight);
      fTree.setTauTriggerWeight(tauTriggerWeight.getEventWeight(), tauTriggerWeight.getEventWeightAbsoluteUncertainty()); 
      increment(fTauTriggerScaleFactorBaselineCounter);

      if (myOneProngRtauPassedIsolatedTaus.size() == 1) increment(fOneTauCounter);

      // Baseline analysis
      return doBaselineAnalysis(iEvent, iSetup, selectedTau, pvData);
    }
    
    // end baseline tauid and selection
 
   ///////////////////////////////////////////////////////////////////
   
    // Inverted tau selection starts
  
    edm::PtrVector<pat::Tau> myOneProngRtauPassedInvertedTaus;    
    for(edm::PtrVector<pat::Tau>::const_iterator iTau = myOneProngRtauPassedTaus.begin(); iTau != myOneProngRtauPassedTaus.end(); ++iTau) {
      
      if ( (*iTau)->tauID(myTauIsolation) < 0.5 ){
	//	std::cout <<"Fails TAU DISCR" << std::endl;
	myOneProngRtauPassedInvertedTaus.push_back(*iTau);
      }	
    }
    
    hOneProngRtauPassedInvertedTaus->Fill(myOneProngRtauPassedInvertedTaus.size());

    if ( myOneProngRtauPassedInvertedTaus.size() >  0 ) {
      increment(fTauVetoAfterTauIDCounter); 
      const edm::Ptr<pat::Tau> selectedInvertedTau = fTauSelection.selectMostLikelyTau(myOneProngRtauPassedInvertedTaus,pvData.getSelectedVertex()->z());
      FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, (*selectedInvertedTau));
      if (!iEvent.isRealData())
	fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), selectedInvertedTau->eta()));
      increment(fTauFakeScaleFactorCounter);
      
      
      if(iEvent.isRealData())
	fTauTriggerEfficiencyScaleFactor.setRun(iEvent.id().run());
      // Apply trigger scale factor here, because it depends only on tau
      TauTriggerEfficiencyScaleFactor::Data tauTriggerWeight = fTauTriggerEfficiencyScaleFactor.applyEventWeight(*(selectedInvertedTau), iEvent.isRealData(), fEventWeight);
      fTree.setTauTriggerWeight(tauTriggerWeight.getEventWeight(), tauTriggerWeight.getEventWeightAbsoluteUncertainty());
      
      increment(fTauTriggerScaleFactorCounter);
      
      return doInvertedAnalysis(iEvent, iSetup, selectedInvertedTau, pvData, genData);
    }
     

    return true;
  }
  // end Inverted selection


  //////////////////////////////////////////////////////////////////////////////////

  bool SignalAnalysisInvertedTau::doBaselineAnalysis( const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau , const VertexSelection::Data& pvData) {
    
 
    // Global electron veto
    ElectronSelection::Data electronVetoData = fElectronSelection.analyze(iEvent, iSetup);   
    if (!electronVetoData.passedEvent()) return false; 
    increment(fBaselineEvetoCounter); 

    // Global muon veto
    MuonSelection::Data muonVetoData = fMuonSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex());    
    if (!muonVetoData.passedEvent()) return false;
    increment(fBaselineMuvetoCounter);
  
	 
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup,  selectedTau,   pvData.getNumberOfAllVertices()); 
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, selectedTau, jetData.getAllJets());
      

    hNJetBaselineTauId->Fill(jetData.getSelectedJets().size());  
    if(metData.passedEvent()) hNJetBaselineTauIdMet->Fill(jetData.getSelectedJets().size()); 

    // plot MET after tau id in bins
    hMETBaselineTauId->Fill(selectedTau->pt() ,metData.getSelectedMET()->et());
         
    
    if(!jetData.passedEvent()) return false;
	  
    increment(fBaselineJetsCounter);

    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
      
    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); 	      // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }  
    increment(fBTaggingScaleFactorCounter);
    
        
    // Met with after jets in bins
    hMETBaselineTauIdJets->Fill(selectedTau->pt() ,metData.getSelectedMET()->et());  
    hNBBaselineTauIdJet->Fill(btagData.getSelectedJets().size());

    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.analyze(iEvent, iSetup, selectedTau, jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    double transverseMass = TransverseMass::reconstruct(*(selectedTau), *(metData.getSelectedMET()) );
    double deltaPhiBaseline = DeltaPhi::reconstruct(*(selectedTau), *(metData.getSelectedMET())) * 57.3; // converted to degrees                                                      
    hMTBaselineTauIdNoMetNoBtagging->Fill(selectedTau->pt() ,transverseMass );
    if (qcdTailKillerData.passedEvent()) {
      hMTBaselineTauIdNoMetNoBtaggingTailKiller->Fill(selectedTau->pt() ,transverseMass );
    }

    if(btagData.passedEvent()) {
      // Met with b tagging in bins
      hMETBaselineTauIdBtag->Fill(selectedTau->pt() ,metData.getSelectedMET()->et());
      // mT with b veto  in bins                                                                                                                                                      
      hMTBaselineTauIdNoMetBtag->Fill(selectedTau->pt() ,transverseMass );
      if (qcdTailKillerData.passedEvent()) {
        hMTBaselineTauIdNoMetBtagTailKiller->Fill(selectedTau->pt() ,transverseMass );
      }
    }
    // Met with b veto in bins
    if( btagData.getSelectedJets().size() < 1 ) {
      hMETBaselineTauIdBveto->Fill(selectedTau->pt() ,metData.getSelectedMET()->et());
      // mT with b veto  in bins 
      hMTBaselineTauIdNoMetBveto->Fill(selectedTau->pt() ,transverseMass );
      if (qcdTailKillerData.passedEvent()) {
	hMTBaselineTauIdNoMetBvetoTailKiller->Fill(selectedTau->pt() ,transverseMass );
      }
    }
    
      
    
    if(!metData.passedEvent()) return false;
    increment(fBaselineMetCounter);
    size_t nVertices = pvData.getNumberOfAllVertices();
    fMETPhiOscillationCorrection.analyze(iEvent, iSetup, nVertices, metData);	      
   
       //------ mT after jets and met in bins
    hMTBaselineTauIdNoBtagging->Fill(selectedTau->pt() ,transverseMass );	
    if (qcdTailKillerData.passedEvent()) {   
	hMTBaselineTauIdNoBtaggingTailKiller->Fill(selectedTau->pt() ,transverseMass );	
      }
      	      
    // mT with b veto  in bins
    if( btagData.getSelectedJets().size() < 1) { 
      hMTBaselineTauIdBveto->Fill(selectedTau->pt() ,transverseMass );
     
    // mT with b veto and deltaPhi cuts  in bins 
      if (qcdTailKillerData.passedEvent()) {   
	hMTBaselineTauIdBvetoTailKiller->Fill(selectedTau->pt() ,transverseMass );	
      }
    }
    

    
    if(!btagData.passedEvent()) return false;
    increment(fBaselineBtagCounter);
      
    
    // mT with b tagging in bins
    hMTBaselineTauIdBtag->Fill(selectedTau->pt() ,transverseMass );  
      
    hDeltaPhiBaseline->Fill(deltaPhiBaseline);
		
	
    // delta phi cuts

    if (deltaPhiBaseline < fDeltaPhiCutValue ) increment(fBaselineDeltaPhiTauMETCounter);

    if (!qcdTailKillerData.passedEvent()) return false;			
	       
    increment(fBaselineDeltaPhiVSDeltaPhiMHTJet1CutCounter); 
       

  // mT with b tagging and deltaPhi cuts 
    //    hMTBaselineTauIdPhi->Fill(selectedTau->pt() ,transverseMass );
    hMTBaselineTauIdAllCutsTailKiller->Fill(selectedTau->pt() ,transverseMass );    
    return true;
  }
  

  ////////////////////////////////////////////////////////////////////////////////////

  
  
  bool SignalAnalysisInvertedTau::doInvertedAnalysis( const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau , const VertexSelection::Data& pvData, const GenParticleAnalysis::Data genData) {


    JetSelection::Data     jetData = fJetSelection.analyze(iEvent, iSetup,  selectedTau,   pvData.getNumberOfAllVertices());   
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, selectedTau, jetData.getAllJets());
    BTagging::Data btagData  = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    
    double deltaPhi = DeltaPhi::reconstruct(*(selectedTau), *(metData.getSelectedMET())) * 57.3; // converted to degrees   
    double transverseMass = TransverseMass::reconstruct(*(selectedTau), *(metData.getSelectedMET()) );

 
     
  
    //hSelectionFlow->Fill(kSignalOrderTauID);
  /*
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Tau> > saveTaus(new std::vector<pat::Tau>());
      copyPtrToVector(tauData.getSelectedTaus(), *saveTaus);
      iEvent.put(saveTaus, "selectedTaus");
    }
  */  
    hSelectedTauEtTauVeto->Fill(selectedTau->pt());
 
    //    hSelectedTauEt->Fill(selectedTau->pt());
    hSelectedTauEta->Fill(selectedTau->eta());
    hSelectedTauPhi->Fill(selectedTau->phi());

    
 
    // Obtain MC matching
    MCSelectedTauMatchType myTauMatch = matchTauToMC(iEvent, selectedTau);
 
  
    //Global electron veto
    ElectronSelection::Data electronVetoData = fElectronSelection.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);
    //hSelectionFlow->Fill(kQCDOrderElectronVeto);  

  
        
   
    /*
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Electron> > saveElectrons(new std::vector<pat::Electron>());
      //     copyPtrToVector(electronVetoData.getSelectedElectrons(), *saveElectrons);
      iEvent.put(saveElectrons, "selectedVetoElectrons");
    }
    */

    // Global muon veto
    MuonSelection::Data muonVetoData = fMuonSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);
    //hSelectionFlow->Fill(kQCDOrderMuonVeto);
    

  
    /*
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Muon> > saveMuons(new std::vector<pat::Muon>());
      //      copyPtrToVector(muonVetoData.getSelectedMuonsBeforePtAndEtaCuts(), *saveMuons);
      iEvent.put(saveMuons, "selectedVetoMuonsBeforePtAndEtaCuts");
      saveMuons.reset(new std::vector<pat::Muon>());
      //      copyPtrToVector(muonVetoData.getSelectedMuons(), *saveMuons);
      iEvent.put(saveMuons, "selectedVetoMuons");
    }
    */

   
    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.analyze(iEvent, iSetup, selectedTau, jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());	

    hMETInvertedTauId->Fill(selectedTau->pt() ,metData.getSelectedMET()->et());         
    hNJetInvertedTauId->Fill(selectedTau->pt(), jetData.getSelectedJets().size());  
    

    if(metData.passedEvent()) {
      hNJetInvertedTauIdMet->Fill(selectedTau->pt(), jetData.getSelectedJets().size());  
    }


    // Hadronic jet selection
    if(!jetData.passedEvent()) return false;
    increment(fNJetsCounter);
    //hSelectionFlow->Fill(kQCDOrderJetSelection);
    hSelectedTauEtJetCut->Fill(selectedTau->pt());
   
 /*
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveJets(new std::vector<pat::Jet>());
      copyPtrToVector(jetData.getSelectedJets(), *saveJets);
      iEvent.put(saveJets, "selectedJets");
    }
    */   
    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); //    Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }   
    increment(fBTaggingScaleFactorInvertedCounter);

    // inverted MET before b tagging and MT before b tagging and Met
    hMETInvertedTauIdJets->Fill(selectedTau->pt(), metData.getSelectedMET()->et());
    hMTInvertedTauIdJet->Fill(selectedTau->pt(), transverseMass); 
    if (qcdTailKillerData.passedEvent()) {       
      hMTInvertedTauIdJetTailKiller->Fill(selectedTau->pt(), transverseMass);  
    }

															      
    // MET with b tagging
    if(btagData.passedEvent()) {
      hMETInvertedTauIdBtag->Fill(selectedTau->pt(), metData.getSelectedMET()->et());
      hMTInvertedTauIdBtagNoMetCut->Fill(selectedTau->pt(), transverseMass); 
      increment(fBTaggingBeforeMETCounter);
      if (qcdTailKillerData.passedEvent()) {
        hMTInvertedTauIdBtagNoMetCutTailKiller->Fill(selectedTau->pt(), transverseMass);
      }

    }
    // MET with b veto 
    if( btagData.getSelectedJets().size() < 1) {
      increment(fBjetVetoCounter);
      hMETInvertedTauIdBveto->Fill(selectedTau->pt(), metData.getSelectedMET()->et()); 	
      hMTInvertedTauIdBvetoNoMetCut->Fill(selectedTau->pt(), transverseMass);
      if (qcdTailKillerData.passedEvent()) {   	
	hMTInvertedTauIdBvetoNoMetCutTailKiller->Fill(selectedTau->pt(), transverseMass);
      }															
    }
  
 
    if(metData.passedEvent()) hDeltaPhiAfterJets->Fill(deltaPhi);   
     

    // MET cut
    if(!metData.passedEvent()) return false;
    increment(fMETCounter);
    size_t nVertices = pvData.getNumberOfAllVertices();
    fMETPhiOscillationCorrection.analyze(iEvent, iSetup, nVertices, metData);

    //hSelectionFlow->Fill(kQCDOrderMET);
    hSelectedTauEtMetCut->Fill(selectedTau->pt());
    hSelectedTauEtaMetCut->Fill(selectedTau->eta());
    hSelectedTauPhiMetCut->Fill(selectedTau->phi());  
 


  // Nbjets for inverted tau before b tagging

    hNBInvertedTauIdJet->Fill(selectedTau->pt(), btagData.getSelectedJets().size()); 
 

   // mt for inverted tau before b tagging
    hMTInvertedTauIdNoBtagging->Fill(selectedTau->pt(), transverseMass); 

   // deltaPhi before b tagging  
    hDeltaPhiInvertedNoB->Fill(selectedTau->pt(),deltaPhi);  

    if (qcdTailKillerData.passedEvent()) {       
      // mt  before b tagging with deltaPhi for factorising b tagging 
      hMTInvertedNoBtaggingTailKiller->Fill(selectedTau->pt(), transverseMass);       
      hNBInvertedTauIdJetDphi->Fill(selectedTau->pt(), btagData.getSelectedJets().size()); 
    }


  // mt  with b veto
    if( btagData.getSelectedJets().size() < 1) { 
      increment(fBvetoCounter); 
  
      hMTInvertedTauIdBveto->Fill(selectedTau->pt(), transverseMass);
      hSelectedTauEtBjetVeto->Fill(selectedTau->pt());

  // mt  with b veto and deltaPhi
      if (qcdTailKillerData.passedEvent()) {         
      //    if ( deltaPhiMetJet1 > Rcut && deltaPhiMetJet2 > Rcut && deltaPhiMetJet3 > Rcut  ) {
	increment(fBvetoDeltaPhiCounter); 
	hMTInvertedTauIdBvetoDphi->Fill(selectedTau->pt(),transverseMass);
        hSelectedTauEtBjetVetoPhiCuts->Fill(selectedTau->pt());
	
      }
    }
  
    // b tagging cut
    //    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderBTagSelection, tauData, btagData.passedEvent(),btagData.getMaxDiscriminatorValue());
    if(!btagData.passedEvent()) return false;
    // Apply scale factor as weight to event 
    increment(fBTaggingCounter);		
    //hSelectionFlow->Fill(kQCDOrderBTag);

    hSelectedTauEtBtagging->Fill(selectedTau->pt());
   
    /*
    if(fProduce) {
      std::auto_ptr<std::vector<pat::Jet> > saveBJets(new std::vector<pat::Jet>());
      copyPtrToVector(btagData.getSelectedJets(), *saveBJets);
      iEvent.put(saveBJets, "selectedBJets");
    }
    */

   // mt for inverted tau with b tagging



    
    hMTInvertedTauIdBtag->Fill(selectedTau->pt(), transverseMass);
   // deltaPhi with b tagging
    hDeltaPhiInverted->Fill(selectedTau->pt(),deltaPhi);  
    hTransverseMassVsDphi->Fill(transverseMass,deltaPhi);

    // mT with deltaPhi(tau,met)
    if (deltaPhi < fDeltaPhiCutValue) {
      hMTInvertedTauIdJetDphi->Fill(selectedTau->pt(),transverseMass);        
      increment(fDeltaPhiTauMETCounter);  
    }

    // tail killer cuts
    if (!qcdTailKillerData.passedEvent()) return false;
    increment(fQCDTailKillerCounter); 
    
    //    increment(fDeltaPhiVSDeltaPhiMETJet1CutCounter);
    hMTInvertedAllCutsTailKiller->Fill(selectedTau->pt(), transverseMass);     
    hMETInvertedAllCutsTailKiller->Fill(selectedTau->pt(), metData.getSelectedMET()->et());
 	       
    //    increment(fDeltaPhiVSDeltaPhiMETJet2CutCounter);
    hSelectedTauEtTailKiller->Fill(selectedTau->pt());
      
    //    increment(fDeltaPhiVSDeltaPhiMETJet3CutCounter);
    //    increment(fDeltaPhiVSDeltaPhiMETJet4CutCounter);
    hTransverseMass->Fill(transverseMass); 
    //    increment(fDeltaPhiAgainstTTCutCounter);   
   
    
    FullHiggsMassCalculator::Data FullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, selectedTau, btagData,
										       metData, &genData);
    double HiggsMass = FullHiggsMassData.getHiggsMass();
    if (HiggsMass > 100 && HiggsMass < 200 ) increment(fHiggsMassCutCounter);
    hHiggsMass->Fill(selectedTau->pt(), HiggsMass); 
   
  
       
    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), selectedTau, metData.getSelectedMET());
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
 
    // top mass with binning    
    double topMass = TopChiSelectionData.getTopMass();    
    hTopMass->Fill(selectedTau->pt(), topMass);
 
 

    hSelectedTauEtAfterCuts->Fill(selectedTau->pt());
    hSelectedTauEtaAfterCuts->Fill(selectedTau->eta());
 
   
    if (TopChiSelectionData.passedEvent() ) {
         increment(fTopChiSelectionCounter);     
	 hTransverseMassTopChiSelection->Fill(transverseMass);     
    } 

    if (BjetSelectionData.passedEvent() ) {
        
      TopWithBSelection::Data TopWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());

      if (TopWithBSelectionData.passedEvent() ) {
	increment(fTopWithBSelectionCounter);
	//      //hSelectionFlow->Fill(kSignalOrderTopSelection);      
	hTransverseMassTopBjetSelection->Fill(transverseMass);     
      }    
    }


   // top mass with possible event cuts
    if (TopSelectionData.passedEvent() ) {
      increment(fTopSelectionCounter);      
      hTransverseMassWithTopCut->Fill(transverseMass);
      if(transverseMass > 80 ) increment(ftransverseMassCut100TopCounter);   
    } 



 
    if(transverseMass < 80 ) return false;
    increment(ftransverseMassCut80Counter);

    if(transverseMass < 100 ) return false;
    increment(ftransverseMassCut100Counter);


    //    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderFakeMETVeto, tauData);   
    //    fillNonQCDTypeIICounters(myTauMatch, kSignalOrderTopSelection, tauData);

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
