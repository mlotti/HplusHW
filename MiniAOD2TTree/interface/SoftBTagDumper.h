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

#include "HiggsAnalysis/MiniAOD2TTree/interface/BaseDumper.h"

#include <string>
#include <vector>

#include "TTree.h"

namespace reco {
  class Vertex;
}


class SoftBTagDumper : public BaseDumper {
    public:
	SoftBTagDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets);
	~SoftBTagDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
	//        bool filter();

	// For Secondary Vertex Collection
	Measurement1D vertexD3d(const reco::VertexCompositePtrCandidate &svcand, const reco::Vertex &pv) const;
        Measurement1D vertexDxy(const reco::VertexCompositePtrCandidate &svcand, const reco::Vertex &pv) const;
        double vertexDdotP(const reco::VertexCompositePtrCandidate &sv, const reco::Vertex &pv) const;

        edm::EDGetTokenT<edm::View<reco::Vertex> > *primaryVertexToken;
	edm::EDGetTokenT<edm::View<reco::VertexCompositePtrCandidate> > *secondaryVertexToken;
	
	// Primary and Secondary Vertex Collections
	short nGoodOfflinePV;
	short nGoodOfflineSV;
	std::vector<double> *svPt;
	std::vector<double> *svEta;
	std::vector<double> *svPhi;
	std::vector<double> *svMass;
	std::vector<int>   *svNTks;
	std::vector<double> *svChi2;
	/* Number of degrees of freedom (Ndof):
           Meant to be Double32_t for soft-assignment fitters:
           tracks may contribute to the vertex with fractional weights.
           The ndof is then = to the sum of the track weights.
           see e.g. CMS NOTE-2006/032, CMS NOTE-2004/002
	*/
	std::vector<double> *svNdof;
	std::vector<double> *svDxy;
	std::vector<double> *svDxyErr;
	std::vector<double> *svD3d;
	std::vector<double> *svD3dErr;
	std::vector<double> *costhetasvpv;
};


#endif
