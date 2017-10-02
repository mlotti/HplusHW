#ifndef EventInfoDumper_h
#define EventInfoDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "DataFormats/Scalers/interface/LumiScalers.h"
#include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"
#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"

#include <string>
#include <vector>

#include "TTree.h"

namespace reco {
  class Vertex;
}

class PileupSummaryInfo;

class EventInfoDumper {
    public:
	EventInfoDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset);
	~EventInfoDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
        bool filter();

	// For Secondary Vertex Collection
	Measurement1D vertexD3d(const reco::VertexCompositePtrCandidate &svcand, const reco::Vertex &pv) const;
        Measurement1D vertexDxy(const reco::VertexCompositePtrCandidate &svcand, const reco::Vertex &pv) const;
        float vertexDdotP(const reco::VertexCompositePtrCandidate &sv, const reco::Vertex &pv) const;

        edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puSummaryToken;
        edm::EDGetTokenT<std::vector<LumiScalers> > instLumiToken;
        edm::EDGetTokenT<LHEEventProduct> lheToken;
        edm::EDGetTokenT<edm::View<reco::Vertex> > vertexToken;
        edm::EDGetTokenT<double> topPtToken;
	edm::EDGetTokenT<edm::View<reco::VertexCompositePtrCandidate> > secvertexToken;
	
	unsigned long long event;
	unsigned int run,lumi;
	float instLumi;
        float prescale;
	short nPU;
	short NUP;
	short nGoodOfflinePV;
        float pvX;
        float pvY;
        float pvZ;
        float distanceToNextPV;
        float distanceToClosestPV;
        float ptSumRatio; // Ratio of track pt sum of first and second vertex
        float topPtWeight; // Weight produced by TopPtProducer

	bool bookLumiScalers;
	bool bookTopPt;

	// Secondary Vertex Collection
	float svPt;
        float svEta;
        float svPhi;
        float svMass;
        int   svNTks;
        float svChi2;
	/* Number of degrees of freedom (Ndof):
           Meant to be Double32_t for soft-assignment fitters:
           tracks may contribute to the vertex with fractional weights.
           The ndof is then = to the sum of the track weights.
           see e.g. CMS NOTE-2006/032, CMS NOTE-2004/002
	*/
        float svNdof;
        float svDxy;
        float svDxyErr;
        float svD3d;
        float svD3dErr;
        float costhetasvpv;
};
#endif
