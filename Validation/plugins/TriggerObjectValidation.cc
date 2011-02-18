#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DQMServices/Core/interface/DQMStore.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DQMServices/Core/interface/MonitorElement.h"

#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"

#include <iostream>
using namespace std;

class TriggerObjectValidation : public edm::EDAnalyzer {
    public:
	TriggerObjectValidation(const edm::ParameterSet&);
	~TriggerObjectValidation();

	void beginRun(const edm::Run&,const edm::EventSetup&);
	void beginJob();
	void analyze( const edm::Event&, const edm::EventSetup&);
	void endJob();
	void endRun(const edm::Run&,const edm::EventSetup&);

    private:
	edm::InputTag src;
	int id;

  	DQMStore *dbe;

        MonitorElement *nEvt;
  	MonitorElement *Pt, *Eta, *Phi;
	MonitorElement *EtaPhi;
};

TriggerObjectValidation::TriggerObjectValidation(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<edm::InputTag>("src")),
  id(iConfig.getParameter<int>("id"))
{
  dbe = 0;
  dbe = edm::Service<DQMStore>().operator->();
}

TriggerObjectValidation::~TriggerObjectValidation() {}

void TriggerObjectValidation::beginJob(){
  if(dbe){
    ///Setting the DQM top directories
    dbe->setCurrentFolder("Validation/TriggerObjects");

    // Number of analyzed events
    nEvt = dbe->book1D("nEvt", "n analyzed Events", 1, 0., 1.);

    //Kinematics
    Pt          = dbe->book1D("Pt","pT", 100 ,0,100);
    Eta         = dbe->book1D("Eta","eta", 100 ,-2.5,2.5);
    Phi		= dbe->book1D("Phi","phi", 100 ,-3.14,3.14);

    EtaPhi	= dbe->book2D("Eta Phi","eta phi", 100 ,-2.5,2.5, 100 ,-3.14,3.14);
  }
}

void TriggerObjectValidation::beginRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}
void TriggerObjectValidation::endRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}

void TriggerObjectValidation::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup){
    nEvt->Fill(0.5);
    edm::Handle<trigger::TriggerEvent> triggerObjs;
    if(iEvent.getByLabel(src,triggerObjs)){
	const trigger::TriggerObjectCollection objs = triggerObjs->getObjects();
	for(unsigned i = 0; i < objs.size(); ++i){
		if(objs[i].id() != id) continue;
		Pt->Fill(objs[i].pt());
        	Eta->Fill(objs[i].eta());
        	Phi->Fill(objs[i].phi());

        	EtaPhi->Fill(objs[i].eta(),objs[i].phi());
	}
    }
}

void TriggerObjectValidation::endJob(){}

DEFINE_FWK_MODULE(TriggerObjectValidation);
