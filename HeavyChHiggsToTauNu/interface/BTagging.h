// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DirectionalCut.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTaggingScaleFactorFromDB.h"

namespace edm {
  class ParameterSet;
}

namespace HPlus {
  class JetSelection;
  class HistoWrapper;
  class WrappedTH1;

  class BTagging: public BaseSelection {
    class BTaggingScaleFactor {
    public:
      BTaggingScaleFactor();
      ~BTaggingScaleFactor();

      void UseDB(BTaggingScaleFactorFromDB*);
      
      void addBFlavorData(double pT, double scaleFactorB, double scaleFactorUncertaintyB, double epsilonMCB);
      void addNonBFlavorData(double pT, double scaleFactorL, double scaleFactorUncertaintyL, double epsilonMCL);
/*      
      double getWeight(std::vector<double>&,std::vector<double>&,std::vector<double>&,std::vector<double>&);
      double getRelativeUncertainty(std::vector<double>&,std::vector<double>&,std::vector<double>&,std::vector<double>&);
      double getAbsoluteUncertainty(std::vector<double>&,std::vector<double>&,std::vector<double>&,std::vector<double>&);
*/
      double getWeight(edm::PtrVector<pat::Jet>,edm::PtrVector<pat::Jet>,edm::PtrVector<pat::Jet>,edm::PtrVector<pat::Jet>);
      double getRelativeUncertainty(edm::PtrVector<pat::Jet>,edm::PtrVector<pat::Jet>,edm::PtrVector<pat::Jet>,edm::PtrVector<pat::Jet>);
      double getAbsoluteUncertainty(edm::PtrVector<pat::Jet>,edm::PtrVector<pat::Jet>,edm::PtrVector<pat::Jet>,edm::PtrVector<pat::Jet>);
      
    private:
      size_t obtainIndex(std::vector<double>& table, double pt);

      double getBtagScaleFactor(double,double);
      double getBtagScaleFactorError(double,double);
      double getMistagScaleFactor(double,double);
      double getMistagScaleFactorError(double,double);
      double getMCBtagEfficiency(double,double);
      double getMCMistagEfficiency(double,double);

      BTaggingScaleFactorFromDB *btagdb;
      
      std::vector<double> fPtBinsB; // lower edges of pT bins for b-flavor jets
      std::vector<double> fPtBinsL; // lower edges of pT bins for l-flavor jets
      std::vector<double> fScaleFactorB; // b-tagging scalefactor for b-flavor jets
      std::vector<double> fScaleFactorL; // b-mistagging scalefactor for non-b-flavor jets
      std::vector<double> fScaleFactorUncertaintyB; // b-tagging scalefactor uncertainty for b-flavor jets
      std::vector<double> fScaleFactorUncertaintyL; // b-mistagging scalefactor uncertainty for non-b-flavor jets
      std::vector<double> fEpsilonMCB; // b-tagging efficiency from MC for b-flavor jets
      std::vector<double> fEpsilonMCL; // b-mistagging efficiency from MC for non-b-flavor jets
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
      const edm::PtrVector<pat::Jet>& getSelectedSubLeadingJets() const { return fBTagging->fSelectedSubLeadingJets; }
      const int getBJetCount() const { return fBTagging->iNBtags; }
      const double getMaxDiscriminatorValue() const { return fBTagging->fMaxDiscriminatorValue; }
      const double getScaleFactor() const { return fBTagging->fScaleFactor; }
      const double getScaleFactorAbsoluteUncertainty() const { return fBTagging->fScaleFactorAbsoluteUncertainty; }
      const double getScaleFactorRelativeUncertainty() const { return fBTagging->fScaleFactorRelativeUncertainty; }
      const bool hasGenuineBJets() const;
      void fillScaleFactorHistograms();

    private:
      const BTagging *fBTagging;
      const bool fPassedEvent;
    };

    BTagging(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~BTagging();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);

    int analyzeOnlyBJetCount(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);
    double analyzeOnlyBJetScaleFactor(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets) {
      analyzeOnlyBJetCount(iEvent,iSetup,jets); return fScaleFactor;
    }

    const std::string getDiscriminator() const { return fDiscriminator; }

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);
    
    void calculateScaleFactor(const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets);

    // Input parameters
    edm::InputTag fSrc;

    // Input parameters
    const double fPtCut;
    const double fEtaCut;
    const std::string fDiscriminator;
    const double fLeadingDiscrCut;
    const double fSubLeadingDiscrCut;
    DirectionalCut fNumberOfBJets;

    BTaggingScaleFactorFromDB *btagDB;
    bool FactorsFromDB;

    // Lookup tables for scale factors
    BTaggingScaleFactor fBTaggingScaleFactor;
    WrappedTH1* hBTagAbsoluteUncertainty;
    WrappedTH1* hBTagRelativeUncertainty;

    // Counters
    Count fTaggedCount;

    Count fAllSubCount;
    Count fTaggedSubCount;
    Count fTaggedPtCutSubCount;
    Count fTaggedEtaCutSubCount;
    Count fTaggedAllRealBJetsSubCount;
    Count fTaggedTaggedRealBJetsSubCount;
    Count fTaggedNoTaggedJet;
    Count fTaggedOneTaggedJet;
    Count fTaggedTwoTaggedJets;

    // Histograms
    WrappedTH1 *hDiscr;
    WrappedTH1 *hPt;
    WrappedTH1 *hEta;
    WrappedTH1 *hDiscrB;
    WrappedTH1 *hPtBCSVT;
    WrappedTH1 *hEtaBCSVT;
    WrappedTH1 *hPtBCSVM;
    WrappedTH1 *hEtaBCSVM;
    WrappedTH1 *hPtBnoTag;
    WrappedTH1 *hEtaBnoTag;
    WrappedTH1 *hDiscrQ;
    WrappedTH1 *hPtQCSVT;
    WrappedTH1 *hEtaQCSVT;
    WrappedTH1 *hPtQCSVM;
    WrappedTH1 *hEtaQCSVM;
    WrappedTH1 *hPtQnoTag;
    WrappedTH1 *hEtaQnoTag;
    WrappedTH1 *hPt1;
    WrappedTH1 *hEta1;
    WrappedTH1 *hPt2;
    WrappedTH1 *hEta2;
    WrappedTH1 *hNumberOfBtaggedJets;
    WrappedTH1 *hNumberOfBtaggedJetsIncludingSubLeading;
    WrappedTH1 *hScaleFactor;
    WrappedTH1 *hMCMatchForPassedJets;
    WrappedTH1 *hControlBTagUncertaintyMode;
    // Selected jets
    edm::PtrVector<pat::Jet> fSelectedJets;
    edm::PtrVector<pat::Jet> fSelectedSubLeadingJets;
    int iNBtags;
    double fMaxDiscriminatorValue;
    double fScaleFactor;
    double fScaleFactorAbsoluteUncertainty;
    double fScaleFactorRelativeUncertainty;
  };
}

#endif
