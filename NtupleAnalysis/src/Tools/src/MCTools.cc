// User
#include "Auxiliary/interface/Table.h"
#include "Tools/interface/MCTools.h"
#include "Framework/interface/Exception.h"

// ROOT
#include "TFile.h"
#include "TH1.h"


MCTools::MCTools(Event &fEvt){
  
  fEvent = &fEvt;
  if( fEvent->isData()==true ) return; 
}

MCTools::~MCTools(){}  


bool MCTools::IsNeutrino(const int pdgId){

  // 
  // Description:
  // Returns true if genParticle is neutrino (e,mu,tau) else false.
  //

  if( ( fabs(pdgId) == 12)  || ( fabs(pdgId) == 14)  || ( fabs(pdgId) == 16) ) return true;
  else return false;
}

std::vector<int> MCTools::GetDaughters(const int my_index,
				       const int my_id,
				       bool bSkipSelf){
  
  // 
  // Description:
  // Investigate all GenParticle and look for their mother's genP_index. 
  // If that index matches the my_index AND the genMom_pdgId matched my_id
  // then the genP is considered a daughter of the particle with 
  // (index, id)=(my_index, my_id). Return all daughters in an std::vector.
  //

  int genP_index = -1;
  std::vector<int> genP_daughters;
  
  // For-loop: GenParticles
  for (auto& p: fEvent->genparticles().getGenParticles()) {
    
    genP_index++;
    int genP_pdgId   = p.pdgId();
    int genMom_index = p.mother();

    
    // Check if mother
    if (genMom_index != my_index) continue;

    if (bSkipSelf == true && my_id == genP_pdgId) continue;

    // Save daughter
    genP_daughters.push_back(genP_index);
  }

  return genP_daughters;
}



bool MCTools::RecursivelyLookForMotherId(const int genP_index,
					 int wantedMom_pdgId,
					 const bool bAbsoluteMomId){
  // 
  // Description:
  // Investigate all the mothers of the GenParticle with index "genP_index". 
  // If any of the GenParticle's mothers has an id equal to "momId" return true,
  // otherwise return false. 
  //

  if (bAbsoluteMomId) wantedMom_pdgId = std::abs(wantedMom_pdgId);
  
  // Get the mother index
  const genParticle p = fEvent->genparticles().getGenParticles()[genP_index];
  double genMom_index = p.mother();
    
  // If mother index less than 0, return false
  if (genMom_index < 0) return false;
  
  // Valid mother exists, therefore get its pdgId
  const genParticle m = fEvent->genparticles().getGenParticles()[genMom_index];
  int genMom_pdgId = m.pdgId();

  if (genMom_pdgId == wantedMom_pdgId)
    {
      return true;
    }
  if (RecursivelyLookForMotherId(genMom_index, wantedMom_pdgId, bAbsoluteMomId) )
    {
      return true;
    }
  
  return false;
}



TLorentzVector MCTools::GetVisibleP4(const unsigned int genP_index){

  // 
  // Description:
  // Return the 4-vector of all of the genParticle's daughters, except for neutrinos.
  //

  const genParticle genP     = fEvent->genparticles().getGenParticles()[genP_index];
  vector<int> genP_daughters = GetDaughters(genP_index, genP.pdgId(), true);

  TLorentzVector p4(0,0,0,0);
  if (genP_daughters.size() == 0) return p4;

  // For-loop: Daughters
  for (unsigned short i = 0; i < genP_daughters.size(); i++){

    // Get daughter
    int dau_Index = genP_daughters.at(i);
    const genParticle dau = fEvent->genparticles().getGenParticles()[dau_Index];

    // Get properties
    math::XYZTLorentzVector dau_p4;
    dau_p4        = dau.p4();
    int dau_PdgId = dau.pdgId();

     // Skip invisible daughters (neutrinos)
    if ( IsNeutrino(dau_PdgId) ) continue;

     TLorentzVector tmp;
     tmp.SetPtEtaPhiM(dau_p4.pt(), dau_p4.eta(), dau_p4.phi(), dau_p4.mass());
     p4 += tmp;

   } // For-loop: Daughters
 
  return p4;
}


int MCTools::GetLdgDaughter(const int genP_index){  // bool bOnlyChargedDaughters){

  // 
  // Description:
  // Returns index for the genParticle's leading pT daughter.
  //


  // Declarations
  const genParticle genP     = fEvent->genparticles().getGenParticles()[genP_index];
  vector<int> genP_daughters = GetDaughters(genP_index, genP.pdgId(), true);
  int ldgPtIndex = -1;
  double ldgPt   = -1.0;

  if (genP_daughters.size() == 0) return ldgPtIndex;

  // For-loop: Daughters
  for (size_t i = 0; i < genP_daughters.size(); i++){
    
    int dau_Index   = genP_daughters.at(i);
    const genParticle dau = fEvent->genparticles().getGenParticles()[dau_Index];
    int dau_PdgId   = dau.pdgId();

    // Skip invisible daughters (neutrinos)
    if ( IsNeutrino(dau_PdgId) ) continue;

    // Get pt and charge
    double dau_Pt  = dau.pt();
    // int dau_Charge = dau.charge();
    
    // if(bOnlyChargedDaughters && fabs(dau_Charge) < 1 ) continue;

    // Find leading daughter index
    if (dau_Pt > ldgPt ){
      ldgPt      = dau_Pt;
      ldgPtIndex = dau_Index;
    }
    
  }  // For-loop: Daughters

  return ldgPtIndex;
}



void MCTools::PrintDaughtersRecursively(const int genP_index){
  
  // 
  // Description:
  // Loops over all daughters of the genParticle with index genP_index
  // and print index and id of each daugthers. For each daughter the same
  // procedure is done in parallel so that the entire 'family' is printed.
  //

  // Create the table format
  Table table("# | genP_index | genP_PdgId | dau_Index | dau_PdgId", "Text"); //LaTeX  

  // Get genParticle
  const genParticle genP = fEvent->genparticles().getGenParticles()[genP_index];
  int genP_PdgId         = genP.pdgId();
  
  // Get daugthers
  vector<int> genP_daughters = GetDaughters(genP_index, genP.pdgId(), true);
  if (genP_daughters.size() == 0) return;

  // For-loop: All daughters
  for (unsigned short i = 0; i < genP_daughters.size(); i++){

    // Get daugther properties
    int dau_Index         = genP_daughters.at(i);
    const genParticle dau = fEvent->genparticles().getGenParticles()[dau_Index];
    int dau_PdgId         = dau.pdgId();

    table.AddRowColumn(i, auxTools.ToString(i, 1));
    table.AddRowColumn(i, auxTools.ToString(genP_index, 1));
    table.AddRowColumn(i, auxTools.ToString(genP_PdgId, 1));
    table.AddRowColumn(i, auxTools.ToString(dau_Index , 1));
    table.AddRowColumn(i, auxTools.ToString(dau_PdgId , 1));
    _PrintDaughtersRecursively(dau_Index, table);
  }
  
  table.Print(true);

  return;
}


void MCTools::_PrintDaughtersRecursively(const int genP_index,
					 Table &table){
  
  // 
  // Description:
  // Loops over all daughters of the genParticle with index genP_index
  // and print index and id of each daugthers. For each daughter the same
  // procedure is done in parallel so that the entire 'family' is printed.
  // Auxiliary function
  //

  // Get genParticle
  const genParticle genP = fEvent->genparticles().getGenParticles()[genP_index];
  int genP_PdgId         = genP.pdgId();
  
  // Get daugthers
  vector<int> genP_daughters = GetDaughters(genP_index, genP.pdgId(), true);
  if (genP_daughters.size() == 0) return;

  // For-loop: All daughters
  for (unsigned short i = 0; i < genP_daughters.size(); i++){

    // Get daugther properties
    int dau_Index         = genP_daughters.at(i);
    const genParticle dau = fEvent->genparticles().getGenParticles()[dau_Index];
    int dau_PdgId         = dau.pdgId();

    table.AddRowColumn(i, auxTools.ToString(i, 1));
    table.AddRowColumn(i, auxTools.ToString(genP_index, 1));
    table.AddRowColumn(i, auxTools.ToString(genP_PdgId, 1));
    table.AddRowColumn(i, auxTools.ToString(dau_Index , 1));
    table.AddRowColumn(i, auxTools.ToString(dau_PdgId , 1));
  }

  return;
}


void MCTools::PrintGenParticle(const int genP_index, bool bPrintHeaders){

  //
  // Description:
  // Print most properties of the GenParticle with index "genP_index". 
  //
  
  // GenParticle
  math::XYZTLorentzVector genP_p4;
  const genParticle genP = fEvent->genparticles().getGenParticles()[genP_index];
  genP_p4                = genP.p4();
  int genP_pdgId         = genP.pdgId();

  // Mother
  int genMom_index = genP.mother();
  int genMom_pdgId = -999999;
  if (genMom_index >= 0)
    {
      const Particle<ParticleCollection<double> > m = fEvent->genparticles().getGenParticles()[genMom_index];
      genMom_pdgId  = m.pdgId();      
    } 

  // Daugthers
  vector<int> genP_daughters = GetDaughters(genP_index, genP.pdgId(), true);

  Table table("Index | PdgId | Pt | Eta | Phi | Energy | Mass | Rapidity | Beta | Mom (Index) | Mom (PdgId) | Daus | Daus (Index)", "Text"); //LaTeX
  table.AddRowColumn(0, auxTools.ToString(genP_index   , 1));
  table.AddRowColumn(0, auxTools.ToString(genP_pdgId   , 1));
  table.AddRowColumn(0, auxTools.ToString(genP_p4.pt() , 3));
  table.AddRowColumn(0, auxTools.ToString(genP_p4.eta(), 4));
  table.AddRowColumn(0, auxTools.ToString(genP_p4.phi(), 3));
  table.AddRowColumn(0, auxTools.ToString(genP_p4.e()  , 4));
  table.AddRowColumn(0, auxTools.ToString(genP_p4.mass()  , 4));
  table.AddRowColumn(0, auxTools.ToString(genP_p4.Rapidity(), 4));
  table.AddRowColumn(0, auxTools.ToString(genP_p4.Beta(), 4));
  table.AddRowColumn(0, auxTools.ToString(genMom_index)    );
  table.AddRowColumn(0, auxTools.ToString(genMom_pdgId)    );
  table.AddRowColumn(0, auxTools.ToString(genP_daughters.size(), 1) );
  table.AddRowColumn(0, auxTools.ConvertIntVectorToString(genP_daughters) );

  table.Print(bPrintHeaders);
  return;
}


double MCTools::GetLxy(const int genP_index,
		       bool wrtPV){

  std::cout << "WARNING! The function MCTools::GetLxy() is still under construction" << std::endl;
  //
  // Description:
  // Investigate the genParticle with index "genP_index". Find its 
  // production and decay vertices. The method vertexX() returns the 
  // production vertex. So, in order to determine the decay vertex 
  // we take one of the particle's daughtes and ask for its prodution
  // vertex. 
  //
  // Explanation:
  // The distance traversed by a long-lived particle is Lxy (decay length).
  // Assuming the origin (0, 0) as the Primary Vertex (the point where the
  // particle was produced) and (vtx_X, vtx_Y) as the Secondary Vertex (the
  // point where the long-lived particle reaches before decaying), then Lxy is
  // obtained from Pythagoras theorem. Particles that decay promptly should 
  // have Lxy very close to zero.
  //
  // Note: [from https://hypernews.cern.ch/HyperNews/CMS/get/generators/2429/1.html]
  // In CMS default pythia8 configuration K_S^0 is considered long-lived
  // enough that we leave them undecayed and they are passed to geant.  So geant
  // will decay them, but you will see them as status 1 for what concerns the
  // GenParticles.
  // OTHER K_S^0).
  //

  /*
  GenParticle genP = GetGenP(genP_index);
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

  return Lxy;
  */
  return 0.0;
}


double MCTools::GetD0Mag(const int genP_index,
			 const int mom_Index,
			 bool wrtPV){

  std::cout << "WARNING! The function MCTools::GetD0Mag() is still under construction" << std::endl;
  //
  //  Description:
  //  Investigate the genParticle with index "genP_index". 
  // 
  //  Explanation: 
  //  The distance traversed by a long-lived particle is Lxy (decay length).
  //  Particles that decay promptly should have Lxy very close to zero.
  //  Simple trigonometry will reveal that the tangent of the angle between the
  //  long-lived particles' decay product and it's own direction will give:
  //  sin( |phi_mom - genP_Phi| ) = d0/Lxy
  //  Then d0 can be simply obtained by multiplying the tangent of the azimuthal
  //  angle difference with the decay length Lxy.
  // 
  //  See:
  //  https://root.cern.ch/root/html524/TMath.html#TopOfPage
  //  https://root.cern.ch/doc/master/classTLorentzVector.html
  // 

  /*
  // Ensure GenParticle with index genP_index has mother with index mom_Index
  if ( !IsItsMother(genP_index, mom_Index) ) return -1.0;

  // Ensure GenParticle with index genP_index has more than 1 daughters
  GenParticle genP = GetGenP(genP_index);
  if (genP.daughters().size() < 2) return -1.0;

  // Get 4-momenta (to calculate angle between the mother and daughter directions)
  TLorentzVector genP_p4 = GetP4(genP_index);
  TLorentzVector mom_p4  = GetP4(mom_Index);

  // Calculate the |d0|
  double angle = genP_p4.Angle(mom_p4.Vect());
  double Lxy   = GetLxy(genP_index, wrtPV);
  double d0Mag = TMath::Sin(angle) * Lxy;

  return d0Mag;
*/
  
return 0.0;
}
