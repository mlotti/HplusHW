#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

MyGlobalPoint MyEventConverter::trackEcalHitPoint(const Track& track, const CaloJet *caloJet) {
        // New method
        math::XYZPoint hitPos = trackAssociator_.trackPositionAtEcal(track);
        const TransientTrack transientTrack = transientTrackBuilder->build(track);


        // Old method
        GlobalPoint ecalHitPosition(0,0,0);
        double maxTowerEt = 0;
        vector<CaloTowerPtr> towers = caloJet->getCaloConstituents();
        for(vector<CaloTowerPtr>::const_iterator iTower = towers.begin();
                                                 iTower != towers.end(); iTower++){
                //size_t numRecHits = (**iTower).constituentsSize();
                if((*iTower)->et() > maxTowerEt){
                        maxTowerEt = (*iTower)->et();
                        /*
                        ecalHitPosition = GlobalPoint((*iTower)->momentum().x(),
                                                      (*iTower)->momentum().y(),
                                                      (*iTower)->momentum().z());
                        */
                        ecalHitPosition = (*iTower)->emPosition();
                }
        }


        MyGlobalPoint ecalHitPoint(0,0,0);
        MyGlobalPoint ecalHitPoint2(0,0,0);

	try{
        	GlobalPoint trackEcalHitPoint = transientTrack.trajectoryStateClosestToPoint(ecalHitPosition).position();
                GlobalPoint trackEcalHitPoint2 = transientTrack.stateOnSurface(ecalHitPosition).globalPosition();
 
		ecalHitPoint.SetX(trackEcalHitPoint.x());
	        ecalHitPoint.SetY(trackEcalHitPoint.y());
                ecalHitPoint.SetZ(trackEcalHitPoint.z());

		ecalHitPoint2.SetX(trackEcalHitPoint2.x());
	        ecalHitPoint2.SetY(trackEcalHitPoint2.y());
                ecalHitPoint2.SetZ(trackEcalHitPoint2.z());

        }catch(...) {;}

        // Comparison
        std::cout << "    Track ecal hit point: TrackAssociator (" << hitPos.x() << "," << hitPos.y() << "," << hitPos.z()
                  << ") TSOS (" << ecalHitPoint2.X() << "," << ecalHitPoint2.Y() << "," << ecalHitPoint.Z()
                  << ") TCSP (" << ecalHitPoint.X() << "," << ecalHitPoint.Y() << "," << ecalHitPoint.Z()
                  << std::endl;

        // Return new method
        return MyGlobalPoint(hitPos.x(), hitPos.y(), hitPos.z());

}

MyGlobalPoint MyEventConverter::trackEcalHitPoint(const GsfElectron* electron){
	math::XYZPoint pos = electron->trackPositionAtCalo();
        return MyGlobalPoint(pos.x(), pos.y(), pos.z());
}

MyGlobalPoint MyEventConverter::trackEcalHitPoint(const pat::Electron* electron){
	math::XYZPoint pos = electron->trackPositionAtCalo();
        return MyGlobalPoint(pos.x(), pos.y(), pos.z());
}

MyGlobalPoint MyEventConverter::trackEcalHitPoint(const TransientTrack& transientTrack,const Conversion* photon){
/*
	Conversion* convPhoton = const_cast<Conversion*>(photon);
	vector<math::XYZPoint> const & ecalHitPositionVector = convPhoton->ecalImpactPosition();

	for(vector<math::XYZPoint>::const_iterator i = ecalHitPositionVector.begin(); i!= ecalHitPositionVector.end(); ++i){
		cout << "ecalhitpoint eta,phi " << i->eta() << " " << i->phi() << endl;
	}
*/
        MyGlobalPoint ecalHitPoint(0,0,0);
        return ecalHitPoint;
}

MyGlobalPoint MyEventConverter::trackEcalHitPoint(const PFCandidate* pfCand){

        math::XYZPointF pos = pfCand->positionAtECALEntrance();

        MyGlobalPoint ecalHitPoint(0,0,0);
        ecalHitPoint.SetX(pos.x());
        ecalHitPoint.SetY(pos.y());
        ecalHitPoint.SetZ(pos.z());

        return ecalHitPoint;
}
