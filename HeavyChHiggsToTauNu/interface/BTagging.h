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

namespace edm {
  class Event;
  class EventSetup;
  class ParameterSet;
}

class BTaggingScaleFactorFromDB;

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;
  class WrappedTH2;

  class BTagging: public BaseSelection {
  public:
    class Data; // Forward declare because it is used in ScaleFactorTable interface

  private:
    class EfficiencyTable; // Forward declared because ScaleFactorTable interface uses it

    class ScaleFactorTable {
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

      double getScaleFactor(double pt) const;
      double getScaleFactorUncertaintyBinned(double pt) const;

      size_t obtainIndex(double pt) { return obtainIndex(fPtBins, pt); }

      double calculateRelativeUncertaintySquared(bool up);

      void printJetTableForValidation();

    private:
      static size_t obtainIndex(const std::vector<double>& table, double pt);

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

    class EfficiencyTable {
    public:
      EfficiencyTable();
      ~EfficiencyTable();

      void setEfficiencyTable(const std::vector<double>& ptBinTable, const std::vector<double>& efficiencyTable, const std::vector<double>& uncertaintyUpTable, const std::vector<double>& uncertaintyDownTable);
      void resetJetTable();
      void addJetSFUncertaintyTerm(double pT, bool isBTagged, ScaleFactorTable& sfTable);

      double getEfficiency(double pT) const;

      size_t obtainIndex(double pt) { return obtainIndex(fPtBins, pt); }

      double calculateRelativeUncertaintySquared(bool up);

    private:
      static size_t obtainIndex(const std::vector<double>& table, double pt);

      // Efficiency look-up table
      std::vector<double> fPtBins; // lower edges of pT bins
      std::vector<double> fEfficiency; // Efficiency of (mis)tagging jet as a b-jet
      std::vector<double> fEffUncertUp; // Uncertainty of (mis)tagging efficienc
      std::vector<double> fEffUncertDown; // Uncertainty of (mis)tagging efficiency
      // Vectors for storing jet info for the calculation of the weight uncertainty
      std::vector<double> fPerBinUncertaintyUp;
      std::vector<double> fPerBinUncertaintyDown;
    };

    struct PerJetInfo {
      std::vector<double> fScaleFactor; // perJetWeight
      std::vector<double> fUncertainty; // perJetWeightUncert
      std::vector<bool> fTagged;        // b-tagging status
      std::vector<bool> fGenuine;       // genuine b-jet?
      
      void reserve(size_t s) {
        fScaleFactor.reserve(s);
        fUncertainty.reserve(s);
        fTagged.reserve(s);
        fGenuine.reserve(s);
      }
      
      size_t size() const { return fScaleFactor.size(); }
      
      void addJetSFTerm(double pT, bool isBTagged, ScaleFactorTable& sfTable, EfficiencyTable& effTable);
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
      const double getScaleFactorAbsoluteUncertainty_up() const { return fEventSFAbsUncert_up; }
      const double getScaleFactorAbsoluteUncertainty_down() const { return fEventSFAbsUncert_down; }
      const double getScaleFactorRelativeUncertainty_up() const { return fEventSFRelUncert_up; }
      const double getScaleFactorRelativeUncertainty_down() const { return fEventSFRelUncert_down; }

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
    };

    BTagging(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~BTagging();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);

    void fillScaleFactorHistograms(BTagging::Data& input);

    const std::string getDiscriminator() const { return fDiscriminator; }

    //PerJetInfo getPerJetInfo(PerJetInfo& bTaggingInfo) const { return bTaggingInfo; } //// Get rid of this function (still required by some plugin)
    void calculateJetSFAndUncertaintyTerm(edm::Ptr<pat::Jet>& iJet, bool isBTagged, PerJetInfo& info, ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag) const;
    double calculateEventScaleFactor(PerJetInfo& bTaggingInfo);
    double calculateRelativeEventScaleFactorUncertainty(bool up, ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag);
    
  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);
    void analyzeMCTagEfficiencyByJetFlavour(const edm::Ptr<pat::Jet>& jet, const bool isBJet, const bool isCJet, const bool isLightJet);
    void setEventScaleFactorInfo(PerJetInfo& bTaggingInfo, ScaleFactorTable& sfTag, ScaleFactorTable& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effCMistag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag, BTagging::Data& output);

    // Input parameters
    edm::InputTag fSrc;

    // Input parameters
    const double fPtCut;
    const double fEtaCut;
    const std::string fDiscriminator;
    const double fLeadingDiscrCut;
    const double fSubLeadingDiscrCut;
    DirectionalCut fNumberOfBJets;

    const bool fVariationEnabled;
    const double fVariationShiftBy;

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
  };
}

#endif
