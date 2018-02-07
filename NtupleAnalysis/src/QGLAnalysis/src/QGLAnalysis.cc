// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

class QGLAnalysis: public BaseSelector {
public:
  explicit QGLAnalysis(const ParameterSet& config, const TH1* skimCounters);
  virtual ~QGLAnalysis() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters
  // const DirectionalCut<float> cfg_PrelimTopFitChiSqr;
  const DirectionalCut<double> cfg_PrelimTopMVACut;

  // Common plots
  CommonPlots fCommonPlots;
  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  TauSelection fTauSelection;
  JetSelection fJetSelection;
  BJetSelection fBJetSelection;
  Count cBTaggingSFCounter;
  METSelection fMETSelection;
  // TopologySelection fTopologySelection;
  TopSelectionBDT fTopSelection;
  Count cSelected;
    
  // Non-common histograms
  
  // pT in the range [30,40)
  WrappedTH1 *hGluonJetsQGL_30pt40;
  WrappedTH1 *hGluonJetsN_30pt40;  
  WrappedTH1 *hGluonJetsPt_30pt40; 
  
  WrappedTH1 *hLightJetsQGL_30pt40;
  WrappedTH1 *hLightJetsN_30pt40;  
  WrappedTH1 *hLightJetsPt_30pt40;
  // pT in the range [40,50)
  WrappedTH1 *hGluonJetsQGL_40pt50;
  WrappedTH1 *hGluonJetsN_40pt50;  
  WrappedTH1 *hGluonJetsPt_40pt50; 
  
  WrappedTH1 *hLightJetsQGL_40pt50;
  WrappedTH1 *hLightJetsN_40pt50;  
  WrappedTH1 *hLightJetsPt_40pt50; 
  // pT in the range [50,65)
  WrappedTH1 *hGluonJetsQGL_50pt65;
  WrappedTH1 *hGluonJetsN_50pt65;  
  WrappedTH1 *hGluonJetsPt_50pt65; 
  
  WrappedTH1 *hLightJetsQGL_50pt65;
  WrappedTH1 *hLightJetsN_50pt65;  
  WrappedTH1 *hLightJetsPt_50pt65; 
  // pT in the range [65,80)
  WrappedTH1 *hGluonJetsQGL_65pt80;
  WrappedTH1 *hGluonJetsN_65pt80;  
  WrappedTH1 *hGluonJetsPt_65pt80; 
  
  WrappedTH1 *hLightJetsQGL_65pt80;
  WrappedTH1 *hLightJetsN_65pt80;  
  WrappedTH1 *hLightJetsPt_65pt80; 
  // pT in the range [80,100)
  WrappedTH1 *hGluonJetsQGL_80pt100;
  WrappedTH1 *hGluonJetsN_80pt100;  
  WrappedTH1 *hGluonJetsPt_80pt100; 
  
  WrappedTH1 *hLightJetsQGL_80pt100;
  WrappedTH1 *hLightJetsN_80pt100;  
  WrappedTH1 *hLightJetsPt_80pt100; 
  // pT in the range [100,125)
  WrappedTH1 *hGluonJetsQGL_100pt125;
  WrappedTH1 *hGluonJetsN_100pt125;  
  WrappedTH1 *hGluonJetsPt_100pt125; 
  
  WrappedTH1 *hLightJetsQGL_100pt125;
  WrappedTH1 *hLightJetsN_100pt125;  
  WrappedTH1 *hLightJetsPt_100pt125; 
  // pT in the range [125,160)
  WrappedTH1 *hGluonJetsQGL_125pt160;
  WrappedTH1 *hGluonJetsN_125pt160;  
  WrappedTH1 *hGluonJetsPt_125pt160; 
  
  WrappedTH1 *hLightJetsQGL_125pt160;
  WrappedTH1 *hLightJetsN_125pt160;  
  WrappedTH1 *hLightJetsPt_125pt160; 
  // pT in the range [160,200)
  WrappedTH1 *hGluonJetsQGL_160pt200;
  WrappedTH1 *hGluonJetsN_160pt200;  
  WrappedTH1 *hGluonJetsPt_160pt200; 
  
  WrappedTH1 *hLightJetsQGL_160pt200;
  WrappedTH1 *hLightJetsN_160pt200;  
  WrappedTH1 *hLightJetsPt_160pt200; 
  // pT in the range [200,250)
  WrappedTH1 *hGluonJetsQGL_200pt250;
  WrappedTH1 *hGluonJetsN_200pt250;  
  WrappedTH1 *hGluonJetsPt_200pt250; 

  WrappedTH1 *hLightJetsQGL_200pt250;
  WrappedTH1 *hLightJetsN_200pt250; 
  WrappedTH1 *hLightJetsPt_200pt250; 
  // pT in the range [250,320)
  WrappedTH1 *hGluonJetsQGL_250pt320;
  WrappedTH1 *hGluonJetsN_250pt320;  
  WrappedTH1 *hGluonJetsPt_250pt320; 
  
  WrappedTH1 *hLightJetsQGL_250pt320;
  WrappedTH1 *hLightJetsN_250pt320;  
  WrappedTH1 *hLightJetsPt_250pt320; 
  // pT in the range [320,400)
  WrappedTH1 *hGluonJetsQGL_320pt400;
  WrappedTH1 *hGluonJetsN_320pt400;  
  WrappedTH1 *hGluonJetsPt_320pt400;  

  WrappedTH1 *hLightJetsQGL_320pt400; 
  WrappedTH1 *hLightJetsN_320pt400;   
  WrappedTH1 *hLightJetsPt_320pt400;  
  // pT in the range [400,630)
  WrappedTH1 *hGluonJetsQGL_400pt630; 
  WrappedTH1 *hGluonJetsN_400pt630;   
  WrappedTH1 *hGluonJetsPt_400pt630;  
  
  WrappedTH1 *hLightJetsQGL_400pt630; 
  WrappedTH1 *hLightJetsN_400pt630;   
  WrappedTH1 *hLightJetsPt_400pt630;  
  // pT in the range [630,800)
  WrappedTH1 *hGluonJetsQGL_630pt800; 
  WrappedTH1 *hGluonJetsN_630pt800;   
  WrappedTH1 *hGluonJetsPt_630pt800;  
  
  WrappedTH1 *hLightJetsQGL_630pt800; 
  WrappedTH1 *hLightJetsN_630pt800;   
  WrappedTH1 *hLightJetsPt_630pt800; 
  // pT in the range [800,inf)
  WrappedTH1 *hGluonJetsQGL_800ptInf; 
  WrappedTH1 *hGluonJetsN_800ptInf;   
  WrappedTH1 *hGluonJetsPt_800ptInf;  

  WrappedTH1 *hLightJetsQGL_800ptInf; 
  WrappedTH1 *hLightJetsN_800ptInf;   
  WrappedTH1 *hLightJetsPt_800ptInf;  
};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(QGLAnalysis);

QGLAnalysis::QGLAnalysis(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    // cfg_PrelimTopFitChiSqr(config, "FakeBMeasurement.prelimTopFitChiSqrCut"),
    cfg_PrelimTopMVACut(config, "FakeBMeasurement.prelimTopMVACut"),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kHplus2tbAnalysis, fHistoWrapper),
    cAllEvents(fEventCounter.addCounter("all events")),
    cTrigger(fEventCounter.addCounter("passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("passed PV")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cBTaggingSFCounter(fEventCounter.addCounter("b tag SF")),
    // fMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fMETSelection(config.getParameter<ParameterSet>("METSelection")), // no subcounter in main counter
    // fTopologySelection(config.getParameter<ParameterSet>("TopologySelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopSelection(config.getParameter<ParameterSet>("TopSelectionBDT"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cSelected(fEventCounter.addCounter("Selected Events"))
{ }


void QGLAnalysis::book(TDirectory *dir) {

  
  // Book common plots histograms
  fCommonPlots.book(dir, isData());

  // Book histograms in event selection classes
  fMETFilterSelection.bookHistograms(dir);
  fElectronSelection.bookHistograms(dir);
  fMuonSelection.bookHistograms(dir);
  fTauSelection.bookHistograms(dir);
  fJetSelection.bookHistograms(dir);
  fBJetSelection.bookHistograms(dir);
  fMETSelection.bookHistograms(dir);
  // fTopologySelection.bookHistograms(dir);
  fTopSelection.bookHistograms(dir);
  
  // Fixed Binning
  const int nBinsQGL = 100;
  const float minQGL = 0.0;
  const float maxQGL = 1.0;
  
  // Obtain binning
  const int nNBins        = fCommonPlots.getNjetsBinSettings().bins();
  const float fNMin       = fCommonPlots.getNjetsBinSettings().min();
  const float fNMax       = fCommonPlots.getNjetsBinSettings().max();
  
  const int  nPtBins      = 2*fCommonPlots.getPtBinSettings().bins();
  const float fPtMin      = fCommonPlots.getPtBinSettings().min();
  const float fPtMax      = 2*fCommonPlots.getPtBinSettings().max();
  
  // Book non-common histograms
  // 30-40, 40-50, 50-65, 65-80, 80-100. 100-125, 125-160,160-200, 200-250, 250-320, 320-400,400-630, 630-800, 800-1000

  // pT in the range [30,40)
  hGluonJetsQGL_30pt40 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_30pt40", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [30,40)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_30pt40   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_30pt40"  , "Gluon Jets Multiplicity with p_{T} in the range [30,40)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_30pt40  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_30pt40" , "Gluon Jets p_{T} (GeV) in the range [30,40)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_30pt40 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_30pt40", "Quark-Gluon discriminator for Light Jets in the p_{T} range [30,40)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_30pt40   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_30pt40"  , "Gluon Jets Multiplicity with p_{T} in the range [30,40)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_30pt40  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_30pt40" , "Gluon Jets p_{T} (GeV) in the range [30,40)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [40,50)
  hGluonJetsQGL_40pt50 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_40pt50", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [40,50)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_40pt50   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_40pt50"  , "Gluon Jets Multiplicity with p_{T} in the range [40,50)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_40pt50  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_40pt50" , "Gluon Jets p_{T} (GeV) in the range [40,50)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_40pt50 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_40pt50", "Quark-Gluon discriminator for Light Jets in the p_{T} range [40,50)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_40pt50   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_40pt50"  , "Gluon Jets Multiplicity with p_{T} in the range [40,50)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_40pt50  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_40pt50" , "Gluon Jets p_{T} (GeV) in the range [40,50)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [50,65)
  hGluonJetsQGL_50pt65 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_50pt65", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [50,65)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_50pt65   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_50pt65"  , "Gluon Jets Multiplicity with p_{T} in the range [50,65)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_50pt65  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_50pt65" , "Gluon Jets p_{T} (GeV) in the range [50,65)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_50pt65 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_50pt65", "Quark-Gluon discriminator for Light Jets in the p_{T} range [50,65)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_50pt65   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_50pt65"  , "Gluon Jets Multiplicity with p_{T} in the range [50,65)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_50pt65  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_50pt65" , "Gluon Jets p_{T} (GeV) in the range [50,65)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [65,80)
  hGluonJetsQGL_65pt80 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_65pt80", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [65,80)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_65pt80   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_65pt80"  , "Gluon Jets Multiplicity with p_{T} in the range [65,80)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_65pt80  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_65pt80" , "Gluon Jets p_{T} (GeV) in the range [65,80)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_65pt80 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_65pt80", "Quark-Gluon discriminator for Light Jets in the p_{T} range [65,80)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_65pt80   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_65pt80"  , "Gluon Jets Multiplicity with p_{T} in the range [65,80)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_65pt80  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_65pt80" , "Gluon Jets p_{T} (GeV) in the range [65,80)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [80,100)
  hGluonJetsQGL_80pt100 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_80pt100", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [80,100)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_80pt100   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_80pt100"  , "Gluon Jets Multiplicity with p_{T} in the range [80,100)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_80pt100  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_80pt100" , "Gluon Jets p_{T} (GeV) in the range [80,100)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_80pt100 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_80pt100", "Quark-Gluon discriminator for Light Jets in the p_{T} range [80,100)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_80pt100   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_80pt100"  , "Gluon Jets Multiplicity with p_{T} in the range [80,100)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_80pt100  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_80pt100" , "Gluon Jets p_{T} (GeV) in the range [80,100)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [100,125)
  hGluonJetsQGL_100pt125 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_100pt125", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [100,125)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_100pt125   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_100pt125"  , "Gluon Jets Multiplicity with p_{T} in the range [100,125)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_100pt125  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_100pt125" , "Gluon Jets p_{T} (GeV) in the range [100,125)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_100pt125 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_100pt125", "Quark-Gluon discriminator for Light Jets in the p_{T} range [100,125)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_100pt125   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_100pt125"  , "Gluon Jets Multiplicity with p_{T} in the range [100,125)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_100pt125  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_100pt125" , "Gluon Jets p_{T} (GeV) in the range [100,125)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [125,160)
  hGluonJetsQGL_125pt160 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_125pt160", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [125,160)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_125pt160   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_125pt160"  , "Gluon Jets Multiplicity with p_{T} in the range [125,160)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_125pt160  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_125pt160" , "Gluon Jets p_{T} (GeV) in the range [125,160)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_125pt160 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_125pt160", "Quark-Gluon discriminator for Light Jets in the p_{T} range [125,160)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_125pt160   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_125pt160"  , "Gluon Jets Multiplicity with p_{T} in the range [125,160)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_125pt160  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_125pt160" , "Gluon Jets p_{T} (GeV) in the range [125,160)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [160,200)
  hGluonJetsQGL_160pt200 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_160pt200", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [160,200)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_160pt200   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_160pt200"  , "Gluon Jets Multiplicity with p_{T} in the range [160,200)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_160pt200  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_160pt200" , "Gluon Jets p_{T} (GeV) in the range [160,200)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_160pt200 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_160pt200", "Quark-Gluon discriminator for Light Jets in the p_{T} range [160,200)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_160pt200   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_160pt200"  , "Gluon Jets Multiplicity with p_{T} in the range [160,200)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_160pt200  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_160pt200" , "Gluon Jets p_{T} (GeV) in the range [160,200)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [200,250)
  hGluonJetsQGL_200pt250 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_200pt250", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [200,250)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_200pt250   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_200pt250"  , "Gluon Jets Multiplicity with p_{T} in the range [200,250)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_200pt250  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_200pt250" , "Gluon Jets p_{T} (GeV) in the range [200,250)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_200pt250 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_200pt250", "Quark-Gluon discriminator for Light Jets in the p_{T} range [200,250)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_200pt250   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_200pt250" , "Gluon Jets Multiplicity with p_{T} in the range [200,250)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_200pt250  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_200pt250" , "Gluon Jets p_{T} (GeV) in the range [200,250)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [250,320)
  hGluonJetsQGL_250pt320 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_250pt320", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [250,320)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_250pt320   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_250pt320"  , "Gluon Jets Multiplicity with p_{T} in the range [250,320)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_250pt320  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_250pt320" , "Gluon Jets p_{T} (GeV) in the range [250,320)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_250pt320 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_250pt320", "Quark-Gluon discriminator for Light Jets in the p_{T} range [250,320)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_250pt320   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_250pt320" , "Gluon Jets Multiplicity with p_{T} in the range [250,320)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_250pt320  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_250pt320" , "Gluon Jets p_{T} (GeV) in the range [250,320)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [320,400)
  hGluonJetsQGL_320pt400 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_320pt400", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [320,400)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_320pt400   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_320pt400"  , "Gluon Jets Multiplicity with p_{T} in the range [320,400)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_320pt400  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_320pt400" , "Gluon Jets p_{T} (GeV) in the range [320,400)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_320pt400 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_320pt400", "Quark-Gluon discriminator for Light Jets in the p_{T} range [320,400)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_320pt400   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_320pt400" , "Gluon Jets Multiplicity with p_{T} in the range [320,400)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_320pt400  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_320pt400" , "Gluon Jets p_{T} (GeV) in the range [320,400)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [400,630)
  hGluonJetsQGL_400pt630 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_400pt630", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [400,630)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_400pt630   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_400pt630"  , "Gluon Jets Multiplicity with p_{T} in the range [400,630)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_400pt630  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_400pt630" , "Gluon Jets p_{T} (GeV) in the range [400,630)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_400pt630 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_400pt630", "Quark-Gluon discriminator for Light Jets in the p_{T} range [400,630)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_400pt630   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_400pt630" , "Gluon Jets Multiplicity with p_{T} in the range [400,630)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_400pt630  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_400pt630" , "Gluon Jets p_{T} (GeV) in the range [400,630)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [630,800)
  hGluonJetsQGL_630pt800 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_630pt800", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [630,800)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_630pt800   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_630pt800"  , "Gluon Jets Multiplicity with p_{T} in the range [630,800)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_630pt800  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_630pt800" , "Gluon Jets p_{T} (GeV) in the range [630,800)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_630pt800 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_630pt800", "Quark-Gluon discriminator for Light Jets in the p_{T} range [630,800)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_630pt800   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_630pt800" , "Gluon Jets Multiplicity with p_{T} in the range [630,800)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_630pt800  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_630pt800" , "Gluon Jets p_{T} (GeV) in the range [630,800)"                          , nPtBins, fPtMin, fPtMax);
  // pT in the range [800,inf)
  hGluonJetsQGL_800ptInf = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL_800ptInf", "Quark-Gluon discriminator for Gluon Jets in the p_{T} range [630,inf)"  , nBinsQGL, minQGL, maxQGL);
  hGluonJetsN_800ptInf   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN_800ptInf"  , "Gluon Jets Multiplicity with p_{T} in the range [630,inf)"              , nNBins, fNMin, fNMax); 
  hGluonJetsPt_800ptInf  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt_800ptInf" , "Gluon Jets p_{T} (GeV) in the range [630,inf)"                          , nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL_800ptInf = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL_800ptInf", "Quark-Gluon discriminator for Light Jets in the p_{T} range [800,inf)"  , nBinsQGL, minQGL, maxQGL);
  hLightJetsN_800ptInf   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN_800ptInf" , "Gluon Jets Multiplicity with p_{T} in the range [800,inf)"              , nNBins, fNMin, fNMax); 
  hLightJetsPt_800ptInf  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt_800ptInf" , "Gluon Jets p_{T} (GeV) in the range [800,inf)"                          , nPtBins, fPtMin, fPtMax);
  
  return;
}


void QGLAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void QGLAnalysis::process(Long64_t entry) {
  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});
  cAllEvents.increment();

  //================================================================================================   
  // 1) Apply trigger 
  //================================================================================================   
  if (0) std::cout << "=== Trigger" << std::endl;
  if ( !(fEvent.passTriggerDecision()) ) return;
  
  cTrigger.increment();
  int nVertices = fEvent.vertexInfo().value();
  fCommonPlots.setNvertices(nVertices);
  fCommonPlots.fillControlPlotsAfterTrigger(fEvent);

  //================================================================================================   
  // 2) MET filters (to remove events with spurious sources of fake MET)
  //================================================================================================   
  if (0) std::cout << "=== MET Filter" << std::endl;
  const METFilterSelection::Data metFilterData = fMETFilterSelection.analyze(fEvent);
  if (!metFilterData.passedSelection()) return;
  fCommonPlots.fillControlPlotsAfterMETFilter(fEvent);  

  //================================================================================================   
  // 3) Primarty Vertex (Check that a PV exists)
  //================================================================================================   
  if (0) std::cout << "=== Vertices" << std::endl;
  if (nVertices < 1) return;
  cVertexSelection.increment();
  fCommonPlots.fillControlPlotsAtVertexSelection(fEvent);
  
  //================================================================================================   
  // 4) Electron veto (Fully hadronic + orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Electron veto" << std::endl;
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons()) return;

  //================================================================================================
  // 5) Muon veto (Fully hadronic + orthogonality)
  //================================================================================================
  if (0) std::cout << "=== Muon veto" << std::endl;
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons()) return;

  //================================================================================================   
  // 6) Tau Veto (HToTauNu Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Tau Veto" << std::endl;
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (tauData.hasIdentifiedTaus() ) return;

  //================================================================================================
  // 7) Jet selection
  //================================================================================================
  if (0) std::cout << "=== Jet selection" << std::endl;
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent, true);
  
  //================================================================================================
  // 8) QGL selection
  //================================================================================================
  int jet_index = -1;
  
  // 30-40, 40-50, 50-65, 65-80, 80-100. 100-125, 125-160,160-200, 200-250, 250-320, 320-400,400-630, 630-800, 800-1000
  int nGluonJets_30pt40   = 0;
  int nGluonJets_40pt50   = 0;
  int nGluonJets_50pt65   = 0;
  int nGluonJets_65pt80   = 0;
  int nGluonJets_80pt100  = 0;
  int nGluonJets_100pt125 = 0;
  int nGluonJets_125pt160 = 0;
  int nGluonJets_160pt200 = 0;
  int nGluonJets_200pt250 = 0;
  int nGluonJets_250pt320 = 0;
  int nGluonJets_320pt400 = 0;
  int nGluonJets_400pt630 = 0;
  int nGluonJets_630pt800 = 0;
  int nGluonJets_800ptInf = 0;
  
  int nLightJets_30pt40   = 0;
  int nLightJets_40pt50   = 0;
  int nLightJets_50pt65   = 0;
  int nLightJets_65pt80   = 0;
  int nLightJets_80pt100  = 0;
  int nLightJets_100pt125 = 0;
  int nLightJets_125pt160 = 0;
  int nLightJets_160pt200 = 0;
  int nLightJets_200pt250 = 0;
  int nLightJets_250pt320 = 0;
  int nLightJets_320pt400 = 0;
  int nLightJets_400pt630 = 0;
  int nLightJets_630pt800 = 0;
  int nLightJets_800ptInf = 0;
  

  // Loop over selected jets
  for(const Jet& jet: jetData.getSelectedJets()) {
    
    jet_index++;
    
    //=== Reject jets consistent with b or c
    if (jet.hadronFlavour() != 0) continue;
    
    const short jetPartonFlavour = std::abs(jet.partonFlavour());
    
    double QGL = jet.QGTaggerAK4PFCHSqgLikelihood();
    double pt  = jet.pt();
    
    // Gluon Jets
    if (jetPartonFlavour == 21)
      {
	// 30-40, 40-50, 50-65, 65-80, 80-100. 100-125, 125-160,160-200, 200-250, 250-320, 320-400,400-630, 630-800, 800-1000
	if (pt >= 30 && pt < 40){
	  nGluonJets_30pt40++;
	  hGluonJetsQGL_30pt40 -> Fill(QGL);
	  hGluonJetsPt_30pt40  -> Fill(pt); 
	}
	else if (pt >= 40 && pt < 50){
	  nGluonJets_40pt50++;
	  hGluonJetsQGL_40pt50 -> Fill(QGL);
	  hGluonJetsPt_40pt50  -> Fill(pt); 
	}
	else if (pt >= 50 && pt < 65){
	  nGluonJets_50pt65++;
	  hGluonJetsQGL_50pt65 -> Fill(QGL);
	  hGluonJetsPt_50pt65  -> Fill(pt);
	}
	else if (pt >= 65 && pt < 80){
	  nGluonJets_65pt80++;
	  hGluonJetsQGL_65pt80 -> Fill(QGL);
	  hGluonJetsPt_65pt80  -> Fill(pt);
	}
	else if (pt >= 80 && pt < 100){
	  nGluonJets_80pt100++;
	  hGluonJetsQGL_80pt100 -> Fill(QGL);
	  hGluonJetsPt_80pt100  -> Fill(pt);
	}
	else if (pt >= 100 && pt < 125){
	  nGluonJets_100pt125++;
	  hGluonJetsQGL_100pt125 -> Fill(QGL);
	  hGluonJetsPt_100pt125  -> Fill(pt);
	}
	else if (pt >= 125 && pt < 160){
	  nGluonJets_125pt160++;
	  hGluonJetsQGL_125pt160 -> Fill(QGL);
	  hGluonJetsPt_125pt160  -> Fill(pt);
	}
	else if (pt >= 160 && pt < 200){
	  nGluonJets_160pt200++;
	  hGluonJetsQGL_160pt200 -> Fill(QGL);
	  hGluonJetsPt_160pt200  -> Fill(pt);
	}
	else if (pt >= 200 && pt < 250){
	  nGluonJets_200pt250++;
	  hGluonJetsQGL_200pt250 -> Fill(QGL);
	  hGluonJetsPt_200pt250  -> Fill(pt);
	}
	else if (pt >= 250 && pt < 320){
	  nGluonJets_250pt320++;
	  hGluonJetsQGL_250pt320 -> Fill(QGL);
	  hGluonJetsPt_250pt320  -> Fill(pt);
	}
	else if (pt >= 320 && pt < 400){
	  nGluonJets_320pt400++;
	  hGluonJetsQGL_320pt400 -> Fill(QGL);
	  hGluonJetsPt_320pt400  -> Fill(pt);
	}
	else if (pt >= 400 && pt < 630){
	  nGluonJets_400pt630++;
	  hGluonJetsQGL_400pt630 -> Fill(QGL);
	  hGluonJetsPt_400pt630  -> Fill(pt);
	}
	else if (pt >= 630 && pt < 800){
	  nGluonJets_630pt800++;
	  hGluonJetsQGL_630pt800 -> Fill(QGL);
	  hGluonJetsPt_630pt800  -> Fill(pt);
	}
	else if (pt >= 800){
	  nGluonJets_800ptInf++;
	  hGluonJetsQGL_800ptInf -> Fill(QGL);
	  hGluonJetsPt_800ptInf  -> Fill(pt);
	}
      }
    
    // Light Jets
    if (jetPartonFlavour == 1 || jetPartonFlavour == 2 || jetPartonFlavour == 3)
      {
	
	// 30-40, 40-50, 50-65, 65-80, 80-100. 100-125, 125-160,160-200, 200-250, 250-320, 320-400,400-630, 630-800, 800-1000
	if (pt >= 30 && pt < 40){
	  nLightJets_30pt40++;
	  hLightJetsQGL_30pt40 -> Fill(QGL);
	  hLightJetsPt_30pt40  -> Fill(pt); 
	}
	else if (pt >= 40 && pt < 50){
	  nLightJets_40pt50++;
	  hLightJetsQGL_40pt50 -> Fill(QGL);
	  hLightJetsPt_40pt50  -> Fill(pt); 
	}
	else if (pt >= 50 && pt < 65){
	  nLightJets_50pt65++;
	  hLightJetsQGL_50pt65 -> Fill(QGL);
	  hLightJetsPt_50pt65  -> Fill(pt);
	}
	else if (pt >= 65 && pt < 80){
	  nLightJets_65pt80++;
	  hLightJetsQGL_65pt80 -> Fill(QGL);
	  hLightJetsPt_65pt80  -> Fill(pt);
	}
	else if (pt >= 80 && pt < 100){
	  nLightJets_80pt100++;
	  hLightJetsQGL_80pt100 -> Fill(QGL);
	  hLightJetsPt_80pt100  -> Fill(pt);
	}
	else if (pt >= 100 && pt < 125){
	  nLightJets_100pt125++;
	  hLightJetsQGL_100pt125 -> Fill(QGL);
	  hLightJetsPt_100pt125  -> Fill(pt);
	}
	else if (pt >= 125 && pt < 160){
	  nLightJets_125pt160++;
	  hLightJetsQGL_125pt160 -> Fill(QGL);
	  hLightJetsPt_125pt160  -> Fill(pt);
	}
	else if (pt >= 160 && pt < 200){
	  nLightJets_160pt200++;
	  hLightJetsQGL_160pt200 -> Fill(QGL);
	  hLightJetsPt_160pt200  -> Fill(pt);
	}
	else if (pt >= 200 && pt < 250){
	  nLightJets_200pt250++;
	  hLightJetsQGL_200pt250 -> Fill(QGL);
	  hLightJetsPt_200pt250  -> Fill(pt);
	}
	else if (pt >= 250 && pt < 320){
	  nLightJets_250pt320++;
	  hLightJetsQGL_250pt320 -> Fill(QGL);
	  hLightJetsPt_250pt320  -> Fill(pt);
	}
	else if (pt >= 320 && pt < 400){
	  nLightJets_320pt400++;
	  hLightJetsQGL_320pt400 -> Fill(QGL);
	  hLightJetsPt_320pt400  -> Fill(pt);
	}
	else if (pt >= 400 && pt < 630){
	  nLightJets_400pt630++;
	  hLightJetsQGL_400pt630 -> Fill(QGL);
	  hLightJetsPt_400pt630  -> Fill(pt);
	}
	else if (pt >= 630 && pt < 800){
	  nLightJets_630pt800++;
	  hLightJetsQGL_630pt800 -> Fill(QGL);
	  hLightJetsPt_630pt800  -> Fill(pt);
	}
	else if (pt >= 800){
	  nLightJets_800ptInf++;
	  hLightJetsQGL_800ptInf -> Fill(QGL);
	  hLightJetsPt_800ptInf  -> Fill(pt);
	}
      }
  }
  
  // 30-40, 40-50, 50-65, 65-80, 80-100. 100-125, 125-160,160-200, 200-250, 250-320, 320-400,400-630, 630-800, 800-1000
  hGluonJetsN_30pt40   -> Fill(nGluonJets_30pt40);
  hGluonJetsN_40pt50   -> Fill(nGluonJets_40pt50);
  hGluonJetsN_50pt65   -> Fill(nGluonJets_50pt65);
  hGluonJetsN_65pt80   -> Fill(nGluonJets_65pt80);
  hGluonJetsN_80pt100  -> Fill(nGluonJets_80pt100);
  hGluonJetsN_100pt125 -> Fill(nGluonJets_100pt125);
  hGluonJetsN_125pt160 -> Fill(nGluonJets_125pt160);
  hGluonJetsN_160pt200 -> Fill(nGluonJets_160pt200);
  hGluonJetsN_200pt250 -> Fill(nGluonJets_200pt250);
  hGluonJetsN_250pt320 -> Fill(nGluonJets_250pt320);
  hGluonJetsN_320pt400 -> Fill(nGluonJets_320pt400);
  hGluonJetsN_400pt630 -> Fill(nGluonJets_400pt630);
  hGluonJetsN_630pt800 -> Fill(nGluonJets_630pt800);
  hGluonJetsN_800ptInf -> Fill(nGluonJets_800ptInf);
  
  hLightJetsN_30pt40   -> Fill(nLightJets_30pt40);
  hLightJetsN_40pt50   -> Fill(nLightJets_40pt50);
  hLightJetsN_50pt65   -> Fill(nLightJets_50pt65);
  hLightJetsN_65pt80   -> Fill(nLightJets_65pt80);
  hLightJetsN_80pt100  -> Fill(nLightJets_80pt100);
  hLightJetsN_100pt125 -> Fill(nLightJets_100pt125);
  hLightJetsN_125pt160 -> Fill(nLightJets_125pt160);
  hLightJetsN_160pt200 -> Fill(nLightJets_160pt200);
  hLightJetsN_200pt250 -> Fill(nLightJets_200pt250);
  hLightJetsN_250pt320 -> Fill(nLightJets_250pt320);
  hLightJetsN_320pt400 -> Fill(nLightJets_320pt400);
  hLightJetsN_400pt630 -> Fill(nLightJets_400pt630);
  hLightJetsN_630pt800 -> Fill(nLightJets_630pt800);
  hLightJetsN_800ptInf -> Fill(nLightJets_800ptInf);
  
  //================================================================================================
  // Finalize
  //================================================================================================
  fEventSaver.save();

  return;
}
