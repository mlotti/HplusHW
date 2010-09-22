#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/MET.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"

#include "Math/GenVector/VectorUtil.h"

#include<string>
#include<vector>
#include<limits>
#include<algorithm>

class HPlusSignalAnalysisNtupleProducer: public edm::EDFilter {
 public:

  explicit HPlusSignalAnalysisNtupleProducer(const edm::ParameterSet&);
  ~HPlusSignalAnalysisNtupleProducer();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  struct METParam {
    METParam(const edm::InputTag& tag, const std::string& label):
      fTag(tag), fLabel(label), 
      fTransverseMassLabel(label+"TransverseMass"),
      fDeltaPhiLabel(label+"DeltaPhi")
    {}
    edm::InputTag fTag;
    std::string fLabel;
    std::string fTransverseMassLabel;
    std::string fDeltaPhiLabel;
  };

  struct Discriminator {
    Discriminator(const std::string& d, const std::string& b): fDiscr(d), fBranch(b) {}
    std::string fDiscr;
    std::string fBranch;
  };

  HPlus::EventCounter eventCounter;
  HPlus::TauSelection fTauSelection;
  HPlus::JetSelection fJetSelection;
  const std::string fPrefix;
  std::vector<METParam> fMETsrc;
  std::vector<Discriminator> fTauDiscriminators;
  std::vector<Discriminator> fBDiscriminators;
};

HPlusSignalAnalysisNtupleProducer::HPlusSignalAnalysisNtupleProducer(const edm::ParameterSet& iConfig):
  eventCounter(),
  fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter),
  fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter),
  fPrefix(iConfig.getUntrackedParameter<std::string>("branchAliasPrefix"))
{
  eventCounter.produces(this);

  std::string name;

  // tau branches
  name = "taupt";
  produces<double>(name).setBranchAlias(fPrefix+name);
  name = "taueta";
  produces<double>(name).setBranchAlias(fPrefix+name);
  name = "rtau";
  produces<double>(name).setBranchAlias(fPrefix+name);

  if(iConfig.exists("tauDiscriminators")) {
    std::vector<edm::ParameterSet> tauParam = iConfig.getUntrackedParameter<std::vector<edm::ParameterSet> >("tauDiscriminators");
    fTauDiscriminators.reserve(tauParam.size());
    for(size_t i=0; i<tauParam.size(); ++i) {
      name = tauParam[i].getUntrackedParameter<std::string>("branch");
      produces<double>(name).setBranchAlias(fPrefix+name);
      fTauDiscriminators.push_back(Discriminator(tauParam[i].getUntrackedParameter<std::string>("discriminator"), name));
    }
  }

  // jet branches
  //name = "jetpts";
  //produces<std::vector<double> >(name).setBranchAlias(fPrefix+name);
  name = "njets";
  produces<int>(name).setBranchAlias(fPrefix+name);

  // b-tagging branches (one branch per discriminator, value is the
  // maximum over the jets passing the pt/eta cuts)
  std::vector<std::string> btagParam = iConfig.getUntrackedParameter<std::vector<std::string> >("btags");
  fBDiscriminators.reserve(btagParam.size()); 
  for(size_t i=0; i<btagParam.size(); ++i) {
    fBDiscriminators.push_back(Discriminator(btagParam[i], "maxBtag"+btagParam[i]));
    name = fBDiscriminators.back().fBranch;
    produces<float>(name).setBranchAlias(fPrefix+name);
  }

  // MET branches, one branch per MET type
  std::vector<edm::ParameterSet> metParam = iConfig.getUntrackedParameter<std::vector<edm::ParameterSet> >("METs");
  fMETsrc.reserve(metParam.size());
  for(size_t i=0; i<metParam.size(); ++i) {
    name = metParam[i].getUntrackedParameter<std::string>("label");
    fMETsrc.push_back(METParam(metParam[i].getUntrackedParameter<edm::InputTag>("src"), name));
    produces<double>(name).setBranchAlias(fPrefix+name);
    name = fMETsrc.back().fTransverseMassLabel;
    produces<double>(name).setBranchAlias(fPrefix+name);
    name = fMETsrc.back().fDeltaPhiLabel;
    produces<double>(name).setBranchAlias(fPrefix+name);
  }
}
HPlusSignalAnalysisNtupleProducer::~HPlusSignalAnalysisNtupleProducer() {}
void HPlusSignalAnalysisNtupleProducer::beginJob() {}

bool HPlusSignalAnalysisNtupleProducer::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusSignalAnalysisNtupleProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  // The event must pass loose tau and jet selections
  if(!fTauSelection.analyze(iEvent, iSetup)) return false;
  if(!fJetSelection.analyze(iEvent, iSetup, fTauSelection.getSelectedTaus())) return false;

  // Take the pt and eta of tau
  edm::Ptr<pat::Tau> tau = fTauSelection.getSelectedTaus()[0];
  iEvent.put(std::auto_ptr<double>(new double(tau->pt())), "taupt");
  iEvent.put(std::auto_ptr<double>(new double(tau->eta())), "taueta");

  std::auto_ptr<double> rtau(new double(0));
  if(tau->pt() > 0) {
    if(tau->isPFTau()) {
      reco::PFCandidateRef leadCand = tau->leadPFChargedHadrCand();
      if(leadCand.isNonnull())
        *rtau = leadCand->p()/tau->p();
    }
    else if(tau->isCaloTau()) {
      reco::TrackRef leadTrack = tau->leadTrack();
      if(leadTrack.isNonnull())
        *rtau = leadTrack->p()/tau->p();
    }
  }
  iEvent.put(rtau, "rtau");

  // Tau discriminators
  for(std::vector<Discriminator>::const_iterator iDiscr = fTauDiscriminators.begin(); iDiscr != fTauDiscriminators.end(); ++iDiscr) {
    iEvent.put(std::auto_ptr<double>(new double(tau->tauID(iDiscr->fDiscr))), iDiscr->fBranch);
  }


  /*
  std::auto_ptr<std::vector<double> > jetpts(new std::vector<double>(fJetSelection.getMinNumber()));
  const edm::PtrVector<pat::Jet>& jets = fJetSelection.getSelectedJets();
  for(size_t i=0; i<jetpts->size(); ++i) {
    (*jetpts)[i] = jets[i]->pt();
  }
  iEvent.put(jetpts, "jetpts");
  */
  // Number of jets passing the jet selection
  const edm::PtrVector<pat::Jet>& jets = fJetSelection.getSelectedJets();
  iEvent.put(std::auto_ptr<int>(new int(jets.size())), "njets");

  // For each b discriminator, take the maximum value over the
  // selected jets (this is enough if we seek for one b-tagged jet,
  // for 2 b-tagged jets we would need the 2nd maximum value)
  for(std::vector<Discriminator>::const_iterator iDiscr = fBDiscriminators.begin(); iDiscr != fBDiscriminators.end(); ++iDiscr) {
    float maxDiscr = std::numeric_limits<float>::quiet_NaN();
    if(!jets.empty()) {
      maxDiscr = jets[0]->bDiscriminator(iDiscr->fDiscr);
    }
    for(size_t i=1; i<jets.size(); ++i) {
      maxDiscr = std::max(maxDiscr, jets[i]->bDiscriminator(iDiscr->fDiscr));
    }

    iEvent.put(std::auto_ptr<float>(new float(maxDiscr)), iDiscr->fBranch);
  }

  // The MET values
  for(size_t i=0; i<fMETsrc.size(); ++i) {
    edm::Handle<edm::View<reco::MET> > hmet;
    iEvent.getByLabel(fMETsrc[i].fTag, hmet);
    edm::Ptr<reco::MET> met = hmet->ptrAt(0);
    iEvent.put(std::auto_ptr<double>(new double(met->et())), fMETsrc[i].fLabel);

    iEvent.put(std::auto_ptr<double>(new double(HPlus::TransverseMass::reconstruct(*tau, *met))), fMETsrc[i].fTransverseMassLabel);
    iEvent.put(std::auto_ptr<double>(new double(ROOT::Math::VectorUtil::DeltaPhi(tau->momentum(), met->momentum()))), fMETsrc[i].fDeltaPhiLabel);
  }

  return true;
}

bool HPlusSignalAnalysisNtupleProducer::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return false;
}

void HPlusSignalAnalysisNtupleProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusSignalAnalysisNtupleProducer);
