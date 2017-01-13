// -*- c++ -*-
#include "EventSelection/interface/TopologySelection.h"

#include "Framework/interface/ParameterSet.h"
#include "EventSelection/interface/CommonPlots.h"
#include "DataFormat/interface/Event.h"
#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"

#include "Math/VectorUtil.h"

TopologySelection::Data::Data()
: bPassedSelection(false),
  fSphericity(-1.0),
  fSphericityT(-1.0), 
  fAplanarity(-1.0),
  fPlanarity(-1.0), 
  fY(-1.0),
  fCircularity(-1.0),
  fY23(-1.0),
  fCparameter(-1.0),
  fDparameter(-1.0),
  fFoxWolframMoment(-1.0),
  fHT(-1.0),
  fJT(-1.0), 
  fMHT(-1.0),
  fCentrality(-1.0)
{ }

TopologySelection::Data::~Data() { }

TopologySelection::TopologySelection(const ParameterSet& config, EventCounter& eventCounter, HistoWrapper& histoWrapper, CommonPlots* commonPlots, const std::string& postfix)
: BaseSelection(eventCounter, histoWrapper, commonPlots, postfix),
  // Input parameters
  fSphericityCut(config, "SphericityCut"),
  fAplanarityCut(config, "AplanarityCut"),
  fPlanarityCut(config, "PlanarityCut"),
  fCircularityCut(config, "CircularityCut"),
  fY23Cut(config, "Y23Cut"),
  fCparameterCut(config, "CparameterCut"),
  fDparameterCut(config, "DparameterCut"),
  fFoxWolframMomentCut(config, "FoxWolframMomentCut"),
  fAlphaTCut(config, "AlphaTCut"),
  fCentralityCut(config, "CentralityCut"),
  // Event counter for passing selection
  cPassedTopologySelection(fEventCounter.addCounter("passed topology selection ("+postfix+")")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("topology selection ("+postfix+")", "All events")),
  cSubPassedSphericity(fEventCounter.addSubCounter("topology selection ("+postfix+")", "Passed Sphericity")),
  cSubPassedAplanarity(fEventCounter.addSubCounter("topology selection ("+postfix+")", "Passed Aplanarity")),
  cSubPassedPlanarity(fEventCounter.addSubCounter("topology selection ("+postfix+")", "Passed Planarity")),
  cSubPassedCircularity(fEventCounter.addSubCounter("topology selection ("+postfix+")", "Passed Circularity")),
  cSubPassedY23(fEventCounter.addSubCounter("topology selection ("+postfix+")", "Passed jet y23")),
  cSubPassedCparameter(fEventCounter.addSubCounter("topology selection ("+postfix+")", "Passed C")),
  cSubPassedDparameter(fEventCounter.addSubCounter("topology selection ("+postfix+")", "Passed D")),
  cSubPassedFoxWolframMoment(fEventCounter.addSubCounter("topology selection ("+postfix+")", "Passed H2")),
  cSubPassedAlphaT(fEventCounter.addSubCounter("topology selection ("+postfix+")", "Passed AlphaT")),
  cSubPassedCentrality(fEventCounter.addSubCounter("topology selection ("+postfix+")", "Passed Centrality"))
{ 
  initialize(config);
}

TopologySelection::TopologySelection(const ParameterSet& config)
: BaseSelection(),
  // Input parameters
  fSphericityCut(config, "SphericityCut"),
  fAplanarityCut(config, "AplanarityCut"),
  fPlanarityCut(config, "PlanarityCut"),
  fCircularityCut(config, "CircularityCut"),
  fY23Cut(config, "Y23Cut"),
  fCparameterCut(config, "CparameterCut"),
  fDparameterCut(config, "DparameterCut"),
  fFoxWolframMomentCut(config, "FoxWolframMomentCut"),
  fAlphaTCut(config, "AlphaTCut"),
  fCentralityCut(config, "CentralityCut"),
  // Event counter for passing selection
  cPassedTopologySelection(fEventCounter.addCounter("passed topology selection")),
  // Sub counters
  cSubAll(fEventCounter.addSubCounter("topology selection", "All events")),
  cSubPassedSphericity(fEventCounter.addSubCounter("topology selection", "Passed Sphericity")),
  cSubPassedAplanarity(fEventCounter.addSubCounter("topology selection", "Passed Aplanarity")),
  cSubPassedPlanarity(fEventCounter.addSubCounter("topology selection", "Passed Planarity")),
  cSubPassedCircularity(fEventCounter.addSubCounter("topology selection", "Passed Circularity")),
  cSubPassedY23(fEventCounter.addSubCounter("topology selection", "Passed jet y23")),
  cSubPassedCparameter(fEventCounter.addSubCounter("topology selection", "Passed C")),
  cSubPassedDparameter(fEventCounter.addSubCounter("topology selection", "Passed D")),
  cSubPassedFoxWolframMoment(fEventCounter.addSubCounter("topology selection", "Passed H2")),
  cSubPassedAlphaT(fEventCounter.addSubCounter("topology selection", "Passed AlphaT")),
  cSubPassedCentrality(fEventCounter.addSubCounter("topology selection", "Passed Centrality"))
{ 
  initialize(config);
  bookHistograms(new TDirectory());
}

TopologySelection::~TopologySelection() { 
  
  // Histograms (1D) 
  delete h_AlphaT_After;
  delete h_AlphaT_Before;
  delete h_Aplanarity_After;
  delete h_Aplanarity_Before;
  delete h_CParameter_After;
  delete h_CParameter_Before;
  delete h_Centrality_After;
  delete h_Centrality_Before;
  delete h_Circularity_After;
  delete h_Circularity_Before;
  delete h_DParameter_After;
  delete h_DParameter_Before;
  delete h_FoxWolframMoment_After;
  delete h_FoxWolframMoment_Before;
  delete h_HT_After;
  delete h_HT_Before;
  delete h_JT_After;
  delete h_JT_Before;
  delete h_MHT_After;
  delete h_MHT_Before;
  delete h_Planarity_After;
  delete h_Planarity_Before;
  delete h_SphericityT_After;
  delete h_SphericityT_Before;
  delete h_Sphericity_After;
  delete h_Sphericity_Before;
  delete h_Y_After;
  delete h_Y_Before;
  delete h_y23_After;
  delete h_y23_Before;

  // Histograms (2D)
  delete h_S_Vs_Y_Before;
  delete h_S_Vs_Y_After;


}

void TopologySelection::initialize(const ParameterSet& config) {
  
}

void TopologySelection::bookHistograms(TDirectory* dir) {
  TDirectory* subdir = fHistoWrapper.mkdir(HistoLevel::kDebug, dir, "topologySelection_"+sPostfix);

  // Histograms (1D)
  h_AlphaT_After            = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AlphaT_After"           , ";#alpha_{T}"    , 100, 0.0,    2.0);
  h_AlphaT_Before           = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "AlphaT_Before"          , ";#alpha_{T}"    , 100, 0.0,    2.0);
  h_Aplanarity_After        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Aplanarity_After"       , ";Aplanarity"    ,  25, 0.0,    0.5);
  h_Aplanarity_Before       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Aplanarity_Before"      , ";Aplanarity"    ,  25, 0.0,    0.5);
  h_CParameter_After        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "CParameter_After"       , ";C"             ,  20, 0.0,    1.0);
  h_CParameter_Before       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "CParameter_Before"      , ";C"             ,  20, 0.0,    1.0);
  h_Centrality_After        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Centrality_After"       , ";Centrality"    ,  20, 0.0,    1.0);
  h_Centrality_Before       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Centrality_Before"      , ";Centrality"    ,  20, 0.0,    1.0);
  h_Circularity_After       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Circularity_After"      , ";Circularity"   ,  20, 0.0,    1.0);
  h_Circularity_Before      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Circularity_Before"     , ";Circularity"   ,  20, 0.0,    1.0);
  h_DParameter_After        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "DParameter_After"       , ";D"             ,  20, 0.0,    1.0);
  h_DParameter_Before       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "DParameter_Before"      , ";D"             ,  20, 0.0,    1.0);
  h_FoxWolframMoment_After  = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "FoxWolframMoment_After" , ";H_{2}"         ,  20, 0.0,    1.0);
  h_FoxWolframMoment_Before = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "FoxWolframMoment_Before", ";H_{2}"         ,  20, 0.0,    1.0);
  h_HT_After                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "HT_After"               , ";H_{T}"         ,  30, 0.0, 1500.0);
  h_HT_Before               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "HT_Before"              , ";H_{T}"         ,  30, 0.0, 1500.0);
  h_JT_After                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "JT_After"               , ";J_{T}"         ,  30, 0.0, 1500.0);
  h_JT_Before               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "JT_Before"              , ";J_{T}"         ,  30, 0.0, 1500.0);
  h_MHT_After               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MHT_After"              , ";MHT"           ,  30, 0.0,  300.0);
  h_MHT_Before              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "MHT_Before"             , ";MHT"           ,  30, 0.0,  300.0);
  h_Planarity_After         = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Planarity_After"        , ";Planarity"     ,  25, 0.0,    0.5);
  h_Planarity_Before        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Planarity_Before"       , ";Planarity"     ,  25, 0.0,    0.5);
  h_SphericityT_After       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SphericityT_After"      , ";Sphericity_{T}",  20, 0.0,    1.00);
  h_SphericityT_Before      = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "SphericityT_Before"     , ";Sphericity_{T}",  20, 0.0,    1.00);
  h_Sphericity_After        = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Sphericity_After"       , ";Sphericity"    ,  20, 0.0,    1.00);
  h_Sphericity_Before       = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Sphericity_Before"      , ";Sphericity"    ,  20, 0.0,    1.00);
  h_Y_After                 = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Y_After"                , ";Y"             ,  50, 0.0,    0.50); 
  h_Y_Before                = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "Y_Before"               , ";Y"             ,  50, 0.0,    0.50); 
  h_y23_After               = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "y23_After"              , ";y_{23}"        ,  25, 0.0,    0.25);
  h_y23_Before              = fHistoWrapper.makeTH<TH1F>(HistoLevel::kVital, subdir, "y23_Before"             , ";y_{23}"        ,  25, 0.0,    0.25);
 
  // Histograms (2D)
  h_S_Vs_Y_After  = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "S_Vs_Y_After" , ";Sphericity;Y=#frac{#sqrt{3}}{2}x(Q1-Q2)", 100, 0.0, 1.0, 50, 0.0, 0.5);
  h_S_Vs_Y_Before = fHistoWrapper.makeTH<TH2F>(HistoLevel::kVital, subdir, "S_Vs_Y_Before", ";Sphericity;Y=#frac{#sqrt{3}}{2}x(Q1-Q2)", 100, 0.0, 1.0, 50, 0.0, 0.5);

  return;
}


TopologySelection::Data TopologySelection::silentAnalyze(const Event& event, const JetSelection::Data& jetData) {
  ensureSilentAnalyzeAllowed(event.eventID());
  // Disable histogram filling and counter
  disableHistogramsAndCounters();
  Data myData = privateAnalyze(event, jetData);
  enableHistogramsAndCounters();
  return myData;
}


TopologySelection::Data TopologySelection::analyze(const Event& event, const JetSelection::Data& jetData) {
  ensureAnalyzeAllowed(event.eventID());
  TopologySelection::Data data = privateAnalyze(event, jetData);

  // Send data to CommonPlots
  // if (fCommonPlots != nullptr) fCommonPlots->fillControlPlotsAtTopologySelection(event, data);

  // Return data
  return data;
}


TopologySelection::Data TopologySelection::privateAnalyze(const Event& event, const JetSelection::Data& jetData) {
  Data output;
  cSubAll.increment();

  std::vector<float> a = GetMomentumTensorEigenValues(jetData  , output);
  std::vector<float> b = GetMomentumTensorEigenValues2D(jetData, output);
  std::vector<float> c = GetSphericityTensorEigenValues(jetData, output);
  calculateAlphaT(jetData, output);

  // Fill Histograms
  h_y23_Before             ->Fill(output.fY23);
  h_Sphericity_Before      ->Fill(output.fSphericity);
  h_SphericityT_Before     ->Fill(output.fSphericityT);
  h_Y_Before               ->Fill(output.fY);
  h_S_Vs_Y_Before          ->Fill(output.fSphericity, output.fY);
  h_Aplanarity_Before      ->Fill(output.fAplanarity);
  h_Planarity_Before       ->Fill(output.fPlanarity);
  h_CParameter_Before      ->Fill(output.fCparameter);
  h_DParameter_Before      ->Fill(output.fDparameter);
  h_FoxWolframMoment_Before->Fill(output.fFoxWolframMoment);
  h_Circularity_Before     ->Fill(output.fCircularity);
  h_Centrality_Before      ->Fill(output.fCentrality);
  h_HT_Before              ->Fill(output.fHT);
  h_JT_Before              ->Fill(output.fJT);
  h_MHT_Before             ->Fill(output.fMHT);
  h_AlphaT_Before          ->Fill(output.fAlphaT);

  // Apply cuts
  if ( !fSphericityCut.passedCut(output.fSphericity) ) return output;
  cSubPassedSphericity.increment();
  
  if ( !fAplanarityCut.passedCut(output.fAplanarity) ) return output;
  cSubPassedAplanarity.increment();

  if ( !fPlanarityCut.passedCut(output.fPlanarity) ) return output;
  cSubPassedPlanarity.increment();

  if ( !fCircularityCut.passedCut(output.fCircularity) ) return output;
  cSubPassedCircularity.increment();

  if ( !fY23Cut.passedCut(output.fY23) ) return output;
  cSubPassedY23.increment();

  if ( !fCparameterCut.passedCut(output.fCparameter) ) return output;
  cSubPassedCparameter.increment();

  if ( !fDparameterCut.passedCut(output.fDparameter) ) return output;
  cSubPassedDparameter.increment();

  if ( !fFoxWolframMomentCut.passedCut(output.fFoxWolframMoment) ) return output;
  cSubPassedFoxWolframMoment.increment();

  if ( !fAlphaTCut.passedCut(output.fAlphaT) ) return output;
  cSubPassedAlphaT.increment();

  if ( !fCentralityCut.passedCut(output.fCentrality) ) return output;
  cSubPassedCentrality.increment();

  // Passed all topology selection cuts
  output.bPassedSelection = true;
  cPassedTopologySelection.increment();

  // Fill histos after all selections
  h_y23_After             ->Fill(output.fY23);
  h_Sphericity_After      ->Fill(output.fSphericity);
  h_SphericityT_After     ->Fill(output.fSphericityT);
  h_Y_After               ->Fill(output.fY);
  h_S_Vs_Y_After          ->Fill(output.fSphericity, output.fY);
  h_Aplanarity_After      ->Fill(output.fAplanarity);
  h_Planarity_After       ->Fill(output.fPlanarity);
  h_CParameter_After      ->Fill(output.fCparameter);
  h_DParameter_After      ->Fill(output.fDparameter);
  h_FoxWolframMoment_After->Fill(output.fFoxWolframMoment);
  h_Circularity_After     ->Fill(output.fCircularity);
  h_Centrality_After      ->Fill(output.fCentrality);
  h_HT_After              ->Fill(output.fHT);
  h_JT_After              ->Fill(output.fJT);
  h_MHT_After             ->Fill(output.fMHT);
  h_AlphaT_After          ->Fill(output.fAlphaT);


  // Return data object
  return output;
}


void TopologySelection::calculateAlphaT(const JetSelection::Data& jetData, Data& output){

  // Calculates the AlphaT variable, defined as an N-jets. This definition reproduces the kinematics of a 
  // di-jet system by constructing two pseudo-jets, which balance one another in Ht. 
  // The two pseudo-jets are formed from the combination of the N objects that minimizes the quantity
  // DeltaHt = |Ht_pseudoJet1 - Ht_pseudoJet2| of the pseudo-jets.                                             

  // Detailed Explanation: 
  // The method "alphaT()" of this class takes as input all jets in the event and uses them to form 
  // two Pseudo-Jets to describe the event. 
  // If there are NJets in a given event this means there are 2^{NJets-1} combinations to do this.
  // The methods does exactly that and for the combination which minimises the quantity
  // DeltaHt = Ht_PseudoJet1 - Ht_PseudoJet2,
  // it calculates the quantity alphaT.
  // The method "alphaT()" employs a double loop to recreate all the possilbe jet combinations 
  // out of NJets, by the use of an NJets-binary system. For example, if NJets=5, the loop
  // indices ("k" outside, "l" inside) run both from "k"=0 to "k"=2^{4}=16 . The upper limit of 
  // the outside loop is given by the expression:
  // 1<<(NJets-1)) = shift the number 1 by (NJets-1) positions to the left. 
  // So, for NJets=5  (i.e. 1  --> 1 0 0 0 0 ) 
  // This is now the way we will represent grouping into 2 Pseudo-Jets. The 0's represent one group and the 1's the other.
  // So, for example 1 0 0 0 0 means 1 jet forms Pseudo-Jet1 and 4 jets form Pseudo-Jet2. 
  // Also, for example, 1 0 0 1 0 means 2 jets form Pseudo-Jet1 and 3 jets form Pseudo-Jet2.
  // The inside loop performs a bitwise right shift of index "k" by "l" positions and then
  // compares the resulting bit to 1. So, for "k"=0, all the resulting comparisons in the 
  // inside loop will result to 0, except the one with "l"=4.
  // This gives the first combination: 0 0 0 0 0   ( i.e. 0 jets form Pseudo-Jet1 and 5 jets form Pseudo-Jet2 )
  // For "k"=1 (00000001 in 8bit representation), the first comparison is 1, since k is shifted by zero positions 
  // and then compared to 1. The rest comparisons yield zero, since by shifting the bit by any position and comparing to 1 gives zero. 
  // Thus, for "k"=1 we have after the second loop: 0 0 0 0 1
  // In the same manner, we get for "k"=2 (00000001 in 8bit representation) we have after the second loop: 0 0 0 1 0
  //
  // To summarise, for NJets=5 we have 16 combinations:
  // For "k"=0  ( 00000000 in 8bit representation) we have after the second loop: 0 0 0 0 0
  // For "k"=1  ( 00000001 in 8bit representation) we have after the second loop: 0 0 0 0 1
  // For "k"=2  ( 00000001 in 8bit representation) we have after the second loop: 0 0 0 1 0
  // For "k"=3  ( 00000011 in 8bit representation) we have after the second loop: 0 0 0 1 1
  // For "k"=4  ( 00000100 in 8bit representation) we have after the second loop: 0 0 1 0 0
  // For "k"=5  ( 00000101 in 8bit representation) we have after the second loop: 0 0 1 0 1
  // For "k"=6  ( 00000110 in 8bit representation) we have after the second loop: 0 0 1 1 0
  // For "k"=7  ( 00000111 in 8bit representation) we have after the second loop: 0 0 1 1 1
  // For "k"=8  ( 00001000 in 8bit representation) we have after the second loop: 0 1 0 0 0
  // For "k"=9  ( 00001001 in 8bit representation) we have after the second loop: 0 1 0 0 1
  // For "k"=10 ( 00010000 in 8bit representation) we have after the second loop: 0 1 0 0 0
  // For "k"=11 ( 00010001 in 8bit representation) we have after the second loop: 0 1 0 0 1
  // For "k"=12 ( 00010010 in 8bit representation) we have after the second loop: 0 1 0 1 0
  // For "k"=13 ( 00010011 in 8bit representation) we have after the second loop: 0 1 0 1 1
  // For "k"=14 ( 00010100 in 8bit representation) we have after the second loop: 0 1 1 0 0
  // For "k"=15 ( 00010101 in 8bit representation) we have after the second loop: 0 1 1 0 1
  // For "k"=16 ( 00010110 in 8bit representation) we have after the second loop: 0 1 1 1 0


  // Sanity Check
  unsigned int nJets = jetData.getSelectedJets().size();
  if ( nJets < 2 ) return;

  // Declare Auxiliary variables
  std::vector<float> vE, vEt, vPx, vPy, vPz;
  std::vector<bool> vPseudo_jet1;
  const bool bList = true;

  // For-Loop: All jets1
  for ( auto jet: jetData.getSelectedJets() )
    {
      // math::XYZTLorentzVector  jet.p4();
      vE.push_back( jet.p4().e() );
      vEt.push_back( jet.p4().Et() );
      vPx.push_back( jet.p4().px() );
      vPy.push_back( jet.p4().py() );
      vPz.push_back( jet.p4().pz() );
    }

  // Calculate sums
  float fSum_e  = accumulate( vE.begin() , vE.end() , 0.0 );
  float fSum_et = accumulate( vEt.begin(), vEt.end(), 0.0 );
  float fSum_px = accumulate( vPx.begin(), vPx.end(), 0.0 );
  float fSum_py = accumulate( vPy.begin(), vPy.end(), 0.0 );

  // Minimum Delta Et for two pseudo-jets
  float fMin_delta_sum_et = -1.0;

  // Iterate through different combinations
  for ( unsigned k=0; k < unsigned(1<<(nJets-1)); k++ ) { 
    float fDelta_sum_et = 0.0;
    std::vector<bool> jet;

    // For-loop: All jet ET Iterate through jets
    for ( unsigned l=0; l < vEt.size(); l++ ) { 
      /// Bitwise shift of "k" by "l" positions to the right and compare to 1 (&1)
      /// i.e.: fDelta_sum_et += vEt[l] * ( 1 - 2*0 );  if comparison is un-successful
      ///       fDelta_sum_et += vEt[l] * ( 1 - 2*1 );  if comparison is successful
      fDelta_sum_et += vEt[l] * ( 1 - 2 * (int(k>>l)&1) ); 
      if ( bList ) { jet.push_back( (int(k>>l)&1) == 0 ); } 
    }

    // Find configuration with minimum value of DeltaHt 
    if ( ( fabs(fDelta_sum_et) < fMin_delta_sum_et || fMin_delta_sum_et < 0.0 ) ) {
      fMin_delta_sum_et = fabs(fDelta_sum_et);
      if ( bList && jet.size() == vEt.size() ){vPseudo_jet1.resize(jet.size());}
    }

  }
    
  // Sanity check
  if ( fMin_delta_sum_et < 0.0 )
    { 
      throw hplus::Exception("LogicError") << "Minimum Delta(Sum_Et) is less than zero! fMin_delta_sum_et = " << fMin_delta_sum_et;
    }
  
  // Calculate Event-Shape Variables
  double dHT = fMin_delta_sum_et;

  // Assign values
  output.fHT         = fSum_et;
  output.fJT         = fSum_et - vEt.at(0); // Ht without considering the Ldg Jet of the Event
  output.fMHT        = sqrt(pow(fSum_px,2) + pow(fSum_py,2));
  output.fCentrality = fSum_et/fSum_e;
  output.fAlphaT     = ( 0.5 * ( output.fHT - dHT ) / sqrt( pow(output.fHT,2) - pow(output.fMHT,2) ) );

  if (0)
    {
      Table vars("Variable | Value | Definition", "Text"); //LaTeX or Text
      vars.AddRowColumn(0, "HT");
      vars.AddRowColumn(0, auxTools.ToString(output.fHT) );
      vars.AddRowColumn(0, "HT = Sum(Jet_Et)");
      //
      vars.AddRowColumn(1, "JT");
      vars.AddRowColumn(1, auxTools.ToString(output.fJT) );
      vars.AddRowColumn(1, "JT = Ht - Jet1_Et");
      //
      vars.AddRowColumn(2, "dHT");
      vars.AddRowColumn(2, auxTools.ToString(dHT) );
      vars.AddRowColumn(2, "DeltaHT = min[Delta(Pseudojet1_Et, Pseudojet2_Et)]");
      //
      vars.AddRowColumn(3, "MHT");
      vars.AddRowColumn(3, auxTools.ToString(output.fMHT) );
      vars.AddRowColumn(3, "MHT = sqrt( pow(Sum(px), 2) + pow(Sum(py), 2))");
      //
      vars.AddRowColumn(4, "AlphaT");
      vars.AddRowColumn(4, auxTools.ToString(output.fAlphaT) );
      vars.AddRowColumn(4, "AlphaT = 0.5 x (HT - dHT) /sqr( pow(HT, 2) - pow(MHT, 2))");
      vars.Print();
    }

  return;
}

TMatrixDSym TopologySelection::ComputeMomentumTensor(const JetSelection::Data& jetData, Data& output, double r)
{

  // r = 2: Corresponds to sphericity tensor (Get: Sphericity, Aplanarity, Planarity, ..)
  // r = 1: Corresponds to linear measures (Get: C, D, Second Fox-Wolfram moment, ...)
  TMatrixDSym momentumTensor(3);
  momentumTensor.Zero();
  
  if (r!=1.0 && r!=2.0)
    {
      throw hplus::Exception("LogicError") << "Invalid value r-value in computing the Momentum Tensor (r=" << r << ").  Supported valued are r=2.0 and r=1.0.";
    }
  
  // Sanity Check
  if ( jetData.getSelectedJets().size() < 2 )
    {
      return momentumTensor;
    }
  
  // Declare the Matrix normalisation (sum of momentum magnitutes to power r). That is: sum(|p|^{r})
  double normalisation = 0.0;
  double trace = 0.0;

  // For-loop: Jets
  for (auto& jet: jetData.getSelectedJets()){
    
    // Get the |p|^2 of the jet
    double p2 = pow(jet.p4().P(), 2);
    
    // For r=2, use |p|^{2}, for r=1 use |p| as the momentum weight
    double pR = ( r == 2.0 ) ? p2 : TMath::Power(p2, 0.5*r);
    
    // For r=2, use |1|, for r=1 use   (|p|^{2})^{-0.5} = |p|^{2 (-1/2)} = |p|^{-1} = 1.0/|p|
    double pRminus2 = ( r == 2.0 ) ? 1.0 : TMath::Power(p2, 0.5*r - 1.0); // 
    
    // Add pR to the matrix normalisation factor
    normalisation += pR;
       
    // Fill the momentum (r=1) or  sphericity (r=2) tensor (Must be symmetric: Mij = Mji)
    momentumTensor(0,0) += pRminus2*jet.p4().px()*jet.p4().px(); // xx
    momentumTensor(0,1) += pRminus2*jet.p4().px()*jet.p4().py(); // xy
    momentumTensor(0,2) += pRminus2*jet.p4().px()*jet.p4().pz(); // xz
    
    momentumTensor(1,0) += pRminus2*jet.p4().py()*jet.p4().px(); // yx
    momentumTensor(1,1) += pRminus2*jet.p4().py()*jet.p4().py(); // yy
    momentumTensor(1,2) += pRminus2*jet.p4().py()*jet.p4().pz(); // yz
    
    momentumTensor(2,0) += pRminus2*jet.p4().pz()*jet.p4().px(); // zx
    momentumTensor(2,1) += pRminus2*jet.p4().pz()*jet.p4().py(); // zy
    momentumTensor(2,2) += pRminus2*jet.p4().pz()*jet.p4().pz(); // zz
    
  }// for (auto& jet: jets){

  // Normalise the tensors to have unit trace (Mxx + Myy + Mzz = 1)
  momentumTensor *= (1.0/normalisation);
  trace = momentumTensor(0,0) + momentumTensor(1,1) + momentumTensor(2,2);
  
  // Print the tensor
  if (0)
    {
      std::cout << "\nMomentum Tensor (r = " << r << "):" << std::endl;
      Table tensor(" |  | ", "Text"); //LaTeX or Text    
      tensor.AddRowColumn(0, auxTools.ToString( momentumTensor(0,0) ) );
      tensor.AddRowColumn(0, auxTools.ToString( momentumTensor(0,1) ) );
      tensor.AddRowColumn(0, auxTools.ToString( momentumTensor(0,2) ) );
      tensor.AddRowColumn(1, auxTools.ToString( momentumTensor(1,0) ) );
      tensor.AddRowColumn(1, auxTools.ToString( momentumTensor(1,1) ) );
      tensor.AddRowColumn(1, auxTools.ToString( momentumTensor(1,2) ) );
      tensor.AddRowColumn(2, auxTools.ToString( momentumTensor(2,0) ) );
      tensor.AddRowColumn(2, auxTools.ToString( momentumTensor(2,1) ) );
      tensor.AddRowColumn(2, auxTools.ToString( momentumTensor(2,2) ) );
      tensor.AddRowColumn(3, "");
      tensor.AddRowColumn(4, "Normalisation");
      tensor.AddRowColumn(4, auxTools.ToString(normalisation));
      tensor.AddRowColumn(5, "IsSymmetric");
      tensor.AddRowColumn(5, auxTools.ToString(momentumTensor.IsSymmetric()));
      tensor.AddRowColumn(6, "Determinant");
      tensor.AddRowColumn(6, auxTools.ToString(momentumTensor.Determinant()));
      tensor.AddRowColumn(7, "Trace");
      tensor.AddRowColumn(7, auxTools.ToString(trace));
      tensor.Print(false);
    }

  if ( abs(trace-1.0) > 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that the Momentum-Tensor (r = " << r << ") Trace is 1.0. Found that abs(trace-1) = " << abs(trace-1) << ", instead.";
    }

  return momentumTensor;
}


TMatrixDSym TopologySelection::ComputeMomentumTensor2D(const JetSelection::Data& jetData, Data& output)
{

  TMatrixDSym momentumTensor(3);
  momentumTensor.Zero();
  
  // Sanity Check
  if ( jetData.getSelectedJets().size() < 2 )
    {
      return momentumTensor;
    }
  
  // Declare the Matrix normalisation (sum of momentum magnitutes to power r). That is: sum(|p|^{r})
  double normalisation = 0.0;
  double trace = 0.0;

  // For-loop: Jets
  for (auto& jet: jetData.getSelectedJets()){
    
    // Get the pT
    double pT = jet.p4().Pt();
    
    // Add pT to the matrix normalisation factor
    normalisation += pow(pT,2);
       
    // Fill the two-dimensional momentum tensor
    momentumTensor(0,0) += jet.p4().px()*jet.p4().px(); // xx
    momentumTensor(0,1) += jet.p4().px()*jet.p4().py(); // xy
    momentumTensor(1,0) += jet.p4().py()*jet.p4().px(); // yx
    momentumTensor(1,1) += jet.p4().py()*jet.p4().py(); // yy
    
  }// for (auto& jet: jets){

  // Normalise tensor to get the normalised 2-d momentum tensor
  momentumTensor *= (1.0/normalisation);
  trace = momentumTensor(0,0) + momentumTensor(1,1);
  
  // Print the tensor
  if (0)
    {
      std::cout << "\nNormalied 2-D Momentum Tensor"  << std::endl;
      Table tensor(" |  | ", "Text"); //LaTeX or Text    
      tensor.AddRowColumn(0, auxTools.ToString( momentumTensor(0,0) ) );
      tensor.AddRowColumn(0, auxTools.ToString( momentumTensor(0,1) ) );
      tensor.AddRowColumn(1, auxTools.ToString( momentumTensor(1,0) ) );
      tensor.AddRowColumn(1, auxTools.ToString( momentumTensor(1,1) ) );
      tensor.AddRowColumn(2, "");
      tensor.AddRowColumn(3, "Normalisation");
      tensor.AddRowColumn(3, auxTools.ToString(normalisation));
      tensor.AddRowColumn(4, "IsSymmetric");
      tensor.AddRowColumn(4, auxTools.ToString(momentumTensor.IsSymmetric()));
      tensor.AddRowColumn(5, "Determinant");
      tensor.AddRowColumn(5, auxTools.ToString(momentumTensor.Determinant()));
      tensor.AddRowColumn(6, "Trace");
      tensor.AddRowColumn(6, auxTools.ToString(trace));
      tensor.Print(false);
    }

  if ( abs(trace-1.0) > 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that the 2D Momentum-Tensor Trace is 1.0. Found that abs(trace-1) = " << abs(trace-1) << ", instead.";
    }

  return momentumTensor;
}


std::vector<float> TopologySelection::GetMomentumTensorEigenValues(const JetSelection::Data& jetData, Data& output)
{

  // Tensor required for calculation of: Sphericity, Aplanarity, Planarity
  // Need all particles in event to calculate kinematic variables. Use all tracks (ch. particles) instead.
  // Links:
  // https://cmssdt.cern.ch/SDT/doxygen/CMSSW_8_0_24/doc/html/d5/d29/EventShapeVariables_8h_source.html
  // https://cmssdt.cern.ch/SDT/doxygen/CMSSW_8_0_24/doc/html/dd/d99/classEventShapeVariables.html

  // Get the Linear Momentum Tensor
  TMatrixDSym MomentumTensor = ComputeMomentumTensor(jetData, output, 1.0);

  // Find the Momentum-Tensor EigenValues (Q1, Q2, Q3)
  TMatrixDSymEigen eigen(MomentumTensor);
  TVectorD eigenvals = eigen.GetEigenValues();

  // Store & Sort the eigenvalues
  std::vector<float> eigenvalues(3);
  eigenvalues.at(0) = eigenvals(0); // Q1
  eigenvalues.at(1) = eigenvals(1); // Q2
  eigenvalues.at(2) = eigenvals(2); // Q3
  sort( eigenvalues.begin(), eigenvalues.end(), std::greater<float>() );

  // Calculate the eigenvalues sum (Requirement: Q1 + Q2 + Q3 = 1)
  float eigenSum = std::accumulate(eigenvalues.begin(), eigenvalues.end(), 0);
  if ( (eigenSum - 1.0) > 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Q1+Q2+Q3=1. Found that Q1+Q2+Q3 = " << eigenSum << ", instead.";
    }

  // Save the final eigenvalues
  float Q1 = eigenvalues.at(0);
  float Q2 = eigenvalues.at(1);
  float Q3 = eigenvalues.at(2);

  // Sanity check on eigenvalues: Q1 >= Q2 >= Q3 (Q1 >= 0)
  bool bQ1Zero = (Q1 >= 0.0);
  bool bQ1Q2   = (Q1 >= Q2);
  bool bQ2Q3   = (Q2 >= Q3);
  bool bInequality = bQ1Zero * bQ1Q2 * bQ2Q3;
  
  if ( !(bInequality) )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that eigenvalues are ordered as Q1 >= Q2 >= Q3 (Q1 >= 0). Q1 = " << Q1 << ", Q2 = " << Q2 << ", Q3 = " << Q3;
    }

  // Calculate the linear combinations C and D
  output.fCparameter       = 3*(Q1*Q2 + Q1*Q3 + Q2*Q3); // Used to measure the 3-jet structure. Vanishes for perfece 2-jet event. Related to the 2nd Fox-Wolfram Moment (H2)
  output.fDparameter       = 27*Q1*Q2*Q3; // Used to measure the 4-jet structure. Vanishes for a planar event
  output.fFoxWolframMoment = 1-output.fCparameter; // The C-measure is related to the second Fox-Wolfram moment (see below), $C = 1 - H_2$.

  // C
  if ( abs(output.fCparameter-1.0) > 1 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that the quantity C satisfies the inequality: 0.0 <= C <= 1.0. Found that C = " << output.fCparameter;
    }

  // D
  if ( abs(output.fDparameter-1.0) > 1 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that the quantity C satisfies the inequality: 0.0 <= D <= 1.0. Found that D = " << output.fDparameter;
    }

  // 2nd Fox-Wolfram Moment
  if ( abs(output.fFoxWolframMoment-1.0) > 1 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that the 2nd Fox-Wolfram Moment (H2) satisfies the inequality: 0.0 <= H2 <= 1.0. Found that fFoxWolframMoment = " << output.fFoxWolframMoment;
    }
  
  if (0)
    {

      Table vars("Variable | Value | Allowed Range | Definition", "Text"); //LaTeX or Text
      vars.AddRowColumn(0, "C");
      vars.AddRowColumn(0, auxTools.ToString(output.fCparameter) );
      vars.AddRowColumn(0, "0.0 <= C <= 1.0");
      vars.AddRowColumn(0, "C = 3 x (Q1Q2 + Q1Q3 + Q2Q3");
      //
      vars.AddRowColumn(1, "D");
      vars.AddRowColumn(1, auxTools.ToString(output.fDparameter) );
      vars.AddRowColumn(1, "0.0 <= D <= 1.0");
      vars.AddRowColumn(1, "D = 27 x Q1 x Q2 x Q3");
      //
      vars.AddRowColumn(2, "2nd F-W Moment");
      vars.AddRowColumn(2, auxTools.ToString(output.fFoxWolframMoment) );
      vars.AddRowColumn(2, "0.0 <= H2 <= 1.0 ");
      vars.AddRowColumn(2, "H2 = 1-C");
      vars.Print();
    }

  return eigenvalues;
}


std::vector<float> TopologySelection::GetMomentumTensorEigenValues2D(const JetSelection::Data& jetData, Data& output)
{

  // For Circularity, the momentum tensor is the 2×2 submatrix of Mjk, normalized by the sum of pT instead by the sum of
  // This matrix has two eigenvalues Qi with 0 < Q1 < Q2. The following definition for the circularity C has been used:
  //  C = 2 × min (Q1,Q2) / (Q1 +Q2)
  // The circularity C is especially interesting for hadron colliders because it only uses the momentum values in x and y direction transverse
  // to the beam line. So C is a two dimensional event shape variable and is therefore independent from a boost along z. 
  // In addition, the normalization by the sum of the particle momenta makes C highly independent from energy calibration effects  (systematic uncertainty).
  // C takes small values for linear and high values for circular events. 
  
  // Find the Momentum-Tensor EigenValues (E1, E2)
  TMatrixDSym MomentumTensor = ComputeMomentumTensor2D(jetData, output);
  TMatrixDSymEigen eigen(MomentumTensor);
  TVectorD eigenvals = eigen.GetEigenValues();

  // Store & Sort the eigenvalues
  std::vector<float> eigenvalues(2);
  eigenvalues.at(0) = eigenvals[0]; // Q1
  eigenvalues.at(1) = eigenvals[1]; // Q2
  sort( eigenvalues.begin(), eigenvalues.end(), std::greater<float>() );

  // Save the final eigenvalues
  float Q1 = eigenvalues.at(0);
  float Q2 = eigenvalues.at(1);

  // Sanity check on eigenvalues: (Q1 > Q2)
  if (Q1 == 0) return eigenvalues;

  bool bInequality = (Q1 > 0 && Q1 > Q2);
  if ( !(bInequality) )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that eigenvalues are ordered as Q1 >= Q2. Found Q1 = " << Q1 << ", Q2 " << Q2;
    }
  
  // Calculate circularity
  output.fCircularity = 2*std::min(Q1, Q2)/(Q1+Q2); // is this definition correct?

  if (0)
    {      
      Table vars("Variable | Value | Allowed Range | Definition", "Text"); //LaTeX or Text
      vars.AddRowColumn(0, "Circularity");
      vars.AddRowColumn(0, auxTools.ToString(output.fCircularity) );
      vars.AddRowColumn(0, "0.0 <= C <= 1.0 ");
      vars.AddRowColumn(0, "C = 2 × min (Q1,Q2)/(Q1+Q2)");
      vars.Print();
    }
  
  return eigenvalues;
}



std::vector<float> TopologySelection::GetSphericityTensorEigenValues(const JetSelection::Data& jetData, Data& output)
{

  // C, D parameters
  // Need all particles in event to calculate kinematic variables. Use all tracks (ch. particles) instead.
  // Links:
  // http://home.fnal.gov/~mrenna/lutp0613man2/node234.html

  // Sanity check: at least 3 jets (for 3rd-jet resolution)
  if( (jetData.getSelectedJets().size()) < 3 )
    {
      std::vector<float> zeros(3, 0);
      return zeros;
    }

  // Sort the jets by pT (leading jet first)
  // std::sort( jets.begin(), jets.end(), PtComparator() );  

  // Get the Sphericity Tensor
  TMatrixDSym SphericityTensor = ComputeMomentumTensor(jetData, output, 2.0);

  // Find the Momentum-Tensor EigenValues (Q1, Q2, Q3)
  TMatrixDSymEigen eigen(SphericityTensor);
  TVectorD eigenvals = eigen.GetEigenValues();

  // Store & Sort the eigenvalues
  std::vector<float> eigenvalues(3);
  eigenvalues.at(0) = eigenvals(0); // Q1
  eigenvalues.at(1) = eigenvals(1); // Q2
  eigenvalues.at(2) = eigenvals(2); // Q3
  sort( eigenvalues.begin(), eigenvalues.end(), std::greater<float>() );

  // Calculate the eigenvalues sum (Requirement: Q1 + Q2 + Q3 = 1)
  float eigenSum = std::accumulate(eigenvalues.begin(), eigenvalues.end(), 0);
  if ( (eigenSum - 1.0) > 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Q1+Q2+Q3=1. Found that Q1+Q2+Q3 = " << eigenSum << ", instead.";
    }

  // Save the final eigenvalues
  float Q1 = eigenvalues.at(0);
  float Q2 = eigenvalues.at(1);
  float Q3 = eigenvalues.at(2);

  // Sanity check on eigenvalues: Q1 >= Q2 >= Q3 (Q1 >= 0)
  bool bQ1Zero = (Q1 >= 0.0);
  bool bQ1Q2   = (Q1 >= Q2);
  bool bQ2Q3   = (Q2 >= Q3);
  bool bInequality = bQ1Zero * bQ1Q2 * bQ2Q3;
  
  if ( !(bInequality) )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that eigenvalues are ordered as Q1 >= Q2 >= Q3 (Q1 >= 0)";
    }


  // Calculate the event-shape variables
  float pT3Squared = pow(jetData.getSelectedJets().at(2).p4().Pt(), 2);
  float HT2Squared = pow(jetData.getSelectedJets().at(0).p4().Pt() + jetData.getSelectedJets().at(1).p4().Pt(), 2);
  output.fY23      = pT3Squared/HT2Squared;
  output.fY        = (sqrt(3.0)/2.0)*(Q2-Q3); // (Since Q1>Q2, then my Q1 corresponds to Q3 when Q's are reversed-ordered). Calculate the Y (for Y-S plane)

  // Check the value of the third-jet resolution
  if (abs(output.fY23-0.25) > 0.25 + 1e-4)
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that y23 satisfies the inequality: 0.0 <= y23 <= 0.25. Found that y23 = " << output.fY23;
    }
  
  // Calculate the Sphericity (0 <= S <= 1). S~0 for a 2-jet event, and S~1 for an isotropic one
  output.fSphericity = 1.5*(Q2 + Q3); 
  if ( abs(output.fSphericity-1.0) > 1 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Sphericity (S) satisfies the inequality: 0.0 <= S <= 1.0. Found that S = " << output.fSphericity;
    }

  // Calculate the Sphericity (0 <= S <= 1). S~0 for a 2-jet event, and S~1 for an isotropic one
    output.fSphericityT = 2.0*Q2/(Q1 + Q2); 
  if ( abs(output.fSphericityT-1.0) > 1 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Transverse Sphericity (ST) satisfies the inequality: 0.0 <= ST <= 1.0. Found that ST = " << output.fSphericityT;
    }

  // Calculate the Aplanarity (0 <= A <= 0.5).  It measures the transverse momentum component out of the event plane
  // A~0 for a planar event, A~0.5 for an isotropic one
  output.fAplanarity = 1.5*(Q3);
  if ( abs(output.fAplanarity-0.5) > 0.5 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Aplanarity (A) satisfies the inequality: 0.0 <= A <= 0.5. Found that A = " << output.fAplanarity;
    }

  // Calculate the Aplanarity (0 <= P <= 0.5)
  output.fPlanarity  = (2.0/3.0)*(output.fSphericity-2*output.fAplanarity);
  if ( abs(output.fPlanarity-0.5) > 0.5 + 1e-4 )
    {
      throw hplus::Exception("LogicError") << "Failure of requirement that Planarity (P) satisfies the inequality: 0.0 <= P <= 0.5. Found that P = " << output.fPlanarity;
    }


  if (0)
    {
      Table vars("Variable | Value | Allowed Range | Definition", "Text"); //LaTeX or Text
      vars.AddRowColumn(0, "y23");
      vars.AddRowColumn(0, auxTools.ToString(output.fY23) );
      vars.AddRowColumn(0, "0.0 <= y23 <= 0.25");
      vars.AddRowColumn(0, "y23 = pow(jet3_Pt, 2) / pow(jet1_Pt + jet2_Pt, 2)" );
      //
      vars.AddRowColumn(1, "Sphericity");
      vars.AddRowColumn(1, auxTools.ToString(output.fSphericity) );
      vars.AddRowColumn(1, "0.0 <= S <= 1.0");
      vars.AddRowColumn(1, "S = 1.5 x (Q2 + Q3)");
      //
      vars.AddRowColumn(2, "Sphericity (T)");
      vars.AddRowColumn(2, auxTools.ToString(output.fSphericityT) );
      vars.AddRowColumn(2, "0.0 <= S (T) <= 1.0");
      vars.AddRowColumn(2, "S (T) = (2 x Q2)/(Q1 + Q2)");
      //
      vars.AddRowColumn(3, "Aplanarity");
      vars.AddRowColumn(3, auxTools.ToString(output.fAplanarity) );
      vars.AddRowColumn(3, "0.0 <= A <= 0.5 ");
      vars.AddRowColumn(3, "A = 1.5 x Q3");
      //
      vars.AddRowColumn(4, "Planarity");
      vars.AddRowColumn(4, auxTools.ToString(output.fPlanarity) );
      vars.AddRowColumn(4, "0.0 <= P <= 0.5 ");
      vars.AddRowColumn(4, "P (2/3) x (S - 2A)");
      //
      vars.AddRowColumn(5, "Y");
      vars.AddRowColumn(5, auxTools.ToString(output.fY) );
      vars.AddRowColumn(5, "");
      vars.AddRowColumn(5, "Y = sqrt(3)/2 x (Q1 - Q2)");
      vars.Print();
    }
    
  return eigenvalues;
  
}
