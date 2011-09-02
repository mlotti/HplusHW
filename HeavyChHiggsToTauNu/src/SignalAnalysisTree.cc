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
    fTree->Branch("jets_EMfrac", &fJetsEMfracs);

    fTree->Branch("met_p4", &fMet);
  }

  void SignalAnalysisTree::fill(const edm::Event& iEvent, const edm::PtrVector<pat::Tau>& taus,
                                const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met) {
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
      double EMfrac = (jets[i]->chargedEmEnergy() + 
                       jets[i]->neutralEmEnergy())/(
                       jets[i]->chargedHadronEnergy() + 
                       jets[i]->neutralHadronEnergy() + 
                       jets[i]->chargedEmEnergy() + 
                       jets[i]->neutralEmEnergy());
      fJetsEMfracs.push_back(EMfrac);
    }

    fMet = met->p4();

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
    fJetsEMfracs.clear();

    fMet.SetXYZT(0, 0, 0, 0);
  }
}
