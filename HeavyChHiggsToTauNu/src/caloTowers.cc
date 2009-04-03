#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyCaloTower> MyEventConverter::caloTowers(const CaloJet& caloJet){
	vector<MyCaloTower> calotowers;

        vector<CaloTowerPtr> towers = caloJet.getCaloConstituents();

        for(vector<CaloTowerPtr>::const_iterator iTower = towers.begin();
                                                 iTower != towers.end(); iTower++){
		vector<TVector3> ECALCells;
	        vector<TVector3> HCALCells;

                size_t numRecHits = (**iTower).constituentsSize();

                // access CaloRecHits
                for(size_t j = 0; j < numRecHits; j++) {
                        DetId recHitDetID = (**iTower).constituent(j);
                        //DetId::Detector detNum=recHitDetID.det();
                        if( recHitDetID.det() == DetId::Ecal ){
			  if((EcalSubdetector)recHitDetID.subdetId()==EcalBarrel){
//                          if( recHitDetID.subdetId() == 1 ){ // Ecal Barrel
                                EBDetId ecalID = recHitDetID;
                                EBRecHitCollection::const_iterator theRecHit = EBRecHits->find(ecalID);
                                if(theRecHit != EBRecHits->end()){
                                  DetId id = theRecHit->detid();
                                  const CaloCellGeometry* this_cell = EB->getGeometry(id);
                                  double energy = theRecHit->energy();
                                  ECALCells.push_back(getCellMomentum(this_cell,energy));
                                }
                          }
//                          if( recHitDetID.subdetId() == 2 ){ // Ecal Endcap
			  if((EcalSubdetector)recHitDetID.subdetId()==EcalEndcap){
                                EEDetId ecalID = recHitDetID;
                                EERecHitCollection::const_iterator theRecHit = EERecHits->find(ecalID);
                                if(theRecHit != EERecHits->end()){
                                  DetId id = theRecHit->detid();
                                  const CaloCellGeometry* this_cell = EE->getGeometry(id);
                                  double energy = theRecHit->energy();
                                  ECALCells.push_back(getCellMomentum(this_cell,energy));
                                }
                          }
                        }
                        if( recHitDetID.det() == DetId::Hcal ){
                          HcalDetId hcalID = recHitDetID;
                          if( recHitDetID.subdetId() == HcalBarrel ){
                            int depth = hcalID.depth();
                            if (depth==1){
                                HBHERecHitCollection::const_iterator theRecHit=HBHERecHits->find(hcalID);
                                if(theRecHit != HBHERecHits->end()){
                                  DetId id = theRecHit->detid();
                                  const CaloCellGeometry* this_cell = HB->getGeometry(id);
                                  double energy = theRecHit->energy();
                                  HCALCells.push_back(getCellMomentum(this_cell,energy));
                                }
                            }
                          }
                          if( recHitDetID.subdetId() == HcalEndcap ){
                            int depth = hcalID.depth();
                            if (depth==1){
                                HBHERecHitCollection::const_iterator theRecHit=HBHERecHits->find(hcalID);
                                if(theRecHit != HBHERecHits->end()){
                                  DetId id = theRecHit->detid();
                                  const CaloCellGeometry* this_cell = HE->getGeometry(id);
                                  double energy = theRecHit->energy();
                                  HCALCells.push_back(getCellMomentum(this_cell,energy));
                                }
                            }
                          }
                        }
                }

                MyCaloTower calotower;
                calotower.eta = (**iTower).eta();
                calotower.phi = (**iTower).phi();
                calotower.ECAL_Energy = (**iTower).emEnergy();
                calotower.HCAL_Energy = (**iTower).hadEnergy();
		calotower.ECALCells = ECALCells;
                calotower.HCALCells = HCALCells;

		calotowers.push_back(calotower);
        }

	return calotowers;
}

const TVector3 MyEventConverter::getCellMomentum(const CaloCellGeometry* cell,double& energy){
        TVector3 momentum(0,0,0);
        if(cell){
                GlobalPoint hitPosition = cell->getPosition();

                double phi   = hitPosition.phi();
                double theta = hitPosition.theta();
                if(theta > 3.14159) theta = 2*3.14159 - theta;
                double px = energy * sin(theta)*cos(phi);
                double py = energy * sin(theta)*sin(phi);
                double pz = energy * cos(theta);

                momentum = TVector3(px,py,pz);
        }
        return momentum;
}

