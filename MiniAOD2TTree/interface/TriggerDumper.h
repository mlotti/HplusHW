#ifndef TriggerDumper_h
#define TriggerDumper_h

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include <string>
#include <vector>

#include "TTree.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"


class TriggerDumper {
    public:
	TriggerDumper(edm::ConsumesCollector&& iConsumesCollector, const edm::ParameterSet& pset);
	~TriggerDumper();

	void book(TTree*);
        void book(const edm::Run&,HLTConfigProvider);
	bool fill(edm::Event&, const edm::EventSetup&);
	void reset();

    private:

        bool filter();
	bool useFilter;
	bool booked;

	TTree* theTree;

	bool *iBit; 
	edm::ParameterSet inputCollection;
	edm::EDGetTokenT<edm::TriggerResults> trgResultsToken;
        edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> trgObjectsToken;
        edm::EDGetTokenT<std::vector<l1extra::L1EtMissParticle>> trgL1ETMToken;
	std::vector<std::string> triggerBits;

	double L1MET_x;
        double L1MET_y;
	double HLTMET_x;
	double HLTMET_y;

        std::vector<double> HLTTau_pt;
        std::vector<double> HLTTau_eta;
        std::vector<double> HLTTau_phi;
        std::vector<double> HLTTau_e;
};
#endif
