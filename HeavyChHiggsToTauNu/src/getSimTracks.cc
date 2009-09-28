#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "SimDataFormats/Track/interface/SimTrack.h"
#include "SimDataFormats/Track/interface/SimTrackContainer.h"
#include "SimDataFormats/Vertex/interface/SimVertex.h"
#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"

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
  vector<MyJet*> taujets = event->getCollection("calotaus");
  for (vector<MyJet*>::const_iterator iJet = taujets.begin() ; iJet != taujets.end(); ++iJet) {
    // Get leading track
    const MyTrack* myLdgTrack = (*iJet)->leadingTrack();
    if(myLdgTrack == 0) continue;
    cout << "jet ldg track eta=" << myLdgTrack->eta()
	 << " phi=" << myLdgTrack->phi() << endl;
    // Loop over SimTracks in container
    SimTrackContainer::const_iterator iSim = simTrackHandle->begin();
    for( ; iSim != simTrackHandle->end(); ++iSim) {
//      const math::XYZTLorentzVectorD & myMomentum = (*iSim).momentum();
      TLorentzVector myMomentum((*iSim).momentum().x(),(*iSim).momentum().y(),(*iSim).momentum().z(),(*iSim).momentum().t());
      ////      const HepLorentzVector myMomentum = (*iSim).momentum();
      if (myMomentum.Et() > 1) { // require sim track pt > 1 GeV
	if (myLdgTrack->p4().DeltaR(myMomentum) < myMatchCone ){
//myDeltaR(myLdgTrack->eta(), myMomentum.eta(),
//		   myLdgTrack->phi(), myMomentum.phi()) < myMatchCone) {
	  //cout << "- simTrack eta=" << myMomentum.eta()
	  //     << " phi=" << myMomentum.phi()
	  //     << " myDeltaR=" 
	  //     << myDeltaR(myLdgTrack.eta(), myMomentum.eta(),
	  //        myLdgTrack.phi(), myMomentum.phi()) << endl;

	  // Save sim track
	  MySimTrack mySim;
	  mySim.SetXYZM(myMomentum.X(), myMomentum.Y(), myMomentum.Z(), 0);
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
	  const math::XYZVectorD & myPos = (*iSim).trackerSurfacePosition();
	  ////const Hep3Vector myPos = (*iSim).trackerSurfacePosition();
	  mySim.trackEcalHitPoint.SetX(myPos.x());
	  mySim.trackEcalHitPoint.SetY(myPos.y());
	  mySim.trackEcalHitPoint.SetZ(myPos.z());
	  // Store sim track
	  //mySim.print();
	  simTracks.push_back(mySim);
	}
      }
    }
  }

  return simTracks;
}

