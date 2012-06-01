// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FullHiggsMassCalculator_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FullHiggsMassCalculator_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
//#include "PhysicsTools/Utilities/interface/Lumi3DReWeighting.h" // no longer needed for Fall11

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TH1;
class TVector3;

namespace HPlus {
  class FullHiggsMassCalculator {
  public:
    class Data {
    public:
      Data(const FullHiggsMassCalculator* calculator, bool passEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      double getHiggsMass() const { return fCalculator->fHiggsMassSolution; }

    private:
      const FullHiggsMassCalculator* fCalculator;
      const bool fPassedEvent;
    };

    FullHiggsMassCalculator(EventCounter& eventCounter, EventWeight& eventWeight);
    ~FullHiggsMassCalculator();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData);
    void myBJet();

  private:
    bool doMCMatching(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& tau, const edm::Ptr<pat::Jet>& bjet);
    void doCalculate(TVector3& tau, TVector3& bjet, TVector3& met, bool doHistogramming = true);

  private:
    // EventWeight object
    EventWeight& fEventWeight;
    //edm::InputTag fVertexSrc;
    //TH1 *hWeights;

    // Calculated results
    double fTopMassSolution;
    double fNeutrinoZSolution;
    double fNeutrinoPtSolution;
    double fHiggsMassSolution;

    // Histograms
    TH1* hHiggsMass;
    TH1* hHiggsMassReal;
    TH1* hHiggsMassImaginary;
    TH1* hTopMass;
    TH1* hTopMassRejected;
    TH1* hTopMassReal;
    TH1* hTopMassRealRejected;
    TH1* hTopMassImaginary;
    TH1* hTopMassImaginaryRejected;
    TH1* hNeutrinoZSolution;
    TH1* hNeutrinoPtSolution;
    TH1* hNeutrinoPtDifference;
  };
}

#endif
