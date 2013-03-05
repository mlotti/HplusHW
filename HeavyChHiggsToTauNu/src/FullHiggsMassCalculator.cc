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
2) 

      Variable naming examples:
      *************************
      on-shell masses          : tauMass
      momentum (three-)vectors : tauVector, tauPlusBVector
      MET (three-)vector       : MET
      energies                 : tauPlusBEnergy
      calculated solutions     : neutrinoPzSolutionMax, topMassSolution1 (contain the word "solution")
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

std::vector<const reco::GenParticle*>   getImmediateMothers(const reco::Candidate&);
std::vector<const reco::GenParticle*>   getMothers(const reco::Candidate& p);
bool  hasImmediateMother(const reco::Candidate& p, int id);
bool  hasMother(const reco::Candidate& p, int id);
void  printImmediateMothers(const reco::Candidate& p);
void  printMothers(const reco::Candidate& p);
std::vector<const reco::GenParticle*>  getImmediateDaughters(const reco::Candidate& p);
std::vector<const reco::GenParticle*>   getDaughters(const reco::Candidate& p);
bool  hasImmediateDaughter(const reco::Candidate& p, int id);
bool  hasDaughter(const reco::Candidate& p, int id);
void  printImmediateDaughters(const reco::Candidate& p);
void printDaughters(const reco::Candidate& p);

namespace HPlus {
  FullHiggsMassCalculator::Data::Data():
    bPassedEvent(false),
    fDiscriminant(0),
    fTopMassSolution(0),
    fNeutrinoZSolution(0),
    fNeutrinoPtSolution(0),
    fHiggsMassSolution(0),
    fMCNeutrinoPz(0),
    LorentzVector_bJetFourMomentum(),
    LorentzVector_visibleTauFourMomentum(),
    LorentzVector_neutrinosFourMomentum(),
    iMisidentificationCode(0),
    strEventClassName(""),
    // Set the physical particle masses required in the calculation (in GeV)
    //c_fPhysicalTopMass(173.4),
    c_fPhysicalTopMass(172.4), // Use the same as in the generator!!!
    c_fPhysicalTauMass(1.778),
    c_fPhysicalBeautyMass(4.19)
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
    eventClass_BadTau_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Bad ID tau")),
    eventClass_BadMET_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Bad ID MET")),
    eventClass_BadTauAndMET_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Bad ID tau && MET")),
    eventClass_BadBjet_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Bad ID b-jet")),
    eventClass_BadBjetAndTau_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Bad ID b-jet && tau")),
    eventClass_MassBadBjetAndMET_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Bad ID b-jet && MET")),
    eventClass_MassBadBjetAndMETAndTau_SubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Bad ID b-jet && MET && tau"))
    
    
  {
    // Add a new directory ("FullHiggsMass") for the histograms produced in this code to the output file
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("FullHiggsMass");
    // Book histograms to be filled by this code
    // Vital histograms
    hHiggsMass                = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "HiggsMass", 
							  "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassDPz100          = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "HiggsMassDPz100", 
							  "Higgs massDPz100;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_TauBmatch      = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "HiggsMassTauBmatch", 
							  "Higgs massTauBmatch;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_TauBMETmatch   = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "HiggsMassTauBMETmatch",
							  "Higgs massTauBMETmatch;m_{H^{+}} (GeV)", 100, 0, 500);
    // Informative histograms
    hTopMass                  = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass", 
							  "Top mass;m_{top} (GeV)", 100, 0, 500);
    hNeutrinoZSolution        = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NeutrinoZSolution", 
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
    // The discriminant using in the neutrino longitudinal momentum calculation
    hDiscriminantPure         = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DiscriminantPure",
							  "DiscriminantPure", 100, -50000, 50000);
    hDiscriminantImpure       = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DiscriminantImpure",
							"DiscriminantImpure", 100, -50000, 50000);
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
  const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData) {
    ensureSilentAnalyzeAllowed(iEvent);
    // Disable histogram filling and counter incrementing until the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();
    return privateAnalyze(iEvent, iSetup, tauData, bData, metData);
  }
  
  FullHiggsMassCalculator::Data FullHiggsMassCalculator::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, tauData, bData, metData);
  }

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, 
  const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData) {
    Data output;
    Data physicalParameters; // this contains particles masses etc.

    std::cout << "==================================================================" << std::endl;

    // 1) Find the b-jet that is closest to the selected tau in (eta, phi) space
    //    This b-jet is assumed to come from the same top quark as a charged Higgs (hence, it belongs to the "Higgs side")
    edm::Ptr<pat::Jet> myHiggsSideBJet;
    myHiggsSideBJet = FullHiggsMassCalculator::findHiggsSideBJet(bData, tauData);
    output.HiggsSideBJet = myHiggsSideBJet;
    if (output.HiggsSideBJet.isNull()) {
      print("No reco Higgs side b-jet found!");
    } else {
      print("Reco Higgs side b-jet found");
    }

//     // 1b) Get the reco tau
//     edm::Ptr<pat::Tau> myTau;
//     myTau = tauData.getSelectedTau();

    // 2) Define b-jet, visible tau, and MET momentum vectors
    // TODO: check this
    std::cout << "####### b-jet energy: " << myHiggsSideBJet->energy() << std::endl;

    TVector3 myBJetVector(myHiggsSideBJet->px(), myHiggsSideBJet->py(), myHiggsSideBJet->pz());
    std::cout << "myBJetVector components: " << myBJetVector.Px() << ", " << myBJetVector.Py() << ", " << myBJetVector.Pz() 
	      << std::endl;
    // TODO: "visibleTau" is only used in MC. Invent a different name
    TVector3 myVisibleTauVector(tauData.getSelectedTau()->px(), tauData.getSelectedTau()->py(),
				      tauData.getSelectedTau()->pz());
    std::cout << "myVisibleTauVector components: " << myVisibleTauVector.Px() << ", " << myVisibleTauVector.Py() << ", "
	      << myVisibleTauVector.Pz() << std::endl;
    // This is the same MET as in the rest of the analysis (as it should be), by default: Type 1 PF
    TVector3 myMETVector(metData.getSelectedMET()->px(), metData.getSelectedMET()->py(), metData.getSelectedMET()->pz());
    std::cout << "myMETVector components: " << myMETVector.Px() << ", " << myMETVector.Py() << ", " << myMETVector.Pz() 
	      << std::endl;

    // 3) Calculate
    calculateNeutrinoPz(myVisibleTauVector, myBJetVector, myMETVector, physicalParameters, output);
    constructFourMomenta(myVisibleTauVector, myBJetVector, myMETVector, physicalParameters, output);
    calculateTopMass(output);
    calculateHiggsMass(output);

    // 4) If MC: Classify event according to what was identified correctly and what was not
    //    (the classification results are stored in output)
    if (!iEvent.isRealData()) {
      print("Doing event classification");
      doEventClassification(iEvent, myBJetVector, myVisibleTauVector, myMETVector, output);
    }

    // 5) Histograms are filled accordingly. There is a separate method to do this for MC and data
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

  edm::Ptr<pat::Jet> FullHiggsMassCalculator::findHiggsSideBJet(const BTagging::Data bData, const TauSelection::Data tauData) {
    double currentDeltaR = 1000.0;
    double smallestDeltaR = 999.0;
    edm::Ptr<pat::Jet> myHiggsSideBJet;
    // Loop over b-jets with tight tag (selected jets)
    for (edm::PtrVector<pat::Jet>::iterator iBjet = bData.getSelectedJets().begin();
	 iBjet != bData.getSelectedJets().end(); ++iBjet) {
      // Calculate the distance in (eta, phi) space between them and the selected tau. Choose the b-jet that is closest to the tau
      currentDeltaR = ROOT::Math::VectorUtil::DeltaR((*iBjet)->p4(), tauData.getSelectedTau()->p4());
      if (currentDeltaR < smallestDeltaR) {
        smallestDeltaR = currentDeltaR;
        myHiggsSideBJet = *iBjet;
      }
    }
    // Loop over b-jets with looser tag (selected sub-leading jets), doing the same as above
    for (edm::PtrVector<pat::Jet>::iterator iBjet = bData.getSelectedSubLeadingJets().begin();
	 iBjet != bData.getSelectedSubLeadingJets().end(); ++iBjet) {
      currentDeltaR = ROOT::Math::VectorUtil::DeltaR((*iBjet)->p4(), tauData.getSelectedTau()->p4());
      if (currentDeltaR < smallestDeltaR) {
        smallestDeltaR = currentDeltaR;
        myHiggsSideBJet = *iBjet;
      }
    }
    // Whichever b-jet (leading or sub-leading) had the smallest angular distance from the selected tau is returned.
    return myHiggsSideBJet;
  }

  void FullHiggsMassCalculator::calculateNeutrinoPz(TVector3& pTau, TVector3& pB, TVector3& MET, 
						    FullHiggsMassCalculator::Data& physicalParameters, 
						    FullHiggsMassCalculator::Data& output) {
    increment(fAllSolutionsCutSubCount);
    // Get the on-shell particle masses
    const double mTop = physicalParameters.c_fPhysicalTopMass;
    const double mTau = physicalParameters.c_fPhysicalTauMass;
    const double mB = physicalParameters.c_fPhysicalBeautyMass;
    std::cout << "Top, tau, and beauty mass: " << mTop << ", " << mTau << ", " << mB << std::endl;
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
      std::cout << "DISCRIMINANT < 0!!!" << std::endl;
      // ***Strategy***
      // Set discriminant to zero
      neutrinoPzSolution1 = A*B / (1 - B*B);
      neutrinoPzSolution2 = A*B / (1 - B*B);
    }
    // Set output
    output.fDiscriminant = discriminant;
    output.fNeutrinoZSolution = neutrinoPzSolution1; // Which solution should be selected?
    // Print information about the calculation steps
    std::cout << "FullHiggsMassCalculator: Reconstructing the neutrino p_z..." << std::endl;
    std::cout << "--- Tau reconstructed momentum = (" << pTau.Px() << ", " << pTau.Py() << ", " << pTau.Pz() << ")" << std::endl;
    std::cout << "--- B-jet reconstructed momentum = (" << pB.Px() << ", " << pB.Py() << ", " << pB.Pz() << ")" << std::endl;
    std::cout << "--- Neutrinos reconstructed momentum = (" << MET.Px() << ", " << MET.Py() << ", " << MET.Pz() << ")" << std::endl;
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
  }

  void FullHiggsMassCalculator::constructFourMomenta(TVector3& pTau, TVector3& pB, TVector3& MET, 
						     FullHiggsMassCalculator::Data& physicalParameters, 
						     FullHiggsMassCalculator::Data& output) {
    TLorentzVector visibleTauMomentum;
    TLorentzVector bJetMomentum;
    TLorentzVector neutrinosMomentum;
    double visibleTauEnergy = TMath::Sqrt(TMath::Power(physicalParameters.c_fPhysicalTauMass,2) + TMath::Power(pTau.Px(),2) +
					  TMath::Power(pTau.Py(),2) + TMath::Power(pTau.Pz(),2));
    double bJetEnergy = TMath::Sqrt(TMath::Power(physicalParameters.c_fPhysicalBeautyMass,2) + TMath::Power(pB.Px(),2) +
				    TMath::Power(pB.Py(),2) + TMath::Power(pB.Pz(),2));
    double neutrinosEnergy = TMath::Sqrt(TMath::Power(MET.Px(),2) + TMath::Power(MET.Py(),2) +
					 TMath::Power(output.fNeutrinoZSolution,2));
    visibleTauMomentum.SetPxPyPzE(pTau.Px(), pTau.Py(), pTau.Pz(), visibleTauEnergy);
    bJetMomentum.SetPxPyPzE(pB.Px(), pB.Py(), pB.Pz(), bJetEnergy);
    neutrinosMomentum.SetPxPyPzE(MET.Px(), MET.Py(), output.fNeutrinoZSolution, neutrinosEnergy);
    output.LorentzVector_visibleTauFourMomentum = visibleTauMomentum;
    output.LorentzVector_bJetFourMomentum = bJetMomentum;
    output.LorentzVector_neutrinosFourMomentum = neutrinosMomentum;
    //std::cout << "Norm of neutrino momentum four-vector (should be zero): " << neutrinosMomentum.M() << std::endl;
  }

  void FullHiggsMassCalculator::calculateTopMass(FullHiggsMassCalculator::Data& output) {
    TLorentzVector topMomentumSolution = output.LorentzVector_visibleTauFourMomentum + output.LorentzVector_bJetFourMomentum +
      output.LorentzVector_neutrinosFourMomentum;
    output.fTopMassSolution = topMomentumSolution.M();
    std::cout << "output.fTopMassSolution: " << output.fTopMassSolution << std::endl;
  }
  
  void FullHiggsMassCalculator::calculateHiggsMass(FullHiggsMassCalculator::Data& output) {
    TLorentzVector higgsMomentumSolution = output.LorentzVector_visibleTauFourMomentum + output.LorentzVector_neutrinosFourMomentum;
    output.fHiggsMassSolution = higgsMomentumSolution.M();
    std::cout << "output.fHiggsMassSolution: " << output.fHiggsMassSolution << std::endl;
  }

  void FullHiggsMassCalculator::doEventClassification(const edm::Event& iEvent, TVector3 recoBJetVector, TVector3 recoTauVector,
						      TVector3 recoMETVector, FullHiggsMassCalculator::Data& output) {
    // Declare variables used to classify events
    double bDeltaR     = 9999999;
    double tauDeltaR   = 9999999;
    double metDeltaPt  = 9999999;
    double metDeltaPhi = 9999999;
    // Specify the cuts used to classify events
    double bDeltaRCut     = 0.4;
    double tauDeltaRCut   = 0.1;
    double metDeltaPtCut  = 20.0; // GeV
    double metDeltaPhiCut = 10.0 * TMath::DegToRad(); // The first number is the cut angle in deg, which is then converted to rad
    // B-jet: compare RECO and GEN information
    reco::Candidate* genHiggsSideBJet = getGenHiggsSideBJet(iEvent);
    if (genHiggsSideBJet == NULL) {
      std::cout << "genHiggsSideBJet == NULL ---> no GEN b-jet found" << std::endl;
    } else {
      TVector3 genBJetVector(genHiggsSideBJet->px(), genHiggsSideBJet->py(), genHiggsSideBJet->pz());
      bDeltaR = recoBJetVector.DeltaR(genBJetVector);
      std::cout << "****** bDeltaR: " << bDeltaR << std::endl;
    }
    // Tau: compare RECO and GEN information
    TVector3 genTauVector = getGenTauFromHiggsVector(iEvent);
    if (genTauVector.Mag() < 0.00001) {
      std::cout << "****** The event did not have a tau from Higgs." << std::endl;
    } else {
      tauDeltaR = recoTauVector.DeltaR(genTauVector);
      std::cout << "****** tauDeltaR: " << tauDeltaR << std::endl;
    }
    // MET: compare RECO and GEN information
    TVector3 genMETVector = getGenMETVector(iEvent);
    metDeltaPt = recoMETVector.Pt() - genMETVector.Pt();
    metDeltaPhi = recoMETVector.DeltaPhi(genMETVector);
    std::cout << "****** metDeltaPt = " << metDeltaPt << std::endl;
    std::cout << "****** metDeltaPhi (in degrees) = " << metDeltaPhi * 180.0 / TMath::Pi() << std::endl;
    // Put the comparison values in histograms
    hBDeltaR->Fill(bDeltaR);
    hTauDeltaR->Fill(tauDeltaR);
    hMETDeltaPt->Fill(metDeltaPt);
    hMETDeltaPhi->Fill(metDeltaPhi * 180.0 / TMath::Pi());

    // Generate the "misidentification code" (an integer). It will be used to determine the event classes
    // NOTE: the if-statements check if something does NOT pass the cuts!
    if (bDeltaR >= bDeltaRCut) {
      output.iMisidentificationCode += 100;
    }
    if (TMath::Abs(metDeltaPt) >= metDeltaPtCut || TMath::Abs(metDeltaPhi) >= metDeltaPhiCut) {
      output.iMisidentificationCode += 10;
    }
    if (tauDeltaR >= tauDeltaRCut) {
      output.iMisidentificationCode += 1;
    }
    std::cout << "HAHAAAAHAHAHAHAHAHAAAAHAAHAHAHAAAAAAAAAAAAAAA: " << output.iMisidentificationCode << std::endl;
    // Define and set the event classes. Informative histograms are filled and counters incremented for each class
    switch (output.iMisidentificationCode) {
    case 0:
      output.strEventClassName = "Pure";
      increment(eventClass_Pure_SubCount);
      hHiggsMassPure->Fill(output.fHiggsMassSolution);
      hDiscriminantPure->Fill(output.fDiscriminant);
      break;
    case 1:
      output.strEventClassName = "BadTau";
      increment(eventClass_BadTau_SubCount);
      hHiggsMassBadTau->Fill(output.fHiggsMassSolution);
      break;
    case 10:
      output.strEventClassName = "BadMET";
      increment(eventClass_BadMET_SubCount);
      hHiggsMassBadMET->Fill(output.fHiggsMassSolution);
      break;
    case 11:
      output.strEventClassName = "BadTauAndMET";
      increment(eventClass_BadTauAndMET_SubCount);
      hHiggsMassBadTauAndMET->Fill(output.fHiggsMassSolution);
      break;
    case 100:
      output.strEventClassName = "BadBjet";
      increment(eventClass_BadBjet_SubCount);
      hHiggsMassBadBjet->Fill(output.fHiggsMassSolution);
      break;
    case 101:
      output.strEventClassName = "BadBjetAndTau";
      increment(eventClass_BadBjetAndTau_SubCount);
      hHiggsMassBadBjetAndTau->Fill(output.fHiggsMassSolution);
      break;
    case 110:
      output.strEventClassName = "BadBjetAndMET";
      increment(eventClass_MassBadBjetAndMET_SubCount);
      hHiggsMassBadBjetAndMET->Fill(output.fHiggsMassSolution);
      break;
    case 111:
      output.strEventClassName = "BadBjetAndMETAndTau";
      increment(eventClass_MassBadBjetAndMETAndTau_SubCount);
      hHiggsMassBadBjetAndMETAndTau->Fill(output.fHiggsMassSolution);
      break;
    default:
      output.strEventClassName = "######";
      std::cout << "EVENT CLASSIFICATON FAILED!" << std::endl;
    }
    std::cout << "strEventClassName = " << output.strEventClassName << std::endl;
    // Also do histogramming and counting for the set of events, in which ANYTHING was misidentified ("impure events")
    if (output.iMisidentificationCode > 0) {
      increment(eventClass_Impure_SubCount);
      hHiggsMassImpure->Fill(output.fHiggsMassSolution);
      hDiscriminantImpure->Fill(output.fDiscriminant);
    }
  }
  
  void FullHiggsMassCalculator::fillHistograms_MC(FullHiggsMassCalculator::Data& output) {
    hHiggsMass->Fill(output.fHiggsMassSolution);
    hTopMass->Fill(output.fTopMassSolution);
    hNeutrinoZSolution->Fill(output.fNeutrinoZSolution);
  }

  void FullHiggsMassCalculator::fillHistograms_Data(FullHiggsMassCalculator::Data& output) {
    hHiggsMass->Fill(output.fHiggsMassSolution);
    hTopMass->Fill(output.fTopMassSolution);
    hNeutrinoZSolution->Fill(output.fNeutrinoZSolution);
  }

  // This is an auxiliary function whose purpose is to facilitate debugging. Print statements can be enabled or disabled
  void FullHiggsMassCalculator::print(TString infoText) {
    bool debug = true;
    if (debug) {
      std::cout << "FullHiggsMassCalculator: " << infoText << std::endl;
    }
  }
}
