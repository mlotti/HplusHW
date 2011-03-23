#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DQMServices/Core/interface/DQMStore.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DQMServices/Core/interface/MonitorElement.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"

#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "Math/VectorUtil.h"

#include <iostream>
using namespace std;

class TauTriggerEfficiencyValidation : public edm::EDAnalyzer {
    public:
	TauTriggerEfficiencyValidation(const edm::ParameterSet&);
	~TauTriggerEfficiencyValidation();

	void beginRun(const edm::Run&,const edm::EventSetup&);
	void beginJob();
	void analyze( const edm::Event&, const edm::EventSetup&);
	void endJob();
	void endRun(const edm::Run&,const edm::EventSetup&);

    private:
	edm::InputTag triggerResults;
	std::string triggerBit;
	edm::InputTag triggerObjects;
	int triggerObjectId;

	edm::InputTag hltPathFilter;
	edm::InputTag tauSrc,tauDiscr;

	double matchingCone;

	edm::InputTag primaryVertexSrc;

  	DQMStore *dbe;

        MonitorElement *nEvt;
	MonitorElement *nTaus;
  	MonitorElement *PtOfflineTau, *EtaOfflineTau, *PhiOfflineTau;
	MonitorElement *PtOfflineTauTriggerMatched, *EtaOfflineTauTriggerMatched, *PhiOfflineTauTriggerMatched;
	MonitorElement *EtaOfflineTauZ,*EtaOfflineTauZTriggerMatched;
};

TauTriggerEfficiencyValidation::TauTriggerEfficiencyValidation(const edm::ParameterSet& iConfig):
    triggerResults(iConfig.getParameter<edm::InputTag>("triggerResults")),
    triggerBit(iConfig.getParameter<std::string>("triggerBit")),
    triggerObjects(iConfig.getParameter<edm::InputTag>("triggerObjects")),
    triggerObjectId(iConfig.getParameter<int>("triggerObjectId")),
    hltPathFilter(iConfig.getParameter<edm::InputTag>("hltPathFilter")),
    tauSrc(iConfig.getParameter<edm::InputTag>("referenceTau")),
    tauDiscr(iConfig.getParameter<edm::InputTag>("referenceTauDiscr")),
    matchingCone(iConfig.getParameter<double>("MatchingCone")),
    primaryVertexSrc(iConfig.getParameter<edm::InputTag>("PrimaryVertex"))
{
  dbe = 0;
  dbe = edm::Service<DQMStore>().operator->();
}

TauTriggerEfficiencyValidation::~TauTriggerEfficiencyValidation() {}

void TauTriggerEfficiencyValidation::beginJob(){
  if(dbe){
    ///Setting the DQM top directories
    dbe->setCurrentFolder("Validation/TriggerEfficiency");

    // Number of analyzed events
    nEvt    = dbe->book1D("nEvt "+hltPathFilter.label()+" "+triggerBit, "n analyzed Events", 2, 0., 2.);

    // Number of analyzed taus
    nTaus   = dbe->book1D("nTaus "+hltPathFilter.label(), "n analyzed Taus", 2, 0., 2.);

    //Kinematics
    PtOfflineTau  = dbe->book1D("Pt tau","pT", 100 ,0,100);
    EtaOfflineTau = dbe->book1D("Eta tau","eta", 100 ,-2.5,2.5);
    PhiOfflineTau = dbe->book1D("Phi tau","phi", 100 ,-3.14,3.14);

    PtOfflineTauTriggerMatched  = dbe->book1D("Pt tau "+hltPathFilter.label()+" matched","pT", 100 ,0,100);
    EtaOfflineTauTriggerMatched = dbe->book1D("Eta tau "+hltPathFilter.label()+" matched","eta", 100 ,-2.5,2.5);
    PhiOfflineTauTriggerMatched = dbe->book1D("Phi tau "+hltPathFilter.label()+" matched","phi", 100 ,-3.14,3.14);

    EtaOfflineTauZ               = dbe->book2D("Eta Z ","eta Z", 100 ,-2.5,2.5, 50 ,-25.,25.);
    EtaOfflineTauZTriggerMatched = dbe->book2D("Eta Z "+hltPathFilter.label()+" matched","eta Z", 100 ,-2.5,2.5, 50 ,-25.,25.);

    std::cout << "Trigger bit: " << triggerBit << std::endl;
    std::cout << "Trigger path: " << hltPathFilter.label() << std::endl;
  }
}

void TauTriggerEfficiencyValidation::beginRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}
void TauTriggerEfficiencyValidation::endRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}

void TauTriggerEfficiencyValidation::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup){

    nEvt->Fill(0.5);

    edm::Handle<reco::VertexCollection> primaryVertices;
    iEvent.getByLabel(primaryVertexSrc,primaryVertices);

    const reco::VertexCollection vertexCollection = *(primaryVertices.product());
    double pv_x = 0;
    double pv_y = 0;
    double pv_z = 0;
    if(vertexCollection.size() > 0){
        pv_x = vertexCollection.begin()->x();
        pv_y = vertexCollection.begin()->y();
        pv_z = vertexCollection.begin()->z();
    }

    edm::Handle<trigger::TriggerEvent> triggerObjs;
    iEvent.getByLabel(triggerObjects,triggerObjs);

    bool triggered = false;
    edm::Handle<reco::PFTauCollection> tauHandle;
    if(iEvent.getByLabel(tauSrc,tauHandle)){
	edm::Handle<reco::PFTauDiscriminator> discrHandle;
	iEvent.getByLabel(tauDiscr,discrHandle);

	for (reco::PFTauCollection::size_type iPFTau=0;iPFTau < tauHandle->size(); iPFTau++) {
		reco::PFTauRef thePFTau(tauHandle,iPFTau);
		double discriminator = (*discrHandle)[thePFTau];

		if(discriminator < 0.5) continue;

		nTaus->Fill(0.5);
		PtOfflineTau->Fill(thePFTau->pt());
		EtaOfflineTau->Fill(thePFTau->eta());
		PhiOfflineTau->Fill(thePFTau->phi());
		EtaOfflineTauZ->Fill(thePFTau->eta(),pv_z);

		if(triggerObjs.isValid()){
			const trigger::TriggerObjectCollection objs(triggerObjs->getObjects());

		        size_t index = triggerObjs->filterIndex(hltPathFilter);

			bool match = false;
		        if(index < triggerObjs->sizeFilters()){
		          const trigger::Keys& KEYS(triggerObjs->filterKeys(index));

		          for(size_t i = 0;i<KEYS.size();++i){
		                const trigger::TriggerObject& TO(objs[KEYS[i]]);

				ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > p4(TO.px(),TO.py(),TO.pz(),TO.energy());
				double DR = ROOT::Math::VectorUtil::DeltaR(p4,thePFTau->p4());
				if(DR < matchingCone) match = true;
			  }
			}
			if(match){
                		nTaus->Fill(1.5);
                		PtOfflineTauTriggerMatched->Fill(thePFTau->pt());
                		EtaOfflineTauTriggerMatched->Fill(thePFTau->eta());
                		PhiOfflineTauTriggerMatched->Fill(thePFTau->phi());
				EtaOfflineTauZTriggerMatched->Fill(thePFTau->eta(),pv_z);
				triggered = true;
			}
		}
	}

    }

    if(!triggered) return;
    nEvt->Fill(1.5);
}

void TauTriggerEfficiencyValidation::endJob(){}

DEFINE_FWK_MODULE(TauTriggerEfficiencyValidation);
