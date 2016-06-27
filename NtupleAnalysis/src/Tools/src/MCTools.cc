#include "Tools/interface/MCTools.h"
#include "Framework/interface/Exception.h"

#include "TFile.h"
#include "TH1.h"

//#define DEBUG

MCTools::MCTools(Event &fEvt){
  fEvent = &fEvt;
  if( fEvent->isData()==true ) return; 
}


MCTools::~MCTools(){}  

bool MCTools::IsNeutrino(const int pdgId){
  if( ( fabs(pdgId) == 12)  || ( fabs(pdgId) == 14)  || ( fabs(pdgId) == 16) ) return true;
  else return false;
}


//GenParticle MCTools::GetGenP(const size_t genP_Index){
//  return fEvent->genparticles()[genP_Index];
//  //could not convert 'GenParticle::operator[](size_t) const(((size_t)genP_Index))' from 'GenParticle' to 'GenParticle'
//}
//

TLorentzVector MCTools::GetP4(const int genP_Index){

  TLorentzVector p4;
/*
  GenParticle genP = GetGenP(genP_Index);
  double genP_Pt   = genP.pt();
  double genP_Eta  = genP.eta();
  double genP_Phi  = genP.phi();                                                                                                                                           
  double genP_Mass = genP.mass();
  p4.SetPtEtaPhiM(genP_Pt, genP_Eta, genP_Phi, genP_Mass);
*/
  return p4;
}


bool MCTools::RecursivelyLookForMotherId(const unsigned int genP_Index,
					 int momId,
					 const bool bAbsoluteMomId){
  
  /* 
     Description:
     Investigate all the mothers of the GenParticle with index "genP_Index". 
     If any of the GenParticle's mothers has an id equal to "momId" return true,
     otherwise return false. 
   */

  // cout << "=== MCTools::RecursivelyLookForMotherId():\n\t Requires debugging!" << endl;
/*
  GenParticle genP     = GetGenP(genP_Index);
  unsigned short nMoms = genP.mothers().size();
  if (nMoms == 0) return false;
*/
#ifdef DEBUG
  cout << "Looking for mother #" << momId << " of GenParticle with index (pdgid) "<< genP_Index << "(" << genP_pdgId << ")" << endl;
#endif
  /*
  int myId;
  // For-loop: All mothers
  for (unsigned short i = 0; i < nMoms; i++){
    unsigned int mom_Index = genP.mothers().at(i);
    GenParticle mom        = GetGenP(mom_Index);
    int mom_PdgId          = mom.pdgId();

    // cout << "genP_Index = " << genP_Index << ", genP_PdgId = " << genP_PdgId << ", mom_Index = " << mom_Index << ", mom_PdgId = " << mom_PdgId << endl;

    if (!bAbsoluteMomId) 
      {
	myId  = fabs(mom_PdgId);
	momId = fabs(momId);
      }
    else myId = mom_PdgId;
    if (myId == momId) return true;
    if (RecursivelyLookForMotherId(mom_Index, momId, bAbsoluteMomId) ) return true;
  }
*/
  return false;
}


int MCTools::GetPosOfMotherId(const unsigned int genP_Index,
			      int momId,
			      const bool bAbsoluteMomId){
  
  /* 
     Description:
     Investigate all the mothers of the GenParticle with index "genP_Index". 
     If any of the GenParticle's mothers has an id equal to "momId" return its index,
     otherwise return -1

     Note:
     What if there are more than 1 mothers? In that case what should I return? 
   */
/*
  GenParticle genP     = GetGenP(genP_Index);
  unsigned short nMoms = genP.mothers().size();
  if (nMoms == 0) return -1; // 65535;
  int myId;
  int mom_Index;

  // For-loop: All mothers
  for (unsigned short i = 0; i < nMoms; i++){

    mom_Index = genP.mothers().at(i);
    GenParticle mom = GetGenP(mom_Index);
    int mom_PdgId   = mom.pdgId();

    if (!bAbsoluteMomId) {
      myId = fabs(mom_PdgId);
      momId = fabs(momId);
    }
    else {
      myId = mom_PdgId;
    } 
    int status = mom.status();
    if (myId == momId) {
      if (status == 3) {
	if(mom.daughters().size()>2){
	  mom_Index = mom.daughters().at(2);
	  return mom_Index;
	}
	else return -1; //65535;
      }
      else return mom_Index;
    }
    else {
      mom_Index = GetPosOfMotherId(mom_Index, momId, bAbsoluteMomId);
      return mom_Index;
    }
  }// for (unsigned short i = 0; i < nMoms; i++){
*/
  return -1;//65535;
}



bool MCTools::LookForMotherId(const unsigned int genP_Index,
			      int momId,
			      const bool bAbsoluteMomId){

  /* 
     Description:
     Investigate the immediate mothers of the GenParticle with index "genP_Index". 
     If an immediate mother has an id equal to "momId" return true,
     otherwise return false.

     Note:
     What if there are more than 1 mothers? In that case what should I return? 
   */
/*
  GenParticle genP     = GetGenP(genP_Index);
  unsigned short nMoms = genP.mothers().size();

  if (nMoms == 0) return false;
  int myId;

  // For-loop: All mothers
  for (unsigned short i = 0; i < nMoms; i++) {

    unsigned short mom_Index = genP.mothers().at(i);
    GenParticle mom          = GetGenP(mom_Index);
    int mom_PdgId            = mom.pdgId();

    if (!bAbsoluteMomId) {
      myId  = fabs(mom_PdgId);
      momId = fabs(momId);
    }
    else myId = mom_PdgId;
    if (myId == momId) return true;

  }// for (unsigned short i = 0; i < nMoms; i++) {
*/
  return false;
}


TLorentzVector MCTools::GetVisibleP4(const unsigned int genP_Index){

  // Overloaded version ofTLorentzVector MCTools::GetVisibleP4() 

  TLorentzVector p4(0,0,0,0);
/*
  GenParticle genP = GetGenP(genP_Index);
  const vector<short unsigned int> daughters = genP.daughters();

  TLorentzVector p4(0,0,0,0);
  if (daughters.size() == 0) return p4;

  // For-loop: Daughters
  for (unsigned short i = 0; i< daughters.size(); i++){

    int dau_Index   = daughters.at(i);
    GenParticle dau = GetGenP(dau_Index);
    int dau_PdgId   = dau.pdgId();
    double dau_Pt   = dau.pt();
    double dau_Eta  = dau.eta();
    double dau_Phi  = dau.phi();                                                                                                                                           
    double dau_Mass = dau.mass();

    // Skip invisible daughters (neutrinos)
    if ( IsNeutrino(dau_PdgId) ) continue;

    TLorentzVector tmp;
    tmp.SetPtEtaPhiM(dau_Pt, dau_Eta, dau_Phi, dau_Mass);
    p4 += tmp;

  } // For-loop: Daughters
*/
  return p4;
}


int MCTools::GetLdgDaughter(const int genP_Index, 
			    bool bOnlyChargedDaughters){
  int ldgPtIndex = -1;  

/*
  GenParticle genP = GetGenP(genP_Index);
  const vector<short unsigned int> daughters = genP.daughters();

  // Declarations
  int ldgPtIndex = -1;
  double ldgPt   = -1.0;

  if (daughters.size() == 0) return ldgPtIndex;

  // For-loop: Daughters
  for (size_t i = 0; i< daughters.size(); i++){
    
    int dau_Index   = daughters.at(i);
    GenParticle dau = GetGenP(dau_Index);
    int dau_PdgId   = dau.pdgId();

    // Skip invisible daughters (neutrinos)
    if ( IsNeutrino(dau_PdgId) ) continue;

    // Get pt and charge
    double dau_Pt  = dau.pt();
    int dau_Charge = dau.charge();
    
    if(bOnlyChargedDaughters && fabs(dau_Charge) < 1 ) continue;

    // Find leading daughter index
    if (dau_Pt > ldgPt ){
      ldgPt      = dau_Pt;
      ldgPtIndex = dau_Index;
    }
    
  }  // For-loop: Daughters
*/
  return ldgPtIndex;
}


double MCTools::GetHadronicTauMaxSignalCone(const int genP_Index,
					    bool bOnlyChargedDaughters, 
					    double minPt){
  double dRMax = -1.0;

/*
  GenParticle genP = GetGenP(genP_Index);

  if ( abs(genP.pdgId()) != 15) {
#ifdef DEBUG
    cout << "=== MCTools::GetHadronicTauMaxSignalCone():" << endl;
    cout << "\t Particle with index " << genP_Index << " is not a tau (pdgId = " << genP.pdgId() << "). Return" << endl;
#endif
    return 0.0;
  }

  const vector<short unsigned int> daughters = genP.daughters();
  if (daughters.size() <= 1) return -1;

  // Get Ldg Charged Track properties
  const int ldgChTk_Index   = GetLdgDaughter(genP_Index, true);
  TLorentzVector ldgChTk_P4 = GetP4(ldgChTk_Index);

  double dRMax = -1.0;

  // For-loop: Daughters
  for (size_t i = 0; i< daughters.size(); i++){

    int dau_Index   = daughters.at(i);
    GenParticle dau = GetGenP(dau_Index);
    int dau_PdgId   = dau.pdgId();

    // Skip self and neutrinos
    if (dau_Index == ldgChTk_Index) continue;
    if (IsNeutrino(dau_PdgId)) continue;

    // Get Daughter properties
    TLorentzVector dau_P4 = GetP4(dau_Index);
    int dau_Charge        = dau.charge();

    // Consider only charged daughters above minPt
    if (dau_P4.Pt() < minPt) continue;
    if (bOnlyChargedDaughters){ if( fabs(dau_Charge) < 1 ) continue; }

    double dR = ROOT::Math::VectorUtil::DeltaR(ldgChTk_P4, dau_P4);
    if (dR > dRMax) dRMax = dR;
    
  } // For-loop: Daughters
*/
  return dRMax;
}


void MCTools::GetHadronicTauFinalDaughters(const int genP_Index,
					   vector<short int>& finalDaughters){
/*
  cout << "=== MCTools::GetHadronicTauFinalDaughters():\n\t Requires debugging!" << endl;
  GenParticle genP = GetGenP(genP_Index);
  int genP_PdgId   = abs(genP.pdgId());

  if (genP_PdgId != 15) {
#ifdef DEBUG
    cout << "=== MCTools::GetHadronicTauFinalDaughters():" << endl;
    cout << "\t Particle with index " << genP_Index << " is not a tau (pdgId = " << genP.pdgId() << "). Return" << endl;
#endif
    return;
  }

  if (genP.daughters().size() == 0) return;

  // For-loop: Daughters
  for (size_t i = 0; i< genP.daughters().size(); i++){

    int dau_Index   = genP.daughters().at(i);
    GenParticle dau = GetGenP(dau_Index);
    int dau_PdgId   = dau.pdgId();

    // Keep only the pi+/-,pi0, K+/-, 
    // K0,K0L,KOS,eta,omegas and gammas from tau->tau+gamma transition
    if ( (dau_PdgId == 111 || dau_PdgId == 211 || dau_PdgId == 321 ||   //pi0,pi+/-,K+/-
          dau_PdgId == 130 || dau_PdgId == 310 || dau_PdgId == 311 ||   //K0L,K0S,K0
	  dau_PdgId == 211 || dau_PdgId == 223)                     //eta and omega
	 || (dau_PdgId == 22 && genP_PdgId==15 && finalDaughters.size()!=0 ) ){  //Avoid leptonic decay
      // Because of the mixing of Generator and Detector simulation particles
      // in the list check if the particle has a parent already in the list
      // If it does then it comes from a hadronic interaction with the
      // detector material and it is not part of the tau decay
      int ifound = 0;

      // For-loop: Daughters
      for (size_t j = 0; j < finalDaughters.size(); j++){

	int jdau_Index   = finalDaughters.at(j);
	GenParticle jdau = GetGenP(jdau_Index);
	int jdau_PdgId   = jdau.pdgId();
	if (RecursivelyLookForMotherId(dau_Index, jdau_PdgId, true) ) ifound += 1;

      }// for (short int j=0; j< daughters.size(); j++){

      if (ifound == 0) finalDaughters.push_back(dau_Index);
    
    } // if ( (dau_PdgId == 111 ...

    GetHadronicTauFinalDaughters(dau_Index, finalDaughters);
  }
*/
  return;
}



void MCTools::_GetHadronicTauChargedOrNeutralPions(int genP_Index, 
						   bool charged,
						   vector<short int> &pions){
/*
  cout << "=== MCTools::_GetHadronicTauChargedOrNeutralPions():\n\t Requires debugging!" << endl;  

  // Only consider taus
  GenParticle genP = GetGenP(genP_Index);

  if (TMath::Abs( genP.pdgId() ) != 15){
#ifdef DEBUG
    cout << "=== MCTools::_GetHadronicTauChargedOrNeutralPions():" << endl;
    cout << "\t Particle with index " << genP_Index << " is not a tau (pdgId = " << genP.pdgId() << "). Return" << endl;
#endif    
    return;
  }
  
  if (genP.daughters().size() == 0) return;

  // Get the pi+/-,pi0, K+/-, K0, K0L, KOS, Eta, Omegas and Gammas
  vector<short int> daughters;
  GetHadronicTauFinalDaughters(genP_Index, daughters);
  
  // For-loop: Daughters
  for (unsigned short i = 0; i< daughters.size(); i++){

    // Get the daughter properties
    int dau_Index   = daughters.at(i);
    GenParticle dau = GetGenP(dau_Index);
    int dau_Charge  = dau.charge();

    // Keep only the pi+/-, K+/-, omegas
    if (charged && abs(dau_Charge)==0 ) continue;

    // Keep only the p0, K0 etc..
    if (!charged && abs(dau_Charge)!=0 ) continue;

    // Save to container
    pions.push_back(dau_Index);
    
  } // For-loop: Daughters
*/  
  return;
}


void MCTools::GetHadronicTauNeutralPions(const int genP_Index, 
					 vector<short int> &neutralPions){

  _GetHadronicTauChargedOrNeutralPions(genP_Index, false, neutralPions);
  return;
}


void MCTools::GetHadronicTauChargedPions(const int genP_Index, 
					 vector<short int> &chargedPions){

  _GetHadronicTauChargedOrNeutralPions(genP_Index, true, chargedPions);
  return;
}


bool MCTools::IsFinalStateTau(const int genP_Index){

  /*
    Description:
    Investigate the GenParticle with index "genP_Index". 
    If it is not a tau (pdgId=15) return false.
    if it has a tau daughter (pdgId=15) return false.
    Otherwise, return true.
    In other words, it checks if a tau decays to a tau.
    If yes, return false.
  */
/*
  GenParticle genP = GetGenP(genP_Index);
  int genP_PdgId   = genP.pdgId();

  // Only consider taus
  if (TMath::Abs( genP_PdgId ) != 15) return false;

  const vector<short unsigned int> daughters = genP.daughters();
  // For-loop: All daughters
  for (unsigned short i = 0; i < daughters.size(); i++){

    int dau_Index   = daughters.at(i);
    GenParticle dau = GetGenP(dau_Index);
    int dau_PdgId   = dau.pdgId();   
    if ( TMath::Abs(dau_PdgId) == 15) return false;
  }
*/
  return true;
}


int MCTools::GetTauDecayMode(const int genP_Index){
  
  /*
    Description:
    Investigate the GenParticle with index "genP_Index". 
    If not a tau-lepton return -1. If the decay is unknown
    (i.e. not supported) return -1.

    Otherwise determine  the decay mode by counting the 
    charged/neutral Pions, Kaons, leptons etc..
  */

  cout << "=== MCTools::GetTauDecayMode():\n\t Requires debugging!" << endl;
/*  
  GenParticle genP = GetGenP(genP_Index);
  int genP_PdgId   = genP.pdgId();

  // Only consider taus
  if (TMath::Abs( genP_PdgId ) != 15) return -1;

  unsigned int nPipm = 0;
  unsigned int nPi0s = 0;
  unsigned int nKpm  = 0;
  unsigned int nCharged=0;
  unsigned int nOtherCharged = 0; // Other than pions, Kaons.
  unsigned int nOtherNeutral = 0; // K_S, K_L, Sigma, etc..
  unsigned int nLeptons = 0;      // e, mu

  const vector<short unsigned int> daughters = genP.daughters();
  if (daughters.size() <= 0) return -1;

  // For-loop: All daughters
  for (unsigned short i = 0; i < daughters.size(); i++){

    int dau_Index   = daughters.at(i);
    GenParticle dau = GetGenP(dau_Index);
    // int dau_PdgId   = dau.pdgId();   
    int dau_Charge  = dau.charge();   
    
    // Leptonic decays
    if ( fabs(dau_Index) == 11 || fabs(dau_Index) == 13 ) nLeptons++;
    
    if (dau_Charge > 0) {
      nCharged++;
      if (dau_Index == 211) {
	nPipm++;
      }
      else if (dau_Index == 321){
	nKpm++;
      }
      else {
	nOtherCharged++;
      }
    }
    else {
      if (dau_Index == 111){
	nPi0s ++;
      }
      else{
	nOtherNeutral++;
      }
    }
  }  // For-loop: Daughters
  
  // Determine return value
  if (nLeptons !=0 ) return 2;
  
  if (nOtherNeutral !=0 ) {
    return ((nCharged/2)*10 + 8);      // it returns 8, 18, 28 for 1, 3, 5 prong
  }
  else{
    return ((nCharged/2)*10 + nPi0s); // it returns a value depending on nProngs+nPi0s (i.e. 3prongs+3pi0 =13)
  }
*/
  return 0; // unknown decay
}


void MCTools::PrintMothersRecursively(const int genP_Index, bool bPrintHeaders){
/*
  GenParticle genP = GetGenP(genP_Index);
  int genP_PdgId   = genP.pdgId();

  const vector<short unsigned int> mothers = genP.mothers();
  if (mothers.size() == 0) return;

  if (bPrintHeaders) cout << "\n" << endl;
  if (bPrintHeaders) cout << setw(15*2) << genP_Index << " (" << genP_PdgId << ")" << endl;
  if (bPrintHeaders) cout << string(15*4, '=') << endl;
  if (bPrintHeaders) cout << setw(15) << "genP_Index " << setw(15) << "genP_PdgId" << setw(15) << "mom_Index " << setw(15) << "mom_PdgId" << endl;
  if (bPrintHeaders) cout << string(15*4, '=') << endl;

  // For-loop: All mothers
  for (unsigned short i = 0; i < mothers.size(); i++){

    int mom_Index   = mothers.at(i);
    GenParticle dau = GetGenP(mom_Index);
    int mom_PdgId   = dau.pdgId();

    cout << setw(15) << genP_Index << setw(15) << genP_PdgId << setw(15) << mom_Index << setw(15) << mom_PdgId << endl;

    PrintMothersRecursively(mom_Index, false);
  }

  if (bPrintHeaders) cout << string(15*4, '=') << endl;
*/
  return;
}


void MCTools::PrintDaughtersRecursively(const int genP_Index, bool bPrintHeaders){
/*
  GenParticle genP = GetGenP(genP_Index);
  int genP_PdgId   = genP.pdgId();

  const vector<short unsigned int> daughters = genP.daughters();
  if (daughters.size() == 0) return;

  if (bPrintHeaders) cout << "\n" << endl;
  if (bPrintHeaders) cout << setw(15*2) << genP_Index << " (" << genP_PdgId << ")" << endl;
  if (bPrintHeaders) cout << string(15*4, '=') << endl;
  if (bPrintHeaders) cout << setw(15) << "genP_Index " << setw(15) << "genP_PdgId" << setw(15) << "dau_Index " << setw(15) << "dau_PdgId" << endl;
  if (bPrintHeaders) cout << string(15*4, '=') << endl;

  // For-loop: All daughters
  for (unsigned short i = 0; i < daughters.size(); i++){

    int dau_Index   = daughters.at(i);
    GenParticle dau = GetGenP(dau_Index);
    int dau_PdgId   = dau.pdgId();

    cout << setw(15) << genP_Index << setw(15) << genP_PdgId << setw(15) << dau_Index << setw(15) << dau_PdgId << endl;

    PrintDaughtersRecursively(dau_Index, false);
  }

  if (bPrintHeaders) cout << string(15*4, '=') << endl;
*/
  return;
}


void MCTools::PrintGenParticle(const int genP_Index, bool bPrintHeaders){
/*
  GenParticle genP    = GetGenP(genP_Index);
  double genP_Pt      = genP.pt();
  double genP_Eta     = genP.eta();
  double genP_Phi     = genP.phi();
  double genP_Mass    = genP.mass();
  double genP_Energy  = genP.e();
  double genP_Status  = genP.status();
  double genP_PdgId   = genP.pdgId();
  double genP_Charge  = genP.charge();
  double genP_VertexX = genP.vertexX();
  double genP_VertexY = genP.vertexY();
  double genP_VertexZ = genP.vertexX();
  double genP_Mothers = genP.mothers().size();
  int genP_Daughters  = genP.daughters().size();
  int mom_1 = -1;
  int mom_2 = -1;
  int dau_1 = -1;
  int dau_2 = -1;

  if (bPrintHeaders)
    {
      if (bPrintHeaders) cout << "\n" << endl;
      if (bPrintHeaders) cout << string(15*10, '=') << endl;
      cout << setw(6)  << "Index "  << setw(10) << "PdgId"   << setw(12) << "Pt"     << setw(14) << "Eta"  << setw(12) << "Phi"
	   << setw(12) << "Mass "   << setw(12) << "Energy"  << setw(8)  << "Status" << setw(4)  << "Q"    << setw(12) << "VertexX"
	   << setw(12) << "VertexY" << setw(12) << "VertexZ" << setw(6)  << "Mom1"   << setw(6)  << "Mom2"
	   << setw(6)  << "Dau1"    << setw(6)  << "Dau2"    << endl;
      if (bPrintHeaders) cout << string(15*10, '=') << endl;
    }

  if (genP_Mothers > 0)
    {
      mom_1 = genP.mothers().at(0);
      mom_2 = genP.mothers().at(genP_Mothers-1);
    }
  if (genP_Daughters > 0)
    {
      dau_1 = genP.daughters().at(0);
      dau_2 = genP.daughters().at(genP_Daughters-1);
    }
  

  cout << std::setprecision(4)     << setw(6)  << genP_Index   << setw(10) << genP_PdgId   << setw(12) << genP_Pt     << setw(14) << genP_Eta  << setw(12) << genP_Phi
       << setw(12) << genP_Mass    << setw(12) << genP_Energy  << setw(8)  << genP_Status  << setw(4)  << genP_Charge << setw(12) << genP_VertexX
       << setw(12) << genP_VertexY << setw(12) << genP_VertexZ << setw(6)  << mom_1        << setw(6)  << mom_2
       << setw(6)  << dau_1        << setw(6)  << dau_2        << endl;  
  
  //  << setw(10) << setprecision(3) << genP_Pt
*/
  return;
}


double MCTools::GetLxy(const int genP_Index,
		       bool wrtPV){

  /* Description:
     Investigate the GenParticle with index "genP_Index". Find its 
     production and decay vertices. The method vertexX() returns the 
     production vertex. So, in order to determine the decay vertex 
     we take one of the particle's daughtes and ask for its prodution
     vertex. 

     Explanation:
     The distance traversed by a long-lived particle is Lxy (decay length).
     Assuming the origin (0, 0) as the Primary Vertex (the point where the
     particle was produced) and (vtx_X, vtx_Y) as the Secondary Vertex (the
     point where the long-lived particle reaches before decaying), then Lxy is
     obtained from Pythagoras theorem. Particles that decay promptly should 
     have Lxy very close to zero.

     Note: [from https://hypernews.cern.ch/HyperNews/CMS/get/generators/2429/1.html]
     In CMS default pythia8 configuration K_S^0 is considered long-lived
     enough that we leave them undecayed and they are passed to geant.  So geant
     will decay them, but you will see them as status 1 for what concerns the
     GenParticles.
     OTHER K_S^0).
  */
/*  
  GenParticle genP = GetGenP(genP_Index);
  double refX  = 0.0;
  double refY  = 0.0;

  const vector<short unsigned int> daughters = genP.daughters();
  if (daughters.size() == 0) return -1.0;

  // Get one of the daugthers to determine the decay vertex (What if no daughters?)
  int dau_Index   = daughters.at(0);
  GenParticle dau = GetGenP(dau_Index);
  double dau_VtxX = dau.vertexX(); // [in cm]
  double dau_VtxY = dau.vertexY(); // [in cm]
  if (wrtPV)
    {
      refX = GetVertexX();
      refY = GetVertexY();
    }
  double LxySq    = pow( (dau_VtxX - refX), 2) + pow( (dau_VtxY - refY), 2);
  double Lxy      = sqrt(LxySq);

#ifdef DEBUG
  cout << "Lxy = [(" << dau_VtxX << " - " << refX << ")^2 + (" <<  dau_VtxY << " - " << refY << ")^2]^(1/2) = " << Lxy << " [cm]" << endl;
#endif
*/
  return 0;//Lxy;
}


double MCTools::GetD0Mag(const int genP_Index,
			 const int mom_Index,
			 bool wrtPV){
  
  /* Description:
     Investigate the GenParticle with index "genP_Index". Find its 

     Explanation: 
     The distance traversed by a long-lived particle is Lxy (decay length).
     Particles that decay promptly should have Lxy very close to zero.
     Simple trigonometry will reveal that the tangent of the angle between the
     long-lived particles' decay product and it's own direction will give:
     sin( |phi_mom - genP_Phi| ) = d0/Lxy
     Then d0 can be simply obtained by multiplying the tangent of the azimuthal
     angle difference with the decay length Lxy.

     See:
     https://root.cern.ch/root/html524/TMath.html#TopOfPage
     https://root.cern.ch/doc/master/classTLorentzVector.html
  */
  /*
  // Ensure GenParticle with index genP_Index has mother with index mom_Index
  if ( !IsItsMother(genP_Index, mom_Index) ) return -1.0;

  // Ensure GenParticle with index genP_Index has more than 1 daughters
  GenParticle genP = GetGenP(genP_Index);
  if (genP.daughters().size() < 2) return -1.0;

  // Get 4-momenta (to calculate angle between the mother and daughter directions)
  TLorentzVector genP_p4 = GetP4(genP_Index);
  TLorentzVector mom_p4  = GetP4(mom_Index);

  // Calculate the |d0|
  double angle = genP_p4.Angle(mom_p4.Vect());
  double Lxy   = GetLxy(genP_Index, wrtPV);
  double d0Mag = TMath::Sin(angle) * Lxy;

#ifdef DEBUG
  cout << "|d0| = sin(" << angle << ") * " << Lxy << " = " << d0Mag << endl;
#endif

  return d0Mag;
*/
return 0;
}


bool MCTools::IsItsMother(const int genP_Index,
			  const int mom_Index){
/*  
  GenParticle genP = GetGenP(genP_Index);

  // For-loop: All mothers
  for (size_t i = 0; i < genP.mothers().size(); i++) {
    unsigned short mom_Index_tmp = genP.mothers().at(i);
    if (mom_Index == mom_Index_tmp) return true;
  }
*/
  return false;
}
