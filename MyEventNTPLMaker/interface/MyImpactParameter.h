#ifndef __MyImpactParameter__
#define __MyImpactParameter__

#include "TROOT.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyMeasurement1D.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEventVersion.h"

/**
 * \brief Impact parameter class for MyEvent dataformat
 */
class MyImpactParameter {
  public:
	MyImpactParameter();

        /**
         * \brief Constructor
         *
         * \param ip_2d   2D impact parameter
         * \param ip_z    Z impact parameter
         * \param ip_3d   3D impact parameter
         */
	MyImpactParameter(const MyMeasurement1D& ip_2d, const MyMeasurement1D& ip_z, const MyMeasurement1D& ip_3d);

	virtual ~MyImpactParameter();

	MyMeasurement1D impactParameter2D() const;
        MyMeasurement1D impactParameterZ() const;
        MyMeasurement1D impactParameter3D() const;

  private:
	MyMeasurement1D ip2D;
	MyMeasurement1D ipZ;
	MyMeasurement1D ip3D;

  ClassDef(MyImpactParameter, MYEVENT_VERSION)
};
#endif
