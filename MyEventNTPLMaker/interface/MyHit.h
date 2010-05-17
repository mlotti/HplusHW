#ifndef __MyHit__
#define __MyHit__

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyGlobalPoint.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEventVersion.h"

#include<iostream>

/**
 * \brief Tracker hit class for MyEvent dataformat
 */
class MyHit: public MyGlobalPoint {
    public:
  	MyHit();
  	virtual ~MyHit();

  	// public methods
  	void print(std::ostream& out = std::cout) const;

	// datafields
  	double theEstimate;           ///< Hit compatibility to trajectory measurement
  	int    theCompositeCount;     ///< Number of hits for composite hits  // INSERT

	int    trackAssociationLabel; ///< For associating the hit to the correct track

    private:
  	ClassDef(MyHit, MYEVENT_VERSION) // The macro
};
#endif
