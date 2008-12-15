#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

MyGlobalPoint MyEventConverter::trackEcalHitPoint(const TransientTrack& transientTrack,const CaloJet* caloJet){

        GlobalPoint ecalHitPosition(0,0,0);
        double maxTowerEt = 0;
        vector<CaloTowerRef> towers = caloJet->getConstituents();
        for(vector<CaloTowerRef>::const_iterator iTower = towers.begin();
                                                 iTower != towers.end(); iTower++){
                //size_t numRecHits = (**iTower).constituentsSize();
                if((*iTower)->et() > maxTowerEt){
                        maxTowerEt = (*iTower)->et();
                        ecalHitPosition = GlobalPoint((*iTower)->momentum().x(),
                                                      (*iTower)->momentum().y(),
                                                      (*iTower)->momentum().z());
                }
        }


        MyGlobalPoint ecalHitPoint(0,0,0);

	try{
        	TrajectoryStateClosestToPoint TSCP = transientTrack.trajectoryStateClosestToPoint(ecalHitPosition);
        	GlobalPoint trackEcalHitPoint = TSCP.position();

		ecalHitPoint.x = trackEcalHitPoint.x();
	        ecalHitPoint.y = trackEcalHitPoint.y();
	        ecalHitPoint.z = trackEcalHitPoint.z() - primaryVertex.z();

        }catch(...) {;}

	return ecalHitPoint;
}

MyGlobalPoint MyEventConverter::trackEcalHitPoint(const TransientTrack& transientTrack,const ConvertedPhoton* photon){

	ConvertedPhoton* convPhoton = const_cast<ConvertedPhoton*>(photon);
	vector<math::XYZPoint> const & ecalHitPositionVector = convPhoton->ecalImpactPosition();

	for(vector<math::XYZPoint>::const_iterator i = ecalHitPositionVector.begin(); i!= ecalHitPositionVector.end(); ++i){
		cout << "ecalhitpoint eta,phi " << i->eta() << " " << i->phi() << endl;
	}

        MyGlobalPoint ecalHitPoint(0,0,0);


        return ecalHitPoint;
}
