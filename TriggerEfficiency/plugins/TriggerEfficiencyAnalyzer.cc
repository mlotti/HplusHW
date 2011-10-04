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

namespace {
  struct EventVariableBase {
    EventVariableBase(const edm::InputTag& t, const std::string& n): tag(t), name(n) {}
    edm::InputTag tag;
    std::string name;
  };

  template <typename T>
  struct EventVariable: public EventVariableBase {
    EventVariable(const edm::InputTag& t, const std::string& n): EventVariableBase(t, n) {}
    T value;
  };
  typedef EventVariable<bool> BoolVariable;
}

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
  edm::InputTag metType1Src;
  edm::InputTag caloMetSrc;
  edm::InputTag caloMetNoHFSrc;

	TTree* TriggerEfficiencyTree;

	bool triggerBit;
  int ntaus;
  float taupt,taueta,met,metType1;
  float caloMet, caloMetNoHF;
  std::vector<BoolVariable> bools;
};

TriggerEfficiencyAnalyzer::TriggerEfficiencyAnalyzer(const edm::ParameterSet& iConfig) :
    triggerResults(iConfig.getParameter<edm::InputTag>("triggerResults")),
    triggerBitName(iConfig.getParameter<std::string>("triggerBit")),
    tauSrc(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
    metSrc(iConfig.getUntrackedParameter<edm::InputTag>("metRawSrc")),
    metType1Src(iConfig.getUntrackedParameter<edm::InputTag>("metType1Src")),
    caloMetSrc(iConfig.getUntrackedParameter<edm::InputTag>("caloMetSrc")),
    caloMetNoHFSrc(iConfig.getUntrackedParameter<edm::InputTag>("caloMetNoHFSrc"))
{
  if(iConfig.exists("bools")) {
    edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("bools");
    std::vector<std::string> names = pset.getParameterNames();
    bools.reserve(names.size());
    for(size_t i=0; i<names.size(); ++i) {
      bools.push_back(BoolVariable(pset.getParameter<edm::InputTag>(names[i]), names[i]));
      
    }
  }

	std::cout << "Trigger table : " << triggerResults.label() << std::endl;
	std::cout << "          bit : " << triggerBitName << std::endl;
	std::cout << "Tau src : " << tauSrc.label() << std::endl;
	std::cout << "MET src : " << metSrc.label() << std::endl;

	edm::Service<TFileService> fs;
	TriggerEfficiencyTree = fs->make<TTree>("TriggerEfficiencyTree", triggerBitName.c_str(),1);

	TriggerEfficiencyTree->Branch("TriggerBit", &triggerBit);
	TriggerEfficiencyTree->Branch("NTaus", &ntaus);
	TriggerEfficiencyTree->Branch("TauPt", &taupt);
	TriggerEfficiencyTree->Branch("TauEta", &taueta);
	TriggerEfficiencyTree->Branch("MET", &met);
	TriggerEfficiencyTree->Branch("METType1", &metType1);
	TriggerEfficiencyTree->Branch("CaloMET", &caloMet);
	TriggerEfficiencyTree->Branch("CaloMETnoHF", &caloMetNoHF);

        for(size_t i=0; i<bools.size(); ++i) {
          TriggerEfficiencyTree->Branch(bools[i].name.c_str(), &bools[i].value);
        }
}

TriggerEfficiencyAnalyzer::~TriggerEfficiencyAnalyzer(){}

void TriggerEfficiencyAnalyzer::beginRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}

void TriggerEfficiencyAnalyzer::beginJob(){}

void TriggerEfficiencyAnalyzer::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup){

	triggerBit = false;
        ntaus = 0;
	taupt      = 0;
	taueta     = 0;
	met 	   = 0;
        caloMet = 0;
        caloMetNoHF = 0;

        for(size_t i=0; i<bools.size(); ++i) {
          bools[i].value = false;
        }

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

        // Booleans
        edm::Handle<bool> hbool;
        for(size_t i=0; i<bools.size(); ++i) {
          iEvent.getByLabel(bools[i].tag, hbool);
          bools[i].value = *hbool;
        }

// Offline taus
	edm::Handle<edm::View<reco::Candidate> > htaus;
	iEvent.getByLabel(tauSrc, htaus);

        ntaus = htaus->size();

//FIXME: what if we have more than 1 taus passing the selection? 25.5.2011/SL
	for(size_t i=0; i<htaus->size(); ++i) {
          edm::Ptr<reco::Candidate> ptr = htaus->ptrAt(i);
          edm::Ptr<pat::Tau> iTau(ptr.id(), dynamic_cast<const pat::Tau *>(ptr.get()), ptr.key());
          taupt  = iTau->pt();
          taueta = iTau->eta();
	}

// Offline MET
	edm::Handle<edm::View<reco::MET> > hmet;
	iEvent.getByLabel(metSrc, hmet);
        met = hmet->at(0).et();

        edm::Handle<edm::View<reco::MET> > hmetType1;
        iEvent.getByLabel(metType1Src, hmetType1);
        metType1 = hmet->at(0).et();

	edm::Handle<edm::View<reco::MET> > hmet2;
	iEvent.getByLabel(caloMetSrc, hmet2);
        caloMet = hmet2->at(0).et();

	edm::Handle<edm::View<reco::MET> > hmet3;
	iEvent.getByLabel(caloMetNoHFSrc, hmet3);
        caloMetNoHF = hmet3->at(0).et();

// Filling..
	TriggerEfficiencyTree->Fill();

}

void TriggerEfficiencyAnalyzer::endJob(){}
void TriggerEfficiencyAnalyzer::endRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}

//define this as a plug-in
DEFINE_FWK_MODULE(TriggerEfficiencyAnalyzer);
