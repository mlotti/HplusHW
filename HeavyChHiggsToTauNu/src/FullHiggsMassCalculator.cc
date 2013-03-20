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

namespace HPlus {
  // Set this variable to true if you want debug print statements to be activated
  bool FullHiggsMassCalculator::bPrintDebugOutput = true;
  // Set the physical particle masses required in the calculation (in GeV)
  double FullHiggsMassCalculator::c_fPhysicalTopMass(172.4); // Use the same as in the generator!!!
  double FullHiggsMassCalculator::c_fPhysicalTauMass(1.778);
  double FullHiggsMassCalculator::c_fPhysicalBeautyMass(4.19);

  
  FullHiggsMassCalculator::Data::Data():
    bPassedEvent(false),
    fDiscriminant(0),
    fTopMassSolution(0),
    fNeutrinoPzSolution1(0),
    fNeutrinoPzSolution2(0),
    fSelectedNeutrinoPzSolution(0),
    fNeutrinoPtSolution(0),
    fHiggsMassSolution(0),
    fMCNeutrinoPz(0),
    LorentzVector_bJetFourMomentum(),
    LorentzVector_visibleTauFourMomentum(),
    LorentzVector_neutrinosFourMomentum(),
    strEventClassName("")
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
    eventClass_OnlyBadBjetAndMETAndTau_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Only bad ID b-jet && MET && tau")),

    eventClass_AllBadTau_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "All bad ID tau")),
    eventClass_AllBadMET_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "All bad ID MET")),
    eventClass_AllBadBjet_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "All bad ID b-jet"))
  {
    // Add a new directory ("FullHiggsMass") for the histograms produced in this code to the output file
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("FullHiggsMass");
    hHiggsMass                = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass",
							  "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassDPz100          = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassDPz100", 
							  "Higgs massDPz100;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_TauBmatch      = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassTauBmatch", 
							  "Higgs massTauBmatch;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_TauBMETmatch   = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassTauBMETmatch",
							  "Higgs massTauBMETmatch;m_{H^{+}} (GeV)", 100, 0, 500);
    // Informative histograms
    hTopMass                  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass", 
							  "Top mass;m_{top} (GeV)", 100, 0, 500);
    hSelectedNeutrinoPzSolution = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SelectedNeutrinoPzSolution", 
							  "Neutrino Z solution;p_{#nu,z} (GeV)", 100, -500, 500);
    hNeutrinoPtSolution       = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NeutrinoPtSolution", 
							  "Neutrino pT solution;p_{#nu,T} (GeV)", 100, 0, 500);
    hNeutrinoPtDifference     = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NeutrinoPtDifference", 
							  "Neutrino pT difference;p_{#nu,T} (GeV)", 200, -500, 500);
    hSolution1PzDifference    = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SolutionMinPzDifference", 
							  "Neutrino/MinSolution pz difference;(GeV)", 200, 0, 1000);
    hSolution2PzDifference    = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SolutionMaxPzDifference",
							  "Neutrino/MaxSolution pz difference;(GeV)", 200, 0, 1000);
    hSolution12PzDifference   = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "MinSolution", "MaxSolution ",
							  100, 0, 1000, 100, 0, 1000);
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
    //edm::FileInPath myDataPUdistribution = iConfig.getParameter<edm::FileInPath>("dataPUdistribution");
  }

  FullHiggsMassCalculator::~FullHiggsMassCalculator() {}

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const TauSelection::Data& tauData, const BTagging::Data& bData, const METSelection::Data& metData) {
    ensureSilentAnalyzeAllowed(iEvent);
    // Disable histogram filling and counter incrementing until the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    // If this method is called with tauData as an argument, get the selected tau from it and pass it on to privateAnalyze():
    const edm::Ptr<pat::Tau> myTau = tauData.getSelectedTau();
    return privateAnalyze(iEvent, iSetup, myTau, bData, metData);
  }

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const edm::Ptr<pat::Tau> myTau, const BTagging::Data& bData, const METSelection::Data& metData) {
    ensureSilentAnalyzeAllowed(iEvent);
    // Disable histogram filling and counter incrementing until the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    return privateAnalyze(iEvent, iSetup, myTau, bData, metData);
  }

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const TauSelection::Data& tauData, const BTagging::Data& bData, const METSelection::Data& metData) {
    ensureAnalyzeAllowed(iEvent);
    // If this method is called with tauData as an argument, get the selected tau from it and pass it on to privateAnalyze():
    const edm::Ptr<pat::Tau> myTau = tauData.getSelectedTau();
    return privateAnalyze(iEvent, iSetup, myTau, bData, metData);
  }

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const edm::Ptr<pat::Tau> myTau, const BTagging::Data& bData, const METSelection::Data& metData) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, myTau, bData, metData);
  }

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const edm::Ptr<pat::Tau> myTau, const BTagging::Data& bData, const METSelection::Data& metData) {
    Data output;

    // 0) Set this to true to print debug output
    if (bPrintDebugOutput) std::cout << "==================================================================" << std::endl;

    // 1) Find the b-jet that is closest to the selected tau in (eta, phi) space
    //    This b-jet is assumed to come from the same top quark as a charged Higgs (hence, it belongs to the "Higgs side")
    edm::Ptr<pat::Jet> myHiggsSideBJet;
    myHiggsSideBJet = FullHiggsMassCalculator::findHiggsSideBJet(bData, myTau);
    output.HiggsSideBJet = myHiggsSideBJet;
    if (output.HiggsSideBJet.isNull()) {
      if (bPrintDebugOutput) std::cout << "No reco Higgs side b-jet found! The code will crash." << std::endl;
    } else {
      if (bPrintDebugOutput) std::cout << "Reco Higgs side b-jet found" << std::endl;
    }

    // 2) Define b-jet, visible tau, and MET momentum vectors
    // TODO: check this
    if (bPrintDebugOutput) std::cout << "####### b-jet energy: " << myHiggsSideBJet->energy() << std::endl;

    TVector3 myBJetVector(myHiggsSideBJet->px(), myHiggsSideBJet->py(), myHiggsSideBJet->pz());
    // TODO: "visibleTau" is only used in MC. Invent a different name
    TVector3 myVisibleTauVector(myTau->px(), myTau->py(), myTau->pz());
    // This is the same MET as in the rest of the analysis (as it should be), normally (as of March 2013) Type 1 PF
    TVector3 myMETVector(metData.getSelectedMET()->px(), metData.getSelectedMET()->py(), metData.getSelectedMET()->pz());
    
    ////////////////////////////////////////////////////////////////////////////////
    // Running the analysis with the correct GEN objects (so far for signal only: //
    ////////////////////////////////////////////////////////////////////////////////
//     if (eventHasGenChargedHiggs(iEvent)) {
//       reco::Candidate* myGenBJet = getGenHiggsSideBJet(iEvent);
//       reco::Candidate* myGenTau = getGenTauFromHiggs(iEvent);
//       myBJetVector.SetXYZ(myGenBJet->px(), myGenBJet->py(), myGenBJet->pz());
//       myVisibleTauVector = getVisibleMomentum(*myGenTau);
//       myMETVector = getGenMETVector(iEvent);
//       myMETVector.SetZ(0.0);
//     }
    ////////////////////////////////////////////////////////
    
    if (bPrintDebugOutput) {
      std::cout << "myBJetVector components: " << myBJetVector.Px() << ", " << myBJetVector.Py() << ", " << myBJetVector.Pz()
		<< std::endl;
      std::cout << "myVisibleTauVector components: " << myVisibleTauVector.Px() << ", " << myVisibleTauVector.Py() << ", " 
		<< myVisibleTauVector.Pz() << std::endl;
      std::cout << "myMETVector components: " << myMETVector.Px() << ", " << myMETVector.Py() << ", " << myMETVector.Pz()
		<< std::endl;
    }

    // 3) Calculate the neutrino p_z solutions. Both are saved in output.
    calculateNeutrinoPz(myVisibleTauVector, myBJetVector, myMETVector, output);
    // 4) Select which neutrino p_z solution is used for the mass calculations. For each selection method, do the following:
    //    Calculate the invariant mass of the top quark and the Higgs boson (or what might be one).
    //    Constructing the four-momenta first greatly simplifies the equations and makes the code more readable.
    constructFourMomenta(myVisibleTauVector, myBJetVector, myMETVector, output);
    calculateTopMass(output);
    calculateHiggsMass(output);

    // 5) If MC: Classify event according to what was identified correctly and what was not
    //    (the classification results are stored in output)
    if (!iEvent.isRealData()) {
      if (bPrintDebugOutput) std::cout << "Doing Monte Carlo event classification" << std::endl;
      doEventClassification(iEvent, myBJetVector, myVisibleTauVector, myMETVector, output);
    }

    // 6) Histograms are filled accordingly. There is a separate method to do this for MC and data
    //    NOTE: events with no real neutrino p_z solutions are ignored at histogramming stage!
    if  (output.fDiscriminant >= 0.0) {
      if (!iEvent.isRealData()) {
	fillHistograms_MC(output);
      } else {
	fillHistograms_Data(output);
      }
    }
    
    // Return data object
    output.bPassedEvent = true; // for now, later implement possibility to cut
    return output;
  }

  edm::Ptr<pat::Jet> FullHiggsMassCalculator::findHiggsSideBJet(const BTagging::Data bData, const edm::Ptr<pat::Tau> myTau) {
    double currentDeltaR = 1000.0;
    double smallestDeltaR = 999.0;
    edm::Ptr<pat::Jet> myHiggsSideBJet;
    // Loop over b-jets with tight tag (selected jets)
    for (edm::PtrVector<pat::Jet>::iterator iBjet = bData.getSelectedJets().begin();
	 iBjet != bData.getSelectedJets().end(); ++iBjet) {
      // Calculate the distance in (eta, phi) space between them and the selected tau. Choose the b-jet that is closest to the tau
      currentDeltaR = ROOT::Math::VectorUtil::DeltaR((*iBjet)->p4(), myTau->p4());
      if (currentDeltaR < smallestDeltaR) {
        smallestDeltaR = currentDeltaR;
        myHiggsSideBJet = *iBjet;
      }
    }
    // Loop over b-jets with looser tag (selected sub-leading jets), doing the same as above
    for (edm::PtrVector<pat::Jet>::iterator iBjet = bData.getSelectedSubLeadingJets().begin();
	 iBjet != bData.getSelectedSubLeadingJets().end(); ++iBjet) {
      currentDeltaR = ROOT::Math::VectorUtil::DeltaR((*iBjet)->p4(), myTau->p4());
      if (currentDeltaR < smallestDeltaR) {
        smallestDeltaR = currentDeltaR;
        myHiggsSideBJet = *iBjet;
      }
    }
    // Whichever b-jet (leading or sub-leading) had the smallest angular distance from the selected tau is returned.
    return myHiggsSideBJet;
  }

  void FullHiggsMassCalculator::calculateNeutrinoPz(TVector3& pTau, TVector3& pB, TVector3& MET, 
						    FullHiggsMassCalculator::Data& output) {
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
      neutrinoPzSolution1 = (A*B + TMath::Sqrt(A*A - MET.Perp2() * (1 - B*B)))/(1 - B*B);
      neutrinoPzSolution2 = (A*B - TMath::Sqrt(A*A - MET.Perp2() * (1 - B*B)))/(1 - B*B);
    }
    // If the discriminant is negative, there are two imaginary solutions
    else {
      increment(fNegativeDiscriminantCutSubCount);
      if (bPrintDebugOutput) std::cout << "DISCRIMINANT < 0!!!" << std::endl;
      // ***Strategy***
      // Set discriminant to zero
      neutrinoPzSolution1 = A*B / (1 - B*B);
      neutrinoPzSolution2 = A*B / (1 - B*B);
    }

    // Set output
    output.fDiscriminant = discriminant;
    output.fNeutrinoPzSolution1 = neutrinoPzSolution1;
    output.fNeutrinoPzSolution2 = neutrinoPzSolution2;
    // To determine which solution should be selected, calculate the angle (deltaR?) between the 
    // two neutrino vectors and the tau vector. The solution giving the smaller angle is selected.
    double angle1 = getAngleBetweenNeutrinosAndTau(pTau, MET, neutrinoPzSolution1);
    double angle2 = getAngleBetweenNeutrinosAndTau(pTau, MET, neutrinoPzSolution2);
    hNeutrinosTauAngle1->Fill(angle1 * TMath::RadToDeg());
    hNeutrinosTauAngle2->Fill(angle2 * TMath::RadToDeg());
    if (angle1 < angle2) {
      output.fSelectedNeutrinoPzSolution = neutrinoPzSolution1;
    } else {
      output.fSelectedNeutrinoPzSolution = neutrinoPzSolution2;
    }

    // Print information about the calculation steps
    if (bPrintDebugOutput) {
      std::cout << "FullHiggsMassCalculator: Reconstructing the neutrino p_z..." << std::endl;
      std::cout << "--- Tau reconstructed momentum = (" << pTau.Px() << ", " << pTau.Py() << ", " << pTau.Pz() << ")" << std::endl;
      std::cout << "--- B-jet reconstructed momentum = (" << pB.Px() << ", " << pB.Py() << ", " << pB.Pz() << ")" << std::endl;
      std::cout << "--- Neutrinos reconstructed momentum = (" << MET.Px() << ", " << MET.Py() << ", "<< MET.Pz() << ")"<< std::endl;
      std::cout << "--- bEnergy = " << bEnergy << std::endl;
      std::cout << "--- visibleTauEnergy = " << visibleTauEnergy << std::endl;
      std::cout << "--- deltaSquaredMasses = " << deltaSquaredMasses << std::endl;    
      std::cout << "--- A = " << A << std::endl;
      std::cout << "--- B = " << B << std::endl;
      std::cout << "--- discriminant = " << discriminant << std::endl;
      std::cout << "--- Y/X = " << A*B / (1 - B*B) << std::endl;
      std::cout << "--- Z/X = " << TMath::Sqrt(A*A - MET.Perp2() * (1 - B*B)) / (1 - B*B) << std::endl;
      std::cout << "--- neutrinoPzSolution1 = " << neutrinoPzSolution1 << std::endl;
      std::cout << "--- neutrinoPzSolution2 = " << neutrinoPzSolution2 << std::endl;
      std::cout << "--- angle1 = " << angle1 << std::endl;
      std::cout << "--- angle2 = " << angle2 << std::endl;
    }
  }

  double FullHiggsMassCalculator::getAngleBetweenNeutrinosAndTau(TVector3& pTau, TVector3& MET, double neutrinoPz) {
    TVector3 neutrinoVector(MET.Px(), MET.Py(), neutrinoPz);
    return neutrinoVector.Angle(pTau);
  }

  void FullHiggsMassCalculator::constructFourMomenta(TVector3& pTau, TVector3& pB, TVector3& MET, 
						     FullHiggsMassCalculator::Data& output) {
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
    //if (bPrintDebugOutput) std::cout << "Norm of neutrino momentum four-vector (should be zero): " << neutrinosMomentum.M() << std::endl;
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

  void FullHiggsMassCalculator::doEventClassification(const edm::Event& iEvent, TVector3& recoBJetVector, TVector3& recoTauVector,
						      TVector3& recoMETVector, FullHiggsMassCalculator::Data& output) {
    // Declare variables used to classify events
    double bDeltaR     = 9999999;
    double tauDeltaR   = 9999999;
    double metDeltaPt  = 9999999;
    double metDeltaPhi = 9999999;
    // Specify the cuts used to classify events
    double bDeltaRCut       =   0.6;
    double tauDeltaRCut     =   0.1;
    double metDeltaPtLoCut  = -20.0; // GeV
    double metDeltaPtHiCut  =  40.0; // GeV
    double metDeltaPhiCut   =  15.0 * TMath::DegToRad(); // The first number is the cut angle in deg, which is then converted to rad

    //bool myEventHasGenChargedHiggs = eventHasGenChargedHiggs(iEvent);
    // B-jet: compare RECO and GEN information
    bDeltaR = getClosestGenBQuarkDeltaR(iEvent, recoBJetVector);
    if (bPrintDebugOutput) std::cout << "****** bDeltaR: " << bDeltaR << std::endl;
    // Tau: compare RECO and GEN information
    tauDeltaR = getClosestGenVisibleTauDeltaR(iEvent, recoTauVector);
    if (bPrintDebugOutput) std::cout << "****** tauDeltaR: " << tauDeltaR << std::endl;
  
    // MET: compare RECO and GEN information
    TVector3 genMETVector = getGenMETVector(iEvent);
    metDeltaPt = recoMETVector.Pt() - genMETVector.Pt();
    metDeltaPhi = recoMETVector.DeltaPhi(genMETVector);
    if (bPrintDebugOutput) std::cout << "****** metDeltaPt = " << metDeltaPt << std::endl;
    if (bPrintDebugOutput) std::cout << "****** metDeltaPhi (in degrees) = " << metDeltaPhi * 180.0 / TMath::Pi() << std::endl;
    // Put the comparison values in histograms
    hBDeltaR->Fill(bDeltaR);
    hTauDeltaR->Fill(tauDeltaR);
    hMETDeltaPt->Fill(metDeltaPt);
    hMETDeltaPhi->Fill(metDeltaPhi * 180.0 / TMath::Pi());

    // Generate the "misidentification code" (an integer). It will be used to determine the event classes
    int misidentificationCode = 0;
    // **********************************************************************************************************
    // Explanation: the misidentification code acts as a three-digit binary code eventual misidentifications
    // (1 = misidentification, 0 = no misidentification)
    // First digit: b-jet                          |      Example:   B M T
    // Second digit: MET                           |                 -----
    // Third digit: tau                            |                 1 0 1
    // Example: misidentificationCode = 101 would mean that the b-jet was misidentified,
    // the MET was identified correctly, and the tau was misidentified.
    // **********************************************************************************************************
    // NOTE: the if-statements below check if something does NOT pass the cuts!
    if (bDeltaR >= bDeltaRCut) {
      misidentificationCode += 100;
      increment(eventClass_AllBadBjet_SubCount);
    }
    if (metDeltaPt <= metDeltaPtLoCut || metDeltaPt >= metDeltaPtHiCut || TMath::Abs(metDeltaPhi) >= metDeltaPhiCut) {
      misidentificationCode += 10;
      increment(eventClass_AllBadMET_SubCount);
    }
    if (tauDeltaR >= tauDeltaRCut) {
      misidentificationCode += 1;
      increment(eventClass_AllBadTau_SubCount);
    }
    if (bPrintDebugOutput) std::cout << "FullHiggsMassCalculator:   misidentificationCode = " << misidentificationCode << std::endl;
    // Define and set the event classes. Informative histograms are filled and counters incremented for each class
    switch (misidentificationCode) {
    case 0:
      output.strEventClassName = "Pure";
      increment(eventClass_Pure_SubCount);
      if (output.fDiscriminant >= 0) hHiggsMassPure->Fill(output.fHiggsMassSolution);
      hDiscriminantPure->Fill(output.fDiscriminant);
      break;
    case 1:
      output.strEventClassName = "OnlyBadTau";
      increment(eventClass_OnlyBadTau_SubCount);
      if (output.fDiscriminant >= 0) hHiggsMassBadTau->Fill(output.fHiggsMassSolution);
      break;
    case 10:
      output.strEventClassName = "OnlyBadMET";
      increment(eventClass_OnlyBadMET_SubCount);
      if (output.fDiscriminant >= 0) hHiggsMassBadMET->Fill(output.fHiggsMassSolution);
      break;
    case 11:
      output.strEventClassName = "OnlyBadTauAndMET";
      increment(eventClass_OnlyBadTauAndMET_SubCount);
      if (output.fDiscriminant >= 0) hHiggsMassBadTauAndMET->Fill(output.fHiggsMassSolution);
      break;
    case 100:
      output.strEventClassName = "OnlyBadBjet";
      increment(eventClass_OnlyBadBjet_SubCount);
      if (output.fDiscriminant >= 0) hHiggsMassBadBjet->Fill(output.fHiggsMassSolution);
      break;
    case 101:
      output.strEventClassName = "OnlyBadBjetAndTau";
      increment(eventClass_OnlyBadBjetAndTau_SubCount);
      if (output.fDiscriminant >= 0) hHiggsMassBadBjetAndTau->Fill(output.fHiggsMassSolution);
      break;
    case 110:
      output.strEventClassName = "OnlyBadBjetAndMET";
      increment(eventClass_OnlyBadBjetAndMET_SubCount);
      if (output.fDiscriminant >= 0) hHiggsMassBadBjetAndMET->Fill(output.fHiggsMassSolution);
      break;
    case 111:
      output.strEventClassName = "OnlyBadBjetAndMETAndTau";
      increment(eventClass_OnlyBadBjetAndMETAndTau_SubCount);
      if (output.fDiscriminant >= 0) hHiggsMassBadBjetAndMETAndTau->Fill(output.fHiggsMassSolution);
      break;
    default:
      output.strEventClassName = "######";
      if (bPrintDebugOutput) std::cout << "EVENT CLASSIFICATON FAILED!" << std::endl;
    }
    if (bPrintDebugOutput) std::cout << "strEventClassName = " << output.strEventClassName << std::endl;
    // Also do histogramming and counting for the set of events, in which ANYTHING was misidentified ("impure events")
    if (misidentificationCode > 0) {
      increment(eventClass_Impure_SubCount);
      if (output.fDiscriminant >= 0) hHiggsMassImpure->Fill(output.fHiggsMassSolution);
      hDiscriminantImpure->Fill(output.fDiscriminant);
    }
  }
  
  void FullHiggsMassCalculator::fillHistograms_MC(FullHiggsMassCalculator::Data& output) {
    hHiggsMass->Fill(output.fHiggsMassSolution);
    hTopMass->Fill(output.fTopMassSolution);
    hSelectedNeutrinoPzSolution->Fill(output.fSelectedNeutrinoPzSolution);
  }

  void FullHiggsMassCalculator::fillHistograms_Data(FullHiggsMassCalculator::Data& output) {
    hHiggsMass->Fill(output.fHiggsMassSolution);
    hTopMass->Fill(output.fTopMassSolution);
    hSelectedNeutrinoPzSolution->Fill(output.fSelectedNeutrinoPzSolution);
  }
}
