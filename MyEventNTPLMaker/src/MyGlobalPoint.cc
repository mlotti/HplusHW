#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyGlobalPoint.h"

#include "TMatrix.h"

#include<cmath>
#include<iostream>

ClassImp(MyGlobalPoint)

MyGlobalPoint::MyGlobalPoint(): TVector3(0,0,0), dxx(0), dxy(0), dxz(0), dyy(0), dyz(0), dzz(0) {}
MyGlobalPoint::MyGlobalPoint(double x, double y, double z): TVector3(x, y, z), dxx(0), dxy(0), dxz(0), dyy(0), dyz(0), dzz(0) {}

MyGlobalPoint::~MyGlobalPoint(){}

double MyGlobalPoint::Xerror() const { return sqrt(dxx); }
double MyGlobalPoint::Yerror() const { return sqrt(dyy); }
double MyGlobalPoint::Zerror() const { return sqrt(dzz); }

double MyGlobalPoint::value() const { return Mag(); }
double MyGlobalPoint::error() const { return sqrt(dxx + 2*dxy + 2*dxz + dyy + 2*dyz + dzz); } // FIXME: the formula is still wrong

double MyGlobalPoint::rotatedError() const {
    // rotating the vector x,y,z so that z' = vector direction 
    // in result z error = error
    // First rotation +phi around z-axis, then rotation +theta around y-axis
    // (Rotating coordinates -> plus sign)

    double x = X();
    double y = Y();
    double z = Z();

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
    double e = rotatedError();
    if(std::abs(e) > 0) significance = value()/e;
    return significance;
}

double MyGlobalPoint::significance() const {  
    double significance = 0;
    double e = error();
    if(std::abs(e) > 0) significance = value()/e;
    return significance;
}

double MyGlobalPoint::phi() const {
    return Phi();
}

double MyGlobalPoint::eta() const {
    return Eta();
}

MyGlobalPoint MyGlobalPoint::operator+(const MyGlobalPoint& q) const {
    MyGlobalPoint point(*this);
    point += q; // exploit TVector3::operator+=(TVector3&)

    point.dxx += q.dxx;
    point.dxy += q.dxy;
    point.dxz += q.dxz;
    point.dyy += q.dyy;
    point.dyz += q.dyz;
    point.dzz += q.dzz;

    return point;
}

MyGlobalPoint MyGlobalPoint::operator-(const MyGlobalPoint& q) const {
    MyGlobalPoint point(*this);
    point -= q; // exploit TVector3::operator-=(TVector3&)

    point.dxx = dxx + q.dxx;
    point.dxy = dxy + q.dxy;
    point.dxz = dxz + q.dxz;
    point.dyy = dyy + q.dyy;
    point.dyz = dyz + q.dyz;
    point.dzz = dzz + q.dzz;

    return point;
}

TVector3 MyGlobalPoint::tvector3() const {
    return TVector3(X(), Y(), Z());
}
