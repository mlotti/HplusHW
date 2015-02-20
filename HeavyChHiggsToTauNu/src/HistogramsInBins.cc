#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistogramsInBins.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {

  HistogramsInBins::HistogramsInBins(HPlus::HistoWrapper::HistoLevel level, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string DirectoryName ,  std::string HistoName, int nbins, double min, double max) {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(DirectoryName);
    hInclusive = histoWrapper.makeTH<TH1F>(level, myDir, HistoName.c_str(), HistoName.c_str(), nbins, min, max);
    h120 = histoWrapper.makeTH<TH1F>(level, myDir, (HistoName+"120").c_str(), (HistoName+"120").c_str(), nbins, min, max);
    h100120 = histoWrapper.makeTH<TH1F>(level, myDir, (HistoName+"100120").c_str(), (HistoName+"100120").c_str(), nbins, min, max);
    h80100 = histoWrapper.makeTH<TH1F>(level, myDir, (HistoName+"80100").c_str(), (HistoName+"80100").c_str(), nbins, min, max);
    h7080 = histoWrapper.makeTH<TH1F>(level, myDir, (HistoName+"7080").c_str(), (HistoName+"7080").c_str(), nbins, min, max);
    h6070 = histoWrapper.makeTH<TH1F>(level, myDir, (HistoName+"6070").c_str(), (HistoName+"6070").c_str(), nbins, min, max);
    h5060 = histoWrapper.makeTH<TH1F>(level, myDir, (HistoName+"5060").c_str(), (HistoName+"5060").c_str(), nbins, min, max);
    h4050 = histoWrapper.makeTH<TH1F>(level, myDir, (HistoName+"4050").c_str(), (HistoName+"4050").c_str(), nbins, min, max);
  }
 
  HistogramsInBins::~HistogramsInBins() {}

  void HistogramsInBins::Fill(double selectedTauPt ,double Variable ){
    
    hInclusive->Fill( Variable);  
    if ( selectedTauPt > 120  ) h120->Fill(Variable);                              
    if ( selectedTauPt > 100 && selectedTauPt  < 120 ) h100120->Fill(Variable);
    if ( selectedTauPt > 80 && selectedTauPt  < 100  ) h80100->Fill(Variable);
    if ( selectedTauPt > 70 && selectedTauPt  < 80 ) h7080->Fill(Variable);
    if ( selectedTauPt > 60 && selectedTauPt  < 70 ) h6070->Fill(Variable);
    if ( selectedTauPt > 50 && selectedTauPt  < 60 ) h5060->Fill(Variable);
    if ( selectedTauPt > 40 && selectedTauPt  < 50 ) h4050->Fill(Variable);    
  }

  void HistogramsInBins::Fill(double selectedTauPt, double Variable, double weight) {
    hInclusive->Fill(Variable, weight);
    if ( selectedTauPt > 120  ) h120->Fill(Variable, weight);
    if ( selectedTauPt > 100 && selectedTauPt  < 120 ) h100120->Fill(Variable, weight);
    if ( selectedTauPt > 80 && selectedTauPt  < 100  ) h80100->Fill(Variable, weight);
    if ( selectedTauPt > 70 && selectedTauPt  < 80 ) h7080->Fill(Variable, weight);
    if ( selectedTauPt > 60 && selectedTauPt  < 70 ) h6070->Fill(Variable, weight);
    if ( selectedTauPt > 50 && selectedTauPt  < 60 ) h5060->Fill(Variable, weight);
    if ( selectedTauPt > 40 && selectedTauPt  < 50 ) h4050->Fill(Variable, weight);
  }

}
