//#######################################################################
// -*- C++ -*-
//       File Name:  EvtTopology.cc
// Original Author:  Alexandros Attikis
//     Description:  Designed to calculate Evt Topology related variables                   
//       Institute:  UCY
//         e-mail :  attikis@cern.ch
//        Comments:  
//#######################################################################

//#########################################################################################################################################
// Detailed Explanation: 
// The method "alphaT()" of this class takes as input iNJets and uses them to form 2 Pseudo-Jets to describe the event. For iNJets 
// in an event this means there are 2^{iNJets-1} combinations to do this. The methods does exactly that and for the combination which
// minimises the quantity DeltaHt = Ht_PseudoJet1 - Ht_PseudoJet2, it calculates the quantity alphaT which maybe can be used to discriminate
// your signal from your background.
// The method "alphaT()" employs a double loop to recreate all the possilbe jet combinations out of iNJets, by 
// the use of an iNJets-binary system. For example, if iNJets=5, the loop indices ("k" outside, "l" inside)
// run both from "k"=0 to "k"=2^{4}=16. The upper limit of the outside loop is given by the expression:
// 1<<(iNJets-1)) = shift the number 1 by (iNJets-1) positions to the left. So, for iNJets=5
// i.e. 1  --> 1 0 0 0 0 
// This is now the way we will represent grouping into 2 Pseudo-Jets. The 0's represent one group and the 1's the other.
// So, for example 1 0 0 0 0 means 1 jet forms Pseudo-Jet1 and 4 jets form Pseudo-Jet2. 
// Also, for example, 1 0 0 1 0 means 2 jets form Pseudo-Jet1 and 3 jets form Pseudo-Jet2.
// The inside loop performs a bitwise right shift of index "k" by "l" positions and then
// compares the resulting bit to 1. So, for "k"=0, all the resulting comparisons in the inside loop will result to 0, except the one 
// with "l"=4.
// This gives the first combination: 0 0 0 0 0   ( i.e. 0 jets form Pseudo-Jet1 and 5 jets form Pseudo-Jet2 )
// For "k"=1 (00000001 in 8bit representation), the first comparison is 1, since k is shifted by zero positions 
// and then compared to 1. The rest comparisons yield zero, since by shifting the bit by any position and comparing to 1 gives zero. 
// Thus, for "k"=1 we have after the second loop: 0 0 0 0 1
// In the same manner, we get for "k"=2 (00000001 in 8bit representation) we have after the second loop: 0 0 0 1 0
//  To summarise:
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
//#########################################################################################################################################
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EvtTopology.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1F.h"
#include "Math/GenVector/VectorUtil.h"

namespace{
  
  vector<float> AlphaTAux( const unsigned iNJets, int iCombinationIndex, const std::vector<Float_t> vEt, const std::vector<Float_t> vPx, const std::vector<Float_t> vPy, const std::vector<Float_t> vPz, const reco::Candidate& tau){
    
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    /// Description                                                                                              
    /// This function works in parallel with EvtTopology::alphaT(..). It takes as input the number of jets       
    /// in the Event and the "winning combination" in terms of minimising the quantity:                          
    /// DeltaHt = |Ht_pseudoJet1 - Ht_pseudoJet2| of the pseudo-jets.                                            
    /// The function then loops over the jets of the "winning combination" and puts the jets into two groups     
    /// differentiated by which one contains the "Tau-jet". Then, for each PseudoJetGroup it loops over all      
    /// possible DiJets combinations and calculates their DiJet mass and stores them in a vector of floats.       
    /// NOTE: The number of possible DiJets that can be formed from a pool of iJets is:  
    /// nCr = iNJets! / (iNJtets-2)!2!                                                                         
    /// so, for example: iNJets = 5, nCr = 5! / (3!2!) = 5x2 = 10                                              
    ///                  iNJets = 4, nCr = 4! / (2!2!) = 3x2 = 6                                              
    ///                  iNJets = 3, nCr = 3! / (1!2!) = 3x1 = 3                                             
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    /// Variable Declaration
    bool bPseudoJetsGroupA = 0;
    bool bTauJetInGroupA   = 0;
    bool bTauJetInGroupB   = 0;
    vector<float> vDiJetMassesNoTau;
    vector<float> vEmpty;
    vector<TLorentzVector> vJetsInTauPseudoJet;
    vector<TLorentzVector> vJetsInNonTauPseudoJet;
    vector<TLorentzVector> vJetsInPseudoJetA;
    vector<TLorentzVector> vJetsInPseudoJetB;
    
    /// Get the "winning combination"
    const int k = iCombinationIndex;
    /// Iterate through jets for combination k.
    for ( unsigned l=0; l < iNJets; l++ ){ 
      /// Bitwise shift of "k" by "l" positions to the right and compare to 1. 
      /// Make a boolean of the comparison so that you can distinguish between PseudoJetGoupA (0's group) from PseudoJetGoupB (1's group)
      bPseudoJetsGroupA = (Int_t(k>>l)&1);
      
      /// If current jet is in groupA (1's)
      if(bPseudoJetsGroupA){
	TLorentzVector tmpJet;
	tmpJet.SetPx( vPx[l] );
	tmpJet.SetPy( vPy[l] );
	tmpJet.SetPz( vPz[l] );
	vJetsInPseudoJetA.push_back(tmpJet);
      } 
      else{ /// If current jet is in groupB (0's)
	TLorentzVector tmpJet;
	tmpJet.SetPx( vPx[l] );
	tmpJet.SetPy( vPy[l] );
	tmpJet.SetPz( vPz[l] );
	vJetsInPseudoJetB.push_back(tmpJet);
      }
    } ///eof:  for ( unsigned l=0; l < iNJets; l++ ) {
    
    /// Determine in which of the two pseudo-jets the tau-jet is found; Start with PseudoJetA.
    for (vector<TLorentzVector>::const_iterator iJet = vJetsInPseudoJetA.begin(); iJet != vJetsInPseudoJetA.end(); ++iJet) {

      float fDeltaR = reco::deltaR( tau.eta(), tau.phi(), (*iJet).Eta(), (*iJet).Phi() ); 
      // inline double deltaR(double eta1, double phi1, double eta2, double phi2) {

      if( fabs(fDeltaR) < 0.1 ){
	bTauJetInGroupA = 1;
	break;
      }
    }

    /// Determine in which of the two pseudo-jets the tau-jet is found; Continue with PseudoJetB.
    for (vector<TLorentzVector>::const_iterator iJet = vJetsInPseudoJetB.begin(); iJet != vJetsInPseudoJetB.end(); ++iJet) {
      
      float fDeltaR = reco::deltaR( tau.eta(), tau.phi(), (*iJet).Eta(), (*iJet).Phi() );
      if( fabs(fDeltaR) < 0.1 ){
	bTauJetInGroupB = 1;
	break;
      }
    }
    
    
    /// In case the pseudo-jet with the tau is not found or found twice return an empty vector
    if ( (bTauJetInGroupA==1 && bTauJetInGroupB==1) || (bTauJetInGroupA==0 && bTauJetInGroupB==0) ){
      return vEmpty;
    }

    if(bTauJetInGroupA){
      // std::cout << "Tau-jet found in Pseudo-Jet A" << std::endl;
      vJetsInTauPseudoJet    = vJetsInPseudoJetA;
      vJetsInNonTauPseudoJet = vJetsInPseudoJetB;
    }
    else{
      // std::cout << "Tau-jet found in Pseudo-Jet B" << std::endl;
      vJetsInTauPseudoJet    = vJetsInPseudoJetB;
      vJetsInNonTauPseudoJet = vJetsInPseudoJetA;
    }
    
    /// We now have a vector containing the Jets comprising each PseudoJet. We want to calculate the DiJet mass for all combination for the 
    /// PseudoJet that does NOT contain the Tau-Jet, hoping to reconstruct the W mass. 
    int iJetsInNonTauPseudoJet = vJetsInNonTauPseudoJet.size();
    
    /// If the PseudoJet has less than 2 jets (impossible to calculate InvMass), abort calculation and return an empty vector
    if(iJetsInNonTauPseudoJet<2){return vEmpty;}
    
    /// Try to reconstruct W mass. Use a double loop with the outside index "m" and the  inside index "n=m+1" (to avoid double counting).
    for(int m = 0; m < iJetsInNonTauPseudoJet; m++){
      for(int n = m+1; n < iJetsInNonTauPseudoJet; n++){
	
	float E1 = vJetsInNonTauPseudoJet[m].Energy();
	float E2 = vJetsInNonTauPseudoJet[n].Energy();
	
	TLorentzVector P1 = vJetsInNonTauPseudoJet[m];
	TLorentzVector P2 = vJetsInNonTauPseudoJet[n];
	
	float fDiJetMassNoTau =  sqrt( (E1+E2)*(E1+E2) - (P1+P2).Mag2() );
	vDiJetMassesNoTau.push_back(fDiJetMassNoTau);
      }
    }
    
    /// Reset variables
    bTauJetInGroupA = 0;
    bTauJetInGroupB = 0;
    
    return vDiJetMassesNoTau;
    
  }//eof: static vector<float> alphaTAux(...){
  
}//eof: namespace{


namespace HPlus {
  EvtTopology::Data::Data():
    fPassedEvent(false) {
      // Initialize
      sAlpha.fAlphaT = 0.;
      sAlpha.fJt = 0.;
      sAlpha.fHt = 0.;
      sAlpha.fDeltaHt = 0.;
      sAlpha.fMHt = 0.;
      //
      sMomentumTensor.fQOne   = 0.0;
      sMomentumTensor.fQTwo   = 0.0;
      sMomentumTensor.fQThree = 0.0;
      sMomentumTensor.fSphericity  = 0.0;
      sMomentumTensor.fAplanarity  = 0.0;
      sMomentumTensor.fCircularity = 0.0;
      //
      sSpherocityTensor.fQOne   = 0.0;
      sSpherocityTensor.fQTwo   = 0.0;
      sSpherocityTensor.fQThree = 0.0;
      sSpherocityTensor.fCparameter = 0.0;
      sSpherocityTensor.fDparameter = 0.0;
      sSpherocityTensor.fJetThrust  = 0.0;
    }
  EvtTopology::Data::~Data() {}

  EvtTopology::EvtTopology(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    // fDiscriminator(iConfig.getUntrackedParameter<std::string>("discriminator")),
    // fDiscrCut(iConfig.getUntrackedParameter<double>("discriminatorCut")),
    fAlphaTCut(iConfig.getUntrackedParameter<double>("alphaT")),
    fSphericityCut(iConfig.getUntrackedParameter<double>("sphericity")),
    fAplanarityCut(iConfig.getUntrackedParameter<double>("aplanarity")),
    fPlanarityCut(iConfig.getUntrackedParameter<double>("planarity")),
    fCircularityCut(iConfig.getUntrackedParameter<double>("circularity")),
    fCparameterCut(iConfig.getUntrackedParameter<double>("Cparameter")),
    fDparameterCut(iConfig.getUntrackedParameter<double>("Dparameter")),
    fJetThrustCut(iConfig.getUntrackedParameter<double>("jetThrust")),
    fEvtTopologyCount(eventCounter.addSubCounter("EvtTopology main","EvtTopology cut")),
    fAlphaTCutCount(eventCounter.addSubCounter("EvtTopology", "alphaT")),
    fSphericityCutCount(eventCounter.addSubCounter("EvtTopology", "sphericity")),
    fAplanarityCutCount(eventCounter.addSubCounter("EvtTopology", "aplanarity")),
    fPlanarityCutCount(eventCounter.addSubCounter("EvtTopology", "planarity")),
    fCircularityCutCount(eventCounter.addSubCounter("EvtTopology", "circularity")),
    fCparameterCutCount(eventCounter.addSubCounter("EvtTopology", "Cparameter")),
    fDparameterCutCount(eventCounter.addSubCounter("EvtTopology", "Dparameter")),
    fJetThrustCutCount(eventCounter.addSubCounter("EvtTopology", "jetThurst"))
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("EvtTopology");
    hAlphaT = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "alphaT", "alphaT", 50, 0.0, 5.0);
    hSphericity = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "sphericity", "sphericity", 20, 0.0, 1.0);
    hAplanarity = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "aplanarity", "aplanarity", 10, 0.0, 0.5);
    hPlanarity = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "planarity", "planarity", 10, 0.0, 0.5);
    hCircularity = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "circularity", "circularity", 20, 0.0, 1.0);
    hCparameter = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "Cparameter", "Cparameter", 20, 0.0, 1.0);
    hDparameter = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "Dparameter", "Dparameter", 20, 0.0, 1.0);
  }

  EvtTopology::~EvtTopology() {}

  EvtTopology::Data EvtTopology::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets ){
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementing until the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, tau, jets);
  }

  EvtTopology::Data EvtTopology::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets ){
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, tau, jets);
  }

  EvtTopology::Data EvtTopology::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets ){
    Data output;
    /// Calcuate standard event-shape-variables (e.g sphericity, aplanarity, planarity, alphaT)

    vector<float> MomentumTensor_EigenValues = CalcMomentumTensorEigenValues(iEvent, iSetup, jets, output);
    vector<float> SpherocityTensor_EigenValues = CalcSpherocityTensorEigenValues(iEvent, iSetup, jets, output);

    // return output;
    bool bPassedSphericity     = CalcSphericity(MomentumTensor_EigenValues, output);
    bool bPassedAplanarity     = CalcAplanarity(MomentumTensor_EigenValues, output);
    bool bPassedPlanarity      = CalcPlanarity(MomentumTensor_EigenValues, output);
    bool bPassedCircularity    = CalcCircularity(jets, output);
    bool bPassedAlphaT         = CalcAlphaT(iEvent, iSetup, tau, jets, output); // tau is used in W invariant mass reconstruction in the pseudo-jets created for alphaT
    bool bPassedCandDparamCuts = CalcCandDParameters(SpherocityTensor_EigenValues, output);
    bool bPassedJetThrust      = CalcJetThrust(iEvent, iSetup, jets, output);

    /// Determine if event has passed the Event-Topology cuts
    bool bPassedCuts = false;
    bPassedCuts = bPassedSphericity * bPassedAplanarity * bPassedPlanarity * bPassedCircularity * bPassedAlphaT * bPassedCandDparamCuts * bPassedJetThrust;

    if(bPassedCuts){
      increment(fEvtTopologyCount);
    }
    output.fPassedEvent = bPassedCuts;
    
    return output;
  }

  bool EvtTopology::CalcAlphaT(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets, EvtTopology::Data& output){
  
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /// AlphaT:
    /// Calculates the AlphaT variable, defined as an N-object system where the set of objects is 1 tau-jet and N-1
    /// jets. This definition reproduces the kinematics of a di-jet system by constructing two pseudo-jets, which balance
    /// one another in Ht. The two pseudo-jets are formed from the combination of the N objects that minimizes the
    /// DeltaHt = |Ht_pseudoJet1 - Ht_pseudoJet2| of the pseudo-jets.                                             
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    /// Declaration of variables 
    std::vector<float> vEt, vPx, vPy, vPz;
    std::vector<bool> vPseudo_jet1;
    const bool bList = true;
    bool bPassedCut = false;

    /// Loop over all selected jets
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {    
      edm::Ptr<pat::Jet> iJet = *iter;
      /// Fill vectors with jets information (jets are SORTED in energy)
      vEt.push_back( iJet->et() );
      vPx.push_back( iJet->px() );
      vPy.push_back( iJet->py() );
      vPz.push_back( iJet->pz() );
    }
    /// Declaration of variables 
    unsigned iNJets = vEt.size();
    int iCombinationIndex = -1;

    /// Calculate sums
    float fSum_et = accumulate( vEt.begin(), vEt.end(), 0.0 );
    float fSum_px = accumulate( vPx.begin(), vPx.end(), 0.0 );
    float fSum_py = accumulate( vPy.begin(), vPy.end(), 0.0 );
    /// Minimum Delta Et for two pseudo-jets
    float fMin_delta_sum_et = -1.0;
    
    if(iNJets > 20){ 
      // Fill the function structure with -2.0 to indicate that combinatorics too much
      output.sAlpha.fAlphaT  = -2.0;
      output.sAlpha.fJt      = -2.0;
      output.sAlpha.fHt      = -2.0;
      output.sAlpha.fDeltaHt = -2.0;
      output.sAlpha.fMHt     = -2.0;
      return false;
    }

    /// Iterate through different combinations
    for ( unsigned k=0; k < unsigned(1<<(iNJets-1)); k++ ) { 
      float fDelta_sum_et = 0.0;
      std::vector<bool> jet;
      /// Iterate through jets
      for ( unsigned l=0; l < vEt.size(); l++ ) { 
	/// Bitwise shift of "k" by "l" positions to the right and compare to 1 (&1)
	/// i.e.: fDelta_sum_et += vEt[l] * ( 1 - 2*0 );  if comparison is un-successful
	///  or   fDelta_sum_et += vEt[l] * ( 1 - 2*1 );  if comparison is successful
	// in this way you add up all Et from PseudoJetsGroupA (belonging to 0's group) and subtract that from PseudoJetsGroupB (1's group)
	fDelta_sum_et += vEt[l] * ( 1 - 2 * (int(k>>l)&1) ); 
	if ( bList ) { jet.push_back( (int(k>>l)&1) == 0 ); } 
      }
      /// Find configuration with minimum value of DeltaHt 
      if ( ( fabs(fDelta_sum_et) < fMin_delta_sum_et || fMin_delta_sum_et < 0.0 ) ) {
	fMin_delta_sum_et = fabs(fDelta_sum_et);
	iCombinationIndex = k; /// overwritten everytime a new minimum is found
	if ( bList && jet.size() == vEt.size() ){vPseudo_jet1.resize(jet.size());}
      }
    }
    
    /// Get DiJet information from Pseudo-jets
    vector<float> vDiJetMassesNoTau =  AlphaTAux(iNJets, iCombinationIndex, vEt, vPx, vPy, vPz, tau);
    /// In the case something goes wrong...
    if ( ( fMin_delta_sum_et < 0.0 ) ){ 
      /// Fill the function structure with -1.0
      output.sAlpha.fAlphaT  = -1.0;
      output.sAlpha.fJt      = -1.0;
      output.sAlpha.fHt      = -1.0;
      output.sAlpha.fDeltaHt = -1.0;
      output.sAlpha.fMHt     = -1.0;
    }
    else{
      /// Remember, the Tau-Jet is stored in the "vEt" vector FIRST. The jets (sorted in Energy) are stored right after the Tau-jet.
      float fHt = fSum_et;
      float fJt = fSum_et - vEt[0] - vEt[1]; // Ht without considering the Ldg Jet of the Event & excluding Tau-jet
      float fDeltaHt = fMin_delta_sum_et;
      float fMHt     = sqrt(pow(fSum_px,2) + pow(fSum_py,2));
      float fAlphaT = ( 0.5 * ( fHt - fDeltaHt ) / sqrt( pow(fHt,2) - pow(fMHt,2) ) );
      /// Fill the function structure
      output.sAlpha.fAlphaT  = fAlphaT;
      output.sAlpha.fJt      = fJt;
      output.sAlpha.fHt      = fHt;
      output.sAlpha.fDeltaHt = fDeltaHt;
      output.sAlpha.fMHt     = fMHt;
      output.sAlpha.vDiJetMassesNoTau = vDiJetMassesNoTau;
    }
    if( output.sAlpha.fAlphaT > fAlphaTCut){
      bPassedCut = true;
      increment(fAlphaTCutCount);
    }
          
    /// Fill Histos
    hAlphaT->Fill(output.sAlpha.fAlphaT);

    return bPassedCut;
  }  


  vector<float> EvtTopology::CalcMomentumTensorEigenValues(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, EvtTopology::Data& output){

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /// Sphericity, Aplanarity, Planarity
    /// Need all particles in event to calculate kinematic variables. Use all tracks (ch. particles) instead.
    /// see: http://cmssdt.cern.ch/SDT/doxygen/CMSSW_3_9_7/doc/html/d5/da7/classEventShape.html#7f045fc98c3f011703370a239d7522d2
    /// and: http://inspirehep.net/record/887920/files/Banerjee.MSc.pdf
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    /* Change jets-loop to tracks-loop once Track collection is available in pattuples
    // Create and attach handle to All Tracks collection
    edm::Handle<reco::TrackCollection> myTracksHandle;
    iEvent.getByLabel("generalTracks", myTracksHandle);
    */

    /// Attempt to remedy absence of tracks by using all jets in the event    
    TMatrixDSym MomentumTensor(3);
    MomentumTensor.Zero();

    /// Sanity check: at least 3 jets
    if( (jets.size()) < 3 ){
      throw cms::Exception("LogicError") << "Expected at least 3 jets for the normalised momentum tensor, only found " << jets.size() + 1 << " at " << __FILE__ << ":" << __LINE__ << std::endl;
    }

    /// Declare momentum vector to be filled with jet's momentum components
    float momentum[3];
    for(int j = 0; j < 3; j++) momentum[j]=0;

    /// Loop over all selected jets
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {    
      edm::Ptr<pat::Jet> iJet = *iter;
      
      momentum[0] = iJet->px();
      momentum[1] = iJet->py();
      momentum[2] = iJet->pz();

      /// Fill the momentum tensor
      for (unsigned int i=0; i < 3; i++){
	for (unsigned int j=0; j <= i; j++){
	  MomentumTensor[i][j] += momentum[i]*momentum[j];
	}
      }
    }//eof: jet loop
    
    /// Calculate the normalised-to-1 momentum tensor =  sum{p_j[a]*p_j[b]}/sum{p_j**2} 
    /// Thus the MomentumTensor has a unit trace: Mxx + Myy + Mzz = 1, 
    /// and is symmetric: Mij = Mji
    MomentumTensor*=1/(MomentumTensor[0][0]+MomentumTensor[1][1]+MomentumTensor[2][2]);

    /// Find the MomentumTensor_EigenValues Q1 + Q2 + Q3 = 1  0 <= Q1 <= Q2 <= Q3
    TMatrixDSymEigen eigen(MomentumTensor);
    TVectorD eigenvals = eigen.GetEigenValues();
    vector<float> eigenvalues(3);
    eigenvalues[0] = eigenvals[0]; // Q1
    eigenvalues[1] = eigenvals[1]; // Q2
    eigenvalues[2] = eigenvals[2]; // Q3
    /// Sort the eigenvalues
    sort( eigenvalues.begin(), eigenvalues.end() );

    /// Sanity check on eigenvalues: 0 <= Q1 <= Q2 <= Q3
    if(!(eigenvalues[0] >= 0 && eigenvalues[1] >= eigenvalues[0] && eigenvalues[2] >= eigenvalues[1])){
      eigenvalues[0] = -1;
      eigenvalues[1] = -1;
      eigenvalues[2] = -1;
      //throw cms::Exception("LogicError") << "Failure of requirement that eigenvalues are ordered as 0 <= Q1 <= Q2 <= Q3 at " << __FILE__ << ":" << __LINE__ << std::endl;
    }
    
    /// Sanity check on eigenvalues: Q1 + Q2 + Q3 = 1
    output.sMomentumTensor.fQOne   = eigenvalues[0];
    output.sMomentumTensor.fQTwo   = eigenvalues[1];
    output.sMomentumTensor.fQThree = eigenvalues[2];

    return eigenvalues;
  
  }


  bool EvtTopology::CalcJetThrust(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, EvtTopology::Data& output){

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /// Jet Thrust (Tz)
    /// Need all particles in event to calculate kinematic variables. Use all tracks (ch. particles) instead.
    /// The jet thrust  is different from the standard definition of thrust (T), where the thrust axis has to be
    /// searched for by maximising the thrust in the expression. For Tz, the thrust axis is defined by the virtual boson axis.
    /// http://www.desy.de/~heramc/proceedings/wg20/mccance.ps.gz
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    bool bPassedCut = false;

    /// Sanity check: at least 3 jets
    if( (jets.size()) < 3 ){
      throw cms::Exception("LogicError") << "Expected at least 3 jets for the normalised momentum tensor, only found " << jets.size() + 1 << " at " << __FILE__ << ":" << __LINE__ << std::endl;
    }

    /// Declare momentum vector to be filled with jet's momentum components
    float momentum[3];
    float momentumMag = 0.0;
    float momentumMagSum = 0.0;
    float momentumZ = 0.0;
    float momentumZSum = 0.0;
    float jetThrust = 0.0;
    
    // Initialise the momentum vectors
    for(int j = 0; j < 3; j++) momentum[j]=0;

    /// Loop over all selected jets
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {    
      edm::Ptr<pat::Jet> iJet = *iter;

      // iJet->boostToCM();  //fixme
      momentumMag = TMath::Abs(iJet->p());
      momentumMagSum = momentumMagSum + momentumMag;
      momentumZ = TMath::Abs(iJet->pz());
      momentumZSum = momentumZSum + momentumZ;

    }//eof: jet loop

    jetThrust = momentumZSum/momentumMagSum;
    
    // std::cout << "*** jetThrust = " << jetThrust << std::endl;
    output.sSpherocityTensor.fJetThrust  = jetThrust;

    if( output.sSpherocityTensor.fJetThrust > fJetThrustCut){
      bPassedCut = true;
      increment(fJetThrustCutCount);
    }
    
    return bPassedCut;
  
  }


  vector<float> EvtTopology::CalcSpherocityTensorEigenValues(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets, EvtTopology::Data& output){

    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /// C, D parameters
    /// Need all particles in event to calculate kinematic variables. Use all tracks (ch. particles) instead.
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    /* Change jets-loop to tracks-loop once Track collection is available in pattuples
    // Create and attach handle to All Tracks collection
    edm::Handle<reco::TrackCollection> myTracksHandle;
    iEvent.getByLabel("generalTracks", myTracksHandle);
    */

    /// Attempt to remedy absence of tracks by using all jets in the event    
    TMatrixDSym SpherocityTensor(3);
    SpherocityTensor.Zero();

    /// Sanity check: at least 3 jets
    if( (jets.size()) < 3 ){
      throw cms::Exception("LogicError") << "Expected at least 3 jets for the normalised momentum tensor, only found " << jets.size() + 1 << " at " << __FILE__ << ":" << __LINE__ << std::endl;
    }

    /// Declare momentum vector to be filled with jet's momentum components
    float momentum[3];
    float momentumMag = 0.0;
    float momentumMagSum = 0.0;

    for(int j = 0; j < 3; j++) momentum[j]=0;

    /// Loop over all selected jets
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {    
      edm::Ptr<pat::Jet> iJet = *iter;

      // iJet->boostToCM(); //fixme
      momentumMag = TMath::Abs(iJet->p());
      momentum[0] = iJet->px();
      momentum[1] = iJet->py();
      momentum[2] = iJet->pz();
      momentumMagSum = momentumMagSum + momentumMag;

      /// Fill the momentum tensor
      for (unsigned int i=0; i < 3; i++){
	for (unsigned int j=0; j <= i; j++){
	  SpherocityTensor[i][j] += momentum[i]*momentum[j]/momentumMag;
	}
      }
    }//eof: jet loop
    
    /// Calculate the normalised-to-1 momentum tensor =  sum{p_j[a]*p_j[b]}/sum{p_j**2} 
    /// Thus the SpherocityTensor has a unit trace: Mxx + Myy + Mzz = 1, 
    /// and is symmetric: Mij = Mji
    SpherocityTensor*=1/(momentumMagSum);

    /// Find the SpherocityTensor_EigenValues Q1 + Q2 + Q3 = 1  0 <= Q1 <= Q2 <= Q3
    TMatrixDSymEigen eigen(SpherocityTensor);
    TVectorD eigenvals = eigen.GetEigenValues();
    vector<float> eigenvalues(3);
    eigenvalues[0] = eigenvals[0]; // Q1
    eigenvalues[1] = eigenvals[1]; // Q2
    eigenvalues[2] = eigenvals[2]; // Q3
    /// Sort the eigenvalues
    sort( eigenvalues.begin(), eigenvalues.end() );

    /// Sanity check on eigenvalues: 0 <= Q1 <= Q2 <= Q3
    if(!(eigenvalues[0] >= 0 && eigenvalues[1] >= eigenvalues[0] && eigenvalues[2] >= eigenvalues[1])){
      eigenvalues[0] = -1;
      eigenvalues[1] = -1;
      eigenvalues[2] = -1;
      //throw cms::Exception("LogicError") << "Failure of requirement that eigenvalues are ordered as 0 <= Q1 <= Q2 <= Q3 at " << __FILE__ << ":" << __LINE__ << std::endl;
    }
    
    /// Sanity check on eigenvalues: Q1 + Q2 + Q3 = 1
    output.sSpherocityTensor.fQOne   = eigenvalues[0];
    output.sSpherocityTensor.fQTwo   = eigenvalues[1];
    output.sSpherocityTensor.fQThree = eigenvalues[2];
    // std::cout << "*** eigenvalues[0] = " <<  eigenvalues[0] << ", eigenvalues[1] = " <<  eigenvalues[1] << ", eigenvalues[2] = " <<  eigenvalues[2] << std::endl;
    
    return eigenvalues;
  
  }

  bool EvtTopology::CalcCandDParameters(vector<float> eigenvalues, EvtTopology::Data& output){

    bool bPassedCut = false;
    bool bPassedCparameterCut = false;
    bool bPassedDparameterCut = false;

    /// For events with planar topology "C" ranges between 0 and 3/4 and "D" is equal to zero
    /// For large number of particles in the final state, both "C" and "D" are close to unity
    /// Thus "C" provides a measure of the multi-jet structure of an event with special emphasis on planar events,
    /// while "D" measures the deviation from planarity of events by receiving major contribution from events with four or more jets.
    float Cparameter = 3*(eigenvalues[0]*eigenvalues[1] + eigenvalues[1]*eigenvalues[2] + eigenvalues[2]*eigenvalues[0]);
    float Dparameter = 27*(eigenvalues[0]*eigenvalues[1]*eigenvalues[2]);
    output.sSpherocityTensor.fCparameter = Cparameter;
    output.sSpherocityTensor.fDparameter = Dparameter;
    // std::cout << "*** Cparameter = " << Cparameter << ", Dparameter = " << Dparameter << std::endl;

    /// Check whether cut is passed
    if( output.sSpherocityTensor.fCparameter > fCparameterCut){
      bPassedCparameterCut = true;
      increment(fCparameterCutCount);
    }

    if( output.sSpherocityTensor.fCparameter > fDparameterCut){
      bPassedDparameterCut = true;
      increment(fDparameterCutCount);
    }

    bPassedCut = bPassedCparameterCut*bPassedDparameterCut;

    /// Fill Histos
    hCparameter->Fill(output.sSpherocityTensor.fCparameter);
    hDparameter->Fill(output.sSpherocityTensor.fDparameter);

    return bPassedCut;

  }



  bool EvtTopology::CalcSphericity(vector<float> eigenvalues, EvtTopology::Data& output){

    /// Computation of variables: 0 <= Q1 <= Q2 <= Q3 are the eigenvalues of the normalised-to-1 MomentumTensor
    /// Sphericity (S) = 3/2*(Q1+Q2)    0 <= S <= 1
    /// S = 1 for spherical, S= 3/4 for planar, S= 0 for linear events

    if (output.sMomentumTensor.fQOne < 0) return false;
    
    bool bPassedCut = false;
    float sphericity = (1.5*(eigenvalues[0]+eigenvalues[1]));
    //std::cout << "S = " << sphericity << ", Q1 = " << eigenvalues[0] << ", Q2 = " << eigenvalues[1] << ", Q3 = " << eigenvalues[2] << std::endl;
    if ( !(sphericity <= 1.0 && sphericity >=0) ){
      throw cms::Exception("LogicError") << "Expected sphericity to be in range  0 <= S <=1, was " << sphericity << " at " << __FILE__ << ":" << __LINE__ << std::endl;
    }
    /// NOTE: sphericity is collinear unsafe (e.g. pi0 -> gamma gamma: use pi0 or decay products changes result)      
    output.sMomentumTensor.fSphericity = sphericity;

    /// Check whether cut is passed
    if( output.sMomentumTensor.fSphericity > fSphericityCut){
      bPassedCut = true;
      increment(fSphericityCutCount);
    }
          
    /// Fill Histos
    hSphericity->Fill(output.sMomentumTensor.fSphericity);

    return bPassedCut;
  }
  
  bool EvtTopology::CalcAplanarity(vector<float> eigenvalues, EvtTopology::Data& output){
    
    /// Aplanarity (A) = 3/2*(Q1)    0 <= A <= 0.5    
    /// A = 0.5 for spherical, A=0 for planar/linear events

    if (output.sMomentumTensor.fQOne < 0) return false;

    bool bPassedCut = false;
    float aplanarity = (1.5*eigenvalues[0]);
    if ( !(aplanarity <= 0.5 && aplanarity >=0) ){
      throw cms::Exception("LogicError") << "Expected aplanarity to be in range  0 <= A <=0.5, was " << aplanarity << " at " << __FILE__ << ":" << __LINE__ << std::endl;
    }
    output.sMomentumTensor.fAplanarity = aplanarity;

    /// Check whether cut is passed
    if( output.sMomentumTensor.fAplanarity > fAplanarityCut){
      bPassedCut = true;
      increment(fAplanarityCutCount);
    }
          
    /// Fill Histos
    hAplanarity->Fill(output.sMomentumTensor.fAplanarity);

    return bPassedCut;
  }
  
  bool EvtTopology::CalcPlanarity(vector<float> eigenvalues, EvtTopology::Data& output){

    /// CMSSW definition for Planarity:
    /// Planarity (P) = Q1/Q2     ? <= P <= ?
    // float planarity = (eigenvalues[0]/eigenvalues[1]);
    /// TextBook definition for Planarity:
    /// Planarity (P) = 3/2*(S-2A) = Q2-Q1     0 <= P <= 0.5

    if (output.sMomentumTensor.fQOne < 0) return false;
    
    bool bPassedCut = false;
    float planarity = (eigenvalues[1]-eigenvalues[0]);
    if ( !(planarity <= 0.5 && planarity >=0) ){
      throw cms::Exception("LogicError") << "Expected planarity to be in range  0 <= P <=0.5, was " << planarity << " at " << __FILE__ << ":" << __LINE__ << std::endl;
    }
    output.sMomentumTensor.fPlanarity = planarity;

    /// Check whether cut is passed
    if( output.sMomentumTensor.fPlanarity > fPlanarityCut){
      bPassedCut = true;
      increment(fPlanarityCutCount);
    }
          
    /// Fill Histos
    hPlanarity->Fill(output.sMomentumTensor.fPlanarity);

    return bPassedCut;
  }
  
  
  bool EvtTopology::CalcCircularity(const edm::PtrVector<pat::Jet>& jets, EvtTopology::Data& output){

    /// Circularity (C) = 2*min(Q1,Q2)/(Q1+Q2)  0 <= C <= 1
    /// C = 1 for spherical, C = 0 for linear events
    
    if (output.sMomentumTensor.fQOne < 0) return false;
    
    bool bPassedCut = false;
    float circularity = -1, phi=0.0, area = 0.0;
    const int nSteps = 1000;
    const float deltaPhi=2*TMath::Pi()/nSteps;

    /// Loop over all selected jets
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {    
      edm::Ptr<pat::Jet> iJet = *iter;
      area+=TMath::Sqrt( iJet->px()*iJet->px() + iJet->py()*iJet->py() );
    }//eof: jet loop
        
    /// Loop over number of steps
    for(int i=0; i< nSteps; ++i){
      phi+=deltaPhi;
      float sum=0.0, tmp=0.0;
      
      /// Loop over all selected jets
      for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {    
	edm::Ptr<pat::Jet> iJet = *iter;
	sum+=TMath::Abs(TMath::Cos(phi)*iJet->px()+TMath::Sin(phi)*iJet->py());
      }
      tmp=TMath::Pi()/2*sum/area;
      if( circularity<0 || tmp<circularity ){
	circularity=tmp;
      }
    }
    
    if ( !(circularity <= 1.0 && circularity >=0) ){
      throw cms::Exception("LogicError") << "Expected circularity to be in range  0 <= C <=1.0, was " << circularity << " at " << __FILE__ << ":" << __LINE__ << std::endl;
    }
    output.sMomentumTensor.fCircularity = circularity;
    
    /// Check whether cut is passed
    if( output.sMomentumTensor.fCircularity > fCircularityCut){
      bPassedCut = true;
      increment(fCircularityCutCount);
    }
    
    /// Fill Histos
    hCircularity->Fill(output.sMomentumTensor.fCircularity);
    
    return bPassedCut;
  }
  
  
}
