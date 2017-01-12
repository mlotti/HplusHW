// -*- c++ -*-
#include "Framework/interface/BaseSelector.h"
#include "Framework/interface/makeTH.h"

#include "EventSelection/interface/CommonPlots.h"
#include "EventSelection/interface/EventSelections.h"

#include "TDirectory.h"

class Hplus2tbAnalysis: public BaseSelector {
public:
  explicit Hplus2tbAnalysis(const ParameterSet& config, const TH1* skimCounters);
  virtual ~Hplus2tbAnalysis() {}

  /// Books histograms
  virtual void book(TDirectory *dir) override;
  /// Sets up branches for reading the TTree
  virtual void setupBranches(BranchManager& branchManager) override;
  /// Called for each event
  virtual void process(Long64_t entry) override;

private:
  // Input parameters
  const HistogramSettings cfg_PtBinSetting;
  const HistogramSettings cfg_EtaBinSetting;

  // Common plots
  CommonPlots fCommonPlots;
  // Event selection classes and event counters (in same order like they are applied)
  Count cAllEvents;
  Count cTrigger;
  METFilterSelection fMETFilterSelection;
  Count cVertexSelection;
  // Count cFakeTauSFCounter;
  // Count cTauTriggerSFCounter;
  // Count cMetTriggerSFCounter;
  ElectronSelection fElectronSelection;
  MuonSelection fMuonSelection;
  TauSelection fTauSelection;
  JetSelection fJetSelection;
  BJetSelection fBJetSelection;
  Count cBTaggingSFCounter;
  METSelection fMETSelection;
  TopologySelection fTopologySelection;
  TopSelection fTopSelection;
  Count cSelected;
    
  // Non-common histograms
  WrappedTH1 *hAssociatedTop_Pt;
  WrappedTH1 *hAssociatedTop_Eta;

};

#include "Framework/interface/SelectorFactory.h"
REGISTER_SELECTOR(Hplus2tbAnalysis);

Hplus2tbAnalysis::Hplus2tbAnalysis(const ParameterSet& config, const TH1* skimCounters)
  : BaseSelector(config, skimCounters),
    cfg_PtBinSetting(config.getParameter<ParameterSet>("CommonPlots.ptBins")),
    cfg_EtaBinSetting(config.getParameter<ParameterSet>("CommonPlots.etaBins")),
    fCommonPlots(config.getParameter<ParameterSet>("CommonPlots"), CommonPlots::kHplus2tbAnalysis, fHistoWrapper),
    cAllEvents(fEventCounter.addCounter("all events")),
    cTrigger(fEventCounter.addCounter("passed trigger")),
    fMETFilterSelection(config.getParameter<ParameterSet>("METFilter"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cVertexSelection(fEventCounter.addCounter("passed PV")),
    // cFakeTauSFCounter(fEventCounter.addCounter("Fake tau SF")), cTauTriggerSFCounter(fEventCounter.addCounter("Tau trigger SF")),
    // cMetTriggerSFCounter(fEventCounter.addCounter("Met trigger SF")),
    fElectronSelection(config.getParameter<ParameterSet>("ElectronSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fMuonSelection(config.getParameter<ParameterSet>("MuonSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fTauSelection(config.getParameter<ParameterSet>("TauSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, "Veto"),
    fJetSelection(config.getParameter<ParameterSet>("JetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fBJetSelection(config.getParameter<ParameterSet>("BJetSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cBTaggingSFCounter(fEventCounter.addCounter("b tag SF")),
    fMETSelection(config.getParameter<ParameterSet>("METSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopologySelection(config.getParameter<ParameterSet>("TopologySelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    fTopSelection(config.getParameter<ParameterSet>("TopSelection"), fEventCounter, fHistoWrapper, &fCommonPlots, ""),
    cSelected(fEventCounter.addCounter("Selected Events"))
{ }


void Hplus2tbAnalysis::book(TDirectory *dir) {

  
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
  fTopologySelection.bookHistograms(dir);
  fTopSelection.bookHistograms(dir);
  
  // Book non-common histograms
  const int nBinsPt   = cfg_PtBinSetting.bins();
  const double minPt  = cfg_PtBinSetting.min();
  const double maxPt  = cfg_PtBinSetting.max();
  
  const int nBinsEta  = cfg_EtaBinSetting.bins();
  const double minEta = cfg_EtaBinSetting.min();
  const double maxEta = cfg_EtaBinSetting.max();
 
  hAssociatedTop_Pt  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Pt", "Associated t pT;p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  hAssociatedTop_Eta = fHistoWrapper.makeTH<TH1F>(HistoLevel::kInformative, dir, "associatedTop_Eta", "Associated t eta;#eta", nBinsEta, minEta, maxEta);
  
  return;
}


void Hplus2tbAnalysis::setupBranches(BranchManager& branchManager) {
  fEvent.setupBranches(branchManager);
  return;
}


void Hplus2tbAnalysis::process(Long64_t entry) {

  //====== Initialize
  fCommonPlots.initialize();
  fCommonPlots.setFactorisationBinForEvent(std::vector<float> {});

  cAllEvents.increment();


  //================================================================================================   
  // GenParticle analysis
  //================================================================================================   
  if (0) std::cout << "=== GenParticles" << std::endl;
  // For-loop: GenParticles
  //  if (fEvent.isMC()) {
  //    
  //    for (auto& p: fEvent.genparticles().getGenParticles()) 
  //      {
  //	
  //	int genP_pdgId  = p.pdgId();
  //	double genP_pt  = p.pt();
  //	double genP_eta = p.eta();
  //	// double genP_Status = p.status(); // PYTHIA8: http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
  //	
  //	if( genP_pdgId == 6)
  //	  {
  //	    hAssociatedTop_Pt ->Fill( genP_pt  );
  //	    hAssociatedTop_Eta->Fill( genP_eta );
  //	  }
  //      }
  //  }
  


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
  // 4) Trigger SF
  //================================================================================================   
  // if (0) std::cout << "=== MET Trigger SF" << std::endl;
  // const METSelection::Data silentMETData = fMETSelection.silentAnalyze(fEvent, nVertices);
  // if (fEvent.isMC()) {
  //   fEventWeight.multiplyWeight(silentMETData.getMETTriggerSF());
  // }
  // cMetTriggerSFCounter.increment();
  // fCommonPlots.fillControlPlotsAfterMETTriggerScaleFactor(fEvent);
  

  //================================================================================================   
  // 5) Electron veto (Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Electron veto" << std::endl;
  const ElectronSelection::Data eData = fElectronSelection.analyze(fEvent);
  if (eData.hasIdentifiedElectrons()) return;


  //================================================================================================
  // 6) Muon veto (Orthogonality)
  //================================================================================================
  if (0) std::cout << "=== Muon veto" << std::endl;
  const MuonSelection::Data muData = fMuonSelection.analyze(fEvent);
  if (muData.hasIdentifiedMuons()) return;


  //================================================================================================   
  // 7) Tau Veto (HToTauNu Orthogonality)
  //================================================================================================   
  if (0) std::cout << "=== Tau-Veto" << std::endl;
  const TauSelection::Data tauData = fTauSelection.analyze(fEvent);
  if (tauData.hasIdentifiedTaus() ) return;

  // Fake-Tau SF
  if (fEvent.isMC()) 
    {      
      // Not needed unless a tau is used!
      // fEventWeight.multiplyWeight(tauData.getTauMisIDSF());
      // cFakeTauSFCounter.increment();
    }
  

  // Tau-Trigger SF
  if (fEvent.isMC())
    {
      // Not needed unless a tau is used!
      // fEventWeight.multiplyWeight(tauData.getTauTriggerSF());
      // cTauTriggerSFCounter.increment();
    }


  //================================================================================================
  // 8) Jet selection
  //================================================================================================
  if (0) std::cout << "=== Jet selection" << std::endl;
  const JetSelection::Data jetData = fJetSelection.analyzeWithoutTau(fEvent);
  if (!jetData.passedSelection()) return;


  //================================================================================================
  // Standard Selections
  //================================================================================================
  // if (0) std::cout << "=== Standard selection" << std::endl;
  fCommonPlots.fillControlPlotsAfterTopologicalSelections(fEvent, true);
  

  //================================================================================================  
  // 9) BJet selection
  //================================================================================================
  if (0) std::cout << "=== BJet selection" << std::endl;
  const BJetSelection::Data bjetData = fBJetSelection.analyze(fEvent, jetData);
  if (!bjetData.passedSelection()) return;


  //================================================================================================  
  // 10) BJet SF  
  //================================================================================================
  if (0) std::cout << "=== BJet SF" << std::endl;
  if (fEvent.isMC()) 
    {
      fEventWeight.multiplyWeight(bjetData.getBTaggingScaleFactorEventWeight());
    }
  cBTaggingSFCounter.increment();


  //================================================================================================
  // 11) MET selection
  //================================================================================================
  if (0) std::cout << "=== MET selection" << std::endl;
  const METSelection::Data METData = fMETSelection.analyze(fEvent, nVertices);
  if (!METData.passedSelection()) return;


  //================================================================================================
  // 12) Topology selection
  //================================================================================================
  if (0) std::cout << "=== Topology selection" << std::endl;
  const TopologySelection::Data TopologyData = fTopologySelection.analyze(fEvent, jetData);
  if (!TopologyData.passedSelection()) return;


  //================================================================================================
  // 13) Top selection
  //================================================================================================
  if (0) std::cout << "=== Top selection" << std::endl;
  const TopSelection::Data TopData = fTopSelection.analyze(fEvent, jetData, bjetData);
  if (!TopData.passedSelection()) return;


  //================================================================================================
  // ?) HT selection
  //================================================================================================
  // if (0) std::cout << "=== HT selection" << std::endl;
  // const METSelection::Data HTData = fMETSelection.analyze(fEvent, nVertices);
  // if (!HTData.passedSelection()) return;
  

  //================================================================================================
  // All cuts passed
  //================================================================================================
  if (0) std::cout << "=== All cuts passed" << std::endl;
  cSelected.increment();


  //================================================================================================
  // Fill final plots
  //================================================================================================
  fCommonPlots.fillControlPlotsAfterAllSelections(fEvent, true);
  

  //================================================================================================
  // Finalize
  //================================================================================================
  fEventSaver.save();
}
