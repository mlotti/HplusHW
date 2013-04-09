/*
FullHiggsMassCalculator.cc

AUTHORS
???, Lauri Wendland, Stefan Richter

PURPOSE
Calculate the full mass of the (tau, nu_{tau}) system which could be
the decay product of a charged Higgs boson. This quantity is usually
referred to as the "full Higgs mass" for brevity.

METHOD
1) Reconstruct the tau neutrino's longitudinal momentum (p_{z}) by using
the mass of its grandmother top quark as a kinematical constraint:
                     t -> H+ b
                           `--> tau nu

      Variable naming examples:
      *************************
      on-shell masses          : tauMass
      momentum (three-)vectors : tauVector, tauPlusBVector
      MET (three-)vector       : MET
      energies                 : tauPlusBEnergy
      calculated solutions     : neutrinoPzSolutionMax, topMassSolution1 (contain the word "solution")

SHORTCOMINGS
1) Event classification does not check if anything is outside the detector acceptance area (eta > 2.1).
This should not cause any significant error, though.
*/

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventClassification.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "Math/GenVector/VectorUtil.h"
//#include "TLorentzVector.h"
#include "TVector3.h"
#include "TMath.h"
#include "TString.h"

std::vector<const reco::GenParticle*> getImmediateMothers(const reco::Candidate&);
std::vector<const reco::GenParticle*> getMothers(const reco::Candidate& p);
bool hasImmediateMother(const reco::Candidate& p, int id);
bool hasMother(const reco::Candidate& p, int id);
void printImmediateMothers(const reco::Candidate& p);
void printMothers(const reco::Candidate& p);
std::vector<const reco::GenParticle*> getImmediateDaughters(const reco::Candidate& p);
std::vector<const reco::GenParticle*> getDaughters(const reco::Candidate& p);
bool hasImmediateDaughter(const reco::Candidate& p, int id);
bool hasDaughter(const reco::Candidate& p, int id);
void printImmediateDaughters(const reco::Candidate& p);
void printDaughters(const reco::Candidate& p);

// Define NaN
//double nan = std::numeric_limits<double>::quiet_NaN();

namespace { 
  // (Containing these variables in an anonymous namespace prevents them from being accessed from code in another file)
  // Set this variable to true if you want debug print statements to be activated
  const bool bPrintDebugOutput = false;
  // Set this variable to true if you want to recover events with a negative discriminant using a special algorithm instead of
  // discarding them
  const bool bTryRecoveringNegativeDiscriminants = false;
  // Set the physical particle masses required in the calculation (in GeV)
  // Note: these are the values used in the generator. Therefore, they should also be used here even if they no longer correspond
  //       to the latest values given by the Particle Data Group.
  const double c_fPhysicalTopMass = 172.5;
  const double c_fPhysicalTauMass = 1.777;
  const double c_fPhysicalBeautyMass = 4.8;
}

namespace HPlus {
  FullHiggsMassCalculator::Data::Data():
    bPassedEvent(false),
    fDiscriminant(0),
    bNegativeDiscriminantRecovered(false),
    fTopMassSolution(0),
    fNeutrinoPzSolution1(0),
    fNeutrinoPzSolution2(0),
    fModifiedMET(0),
    fSelectedNeutrinoPzSolution(0),
    fNeutrinoPtSolution(0),
    fHiggsMassSolution(0),
    fTrueNeutrinoPz(0),
    LorentzVector_bJetFourMomentum(),
    LorentzVector_visibleTauFourMomentum(),
    LorentzVector_neutrinosFourMomentum(),
    fNeutrinoPzSolutionGreater(999999999.9),
    fNeutrinoPzSolutionSmaller(999999999.9),
    fNeutrinoPzSolutionTauNuAngleMax(999999999.9),
    fNeutrinoPzSolutionTauNuAngleMin(999999999.9),
    eEventClassCode()
  { }
  
  FullHiggsMassCalculator::Data::~Data() { }

  FullHiggsMassCalculator::FullHiggsMassCalculator(HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    // Define counters to be incremented during this analysis
    BaseSelection(eventCounter, histoWrapper),
    fAllSolutionsCutSubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "All neutrino p_z solutions")),
    fPositiveDiscriminantCutSubCount(eventCounter.addSubCounter("FullHiggsMassCalculator",
								"Positive discriminant in p_z calculation")),
    fNegativeDiscriminantCutSubCount(eventCounter.addSubCounter("FullHiggsMassCalculator",
								"Negative discriminant in p_z calculation")),
    eventClass_Pure_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Good identification of b-jet, tau, and MET")),
    eventClass_Impure_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator",
							  "Misidentification of b-jet and/or tau and/or MET")),
    eventClass_OnlyBadTau_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Only bad ID tau")),
    eventClass_OnlyBadMET_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Only bad ID MET")),
    eventClass_OnlyBadTauAndMET_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Only bad ID tau && MET")),
    eventClass_OnlyBadBjet_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Only bad ID b-jet")),
    eventClass_OnlyBadBjetAndTau_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Only bad ID b-jet && tau")),
    eventClass_OnlyBadBjetAndMET_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Only bad ID b-jet && MET")),
    eventClass_OnlyBadBjetAndMETAndTau_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator",
									   "Only bad ID b-jet && MET && tau")),
    eventClass_AllBadTau_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "All bad ID tau")),
    eventClass_AllBadMET_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "All bad ID MET")),
    eventClass_AllBadBjet_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "All bad ID b-jet")),
    fAllSelections_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Neutrino p_z solution selected")),
    fSelectionGreaterCorrect_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Greater solution closest")),
    fSelectionSmallerCorrect_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Smaller solution closest")),
    fSelectionTauNuAngleMaxCorrect_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator",
								       "TauNuAngleMax solution closest")),
    fSelectionTauNuAngleMinCorrect_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", 
								       "TauNuAngleMin solution closest")),
    fSelectionTauNuDeltaEtaMaxCorrect_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", 
									  "TauNuDeltaEtaMax solution closest")),
    fSelectionTauNuDeltaEtaMinCorrect_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", 
									  "TauNuDeltaEtaMin solution closest"))
  {
    // Add a new directory ("FullHiggsMass") for the histograms produced in this code to the output file
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("FullHiggsMass");
    // Book histograms to be filled by this code
    // Vital histograms
    hHiggsMass                = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "HiggsMass", 
							  "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN            = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "HiggsMass_GEN", 
							  "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_NeutrinosReplacedWithMET = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, 
									"HiggsMass_GEN_NeutrinosReplacedWithMET", 
									"Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hDiscriminant             = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Discriminant",
							  "Discriminant", 100, -50000, 50000);
    hDiscriminant_GEN         = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Discriminant_GEN",
							  "Discriminant", 100, -50000, 50000);
    hDiscriminant_GEN_NeutrinosReplacedWithMET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, 
									   "Discriminant_GEN_NeutrinosReplacedWithMET",
									   "Discriminant", 100, -50000, 50000);
    h2TransverseMassAndInvariantMass = histoWrapper.makeTH<TH2F>(HistoWrapper::kVital, myDir, "TransMassVsInvMass", 
	                      "TransMassVsInvMass;Transverse mass m_{T};Invariant mass m(#tau, #nu_{#tau});Events",
								 100, 0, 500, 100, 0, 500);
    // Informative histograms
    // Histograms for all the different solution selection methods
    //---RECO:
    hHiggsMass_greater        = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_greater", 
							  "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_smaller        = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_smaller", 
							  "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_tauNuAngleMax  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_tauNuAngleMax", 
							  "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_tauNuAngleMin  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_tauNuAngleMin", 
							  "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_tauNuDeltaEtaMax = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_tauNuDeltaEtaMax", 
							    "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_tauNuDeltaEtaMin = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_tauNuDeltaEtaMin", 
							    "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    //---GEN:
    hHiggsMass_GEN_greater        = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_GEN_greater", 
							      "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_smaller        = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_GEN_smaller", 
							      "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_tauNuAngleMax  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_GEN_tauNuAngleMax", 
							      "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_tauNuAngleMin  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_GEN_tauNuAngleMin", 
							      "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_tauNuDeltaEtaMax = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, 
								"HiggsMass_GEN_tauNuDeltaEtaMax", 
								"Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_tauNuDeltaEtaMin = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, 
								"HiggsMass_GEN_tauNuDeltaEtaMin", 
								"Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    //---GEN, neutrinos replaced with GENMET:
    hHiggsMass_GEN_NuToMET_greater        = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, 
								      "HiggsMass_GEN_NuToMET_greater", 
								      "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_NuToMET_smaller        = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, 
								      "HiggsMass_GEN_NuToMET_smaller", 
								      "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_NuToMET_tauNuAngleMax  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, 
								      "HiggsMass_GEN_NuToMET_tauNuAngleMax", 
								      "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_NuToMET_tauNuAngleMin  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, 
								      "HiggsMass_GEN_NuToMET_tauNuAngleMin", 
								      "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_NuToMET_tauNuDeltaEtaMax = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, 
									"HiggsMass_GEN_NuToMET_tauNuDeltaEtaMax", 
									"Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_NuToMET_tauNuDeltaEtaMin = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, 
									"HiggsMass_GEN_NuToMET_tauNuDeltaEtaMin", 
									"Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    // Others and event classification:
    hTopMassSolution          = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMassSolution", 
							  "Top mass solution;m_{top} (GeV)", 100, 0, 500);
    hSelectedNeutrinoPzSolution = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SelectedNeutrinoPzSolution", 
							  "Neutrino Z solution;p_{#nu,z} (GeV)", 100, -500, 500);
    hHiggsMassPure            = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassPure",
                                                          "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassImpure          = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassImpure",
                                                          "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassBadTau          = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassBadTau",
                                                          "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassBadMET          = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassBadMET",
                                                          "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassBadTauAndMET    = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassBadTauAndMET",
                                                          "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassBadBjet         = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassBadBjet",
                                                          "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassBadBjetAndTau   = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassBadBjetAndTau",
                                                          "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassBadBjetAndMET   = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassBadBjetAndMET",
                                                          "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassBadBjetAndMETAndTau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassBadBjetAndMETAndTau",
                                                          "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    // Quantities related to the neutrino longitudinal momentum calculation and solution selection

    hDiscriminantPure         = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DiscriminantPure",
							  "DiscriminantPure", 100, -50000, 50000);
    hDiscriminantImpure       = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DiscriminantImpure",
							  "DiscriminantImpure", 100, -50000, 50000);
    hNeutrinosTauAngle1       = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NeutrinosTauAngle1",
							  "Angle between neutrinos and tau;(degrees)", 180, -180, 180);
    hNeutrinosTauAngle2       = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NeutrinosTauAngle2",
							  "Angle between neutrinos and tau;(degrees)", 180, -180, 180);
    // Variables describing the quality of the reconstruction (used for event classification)
    hBDeltaR                  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "BDeltaR",
                                                          "B-jet #Delta R;#Delta R", 100, 0, 10);
    hTauDeltaR                = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TauDeltaR",
                                                          "Tau #Delta R;#Delta R", 100, 0, 10);
    hMETDeltaPt               = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "METDeltaPt",
                                                          "MET #Delta p_T;#Delta p_T (GeV)", 100, -200, 200);
    hMETDeltaPhi              = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "METDeltaPhi",
                                                          "MET #Delta #phi;#Delta #phi (degrees)", 180, -180, 180);
    // Generator information
    hTopInvariantMassInGenerator = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopInvariantMassInGenerator",
							     "Top invariant mass (GEN);m_{top} (GeV)", 100, 0, 500);
  }

  FullHiggsMassCalculator::~FullHiggsMassCalculator() {}

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const TauSelection::Data& tauData, const BTagging::Data& bData, const METSelection::Data& metData, 
  const GenParticleAnalysis::Data* genDataPtr) {
    ensureSilentAnalyzeAllowed(iEvent);
    // Disable histogram filling and counter incrementing until the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    // If this method is called with tauData as an argument, get the selected tau from it and pass it on to privateAnalyze():
    const edm::Ptr<pat::Tau> myTau = tauData.getSelectedTau();
    return privateAnalyze(iEvent, iSetup, myTau, bData, metData, genDataPtr);
  }

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const edm::Ptr<pat::Tau> myTau, const BTagging::Data& bData, const METSelection::Data& metData, 
  const GenParticleAnalysis::Data* genDataPtr) {
    ensureSilentAnalyzeAllowed(iEvent);
    // Disable histogram filling and counter incrementing until the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    return privateAnalyze(iEvent, iSetup, myTau, bData, metData, genDataPtr);
  }

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const TauSelection::Data& tauData, const BTagging::Data& bData, const METSelection::Data& metData, 
  const GenParticleAnalysis::Data* genDataPtr) {
    ensureAnalyzeAllowed(iEvent);
    // If this method is called with tauData as an argument, get the selected tau from it and pass it on to privateAnalyze():
    const edm::Ptr<pat::Tau> myTau = tauData.getSelectedTau();
    return privateAnalyze(iEvent, iSetup, myTau, bData, metData, genDataPtr);
  }

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const edm::Ptr<pat::Tau> myTau, const BTagging::Data& bData, const METSelection::Data& metData, 
  const GenParticleAnalysis::Data* genDataPtr) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, myTau, bData, metData, genDataPtr);
  }

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const edm::Ptr<pat::Tau> myTau, const BTagging::Data& bData, const METSelection::Data& metData, 
  const GenParticleAnalysis::Data* genDataPtr) {
    // Define a FullHiggsMassCalculator::Data object to hold many different values of interest and be returned at the end.
    Data output;
    if (bPrintDebugOutput) std::cout << "==================================================================" << std::endl;
    std::cout << "==================================================================" << std::endl;

    // CALCULATION USING RECONSTRUCTED MOMENTA
    // ---------------------------------------
    // Find the b-jet that is closest to the selected tau in (eta, phi) space this b-jet is assumed to come from the same 
    // side of the Feynman diagram as the selected tau.
    edm::Ptr<pat::Jet> selectedRecoBJet = FullHiggsMassCalculator::findHiggsSideBJet(bData, myTau);
    if (bPrintDebugOutput) {
      if (selectedRecoBJet.isNull()) std::cout << "No reco Higgs side b-jet found!The code will crash." << std::endl;
      else std::cout << "Reco Higgs side b-jet found" << std::endl;
    }
    TVector3 recoBJetVector(selectedRecoBJet->px(), selectedRecoBJet->py(), selectedRecoBJet->pz());
    TVector3 recoTauVector(myTau->px(), myTau->py(), myTau->pz());
    // The MET is the same as in the rest of the analysis (as it should be), normally (as of March 2013) Type 1 PF corrected.    
    TVector3 recoMETVector(metData.getSelectedMET()->px(), metData.getSelectedMET()->py(), metData.getSelectedMET()->pz());
    if (bPrintDebugOutput) {
      std::cout << "recoBJetVector: "<< recoBJetVector.Px() << ", "<< recoBJetVector.Py() << ", "<< recoBJetVector.Pz()<< std::endl;
      std::cout << "recoTauVector: " << recoTauVector.Px() << ", " << recoTauVector.Py() << ", " << recoTauVector.Pz() << std::endl;
      std::cout << "recoMETVector: " << recoMETVector.Px() << ", " << recoMETVector.Py() << ", " << recoMETVector.Pz() << std::endl;
    }
    doCalculations(iEvent, recoBJetVector, recoTauVector, recoMETVector, output, eRECO);
    // Classify MC events according to what was identified correctly and what was not
    if (!iEvent.isRealData())
      doEventClassification(iEvent, recoBJetVector, recoTauVector, recoMETVector, output, genDataPtr);

    // The rest of the analysis is only done for MC signal events with a light charged Higgs (at least for now)
    if (iEvent.isRealData() || !eventHasLightChargedHiggs(iEvent)) return output;

    // Histogram the invariant mass of the top mother of the Higgs.
    hTopInvariantMassInGenerator->Fill(getGenHiggsSideTop(iEvent)->mass());

    // CALCULATION USING TRUE MOMENTA FROM MC
    // --------------------------------------
    reco::Candidate* myGenBJet = getGenHiggsSideBJet(iEvent);
    TVector3 genBJetVector(myGenBJet->px(), myGenBJet->py(), myGenBJet->pz());
    reco::Candidate* myGenTau = getGenTauFromHiggs(iEvent);
    TVector3 genVisibleTauVector = getVisibleMomentum(*myGenTau);
    reco::Candidate* myGenNeutrino1 = getGenNeutrinoFromHiggs(iEvent);
    TVector3 myNeutrino1Vector(myGenNeutrino1->px(), myGenNeutrino1->py(), myGenNeutrino1->pz());
    // In addition to the above neutrino, we also need to take into account the one coming from the decay of the tau lepton:
    TVector3 myNeutrino2Vector = getInvisibleMomentum(*myGenTau);
    TVector3 genBothNeutrinosVector = myNeutrino1Vector + myNeutrino2Vector;
    // Set true value of neutrino p_z
    output.fTrueNeutrinoPz = genBothNeutrinosVector.Pz();
    doCalculations(iEvent, genBJetVector, genVisibleTauVector, genBothNeutrinosVector, output, eGEN);

    // NOTE: doEventClassification should only be called once for each event. DO NOT uncomment this line without commenting above!
    // doEventClassification(iEvent, genBJetVector, genVisibleTauVector, genBothNeutrinosVector, output, genDataPtr);


    // CALCULATION USING TRUE MOMENTA FROM MC FOR B-JET AND VISIBLE TAU, BUT GEN MET INSTEAD OF TAU NEUTRINO MOMENTA
    // -------------------------------------------------------------------------------------------------------------
    // B-jet and visible tau are as before.
    // If GenParticleAnalysis::Data* genData is available, the correct GenMET vector is retrieved from it.
    // If it is not available, an estimate for the GenMET is calculated by summing the momenta of all GEN neutrinos that were
    // not filtered from the event to save space.
    TVector3 genMETVector(0.0, 0.0, 0.0);
    if (genDataPtr != NULL) {
      edm::Ptr<reco::GenMET> myGenMET = genDataPtr->getGenMET();
      genMETVector.SetXYZ(myGenMET->px(), myGenMET->py(), myGenMET->pz());
    } else {
      genMETVector = calculateGenMETVectorFromNeutrinos(iEvent);
    }
    doCalculations(iEvent, genBJetVector, genVisibleTauVector, genMETVector, output, eGEN_NeutrinosReplacedWithMET);

    // Now we can also analyze the composition of the MET
    analyzeMETComposition(recoMETVector, genBothNeutrinosVector, genMETVector);
    
    output.bPassedEvent = true; // for now, later implement possibility to cut
    return output;
  }

  edm::Ptr<pat::Jet> FullHiggsMassCalculator::findHiggsSideBJet(const BTagging::Data bData, const edm::Ptr<pat::Tau> myTau) {
    double currentDeltaR = 1000.0;
    double smallestDeltaR = 999.0;
    edm::Ptr<pat::Jet> selectedRecoBJet;
    // Loop over b-jets with tight tag (selected jets)
    for (edm::PtrVector<pat::Jet>::iterator iBjet = bData.getSelectedJets().begin();
	 iBjet != bData.getSelectedJets().end(); ++iBjet) {
      // Calculate the distance in (eta, phi) space between them and the selected tau. Choose the b-jet that is closest to the tau
      currentDeltaR = ROOT::Math::VectorUtil::DeltaR((*iBjet)->p4(), myTau->p4());
      if (currentDeltaR < smallestDeltaR) {
        smallestDeltaR = currentDeltaR;
        selectedRecoBJet = *iBjet;
      }
    }
    // Loop over b-jets with looser tag (selected sub-leading jets), doing the same as above
    for (edm::PtrVector<pat::Jet>::iterator iBjet = bData.getSelectedSubLeadingJets().begin();
	 iBjet != bData.getSelectedSubLeadingJets().end(); ++iBjet) {
      currentDeltaR = ROOT::Math::VectorUtil::DeltaR((*iBjet)->p4(), myTau->p4());
      if (currentDeltaR < smallestDeltaR) {
        smallestDeltaR = currentDeltaR;
        selectedRecoBJet = *iBjet;
      }
    }
    // Whichever b-jet (leading or sub-leading) had the smallest angular distance from the selected tau is returned.
    return selectedRecoBJet;
  }

  void FullHiggsMassCalculator::doCalculations(const edm::Event& iEvent, TVector3& tauVector, TVector3& bJetVector, 
					       TVector3& METVector, 
					       FullHiggsMassCalculator::Data& output, InputDataType myInputDataType) {
    // Outline:
    // - Calculate the neutrino p_z solutions. Both are saved in output.
    // - Select which neutrino p_z solution is used for the mass calculations.
    // - Calculate the invariant mass of the top quark and the Higgs boson (or what might be one).
    // - Constructing the four-momenta first greatly simplifies the equations and makes the code more readable.

    calculateNeutrinoPz(tauVector, bJetVector, METVector, output);

    // Selection method: greater
    output.fNeutrinoPzSolutionGreater = selectNeutrinoPzSolution(tauVector, bJetVector, output, eGreater);
    constructFourMomenta(tauVector, bJetVector, METVector, output);
    calculateTopMass(output);
    calculateHiggsMass(output);
    if (output.bPassedEvent) {
      if (myInputDataType == eRECO) hHiggsMass_greater->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN) hHiggsMass_GEN_greater->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN_NeutrinosReplacedWithMET) hHiggsMass_GEN_NuToMET_greater->Fill(output.fHiggsMassSolution);
    }
    // Selection method: smaller
    output.fNeutrinoPzSolutionSmaller = selectNeutrinoPzSolution(tauVector, bJetVector, output, eSmaller);
    constructFourMomenta(tauVector, bJetVector, METVector, output);
    calculateTopMass(output);
    calculateHiggsMass(output);
    if (output.bPassedEvent) {
      if (myInputDataType == eRECO) hHiggsMass_smaller->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN) hHiggsMass_GEN_smaller->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN_NeutrinosReplacedWithMET) hHiggsMass_GEN_NuToMET_smaller->Fill(output.fHiggsMassSolution);
    }
    // Selection method: tauNuAngleMin
    output.fNeutrinoPzSolutionTauNuAngleMin = selectNeutrinoPzSolution(tauVector, bJetVector, output, eTauNuAngleMin);
    constructFourMomenta(tauVector, bJetVector, METVector, output);
    calculateTopMass(output);
    calculateHiggsMass(output);
    if (output.bPassedEvent) {
      if (myInputDataType == eRECO) hHiggsMass_tauNuAngleMin->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN) hHiggsMass_GEN_tauNuAngleMin->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN_NeutrinosReplacedWithMET) hHiggsMass_GEN_NuToMET_tauNuAngleMin->Fill(output.fHiggsMassSolution);
    }
    // Selection method: TauNuDeltaEtaMax
    output.fNeutrinoPzSolutionTauNuDeltaEtaMax = selectNeutrinoPzSolution(tauVector, bJetVector, output, eTauNuDeltaEtaMax);
    constructFourMomenta(tauVector, bJetVector, METVector, output);
    calculateTopMass(output);
    calculateHiggsMass(output);
    if (output.bPassedEvent) {
      if (myInputDataType == eRECO) hHiggsMass_tauNuDeltaEtaMax->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN) hHiggsMass_GEN_tauNuDeltaEtaMax->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN_NeutrinosReplacedWithMET) 
	hHiggsMass_GEN_NuToMET_tauNuDeltaEtaMax->Fill(output.fHiggsMassSolution);
    }
    // Selection method: TauNuDeltaEtaMin
    output.fNeutrinoPzSolutionTauNuDeltaEtaMin = selectNeutrinoPzSolution(tauVector, bJetVector, output, eTauNuDeltaEtaMin);
    constructFourMomenta(tauVector, bJetVector, METVector, output);
    calculateTopMass(output);
    calculateHiggsMass(output);
    if (output.bPassedEvent) {
      if (myInputDataType == eRECO) hHiggsMass_tauNuDeltaEtaMin->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN) hHiggsMass_GEN_tauNuDeltaEtaMin->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN_NeutrinosReplacedWithMET) 
	hHiggsMass_GEN_NuToMET_tauNuDeltaEtaMin->Fill(output.fHiggsMassSolution);
    }
    // NOTE: THE LAST CALCULATION DETERMINES WHICH SELECTION METHOD IS USED FOR THE MAIN OUTPUT:
    // Selection method: tauNuAngleMax
    output.fNeutrinoPzSolutionTauNuAngleMax = selectNeutrinoPzSolution(tauVector, bJetVector, output, eTauNuAngleMax);
    constructFourMomenta(tauVector, bJetVector, METVector, output);
    calculateTopMass(output);
    calculateHiggsMass(output);
    if (output.bPassedEvent) {
      if (myInputDataType == eRECO) hHiggsMass_tauNuAngleMax->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN) hHiggsMass_GEN_tauNuAngleMax->Fill(output.fHiggsMassSolution);
      if (myInputDataType == eGEN_NeutrinosReplacedWithMET) hHiggsMass_GEN_NuToMET_tauNuAngleMax->Fill(output.fHiggsMassSolution);
    }

    doCountingAndHistogramming(iEvent, output, myInputDataType);
  }

  void FullHiggsMassCalculator::calculateNeutrinoPz(TVector3& pB, TVector3& pTau, TVector3& MET, 
						    FullHiggsMassCalculator::Data& output) {
    output.bNegativeDiscriminantRecovered = false; // THIS IS IMPORTANT!
    increment(fAllSolutionsCutSubCount);
    // Get the on-shell particle masses
    const double mTop = c_fPhysicalTopMass;
    const double mTau = c_fPhysicalTauMass;
    const double mB   = c_fPhysicalBeautyMass;
    if (bPrintDebugOutput) std::cout << "Top, tau, and beauty mass: " << mTop << ", " << mTau << ", " << mB << std::endl;
    // Calculate quantities appearing in the calculation
    double bEnergy = TMath::Sqrt(mB * mB + pB.Mag2());
    double visibleTauEnergy = TMath::Sqrt(mTau * mTau + pTau.Mag2());
    double deltaSquaredMasses = mTop * mTop - mB * mB - mTau * mTau;
    double A = (deltaSquaredMasses / 2.0 - bEnergy * visibleTauEnergy + pB.Dot(pTau) +
		pB.XYvector() * MET.XYvector() + pTau.XYvector() * MET.XYvector()) / (bEnergy + visibleTauEnergy);
    double B = (pB.Pz() + pTau.Pz()) / (bEnergy + visibleTauEnergy);
    double discriminant = A*A - MET.Perp2() * (1 - B*B);
    // Initialize solutions
    double neutrinoPzSolution1 = -999999.0;
    double neutrinoPzSolution2 = -999999.0;
    // Calculate the solutions...
    // If the discriminant is positive, there are two real solutions
    if (discriminant >= 0.0) {
      increment(fPositiveDiscriminantCutSubCount);
      neutrinoPzSolution1 = (A*B + TMath::Sqrt(discriminant))/(1 - B*B);
      neutrinoPzSolution2 = (A*B - TMath::Sqrt(discriminant))/(1 - B*B);
    }
    // If the discriminant is negative, there are two complex (and hence unphysical) solutions. We try to remedy this as follows.
    // Negative discriminant recovery strategy:
    //  * Set discriminant to zero and calculate (unambiguous) neutrino p_z
    //  * Solve MET value from requirement "discriminant = 0". (Which is a quadratic equation with two real solutions for MET)
    //  * Select the value that is closer to the original value (minimal modification principle)
    // [* Could be implemented later: if the new MET differs from the original MET by more than some cut value, reject event]
    else {
      increment(fNegativeDiscriminantCutSubCount);
      if (bPrintDebugOutput) std::cout << "DISCRIMINANT < 0!!!" << std::endl;
      // Set discriminant to zero and calculate neutrino p_z (the two solutions are equal)
      neutrinoPzSolution1 = A*B / (1 - B*B);
      neutrinoPzSolution2 = A*B / (1 - B*B);
      if (bTryRecoveringNegativeDiscriminants) {
	output.bNegativeDiscriminantRecovered = true;
	// Calculate solutions for the modified MET value.
	double modifiedMETSolution1 = (deltaSquaredMasses / 2.0 - bEnergy * visibleTauEnergy + pB.Dot(pTau)) / 
	  (- pB.Pt() * TMath::Cos(pB.DeltaPhi(MET)) - pTau.Pt() * TMath::Cos(pTau.DeltaPhi(MET))
	   + TMath::Sqrt((bEnergy + visibleTauEnergy)*(bEnergy + visibleTauEnergy) - (pB.Pz() + pTau.Pz())*(pB.Pz() + pTau.Pz())));
	double modifiedMETSolution2 = (deltaSquaredMasses / 2.0 - bEnergy * visibleTauEnergy + pB.Dot(pTau)) / 
	  (- pB.Pt() * TMath::Cos(pB.DeltaPhi(MET)) - pTau.Pt() * TMath::Cos(pTau.DeltaPhi(MET))
	   - TMath::Sqrt((bEnergy + visibleTauEnergy)*(bEnergy + visibleTauEnergy) - (pB.Pz() + pTau.Pz())*(pB.Pz() + pTau.Pz())));
	// Select the MET solution that is closer to the original value
	if (TMath::Abs(modifiedMETSolution1 - MET.Perp()) < TMath::Abs(modifiedMETSolution2 - MET.Perp()))
	  output.fModifiedMET = modifiedMETSolution1;
	else 
	  output.fModifiedMET = modifiedMETSolution2;
	// // VALIDATION:
// 	TVector3 modifiedMETVector1;
// 	modifiedMETVector1.SetPtEtaPhi(modifiedMETSolution1, MET.Eta(), MET.Phi());
// 	TVector3 modifiedMETVector2 = MET;
// 	//modifiedMETVector1.SetPerp(modifiedMETSolution1);
// 	modifiedMETVector2.SetPerp(modifiedMETSolution2);
// 	double modifiedA1 = (deltaSquaredMasses / 2.0 - bEnergy * visibleTauEnergy + pB.Dot(pTau) +
// 			     pB.XYvector() * modifiedMETVector1.XYvector() + pTau.XYvector() * modifiedMETVector1.XYvector()) 
// 	  / (bEnergy + visibleTauEnergy);
// 	std::cout << "A = " << A << std::endl;
// 	std::cout << "modifiedA1 = " << modifiedA1 << std::endl;
// 	std::cout << modifiedMETSolution1*modifiedMETSolution1 << " = " << modifiedMETVector1.Perp2() << std::endl;
// 	double modifiedA2 = (deltaSquaredMasses / 2.0 - bEnergy * visibleTauEnergy + pB.Dot(pTau) +
// 			     pB.XYvector() * modifiedMETVector2.XYvector() + pTau.XYvector() * modifiedMETVector2.XYvector()) 
// 	  / (bEnergy + visibleTauEnergy);
// 	double modifiedDiscriminant1 = modifiedA1*modifiedA1 - modifiedMETVector1.Perp2() * (1 - B*B);
// 	double modifiedDiscriminant2 = modifiedA2*modifiedA2 - modifiedMETVector2.Perp2() * (1 - B*B);
// 	bool bPrintDebugOutput_recovery = true; // DELETE LATER
// 	if (bPrintDebugOutput_recovery) {
// 	  std::cout << "_______________________ original MET: " << MET.Perp() << std::endl;
// 	  std::cout << "_______________________ modifiedMETSolution1 = " << modifiedMETSolution1 << std::endl;
// 	  std::cout << "_______________________ modifiedMETSolutionA = " << modifiedMETSolutionA << std::endl;
// 	  std::cout << "_______________________ modifiedMETSolution2 = " << modifiedMETSolution2 << std::endl;
// 	  std::cout << "_______________________ modifiedMETSolutionB = " << modifiedMETSolutionB << std::endl;
// 	  std::cout << "_______________________ discriminant for modifiedMETSolution1: " << modifiedDiscriminant1 << std::endl;
// 	  std::cout << "_______________________ discriminant for modifiedMETSolution2: " << modifiedDiscriminant2 << std::endl;
// 	  std::cout << "(checking phi before and after calculation) " <<  MET.Phi() << " = " 
// 		    << modifiedMETVector1.Phi() << std::endl;
// 	}
// 	// DELETE --->
// 	modifiedMETSolution1 = MET.Perp();
// 	modifiedMETVector1.SetPtEtaPhi(modifiedMETSolution1, MET.Eta(), MET.Phi());
//       modifiedA1 = (deltaSquaredMasses / 2.0 - bEnergy * visibleTauEnergy + pB.Dot(pTau) +
// 		    pB.XYvector() * modifiedMETVector1.XYvector() + pTau.XYvector() * modifiedMETVector1.XYvector())
// 	/ (bEnergy + visibleTauEnergy);
//       modifiedDiscriminant1 = modifiedA1*modifiedA1 - modifiedMETVector1.Perp2() * (1 - B*B);
//       std::cout << discriminant << " = " << modifiedDiscriminant1 << std::endl;
//       // <--- /DELETE
//       // output.fSelectedModifiedMETValue = ...
//       // ---> in constructFourMomenta: (met).SetPerp(output.fSelectedModifiedMETValue);
      }
    }
    // Set output
    output.fDiscriminant = discriminant;
    output.fNeutrinoPzSolution1 = neutrinoPzSolution1;
    output.fNeutrinoPzSolution2 = neutrinoPzSolution2;
    if (output.fDiscriminant >= 0 || output.bNegativeDiscriminantRecovered)
      output.bPassedEvent = true;
    else 
      output.bPassedEvent = false;
    // Print information about the calculation steps
    if (bPrintDebugOutput) {
      std::cout << "FullHiggsMassCalculator: Reconstructing the neutrino p_z..." << std::endl;
      std::cout << "--- Tau momentum               = (" << pTau.Px() << ", " << pTau.Py() << ", " << pTau.Pz() << ")" << std::endl;
      std::cout << "--- B-jet momentum             = (" << pB.Px() << ", " << pB.Py() << ", " << pB.Pz() << ")" << std::endl;
      std::cout << "--- Combined neutrino momentum = (" << MET.Px() << ", " << MET.Py() << ", "<< MET.Pz() << ")"<< std::endl;
      std::cout << "--- B-jet energy = " << bEnergy << std::endl;
      std::cout << "--- Tau energy   = " << visibleTauEnergy << std::endl;
      std::cout << "--- deltaSquaredMasses = " << deltaSquaredMasses << std::endl;    
      std::cout << "--- A = " << A << std::endl;
      std::cout << "--- B = " << B << std::endl;
      std::cout << "--- Discriminant = " << discriminant << std::endl;
      std::cout << "--- Y/X = " << A*B / (1 - B*B) << std::endl;
      std::cout << "--- Z/X = " << TMath::Sqrt(A*A - MET.Perp2() * (1 - B*B)) / (1 - B*B) << std::endl;
      std::cout << "--- neutrinoPzSolution1 = " << neutrinoPzSolution1 << std::endl;
      std::cout << "--- neutrinoPzSolution2 = " << neutrinoPzSolution2 << std::endl;
    }
  }

  double FullHiggsMassCalculator::selectNeutrinoPzSolution(TVector3& pTau, TVector3& MET, FullHiggsMassCalculator::Data& output, 
							 PzSelectionMethod selectionMethod) {
    // The following two variables (solution1, solution2) are only introduced to improve code readability!
    double solution1 = output.fNeutrinoPzSolution1;
    double solution2 = output.fNeutrinoPzSolution2;

    // Calculate some auxiliary quantities that may or may not be used for selecting a solution
    double angle1 = getAngleBetweenNeutrinosAndTau(pTau, MET, solution1);
    double angle2 = getAngleBetweenNeutrinosAndTau(pTau, MET, solution2);
    double deltaEta1 = getDeltaEtaBetweenNeutrinosAndTau(pTau, MET, solution1);
    double deltaEta2 = getDeltaEtaBetweenNeutrinosAndTau(pTau, MET, solution2);
    if (bPrintDebugOutput) {
      std::cout << "--- angle1 = " << angle1 * TMath::RadToDeg() << " degrees" << std::endl;
      std::cout << "--- angle2 = " << angle2 * TMath::RadToDeg() << " degrees" << std::endl;
      std::cout << "--- deltaEta1 = " << deltaEta1 << std::endl;
      std::cout << "--- deltaEta2 = " << deltaEta2 << std::endl;
    }
    if (deltaEta1 > deltaEta2 && angle1 > angle2)
      std::cout << "1" << std::endl;
    else if (deltaEta1 < deltaEta2 && angle1 < angle2)
      std::cout << "1" << std::endl;
    else
      std::cout << "0" << std::endl;

    // Select a solution using the desired method
    // Initialize...
    bool selectSolution1 = false;
    // Go!
    if (bPrintDebugOutput) std::cout << "Neutrino p_z solution selection: ";
    switch (selectionMethod) {
    case eGreater:
      if (solution1 > solution2) selectSolution1 = true;
      if (bPrintDebugOutput) std::cout << "select the greater solution" << std::endl;
      break;
    case eSmaller:
      if (solution1 < solution2) selectSolution1 = true;
      if (bPrintDebugOutput) std::cout << "select the smaller solution" << std::endl;
      break;
    case eTauNuAngleMax:
      if (angle1 > angle2) selectSolution1 = true;
      if (bPrintDebugOutput) std::cout << "select the solution which maximizes the angle between the tau and the neutrinos"
				       << std::endl;
      break;
    case eTauNuAngleMin:
      if (angle1 < angle2) selectSolution1 = true;
      if (bPrintDebugOutput) std::cout << "select the solution which minimizes the angle between the tau and the neutrinos"
				       << std::endl;
      break;
    case eTauNuDeltaEtaMax:
      if (deltaEta1 > deltaEta2) selectSolution1 = true;
      if (bPrintDebugOutput) std::cout << "select the solution which maximizes the eta difference between the tau and the neutrinos"
				       << std::endl;
      break;
    case eTauNuDeltaEtaMin:
      if (deltaEta1 < deltaEta2) selectSolution1 = true;
      if (bPrintDebugOutput) std::cout << "select the solution which minimizes the eta difference between the tau and the neutrinos"
				       << std::endl;
      break;
    default:
      // Throw exception!
      throw cms::Exception("LogicError")
	<< "No implementation for the given neutrino p_z selection method found! Please check FullHiggsMassCalculator.cc and .h";
    }
    // Set the output according to what the selection outcome was
    if (selectSolution1) {
      output.fSelectedNeutrinoPzSolution = solution1;
      if (bPrintDebugOutput) std::cout << "Selected neutrino p_z solution 1" << std::endl;
    } else {
      output.fSelectedNeutrinoPzSolution = solution2;
      if (bPrintDebugOutput) std::cout << "Selected neutrino p_z solution 2" << std::endl;
    }
    return output.fSelectedNeutrinoPzSolution;
  }

  double FullHiggsMassCalculator::getAngleBetweenNeutrinosAndTau(TVector3& pTau, TVector3& MET, double neutrinoPzSolution) {
    TVector3 neutrinoVector(MET.Px(), MET.Py(), neutrinoPzSolution);
    return neutrinoVector.Angle(pTau);
  }

  double FullHiggsMassCalculator::getDeltaEtaBetweenNeutrinosAndTau(TVector3& pTau, TVector3& MET, double neutrinoPzSolution) {
    TVector3 neutrinoVector(MET.Px(), MET.Py(), neutrinoPzSolution);
    //return TMath::Abs(neutrinoVector.Eta() - pTau.Eta());

    // TODO, IMPORTANT!!!! REMOVE THIS AND UNCOMMENT THE LINE ABOVE. THIS IS ONLY FOR TESTING!
    return neutrinoVector.DeltaR(pTau);
  }

  bool FullHiggsMassCalculator::selectedSolutionIsClosestToTrueValue(double selectedSolution, 
								     FullHiggsMassCalculator::Data& output) {
    if (!output.bPassedEvent) return false;
    if (selectedSolution > 999999.0) return false; // Always return false if the solution was not calculated
    // Note: this method will also return true if the two solutions were equal
    // Otherwise, find out which solution (1 or 2) was selected:
    if (TMath::Abs(selectedSolution - output.fNeutrinoPzSolution1) <= TMath::Abs(selectedSolution - output.fNeutrinoPzSolution2)) {
      // ...solution 1 was selected. Return false if it wasn't the closer one:
      if (TMath::Abs(output.fNeutrinoPzSolution1 - output.fTrueNeutrinoPz) >
	  TMath::Abs(output.fNeutrinoPzSolution2 - output.fTrueNeutrinoPz)) return false;
    } else {
      // ...solution 2 was selected. Return false if it wasn't the closer one:
      if (TMath::Abs(output.fNeutrinoPzSolution2 - output.fTrueNeutrinoPz) >
	  TMath::Abs(output.fNeutrinoPzSolution1 - output.fTrueNeutrinoPz)) return false;
    }
    return true;
  }

//   bool FullHiggsMassCalculator::selectedSolutionGivesVectorClosestToTrue(double selectedSolution,
// 									 FullHiggsMassCalculator::Data& output) {
//     return true;
//   }

  void FullHiggsMassCalculator::constructFourMomenta(TVector3& pB, TVector3& pTau, TVector3& MET, 
						     FullHiggsMassCalculator::Data& output) {
    if (output.bNegativeDiscriminantRecovered) MET.SetPerp(output.fModifiedMET);
    TLorentzVector visibleTauMomentum;
    TLorentzVector bJetMomentum;
    TLorentzVector neutrinosMomentum;
    double visibleTauEnergy = TMath::Sqrt(TMath::Power(c_fPhysicalTauMass,2) + TMath::Power(pTau.Px(),2) +
					  TMath::Power(pTau.Py(),2) + TMath::Power(pTau.Pz(),2));
    double bJetEnergy = TMath::Sqrt(TMath::Power(c_fPhysicalBeautyMass,2) + TMath::Power(pB.Px(),2) +
				    TMath::Power(pB.Py(),2) + TMath::Power(pB.Pz(),2));
    double neutrinosEnergy = TMath::Sqrt(TMath::Power(MET.Px(),2) + TMath::Power(MET.Py(),2) +
					 TMath::Power(output.fSelectedNeutrinoPzSolution,2));
    visibleTauMomentum.SetPxPyPzE(pTau.Px(), pTau.Py(), pTau.Pz(), visibleTauEnergy);
    bJetMomentum.SetPxPyPzE(pB.Px(), pB.Py(), pB.Pz(), bJetEnergy);
    neutrinosMomentum.SetPxPyPzE(MET.Px(), MET.Py(), output.fSelectedNeutrinoPzSolution, neutrinosEnergy);
    output.LorentzVector_visibleTauFourMomentum = visibleTauMomentum;
    output.LorentzVector_bJetFourMomentum = bJetMomentum;
    output.LorentzVector_neutrinosFourMomentum = neutrinosMomentum;
  }

  void FullHiggsMassCalculator::calculateTopMass(FullHiggsMassCalculator::Data& output) {
    TLorentzVector topMomentumSolution = output.LorentzVector_visibleTauFourMomentum + output.LorentzVector_bJetFourMomentum +
      output.LorentzVector_neutrinosFourMomentum;
    output.fTopMassSolution = topMomentumSolution.M();
    if (bPrintDebugOutput) std::cout << "output.fTopMassSolution: " << output.fTopMassSolution << std::endl;
  }
  
  void FullHiggsMassCalculator::calculateHiggsMass(FullHiggsMassCalculator::Data& output) {
    TLorentzVector higgsMomentumSolution = output.LorentzVector_visibleTauFourMomentum + output.LorentzVector_neutrinosFourMomentum;
    output.fHiggsMassSolution = higgsMomentumSolution.M();
    if (bPrintDebugOutput) std::cout << "output.fHiggsMassSolution: " << output.fHiggsMassSolution << std::endl;
  }
  
  void FullHiggsMassCalculator::applyCuts(FullHiggsMassCalculator::Data& output) {
    if (140.0 < output.fTopMassSolution < 200.0) output.bPassedEvent = false;
    //TMath::Output(output.fModifiedMET - <original MET>)
  }
  
  void FullHiggsMassCalculator::doCountingAndHistogramming(const edm::Event& iEvent, FullHiggsMassCalculator::Data& output, 
							   InputDataType myInputDataType) {
    // Apply cuts:
    applyCuts(output);

    switch (myInputDataType) {
    case eRECO:
      hDiscriminant->Fill(output.fDiscriminant);
      if (!output.bPassedEvent) break;
      hHiggsMass->Fill(output.fHiggsMassSolution);
      hTopMassSolution->Fill(output.fTopMassSolution);
      hSelectedNeutrinoPzSolution->Fill(output.fSelectedNeutrinoPzSolution);
      // Counters (note: only incremented if the event has passed)
      increment(fAllSelections_SubCount);
      if (iEvent.isRealData()) break; // The true solution is not known for real data.
      if (selectedSolutionIsClosestToTrueValue(output.fNeutrinoPzSolutionGreater, output))
	increment(fSelectionGreaterCorrect_SubCount);
      if (selectedSolutionIsClosestToTrueValue(output.fNeutrinoPzSolutionSmaller, output))
	increment(fSelectionSmallerCorrect_SubCount);
      if (selectedSolutionIsClosestToTrueValue(output.fNeutrinoPzSolutionTauNuAngleMax, output))
	increment(fSelectionTauNuAngleMaxCorrect_SubCount);
      if (selectedSolutionIsClosestToTrueValue(output.fNeutrinoPzSolutionTauNuAngleMin, output))
	increment(fSelectionTauNuAngleMinCorrect_SubCount);
      if (selectedSolutionIsClosestToTrueValue(output.fNeutrinoPzSolutionTauNuDeltaEtaMax, output))
	increment(fSelectionTauNuDeltaEtaMaxCorrect_SubCount);
      if (selectedSolutionIsClosestToTrueValue(output.fNeutrinoPzSolutionTauNuDeltaEtaMin, output))
	increment(fSelectionTauNuDeltaEtaMinCorrect_SubCount);
      break;
    case eGEN:
      hDiscriminant_GEN->Fill(output.fDiscriminant);
      if (!output.bPassedEvent) break;
      hHiggsMass_GEN->Fill(output.fHiggsMassSolution);
      //hTopMassSolution_GEN->Fill(output.fTopMassSolution);
      break;
    case eGEN_NeutrinosReplacedWithMET:
      hDiscriminant_GEN_NeutrinosReplacedWithMET->Fill(output.fDiscriminant);
      if (!output.bPassedEvent) break;
      hHiggsMass_GEN_NeutrinosReplacedWithMET->Fill(output.fHiggsMassSolution);
      //hTopMassSolution_GEN_NeutrinosReplacedWithMET->Fill(output.fTopMassSolution);
      break;
    default:
      //Throw exception!
      throw cms::Exception("LogicError") << "The given InputDataType is invalid. Please check FullHiggsMassCalculator.cc and .h";
    }
  }

  void FullHiggsMassCalculator::doEventClassification(const edm::Event& iEvent, TVector3& bJetVector, TVector3& tauVector,
						      TVector3& METVector, FullHiggsMassCalculator::Data& output,
						      const GenParticleAnalysis::Data* genDataPtr) {
    // Declare variables used to classify events
    double bDeltaR     = 9999;
    double tauDeltaR   = 9999;
    double metDeltaPt  = 9999;
    double metDeltaPhi = 9999;
    // Specify the cuts used to classify events
    double bDeltaRCut       =   0.6;
    double tauDeltaRCut     =   0.1;
    double metDeltaPtLoCut  = -20.0; // GeV
    double metDeltaPtHiCut  =  40.0; // GeV
    double metDeltaPhiCut   =  15.0 * TMath::DegToRad(); // The first number is the cut angle in deg, which is then converted to rad

    // B-jet: compare RECO and GEN information
    bDeltaR = getClosestGenBQuarkDeltaR(iEvent, bJetVector);
    if (bPrintDebugOutput) std::cout << "****** bDeltaR: " << bDeltaR << std::endl;
    // Tau: compare RECO and GEN information
    tauDeltaR = getClosestGenVisibleTauDeltaR(iEvent, tauVector);
    if (bPrintDebugOutput) std::cout << "****** tauDeltaR: " << tauDeltaR << std::endl;
  
    // MET: compare RECO and GEN information
    TVector3 genMETVector;
    if (genDataPtr != NULL) {
      // This is the entirely correct way, will work if GenParticleAnalysis::Data is available
      edm::Ptr<reco::GenMET> myGenMET = genDataPtr->getGenMET();
      genMETVector.SetXYZ(myGenMET->px(), myGenMET->py(), myGenMET->pz());
    } else {
      // This way is approximate, but will work even if GenParticleAnalysis::Data is unavailable
      genMETVector = calculateGenMETVectorFromNeutrinos(iEvent);
    }
    metDeltaPt = METVector.Pt() - genMETVector.Pt();
    metDeltaPhi = METVector.DeltaPhi(genMETVector);
    if (bPrintDebugOutput) std::cout << "****** metDeltaPt = " << metDeltaPt << std::endl;
    if (bPrintDebugOutput) std::cout << "****** metDeltaPhi (in degrees) = " << metDeltaPhi * 180.0 / TMath::Pi() << std::endl;
    // Put the comparison values in histograms
    hBDeltaR->Fill(bDeltaR);
    hTauDeltaR->Fill(tauDeltaR);
    hMETDeltaPt->Fill(metDeltaPt);
    hMETDeltaPhi->Fill(metDeltaPhi * 180.0 / TMath::Pi());

    int eventClassCode = 0;
    TString eventClassName; // This is only to be used for print statements
    // NOTE: the if-statements below check if something does NOT pass the cuts!
    if (bDeltaR >= bDeltaRCut) {
      eventClassCode += eOnlyBadBjet;
      increment(eventClass_AllBadBjet_SubCount);
    }
    if (metDeltaPt <= metDeltaPtLoCut || metDeltaPt >= metDeltaPtHiCut || TMath::Abs(metDeltaPhi) >= metDeltaPhiCut) {
      eventClassCode += eOnlyBadMET;
      increment(eventClass_AllBadMET_SubCount);
    }
    if (tauDeltaR >= tauDeltaRCut) {
      eventClassCode += eOnlyBadTau;
      increment(eventClass_AllBadTau_SubCount);
    }
    if (bPrintDebugOutput) std::cout << "FullHiggsMassCalculator:   eventClassCode = " << eventClassCode << std::endl;
    // Define and set the event classes. Informative histograms are filled and counters incremented for each class
    switch (eventClassCode) {
    case ePure:
      output.eEventClassCode = ePure;
      eventClassName = "Pure";
      increment(eventClass_Pure_SubCount);
      if (output.bPassedEvent) hHiggsMassPure->Fill(output.fHiggsMassSolution);
      hDiscriminantPure->Fill(output.fDiscriminant);
      break;
    case eOnlyBadTau:
      output.eEventClassCode = eOnlyBadTau;
      eventClassName = "OnlyBadTau";
      increment(eventClass_OnlyBadTau_SubCount);
      if (output.bPassedEvent) hHiggsMassBadTau->Fill(output.fHiggsMassSolution);
      break;
    case eOnlyBadMET:
      output.eEventClassCode = eOnlyBadMET;
      eventClassName = "OnlyBadMET";
      increment(eventClass_OnlyBadMET_SubCount);
      if (output.bPassedEvent) hHiggsMassBadMET->Fill(output.fHiggsMassSolution);
      break;
    case eOnlyBadTauAndMET:
      output.eEventClassCode = eOnlyBadTauAndMET;
      eventClassName = "OnlyBadTauAndMET";
      increment(eventClass_OnlyBadTauAndMET_SubCount);
      if (output.bPassedEvent) hHiggsMassBadTauAndMET->Fill(output.fHiggsMassSolution);
      break;
    case eOnlyBadBjet:
      output.eEventClassCode = eOnlyBadBjet;
      eventClassName = "OnlyBadBjet";
      increment(eventClass_OnlyBadBjet_SubCount);
      if (output.bPassedEvent) hHiggsMassBadBjet->Fill(output.fHiggsMassSolution);
      break;
    case eOnlyBadBjetAndTau:
      output.eEventClassCode = eOnlyBadBjetAndTau;
      eventClassName = "OnlyBadBjetAndTau";
      increment(eventClass_OnlyBadBjetAndTau_SubCount);
      if (output.bPassedEvent) hHiggsMassBadBjetAndTau->Fill(output.fHiggsMassSolution);
      break;
    case eOnlyBadBjetAndMET:
      output.eEventClassCode = eOnlyBadBjetAndMET;
      eventClassName = "OnlyBadBjetAndMET";
      increment(eventClass_OnlyBadBjetAndMET_SubCount);
      if (output.bPassedEvent) hHiggsMassBadBjetAndMET->Fill(output.fHiggsMassSolution);
      break;
    case eOnlyBadBjetAndMETAndTau:
      output.eEventClassCode = eOnlyBadBjetAndMETAndTau;
      eventClassName = "OnlyBadBjetAndMETAndTau";
      increment(eventClass_OnlyBadBjetAndMETAndTau_SubCount);
      if (output.bPassedEvent) hHiggsMassBadBjetAndMETAndTau->Fill(output.fHiggsMassSolution);
      break;
    default:
      // Throw exception!
      eventClassName = "######";
      if (bPrintDebugOutput) std::cout << "EVENT CLASSIFICATON FAILED!" << std::endl;
      throw cms::Exception("LogicError")
	<< "The event classification code received an invalid value. Please check FullHiggsMassCalculator.cc and .h";
    }
    if (bPrintDebugOutput) std::cout << "eventClassName = " << eventClassName << std::endl;
    // Also do histogramming and counting for the set of events, in which ANYTHING was misidentified ("impure events")
    if (eventClassCode > 0) {
      increment(eventClass_Impure_SubCount);
      if (output.bPassedEvent) hHiggsMassImpure->Fill(output.fHiggsMassSolution);
      hDiscriminantImpure->Fill(output.fDiscriminant);
    }
  }

  void FullHiggsMassCalculator::analyzeMETComposition(TVector3& recoMETVector, TVector3& genBothNeutrinosVector, 
						      TVector3& genMETVector) {
    // "Primary" MET contributions:
    double recoMET = recoMETVector.Pt();
    double genMET = genMETVector.Pt();
    double tauNeutrinosMET = genBothNeutrinosVector.Pt();
    // "Derived" contributions:
    double otherNeutrinosMET = genMET - tauNeutrinosMET;
    double mismeasurementMET = recoMET - genMET;
    if (bPrintDebugOutput) {
      std::cout << "MET FRACTIONS: RECOMET = " << 1.0 << ", GENMET = " << genMET/recoMET << std::endl;
      std::cout << "                   due to tau neutrinos   = " << tauNeutrinosMET/recoMET << std::endl;
      std::cout << "                   due to other neutrinos = " << otherNeutrinosMET/recoMET << std::endl;
      std::cout << "                   due to mismeasurement  = " << mismeasurementMET/recoMET << std::endl;
    }
    
    bool bPrintMachineReadableOutput = false;
    if (!bPrintDebugOutput && bPrintMachineReadableOutput) {
      std::cout << recoMET << " " << tauNeutrinosMET/recoMET << " " << otherNeutrinosMET/recoMET << " " 
		<< mismeasurementMET/recoMET << std::endl;
    }
  }
}
