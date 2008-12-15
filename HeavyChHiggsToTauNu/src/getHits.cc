#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

vector<MyHit> MyEventConverter::getHits(const Trajectory& trajectory, int& trackLabel){

	vector<MyHit> hits;

        // Loop over measurements to get hits and hit estimates
        vector<TrajectoryMeasurement> meas = trajectory.measurements();
        vector<TrajectoryMeasurement>::const_iterator iMeasEnd = meas.end();
        vector<TrajectoryMeasurement>::const_iterator iMeas;
        for(iMeas = meas.begin(); iMeas != iMeasEnd; ++iMeas) {
                const TrajectoryMeasurement myMeasurement = *iMeas;
                const TransientTrackingRecHit* myMeasuredRecHit = &(*myMeasurement.recHit());
                if (myMeasuredRecHit->isValid()) {
		  MyHit hit = myHitConverter(myMeasuredRecHit, iMeas->estimate());
		  hit.trackAssociationLabel = trackLabel;
                  hits.push_back(hit);
                }
        }
	return hits;
}
