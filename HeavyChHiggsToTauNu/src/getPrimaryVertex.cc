#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexConverter.h"

MyGlobalPoint MyEventConverter::getPrimaryVertex(){
	return VertexConverter::convert(primaryVertex);
}
