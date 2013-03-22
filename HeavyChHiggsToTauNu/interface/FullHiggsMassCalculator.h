// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FullHiggsMassCalculator_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FullHiggsMassCalculator_h

#include "FWCore/Utilities/interface/InputTag.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TopChiSelection.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleAnalysis.h"

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
    enum EventClassCode {
      // Explanation: the integers can be understood as a three-digit binary code keeping track of eventual misidentifications
      // First digit: b-jet                          |      Example:   B M T
      // Second digit: MET                           |                 -----
      // Third digit: tau                            |                 1 0 1
      ePure = 0,
      eOnlyBadTau = 1,
      eOnlyBadMET = 10,
      eOnlyBadTauAndMET = 11,
      eOnlyBadBjet = 100,
      eOnlyBadBjetAndTau = 101,
      eOnlyBadBjetAndMET = 110,
      eOnlyBadBjetAndMETAndTau = 111
    };
    
    enum PzSelectionMethod {
      eGreater,
      eSmaller,
      eTauNuAngleMax,
      eTauNuAngleMin,
      eTauNuDeltaEtaMax,
      eTauNuDeltaEtaMin
    };

    enum InputDataType {
      eRECO,
      eGEN,
      eGEN_NeutrinosReplacedWithMET
    };

    class Data {
    public:
      Data();
      ~Data();
      const bool passedEvent() const { return bPassedEvent; }
      //const edm::Ptr<pat::Jet>& getBjetHiggsSide() const { return BjetHiggsSide; }
      const double getDiscriminant() const { return fDiscriminant; }
      const double getHiggsMass() const { return fHiggsMassSolution; }
      const double getTopMass() const { return fTopMassSolution; }
      const double getSelectedNeutrinoPzSolution() const { return fSelectedNeutrinoPzSolution; }
      const double getNeutrinoPtSolution() const { return fNeutrinoPtSolution; }
      const double getTrueNeutrinoPz() const { return fTrueNeutrinoPz; }
      const EventClassCode getEventClassCode() const { return eEventClassCode; }

      friend class FullHiggsMassCalculator;
    private:
      bool bPassedEvent;
      // Calculated results
      double fDiscriminant;
      double fTopMassSolution;
      double fNeutrinoPzSolution1;
      double fNeutrinoPzSolution2;
      double fSelectedNeutrinoPzSolution;
      double fNeutrinoPtSolution;
      double fHiggsMassSolution;
      double fTrueNeutrinoPz;
      TVector3 visibleTau;
      TVector3 mcNeutrinos;
      TVector3 mcBjetHiggsSide;
      TLorentzVector LorentzVector_bJetFourMomentum;
      TLorentzVector LorentzVector_visibleTauFourMomentum;
      TLorentzVector LorentzVector_neutrinosFourMomentum;
      // Neutrino p_z solution selection
      double fNeutrinoPzSolutionGreater;
      double fNeutrinoPzSolutionSmaller;
      double fNeutrinoPzSolutionTauNuAngleMax;
      double fNeutrinoPzSolutionTauNuAngleMin;
      double fNeutrinoPzSolutionTauNuDeltaEtaMax;
      double fNeutrinoPzSolutionTauNuDeltaEtaMin;
      // Event classification results
      EventClassCode eEventClassCode;
    };

    FullHiggsMassCalculator(EventCounter& eventCounter, HistoWrapper& histoWrapper);
    ~FullHiggsMassCalculator();

    // Use silentAnalyze if you do not want to fill histograms or increment counters
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData,
		       const BTagging::Data& bData, const METSelection::Data& metData, 
		       const GenParticleAnalysis::Data* genDataPtr = NULL);
    Data silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> myTau,
		       const BTagging::Data& bData, const METSelection::Data& metData, 
		       const GenParticleAnalysis::Data* genDataPtr = NULL);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, 
		 const BTagging::Data& bData, const METSelection::Data& metData, 
		 const GenParticleAnalysis::Data* genDataPtr = NULL);
    Data analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> myTau, 
		 const BTagging::Data& bData, const METSelection::Data& metData, 
		 const GenParticleAnalysis::Data* genDataPtr = NULL);

  private:
    Data privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::Ptr<pat::Tau> myTau, 
			const BTagging::Data& bData, const METSelection::Data& metData,
			const GenParticleAnalysis::Data* genDataPtr = NULL);
    edm::Ptr<pat::Jet> findHiggsSideBJet(const BTagging::Data bData, const edm::Ptr<pat::Tau> myTau); // TODO: change name
    // "selectBJetClosestToTau"?
    void doCalculations(TVector3& tauVector, TVector3& bJetVector, TVector3& METVector,
			FullHiggsMassCalculator::Data& output, InputDataType myInputDataType);
    void calculateNeutrinoPz(TVector3& pB, TVector3& pTau, TVector3& MET, FullHiggsMassCalculator::Data& output);
    double selectNeutrinoPzSolution(TVector3& pTau, TVector3& MET, FullHiggsMassCalculator::Data& output,
				  PzSelectionMethod selectionMethod);
    double getAngleBetweenNeutrinosAndTau(TVector3& pTau, TVector3& MET, double neutrinoPz);
    double getDeltaEtaBetweenNeutrinosAndTau(TVector3& pTau, TVector3& MET, double neutrinoPz);
    bool selectedSolutionIsClosestToTrueValue(double selectedSolution, FullHiggsMassCalculator::Data& output);
    void constructFourMomenta(TVector3& pB, TVector3& pTau, TVector3& MET, FullHiggsMassCalculator::Data& output);
    void calculateTopMass(FullHiggsMassCalculator::Data& output);
    void calculateHiggsMass(FullHiggsMassCalculator::Data& output);
    void doEventClassification(const edm::Event& iEvent, TVector3& bJetVector, TVector3& tauVector, 
			       TVector3& METVector, FullHiggsMassCalculator::Data& output, 
			       const GenParticleAnalysis::Data* genDataPtr = NULL);
    void doCountingAndHistogramming(FullHiggsMassCalculator::Data& output, InputDataType myInputDataType);
    void analyzeMETComposition(TVector3& recoMETVector, TVector3& genBothNeutrinosVector, TVector3& genMETVector);
    
  private:

    // Counters
    // Discriminant and neutrino p_z calculation
    Count fAllSolutionsCutSubCount; // all calculations
    Count fPositiveDiscriminantCutSubCount;
    Count fNegativeDiscriminantCutSubCount;
    // Selection of the neutrino p_z solution
    Count fAllSelections_SubCount;
    Count fSelectionGreaterCorrect_SubCount;
    Count fSelectionSmallerCorrect_SubCount;
    Count fSelectionTauNuAngleMaxCorrect_SubCount;
    Count fSelectionTauNuAngleMinCorrect_SubCount;
    Count fSelectionTauNuDeltaEtaMaxCorrect_SubCount;
    Count fSelectionTauNuDeltaEtaMinCorrect_SubCount;
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
    // The most important ones at the moment
    WrappedTH1* hHiggsMass;
    WrappedTH1* hHiggsMass_GEN;
    WrappedTH1* hHiggsMass_GEN_NeutrinosReplacedWithMET;
    WrappedTH1* hDiscriminant;
    WrappedTH1* hDiscriminant_GEN;
    WrappedTH1* hDiscriminant_GEN_NeutrinosReplacedWithMET;

    WrappedTH1* hTopMassSolution;
    WrappedTH1* hTopInvariantMassInGenerator;
    WrappedTH1* hSelectedNeutrinoPzSolution;

    // Histograms for all the different solution selection methods
    //---RECO:
    WrappedTH1* hHiggsMass_greater;
    WrappedTH1* hHiggsMass_smaller;
    WrappedTH1* hHiggsMass_tauNuAngleMax;
    WrappedTH1* hHiggsMass_tauNuAngleMin;
    WrappedTH1* hHiggsMass_tauNuDeltaEtaMax;
    WrappedTH1* hHiggsMass_tauNuDeltaEtaMin;
    //---GEN:
    WrappedTH1* hHiggsMass_GEN_greater;
    WrappedTH1* hHiggsMass_GEN_smaller;
    WrappedTH1* hHiggsMass_GEN_tauNuAngleMax;
    WrappedTH1* hHiggsMass_GEN_tauNuAngleMin;
    WrappedTH1* hHiggsMass_GEN_tauNuDeltaEtaMax;
    WrappedTH1* hHiggsMass_GEN_tauNuDeltaEtaMin;
    //---GEN, neutrinos replaced with GENMET:
    WrappedTH1* hHiggsMass_GEN_NuToMET_greater;
    WrappedTH1* hHiggsMass_GEN_NuToMET_smaller;
    WrappedTH1* hHiggsMass_GEN_NuToMET_tauNuAngleMax;
    WrappedTH1* hHiggsMass_GEN_NuToMET_tauNuAngleMin;
    WrappedTH1* hHiggsMass_GEN_NuToMET_tauNuDeltaEtaMax;
    WrappedTH1* hHiggsMass_GEN_NuToMET_tauNuDeltaEtaMin;

    // Neutrino solution selection histograms
    WrappedTH1* hNeutrinosTauAngle1;
    WrappedTH1* hNeutrinosTauAngle2;

    // Event classification histograms
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

    // Event classification variable histograms
    WrappedTH1* hBDeltaR;
    WrappedTH1* hTauDeltaR;
    WrappedTH1* hMETDeltaPt;
    WrappedTH1* hMETDeltaPhi;
  };
}

#endif
