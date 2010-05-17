#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyVertex.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyJet.h"

using namespace std;

ClassImp(MyVertex)

MyVertex::MyVertex(): MyGlobalPoint() {}

MyVertex::MyVertex(double x, double y, double z): MyGlobalPoint(x, y, z) {}

MyVertex::~MyVertex(){}

double MyVertex::eta() const {
    return Eta();
}

double MyVertex::phi() const {
    return Phi();
}

MyVertex MyVertex::operator+(const MyVertex& q) const {
    MyVertex point(*this);
    point += q; // exploit TVector3::operator+=(TVector3&)

    point.dxx += q.dxx;
    point.dxy += q.dxy;
    point.dxz += q.dxz;
    point.dyy += q.dyy;
    point.dyz += q.dyz;
    point.dzz += q.dzz;

    return point;
}

MyVertex MyVertex::operator-(const MyVertex& q) const {
    MyVertex point(*this);
    point -= q; // exploit TVector3::operator-=(TVector3&)

    point.dxx += q.dxx;
    point.dxy += q.dxy;
    point.dxz += q.dxz;
    point.dyy += q.dyy;
    point.dyz += q.dyz;
    point.dzz += q.dzz;

    return point;
}

void MyVertex::print(std::ostream& out) const {
    out << "    Vertex eta,phi,ntracks " << Eta() 
        << " " << Phi() << " " << assocTrackIndices.size() << endl;
}

