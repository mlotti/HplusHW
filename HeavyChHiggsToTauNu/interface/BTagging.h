// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"

namespace edm {
  class ParameterSet;
}

class TH1;

namespace HPlus {
  class JetSelection;

  class BTagging {
  enum BTaggingVariationMode {
    kBTagVariationNormal,
    kBTagVariationMinus,
    kBTagVariationPlus
  };
  public:
    /**
     * Class to encapsulate the access to the data members of
     * TauSelection. If you want to add a new accessor, add it here
     * and keep all the data of TauSelection private.
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data(const BTagging *bTagging, bool passedEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      const edm::PtrVector<pat::Jet>& getSelectedJets() const { return fBTagging->fSelectedJets; }
      const int getBJetCount() const { return fBTagging->iNBtags; }
      const double getMaxDiscriminatorValue() const { return fBTagging->fMaxDiscriminatorValue; }

    private:
      const BTagging *fBTagging;
      const bool fPassedEvent;
    };
    
    BTagging(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);  
    ~BTagging();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);

  private:
    void applyScaleFactor(const edm::PtrVector<pat::Jet>& jets);

    // Input parameters                                                                                                                                                                          
    edm::InputTag fSrc;

    // Input parameters
    const double fPtCut;
    const double fEtaCut;
    const std::string fDiscriminator;
    const double fDiscrCut;
    const uint32_t fMin;
    double fScaleFactorBFlavor;
    double fScaleFactorLightFlavor;
    BTaggingVariationMode fVariationMode;
    
    // Counters
    Count fTaggedCount;

    Count fAllSubCount;
    Count fTaggedSubCount;
    Count fTaggedEtaCutSubCount;
    Count fTaggedAllRealBJetsSubCount;
    Count fTaggedTaggedRealBJetsSubCount;
    Count fTaggedNoTaggedJet;
    Count fTaggedOneTaggedJet;
    Count fTaggedTwoTaggedJets;

    // EventWeight object
    EventWeight& fEventWeight;
    
    // Histograms
    TH1 *hDiscr;
    TH1 *hPt;
    TH1 *hEta;
    TH1 *hDiscrB;
    TH1 *hPtB;
    TH1 *hEtaB;
    TH1 *hPt1;
    TH1 *hEta1;
    TH1 *hPt2;
    TH1 *hEta2;
    TH1 *hNumberOfBtaggedJets;
    TH1 *hScaleFactor;
    TH1 *hMCMatchForPassedJets;
    TH1 *hControlBTagUncertaintyMode;
    // Selected jets
    edm::PtrVector<pat::Jet> fSelectedJets;
    int iNBtags;
    double fMaxDiscriminatorValue;
    double fScaleFactor;
  };
}

#endif
