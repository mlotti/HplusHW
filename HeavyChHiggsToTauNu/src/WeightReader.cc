#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/WeightReader.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  WeightReader::WeightReader(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper, const std::string& directory):
    fWeightSrc(iConfig.getParameter<edm::InputTag>("weightSrc")),
    fEnabled(iConfig.getParameter<bool>("enabled")) {

    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir(directory);
    hWeightsLow = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Weight_Low_part", "Weight_Low_part;Weight;N_{events} / 0.1", 100, 0., 10.);
    hWeightsMedium = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Weight_Medium_part", "Weight_Medium_part;Weight;N_{events} / 1", 100, 0., 100.);
    hWeightsHigh = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Weight_High_part", "Weight_High_part;Weight;N_{events} / 50", 200, 0., 10000.);
    hWeightsVeryHigh = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "Weight_VeryHigh_part", "Weight_VeryHigh_part;Weight;N_{events} / 1", 200, 0., 1000000.);
  }
  WeightReader::~WeightReader() {}

  double WeightReader::getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    double weight = 1.0;
    if(fEnabled) {
      edm::Handle<double> hweight;
      iEvent.getByLabel(fWeightSrc, hweight);
      weight = *hweight;
    }

    // Fill without weighting (= weight 1.0), since that's more
    // relevant for these monitoring histograms
    hWeightsLow->Fill(weight, 1.0);
    hWeightsMedium->Fill(weight, 1.0);
    hWeightsHigh->Fill(weight, 1.0);
    hWeightsVeryHigh->Fill(weight, 1.0);

    return weight;
  }
}
