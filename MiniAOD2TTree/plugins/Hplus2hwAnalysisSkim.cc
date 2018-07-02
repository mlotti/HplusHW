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

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "FWCore/Framework/interface/LuminosityBlock.h"

#include <iostream>
#include <regex>

class Hplus2hwAnalysisSkim : public edm::EDFilter {

    public:
        explicit Hplus2hwAnalysisSkim(const edm::ParameterSet&);
        ~Hplus2hwAnalysisSkim();

        virtual bool filter(edm::Event&, const edm::EventSetup& );

   private:
//	edm::EDGetTokenT<edm::TriggerResults> trgResultsToken;
//        std::vector<std::string> triggerBits;

        edm::EDGetTokenT<edm::View<pat::Jet>> jetToken;

        edm::EDGetTokenT<edm::View<pat::Tau>> tauToken;
	const int nTaus;
	
	edm::EDGetTokenT<edm::View<pat::MET>> metToken;

	edm::EDGetTokenT<edm::View<pat::Muon>> muonToken;
	const int nMuons;

        int nEvents;
        int nSelectedEvents;
};

Hplus2hwAnalysisSkim::Hplus2hwAnalysisSkim(const edm::ParameterSet& iConfig)
:// trgResultsToken(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("TriggerResults"))),
 // triggerBits(iConfig.getParameter<std::vector<std::string> >("HLTPaths")),
  jetToken(consumes<edm::View<pat::Jet>>(iConfig.getParameter<edm::InputTag>("JetCollection"))),
  tauToken(consumes<edm::View<pat::Tau>>(iConfig.getParameter<edm::InputTag>("TauCollection"))),
  nTaus(iConfig.getParameter<int>("NTaus")),
  metToken(consumes<edm::View<pat::MET>>(iConfig.getParameter<edm::InputTag>("METCollection"))),
  muonToken(consumes<edm::View<pat::Muon>>(iConfig.getParameter<edm::InputTag>("MuonCollection"))),
  nMuons(iConfig.getParameter<int>("NMuons")),
  nEvents(0),
  nSelectedEvents(0)
{

}

Hplus2hwAnalysisSkim::~Hplus2hwAnalysisSkim(){
    double eff = 0;
    if(nEvents > 0) eff = ((double)nSelectedEvents)/((double) nEvents);
    std::cout << "Hplus2hwAnalysisSkim: " //      edm::LogVerbatim("Hplus2hwAnalysisSkim") 
              << " Number_events_read " << nEvents
              << " Number_events_kept " << nSelectedEvents
              << " Efficiency         " << eff << std::endl;
}


bool Hplus2hwAnalysisSkim::filter(edm::Event& iEvent, const edm::EventSetup& iSetup ){

    nEvents++;

    ////////
    // Trigger bits
    ////////

/*    edm::Handle<edm::TriggerResults> trghandle;
    iEvent.getByToken(trgResultsToken,trghandle);
    if(trghandle.isValid()){
        edm::TriggerResults tr = *trghandle;
        bool fromPSetRegistry;
        edm::Service<edm::service::TriggerNamesService> tns;
        std::vector<std::string> hlNames; 
        tns->getTrigPaths(tr, hlNames, fromPSetRegistry);
        bool passed = false;
        bool trgBitFound = false;
        for(size_t i = 0; i < triggerBits.size(); ++i){
            std::regex hlt_re(triggerBits[i]);
            int n = 0;
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
	}
	if(!trgBitFound) {
            std::cout << "Skimming with trigger bit, but none of the triggers was found!" << std::endl;
            std::cout << "Looked for triggers:" << std::endl;
            for (auto& p: triggerBits) {
                std::cout << "    " << p << std::endl;
            }

            std::cout << "Available triggers in dataset:" << std::endl;
            for(std::vector<std::string>::const_iterator j = hlNames.begin(); j!= hlNames.end(); ++j){
                std::cout << "    " << *j << std::endl;
            }
            exit(1);
        }

	if(!passed) return false; 
    }

*/
    ////////
    // Taus
    ////////

    edm::Handle<edm::View<pat::Tau> > tauhandle;
    iEvent.getByToken(tauToken, tauhandle);
    int ntaus = 0;
    if (tauhandle.isValid()){
        for(size_t i = 0; i < tauhandle->size(); ++i) {
            const pat::Tau& obj = tauhandle->at(i);
            ++ntaus;
        }
    }
    if (ntaus < nTaus) return false;

    ////////
    // Jets
    ////////

    edm::Handle<edm::View<pat::Jet> > jethandle;
    iEvent.getByToken(jetToken, jethandle);
    int njets = 0;
    if(jethandle.isValid()){
        for(size_t i=0; i<jethandle->size(); ++i) {
            const pat::Jet& obj = jethandle->at(i);
            njets++;
        }
    }



    ////////
    // Muons
    ////////

    edm::Handle<edm::View<pat::Muon> > muonHandle;
    iEvent.getByToken(muonToken, muonHandle);
    int nmuons = 0;
    if(muonHandle.isValid()){
      for(size_t i=0; i<muonHandle->size(); ++i) {
            const pat::Muon& obj = muonHandle->at(i);
	    if (obj.p4().pt() < 23) continue;
            if (fabs(obj.p4().eta()) > 2.1) continue;

            nmuons++;
      }
    }
    if (nmuons < nMuons) return false;
  
    ////////
    // All selections passed
    ////////

    nSelectedEvents++;
    return true;
}


DEFINE_FWK_MODULE(Hplus2hwAnalysisSkim);
