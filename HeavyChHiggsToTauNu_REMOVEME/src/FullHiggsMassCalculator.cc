#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventClassification.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/genParticleMotherTools.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
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
#include "TLorentzVector.h"
#include "TVector3.h"
#include "TMath.h"
#include "TString.h"

namespace {
  // (Containing these variables in an anonymous namespace prevents them from being accessed from code in another file)
  // FLAGS:
  // Set this variable to true if you want debug print statements to be activated
  const bool bPrintDebugOutput = false;
  // Set this variable to true if you want to recover events with a negative discriminant using a special algorithm instead of
  // discarding them
  const bool bTryRecoveringNegativeDiscriminants = true; // Do not set this to false unless you are sure that's what you want.
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
    bNegativeDiscriminantRecovered(false),
    fDiscriminant(0),
    fTopMassSolutionSelected(0),
    fTopMassSolution1(0),
    fTopMassSolution2(0),
    fNeutrinoPzSolution1(0),
    fNeutrinoPzSolution2(0),
    fNeutrinoPzSolutionSelected(0),
    fModifiedMETSolution1(0),
    fModifiedMETSolution2(0),
    fModifiedMETSolutionSelected(0),
    fHiggsMassSolution1(0),
    fHiggsMassSolution2(0),
    fHiggsMassSolutionSelected(0),
    fNeutrinoPtSolution(0),
    fTrueNeutrinoPz(0),
    bJetFourMomentum(),
    visibleTauFourMomentum(),
    neutrinosFourMomentum1(),
    neutrinosFourMomentum2(),
    fNeutrinoPzSolutionGreater(999999999.9),
    fNeutrinoPzSolutionSmaller(999999999.9),
    fNeutrinoPzSolutionTauNuAngleMax(999999999.9),
    fNeutrinoPzSolutionTauNuAngleMin(999999999.9),
    eEventClassCode()
  { }

  FullHiggsMassCalculator::Data::~Data() { }

  FullHiggsMassCalculator::FullHiggsMassCalculator(const edm::ParameterSet& iConfig, HPlus::EventCounter& eventCounter, 
						   HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    // Get the parameters from the configuration
    fTopInvMassLowerCut(iConfig.getUntrackedParameter<double>("topInvMassLowerCut")),
    fTopInvMassUpperCut(iConfig.getUntrackedParameter<double>("topInvMassUpperCut")),
    // Define counters to be incremented during this analysis
    allEvents_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "All events")),
    positiveDiscriminant_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator",
								"Positive discriminant")),
    negativeDiscriminant_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator",
								"Negative discriminant")),
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

    count_passedEvent(eventCounter.addSubCounter("FullMassEventClassification", "all passed events")),
    count_pure(eventCounter.addSubCounter("FullMassEventClassification", "pure")),
    count_tauGenuine(eventCounter.addSubCounter("FullMassEventClassification", "#tau genuine")),
    count_bGenuine(eventCounter.addSubCounter("FullMassEventClassification", "b genuine")),
    count_tauMeasurementGood(eventCounter.addSubCounter("FullMassEventClassification", "#tau measurement good")),
    count_bMeasurementGood(eventCounter.addSubCounter("FullMassEventClassification", "b measurement good")),
    count_tauAndBjetFromSameTopQuark(eventCounter.addSubCounter("FullMassEventClassification", "#tau and b from same top")),
    count_neutrinoMETCorrespondenceGood(eventCounter.addSubCounter("FullMassEventClassification", "MET #approx p_{#nu,T}")),

    passedEvents_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Passed events")),
    selectionGreaterCorrect_SubCount(eventCounter.addSubCounter("SolutionSelection", "Greater solution closest")),
    selectionSmallerCorrect_SubCount(eventCounter.addSubCounter("SolutionSelection", "Smaller solution closest")),
    selectionTauNuAngleMaxCorrect_SubCount(eventCounter.addSubCounter("SolutionSelection",
								      "TauNuAngleMax solution closest")),
    selectionTauNuAngleMinCorrect_SubCount(eventCounter.addSubCounter("SolutionSelection", 
								      "TauNuAngleMin solution closest")),
    selectionTauNuDeltaEtaMaxCorrect_SubCount(eventCounter.addSubCounter("SolutionSelection", 
									 "TauNuDeltaEtaMax solution closest")),
    selectionTauNuDeltaEtaMinCorrect_SubCount(eventCounter.addSubCounter("SolutionSelection", 
									 "TauNuDeltaEtaMin solution closest"))
  {
    std::string myMethod = iConfig.getUntrackedParameter<std::string>("pzSelectionMethod");
    if (myMethod == "DeltaEtaMax") fPzSelectionMethod = eTauNuDeltaEtaMax;
    else if (myMethod == "DeltaEtaMin") fPzSelectionMethod = eTauNuDeltaEtaMin;
    else if (myMethod == "AngleMax") fPzSelectionMethod = eTauNuAngleMax;
    else if (myMethod == "AngleMin") fPzSelectionMethod = eTauNuAngleMin;
    else if (myMethod == "Smaller") fPzSelectionMethod = eSmaller;
    else if (myMethod == "Greater") fPzSelectionMethod = eGreater;
    else {
      throw cms::Exception("LogicError") << "Error: Invariant mass config parameter pzSelectionMethod = '" << myMethod << "' is unknown!" << std::endl
        << "Options are 'DeltaEtaMax', 'DeltaEtaMin', 'AngleMax', 'AngleMin', 'Smaller', 'Greater'" << std::endl;
    }
    
    std::string myMetMethod = iConfig.getUntrackedParameter<std::string>("metSelectionMethod");
    if (myMetMethod == "SmallestMagnitude") fMetSelectionMethod = eSmallestMagnitude;
    else if (myMetMethod == "GreatestMagnitude") fMetSelectionMethod = eGreatestMagnitude;
    else if (myMetMethod == "ClosestToTopMass") fMetSelectionMethod = eClosestToTopMass;
    else {
      throw cms::Exception("LogicError") << "Error: Invariant mass config parameter metSelectionMethod = '" << myMetMethod << "' is unknown!" << std::endl
        << "Options are 'SmallestMagnitude', 'GreatestMagnitude', 'ClosestToTopMass'" << std::endl;
    }
    
    fReApplyMetCut = iConfig.getUntrackedParameter<double>("reApplyMetCut");

    fReApplyMetCut = iConfig.getUntrackedParameter<double>("reApplyMetCut");

    // Add a new directory ("FullHiggsMass") for the histograms produced in this code to the output file
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("FullHiggsMass");
    // Book histograms to be filled by this code
    // Vital histograms
    hHiggsMass                = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass", 
							  "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassPositiveDiscriminant = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassPositiveDiscriminant", 
							       "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassNegativeDiscriminant = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassNegativeDiscriminant", 
							       "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN            = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_GEN", 
							  "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_GEN_NeutrinosReplacedWithMET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, 
									"HiggsMass_GEN_NeutrinosReplacedWithMET", 
									"Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hDiscriminant             = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Discriminant",
							  "Discriminant", 100, -50000, 50000);
    hDiscriminant_GEN         = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Discriminant_GEN",
							  "Discriminant", 100, -50000, 50000);
    hDiscriminant_GEN_NeutrinosReplacedWithMET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, 
									   "Discriminant_GEN_NeutrinosReplacedWithMET",
									   "Discriminant", 100, -50000, 50000);
    h2TransverseMassVsInvariantMass = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "TransMassVsInvMass", 
				      "TransMassVsInvMass;Transverse mass m_{T};Invariant mass m(#tau, #nu_{#tau});Events",
				      100, 0, 500, 100, 0, 500); // Do not put as kSystematics
    h2MetSignificanceVsBadMet = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "METSignificanceVsBadMet", 
				      "METSignificnce;E_{T}^{miss} Significance; bad E_{T}^{miss};Events",
				      100, 0, 500, 100, 0, 500);
    h2TransverseMassVsInvariantMassPositiveDiscriminant = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, 
										    "TransMassVsInvMassPositiveDiscriminant", 
				      "TransMassVsInvMass;Transverse mass m_{T};Invariant mass m(#tau, #nu_{#tau});Events",
				      100, 0, 500, 100, 0, 500);
    h2TransverseMassVsInvariantMassNegativeDiscriminant = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, 
										    "TransMassVsInvMassNegativeDiscriminant", 
				      "TransMassVsInvMass;Transverse mass m_{T};Invariant mass m(#tau, #nu_{#tau});Events",
				      100, 0, 500, 100, 0, 500);
    h2TopMassVsInvariantMass = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "TopMassVsInvMass", 
							 "TransMassVsInvMass;m_{top};Invariant mass m(#tau, #nu_{#tau});Events",
							 100, 0, 500, 100, 0, 500);
    h2TopMassVsNeutrinoNumber = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "TopMassVsNeutrinoNumber",
							  "TransMassVsNeutrinoNumber;m_{top};Number of neutrinos);Events",
							  100, 0, 500, 10, 0, 10);
    h2InvariantMassVsNeutrinoNumber = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "InvMassVsNeutrinoNumber",
						   "InvMassVsNeutrinoNumber;m(#tau,#nu_{#tau};Number of neutrinos);Events",
								100, 0, 500, 10, 0, 10);
    hHiggsMass_betterSolution = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_betterSolution", 
							    "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_worseSolution = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass_worseSolution", 
							       "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hTopInvariantMassInGenerator = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopInvariantMassInGenerator", "Top invariant mass;m_{t} (GeV)", 100, 0, 500);
    hMETSignificance = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "METSignificance",
							  "METSignificance", 100, 0, 500);
    hNeutrinoNumberInPassedEvents = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NeutrinoNumberInPassedEvents",
							      "NeutrinoNumberInPassedEvents", 10, 0, 10);
    hNeutrinoNumberInRejectedEvents = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NeutrinoNumberInRejectedEvents",
								"NeutrinoNumberInRejectedEvents", 10, 0, 10);

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
    hDeltaPhiTauAndMetForBadMet = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaPhiTauAndMetForBadMet",
                                                          "#Delta #phi tau-MET for bad MET;#Delta #phi (#tau , E_{T}^{miss}) (degrees)", 180, -180, 180);
    hDeltaPhiTauAndBjetForBadMet = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaPhiTauAndBjetForBadMet",
                                                          "#Delta #phi tau-bjet for bad MET;#Delta #phi (#tau , b-jet) (degrees)", 180, -180, 180);
    hDeltaRTauAndMetForBadMet = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaRTauAndMetForBadMet",
                                                          "#Delta R tau-MET for bad MET;#Delta R (#tau , E_{T}^{miss})", 100, 0, 10);
    hDeltaRTauAndBjetForBadMet = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaRTauAndBjetForBadMet",
                                                          "#Delta R tau-bjet for bad MET;#Delta R (#tau , b-jet)", 100, 0, 10);

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
    Data outputReco;

    if (bPrintDebugOutput) std::cout << "==================================================================" << std::endl;

    // CALCULATION USING RECONSTRUCTED MOMENTA
    // ---------------------------------------
    // Find the b-jet that is closest to the selected tau in (eta, phi) space this b-jet is assumed to come from the same 
    // side of the Feynman diagram as the selected tau.
    edm::Ptr<pat::Jet> selectedRecoBJet = FullHiggsMassCalculator::findHiggsSideBJet(bData, myTau);
    if (selectedRecoBJet.isNull()) {
      // ...the event does not contain a tagged b-jet, set a few values and return:
      if (bPrintDebugOutput) std::cout << "No reco Higgs side b-jet found!" << std::endl;
      outputReco.fHiggsMassSolutionSelected = -1;
      outputReco.bPassedEvent = false;
      return outputReco;
    }
    TVector3 recoBJetVector(selectedRecoBJet->px(), selectedRecoBJet->py(), selectedRecoBJet->pz());
    TVector3 recoTauVector(myTau->px(), myTau->py(), myTau->pz());
    // The MET is the same as in the rest of the analysis (as it should be), normally (as of March 2013) Type 1 PF corrected.    
    TVector3 recoMETVector(metData.getSelectedMET()->px(), metData.getSelectedMET()->py(), metData.getSelectedMET()->pz());
    if (bPrintDebugOutput) {
      std::cout << "                                  AT START" << std::endl;
      std::cout << "recoBJetVector: "<< recoBJetVector.Px() << ", "<< recoBJetVector.Py() << ", "<< recoBJetVector.Pz()<< std::endl;
      std::cout << "recoTauVector: " << recoTauVector.Px() << ", " << recoTauVector.Py() << ", " << recoTauVector.Pz() << std::endl;
      std::cout << "recoMETVector: " << recoMETVector.Px() << ", " << recoMETVector.Py() << ", " << recoMETVector.Pz() << std::endl;
    }
    doCalculations(iEvent, recoTauVector, recoBJetVector, recoMETVector, outputReco, eRECO);
    // Make a 2D histogram of the transverse mass and the invariant mass
    double transverseMass = TransverseMass::reconstruct(*myTau, *(metData.getSelectedMET()));
    if (outputReco.bPassedEvent) {
      h2TransverseMassVsInvariantMass->Fill(transverseMass, outputReco.fHiggsMassSolutionSelected);
      if (outputReco.fDiscriminant >= 0) 
	h2TransverseMassVsInvariantMassPositiveDiscriminant->Fill(transverseMass, outputReco.fHiggsMassSolutionSelected);
      else
	h2TransverseMassVsInvariantMassNegativeDiscriminant->Fill(transverseMass, outputReco.fHiggsMassSolutionSelected);
    }
    // Make a histogram of the MET significance variable (we may want to cut on it)
    if (outputReco.bPassedEvent) hMETSignificance->Fill(metData.getSelectedMET()->significance());
    // Classify MC events according to what was identified correctly and what was not
    if (!iEvent.isRealData())
      doEventClassification(iEvent, recoBJetVector, recoTauVector, recoMETVector, outputReco, metData, genDataPtr);

    // The rest of the analysis is only done for MC signal events with a light charged Higgs (at least for now)
    if (iEvent.isRealData() || !eventHasLightChargedHiggs(iEvent)) return outputReco;

    // CALCULATION USING TRUE MOMENTA FROM MC
    // --------------------------------------
    Data outputMC;
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
    outputMC.fTrueNeutrinoPz = genBothNeutrinosVector.Pz();
    doCalculations(iEvent, genVisibleTauVector, genBJetVector, genBothNeutrinosVector, outputMC, eGEN);
    // Histogram of top invariant mass in generator:
    if (eventHasTopQuark(iEvent)) hTopInvariantMassInGenerator->Fill(getTopQuarkInvariantMass(iEvent));

    // NOTE: doEventClassification should only be called once for each event. DO NOT uncomment this line without commenting above!
    // doEventClassification(iEvent, genBJetVector, genVisibleTauVector, genBothNeutrinosVector, outputMC, genDataPtr);


    // CALCULATION USING TRUE MOMENTA FROM MC FOR B-JET AND VISIBLE TAU, BUT GEN MET INSTEAD OF TAU NEUTRINO MOMENTA
    // -------------------------------------------------------------------------------------------------------------
    // B-jet and visible tau are as before.
    // If GenParticleAnalysis::Data* genData is available, the correct GenMET vector is retrieved from it.
    // If it is not available, an estimate for the GenMET is calculated by summing the momenta of all GEN neutrinos that were
    // not filtered from the event to save space.
    Data outputMCHybrid;
    TVector3 genMETVector(0.0, 0.0, 0.0);
    if (genDataPtr != NULL && genDataPtr->isValid()) {
      edm::Ptr<reco::GenMET> myGenMET = genDataPtr->getGenMET();
      genMETVector.SetXYZ(myGenMET->px(), myGenMET->py(), myGenMET->pz());
    } else {
      genMETVector = calculateGenMETVectorFromNeutrinos(iEvent);
    }
    doCalculations(iEvent, genVisibleTauVector, genBJetVector, genMETVector, outputMCHybrid, eGEN_NeutrinosReplacedWithMET);

    // Now we can also analyze the composition of the MET
    analyzeMETComposition(recoMETVector, genBothNeutrinosVector, genMETVector);
    
    return outputReco;
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
    // Common calculations (two neutrino momentum vectors are reconstructed, two top and Higgs masses are calculated)
    calculateNeutrinoPz(tauVector, bJetVector, METVector, output);
    constructFourMomenta(tauVector, bJetVector, METVector, output);
    calculateTopMasses(output);
    // selectModifiedMETSolution(output);
    selectModifiedMETSolution(output, fMetSelectionMethod);
    calculateHiggsMasses(output);

    // Now select which neutrino p_z solution (if there are two) and which Higgs mass solution (there are always two) to select
    if (output.fDiscriminant < 0) {
      // In this case, there is only one neutrino p_z solution, but two modified MET solutions. The better one has already been
      // selected above. Set the selected Higgs mass according to which it was.
      if (modifiedMETSolutionOneWasSelected(output))
	output.fHiggsMassSolutionSelected = output.fHiggsMassSolution1;
      else
	output.fHiggsMassSolutionSelected = output.fHiggsMassSolution2;
    } else {
      // The discriminant was positive, so there are two neutrino p_z solutions. One needs to be selected.
      // Selection method: greater
      selectNeutrinoPzAndHiggsMassSolution(output, eGreater);
      output.fNeutrinoPzSolutionGreater = output.fNeutrinoPzSolutionSelected;      
      if (output.bPassedEvent) {
	if (myInputDataType == eRECO) hHiggsMass_greater->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN) hHiggsMass_GEN_greater->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN_NeutrinosReplacedWithMET) 
	  hHiggsMass_GEN_NuToMET_greater->Fill(output.fHiggsMassSolutionSelected);
      }
      // Selection method: smaller
      selectNeutrinoPzAndHiggsMassSolution(output, eSmaller);
      output.fNeutrinoPzSolutionSmaller = output.fNeutrinoPzSolutionSelected;
      if (output.bPassedEvent) {
	if (myInputDataType == eRECO) hHiggsMass_smaller->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN) hHiggsMass_GEN_smaller->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN_NeutrinosReplacedWithMET) 
	  hHiggsMass_GEN_NuToMET_smaller->Fill(output.fHiggsMassSolutionSelected);
      }
      // Selection method: tauNuAngleMax
      selectNeutrinoPzAndHiggsMassSolution(output, eTauNuAngleMax);
      output.fNeutrinoPzSolutionTauNuAngleMax = output.fNeutrinoPzSolutionSelected;
      if (output.bPassedEvent) {
	if (myInputDataType == eRECO) hHiggsMass_tauNuAngleMax->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN) hHiggsMass_GEN_tauNuAngleMax->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN_NeutrinosReplacedWithMET) 
	  hHiggsMass_GEN_NuToMET_tauNuAngleMax->Fill(output.fHiggsMassSolutionSelected);
      }
      // Selection method: tauNuAngleMin
      selectNeutrinoPzAndHiggsMassSolution(output, eTauNuAngleMin);
      output.fNeutrinoPzSolutionTauNuAngleMin = output.fNeutrinoPzSolutionSelected;
      if (output.bPassedEvent) {
	if (myInputDataType == eRECO) hHiggsMass_tauNuAngleMin->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN) hHiggsMass_GEN_tauNuAngleMin->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN_NeutrinosReplacedWithMET) 
	  hHiggsMass_GEN_NuToMET_tauNuAngleMin->Fill(output.fHiggsMassSolutionSelected);
      }
      // Selection method: TauNuDeltaEtaMax
      selectNeutrinoPzAndHiggsMassSolution(output, eTauNuDeltaEtaMax);
      output.fNeutrinoPzSolutionTauNuDeltaEtaMax = output.fNeutrinoPzSolutionSelected;
      if (output.bPassedEvent) {
	if (myInputDataType == eRECO) hHiggsMass_tauNuDeltaEtaMax->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN) hHiggsMass_GEN_tauNuDeltaEtaMax->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN_NeutrinosReplacedWithMET) 
	  hHiggsMass_GEN_NuToMET_tauNuDeltaEtaMax->Fill(output.fHiggsMassSolutionSelected);
      }
      // Selection method: TauNuDeltaEtaMin
      selectNeutrinoPzAndHiggsMassSolution(output, eTauNuDeltaEtaMin);
      output.fNeutrinoPzSolutionTauNuDeltaEtaMin = output.fNeutrinoPzSolutionSelected;
      if (output.bPassedEvent) {
	if (myInputDataType == eRECO) hHiggsMass_tauNuDeltaEtaMin->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN) hHiggsMass_GEN_tauNuDeltaEtaMin->Fill(output.fHiggsMassSolutionSelected);
	if (myInputDataType == eGEN_NeutrinosReplacedWithMET) 
	  hHiggsMass_GEN_NuToMET_tauNuDeltaEtaMin->Fill(output.fHiggsMassSolutionSelected);
      }
    }
    // More common actions:
    applyCuts(output);
    doCountingAndHistogramming(iEvent, output, myInputDataType);
    // FINISHED CALCULATIONS.
  }

  void FullHiggsMassCalculator::calculateNeutrinoPz(TVector3& pTau, TVector3& pB, TVector3& MET, 
						    FullHiggsMassCalculator::Data& output) {
    output.bNegativeDiscriminantRecovered = false; // THIS IS IMPORTANT!
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
      neutrinoPzSolution1 = (A*B + TMath::Sqrt(discriminant))/(1 - B*B);
      neutrinoPzSolution2 = (A*B - TMath::Sqrt(discriminant))/(1 - B*B);
    }
    // If the discriminant is negative, there are two complex (and hence unphysical) solutions. We try to remedy this as follows.
    // Negative discriminant recovery strategy:
    //  * Set discriminant to zero and calculate (unambiguous) neutrino p_z
    //  * Solve MET value from requirement "discriminant = 0". (Which is a quadratic equation with two real solutions for MET)
    else {
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
	// Set output:
	output.fModifiedMETSolution1 = modifiedMETSolution1;
	output.fModifiedMETSolution2 = modifiedMETSolution2;
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
      std::cout << "                                AT CALCULATION" << std::endl;
      std::cout << "bJetVector: "<< pB.Px() << ", "<< pB.Py() << ", "<< pB.Pz()<< std::endl;
      std::cout << "tauVector: " << pTau.Px() << ", " << pTau.Py() << ", " << pTau.Pz() << std::endl;
      std::cout << "METVector: " << MET.Px() << ", " << MET.Py() << ", " << MET.Pz() << std::endl;
      std::cout << std::endl;
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

  void FullHiggsMassCalculator::constructFourMomenta(TVector3& pTau, TVector3& pB, TVector3& MET, 
						     FullHiggsMassCalculator::Data& output) {
    /* This method constructs the four-momenta of the tau, b-jet, and neutrinos. For the latter there are always two solutions.
       All four-momenta are saved to output. */
    TLorentzVector visibleTauMomentum;
    TLorentzVector bJetMomentum;
    TLorentzVector neutrinosMomentum1;
    TLorentzVector neutrinosMomentum2;
    double visibleTauEnergy = TMath::Sqrt(TMath::Power(c_fPhysicalTauMass,2) + TMath::Power(pTau.Px(),2) +
					  TMath::Power(pTau.Py(),2) + TMath::Power(pTau.Pz(),2));
    double bJetEnergy = TMath::Sqrt(TMath::Power(c_fPhysicalBeautyMass,2) + TMath::Power(pB.Px(),2) +
				    TMath::Power(pB.Py(),2) + TMath::Power(pB.Pz(),2));
    visibleTauMomentum.SetPxPyPzE(pTau.Px(), pTau.Py(), pTau.Pz(), visibleTauEnergy);
    bJetMomentum.SetPxPyPzE(pB.Px(), pB.Py(), pB.Pz(), bJetEnergy);
    neutrinosMomentum1.SetPxPyPzE(MET.Px(), MET.Py(), output.fNeutrinoPzSolution1, 
				  TMath::Sqrt(TMath::Power(MET.Px(), 2) + TMath::Power(MET.Py(), 2) + 
					      TMath::Power(output.fNeutrinoPzSolution1, 2)));
    neutrinosMomentum2.SetPxPyPzE(MET.Px(), MET.Py(), output.fNeutrinoPzSolution2, 
				  TMath::Sqrt(TMath::Power(MET.Px(), 2) + TMath::Power(MET.Py(), 2) + 
					      TMath::Power(output.fNeutrinoPzSolution2, 2)));
    if (output.fDiscriminant < 0) {
      // If the discriminant is zero, neutrinosFourMomentum1 will be equal to neutrinosFourMomentum2.
      // After the code below, they will still have the same z-components but rescaled transverse componentes
      neutrinosMomentum1.SetPerp(output.fModifiedMETSolution1);
      neutrinosMomentum2.SetPerp(output.fModifiedMETSolution2);
    }
    // Set output
    output.visibleTauFourMomentum = visibleTauMomentum;
    output.bJetFourMomentum = bJetMomentum;
    output.neutrinosFourMomentum1 = neutrinosMomentum1;
    output.neutrinosFourMomentum2 = neutrinosMomentum2;
    if (bPrintDebugOutput) {
      std::cout << "visible tau four-momentum " << output.visibleTauFourMomentum.Px() << " "
		<< output.visibleTauFourMomentum.Py() << " " << output.visibleTauFourMomentum.Pz()
		<< " " << output.visibleTauFourMomentum.M() << std::endl;
      std::cout << "b-jet four-momentum " << output.bJetFourMomentum.Px() << " "
		<< output.bJetFourMomentum.Py() << " " << output.bJetFourMomentum.Pz()
		<< " " << output.bJetFourMomentum.M() << std::endl;
      std::cout << "neutrinos four-momentum 1 " << output.neutrinosFourMomentum1.Px() << " "
		<< output.neutrinosFourMomentum1.Py() << " " << output.neutrinosFourMomentum1.Pz()
		<< " " << output.neutrinosFourMomentum1.M() << std::endl;
      std::cout << "neutrinos four-momentum 2 " << output.neutrinosFourMomentum2.Px() << " "
		<< output.neutrinosFourMomentum2.Py() << " " << output.neutrinosFourMomentum2.Pz()
		<< " " << output.neutrinosFourMomentum2.M() << std::endl;
    }
  }

  void FullHiggsMassCalculator::calculateTopMasses(FullHiggsMassCalculator::Data& output) {
    /* This method calculates the two top masses obtained for the two different neutrino momenta and saves them in output.
       In addition, it saves the one closer to the top rest mass as the selected value. */
    TLorentzVector topFourMomentum1 = output.visibleTauFourMomentum + output.bJetFourMomentum + output.neutrinosFourMomentum1;
    TLorentzVector topFourMomentum2 = output.visibleTauFourMomentum + output.bJetFourMomentum + output.neutrinosFourMomentum2;
    if (bPrintDebugOutput) {
      std::cout << "Top energy 1: " << topFourMomentum1.E() << std::endl;
      std::cout << "Top energy 2: " << topFourMomentum2.E() << std::endl;
      std::cout << "Top p_z component 1: " << topFourMomentum1.Pz() << std::endl;
      std::cout << "Top p_z component 2: " << topFourMomentum2.Pz() << std::endl;
      std::cout << "Top energy^2 - p_z^2   1: " << topFourMomentum1.E()*topFourMomentum1.E() - 
	topFourMomentum1.Pz()*topFourMomentum1.Pz() << std::endl;
      std::cout << "Top energy^2 - p_z^2   2: " << topFourMomentum2.E()*topFourMomentum2.E() - 
	topFourMomentum2.Pz()*topFourMomentum2.Pz() << std::endl;
    }
    output.fTopMassSolution1 = topFourMomentum1.M();
    output.fTopMassSolution2 = topFourMomentum2.M();
    // Select the one closer to the top rest mass:
    if (TMath::Abs(output.fTopMassSolution1 - c_fPhysicalTopMass) < TMath::Abs(output.fTopMassSolution2 - c_fPhysicalTopMass))
      output.fTopMassSolutionSelected = output.fTopMassSolution1;
    else output.fTopMassSolutionSelected = output.fTopMassSolution2;
  }

  void FullHiggsMassCalculator::selectModifiedMETSolution(FullHiggsMassCalculator::Data& output) {
    /* This method saves the modified MET solution that gives a better top mass match (closer to the rest mass) as the selected
       one in output. If the MET was not modified (the discriminant was positive), this method is a dummy. */
    if (TMath::Abs(output.fTopMassSolution1 - c_fPhysicalTopMass) < TMath::Abs(output.fTopMassSolution2 - c_fPhysicalTopMass))
      output.fModifiedMETSolutionSelected = output.fModifiedMETSolution1;
    else output.fModifiedMETSolutionSelected = output.fModifiedMETSolution2;
  }

  void FullHiggsMassCalculator::selectModifiedMETSolution(FullHiggsMassCalculator::Data& output, MetSelectionMethod myMetSelectionMethod) {
    /* This method saves the modified MET solution according to the method passed from the python cfg file parameters.
       one in output. If the MET was not modified (the discriminant was positive), this method is a dummy. */

    switch (myMetSelectionMethod) {
    case eSmallestMagnitude:
      if (TMath::Abs(output.fModifiedMETSolution1) < TMath::Abs(output.fModifiedMETSolution2) ){
	output.fModifiedMETSolutionSelected = output.fModifiedMETSolution1;
      }
      else output.fModifiedMETSolutionSelected = output.fModifiedMETSolution2;
      break;
    case eGreatestMagnitude:
      if (TMath::Abs(output.fModifiedMETSolution1) > TMath::Abs(output.fModifiedMETSolution2) ){
	output.fModifiedMETSolutionSelected = output.fModifiedMETSolution1;
      }
      else output.fModifiedMETSolutionSelected = output.fModifiedMETSolution2;
      break;
    case eClosestToTopMass:
      if (TMath::Abs(output.fTopMassSolution1 - c_fPhysicalTopMass) < TMath::Abs(output.fTopMassSolution2 - c_fPhysicalTopMass))
	output.fModifiedMETSolutionSelected = output.fModifiedMETSolution1;
      else output.fModifiedMETSolutionSelected = output.fModifiedMETSolution2;
      break;
    default:
      // Throw exception!
      throw cms::Exception("LogicError")
	<< "No implementation for the MET selection method found! Please check FullHiggsMassCalculator.cc and .h";
    }
   
    return;
  }
  
  void FullHiggsMassCalculator::calculateHiggsMasses(FullHiggsMassCalculator::Data& output) {
    /* This method calculates the two Higgs mass solutions and saves them to output. */
    TLorentzVector higgsMomentumSolution1 = output.visibleTauFourMomentum + output.neutrinosFourMomentum1;
    TLorentzVector higgsMomentumSolution2 = output.visibleTauFourMomentum + output.neutrinosFourMomentum2;
    output.fHiggsMassSolution1 = higgsMomentumSolution1.M();
    output.fHiggsMassSolution2 = higgsMomentumSolution2.M();
    if (bPrintDebugOutput) {
      std::cout << "Higgs energy^2 - p_z^2   1: " << higgsMomentumSolution1.E()*higgsMomentumSolution1.E() -
        higgsMomentumSolution1.Pz()*higgsMomentumSolution1.Pz() << std::endl;
      std::cout << "Higgs energy^2 - p_z^2   2: " << higgsMomentumSolution2.E()*higgsMomentumSolution2.E() -
        higgsMomentumSolution2.Pz()*higgsMomentumSolution2.Pz() << std::endl;
      std::cout << "Higgs mass solution 1: " << output.fHiggsMassSolution1 << std::endl;
      std::cout << "Higgs mass solution 2: " << output.fHiggsMassSolution2 << std::endl;
    }
  }

  bool FullHiggsMassCalculator::modifiedMETSolutionOneWasSelected(FullHiggsMassCalculator::Data& output) {
    /* This method returns true if the selected modified MET solution was solution 1 and false if it was solution 2.
       Returns false if the solutions are equal. */
    if (TMath::Abs(output.fModifiedMETSolutionSelected - output.fModifiedMETSolution1) <
        TMath::Abs(output.fModifiedMETSolutionSelected - output.fModifiedMETSolution2))
      return true;
    else return false;
  }

  bool FullHiggsMassCalculator::modifiedMETSolutionTwoWasSelected(FullHiggsMassCalculator::Data& output) {
    /* This method returns true if the selected modified MET solution was solution 2 and false if it was solution 1.
       Returns false if the solutions are equal. */
    if (TMath::Abs(output.fModifiedMETSolutionSelected - output.fModifiedMETSolution2) <
        TMath::Abs(output.fModifiedMETSolutionSelected - output.fModifiedMETSolution1))
      return true;
    else return false;
  }

  void FullHiggsMassCalculator::selectNeutrinoPzAndHiggsMassSolution(FullHiggsMassCalculator::Data& output, 
								       PzSelectionMethod selectionMethod) {
    // The following two variables (solution1, solution2) are only introduced to improve code readability!
    double solution1 = output.fNeutrinoPzSolution1;
    double solution2 = output.fNeutrinoPzSolution2;

    // Calculate some auxiliary quantities that may or may not be used for selecting a solution
    double angle1 = getAngleBetweenNeutrinosAndTau(output.visibleTauFourMomentum, output.neutrinosFourMomentum1);
    double angle2 = getAngleBetweenNeutrinosAndTau(output.visibleTauFourMomentum, output.neutrinosFourMomentum2);
    double deltaEta1 = getDeltaEtaBetweenNeutrinosAndTau(output.visibleTauFourMomentum, output.neutrinosFourMomentum1);
    double deltaEta2 = getDeltaEtaBetweenNeutrinosAndTau(output.visibleTauFourMomentum, output.neutrinosFourMomentum2);
    double deltaR1 = getDeltaRBetweenNeutrinosAndTau(output.visibleTauFourMomentum, output.neutrinosFourMomentum1);
    double deltaR2 = getDeltaRBetweenNeutrinosAndTau(output.visibleTauFourMomentum, output.neutrinosFourMomentum2);

    // Select a solution using the desired method
    // Initialize...
    bool selectSolution1 = false;
    // Go!
    if (bPrintDebugOutput) std::cout << "Neutrino p_z solution selection: ";
    switch (selectionMethod) {
    case eGreater:
      if (TMath::Abs(solution1) > TMath::Abs(solution2)) selectSolution1 = true;
      if (bPrintDebugOutput) std::cout << "select the greater solution" << std::endl;
      break;
    case eSmaller:
      if (TMath::Abs(solution1) < TMath::Abs(solution2)) selectSolution1 = true;
      if (bPrintDebugOutput) std::cout << "select the smaller solution" << std::endl;
      break;
    case eTauNuAngleMax:
      if (TMath::Abs(angle1) > TMath::Abs(angle2)) selectSolution1 = true;
      //if (angle1 > angle2) selectSolution1 = true;
      if (bPrintDebugOutput) std::cout << "select the solution which maximizes the angle between the tau and the neutrinos"
				       << std::endl;
      break;
    case eTauNuAngleMin:
      if (TMath::Abs(angle1) < TMath::Abs(angle2)) selectSolution1 = true;
      //if (angle1 < angle2) selectSolution1 = true;
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
      output.fNeutrinoPzSolutionSelected = solution1;
      output.fHiggsMassSolutionSelected = output.fHiggsMassSolution1;
      if (bPrintDebugOutput) std::cout << "Selected neutrino p_z and Higgs mass solution 1" << std::endl;
    } else {
      output.fNeutrinoPzSolutionSelected = solution2;
      output.fHiggsMassSolutionSelected = output.fHiggsMassSolution2;
      if (bPrintDebugOutput) std::cout << "Selected neutrino p_z and Higgs mass solution 2" << std::endl;
    }
  }

  double FullHiggsMassCalculator::getAngleBetweenNeutrinosAndTau(TLorentzVector& tauFourMom, TLorentzVector& neutrinosFourMom) {
    TVector3 neutrinoVector = neutrinosFourMom.Vect();
    return neutrinoVector.Angle(tauFourMom.Vect());
  }

  double FullHiggsMassCalculator::getDeltaEtaBetweenNeutrinosAndTau(TLorentzVector& tauFourMom, TLorentzVector& neutrinosFourMom) {
    return TMath::Abs(tauFourMom.Eta() - neutrinosFourMom.Eta());
  }

  double FullHiggsMassCalculator::getDeltaRBetweenNeutrinosAndTau(TLorentzVector& tauFourMom, TLorentzVector& neutrinosFourMom) {
    return tauFourMom.DeltaR(neutrinosFourMom);
  }
  
  bool FullHiggsMassCalculator::isBetterSolution(const edm::Event& iEvent, double selectedSolution,
						 FullHiggsMassCalculator::Data& output) {
    // Always return false if the event did not pass the selection in this file OR no valid p_z solution was calculated (for
    // whatever reason)
    if (!output.bPassedEvent || selectedSolution > 999999.0) return false;
    // If the event does not have a light charged Higgs, use the alternative method for determining the better solution.
    if (!eventHasLightChargedHiggs(iEvent)) return isBetterSolutionNoChargedHiggs(selectedSolution, output);
    double trueHiggsMass = getChargedHiggs(iEvent)->mass();
    // Find out which solution (1 or 2) was selected:
    if (neutrinoPzSolutionOneWasSelected(selectedSolution, output)) {
      if (TMath::Abs(output.fHiggsMassSolution1 - trueHiggsMass) > TMath::Abs(output.fHiggsMassSolution2 - trueHiggsMass))
	return false;
    } else if (neutrinoPzSolutionTwoWasSelected(selectedSolution, output)) {
      if (TMath::Abs(output.fHiggsMassSolution2 - trueHiggsMass) > TMath::Abs(output.fHiggsMassSolution1 - trueHiggsMass))
	return false;
    }
    else return false; // Return false if the two p_z solutions were equal.
    return true;
  }

  bool FullHiggsMassCalculator::isBetterSolutionNoChargedHiggs(double selectedSolution, FullHiggsMassCalculator::Data& output) {
    // Always return false if the event did not pass the selection in this file OR no valid p_z solution was calculated (for
    // whatever reason)
    if (!output.bPassedEvent || selectedSolution > 999999.0) return false;
    // Find out which solution (1 or 2) was selected:
    if (neutrinoPzSolutionOneWasSelected(selectedSolution, output)) {
      if (TMath::Abs(output.fNeutrinoPzSolution1 - output.fTrueNeutrinoPz) > 
	  TMath::Abs(output.fNeutrinoPzSolution2 - output.fTrueNeutrinoPz)) return false;
    } else if (neutrinoPzSolutionTwoWasSelected(selectedSolution, output)) {
      if (TMath::Abs(output.fNeutrinoPzSolution2 - output.fTrueNeutrinoPz) >
          TMath::Abs(output.fNeutrinoPzSolution1 - output.fTrueNeutrinoPz)) return false;
    }
    else return false; // Return false if the two p_z solutions were equal.
    return true;
  }

  bool FullHiggsMassCalculator::neutrinoPzSolutionOneWasSelected(double selectedSolution, FullHiggsMassCalculator::Data& output) {
    /* This method returns true if the selected neutrino p_z solution was solution 1 and false if it was solution 2.
       Returns false if the solutions are equal. */
    if (TMath::Abs(selectedSolution - output.fNeutrinoPzSolution1) < 
	TMath::Abs(selectedSolution - output.fNeutrinoPzSolution2))
      return true;
    else return false;
  }

  bool FullHiggsMassCalculator::neutrinoPzSolutionTwoWasSelected(double selectedSolution, FullHiggsMassCalculator::Data& output) {
    /* This method returns true if the selected neutrino p_z solution was solution 2 and false if it was solution 1.
       Returns false if the solutions are equal. */
    if (TMath::Abs(selectedSolution - output.fNeutrinoPzSolution2) <
	TMath::Abs(selectedSolution - output.fNeutrinoPzSolution1))
      return true;
    else return false;
  }
  
  void FullHiggsMassCalculator::applyCuts(FullHiggsMassCalculator::Data& output) {
    //if (output.fDiscriminant > 0) std::cout << output.fTopMassSolutionSelected << std::endl;
    if (output.fDiscriminant > 0 && (output.fTopMassSolutionSelected > 173.0 || output.fTopMassSolutionSelected < 172.0))
      output.bPassedEvent = false;
    if (fTopInvMassLowerCut >= 0 && output.fTopMassSolutionSelected < fTopInvMassLowerCut) output.bPassedEvent = false;
    if (fTopInvMassUpperCut >= 0 && output.fTopMassSolutionSelected > fTopInvMassUpperCut) output.bPassedEvent = false;
    // Re-apply (or not) the SignalAnalysis MET cut on the modified MET object
    if (output.fDiscriminant < 0 && fReApplyMetCut >= 0) {
      if (output.fModifiedMETSolutionSelected >= fReApplyMetCut) output.bPassedEvent = true;
      else output.bPassedEvent = false;
    }

    //std::cout << "fTopInvMassLowerCut: " << fTopInvMassLowerCut << std::endl;
    //std::cout << "fTopInvMassUpperCut: " << fTopInvMassUpperCut << std::endl;
    //if (output.fTopMassSolutionSelected < 140.0 || output.fTopMassSolutionSelected > 200.0) output.bPassedEvent = false;
    //if (output.fTopMassSolutionSelected < 100.0 || output.fTopMassSolutionSelected > 240.0) output.bPassedEvent = false;
    //if (output.fDiscriminant < -20000) output.bPassedEvent = false; // At -20000, the cut does not make much difference
    //TMath::Abs(output.fModifiedMET - <original MET>)
  }
  
  void FullHiggsMassCalculator::doCountingAndHistogramming(const edm::Event& iEvent, FullHiggsMassCalculator::Data& output, 
							   InputDataType myInputDataType) {
    // Choose the neutrino p_z selection method (can be set in python configuration scripts)
    selectNeutrinoPzAndHiggsMassSolution(output, fPzSelectionMethod);
    // Increment counters and fill Histograms
    switch (myInputDataType) {
    case eRECO:
      increment(allEvents_SubCount);
      hDiscriminant->Fill(output.fDiscriminant);
      if (output.fDiscriminant >= 0) {
	increment(positiveDiscriminant_SubCount);
	if (output.bPassedEvent) hHiggsMassPositiveDiscriminant->Fill(output.fHiggsMassSolutionSelected);
      } else {
	increment(negativeDiscriminant_SubCount);
	if (output.bPassedEvent) hHiggsMassNegativeDiscriminant->Fill(output.fHiggsMassSolutionSelected);
      }
      // THESE HISTOGRAMS ARE FILLED EVEN IF THE EVENT DOES NOT PASS --->
      hTopMassSolution->Fill(output.fTopMassSolutionSelected);
      h2TopMassVsInvariantMass->Fill(output.fTopMassSolutionSelected, output.fHiggsMassSolutionSelected);
      if (!iEvent.isRealData()) {
	h2TopMassVsNeutrinoNumber->Fill(output.fTopMassSolutionSelected, getNumberOfNeutrinosInEvent(iEvent));
	h2InvariantMassVsNeutrinoNumber->Fill(output.fHiggsMassSolutionSelected, getNumberOfNeutrinosInEvent(iEvent));
	if (!output.bPassedEvent) hNeutrinoNumberInRejectedEvents->Fill(getNumberOfNeutrinosInEvent(iEvent));
      }
      if (!output.bPassedEvent) break;
      // THESE HISTOGRAMS ARE FILLED ONLY IF THE EVENT HAS PASSED --->
      hHiggsMass->Fill(output.fHiggsMassSolutionSelected);
      if (bPrintDebugOutput) std::cout << "Solution put in histogram HiggsMass: " << output.fHiggsMassSolutionSelected << std::endl;
      if (!iEvent.isRealData()) hNeutrinoNumberInPassedEvents->Fill(getNumberOfNeutrinosInEvent(iEvent));
      hSelectedNeutrinoPzSolution->Fill(output.fNeutrinoPzSolutionSelected);
      // Counters (note: only incremented if the event has passed)
      increment(passedEvents_SubCount);
      if (iEvent.isRealData()) break; // The true solution is not known for real data.
      if (output.fDiscriminant > 0) { // this is done only for positive discriminants / two different possible p_z solutions:
	// Fill histograms with better and worse solutions:
	if (isBetterSolution(iEvent, output.fNeutrinoPzSolution1, output)) {
	  hHiggsMass_betterSolution->Fill(output.fHiggsMassSolution1);
	  hHiggsMass_worseSolution->Fill(output.fHiggsMassSolution2);
	} else if (isBetterSolution(iEvent, output.fNeutrinoPzSolution2, output)) {
	  hHiggsMass_betterSolution->Fill(output.fHiggsMassSolution2);
	  hHiggsMass_worseSolution->Fill(output.fHiggsMassSolution1);
	}
	else { // the solutions are the same and both histograms are filled with any of them
	  hHiggsMass_betterSolution->Fill(output.fHiggsMassSolution1);
	  hHiggsMass_worseSolution->Fill(output.fHiggsMassSolution1);
	}
	if (isBetterSolution(iEvent, output.fNeutrinoPzSolutionGreater, output)) // This works for both signal and bkg events!
	  increment(selectionGreaterCorrect_SubCount);
	if (isBetterSolution(iEvent, output.fNeutrinoPzSolutionSmaller, output))
	  increment(selectionSmallerCorrect_SubCount);
	if (isBetterSolution(iEvent, output.fNeutrinoPzSolutionTauNuAngleMax, output))
	  increment(selectionTauNuAngleMaxCorrect_SubCount);
	if (isBetterSolution(iEvent, output.fNeutrinoPzSolutionTauNuAngleMin, output))
	  increment(selectionTauNuAngleMinCorrect_SubCount);
	if (isBetterSolution(iEvent, output.fNeutrinoPzSolutionTauNuDeltaEtaMax, output))
	  increment(selectionTauNuDeltaEtaMaxCorrect_SubCount);
	if (isBetterSolution(iEvent, output.fNeutrinoPzSolutionTauNuDeltaEtaMin, output))
	  increment(selectionTauNuDeltaEtaMinCorrect_SubCount);
      }
      break;
    case eGEN:
      hDiscriminant_GEN->Fill(output.fDiscriminant);
      if (!output.bPassedEvent) break;
      hHiggsMass_GEN->Fill(output.fHiggsMassSolutionSelected);
      //hTopMassSolution_GEN->Fill(output.fTopMassSolutionSelected);
      break;
    case eGEN_NeutrinosReplacedWithMET:
      hDiscriminant_GEN_NeutrinosReplacedWithMET->Fill(output.fDiscriminant);
      if (!output.bPassedEvent) break;
      hHiggsMass_GEN_NeutrinosReplacedWithMET->Fill(output.fHiggsMassSolutionSelected);
      //hTopMassSolution_GEN_NeutrinosReplacedWithMET->Fill(output.fTopMassSolutionSelected);
      break;
    default:
      //Throw exception!
      throw cms::Exception("LogicError") << "The given InputDataType is invalid. Please check FullHiggsMassCalculator.cc and .h";
    }
  }

  void FullHiggsMassCalculator::doEventClassification(const edm::Event& iEvent, TVector3& bJetVector, TVector3& tauVector,
						      TVector3& METVector, FullHiggsMassCalculator::Data& output, const METSelection::Data& metData,
						      const GenParticleAnalysis::Data* genDataPtr) {
    if (!output.bPassedEvent) return; // Only passing events are classified; remove this if desired!
    increment(count_passedEvent);

    bool tauGenuine = false;
    bool bGenuine = false;
    reco::Candidate* closestGenTau = getClosestGenTau(iEvent, tauVector);
    reco::Candidate* closestGenBquark = getClosestGenBquark(iEvent, tauVector);
    if (closestGenTau != NULL) {
      tauGenuine = true;
      increment(count_tauGenuine);
    }
    if (closestGenBquark != NULL) {
      bGenuine = true;
      increment(count_bGenuine);
    }
    if (tauGenuine && bGenuine && tauAndBJetFromSameTopQuark(iEvent, *closestGenTau, *closestGenBquark))
      increment(count_tauAndBjetFromSameTopQuark);

    // Declare variables used to classify events
    double bDeltaR     = 9999;
    double tauDeltaR   = 9999;
    double metDeltaPt  = 9999;
    double metDeltaPhi = 9999;
    // Specify the cuts used to classify events
    double bDeltaRCut       =   0.6;
    double tauDeltaRCut     =   0.1;
    double metDeltaPtLoCut  = -40.0; // GeV
    double metDeltaPtHiCut  =  60.0; // GeV
    double metDeltaPhiCut   =  15.0 * TMath::DegToRad(); // The first number is the cut angle in deg, which is then converted to rad

    // B-jet: compare RECO and GEN information
    bDeltaR = getClosestGenBQuarkDeltaR(iEvent, bJetVector);
    if (bPrintDebugOutput) std::cout << "****** bDeltaR: " << bDeltaR << std::endl;
    // Tau: compare RECO and GEN information
    tauDeltaR = getClosestGenVisibleTauDeltaR(iEvent, tauVector);
    if (bPrintDebugOutput) std::cout << "****** tauDeltaR: " << tauDeltaR << std::endl;
  
    // MET: compare RECO and GEN information
    TVector3 genMETVector;
    if (genDataPtr != NULL && genDataPtr->isValid()) {
      // This gives the true GenMET, will work if GenParticleAnalysis::Data is available
      edm::Ptr<reco::GenMET> myGenMET = genDataPtr->getGenMET();
      genMETVector.SetXYZ(myGenMET->px(), myGenMET->py(), myGenMET->pz());
    } else {
      // This gives an approximate GenMET, but will work even if GenParticleAnalysis::Data is unavailable
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
    else increment(count_bMeasurementGood);
    if (metDeltaPt <= metDeltaPtLoCut || metDeltaPt >= metDeltaPtHiCut || TMath::Abs(metDeltaPhi) >= metDeltaPhiCut) {
      eventClassCode += eOnlyBadMET;
      increment(eventClass_AllBadMET_SubCount);
    }
    else increment(count_neutrinoMETCorrespondenceGood);
    if (tauDeltaR >= tauDeltaRCut) {
      eventClassCode += eOnlyBadTau;
      increment(eventClass_AllBadTau_SubCount);
    }
    else increment(count_tauMeasurementGood);

    if (tauGenuine && bGenuine && tauAndBJetFromSameTopQuark(iEvent, *closestGenTau, *closestGenBquark) && bDeltaR < bDeltaRCut && 
      metDeltaPt > metDeltaPtLoCut && metDeltaPt < metDeltaPtHiCut && TMath::Abs(metDeltaPhi) < metDeltaPhiCut && 
      tauDeltaR < tauDeltaRCut) increment(count_pure);

    if (bPrintDebugOutput) std::cout << "FullHiggsMassCalculator:   eventClassCode = " << eventClassCode << std::endl;
    // Define and set the event classes. Informative histograms are filled and counters incremented for each class
    switch (eventClassCode) {
    case ePure:
      output.eEventClassCode = ePure;
      eventClassName = "Pure";
      increment(eventClass_Pure_SubCount);
      if (output.bPassedEvent) hHiggsMassPure->Fill(output.fHiggsMassSolutionSelected);
      hDiscriminantPure->Fill(output.fDiscriminant);
      break;
    case eOnlyBadTau:
      output.eEventClassCode = eOnlyBadTau;
      eventClassName = "OnlyBadTau";
      increment(eventClass_OnlyBadTau_SubCount);
      if (output.bPassedEvent) hHiggsMassBadTau->Fill(output.fHiggsMassSolutionSelected);
      break;
    case eOnlyBadMET:
      output.eEventClassCode = eOnlyBadMET;
      eventClassName = "OnlyBadMET";
      increment(eventClass_OnlyBadMET_SubCount);
      if (output.bPassedEvent){
	hHiggsMassBadMET->Fill(output.fHiggsMassSolutionSelected);
	h2MetSignificanceVsBadMet->Fill(metData.getSelectedMET()->significance(), metData.getSelectedMET()->pt());
 	hDeltaPhiTauAndMetForBadMet->Fill( METVector.DeltaPhi(tauVector)*TMath::RadToDeg() );
  	hDeltaPhiTauAndBjetForBadMet->Fill( bJetVector.DeltaPhi(tauVector)*TMath::RadToDeg() );
 	hDeltaRTauAndMetForBadMet->Fill( METVector.DeltaR(tauVector) );
 	hDeltaRTauAndBjetForBadMet->Fill( bJetVector.DeltaR(tauVector) );
      }
      break;
    case eOnlyBadTauAndMET:
      output.eEventClassCode = eOnlyBadTauAndMET;
      eventClassName = "OnlyBadTauAndMET";
      increment(eventClass_OnlyBadTauAndMET_SubCount);
      if (output.bPassedEvent) hHiggsMassBadTauAndMET->Fill(output.fHiggsMassSolutionSelected);
      break;
    case eOnlyBadBjet:
      output.eEventClassCode = eOnlyBadBjet;
      eventClassName = "OnlyBadBjet";
      increment(eventClass_OnlyBadBjet_SubCount);
      if (output.bPassedEvent) hHiggsMassBadBjet->Fill(output.fHiggsMassSolutionSelected);
      break;
    case eOnlyBadBjetAndTau:
      output.eEventClassCode = eOnlyBadBjetAndTau;
      eventClassName = "OnlyBadBjetAndTau";
      increment(eventClass_OnlyBadBjetAndTau_SubCount);
      if (output.bPassedEvent) hHiggsMassBadBjetAndTau->Fill(output.fHiggsMassSolutionSelected);
      break;
    case eOnlyBadBjetAndMET:
      output.eEventClassCode = eOnlyBadBjetAndMET;
      eventClassName = "OnlyBadBjetAndMET";
      increment(eventClass_OnlyBadBjetAndMET_SubCount);
      if (output.bPassedEvent) hHiggsMassBadBjetAndMET->Fill(output.fHiggsMassSolutionSelected);
      break;
    case eOnlyBadBjetAndMETAndTau:
      output.eEventClassCode = eOnlyBadBjetAndMETAndTau;
      eventClassName = "OnlyBadBjetAndMETAndTau";
      increment(eventClass_OnlyBadBjetAndMETAndTau_SubCount);
      if (output.bPassedEvent) hHiggsMassBadBjetAndMETAndTau->Fill(output.fHiggsMassSolutionSelected);
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
      if (output.bPassedEvent) hHiggsMassImpure->Fill(output.fHiggsMassSolutionSelected);
      hDiscriminantImpure->Fill(output.fDiscriminant);
    }
    // TODO! If the tau and b-jet were identified correctly, check if they came from the same quark (i.e. if the correct b-jet
    //       was chosen by the mass calculation algorithm.
    //if (tauAndBJetFromSameTopQuark(...)) ...
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
