#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"

MyGlobalPoint MyEventConverter::getMCPrimaryVertex(const edm::Event& iEvent){

	Handle<SimVertexContainer> simVertices;
	iEvent.getByLabel("g4SimHits",simVertices);

	MyGlobalPoint mcPV;
	if(simVertices->size() > 0){
		mcPV.SetX((*simVertices)[0].position().x());
		mcPV.SetY((*simVertices)[0].position().y());
		mcPV.SetZ((*simVertices)[0].position().z());
	}else{
                mcPV.SetX(-999);
                mcPV.SetY(-999);
                mcPV.SetZ(-999);
	}
	return mcPV;
}
