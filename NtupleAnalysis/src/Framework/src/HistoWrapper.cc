#include "Framework/interface/HistoWrapper.h"
#include "Framework/interface/Exception.h"

#include <iostream>
#include <TROOT.h>


namespace {
  std::string histoLevelNames[static_cast<int>(HistoLevel::kNumberOfLevels)] = {
    "Never",
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
  if (level == "Never") {
    fAmbientLevel = HistoLevel::kNever;
  } else if (level == "Systematics") {
    fAmbientLevel = HistoLevel::kSystematics;
  } else if (level == "Vital") {
    fAmbientLevel = HistoLevel::kVital;
  } else if (level == "Informative") {
    fAmbientLevel = HistoLevel::kInformative;
  } else if (level == "Debug") {
    fAmbientLevel = HistoLevel::kDebug;
  } else {
    throw hplus::Exception("Logic") << "HistoWrapper: Error in ambient histogram level! Valid options are: 'Never', 'Systematics', 'Vital', 'Informative', 'Debug' (you specified: '" << level << "'";
  }
}
HistoWrapper::~HistoWrapper() {
//   printHistoStatistics();
//   std::cout << "gDirectory" << gDirectory->GetList()->GetSize() << std::endl;
//   std::cout << "list " << gROOT->GetList()->GetSize() << std::endl;
//   std::cout << "globals " << gROOT->GetListOfGlobals()->GetSize() << std::endl;
//   std::cout << "files" << gROOT->GetListOfFiles()->GetSize() << std::endl;
//   std::cout << "specials " << gROOT->GetListOfSpecials()->GetSize() << std::endl;
  //gDirectory->GetList()->Delete();
//   gROOT->GetList()->Delete();
//   gROOT->GetListOfGlobals()->Delete();
//   TIter next(gROOT->GetList());
//   while (TObject* o = dynamic_cast<TObject*>(next())) {
//     o->Delete();
//   }
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
