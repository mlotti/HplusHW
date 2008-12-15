#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyImpactParameter.h"

ClassImp(MyImpactParameter)

MyImpactParameter::MyImpactParameter(){
	ip2D = MyMeasurement1D(0,0);
        ipZ  = MyMeasurement1D(0,0);
        ip3D = MyMeasurement1D(0,0);
}

MyImpactParameter::MyImpactParameter(MyMeasurement1D ip_2d,MyMeasurement1D ip_z,MyMeasurement1D ip_3d){
	ip2D = ip_2d;
        ipZ  = ip_z;
	ip3D = ip_3d;
}
MyImpactParameter::~MyImpactParameter(){}

MyMeasurement1D MyImpactParameter::impactParameter2D(){ return ip2D; }
MyMeasurement1D MyImpactParameter::impactParameterZ() { return ipZ; }
MyMeasurement1D MyImpactParameter::impactParameter3D(){ return ip3D; }

