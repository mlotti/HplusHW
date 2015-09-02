#ifndef SkimDumper_h
#define SkimDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Common/interface/MergeableCounter.h"

#include <string>
#include <vector>
#include <iostream>

#include "TH1F.h"

//#include "FWCore/ServiceRegistry/interface/Service.h"
//#include "FWCore/Framework/interface/TriggerNamesService.h"

class SkimDumper {
    public:
	SkimDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset);
	~SkimDumper();

	void book();
	bool fill(const edm::LuminosityBlock&,const edm::EventSetup&);
	void reset();
	TH1F* getCounter();


    private:
	bool booked;

	edm::ParameterSet inputCollection;
        edm::EDGetTokenT<edm::MergeableCounter>* token;
	//std::vector<edm::InputTag> tags;

	TH1F* hCounter;
};
#endif
