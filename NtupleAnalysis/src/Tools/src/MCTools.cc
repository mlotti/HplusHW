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


double MCTools::DeltaPhi(const double phi1, 
			 const double phi2){
  //	
  // See: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_4_4_2/doc/html/d1/d92/DataFormats_2Math_2interface_2deltaPhi_8h_source.html
  //
  Double_t result = phi1 - phi2;
  while (result > PI) result -= 2*PI;
  while (result <= -PI) result += 2*PI; 

  return result;
}


double MCTools::DeltaAbs(const double val1, 
			 const double val2){
  //
  // See: https://cmssdt.cern.ch/SDT/doxygen/CMSSW_4_4_2/doc/html/d1/d92/DataFormats_2Math_2interface_2deltaPhi_8h_source.html
  //
  Double_t deltaAbs = fabs ( val1 - val2 );
  return deltaAbs;
}


double MCTools::GetRapidity(const math::XYZTLorentzVector p4){
  // 
  // Description:
  // Returns rapidity of the particle with 4-momentum p4.
  //
  double rapidity = 0.5*log( (p4.e() + p4.pz()) / (p4.e() - p4.pz()) );
  return rapidity;
}



bool MCTools::IsNeutrino(const int pdgId){

  // 
  // Description:
  // Returns true if genParticle is neutrino (v_e, v_mu, v_tau), else false.
  //

  if( (abs(pdgId) == 12) || (abs(pdgId) == 14) || (abs(pdgId) == 16) ) return true;
  else return false;
}


bool MCTools::IsLepton(const int pdgId){

  // 
  // Description:
  // Returns true if genParticle is a lepton (e, mu, tau & associated neutrinos), else false.
  //

  if( (abs(pdgId) == 11) || (abs(pdgId) == 12)  ||
      (abs(pdgId) == 13) || (abs(pdgId) == 14)  ||
      (abs(pdgId) == 15) || (abs(pdgId) == 16) ) return true;
  else return false;
}


bool MCTools::IsChargedLepton(const int pdgId){

  // 
  // Description:
  // Returns true if genParticle is a charged lepton (e, mu, tau), else false.
  //

  if( (abs(pdgId) == 11) || (abs(pdgId) == 13) || (abs(pdgId) == 15) ) return true;
  else return false;
}


bool MCTools::IsQuark(const int pdgId){

  // 
  // Description:
  // Returns true if genParticle is a quark (u, d, c, s, t, b), else false.
  //

  if( (abs(pdgId) == 1) || (abs(pdgId) == 2)  ||
      (abs(pdgId) == 3) || (abs(pdgId) == 4)  ||
      (abs(pdgId) == 5) || (abs(pdgId) == 6) ) return true;
  else return false;
}


bool MCTools::HasDaughter(const int genP_index,
			  const int my_pdgId,
			  bool bAllDaughters,
			  bool bApplyAbs){
  // 
  // Description:
  // Get all daughters for genParticle with index genP_index.
  // Search inside the daughters vector (pdgId, not index)
  // and look for a specific particle with pdgId. The boolean
  // controls whether you care or not about the particle's charge
  //

  // Declarations
  std::vector<int> daughters;
  std::vector<int> daughters_abs;

  // Get the daughters
  if (bAllDaughters) daughters = GetAllDaughters(genP_index, false);
  else daughters = GetDaughters(genP_index, false);

  // For-loop: Daughters
  for (size_t i = 0; i < daughters.size(); i++)
    {
      int dau_index         = daughters.at(i);
      const genParticle dau = fEvent->genparticles().getGenParticles()[dau_index];
      int pdgId_abs         = std::abs(dau.pdgId());
      daughters_abs.push_back(pdgId_abs);
    }
  
  if (bApplyAbs) daughters = daughters_abs;
  if ( std::find(daughters.begin(), daughters.end(), std::abs(my_pdgId) ) == daughters.end() ) return false;
  else return true;
}
 

int MCTools::GetFinalSelf(const int genP_index){
  std::cout << "*** MCTools::GetFinalSelf(): WARNING! Since CMSSW_8X this is obsolete. Doing nothing" << std::endl;
  return -1;

  int new_index = genP_index;
  genParticle p = fEvent->genparticles().getGenParticles()[genP_index];
  vector<int> daughters = GetAllDaughters(genP_index, false);
  if (daughters.size() < 1) return new_index;
  
  // For-loop: All daughters
  for (unsigned short i = 0; i < daughters.size(); i++){

    int dau_index = daughters.at(i);
    genParticle d = fEvent->genparticles().getGenParticles()[dau_index];
    if ( d.pdgId() == p.pdgId() ) new_index = dau_index;
  }

  return new_index;
}


std::vector<int> MCTools::GetDaughters(const int my_index,
				       bool bReturnIds){
  
  // 
  // Description:
  // Investigate all GenParticle and look for their mother's genP_index. 
  // If that index matches the my_index then the genP is considered a
  // daughter of the particle with (index, id)=(my_index, my_id).
  // Returns all daughters in an std::vector.
  //
  std::cout << "*** MCTools::GetDaughters(): WARNING! Since CMSSW_8X this is obsolete. Doing nothing" << std::endl;

  std::vector<int> genP_daughters;
  
  /*
  int genP_index = -1;
  // For-loop: GenParticles
  for (auto& p: fEvent->genparticles().getGenParticles()) {
    
    genP_index++;
    int genP_pdgId   = p.pdgId();
    int genMom_index = p.mother();
    
    // Check if mother
    if (genMom_index != my_index) continue;

    // Save daughters
    if (bReturnIds) genP_daughters.push_back(genP_pdgId);
    else genP_daughters.push_back(genP_index);
  }
  */

  return genP_daughters;
}


bool MCTools::HasMother(std::vector<short> genP_mothers,
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
  if (genP_mothers.size() < 1) return false;
  
  // Look for mothers
  int genMom_pdgId = 0;
  for (size_t i = 0; i < genP_mothers.size(); i++)
    {
      
      
      const genParticle m = fEvent->genparticles().getGenParticles()[genP_mothers.at(i)];
      if (bAbsoluteMomId) genMom_pdgId = std::abs(m.pdgId());
      else genMom_pdgId = m.pdgId();
      
      if (genMom_pdgId == wantedMom_pdgId)
	{
	  return true;
	}
    }
  
  return false;
}



TLorentzVector MCTools::GetVisibleP4(const int genP_index){

  // 
  // Description:
  // Return the 4-vector of all of the genParticle's daughters, except for neutrinos.
  //

  const genParticle genP     = fEvent->genparticles().getGenParticles()[genP_index];
  vector<int> genP_daughters = GetDaughters(genP_index, true);

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
  vector<int> genP_daughters = GetDaughters(genP_index, true);
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



void MCTools::PrintDaughters(const int genP_index, bool bPrintIds){
  
  // 
  // Description:
  // Loops over all daughters of the genParticle with index genP_index
  // and prints all its daugthers. For each daughter the same
  // procedure is done in parallel so that the entire 'family' is printed.
  //

  // Create the table format
  Table table(" (Mom) | A | -> | B | -> | C | -> | D | -> | E | -> | F | -> | G | -> | H | -> | I  | -> | J  | -> | K | -> | L | -> | M | -> | N", "Text");

  // Get genParticles of interest
  const genParticle genP  = fEvent->genparticles().getGenParticles()[genP_index];
  std::cout << "*** WARNING! Since CMSSW_8X this is obsolete. Doing nothing" << std::endl;
  return;

  /*
  int genMom_index        =  genP.mother();
  int genMom_pdgId        = 0;
  if (genMom_index >= 0)
    {
      const genParticle genMom = fEvent->genparticles().getGenParticles()[genMom_index];
      genMom_pdgId = genMom.pdgId();
    }
  vector<int> genP_daughters   = GetDaughters(genP_index, false);
  vector<int> genP_daughtersId = GetDaughters(genP_index, true);

  // Row number and Column Level 
  int cLevel = 0;  
  int row    = 0;

  // Add row to table
  if (bPrintIds)
    {
      table.AddRowColumn(row, "(" + auxTools.ToString(genMom_pdgId) + ")" );
      table.AddRowColumn(row, auxTools.ToString(genP.pdgId()));
      table.AddRowColumn(row, "->");
      table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genP_daughtersId));
    }
  else
    {
      table.AddRowColumn(row, "(" + auxTools.ToString(genMom_index) + ")" );
      table.AddRowColumn(row, auxTools.ToString(genP_index));
      table.AddRowColumn(row, "->");
      table.AddRowColumn(row, auxTools.ConvertIntVectorToString(genP_daughters));      
    }

  // Increment the level
  cLevel++;
  int cLevel_ = cLevel;

  
  // For-loop: All daughters
  for (size_t iDau = 0; iDau < genP_daughters.size(); iDau++){

    // Increment row number
    row++;
    
    // Get daugther properties
    int dau_index               = genP_daughters.at(iDau);
    const genParticle dau       = fEvent->genparticles().getGenParticles()[dau_index];
    vector<int> dau_daughters   = GetDaughters(dau_index, false);
    vector<int> dau_daughtersId = GetDaughters(dau_index, true);
    
    // Add row to table
    for (int j = 0; j < 2*cLevel; j++) table.AddRowColumn(row, "");

    if (bPrintIds)
      {
	table.AddRowColumn(row, "");
	table.AddRowColumn(row, auxTools.ToString(dau.pdgId()));
	table.AddRowColumn(row, "->");
	table.AddRowColumn(row, auxTools.ConvertIntVectorToString(dau_daughtersId));
      }
    else
      {
	table.AddRowColumn(row, "");
	table.AddRowColumn(row, auxTools.ToString(dau_index));
	table.AddRowColumn(row, "->");
	table.AddRowColumn(row, auxTools.ConvertIntVectorToString(dau_daughters));
      }

    // Print this daughter's daughters
    _PrintDaughters(dau_index, cLevel, row, table, bPrintIds);
    cLevel = cLevel_;
  }
  std::cout << "\n" << std::endl;
  table.Print(true);

  return;
*/
}


vector<int> MCTools::GetAllDaughters(const int genP_index, bool bGetIds){
  
  // 
  // Description:
  // Loops over all daughters of the genParticle with index genP_index
  // and saves all its daugthers. For each daughter the same
  // procedure is done in parallel so that the entire 'family' is acquired
  // and returned as a vector<int>.
  //

  vector<int> genP_allDaughters;
  
  // Get genParticles of interest
  const genParticle genP       = fEvent->genparticles().getGenParticles()[genP_index];
  vector<int> genP_daughters   = GetDaughters(genP_index, false);
  vector<int> genP_daughtersId = GetDaughters(genP_index, true);
  vector<int> genP_daus        = GetDaughters(genP_index, true);

  if (bGetIds)
    {
      genP_daus = genP_daughtersId;
    }
  else
    {
      genP_daus = genP_daughters;
    }

  // Get daughters
  genP_allDaughters.insert(genP_allDaughters.end(), genP_daus.begin(), genP_daus.end());
  
  // For each daugher, get its daughters
  for (size_t iDau = 0; iDau < genP_daughters.size(); iDau++){

    int dau_index = genP_daughters.at(iDau);
    _GetAllDaughters(dau_index, genP_allDaughters, bGetIds);
  }

  return genP_allDaughters;
}


void MCTools::_GetAllDaughters(const int genP_index, vector<int> &genP_allDaughters, bool bGetIds){
  
  // 
  // Description:
  // Auxiliary function to vector<int> MCTools::GetAllDaughters()
  //
  
  // Get genParticles of interest
  const genParticle genP       = fEvent->genparticles().getGenParticles()[genP_index];
  vector<int> genP_daughters   = GetDaughters(genP_index, false);
  vector<int> genP_daughtersId = GetDaughters(genP_index, true);
  vector<int> genP_daus;

  if (bGetIds)
    {
      genP_daus = genP_daughtersId;
    }
  else
    {
      genP_daus = genP_daughters;
    }
  // Get daughters
  genP_allDaughters.insert(genP_allDaughters.end(), genP_daus.begin(), genP_daus.end());
  
  // For each daugher, get its daughter
  for (size_t iDau = 0; iDau < genP_daughters.size(); iDau++){
    
    // Get daugther properties
    int dau_index               = genP_daughters.at(iDau);
    const genParticle dau       = fEvent->genparticles().getGenParticles()[dau_index];
    vector<int> dau_daughters   = GetDaughters(dau_index, false);
    vector<int> dau_daughtersId = GetDaughters(dau_index, true);
    vector<int> dau_daus;

    if (bGetIds)
      {
	dau_daus = dau_daughtersId;
      }
    else
      {
	dau_daus = dau_daughters;
      }

    // Append to the daughters vector
    // genP_allDaughters.insert(genP_allDaughters.end(), dau_daus.begin(), dau_daus.end()); //duplicates
    _GetAllDaughters(dau_index, genP_allDaughters, bGetIds);
  }

  return;
}



void MCTools::_PrintDaughters(const int genP_index,
			      int &cLevel,
			      int &row,
			      Table &table,
			      bool bPrintIds){
  
  // 
  // Description:
  // Auxiliary function to void MCTools::PrintDaughters().
  //

  // Increment level
  cLevel++;
  int cLevel_ = cLevel;
  
  // Get genParticles of interest
  const genParticle genP     = fEvent->genparticles().getGenParticles()[genP_index];
  vector<int> genP_daughters = GetDaughters(genP_index, false);
  
  // For-loop: All daughters
  for (size_t iDau = 0; iDau < genP_daughters.size(); iDau++){

    // Increment row number
    row++;

    // Get daugther properties
    int dau_index               = genP_daughters.at(iDau);
    const genParticle dau       = fEvent->genparticles().getGenParticles()[dau_index];
    vector<int> dau_daughters   = GetDaughters(dau_index, false);
    vector<int> dau_daughtersId = GetDaughters(dau_index, true);
    
    // Add row to table
    for (int j = 0; j < 2*cLevel; j++) table.AddRowColumn(row, "");

    if (bPrintIds)
      {
	table.AddRowColumn(row, "");
	table.AddRowColumn(row, auxTools.ToString(dau.pdgId()));
	table.AddRowColumn(row, "->");
	table.AddRowColumn(row, auxTools.ConvertIntVectorToString(dau_daughtersId));
      }
    else
      {
	table.AddRowColumn(row, "");
	table.AddRowColumn(row, auxTools.ToString(dau_index));
	table.AddRowColumn(row, "->");
	table.AddRowColumn(row, auxTools.ConvertIntVectorToString(dau_daughters));
      }
        
    // Print this daughter's daughters
    _PrintDaughters(dau_index, cLevel, row, table, bPrintIds);
    cLevel = cLevel_;
  }

  return;
}


void MCTools::PrintGenParticle(const int genP_index, bool bPrintHeaders){

  //
  // Description:
  // Print most properties of the GenParticle with index "genP_index". 
  //
  std::cout << "*** MCTools::PrintGenParticle(): WARNING! Since CMSSW_8X this is obsolete. Doing nothing" << std::endl;
  return;

  // GenParticle
  math::XYZTLorentzVector genP_p4;
  const genParticle genP = fEvent->genparticles().getGenParticles()[genP_index];
  genP_p4                = genP.p4();
  int genP_pdgId         = genP.pdgId();
  int genP_status        = genP.status();

  // Mother
  int genMom_index = genP.mothers().at(0);
  int genMom_pdgId = -999999;
  if (genMom_index >= 0)
    {
      const genParticle m = fEvent->genparticles().getGenParticles()[genMom_index];
      genMom_pdgId  = m.pdgId();      
    } 

  // Daugthers
  vector<int> genP_daughters = GetDaughters(genP_index, false);

  Table table("Index | PdgId | Status | Pt | Eta | Phi | Energy | Mass | Rapidity | Beta | Mom (Index) | Mom (PdgId) | Daus | Daus (Index)", "Text"); //LaTeX
  table.AddRowColumn(0, auxTools.ToString(genP_index   , 1));
  table.AddRowColumn(0, auxTools.ToString(genP_pdgId   , 1));
  table.AddRowColumn(0, auxTools.ToString(genP_status  , 1));
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

  //
  // Description:
  // Investigate the genParticle with index "genP_index". Find its 
  // production and decay vertices. The method GetPV() returns the 
  // Primary Vertex of the hard interaction. So, in order to determine
  // the decay vertex we take one of the particle's daughtes and
  // ask for its prodution vertex.  Return Lxy in mm.
  //
  // Explanation:
  // The distance traversed by a long-lived particle is Lxy (decay length).
  // Assuming the origin (0, 0) as the Primary Vertex (the point where the
  // particle was produced) and (vtxX, vtxY) as the Secondary Vertex (the
  // point where the long-lived particle reaches before decaying), then Lxy is
  // obtained from Pythagoras theorem. Particles that decay promptly should 
  // have Lxy very close to zero.
  //
  // Note: [from https://hypernews.cern.ch/HyperNews/CMS/get/generators/2429/1.html]
  // In CMS default pythia8 configuration K_S^0 is considered long-lived
  // enough that we leave them undecayed and they are passed to GEANT.  So GEANT
  // will decay them, but you will see them as status 1 for what concerns the
  // genParticles.
  //

  // Get the genParticle
  genParticle p = fEvent->genparticles().getGenParticles()[genP_index];

  // If proton return 0
  genParticle m;
  int mom_index = p.mothers().at(0);
  if( (p.pdgId() == 2212) && (mom_index < 0)) return 0.0;

  // Get the daughters
  std::vector<int>  daughters = GetDaughters(genP_index, false);
  if (daughters.size() == 0) return 0.0;

  // Get one of the daugthers to determine the decay vertex
  int dau_index = daughters.at(0);
  genParticle d = fEvent->genparticles().getGenParticles()[dau_index];

  // Get the daughter production vertex
  ROOT::Math::XYZPoint dau_xyz(d.vtxX()*10, d.vtxY()*10, d.vtxZ()*10); // [in mm]

  // Get the reference point: (pvX, pvY) or (0,0)?
  ROOT::Math::XYZPoint xyz;
  ROOT::Math::XYZPoint vtx = GetVertex(); // in mm 
  ROOT::Math::XYZPoint pv  = GetPV();     // in mm
  if (wrtPV) xyz = pv;
  else xyz = vtx;
  
  // Calculate the distance Lxy (in mm)
  double LxySq = pow( (dau_xyz.x() - xyz.x()), 2) + pow( (dau_xyz.y() - xyz.y()), 2);
  double Lxy   = sqrt(LxySq);

  return Lxy;
}


double MCTools::GetD0Mag(const int genP_index,
			 bool wrtPV){

  //
  //  Description:
  //  Investigate the genParticle with index "genP_index". Return
  //  |d0| in mm.
  // 
  //  Explanation: 
  //  The distance traversed by a long-lived particle is Lxy (decay length).
  //  Particles that decay promptly should have Lxy very close to zero.
  //  Simple trigonometry will reveal that the tangent of the angle between the
  //  long-lived particles' decay product and it's own direction will give:
  //  sin( |genP_phi - mom_phi| ) = d0/Lxy
  //  Then d0 can be simply obtained by multiplying the tangent of the azimuthal
  //  angle difference with the decay length Lxy.
  // 
  //  See:
  //  https://root.cern.ch/root/html524/TMath.html#TopOfPage
  //  https://root.cern.ch/doc/master/classTLorentzVector.html
  // 

  // Get the particle
  genParticle p = fEvent->genparticles().getGenParticles()[genP_index];
  
  // Particle MUST have a mother!
  genParticle m;
  int mom_index = p.mothers().at(0);
  if (mom_index >= 0) m = fEvent->genparticles().getGenParticles()[mom_index];
  else return 0.0; //-99999.0;
    
  // Ensure the particle has more than 1 daughters
  std::vector<int> daughters = GetDaughters(genP_index, false);
  if (daughters.size() < 2) return 0.0; //-99999.0;

  // Get the TLorentzVectors
  TLorentzVector p_p4;
  p_p4.SetPtEtaPhiM(p.p4().pt(), p.p4().eta(), p.p4().phi(), p.p4().mass() );


  TLorentzVector m_p4;
  m_p4.SetPtEtaPhiM(m.p4().pt(), m.p4().eta(), m.p4().phi(), m.p4().mass() );
  // Sanity check
  if ( (m.p4().pt() == 0) && (m.p4().phi() == 0) ) return 0.0; //-99999.0;

	 
  // Calculate the Aagle between two vectors (in radians)
  double angle = p_p4.Angle( m_p4.Vect() );
  
  // Get the Lxy (in mm)
  double Lxy = GetLxy(genP_index, wrtPV); 

  // Calculate the |d0| (in mm). [The TMath::Sin() requires angle in radians]
  double d0Mag = TMath::Sin(angle) * Lxy;
  // std::cout << "d0Mag = TMath::Sin("<<angle<<") * " << Lxy << "= " << d0Mag  << std::endl;

  return d0Mag;
}


ROOT::Math::XYZPoint MCTools::GetPV(void){

  //
  //  Description:
  //  Return the offline Primary Vertex (PV) as a XYZPoint (by default in mm).
  // 

  ROOT::Math::XYZPoint pv(fEvent->vertexInfo().pvX(), fEvent->vertexInfo().pvY(), fEvent->vertexInfo().pvZ() );
  
  return pv;
}


ROOT::Math::XYZPoint MCTools::GetVertex(void){

  //
  //  Description:
  //  Return the genParticle vertex as a XYZPoint (in mm).
  //  This is defined as the vertex of the proton (first) daughters.
  // 

  // Declarations
  ROOT::Math::XYZPoint vtx(0.0, 0.0, 0.0);
  
  // For-loop: All genParticles 
  int genP_index = -1;
  for (auto& p: fEvent->genparticles().getGenParticles())
    {
      genP_index++;

      // Skip the protons (have no vertex)
      if (p.pdgId() == 2212) continue;

      // Get the daughters
      std::vector<int> genP_daughters = GetDaughters(genP_index, false);

      // Get the mother
      int genMom_index = p.mothers().at(0);
      genParticle m    = fEvent->genparticles().getGenParticles()[genMom_index];
      if (m.pdgId() == 2212)
	{
	  vtx.SetXYZ(p.vtxX()*10, p.vtxY()*10, p.vtxZ()*10);
	  break;
	}
    }
  
  return vtx;
}
