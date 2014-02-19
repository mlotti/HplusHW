// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DirectionalCut.h"
#include "TF1.h"

#include <boost/utility.hpp>

namespace edm {
  class Event;
  class EventSetup;
  class ParameterSet;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class WrappedTH2;

  class BTagging: public BaseSelection {
  public:
    class Data; // Forward declare because it is used in ScaleFactorTable interface

  private:
    class EfficiencyTable; // Forward declared because ScaleFactorTable interface uses it

    class ScaleFactorTable: private boost::noncopyable {
    public:
      ScaleFactorTable();
      ~ScaleFactorTable();

      void setScaleFactorTable(const std::vector<double>& ptBinTable, const char* SFFunctionExpression, const std::vector<double>& uncertaintyTable);
      void setScaleFactorTable(TF1* scaleFactorFunction, TF1* sfUncertUpFunction, TF1* sfUncertDownFunction);
      void setScaleFactorFunction(const char* expression);
      void setScaleFactorUncertaintyFunctions(const char* expressionUp, const char* expressionDown);

      void resetJetTable();
      void addUncertaintyTagged(double pT);
      void addUncertaintyTagged(double pT, double uncertaintyFactor);
      void addUncertaintyUntagged(double pT, EfficiencyTable& efficiencyTable);
      void addUncertaintyUntagged(double pT, EfficiencyTable& efficiencyTable, double uncertaintyFactor);

      void addJetSFUncertaintyTerm(double pT, bool isBTagged, EfficiencyTable& effTable, double factor);
      void addJetSFUncertaintyTerm(double pT, bool isBTagged, EfficiencyTable& effTable);

      double getScaleFactor(double pT) const;
      double getScaleFactorUncertaintyBinned(double pT) const;
      double getMaximumUncertainty(double pT) const;

      size_t obtainIndex(double pT) { return obtainIndex(fPtBins, pT); }

      double calculateRelativeUncertaintySquared(bool up);

      void printJetTableForValidation();

    private:
      static size_t obtainIndex(const std::vector<double>& table, double pT);

      // Scale factors and/or their uncertainties may be given as parametrized functions
      TF1 *fScaleFactorFunction;
      TF1 *fScaleFactorUncertUpFunction;
      TF1 *fScaleFactorUncertDownFunction;
      // Per-jet scale factor look-up table
      std::vector<double> fPtBins; // lower edges of pT bins
      std::vector<double> fScaleFactor; // b-tagging scale factor
      std::vector<double> fScaleFactorUncertainty; // b-tagging scale factor uncertainty
      // Vectors for storing jet info for the calculation of the weight uncertainty
      std::vector<double> fPerBinUncertaintyUp;
      std::vector<double> fPerBinUncertaintyDown;
      std::vector<double> fUnbinnedUncertaintyUp;
      std::vector<double> fUnbinnedUncertaintyDown;
    };

    class EfficiencyTable: private boost::noncopyable {
    public:
      EfficiencyTable();
      ~EfficiencyTable();

      void setEfficiencyTable(const std::vector<double>& ptBinTable, const std::vector<double>& efficiencyTable, const std::vector<double>& uncertaintyUpTable, const std::vector<double>& uncertaintyDownTable);
      void resetJetTable();
      void addJetSFUncertaintyTerm(double pT, bool isBTagged, ScaleFactorTable& sfTable);

      double getEfficiency(double pT) const;
      double getMaximumUncertainty(double pT) const;

      size_t obtainIndex(double pT) { return obtainIndex(fPtBins, pT); }

      double calculateRelativeUncertaintySquared(bool up);

    private:
      static size_t obtainIndex(const std::vector<double>& table, double pT);

      // Efficiency look-up table
      std::vector<double> fPtBins; // lower edges of pT bins
      std::vector<double> fEfficiency; // Efficiency of (mis)tagging jet as a b-jet
      std::vector<double> fEffUncertUp; // Uncertainty of (mis)tagging efficienc
      std::vector<double> fEffUncertDown; // Uncertainty of (mis)tagging efficiency
      // Vectors for storing jet info for the calculation of the weight uncertainty
      std::vector<double> fPerBinUncertaintyUp;
      std::vector<double> fPerBinUncertaintyDown;
    };
    
  public:
    class Data {
    public:
      Data();
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      const edm::PtrVector<pat::Jet>& getSelectedJets() const { return fSelectedJets; }
      const edm::PtrVector<pat::Jet>& getSelectedSubLeadingJets() const { return fSelectedSubLeadingJets; }
      const int getBJetCount() const { return iNBtags; }
      const double getMaxDiscriminatorValue() const { return fMaxDiscriminatorValue; }
      const double getScaleFactor() const { return fEventScaleFactor; }
      const double getScaleFactorMaxAbsUncertainty() const { return fEventSFAbsUncert_max; }
      const double getScaleFactorAbsoluteUncertainty_up() const { return fEventSFAbsUncert_up; }
      const double getScaleFactorAbsoluteUncertainty_down() const { return fEventSFAbsUncert_down; }
      const double getScaleFactorRelativeUncertainty_up() const { return fEventSFRelUncert_up; }
      const double getScaleFactorRelativeUncertainty_down() const { return fEventSFRelUncert_down; }
      const std::string getDiscriminatorName() const { return fDiscriminatorName; }
      const double getProbabilityToPassBtagging() const { return fProbabilityToPassBtagging; }

      const bool hasGenuineBJets() const;

      friend class BTagging;

    private:
      bool fPassedEvent;
      // Selected jets
      edm::PtrVector<pat::Jet> fSelectedJets;
      edm::PtrVector<pat::Jet> fSelectedSubLeadingJets;
      int iNBtags;
      double fMaxDiscriminatorValue;
      double fEventScaleFactor;
      double fEventSFAbsUncert_up;
      double fEventSFAbsUncert_down;
      double fEventSFRelUncert_up;
      double fEventSFRelUncert_down;
      double fEventSFAbsUncert_max;
      std::string fDiscriminatorName;
      double fProbabilityToPassBtagging;
    };

    struct PerJetInfo {
      std::vector<double> scaleFactor; // perJetWeight
      std::vector<double> uncertainty; // perJetWeightUncert
      std::vector<bool> tagged;        // b-tagging status
      std::vector<bool> genuine;       // genuine b-jet?

      void reserve(size_t s) {
	scaleFactor.reserve(s);
	uncertainty.reserve(s);
	tagged.reserve(s);
	genuine.reserve(s);
      }
    };

    struct EventSFTerms {
      std::vector<double> SFTerms;
      void reserve(size_t s) { SFTerms.reserve(s); }
      void addJetSFTerm(double pT, bool isBTagged, ScaleFactorTable& sfTable, EfficiencyTable& effTable);
      double calculateEventScaleFactor();
    };

    BTagging(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~BTagging();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);

    void fillScaleFactorHistograms(BTagging::Data& input);

    const std::string getDiscriminator() const { return fDiscriminator; }

    PerJetInfo getPerJetInfo(edm::PtrVector<pat::Jet> jetCollection, BTagging::Data& bTagData, bool isRealData) const;
    double calculateJetSFTerm(double pT, bool isBTagged, const ScaleFactorTable& sfTable, const EfficiencyTable& effTable) const;
    double calculateJetSFUncertaintyTerm(double pT, bool isBTagged, const ScaleFactorTable& sfTable, const EfficiencyTable& effTable, double SFUncertaintyFactor) const;

    void calculateJetSFAndUncertaintyTerm(edm::Ptr<pat::Jet>& iJet, bool isBTagged, EventSFTerms& terms, ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag) const;
    double calculateRelativeEventScaleFactorUncertainty(bool up, ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag);
    
  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);
    void analyzeMCTagEfficiencyByJetFlavour(const edm::Ptr<pat::Jet>& jet, const bool isBJet, const bool isCJet, const bool isLightJet);
    void setEventScaleFactorInfo(EventSFTerms& terms, ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag, BTagging::Data& output);
    double calculateProbabilityToPassBTagging(const edm::Event& iEvent, const edm::PtrVector<pat::Jet>& jets);

    // Input parameters
    edm::InputTag fSrc;

    // Input parameters
    const double fPtCut;
    const double fEtaCut;
    const std::string fDiscriminator;
    std::string payloadName;
    const double fLeadingDiscrCut;
    const double fSubLeadingDiscrCut;
    DirectionalCut fNumberOfBJets;

    const bool fVariationEnabled;
    const double fVariationShiftBy;

//     // Structure for storing per-jet information
//     PerJetInfo fBTaggingInfo;

    // Lookup tables for scale factors
    ScaleFactorTable fTagSFTable;
    ScaleFactorTable fMistagSFTable;

    // Lookup tables for tagging efficiencies in MC
    EfficiencyTable fTagEffTable;
    EfficiencyTable fCMistagEffTable;
    EfficiencyTable fGMistagEffTable;
    EfficiencyTable fUDSMistagEffTable;

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

    Count allJetsCount2;
    Count genuineBJetsCount2;
    Count genuineBJetsWithBTagCount2;

    // Histograms
    WrappedTH1 *hSFBCSVM;
    WrappedTH2 *hSFBCSVM_pt;
    WrappedTH2 *hSFBCSVM_eta;
    //WrappedTH1 *hEffBCSVM_eta;
    //WrappedTH2 *hEffBCSVM_eta_pt;
    WrappedTH1 *hDiscriminator;
    WrappedTH1 *hPt;
    WrappedTH1 *hEta;
    WrappedTH1 *hPtBCSVT;
    WrappedTH1 *hEtaBCSVT;
    WrappedTH1 *hPtBCSVM;
    WrappedTH1 *hEtaBCSVM;
    WrappedTH1 *hPtBnoTag;
    WrappedTH1 *hEtaBnoTag;
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
    WrappedTH1 *hMCMatchForPassedJets;
    WrappedTH1 *hControlBTagUncertaintyMode;
    // MC btagging and mistagging efficiency
    WrappedTH1 *hMCAllBJetsByPt;
    WrappedTH1 *hMCAllCJetsByPt;
    WrappedTH1 *hMCAllLightJetsByPt;
    WrappedTH1 *hMCBtaggedBJetsByPt;
    WrappedTH1 *hMCBtaggedCJetsByPt;
    WrappedTH1 *hMCBtaggedLightJetsByPt;
    WrappedTH1 *hMCBmistaggedBJetsByPt;
    WrappedTH1 *hMCBmistaggedCJetsByPt;
    WrappedTH1 *hMCBmistaggedLightJetsByPt;
    WrappedTH2 *hMCAllBJetsByPtAndEta;
    WrappedTH2 *hMCAllCJetsByPtAndEta;
    WrappedTH2 *hMCAllLightJetsByPtAndEta;
    WrappedTH2 *hMCBtaggedBJetsByPtAndEta;
    WrappedTH2 *hMCBtaggedCJetsByPtAndEta;
    WrappedTH2 *hMCBtaggedLightJetsByPtAndEta;
    WrappedTH2 *hMCBmistaggedBJetsByPtAndEta;
    WrappedTH2 *hMCBmistaggedCJetsByPtAndEta;
    WrappedTH2 *hMCBmistaggedLightJetsByPtAndEta;
    // Scale factor histograms (needed for evaluating syst. uncertainty of b-tagging in datacard generator)
    WrappedTH1 *hScaleFactor;
    WrappedTH1 *hBTagAbsoluteUncertainty;
    WrappedTH1 *hBTagRelativeUncertainty;
    WrappedTH1 *hProbabilityForPassingBtag;
   };
}

#endif
