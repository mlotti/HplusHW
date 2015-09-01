#ifndef GenWeightDumper_h
#define GenWeightDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/GenMET.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include <string>
#include <vector>

#include "TTree.h"
#include "DataFormats/Math/interface/LorentzVector.h"


class GenWeightDumper {
    public:
	GenWeightDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet> psets);
	~GenWeightDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
	bool filter();
        bool useFilter;
	bool booked;

	std::vector<edm::ParameterSet> inputCollections;
	edm::EDGetTokenT<GenEventInfoProduct> *token;

        double GenWeight;
};
#endif
