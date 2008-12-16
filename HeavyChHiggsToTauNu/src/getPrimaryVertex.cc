#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

MyGlobalPoint MyEventConverter::getPrimaryVertex(){
	return myVertexConverter(primaryVertex);
}
