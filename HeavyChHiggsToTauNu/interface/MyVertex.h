#ifndef __MyVertex__
#define __MyVertex__

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyTrack.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MyEventVersion.h"
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

        /**
         * \brief Get associated tracks
         */
        std::vector<MyTrack *> getAssocTracks() const;

        void print(std::ostream& out = std::cout) const;

        
        /**
         * \brief Pointer to parent jet
         *
         * ROOT is (or at least should be) able to serialize the
         * pointer to the parent jet correctly.
         */
        MyJet *parentJet;

        /**
         * \brief Indices to track collection in the parent jet
         *
         * \see parentJet
         */
        std::vector<unsigned int> assocTrackIndices;


    private:
    	ClassDef(MyVertex, MYEVENT_VERSION)
};
#endif
