#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyImpactParameter.h"

ClassImp(MyImpactParameter)

MyImpactParameter::MyImpactParameter(): ip2D(), ipZ(), ip3D() {}

MyImpactParameter::MyImpactParameter(const MyMeasurement1D& ip_2d, const MyMeasurement1D& ip_z, const MyMeasurement1D& ip_3d):
  ip2D(ip_2d), ipZ(ip_z), ip3D(ip_3d)
{}

MyImpactParameter::~MyImpactParameter(){}

MyMeasurement1D MyImpactParameter::impactParameter2D() const { return ip2D; }
MyMeasurement1D MyImpactParameter::impactParameterZ()  const { return ipZ; }
MyMeasurement1D MyImpactParameter::impactParameter3D() const { return ip3D; }

