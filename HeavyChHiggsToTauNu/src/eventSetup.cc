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
		jetEnergyCorrections[i] = theCorrector;
	}
//        if(jetEnergyCorrectionType != "none"){
//	  jetEnergyCorrection = JetCorrector::getJetCorrector(jetEnergyCorrectionType,iSetup);
//	}


        // geometry initialization
        ESHandle<CaloGeometry> geometry;
        iSetup.get<IdealGeometryRecord>().get(geometry);

        EB = geometry->getSubdetectorGeometry(DetId::Ecal,EcalBarrel);
        EE = geometry->getSubdetectorGeometry(DetId::Ecal,EcalEndcap);
        HB = geometry->getSubdetectorGeometry(DetId::Hcal,HcalBarrel);
        HE = geometry->getSubdetectorGeometry(DetId::Hcal,HcalEndcap);
        HO = geometry->getSubdetectorGeometry(DetId::Hcal,HcalOuter);
        HF = geometry->getSubdetectorGeometry(DetId::Hcal,HcalForward);
}
