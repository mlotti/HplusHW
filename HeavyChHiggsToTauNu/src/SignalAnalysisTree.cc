#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"

#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Framework/interface/Event.h"

#include "CommonTools/Utils/interface/TFileDirectory.h"

#include "TTree.h"

namespace HPlus {
  SignalAnalysisTree::SignalAnalysisTree(const std::string& bDiscriminator):
    fBdiscriminator(bDiscriminator), fTree(0)
  {
    reset();
  }
  SignalAnalysisTree::~SignalAnalysisTree() {}

  void SignalAnalysisTree::init(TFileDirectory& dir) {
    fTree = dir.make<TTree>("tree", "Tree");

    fTree->Branch("event", &fEvent);
    fTree->Branch("lumi", &fLumi);
    fTree->Branch("run", &fRun);

    fTree->Branch("weightPrescale", &fPrescaleWeight);
    fTree->Branch("weightPileup", &fPileupWeight);
    fTree->Branch("weightTrigger", &fTriggerWeight);

    fTree->Branch("goodPrimaryVertices_n", &fNVertices);

    fTree->Branch("tau_p4", &fTau);
    fTree->Branch("tau_leadPFChargedHadrCand_p4", &fTauLeadingChCand);

    fTree->Branch("jets_p4", &fJets);
    fTree->Branch("jets_btag", &fJetsBtags);
    fTree->Branch("jets_chf", &fJetsChf); // charged hadron
    fTree->Branch("jets_nhf", &fJetsNhf); // neutral hadron
    fTree->Branch("jets_elf", &fJetsElf);  // electron
    fTree->Branch("jets_phf", &fJetsPhf);  // photon
    fTree->Branch("jets_muf", &fJetsMuf);   // muon
    fTree->Branch("jets_chm", &fJetsChm);
    fTree->Branch("jets_nhm", &fJetsNhm);
    fTree->Branch("jets_elm", &fJetsElm);
    fTree->Branch("jets_phm", &fJetsPhm);
    fTree->Branch("jets_mum", &fJetsMum);
    fTree->Branch("jets_jecToRaw", &fJetsJec);
    fTree->Branch("jets_area", &fJetsArea);
    fTree->Branch("jets_looseId", &fJetsLooseId);
    fTree->Branch("jets_tightId", &fJetsTightId);

    fTree->Branch("met_p4", &fMet);
    fTree->Branch("met_sumet", &fMetSumEt);

    fTree->Branch("topreco_p4", &fTop);

    fTree->Branch("alphaT", &fAlphaT);
  }

  void SignalAnalysisTree::fill(const edm::Event& iEvent, const edm::PtrVector<pat::Tau>& taus,
                                const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met,
                                const XYZTLorentzVector& top, double alphaT) {
    if(taus.size() != 1)
      throw cms::Exception("LogicError") << "Expected tau collection size to be 1, was " << taus.size() << " at " << __FILE__ << ":" << __LINE__ << std::endl;

    fEvent = iEvent.id().event();
    fLumi = iEvent.id().luminosityBlock();
    fRun = iEvent.id().run();

    fTau = taus[0]->p4();
    fTauLeadingChCand = taus[0]->leadPFChargedHadrCand()->p4();

    for(size_t i=0; i<jets.size(); ++i) {
      fJets.push_back(jets[i]->p4());
      fJetsBtags.push_back(jets[i]->bDiscriminator(fBdiscriminator));

      double eta = jets[i]->eta();

      double chf = jets[i]->chargedHadronEnergyFraction();
      double nhf = jets[i]->neutralHadronEnergyFraction();
      double elf = jets[i]->chargedEmEnergyFraction();
      double phf = jets[i]->neutralEmEnergyFraction();
      // for some reason the muonEnergyFraction is calculated w.r.t. *corrected* energy in pat::Jet
      double muf = jets[i]->muonEnergy() / (jets[i]->jecFactor(0) * jets[i]->energy());

      double sum = chf+nhf+elf+phf+muf;
      if(std::abs(sum - 1.0) > 0.000001) {
        throw cms::Exception("Assert") << "The assumption that chf+nhf+elf+phf+muf=1 failed, the sum was " << (chf+nhf+elf+phf+muf) 
                                       << " the sum-1 was " << (sum-1.0)
                                       << std::endl;
      }

      fJetsChf.push_back(chf);
      fJetsNhf.push_back(nhf);
      fJetsElf.push_back(elf);
      fJetsPhf.push_back(phf);
      fJetsMuf.push_back(muf);

      int chm = jets[i]->chargedHadronMultiplicity();
      fJetsChm.push_back(chm);
      fJetsNhm.push_back(jets[i]->neutralHadronMultiplicity());
      fJetsElm.push_back(jets[i]->electronMultiplicity());
      fJetsPhm.push_back(jets[i]->photonMultiplicity());
      fJetsMum.push_back(jets[i]->muonMultiplicity());

      fJetsJec.push_back(jets[i]->jecFactor(0));

      int npr = jets[i]->chargedMultiplicity() + jets[i]->neutralMultiplicity();

      fJetsLooseId.push_back( npr > 1 && phf < 0.99 && nhf < 0.99 && ((std::abs(eta) <= 2.4 && elf < 0.99 && chf > 0 && chm > 0) ||
                                                                      std::abs(eta) > 2.4) );
      fJetsTightId.push_back( npr > 1 && phf < 0.99 && nhf < 0.99 && ((std::abs(eta) <= 2.4 && nhf < 0.9 && phf < 0.9 && elf < 0.99 && chf > 0 && chm > 0) ||
                                                                      std::abs(eta) > 2.4) );

      fJetsArea.push_back(jets[i]->jetArea());
    }
    fMet = met->p4();
    fMetSumEt = met->sumEt();

    fTop = top;

    fAlphaT = alphaT;

    fTree->Fill();
    reset();
  }

  void SignalAnalysisTree::reset() {
    fEvent = 0;
    fLumi = 0;
    fRun = 0;

    fPrescaleWeight = 1.0;
    fPileupWeight = 1.0;
    fTriggerWeight = 1.0;

    fNVertices = 0;

    fTau.SetXYZT(0, 0, 0, 0);
    fTauLeadingChCand.SetXYZT(0, 0, 0, 0);

    fJets.clear();
    fJetsBtags.clear();

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

    fJetsJec.clear();
    fJetsArea.clear();

    fJetsLooseId.clear();
    fJetsTightId.clear();

    fMet.SetXYZT(0, 0, 0, 0);
    fMetSumEt = 0.0;

    fTop.SetXYZT(0, 0, 0, 0);

    fAlphaT = 0;
  }
}
