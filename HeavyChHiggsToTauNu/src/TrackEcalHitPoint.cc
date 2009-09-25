#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackEcalHitPoint.h"

#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"

#include<vector>

using std::vector;

using reco::TransientTrack;
using reco::CaloJet;
using reco::GsfElectron;
using reco::Conversion;
using reco::PFCandidate;

MyGlobalPoint TrackEcalHitPoint::convert(const TransientTrack& transientTrack,const CaloJet* caloJet){

        GlobalPoint ecalHitPosition(0,0,0);
        double maxTowerEt = 0;
        vector<CaloTowerPtr> towers = caloJet->getCaloConstituents();
        for(vector<CaloTowerPtr>::const_iterator iTower = towers.begin();
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

		ecalHitPoint.SetX(trackEcalHitPoint.x());
	        ecalHitPoint.SetY(trackEcalHitPoint.y());
	        ecalHitPoint.SetZ(trackEcalHitPoint.z());

        }catch(...) {;}

	return ecalHitPoint;
}

MyGlobalPoint TrackEcalHitPoint::convert(const TransientTrack& transientTrack,const GsfElectron* electron){

        GlobalPoint ecalHitPosition(0,0,0);
	math::XYZVector pos = electron->trackMomentumAtCalo();

	MyGlobalPoint ecalHitPoint(0,0,0);
	ecalHitPoint.SetX(pos.x());
	ecalHitPoint.SetY(pos.y());
	ecalHitPoint.SetZ(pos.z());

        return ecalHitPoint;
}

MyGlobalPoint TrackEcalHitPoint::convert(const TransientTrack& transientTrack,const pat::Electron* electron){

        GlobalPoint ecalHitPosition(0,0,0);
        math::XYZVector pos = electron->trackMomentumAtCalo();

	MyGlobalPoint ecalHitPoint(0,0,0);
        ecalHitPoint.SetX(pos.x());
        ecalHitPoint.SetY(pos.y());
        ecalHitPoint.SetZ(pos.z());

        return ecalHitPoint;
}

MyGlobalPoint TrackEcalHitPoint::convert(const TransientTrack& transientTrack,const Conversion* photon){
/* FIXME
	Conversion* convPhoton = const_cast<Conversion*>(photon);
	vector<math::XYZPoint> const & ecalHitPositionVector = convPhoton->ecalImpactPosition();

	for(vector<math::XYZPoint>::const_iterator i = ecalHitPositionVector.begin(); i!= ecalHitPositionVector.end(); ++i){
		cout << "ecalhitpoint eta,phi " << i->eta() << " " << i->phi() << endl;
	}
*/
        MyGlobalPoint ecalHitPoint(0,0,0);
        return ecalHitPoint;
}

MyGlobalPoint TrackEcalHitPoint::convert(const PFCandidate* pfCand){

        math::XYZPointF pos = pfCand->positionAtECALEntrance();

        MyGlobalPoint ecalHitPoint(0,0,0);
        ecalHitPoint.SetX(pos.x());
        ecalHitPoint.SetY(pos.y());
        ecalHitPoint.SetZ(pos.z());

        return ecalHitPoint;
}
