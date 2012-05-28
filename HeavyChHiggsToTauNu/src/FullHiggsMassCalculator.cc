#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "TLorentzVector.h"
#include "TMath.h"
#include "TH1F.h"

namespace HPlus {
  FullHiggsMassCalculator::Data::Data(const FullHiggsMassCalculator* calculator, bool passEvent)
  : fCalculator(calculator),
    fPassedEvent(passEvent) { }
  FullHiggsMassCalculator::Data::~Data() { }

  FullHiggsMassCalculator::FullHiggsMassCalculator(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight)
  : fEventWeight(eventWeight)
 //   fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("FullHiggsMass");
    //hWeights = fs->make<TH1F>("pileupReweightWeights", "Reweighting weight distribution", 100, 0, 10);

    hHiggsMass = fs->make<TH1F>(myDir, "HiggsMass", "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassReal = fs->make<TH1F>(myDir, "HiggsMassReal", "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassImaginary = fs->make<TH1F>(myDir, "HiggsMassImaginary", "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hTopMass = fs->make<TH1F>(myDir, "TopMass", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassRejected = fs->make<TH1F>(myDir, "TopMassRejected", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassReal = fs->make<TH1F>(myDir, "TopMassReal", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassRealRejected = fs->make<TH1F>(myDir, "TopMassRealRejected", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassImaginary = fs->make<TH1F>(myDir, "TopMassImaginary", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassImaginaryRejected = fs->make<TH1F>(myDir, "TopMassImaginaryRejected", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hNeutrinoZSolution = fs->make<TH1F>(myDir, "NeutrinoZSolution", "Neutrino Z solution;p_{#nu,z} (GeV)", 100, -500, 500);
    hNeutrinoPtSolution = fs->make<TH1F>(myDir, "NeutrinoPtSolution", "Neutrino pT solution;p_{#nu,T} (GeV)", 100, 0, 500);
    hNeutrinoPtDifference = fs->make<TH1F>(myDir, "NeutrinoPtDifference", "Neutrino pT difference;p_{#nu,T} (GeV)", 200, -500, 500);

      //edm::FileInPath myDataPUdistribution = iConfig.getParameter<edm::FileInPath>("dataPUdistribution");
  }
  FullHiggsMassCalculator::~FullHiggsMassCalculator() {}


  FullHiggsMassCalculator::Data FullHiggsMassCalculator::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData) {
    // Initialise
    double fTopMassSolution = -1.0;
    double fNeutrinoZSolution = -1.0;
    double fNeutrinoPtSolution = -1.0;

    const double myTauMass = 1.778;
    const double myTopMass = 173.4;
    const double myBQuarkMass = 6.0;

    bool myPassedStatus = true;
    // 1) find b-jet
    // FIXME: add to b-tagging second b-jet threshold of 20 GeV
    TLorentzVector myBJet;
    double myMinDeltaR = 99.0;
    for (edm::PtrVector<pat::Jet>::iterator iBjet = bData.getSelectedJets().begin(); iBjet != bData.getSelectedJets().end(); ++iBjet) {
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR((*iBjet)->p4(), tauData.getSelectedTau()->p4());
      if (myDeltaR < myMinDeltaR) {
        myMinDeltaR = myDeltaR;
        myBJet = (*iBjet)->p4();
      }
    }
    // match in MC to see if it was the correct one
    
    // analyse deltaR
    
    // 2) set tau and MET info
    TLorentzVector myTau = tauData.getSelectedTau()->p4();
    TLorentzVector myMET = metData.getSelectedMET()->p4();
    
    // 3) Make three-vectors
    TVector3 myTauPlusBVector = myTau.vector3() + myMET.vector3();
    TVector3 myMETVector = myMET.vector3();
    double myDeltaSquared = TMath::Power(myTopMass,2) - TMath::Power(myTauMass,2) - TMath::Power(myBQuarkMass,2);
    double a = 2.0 * (myMETVector.X() * myTauPlusBVector.X() + myMETVector.Y() * myTauPlusBVector.Y()) + myDeltaSquared;
    double myTauPlusBEnergy = TMath::Sqrt(TMath::Power(myTauPlusBVector.P(),2)+TMath::Power(myTauMass+myBQuarkMass,2));
    double discriminant = TMath::Power(a,2) + 4.0 * TMath::Power(myTauPlusBVector.Z(),2) * TMath::Power(myMETVector.Perp(),2)
      - 4.0 * TMath::Power(myMETVector.Perp(),2) * (TMath::Power(myTauPlusBEnergy,2));
    if (discriminant > 0.0) {
      // Two real solutions exist
      double mySolution1 = (-4.0*a*myTauPlusBVector.Z() - myTauPlusBEnergy * TMath::Sqrt(discriminant))
        / (2.0 * TMath::Power(myTauPlusBVector.Z(),2) * TMath::Power(myTauPlusBEnergy,2));
      double mySolution2 = (-4.0*a*myTauPlusBVector.Z() + myTauPlusBEnergy * TMath::Sqrt(discriminant))
        / (2.0 * TMath::Power(myTauPlusBVector.Z(),2) * TMath::Power(myTauPlusBEnergy,2));
      // Calculate what the missing energy Z coordinate solutions yield for top mass
      double myTopMassSolution1 = TMath::Sqrt(TMath::Power(myTauMass,2)+TMath::Power(myBQuarkMass,2)
        + 2.0 * (TMath::Power(myMETVector.Perp(),2) + TMath::Power(mySolution1,2)) * myTauPlusBEnergy
        - 2.0 * (myTauPlusBVector.X() * myMETVector.X() + myTauPlusBVector.Y() * myMETVector.Y() + myTauPlusBVector.Z() * mySolution1));
      double myTopMassSolution2 = TMath::Sqrt(TMath::Power(myTauMass,2)+TMath::Power(myBQuarkMass,2)
        + 2.0 * (TMath::Power(myMETVector.Perp(),2) + TMath::Power(mySolution2,2)) * myTauPlusBEnergy
        - 2.0 * (myTauPlusBVector.X() * myMETVector.X() + myTauPlusBVector.Y() * myMETVector.Y() + myTauPlusBVector.Z() * mySolution2));
      fNeutrinoZSolution = mySolution1;
      fTopMassSolution = myTopMassSolution1;
      if (TMath::Abs(myTopMassSolution2 - myTopMass) < TMath::Abs(myTopMassSolution1 - myTopMass)) {
        fNeutrinoZSolution = mySolution2;
        fTopMassSolution = myTopMassSolution2;
        hTopMassRealRejected->Fill(myTopMassSolution1, fEventWeight.getWeight());
      } else {
        hTopMassRealRejected->Fill(myTopMassSolution2, fEventWeight.getWeight());
      }
    } else {
      // Two imaginary solutions exist; take real solutions as solution for neutrino Z and solve neutrino pT from discriminant = 0 equation
      fNeutrinoZSolution = (-4.0*a*myTauPlusBVector.Z()
        / (2.0 * TMath::Power(myTauPlusBVector.Z(),2) * TMath::Power(myTauPlusBEnergy,2));
      // Solutions from discriminant = 0 equation for neutrino pT
      double alpha = (myTauPlusBVector.X() * myMETVector.X() + myTauPlusBVector.Y() * myMETVector.Y())
        / myMETVector.Perp();
      double mySolution1 = (-alpha*myDeltaSquared + myDeltaSquared *
        TMath::Sqrt(TMath::Power(myTauPlusBEnergy,2) + TMath::Power(myTauPlusBVector.Z(),2)))
        / (2.0 * (TMath::Power(alpha,2) + TMath::Power(myTauPlusBVector,Z(),2) - TMath::Power(myTauPlusBEnergy,2)));
      double mySolution2 = (-alpha*myDeltaSquared + myDeltaSquared *
        TMath::Sqrt(TMath::Power(myTauPlusBEnergy,2) - TMath::Power(myTauPlusBVector.Z(),2)))
        / (2.0 * (TMath::Power(alpha,2) + TMath::Power(myTauPlusBVector,Z(),2) - TMath::Power(myTauPlusBEnergy,2)));
      // Calculate what the solutions yield for top mass
      double myTopMassSolution1 = TMath::Sqrt(TMath::Power(myTauMass,2)+TMath::Power(myBQuarkMass,2)
        + 2.0 * (TMath::Power(mySolution1,2) + TMath::Power(fNeutrinoZSolution,2)) * myTauPlusBEnergy
        - 2.0 * (alpha * mySolution1 + myTauPlusBVector.Z() * fNeutrinoZSolution));
      double myTopMassSolution2 = TMath::Sqrt(TMath::Power(myTauMass,2)+TMath::Power(myBQuarkMass,2)
        + 2.0 * (TMath::Power(mySolution2,2) + TMath::Power(fNeutrinoZSolution,2)) * myTauPlusBEnergy
        - 2.0 * (alpha * mySolution2 + myTauPlusBVector.Z() * fNeutrinoZSolution));
      fNeutrinoPtSolution = mySolution1;
      fTopMassSolution = myTopMassSolution1;
      if (TMath::Abs(myTopMassSolution2 - myTopMass) < TMath::Abs(myTopMassSolution1 - myTopMass)) {
        fNeutrinoPtSolution = mySolution2;
        fTopMassSolution = myTopMassSolution2;
        hTopMassImaginaryRejected->Fill(myTopMassSolution1, fEventWeight.getWeight());
      } else {
        hTopMassImaginaryRejected->Fill(myTopMassSolution2, fEventWeight.getWeight());
      }
    }
    // Fill top mass histograms
    hTopMass->Fill(fTopMassSolution, fEventWeight.getWeight());
    if (discriminant >= 0.0) {
      hTopMassReal->Fill(fTopMassSolution, fEventWeight.getWeight());
    } else {
      hTopMassImaginary->Fill(fTopMassSolution, fEventWeight.getWeight());
    }
    // Fill neutrino histograms
    hNeutrinoZSolution->Fill(fNeutrinoZSolution, fEventWeight.getWeight());
    if (hNeutrinoPtSolution > 0.0) {
      hNeutrinoPtSolution->Fill(fNeutrinoPtSolution, fEventWeight.getWeight());
      hNeutrinoPtDifference->Fill(fNeutrinoPtSolution, fEventWeight.getWeight()-myMETVector.Perp());
    }
    // Neutrino three vector has been solved, let's calculate Higgs mass
    // m_h^2 = m_tau^2 + 2 E_tau E_neutrinoes
    myNeutrinoEnergy = 0.0;
    if (fNeutrinoPtSolution >= 0.0) {
      myNeutrinoEnergy = TMath::Sqrt(TMath::Power(fNeutrinoPtSolution,2) + TMath::Power(fNeutrinoZSolution,2));
    } else {
      myNeutrinoEnergy = TMath::Sqrt(TMath::Power(myMETVector.Perp(),2) + TMath::Power(fNeutrinoZSolution,2));
    }
    fHiggsMassSolution = TMath::Sqrt(TMath::Power(myTauMass,2)
      + 2.0 * TMath::Sqrt(TMath::Power(myTau.P(),2) + TMath::Power(myTauMass,2)) * myNeutrinoEnergy);
    hHiggsMass->Fill(fHiggsMassSolution, fEventWeight.getWeight());
    if (discriminant >= 0.0) {
      hHiggsMassReal->Fill(fHiggsMassSolution, fEventWeight.getWeight());
    } else {
      hHiggsMassImaginary->Fill(fHiggsMassSolution, fEventWeight.getWeight());
    }
    // Return data object
    return FullHiggsMassCalculator::Data(this, myPassedStatus);
  }
}
