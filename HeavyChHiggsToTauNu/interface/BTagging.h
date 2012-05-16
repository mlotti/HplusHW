// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_BTagging_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DirectionalCut.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTaggingScaleFactorFromDB.h"

namespace edm {
  class ParameterSet;
}

class TH1;

namespace HPlus {
  class JetSelection;

  class BTagging {
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
      const int getBJetCount() const { return fBTagging->iNBtags; }
      const double getMaxDiscriminatorValue() const { return fBTagging->fMaxDiscriminatorValue; }
      const double getScaleFactor() const { return fBTagging->fScaleFactor; }
      const double getScaleFactorAbsoluteUncertainty() const { return fBTagging->fScaleFactorAbsoluteUncertainty; }
      const double getScaleFactorRelativeUncertainty() const { return fBTagging->fScaleFactorRelativeUncertainty; }
      void fillScaleFactorHistograms();

    private:
      const BTagging *fBTagging;
      const bool fPassedEvent;
    };
    
    BTagging(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight);  
    ~BTagging();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<pat::Jet>& jets);

    const std::string getDiscriminator() const { return fDiscriminator; }

  private:
    void applyScaleFactor(const edm::PtrVector<pat::Jet>& jets, const edm::PtrVector<pat::Jet>& bjets);

    // Input parameters                                                                                                                                                                          
    edm::InputTag fSrc;

    // Input parameters
    const double fPtCut;
    const double fEtaCut;
    const std::string fDiscriminator;
    const double fDiscrCut;
    DirectionalCut fNumberOfBJets;
    const uint32_t fMin;

    BTaggingScaleFactorFromDB *btagDB;
    bool FactorsFromDB;

    // Lookup tables for scale factors
    BTaggingScaleFactor fBTaggingScaleFactor;
    TH1* hBTagAbsoluteUncertainty;
    TH1* hBTagRelativeUncertainty;

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
    TH1 *hPtB33;
    TH1 *hEtaB33;
    TH1 *hPtB17;
    TH1 *hEtaB17;
    TH1 *hPtBnoTag;
    TH1 *hEtaBnoTag;
    TH1 *hDiscrQ;
    TH1 *hPtQ33;
    TH1 *hEtaQ33;
    TH1 *hPtQ17;
    TH1 *hEtaQ17;
    TH1 *hPtQnoTag;
    TH1 *hEtaQnoTag;
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
    double fScaleFactorAbsoluteUncertainty;
    double fScaleFactorRelativeUncertainty;
  };
}

#endif
