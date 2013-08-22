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

    struct WeightWithUncertainty {
      double weight;
      double uncert;
    };

  private:
    class BTaggingScaleFactor {
    public:
      BTaggingScaleFactor();
      ~BTaggingScaleFactor();

      void UseDB(BTaggingScaleFactorFromDB*);
      
      void addBFlavorData(double pT, double scaleFactorB, double scaleFactorUncertaintyB, double epsilonMCB);
      void addNonBFlavorData(double pT, double scaleFactorL, double scaleFactorUncertaintyL, double epsilonMCL);
   
      static double calculateScaleFactor(const PerJetInfo& info);
      static double calculateAbsoluteUncertainty(const PerJetInfo& info);
      static double calculateRelativeUncertainty(const PerJetInfo& info);

      double getBtagScaleFactor(double,double) const;
      double getBtagScaleFactorError(double,double) const;
      double getMistagScaleFactor(double,double) const;
      double calculateMistagScaleFactor(double) const;
      double getMistagScaleFactorError(double,double) const;
      double getMCBtagEfficiency(double,double) const;
      double getMCMistagEfficiency(double,double) const;

    private:
      static size_t obtainIndex(const std::vector<double>& table, double pt);

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

    class EfficiencyTable {
    public:
      EfficiencyTable();
      ~EfficiencyTable();

      void addTagEfficiencyData(double pT, double efficiency, double effUncertainty);
      void addGMistagEfficiencyData(double pT, double efficiency, double effUncertainty);
      void addUDSMistagEfficiencyData(double pT, double efficiency, double effUncertainty);

      double getTagEfficiency(double) const;
      double getGMistagEfficiency(double) const;
      double getUDSMistagEfficiency(double) const;
      double getTagEffUncertainty(double) const;
      double getGMistagEffUncertainty(double) const;
      double getUDSMistagEffUncertainty(double) const;

    private:
      static size_t obtainIndex(const std::vector<double>& table, double pt);

      std::vector<double> fPtBinsTag; // lower edges of pT bins for b- and c-jets
      std::vector<double> fPtBinsGMistag; // lower edges of pT bins for g- and light quark jets
      std::vector<double> fPtBinsUDSMistag; // lower edges of pT bins for l-flavor jets
      std::vector<double> fEfficiencyTag; // Efficiency of (mis)tagging a b- or c-jet as a b-jet
      std::vector<double> fEfficiencyGMistag; // Efficiency of mistagging a gluon jet as a b-jet
      std::vector<double> fEfficiencyUDSMistag; // Efficiency of mistagging a light quark (u, d, s) jet as a b-jet
      std::vector<double> fEffUncertaintyTag; // Uncertainty of b- and c-jet (mis)tagging efficiency
      std::vector<double> fEffUncertaintyGMistag; // Uncertainty of gluon jet mistagging efficiency
      std::vector<double> fEffUncertaintyUDSMistag; // Uncertainty of light quark jet mistagging efficiency
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
    WeightWithUncertainty calculateJetWeight(edm::Ptr<pat::Jet>&, bool, BTaggingScaleFactor& sf, EfficiencyTable& eff) const;
    
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
    BTaggingScaleFactorFromDB *btagDB;
    bool FactorsFromDB;

    // Object for storing weigth information
    PerJetInfo fBTaggingInfo;

    // Lookup tables for scale factors
    BTaggingScaleFactor fBTaggingScaleFactor;

    // Lookup tables for tagging efficiencies in MC
    EfficiencyTable fEfficiencyTable;

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
