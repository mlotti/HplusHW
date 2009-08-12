#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyVertex.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyJet.h"

using namespace std;

ClassImp(MyVertex)

MyVertex::MyVertex(): MyGlobalPoint(), parentJet(0) {}

MyVertex::MyVertex(double x, double y, double z): MyGlobalPoint(x, y, z), parentJet(0) {}

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

std::vector<MyTrack *> MyVertex::getAssocTracks() const {
    if(!parentJet) {
        std::cout << "Requesting associated tracks of a secondary vertex, but the pointer to the parent jet is null!" << std::endl;
        std::exit(0);
    }

    std::vector<MyTrack *> ret;
    ret.reserve(assocTrackIndices.size());

    std::vector<MyTrack *> tracks = parentJet->getTracks();
    for(std::vector<unsigned int>::const_iterator ind = assocTrackIndices.begin(); ind != assocTrackIndices.end(); ++ind) {
        ret.push_back(tracks[*ind]);
    }

    return ret;
}

void MyVertex::print(std::ostream& out) const {
    out << "    Vertex eta,phi,ntracks " << Eta() 
        << " " << Phi() << " " << assocTrackIndices.size() << endl;
}

