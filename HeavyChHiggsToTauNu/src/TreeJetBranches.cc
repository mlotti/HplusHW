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

  ////////////////////////////////////////

  TreeJetBranches::TreeJetBranches(const edm::ParameterSet& iConfig, bool jetComposition, const std::string& prefix):
    fJetSrc(iConfig.getParameter<edm::InputTag>("src")),
    fPrefix(prefix),
    fEnabled(iConfig.getParameter<bool>("enabled")),
    fDetailsEnabled(iConfig.getParameter<bool>("detailsEnabled")),
    fJetComposition(jetComposition)
  {
    if(!enabled())
      return;

    edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("functions");
    std::vector<std::string> names = pset.getParameterNames();
    fJetsFunctions.reserve(names.size());
    for(size_t i=0; i<names.size(); ++i) {
      fJetsFunctions.push_back(JetFunctionBranch(fPrefix+"f_"+names[i], pset.getParameter<std::string>(names[i])));
    }

    edm::ParameterSet pset2 = iConfig.getParameter<edm::ParameterSet>("pileupIDs");
    std::vector<std::string> names2 = pset2.getParameterNames();
    fJetsPileupIDs.reserve(names2.size());
    for(size_t i=0; i<names2.size(); ++i) {
      edm::ParameterSet pset3 = pset2.getParameter<edm::ParameterSet>(names2[i]);
      fJetsPileupIDs.push_back(PileupID(fPrefix+"puid_"+names2[i], pset3.getParameter<edm::InputTag>("mvaSrc"), pset3.getParameter<edm::InputTag>("flagSrc")));
    }

    edm::ParameterSet pset3 = iConfig.getParameter<edm::ParameterSet>("floats");
    std::vector<std::string> names3 = pset3.getParameterNames();
    fJetsFloats.reserve(names3.size());
    for(size_t i=0; i<names3.size(); ++i) {
      fJetsFloats.push_back(TreeValueMapBranch<float>(fPrefix+names3[i], pset3.getParameter<edm::InputTag>(names3[i])));
    }

    edm::ParameterSet pset4 = iConfig.getParameter<edm::ParameterSet>("bools");
    std::vector<std::string> names4 = pset4.getParameterNames();
    fJetsBools.reserve(names4.size());
    for(size_t i=0; i<names4.size(); ++i) {
      fJetsBools.push_back(TreeValueMapBranch<bool>(fPrefix+names4[i], pset4.getParameter<edm::InputTag>(names4[i])));
    }
  }
  TreeJetBranches::~TreeJetBranches() {}


  void TreeJetBranches::book(TTree *tree) {
    if(!enabled())
      return;

    tree->Branch((fPrefix+"p4").c_str(), &fJets);
    for(size_t i=0; i<fJetsFunctions.size(); ++i) {
      fJetsFunctions[i].book(tree);
    }
    for(size_t i=0; i<fJetsPileupIDs.size(); ++i) {
      fJetsPileupIDs[i].book(tree);
    }
    for(size_t i=0; i<fJetsFloats.size(); ++i) {
      fJetsFloats[i].book(tree);
    }
    for(size_t i=0; i<fJetsBools.size(); ++i) {
      fJetsBools[i].book(tree);
    }

    if(fJetComposition) {
      tree->Branch((fPrefix+"chf").c_str(), &fJetsChf); // charged hadron
      tree->Branch((fPrefix+"nhf").c_str(), &fJetsNhf); // neutral hadron
      tree->Branch((fPrefix+"elf").c_str(), &fJetsElf);  // electron
      tree->Branch((fPrefix+"phf").c_str(), &fJetsPhf);  // photon
      tree->Branch((fPrefix+"muf").c_str(), &fJetsMuf);   // muon
      tree->Branch((fPrefix+"chm").c_str(), &fJetsChm);
      tree->Branch((fPrefix+"nhm").c_str(), &fJetsNhm);
      tree->Branch((fPrefix+"elm").c_str(), &fJetsElm);
      tree->Branch((fPrefix+"phm").c_str(), &fJetsPhm);
      tree->Branch((fPrefix+"mum").c_str(), &fJetsMum);
    }
    if(fDetailsEnabled) {
      tree->Branch((fPrefix+"numberOfDaughters").c_str(), &fJetsNumberOfDaughters);
      tree->Branch((fPrefix+"flavour").c_str(), &fJetsFlavour);
      tree->Branch((fPrefix+"genPartonPdgId").c_str(), &fJetsGenPartonPdgId);
      tree->Branch((fPrefix+"jecToRaw").c_str(), &fJetsJec);
      tree->Branch((fPrefix+"area").c_str(), &fJetsArea);
      tree->Branch((fPrefix+"looseId").c_str(), &fJetsLooseId);
      tree->Branch((fPrefix+"tightId").c_str(), &fJetsTightId);
    }
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
      std::cout << "Jet handle id " << hcands.id() << " ptrvector id " << hcands->ptrVector().id() << " jets id " 
                << jets.id() << " first jet id " << jets[0].id() 
                << " src " << fJetSrc
                << std::endl;
      */

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

      if(fDetailsEnabled) {
        fJetsNumberOfDaughters.push_back(jet.numberOfDaughters());

        fJetsJec.push_back(jet.jecFactor(0));

        fJetsLooseId.push_back( npr > 1 && phf < 0.99 && nhf < 0.99 && ((std::abs(eta) <= 2.4 && elf < 0.99 && chf > 0 && chm > 0) ||
                                                                        std::abs(eta) > 2.4) );
        fJetsTightId.push_back( npr > 1 && phf < 0.99 && nhf < 0.99 && ((std::abs(eta) <= 2.4 && nhf < 0.9 && phf < 0.9 && elf < 0.99 && chf > 0 && chm > 0) ||
                                                                        std::abs(eta) > 2.4) );

        fJetsArea.push_back(jet.jetArea());
      }
    }

    for(size_t i=0; i<fJetsFunctions.size(); ++i) {
      fJetsFunctions[i].setValues(jets);
    }
    for(size_t i=0; i<fJetsPileupIDs.size(); ++i) {
      fJetsPileupIDs[i].setValues(iEvent, jets);
    }
    for(size_t i=0; i<fJetsFloats.size(); ++i) {
      fJetsFloats[i].setValues(iEvent, jets);
    }
    for(size_t i=0; i<fJetsBools.size(); ++i) {
      fJetsBools[i].setValues(iEvent, jets);
    }
  }

  void TreeJetBranches::reset() {
    fJets.clear();
    for(size_t i=0; i<fJetsFunctions.size(); ++i)
      fJetsFunctions[i].reset();
    for(size_t i=0; i<fJetsPileupIDs.size(); ++i) {
      fJetsPileupIDs[i].reset();
    }
    for(size_t i=0; i<fJetsFloats.size(); ++i) {
      fJetsFloats[i].reset();
    }
    for(size_t i=0; i<fJetsBools.size(); ++i) {
      fJetsBools[i].reset();
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
