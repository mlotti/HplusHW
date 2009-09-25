#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TrackConverter.h"

void MyEventConverter::getTracks(const edm::Event& iEvent){

        Handle<TrackCollection> trackHandle;
        try{
          //iEvent.getByLabel("ctfWithMaterialTracks",trackHandle);
          iEvent.getByLabel(trackCollectionSelection,trackHandle);
        }catch(...) {;}

        if(trackHandle.isValid()) tracks = *(trackHandle.product());
        cout << "Track collection " << trackCollectionSelection.label()
             << " size " << tracks.size() << endl;
}

vector<MyTrack> MyEventConverter::getTracks(MyJet& direction){
	vector<MyTrack> tracksInJetCone = direction.tracks;
	TrackCollection::const_iterator iTrack;

	// remove duplicate lepton tracks
	TrackCollection::const_iterator leptonTrack = tracks.end();
	if(direction.getTracks().size() > 0){
		double DRmin = 9999;
		for(iTrack = tracks.begin(); iTrack != tracks.end(); ++iTrack){
			TLorentzVector p4(iTrack->momentum().x(),iTrack->momentum().y(),iTrack->momentum().z(),iTrack->momentum().r());
                	double DR = direction.p4().DeltaR(p4);
			if(DR < DRmin){
				DRmin = DR;
				leptonTrack = iTrack;
			}
		}
	}

	for(iTrack = tracks.begin(); iTrack != tracks.end(); ++iTrack){
		if(iTrack == leptonTrack) continue;
		TLorentzVector p4(iTrack->momentum().x(),iTrack->momentum().y(),iTrack->momentum().z(),iTrack->momentum().r());
                double DR = direction.p4().DeltaR(p4);
		if(DR < 0.5){
			tracksInJetCone.push_back(TrackConverter::convert(*iTrack));
		}
	}

	return tracksInJetCone;
}

vector<Track> MyEventConverter::tracksInCone(const math::XYZTLorentzVector direction,double cone){

	vector<Track> associatedTracks;

	TrackCollection::const_iterator iTrack;
	for(iTrack = tracks.begin(); iTrack != tracks.end(); iTrack++){
	  //		TVector3 p(iTrack->momentum().x(),iTrack->momentum().y(),iTrack->momentum().z());
		double DR = ROOT::Math::VectorUtil::DeltaR(direction,iTrack->momentum());
		//if(DR < cone) associatedTracks.push_back(edm::Ref<TrackCollection>(tracks, t));
		if(DR < cone) associatedTracks.push_back(*iTrack);
	}
	return associatedTracks;
}

vector<Track> MyEventConverter::tracksInCone(const math::XYZTLorentzVector direction, double cone, vector<Trajectory>* associatedTrajectories) {
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
