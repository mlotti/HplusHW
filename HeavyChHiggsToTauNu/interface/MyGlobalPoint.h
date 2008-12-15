#ifndef MY_GLOBALPOINT
#define MY_GLOBALPOINT

namespace std{}
using namespace std;

#include "TROOT.h"
#include "TVector3.h"
#include <string>
#include <math.h>

class MyGlobalPoint {
   public:
        MyGlobalPoint();
      	MyGlobalPoint(double,double,double);
      	virtual ~MyGlobalPoint();

      	double 	getX() const;
      	double  getY() const;
      	double  getZ() const;

      	double  getXerror() const;
      	double  getYerror() const;
      	double  getZerror() const;

      	double	value() const;
      	double 	error() const;
      	double	significance() const;

      	double 	getPhi() const;
	double 	Phi() const;
	double 	phi() const;

	double getEta() const;
	double Eta() const;
	double eta() const;

      	double    rotatedError() const;
      	double    rotatedSignificance() const;

      	void	use(string D); // values = "2D","3D","Z"

      	MyGlobalPoint operator + (const MyGlobalPoint&) const;
      	MyGlobalPoint operator - (const MyGlobalPoint&) const;

      	TVector3	tvector3();

      	double 	x,
		y,
		z,
		dxx,
		dxy,
		dxz,
		dyy,
		dyz,
		dzz;

      	string    name;

   private:
      	double    DValue(double xx, double yy, double zz) const;
      	int       dimension;

   ClassDef(MyGlobalPoint,1)
};
#endif
