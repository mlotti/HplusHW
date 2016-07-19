#include "HiggsAnalysis/MiniAOD2TTree/interface/GenParticleDumper.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/NtupleAnalysis_fwd.h"
#include "HiggsAnalysis/MiniAOD2TTree/interface/GenParticleTools.h"


#include "TLorentzVector.h"

GenParticleDumper::GenParticleDumper(edm::ConsumesCollector&& iConsumesCollector, std::vector<edm::ParameterSet>& psets){
  inputCollections = psets;
  booked           = false;

  // General particle list
  pt  = new std::vector<double>[inputCollections.size()];
  eta = new std::vector<double>[inputCollections.size()];    
  phi = new std::vector<double>[inputCollections.size()];    
  e   = new std::vector<double>[inputCollections.size()];    
  pdgId  = new std::vector<short>[inputCollections.size()];
  status = new std::vector<short>[inputCollections.size()];
  charge = new std::vector<short>[inputCollections.size()];
  mother = new std::vector<short>[inputCollections.size()];
  vtxX   = new std::vector<double>[inputCollections.size()];
  vtxY   = new std::vector<double>[inputCollections.size()];
  vtxZ   = new std::vector<double>[inputCollections.size()];

  // Electrons
  electrons = new FourVectorDumper[inputCollections.size()];
  
  // Muons
  muons = new FourVectorDumper[inputCollections.size()];
  
  // Taus
  taus = new FourVectorDumper[inputCollections.size()];
  visibleTaus = new FourVectorDumper[inputCollections.size()];
  tauNcharged = new std::vector<short>[inputCollections.size()];
  tauNPi0 = new std::vector<short>[inputCollections.size()];
  tauRtau = new std::vector<double>[inputCollections.size()];
  tauAssociatedWithHpm = new short[inputCollections.size()];
  tauMother = new std::vector<short>[inputCollections.size()];
  tauDecaysToElectron = new std::vector<bool>[inputCollections.size()];
  tauDecaysToMuon = new std::vector<bool>[inputCollections.size()];
  tauSpinEffects = new std::vector<double>[inputCollections.size()];
  tauNeutrinos = new FourVectorDumper[inputCollections.size()];
  
  // Neutrinos
  neutrinos = new FourVectorDumper[inputCollections.size()];
  
  // Top info
  top = new FourVectorDumper[inputCollections.size()];
  topDecayMode = new std::vector<short>[inputCollections.size()];
  topBQuark = new FourVectorDumper[inputCollections.size()];
  topBJetContainsLeptons = new std::vector<bool>[inputCollections.size()];
  topBNeutrinos = new FourVectorDumper[inputCollections.size()];
  
  // W info
  W = new FourVectorDumper[inputCollections.size()];
  WDecayMode = new std::vector<short>[inputCollections.size()];
  WNeutrinos = new FourVectorDumper[inputCollections.size()];
  
  // H+ info
  Hplus = new FourVectorDumper[inputCollections.size()];
  HplusNeutrinos = new FourVectorDumper[inputCollections.size()];

  //handle = new edm::Handle<reco::GenParticleCollection>[inputCollections.size()];
  token = new edm::EDGetTokenT<reco::GenParticleCollection>[inputCollections.size()];
  for(size_t i = 0; i < inputCollections.size(); ++i){
    edm::InputTag inputtag = inputCollections[i].getParameter<edm::InputTag>("src");
    token[i] = iConsumesCollector.consumes<reco::GenParticleCollection>(inputtag);
  }
  
  useFilter = false;
  for(size_t i = 0; i < inputCollections.size(); ++i){
      bool param = inputCollections[i].getUntrackedParameter<bool>("filter",false);
      if(param) useFilter = true;
  }
}

GenParticleDumper::~GenParticleDumper(){}

void GenParticleDumper::book(TTree* tree){
  booked = true;
  for(size_t i = 0; i < inputCollections.size(); ++i){
    std::string name = inputCollections[i].getUntrackedParameter<std::string>("branchname","");
    if(name.length() == 0) name = inputCollections[i].getParameter<edm::InputTag>("src").label();

    if (inputCollections[i].getUntrackedParameter<bool>("saveAllGenParticles", false)) {
      tree->Branch((name+"_pt").c_str()    , &pt[i]);
      tree->Branch((name+"_eta").c_str()   , &eta[i]);
      tree->Branch((name+"_phi").c_str()   , &phi[i]);
      tree->Branch((name+"_e").c_str()     , &e[i]);
      tree->Branch((name+"_pdgId").c_str() , &pdgId[i]);
      tree->Branch((name+"_mother").c_str(), &mother[i]);
      tree->Branch((name+"_status").c_str(), &status[i]);
      tree->Branch((name+"_charge").c_str(), &charge[i]);
      tree->Branch((name+"_vtxX").c_str()  , &vtxX[i]);
      tree->Branch((name+"_vtxY").c_str()  , &vtxY[i]);
      tree->Branch((name+"_vtxZ").c_str()  , &vtxZ[i]);
    }
    if (inputCollections[i].getUntrackedParameter<bool>("saveGenElectrons", false)) {
      electrons[i].book(tree, name, "GenElectron");
    }
    if (inputCollections[i].getUntrackedParameter<bool>("saveGenMuons", false)) {
      muons[i].book(tree, name, "GenMuon");
    }
    if (inputCollections[i].getUntrackedParameter<bool>("saveGenTaus", false)) {
      taus[i].book(tree, name, "GenTau");
      visibleTaus[i].book(tree, name, "GenVisibleTau");
      tree->Branch((name+"_GenTauProngs").c_str(),&tauNcharged[i]);
      tree->Branch((name+"_GenTauNpi0").c_str(),&tauNPi0[i]);
      tree->Branch((name+"_GenTauRtau").c_str(),&tauRtau[i]);
      tree->Branch((name+"_GenTauAssociatedWithHpm").c_str(),&tauAssociatedWithHpm[i]);
      tree->Branch((name+"_GenTauMother").c_str(),&tauMother[i]);
      tree->Branch((name+"_GenTauDecaysToElectron").c_str(),&tauDecaysToElectron[i]);
      tree->Branch((name+"_GenTauDecaysToMuon").c_str(),&tauDecaysToMuon[i]);
      tree->Branch((name+"_GenTauSpinEffects").c_str(),&tauSpinEffects[i]);
      tauNeutrinos[i].book(tree, name, "GenTauNeutrinos");
    }
    if (inputCollections[i].getUntrackedParameter<bool>("saveGenNeutrinos", false)) {
      neutrinos[i].book(tree, name, "GenNeutrinos");
    }
    if (inputCollections[i].getUntrackedParameter<bool>("saveTopInfo", false)) {
      top[i].book(tree, name, "GenTop");
      tree->Branch((name+"_GenTopDecayMode").c_str(),&topDecayMode[i]);
      topBQuark[i].book(tree, name, "GenTopBQuark");
      tree->Branch((name+"_GenTopBJetContainsLeptons").c_str(),&topBJetContainsLeptons[i]);
      topBNeutrinos[i].book(tree, name, "GenTopBNeutrinos");
    }
    if (inputCollections[i].getUntrackedParameter<bool>("saveWInfo", false)) {
      W[i].book(tree, name, "GenW");
      tree->Branch((name+"_GenWDecayMode").c_str(),&WDecayMode[i]);
      WNeutrinos[i].book(tree, name, "GenWNeutrinos");
    }
    if (inputCollections[i].getUntrackedParameter<bool>("saveHplusInfo", false)) {
      Hplus[i].book(tree, name, "GenHplus");
      HplusNeutrinos[i].book(tree, name, "GenHplusNeutrinos");
    }
  }
}

bool GenParticleDumper::fill(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!booked) return true;

  for(size_t ic = 0; ic < inputCollections.size(); ++ic){
    //iEvent.getByLabel(inputtag, handle);
    edm::Handle<reco::GenParticleCollection> handle;
    iEvent.getByToken(token[ic], handle);
    if(handle.isValid()){
      // General particle list
      if (inputCollections[ic].getUntrackedParameter<bool>("saveAllGenParticles", false)) {
        for(size_t i = 0; i < handle->size(); ++i) {
          const reco::Candidate & gp = handle->at(i);
          pt[ic].push_back(gp.pt());
          eta[ic].push_back(gp.eta());
          phi[ic].push_back(gp.phi());
          e[ic].push_back(gp.energy());   
          pdgId[ic].push_back(gp.pdgId());
	  status[ic].push_back(gp.status());
	  charge[ic].push_back(gp.charge());
	  vtxX[ic].push_back(gp.vx());
	  vtxY[ic].push_back(gp.vy());
	  vtxZ[ic].push_back(gp.vz());
    
          // Find mother index
          short index = -1;
          if (gp.mother() != nullptr) {
            for(size_t j = 0; j < handle->size(); ++j) {
              if (gp.mother() == &(handle->at(j)))
                index = j;
            }
          }
          mother[ic].push_back(index);
        }
      }
      // MC electrons
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenElectrons", false)) {
        saveLeptons(handle, electrons[ic], 11);
      }
      // MC muons
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenMuons", false)) {
        saveLeptons(handle, muons[ic], 13);
      }
      // MC taus
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenTaus", false)) {
        tauAssociatedWithHpm[ic] = -1;
        std::vector<const reco::Candidate*> tauLeptons = GenParticleTools::findParticles(handle, 15);
        size_t tauIndex = 0;
        for (auto& p: tauLeptons) {
          // 4-momentum of tau lepton
          taus[ic].add(p->pt(), p->eta(), p->phi(), p->energy());
          // tau offspring information
          std::vector<const reco::Candidate*> offspring = GenParticleTools::findOffspring(handle, p);
          short nCharged = 0;
          short nPi0 = 0;
          bool decaysToElectron = false;
          bool decaysToMuon = false;
          math::XYZTLorentzVector neutrinoMomentum;
          for (auto&po: offspring) {
            int absPid = std::abs(po->pdgId());
            if (absPid == 11) { // Electron
              ++nCharged;
              decaysToElectron = true;
            } else if (absPid == 13) { // Muon
              ++nCharged;
              decaysToMuon = true;
            } else if (absPid == 111) { // Pi0
              ++nPi0;
            } else if (absPid == 211 || absPid == 321) { // Pi+, K+
              ++nCharged;
            } else if (absPid == 12 || absPid == 14 || absPid == 16) { // neutrino
              neutrinoMomentum += po->p4();
            }
          }
          // Visible tau
          math::XYZTLorentzVector visibleTau = p->p4() - neutrinoMomentum;
          visibleTaus[ic].add(visibleTau.pt(), visibleTau.eta(), visibleTau.phi(), visibleTau.energy());
          // Other offspring information
          tauNcharged[ic].push_back(nCharged);
          tauNPi0[ic].push_back(nPi0);
          tauDecaysToElectron[ic].push_back(decaysToElectron);
          tauDecaysToMuon[ic].push_back(decaysToMuon);
          tauNeutrinos[ic].add(neutrinoMomentum.pt(), neutrinoMomentum.eta(), neutrinoMomentum.phi(), neutrinoMomentum.energy());
          // rtau and spineffects
          saveHelicityInformation(visibleTau, offspring, ic);
          // tau ancestry information
          std::vector<const reco::Candidate*> ancestry = GenParticleTools::findAncestry(handle, p);
          int tauOriginCode = kOriginUnknown;
          for (auto& p: ancestry) {
            int absPid = std::abs(p->pdgId());
            if (absPid == kFromZ || absPid == kFromW) {
              tauOriginCode = absPid;
            } else if (absPid == kFromHplus) {
              tauOriginCode = absPid;
              tauAssociatedWithHpm[ic] = tauIndex;
            }
          }
          if (tauOriginCode == kOriginUnknown && ancestry.size() > 0) {
            tauOriginCode = kFromOtherSource;
          }
          tauMother[ic].push_back(tauOriginCode);
          ++tauIndex;
        }
      }
      // Neutrinos
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenNeutrinos", false)) {
        saveLeptons(handle, neutrinos[ic], 12);
        saveLeptons(handle, neutrinos[ic], 14);
        saveLeptons(handle, neutrinos[ic], 16);
      }
      // Top info
      if (inputCollections[ic].getUntrackedParameter<bool>("saveTopInfo", false)) {
        std::vector<const reco::Candidate*> tops = GenParticleTools::findParticles(handle, 6);
        for (auto& p: tops) {
          short topDecay = kTopDecayUnknown;
          bool bToLeptons = false;
          math::XYZTLorentzVector bquark;
          math::XYZTLorentzVector bNeutrinos;
          std::vector<const reco::Candidate*> offspring = GenParticleTools::findOffspring(handle, p);
          for (auto& po: offspring) {
            short absPid = std::abs(po->pdgId());
            if (absPid == 5) {
              // b quark from top decay
              bquark = po->p4();
              std::vector<const reco::Candidate*> boffspring = GenParticleTools::findOffspring(handle, po);
              for (auto& pob: boffspring) {
                short bPid = std::abs(pob->pdgId());
                if (bPid == 11 || bPid == 13 || bPid == 15) {
                  bToLeptons = true;
                } else if (bPid == 12 || bPid == 14 || bPid == 16) {
                  bNeutrinos += pob->p4();
                }
              }
            } else if (absPid == 11 || absPid == 13 || absPid == 15) {
              std::vector<const reco::Candidate*> ancestry = GenParticleTools::findAncestry(handle, po);
              bool ancestryContainsBQuark = false;
              for (auto& pa: ancestry) {
                if (std::abs(pa->pdgId()) == 5)
                  ancestryContainsBQuark = true;
              }
              if (!ancestryContainsBQuark) {
                topDecay = absPid;
              }
            }
          }
          top[ic].add(p->pt(), p->eta(), p->phi(), p->energy());
          if (topDecay == kTopDecayUnknown && offspring.size() > 0)
            topDecay = kTopToHadrons;
          topDecayMode[ic].push_back(topDecay);
          topBQuark[ic].add(bquark.pt(), bquark.eta(), bquark.phi(), bquark.energy());
          topBJetContainsLeptons[ic].push_back(bToLeptons);
          topBNeutrinos[ic].add(bNeutrinos.pt(), bNeutrinos.eta(), bNeutrinos.phi(), bNeutrinos.energy());
        }
      }
      // W info
      if (inputCollections[ic].getUntrackedParameter<bool>("saveWInfo", false)) {
        std::vector<const reco::Candidate*> Ws = GenParticleTools::findParticles(handle, 24);
        for (auto& p: Ws) {
          short WDecay = kWDecayUnknown;
          math::XYZTLorentzVector neutrinos;
          std::vector<const reco::Candidate*> offspring = GenParticleTools::findOffspring(handle, p);
          for (auto& po: offspring) {
            short absPid = std::abs(po->pdgId());
            if (absPid == 11 || absPid == 13 || absPid == 15) {
              WDecay = absPid;
            } else if (absPid == 12 || absPid == 14 || absPid == 16) {
              neutrinos += p->p4();
            }
          }
          W[ic].add(p->pt(), p->eta(), p->phi(), p->energy());
          if (WDecay == kWDecayUnknown && offspring.size() > 0)
            WDecay = kWToHadrons;
          WDecayMode[ic].push_back(WDecay);
          WNeutrinos[ic].add(neutrinos.pt(), neutrinos.eta(), neutrinos.phi(), neutrinos.energy());
        }
      }
      // H+ info
      if (inputCollections[ic].getUntrackedParameter<bool>("saveHplusInfo", false)) {
        std::vector<const reco::Candidate*> higgses = GenParticleTools::findParticles(handle, 37);
        for (auto& p: higgses) {
          math::XYZTLorentzVector neutrinos;
          std::vector<const reco::Candidate*> offspring = GenParticleTools::findOffspring(handle, p);
          for (auto& po: offspring) {
            short absPid = std::abs(po->pdgId());
            if (absPid == 12 || absPid == 14 || absPid == 16) {
              neutrinos += p->p4();
            }
          }
          Hplus[ic].add(p->pt(), p->eta(), p->phi(), p->energy());
          HplusNeutrinos[ic].add(neutrinos.pt(), neutrinos.eta(), neutrinos.phi(), neutrinos.energy());
        }
      }
    } // Handle is valid
  } // Loop over input collections
  return filter();
}

bool GenParticleDumper::filter(){
  if(!useFilter) return true;
  return true;
}

void GenParticleDumper::reset(){
  if(booked){
    for(size_t ic = 0; ic < inputCollections.size(); ++ic){
      if (inputCollections[ic].getUntrackedParameter<bool>("saveAllGenParticles", false)) {
        pt[ic].clear();
        eta[ic].clear();
        phi[ic].clear();
        e[ic].clear();
        //et[ic].clear();
        pdgId[ic].clear();
        status[ic].clear();
        charge[ic].clear();
        mother[ic].clear();
        vtxX[ic].clear();
        vtxY[ic].clear();
        vtxZ[ic].clear();
      }
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenElectrons", false)) {
        electrons[ic].reset();
      }
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenMuons", false)) {
        muons[ic].reset();
      }
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenTaus", false)) {
        taus[ic].reset();
        visibleTaus[ic].reset();
        tauNcharged[ic].clear();
        tauNPi0[ic].clear();
        tauRtau[ic].clear();
        tauMother[ic].clear();
        tauDecaysToElectron[ic].clear();
        tauDecaysToMuon[ic].clear();
        tauSpinEffects[ic].clear();
        tauNeutrinos[ic].reset();
      }
      if (inputCollections[ic].getUntrackedParameter<bool>("saveGenNeutrinos", false)) {
        neutrinos[ic].reset();
      }
      if (inputCollections[ic].getUntrackedParameter<bool>("saveTopInfo", false)) {
        top[ic].reset();
        topDecayMode[ic].clear();
        topBQuark[ic].reset();
        topBJetContainsLeptons[ic].clear();
        topBNeutrinos[ic].reset();
      }
      if (inputCollections[ic].getUntrackedParameter<bool>("saveWInfo", false)) {
        W[ic].reset();
        WDecayMode[ic].clear();
        WNeutrinos[ic].reset();
      }
      if (inputCollections[ic].getUntrackedParameter<bool>("saveHplusInfo", false)) {
        Hplus[ic].reset();
        HplusNeutrinos[ic].reset();
      }
    }
  }
}

void GenParticleDumper::saveLeptons(edm::Handle<reco::GenParticleCollection>& handle, FourVectorDumper& dumper, int pID) {
  std::vector<const reco::Candidate*> matches = GenParticleTools::findParticles(handle, pID);
  for (auto& p: matches) {
    dumper.add(p->pt(), p->eta(), p->phi(), p->energy());
  }
}

void GenParticleDumper::saveHelicityInformation(math::XYZTLorentzVector& visibleTau, const std::vector<const reco::Candidate*>& offspring, const size_t index) {
  // Find leading ch. particle
  math::XYZTLorentzVector ldgPion;
  for (auto& p: offspring) {
    if (std::abs(p->pdgId()) == 211) {
      if (p->p4().P() > ldgPion.P()) {
        ldgPion = p->p4();
      }
    }
  }
  // Save rtau
  double rtau = -1;
  if (visibleTau.P() > 0.0) {
    rtau = ldgPion.P() / visibleTau.P();
  }
  tauRtau[index].push_back(rtau);
  // Save spin effects info
  TLorentzVector ldgPionBoosted(ldgPion.px(), ldgPion.py(), ldgPion.pz(), ldgPion.energy());
  TLorentzVector visibleTauForBoost(visibleTau.px(), visibleTau.py(), visibleTau.pz(), visibleTau.energy());
  ldgPionBoosted.Boost(-1.0 * visibleTauForBoost.BoostVector());
  tauSpinEffects[index].push_back(ldgPionBoosted.E() / 1.778 / 2.0);
}
 
void GenParticleDumper::printDescendants(edm::Handle<reco::GenParticleCollection>& handle, const reco::Candidate* p) {
  std::vector<const reco::Candidate*> offspring = GenParticleTools::findOffspring(handle, p);
  std::cout << "Offspring for pid=" << p->pdgId() << std::endl;
  for (auto& p: offspring) {
    std::cout << "  " << p->pdgId() << std::endl;
  }
}
