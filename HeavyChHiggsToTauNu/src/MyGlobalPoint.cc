#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyGlobalPoint.h"

double phifun(double,double);
double etafun(double,double,double);

ClassImp(MyGlobalPoint)

MyGlobalPoint::MyGlobalPoint(){}
MyGlobalPoint::MyGlobalPoint(double xx,double yy,double zz){
	x = xx;
	y = yy;
	z = zz;
}
MyGlobalPoint::~MyGlobalPoint(){}

double MyGlobalPoint::getX() const { return x; }
double MyGlobalPoint::getY() const { return y; }
double MyGlobalPoint::getZ() const { return z; }

double MyGlobalPoint::getXerror() const { return sqrt(dxx); }
double MyGlobalPoint::getYerror() const { return sqrt(dyy); }
double MyGlobalPoint::getZerror() const { return sqrt(dzz); }

double MyGlobalPoint::DValue(double xx, double yy, double zz) const {

    double dvalue = 0;

    switch(dimension){
        case 1:  dvalue = zz; break;
        case 2:  dvalue = sqrt(xx*xx + yy*yy); break;
        //case 3:  dvalue = sqrt(xx*xx + yy*yy + zz*zz); break; 
        default: dvalue = sqrt(xx*xx + yy*yy + zz*zz); break;
    }
    return dvalue;
}

double MyGlobalPoint::value() const { return DValue(getX(),getY(),getZ());}
double MyGlobalPoint::error() const { return DValue(getXerror(),getYerror(),getZerror());}

#include "TMatrix.h"

double MyGlobalPoint::rotatedError() const {
    // rotating the vector x,y,z so that z' = vector direction 
    // in result z error = error
    // First rotation +phi around z-axis, then rotation +theta around y-axis
    // (Rotating coordinates -> plus sign)

    double T = sqrt(x*x + y*y);
    double R = sqrt(T*T + z*z);

    TMatrix rotationMatrix(3,3);
    rotationMatrix(0,0) = x*z/(R*T);
    rotationMatrix(0,1) = -y/T;
    rotationMatrix(0,2) = x/R;
    rotationMatrix(1,0) = y*z/(R*T);
    rotationMatrix(1,1) = x/T;
    rotationMatrix(1,2) = y/R;
    rotationMatrix(2,0) = -T/R;
    rotationMatrix(2,1) = 0;
    rotationMatrix(2,2) = z/R;

    TMatrix errorMatrix(3,3);
    errorMatrix(0,0) = dxx;
    errorMatrix(0,1) = dxy;
    errorMatrix(0,2) = dxz;
    errorMatrix(1,0) = errorMatrix(0,1);
    errorMatrix(1,1) = dyy;
    errorMatrix(1,2) = dyz;
    errorMatrix(2,0) = errorMatrix(0,2);
    errorMatrix(2,1) = errorMatrix(1,2);
    errorMatrix(2,2) = dzz;

    TMatrix rotatedMatrix = rotationMatrix;
    rotatedMatrix *= errorMatrix;
    rotatedMatrix *= TMatrix(TMatrix::kTransposed,rotationMatrix);

    return rotatedMatrix(2,2);
}

double MyGlobalPoint::rotatedSignificance() const {
    double significance = 0;
    if(rotatedError() != 0) significance = value()/rotatedError();
    return significance;
}

double MyGlobalPoint::significance() const {  
    double significance = 0;
    if(error() != 0) significance = value()/error();
    return significance;
}

double MyGlobalPoint::getPhi() const {
    return Phi();
}

double MyGlobalPoint::Phi() const {
    return phifun(getX(),getY());
}

double MyGlobalPoint::phi() const {
    return Phi();
}

double MyGlobalPoint::Eta() const {
    return etafun(getX(),getY(),getZ());
}

double MyGlobalPoint::eta() const {
	return Eta();
}

double MyGlobalPoint::getEta() const {
        return Eta();
}


void MyGlobalPoint::use(string D){ 
    dimension = 0;
    if(D == "2D")            dimension = 2;
    if(D == "3D")            dimension = 3;
    if(D == "z" || D == "Z") dimension = 1;
}

MyGlobalPoint MyGlobalPoint::operator + (const MyGlobalPoint& q) const {
    MyGlobalPoint point;
    point.x = x + q.getX();
    point.y = y + q.getY();
    point.z = z + q.getZ();

    point.dxx = dxx + q.dxx;
    point.dxy = dxy + q.dxy;
    point.dxz = dxz + q.dxz;
    point.dyy = dyy + q.dyy;
    point.dyz = dyz + q.dyz;
    point.dzz = dzz + q.dzz;

    return point;
}

MyGlobalPoint MyGlobalPoint::operator - (const MyGlobalPoint& q) const {
    MyGlobalPoint point;
    point.x = x - q.getX();
    point.y = y - q.getY();
    point.z = z - q.getZ();

    point.dxx = dxx + q.dxx;
    point.dxy = dxy + q.dxy;
    point.dxz = dxz + q.dxz;
    point.dyy = dyy + q.dyy;
    point.dyz = dyz + q.dyz;
    point.dzz = dzz + q.dzz;

    return point;
}

TVector3 MyGlobalPoint::tvector3(){
	return TVector3(x,y,z);
}
