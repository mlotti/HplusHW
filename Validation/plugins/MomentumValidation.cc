#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DQMServices/Core/interface/DQMStore.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DQMServices/Core/interface/MonitorElement.h"

#include "DataFormats/Candidate/interface/Candidate.h"

#include <iostream>
using namespace std;

class MomentumValidation : public edm::EDAnalyzer {
    public:
	MomentumValidation(const edm::ParameterSet&);
	~MomentumValidation();

	void beginRun(const edm::Run&,const edm::EventSetup&);
	void beginJob();
	void analyze( const edm::Event&, const edm::EventSetup&);
	void endJob();
	void endRun(const edm::Run&,const edm::EventSetup&);

    private:
	template <class T> void loop(const edm::Event& iEvent,const edm::EventSetup& iSetup, const T& collection);

	edm::InputTag src;

  	DQMStore *dbe;

        MonitorElement *nEvt;
  	MonitorElement *Pt, *Eta, *Phi;
};

MomentumValidation::MomentumValidation(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<edm::InputTag>("src"))
{
  dbe = 0;
  dbe = edm::Service<DQMStore>().operator->();
}

MomentumValidation::~MomentumValidation() {}

void MomentumValidation::beginJob(){
  if(dbe){
    ///Setting the DQM top directories
    dbe->setCurrentFolder("Validation/Momentum");

    // Number of analyzed events
    nEvt = dbe->book1D("nEvt", "n analyzed Events", 1, 0., 1.);

    //Kinematics
    Pt          = dbe->book1D("Pt "+src.label(),"pT", 100 ,0,100);
    Eta         = dbe->book1D("Eta "+src.label(),"eta", 100 ,-2.5,2.5);
    Phi		= dbe->book1D("Phi "+src.label(),"phi", 100 ,-3.14,3.14);
  }
}

void MomentumValidation::beginRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}
void MomentumValidation::endRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}

void MomentumValidation::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup){
    nEvt->Fill(0.5);

    edm::Handle<edm::View<reco::Candidate> > genericObjs;
    if(iEvent.getByLabel(src,genericObjs)){
	loop(iEvent,iSetup,*genericObjs);
//	cout << "check genericObjs size " << genericObjs->size() << endl;
    }

}

template <class T>
void MomentumValidation::loop(const edm::Event& iEvent,const edm::EventSetup& iSetup, const T& collection) {
    for(typename T::const_iterator i = collection.begin(); 
                                   i!= collection.end(); ++i){
	Pt->Fill(i->p4().Pt());
	Eta->Fill(i->p4().Eta());
	Phi->Fill(i->p4().Phi());
    }
}
void MomentumValidation::endJob(){}

DEFINE_FWK_MODULE(MomentumValidation);
