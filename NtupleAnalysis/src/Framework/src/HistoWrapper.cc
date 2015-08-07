#include "Framework/interface/HistoWrapper.h"

#include <iostream>

namespace {
  std::string histoLevelNames[static_cast<int>(HistoLevel::kNumberOfLevels)] = {
    "Systematics",
    "Vital",
    "Informative",
    "Debug"
  };
}

HistoWrapper::HistoWrapper(const EventWeight& eventWeight, const std::string& level):
  fEventWeight(eventWeight),
  fIsEnabled(true)
{ 
  for(int i=0; i<static_cast<int>(HistoLevel::kNumberOfLevels); ++i)
    fHistoLevelStats[i] = 0;

  // Find level from string
  if (level == "Systematics") {
    fAmbientLevel = HistoLevel::kSystematics;
  } else if (level == "Vital") {
    fAmbientLevel = HistoLevel::kVital;
  } else if (level == "Informative") {
    fAmbientLevel = HistoLevel::kInformative;
  } else if (level == "Debug") {
    fAmbientLevel = HistoLevel::kDebug;
  } else {
    throw std::logic_error("HistoWrapper: Error in ambient histogram level! Valid options are: 'Systematics', 'Vital', 'Informative', 'Debug' (you specified: '"+level+"'");
  }
}
HistoWrapper::~HistoWrapper() {
}

void HistoWrapper::printHistoStatistics() const {
  std::cout << "HistoWrapper:" << std::endl;
  int total = 0;
  for(int i=0; i<static_cast<int>(HistoLevel::kNumberOfLevels); ++i) {
    std::cout << "  Level " << histoLevelNames[i] << " (" << i << ") " << fHistoLevelStats[i] << " histograms" << std::endl;
    total += fHistoLevelStats[i];
  }
  std::cout << "  Total " << total << " histograms booked" << std::endl;
}

// Do not destroy histogram objects (they are owned by the root file)
WrappedTH1::~WrappedTH1() { }
WrappedTH2::~WrappedTH2() { }
WrappedTH3::~WrappedTH3() { }
WrappedUnfoldedFactorisationHisto::~WrappedUnfoldedFactorisationHisto() { }
