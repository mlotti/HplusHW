#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FullHiggsMassCalculator.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "Math/GenVector/VectorUtil.h"
#include "TLorentzVector.h"
#include "TVector3.h"
#include "TMath.h"




namespace HPlus {
  FullHiggsMassCalculator::Data::Data() :
  fPassedEvent(false),
  fTopMassSolution(0),
  fNeutrinoZSolution(0),
  fNeutrinoPtSolution(0),
  fHiggsMassSolution(0),
  fMCNeutrinoPz(0) { }
  FullHiggsMassCalculator::Data::~Data() { }

  FullHiggsMassCalculator::FullHiggsMassCalculator(HPlus::EventCounter& eventCounter, HPlus::HistoWrapper& histoWrapper):
    BaseSelection(eventCounter, histoWrapper),
    fAllSolutionsCutSubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "All solutions")),
    fRealDiscriminantCutSubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Real Discriminant")),
    fImaginarySolutionCutSubCount(eventCounter.addSubCounter("FullHiggsMassCalculator", "Imaginary solution"))
{
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("FullHiggsMass");
    hHiggsMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMass", "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassDPz100 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassDPz100", "Higgs massDPz100;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_TauBmatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassTauBmatch", "Higgs massTauBmatch;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMass_TauBMETmatch = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassTauBMETmatch", "Higgs massTauBMETmatch;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassReal = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassReal", "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hHiggsMassImaginary = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsMassImaginary", "Higgs mass;m_{H^{+}} (GeV)", 100, 0, 500);
    hTopMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMass", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassRejected = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMassRejected", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassReal = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMassReal", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassRealRejected = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMassRealRejected", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassImaginary = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMassImaginary", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hTopMassImaginaryRejected = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "TopMassImaginaryRejected", "Top mass;m_{top} (GeV)", 100, 0, 500);
    hNeutrinoZSolution = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NeutrinoZSolution", "Neutrino Z solution;p_{#nu,z} (GeV)", 100, -500, 500);
    hNeutrinoPtSolution = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NeutrinoPtSolution", "Neutrino pT solution;p_{#nu,T} (GeV)", 100, 0, 500);
    hNeutrinoPtDifference = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "NeutrinoPtDifference", "Neutrino pT difference;p_{#nu,T} (GeV)", 200, -500, 500);
    hSolution1PzDifference = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SolutionMinPzDifference", "Neutrino/MinSolution pz difference;(GeV)", 200, 0, 1000);
    hSolution2PzDifference = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "SolutionMaxPzDifference", "Neutrino/MaxSolution pz difference;(GeV)", 200, 0, 1000);

    hSolution12PzDifference = histoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myDir, "MinSolution", "MaxSolution ", 100, 0, 1000, 100, 0, 1000);
      //edm::FileInPath myDataPUdistribution = iConfig.getParameter<edm::FileInPath>("dataPUdistribution");
  }
  FullHiggsMassCalculator::~FullHiggsMassCalculator() {}

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::silentAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData) {
    ensureSilentAnalyzeAllowed(iEvent);

    // Disable histogram filling and counter incrementinguntil the return call
    // The destructor of HistoWrapper::TemporaryDisabler will re-enable filling and incrementing
    HistoWrapper::TemporaryDisabler histoTmpDisabled = fHistoWrapper.disableTemporarily();
    EventCounter::TemporaryDisabler counterTmpDisabled = fEventCounter.disableTemporarily();

    return privateAnalyze(iEvent, iSetup, tauData, bData, metData);
  }

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData) {
    ensureAnalyzeAllowed(iEvent);
    return privateAnalyze(iEvent, iSetup, tauData, bData, metData);
  }

  FullHiggsMassCalculator::Data FullHiggsMassCalculator::privateAnalyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data tauData, const BTagging::Data bData, const METSelection::Data metData) {
    Data output;
    // 1) find b-jet

    TVector3 myBJetVector;
    double myMinDeltaR = 99.0;
    edm::Ptr<pat::Jet> myBJet;
    // Loop over bjets with tight tag
    for (edm::PtrVector<pat::Jet>::iterator iBjet = bData.getSelectedJets().begin(); iBjet != bData.getSelectedJets().end(); ++iBjet) {
      //      double DeltaJet = ROOT::Math::VectorUtil::DeltaR((*iBjet)->p4(), TopChiSelectionData.getSelectedBjet()->p4());
      //      if (DeltaJet < 0.001) continue;
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR((*iBjet)->p4(), tauData.getSelectedTau()->p4());
      if (myDeltaR < myMinDeltaR) {
        myMinDeltaR = myDeltaR;
        myBJet = *iBjet;
        output.BjetHiggsSide = *iBjet;
        myBJetVector.SetXYZ((*iBjet)->px(), (*iBjet)->py(), (*iBjet)->pz());
      }
    }
    // Loop over bjets with looser tag
    for (edm::PtrVector<pat::Jet>::iterator iBjet = bData.getSelectedSubLeadingJets().begin(); iBjet != bData.getSelectedSubLeadingJets().end(); ++iBjet) {
      double myDeltaR = ROOT::Math::VectorUtil::DeltaR((*iBjet)->p4(), tauData.getSelectedTau()->p4());
      if (myDeltaR < myMinDeltaR) {
        myMinDeltaR = myDeltaR;
        myBJet = *iBjet;
        myBJetVector.SetXYZ((*iBjet)->px(), (*iBjet)->py(), (*iBjet)->pz());
      }
    }
    //    std::cout << "B jet in Higgs mass:  myMinDeltaR " << myMinDeltaR  << " pt " << myBJet->pt() << " eta  " << myBJet->eta() << std::endl;


    // match in MC to see if it was the correct one
    bool myMatchStatus = false;
    if (!iEvent.isRealData())
      myMatchStatus = doMCMatching(iEvent, tauData.getSelectedTau(), myBJet, output);

    // 2) set tau and MET info
    TVector3 myTauVector(tauData.getSelectedTau()->px(), tauData.getSelectedTau()->py(), tauData.getSelectedTau()->pz());
    TVector3 myMETVector(metData.getSelectedMET()->px(), metData.getSelectedMET()->py(), metData.getSelectedMET()->pz());

    // 3) calculate
    doCalculate(myTauVector, myBJetVector, myMETVector, output, myMatchStatus);

    // Return data object
    output.fPassedEvent = true; // for now, later implement possibility to cut
    return output;
  }



  void FullHiggsMassCalculator::doCalculate(TVector3& tau, TVector3& bjet, TVector3& met, FullHiggsMassCalculator::Data& output, bool myMatchStatus,  bool doHistogramming) {
    // Initialise
    const double myTauMass = 1.778;
    const double myTopMass = 173.4;
    const double myBQuarkMass = 4.19;
    TVector3 myTauPlusBVector = tau + bjet;
    double SolutionMax = -1;
    double deltaNeutrinoZSolution = -999;

    double myDeltaSquared = TMath::Power(myTopMass,2) - TMath::Power(myTauMass,2) - TMath::Power(myBQuarkMass,2);
    //    double a = 2.0 * (met.X() * myTauPlusBVector.X() + met.Y() * myTauPlusBVector.Y()) + myDeltaSquared;

   
    double a = 2.0 * (met.X() * myTauPlusBVector.X() + met.Y() * myTauPlusBVector.Y() + tau.X()*bjet.X() + tau.Y()*bjet.Y()+ tau.Z()*bjet.Z() - TMath::Sqrt(TMath::Power(tau.Mag(),2)+TMath::Power(myTauMass,2))*TMath::Sqrt(TMath::Power(bjet.Mag(),2)+TMath::Power(myBQuarkMass,2)))  + myDeltaSquared;


    double myTauPlusBEnergy = TMath::Sqrt(TMath::Power(myTauPlusBVector.Mag(),2)+TMath::Power(myTauMass+myBQuarkMass,2));
    double discriminant = TMath::Power(a,2) + 4.0 * TMath::Power(myTauPlusBVector.Z(),2) * TMath::Power(met.Perp(),2)
      - 4.0 * TMath::Power(met.Perp(),2) * (TMath::Power(myTauPlusBEnergy,2));

    /*std::cout << "tau+b:, " << myTauPlusBVector.X() << ", " << myTauPlusBVector.Y() << ", " << myTauPlusBVector.Z() << std::endl;
    std::cout << "tau:, " << tau.X() << ", " << tau.Y() << ", " << tau.Z() << std::endl;
    std::cout << "bjet:, " << bjet.X() << ", " << bjet.Y() << ", " << bjet.Z() << std::endl;
    std::cout << "MET:, " << met.X() << ", " << met.Y() << ", " << met.Z() << std::endl;
    std::cout << "DeltaSquared, " << myDeltaSquared << std::endl;
    std::cout << "a, " << a << std::endl;
    std::cout << "tau+b energy, " << myTauPlusBEnergy << std::endl;
    std::cout << "discriminant, " << discriminant << std::endl;
    */
    increment(fAllSolutionsCutSubCount);
    if (discriminant > 0.0) {
      increment(fRealDiscriminantCutSubCount);
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

      //std::cout << "real solution, nu_Z, " << mySolution1 << ", " << mySolution2 << ", mc z, " << met.Z() << std::endl;
      //std::cout << "real solution, mtop, " << myTopMassSolution1 << ", " << myTopMassSolution2 << std::endl;

      output.fNeutrinoZSolution = mySolution1;
      SolutionMax = mySolution2;
      output.fTopMassSolution = myTopMassSolution1;

      if (TMath::Abs(mySolution2) <  TMath::Abs(mySolution1)) {      
	//      if (TMath::Abs(myTopMassSolution2 - myTopMass) < TMath::Abs(myTopMassSolution1 - myTopMass)) {
        output.fNeutrinoZSolution = mySolution2;
	SolutionMax = mySolution1;
        output.fTopMassSolution = myTopMassSolution2;
        if (doHistogramming)
          hTopMassRealRejected->Fill(myTopMassSolution1);
      } else {
        if (doHistogramming)
          hTopMassRealRejected->Fill(myTopMassSolution2);
      }
 

      double deltaPzMin = TMath::Abs(output.fMCNeutrinoPz - output.fNeutrinoZSolution);
      double deltaPzMax = TMath::Abs(output.fMCNeutrinoPz - SolutionMax);
      deltaNeutrinoZSolution = deltaPzMin;

      hSolution1PzDifference->Fill(deltaPzMin);
      hSolution2PzDifference->Fill(deltaPzMax);

    
      // Calculate Higgs boson mass
      double myNeutrinoEnergy = TMath::Sqrt(TMath::Power(met.Perp(),2) + TMath::Power(output.fNeutrinoZSolution,2));
      output.fHiggsMassSolution = TMath::Sqrt(TMath::Power(myTauMass,2)
        + 2.0 * TMath::Sqrt(TMath::Power(tau.Mag(),2) + TMath::Power(myTauMass,2)) * myNeutrinoEnergy
        - 2.0 * (tau.X()*met.X() + tau.Y()*met.Y() + tau.Z()*output.fNeutrinoZSolution));
      /*     
      // test
      double myNeutrinoEnergy1 = TMath::Sqrt(TMath::Power(met.Perp(),2) + TMath::Power(mySolution1,2));
      output.fHiggsMassSolution = TMath::Sqrt(TMath::Power(myTauMass,2)
        + 2.0 * TMath::Sqrt(TMath::Power(tau.Mag(),2) + TMath::Power(myTauMass,2)) * myNeutrinoEnergy1
        - 2.0 * (tau.X()*met.X() + tau.Y()*met.Y() + tau.Z()*mySolution1));
      double myNeutrinoEnergy2 = TMath::Sqrt(TMath::Power(met.Perp(),2) + TMath::Power(mySolution2,2));
      output.fHiggsMassSolution2 = TMath::Sqrt(TMath::Power(myTauMass,2)
        + 2.0 * TMath::Sqrt(TMath::Power(tau.Mag(),2) + TMath::Power(myTauMass,2)) * myNeutrinoEnergy2
        - 2.0 * (tau.X()*met.X() + tau.Y()*met.Y() + tau.Z()*mySolution2));
      */

    } else {
      increment(fImaginarySolutionCutSubCount);
      // Two imaginary solutions exist; take real solutions as solution for neutrino Z and solve neutrino pT from discriminant = 0 equation
      output.fNeutrinoZSolution = (-a*myTauPlusBVector.Z())
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
        + 2.0 * TMath::Sqrt(TMath::Power(mySolution1,2) + TMath::Power(output.fNeutrinoZSolution,2)) * myTauPlusBEnergy
        - 2.0 * (alpha * mySolution1 + myTauPlusBVector.Z() * output.fNeutrinoZSolution));
      double myTopMassSolution2 = TMath::Sqrt(TMath::Power(myTauMass,2)+TMath::Power(myBQuarkMass,2)
        + 2.0 * TMath::Sqrt(TMath::Power(mySolution2,2) + TMath::Power(output.fNeutrinoZSolution,2)) * myTauPlusBEnergy
        - 2.0 * (alpha * mySolution2 + myTauPlusBVector.Z() * output.fNeutrinoZSolution));

      //std::cout << "imag solution, nu_Z/alpha/nu_T, " << output.fNeutrinoZSolution << ", " << alpha << ", " << mySolution1 << ", " << mySolution2 << ", mc z, " << met.Z() << ", mc pt, " << met.Perp() << std::endl;
      //std::cout << "imag solution, mtop, " << myTopMassSolution1 << ", " << myTopMassSolution2 << std::endl;

      output.fNeutrinoPtSolution = mySolution1;
      output.fTopMassSolution = myTopMassSolution1;
      if (TMath::Abs(myTopMassSolution2 - myTopMass) < TMath::Abs(myTopMassSolution1 - myTopMass)) {
        output.fNeutrinoPtSolution = mySolution2;
        output.fTopMassSolution = myTopMassSolution2;
        if (doHistogramming)
          hTopMassImaginaryRejected->Fill(myTopMassSolution1);
      } else {
        if (doHistogramming)
          hTopMassImaginaryRejected->Fill(myTopMassSolution2);
      }
      // Calculate Higgs boson mass
      double alphaPrime = (tau.X() * met.X() + tau.Y() * met.Y()) / met.Perp();
      double myNeutrinoEnergy = TMath::Sqrt(TMath::Power(output.fNeutrinoPtSolution,2) + TMath::Power(output.fNeutrinoZSolution,2));
      output.fHiggsMassSolution = TMath::Sqrt(TMath::Power(myTauMass,2)
        + 2.0 * TMath::Sqrt(TMath::Power(tau.Mag(),2) + TMath::Power(myTauMass,2)) * myNeutrinoEnergy
        - 2.0 * alphaPrime * output.fNeutrinoPtSolution);

      //std::cout << "alpha prime/Enu, " << alphaPrime << ", " << myNeutrinoEnergy << std::endl;

    }
    // Fill top mass histograms
    if (doHistogramming) {
      hTopMass->Fill(output.fTopMassSolution);
      if (discriminant >= 0.0) {
        hTopMassReal->Fill(output.fTopMassSolution);
      } else {
        hTopMassImaginary->Fill(output.fTopMassSolution);
      }
    }
    // Fill neutrino histograms
    if (doHistogramming) {
      hNeutrinoZSolution->Fill(output.fNeutrinoZSolution);
      if (output.fNeutrinoPtSolution > 0.0) {
        hNeutrinoPtSolution->Fill(output.fNeutrinoPtSolution);
        hNeutrinoPtDifference->Fill(output.fNeutrinoPtSolution-met.Perp());
      }
    }

    //std::cout << "mHiggs, " << output.fHiggsMassSolution << std::endl;
    // transverse neutrino matching
    double DeltaPhi = (output.mcNeutrinos.X() * met.X() + output.mcNeutrinos.Y() * met.Y()) / output.mcNeutrinos.Perp()/ met.Perp();


    if (doHistogramming) {
      hHiggsMass->Fill(output.fHiggsMassSolution);
      if (deltaNeutrinoZSolution < 50) hHiggsMassDPz100->Fill(output.fHiggsMassSolution);
      if ( myMatchStatus) hHiggsMass_TauBmatch->Fill(output.fHiggsMassSolution);
      if ( myMatchStatus && DeltaPhi < 0.4) hHiggsMass_TauBMETmatch->Fill(output.fHiggsMassSolution);
  
      if (discriminant >= 0.0) {
        hHiggsMassReal->Fill(output.fHiggsMassSolution);
      } else {
        hHiggsMassImaginary->Fill(output.fHiggsMassSolution);
      }
    }
  }






  bool FullHiggsMassCalculator::doMCMatching(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& tau, const edm::Ptr<pat::Jet>& bjet, FullHiggsMassCalculator::Data& output) {
    edm::Handle <reco::GenParticleCollection> genParticles;
    iEvent.getByLabel("genParticles", genParticles);
    // Find last Hplus line
    size_t myHiggsLine = 0;
    for (size_t i=0; i < genParticles->size(); ++i) {
      const reco::Candidate & p = (*genParticles)[i];
      if (TMath::Abs(p.pdgId()) == 37)
        myHiggsLine = i;
    }

    //std::cout << "FullMass: Higgs line " << myHiggsLine << std::endl;

    if (!myHiggsLine) return false;
    // Find top, from which Higgs comes from
    reco::Candidate* myHiggsSideTop = const_cast<reco::Candidate*>(genParticles->at(myHiggsLine).mother());
    bool myStatus = true;
    while (myStatus) {

//      if (!myHiggsSideTop) myStatus = false;
      if (!myHiggsSideTop)
        return false;


      //std::cout << "FullMass: Higgs side mother = " << myHiggsSideTop->pdgId() << std::endl;

      if (TMath::Abs(myHiggsSideTop->pdgId()) == 6) myStatus = false;
      if (myStatus)
        myHiggsSideTop = const_cast<reco::Candidate*>(myHiggsSideTop->mother());
    }
    if (!myHiggsSideTop)
      return false;

    //std::cout << "FullMass: Higgs side top selected " << std::endl;
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

            //std::cout << "FullMass: B quark mother = " << myBMother->pdgId() << std::endl;

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

    //std::cout << "FullMass: Higgs side bjet found, pt=" << myHiggsSideBJet->pt() << ", eta=" << myHiggsSideBJet->eta() << std::endl;

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

                //std::cout << "FullMass: tau found" << std::endl;

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
    output.visibleTau =  myVisibleTau;
    output.mcNeutrinos = myNeutrinoes;
    output.fMCNeutrinoPz =  myNeutrinoes.Pz();
    output.mcBjetHiggsSide.SetXYZ(myHiggsSideBJet->p4().px(),myHiggsSideBJet->p4().py(),myHiggsSideBJet->p4().pz());

    //    std::cout << "FullMass: tau pt=" << myVisibleTau.Perp() << " prongs=" << myChargedCount << " leptonicDecay=" << myLeptonicTauDecayStatus << ", neutrino pt=" << myNeutrinoes.Perp() << std::endl;
    // Make MC matching of bjet
    double myDeltaRBJet = ROOT::Math::VectorUtil::DeltaR(bjet->p4(), myHiggsSideBJet->p4());

    //    std::cout << "FullMass: bjet deltaR = " << myDeltaRBJet << std::endl;
    if (myDeltaRBJet > 0.4) return false;
    // Make MC matching of tau jet
    double myDeltaRTau = ROOT::Math::VectorUtil::DeltaR(tau->p4(), myTauFromHiggs->p4());
    //    std::cout << "FullMass: tau deltaR = " << myDeltaRTau << std::endl;
    if (myDeltaRTau > 0.4) return false;

    // Calculate result
    TVector3 myBJetVector(myHiggsSideBJet->px(), myHiggsSideBJet->py(), myHiggsSideBJet->pz());
    //    doCalculate(myVisibleTau, myBJetVector, myNeutrinoes, true);

    return true;
  }
}
