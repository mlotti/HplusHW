#ifndef MY_IMPACTPARAMETER
#define MY_IMPACTPARAMETER

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyMeasurement1D.h"
using namespace std;

#include "TROOT.h"

class MyImpactParameter {
  public:
	MyImpactParameter();
	MyImpactParameter(MyMeasurement1D,MyMeasurement1D,MyMeasurement1D);
	virtual ~MyImpactParameter();

	MyMeasurement1D impactParameter2D();
        MyMeasurement1D impactParameterZ();
        MyMeasurement1D impactParameter3D();

  private:
	MyMeasurement1D ip2D;
	MyMeasurement1D ipZ;
	MyMeasurement1D ip3D;

  ClassDef(MyImpactParameter,1)
};
#endif
