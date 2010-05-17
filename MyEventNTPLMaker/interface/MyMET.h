#ifndef __MyMet__
#define __MyMet__

#include "TVector2.h"
#include "TVector3.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEventVersion.h"

#include<iostream>
#include<string>

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

        TVector3 tvector3() const;

      	void print(std::ostream& out = std::cout) const;

        /**
         * \brief Name of the MET object
         *
         * This is the same as is the key in the MyEvent::mets map. We
         * felt that it would be important for the MET object itself
         * to know it's name, so it can be checked from the object itself.
         *
         * The name is set by MyEvent::getMET(const std::string&), and
         * hence it doesn't have to be stored in the TTree by ROOT. To
         * prevent the serialization, there is the //! after it.
         * Actually this might only work for CINT dictionaries, for
         * reflex we need something else.
         */
        std::string name; //!
   private:

   ClassDef(MyMET, MYEVENT_VERSION)
};
#endif
