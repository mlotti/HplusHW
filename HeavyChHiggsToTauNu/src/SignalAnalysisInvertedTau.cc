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
  SignalAnalysisInvertedTau::SignalAnalysisInvertedTau(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper):
    fEventWeight(eventWeight),
    fHistoWrapper(histoWrapper),
    bBlindAnalysisStatus(iConfig.getUntrackedParameter<bool>("blindAnalysisStatus")),
    fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    // Common counters
    fAllCounter(eventCounter.addCounter("All events")),
    fWJetsWeightCounter(eventCounter.addCounter("WJets inc+exl weight")),
    fMETFiltersCounter(eventCounter.addCounter("MET filters")),
    fTriggerCounter(eventCounter.addCounter("Trigger and HLT_MET cut")),  
    fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
    fVertexFilterCounter(eventCounter.addCounter("Vertex number filter")),
    fTauCandidateCounter(eventCounter.addCounter("Tau candidates found")),
    fNprongsAfterTauIDCounter(eventCounter.addCounter("Nprongs cut, all tau candidates")),
    fRtauAfterTauIDCounter(eventCounter.addCounter("Rtau cut, all tau candidates")),
    // Baseline counters
    fBaselineTauIDCounter(eventCounter.addCounter("Baseline: at least one tau")),
    fBaselineTauFakeScaleFactorCounter(eventCounter.addCounter("Baseline:tau fake scale factor, all passed taus")),
    fBaselineTauTriggerScaleFactorCounter(eventCounter.addCounter("Baseline:tau trig scale factor, all passed taus")),  
    fBaselineOneTauCounter(eventCounter.addCounter("Baseline: one tau candidate only")),
    fBaselineEvetoCounter(eventCounter.addCounter("Baseline: electron veto")),
    fBaselineMuvetoCounter(eventCounter.addCounter("Baseline: muon veto")),
    fBaselineJetsCounter(eventCounter.addCounter("Baseline: njets")),
    fBaselineMetTriggerScaleFactorCounter(eventCounter.addCounter("Baseline: MET SF")),
    fBaselineQCDTailKillerCollinearCounter(eventCounter.addCounter("Baseline: QCD tail killer collinear")),
    fBaselineMetCounter(eventCounter.addCounter("Baseline: MET")),
    fBaselineBtagCounter(eventCounter.addCounter("Baseline: btagging")),
    fBaselineBTaggingScaleFactorCounter(eventCounter.addCounter("Baseline: btagging scale factor")),
    fBaselineQCDTailKillerBackToBackCounter(eventCounter.addCounter("Baseline: QCD tail killer back-to-back")),
    fBaselineDeltaPhiTauMETCounter(eventCounter.addCounter("Baseline: -> DeltaPhi(Tau,MET) upper limit")),
    fBaselineSelectedEventsCounter(eventCounter.addCounter("Baseline: Selected events")),
    fBaselineSelectedEventsInvariantMassCounter(eventCounter.addCounter("Baseline: Selected events invariant mass")),
    // Inverted counters
    fInvertedTauIDCounter(eventCounter.addCounter("Inverted: Taus found")),
    fInvertedTauFakeScaleFactorCounter(eventCounter.addCounter("Inverted: tau fake scale factor, all cands")),
    fInvertedTauTriggerScaleFactorCounter(eventCounter.addCounter("Inverted: tau trigger scale factor, all cands")),
    fInvertedOneTauCounter(eventCounter.addCounter("Inverted: one tau candidate only")),
    fInvertedElectronVetoCounter(eventCounter.addCounter("Inverted: electron veto")),
    fInvertedMuonVetoCounter(eventCounter.addCounter("Inverted: muon veto")),
    fInvertedNJetsCounter(eventCounter.addCounter("Inverted: njets")),
    fInvertedMetTriggerScaleFactorCounter(eventCounter.addCounter("Inverted: MET SF")),
    fInvertedQCDTailKillerCollinearCounter(eventCounter.addCounter("Inverted: QCD tail killer collinear")),
    fInvertedBTaggingBeforeMETCounter(eventCounter.addCounter("Inverted: btagging before MET")),
    fInvertedBjetVetoCounter(eventCounter.addCounter("Inverted: -> Veto on b jets before MET")),
    fInvertedMetCounter(eventCounter.addCounter("Inverted: MET")),
    fInvertedBvetoCounter(eventCounter.addCounter("Inverted: -> Veto on b jets after MET")),
    fInvertedBvetoDeltaPhiCounter(eventCounter.addCounter("Inverted: -> Veto on b jets after MET and Dphi")),
    fInvertedBTaggingCounter(eventCounter.addCounter("Inverted: btagging")),
    fInvertedBTaggingScaleFactorCounter(eventCounter.addCounter("Inverted: btagging scale factor")),
    fInvertedQCDTailKillerBackToBackCounter(eventCounter.addCounter("Inverted: QCD tail killer back-to-back")),
    fInvertedDeltaPhiTauMETCounter(eventCounter.addCounter("Inverted: -> DeltaPhi(Tau,MET) upper limit")),
    fInvertedSelectedEventsCounter(eventCounter.addCounter("Inverted: Selected events")),
    fInvertedSelectedEventsInvariantMassCounter(eventCounter.addCounter("Inverted: Selected events invariant mass")),
    // Other counters
//     fDeltaPhiVSDeltaPhiMETJet1CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet1,MET) vs DeltaPhi cut")),
//     fDeltaPhiVSDeltaPhiMETJet2CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet2,MET) vs DeltaPhi cut")),
//     fDeltaPhiVSDeltaPhiMETJet3CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet3,MET) vs DeltaPhi cut")),
//     fDeltaPhiVSDeltaPhiMETJet4CutCounter(eventCounter.addCounter("Inverted:DeltaPhi(Jet4,MET) vs DeltaPhi cut")), 
//     fHiggsMassCutCounter(eventCounter.addCounter("Inverted: HiggsMassCut")),
    ftransverseMassCut80Counter(eventCounter.addCounter("Inverted: -> transverseMass > 80")),
    ftransverseMassCut100Counter(eventCounter.addCounter("Inverted: -> transverseMass > 100")),
    fTopSelectionCounter(eventCounter.addCounter("Inverted: -> Top Selection cut")),
    fTopChiSelectionCounter(eventCounter.addCounter("Inverted: -> Top ChiSelection cut")),
    fTopWithBSelectionCounter(eventCounter.addCounter("Inverted: -> Top with B Selection cut")),
    ftransverseMassCut100TopCounter(eventCounter.addCounter("Inverted: -> transverseMass > 100 top cut")),

    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
    fElectronSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("ElectronSelection"), fPrimaryVertexSelection.getSelectedSrc(), eventCounter, fHistoWrapper),
    fMuonSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MuonSelection"), eventCounter, fHistoWrapper),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, fHistoWrapper),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, fHistoWrapper, "MET", fTauSelection.getIsolationDiscriminator()),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, fHistoWrapper),
    fFakeMETVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeMETVeto"), eventCounter, fHistoWrapper),
    fJetTauInvMass(iConfig.getUntrackedParameter<edm::ParameterSet>("jetTauInvMass"), eventCounter, fHistoWrapper),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, fHistoWrapper),
    fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, fHistoWrapper),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, fHistoWrapper),
    fFullHiggsMassCalculator(iConfig.getUntrackedParameter<edm::ParameterSet>("invMassReco"), eventCounter, fHistoWrapper),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, fHistoWrapper),
    fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, fHistoWrapper),
    fCorrelationAnalysis(eventCounter, fHistoWrapper, "HistoName"),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, fHistoWrapper),
    fTauTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("tauTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fMETTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("metTriggerEfficiencyScaleFactor"), fHistoWrapper),
    fPrescaleWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("prescaleWeightReader"), fHistoWrapper, "PrescaleWeight"),
    fPileupWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("pileupWeightReader"), fHistoWrapper, "PileupWeight"),
    fMETFilters(iConfig.getUntrackedParameter<edm::ParameterSet>("metFilters"), eventCounter),
    fQCDTailKiller(iConfig.getUntrackedParameter<edm::ParameterSet>("QCDTailKiller"), eventCounter, fHistoWrapper),
    fWJetsWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("wjetsWeightReader"), fHistoWrapper, "WjetsWeight"),
    fFakeTauIdentifier(iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"), fHistoWrapper, "TauID"),
    // Common plots
    fCommonPlots(iConfig.getUntrackedParameter<edm::ParameterSet>("commonPlotsSettings"), eventCounter, fHistoWrapper, CommonPlots::kQCDInverted),
    fProduce(iConfig.getUntrackedParameter<bool>("produceCollections", false)),
    fOnlyGenuineTaus(iConfig.getUntrackedParameter<bool>("onlyGenuineTaus", false))
  {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());
 
    TFileDirectory myInverted = fs->mkdir("Inverted");
    TFileDirectory myBaseline = fs->mkdir("BaseLine");
    // Book histograms filled in the analysis body
    hOneProngRtauPassedInvertedTaus= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "OneProngRtauPassedInvertedTaus", "OneProngRtauPassedInvertedTaus", 10, 0, 10);

    hVerticesBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "verticesBeforeWeight", "Number of vertices without weighting", 60, 0, 60);
    hVerticesAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "verticesAfterWeight", "Number of vertices with weighting", 60, 0, 60);
    hTransverseMassWithTopCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassWithTopCut", "transverseMassWithTopCut;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassTopChiSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassTopChiSelection", "transverseMassTopChiSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassTopBjetSelection = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kDebug, *fs, "transverseMassTopBjetSelection", "transverseMassTopBjetSelection;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 80, 0., 400.);
    hTransverseMassVsDphi = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, *fs, "transverseMassVsDphi", "transverseMassVsDphi;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.,180,0.,180.);
    hSelectedTauEt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedTau_pT_AfterTauID", "SelectedTau_pT_AfterTauID;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);    
    hSelectedTauEta = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedTau_eta_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.1", 150, -3.0, 3.0);   
    hSelectedTauEtAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedInvertedTauAfterCuts", "SelectedInvertedTauAfterCuts", 100, 0.0, 400.0);
    hSelectedTauEtaAfterCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedInvertedTau_eta_AfterCuts", "SelectedInvertedTau_eta_AfterCuts", 60, -3.0, 3.0);
    hSelectedTauPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedTau_phi_AfterTauID", "SelectedTau_eta_AfterTauID;#tau #eta;N_{events} / 0.087", 180, -3.1415926, 3.1415926);
    hSelectedTauRtau = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedTau_Rtau_AfterTauID", "SelectedTau_Rtau_AfterTauID;R_{#tau};N_{events} / 0.1", 240, 0., 1.2);
    hSelectedTauLeadingTrackPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedTau_TauLeadingTrackPt", "SelectedTau_TauLeadingTrackPt;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    // baseline MET histos
    hMETBaselineTauIdJetsCollinear =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MET_BaseLineTauIdJetsCollinear", 250, 0.0 , 500.0 );
    hMETBaselineTauIdBvetoCollinear = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MET_BaseLineTauIdBvetoCollinear", 250, 0.0 , 500.0 );
    hMETBaselineTauIdBtagCollinear = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MET_BaseLineTauIdBtagCollinear", 250, 0.0 , 500.0 );
    hMETBaselineTauIdJets = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MET_BaselineTauIdJets", 250, 0.0 , 500.0 );
    hMETBaselineTauIdBveto = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MET_BaselineTauIdBveto", 250, 0.0 , 500.0 );
    hMETBaselineTauIdBtag = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MET_BaselineTauIdBtag", 250, 0.0 , 500.0 );

    // baseline MT histos
    hMTBaselineTauIdSoftBtaggingTK= new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdSoftBtaggingTK", 200, 0.0, 400.0 );
    hMTBaselineTauIdBtag =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdBtag", 200, 0.0, 400.0 );
    hMTBaselineTauIdBveto =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdBveto", 200, 0.0, 400.0 );
    hMTBaselineTauIdBvetoTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdBvetoTailKiller", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoMetBveto =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdNoMetBveto", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoMetBvetoTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdNoMetBvetoTailKiller", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoBtagging = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdNoBtagging", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoBtaggingTailKiller= new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdNoBtaggingTailKiller", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoMetBtag =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdNoMetBtag", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoMetBtagTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdNoMetBtagTailKiller", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoMetNoBtagging=  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdNoMetBtagging", 200, 0.0, 400.0 );
    hMTBaselineTauIdNoMetNoBtaggingTailKiller=  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdNoMetBtaggingTailKiller", 200, 0.0, 400.0 );
    hMTBaselineTauIdAllCutsTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "BaseLine","MTBaseLineTauIdAllCutsTailKiller", 200, 0.0, 400.0 ); 
    // inverted MET histos
    hMETInvertedTauIdJets = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MET_InvertedTauIdJets", 250, 0.0 , 500.0 );  
    hMETInvertedTauIdJetsCollinear = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MET_InvertedTauIdJetsCollinear", 250, 0.0 , 500.0 );
    hMETInvertedTauIdBtag = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MET_InvertedTauIdBtag", 250, 0.0 , 500.0 );
    hMETInvertedTauIdBvetoCollinear = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MET_InvertedTauIdBvetoCollinear", 250, 0.0 , 500.0 );
    hMETInvertedTauIdBveto = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MET_InvertedTauIdBveto", 250, 0.0 , 500.0 );
    hMETInvertedAllCutsTailKiller = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MET_InvertedAllCutsTailKiller", 250, 0.0 , 500.0 );
    // inverted MT histos
    hMTInvertedTauIdSoftBtaggingTK=  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdSoftBtaggingTK", 200, 0.0, 400.0 );
    hMTInvertedTauIdBtagNoMetCut =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBtagNoMetCut", 200, 0.0, 400.0 );
    hMTInvertedTauIdBvetoNoMetCut =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBvetoNoMetCut", 200, 0.0, 400.0 );
    hMTInvertedTauIdBvetoNoMetCutTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBvetoNoMetCutTailKiller", 200, 0.0, 400.0 );
    hMTInvertedTauIdJet =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdJet", 200, 0.0, 400.0 );
    hMTInvertedTauIdJetTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdJetTailKiller", 200, 0.0, 400.0 );
    hMTInvertedNoBtaggingTailKiller = new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedNoBtaggingTailKiller", 200, 0.0, 400.0 );
    hMTInvertedTauIdNoBtagging=  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdNoBtagging", 200, 0.0, 400.0 );
    hMTInvertedTauIdBveto =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBveto", 200, 0.0, 400.0 ); 
    hMTInvertedTauIdBtag =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBtag", 200, 0.0, 400.0 ); 
    hMTInvertedTauIdBvetoDphi =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdBvetoTailKiller", 200, 0.0, 400.0 );
    hMTInvertedTauIdJetDphi =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedTauIdJetDphi", 200, 0.0, 400.0 ); 
    hMTInvertedAllCutsTailKiller =  new HistogramsInBins(HistoWrapper::kVital, eventCounter, fHistoWrapper, "Inverted","MTInvertedAllCutsTailKiller", 200, 0.0, 400.0 );
    
    hTopMass =  new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","TopMass", 200, 0.0, 400.0 );
    //    hHiggsMassTailKiller =  new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","HiggsMassTailKiller", 250, 0.0 , 500.0 );

    hNBInvertedTauIdJet =  new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","NBInvertedTauIdJet", 10, 0.0 , 10.0 );
    hNBInvertedTauIdJetDphi =  new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","NBInvertedTauIdJetDphi", 10, 0.0 , 10.0 );
    //hNJetInvertedTauId =  new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","NJetInvertedTauId", 10, 0.0 , 10.0 );
    //hNJetInvertedTauIdMet =  new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","NJetInvertedTauIdMet", 10, 0.0 , 10.0 );
    hDeltaPhiInverted =   new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","DeltaPhiInverted", 180, 0., 180.);
    hDeltaPhiInvertedNoB =   new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","DeltaPhiInvertedNoB", 180, 0., 180.);

    //     hQCDTailKillerJet0BackToBackInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInverted ,"QCDTailKillerJet0BackToBackInverted","QCDTailKillerJet0BackToBackInverted", 52, 0., 260.);
    //     hQCDTailKillerJet0BackToBackBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaseline ,"QCDTailKillerJet0BackToBackBaseline","QCDTailKillerJet0BackToBackBaseline", 52, 0., 260.);  
    //     hQCDTailKillerJet0CollinearInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInverted ,"QCDTailKillerJet0CollinearInverted","QCDTailKillerJet0CollinearInverted", 52, 0., 260.);
    //     hQCDTailKillerJet0CollinearBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaseline ,"QCDTailKillerJet0CollinearBaseline","QCDTailKillerJet0CollinearBaseline", 52, 0., 260.); 
    //     hQCDTailKillerJet1BackToBackInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInverted ,"QCDTailKillerJet1BackToBackInverted","QCDTailKillerJet1BackToBackInverted", 52, 0., 260.);
    //     hQCDTailKillerJet1BackToBackBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaseline ,"QCDTailKillerJet1BackToBackBaseline","QCDTailKillerJet1BackToBackBaseline", 52, 0., 260.);  
    //     hQCDTailKillerJet1CollinearInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInverted ,"QCDTailKillerJet1CollinearInverted","QCDTailKillerJet1CollinearInverted", 52, 0., 260.);
    //     hQCDTailKillerJet1CollinearBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaseline ,"QCDTailKillerJet1CollinearBaseline","QCDTailKillerJet1CollinearBaseline", 52, 0., 260.); 
    //     hQCDTailKillerJet2BackToBackInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInverted ,"QCDTailKillerJet2BackToBackInverted","QCDTailKillerJet2BackToBackInverted", 52, 0., 260.);
    //     hQCDTailKillerJet2BackToBackBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaseline ,"QCDTailKillerJet2BackToBackBaseline","QCDTailKillerJet2BackToBackBaseline", 52, 0., 260.);  
    //     hQCDTailKillerJet2CollinearInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInverted ,"QCDTailKillerJet2CollinearInverted","QCDTailKillerJet2CollinearInverted", 52, 0., 260.);
    //     hQCDTailKillerJet2CollinearBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaseline ,"QCDTailKillerJet2CollinearBaseline","QCDTailKillerJet2CollinearBaseline", 52, 0., 260.); 
    //     hQCDTailKillerJet3BackToBackInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInverted ,"QCDTailKillerJet3BackToBackInverted","QCDTailKillerJet3BackToBackInverted", 52, 0., 260.);
    //     hQCDTailKillerJet3BackToBackBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaseline ,"QCDTailKillerJet3BackToBackBaseline","QCDTailKillerJet3BackToBackBaseline", 52, 0., 260.);  
    //     hQCDTailKillerJet3CollinearInverted = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myInverted ,"QCDTailKillerJet3CollinearInverted","QCDTailKillerJet3CollinearInverted", 52, 0., 260.);
    //     hQCDTailKillerJet3CollinearBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative,myBaseline ,"QCDTailKillerJet3CollinearBaseline","QCDTailKillerJet3CollinearBaseline", 52, 0., 260.); 

    hNBBaselineTauIdJet = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBaseline, "NBBaselineTauIdJet", "NBBaselineTauIdJet", 10, 0., 10.);
    //hNJetBaselineTauIdMet= fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBaseline, "NJetBaselineTauIdJetMet", "NJetBaselineTauIdJetMet", 10, 0., 10.);
    //hNJetBaselineTauId = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBaseline, "NJetBaselineTauIdJet", "NJetBaselineTauIdJet", 20, 0., 20.);
    hDeltaPhiBaseline = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myBaseline , "deltaPhiBaseline", "deltaPhi;#Delta#phi", 180, 0., 180.);


    hSelectedTauEtTauVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "SelectedTau_pT_AfterTauVeto", "SelectedTau_pT_AfterTauVeto", 200, 0.0, 400.0);     
    hSelectedTauEtJetCut = new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","SelectedTau_pT_AfterJetCut", 200, 0.0 , 400.0 );
    // hSelectedTauEtJetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "SelectedTau_pT_AfterJetCut", "SelectedTau_pT_AfterJetCut", 200, 0.0, 400.0);
    //hSelectedTauEtCollinearTailKiller = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "SelectedTau_pT_CollinearTailKiller", "SelectedTau_pT_CollinearTailKiller", 200, 0.0, 400.0);
    hSelectedTauEtCollinearTailKiller  = new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","SelectedTau_pT_CollinearTailKiller", 200, 0.0 , 400.0 );
    hSelectedTauEtMetCut  = new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","SelectedTau_pT_AfterMetCut", 200, 0.0 , 400.0);
    //hSelectedTauEtMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "SelectedTau_pT_AfterMetCut", "SelectedTau_pT_AfterMetCut", 200, 0.0, 400.0);
    hSelectedTauEtBtagging  = new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","SelectedTau_pT_AfterBtagging", 200, 0.0 , 400.0);
 
    //hSelectedTauEtBtagging = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "SelectedTau_pT_AfterBtagging", "SelectedTau_pT_AfterBtagging", 200, 0.0, 400.0);
    hSelectedTauEtBjetVeto = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "SelectedTau_pT_AfterBveto", "SelectedTau_pT_AfterBveto", 200, 0.0, 400.0);
    hSelectedTauEtBjetVetoPhiCuts = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "SelectedTau_pT_AfterBvetoPhiCuts", "SelectedTau_pT_AfterBvetoPhiCuts", 200, 0.,400.0);
    // hSelectedTauEtBackToBackTailKiller = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "SelectedTau_pT_BackToBackTailKiller", "SelectedTau_pT_BackToBackTailKiller", 200, 0.0, 400.0);
    hSelectedTauEtBackToBackTailKiller   = new HistogramsInBins(HistoWrapper::kInformative, eventCounter, fHistoWrapper, "Inverted","SelectedTau_pT_BackToBackTailKiller", 200, 0.0 , 400.0);
          
    //    hSelectedTauEtMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedTau_pT_AfterMetCut", "SelectedTau_pT_AfterMetCut;#tau p_{T}, GeV/c;N_{events} / 10 GeV/c", 200, 0.0, 400.0);
    hSelectedTauEtaMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedTau_eta_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.1", 150, -3.0, 3.0);
    hSelectedTauPhiMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedTau_phi_AfterMetCut", "SelectedTau_eta_AfterMetCut;#tau #eta;N_{events} / 0.087", 180, -3.1415926, 3.1415926);
    hSelectedTauRtauMetCut = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "SelectedTau_Rtau_AfterMetCut", "SelectedTau_Rtau_AfterMetCut;R_{#tau};N_{events} / 0.1", 180, 0., 1.2);

    hDeltaR_TauMETJet1MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "DeltaR_TauMETJet1MET", "DeltaR_TauMETJet1MET ", 65, 0., 260.);
    hDeltaR_TauMETJet2MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "DeltaR_TauMETJet2MET", "DeltaR_TauMETJet2MET ", 65, 0., 260.);
    hDeltaR_TauMETJet3MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "DeltaR_TauMETJet3MET", "DeltaR_TauMETJet3MET ", 65, 0., 260.);
    hDeltaR_TauMETJet4MET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myInverted, "DeltaR_TauMETJet4MET", "DeltaR_TauMETJet4MET ", 65, 0., 260.);

    fCommonPlots.disableCommonPlotsFilledAtEveryStep();
  }

  SignalAnalysisInvertedTau::~SignalAnalysisInvertedTau() { }

  void SignalAnalysisInvertedTau::produces(edm::EDFilter *producer) const {

  }

  bool SignalAnalysisInvertedTau::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    fEventWeight.beginEvent();

//------ Set prescale
    const double prescaleWeight = fPrescaleWeightReader.getWeight(iEvent, iSetup);
    fEventWeight.multiplyWeight(prescaleWeight);

//------ Pileup weight
    double myWeightBeforePileupReweighting = fEventWeight.getWeight();
    if(!iEvent.isRealData()) {
      const double myPileupWeight = fPileupWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(myPileupWeight);
    }
    increment(fAllCounter);

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
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);
    //hSelectionFlow->Fill(kQCDOrderTrigger);

//------ GenParticle analysis (must be done here when we effectively trigger all MC)
    GenParticleAnalysis::Data genData;
    if (!iEvent.isRealData()) {
      genData = fGenparticleAnalysis.analyze(iEvent, iSetup);
    }

//------ Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    size_t nVertices = pvData.getNumberOfAllVertices();
    //hSelectionFlow->Fill(kSignalOrderVertexSelection);
    hVerticesBeforeWeight->Fill(nVertices, myWeightBeforePileupReweighting);
    hVerticesAfterWeight->Fill(nVertices);
    //hSelectionFlow->Fill(kQCDOrderVertexSelection);

    // test for pile-up dependence
    //    if (nVertices > 12 )  return false;
    //    if (nVertices < 13 || nVertices > 18 )  return false;
    //    if (nVertices < 19 )  return false;
    increment(fVertexFilterCounter);

    // Setup common plots
    fCommonPlots.initialize(iEvent, iSetup, pvData, fTauSelection, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETSelection, fBTagging, fQCDTailKiller, fTopChiSelection, fEvtTopology, fFullHiggsMassCalculator);
    fCommonPlots.fillControlPlotsAfterVertexSelection(iEvent, pvData);

//------ Tau candidate selection
    // Do tau-candidate selection
    TauSelection::Data tauCandidateDataTmp = fTauSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex()->z());
    if(!tauCandidateDataTmp.passedEvent()) return false; // Require at least one tau
    increment(fTauCandidateCounter);
    edm::PtrVector<pat::Tau> mySelectedTauList = tauCandidateDataTmp.getSelectedTausBeforeIsolation();
    // Apply nprongs cut
    edm::PtrVector<pat::Tau> myTmpVector;
    for (edm::PtrVector<pat::Tau>::iterator iTau = mySelectedTauList.begin(); iTau != mySelectedTauList.end(); ++iTau) {
      if (fTauSelection.getPassesNProngsStatusOfTauObject(*iTau))
        myTmpVector.push_back(*iTau);
    }
    mySelectedTauList = myTmpVector;
    myTmpVector.clear();
    if (!mySelectedTauList.size()) return false; // Require at least one tau passed nprongs cut
    increment(fNprongsAfterTauIDCounter);
    // Apply Rtau cut
    for (edm::PtrVector<pat::Tau>::iterator iTau = mySelectedTauList.begin(); iTau != mySelectedTauList.end(); ++iTau) {
      if (fTauSelection.getPassesRtauStatusOfTauObject(*iTau))
        myTmpVector.push_back(*iTau);
    }
    mySelectedTauList = myTmpVector;
    myTmpVector.clear();
    if (!mySelectedTauList.size()) return false; // Require at least one tau passed rtau cut
    increment(fRtauAfterTauIDCounter);
    // Dirty hack to make code crash if tauCandidateDataTmp.getSelectedTau() is called (i.e. don't use tauCandidateDataTmp beyond this line)
    const_cast<TauSelection::Data*>(&tauCandidateDataTmp)->invalidate();

//------ Select most likely tau candidate for baseline analysis (full tau ID)
    // Construct list of taus which pass isolation
    for (edm::PtrVector<pat::Tau>::iterator iTau = mySelectedTauList.begin(); iTau != mySelectedTauList.end(); ++iTau) {
      if (fTauSelection.getPassesIsolationStatusOfTauObject(*iTau))
        myTmpVector.push_back(*iTau);
    }
    TauSelection::Data tauDataForBaseline;
    bool myMultipleTausPassForBaselineStatus = false;
    if (!myTmpVector.size()) {
      // No tau candidates pass isolation, construct data object
      edm::Ptr<pat::Tau> myZeroPointer;
      tauDataForBaseline = fTauSelection.setSelectedTau(myZeroPointer, false);
    } else {
      // One or more tau candidates pass isolation, construct data object
      edm::Ptr<pat::Tau> mySelectedTau = fTauSelection.selectMostLikelyTau(myTmpVector, pvData.getSelectedVertex()->z());
      tauDataForBaseline = fTauSelection.setSelectedTau(mySelectedTau, true);
      myMultipleTausPassForBaselineStatus = myTmpVector.size() != 1;
    }
    myTmpVector.clear();

//------ Select most likely tau candidate for inverted analysis (full tau ID)
    for (edm::PtrVector<pat::Tau>::iterator iTau = mySelectedTauList.begin(); iTau != mySelectedTauList.end(); ++iTau) {
      if (!fTauSelection.getPassesIsolationStatusOfTauObject(*iTau))
        myTmpVector.push_back(*iTau);
    }
    TauSelection::Data tauDataForInverted;
    bool myMultipleTausPassForInvertedStatus = false;
    if (!myTmpVector.size() || myTmpVector.size() != mySelectedTauList.size()) {
      // No tau candidates or a tau candidate passes isolation (i.e. fails inversion), construct data object
      edm::Ptr<pat::Tau> myZeroPointer;
      tauDataForInverted = fTauSelection.setSelectedTau(myZeroPointer, false);
    } else {
      // All tau candidates are non-isolated, construct data object
      edm::Ptr<pat::Tau> mySelectedTau = fTauSelection.selectMostLikelyTau(myTmpVector, pvData.getSelectedVertex()->z());
      tauDataForInverted = fTauSelection.setSelectedTau(mySelectedTau, true);
      myMultipleTausPassForInvertedStatus = myTmpVector.size() != 1;
    }
    myTmpVector.clear();

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // baseline (full tauID) selection (use same counters like for signal analysis to be able to cross-check)
    if (tauDataForBaseline.passedEvent()) {
      increment(fBaselineTauIDCounter);
      // Match tau to MC
      FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, *(tauDataForBaseline.getSelectedTau()));
      bool myFakeTauStatus = fFakeTauIdentifier.isFakeTau(tauMatchData.getTauMatchType()); // True if the selected tau is a fake
      // Apply scale factor for fake tau
      if (!iEvent.isRealData()) {
        fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauDataForBaseline.getSelectedTau()->eta()));
      }
      increment(fBaselineTauFakeScaleFactorCounter);
      // Apply scale factor tau part of trigger
      if (!iEvent.isRealData()) {
        const TauTriggerEfficiencyScaleFactor::Data tauTriggerWeightData = fTauTriggerEfficiencyScaleFactor.applyEventWeight(*(tauDataForBaseline.getSelectedTau()), iEvent.isRealData(), fEventWeight);
      }
      increment(fBaselineTauTriggerScaleFactorCounter);
      // Check if multiple taus passed
      if (!myMultipleTausPassForBaselineStatus) increment(fBaselineOneTauCounter);
      //hSelectionFlow->Fill(kQCDOrderTauCandidateSelection);
      return doBaselineAnalysis(iEvent, iSetup, tauDataForBaseline.getSelectedTau(), pvData, myFakeTauStatus);
    }
    // end of baseline selection
    ////////////////////////////////////////////////////////////////////////////////////////////////

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // Inverted tau selection starts (do here common plots)
    if (tauDataForInverted.passedEvent()) {
      increment(fInvertedTauIDCounter);
      // Match tau to MC
      FakeTauIdentifier::Data tauMatchData = fFakeTauIdentifier.matchTauToMC(iEvent, *(tauDataForInverted.getSelectedTau()));
      //bool myFakeTauStatus = fFakeTauIdentifier.isFakeTau(tauMatchData.getTauMatchType()); // True if the selected tau is a fake
      // Now re-initialize common plots with the correct selection for tau (affects jet selection, b-tagging, type I MET, delta phi cuts)
      fCommonPlots.initialize(iEvent, iSetup, pvData, tauDataForInverted, fFakeTauIdentifier, fElectronSelection, fMuonSelection, fJetSelection, fMETSelection, fBTagging, fQCDTailKiller, fTopChiSelection, fEvtTopology, fFullHiggsMassCalculator);
      fCommonPlots.fillControlPlotsAfterTauSelection(iEvent, iSetup, tauDataForInverted, tauMatchData, fMETSelection);
      // Apply scale factor for fake tau
      if (!iEvent.isRealData()) {
        fEventWeight.multiplyWeight(fFakeTauIdentifier.getFakeTauScaleFactor(tauMatchData.getTauMatchType(), tauDataForInverted.getSelectedTau()->eta()));
      }
      increment(fInvertedTauFakeScaleFactorCounter);
      // Apply scale factor tau part of trigger
      if (!iEvent.isRealData()) {
        const TauTriggerEfficiencyScaleFactor::Data tauTriggerWeightData = fTauTriggerEfficiencyScaleFactor.applyEventWeight(*(tauDataForInverted.getSelectedTau()), iEvent.isRealData(), fEventWeight);
      }
      increment(fInvertedTauTriggerScaleFactorCounter);
      // Check if multiple taus passed
      if (!myMultipleTausPassForInvertedStatus) increment(fInvertedOneTauCounter);

      fCommonPlots.fillControlPlotsAfterTauTriggerScaleFactor(iEvent);
      hSelectedTauEt->Fill(tauDataForInverted.getSelectedTau()->pt());
      hSelectedTauEta->Fill(tauDataForInverted.getSelectedTau()->eta());
      hSelectedTauPhi->Fill(tauDataForInverted.getSelectedTau()->phi());
      hSelectedTauRtau->Fill(tauDataForInverted.getSelectedTauRtauValue());
      hSelectedTauLeadingTrackPt->Fill(tauDataForInverted.getSelectedTau()->leadPFChargedHadrCand()->pt());

      return doInvertedAnalysis(iEvent, iSetup, tauDataForInverted.getSelectedTau(), pvData, genData);
    }
    // end of inverted selection
    ////////////////////////////////////////////////////////////////////////////////////////////////

    // Never reached
    return true;
  }

  bool SignalAnalysisInvertedTau::doBaselineAnalysis( const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau , const VertexSelection::Data& pvData, bool myFakeTauStatus) {
//------ Veto against second tau in event
    // Implement only, if necessary

//------ Global electron veto
    ElectronSelection::Data electronVetoData = fElectronSelection.silentAnalyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false; 
    increment(fBaselineEvetoCounter);

//------ Global muon veto
    MuonSelection::Data muonVetoData = fMuonSelection.silentAnalyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return false;
    increment(fBaselineMuvetoCounter);

//------ Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.silentAnalyze(iEvent, iSetup, selectedTau, pvData.getNumberOfAllVertices());
    if(!jetData.passedEvent()) return false;
    increment(fBaselineJetsCounter);

//------ MET trigger scale factor (after this step, the MET and its derivatives, such as transverse mass, are physically meaningful)
    METSelection::Data metDataTmp = fMETSelection.silentAnalyze(iEvent, iSetup, pvData.getNumberOfAllVertices(), selectedTau, jetData.getAllJets());
    // Apply trigger scale factor here for now, SF calculated for tau+3 jets events
    METTriggerEfficiencyScaleFactor::Data metTriggerWeight = fMETTriggerEfficiencyScaleFactor.applyEventWeight(*(metDataTmp.getSelectedMET()), iEvent.isRealData(), fEventWeight);
    increment(fBaselineMetTriggerScaleFactorCounter);
    hMETBaselineTauIdJets->Fill(selectedTau->pt(), metDataTmp.getSelectedMET()->et());

    // Obtain transverse mass for plotting
    double transverseMass = TransverseMass::reconstruct(*(selectedTau), *(metDataTmp.getSelectedMET()));
 
   // Use btag scale factor in histogram filling if btagging or btag veto is applied                                                                                                                                                                                
    BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();
 
   if (btagDataTmp.passedEvent()) {
      hMETBaselineTauIdBtag->Fill(selectedTau->pt(), metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
    }
   if (btagDataTmp.getSelectedJets().size() < 1) {
     hMETBaselineTauIdBveto->Fill(selectedTau->pt(), metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
   }

//------ Improved delta phi cut, a.k.a. QCD tail killer - collinear part
    const QCDTailKiller::Data qcdTailKillerDataCollinear = fQCDTailKiller.silentAnalyze(iEvent, iSetup, selectedTau, jetData.getSelectedJetsIncludingTau(), metDataTmp.getSelectedMET());
    if (!qcdTailKillerDataCollinear.passedCollinearCuts()) return false;
    increment(fBaselineQCDTailKillerCollinearCounter);

    // At this point, let's fill histograms for closure test and for normalisation
    hMETBaselineTauIdJetsCollinear->Fill(selectedTau->pt(), metDataTmp.getSelectedMET()->et()); // no btag scale factor needed
    hMTBaselineTauIdNoMetNoBtagging->Fill(selectedTau->pt(), transverseMass); // no btag scale factor needed
    if (qcdTailKillerDataCollinear.passedEvent()) {
      hMTBaselineTauIdNoMetNoBtaggingTailKiller->Fill(selectedTau->pt() ,transverseMass );
    }
    // Use btag scale factor in histogram filling if btagging or btag veto is applied
    //    BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    // double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();
    hNBBaselineTauIdJet->Fill(btagDataTmp.getSelectedJets().size(), myWeightWithBtagSF);
    if (btagDataTmp.passedEvent()) {
      // mT with b veto in bins
      hMTBaselineTauIdNoMetBtag->Fill(selectedTau->pt() ,transverseMass, myWeightWithBtagSF);
      if (qcdTailKillerDataCollinear.passedEvent()) {
        hMTBaselineTauIdNoMetBtagTailKiller->Fill(selectedTau->pt() ,transverseMass, myWeightWithBtagSF);
      }
      hMETBaselineTauIdBtagCollinear->Fill(selectedTau->pt(), metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
    }
    if (btagDataTmp.getSelectedJets().size() < 1) {
      // mT with b veto in bins 
      hMTBaselineTauIdNoMetBveto->Fill(selectedTau->pt(), transverseMass, myWeightWithBtagSF);
      if (qcdTailKillerDataCollinear.passedEvent()) {
        hMTBaselineTauIdNoMetBvetoTailKiller->Fill(selectedTau->pt(), transverseMass, myWeightWithBtagSF);
      }
      hMETBaselineTauIdBvetoCollinear->Fill(selectedTau->pt(), metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
    }

//------ MET cut
    METSelection::Data metData = fMETSelection.silentAnalyze(iEvent, iSetup, pvData.getNumberOfAllVertices(), selectedTau, jetData.getAllJets());
    if(!metData.passedEvent()) return false;
    increment(fBaselineMetCounter);

    // mT after jets and met in bins
    hMTBaselineTauIdNoBtagging->Fill(selectedTau->pt() ,transverseMass );
    if (qcdTailKillerDataCollinear.passedEvent()) {
      hMTBaselineTauIdNoBtaggingTailKiller->Fill(selectedTau->pt() ,transverseMass );
    }

    // mT with b veto in bins
    if (btagDataTmp.getSelectedJets().size() < 1) { 
      hMTBaselineTauIdBveto->Fill(selectedTau->pt() ,transverseMass, myWeightWithBtagSF);
      // mT with b veto and deltaPhi cuts in bins
      if (qcdTailKillerDataCollinear.passedEvent()) {   
        hMTBaselineTauIdBvetoTailKiller->Fill(selectedTau->pt() ,transverseMass, myWeightWithBtagSF);
      }
    }

    // MT for closure test with soft b tagging  
    if (btagDataTmp.getSelectedSubLeadingJets().size() > 0) {
      if (qcdTailKillerDataCollinear.passedEvent()) {
        hMTBaselineTauIdSoftBtaggingTK->Fill(selectedTau->pt() ,transverseMass, myWeightWithBtagSF);
      }
    }

//------ b tagging cut
    BTagging::Data btagData = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    if (btagData.passedEvent()) increment(fBaselineBtagCounter);
    // Apply scale factor as weight to event
    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
    // Beyond this point, the b tag scale factor has already been applied
    if(!btagData.passedEvent()) return false;
    increment(fBaselineBTaggingScaleFactorCounter);

    // mT with b tagging in bins
    hMTBaselineTauIdBtag->Fill(selectedTau->pt() ,transverseMass );


//------ Improved delta phi cut, a.k.a. QCD tail killer, back-to-back part
    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.silentAnalyze(iEvent, iSetup, selectedTau, jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    if (!qcdTailKillerData.passedBackToBackCuts()) return false;
    increment(fBaselineQCDTailKillerBackToBackCounter);

//     hQCDTailKillerJet0BackToBackBaseline->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(0)); // Make control plot before cut
//     hQCDTailKillerJet1BackToBackBaseline->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(1)); // Make control plot before cut
//     hQCDTailKillerJet2BackToBackBaseline->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(2)); // Make control plot before cut
//     hQCDTailKillerJet3BackToBackBaseline->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(3)); // Make control plot before cut

    // delta phi cuts
    double deltaPhi = DeltaPhi::reconstruct(*(selectedTau), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    hDeltaPhiBaseline->Fill(deltaPhi);
    if (deltaPhi < fDeltaPhiCutValue ) increment(fBaselineDeltaPhiTauMETCounter);

    // mT with b tagging and deltaPhi cuts 
    //    hMTBaselineTauIdPhi->Fill(selectedTau->pt() ,transverseMass );
    hMTBaselineTauIdAllCutsTailKiller->Fill(selectedTau->pt() ,transverseMass );
    
    increment(fBaselineSelectedEventsCounter);
    
    return true;
  }

  ////////////////////////////////////////////////////////////////////////////////////
  bool SignalAnalysisInvertedTau::doInvertedAnalysis( const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> selectedTau , const VertexSelection::Data& pvData, const GenParticleAnalysis::Data& genData) {

//------ Veto against second tau in event
    // Implement only, if necessary
    //fCommonPlots.fillControlPlotsAtTauVetoSelection(iEvent, iSetup, vetoTauData);
    //hSelectionFlow->Fill(kSignalOrderTauID);
    hSelectedTauEtTauVeto->Fill(selectedTau->pt());

//------ Global electron veto
    ElectronSelection::Data electronVetoData = fElectronSelection.analyze(iEvent, iSetup);
    fCommonPlots.fillControlPlotsAtElectronSelection(iEvent, electronVetoData);
    if (!electronVetoData.passedEvent()) return false;
    increment(fInvertedElectronVetoCounter);

//------ Global muon veto
    MuonSelection::Data muonVetoData = fMuonSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    fCommonPlots.fillControlPlotsAtMuonSelection(iEvent, muonVetoData);
    if (!muonVetoData.passedEvent()) return false;
    increment(fInvertedMuonVetoCounter);

//------ Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, selectedTau, pvData.getNumberOfAllVertices());
    fCommonPlots.fillControlPlotsAtJetSelection(iEvent, jetData);
    if(!jetData.passedEvent()) return false;
    increment(fInvertedNJetsCounter);

//------ MET trigger scale factor (after this step, the MET and its derivatives, such as transverse mass, are physically meaningful)
    METSelection::Data metDataTmp = fMETSelection.silentAnalyze(iEvent, iSetup, pvData.getNumberOfAllVertices(), selectedTau, jetData.getAllJets());
    // Apply trigger scale factor here for now, SF calculated for tau+3 jets events
    METTriggerEfficiencyScaleFactor::Data metTriggerWeight = fMETTriggerEfficiencyScaleFactor.applyEventWeight(*(metDataTmp.getSelectedMET()), iEvent.isRealData(), fEventWeight);
    increment(fInvertedMetTriggerScaleFactorCounter);
    hSelectedTauEtJetCut->Fill(selectedTau->pt() ,selectedTau->pt());
    fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(iEvent);

    hMETInvertedTauIdJets->Fill(selectedTau->pt(), metDataTmp.getSelectedMET()->et());

    // Obtain transverse mass for plotting
    double transverseMass = TransverseMass::reconstruct(*(selectedTau), *(metDataTmp.getSelectedMET()));

    // Use btag scale factor in histogram filling if btagging or btag veto is applied                                                                                                                                                                                
    BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();
    if(btagDataTmp.passedEvent()) {
      hMETInvertedTauIdBtag->Fill(selectedTau->pt(), metDataTmp.getSelectedMET()->et());
    }

    if( btagDataTmp.getSelectedJets().size() < 1) {
      hMETInvertedTauIdBveto->Fill(selectedTau->pt(), metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
    }

//------ Improved delta phi cut, a.k.a. QCD tail killer - collinear part
    const QCDTailKiller::Data qcdTailKillerDataCollinear = fQCDTailKiller.silentAnalyze(iEvent, iSetup, selectedTau, jetData.getSelectedJetsIncludingTau(), metDataTmp.getSelectedMET());
    fCommonPlots.fillControlPlotsAtCollinearDeltaPhiCuts(iEvent, qcdTailKillerDataCollinear);
    if (!qcdTailKillerDataCollinear.passedCollinearCuts()) return false;
    increment(fInvertedQCDTailKillerCollinearCounter);

    // At this point, let's fill histograms for closure test and for normalisation
    hSelectedTauEtCollinearTailKiller->Fill(selectedTau->pt() ,selectedTau->pt());
    // inverted MET before b tagging and MT before b tagging and Met
    hMTInvertedTauIdJet->Fill(selectedTau->pt(), transverseMass); 
    if (qcdTailKillerDataCollinear.passedEvent()) {       
      hMTInvertedTauIdJetTailKiller->Fill(selectedTau->pt(), transverseMass); 
    }
    hMETInvertedTauIdJetsCollinear->Fill(selectedTau->pt(), metDataTmp.getSelectedMET()->et()); 

    // Use btag scale factor in histogram filling if btagging or btag veto is applied
    //    BTagging::Data btagDataTmp = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    //    double myWeightWithBtagSF = fEventWeight.getWeight() * btagDataTmp.getScaleFactor();
    // MT with b tagging
    if(btagDataTmp.passedEvent()) {
      hMTInvertedTauIdBtagNoMetCut->Fill(selectedTau->pt(), transverseMass, myWeightWithBtagSF);
      increment(fInvertedBTaggingBeforeMETCounter); // NOTE: Will not give correct value for MC because btag SF is not applied
    }
    // MT with b veto 
    if( btagDataTmp.getSelectedJets().size() < 1) {
      increment(fInvertedBjetVetoCounter);// NOTE: Will not give correct value for MC because btag SF is not applied
      hMTInvertedTauIdBvetoNoMetCut->Fill(selectedTau->pt(), transverseMass, myWeightWithBtagSF);
      if (qcdTailKillerDataCollinear.passedEvent()) {
        hMTInvertedTauIdBvetoNoMetCutTailKiller->Fill(selectedTau->pt(), transverseMass, myWeightWithBtagSF);
      }
      hMETInvertedTauIdBvetoCollinear->Fill(selectedTau->pt(), metDataTmp.getSelectedMET()->et(), myWeightWithBtagSF);
    }

    //------ MET cut
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, pvData.getNumberOfAllVertices(), selectedTau, jetData.getAllJets());
    fCommonPlots.fillControlPlotsAtMETSelection(iEvent, metData);
    if(!metData.passedEvent()) return false;
    increment(fInvertedMetCounter);

    //hSelectionFlow->Fill(kQCDOrderMET);
    hSelectedTauEtMetCut->Fill(selectedTau->pt() ,selectedTau->pt());
    hSelectedTauEtaMetCut->Fill(selectedTau->eta());
    hSelectedTauPhiMetCut->Fill(selectedTau->phi());  


    hNBInvertedTauIdJet->Fill(selectedTau->pt(), btagDataTmp.getSelectedJets().size()); 

    // mt for inverted tau before b tagging
    hMTInvertedTauIdNoBtagging->Fill(selectedTau->pt(), transverseMass); 
    // deltaPhi before b tagging
    double deltaPhi = DeltaPhi::reconstruct(*(selectedTau), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    hDeltaPhiInvertedNoB->Fill(selectedTau->pt(),deltaPhi);  
    if (qcdTailKillerDataCollinear.passedEvent()) {
      // mt  before b tagging with deltaPhi for factorising b tagging 
      hMTInvertedNoBtaggingTailKiller->Fill(selectedTau->pt(), transverseMass);       
      hNBInvertedTauIdJetDphi->Fill(selectedTau->pt(), btagDataTmp.getSelectedJets().size()); 
    }

    // mt  with b veto
    if( btagDataTmp.getSelectedJets().size() < 1) {
      increment(fInvertedBvetoCounter); // NOTE: incorrect count because no btag scale factor has been applied
      hMTInvertedTauIdBveto->Fill(selectedTau->pt(), transverseMass, myWeightWithBtagSF);
      hSelectedTauEtBjetVeto->Fill(selectedTau->pt(), myWeightWithBtagSF);
      // mt  with b veto and deltaPhi
      if (qcdTailKillerDataCollinear.passedEvent()) {
        //    if ( deltaPhiMetJet1 > Rcut && deltaPhiMetJet2 > Rcut && deltaPhiMetJet3 > Rcut  ) {
        increment(fInvertedBvetoDeltaPhiCounter);  // NOTE: incorrect count because no btag scale factor has been applied
        hMTInvertedTauIdBvetoDphi->Fill(selectedTau->pt(),transverseMass, myWeightWithBtagSF);
        hSelectedTauEtBjetVetoPhiCuts->Fill(selectedTau->pt(), myWeightWithBtagSF);
      }
    }

    // MT for closure test with soft b tagging  
    if( btagDataTmp.getSelectedSubLeadingJets().size() > 0) {  
      if (qcdTailKillerDataCollinear.passedEvent()) {
        hMTInvertedTauIdSoftBtaggingTK->Fill(selectedTau->pt() ,transverseMass, myWeightWithBtagSF);
      }
    }

    //------ b tagging cut
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    // Apply scale factor as weight to event
    if (btagData.passedEvent()) increment(fInvertedBTaggingCounter);

    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
    // Beyond this point, the b tag scale factor has already been applied
    fCommonPlots.fillControlPlotsAtBtagging(iEvent, btagData);
    if (!btagData.passedEvent()) return false;
    increment(fInvertedBTaggingScaleFactorCounter);

    //hSelectionFlow->Fill(kQCDOrderBTag);
    hSelectedTauEtBtagging->Fill(selectedTau->pt() ,selectedTau->pt());

    // mt for inverted tau with b tagging
    hMTInvertedTauIdBtag->Fill(selectedTau->pt(), transverseMass);
    // deltaPhi with b tagging
    hDeltaPhiInverted->Fill(selectedTau->pt(),deltaPhi);  
    hTransverseMassVsDphi->Fill(transverseMass,deltaPhi);

    //------ Improved delta phi cut, a.k.a. QCD tail killer, back-to-back part
    const QCDTailKiller::Data qcdTailKillerData = fQCDTailKiller.analyze(iEvent, iSetup, selectedTau, jetData.getSelectedJetsIncludingTau(), metData.getSelectedMET());
    fCommonPlots.fillControlPlotsAtBackToBackDeltaPhiCuts(iEvent, qcdTailKillerData);
    if (!qcdTailKillerData.passedBackToBackCuts()) return false;
    increment(fInvertedQCDTailKillerBackToBackCounter);

//     hQCDTailKillerJet0BackToBackInverted->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(0)); // Make control plot before cut 
//     hQCDTailKillerJet1BackToBackInverted->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(2)); // Make control plot before cut 
//     hQCDTailKillerJet2BackToBackInverted->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(2)); // Make control plot before cut 
//     hQCDTailKillerJet3BackToBackInverted->Fill(qcdTailKillerData.getRadiusFromBackToBackCorner(3)); // Make control plot before cut 


    // mT with deltaPhi(tau,met)
    if (deltaPhi < fDeltaPhiCutValue) {
      hMTInvertedTauIdJetDphi->Fill(selectedTau->pt(),transverseMass);        
      increment(fInvertedDeltaPhiTauMETCounter);  
    }

    // cut values for circular deltaPhi cuts
    //double radius = 80;
    //double Rcut = 0;
    //if ( deltaPhi > (180-radius)) Rcut = sqrt(radius*radius - (180-deltaPhi)*(180-deltaPhi));
    //    std::cout << " Rcut " <<  Rcut  << " deltaPhi " <<  deltaPhi  << std::endl;
    //if (deltaPhiMetJet1 > Rcut && deltaPhiMetJet2 > Rcut && deltaPhiMetJet3 > Rcut ) increment(fQCDTailKillerCounter);	
    //    if (deltaPhiMetJet1 < Rcut || deltaPhiMetJet2 < Rcut || deltaPhiMetJet3 < Rcut ) return false;

    //    increment(fDeltaPhiVSDeltaPhiMETJet1CutCounter);
    hMTInvertedAllCutsTailKiller->Fill(selectedTau->pt(), transverseMass);     
    hMETInvertedAllCutsTailKiller->Fill(selectedTau->pt(), metData.getSelectedMET()->et());
    //    increment(fDeltaPhiVSDeltaPhiMETJet2CutCounter);
    hSelectedTauEtBackToBackTailKiller->Fill(selectedTau->pt() ,selectedTau->pt());

    // Top reconstruction
    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), selectedTau, metData.getSelectedMET());
    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    //fCommonPlots.fillControlPlotsAtTopSelection(iEvent, TopChiSelectionData);
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
    
    // All selections passed
    fCommonPlots.fillControlPlotsAfterAllSelections(iEvent, transverseMass);
    increment(fInvertedSelectedEventsCounter);

    //------ Invariant Higgs mass
    FullHiggsMassCalculator::Data fullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, selectedTau, btagData,
										       metData, &genData);
    if (!fullHiggsMassData.passedEvent()) return false;
    fCommonPlots.fillControlPlotsAfterAllSelectionsWithFullMass(iEvent, fullHiggsMassData);
    increment(fInvertedSelectedEventsInvariantMassCounter);
    //double HiggsMass = fullHiggsMassData.getHiggsMass();
    //if (HiggsMass > 100 && HiggsMass < 200 ) increment(fHiggsMassCutCounter);
    //hHiggsMass->Fill(selectedTau->pt(), HiggsMass);

    if(transverseMass < 80 ) increment(ftransverseMassCut80Counter);

    if(transverseMass < 100 ) increment(ftransverseMassCut100Counter);

    return true;
  }

}
