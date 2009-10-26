#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"

using edm::Handle;
using reco::Vertex;
using reco::VertexCollection;

bool MyEventConverter::primaryVertexFound(const edm::Event& iEvent){
	bool primaryVertexFound = false;

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
//                                track_iterator iTrack;
				Vertex::trackRef_iterator iTrack;
                                for(iTrack  = iVertex->tracks_begin();
                                    iTrack != iVertex->tracks_end();++iTrack){
                                        ptsum += (*iTrack)->pt();
                                }
                                if(ptsum > ptmax){
                                        ptmax = ptsum;
                                        primaryVertex = *iVertex;
					primaryVertexFound = true;
                                }
                        }
                }
        }
	return primaryVertexFound;
}
