#ifndef __MyCaloTower__
#define __MyCaloTower__

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventVersion.h"
#include "TVector3.h"

#include<vector>
#include<iostream>

/**
 * \brief Calorimeter tower class for MyEvent dataformat
 */
class MyCaloTower {
    public:
      	MyCaloTower();
      	virtual ~MyCaloTower();

	void print(std::ostream& out = std::cout) const;

        std::vector<TVector3 *> getECALCells();
        std::vector<TVector3 *> getHCALCells();

        std::vector<TVector3> ECALCells; ///< ECAL cells
        std::vector<TVector3> HCALCells; ///< HCAL cells

        double eta;         ///< Eta of the tower
        double phi;         ///< Phi of the tower
        double ECAL_Energy; ///< Total ECAL energy
        double HCAL_Energy; ///< Total HCAL energy

    private:
   	ClassDef(MyCaloTower, MYEVENT_VERSION)
};
#endif
