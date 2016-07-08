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

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "FWCore/Framework/interface/LuminosityBlock.h"

#include <iostream>
#include <regex>

class SignalAnalysisSkim : public edm::EDFilter {

    public:
        explicit SignalAnalysisSkim(const edm::ParameterSet&);
        ~SignalAnalysisSkim();

  	virtual bool filter(edm::Event&, const edm::EventSetup& );

   private:
	edm::EDGetTokenT<edm::TriggerResults> trgResultsToken;
	std::vector<std::string> triggerBits;

        edm::EDGetTokenT<edm::View<pat::Jet>> jetToken;
        std::vector<std::string> jetUserFloats;
        const double fJetEtCut;
        const double fJetEtaCut;
        const int nJets;
        
        edm::EDGetTokenT<edm::View<pat::Tau>> tauToken;
        const double fTauPtCut;
        const double fTauEtaCut;
        const double fTauLdgTrkPtCut;

        edm::EDGetTokenT<edm::View<pat::MET>> metToken;

        int nEvents;
        int nSelectedEvents;
};

SignalAnalysisSkim::SignalAnalysisSkim(const edm::ParameterSet& iConfig)
: trgResultsToken(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("TriggerResults"))),
  triggerBits(iConfig.getParameter<std::vector<std::string> >("HLTPaths")),
  jetToken(consumes<edm::View<pat::Jet>>(iConfig.getParameter<edm::InputTag>("JetCollection"))),
  jetUserFloats(iConfig.getParameter<std::vector<std::string> >("JetUserFloats")),
  fJetEtCut(iConfig.getParameter<double>("JetEtCut")),
  fJetEtaCut(iConfig.getParameter<double>("JetEtaCut")),
  nJets(iConfig.getParameter<int>("NJets")),
  tauToken(consumes<edm::View<pat::Tau>>(iConfig.getParameter<edm::InputTag>("TauCollection"))),
  fTauPtCut(iConfig.getParameter<double>("TauPtCut")),
  fTauEtaCut(iConfig.getParameter<double>("TauEtaCut")),
  fTauLdgTrkPtCut(iConfig.getParameter<double>("TauLdgTrkPtCut")),
  metToken(consumes<edm::View<pat::MET>>(iConfig.getParameter<edm::InputTag>("METCollection"))),
  nEvents(0),
  nSelectedEvents(0)
{
  
}


SignalAnalysisSkim::~SignalAnalysisSkim(){
    double eff = 0;
    if(nEvents > 0) eff = ((double)nSelectedEvents)/((double) nEvents);
    std::cout << "SignalAnalysisSkim: " //  	edm::LogVerbatim("SignalAnalysisSkim") 
              << " Number_events_read " << nEvents
              << " Number_events_kept " << nSelectedEvents
              << " Efficiency         " << eff << std::endl;
}


bool SignalAnalysisSkim::filter(edm::Event& iEvent, const edm::EventSetup& iSetup ){

    nEvents++;

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
/*
    // FIXME: CaloMET to emulate Trigger MET leg, to skim the samples at least with the MET leg 09062016/SL
    edm::Handle<edm::View<pat::MET>> methandle;                                                                                                                                                    
    iEvent.getByToken(metToken, methandle);                                                                                                                                                        
    if(methandle.isValid()){
      // Member ftion caloMETPt() returns caloMET only for slimmedMETs, for MET_Type1_NoHF and Puppi it seems to return the PFMET.                                                            
      // Fixed by hard coding the caloMET to use slimmedMETs                                                                                                                                  
      // 05112015/SL                                                                                                                                                                          
      if(methandle->ptrAt(0)->caloMETPt()){                                                                   
	double caloMET = methandle->ptrAt(0)->caloMETPt();
	//std::cout << "check skim calomet " << caloMET << std::endl;
	if(caloMET < 80) return false;
      }
    }
*/

    // Taus
    edm::Handle<edm::View<pat::Tau> > tauhandle;
    iEvent.getByToken(tauToken, tauhandle);
    int ntaus = 0;
    if (tauhandle.isValid()){
        for(size_t i = 0; i < tauhandle->size(); ++i) {
            const pat::Tau& obj = tauhandle->at(i);
            if (obj.p4().pt() < fTauPtCut) continue;
            if (fabs(obj.p4().eta()) > fTauEtaCut) continue;
            if (obj.leadChargedHadrCand()->p4().Pt() < fTauLdgTrkPtCut) continue;
            // Passed the loose tau selections
            ++ntaus;
        }
    }
    if (ntaus == 0) return false;
    
    // Jets
    edm::Handle<edm::View<pat::Jet> > jethandle;
    iEvent.getByToken(jetToken, jethandle);
    int njets = 0;
    if(jethandle.isValid()){
        for(size_t i=0; i<jethandle->size(); ++i) {
            const pat::Jet& obj = jethandle->at(i);

	    if(obj.p4().pt() < fJetEtCut) continue;
	    if(fabs(obj.p4().eta()) > fJetEtaCut) continue;
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
    
    // All selections passed
    nSelectedEvents++;
    return true;
}

DEFINE_FWK_MODULE(SignalAnalysisSkim);   

