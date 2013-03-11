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
    static bool bPrintDebugOutput; //RENAME: s_bPrintDebugOutput
    // Physical parameters of the particles
    static double c_fPhysicalTopMass;
    static double c_fPhysicalTauMass;
    static double c_fPhysicalBeautyMass;

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
      const double getSelectedNeutrinoPzSolution() const { return fSelectedNeutrinoPzSolution; }
      const double getNeutrinoPtSolution() const { return fNeutrinoPtSolution; }
      const double getMCNeutrinoPz() const { return fMCNeutrinoPz; }
      // string getEventClass()
      
      //      const edm::Ptr<pat::Jet>& getSelectedBjet() const { return fCalculator->selectedBjet; }

      friend class FullHiggsMassCalculator;
    private:
      bool bPassedEvent;
      edm::Ptr<pat::Jet> HiggsSideBJet;
      // Calculated results
      double fDiscriminant;
      double fTopMassSolution;
      double fNeutrinoPzSolution1;
      double fNeutrinoPzSolution2;
      double fSelectedNeutrinoPzSolution;
      double fNeutrinoPtSolution;
      double fHiggsMassSolution;
      double fMCNeutrinoPz;
      TVector3 visibleTau;
      TVector3 mcNeutrinos;
      TVector3 mcBjetHiggsSide;
      TLorentzVector LorentzVector_bJetFourMomentum;
      TLorentzVector LorentzVector_visibleTauFourMomentum;
      TLorentzVector LorentzVector_neutrinosFourMomentum;
      // Event classification results
      TString strEventClassName;
    };

    FullHiggsMassCalculator(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~FullHiggsMassCalculator();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData,
		       const BTagging::Data& bData, const METSelection::Data& metData);
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> myTau,
		       const BTagging::Data& bData, const METSelection::Data& metData);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, 
		 const BTagging::Data& bData, const METSelection::Data& metData);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> myTau, 
		 const BTagging::Data& bData, const METSelection::Data& metData);

    void myBJet();

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> myTau, 
			const BTagging::Data& bData, const METSelection::Data& metData);
    edm::Ptr<pat::Jet> findHiggsSideBJet(const BTagging::Data bData, const edm::Ptr<pat::Tau> myTau);
    //bool doMCMatching(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& tau, const edm::Ptr<pat::Jet>& bjet, FullHiggsMassCalculator::Data& output);
    void calculateNeutrinoPz(TVector3& pTau, TVector3& pB, TVector3& MET, FullHiggsMassCalculator::Data& output);
    double getAngleBetweenNeutrinosAndTau(TVector3& pTau, TVector3& MET, double neutrinoPz);
    void constructFourMomenta(TVector3& pTau, TVector3& pB, TVector3& MET, FullHiggsMassCalculator::Data& output);
    void calculateTopMass(FullHiggsMassCalculator::Data& output);
    void calculateHiggsMass(FullHiggsMassCalculator::Data& output);
    void doEventClassification(const edm::Event& iEvent, TVector3& myBJetVector, TVector3& myVisibleTauVector, 
			       TVector3& myMETVector, FullHiggsMassCalculator::Data& output);
    void fillHistograms_MC(FullHiggsMassCalculator::Data& output);
    void fillHistograms_Data(FullHiggsMassCalculator::Data& output);

  private:

    // Counters
    Count fAllSolutionsCutSubCount;
    Count fPositiveDiscriminantCutSubCount;
    Count fNegativeDiscriminantCutSubCount;
    // two main categories of events (pure or impure):
    Count eventClass_Pure_SubCount;
    Count eventClass_Impure_SubCount;
    // detailed, mutually exclusive event classes:
    Count eventClass_OnlyBadTau_SubCount;
    Count eventClass_OnlyBadMET_SubCount;
    Count eventClass_OnlyBadTauAndMET_SubCount;
    Count eventClass_OnlyBadBjet_SubCount;
    Count eventClass_OnlyBadBjetAndTau_SubCount;
    Count eventClass_OnlyBadBjetAndMET_SubCount;
    Count eventClass_OnlyBadBjetAndMETAndTau_SubCount;
    // counts of all misidentifications of some object
    Count eventClass_AllBadTau_SubCount;
    Count eventClass_AllBadMET_SubCount;
    Count eventClass_AllBadBjet_SubCount;


    // Histograms 
    WrappedTH1* hSolution1PzDifference;
    WrappedTH1* hSolution2PzDifference;
    WrappedTH2* hSolution12PzDifference;
    WrappedTH1* hHiggsMass;
    WrappedTH1* hHiggsMassDPz100;
    WrappedTH1* hHiggsMass_TauBmatch;
    WrappedTH1* hHiggsMass_TauBMETmatch;
    //WrappedTH1* hHiggsMassReal;
    //WrappedTH1* hHiggsMassImaginary;
    WrappedTH1* hTopMass;
    //WrappedTH1* hTopMassRejected;
    //WrappedTH1* hTopMassReal;
    //WrappedTH1* hTopMassRealRejected;
    //WrappedTH1* hTopMassImaginary;
    //WrappedTH1* hTopMassImaginaryRejected;
    
    // Neutrino longitudinal momentum histograms
    WrappedTH1* hSelectedNeutrinoPzSolution;
    WrappedTH1* hNeutrinoPtSolution;
    WrappedTH1* hNeutrinoPtDifference;
    //WrappedTH1* hTrueHiggsMass;
    //WrappedTH1* hHiggsMassNoActualHiggs;
    //WrappedTH1* hHiggsMassCorrectId;
    //WrappedTH1* hHiggsMassIncorrectId;

    // Higgs mass histograms
    WrappedTH1* hHiggsMassPure;
    WrappedTH1* hHiggsMassImpure;
    WrappedTH1* hHiggsMassBadTau;
    WrappedTH1* hHiggsMassBadMET;
    WrappedTH1* hHiggsMassBadTauAndMET;
    WrappedTH1* hHiggsMassBadBjet;
    WrappedTH1* hHiggsMassBadBjetAndTau;
    WrappedTH1* hHiggsMassBadBjetAndMET;
    WrappedTH1* hHiggsMassBadBjetAndMETAndTau;
    WrappedTH1* hDiscriminantPure;
    WrappedTH1* hDiscriminantImpure;

    // Neutrino solution selection histograms
    WrappedTH1* hNeutrinosTauAngle1;
    WrappedTH1* hNeutrinosTauAngle2;

    // Event classification variable histograms
    WrappedTH1* hBDeltaR;
    WrappedTH1* hTauDeltaR;
    WrappedTH1* hMETDeltaPt;
    WrappedTH1* hMETDeltaPhi;
  };
}

#endif
