#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DQMServices/Core/interface/DQMStore.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DQMServices/Core/interface/MonitorElement.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include <iostream>
using namespace std;

class GeneratorMassValidation : public edm::EDAnalyzer {
    public:
	GeneratorMassValidation(const edm::ParameterSet&);
	~GeneratorMassValidation();

	void beginRun(const edm::Run&,const edm::EventSetup&);
	void beginJob();
	void analyze( const edm::Event&, const edm::EventSetup&);
	void endJob();
	void endRun(const edm::Run&,const edm::EventSetup&);

    private:
	edm::InputTag src;
	std::vector<int> particles;

  	DQMStore *dbe;

	MonitorElement *nEvt;
        MonitorElement **mass;
};

GeneratorMassValidation::GeneratorMassValidation(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<edm::InputTag>("src")),
  particles(iConfig.getParameter< std::vector<int> >("particles"))
{
  dbe = 0;
  dbe = edm::Service<DQMStore>().operator->();

  mass = new MonitorElement*[particles.size()];
}

GeneratorMassValidation::~GeneratorMassValidation() {}

void GeneratorMassValidation::beginJob(){}

void GeneratorMassValidation::beginRun(const edm::Run& iRun,const edm::EventSetup& iSetup){
  if(dbe){
    ///Setting the DQM top directories
    dbe->setCurrentFolder("Validation/Mass");

    // Number of analyzed events
    nEvt = dbe->book1D("nEvt "+src.label(), "n analyzed Events", 1, 0., 1.);

    //Mass
    for(size_t i = 0; i < particles.size(); ++i){
        char buffer[10];
	sprintf(buffer,"Mass %i",particles[i]);
	mass[i] = dbe->book1D(buffer,"m(GeV)", 100 ,0,200);
    }
  }
}
void GeneratorMassValidation::endRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}

void GeneratorMassValidation::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup){
    nEvt->Fill(0.5);

    edm::Handle<reco::GenParticleCollection> genParticles;
    iEvent.getByLabel(src, genParticles);

    if(genParticles.isValid()){
    for(size_t i = 0; i < genParticles->size(); ++ i) {
        const reco::GenParticle & p = (*genParticles)[i];
	for(size_t j = 0; j < particles.size(); ++j) {
	    if(abs(p.pdgId())== particles[j] && p.pdgId() != p.mother(0)->pdgId()){
		mass[j]->Fill(p.mass());
	    }
	}
    }
  }
}

void GeneratorMassValidation::endJob(){}

DEFINE_FWK_MODULE(GeneratorMassValidation);
