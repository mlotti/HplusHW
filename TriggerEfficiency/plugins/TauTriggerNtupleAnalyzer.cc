#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeEventBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeFunctionBranch.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include "TTree.h"

#include<vector>

class TauTriggerNtupleAnalyzer: public edm::EDAnalyzer {
public:
  TauTriggerNtupleAnalyzer(const edm::ParameterSet& iConfig);

  ~TauTriggerNtupleAnalyzer();

private:
  void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  void reset();

  edm::InputTag fMuonSrc;
  edm::InputTag fTauSrc;
  edm::InputTag fMuonTauSrc;
  edm::InputTag fPatTriggerSrc;
  edm::InputTag fGenParticleSrc;

  TTree *fTree;
  
  typedef math::XYZTLorentzVector XYZTLorentzVector;

  struct TauId {
    TauId(const std::string& n): name(n) {}
    void reset() { values.clear(); }
    std::string name;
    std::vector<double> values;
  };
  typedef HPlus::TreeFunctionVectorBranch<pat::Muon> MuonFunctionBranch;

  struct TriggerPath {
    TriggerPath(const std::string& n): name(n), value(false) {}
    void reset() { value = false; }
    std::string name;
    bool value;
  };

  HPlus::TreeEventBranches fEventBranches;

  std::vector<TriggerPath> fTriggerPaths;

  // Tau branches
  std::vector<XYZTLorentzVector> fTaus;
  std::vector<XYZTLorentzVector> fTausLeadingChCand;
  std::vector<double> fTausEmFraction;
  std::vector<unsigned int> fTausSignalChCands;
  std::vector<TauId> fTausId;
  std::vector<int> fTausPdgId;
  std::vector<int> fTausMotherPdgId;
  std::vector<int> fTausGrandMotherPdgId;
  //std::vector<size_t> fTausClosestMuonIndex;
  //std::vector<double> fTausClosestMuonDR;

  // Muon branches
  std::vector<XYZTLorentzVector> fMuons;
  std::vector<MuonFunctionBranch> fMuonsFunctions;
  //std::vector<size_t> fMuonsClosestTauIndex;
  //std::vector<double> fTausClosestMuonDR;
  std::vector<int> fMuonsPdgId;
  std::vector<int> fMuonsMotherPdgId;
  std::vector<int> fMuonsGrandMotherPdgId;

  // Pair branches
  std::vector<XYZTLorentzVector> fPairs;
  std::vector<int> fPairsTauIndex;
  std::vector<int> fPairsMuonIndex;
  std::vector<double> fPairsDeltaR;
};

TauTriggerNtupleAnalyzer::TauTriggerNtupleAnalyzer(const edm::ParameterSet& iConfig):
  fMuonSrc(iConfig.getParameter<edm::InputTag>("muonSrc")),
  fTauSrc(iConfig.getParameter<edm::InputTag>("tauSrc")),
  fMuonTauSrc(iConfig.getParameter<edm::InputTag>("muonTauSrc")),
  fPatTriggerSrc(iConfig.getParameter<edm::InputTag>("patTriggerEvent")),
  fGenParticleSrc(iConfig.getParameter<edm::InputTag>("genParticleSrc"))
{
  std::vector<std::string> triggerPaths = iConfig.getParameter<std::vector<std::string> >("triggerPaths");
  fTriggerPaths.reserve(triggerPaths.size());
  for(size_t i=0; i<triggerPaths.size(); ++i) {
    fTriggerPaths.push_back(triggerPaths[i]);
  }

  edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("muonFunctions");
  std::vector<std::string> names = pset.getParameterNames();
  fMuonsFunctions.reserve(names.size());
  for(size_t i=0; i<names.size(); ++i) {
    fMuonsFunctions.push_back(MuonFunctionBranch(names[i], pset.getParameter<std::string>(names[i])));
  }

  edm::Service<TFileService> fs;
  fTree = fs->make<TTree>("tree", "Tree");

  fEventBranches.book(fTree);

  for(size_t i=0; i<fTriggerPaths.size(); ++i) {
    fTree->Branch(fTriggerPaths[i].name.c_str(), &(fTriggerPaths[i].value));
  }

  fTree->Branch("taus_p4", &fTaus);
  fTree->Branch("taus_leadPFChargedHadrCand_p4", &fTausLeadingChCand);
  fTree->Branch("taus_signalPFChargedHadrCands_n", &fTausSignalChCands);
  fTree->Branch("taus_emFraction", &fTausEmFraction);
  for(size_t i=0; i<fTausId.size(); ++i) {
    fTree->Branch( ("taus_id_"+fTausId[i].name).c_str(), &(fTausId[i].values) );
  }
  fTree->Branch("taus_pdgid", &fTausPdgId);
  fTree->Branch("taus_mother_pdgid", &fTausMotherPdgId);
  fTree->Branch("taus_grandmother_pdgid", &fTausGrandMotherPdgId);

  fTree->Branch("muons_p4", &fMuons);
  for(size_t i=0; i<fMuonsFunctions.size(); ++i) {
    fMuonsFunctions[i].book(fTree);
  }
  fTree->Branch("muons_pdgid", &fMuonsPdgId);
  fTree->Branch("muons_mother_pdgid", &fMuonsMotherPdgId);
  fTree->Branch("muons_grandmother_pdgid", &fMuonsGrandMotherPdgId);

  fTree->Branch("pairs_p4", &fPairs);
  fTree->Branch("pairs_tauIndex", &fPairsTauIndex);
  fTree->Branch("pairs_muonIndex", &fPairsMuonIndex);
  fTree->Branch("pairs_deltaR", &fPairsDeltaR);
}

TauTriggerNtupleAnalyzer::~TauTriggerNtupleAnalyzer() {}

void TauTriggerNtupleAnalyzer::reset() {
  fEventBranches.reset();

  for(size_t i=0; i< fTriggerPaths.size(); ++i) {
    fTriggerPaths[i].reset();
  }

  fTaus.clear();
  fTausLeadingChCand.clear();
  fTausEmFraction.clear();
  fTausSignalChCands.clear();
  for(size_t i=0; i<fTausId.size(); ++i)
    fTausId[i].reset();
  fTausPdgId.clear();
  fTausMotherPdgId.clear();
  fTausGrandMotherPdgId.clear();

  fMuons.clear();
  for(size_t i=0; i<fMuonsFunctions.size(); ++i)
    fMuonsFunctions[i].reset();
  fMuonsPdgId.clear();
  fMuonsMotherPdgId.clear();
  fMuonsGrandMotherPdgId.clear();

  fPairs.clear();
  fPairsTauIndex.clear();
  fPairsMuonIndex.clear();
  fPairsDeltaR.clear();
}

void TauTriggerNtupleAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  fEventBranches.setValues(iEvent);

  edm::Handle<edm::View<pat::Tau> > htaus;
  iEvent.getByLabel(fTauSrc, htaus);

  edm::Handle<edm::View<pat::Muon> > hmuons;
  iEvent.getByLabel(fMuonSrc, hmuons);

  edm::Handle<edm::View<reco::CompositeCandidate> > hpairs;
  iEvent.getByLabel(fMuonTauSrc, hpairs);

  edm::Handle<pat::TriggerEvent> htrigger;
  iEvent.getByLabel(fPatTriggerSrc, htrigger);

  edm::Handle<edm::View<reco::GenParticle> > hgenparticles;
  if(!iEvent.isRealData())
    iEvent.getByLabel(fGenParticleSrc, hgenparticles);

  // Trigger paths
  pat::TriggerPathRefVector acceptedPaths = htrigger->acceptedPaths();
  for(size_t i=0; i<fTriggerPaths.size(); ++i) {
    for(pat::TriggerPathRefVector::const_iterator iter = acceptedPaths.begin(); iter != acceptedPaths.end(); ++iter) {
      if((*iter)->name() == fTriggerPaths[i].name && (*iter)->wasAccept()) {
        fTriggerPaths[i].value = true;
      }
    }
  }

  // Taus
  for(size_t i=0; i<htaus->size(); ++i) {
    const pat::Tau& tau = htaus->at(i);
    fTaus.push_back(tau.p4());
    fTausLeadingChCand.push_back(tau.leadPFChargedHadrCand()->p4());
    fTausEmFraction.push_back(tau.emFraction());
    fTausSignalChCands.push_back(tau.signalPFChargedHadrCands().size());
    for(size_t i=0; i<fTausId.size(); ++i) {
      fTausId[i].values.push_back(tau.tauID(fTausId[i].name) > 0.5);
    }

    if(!iEvent.isRealData()) {
      const reco::GenParticle *gen = HPlus::GenParticleTools::findMatching(hgenparticles->begin(), hgenparticles->end(), 15, tau, 0.5);
      if(!gen) {
        gen = HPlus::GenParticleTools::findMatching(hgenparticles->begin(), hgenparticles->end(), 13, tau, 0.5);
      }
      if(!gen) {
        gen = HPlus::GenParticleTools::findMatching(hgenparticles->begin(), hgenparticles->end(), 11, tau, 0.5);
      }

      int pdgId = 0;
      int motherPdgId = 0;
      int grandMotherPdgId = 0;
      if(gen) {
        pdgId = gen->pdgId();
        const reco::GenParticle *mother = HPlus::GenParticleTools::findMother(gen);
        if(mother) {
          motherPdgId = mother->pdgId();
          const reco::GenParticle *grandMother = HPlus::GenParticleTools::findMother(mother);
          if(grandMother)
            grandMotherPdgId = grandMother->pdgId();
        }
      }

      fTausPdgId.push_back(pdgId);
      fTausMotherPdgId.push_back(motherPdgId);
      fTausGrandMotherPdgId.push_back(motherPdgId);
    }
  }

  // Muons
  for(size_t i=0; i<hmuons->size(); ++i) {
    const pat::Muon& muon = hmuons->at(i);
    fMuons.push_back(muon.p4());

    if(!iEvent.isRealData()) {
      const reco::GenParticle *gen = HPlus::GenParticleTools::findMatching(hgenparticles->begin(), hgenparticles->end(), 13, muon, 0.5);

      int pdgId = 0;
      int motherPdgId = 0;
      int grandMotherPdgId = 0;
      if(gen) {
        pdgId = gen->pdgId();
        const reco::GenParticle *mother = HPlus::GenParticleTools::findMother(gen);
        if(mother) {
          motherPdgId = mother->pdgId();
          const reco::GenParticle *grandMother = HPlus::GenParticleTools::findMother(mother);
          if(grandMother)
            grandMotherPdgId = grandMother->pdgId();
        }
      }

      fMuonsPdgId.push_back(pdgId);
      fMuonsMotherPdgId.push_back(motherPdgId);
      fMuonsGrandMotherPdgId.push_back(motherPdgId);
    }
  }
  for(size_t i=0; i<fMuonsFunctions.size(); ++i) {
    fMuonsFunctions[i].setValues(*hmuons);
  }

  // Muon+Tau pairs
  for(size_t i=0; i<hpairs->size(); ++i) {
    const reco::CompositeCandidate& pair = hpairs->at(i);
    if(pair.numberOfDaughters() != 2)
      throw cms::Exception("Assert") << "Got mu-tau pairs with " << pair.numberOfDaughters() << " daughters != 2 from " << fMuonTauSrc.encode() << std::endl;

    const pat::Muon *muon = dynamic_cast<const pat::Muon *>(pair.daughter(0));
    const pat::Tau *tau = dynamic_cast<const pat::Tau *>(pair.daughter(1));
    if(!muon)
      throw cms::Exception("Assert") << "Daughter 0 was not pat::Muon from " << fMuonTauSrc.encode() << std::endl;
    if(!tau)
      throw cms::Exception("Assert") << "Daughter 1 was not pat::Muon from " << fMuonTauSrc.encode() << std::endl;

    int index = -1;
    for(size_t i=0; i<hmuons->size(); ++i) {
      if(reco::deltaR(*muon, hmuons->at(i)) < 0.01) {
        index = i;
      }
    }
    if(index < 0)
      throw cms::Exception("Assert") << "Didn't find muon from pair " << fMuonTauSrc.encode() << " from muon collection " << fMuonSrc.encode() << std::endl;
    fPairsMuonIndex.push_back(index);
    
    index = -1;
    for(size_t i=0; i<htaus->size(); ++i) {
      if(reco::deltaR(*tau, htaus->at(i)) < 0.01) {
        index = i;
      }
    }
    if(index < 0)
      throw cms::Exception("Assert") << "Didn't find tau from pair " << fMuonTauSrc.encode() << " from muon collection " << fMuonSrc.encode() << std::endl;
    fPairsTauIndex.push_back(index);

    fPairs.push_back(pair.p4());
    fPairsDeltaR.push_back(reco::deltaR(*muon, *tau));

  }

  reset();
}

DEFINE_FWK_MODULE(TauTriggerNtupleAnalyzer);
