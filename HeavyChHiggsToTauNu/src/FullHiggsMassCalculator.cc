#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "Math/GenVector/VectorUtil.h"
#include "TLorentzVector.h"
#include "TVector3.h"
#include "TMath.h"
#include "TH1F.h"

namespace HPlus {
  FullHiggsMassCalculator::Data::Data(const FullHiggsMassCalculator* calculator, bool passEvent)
  : fCalculator(calculator),
    fPassedEvent(passEvent) { }
  FullHiggsMassCalculator::Data::~Data() { }

  FullHiggsMassCalculator::FullHiggsMassCalculator(EventCounter& eventCounter, EventWeight& eventWeight)
  : fEventWeight(eventWeight)
 //   fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
  {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("FullHiggsMass");
    //hWeights = makeTH<TH1F>("pileupReweightWeights", "Reweighting weight distribution", 100, 0, 10);
    hHiggsMass = makeTH<TH1F>(myDir, "HiggsMass", "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassReal = makeTH<TH1F>(myDir, "HiggsMassReal", "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassImaginary = makeTH<TH1F>(myDir, "HiggsMassImaginary", "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hTopMass = makeTH<TH1F>(myDir, "TopMass", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassRejected = makeTH<TH1F>(myDir, "TopMassRejected", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassReal = makeTH<TH1F>(myDir, "TopMassReal", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassRealRejected = makeTH<TH1F>(myDir, "TopMassRealRejected", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassImaginary = makeTH<TH1F>(myDir, "TopMassImaginary", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassImaginaryRejected = makeTH<TH1F>(myDir, "TopMassImaginaryRejected", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hNeutrinoZSolution = makeTH<TH1F>(myDir, "NeutrinoZSolution", "Neutrino Z solution;p_{#nu,z} (GeV)", 100, -500, 500);
    hNeutrinoPtSolution = makeTH<TH1F>(myDir, "NeutrinoPtSolution", "Neutrino pT solution;p_{#nu,T} (GeV)", 100, 0, 500);
    hNeutrinoPtDifference = makeTH<TH1F>(myDir, "NeutrinoPtDifference", "Neutrino pT difference;p_{#nu,T} (GeV)", 200, -500, 500);

      //edm::FileInPath myDataPUdistribution = iConfig.getParameter<edm::FileInPath>("dataPUdistribution");
  }
  FullHiggsMassCalculator::~FullHiggsMassCalculator() {}


  FullHiggsMassCalculator::Data FullHiggsMassCalculator::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData) {
    bool myPassedStatus = true;
    // 1) find b-jet
    // FIXME: add to b-tagging second b-jet threshold of 20 GeV
    TVector3 myBJetVector;
    double myMinDeltaR = 99.0;
    edm::Ptr<pat::Jet> myBJet;
    for (edm::PtrVector<pat::Jet>::iterator iBjet = bData.getSelectedJets().begin(); iBjet != bData.getSelectedJets().end(); ++iBjet) {
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR((*iBjet)->p4(), tauData.getSelectedTau()->p4());
      if (myDeltaR < myMinDeltaR) {
        myMinDeltaR = myDeltaR;
        myBJet = *iBjet;
        myBJetVector.SetXYZ((*iBjet)->px(), (*iBjet)->py(), (*iBjet)->pz());
      }
    }
    // match in MC to see if it was the correct one
    if (!iEvent.isRealData())
      bool myMatchStatus = doMCMatching(iEvent, tauData.getSelectedTau(), myBJet);

    // 2) set tau and MET info
    TVector3 myTauVector(tauData.getSelectedTau()->px(), tauData.getSelectedTau()->py(), tauData.getSelectedTau()->pz());
    TVector3 myMETVector(metData.getSelectedMET()->px(), metData.getSelectedMET()->py(), metData.getSelectedMET()->pz());

    // 3) calculate
    // FIXME doCalculate(myTauVector, myBJetVector, myMETVector);

    // Return data object
    return FullHiggsMassCalculator::Data(this, myPassedStatus);
  }
  
  void FullHiggsMassCalculator::doCalculate(TVector3& tau, TVector3& bjet, TVector3& met, bool doHistogramming) {
    // Initialise
    double fTopMassSolution = -1.0;
    double fNeutrinoZSolution = -1.0;
    double fNeutrinoPtSolution = -1.0;
    const double myTauMass = 1.778;
    const double myTopMass = 173.4;
    const double myBQuarkMass = 4.19;
    TVector3 myTauPlusBVector = tau + bjet;

    double myDeltaSquared = TMath::Power(myTopMass,2) - TMath::Power(myTauMass,2) - TMath::Power(myBQuarkMass,2);
    double a = 2.0 * (met.X() * myTauPlusBVector.X() + met.Y() * myTauPlusBVector.Y()) + myDeltaSquared;
    double myTauPlusBEnergy = TMath::Sqrt(TMath::Power(myTauPlusBVector.Mag(),2)+TMath::Power(myTauMass+myBQuarkMass,2));
    double discriminant = TMath::Power(a,2) + 4.0 * TMath::Power(myTauPlusBVector.Z(),2) * TMath::Power(met.Perp(),2)
      - 4.0 * TMath::Power(met.Perp(),2) * (TMath::Power(myTauPlusBEnergy,2));
    std::cout << "tau+b:, " << myTauPlusBVector.X() << ", " << myTauPlusBVector.Y() << ", " << myTauPlusBVector.Z() << std::endl;
    std::cout << "tau:, " << tau.X() << ", " << tau.Y() << ", " << tau.Z() << std::endl;
    std::cout << "bjet:, " << bjet.X() << ", " << bjet.Y() << ", " << bjet.Z() << std::endl;
    std::cout << "MET:, " << met.X() << ", " << met.Y() << ", " << met.Z() << std::endl;
    std::cout << "DeltaSquared, " << myDeltaSquared << std::endl;
    std::cout << "a, " << a << std::endl;
    std::cout << "tau+b energy, " << myTauPlusBEnergy << std::endl;
    std::cout << "discriminant, " << discriminant << std::endl;

    if (discriminant > 0.0) {
      // Two real solutions exist
      double mySolution1 = (-a*myTauPlusBVector.Z() - myTauPlusBEnergy * TMath::Sqrt(discriminant))
        / (2.0 * (TMath::Power(myTauPlusBVector.Z(),2) - TMath::Power(myTauPlusBEnergy,2)));
      double mySolution2 = (-a*myTauPlusBVector.Z() + myTauPlusBEnergy * TMath::Sqrt(discriminant))
        / (2.0 * (TMath::Power(myTauPlusBVector.Z(),2) - TMath::Power(myTauPlusBEnergy,2)));
      // Calculate what the missing energy Z coordinate solutions yield for top mass
      double myTopMassSolution1 = TMath::Sqrt(TMath::Power(myTauMass,2)+TMath::Power(myBQuarkMass,2)
        + 2.0 * TMath::Sqrt(TMath::Power(met.Perp(),2) + TMath::Power(mySolution1,2)) * myTauPlusBEnergy
        - 2.0 * (myTauPlusBVector.X() * met.X() + myTauPlusBVector.Y() * met.Y() + myTauPlusBVector.Z() * mySolution1));
      double myTopMassSolution2 = TMath::Sqrt(TMath::Power(myTauMass,2)+TMath::Power(myBQuarkMass,2)
        + 2.0 * TMath::Sqrt(TMath::Power(met.Perp(),2) + TMath::Power(mySolution2,2)) * myTauPlusBEnergy
        - 2.0 * (myTauPlusBVector.X() * met.X() + myTauPlusBVector.Y() * met.Y() + myTauPlusBVector.Z() * mySolution2));
      std::cout << "real solution, nu_Z, " << mySolution1 << ", " << mySolution2 << std::endl;
      std::cout << "real solution, mtop, " << myTopMassSolution1 << ", " << myTopMassSolution2 << std::endl;
      fNeutrinoZSolution = mySolution1;
      fTopMassSolution = myTopMassSolution1;
      if (TMath::Abs(myTopMassSolution2 - myTopMass) < TMath::Abs(myTopMassSolution1 - myTopMass)) {
        fNeutrinoZSolution = mySolution2;
        fTopMassSolution = myTopMassSolution2;
        if (doHistogramming)
          hTopMassRealRejected->Fill(myTopMassSolution1, fEventWeight.getWeight());
      } else {
        if (doHistogramming)
          hTopMassRealRejected->Fill(myTopMassSolution2, fEventWeight.getWeight());
      }
      // Calculate Higgs boson mass
      double myNeutrinoEnergy = TMath::Sqrt(TMath::Power(met.Perp(),2) + TMath::Power(fNeutrinoZSolution,2));
      fHiggsMassSolution = TMath::Sqrt(TMath::Power(myTauMass,2)
        + 2.0 * TMath::Sqrt(TMath::Power(tau.Mag(),2) + TMath::Power(myTauMass,2)) * myNeutrinoEnergy
        - 2.0 * (tau.X()*met.X() + tau.Y()*met.Y() + tau.Z()*fNeutrinoZSolution));
    } else {
      // Two imaginary solutions exist; take real solutions as solution for neutrino Z and solve neutrino pT from discriminant = 0 equation
      fNeutrinoZSolution = (-a*myTauPlusBVector.Z())
        / (2.0 * (TMath::Power(myTauPlusBVector.Z(),2) - TMath::Power(myTauPlusBEnergy,2)));
      // Solutions from discriminant = 0 equation for neutrino pT
      double alpha = (myTauPlusBVector.X() * met.X() + myTauPlusBVector.Y() * met.Y()) / met.Perp();
      double mySolution1 = (-alpha*myDeltaSquared + myDeltaSquared *
        TMath::Sqrt(TMath::Power(myTauPlusBEnergy,2) - TMath::Power(myTauPlusBVector.Z(),2)))
        / (2.0 * (TMath::Power(alpha,2) + TMath::Power(myTauPlusBVector.Z(),2) - TMath::Power(myTauPlusBEnergy,2)));
      double mySolution2 = (-alpha*myDeltaSquared - myDeltaSquared *
        TMath::Sqrt(TMath::Power(myTauPlusBEnergy,2) - TMath::Power(myTauPlusBVector.Z(),2)))
        / (2.0 * (TMath::Power(alpha,2) + TMath::Power(myTauPlusBVector.Z(),2) - TMath::Power(myTauPlusBEnergy,2)));
      // Calculate what the solutions yield for top mass
      double myTopMassSolution1 = TMath::Sqrt(TMath::Power(myTauMass,2)+TMath::Power(myBQuarkMass,2)
        + 2.0 * TMath::Sqrt(TMath::Power(mySolution1,2) + TMath::Power(fNeutrinoZSolution,2)) * myTauPlusBEnergy
        - 2.0 * (alpha * mySolution1 + myTauPlusBVector.Z() * fNeutrinoZSolution));
      double myTopMassSolution2 = TMath::Sqrt(TMath::Power(myTauMass,2)+TMath::Power(myBQuarkMass,2)
        + 2.0 * TMath::Sqrt(TMath::Power(mySolution2,2) + TMath::Power(fNeutrinoZSolution,2)) * myTauPlusBEnergy
        - 2.0 * (alpha * mySolution2 + myTauPlusBVector.Z() * fNeutrinoZSolution));
      std::cout << "imag solution, nu_Z/alpha/nu_T, " << fNeutrinoZSolution << ", " << alpha << ", " << mySolution1 << ", " << mySolution2 << std::endl;
      std::cout << "imag solution, mtop, " << myTopMassSolution1 << ", " << myTopMassSolution2 << std::endl;
      fNeutrinoPtSolution = mySolution1;
      fTopMassSolution = myTopMassSolution1;
      if (TMath::Abs(myTopMassSolution2 - myTopMass) < TMath::Abs(myTopMassSolution1 - myTopMass)) {
        fNeutrinoPtSolution = mySolution2;
        fTopMassSolution = myTopMassSolution2;
        if (doHistogramming)
          hTopMassImaginaryRejected->Fill(myTopMassSolution1, fEventWeight.getWeight());
      } else {
        if (doHistogramming)
          hTopMassImaginaryRejected->Fill(myTopMassSolution2, fEventWeight.getWeight());
      }
      // Calculate Higgs boson mass
      double alphaPrime = (tau.X() * met.X() + tau.Y() * met.Y()) / met.Perp();
      double myNeutrinoEnergy = TMath::Sqrt(TMath::Power(fNeutrinoPtSolution,2) + TMath::Power(fNeutrinoZSolution,2));
      fHiggsMassSolution = TMath::Sqrt(TMath::Power(myTauMass,2)
        + 2.0 * TMath::Sqrt(TMath::Power(tau.Mag(),2) + TMath::Power(myTauMass,2)) * myNeutrinoEnergy
        - 2.0 * alphaPrime * fNeutrinoPtSolution);
      std::cout << "alpha prime/Enu, " << alphaPrime << ", " << myNeutrinoEnergy << std::endl;
    }
    // Fill top mass histograms
    if (doHistogramming) {
      hTopMass->Fill(fTopMassSolution, fEventWeight.getWeight());
      if (discriminant >= 0.0) {
        hTopMassReal->Fill(fTopMassSolution, fEventWeight.getWeight());
      } else {
        hTopMassImaginary->Fill(fTopMassSolution, fEventWeight.getWeight());
      }
    }
    // Fill neutrino histograms
    if (doHistogramming) {
      hNeutrinoZSolution->Fill(fNeutrinoZSolution, fEventWeight.getWeight());
      if (fNeutrinoPtSolution > 0.0) {
        hNeutrinoPtSolution->Fill(fNeutrinoPtSolution, fEventWeight.getWeight());
        hNeutrinoPtDifference->Fill(fNeutrinoPtSolution-met.Perp(), fEventWeight.getWeight());
      }
    }
    std::cout << "mHiggs, " << fHiggsMassSolution << std::endl;
    if (doHistogramming) {
      hHiggsMass->Fill(fHiggsMassSolution, fEventWeight.getWeight());
      if (discriminant >= 0.0) {
        hHiggsMassReal->Fill(fHiggsMassSolution, fEventWeight.getWeight());
      } else {
        hHiggsMassImaginary->Fill(fHiggsMassSolution, fEventWeight.getWeight());
      }
    }
  }
  
  bool FullHiggsMassCalculator::doMCMatching(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& tau, const edm::Ptr<pat::Jet>& bjet) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    // Find last Hplus line
    size_t myHiggsLine = 0;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (TMath::Abs(p.pdgId()) == 37)
        myHiggsLine = i;
    }
    std::cout << "FullMass: Higgs line " << myHiggsLine << std::endl;
    if (!myHiggsLine) return false;
    // Find top, from which Higgs comes from
    reco::Candidate* myHiggsSideTop = const_cast<reco::Candidate*>(genParticles->at(myHiggsLine).mother());
    bool myStatus = true;
    while (myStatus) {
      if (!myHiggsSideTop) myStatus = false;
      std::cout << "FullMass: Higgs side mother = " << myHiggsSideTop->pdgId() << std::endl;
      if (TMath::Abs(myHiggsSideTop->pdgId()) == 6) myStatus = false;
      if (myStatus)
        myHiggsSideTop = const_cast<reco::Candidate*>(myHiggsSideTop->mother());
    }
    if (!myHiggsSideTop)
      return false;
    std::cout << "FullMass: Higgs side top selected " << std::endl;
    // Look at Higgs side top daughters to find b jet
    reco::Candidate* myHiggsSideBJet = 0;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (TMath::Abs(p.pdgId()) == 5) {
        myStatus = true;
        reco::Candidate* myBMother = const_cast<reco::Candidate*>(p.mother());
        while (myStatus) {
          if (!myBMother) {
            myStatus = false;
          } else {
            std::cout << "FullMass: B quark mother = " << myBMother->pdgId() << std::endl;
            if (TMath::Abs(myBMother->pdgId()) == 6) {
              myStatus = false;
              double myDeltaR = ROOT::Math::VectorUtil::DeltaR(myBMother->p4(), myHiggsSideTop->p4());
              if (myDeltaR < 0.01) {
                myHiggsSideBJet = const_cast<reco::Candidate*>(&p);
                i = genParticles->size();
              }
            }
            if (myStatus)
              myBMother = const_cast<reco::Candidate*>(myBMother->mother());
          }
        }
      }
    }
    if (!myHiggsSideBJet) return false;
    std::cout << "FullMass: Higgs side bjet found, pt=" << myHiggsSideBJet->pt() << ", eta=" << myHiggsSideBJet->eta() << std::endl;
    // Look if tau decays into one prong (hadronic)
    reco::Candidate* myTauFromHiggs = 0;
    TVector3 myNeutrinoes(0.0, 0.0, 0.0);
    TVector3 myVisibleTau(0.0, 0.0, 0.0);
    bool myLeptonicTauDecayStatus = false;
    int myChargedCount = 0;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      int myId = TMath::Abs(p.pdgId());
      if ((myId >= 11 && myId <= 16) || myId==211) {
        // Check if tau is coming from H+
        myStatus = true;
        reco::Candidate* myMother = const_cast<reco::Candidate*>(p.mother());
        while (myStatus) {
          if (!myMother) {
            myStatus = false;
          } else {
            int myMotherId = TMath::Abs(myMother->pdgId());
            //std::cout << "FullMass: H+ decay products mother = " << myMother->pdgId() << " line=" << i << std::endl;
            if (myMotherId == 16) {
              myStatus = false; // reject tau neutrinoes on documentation lines from H+ -> tau nu
            } else if ((myMotherId >= 1 && myMotherId <= 6) || myMotherId == 21) {
              myStatus = false;
            } else if (myMotherId == 37) {
              // ancestor is H+
              myStatus = false;
              if (myId == 15) {
                myTauFromHiggs = const_cast<reco::Candidate*>(&p);
                std::cout << "FullMass: tau found" << std::endl;
              } else if (myId == 11 || myId == 13) {
                myLeptonicTauDecayStatus = true;
              } else if (myId == 12 || myId == 14 || myId == 16) {
                myNeutrinoes.SetXYZ(p.px() + myNeutrinoes.X(),
                                    p.py() + myNeutrinoes.Y(),
                                    p.pz() + myNeutrinoes.Z());
                myVisibleTau.SetXYZ(-p.px() + myVisibleTau.X(),
                                    -p.py() + myVisibleTau.Y(),
                                    -p.pz() + myVisibleTau.Z());
              } else if (myId == 211) {
                ++myChargedCount;
              }
            }
            if (myStatus)
              myMother = const_cast<reco::Candidate*>(myMother->mother());
          }
        }
      }
    }
    if (!myTauFromHiggs) return false;
    myVisibleTau.SetXYZ(myVisibleTau.X()+myTauFromHiggs->px(),
                        myVisibleTau.Y()+myTauFromHiggs->py(),
                        myVisibleTau.Z()+myTauFromHiggs->pz());
    std::cout << "FullMass: tau pt=" << myVisibleTau.Perp() << " prongs=" << myChargedCount << " leptonicDecay=" << myLeptonicTauDecayStatus << ", neutrino pt=" << myNeutrinoes.Perp() << std::endl;
    // Make MC matching of bjet
    double myDeltaRBJet = ROOT::Math::VectorUtil::DeltaR(bjet->p4(), myHiggsSideBJet->p4());
    std::cout << "FullMass: bjet deltaR = " << myDeltaRBJet << std::endl;
    if (myDeltaRBJet > 0.4) return false;
    // Make MC matching of tau jet
    double myDeltaRTau = ROOT::Math::VectorUtil::DeltaR(tau->p4(), myTauFromHiggs->p4());
    std::cout << "FullMass: tau deltaR = " << myDeltaRTau << std::endl;
    if (myDeltaRTau > 0.4) return false;
    // Calculate result
    TVector3 myBJetVector(myHiggsSideBJet->px(), myHiggsSideBJet->py(), myHiggsSideBJet->pz());
    doCalculate(myVisibleTau, myBJetVector, myNeutrinoes, true);
    return true;
  }
}
