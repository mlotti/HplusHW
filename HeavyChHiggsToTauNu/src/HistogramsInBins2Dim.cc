#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistogramsInBins2Dim.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"
#include "TH2F.h"


namespace HPlus {

  HistogramsInBins2Dim::HistogramsInBins2Dim(HPlus::HistoWrapper::HistoLevel level, EventCounter& eventCounter, HistoWrapper& histoWrapper, std::string DirectoryName, std::string HistoName1, std::string HistoName2,  int nbins1, double min1, double max1, int nbins2, double min2, double max2) {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(DirectoryName);
    hInclusive = histoWrapper.makeTH<TH2F>(level, myDir, HistoName1.c_str(), HistoName2.c_str(), nbins1, min1, max1, nbins2, min2, max2);
    h120 = histoWrapper.makeTH<TH2F>(level, myDir,     (HistoName1+"120").c_str(),(HistoName2+"120").c_str(), nbins1, min1, max1, nbins2, min2, max2);
    h100120 = histoWrapper.makeTH<TH2F>(level, myDir, (HistoName1+"100120").c_str(), (HistoName2+"100120").c_str(), nbins1, min1, max1, nbins2, min2, max2);
    h80100 = histoWrapper.makeTH<TH2F>(level, myDir, (HistoName1+"80100").c_str(),(HistoName2+"80100").c_str(), nbins1, min1, max1, nbins2, min2, max2);
    h7080 = histoWrapper.makeTH<TH2F>(level, myDir, (HistoName1+"7080").c_str(), (HistoName2+"7080").c_str(),nbins1, min1, max1, nbins2, min2, max2);
    h6070 = histoWrapper.makeTH<TH2F>(level, myDir, (HistoName1+"6070").c_str(),(HistoName2+"6070").c_str(), nbins1, min1, max1, nbins2, min2, max2);
    h5060 = histoWrapper.makeTH<TH2F>(level, myDir, (HistoName1+"5060").c_str(),(HistoName2+"5060").c_str(), nbins1, min1, max1, nbins2, min2, max2);
    h4050 = histoWrapper.makeTH<TH2F>(level, myDir, (HistoName1+"4050").c_str(),(HistoName2+"4050").c_str(), nbins1, min1, max1, nbins2, min2, max2);
  }
 
  HistogramsInBins2Dim::~HistogramsInBins2Dim() {}

  void HistogramsInBins2Dim::Fill(double selectedTauPt ,double Variable1,double Variable2 ){
    
    hInclusive->Fill( Variable1,Variable2);  
    if ( selectedTauPt > 120  ) h120->Fill(Variable1,Variable2);                              
    if ( selectedTauPt > 100 && selectedTauPt  < 120 ) h100120->Fill(Variable1,Variable2);
    if ( selectedTauPt > 80 && selectedTauPt  < 100  ) h80100->Fill(Variable1,Variable2);
    if ( selectedTauPt > 70 && selectedTauPt  < 80 ) h7080->Fill(Variable1,Variable2);
    if ( selectedTauPt > 60 && selectedTauPt  < 70 ) h6070->Fill(Variable1,Variable2);
    if ( selectedTauPt > 50 && selectedTauPt  < 60 ) h5060->Fill(Variable1,Variable2);
    if ( selectedTauPt > 40 && selectedTauPt  < 50 ) h4050->Fill(Variable1,Variable2);    
  }

  void HistogramsInBins2Dim::Fill(double selectedTauPt, double Variable1, double Variable2, double weight ) {
    hInclusive->Fill( Variable1,Variable2, weight);
    if ( selectedTauPt > 120  ) h120->Fill(Variable1,Variable2, weight);
    if ( selectedTauPt > 100 && selectedTauPt  < 120 ) h100120->Fill(Variable1,Variable2, weight);
    if ( selectedTauPt > 80 && selectedTauPt  < 100  ) h80100->Fill(Variable1,Variable2, weight);
    if ( selectedTauPt > 70 && selectedTauPt  < 80 ) h7080->Fill(Variable1,Variable2, weight);
    if ( selectedTauPt > 60 && selectedTauPt  < 70 ) h6070->Fill(Variable1,Variable2, weight);
    if ( selectedTauPt > 50 && selectedTauPt  < 60 ) h5060->Fill(Variable1,Variable2, weight);
    if ( selectedTauPt > 40 && selectedTauPt  < 50 ) h4050->Fill(Variable1,Variable2, weight);
  }
}
