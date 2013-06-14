#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeJetBranches.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/PtrVectorCast.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/ValueMap.h"

#include "CMGTools/External/interface/PileupJetIdentifier.h" // Will be at DataFormats/JetReco/interface from 6_x_y

#include "TTree.h"

#include<string>

namespace HPlus {
  TreeJetBranches::PileupID::PileupID(const std::string& prefix, const edm::InputTag& mvaSrc, const edm::InputTag& flagSrc):
    fPrefix(prefix), fMVAValueSrc(mvaSrc), fIDFlagSrc(flagSrc) {
  }
  TreeJetBranches::PileupID::~PileupID() {}
  void TreeJetBranches::PileupID::book(TTree *tree) {
    tree->Branch((fPrefix+"_discriminant").c_str(), &fMVAValue);
    tree->Branch((fPrefix+"_loose").c_str(), &fIDFlagLoose);
    tree->Branch((fPrefix+"_medium").c_str(), &fIDFlagMedium);
    tree->Branch((fPrefix+"_tight").c_str(), &fIDFlagTight);
  }
  void TreeJetBranches::PileupID::setValues(const edm::Event& iEvent, const edm::PtrVector<pat::Jet>& jets) {
    edm::Handle<edm::ValueMap<float> > hmva;
    iEvent.getByLabel(fMVAValueSrc, hmva);

    edm::Handle<edm::ValueMap<int> > hflag;
    iEvent.getByLabel(fIDFlagSrc, hflag);

    for(size_t i=0; i<jets.size(); ++i) {
      fMVAValue.push_back((*hmva)[jets[i]]);

      int flag = (*hflag)[jets[i]];

      fIDFlagLoose.push_back(PileupJetIdentifier::passJetId(flag, PileupJetIdentifier::kLoose));
      fIDFlagMedium.push_back(PileupJetIdentifier::passJetId(flag, PileupJetIdentifier::kMedium));
      fIDFlagTight.push_back(PileupJetIdentifier::passJetId(flag, PileupJetIdentifier::kTight));
    }
  }
  void TreeJetBranches::PileupID::reset() {
    fMVAValue.clear();
    fIDFlagLoose.clear();
    fIDFlagMedium.clear();
    fIDFlagTight.clear();
  }


  TreeJetBranches::TreeJetBranches(const edm::ParameterSet& iConfig, bool jetComposition):
    fJetSrc(iConfig.getParameter<edm::InputTag>("src")),
    fEnabled(iConfig.getParameter<bool>("enabled")),
    fJetComposition(jetComposition)
  {
    if(!enabled())
      return;

    edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("functions");
    std::vector<std::string> names = pset.getParameterNames();
    fJetsFunctions.reserve(names.size());
    for(size_t i=0; i<names.size(); ++i) {
      fJetsFunctions.push_back(JetFunctionBranch("jets_f_"+names[i], pset.getParameter<std::string>(names[i])));
    }

    edm::ParameterSet pset2 = iConfig.getParameter<edm::ParameterSet>("pileupIDs");
    std::vector<std::string> names2 = pset2.getParameterNames();
    fJetsPileupIDs.reserve(names2.size());
    for(size_t i=0; i<names2.size(); ++i) {
      edm::ParameterSet pset3 = pset2.getParameter<edm::ParameterSet>(names2[i]);
      fJetsPileupIDs.push_back(PileupID("jets_puid_"+names2[i], pset3.getParameter<edm::InputTag>("mvaSrc"), pset3.getParameter<edm::InputTag>("flagSrc")));
    }
  }
  TreeJetBranches::~TreeJetBranches() {}


  void TreeJetBranches::book(TTree *tree) {
    if(!enabled())
      return;

    tree->Branch("jets_p4", &fJets);
    for(size_t i=0; i<fJetsFunctions.size(); ++i) {
      fJetsFunctions[i].book(tree);
    }
    for(size_t i=0; i<fJetsPileupIDs.size(); ++i) {
      fJetsPileupIDs[i].book(tree);
    }

    if(fJetComposition) {
      tree->Branch("jets_chf", &fJetsChf); // charged hadron
      tree->Branch("jets_nhf", &fJetsNhf); // neutral hadron
      tree->Branch("jets_elf", &fJetsElf);  // electron
      tree->Branch("jets_phf", &fJetsPhf);  // photon
      tree->Branch("jets_muf", &fJetsMuf);   // muon
      tree->Branch("jets_chm", &fJetsChm);
      tree->Branch("jets_nhm", &fJetsNhm);
      tree->Branch("jets_elm", &fJetsElm);
      tree->Branch("jets_phm", &fJetsPhm);
      tree->Branch("jets_mum", &fJetsMum);
    }
    tree->Branch("jets_numberOfDaughters", &fJetsNumberOfDaughters);
    tree->Branch("jets_flavour", &fJetsFlavour);
    tree->Branch("jets_genPartonPdgId", &fJetsGenPartonPdgId);
    tree->Branch("jets_jecToRaw", &fJetsJec);
    tree->Branch("jets_area", &fJetsArea);
    tree->Branch("jets_looseId", &fJetsLooseId);
    tree->Branch("jets_tightId", &fJetsTightId);
  }

  void TreeJetBranches::setValues(const edm::Event& iEvent) {
    if(!enabled())
      return;

    edm::PtrVector<pat::Jet> jets;
    edm::Handle<edm::View<pat::Jet> > hjets;
    edm::Handle<edm::View<reco::Candidate> > hcands;
    iEvent.getByLabel(fJetSrc, hjets);
    if(hjets.isValid()) {
      jets = hjets->ptrVector();
    }
    else {
      iEvent.getByLabel(fJetSrc, hcands);
      jets = PtrVectorCast<pat::Jet>(hcands->ptrVector());
      /*
      jets = edm::PtrVector<pat::Jet>(hcands->id());
      for(size_t i=0; i<hcands->size(); ++i) {
        edm::Ptr<reco::Candidate> ptr = hcands->ptrAt(i);
        jets.push_back(edm::Ptr<pat::Jet>(ptr.id(), dynamic_cast<const pat::Jet *>(ptr.get()), ptr.key()));
      }
      */
    }
    
    for(size_t i=0; i<jets.size(); ++i) {
      const pat::Jet& jet = *(jets[i]);
      fJets.push_back(jet.p4());

      double eta = jet.eta();

      double chf = jet.chargedHadronEnergyFraction();
      double nhf = jet.neutralHadronEnergyFraction();
      double elf = jet.chargedEmEnergyFraction();
      double phf = jet.neutralEmEnergyFraction();
      // for some reason the muonEnergyFraction is calculated w.r.t. *corrected* energy in pat::Jet
      double muf = jet.muonEnergy() / (jet.jecFactor(0) * jet.energy());

      int chm = jet.chargedHadronMultiplicity();
      int npr = jet.chargedMultiplicity() + jet.neutralMultiplicity();
      if (!iEvent.isRealData()) {
	const reco::GenParticle* myParticle = jet.genParton();
        int pdgId = 0;
	if (myParticle != 0 ) pdgId = myParticle->pdgId();

        fJetsFlavour.push_back(jet.partonFlavour());
        fJetsGenPartonPdgId.push_back(pdgId);
      }

      if(fJetComposition) {
        double sum = chf+nhf+elf+phf+muf;
        if(std::abs(sum - 1.0) > 0.000001) {
          throw cms::Exception("Assert") << "The assumption that chf+nhf+elf+phf+muf=1 failed, the sum was " << (chf+nhf+elf+phf+muf)
                                         << " the sum-1 was " << (sum-1.0)
                                         << " Jet " << i << " pt " << jet.pt() << " eta " << eta
                                         << " chf " << chf << " nhf " << nhf << " elf " << elf << " phf " << phf << " muf " << muf
                                         << std::endl;
        }

        fJetsChf.push_back(chf);
        fJetsNhf.push_back(nhf);
        fJetsElf.push_back(elf);
        fJetsPhf.push_back(phf);
        fJetsMuf.push_back(muf);
      
        fJetsChm.push_back(chm);
        fJetsNhm.push_back(jet.neutralHadronMultiplicity());
        fJetsElm.push_back(jet.electronMultiplicity());
        fJetsPhm.push_back(jet.photonMultiplicity());
        fJetsMum.push_back(jet.muonMultiplicity());
      }

      fJetsNumberOfDaughters.push_back(jet.numberOfDaughters());

      fJetsJec.push_back(jet.jecFactor(0));


      fJetsLooseId.push_back( npr > 1 && phf < 0.99 && nhf < 0.99 && ((std::abs(eta) <= 2.4 && elf < 0.99 && chf > 0 && chm > 0) ||
                                                                      std::abs(eta) > 2.4) );
      fJetsTightId.push_back( npr > 1 && phf < 0.99 && nhf < 0.99 && ((std::abs(eta) <= 2.4 && nhf < 0.9 && phf < 0.9 && elf < 0.99 && chf > 0 && chm > 0) ||
                                                                      std::abs(eta) > 2.4) );

      fJetsArea.push_back(jet.jetArea());
    }

    for(size_t i=0; i<fJetsFunctions.size(); ++i) {
      fJetsFunctions[i].setValues(jets);
    }
    for(size_t i=0; i<fJetsPileupIDs.size(); ++i) {
      fJetsPileupIDs[i].setValues(iEvent, jets);
    }
  }

  void TreeJetBranches::reset() {
    fJets.clear();
    for(size_t i=0; i<fJetsFunctions.size(); ++i)
      fJetsFunctions[i].reset();
    for(size_t i=0; i<fJetsPileupIDs.size(); ++i) {
      fJetsPileupIDs[i].reset();
    }

    if(fJetComposition) {
      fJetsChf.clear();
      fJetsNhf.clear();
      fJetsElf.clear();
      fJetsPhf.clear();
      fJetsMuf.clear();
      fJetsChm.clear();
      fJetsNhm.clear();
      fJetsElm.clear();
      fJetsPhm.clear();
      fJetsMum.clear();
    }
    fJetsNumberOfDaughters.clear();
    fJetsFlavour.clear();
    fJetsGenPartonPdgId.clear();

    fJetsJec.clear();
    fJetsArea.clear();

    fJetsLooseId.clear();
    fJetsTightId.clear();
  }
}
