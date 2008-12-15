#ifndef MYVERTEX
#define MYVERTEX

using namespace std;

#include "TROOT.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyTrack.h"
#include <vector>

class MyVertex : public MyGlobalPoint {
    public:
    	MyVertex();
	MyVertex(double,double,double);
    	virtual ~MyVertex();

    	double   Eta() const;
    	double   Phi() const;

    	double   eta() const;
    	double   phi() const;

    	MyVertex operator + (const MyVertex&) const;
    	MyVertex operator - (const MyVertex&) const;

    	vector<MyTrack> assocTracks;
	inline vector<MyTrack>::const_iterator assocTracks_begin() const { return assocTracks.begin(); }
        inline vector<MyTrack>::const_iterator assocTracks_end() const { return assocTracks.end(); }

	void print() const;

    	ClassDef(MyVertex,1)
};
#endif
