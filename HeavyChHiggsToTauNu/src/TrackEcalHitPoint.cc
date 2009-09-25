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

        double maxTowerEt = 0;
        vector<CaloTowerPtr> towers = caloJet->getCaloConstituents();
        vector<CaloTowerPtr>::const_iterator maxTower = towers.end();
        for(vector<CaloTowerPtr>::const_iterator iTower = towers.begin();
                                                 iTower != towers.end(); iTower++){
                //size_t numRecHits = (**iTower).constituentsSize();
                if((*iTower)->et() > maxTowerEt){
                        maxTowerEt = (*iTower)->et();
                        maxTower = iTower;
                }
        }
        if(maxTower == towers.end())
          return MyGlobalPoint(0,0,0);

        //FIXME: is this correct?
        CaloTower::Vector mom = (*maxTower)->momentum();
        TrajectoryStateClosestToPoint TSCP = transientTrack.trajectoryStateClosestToPoint(GlobalPoint(mom.x(), mom.y(), mom.z()));
        GlobalPoint trackEcalHitPoint = TSCP.position();

        return MyGlobalPoint(trackEcalHitPoint.x(), trackEcalHitPoint.y(), trackEcalHitPoint.z());
}

MyGlobalPoint TrackEcalHitPoint::convert(const TransientTrack& transientTrack,const GsfElectron* electron){
        //FIXME: is this correct?
	math::XYZVector pos = electron->trackMomentumAtCalo();
        return MyGlobalPoint(pos.x(), pos.y(), pos.z());
}

MyGlobalPoint TrackEcalHitPoint::convert(const TransientTrack& transientTrack,const pat::Electron* electron){
        //FIXME: is this correct?
        math::XYZVector pos = electron->trackMomentumAtCalo();
        return MyGlobalPoint(pos.x(), pos.y(), pos.z());
}

MyGlobalPoint TrackEcalHitPoint::convert(const TransientTrack& transientTrack,const Conversion* photon){
/* FIXME
	Conversion* convPhoton = const_cast<Conversion*>(photon);
	vector<math::XYZPoint> const & ecalHitPositionVector = convPhoton->ecalImpactPosition();

	for(vector<math::XYZPoint>::const_iterator i = ecalHitPositionVector.begin(); i!= ecalHitPositionVector.end(); ++i){
		cout << "ecalhitpoint eta,phi " << i->eta() << " " << i->phi() << endl;
	}
*/
        return MyGlobalPoint(0,0,0);
}

MyGlobalPoint TrackEcalHitPoint::convert(const PFCandidate* pfCand){
        const math::XYZPointF& pos = pfCand->positionAtECALEntrance();
        return MyGlobalPoint(pos.x(), pos.y(), pos.z());
}
