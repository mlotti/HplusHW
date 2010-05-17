#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyCaloTower.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyConvertCollection.h"

using std::endl;
using std::vector;

ClassImp(MyCaloTower)

MyCaloTower::MyCaloTower(): eta(0), phi(0), ECAL_Energy(0), HCAL_Energy(0) {}
MyCaloTower::~MyCaloTower(){}

void MyCaloTower::print(std::ostream& out) const {
	out << "        eta,phi,ECAL_Energy,HCAL_Energy " << eta << " " << phi 
             << " " << ECAL_Energy << " " << HCAL_Energy << endl;
	if(ECALCells.size() > 0){
	  out << "          ECAL cells " << endl;
	  for(vector<TVector3>::const_iterator i = ECALCells.begin(); i!= ECALCells.end(); ++i){
		out << "            Et,eta,phi " << i->Perp() << " " << i->Eta() << " " << i->Phi() << endl;
	  }
	}
	if(HCALCells.size() > 0){
          out << "          HCAL cells " << endl;
          for(vector<TVector3>::const_iterator i = HCALCells.begin(); i!= HCALCells.end(); ++i){
                out << "            Et,eta,phi " << i->Perp() << " " << i->Eta() << " " << i->Phi() << endl;
          }
	}
	out << endl;
}

std::vector<TVector3 *> MyCaloTower::getECALCells() {
  return convertCollection(ECALCells);
}
std::vector<TVector3 *> MyCaloTower::getHCALCells() {
  return convertCollection(HCALCells);
}
