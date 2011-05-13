//#######################################################################
// -*- C++ -*-
//       File Name:  EvtTopology.cc
// Original Author:  Alexandros Attikis
//         Created:  Mon 4 Oct 2010
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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1F.h"
#include "Math/GenVector/VectorUtil.h"

namespace{
  
  vector<float> AlphaTAux( const unsigned iNJets, int iCombinationIndex, const std::vector<Float_t> vEt, const std::vector<Float_t> vPx, const std::vector<Float_t> vPy, const std::vector<Float_t> vPz, const TLorentzVector& tau, bool bTauJetExists ){
    
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    /// Description                                                                                              
    /// This function works in parallel with EvtTopology::alphaT(..). It takes as input the number of jets       
    /// in the Event and the "winning combination" in terms of minimising the quantity:                          
    /// DeltaHt = |Ht_pseudoJet1 - Ht_pseudoJet2| of the pseudo-jets.                                            
    /// The function then loops over the jets of the "winning combination" and puts the jets into two groups     
    /// differentiated by which one contains the "Tau-jet". Then, for each PseudoJetGroup it loops over all      
    /// possible DiJets combinations and calculates their DiJet mass and stores them in a vector of floats       
    /// It is worth stating here that the number of possible DiJets that can be formed from a pool of iJets is:  
    /// nCr = iNJets! / (iNJtets-2)!2!                                                                         
    /// so, for example: iNJets = 5, nCr = 5! / (3!2!) = 5x2 = 10                                              
    /// so, for example: iNJets = 4, nCr = 4! / (2!2!) = 3x2 = 6                                              
    /// so, for example: iNJets = 3, nCr = 3! / (1!2!) = 3x1 = 3                                             
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    /// Variable Declaration
    bool bPseudoJetsGroupA = 0;
    bool bTauJetInGroupA   = 0;
    bool bTauJetInGroupB   = 0;
    vector<float> vDiJetMassesNoTau;
    vector<float> vEmpty;
    MathFunctions oMath;
    vector<TLorentzVector> vJetsInTauPseudoJet;
    vector<TLorentzVector> vJetsInNonTauPseudoJet;
    vector<TLorentzVector> vJetsInPseudoJetA;
    vector<TLorentzVector> vJetsInPseudoJetB;
    
    /// The calculation only takes place if a "Tau-jet" exists in the Event.
    if(!bTauJetExists){return vEmpty;}
    
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
      } //eof: if(bPseudoJetsGroupA){
      else{ /// If current jet is in groupB (0's)
	TLorentzVector tmpJet;
	tmpJet.SetPx( vPx[l] );
	tmpJet.SetPy( vPy[l] );
	tmpJet.SetPz( vPz[l] );
	vJetsInPseudoJetB.push_back(tmpJet);
      } //eof: else{
    } //eof:  for ( unsigned l=0; l < iNJets; l++ ) {
    
    /// Determine in which of the two pseudo-jets the tau-jet is found.
    for(unsigned i = 0; i < vJetsInPseudoJetA.size(); i++){
      TLorentzVector tauJetCandidate;
      tauJetCandidate.SetXYZM(vJetsInPseudoJetA[i].Px(), vJetsInPseudoJetA[i].Py(),vJetsInPseudoJetA[i].Pz(), 1.777);
      float fDeltaR = oMath.getDeltaR( oMath.getDeltaPhi(tauJetCandidate.Phi(),tau.Phi()), oMath.getDeltaEta(tauJetCandidate.Eta(),tau.Eta()) );      
      /// make sure that it is indeed the tau-jet. Comapare Et and deltaR
      if( (fabs(tau.Et() - tauJetCandidate.Et()) < 2.0) && (fabs(fDeltaR) < 0.5) ){bTauJetInGroupA = 1;}
    }//eof: for(unsigned i = 0; i < vJetsInPseudoJetA.size(); i++){
    if(bTauJetInGroupA){
      // std::cout << "Tau-jet found in Pseudo-Jet A" << std::endl;
      vJetsInTauPseudoJet    = vJetsInPseudoJetA;
      vJetsInNonTauPseudoJet = vJetsInPseudoJetB;
    }else{
      // std::cout << "Tau-jet found in Pseudo-Jet B" << std::endl;
      vJetsInTauPseudoJet    = vJetsInPseudoJetB;
      vJetsInNonTauPseudoJet = vJetsInPseudoJetA;
    }
    /// We now have a vector containing the Jets comprising each PseudoJet. We want to calculate the DiJet mass for all combination for the 
    /// PseudoJet that doesn't contain the Tau-Jet, hoping to reconstruct the W mass. Use a double loop with the outside index "m" and the 
    /// inside index "n=m+1" to avoid double counting.
    int iJetsInNonTauPseudoJet = vJetsInNonTauPseudoJet.size();
    
    /// If the PseudoJet has less than 2 jets (impossible to calculate InvMass), abort calculation and return an empty vector
    if(iJetsInNonTauPseudoJet<2){return vEmpty;}
    
    for(int m = 0; m < iJetsInNonTauPseudoJet; m++){
      for(int n = m+1; n < iJetsInNonTauPseudoJet; n++){
	
	float E1 = vJetsInNonTauPseudoJet[m].Energy();
	float E2 = vJetsInNonTauPseudoJet[n].Energy();
	
	TLorentzVector P1 = vJetsInNonTauPseudoJet[m];
	TLorentzVector P2 = vJetsInNonTauPseudoJet[n];
	
	float fDiJetMassNoTau =  sqrt( (E1+E2)*(E1+E2) - (P1+P2).Mag2() );
	vDiJetMassesNoTau.push_back(fDiJetMassNoTau);
      } //eof: for(int n = m+1; m < vJetsInNonTauPseudoJet.size(); n++){
    } //eof: for(int m = 0; m < vJetsInNonTauPseudoJet.size(); m++){
    
    /// Reset variables
    bTauJetInGroupA = 0;
    bTauJetInGroupB = 0;
    
    return vDiJetMassesNoTau;
    
  }//eof: static vector<float> alphaTAux(...){
  
}//eof: namespace{


namespace HPlus {
  EvtTopology::Data::Data(const EvtTopology *evtTopology, bool passedEvent):
    fEvtTopology(evtTopology), fPassedEvent(passedEvent) {}
  EvtTopology::Data::~Data() {}

  EvtTopology::EvtTopology(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    // fDiscriminator(iConfig.getUntrackedParameter<std::string>("discriminator")),
    // fDiscrCut(iConfig.getUntrackedParameter<double>("discriminatorCut")),
    fAlphaTCut(iConfig.getUntrackedParameter<double>("alphaT")),
    fEvtTopologyCount(eventCounter.addSubCounter("EvtTopology main","EvtTopology cut")),
    fAlphaTCutCount(eventCounter.addSubCounter("EvtTopology", "alphaT")),
    fEventWeight(eventWeight)
  {
    edm::Service<TFileService> fs;
    hAlphaT = makeTH<TH1F>(*fs, "alphaT", "alphaT", 50, 0.0, 5.0);
    /*
    hDiJetInvMass      = makeTH<TH1F>(*fs, "EvtTopology_DiJetInvMass", "EvtTopology_DiJetInvMass", 1000, 0.0, 1000.0);
    hDiJetInvMassCutFail    = makeTH<TH1F>(*fs, "EvtTopology_DiJetInvMassCutFail", "EvtTopology_DiJetInvMassCutFail", 1000, 0.0, 1000.0);
    hDiJetInvMassCutPass    = makeTH<TH1F>(*fs, "EvtTopology_DiJetInvMassCutPass", "EvtTopology_DiJetInvMassCutPass", 1000, 0.0, 1000.0);
    hDiJetInvMassWCutFail   = makeTH<TH1F>(*fs, "EvtTopology_DiJetInvMassWCutFail", "EvtTopology_DiJetInvMassWCutFail", 1000, 0.0, 1000.0);
    */
  }

  EvtTopology::~EvtTopology() {}

  EvtTopology::Data EvtTopology::analyze( const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets ){

  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /// Description                                                                                                
  /// Calculates the AlphaT variable, defined as an N-object system where the set of objects is 1 tau-jet and N-1
  /// jets. This definition reproduces the kinematics of a di-jet system by constructing two pseudo-jets, which balance
  /// one another in Ht. The two pseudo-jets are formed from the combination of the N objects that minimizes the
  /// DeltaHt = |Ht_pseudoJet1 - Ht_pseudoJet2| of the pseudo-jets.                                             
  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    /// Declaration of variables 
    std::vector<float> vEt, vPx, vPy, vPz;
    std::vector<bool> vPseudo_jet1;
    const bool bList = true;
    const bool bTauJetExists = true;
    bool bPassedCut = false;
    /// Tau
    TLorentzVector myTau;
    myTau.SetXYZM(tau.px(), tau.py(), tau.pz(), 1.777); 
    /// Fill vectors with Tau-jet information
    vEt.push_back( myTau.Et() );
    vPx.push_back( myTau.Px() );
    vPy.push_back( myTau.Py() );
    vPz.push_back( myTau.Pz() );

    /// Loop over all selected jets
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {    
      edm::Ptr<pat::Jet> iJet = *iter;
      /// Fill vectors with jets information (jets are SORTED in energy)
      vEt.push_back( iJet->et() );
      vPx.push_back( iJet->px() );
      vPy.push_back( iJet->py() );
      vPz.push_back( iJet->pz() );
    }//eof: for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {    
    /// Declaration of variables 
    unsigned iNJets = vEt.size();
    int iCombinationIndex = -1;

    /// Calculate sums
    float fSum_et = accumulate( vEt.begin(), vEt.end(), 0.0 );
    float fSum_px = accumulate( vPx.begin(), vPx.end(), 0.0 );
    float fSum_py = accumulate( vPy.begin(), vPy.end(), 0.0 );
    /// Minimum Delta Et for two pseudo-jets
    float fMin_delta_sum_et = -1.0;
    
    if(iNJets > 18){ 
      // Fill the function structure with -2.0 to indicate that combinatorics too much
      sAlpha.fAlphaT  = -2.0;
      sAlpha.fJt      = -2.0;
      sAlpha.fHt      = -2.0;
      sAlpha.fDeltaHt = -2.0;
      sAlpha.fMHt     = -2.0;
      return Data(this, false);
    }

    /// Iterate through different combinations
    for ( unsigned k=0; k < unsigned(1<<(iNJets-1)); k++ ) { 
      float fDelta_sum_et = 0.0;
      std::vector<bool> jet;
      /// Iterate through jets
      for ( unsigned l=0; l < vEt.size(); l++ ) { 
	// Bitwise shift of "k" by "l" positions to the right and compare to 1 (&1)
	fDelta_sum_et += vEt[l] * ( 1 - 2 * (int(k>>l)&1) ); 
	// i.e.: fDelta_sum_et += vEt[l] * ( 1 - 2*0 );  if comparison is un-successful
	//  or   fDelta_sum_et += vEt[l] * ( 1 - 2*1 );  if comparison is successful
	// in this way you add up all Et from PseudoJetsGroupA (belonging to 0's group) and subtract that from PseudoJetsGroupB (1's group)
	if ( bList ) { jet.push_back( (int(k>>l)&1) == 0 ); } 
      } //eof:  for ( unsigned l=0; l < vEt.size(); l++ ) {
      /// Find configuration with minimum value of DeltaHt 
      if ( ( fabs(fDelta_sum_et) < fMin_delta_sum_et || fMin_delta_sum_et < 0.0 ) ) {
	fMin_delta_sum_et = fabs(fDelta_sum_et);
	iCombinationIndex = k; /// overwritten everytime a new minimum is found
	if ( bList && jet.size() == vEt.size() ){vPseudo_jet1.resize(jet.size());}
      } //eof: if ( ( fabs(fDelta_sum_et) < fMin_delta_sum_et || fMin_delta_sum_et < 0.0 ) ) {
    } //eof: for ( unsigned k=0; k < unsigned(1<<(iNJets-1)); k++ ) { 
    
    /// Get DiJet information from Pseudo-jets
    vector<float> vDiJetMassesNoTau =  AlphaTAux(iNJets, iCombinationIndex, vEt, vPx, vPy, vPz, myTau, bTauJetExists );
    // std::cout << "3) vDiJetMassesNoTau.size() = " <<  vDiJetMassesNoTau.size() << std::endl;
    /// In the case something goes wrong...
    if ( ( fMin_delta_sum_et < 0.0 ) || (!bTauJetExists) ){ 
      /// Fill the function structure with -1.0
      sAlpha.fAlphaT  = -1.0;
      sAlpha.fJt      = -1.0;
      sAlpha.fHt      = -1.0;
      sAlpha.fDeltaHt = -1.0;
      sAlpha.fMHt     = -1.0;
    } //eof: if ( ( fMin_delta_sum_et < 0.0 ) || (bTauJetExists) ){
    else{
      /// Remember, the Tau-Jet is stored in the "vEt" vector FIRST. The jets (sorted in Energy) are stored right after the Tau-jet.
      float fHt = fSum_et;
      float fJt = fSum_et - vEt[0] - vEt[1]; // Ht without considering the Ldg Jet of the Event & excluding Tau-jet
      float fDeltaHt = fMin_delta_sum_et;
      float fMHt     = sqrt(pow(fSum_px,2) + pow(fSum_py,2));
      float fAlphaT = ( 0.5 * ( fHt - fDeltaHt ) / sqrt( pow(fHt,2) - pow(fMHt,2) ) );
      /// Fill the function structure
      sAlpha.fAlphaT  = fAlphaT;
      sAlpha.fJt      = fJt;
      sAlpha.fHt      = fHt;
      sAlpha.fDeltaHt = fDeltaHt;
      sAlpha.fMHt     = fMHt;
      sAlpha.vDiJetMassesNoTau = vDiJetMassesNoTau;
    } //eof: else{
    if( sAlpha.fAlphaT > fAlphaTCut){
      bPassedCut = true;
      increment(fAlphaTCutCount);
    }
    
    if(bPassedCut){
      increment(fEvtTopologyCount);
    } // in the future one might add Ht cut or Jt cut or Invariant mass Cuts.
    
    /// Fill Histos
    hAlphaT->Fill(sAlpha.fAlphaT, fEventWeight.getWeight());

    // if(vDiJetMassesNoTau.size()>1){std::cout << "*** bool EvtTopology::analyze(...) *** Found " << vDiJetMassesNoTau.size() << " jets in the Pseudo-Jet without the tau-Jet. This means there are " << (oMath.Factorial(vDiJetMassesNoTau.size())/(oMath.Factorial(vDiJetMassesNoTau.size()-2)*2)) << " possible DiJet mass combinations." << std::endl;}

    return Data(this, bPassedCut);
  } //eof: bool EvtTopology::alphaT( const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets ){
  
 
}//eof: namespace HPlus {
