#ifndef __MyMet__
#define __MyMet__

#include "TVector2.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventVersion.h"

#include<iostream>

/**
 * \brief Missing transverse energy class for MyEvent dataformat
 */
class MyMET: public TVector2 {
   public:
      	MyMET();
        
        /**
         * \brief Constructor
         *
         * \param x  x component
         * \param y  y component
         */
        MyMET(double x, double y);
      	virtual ~MyMET();

        /**
         * \brief Get the length of the vector
         */
        double value() const;

        double x() const;
        double y() const;
        double phi() const;

      	void print(std::ostream& out = std::cout) const;

   private:

   ClassDef(MyMET, MYEVENT_VERSION)
};
#endif
