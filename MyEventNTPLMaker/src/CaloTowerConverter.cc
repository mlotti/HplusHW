#include "HiggsAnalysis/MyEventNTPLMaker/interface/CaloTowerConverter.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyCaloTower.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "DataFormats/EcalDetId/interface/EcalSubdetector.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/CaloTowers/interface/CaloTower.h"
#include "DataFormats/CaloTowers/interface/CaloTowerFwd.h"

#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloCellGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"

using reco::CaloJet;
using std::vector;

template <class T>
static const T& helper(const edm::Event& iEvent, const edm::InputTag& label) {
  edm::Handle<T> handle;
  iEvent.getByLabel(label, handle);
  return *handle;
}

CaloTowerConverter::CaloTowerConverter(const edm::Event& iEvent, const edm::EventSetup& iSetup):
        EBRecHits(helper<EBRecHitCollection>(iEvent, edm::InputTag("ecalRecHit", "EcalRecHitsEB"))),
        EERecHits(helper<EERecHitCollection>(iEvent, edm::InputTag("ecalRecHit", "EcalRecHitsEE"))),
        HBHERecHits(helper<HBHERecHitCollection>(iEvent, edm::InputTag("hbhereco"))) {
        //iEvent.getByLabel( "horeco", HORecHits );
        //iEvent.getByLabel( "hfreco", HFRecHits );

        edm::ESHandle<CaloGeometry> geometry;
        iSetup.get<CaloGeometryRecord>().get(geometry);
        EB = geometry->getSubdetectorGeometry(DetId::Ecal,EcalBarrel);
        EE = geometry->getSubdetectorGeometry(DetId::Ecal,EcalEndcap);
        HB = geometry->getSubdetectorGeometry(DetId::Hcal,HcalBarrel);
        HE = geometry->getSubdetectorGeometry(DetId::Hcal,HcalEndcap);

        // FIXME: these are from eventSetup.cc, but they are not currently used?
        //HO = geometry->getSubdetectorGeometry(DetId::Hcal,HcalOuter);
        //HF = geometry->getSubdetectorGeometry(DetId::Hcal,HcalForward);
}
CaloTowerConverter::~CaloTowerConverter() {}

void CaloTowerConverter::convert(const CaloJet& caloJet, vector<MyCaloTower>& calotowers) const {
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
                                EBRecHitCollection::const_iterator theRecHit = EBRecHits.find(ecalID);
                                if(theRecHit != EBRecHits.end()){
                                  DetId id = theRecHit->detid();
                                  const CaloCellGeometry* this_cell = EB->getGeometry(id);
                                  double energy = theRecHit->energy();
                                  ECALCells.push_back(getCellMomentum(this_cell,energy));
                                }
                          }
//                          if( recHitDetID.subdetId() == 2 ){ // Ecal Endcap
			  if((EcalSubdetector)recHitDetID.subdetId()==EcalEndcap){
                                EEDetId ecalID = recHitDetID;
                                EERecHitCollection::const_iterator theRecHit = EERecHits.find(ecalID);
                                if(theRecHit != EERecHits.end()){
                                  DetId id = theRecHit->detid();
                                  const CaloCellGeometry* this_cell = EE->getGeometry(id);
                                  double energy = theRecHit->energy();
                                  ECALCells.push_back(getCellMomentum(this_cell,energy));
                                }
                          }
                        }
                        if( recHitDetID.det() == DetId::Hcal ){
                          // FIXME
                          // Is this correct? I mean, using HBHERecHits for both barrel and endcap?
                          HcalDetId hcalID = recHitDetID;
                          if( recHitDetID.subdetId() == HcalBarrel ){
                            int depth = hcalID.depth();
                            if (depth==1){
                                HBHERecHitCollection::const_iterator theRecHit=HBHERecHits.find(hcalID);
                                if(theRecHit != HBHERecHits.end()){
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
                                HBHERecHitCollection::const_iterator theRecHit=HBHERecHits.find(hcalID);
                                if(theRecHit != HBHERecHits.end()){
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
}

TVector3 CaloTowerConverter::getCellMomentum(const CaloCellGeometry *cell, double energy) const {
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

