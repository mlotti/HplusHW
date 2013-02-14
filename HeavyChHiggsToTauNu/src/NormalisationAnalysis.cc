// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/NormalisationAnalysis.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {

  NormalisationAnalysis::NormalisationAnalysis(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper) :
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper) {
      createHistograms();
  }

  NormalisationAnalysis::NormalisationAnalysis(EventCounter& eventCounter, HistoWrapper& histoWrapper) :
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper) {
      createHistograms();
  }

  void NormalisationAnalysis::createHistograms() {
    edm::Service<TFileService> fs;
    TFileDirectory myBaseDir = fs->mkdir("NormalisationAnalysis");

    // Create histograms
    // e -> tau fakes
    TFileDirectory myEtoTauDir = myBaseDir.mkdir("eToTau");
    hEtoTauZmassAll = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_mZ_all", "etotau_mZ_all;m_{ee} / GeV/c^{2};N_{events}", 100, 0, 500);
    hEtoTauZmassDecayMode0 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_mZ_decayMode0", "etotau_mZ_decayMode0;m_{ee} / GeV/c^{2};N_{events}", 100, 0, 500);
    hEtoTauZmassDecayMode1 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_mZ_decayMode1", "etotau_mZ_decayMode1;m_{ee} / GeV/c^{2};N_{events}", 100, 0, 500);
    hEtoTauZmassDecayMode2 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_mZ_decayMode2", "etotau_mZ_decayMode2;m_{ee} / GeV/c^{2};N_{events}", 100, 0, 500);
    hEtoTauTauPtAll = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_taupT_all", "etotau_tauPt_all;#tau p_{T} / GeV/c;N_{events}", 100, 0, 500);
    hEtoTauTauPtDecayMode0 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_taupT_decayMode0", "etotau_tauPt_decayMode0;#tau p_{T} / GeV/c;N_{events}", 100, 0, 500);
    hEtoTauTauPtDecayMode1 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_taupT_decayMode1", "etotau_tauPt_decayMode1;#tau p_{T} / GeV/c;N_{events}", 100, 0, 500);
    hEtoTauTauPtDecayMode2 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_taupT_decayMode2", "etotau_tauPt_decayMode2;#tau p_{T} / GeV/c;N_{events}", 100, 0, 500);
  }

  NormalisationAnalysis::~NormalisationAnalysis() {}

  void NormalisationAnalysis::analyseEToTauFakes(const VertexSelection::Data& vertexData,
                                                 const TauSelection::Data& tauData,
                                                 const FakeTauIdentifier::Data& fakeTauData,
                                                 const ElectronSelection::Data& electronData) {
    // Make sure vertex has been found
    if (!vertexData.passedEvent()) return;
    // Make sure tau has been found
    if (!tauData.passedEvent()) return;
    // Find one electron that is not compatible with tau
    edm::Ptr<pat::Electron> myElectron;
    int myElectronCount = 0;
    edm::PtrVector<pat::Electron> myElectrons = electronData.getSelectedElectronsTight();
    for (edm::PtrVector<pat::Electron>::iterator i = myElectrons.begin(); i != myElectrons.end(); ++i) {
      double myDeltaR = reco::deltaR(tauData.getSelectedTau()->p4(), (*i)->p4());
      if (myDeltaR > 0.4) {
        ++myElectronCount;
        myElectron = *i;
      }
    }
    if (myElectronCount != 1) return;
    // TODO: if purity is not sufficient, then consider adding b jet veto
    // Calculate Z mass
    LorentzVector myZCandidate;
    myZCandidate += tauData.getSelectedTau()->p4();
    myZCandidate += myElectron->p4();
    double myZCandidateMass = myZCandidate.M();
    // Fill histograms
    hEtoTauZmassAll->Fill(myZCandidateMass);
    if (tauData.getSelectedTau()->decayMode() == 0) {
      hEtoTauZmassDecayMode0->Fill(myZCandidateMass);
    } else if (tauData.getSelectedTau()->decayMode() == 1) {
      hEtoTauZmassDecayMode1->Fill(myZCandidateMass);
    } else if (tauData.getSelectedTau()->decayMode() == 2) {
      hEtoTauZmassDecayMode2->Fill(myZCandidateMass);
    }
    // Select events with Z mass
    if (!(myZCandidateMass > 70 && myZCandidateMass < 100)) return;
    double myTauPt = tauData.getSelectedTau()->pt();
    hEtoTauTauPtAll->Fill(myTauPt);
    if (tauData.getSelectedTau()->decayMode() == 0) {
      hEtoTauTauPtDecayMode0->Fill(myTauPt);
    } else if (tauData.getSelectedTau()->decayMode() == 1) {
      hEtoTauTauPtDecayMode1->Fill(myTauPt);
    } else if (tauData.getSelectedTau()->decayMode() == 2) {
      hEtoTauTauPtDecayMode2->Fill(myTauPt);
    }
  }
}