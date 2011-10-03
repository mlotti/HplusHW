#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysisTree.h"

#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CommonTools/Utils/interface/TFileDirectory.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Muon.h"


#include "TTree.h"

#include <limits>

namespace HPlus {
  SignalAnalysisTree::SignalAnalysisTree(const edm::ParameterSet& iConfig, const std::string& bDiscriminator):
    fBdiscriminator(bDiscriminator), 
    fDoFill(iConfig.getUntrackedParameter<bool>("fill")),
    fTauEmbeddingInput(iConfig.getUntrackedParameter<bool>("tauEmbeddingInput", false)),
    fTree(0)
  {
    if(fTauEmbeddingInput) {
      fTauEmbeddingMuonSource = iConfig.getUntrackedParameter<edm::InputTag>("tauEmbeddingMuonSource");
      fTauEmbeddingMetSource = iConfig.getUntrackedParameter<edm::InputTag>("tauEmbeddingMetSource");
      fTauEmbeddingCaloMetSource = iConfig.getUntrackedParameter<edm::InputTag>("tauEmbeddingCaloMetSource");
    }

    std::vector<std::string> tauIds = iConfig.getUntrackedParameter<std::vector<std::string> >("tauIDs");
    fTauIds.reserve(tauIds.size());
    for(size_t i=0; i<tauIds.size(); ++i) {
      fTauIds.push_back(TauId(tauIds[i]));
    }

    reset();
  }
  SignalAnalysisTree::~SignalAnalysisTree() {}

  void SignalAnalysisTree::init(TFileDirectory& dir) {
    if(!fDoFill)
      return;

    fTree = dir.make<TTree>("tree", "Tree");

    fTree->Branch("event", &fEvent);
    fTree->Branch("lumi", &fLumi);
    fTree->Branch("run", &fRun);

    fTree->Branch("weightPrescale", &fPrescaleWeight);
    fTree->Branch("weightPileup", &fPileupWeight);
    fTree->Branch("weightTrigger", &fTriggerWeight);
    fTree->Branch("weightBTagging", &fBTaggingWeight);
    fTree->Branch("weightAtFill", &fFillWeight);

    fTree->Branch("goodPrimaryVertices_n", &fNVertices);
    fTree->Branch("hltTaus_n", &fNHltTaus);

    fTree->Branch("tau_p4", &fTau);
    fTree->Branch("tau_leadPFChargedHadrCand_p4", &fTauLeadingChCand);
    fTree->Branch("tau_signalPFChargedHadrCands_n", &fTauSignalChCands);
    for(size_t i=0; i<fTauIds.size(); ++i) {
      fTree->Branch( ("tau_id_"+fTauIds[i].name).c_str(), &(fTauIds[i].value) );
    }

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

    fTree->Branch("met_p4", &fRawMet);
    fTree->Branch("met_sumet", &fRawMetSumEt);

    fTree->Branch("metType1_p4", &fType1Met);
    fTree->Branch("metType2_p4", &fType2Met);

    fTree->Branch("topreco_p4", &fTop);

    fTree->Branch("alphaT", &fAlphaT);

    fTree->Branch("passedBTagging", &fPassedBTagging);

    if(fTauEmbeddingInput) {
      fTree->Branch("temuon_p4", &fTauEmbeddingMuon);
      fTree->Branch("temet_p4", &fTauEmbeddingMet);
      fTree->Branch("tecalomet_p4", &fTauEmbeddingCaloMet);
    }
  }

  void SignalAnalysisTree::fill(const edm::Event& iEvent, const edm::PtrVector<pat::Tau>& taus,
                                const edm::PtrVector<pat::Jet>& jets,
                                double alphaT) {
    if(!fDoFill)
      return;

    if(taus.size() != 1)
      throw cms::Exception("LogicError") << "Expected tau collection size to be 1, was " << taus.size() << " at " << __FILE__ << ":" << __LINE__ << std::endl;

    fEvent = iEvent.id().event();
    fLumi = iEvent.id().luminosityBlock();
    fRun = iEvent.id().run();

    fTau = taus[0]->p4();
    fTauLeadingChCand = taus[0]->leadPFChargedHadrCand()->p4();
    fTauSignalChCands = taus[0]->signalPFChargedHadrCands().size();
    for(size_t i=0; i<fTauIds.size(); ++i) {
      fTauIds[i].value = taus[0]->tauID(fTauIds[i].name) > 0.5;
    }

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
    fAlphaT = alphaT;

    if(fTauEmbeddingInput) {
      edm::Handle<edm::View<pat::Muon> > hmuon;
      iEvent.getByLabel(fTauEmbeddingMuonSource, hmuon);
      if(hmuon->size() != 1)
        throw cms::Exception("Assert") << "The assumption that tau embedding muon collection size is 1 failed, the size was " << hmuon->size() << std::endl;

      edm::Handle<edm::View<reco::MET> > hmet;
      iEvent.getByLabel(fTauEmbeddingMetSource, hmet);
      if(hmet->size() != 1)
        throw cms::Exception("Assert") << "The assumption that tau embedding met collection size is 1 failed, the size was " << hmet->size() << std::endl;

      edm::Handle<edm::View<reco::MET> > hcalomet;
      iEvent.getByLabel(fTauEmbeddingCaloMetSource, hcalomet);
      if(hcalomet->size() != 1)
        throw cms::Exception("Assert") << "The assumption that tau embedding calomet collection size is 1 failed, the size was " << hcalomet->size() << std::endl;

      fTauEmbeddingMuon = hmuon->at(0).p4();
      fTauEmbeddingMet = hmet->at(0).p4();
      fTauEmbeddingCaloMet = hcalomet->at(0).p4();
    }

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
    fBTaggingWeight = 1.0;
    fFillWeight = 1.0;

    fNVertices = 0;
    fNHltTaus = 0;

    double nan = std::numeric_limits<double>::quiet_NaN();

    fTau.SetXYZT(nan, nan, nan, nan);
    fTauLeadingChCand.SetXYZT(nan, nan, nan, nan);
    fTauSignalChCands = 0;
    for(size_t i=0; i<fTauIds.size(); ++i)
      fTauIds[i].reset();

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

    fRawMet.SetXYZT(nan, nan, nan, nan);
    fRawMetSumEt = nan;

    fType1Met.SetXYZT(nan, nan, nan, nan);
    fType2Met.SetXYZT(nan, nan, nan, nan);

    fTop.SetXYZT(nan, nan, nan, nan);

    fAlphaT = nan;

    fPassedBTagging = false;

    fTauEmbeddingMuon.SetXYZT(nan, nan, nan, nan);
    fTauEmbeddingMet.SetXYZT(nan, nan, nan, nan);
    fTauEmbeddingCaloMet.SetXYZT(nan, nan, nan, nan);
  }
}
