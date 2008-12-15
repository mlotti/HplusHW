#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"

MyGlobalPoint MyEventConverter::getMCPrimaryVertex(const edm::Event& iEvent){

	Handle<SimVertexContainer> simVertices;
	iEvent.getByLabel("g4SimHits",simVertices);

	MyGlobalPoint mcPV;
	if(simVertices->size() > 0){
		mcPV.x = (*simVertices)[0].position().x();
		mcPV.y = (*simVertices)[0].position().y();
		mcPV.z = (*simVertices)[0].position().z();
	}else{
                mcPV.x = -999;
                mcPV.y = -999;
                mcPV.z = -999;
	}
	return mcPV;
}
