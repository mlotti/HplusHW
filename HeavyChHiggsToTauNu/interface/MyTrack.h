#ifndef MY_TRACK
#define MY_TRACK

#include "TROOT.h"
#include "TLorentzVector.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyGlobalPoint.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyImpactParameter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyHit.h" // LAW 11.02.08

#include <vector>

class MyTrack : public TLorentzVector {
   public:
      	MyTrack();
        MyTrack(double,double,double,double);
	MyTrack(const MyTrack&);
      	virtual ~MyTrack();

      	double   pt()  const;
      	double   eta() const;
      	double   phi() const;

      	double   px()  const;
      	double   py()  const;
      	double   pz()  const;
	double   p()   const;

        TLorentzVector p4() const;
	void setP4(TLorentzVector&);

	double charge() const;
	double normalizedChi2() const;
	double numberOfValidHits() const;
        double pfType() const;

	MyImpactParameter impactParameter() const;

        MyGlobalPoint ecalHitPoint() const;

//	inline vector<MyHit>::const_iterator hits_begin() const { return hits.begin(); }
//	inline vector<MyHit>::const_iterator hits_end() const { return hits.end(); }

      	double  trackCharge, 
        	chiSquared,
        	nHits,
        	nPixHits,
		particleType; // for PF tracks: X=0,h=1,e=2,mu=3,gamma=4,h0=5

	MyImpactParameter ip;

        MyGlobalPoint trackEcalHitPoint;

//        vector<MyHit> hits; // Hit information of track // LAW 11.02.08

	void print() const;

   ClassDef(MyTrack,1)
};
#endif
