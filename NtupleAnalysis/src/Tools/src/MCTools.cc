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


void MCTools::PrintGenDaughters(const genParticle &genP){
  
  // 
  // Description:
  // Loops over all daughters of the particle and prints all its daugthers. 
  // For each daughter the same procedure is done in parallel so that the entire 'family' is printed.
  //

  // Create the table format
  Table table(" | (Mothers) | Particle | -> | A | -> | B | -> | C | -> | D | -> | E | -> | F | -> | G | -> | H | -> | I", "Text");

  // Create pointer to the particle
  const genParticle *p = &genP;
  
  // Count of numbrer of rows
  int iRow = 0;

  // Add rows to the table
  std::string s_moms;
  if (p->mothers().size() > 0)  s_moms = "(" + auxTools.ConvertIntVectorToString(p->mothers()) + ")"; 
  else s_moms = "(NONE)";
  
  std::string s_daughters;
  if (p->daughters().size() > 0) s_daughters = auxTools.ConvertIntVectorToString(p->daughters());
  else s_daughters = "END";

  if (0) std::cout << "\n=== MCTools::PrintGenDaughters(): p->index() = " << p->index() << ", p->daughters().size() = " << p->daughters().size() << std::endl;
  table.AddRowColumn(iRow, auxTools.ToString(iRow) );
  table.AddRowColumn(iRow, s_moms);
  table.AddRowColumn(iRow, auxTools.ToString(p->index()));
  table.AddRowColumn(iRow, "->");
  table.AddRowColumn(iRow, s_daughters);
  
  // For-loop: All daughters
  for (size_t iDau = 0; iDau < p->daughters().size(); iDau++){
    
    // Increment index of the table row
    iRow++;    

    // Get daugther properties
    int dau_index        = p->daughters().at(iDau);
    const genParticle d = fEvent->genparticles().getGenParticles()[dau_index];
    if (0) std::cout << "=== MCTools::PrintGenDaughters(): d.index() = " << d.index() << ", d.daughters().size() = " << d.daughters().size() << std::endl;
    
    std::string s_daughters;
    if (d.daughters().size() > 0) s_daughters = auxTools.ConvertIntVectorToString(d.daughters());
    else s_daughters = "END";
    
    table.AddRowColumn(iRow, auxTools.ToString(iRow) );
    // Add 3 empty columns, thus shift the daughter cells to the right
    for (int i=1; i<= 3; i++) table.AddRowColumn(iRow, " ");
    table.AddRowColumn(iRow, auxTools.ToString(dau_index));
    table.AddRowColumn(iRow, "->");
    table.AddRowColumn(iRow, s_daughters);
    _PrintGenDaughters(d, iRow, table, 0);
  }
  
  // Print the table
  table.Print(true);
  
  return;

}


void MCTools::_PrintGenDaughters(const genParticle &p, 
				 int &iRow, 
				 Table &table,
				 int shiftLevel){
  
  // 
  // Description:
  // Auxiliary function, meant to be used with MCTools::PrintGenDaughters().
  //
  vector<short> daughters = p.daughters();  

  // For-loop: All daughters
  for (size_t iDau = 0; iDau < daughters.size(); iDau++){

    // Increment index of the table row
    iRow++;    

    int dau_index = daughters.at(iDau);
    const genParticle d = fEvent->genparticles().getGenParticles()[dau_index];
    
    std::string s_daughters;
    if (d.daughters().size() > 0) s_daughters = auxTools.ConvertIntVectorToString(d.daughters());
    else s_daughters = "END";
    
    table.AddRowColumn(iRow, auxTools.ToString(iRow));
    // Add empty columns to  shift the daughter columns to the right
    int nShift = 5+2*shiftLevel;

    // N.B.: If this is not controled well it causes segmentation fault!
    if (shiftLevel < 7) // can go up values of 5 and 6 but seg faults at some point
      {
	for (int i=1; i<= nShift; i++) table.AddRowColumn(iRow, " ");
      }
    else
      {
	std::cout << "MCTools::_PrintGenDaughters(): Reached limit in nested loop" << std::endl;
	break;
      }
    
    table.AddRowColumn(iRow, auxTools.ToString(d.index()));
    table.AddRowColumn(iRow, "->");
    table.AddRowColumn(iRow, s_daughters);
    shiftLevel++;
    _PrintGenDaughters(d, iRow, table, shiftLevel);
    shiftLevel--;
  }

  return;

}


void MCTools::PrintGenParticle(const genParticle &genP, bool bPrintHeaders){

  //
  // Description:
  // Print most properties of the GenParticle.
  //

  // Get the particle
  const genParticle *p = &genP;

  // Fill the table 
  Table table("Index | Pt | Eta | Phi | Energy |  PdgId | Status | Mass | Charge | Vertex (mm) | Rapidity | Beta | Mother(s) | Daughter(s)", "Text"); //LaTeX
  table.AddRowColumn(0, auxTools.ToString(p->index()        , 1) );
  table.AddRowColumn(0, auxTools.ToString(p->p4().pt()      , 3) );
  table.AddRowColumn(0, auxTools.ToString(p->p4().eta()     , 4) );
  table.AddRowColumn(0, auxTools.ToString(p->p4().phi()     , 3) );
  table.AddRowColumn(0, auxTools.ToString(p->p4().e()       , 4) );
  table.AddRowColumn(0, auxTools.ToString(p->pdgId()        , 1) );
  table.AddRowColumn(0, auxTools.ToString(p->status()       , 1) );
  table.AddRowColumn(0, auxTools.ToString(p->p4().mass()    , 4) );
  table.AddRowColumn(0, auxTools.ToString(p->charge()       , 1) );
  table.AddRowColumn(0, "(" + auxTools.ToString(p->vtxX()*10, 3) + ", " + auxTools.ToString(p->vtxY()*10, 3)  + ", " + auxTools.ToString(p->vtxZ()*10, 3) + ")" );
  table.AddRowColumn(0, auxTools.ToString(p->p4().Rapidity(), 4) );
  table.AddRowColumn(0, auxTools.ToString(p->p4().Beta()    , 4) );
  table.AddRowColumn(0, auxTools.ConvertIntVectorToString(p->mothers()  ) );
  table.AddRowColumn(0, auxTools.ConvertIntVectorToString(p->daughters()) );

  table.Print(bPrintHeaders);
  return;
}


double MCTools::GetLxy(const genParticle &genP,
		       const genParticle &mother,
		       const genParticle &daughter,
		       ROOT::Math::XYZPoint vtx){

  //
  // Description:
  // Find the particle production vertexand decay vertex. The variale pv
  // is the Primary Vertex of the hard interaction (in mm). So, in order to determine
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

  // Get the particles
  const genParticle *p = &genP;
  const genParticle *d = &daughter;

  // Ensure the particle has a mother!
  // if( (p->index() == 0) || (p->index() == 1) ) return -1.0;
  if (p->mothers().size() < 1) return 0.0;

  // Ensure the particle has more than 1 daughters
  if (p->daughters().size() < 1) return -2.0;
  
  // Calculate the distance Lxy (in mm) wrt to the point "vtx"
  double LxySq = pow( (d->vtxX() - vtx.x()), 2) + pow( (d->vtxY() - vtx.y()), 2);
  double Lxy   = sqrt(LxySq)*10; // factor of 10 needed convert from cm to mm

  if (0) std::cout << "\n=== MCTools::GetLxy(): Lxy = " << Lxy << " (mm) wrt point (" << vtx.x() << ", " << vtx.y() << ", " << vtx.z() << "). Particle with index " << p->index() << " was produced at (" << p->vtxX() << ", " << p->vtxY() << ", " << p->vtxZ() << ") and decayed at (" << d->vtxX() << ", " << d->vtxY() << ", " << d->vtxZ() << ")." << std::endl;

  return Lxy;
}


double MCTools::GetD0(const genParticle &genP,
		      const genParticle &mother,
		      const genParticle &daughter,
		      ROOT::Math::XYZPoint vtx){
  
  //
  //  Description:
  //  Returns the particle's |d0| in mm.
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

  // Get the particles
  const genParticle *p = &genP;
  const genParticle *m = &mother;
 
  // Ensure the particle has a mother!
  if (p->mothers().size() < 1) return 0.0;

  // If the mother is the incoming proton return 0
  if( (m->index() == 0) || (m->index() == 1) ) return -1.0;

  // Ensure the particle has more than 1 daughters
  if (p->daughters().size() < 1) return -2.0;

  // Get the TLorentzVectors
  TLorentzVector p_p4;
  p_p4.SetPtEtaPhiM(p->p4().pt(), p->p4().eta(), p->p4().phi(), p->p4().mass() );

  TLorentzVector m_p4;
  m_p4.SetPtEtaPhiM(m->p4().pt(), m->p4().eta(), m->p4().phi(), m->p4().mass() );

  // In case mother has zero pt ( angle = nan)
  if (m_p4.Pt() == 0) return -3.0;


  // Calculate the Angle between two vectors (in radians)
  double angle = p_p4.Angle( m_p4.Vect() );
  
  // Get the Lxy (in mm)
  double Lxy = GetLxy(genP, mother, daughter, vtx); 

  // Calculate the |d0| (in mm). [The TMath::Sin() requires angle in radians]
  double d0Mag = TMath::Sin(angle) * Lxy;
  
  if (0) std::cout << "=== MCTools::GetD0(): |d0| = Sin("<<angle<<") * " << Lxy << " = " << d0Mag  << ", wrt point (" << vtx.x() << ", " << vtx.y() << ", " << vtx.z() << "). Particle with index " << p->index() << " has mother with index " << m->index() << "." << std::endl;

  return d0Mag;
}



bool MCTools::HasMother(const genParticle &p,
			const int mom_pdgId){
  
  //
  //  Description:
  //  Returns true if the particle has a mother with pdgId equal to mom_pdgId.
  // 

  // PrintGenParticle(p);

  // Ensure the particle has a mother!
  if (p.mothers().size() < 1) return false;

  // For-loop: All mothers
  for (size_t iMom = 0; iMom < p.mothers().size(); iMom++)
    {

      int mom_index =  p.mothers().at(iMom);
      const genParticle m = fEvent->genparticles().getGenParticles()[mom_index];
      if (m.pdgId() == mom_pdgId) return true;
      else continue;

    }

  return false;
}
