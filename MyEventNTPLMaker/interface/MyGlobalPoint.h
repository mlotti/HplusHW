#ifndef __MyGlobalPoint__
#define __MyGlobalPoint__

#include "TVector3.h"

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEventVersion.h"

/**
 * \brief Global point class for MyEvent dataformat
 */
class MyGlobalPoint: public TVector3 {
   public:
        MyGlobalPoint();

        /**
         * \brief Constructor
         *
         * \param x  x component
         * \param y  y component
         * \param z  z component
         */
      	MyGlobalPoint(double x, double y, double z);

      	virtual ~MyGlobalPoint();

      	double Xerror() const;
      	double Yerror() const;
      	double Zerror() const;

	double phi() const;
	double eta() const;

        /**
         * \brief Get the length of the vector
         */
      	double value() const;

        /**
         * \brief Get the uncertainty of the point
         *
         * The covariances between the vector components are taken
         * into account.
         */
      	double error() const;

        /**
         * \brief Calculate the significance, i.e. value/error
         */
      	double significance() const;

        /**
         * \brief Calculate rotated error
         *
         * rotating the vector x,y,z so that z' = vector direction 
         * in result z error = error
         * First rotation +phi around z-axis, then rotation +theta around y-axis
         * (Rotating coordinates -> plus sign)
         */
      	double rotatedError() const;

        /**
         * \brief Calculate the significance with rotated error
         */
      	double rotatedSignificance() const;

      	MyGlobalPoint operator+(const MyGlobalPoint&) const;
      	MyGlobalPoint operator-(const MyGlobalPoint&) const;

      	TVector3	tvector3() const;

        double   dxx;  ///< Covariance matrix xx-component
        double   dxy;  ///< Covariance matrix xy-component
        double   dxz;  ///< Covariance matrix xz-component
        double   dyy;  ///< Covariance matrix yy-component
        double   dyz;  ///< Covariance matrix yz-component
        double   dzz;  ///< Covariance matrix zz-component

   private:

   ClassDef(MyGlobalPoint, MYEVENT_VERSION)
};
#endif
