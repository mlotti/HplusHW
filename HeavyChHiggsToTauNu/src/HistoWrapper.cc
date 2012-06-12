#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

namespace HPlus {
  
  HistoWrapper::HistoWrapper(EventWeight& eventWeight, std::string level)
  : fEventWeight(eventWeight) { 
    // Find level from string
    if (level == "Vital") {
      fAmbientLevel = kVital;
    } else if (level == "Informative") {
      fAmbientLevel = kInformative;
    } else if (level == "Debug") {
      fAmbientLevel = kDebug;
    } else {
      throw cms::Exception("config") << "HistoWrapper: Error in ambient histogram level! Valid options are: 'Vital', 'Informative', 'Debug' (you specified: '" << level << "'";
    }
  }
  HistoWrapper::~HistoWrapper() {
    // Do not destroy histogram objects (they are owned by the root file)
    for (std::vector<WrappedTH1*>::iterator it = fAllTH1Histos.begin(); it != fAllTH1Histos.end(); ++it)
      delete *it;
    for (std::vector<WrappedTH2*>::iterator it = fAllTH2Histos.begin(); it != fAllTH2Histos.end(); ++it)
      delete *it;
  }

  WrappedTH1::WrappedTH1(EventWeight& eventWeight, TH1* histo, bool isActive)
  : fEventWeight(eventWeight),
  h(histo),
  bIsActive(isActive) { }

  WrappedTH1::~WrappedTH1() { }

  WrappedTH2::WrappedTH2(EventWeight& eventWeight, TH2* histo, bool isActive)
  : fEventWeight(eventWeight),
  h(histo),
  bIsActive(isActive) { }

  WrappedTH2::~WrappedTH2() { }

}