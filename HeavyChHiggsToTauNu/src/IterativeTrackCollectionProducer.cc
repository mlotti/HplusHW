#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/IterativeTrackCollectionProducer.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "TrackingTools/PatternTools/interface/Trajectory.h"

using namespace reco;

IterativeTrackCollectionProducer::IterativeTrackCollectionProducer(const edm::ParameterSet& iConfig){
	produces<TrackCollection>().setBranchAlias("iterativeTracks");
	produces< vector<Trajectory> >().setBranchAlias("iterativeTrajectories");
}

IterativeTrackCollectionProducer::~IterativeTrackCollectionProducer(){}

void IterativeTrackCollectionProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup){

        //
        Handle<TrackCollection> firstIterativeTrackHandle;
        try{
          iEvent.getByLabel("firstvtxFilt",firstIterativeTrackHandle);
        }catch(...) {;}

        TrackCollection iterTracks1;
        if(firstIterativeTrackHandle.isValid()) iterTracks1 = *(firstIterativeTrackHandle.product());
        cout << "Iterative track collection 1 size " << iterTracks1.size() << endl;

	Handle<vector<Trajectory> > firstTrajectoryHandle;
        try { 
	  iEvent.getByLabel("firstvtxFilt",firstTrajectoryHandle);
	}catch(...) {;}

        vector<Trajectory> trajectories1;
        if(firstTrajectoryHandle.isValid()) trajectories1 = *(firstTrajectoryHandle.product());
        cout << "Iterative trajectory collection 1 size " << trajectories1.size() << endl;

        //
        Handle<TrackCollection> secondIterativeTrackHandle;
        try{
          iEvent.getByLabel("secondvtxFilt",secondIterativeTrackHandle);
        }catch(...) {;}

        TrackCollection iterTracks2;
        if(secondIterativeTrackHandle.isValid()) iterTracks2 = *(secondIterativeTrackHandle.product());
        cout << "Iterative track collection 2 size " << iterTracks2.size() << endl;

        Handle<vector<Trajectory> > secondTrajectoryHandle;
        try { 
	  iEvent.getByLabel("secondvtxFilt",secondTrajectoryHandle); 
	}catch(...) {;}

        vector<Trajectory> trajectories2;
        if(secondTrajectoryHandle.isValid()) trajectories2 = *(secondTrajectoryHandle.product());
        cout << "Iterative trajectory collection 2 size " << trajectories2.size() << endl;

        //
        Handle<TrackCollection> thirdIterativeTrackHandle;
        try{
          iEvent.getByLabel("thirdvtxFilt",thirdIterativeTrackHandle);
        }catch(...) {;}

        TrackCollection iterTracks3;
        if(thirdIterativeTrackHandle.isValid()) iterTracks3 = *(thirdIterativeTrackHandle.product());
        cout << "Iterative track collection 3 size " << iterTracks3.size() << endl;

        Handle<vector<Trajectory> > thirdTrajectoryHandle;
        try{
	  iEvent.getByLabel("thirdvtxFilt",thirdTrajectoryHandle); 
	}catch(...) {;}

        vector<Trajectory> trajectories3;
        if(thirdTrajectoryHandle.isValid()) trajectories3 = *(thirdTrajectoryHandle.product());
        cout << "Iterative trajectory collection 3 size " << trajectories3.size() << endl;

        //
        Handle<TrackCollection> fourthIterativeTrackHandle;
        try{
          iEvent.getByLabel("fourthvtxFilt",fourthIterativeTrackHandle);
        }catch(...) {;}

        TrackCollection iterTracks4;
        if(fourthIterativeTrackHandle.isValid()) iterTracks4 = *(fourthIterativeTrackHandle.product());
        cout << "Iterative track collection 4 size " << iterTracks4.size() << endl;

        Handle<vector<Trajectory> > fourthTrajectoryHandle;
        try{
 	  iEvent.getByLabel("fourthvtxFilt",fourthTrajectoryHandle); 
	}catch(...) {;}

        vector<Trajectory> trajectories4;
        if(fourthTrajectoryHandle.isValid()) trajectories4 = *(fourthTrajectoryHandle.product());
        cout << "Iterative trajectory collection 4 size " << trajectories4.size() << endl;



	// Add tracks to event
        TrackCollection* iterativeTrackCollection = new TrackCollection;

        TrackCollection::const_iterator iTrack;
        for(iTrack = iterTracks1.begin(); iTrack != iterTracks1.end(); ++iTrack){
                iterativeTrackCollection->push_back(*iTrack);
        }
        for(iTrack = iterTracks2.begin(); iTrack != iterTracks2.end(); ++iTrack){
                iterativeTrackCollection->push_back(*iTrack);
        }
        for(iTrack = iterTracks3.begin(); iTrack != iterTracks3.end(); ++iTrack){
                iterativeTrackCollection->push_back(*iTrack);
        }
        for(iTrack = iterTracks4.begin(); iTrack != iterTracks4.end(); ++iTrack){
                iterativeTrackCollection->push_back(*iTrack);
        }

        auto_ptr<TrackCollection> itc(iterativeTrackCollection);
        iEvent.put(itc);


        // Add trajectories to event
        vector<Trajectory>* trajectoryCollection = new vector<Trajectory>;
        vector<Trajectory>::const_iterator iTraj;
        for (iTraj = trajectories1.begin(); iTraj != trajectories1.end(); ++iTraj) {
          trajectoryCollection->push_back(*iTraj);
        }
        for (iTraj = trajectories2.begin(); iTraj != trajectories2.end(); ++iTraj) {
          trajectoryCollection->push_back(*iTraj);
        }
        for (iTraj = trajectories3.begin(); iTraj != trajectories3.end(); ++iTraj) {
          trajectoryCollection->push_back(*iTraj);
        }
        for (iTraj = trajectories4.begin(); iTraj != trajectories4.end(); ++iTraj) {
          trajectoryCollection->push_back(*iTraj);
        }
        auto_ptr<vector<Trajectory> > iTrajPtr(trajectoryCollection);
        iEvent.put(iTrajPtr);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE( IterativeTrackCollectionProducer );
