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

#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"

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


  std::string stripCollection(const std::string& name) {
    size_t pos = name.find(":");
    return name.substr(0, pos);
  }
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
  edm::InputTag patTriggerEventSrc;
  std::string   triggerBitName;
  std::string hltPath;
  edm::InputTag tauSrc;
  edm::InputTag metSrc;
  edm::InputTag metType1Src;
  edm::InputTag caloMetSrc;
  edm::InputTag caloMetNoHFSrc;

  TTree* tree;

  typedef math::XYZTLorentzVector LorentzVector;

  bool triggerBit;
  int ntaus;
  float taupt,taueta,met,metType1;
  float caloMet, caloMetNoHF;
  float l1Met;
  float hltMet;
  std::vector<LorentzVector> l1CenJets;
  std::vector<LorentzVector> l1TauJets;
  std::vector<LorentzVector> l1ForJets;
  std::vector<LorentzVector> hltTaus;
  std::vector<BoolVariable> bools;
};

TriggerEfficiencyAnalyzer::TriggerEfficiencyAnalyzer(const edm::ParameterSet& iConfig) :
    triggerResults(iConfig.getParameter<edm::InputTag>("triggerResults")),
    patTriggerEventSrc(iConfig.getParameter<edm::InputTag>("patTriggerEvent")),
    triggerBitName(iConfig.getParameter<std::string>("triggerBit")),
    hltPath(iConfig.getParameter<std::string>("hltPath")),
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
	tree = fs->make<TTree>("tree", triggerBitName.c_str(),1);

	tree->Branch("TriggerBit", &triggerBit);
	tree->Branch("NTaus", &ntaus);
	tree->Branch("TauPt", &taupt);
	tree->Branch("TauEta", &taueta);
	tree->Branch("MET", &met);
	tree->Branch("METType1", &metType1);
	tree->Branch("CaloMET", &caloMet);
	tree->Branch("CaloMETnoHF", &caloMetNoHF);
        tree->Branch("L1MET", &l1Met);
        tree->Branch("L1CenJet_p4", &l1CenJets);
        tree->Branch("L1TauJet_p4", &l1TauJets);
        tree->Branch("L1ForJet_p4", &l1ForJets);
        tree->Branch("HLTMET", &hltMet);
        tree->Branch("HLTTau_p4", &hltTaus);

        for(size_t i=0; i<bools.size(); ++i) {
          tree->Branch(bools[i].name.c_str(), &bools[i].value);
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
        l1Met = -1;
        l1CenJets.clear();
        l1TauJets.clear();
        l1ForJets.clear();
        hltMet = -1;
        hltTaus.clear();

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

        // Trigger objects from pat trigger event
        edm::Handle<pat::TriggerEvent> htrigger;
        iEvent.getByLabel(patTriggerEventSrc, htrigger);

        // L1 MET
        pat::TriggerObjectRefVector l1mets = htrigger->objects(trigger::TriggerL1ETM);
        if(!l1mets.empty()) {
          if(l1mets.size() != 1)
            throw cms::Exception("Assert") << "L1 MET exists, but l1mets.size() = " << l1mets.size() << " != 1 at " << __FILE__ << ":" << __LINE__ << std::endl;
          l1Met = l1mets[0]->et();
        }

        // L1 jets
        pat::TriggerObjectRefVector l1cenjets = htrigger->objects(trigger::TriggerL1CenJet);
        for(size_t i=0; i<l1cenjets.size(); ++i)
          l1CenJets.push_back(l1cenjets[i]->p4());
        pat::TriggerObjectRefVector l1taujets = htrigger->objects(trigger::TriggerL1TauJet);
        for(size_t i=0; i<l1taujets.size(); ++i)
          l1TauJets.push_back(l1taujets[i]->p4());
        pat::TriggerObjectRefVector l1forjets = htrigger->objects(trigger::TriggerL1ForJet);
        for(size_t i=0; i<l1forjets.size(); ++i)
          l1ForJets.push_back(l1forjets[i]->p4());

        // HLT MET
        pat::TriggerObjectRefVector hltmets = htrigger->objects(trigger::TriggerMET);
        if(!hltmets.empty()) {
          for(size_t i=0; i<hltmets.size(); ++i) {
            if(stripCollection(hltmets[i]->collection()) == "hltMet")
              hltMet = hltmets[i]->et();
          }
        }

        // HLT Taus
        pat::TriggerFilterRefVector filters = htrigger->pathFilters(hltPath, false);
        if(filters.size() == 0)
          throw cms::Exception("LogicError") << "No filters for path " << hltPath << std::endl;
        pat::TriggerObjectRefVector hltobjs = htrigger->filterObjects(filters[filters.size()-1]->label());
        for(size_t i=0; i<hltobjs.size(); ++i) {
          if(hltobjs[i]->id(trigger::TriggerTau)) {
            hltTaus.push_back(hltobjs[i]->p4());
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
        metType1 = hmetType1->at(0).et();

	edm::Handle<edm::View<reco::MET> > hmet2;
	iEvent.getByLabel(caloMetSrc, hmet2);
        caloMet = hmet2->at(0).et();

	edm::Handle<edm::View<reco::MET> > hmet3;
	iEvent.getByLabel(caloMetNoHFSrc, hmet3);
        caloMetNoHF = hmet3->at(0).et();

// Filling..
	tree->Fill();

}

void TriggerEfficiencyAnalyzer::endJob(){}
void TriggerEfficiencyAnalyzer::endRun(const edm::Run& iRun,const edm::EventSetup& iSetup){}

//define this as a plug-in
DEFINE_FWK_MODULE(TriggerEfficiencyAnalyzer);
