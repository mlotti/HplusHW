#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EmbeddingMuonEfficiency.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include <limits>
#include <cmath>

namespace HPlus {
  EmbeddingMuonEfficiency::Data::Data():
    fWeight(std::numeric_limits<double>::quiet_NaN()),
    fWeightAbsUnc(1.0) {}
  EmbeddingMuonEfficiency::Data::~Data() {}
  void EmbeddingMuonEfficiency::Data::check() const {
    if(isnan(fWeight))
      throw cms::Exception("Assert") << "EmbeddingMuonEfficiency::Data: This Data object was constructed with the default constructor, not with EmbeddingMuonEfficiency::applyEventWeight(). There is something wrong in your code." << std::endl;
  }

  EmbeddingMuonEfficiency::EmbeddingMuonEfficiency(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper)
    //fMuonSrc(iConfig.getParameter<edm::InputTag>("muonSrc"))
  {
    std::string mode = iConfig.getParameter<std::string>("mode");
    if     (mode == "efficiency") fMode = kEfficiency;
    else if(mode == "disabled")   fMode = kDisabled;
    else throw cms::Exception("Configuration") << "EmbeddingMuonEfficiency: Unsupported value for parameter 'mode' " << mode << ", should be 'efficiency', or 'disabled'" << std::endl;

    if(fMode == kDisabled)
      return;

    edm::ParameterSet dataParameters = iConfig.getParameter<edm::ParameterSet>("dataParameters");
    edm::ParameterSet mcParameters = iConfig.getParameter<edm::ParameterSet>("mcParameters");

    // Data Pset names are not relevant, just to have the same syntax as with TriggerEfficiencyScaleFactor
    std::vector<std::string> dataNames = dataParameters.getParameterNames();
    for(std::vector<std::string>::const_iterator iName = dataNames.begin(); iName != dataNames.end(); ++iName) {
      edm::ParameterSet pset = dataParameters.getParameter<edm::ParameterSet>(*iName);

      EffValue ev;
      ev.firstRun = pset.getParameter<unsigned>("firstRun");
      ev.lastRun = pset.getParameter<unsigned>("lastRun");
      ev.value = pset.getParameter<double>("efficiency");
      ev.uncertainty = pset.getParameter<double>("uncertainty");
      fDataValues.push_back(ev);
    }

    // MC values
    fMCValue = mcParameters.getParameter<double>("efficiency");
    fMCUncertainty = mcParameters.getParameter<double>("uncertainty");
  }
  EmbeddingMuonEfficiency::~EmbeddingMuonEfficiency() {}

  EmbeddingMuonEfficiency::Data EmbeddingMuonEfficiency::applyEventWeight(const edm::Event& iEvent, EventWeight& eventWeight) {
    Data output;
    
    if(fMode == kDisabled)
      return output;

    /* Not needed yet
    // Obtain original muon
    edm::Handle<edm::View<pat::Muon> > hmuon;
    iEvent.getByLabel(fMuonSrc, hmuon);

    if(hmuon->size() != 1)
      throw cms::Exception("Assert") << "Read " << hmuon->size() << " muons for the original muon, expected exactly 1. Muon src was " << fMuonSrc.encode() << std::endl;

    const pat::Muon& originalMuon = hmuon->at(0);
    */
    

    if(iEvent.isRealData()) {
      unsigned run = iEvent.id().run();
      bool found = false;
      size_t foundIndex = 0;
      for(size_t i=0; i<fDataValues.size(); ++i) {
        if(fDataValues[i].firstRun <= run && run <= fDataValues[i].lastRun) {
          found = true;
          foundIndex = i;
          //std::cout << "Index " << i << " firstRun " << fDataValues[i].firstRun << " lastRun " << fDataValues[i].lastRun << " run " << run << " found " << found << std::endl;
          break;
        }
      }
      if(!found)
        throw cms::Exception("Assert") << "EmbeddingMuonEfficiency: encountered run " << run << " which is not included in the configuration" << std::endl;

      output.fWeight = fDataValues[foundIndex].value;
      output.fWeightAbsUnc = fDataValues[foundIndex].uncertainty;
    }
    else {
      output.fWeight = fMCValue;
      output.fWeightAbsUnc = fMCUncertainty;
    }

    // Weight is actually the inverse of the efficiency
    output.fWeightAbsUnc = output.fWeightAbsUnc / (output.fWeight*output.fWeight);
    output.fWeight = 1.0/output.fWeight;

    eventWeight.multiplyWeight(output.fWeight);
    return output;
  }
}
