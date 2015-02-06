#ifndef EventInfoDumper_h
#define EventInfoDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include <string>
#include <vector>

#include "TTree.h"

class EventInfoDumper {
    public:
	EventInfoDumper(edm::ParameterSet&);
	~EventInfoDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
        bool filter();

	int event,run,lumi;
	int nPU;
	int NUP;
	int nGoodOfflinePV;

        edm::InputTag pileupSummaryInfoSrc;
//	edm::InputTag lheSrc;
	edm::InputTag offlinePrimaryVertexSrc;
};
#endif
