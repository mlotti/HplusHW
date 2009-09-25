#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventConverter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MeasurementConverter.h"

#include "RecoBTag/BTagTools/interface/SignedTransverseImpactParameter.h"
#include "RecoBTag/BTagTools/interface/SignedImpactParameter3D.h"


MyImpactParameter MyEventConverter::impactParameter(const TransientTrack& transientTrack){

	Track track = transientTrack.track();
        GlobalVector direction(track.px(),track.py(),track.pz());

        return impactParameter(transientTrack,direction);
}

MyImpactParameter MyEventConverter::impactParameter(const TransientTrack& transientTrack,const CaloJet* caloJet){

        GlobalVector direction(caloJet->px(),caloJet->py(),caloJet->pz());

	return impactParameter(transientTrack,direction);
}

MyImpactParameter MyEventConverter::impactParameter(const TransientTrack& transientTrack,const Conversion* photon){

        GlobalVector direction(photon->pairMomentum().x(),
                               photon->pairMomentum().y(),
                               photon->pairMomentum().z());

        return impactParameter(transientTrack,direction);
}

MyImpactParameter MyEventConverter::impactParameter(const TransientTrack& transientTrack, const GlobalVector& direction){

        SignedTransverseImpactParameter stip;
        Measurement1D ip  = stip.apply(transientTrack,direction,primaryVertex).second;
        Measurement1D ipZ = stip.zImpactParameter(transientTrack,direction,primaryVertex).second;

        SignedImpactParameter3D signed_ip3D;
        Measurement1D ip3D = signed_ip3D.apply(transientTrack,direction,primaryVertex).second;

	MyMeasurement1D my_ip   = MeasurementConverter::convert(ip);
        MyMeasurement1D my_ipZ  = MeasurementConverter::convert(ipZ);
        MyMeasurement1D my_ip3D = MeasurementConverter::convert(ip3D);

	return MyImpactParameter(my_ip,my_ipZ,my_ip3D);
}
