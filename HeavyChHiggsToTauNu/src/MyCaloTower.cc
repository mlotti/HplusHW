#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyCaloTower.h"

#include <iostream>

using namespace std;

ClassImp(MyCaloTower)

MyCaloTower::MyCaloTower(){;}
MyCaloTower::~MyCaloTower(){;}

void MyCaloTower::print() const {
	cout << "        eta,phi,ECAL_Energy,HCAL_Energy " << eta << " " << phi 
             << " " << ECAL_Energy << " " << HCAL_Energy << endl;
	if(ECALCells.size() > 0){
	  cout << "          ECAL cells " << endl;
	  for(vector<TVector3>::const_iterator i = ECALCells_begin(); i!= ECALCells_end(); ++i){
		cout << "            Et,eta,phi " << i->Perp() << " " << i->Eta() << " " << i->Phi() << endl;
	  }
	}
	if(HCALCells.size() > 0){
          cout << "          HCAL cells " << endl;
          for(vector<TVector3>::const_iterator i = HCALCells_begin(); i!= HCALCells_end(); ++i){
                cout << "            Et,eta,phi " << i->Perp() << " " << i->Eta() << " " << i->Phi() << endl;
          }
	}
	cout << endl;
}
