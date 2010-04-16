#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexConverter.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"

bool VertexConverter::findPrimaryVertex(const edm::Event& iEvent, const edm::InputTag& label, reco::Vertex* primaryVertex) {
        edm::Handle<edm::View<reco::Vertex> > vertexHandle;

        iEvent.getByLabel(label, vertexHandle);

        const edm::View<reco::Vertex>& vertexCollection(*vertexHandle);
/*
        double ptmax = 0;
        edm::View<reco::Vertex>::const_iterator iVertex;
        edm::View<reco::Vertex>::const_iterator found = vertexCollection.end();
        for(iVertex = vertexCollection.begin(); iVertex!= vertexCollection.end(); ++iVertex) {
                double ptsum = 0;
                reco::Vertex::trackRef_iterator iTrack;
                for(iTrack  = iVertex->tracks_begin(); iTrack != iVertex->tracks_end(); ++iTrack)
                        ptsum += (*iTrack)->pt();

                if(ptsum > ptmax) {
                        ptmax = ptsum;
                        found = iVertex;
                }
        }
        if(found == vertexCollection.end())
                return false;
        *primaryVertex = *found;
        return true;
*/
// 16.4.2010/SLehti: In the 7 TeV data all events have a vertex, but the vertices
//                   contain no associated tracks. Therefore the ptsum calc. is
//                   disabled, and vertex selection simplified. FIXME: This situation
//                   needs to be checked later!
	if(vertexHandle->size() == 0) return false;
	*primaryVertex = *(vertexCollection.begin());
	return true;
// End of fix
}

MyVertex VertexConverter::convert(const reco::Vertex& vertex){

	MyVertex V;
	V.SetX(vertex.x());
	V.SetY(vertex.y());
        V.SetZ(vertex.z());

        V.dxx  = vertex.covariance(0,0);
        V.dxy  = vertex.covariance(0,1);
        V.dxz  = vertex.covariance(0,2);
        V.dyy  = vertex.covariance(1,1);
        V.dyz  = vertex.covariance(1,2);
        V.dzz  = vertex.covariance(2,2);

	/*
        V.dxx  = vertex.covariance(1,1);
        V.dxy  = vertex.covariance(1,2);
        V.dxz  = vertex.covariance(1,3);
        V.dyy  = vertex.covariance(2,2);
        V.dyz  = vertex.covariance(2,3);
        V.dzz  = vertex.covariance(3,3);
	*/
	return V;
}

MyVertex VertexConverter::convert(const TransientVertex& vertex){

        MyVertex V(0,0,0);
	if(vertex.isValid()) {
          V.SetX(vertex.position().x());
          V.SetY(vertex.position().y());
          V.SetZ(vertex.position().z());

          V.dxx  = vertex.positionError().matrix()(1,1);
          V.dxy  = vertex.positionError().matrix()(1,2);
          V.dxz  = vertex.positionError().matrix()(1,3);
          V.dyy  = vertex.positionError().matrix()(2,2);
          V.dyz  = vertex.positionError().matrix()(2,3);
          V.dzz  = vertex.positionError().matrix()(3,3);
	}
        return V;
}

void VertexConverter::addSecondaryVertices(const std::vector<reco::TransientTrack>& transientTracks, std::vector<MyVertex>& vertices) {
	if(transientTracks.size() > 1){
		KalmanVertexFitter kvf(true);
		TransientVertex tv = kvf.vertex(transientTracks);

		if(tv.isValid()){
			MyVertex vertex = convert(tv);
			vertices.push_back(vertex);
		}
	}
}

