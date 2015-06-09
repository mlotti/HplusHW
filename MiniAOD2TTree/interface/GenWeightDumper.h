#ifndef GenWeightDumper_h
#define GenWeightDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

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
	GenWeightDumper(std::vector<edm::ParameterSet>);
	~GenWeightDumper();

	void book(TTree*);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:
	bool filter();
        bool useFilter;
	bool booked;

	std::vector<edm::ParameterSet> inputCollections;
	edm::Handle<GenEventInfoProduct> *handle;

        double GenWeight;

};
#endif
