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

    enum MetSelectionMethod {
      eGreatestMagnitude,
      eSmallestMagnitude,
      eClosestToTopMass
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
      const double getHiggsMass() const { return fHiggsMassSolutionSelected; }
      const double getTopMass() const { return fTopMassSolutionSelected; }
      const double getSelectedNeutrinoPzSolution() const { return fNeutrinoPzSolutionSelected; }
      const double getNeutrinoPtSolution() const { return fNeutrinoPtSolution; }
      const double getMCNeutrinoPz() const { return fTrueNeutrinoPz; }
      const EventClassCode getEventClassCode() const { return eEventClassCode; }

      friend class FullHiggsMassCalculator;
    private:
      bool bPassedEvent;
      bool bNegativeDiscriminantRecovered;

      // Calculated results
      double fDiscriminant;

      double fTopMassSolutionSelected;
      double fTopMassSolution1;
      double fTopMassSolution2;

      double fNeutrinoPzSolution1;
      double fNeutrinoPzSolution2;
      double fNeutrinoPzSolutionSelected;

      double fModifiedMETSolution1;
      double fModifiedMETSolution2;
      double fModifiedMETSolutionSelected;

      double fHiggsMassSolution1;
      double fHiggsMassSolution2;
      double fHiggsMassSolutionSelected;

      double fNeutrinoPtSolution;
      double fTrueNeutrinoPz;
      TLorentzVector bJetFourMomentum;
      TLorentzVector visibleTauFourMomentum;
      TLorentzVector neutrinosFourMomentum1;
      TLorentzVector neutrinosFourMomentum2;
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

    FullHiggsMassCalculator(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper);
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
    void doCalculations(const edm::Event& iEvent, TVector3& tauVector, TVector3& bJetVector, TVector3& METVector,
			FullHiggsMassCalculator::Data& output, InputDataType myInputDataType);
    void calculateNeutrinoPz(TVector3& pTau, TVector3& pB, TVector3& MET, FullHiggsMassCalculator::Data& output);
    //bool calculateModifiedMET(TVector3& pB, TVector3& pTau, TVector3& MET, FullHiggsMassCalculator::Data& output);
    void selectNeutrinoPzAndHiggsMassSolution(FullHiggsMassCalculator::Data& output, PzSelectionMethod selectionMethod);
    double getAngleBetweenNeutrinosAndTau(TLorentzVector& tauFourMom, TLorentzVector& neutrinosFourMom);
    double getDeltaEtaBetweenNeutrinosAndTau(TLorentzVector& tauFourMom, TLorentzVector& neutrinosFourMom);
    double getDeltaRBetweenNeutrinosAndTau(TLorentzVector& tauFourMom, TLorentzVector& neutrinosFourMom);
    bool isBetterSolution(const edm::Event& iEvent, double selectedSolution, FullHiggsMassCalculator::Data& output);
    bool isBetterSolutionNoChargedHiggs(double selectedSolution, FullHiggsMassCalculator::Data& output);
    bool neutrinoPzSolutionOneWasSelected(double selectedSolution, FullHiggsMassCalculator::Data& output);
    bool neutrinoPzSolutionTwoWasSelected(double selectedSolution, FullHiggsMassCalculator::Data& output);
//     bool selectedSolutionGivesVectorClosestToTrue(const edm::Event& iEvent, double selectedSolution,
// 						  FullHiggsMassCalculator::Data& output, TVector3& MET);
    void constructFourMomenta(TVector3& pTau, TVector3& pB, TVector3& MET, FullHiggsMassCalculator::Data& output);
    void calculateTopMasses(FullHiggsMassCalculator::Data& output);
    void selectModifiedMETSolution(FullHiggsMassCalculator::Data& output);
    void selectModifiedMETSolution(FullHiggsMassCalculator::Data& output, MetSelectionMethod myMetSelectionMethod);
    void calculateHiggsMasses(FullHiggsMassCalculator::Data& output);
    bool modifiedMETSolutionOneWasSelected(FullHiggsMassCalculator::Data& output);
    bool modifiedMETSolutionTwoWasSelected(FullHiggsMassCalculator::Data& output);
    void doEventClassification(const edm::Event& iEvent, TVector3& bJetVector, TVector3& tauVector, 
			       TVector3& METVector, FullHiggsMassCalculator::Data& output, const METSelection::Data& metData,
			       const GenParticleAnalysis::Data* genDataPtr = NULL );
    void applyCuts(FullHiggsMassCalculator::Data& output);
    void doCountingAndHistogramming(const edm::Event& iEvent, FullHiggsMassCalculator::Data& output, InputDataType myInputDataType);
    void analyzeMETComposition(TVector3& recoMETVector, TVector3& genBothNeutrinosVector, TVector3& genMETVector);

    double fTopInvMassLowerCut;
    double fTopInvMassUpperCut;
    PzSelectionMethod fPzSelectionMethod;
    MetSelectionMethod fMetSelectionMethod;
    double fReApplyMetCut;

    // Counters
    // Discriminant and neutrino p_z calculation
    Count allEvents_SubCount; // all calculations
    Count positiveDiscriminant_SubCount;
    Count negativeDiscriminant_SubCount;
    // Selection of the neutrino p_z solution
    Count passedEvents_SubCount;
    Count selectionGreaterCorrect_SubCount;
    Count selectionSmallerCorrect_SubCount;
    Count selectionTauNuAngleMaxCorrect_SubCount;
    Count selectionTauNuAngleMinCorrect_SubCount;
    Count selectionTauNuDeltaEtaMaxCorrect_SubCount;
    Count selectionTauNuDeltaEtaMinCorrect_SubCount;

    // Old event classification:
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

    // New event classification:
    Count count_passedEvent;
    Count count_pure;
    Count count_tauGenuine;
    Count count_bGenuine;
    Count count_tauMeasurementGood;
    Count count_bMeasurementGood;
    Count count_tauAndBjetFromSameTopQuark;
    Count count_neutrinoMETCorrespondenceGood;

    // Histograms 
    // The most important ones at the moment
    WrappedTH1* hHiggsMass;
    WrappedTH1* hHiggsMassPositiveDiscriminant;
    WrappedTH1* hHiggsMassNegativeDiscriminant;
    WrappedTH1* hHiggsMass_GEN;
    WrappedTH1* hHiggsMass_GEN_NeutrinosReplacedWithMET;
    WrappedTH1* hDiscriminant;
    WrappedTH1* hDiscriminant_GEN;
    WrappedTH1* hDiscriminant_GEN_NeutrinosReplacedWithMET;
    WrappedTH2* h2TransverseMassVsInvariantMass;
    WrappedTH2* h2TransverseMassVsInvariantMassPositiveDiscriminant;
    WrappedTH2* h2TransverseMassVsInvariantMassNegativeDiscriminant;
    WrappedTH2* h2TopMassVsInvariantMass;
    WrappedTH2* h2TopMassVsNeutrinoNumber;
    WrappedTH2* h2InvariantMassVsNeutrinoNumber;
    WrappedTH2* h2MetSignificanceVsBadMet;

    WrappedTH1* hTopMassSolution;
    WrappedTH1* hSelectedNeutrinoPzSolution;

    WrappedTH1* hHiggsMass_betterSolution;
    WrappedTH1* hHiggsMass_worseSolution;

    WrappedTH1* hTopInvariantMassInGenerator;
    
    // Histograms that may be used to identify good cut possibilities
    WrappedTH1* hMETSignificance;
    WrappedTH1* hNeutrinoNumberInPassedEvents;
    WrappedTH1* hNeutrinoNumberInRejectedEvents;

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
    //WrappedTH1* hHiggsMass_GEN_closerToRestMass;
    //WrappedTH1* hHiggsMass_GEN_furtherFromRestMass;
    //---GEN, neutrinos replaced with GENMET:
    WrappedTH1* hHiggsMass_GEN_NuToMET_greater;
    WrappedTH1* hHiggsMass_GEN_NuToMET_smaller;
    WrappedTH1* hHiggsMass_GEN_NuToMET_tauNuAngleMax;
    WrappedTH1* hHiggsMass_GEN_NuToMET_tauNuAngleMin;
    WrappedTH1* hHiggsMass_GEN_NuToMET_tauNuDeltaEtaMax;
    WrappedTH1* hHiggsMass_GEN_NuToMET_tauNuDeltaEtaMin;
    //WrappedTH1* hHiggsMass_GEN_NuToMET_closerToRestMass;
    //WrappedTH1* hHiggsMass_GEN_NuToMET_furtherFromRestMass;

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
    WrappedTH1* hDeltaPhiTauAndMetForBadMet;
    WrappedTH1* hDeltaPhiTauAndBjetForBadMet;
    WrappedTH1* hDeltaRTauAndMetForBadMet;
    WrappedTH1* hDeltaRTauAndBjetForBadMet;

    // Event classification variable histograms
    WrappedTH1* hBDeltaR;
    WrappedTH1* hTauDeltaR;
    WrappedTH1* hMETDeltaPt;
    WrappedTH1* hMETDeltaPhi;
  };
}

#endif
