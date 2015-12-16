/** \class TauLegSkim
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

class TauLegSkim : public edm::EDFilter {

    public:
        explicit TauLegSkim(const edm::ParameterSet&);
        ~TauLegSkim();

  	virtual bool filter(edm::Event&, const edm::EventSetup& );

   private:
	edm::EDGetTokenT<edm::TriggerResults> trgResultsToken;
	std::vector<std::string> triggerBits;

        edm::EDGetTokenT<edm::View<pat::Tau>> tauToken;
        edm::EDGetTokenT<edm::View<pat::Muon>> muonToken;

        edm::EDGetTokenT<GenEventInfoProduct> *genWeightToken;
        std::vector<edm::ParameterSet> genWeights;

        std::vector<std::string> tauDiscriminators;
        std::vector<std::string> muonDiscriminators;

	double tauPtCut,tauEtaCut;
	double muonPtCut,muonEtaCut;

        int nRead, nEvents, nSelectedEvents;
};

TauLegSkim::TauLegSkim(const edm::ParameterSet& iConfig)
: trgResultsToken(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("TriggerResults"))),
  tauToken(consumes<edm::View<pat::Tau>>(iConfig.getParameter<edm::InputTag>("TauCollection"))),
  muonToken(consumes<edm::View<pat::Muon>>(iConfig.getParameter<edm::InputTag>("MuonCollection")))
{
    triggerBits        = iConfig.getParameter<std::vector<std::string> >("HLTPaths");

    tauDiscriminators  = iConfig.getParameter<std::vector<std::string> >("TauDiscriminators");
    muonDiscriminators = iConfig.getParameter<std::vector<std::string> >("MuonDiscriminators");

    tauPtCut           = iConfig.getParameter<double>("TauPtCut");
    tauEtaCut          = iConfig.getParameter<double>("TauEtaCut");                            

    muonPtCut          = iConfig.getParameter<double>("MuonPtCut");                            
    muonPtCut          = iConfig.getParameter<double>("MuonEtaCut");                            

    genWeights = iConfig.getParameter<std::vector<edm::ParameterSet> >("GenWeights");
    genWeightToken = new edm::EDGetTokenT<GenEventInfoProduct>[genWeights.size()];

    for(size_t i = 0; i < genWeights.size(); ++i){
      edm::InputTag inputtag = genWeights[i].getParameter<edm::InputTag>("src");
      genWeightToken[i] = consumesCollector().consumes<GenEventInfoProduct>(inputtag);
    }

    nEvents         = 0;
    nSelectedEvents = 0;
}


TauLegSkim::~TauLegSkim(){
    double eff = 0;
    if(nEvents > 0) eff = ((double)nSelectedEvents)/((double) nEvents);
    std::cout << "TauLegSkim: " //  	edm::LogVerbatim("TauLegSkim") 
              << " Number_events_read     " << nRead
              << " Number_events_weighted " << nEvents
              << " Number_events_kept (w) " << nSelectedEvents
              << " Efficiency         " << eff << std::endl;
}


bool TauLegSkim::filter(edm::Event& iEvent, const edm::EventSetup& iSetup ){

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

    // Tau
    std::vector<pat::Tau> selectedTaus;
    edm::Handle<edm::View<pat::Tau> > tauhandle;
    iEvent.getByToken(tauToken, tauhandle);
    if(tauhandle.isValid()){
        for(size_t i=0; i<tauhandle->size(); ++i) {
            const pat::Tau& tau = tauhandle->at(i);
	    if(tau.p4().pt() < tauPtCut) continue;
	    if(abs(tau.p4().eta()) > tauEtaCut) continue;
	    bool d = true;
	    for(size_t j=0; j<tauDiscriminators.size(); ++j) {
		d = d && tau.tauID(tauDiscriminators[j]);
	    }
	    if(!d) continue;
	    selectedTaus.push_back(tau);
	}
    }
    if(selectedTaus.size() == 0) return false;

    // Muon
    std::vector<pat::Muon> selectedMuons;
    edm::Handle<edm::View<pat::Muon> > muonhandle;
    iEvent.getByToken(muonToken, muonhandle);
    if(muonhandle.isValid()){
        for(size_t i=0; i<muonhandle->size(); ++i) {
            const pat::Muon& muon = muonhandle->at(i);
            if(muon.p4().pt() < muonPtCut) continue;
            if(abs(muon.p4().eta()) > muonEtaCut) continue;
	    selectedMuons.push_back(muon);
        }
    }
    if(selectedMuons.size() == 0) return false;
/*
    double muTauInvMass = (selectedMuons[0].p4() + selectedTaus[0].p4()).M();
std::cout << "check muTauInvMass " << muTauInvMass << std::endl;
    if(muTauInvMass < 70) return false;
*/
    nSelectedEvents += eventWeight;
    return true;
}

DEFINE_FWK_MODULE(TauLegSkim);   

