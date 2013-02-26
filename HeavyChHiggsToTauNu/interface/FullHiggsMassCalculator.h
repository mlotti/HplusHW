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

#include "TString.h"
#include "TVector3.h"
#include "TLorentzVector.h"

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

//class TVector3;
class TLorentzVector;

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class FullHiggsMassCalculator: public BaseSelection {
  public:
    class Data {
    public:
      Data();
      ~Data();
      const bool passedEvent() const { return bPassedEvent; }
      //const edm::Ptr<pat::Jet>& getBjetHiggsSide() const { return BjetHiggsSide; }
      const edm::Ptr<pat::Jet>& getHiggsSideBJet() const { return HiggsSideBJet; }
      const double getDiscriminant() const { return fDiscriminant; }
      const double getHiggsMass() const { return fHiggsMassSolution; }
      const double getTopMass() const { return fTopMassSolution; }
      const double getNeutrinoZ() const { return fNeutrinoZSolution; }
      const double getNeutrinoPt() const { return fNeutrinoPtSolution; }
      const double getMCNeutrinoZ() const { return fMCNeutrinoPz; }
      const double getPhysicalTopMass() const { return c_fPhysicalTopMass; }
      const double getPhysicalTauMass() const { return c_fPhysicalTauMass; }
      const double getPhysicalBeautyMass() const { return c_fPhysicalBeautyMass; }
      // string getEventClass()
      
      //      const edm::Ptr<pat::Jet>& getSelectedBjet() const { return fCalculator->selectedBjet; }

      friend class FullHiggsMassCalculator;
    private:
      bool bPassedEvent;
      edm::Ptr<pat::Jet> HiggsSideBJet;
      // Calculated results
      double fDiscriminant;
      double fTopMassSolution;
      double fNeutrinoZSolution;
      double fNeutrinoPtSolution;
      double fHiggsMassSolution;
      double fMCNeutrinoPz;
      TVector3 visibleTau; // TODO: make notation Hungarian
      TVector3 mcNeutrinos;
      TVector3 mcBjetHiggsSide;
      TLorentzVector LorentzVector_bJetFourMomentum;
      TLorentzVector LorentzVector_visibleTauFourMomentum;
      TLorentzVector LorentzVector_neutrinosFourMomentum;
      // Event classification results
      //string eventClass;
      // Physical parameters of the particles
      const double c_fPhysicalTopMass;
      const double c_fPhysicalTauMass;
      const double c_fPhysicalBeautyMass;
    };

    FullHiggsMassCalculator(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~FullHiggsMassCalculator();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData);

    void myBJet();

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData);
    edm::Ptr<pat::Jet> findHiggsSideBJet(const BTagging::Data bData, const TauSelection::Data tauData);
    //bool doMCMatching(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& tau, const edm::Ptr<pat::Jet>& bjet, FullHiggsMassCalculator::Data& output);
    void calculateNeutrinoPz(TVector3& pTau, TVector3& pB, TVector3& MET,
			     FullHiggsMassCalculator::Data& physicalParameters, FullHiggsMassCalculator::Data& output);
    void constructFourMomenta(TVector3& pTau, TVector3& pB, TVector3& MET,
			      FullHiggsMassCalculator::Data& physicalParameters,
			      FullHiggsMassCalculator::Data& output);
    void calculateTopMass(FullHiggsMassCalculator::Data& output);
    void calculateHiggsMass(FullHiggsMassCalculator::Data& output);
    void doEventClassification(const edm::Event& iEvent, edm::Ptr<pat::Jet> recoHiggsSideBJet);
    void fillHistograms_MC(FullHiggsMassCalculator::Data& output);
    void fillHistograms_Data(FullHiggsMassCalculator::Data& output);
    void print(TString infoText);

  private:


    // EventWeight object
    /////////////////////////////////////////////    EventWeight& fEventWeight;
    //edm::InputTag fVertexSrc;
    //TH1 *hWeights;

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
    WrappedTH1* hHiggsMassNoActualHiggs;
    WrappedTH1* hHiggsMassCorrectId;
    WrappedTH1* hHiggsMassIncorrectId;
  };
}

#endif
