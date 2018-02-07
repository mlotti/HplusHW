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
  WrappedTH1 *hGluonJetsQGL;
  WrappedTH1 *hGluonJetsN;
  WrappedTH1 *hGluonJetsPt;
  
  WrappedTH1 *hLightJetsQGL;
  WrappedTH1 *hLightJetsN;
  WrappedTH1 *hLightJetsPt;
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
  hGluonJetsQGL = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsQGL", "Quark-Gluon discriminator for Gluon Jets", nBinsQGL, minQGL, maxQGL);
  hGluonJetsN   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsN", "Gluon Jets Multiplicity", nNBins, fNMin, fNMax); 
  hGluonJetsPt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "GluonJetsPt", "Gluon Jets p_{T} (GeV)", nPtBins, fPtMin, fPtMax);
  
  hLightJetsQGL = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsQGL", "Quark-Gluon discriminator for Light Jets", nBinsQGL, minQGL, maxQGL);
  hLightJetsN   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsN", "Gluon Jets Multiplicity", nNBins, fNMin, fNMax); 
  hLightJetsPt = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "LightJetsPt", "Gluon Jets p_{T} (GeV)", nPtBins, fPtMin, fPtMax);
  
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
  int nGluonJets = 0;
  int nLightJets = 0;

  // Loop over selected jets
  for(const Jet& jet: jetData.getSelectedJets()) {
    
    jet_index++;
    
    //=== Reject jets consistent with b or c
    if (jet.hadronFlavour() != 0) continue;
    
    const short jetPartonFlavour = std::abs(jet.partonFlavour());
    
    // Gluon Jets
    if (jetPartonFlavour == 21)
      {
	hGluonJetsQGL->Fill(jet.QGTaggerAK4PFCHSqgLikelihood());
	hGluonJetsPt -> Fill(jet.pt());
	nGluonJets++;
      }
    
    // Light Jets
    if (jetPartonFlavour == 1 || jetPartonFlavour == 2 || jetPartonFlavour == 3)
      {
	hLightJetsQGL->Fill(jet.QGTaggerAK4PFCHSqgLikelihood());
	hLightJetsPt ->Fill(jet.pt());
	nLightJets++;
      }
  }
  
  hGluonJetsN -> Fill(nGluonJets);
  hLightJetsN -> Fill(nLightJets);
   
  //================================================================================================
  // Finalize
  //================================================================================================
  fEventSaver.save();

  return;
}
