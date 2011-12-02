#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TreeJetBranches.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TTree.h"

#include<string>

namespace HPlus {
  TreeJetBranches::TreeJetBranches(const edm::ParameterSet& iConfig, bool jetComposition):
    fJetSrc(iConfig.getParameter<edm::InputTag>("jetSrc")),
    fJetComposition(jetComposition)
  {
    edm::ParameterSet pset = iConfig.getParameter<edm::ParameterSet>("jetFunctions");
    std::vector<std::string> names = pset.getParameterNames();
    fJetsFunctions.reserve(names.size());
    for(size_t i=0; i<names.size(); ++i) {
      fJetsFunctions.push_back(JetFunctionBranch("jets_f_"+names[i], pset.getParameter<std::string>(names[i])));
    }
  }
  TreeJetBranches::~TreeJetBranches() {}


  void TreeJetBranches::book(TTree *tree) {
    tree->Branch("jets_p4", &fJets);
    for(size_t i=0; i<fJetsFunctions.size(); ++i) {
      fJetsFunctions[i].book(tree);
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
    tree->Branch("jets_jecToRaw", &fJetsJec);
    tree->Branch("jets_area", &fJetsArea);
    tree->Branch("jets_looseId", &fJetsLooseId);
    tree->Branch("jets_tightId", &fJetsTightId);
  }

  void TreeJetBranches::setValues(const edm::Event& iEvent) {
    edm::Handle<edm::View<pat::Jet> > hjets;
    iEvent.getByLabel(fJetSrc, hjets);

    for(size_t i=0; i<hjets->size(); ++i) {
      const pat::Jet& jet = hjets->at(i);
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

      fJetsJec.push_back(jet.jecFactor(0));


      fJetsLooseId.push_back( npr > 1 && phf < 0.99 && nhf < 0.99 && ((std::abs(eta) <= 2.4 && elf < 0.99 && chf > 0 && chm > 0) ||
                                                                      std::abs(eta) > 2.4) );
      fJetsTightId.push_back( npr > 1 && phf < 0.99 && nhf < 0.99 && ((std::abs(eta) <= 2.4 && nhf < 0.9 && phf < 0.9 && elf < 0.99 && chf > 0 && chm > 0) ||
                                                                      std::abs(eta) > 2.4) );

      fJetsArea.push_back(jet.jetArea());
    }

    for(size_t i=0; i<fJetsFunctions.size(); ++i) {
      fJetsFunctions[i].setValues(*hjets);
    }
  }

  void TreeJetBranches::reset() {
    fJets.clear();
    for(size_t i=0; i<fJetsFunctions.size(); ++i)
      fJetsFunctions[i].reset();

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

    fJetsJec.clear();
    fJetsArea.clear();

    fJetsLooseId.clear();
    fJetsTightId.clear();
  }
}
