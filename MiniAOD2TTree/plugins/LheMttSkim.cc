/** \class LheHTSkim
 *
 *  
 *  Filter to select events from inclusive ttbar sample
 *  with inv mass m(tt) > 700 (we have bins 700-1000 and 1000-Inf) 
 *  to avoid double counting. 
 *
 *  \author Sami Lehti  -  HIP Helsinki
 */

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

#include "TLorentzVector.h"

#include <iostream>


class LheMttSkim : public edm::EDFilter {

    public:
        explicit LheMttSkim(const edm::ParameterSet&);
        ~LheMttSkim();

  	virtual bool filter(edm::Event&, const edm::EventSetup& );

   private:
        edm::EDGetTokenT<LHEEventProduct> lheToken;

        float Mttmin,Mttmax;
        int nEvents;
        int nSelectedEvents;
};

LheMttSkim::LheMttSkim(const edm::ParameterSet& iConfig):
  lheToken(consumes<LHEEventProduct>(iConfig.getParameter<edm::InputTag>("src"))),
  Mttmin(iConfig.getParameter<double>("Mttmin")),
  Mttmax(iConfig.getParameter<double>("Mttmax")),
  nEvents(0),
  nSelectedEvents(0)
{}


LheMttSkim::~LheMttSkim(){
    double eff = 0;
    if(nEvents > 0) eff = ((double)nSelectedEvents)/((double) nEvents);
    std::cout << "LheMttSkim: Mtt range " << Mttmin << " - " << Mttmax //  	edm::LogVerbatim("LheMttSkim") 
              << " Number_events_read " << nEvents
              << " Number_events_kept " << nSelectedEvents
              << " Efficiency         " << eff << std::endl;
}


bool LheMttSkim::filter(edm::Event& iEvent, const edm::EventSetup& iSetup ){

    nEvents++;

    edm::Handle<LHEEventProduct> lheHandle;
    iEvent.getByToken(lheToken, lheHandle);

    TLorentzVector mInv(0,0,0,0);
    int ntops = 0;
    if(lheHandle.isValid()){
        const auto& hepeup = lheHandle->hepeup(); 
        for(unsigned i=0; i<hepeup.IDUP.size(); ++i){
            if (hepeup.ISTUP[i] != 1) continue; //Outgoing final state particle
            TLorentzVector p4(hepeup.PUP[i][0],hepeup.PUP[i][1],hepeup.PUP[i][2],hepeup.PUP[i][3]);
            if(abs(hepeup.IDUP[i]) ==6) {
              mInv += p4;
              ntops++;
            }
        }
    }
    double Mtt = mInv.M();
std::cout << "check Mtt " << ntops << " "<< mInv.M() << std::endl;
    if(Mtt < Mttmin || Mtt > Mttmax) return false;
    
    // All selections passed
    nSelectedEvents++;
    return true;
}

DEFINE_FWK_MODULE(LheMttSkim);   

