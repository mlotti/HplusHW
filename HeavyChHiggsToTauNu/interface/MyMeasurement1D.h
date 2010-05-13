#ifndef __MyMeasurement1D__
#define __MyMeasurement1D__

#include "TROOT.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventVersion.h"

/**
 * \brief Class for 1D measurement for MyEvent dataformat
 *
 * 1D measurement contains the measurement value and the uncertainty.
 */
class MyMeasurement1D {
   public:
      /**
       * \brief Constructor
       *
       * \param aValue  Value
       * \param aError  Error estimate (standard deviation)
       */
      MyMeasurement1D(double aValue=0.0, double aError=0.0);

      virtual ~MyMeasurement1D();

      double value() const;
      double error() const;
      double significance() const;

   private:
      double theValue,
             theError;

   ClassDef(MyMeasurement1D, MYEVENT_VERSION)
};
#endif
