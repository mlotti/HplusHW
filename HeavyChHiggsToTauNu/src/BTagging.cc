#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {

  BTagging::BTagging(const edm::ParameterSet& iConfig, EventCounter& eventCounter):
    fDiscriminator(iConfig.getUntrackedParameter<std::string>("discriminator")),
    fDiscrCut(iConfig.getUntrackedParameter<double>("discriminatorCut")),
    fMin(iConfig.getUntrackedParameter<uint32_t>("minNumber")),
    fTaggedCount(eventCounter.addCounter("b-tagging")),
    fAllSubCount(eventCounter.addSubCounter("b-tagging", "all jets")),
    fTaggedSubCount(eventCounter.addSubCounter("b-tagging", "tagged"))
  {
    edm::Service<TFileService> fs;
    hDiscr = fs->make<TH1F>("jet_bdiscriminator", ("b discriminator "+fDiscriminator).c_str(), 80, -10, 10);
    hPt = fs->make<TH1F>("bjet_pt", "bjet_pt", 100, 0., 100.);
    hEta = fs->make<TH1F>("bjet_eta", "bjet_pt", 60, -3., 3.);
  }

  BTagging::~BTagging() {}

  bool BTagging::analyze(const edm::PtrVector<pat::Jet>& jets) {
    fSelectedJets.clear();
    fSelectedJets.reserve(jets.size());

    size_t passed = 0;
    
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      edm::Ptr<pat::Jet> iJet = *iter;

      increment(fAllSubCount);

      float discr = iJet->bDiscriminator(fDiscriminator);
      hDiscr->Fill(discr);
      if(!(discr > fDiscrCut)) continue;
      increment(fTaggedSubCount);
      ++passed;

      hPt->Fill(iJet->pt());
      hEta->Fill(iJet->eta());

      fSelectedJets.push_back(iJet);
    }

    if(passed < fMin) return false;
    increment(fTaggedCount);
    return true;
  }
}