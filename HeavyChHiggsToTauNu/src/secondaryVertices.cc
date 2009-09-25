#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexConverter.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"

vector<MyVertex> MyEventConverter::secondaryVertices(vector<TransientTrack>& transientTracks){
	vector<MyVertex> vertices;

	if(transientTracks.size() > 1){
		KalmanVertexFitter kvf(true);
		TransientVertex tv = kvf.vertex(transientTracks);

		if(tv.isValid()){
			MyVertex vertex = VertexConverter::convert(tv);
			vertices.push_back(vertex);
		}
	}
	return vertices;
}
