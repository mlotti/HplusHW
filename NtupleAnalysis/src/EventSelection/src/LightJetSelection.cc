// -*- c++ -*-
#include "EventSelection/interface/LightJetSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

LightJetSelection::Data::Data()
: bPassedSelection(false)
{ }

LightJetSelection::Data::~Data() { }

LightJetSelection::LightJetSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  fJetPtCut(config.getParameter<float>("jetPtCut")),
  fJetEtaCut(config.getParameter<float>("jetEtaCut")),
  fBjetMatchingDeltaR(config.getParameter<float>("bjetMatchingDeltaR")),
  fNumberOfJetsCut(config, "numberOfJetsCut"),
  // Event counter for passing selection
  cPassedLightJetSelection(fEventCounter.addCounter("passed light-jet selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("light-jet selection ("+postfix+")", "All events")),
  cSubPassedEta(fEventCounter.addSubCounter("light-jet selection ("+postfix+")", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("light-jet selection ("+postfix+")", "Passed pt cut")),
  cSubPassedJetCount(fEventCounter.addSubCounter("light-jet selection ("+postfix+")", "Passed jet number cut"))
{ 
  initialize(config);
}

LightJetSelection::LightJetSelection(const ParameterSet& config)
: BaseSelection(),
  fJetPtCut(config.getParameter<float>("jetPtCut")),
  fJetEtaCut(config.getParameter<float>("jetEtaCut")),
  fBjetMatchingDeltaR(config.getParameter<float>("bjetMatchingDeltaR")),
  fNumberOfJetsCut(config, "numberOfJetsCut"),
  // Event counter for passing selection
  cPassedLightJetSelection(fEventCounter.addCounter("passed jet selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("light-jet selection", "All events")),
  cSubPassedEta(fEventCounter.addSubCounter("light-jet selection", "Passed eta cut")),
  cSubPassedPt(fEventCounter.addSubCounter("light-jet selection", "Passed pt cut")),
  cSubPassedJetCount(fEventCounter.addSubCounter("light-jet selection", "Passed jet number cut"))
{ 
  initialize(config);
  bookHistograms(new TDirectory());
}

LightJetSelection::~LightJetSelection() { 
  delete hJetPtAll;
  delete hJetEtaAll;
  delete hJetPtPassed;
  delete hJetEtaPassed;
  for (auto p: hSelectedJetPt) delete p;
  for (auto p: hSelectedJetEta) delete p;  
}

void LightJetSelection::initialize(const ParameterSet& config) {
  
}

void LightJetSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "lightJetSelection_"+sPostfix);

  // Histograms (1D)
  hJetPtAll     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "jetPtAll", "Jet pT, all;p_{T} (GeV/c)", 50, 0.0, 500.0);
  hJetEtaAll    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "jetEtaAll", "Jet #eta, all;#eta", 50, -2.5, 2.5);
  hJetPtPassed  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "jetPtPassed", "Jet pT, passed;p_{T} (GeV/c)", 50, 0.0, 500.0);
  hJetEtaPassed = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "jetEtaPassed", "Jet Eta, passed", 50, -2.5, 2.5);

  hSelectedJetPt.push_back( fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsFirstJetPt"  , "First light-jet pT;p_{T} (GeV/c);Events / %.0f GeV/c"  , 50, 0.0, 500.0) );
  hSelectedJetPt.push_back( fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsSecondJetPt" , "Second light-jet pT;p_{T} (GeV/c);Events / %.0f GeV/c" , 50, 0.0, 500.0) );
  hSelectedJetPt.push_back( fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsThirdJetPt"  , "Third light-jet pT;p_{T} (GeV/c);Events / %.0f GeV/c"  , 50, 0.0, 500.0) );
  hSelectedJetPt.push_back( fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsFourthJetPt" , "Fourth light-jet pT;p_{T} (GeV/c);Events / %.0f GeV/c" , 50, 0.0, 500.0) );

  hSelectedJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsFirstJetEta" , "First light-jet #eta;#eta;Events / %.2f"  , 50, -2.5, +2.5) );
  hSelectedJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsSecondJetEta", "Second light-jet #eta;#eta;Events / %.2f" , 50, -2.5, +2.5) );
  hSelectedJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsThirdJetEta" , "Third light-jet #eta;#eta;Events / %.2f"  , 50, -2.5, +2.5) );
  hSelectedJetEta.push_back(fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "selectedJetsFourthJetEta", "Fourth light-jet #eta;#eta;Events / %.2f" , 50, -2.5, +2.5) );

  return;
}

LightJetSelection::Data LightJetSelection::silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, jetData, bjetData);
  enableHistogramsAndCounters();
  return myData;
}

LightJetSelection::Data LightJetSelection::analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureAnalyzeAllowed(event.eventID());
  LightJetSelection::Data data = privateAnalyze(event, jetData, bjetData);
  // Send data to CommonPlots
  // if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtLightJetSelection(event, data); //fixme
  return data;
}

LightJetSelection::Data LightJetSelection::privateAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  Data output;
  cSubAll.increment();
  bool passedEta = false;
  bool passedPt  = false;
  int nLightJets = jetData.getNumberOfSelectedJets() - bjetData.getNumberOfSelectedBJets();

  // Loop over jets
  for(Jet jet: event.jets()) {

    //=== Skip b-tagged jets
    if ( isBJet(jet, bjetData.getSelectedBJets(), fBjetMatchingDeltaR) ) continue;

    // Fill histos
    hJetPtAll->Fill(jet.pt());
    hJetEtaAll->Fill(jet.eta());


    //=== Apply cut on eta
    if (std::fabs(jet.eta()) > fJetEtaCut) continue;
    passedEta = true;

    //=== Apply cut on pt
    if (jet.pt() < fJetPtCut) continue;
    passedPt = true;

    // Jet passed all cuts
    output.fSelectedLJets.push_back(jet);
    hJetPtPassed->Fill(jet.pt());
    hJetEtaPassed->Fill(jet.eta());
  }

  // Fill counters so far
  if (passedEta) cSubPassedEta.increment();
  if (passedPt) cSubPassedPt.increment();

  //=== Apply cut on number of light-jets
  if (!fNumberOfJetsCut.passedCut(nLightJets)) return output;
  cSubPassedJetCount.increment();

  // Sort jets by pT (descending order)
  std::sort(output.fSelectedLJets.begin(), output.fSelectedLJets.end());

  //=== Passed all light-jet selections
  output.bPassedSelection = true;
  cPassedLightJetSelection.increment();

  // Fill pt and eta of jets
  size_t i = 0;
  for (Jet jet: output.fSelectedLJets) {
    if (i < 4) {
      hSelectedJetPt[i]->Fill(jet.pt());
      hSelectedJetEta[i]->Fill(jet.eta());
    }
    ++i;
  }


  // Return data object
  return output;
}

    
bool LightJetSelection::isBJet(const Jet& jet, const std::vector<Jet>& bjets, const float dR_match){
  
  for (auto bjet: bjets) {
    float dR = ROOT::Math::VectorUtil::DeltaR(jet.p4(), bjet.p4());
    if (dR <= dR_match) return true;
  }

  return false;
}
