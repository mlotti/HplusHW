#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

void MyEventConverter::eventSetup(const edm::EventSetup& iSetup){

        edm::ESHandle<TransientTrackBuilder> builder;
        iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",builder);
        transientTrackBuilder = builder.product();

        // transient rec hit builder
//        edm::ESHandle<TransientTrackingRecHitBuilder> theTTRHBuilderHandle;
//        iSetup.get<TransientRecHitRecord>().get("WithoutRefit",theTTRHBuilderHandle);
//        TTRHBuilder = theTTRHBuilderHandle.product();

	for(unsigned int i = 0; i < jetEnergyCorrectionTypes.size(); ++i){
		const JetCorrector* theCorrector = JetCorrector::getJetCorrector(jetEnergyCorrectionTypes[i].label(),iSetup);
		jetEnergyCorrections.push_back(theCorrector);
	}
}
