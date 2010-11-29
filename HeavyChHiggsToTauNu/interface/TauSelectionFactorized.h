// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TauSelectionFactorized_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TauSelectionFactorized_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FactorizationTable.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
#include "TH2.h"

namespace HPlus {
  class TauSelectionFactorized {
  public:
    /**
     * Class to encapsulate the access to the data members of
     * TauSelectionFactorized. If you want to add a new accessor, add it here
     * and keep all the data of TauSelectionFactorized private.
     */
    class Data {
    public:
      // The reason for pointer instead of reference is that const
      // reference allows temporaries, while const pointer does not.
      // Here the object pointed-to must live longer than this object.
      Data(const TauSelectionFactorized *TauSelectionFactorized, bool passedEvent, const TauSelection::Data tauSelectionData);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      TauSelection::Data tauSelectionData() const { return fTauSelectionData; }
      const edm::Ptr<pat::Tau>& getSelectedTau() const { return fTauSelectionFactorized->fSelectedTau; }
      double factorizationCoefficient() const { return fTauSelectionFactorized->fFactorizationCoefficient; }

    private:
      const TauSelectionFactorized *fTauSelectionFactorized;
      const bool fPassedEvent;
      const TauSelection::Data fTauSelectionData;
    };

    TauSelectionFactorized(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, TauSelection& tauSelectionObject);
    ~TauSelectionFactorized();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);

  private:
    TauSelection::Data evaluateFactorizationCoefficients(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Tau>& taus);

  private:
    // Input parameters
    edm::InputTag fSrc;
    const double fPtCut;
    const double fEtaCut;

    // Counters
    Count fInitialTausCount;
    Count fTriggerMatchedTausExistCount;
    Count fPtCutCount;
    Count fEtaCutCount;
    Count fTauFoundCount;

    // EventWeight object
    EventWeight& fEventWeight;
    
    // Tau selection object
    TauSelection fTauSelection;
    
    // Factorization table objects
    FactorizationTable fFactorizationTable;

    // Histograms
    TH1 *hPtSelectedTaus;
    TH1 *hEtaSelectedTaus;
    TH1 *hCategory;
    // Weighted histograms
    TH1 *hPtBeforeTauID;
    TH1 *hPtAfterTauID;
    TH1 *hEtaBeforeTauID;
    TH1 *hEtaAfterTauID;
    TH2 *hPtVsEtaBeforeTauID;
    TH2 *hPtVsEtaAfterTauID;
    // Unweighted histograms (needed to obtain the statistical error)
    TH1 *hPtBeforeTauIDUnweighted;
    TH1 *hPtAfterTauIDUnweighted;
    TH1 *hEtaBeforeTauIDUnweighted;
    TH1 *hEtaAfterTauIDUnweighted;
    TH2 *hPtVsEtaBeforeTauIDUnweighted;
    TH2 *hPtVsEtaAfterTauIDUnweighted;

    // Selected tau
    double fFactorizationCoefficient;
    edm::Ptr<pat::Tau> fSelectedTau;
  };
}

#endif
