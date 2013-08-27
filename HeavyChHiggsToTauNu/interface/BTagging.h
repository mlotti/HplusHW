// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DirectionalCut.h"

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
    class Data; // Forward declare because it is used in BTaggingScaleFactor interface
    struct PerJetInfo {
      std::vector<double> scaleFactor; // perJetWeight
      std::vector<double> uncertainty; // perJetWeightUncert
      std::vector<bool> tagged;        // 
      std::vector<bool> genuine;       // 

      void reserve(size_t s) {
        scaleFactor.reserve(s);
        uncertainty.reserve(s);
        tagged.reserve(s);
        genuine.reserve(s);
      }

      size_t size() const { return scaleFactor.size(); }
    };

    struct NumberOfJetsPerBin {
      std::vector<int> nTagB; // Number of b-tagged b- and c-flavor jets. C-jets are counted double as this is the simplest way of obtaining the correct uncertainty for them.
      std::vector<int> nTagG; // Number of b-tagged gluon jets
      std::vector<int> nTagUDS; // Number of b-tagged u/d/s-jets
      std::vector<int> nNoTagB; // Number of not b-tagged b- and c-flavor jets. C-jets are counted double (see above)
      std::vector<int> nNoTagG; // Number of not b-tagged gluon jets
      std::vector<int> nNoTagUDS; // Number of not b-tagged u/d/s-jets

      void initialize(size_t s) {
        size_t i = 0;
	while (i < s) {
	  nTagB.push_back(0);
	  nTagG.push_back(0);
	  nTagUDS.push_back(0);
	  nNoTagB.push_back(0);
	  nNoTagG.push_back(0);
	  nNoTagUDS.push_back(0);
	  i++;
	}
      }
    };

    ////struct PerJetWeightData
    struct WeightWithUncertainty {
      double weight;
      NumberOfJetsPerBin jetsPerSFBin;
      NumberOfJetsPerBin jetsPerEffBin;
    };

  private:
    class BTaggingScaleFactor {
    public:
      BTaggingScaleFactor();
      ~BTaggingScaleFactor();

      void addScaleFactorData(double pT, double scaleFactor, double scaleFactorUncertainty);
   
      static double calculateScaleFactor(const PerJetInfo& info);
      static double calculateAbsoluteUncertainty(const PerJetInfo& info);
      static double calculateRelativeUncertainty(const PerJetInfo& info);

      double getScaleFactor(double, double) const;
      double getScaleFactorUncertainty(double, double) const;
      double calculateMistagScaleFactor(double) const;

      size_t getNumberOfBins() { return fPtBins.size(); }
      size_t obtainIndex(double pt) { return obtainIndex(fPtBins, pt); }

    private:
      static size_t obtainIndex(const std::vector<double>& table, double pt);

      std::vector<double> fPtBins; // lower edges of pT bins
      std::vector<double> fScaleFactor; // b-tagging scale factor
      std::vector<double> fScaleFactorUncertainty; // b-tagging scale factor uncertainty
    };

    class EfficiencyTable {
    public:
      EfficiencyTable();
      ~EfficiencyTable();

      void addEfficiencyData(double pT, double efficiency, double effUncertainty);

      double getEfficiency(double) const;
      double getEffUncertainty(double) const;

      size_t getNumberOfBins() { return fPtBins.size(); }
      size_t obtainIndex(double pt) { return obtainIndex(fPtBins, pt); }
    private:
      static size_t obtainIndex(const std::vector<double>& table, double pt);

      std::vector<double> fPtBins; // lower edges of pT bins
      std::vector<double> fEfficiency; // Efficiency of (mis)tagging jet as a b-jet
      std::vector<double> fEffUncertainty; // Uncertainty of (mis)tagging efficiency
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
      const double getScaleFactor() const { return fScaleFactor; }
      const double getScaleFactorAbsoluteUncertainty() const { return fScaleFactorAbsoluteUncertainty; }
      const double getScaleFactorRelativeUncertainty() const { return fScaleFactorRelativeUncertainty; }
      const bool hasGenuineBJets() const;

      friend class BTagging;

    private:
      bool fPassedEvent;
      // Selected jets
      edm::PtrVector<pat::Jet> fSelectedJets;
      edm::PtrVector<pat::Jet> fSelectedSubLeadingJets;
      int iNBtags;
      double fMaxDiscriminatorValue;
      double fScaleFactor;
      double fScaleFactorAbsoluteUncertainty;
      double fScaleFactorRelativeUncertainty;
    };

    BTagging(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~BTagging();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);

    void fillScaleFactorHistograms(BTagging::Data& input);

    const std::string getDiscriminator() const { return fDiscriminator; }

    PerJetInfo getPerJetInfo(const edm::PtrVector<pat::Jet>& jets, const Data& btagData, bool isData) const;
    WeightWithUncertainty calculateJetWeight(edm::Ptr<pat::Jet>& iJet, bool isBTagged, BTaggingScaleFactor& sfTag, BTaggingScaleFactor& sfMistag, EfficiencyTable& effTag, EfficiencyTable& effGMistag, EfficiencyTable& effUDSMistag) const;
    
  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);
    void analyzeMCTagEfficiencyByJetFlavour(const edm::Ptr<pat::Jet>& jet, const bool isBJet, const bool isCJet, const bool isLightJet);
    void calculateScaleFactorInfo(PerJetInfo& bTaggingInfo, BTagging::Data& output);

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

    // Objects for storing weight information
    PerJetInfo fBTaggingInfo;
    NumberOfJetsPerBin fJetsPerSFBin;
    NumberOfJetsPerBin fJetsPerEffBin;

    // Lookup tables for scale factors
    BTaggingScaleFactor fTagSFTable;
    BTaggingScaleFactor fMistagSFTable;

    // Lookup tables for tagging efficiencies in MC
    EfficiencyTable fTagEffTable;
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
    WrappedTH1 *hDiscriminatorB;
    WrappedTH1 *hPtBCSVT;
    WrappedTH1 *hEtaBCSVT;
    WrappedTH1 *hPtBCSVM;
    WrappedTH1 *hEtaBCSVM;
    WrappedTH1 *hPtBnoTag;
    WrappedTH1 *hEtaBnoTag;
    WrappedTH1 *hDiscriminatorQ;
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
    // Scale factor histograms (needed for evaluating syst. uncertainty of btagging in datacard generator)
    WrappedTH1 *hScaleFactor;
    WrappedTH1 *hBTagAbsoluteUncertainty;
    WrappedTH1 *hBTagRelativeUncertainty;
  };
}

#endif
