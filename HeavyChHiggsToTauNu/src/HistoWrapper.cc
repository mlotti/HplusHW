#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include<iostream>

namespace {
  std::string histoLevelNames[HPlus::HistoWrapper::kNumberOfLevels] = {
    "Systematics",
    "Vital",
    "Informative",
    "Debug"
  };
}

namespace HPlus {

  HistoWrapper::HistoWrapper(const EventWeight& eventWeight, std::string level):
    fEventWeight(eventWeight),
    fIsEnabled(true)
  { 
    for(int i=0; i<kNumberOfLevels; ++i)
      fHistoLevelStats[i] = 0;

    // Find level from string
    if (level == "Systematics") {
      fAmbientLevel = kSystematics;
    } else if (level == "Vital") {
      fAmbientLevel = kVital;
    } else if (level == "Informative") {
      fAmbientLevel = kInformative;
    } else if (level == "Debug") {
      fAmbientLevel = kInformative;
    } else {
      throw cms::Exception("Configuration") << "HistoWrapper: Error in ambient histogram level! Valid options are: 'Systematics', 'Vital', 'Informative', 'Debug' (you specified: '" << level << "'";
    }
  }
  HistoWrapper::~HistoWrapper() {
    // Do not destroy histogram objects (they are owned by the root file)
    for (std::vector<WrappedTH1*>::iterator it = fAllTH1Histos.begin(); it != fAllTH1Histos.end(); ++it)
      delete *it;
    for (std::vector<WrappedTH2*>::iterator it = fAllTH2Histos.begin(); it != fAllTH2Histos.end(); ++it)
      delete *it;
    for (std::vector<WrappedTH3*>::iterator it = fAllTH3Histos.begin(); it != fAllTH3Histos.end(); ++it)
      delete *it;
    for (std::vector<WrappedUnfoldedFactorisationHisto*>::iterator it = fAllUnfoldedFactorisationHistos.begin(); it != fAllUnfoldedFactorisationHistos.end(); ++it)
      delete *it;
  }

  bool HistoWrapper::checkIfDirExists(TDirectory* d, std::string name) const {
    for (int i = 0; i < d->GetNkeys(); ++i) {
      std::string s = d->GetListOfKeys()->At(i)->GetTitle();
      if (s == name)
        return true;
    }
    return false;
  }

  void HistoWrapper::printHistoStatistics() const {
    std::cout << "HistoWrapper:" << std::endl;
    int total = 0;
    for(int i=0; i<kNumberOfLevels; ++i) {
      std::cout << "  Level " << histoLevelNames[i] << " (" << i << ") " << fHistoLevelStats[i] << " histograms" << std::endl;
      total += fHistoLevelStats[i];
    }
    std::cout << "  Total " << total << " histograms booked" << std::endl;
  }

  WrappedTH1::WrappedTH1(HistoWrapper& histoWrapper, TH1* histo, HistoWrapper::HistoLevel level)
  : fHistoWrapper(histoWrapper),
  h(histo),
  fLevel(level) { }

  WrappedTH1::~WrappedTH1() { }

  WrappedTH2::WrappedTH2(HistoWrapper& histoWrapper, TH2* histo, HistoWrapper::HistoLevel level)
  : fHistoWrapper(histoWrapper),
  h(histo),
  fLevel(level) { }

  WrappedTH2::~WrappedTH2() { }

  WrappedTH3::WrappedTH3(HistoWrapper& histoWrapper, TH3* histo, HistoWrapper::HistoLevel level)
  : fHistoWrapper(histoWrapper),
  h(histo),
  fLevel(level) { }

  WrappedTH3::~WrappedTH3() { }

  WrappedUnfoldedFactorisationHisto::WrappedUnfoldedFactorisationHisto(HistoWrapper& histoWrapper, TH2* histo, HistoWrapper::HistoLevel level)
  : fHistoWrapper(histoWrapper),
  h(histo),
  fLevel(level) { }

  WrappedUnfoldedFactorisationHisto::~WrappedUnfoldedFactorisationHisto() { }

}
