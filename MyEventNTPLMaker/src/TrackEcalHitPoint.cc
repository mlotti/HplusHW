#include "HiggsAnalysis/MyEventNTPLMaker/interface/TrackEcalHitPoint.h"

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

TrackEcalHitPoint::TrackEcalHitPoint(const edm::ParameterSet& iConfig):
  trackAssociator_(iConfig)
{}
TrackEcalHitPoint::~TrackEcalHitPoint() {}

void TrackEcalHitPoint::setEvent(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  trackAssociator_.setEvent(iEvent, iSetup);
}

void TrackEcalHitPoint::reset() {
  trackAssociator_.reset();
}

MyGlobalPoint TrackEcalHitPoint::convert(const TransientTrack& transientTrack,const CaloJet& caloJet) {
        // New method
        math::XYZPoint hitPos = trackAssociator_.trackPositionAtEcal(transientTrack.track());
        // Return new method
        return MyGlobalPoint(hitPos.x(), hitPos.y(), hitPos.z());

        // The old method produced sometimes TrajectoryStateException
#ifdef OLD
        // Old method
        GlobalPoint ecalHitPosition(0,0,0);
        double maxTowerEt = 0;
        vector<CaloTowerPtr> towers = caloJet.getCaloConstituents();
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

        GlobalPoint trackEcalHitPoint = transientTrack.trajectoryStateClosestToPoint(ecalHitPosition).position();
        GlobalPoint trackEcalHitPoint2 = transientTrack.stateOnSurface(ecalHitPosition).globalPosition();
 
        MyGlobalPoint ecalHitPoint(trackEcalHitPoint.x(), trackEcalHitPoint.y(), trackEcalHitPoint.z());
        MyGlobalPoint ecalHitPoint2(trackEcalHitPoint2.x(), trackEcalHitPoint2.y(), trackEcalHitPoint.z());

        // Comparison
        /*
        std::cout << "    Track ecal hit point: TrackAssociator (" << hitPos.x() << "," << hitPos.y() << "," << hitPos.z()
                  << ") TSOS (" << ecalHitPoint2.X() << "," << ecalHitPoint2.Y() << "," << ecalHitPoint.Z()
                  << ") TCSP (" << ecalHitPoint.X() << "," << ecalHitPoint.Y() << "," << ecalHitPoint.Z()
                  << std::endl;
        */

        // Return new method
        return MyGlobalPoint(hitPos.x(), hitPos.y(), hitPos.z());
#endif
}

MyGlobalPoint TrackEcalHitPoint::convert(const GsfElectron& electron){
	math::XYZPoint pos = electron.trackPositionAtCalo();
        return MyGlobalPoint(pos.x(), pos.y(), pos.z());
}

MyGlobalPoint TrackEcalHitPoint::convert(const pat::Electron& electron){
	math::XYZPoint pos = electron.trackPositionAtCalo();
        return MyGlobalPoint(pos.x(), pos.y(), pos.z());
}

MyGlobalPoint TrackEcalHitPoint::convert(const TransientTrack& transientTrack,const Conversion& photon){
/* FIXME
	Conversion* convPhoton = const_cast<Conversion*>(photon);
	vector<math::XYZPoint> const & ecalHitPositionVector = convPhoton->ecalImpactPosition();

	for(vector<math::XYZPoint>::const_iterator i = ecalHitPositionVector.begin(); i!= ecalHitPositionVector.end(); ++i){
		cout << "ecalhitpoint eta,phi " << i->eta() << " " << i->phi() << endl;
	}
*/
        return MyGlobalPoint(0,0,0);
}

MyGlobalPoint TrackEcalHitPoint::convert(const PFCandidate& pfCand){
        const math::XYZPointF& pos = pfCand.positionAtECALEntrance();
        return MyGlobalPoint(pos.x(), pos.y(), pos.z());
}
