#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
        
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/Common/interface/TriggerResults.h"  
#include "FWCore/Common/interface/TriggerNames.h"

#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "DataFormats/METReco/interface/MET.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TTree.h"

class TriggerEfficiencyAnalyzer : public edm::EDAnalyzer {
    public:
        TriggerEfficiencyAnalyzer(const edm::ParameterSet&);
        ~TriggerEfficiencyAnalyzer();

    private:
        virtual void beginRun(const edm::Run&,const edm::EventSetup&);
        virtual void beginJob();
        virtual void analyze( const edm::Event&, const edm::EventSetup&);
        virtual void endJob();
        virtual void endRun(const edm::Run&,const edm::EventSetup&);

	edm::InputTag triggerResults;
	std::string   triggerBitName;
	edm::InputTag tauSrc;
	edm::InputTag metSrc;

	TTree* TriggerEfficiencyTree;

	int triggerBit;
	float taupt,taueta,met;
};

TriggerEfficiencyAnalyzer::TriggerEfficiencyAnalyzer(const edm::ParameterSet& iConfig) :
    triggerResults(iConfig.getParameter<edm::InputTag>("triggerResults")),
    triggerBitName(iConfig.getParameter<std::string>("triggerBit")),
    tauSrc(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
    metSrc(iConfig.getUntrackedParameter<edm::InputTag>("metSrc"))
{
	std::cout << "Trigger table : " << triggerResults.label() << std::endl;
	std::cout << "          bit : " << triggerBitName << std::endl;
	std::cout << "Tau src : " << tauSrc.label() << std::endl;
	std::cout << "MET src : " << metSrc.label() << std::endl;

	edm::Service<TFileService> fs;
	TriggerEfficiencyTree = fs->make<TTree>("TriggerEfficiencyTree", triggerBitName.c_str(),1);

	TriggerEfficiencyTree->Branch("TriggerBit",&triggerBit,"triggerBit/I");
	TriggerEfficiencyTree->Branch("TauPt",&taupt,"taupt/F");
	TriggerEfficiencyTree->Branch("TauEta",&taueta,"taueta/F");
	TriggerEfficiencyTree->Branch("MET",&met,"met/F");
}

TriggerEfficiencyAnalyzer::~TriggerEfficiencyAnalyzer(){}

void TriggerEfficiencyAnalyzer::beginRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}

void TriggerEfficiencyAnalyzer::beginJob(){}

void TriggerEfficiencyAnalyzer::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup){

	triggerBit = 0;
	taupt      = 0;
	taueta     = 0;
	met 	   = 0;

// Trigger bit
	edm::Handle<edm::TriggerResults> hltHandle;
	iEvent.getByLabel(triggerResults,hltHandle);

	const edm::TriggerNames & triggerNames = iEvent.triggerNames(*hltHandle);
      	for (unsigned int i=0; i<triggerNames.size(); i++) {
        	//std::cout << "trigger path= " << triggerNames.triggerName(i) << std::endl;
        	if(triggerBitName == triggerNames.triggerName(i) && hltHandle->accept(i)){
			triggerBit = 1;
                	i = triggerNames.size();
        	}
      	}

// Offline taus
	edm::Handle<edm::View<pat::Tau> > htaus;
	iEvent.getByLabel(tauSrc, htaus);

	const edm::PtrVector<pat::Tau>& taus = htaus->ptrVector();
//FIXME: what if we have more than 1 taus passing the selection? 25.5.2011/SL
	for(edm::PtrVector<pat::Tau>::const_iterator iter = taus.begin();
                                                     iter!= taus.end(); ++iter) {
      		const edm::Ptr<pat::Tau> iTau = *iter;
		taupt  = iTau->pt();
		taueta = iTau->eta();
	}

// Offline MET
	edm::Handle<edm::View<reco::MET> > hmet;
	iEvent.getByLabel(metSrc, hmet);

	edm::Ptr<reco::MET> metptr = hmet->ptrAt(0);
	met = metptr->et();


// Filling..
	TriggerEfficiencyTree->Fill();

}

void TriggerEfficiencyAnalyzer::endJob(){}
void TriggerEfficiencyAnalyzer::endRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}

//define this as a plug-in
DEFINE_FWK_MODULE(TriggerEfficiencyAnalyzer);
