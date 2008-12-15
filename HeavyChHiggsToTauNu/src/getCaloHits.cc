#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"

void MyEventConverter::getCaloHits(const edm::Event& iEvent){
        //hits
        iEvent.getByLabel( "ecalRecHit", "EcalRecHitsEB", EBRecHits );
        iEvent.getByLabel( "ecalRecHit", "EcalRecHitsEE", EERecHits );

        iEvent.getByLabel( "hbhereco", HBHERecHits );
        iEvent.getByLabel( "horeco", HORecHits );
        iEvent.getByLabel( "hfreco", HFRecHits );
}

