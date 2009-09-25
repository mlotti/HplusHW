#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackConverter.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"

using reco::TransientTrack;
using reco::Track;
using reco::PFCandidate;

MyTrack TrackConverter::convert(const TransientTrack& transientTrack){
	return convert(transientTrack.track());
}

MyTrack TrackConverter::convert(const Track& recTrack){

        MyTrack track;
        track.SetPx(recTrack.px());
        track.SetPy(recTrack.py());
        track.SetPz(recTrack.pz());
        track.SetE(recTrack.p());
        track.trackCharge    = recTrack.charge();
        track.normChiSquared = recTrack.normalizedChi2();
        track.nHits          = recTrack.numberOfValidHits();

        return track;
}

MyTrack TrackConverter::convert(const PFCandidate* pfTrack){

        MyTrack track;
        track.SetPx(pfTrack->px());
        track.SetPy(pfTrack->py());
        track.SetPz(pfTrack->pz());
        track.SetE(pfTrack->p());
        track.trackCharge  = pfTrack->charge();
	track.particleType = pfTrack->particleId();

        return track;
}
/*
MyTrack MyEventConverter::myTrackConverter(const TransientTrack& transientTrack){
   return myTrackConverter(transientTrack.track());
}

MyTrack MyEventConverter::myTrackConverter(const Track& recTrack, const Trajectory& trajectory){
	MyTrack track = myTrackConverter(recTrack); 

        // Loop over measurements to get hits and hit estimates
        vector<TrajectoryMeasurement> myMeasurements = trajectory.measurements();
        vector<TrajectoryMeasurement>::const_iterator iMeasEnd = myMeasurements.end();
        for(vector<TrajectoryMeasurement>::const_iterator iMeas = myMeasurements.begin(); iMeas != iMeasEnd; ++iMeas) {
       		const TrajectoryMeasurement myMeasurement = *iMeas;
         	const TransientTrackingRecHit* myMeasuredRecHit = &(*myMeasurement.recHit());
         	if (myMeasuredRecHit->isValid()) {
           	  track.hits.push_back(myHitConverter(myMeasuredRecHit, iMeas->estimate()));
         	}
       	}

       	return track;
}
*/
