#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"

void MyEventConverter::eventSetup(const edm::EventSetup& iSetup){

        edm::ESHandle<TransientTrackBuilder> builder;
        iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",builder);
        transientTrackBuilder = builder.product();

        // transient rec hit builder
//        edm::ESHandle<TransientTrackingRecHitBuilder> theTTRHBuilderHandle;
//        iSetup.get<TransientRecHitRecord>().get("WithoutRefit",theTTRHBuilderHandle);
//        TTRHBuilder = theTTRHBuilderHandle.product();
}
