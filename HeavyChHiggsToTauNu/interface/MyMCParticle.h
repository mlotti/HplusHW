#ifndef MY_MCPARTICLE
#define MY_MCPARTICLE

#include "TROOT.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyTrack.h"
#include <vector>

using namespace std;

class MyMCParticle : public MyTrack {
    public:
        MyMCParticle();
	MyMCParticle(double,double,double,double);
        virtual ~MyMCParticle();
/*
        MyGlobalPoint GetMCVertex() const;
        MyGlobalPoint GetImpactParameter() const;
*/
	int         pid;
	int 	    status;
	int	    barcode;
        vector<int> mother;
	inline vector<int>::const_iterator mother_begin() const { return mother.begin();}
        inline vector<int>::const_iterator mother_end() const { return mother.end();}

	vector<int> motherBarcodes;
        inline vector<int>::const_iterator motherBarcodes_begin() const { return motherBarcodes.begin();}
        inline vector<int>::const_iterator motherBarcodes_end() const { return motherBarcodes.end();}

    ClassDef(MyMCParticle,1)
};
#endif
