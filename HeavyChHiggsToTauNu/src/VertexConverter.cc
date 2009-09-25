#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexConverter.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"


MyVertex VertexConverter::convert(const reco::Vertex& vertex){

	MyVertex V;
	V.SetX(vertex.x());
	V.SetY(vertex.y());
        V.SetZ(vertex.z());

        V.dxx  = vertex.covariance(1,1);
        V.dxy  = vertex.covariance(1,2);
        V.dxz  = vertex.covariance(1,3);
        V.dyy  = vertex.covariance(2,2);
        V.dyz  = vertex.covariance(2,3);
        V.dzz  = vertex.covariance(3,3);

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

