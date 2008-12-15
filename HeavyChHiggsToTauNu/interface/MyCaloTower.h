#ifndef MY_CALOTOWER
#define MY_CALOTOWER

using namespace std;

#include <vector>
#include "TROOT.h"
#include "TVector3.h"

class MyCaloTower : public TObject {
    public:
      	MyCaloTower();
      	virtual ~MyCaloTower();

      	double  eta,
               	phi,
                ECAL_Energy,
                HCAL_Energy;

      	vector<TVector3> ECALCells;
	inline vector<TVector3>::const_iterator ECALCells_begin() const { return ECALCells.begin();}
        inline vector<TVector3>::const_iterator ECALCells_end() const { return ECALCells.end();}

      	vector<TVector3> HCALCells;
        inline vector<TVector3>::const_iterator HCALCells_begin() const { return HCALCells.begin();}
        inline vector<TVector3>::const_iterator HCALCells_end() const { return HCALCells.end();}

	void print() const;

   	ClassDef(MyCaloTower,1)
};
#endif
