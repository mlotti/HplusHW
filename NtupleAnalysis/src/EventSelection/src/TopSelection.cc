// -*- c++ -*-
#include "EventSelection/interface/TopSelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"
//#include "Framework/interface/makeTH.h"

#include "Math/VectorUtil.h"

TopSelection::Data::Data()
: bPassedSelection(false),
  fJet1_p4(),
  fJet2_p4(),
  fJet3_p4(),
  fJet4_p4(),
  fBJet1_p4(),
  fBJet2_p4(),
  fChiSqr(-1.0)
{ }

TopSelection::Data::~Data() { }


TopSelection::TopSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
  : BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
    // Input parameters
    fMassW(config.getParameter<float>("MassW")),
    fdiJetSigma(config.getParameter<float>("DiJetSigma")),
    ftriJetSigma(config.getParameter<float>("TriJetSigma")),
    fChiSqrCut(config, "ChiSqrCut"),
    // Event counter for passing selection
    cPassedTopSelection(fEventCounter.addCounter("passed top selection ("+postfix+")")),
    // Sub counters
    cSubAll(fEventCounter.addSubCounter("top selection ("+postfix+")", "All events")),
    cSubPassedChiSqCut(fEventCounter.addSubCounter("top selection ("+postfix+")", "Passed chiSq cut"))
{
  initialize(config);
}

TopSelection::TopSelection(const ParameterSet& config)
: BaseSelection(),
  // Input parameters
  fMassW(config.getParameter<float>("MassW")),
  fdiJetSigma(config.getParameter<float>("DiJetSigma")),
  ftriJetSigma(config.getParameter<float>("TriJetSigma")),
  fChiSqrCut(config, "ChiSqrCut"),
  // Event counter for passing selection
  cPassedTopSelection(fEventCounter.addCounter("passed top selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("top selection", "All events")),
  cSubPassedChiSqCut(fEventCounter.addSubCounter("top selection", "Passed a cut"))
{
  initialize(config);
  bookHistograms(new TDirectory());
}

TopSelection::~TopSelection() {
  
}

void TopSelection::initialize(const ParameterSet& config) {
  
}

void TopSelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "topSelection_"+sPostfix);

  // Histograms (1D) 
  // hJetPtAll = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "jetPtAll", "Jet pT, all", 40, 0, 400);
  // fixme: add pt and eta of all jets involved
  // fimxe: add mass distributions of both tops
  // fixme: add chi-square value
  // fixme: add more relevant distributions (W-mass?)

  // Histograms (2D) 
  // fixme: add more relevant distributions (chiSq Vs mass?)

  return;
}

TopSelection::Data TopSelection::silentAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, jetData, bjetData);
  enableHistogramsAndCounters();
  return myData;
}

TopSelection::Data TopSelection::analyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  ensureAnalyzeAllowed(event.eventID());
  TopSelection::Data data = privateAnalyze(event, jetData, bjetData);

  // Send data to CommonPlots
  // if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtTopSelection(event, data);
  
  // Return data
  return data;
}

TopSelection::Data TopSelection::privateAnalyze(const Event& event, const JetSelection::Data& jetData, const BJetSelection::Data& bjetData) {
  Data output;
  cSubAll.increment();
  
  double minChiSqr = -1.0;

  // For-loop: Selected jets
  for (auto jet1: jetData.getSelectedJets()) {

    // Skip this jet if it is a b-jet
    if (matchesToBJet(jet1, bjetData)) continue; 


    // For-loop: Selected jets
    for (auto jet2: jetData.getSelectedJets()) {
      
      // Skip this jet if it is a b-jet
      if (matchesToBJet(jet2, bjetData)) continue;      
      // Skip this jet if it matches jet1
      if (sameJets(jet2, jet1)) continue;


      // For-loop: Selected jets
      for (auto jet3: jetData.getSelectedJets()) {
	
	// Skip this jet if it is a b-jet
	if (matchesToBJet(jet3, bjetData)) continue;
	// Skip this jet if it matches jet1 or jet2
	if (sameJets(jet3, jet1) || sameJets(jet3, jet2)) continue;


	// For-loop: Selected jets 
	for (auto jet4: jetData.getSelectedJets()) {

	  // Skip this jet if it is a b-jet	  
	  if (matchesToBJet(jet4, bjetData)) continue;
	  // Skip this jet if it matches jet1 or jet2 or jet3
	  if (sameJets(jet4, jet1) || sameJets(jet4, jet2) || sameJets(jet4, jet3)) continue;


	  // For-loop: Selected b-jets
	  for (auto bjet1: bjetData.getSelectedBJets()) {


	    // For-loop: Selected b-jets
	    for (auto bjet2: bjetData.getSelectedBJets()) {

	      // Skip this jet if it matched bjet1
	      if (sameJets(bjet1, bjet2)) continue;
	      
	      // Construct chi-square variable using jets(1-4) nd b-jets(1-2)
	      double ChiSqr = CalculateChiSqrForTriJetSystems(jet1, jet2, jet3, jet4, bjet1, bjet2);

	      // Find the configuration that minimised chi-sqrt
	      if (minChiSqr == -1 || ChiSqr < minChiSqr) {

		minChiSqr = ChiSqr;
		
		// Assign values
		output.fJet1_p4  = jet1.p4();
		output.fJet2_p4  = jet2.p4();
		output.fJet3_p4  = jet3.p4();
		output.fJet4_p4  = jet4.p4();
		output.fBJet1_p4 = bjet1.p4();
		output.fBJet2_p4 = bjet2.p4();
		output.fChiSqr   = minChiSqr;

	      }//eof: if (minChiSqr == -1 || ChiSqr < minChiSqr) {	            
	    } //eof: bjets2 loop
	  }  //eof: bjets1 loop
	} //eof: jets4 loop
      } //eof: jets3 loop
    } //eof: jets2 loop
  } //eof: jets1 loop

  // Apply cuts
  if ( !fChiSqrCut.passedCut(output.fChiSqr) ) return output;
  cSubPassedChiSqCut.increment();

  // Passed all top selection cuts
  output.bPassedSelection = true;
  cPassedTopSelection.increment();
  
  // Return data object
  return output;
}


bool TopSelection::matchesToBJet(const Jet& jet, const BJetSelection::Data& bjetData) const {
  for (auto bjet: bjetData.getSelectedBJets()) {
    if (std::abs(jet.pt()-bjet.pt()) < 0.0001 && std::abs(jet.eta()-bjet.eta()) < 0.0001)
      return true;
  }
  return false;
}


bool TopSelection::sameJets(const Jet& jet1, const Jet& jet2) {
  if (std::abs(jet1.pt()-jet2.pt()) < 0.0001 && std::abs(jet1.eta()-jet2.eta()) < 0.0001)
    return true;

  return false;
}


double TopSelection::CalculateChiSqrForTriJetSystems(const Jet& jet1, 
						     const Jet& jet2,
						     const Jet& jet3, 
						     const Jet& jet4,
						     const Jet& bjet1,
						     const Jet& bjet2) {

  // Known mass of W-boson (default: 80.385)
  const double massW = fMassW;

  // Varianace of the gaussian fitting of the mass of the diJet system (default: 10.2)
  const double diJetSigma  = fdiJetSigma;

  // Varianace of the gaussian fitting of the mass difference of the 2 triJet systems (default: 27.2)
  const double triJetSigma = ftriJetSigma;

  // Calculate the chi-sqruare of the two trijet systems
  double a = pow(( (jet1.p4() + jet2.p4()).mass()  - massW),2)/pow(diJetSigma, 2);
  double b = pow(( (jet3.p4() + jet4.p4()).mass()  - massW),2)/pow(diJetSigma, 2); 
  double c = pow(( (jet1.p4() + jet2.p4() + bjet1.p4()).mass() - (jet3.p4() + jet4.p4() + bjet2.p4()).mass()),2)/pow(triJetSigma, 2);
  double chiSqr = a + b + c;

  return chiSqr;
}
