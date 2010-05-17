#include "HiggsAnalysis/MyEventNTPLMaker/interface/TrackConverter.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyJet.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"

#include "Math/VectorUtil.h"

using reco::TransientTrack;
using reco::Track;
using reco::TrackCollection;
using reco::PFCandidate;
using std::vector;

static const reco::TrackCollection& helper(const edm::Event& iEvent, const edm::InputTag& label) {
        edm::Handle<reco::TrackCollection> handle;
        iEvent.getByLabel(label, handle);
        if(edm::isDebugEnabled())
                LogDebug("MyEventConverter") << "Track collection " << label << " size " << handle->size() << std::endl;
        return *handle;
}

TrackConverter::TrackConverter(const edm::Event& iEvent, const edm::InputTag& label_):
        tracks(helper(iEvent, label_)),
        label(label_)
{}
TrackConverter::~TrackConverter() {}

const std::string& TrackConverter::getCollectionLabel() const {
        return label.label();
}

void TrackConverter::addTracksInCone(MyJet& direction, double cone) const {
	TrackCollection::const_iterator iTrack;

	// remove duplicate lepton tracks
	TrackCollection::const_iterator leptonTrack = tracks.end();
	if(direction.tracks.size() > 0) {
		double DRmin = 9999;
		for(iTrack = tracks.begin(); iTrack != tracks.end(); ++iTrack){
                	double DR = direction.DeltaR(TLorentzVector(iTrack->momentum().x(), iTrack->momentum().y(), iTrack->momentum().z(), iTrack->momentum().r()));
			if(DR < DRmin){
				DRmin = DR;
				leptonTrack = iTrack;
			}
		}
	}

	for(iTrack = tracks.begin(); iTrack != tracks.end(); ++iTrack){
		if(iTrack == leptonTrack) continue;
                double DR = direction.DeltaR(TLorentzVector(iTrack->momentum().x(), iTrack->momentum().y(), iTrack->momentum().z(), iTrack->momentum().r()));
		if(DR < cone) {
			direction.tracks.push_back(convert(*iTrack));
		}
	}
}

std::vector<Track> TrackConverter::getTracksInCone(const math::XYZTLorentzVector& direction, double cone) const {
	vector<Track> associatedTracks;

	TrackCollection::const_iterator iTrack;
	for(iTrack = tracks.begin(); iTrack != tracks.end(); iTrack++){
		double DR = ROOT::Math::VectorUtil::DeltaR(direction,iTrack->momentum());
		//if(DR < cone) associatedTracks.push_back(edm::Ref<TrackCollection>(tracks, t));
		if(DR < cone) associatedTracks.push_back(*iTrack);
	}
	return associatedTracks;
}

std::vector<Track> TrackConverter::getTracksInCone(const math::XYZTLorentzVector& direction, double cone, const std::vector<Trajectory>& associatedTrajectories) const {
        	// Check that track collection and trajectory collection are equally long
//       	bool trajectoryMatchedStatus = (myTrajectoryCollectionHandle->size() == tracks.size()); // tracks is here the track collection

        vector<Track> associatedTracks;

   	TrackCollection::const_iterator iTrack;
//       	vector<Trajectory>::const_iterator iTrajectory = myTrajectoryCollectionHandle->begin();
   	for(iTrack = tracks.begin(); iTrack != tracks.end(); iTrack++){
       		double DR = ROOT::Math::VectorUtil::DeltaR(direction,iTrack->momentum());
       		if(DR < cone) {
                  associatedTracks.push_back(*iTrack);
/*
                  if (trajectoryMatchedStatus) {
                    associatedTrajectories->push_back(*iTrajectory);
                  }else{
                    // Loop over trajectories to match with hits, pt and eta
                    double minDr = 999999;
                    vector<Trajectory>::const_iterator iTrajSelected;
                    vector<Trajectory>::const_iterator iTrajEnd = myTrajectoryCollectionHandle->end();
                    for(vector<Trajectory>::const_iterator iTraj = myTrajectoryCollectionHandle->begin(); 
                                                           iTraj!= iTrajEnd; ++iTraj) {
                     	// hit count has to be equal
                     	if ((int)iTrack->recHitsSize() == iTraj->foundHits()) {
                       	  // match pt and eta; phi is too inaccurate for low pt tracks
                          GlobalVector myTrajectoryMom = iTraj->firstMeasurement().predictedState().globalMomentum();
                       	  double deltaPx = iTrack->innerMomentum().x() - myTrajectoryMom.x();
                          double deltaPy = iTrack->innerMomentum().y() - myTrajectoryMom.y();
                          double deltaEta = iTrack->innerMomentum().eta() - myTrajectoryMom.eta();
                          double myDelta = deltaPx*deltaPx + deltaPy*deltaPy + deltaEta*deltaEta;
                          if (myDelta < minDr) {
                            minDr = myDelta;
                            iTrajSelected = iTraj;
                          }
                     	}
                    }
                    if (TMath::Sqrt(minDr) < 999999) {
                       associatedTrajectories->push_back(*iTrajSelected);
                    }
              	  }
*/
		}
//        	++iTrajectory;
   	}
   	return associatedTracks;
}



MyTrack TrackConverter::convert(const TransientTrack& transientTrack){
	return convert(transientTrack.track());
}

MyTrack TrackConverter::convert(const Track& recTrack){

        MyTrack track(recTrack.px(), recTrack.py(), recTrack.pz(), recTrack.p());
        track.trackCharge    = recTrack.charge();
        track.normChiSquared = recTrack.normalizedChi2();
        track.nHits          = recTrack.numberOfValidHits();

        return track;
}

MyTrack TrackConverter::convert(const PFCandidate& pfTrack){

        MyTrack track(pfTrack.px(), pfTrack.py(), pfTrack.pz(), pfTrack.p());
        track.trackCharge  = pfTrack.charge();
	track.particleType = pfTrack.particleId();

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
