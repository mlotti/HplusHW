#ifndef SoftBTagDumper_h
#define SoftBTagDumper_h

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

class SoftBTagDumper {
    public:
	SoftBTagDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset);
	~SoftBTagDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
        bool filter();

	// For Secondary Vertex Collection
	Measurement1D vertexD3d(const reco::VertexCompositePtrCandidate &svcand, const reco::Vertex &pv) const;
        Measurement1D vertexDxy(const reco::VertexCompositePtrCandidate &svcand, const reco::Vertex &pv) const;
        float vertexDdotP(const reco::VertexCompositePtrCandidate &sv, const reco::Vertex &pv) const;

        edm::EDGetTokenT<edm::View<reco::Vertex> > primaryVertexToken;
	edm::EDGetTokenT<edm::View<reco::VertexCompositePtrCandidate> > secondaryVertexToken;
	
	// Primary and Secondary Vertex Collections
	short nGoodOfflinePV;
	short nGoodOfflineSV;
	std::vector<float> *svPt;
	std::vector<float> *svEta;
	std::vector<float> *svPhi;
	std::vector<float> *svMass;
	std::vector<int>   *svNTks;
	std::vector<float> *svChi2;
	/* Number of degrees of freedom (Ndof):
           Meant to be Double32_t for soft-assignment fitters:
           tracks may contribute to the vertex with fractional weights.
           The ndof is then = to the sum of the track weights.
           see e.g. CMS NOTE-2006/032, CMS NOTE-2004/002
	*/
	std::vector<float> *svNdof;
	std::vector<float> *svDxy;
	std::vector<float> *svDxyErr;
	std::vector<float> *svD3d;
	std::vector<float> *svD3dErr;
	std::vector<float> *costhetasvpv;
};
#endif
