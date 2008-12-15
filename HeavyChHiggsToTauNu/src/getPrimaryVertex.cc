#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

MyGlobalPoint MyEventConverter::getPrimaryVertex(){
	return myVertexConverter(primaryVertex);
}

MyGlobalPoint MyEventConverter::getPrimaryVertex(const edm::Event& iEvent){

	MyGlobalPoint pv(0,0,-999);
	PVFound = false;

        Handle<VertexCollection> vertexHandle;
        try{
//          iEvent.getByLabel("offlinePrimaryVerticesFromCFTTracks",vertexHandle);
          iEvent.getByLabel("pixelVertices",vertexHandle);
        }catch(...) {;}

        if(vertexHandle.isValid()){
                const reco::VertexCollection vertexCollection = *(vertexHandle.product());
                if(vertexCollection.size() > 0){
                        double ptmax = 0;
                        VertexCollection::const_iterator iVertex;
                        for(iVertex = vertexCollection.begin();
                            iVertex!= vertexCollection.end(); iVertex++){
                                //cout << "vertex x,y,z " << iVertex->x() << " "
                                //                        << iVertex->y() << " "
                                //                        << iVertex->z() << endl;
                                double ptsum = 0;
                                track_iterator iTrack;
                                for(iTrack  = iVertex->tracks_begin();
                                    iTrack != iVertex->tracks_end();iTrack++){
                                        ptsum += (*iTrack)->pt();
                                }
                                if(ptsum > ptmax){
                                        ptmax = ptsum;
                                        primaryVertex = *iVertex;
                                        PVFound = true;
                                }
                        }
                }
        }
	if(PVFound) pv = myVertexConverter(primaryVertex);
	return pv;
}
