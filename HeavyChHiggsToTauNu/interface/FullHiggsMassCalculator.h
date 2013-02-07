// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FullHiggsMassCalculator_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FullHiggsMassCalculator_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "TVector3.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TVector3;

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class FullHiggsMassCalculator: public BaseSelection {
  public:
    class Data {
    public:
      Data(const FullHiggsMassCalculator* calculator, bool passEvent);
      ~Data();
      bool passedEvent() const { return fPassedEvent; }
      const edm::Ptr<pat::Jet>& getBjetHiggsSide() const { return fCalculator->BjetHiggsSide; }
      double getHiggsMass() const { return fCalculator->fHiggsMassSolution; }
      //      const edm::Ptr<pat::Jet>& getSelectedBjet() const { return fCalculator->selectedBjet; }


    private:
      const FullHiggsMassCalculator* fCalculator;
      const bool fPassedEvent;
    };

    FullHiggsMassCalculator(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~FullHiggsMassCalculator();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData);

    void myBJet();

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData);

    bool doMCMatching(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& tau, const edm::Ptr<pat::Jet>& bjet);
    void doCalculate(TVector3& tau, TVector3& bjet, TVector3& met, bool myMatchStaus=false, bool doHistogramming = true);
    void calculateTrueHiggsMass(const edm::Event& iEvent);

  private:


    // EventWeight object
    /////////////////////////////////////////////    EventWeight& fEventWeight;
    //edm::InputTag fVertexSrc;
    //TH1 *hWeights;

    // Calculated results
    double fTopMassSolution;
    double fNeutrinoZSolution;
    double fNeutrinoPtSolution;
    double fHiggsMassSolution;
    double NeutrinoPz;
    TVector3 visibleTau;
    TVector3 mcNeutrinos;
    TVector3 mcBjetHiggsSide;
    //   edm::Ptr<pat::Jet> mcBjetHiggsSide;

    // Histograms


    Count fAllSolutionsCutSubCount;
    Count fRealDiscriminantCutSubCount;
    Count fImaginarySolutionCutSubCount;
 
    WrappedTH1* hSolution1PzDifference;
    WrappedTH1* hSolution2PzDifference;
    WrappedTH2* hSolution12PzDifference;
    WrappedTH1* hHiggsMass;
    WrappedTH1* hHiggsMassDPz100;
    WrappedTH1* hHiggsMass_TauBmatch;
    WrappedTH1* hHiggsMass_TauBMETmatch;
    WrappedTH1* hHiggsMassReal;
    WrappedTH1* hHiggsMassImaginary;
    WrappedTH1* hTopMass;
    WrappedTH1* hTopMassRejected;
    WrappedTH1* hTopMassReal;
    WrappedTH1* hTopMassRealRejected;
    WrappedTH1* hTopMassImaginary;
    WrappedTH1* hTopMassImaginaryRejected;
    WrappedTH1* hNeutrinoZSolution;
    WrappedTH1* hNeutrinoPtSolution;
    WrappedTH1* hNeutrinoPtDifference;
    WrappedTH1* hTrueHiggsMass;
 
    edm::Ptr<pat::Jet> BjetHiggsSide;

   
  };
}

#endif
