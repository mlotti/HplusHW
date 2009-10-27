#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyVertex.h"

#include <iostream>
using namespace std;

double etafun(double,double,double);
double phifun(double,double);

ClassImp(MyVertex)

MyVertex::MyVertex(){
        x = 0;
        y = 0;
        z = 0;
        dxx = 0;
        dxy = 0;
        dxz = 0;
        dyy = 0;
        dyz = 0;
        dzz = 0;
        use("3D");
}

MyVertex::MyVertex(double xx,double yy,double zz){
        x = xx;
        y = yy;
        z = zz;
        dxx = 0;
        dxy = 0;
        dxz = 0;
        dyy = 0;
        dyz = 0;
        dzz = 0;
        use("3D");
}


MyVertex::~MyVertex(){}

double MyVertex::Eta() const {
    return etafun(x,y,z);
}

double MyVertex::Phi() const {
    return phifun(x,y);
}

double MyVertex::eta() const {
    return Eta();
}

double MyVertex::phi() const {
    return Phi();
}

MyVertex MyVertex::operator + (const MyVertex& q) const {
    MyVertex point;
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

MyVertex MyVertex::operator - (const MyVertex& q) const {
    MyVertex point;
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

void MyVertex::print() const {
	cout << "    Vertex eta,phi,ntracks " << this->Eta() 
             << " " << this->Phi() << " " << assocTracks.size() << endl;
}

