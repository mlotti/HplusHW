// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FullHiggsMassCalculator_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FullHiggsMassCalculator_h

#include "FWCore/Utilities/interface/InputTag.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
//#include "PhysicsTools/Utilities/interface/Lumi3DReWeighting.h" // no longer needed for Fall11

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TVector3;

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class FullHiggsMassCalculator {
  public:
    class Data {
    public:
      Data(const FullHiggsMassCalculator* calculator, bool passEvent);
      ~Data();

      bool passedEvent() const { return fPassedEvent; }
      double getHiggsMass() const { return fCalculator->fHiggsMassSolution; }
      //      const edm::Ptr<pat::Jet>& getSelectedBjet() const { return fCalculator->selectedBjet; }


    private:
      const FullHiggsMassCalculator* fCalculator;
      const bool fPassedEvent;
    };


    FullHiggsMassCalculator(EventCounter& eventCounter, HistoWrapper& histoWrapper);

    ~FullHiggsMassCalculator();

    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData);
    //    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData, const TopChiSelection::Data TopChiSelectionData );
    void myBJet();

  private:
    bool doMCMatching(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& tau, const edm::Ptr<pat::Jet>& bjet);
    void doCalculate(TVector3& tau, TVector3& bjet, TVector3& met, bool doHistogramming = true);

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
    //    edm::Ptr<pat::Jet> selectedBjet;

    // Histograms
 
    WrappedTH1* hSolution1PzDifference;
    WrappedTH1* hSolution2PzDifference;
    WrappedTH2* hSolution12PzDifference;
    WrappedTH1* hHiggsMass;
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
   
  };
}

#endif
