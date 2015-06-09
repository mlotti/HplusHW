/** \class SignalAnalysisSkim
 *
 *  
 *  Filter to select events for 
 *  tau+MET trigger MET-leg efficiency study
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

#include "FWCore/Framework/interface/TriggerNamesService.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

#include "FWCore/Framework/interface/LuminosityBlock.h"

#include <iostream>
#include <regex>

class SignalAnalysisSkim : public edm::EDFilter {

    public:
        explicit SignalAnalysisSkim(const edm::ParameterSet&);
        ~SignalAnalysisSkim();

  	virtual bool filter(edm::Event&, const edm::EventSetup& );

   private:
	edm::InputTag triggerResults;
	std::vector<std::string> triggerBits;

        edm::InputTag	jetCollection;

        std::vector<std::string> jetUserFloats;

	double jetEtCut,jetEtaCut;
	int nJets;

        int nEvents, nSelectedEvents;
};

SignalAnalysisSkim::SignalAnalysisSkim(const edm::ParameterSet& iConfig) {
    triggerResults     = iConfig.getParameter<edm::InputTag>("TriggerResults");
    triggerBits        = iConfig.getParameter<std::vector<std::string> >("HLTPaths");

    jetCollection      = iConfig.getParameter<edm::InputTag>("JetCollection");
    jetUserFloats      = iConfig.getParameter<std::vector<std::string> >("JetUserFloats");

    jetEtCut           = iConfig.getParameter<double>("JetEtCut");
    jetEtaCut          = iConfig.getParameter<double>("JetEtaCut");                            
    nJets              = iConfig.getParameter<int>("NJets");

    nEvents         = 0;
    nSelectedEvents = 0;
}


SignalAnalysisSkim::~SignalAnalysisSkim(){
    std::cout << "SignalAnalysisSkim: " //  	edm::LogVerbatim("SignalAnalysisSkim") 
              << " Number_events_read " << nEvents
              << " Number_events_kept " << nSelectedEvents
              << " Efficiency         " << ((double)nSelectedEvents)/((double) nEvents) << std::endl;
}


bool SignalAnalysisSkim::filter(edm::Event& iEvent, const edm::EventSetup& iSetup ){

    nEvents++;

    // Trigger bits
    edm::Handle<edm::TriggerResults> trghandle;
    iEvent.getByLabel(triggerResults,trghandle);
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
	    bool trgBitFound = false;
            for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
		if (std::regex_search(*j, hlt_re)) {
		    trgBitFound = true;
		    if(trghandle->accept(n)) {
			passed = true;
                        break;
		    }
                }
		n++;
            }
	    if(!trgBitFound) {
		std::cout << "Skimming with " << triggerBits[i] << ", but trigger not found" << std::endl;
		for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
		    std::cout << "    " << *j << std::endl;
		}
		exit(1);
	    }
        }

	if(!passed) return false; 
    }

    edm::Handle<edm::View<pat::Jet> > jethandle;
    iEvent.getByLabel(jetCollection, jethandle);
    int njets = 0;
    if(jethandle.isValid()){
        for(size_t i=0; i<jethandle->size(); ++i) {
            const pat::Jet& obj = jethandle->at(i);

	    if(obj.p4().pt() < jetEtCut) continue;
	    if(fabs(obj.p4().eta()) > jetEtaCut) continue;
/*
	    bool passed = true;
	    for(size_t j = 0; j < jetUserFloats.size(); ++j){
		if(obj.userFloat(jetUserFloats[j]) < 0) {
		    passed = false;
		    break;
		}
	    }
	    if(!passed) continue;
*/
	    njets++;
	}
    }
    if(njets < nJets) return false;

    nSelectedEvents++;
    return true;
}

DEFINE_FWK_MODULE(SignalAnalysisSkim);   

