#include "HiggsAnalysis/MyEventNTPLMaker/interface/ImpactParameterConverter.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MeasurementConverter.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "DataFormats/JetReco/interface/CaloJet.h"

#include "RecoBTag/BTagTools/interface/SignedTransverseImpactParameter.h"
#include "RecoBTag/BTagTools/interface/SignedImpactParameter3D.h"

using reco::TransientTrack;
using reco::CaloJet;
using reco::Conversion;
using reco::Track;

ImpactParameterConverter::ImpactParameterConverter(const reco::Vertex& pv):
  primaryVertex(pv)
{}
ImpactParameterConverter::~ImpactParameterConverter() {}

MyImpactParameter ImpactParameterConverter::convert(const TransientTrack& transientTrack) const{
	const Track& track = transientTrack.track();
        GlobalVector direction(track.px(),track.py(),track.pz());

        return convert(transientTrack,direction);
}

MyImpactParameter ImpactParameterConverter::convert(const TransientTrack& transientTrack, const GlobalVector& direction) const {

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
