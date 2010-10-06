// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"

namespace edm {
  class ParameterSet;
}

class TH1;

namespace HPlus {
  class JetSelection;

  class BTagging {
  public:
    BTagging(const edm::ParameterSet& iConfig, EventCounter& eventCounter);
    ~BTagging();

    bool analyze(const edm::PtrVector<pat::Jet>& jets);

    const edm::PtrVector<pat::Jet>& getSelectedJets() const {
      return fSelectedJets;
    }

  private:
    // Input parameters
    std::string fDiscriminator;
    double fDiscrCut;
    double fEtaCut;
    double fPtCut;
    uint32_t fMin;

    // Counters
    Count fTaggedCount;

    Count fAllSubCount;
    Count fTaggedSubCount;
    Count fTaggedEtaCutSubCount;

    // Histograms
    TH1 *hDiscr;
    TH1 *hPt;
    TH1 *hEta;
    TH1 *hNumberOfBtaggedJets;

    // Selected jets
    edm::PtrVector<pat::Jet> fSelectedJets;
  };
}

#endif
