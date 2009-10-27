#ifndef MY_MEASUREMENT1D
#define MY_MEASUREMENT1D

using namespace std;

#include "TROOT.h"

class MyMeasurement1D {
   public:
      MyMeasurement1D();
      MyMeasurement1D(double);
      MyMeasurement1D(double,double);
      virtual ~MyMeasurement1D();

      double value() const;
      double error() const;
      double significance() const;

   private:
      double theValue,
             theError;

   ClassDef(MyMeasurement1D,1)
};
#endif
