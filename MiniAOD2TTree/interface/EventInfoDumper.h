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

        edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puSummaryToken;
        edm::EDGetTokenT<LHEEventProduct> lheToken;
        edm::EDGetTokenT<edm::View<reco::Vertex> > vertexToken;
        
	unsigned long long event;
	unsigned int run,lumi;
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

};
#endif
