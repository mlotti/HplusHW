/** \class LheHTSkim
 *
 *  
 *  Filter to select events for 
 *  tau+MET trigger MET-leg efficiency study
 *
 *  \author Sami Lehti  -  HIP Helsinki
 *  based on example from A.Marini, MIT
 *
 */

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

#include "TLorentzVector.h"

/*




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
*/
#include <iostream>
//#include <regex>

class LheHTSkim : public edm::EDFilter {

    public:
        explicit LheHTSkim(const edm::ParameterSet&);
        ~LheHTSkim();

  	virtual bool filter(edm::Event&, const edm::EventSetup& );

   private:
        edm::EDGetTokenT<LHEEventProduct> lheToken;

        float HTmin,HTmax;
        int nEvents;
        int nSelectedEvents;
};

LheHTSkim::LheHTSkim(const edm::ParameterSet& iConfig):
  lheToken(consumes<LHEEventProduct>(iConfig.getParameter<edm::InputTag>("src"))),
  HTmin(iConfig.getParameter<double>("HTmin")),
  HTmax(iConfig.getParameter<double>("HTmax")),
  nEvents(0),
  nSelectedEvents(0)
{}


LheHTSkim::~LheHTSkim(){
    double eff = 0;
    if(nEvents > 0) eff = ((double)nSelectedEvents)/((double) nEvents);
    std::cout << "LheHTSkim: HT range " << HTmin << " - " << HTmax //  	edm::LogVerbatim("LheHTSkim") 
              << " Number_events_read " << nEvents
              << " Number_events_kept " << nSelectedEvents
              << " Efficiency         " << eff << std::endl;
}


bool LheHTSkim::filter(edm::Event& iEvent, const edm::EventSetup& iSetup ){

    nEvents++;

    float HT = 0;
    edm::Handle<LHEEventProduct> lheHandle;
    iEvent.getByToken(lheToken, lheHandle);

    if(lheHandle.isValid()){
        const auto& hepeup = lheHandle->hepeup(); 
        for(unsigned i=0; i<hepeup.IDUP.size(); ++i){
            if (hepeup.ISTUP[i] != 1) continue; //Outgoing final state particle
            TLorentzVector p4(hepeup.PUP[i][0],hepeup.PUP[i][1],hepeup.PUP[i][2],hepeup.PUP[i][3]);
            if((abs(hepeup.IDUP[i]) <=6) or hepeup.IDUP[i] ==21) HT += p4.Pt();
        }
    }
    if(HT < HTmin || HT > HTmax) return false;
    
    // All selections passed
    nSelectedEvents++;
    return true;
}

DEFINE_FWK_MODULE(LheHTSkim);   

