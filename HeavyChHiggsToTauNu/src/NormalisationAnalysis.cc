// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NormalisationAnalysis.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {

  NormalisationAnalysis::NormalisationAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string label) :
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper) {
      createCommonHistograms(label);
  }

  NormalisationAnalysis::NormalisationAnalysis(EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string label) :
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper) {
      createCommonHistograms(label);
  }

  void NormalisationAnalysis::createCommonHistograms(std::string label) {
    edm::Service<TFileService> fs;
    TFileDirectory myBaseDir = fs->mkdir("NormalisationAnalysis");
    TFileDirectory myDir = myBaseDir.mkdir(label.c_str());
    fMyDir += "NormalisationAnalysis/";
    fMyDir += label;

    hTauPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "tauPt", "tauPt;tau p_{T} / GeV/c;N_{events}", 50, 0, 500);
    hNJets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "nJets", "nJets;N_{jets};N_{events}", 20, 0, 20);
    hMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "met", "met;E_{T}^{miss.} / GeV;N_{events}", 50, 0, 500);
    hMETphi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "metPhi", "metPhi;E_{T}^{miss.} #phi;N_{events}", 18, -3.1415926, 3.1415926);
    hNBJets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "nBJets", "nBJets;N_{b jets};N_{events}", 20, 0, 20);
    hTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "transverseMass", "transverseMass;m_{T} / GeV/c^{2};N_{events}", 50, 0, 500);
    hZMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "zMass", "zMass;m_{Z} / GeV/c^{2};N_{events}", 30, 0, 300);

    hFakeTauTauPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "fakeTauTauPt", "fakeTauTauPt;tau p_{T} / GeV/c;N_{events}", 50, 0, 500);
    hFakeTauNJets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "fakeTauNJets", "fakeTauNJets;N_{jets};N_{events}", 20, 0, 20);
    hFakeTauMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "fakeTauMet", "fakeTauMet;E_{T}^{miss.} / GeV;N_{events}", 50, 0, 500);
    hFakeTauMETphi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "fakeTauMetPhi", "fakeTauMetPhi;E_{T}^{miss.} #phi;N_{events}", 18, -3.1415926, 3.1415926);
    hFakeTauNBJets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "fakeTauNBJets", "fakeTauNBJets;N_{b jets};N_{events}", 20, 0, 20);
    hFakeTauTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "fakeTauTransverseMass", "fakeTauTransverseMass;m_{T} / GeV/c^{2};N_{events}", 50, 0, 500);
    hFakeTauZMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "fakeTauZMass", "fakeTauZMass;m_{Z} / GeV/c^{2};N_{events}", 30, 0, 300);
  }

  NormalisationAnalysis::~NormalisationAnalysis() {}

  void NormalisationAnalysis::analyse(const edm::Event& iEvent,
                                      const TauSelection::Data& tauData,
                                      const FakeTauIdentifier::Data& fakeTauData,
                                      const ElectronSelection::Data& electronData,
                                      const MuonSelection::Data& muonData,
                                      const JetSelection::Data& jetData,
                                      METTriggerEfficiencyScaleFactor* metTrgSF,
                                      const QCDTailKiller::Data& tailKillerData,
                                      const METSelection::Data& metData,
                                      const BTagging::Data& btagData) { }

  void NormalisationAnalysis::createHistogramsAndCounters() { }

}