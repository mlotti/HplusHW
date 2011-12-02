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
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMapRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMap.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeEventBranches.h"

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

  struct TriggerBit {
    TriggerBit(const std::string& n): name(n), value(false) {}
    std::string name;
    bool value;
  };

  edm::InputTag triggerResults;
  edm::InputTag l1ReadoutSrc;
  edm::InputTag l1ObjectSrc;
  edm::InputTag patTriggerEventSrc;
  std::string   triggerBitName;
  std::vector<TriggerBit> l1Bits;
  std::string hltPath;
  edm::InputTag tauSrc;
  edm::InputTag metSrc;
  edm::InputTag metType1Src;
  edm::InputTag caloMetSrc;
  edm::InputTag caloMetNoHFSrc;

  std::string l1MetCollection;
  std::string l1CenJetCollection;
  std::string l1TauJetCollection;
  std::string l1ForJetCollection;

  TTree* tree;

  typedef math::XYZTLorentzVector LorentzVector;

  HPlus::TreeEventBranches eventBranches;

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
    l1ReadoutSrc(iConfig.getParameter<edm::InputTag>("l1ReadoutSrc")),
    l1ObjectSrc(iConfig.getParameter<edm::InputTag>("l1ObjectSrc")),
    patTriggerEventSrc(iConfig.getParameter<edm::InputTag>("patTriggerEvent")),
    triggerBitName(iConfig.getParameter<std::string>("triggerBit")),
    hltPath(iConfig.getParameter<std::string>("hltPath")),
    tauSrc(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
    metSrc(iConfig.getUntrackedParameter<edm::InputTag>("metRawSrc")),
    metType1Src(iConfig.getUntrackedParameter<edm::InputTag>("metType1Src")),
    caloMetSrc(iConfig.getUntrackedParameter<edm::InputTag>("caloMetSrc")),
    caloMetNoHFSrc(iConfig.getUntrackedParameter<edm::InputTag>("caloMetNoHFSrc")),
    l1MetCollection("l1extraParticles:MET"),
    l1CenJetCollection("l1extraParticles:Central"),
    l1TauJetCollection("l1extraParticles:Tau"),
    l1ForJetCollection("l1extraParticles:Forward")
{
  if(iConfig.exists("bools")) {
    edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("bools");
    std::vector<std::string> names = pset.getParameterNames();
    bools.reserve(names.size());
    for(size_t i=0; i<names.size(); ++i) {
      bools.push_back(BoolVariable(pset.getParameter<edm::InputTag>(names[i]), names[i]));
      
    }
  }

  std::vector<std::string> l1names = iConfig.getParameter<std::vector<std::string> >("l1Bits");
  for(size_t i=0; i<l1names.size(); ++i) {
    l1Bits.push_back(l1names[i]);
  }

	std::cout << "Trigger table : " << triggerResults.label() << std::endl;
	std::cout << "          bit : " << triggerBitName << std::endl;
	std::cout << "Tau src : " << tauSrc.label() << std::endl;
	std::cout << "MET src : " << metSrc.label() << std::endl;

	edm::Service<TFileService> fs;
	tree = fs->make<TTree>("tree", triggerBitName.c_str(),1);

        eventBranches.book(tree);

	tree->Branch("TriggerBit", &triggerBit);
        for(size_t i=0; i<l1Bits.size(); ++i) {
          tree->Branch(l1Bits[i].name.c_str(), &(l1Bits[i].value));
        }

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

  eventBranches.reset();
	triggerBit = false;
        for(size_t i=0; i<l1Bits.size(); ++i) {
          l1Bits[i].value = false;
        }
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

        eventBranches.setValues(iEvent);

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

        // L1 bits
        // Simplify to use PAT trigger when we have the algorithms available
        edm::Handle<L1GlobalTriggerReadoutRecord> l1Readout;
        iEvent.getByLabel(l1ReadoutSrc, l1Readout);

        edm::Handle<L1GlobalTriggerObjectMapRecord> l1Objects;
        iEvent.getByLabel(l1ObjectSrc, l1Objects);

        const DecisionWord& gtDecisionWord = l1Readout->decisionWord();
        const std::vector<L1GlobalTriggerObjectMap>& objMapVec = l1Objects->gtObjectMap();
        for(size_t i=0; i<l1Bits.size(); ++i) {
          for (std::vector<L1GlobalTriggerObjectMap>::const_iterator itMap = objMapVec.begin();
               itMap != objMapVec.end(); ++itMap) {
            if(l1Bits[i].name == itMap->algoName()) {
              l1Bits[i].value = gtDecisionWord[itMap->algoBitNumber()];
              break;
            }
          }
        }

        /*
        const pat::TriggerAlgorithmRefVector& l1algos = htrigger->algorithmRefs();
        for(size_t i=0; i<l1algos.size(); ++i) {
          std::cout << l1algos[i]->name() << std::endl;
        }
        */

        // L1 MET
        pat::TriggerObjectRefVector l1mets = htrigger->objects(trigger::TriggerL1ETM);
        if(!l1mets.empty()) {
          if(l1mets.size() != 1) {
            bool found = false;
            for(size_t i=0; i<l1mets.size(); ++i) {
              if(l1mets[i]->coll(l1MetCollection)) {
                l1Met = l1mets[i]->et();
                found = true;
                break;
              }
            }
            if(!found) {
              std::stringstream ss;
              for(size_t i=0; i<l1mets.size(); ++i) {
                ss << l1mets[i]->collection() << " " << l1mets[i]->et() << " ";
              }
              throw cms::Exception("Assert") << "No L1 MET from collection " << l1MetCollection 
                                             << ", have " << l1mets.size() << " L1 MET objects: " << ss.str()
                                             << " at " << __FILE__ << ":" << __LINE__ << std::endl;
            }
          }
          l1Met = l1mets[0]->et();
        }

        // L1 jets
        pat::TriggerObjectRefVector l1cenjets = htrigger->objects(trigger::TriggerL1CenJet);
        for(size_t i=0; i<l1cenjets.size(); ++i)
          if(l1cenjets[i]->coll(l1CenJetCollection))
             l1CenJets.push_back(l1cenjets[i]->p4());
        pat::TriggerObjectRefVector l1taujets = htrigger->objects(trigger::TriggerL1TauJet);
        for(size_t i=0; i<l1taujets.size(); ++i)
          if(l1taujets[i]->coll(l1TauJetCollection))
             l1TauJets.push_back(l1taujets[i]->p4());
        pat::TriggerObjectRefVector l1forjets = htrigger->objects(trigger::TriggerL1ForJet);
        for(size_t i=0; i<l1forjets.size(); ++i)
          if(l1forjets[i]->coll(l1ForJetCollection))
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
