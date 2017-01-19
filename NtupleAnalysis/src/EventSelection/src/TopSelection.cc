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
  fDiJet1_p4(),
  fDiJet2_p4(),
  fTriJet1_p4(),
  fTriJet2_p4(),
  fChiSqr(-1.0),
  fBJet3_p4()
{ }

TopSelection::Data::~Data() { }


TopSelection::TopSelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
  : BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
    // Input parameters
    cfg_MassW(config.getParameter<float>("MassW")),
    cfg_diJetSigma(config.getParameter<float>("DiJetSigma")),
    cfg_triJetSigma(config.getParameter<float>("TriJetSigma")),
    cfg_ChiSqrCut(config, "ChiSqrCut"),
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
  cfg_MassW(config.getParameter<float>("MassW")),
  cfg_diJetSigma(config.getParameter<float>("DiJetSigma")),
  cfg_triJetSigma(config.getParameter<float>("TriJetSigma")),
  cfg_ChiSqrCut(config, "ChiSqrCut"),
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

  // Fixed binning
  const int nBinsPt    = 50;
  const double minPt   = 0.0;
  const double maxPt   = 500.0;
  const int nBinsEta   = 50;
  const double minEta  = -5.0;
  const double maxEta  = 5.0;
  const int nBinsM     = 50;
  const double minM    = 0.0;
  const double maxM    = 500.0;
  const int nBinsdEta  = 50;
  const double mindEta = 0.0;
  const double maxdEta = 10.0;
  const int nBinsdPhi  = 32;
  const double mindPhi = 0.0;
  const double maxdPhi = 3.2;
  const int nBinsdR    = 50;
  const double mindR   = 0.0;
  const double maxdR   = 10.0;

  // Histograms (1D) 
  h_JetPtAll_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "JetPtAll_Before"  , "'p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_JetPtAll_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "JetPtAll_After"   , ";p_{T} (GeV/c)", nBinsPt, minPt, maxPt);
  h_JetEtaAll_Before  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "JetEtaAll_Before" , ";#eta", nBinsEta, minEta, maxEta);
  h_JetEtaAll_After   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "JetEtaAll_After"  , ";#eta", nBinsEta, minEta, maxEta);
  h_TriJetMass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "TriJetMass_Before", ";M (GeV/c^{2})", nBinsM, minM, maxM);
  h_TriJetMass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "TriJetMass_After" , ";M (GeV/c^{2})", nBinsM, minM, maxM);
  h_LdgTriJetMass_Before    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "LdgTriJetMass_Before"   ,";M (GeV/c^{2})", nBinsM, minM, maxM);
  h_LdgTriJetMass_After     = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "LdgTriJetMass_After"    ,";M (GeV/c^{2})", nBinsM, minM, maxM);
  h_SubLdgTriJetMass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "SubLdgTriJetMass_Before",";M (GeV/c^{2})", nBinsM, minM, maxM);
  h_SubLdgTriJetMass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "SubLdgTriJetMass_After" ,";M (GeV/c^{2})", nBinsM, minM, maxM);
  h_ClosestTo3rdBJet_TriJetMass_Before  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "ClosestTo3rdBJet_TriJetMass_Before" , ";M (GeV/c^{2})", nBinsM, minM, maxM);
  h_ClosestTo3rdBJet_TriJetMass_After   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "ClosestTo3rdBJet_TriJetMass_After"  , ";M (GeV/c^{2})", nBinsM, minM, maxM);
  h_FurthestTo3rdBJet_TriJetMass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FurthestTo3rdBJet_TriJetMass_Before", ";M (GeV/c^{2})", nBinsM, minM, maxM);
  h_FurthestTo3rdBJet_TriJetMass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "FurthestTo3rdBJet_TriJetMass_After" , ";M (GeV/c^{2})", nBinsM, minM, maxM);
  h_ChiSqr_Before    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "ChiSqr_Before"   , ";#chi^{2}"     ,    100,  0.0, 100.0);
  h_DiJetMass_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJetMass_Before", ";M (GeV/c^{2})", nBinsM, minM, maxM);
  h_DiJetMass_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJetMass_After" , ";M (GeV/c^{2})", nBinsM, minM, maxM);
  
  // dR, dPhi, dEta of jets from same W
  h_DiJet_DR_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJet_DR_Before"  , ";#Delta R(j_{1},j_{2})"  , nBinsdR  , mindR  , maxdR);
  h_DiJet_DR_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJet_DR_After"   , ";#Delta R(j_{1},j_{2})"  , nBinsdR  , mindR  , maxdR);
  h_DiJet_DPhi_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJet_DPhi_Before", ";#Delta#phi(j_{1},j_{2})", nBinsdPhi, mindPhi, maxdPhi);
  h_DiJet_DPhi_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJet_DPhi_After" , ";#Delta#phi(j_{1},j_{2})", nBinsdPhi, mindPhi, maxdPhi);
  h_DiJet_DEta_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJet_DEta_Before", ";#Delta#eta(j_{1},j_{2})", nBinsdEta, mindEta, maxdEta);
  h_DiJet_DEta_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJet_DEta_After" , ";#Delta#eta(j_{1},j_{2})", nBinsdEta, mindEta, maxdEta);
  
  // dR, dPhi, dEta of dijet(W) and the corresponding bjet from top 
  h_DiJetBJet_DR_Before   = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJetBJet_DR_Before"  , "#Delta R(dijet,bjet)"  , nBinsdR  , mindR  , maxdR);
  h_DiJetBJet_DR_After    = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJetBJet_DR_After"   , "#Delta R(dijet,bjet)"  , nBinsdR  , mindR  , maxdR);
  h_DiJetBJet_DPhi_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJetBJet_DPhi_Before", "#Delta#phi(dijet,bjet)", nBinsdPhi, mindPhi, maxdPhi);
  h_DiJetBJet_DPhi_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJetBJet_DPhi_After" , "#Delta#phi(dijet,bjet)", nBinsdPhi, mindPhi, maxdPhi);
  h_DiJetBJet_DEta_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJetBJet_DEta_Before", "#Delta#eta(dijet,bjet)", nBinsdEta, mindEta, maxdEta);
  h_DiJetBJet_DEta_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kDebug, subdir, "DiJetBJet_DEta_After" , "#Delta#eta(dijet,bjet)", nBinsdEta, mindEta, maxdEta);

  // Histograms (2D) 
  h_TriJetMass_Vs_ChiSqr_Before = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, "TriJetMass_Vs_ChiSqr_Before", ";M (GeV/c^{2}); #chi^{2}", nBinsM, minM, maxM, 100, 0.0, 100.0);
  h_DiJetPt_Vs_DiJetDR_Before   = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, "DiJetPt_Vs_DiJetDR_Before"  , ";p_{T} (GeV/c);#Delta R(j_{1},j_{2}", nBinsPt, minPt, maxPt, nBinsdR, mindR, maxdR);
  h_DiJetPt_Vs_DiJetDR_After    = fHistoWrapper.makeTH<TH2F>(HistoLevel::kDebug, subdir, "DiJetPt_Vs_DiJetDR_After"   , ";p_{T} (GeV/c);#Delta R(j_{1},j_{2}", nBinsPt, minPt, maxPt, nBinsdR, mindR, maxdR);

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
  
  // Initialise variables
  double minChiSqr = -1.0;
  unsigned int nUntaggedJets = jetData.getNumberOfSelectedJets() - bjetData.getNumberOfSelectedBJets();


  // For-loop: Selected jets
  for (auto jet1: jetData.getSelectedJets()) {

    // Skip this jet if it is a b-jet and if there are enough untagged jets
    if (matchesToBJet(jet1, bjetData) && nUntaggedJets >= 4) continue; 

    // For-loop: Selected jets
    for (auto jet2: jetData.getSelectedJets()) {
      
      // Skip this jet if it is a b-jet and if there are enough untagged jets
      if (matchesToBJet(jet2, bjetData) && nUntaggedJets >= 4) continue;      

      // Skip this jet if it matches jet1
      if (sameJets(jet2, jet1)) continue;

      // For-loop: Selected jets
      for (auto jet3: jetData.getSelectedJets()) {
	
	// Skip this jet if it is a b-jet and if there are enough untagged jets
	if (matchesToBJet(jet3, bjetData) && nUntaggedJets >= 4) continue;

	// Skip this jet if it matches jet1 or jet2
	if (sameJets(jet3, jet1) || sameJets(jet3, jet2)) continue;

	// For-loop: Selected jets 
	for (auto jet4: jetData.getSelectedJets()) {

	  // Skip this jet if it is a b-jet and if there are enough untagged jets  
	  if (matchesToBJet(jet4, bjetData) && nUntaggedJets >= 4) continue;

	  // Skip this jet if it matches jet1 or jet2 or jet3
	  if (sameJets(jet4, jet1) || sameJets(jet4, jet2) || sameJets(jet4, jet3)) continue;

	  // For-loop: Selected b-jets
	  for (auto bjet1: bjetData.getSelectedBJets()) {

	    // Skip this jet if it matches jet1, jet2, jet3 or jet4
	    if (sameJets(bjet1, jet1) || sameJets(bjet1, jet2) || 
		sameJets(bjet1, jet3) || sameJets(bjet1, jet4)  ) continue;

	    // For-loop: Selected b-jets
	    for (auto bjet2: bjetData.getSelectedBJets()) {

	      // Skip this jet if it matches jet1, jet2, jet3, jet4 or bjet1
	      if (sameJets(bjet2, jet1) || sameJets(bjet2, jet2) ||
		  sameJets(bjet2, jet3) || sameJets(bjet2, jet4) || sameJets(bjet2, bjet1) ) continue;
	            
	      // In case where b-tagged Jets are assigned to jet1-jet4, their b-Discriminator values 
	      // must be worse than those of bjet1 and bjet2
	      if (jet1.bjetDiscriminator() > bjet1.bjetDiscriminator() || jet1.bjetDiscriminator() > bjet2.bjetDiscriminator() ||
		  jet2.bjetDiscriminator() > bjet1.bjetDiscriminator() || jet2.bjetDiscriminator() > bjet2.bjetDiscriminator() ||
		  jet3.bjetDiscriminator() > bjet1.bjetDiscriminator() || jet3.bjetDiscriminator() > bjet2.bjetDiscriminator() ||
		  jet4.bjetDiscriminator() > bjet1.bjetDiscriminator() || jet4.bjetDiscriminator() > bjet2.bjetDiscriminator()  ) {
		continue; }
	      
	      // Construct chi-square variable using jets(1-4) and b-jets(1-2)
              double ChiSqr = CalculateChiSqrForTriJetSystems(jet1, jet2, jet3, jet4, bjet1, bjet2);

	      // Find the configuration that minimised chi-sqrt
	      if (minChiSqr == -1 || ChiSqr < minChiSqr) {

		minChiSqr = ChiSqr;
		
		// 4-momenta of the 3rd b-jet
		math::XYZTLorentzVector BJet3_p4;
		
		// For-loop: Selected b-jets 
		for (auto bjet3: bjetData.getSelectedBJets()) {
		  
		  // Skip this jet if it matches jet1, jet2, jet3, jet4, bjet1 or bjet2
		  if (sameJets(bjet3, jet1)  || sameJets(bjet3, jet2)  ||
		      sameJets(bjet3, jet3)  || sameJets(bjet3, jet4)  ||
		      sameJets(bjet3, bjet1) || sameJets(bjet3, bjet2)  ) continue;

		  // keep the b-jet with tha maximum pT               
		  if (bjet3.pt() > BJet3_p4.pt()) BJet3_p4 = bjet3.p4();
		}
		
		// Assign values
                output.fJet1_p4    = jet1.p4();
                output.fJet2_p4    = jet2.p4();
                output.fJet3_p4    = jet3.p4();
                output.fJet4_p4    = jet4.p4();
                output.fBJet1_p4   = bjet1.p4();
                output.fBJet2_p4   = bjet2.p4();
		output.fDiJet1_p4  = jet1.p4() + jet2.p4();
                output.fDiJet2_p4  = jet3.p4() + jet4.p4();
                output.fTriJet1_p4 = jet1.p4() + jet2.p4() + bjet1.p4();
                output.fTriJet2_p4 = jet3.p4() + jet4.p4() + bjet2.p4();
                output.fChiSqr     = minChiSqr;
		output.fBJet3_p4   = BJet3_p4;
		
	      }//eof: if (minChiSqr == -1 || ChiSqr < minChiSqr) {            
	    } //eof: bjets2 loop
	  } //eof: bjets1 loop
	} //eof: jets4 loop
      } //eof: jets3 loop
    } //eof: jets2 loop
  } //eof: jets1 loop
  
  // Fill Histograms (Before cuts)
  h_JetPtAll_Before->Fill(output.fJet1_p4.pt());
  h_JetPtAll_Before->Fill(output.fJet2_p4.pt());
  h_JetPtAll_Before->Fill(output.fJet3_p4.pt());
  h_JetPtAll_Before->Fill(output.fJet4_p4.pt());
  h_JetPtAll_Before->Fill(output.fBJet1_p4.pt());
  h_JetPtAll_Before->Fill(output.fBJet2_p4.pt());
  h_JetEtaAll_Before->Fill(output.fJet1_p4.eta());
  h_JetEtaAll_Before->Fill(output.fJet2_p4.eta());
  h_JetEtaAll_Before->Fill(output.fJet3_p4.eta());
  h_JetEtaAll_Before->Fill(output.fJet4_p4.eta());
  h_JetEtaAll_Before->Fill(output.fBJet1_p4.eta());
  h_JetEtaAll_Before->Fill(output.fBJet2_p4.eta());
  h_TriJetMass_Before->Fill(output.fTriJet1_p4.mass());
  h_TriJetMass_Before->Fill(output.fTriJet2_p4.mass());
  // Leading/Ssubleading top
  if (output.fTriJet1_p4.pt() > output.fTriJet2_p4.pt()) {
    h_LdgTriJetMass_Before    ->Fill(output.fTriJet1_p4.mass());
    h_SubLdgTriJetMass_Before ->Fill(output.fTriJet2_p4.mass());
  }
  else {
    h_LdgTriJetMass_Before    ->Fill(output.fTriJet2_p4.mass());
    h_SubLdgTriJetMass_Before ->Fill(output.fTriJet1_p4.mass());
  }
  // Closest/furthest top to the 3rd bjet
  if (output.fBJet3_p4.pt() != 0) {
    if ( ROOT::Math::VectorUtil::DeltaR(output.fTriJet1_p4, output.fBJet3_p4) < ROOT::Math::VectorUtil::DeltaR(output.fTriJet2_p4, output.fBJet3_p4)    ) {
      h_ClosestTo3rdBJet_TriJetMass_Before  ->Fill(output.fTriJet1_p4.mass());
      h_FurthestTo3rdBJet_TriJetMass_Before ->Fill(output.fTriJet2_p4.mass());
    }
    else {
      h_ClosestTo3rdBJet_TriJetMass_Before  ->Fill(output.fTriJet2_p4.mass());
      h_FurthestTo3rdBJet_TriJetMass_Before ->Fill(output.fTriJet1_p4.mass());
    }
  }
  h_ChiSqr_Before->Fill(output.fChiSqr);
  h_DiJetMass_Before->Fill(output.fDiJet1_p4.mass());
  h_DiJetMass_Before->Fill(output.fDiJet2_p4.mass());
  h_DiJet_DR_Before  ->Fill(ROOT::Math::VectorUtil::DeltaR(output.fJet1_p4, output.fJet2_p4));
  h_DiJet_DR_Before  ->Fill(ROOT::Math::VectorUtil::DeltaR(output.fJet3_p4, output.fJet4_p4));
  h_DiJet_DPhi_Before->Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fJet1_p4, output.fJet2_p4)));
  h_DiJet_DPhi_Before->Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fJet3_p4, output.fJet4_p4)));
  h_DiJet_DEta_Before->Fill(std::abs(output.fJet1_p4.eta() - output.fJet2_p4.eta()));
  h_DiJet_DEta_Before->Fill(std::abs(output.fJet3_p4.eta() - output.fJet4_p4.eta()));
  h_DiJetBJet_DR_Before   ->Fill(ROOT::Math::VectorUtil::DeltaR(output.fDiJet1_p4, output.fBJet1_p4));
  h_DiJetBJet_DR_Before   ->Fill(ROOT::Math::VectorUtil::DeltaR(output.fDiJet2_p4, output.fBJet2_p4));
  h_DiJetBJet_DPhi_Before ->Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fDiJet1_p4, output.fBJet1_p4)));
  h_DiJetBJet_DPhi_Before ->Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fDiJet2_p4, output.fBJet2_p4)));
  h_DiJetBJet_DEta_Before ->Fill(std::abs(output.fDiJet1_p4.eta() - output.fBJet1_p4.eta()));
  h_DiJetBJet_DEta_Before ->Fill(std::abs(output.fDiJet2_p4.eta() - output.fBJet2_p4.eta()));
  h_TriJetMass_Vs_ChiSqr_Before ->Fill(output.fTriJet1_p4.mass(), output.fChiSqr);
  h_TriJetMass_Vs_ChiSqr_Before ->Fill(output.fTriJet2_p4.mass(), output.fChiSqr);
  h_DiJetPt_Vs_DiJetDR_Before ->Fill(output.fDiJet1_p4.pt(), ROOT::Math::VectorUtil::DeltaR(output.fJet1_p4, output.fJet2_p4));
  h_DiJetPt_Vs_DiJetDR_Before ->Fill(output.fDiJet2_p4.pt(), ROOT::Math::VectorUtil::DeltaR(output.fJet3_p4, output.fJet4_p4));


  // Apply cuts
  if ( !cfg_ChiSqrCut.passedCut(output.fChiSqr) ) return output;
  cSubPassedChiSqCut.increment();

  // Fill Histograms (After cuts)
  h_JetPtAll_After->Fill(output.fJet1_p4.pt());
  h_JetPtAll_After->Fill(output.fJet2_p4.pt());
  h_JetPtAll_After->Fill(output.fJet3_p4.pt());
  h_JetPtAll_After->Fill(output.fJet4_p4.pt());
  h_JetPtAll_After->Fill(output.fBJet1_p4.pt());
  h_JetPtAll_After->Fill(output.fBJet2_p4.pt());
  h_JetEtaAll_After->Fill(output.fJet1_p4.eta());
  h_JetEtaAll_After->Fill(output.fJet2_p4.eta());
  h_JetEtaAll_After->Fill(output.fJet3_p4.eta());
  h_JetEtaAll_After->Fill(output.fJet4_p4.eta());
  h_JetEtaAll_After->Fill(output.fBJet1_p4.eta());
  h_JetEtaAll_After->Fill(output.fBJet2_p4.eta());
  h_TriJetMass_After->Fill(output.fTriJet1_p4.mass());
  h_TriJetMass_After->Fill(output.fTriJet2_p4.mass());
  if (output.fTriJet1_p4.pt() > output.fTriJet2_p4.pt()) {
    h_LdgTriJetMass_After    ->Fill(output.fTriJet1_p4.mass());
    h_SubLdgTriJetMass_After ->Fill(output.fTriJet2_p4.mass());
  }
  else {
    h_LdgTriJetMass_After    ->Fill(output.fTriJet2_p4.mass());
    h_SubLdgTriJetMass_After ->Fill(output.fTriJet1_p4.mass());
  }
  if (output.fBJet3_p4.pt() != 0) {
    if ( ROOT::Math::VectorUtil::DeltaR(output.fTriJet1_p4, output.fBJet3_p4) < \
	 ROOT::Math::VectorUtil::DeltaR(output.fTriJet2_p4, output.fBJet3_p4)    ) {
      h_ClosestTo3rdBJet_TriJetMass_After  ->Fill(output.fTriJet1_p4.mass());
      h_FurthestTo3rdBJet_TriJetMass_After ->Fill(output.fTriJet2_p4.mass());
    }
    else {
      h_ClosestTo3rdBJet_TriJetMass_After  ->Fill(output.fTriJet2_p4.mass());
      h_FurthestTo3rdBJet_TriJetMass_After ->Fill(output.fTriJet1_p4.mass());
    }
  }
  h_DiJetMass_After ->Fill(output.fDiJet1_p4.mass());
  h_DiJetMass_After ->Fill(output.fDiJet2_p4.mass());
  h_DiJet_DR_After  ->Fill(ROOT::Math::VectorUtil::DeltaR(output.fJet1_p4, output.fJet2_p4));
  h_DiJet_DR_After  ->Fill(ROOT::Math::VectorUtil::DeltaR(output.fJet3_p4, output.fJet4_p4));
  h_DiJet_DPhi_After->Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fJet1_p4, output.fJet2_p4)));
  h_DiJet_DPhi_After->Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fJet3_p4, output.fJet4_p4)));
  h_DiJet_DEta_After->Fill(std::abs(output.fJet1_p4.eta() - output.fJet2_p4.eta()));
  h_DiJet_DEta_After->Fill(std::abs(output.fJet3_p4.eta() - output.fJet4_p4.eta()));
  h_DiJetBJet_DR_After  ->Fill(ROOT::Math::VectorUtil::DeltaR(output.fDiJet1_p4, output.fBJet1_p4));
  h_DiJetBJet_DR_After  ->Fill(ROOT::Math::VectorUtil::DeltaR(output.fDiJet2_p4, output.fBJet2_p4));
  h_DiJetBJet_DPhi_After->Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fDiJet1_p4, output.fBJet1_p4)));
  h_DiJetBJet_DPhi_After->Fill(std::abs(ROOT::Math::VectorUtil::DeltaPhi(output.fDiJet2_p4, output.fBJet2_p4)));
  h_DiJetBJet_DEta_After->Fill(std::abs(output.fDiJet1_p4.eta() - output.fBJet1_p4.eta()));
  h_DiJetBJet_DEta_After->Fill(std::abs(output.fDiJet2_p4.eta() - output.fBJet2_p4.eta()));
  h_DiJetPt_Vs_DiJetDR_After->Fill(output.fDiJet1_p4.pt(), ROOT::Math::VectorUtil::DeltaR(output.fJet1_p4, output.fJet2_p4));
  h_DiJetPt_Vs_DiJetDR_After->Fill(output.fDiJet2_p4.pt(), ROOT::Math::VectorUtil::DeltaR(output.fJet3_p4, output.fJet4_p4));

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
  const double massW = cfg_MassW;

  // Varianace of the gaussian fitting of the mass of the diJet system (default: 10.2)
  const double diJetSigma = cfg_diJetSigma;

  // Varianace of the gaussian fitting of the mass difference of the 2 triJet systems (default: 27.2)
  const double triJetSigma = cfg_triJetSigma;

  // Calculate the chi-sqruare of the two trijet systems
  double a = pow(( (jet1.p4() + jet2.p4()).mass()  - massW),2)/pow(diJetSigma, 2);
  double b = pow(( (jet3.p4() + jet4.p4()).mass()  - massW),2)/pow(diJetSigma, 2); 
  double c = pow(( (jet1.p4() + jet2.p4() + bjet1.p4()).mass() - (jet3.p4() + jet4.p4() + bjet2.p4()).mass()),2)/pow(triJetSigma, 2);
  double chiSqr = a + b + c;

  return chiSqr;
}
