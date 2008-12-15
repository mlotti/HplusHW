#ifndef MYHIT_H
#define MYHIT_H

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyGlobalPoint.h"
#include "TROOT.h"
#include "TVector3.h"

class MyHit : public MyGlobalPoint {
    public:
  	MyHit();
  	virtual ~MyHit();

  	// public methods
	void print();

	// datafields
  	double theEstimate;           // Hit compatibility to trajectory measurement
  	int    theCompositeCount;     // Number of hits for composite hits  // INSERT

	int    trackAssociationLabel; // For associating the hit to the correct track

    private:

  	ClassDef(MyHit,1) // The macro
};
#endif
