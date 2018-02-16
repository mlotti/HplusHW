/** \class TriggerSkim
 *
 *  
 *  Filter to select events for 
 *  tau+MET trigger tau-leg efficiency study
 *
 *  \author Sami Lehti  -  HIP Helsinki
 *
 */

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "FWCore/Framework/interface/LuminosityBlock.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include <iostream>
#include <regex>

class TriggerSkim : public edm::EDFilter {

    public:
        explicit TriggerSkim(const edm::ParameterSet&);
        ~TriggerSkim();

  	virtual bool filter(edm::Event&, const edm::EventSetup& );

   private:
	edm::EDGetTokenT<edm::TriggerResults> trgResultsToken;
	std::vector<std::string> triggerBits;

        edm::EDGetTokenT<GenEventInfoProduct> *genWeightToken;
        std::vector<edm::ParameterSet> genWeights;

        int nRead, nEvents, nSelectedEvents;
};

TriggerSkim::TriggerSkim(const edm::ParameterSet& iConfig)
: trgResultsToken(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("TriggerResults")))
{
    triggerBits        = iConfig.getParameter<std::vector<std::string> >("HLTPaths");

    nEvents         = 0;
    nSelectedEvents = 0;
}


TriggerSkim::~TriggerSkim(){
    double eff = 0;
    if(nEvents > 0) eff = ((double)nSelectedEvents)/((double) nEvents);
    std::cout << "TriggerSkim: " //  	edm::LogVerbatim("TriggerSkim") 
              << " Number_events_read     " << nRead
              << " Number_events_weighted " << nEvents
              << " Number_events_kept (w) " << nSelectedEvents
              << " Efficiency         " << eff << std::endl;
}


bool TriggerSkim::filter(edm::Event& iEvent, const edm::EventSetup& iSetup ){

    nRead++;
    
    int eventWeight = 1;
    for(size_t i = 0; i < genWeights.size(); ++i){
        edm::Handle<GenEventInfoProduct> handle;
        iEvent.getByToken(genWeightToken[i], handle);
        if(handle.isValid() && handle->weight() < 0) eventWeight = -1;
    }

    nEvents += eventWeight;

    // Trigger bits
    edm::Handle<edm::TriggerResults> trghandle;
    iEvent.getByToken(trgResultsToken,trghandle);
    if(trghandle.isValid()){
        edm::TriggerResults tr = *trghandle;
        bool fromPSetRegistry;
        edm::Service<edm::service::TriggerNamesService> tns;
        std::vector<std::string> hlNames; 
        tns->getTrigPaths(tr, hlNames, fromPSetRegistry);

	bool passed = false;
        for(size_t i = 0; i < triggerBits.size(); ++i){
	    std::regex hlt_re(triggerBits[i]);
	    int n = 0;
            for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
		if (std::regex_search(*j, hlt_re)) {
		    if(trghandle->accept(n)) {
			passed = true;
                        break;
		    }
                }
		n++;
            }
        }
	if(!passed) return false; 
    }

    nSelectedEvents += eventWeight;
    return true;
}

DEFINE_FWK_MODULE(TriggerSkim);   

