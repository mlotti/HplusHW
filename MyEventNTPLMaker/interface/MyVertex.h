#ifndef __MyVertex__
#define __MyVertex__

#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyTrack.h"
#include "HiggsAnalysis/MyEventNTPLMaker/interface/MyEventVersion.h"
#include <vector>

#include<iostream>

// Forward declare MyJet in order to avoid circular dependency
class MyJet;

/**
 * \brief Vertex class for MyEvent dataformat
 */
class MyVertex: public MyGlobalPoint {
    public:
    	MyVertex();

        /**
         * \brief Constructor
         *
         * \param x  x component
         * \param y  y component
         * \param z  z component
         */
	MyVertex(double x, double y, double z);

    	virtual ~MyVertex();

    	double   eta() const;
    	double   phi() const;

    	MyVertex operator+(const MyVertex&) const;
    	MyVertex operator-(const MyVertex&) const;

        void print(std::ostream& out = std::cout) const;

        
        /**
         * \brief Indices to track collection in the parent jet
         */
        std::vector<unsigned int> assocTrackIndices;


    private:
    	ClassDef(MyVertex, MYEVENT_VERSION)
};
#endif
