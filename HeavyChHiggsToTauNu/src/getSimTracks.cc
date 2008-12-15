#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "SimDataFormats/Track/interface/SimTrack.h"
#include "SimDataFormats/Track/interface/SimTrackContainer.h"
#include "SimDataFormats/Vertex/interface/SimVertex.h"
#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"

double deltaR(double eta1, double eta2, double phi1, double phi2);

vector<MySimTrack> MyEventConverter::getSimTracks(const edm::Event& iEvent,MyEvent* event){
  vector<MySimTrack> simTracks;
  // save sim tracks in cone of 0.7 around tau candidate leading track
  const double myMatchCone = 0.70;

  Handle<SimTrackContainer> simTrackHandle;
  iEvent.getByType<SimTrackContainer>(simTrackHandle);
  if (! simTrackHandle.isValid()) {
    cout << "getSimTracks error! No SimTracks found!" << endl;
    return simTracks; // return empty vector
  }
  Handle<SimVertexContainer> simVertices;
  iEvent.getByType<SimVertexContainer>(simVertices);
  if (! simTrackHandle.isValid()) {
    cout << "getSimTracks error! No SimVertices found!" << endl;
    return simTracks; // return empty vector
  }

  // Loop over tau candidates
  vector<MyJet>::iterator iJet = event->taujets.begin();
  for ( ; iJet != event->taujets.end(); ++iJet) {
    // Get leading track
    MyTrack myLdgTrack = (*iJet).leadingTrack();
//    cout << "jet ldg track eta=" << myLdgTrack.eta()
//	 << " phi=" << myLdgTrack.phi() << endl;

    // Loop over SimTracks in container
    SimTrackContainer::const_iterator iSim = simTrackHandle->begin();
    for( ; iSim != simTrackHandle->end(); ++iSim) {
      const HepLorentzVector myMomentum = (*iSim).momentum();
      if (myMomentum.perp() > 1) { // require sim track pt > 1 GeV
	if (deltaR(myLdgTrack.eta(), myMomentum.eta(),
		   myLdgTrack.phi(), myMomentum.phi()) < myMatchCone) {
	  //cout << "- simTrack eta=" << myMomentum.eta()
	  //     << " phi=" << myMomentum.phi()
	  //     << " DeltaR=" 
	  //     << deltaR(myLdgTrack.eta(), myMomentum.eta(),
	  //        myLdgTrack.phi(), myMomentum.phi()) << endl;

	  // Save sim track
	  MySimTrack mySim;
	  mySim.SetXYZM(myMomentum.x(), myMomentum.y(), myMomentum.z(), 0);
	  mySim.theGenPID = (*iSim).genpartIndex();
	  mySim.theType = (*iSim).type();
	  mySim.theTrackID = (int)(*iSim).trackId();
	  // Production point of sim track
	  if ((*iSim).vertIndex() >= 0) {
	    SimVertex mySimVertex = (*simVertices)[(*iSim).vertIndex()];
	    mySim.thePosition.SetXYZ(mySimVertex.position().x(),
				     mySimVertex.position().y(),
				     mySimVertex.position().z());
	  } else {
	    mySim.thePosition.SetXYZ(0,0,0);
	  }
	  // ECAL hit point
	  const Hep3Vector myPos = (*iSim).trackerSurfacePosition();
	  mySim.trackEcalHitPoint.x = myPos.x();
	  mySim.trackEcalHitPoint.y = myPos.y();
	  mySim.trackEcalHitPoint.z = myPos.z();
	  // Store sim track
	  //mySim.print();
	  simTracks.push_back(mySim);
	}
      }
    }
  }

  return simTracks;
}

