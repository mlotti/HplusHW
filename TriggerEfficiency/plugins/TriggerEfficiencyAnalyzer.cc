#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
        
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/Handle.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TTree.h"

class TriggerEfficiencyAnalyzer : public edm::EDAnalyzer {
    public:
        TriggerEfficiencyAnalyzer(const edm::ParameterSet&);
        ~TriggerEfficiencyAnalyzer();

        void beginRun(const edm::Run&,const edm::EventSetup&);
        void beginJob();
        void analyze( const edm::Event&, const edm::EventSetup&);
        void endJob();
        void endRun(const edm::Run&,const edm::EventSetup&);

    private:
	edm::InputTag triggerResults;
	std::string   triggerBitName;
	edm::InputTag tauSrc;
	edm::InputTag metSrc;

	TTree* TriggerEfficiencyTree;

	int triggerBit;
	double taupt,taueta,met;
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
	fs->make<TTree>("TriggerEfficiencyTree", triggerBitName.c_str());

	TriggerEfficiencyTree->Branch("triggerBit",&triggerBit,"triggerBit/I");
}

TriggerEfficiencyAnalyzer::~TriggerEfficiencyAnalyzer(){}

void TriggerEfficiencyAnalyzer::beginRun(const edm::Run&,const edm::EventSetup&){}
void TriggerEfficiencyAnalyzer::beginJob(){}
void TriggerEfficiencyAnalyzer::analyze( const edm::Event&, const edm::EventSetup&){

	triggerBit = 0;

	TriggerEfficiencyTree->Fill();
}
void TriggerEfficiencyAnalyzer::endJob(){}
void TriggerEfficiencyAnalyzer::endRun(const edm::Run&,const edm::EventSetup&){}

//define this as a plug-in
DEFINE_FWK_MODULE(TriggerEfficiencyAnalyzer);
