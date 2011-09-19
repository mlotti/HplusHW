#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/VertexReco/interface/Vertex.h"

#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

namespace HPlus {
  VertexWeight::VertexWeight(const edm::ParameterSet& iConfig):
    fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
    fPuSummarySrc(iConfig.getParameter<edm::InputTag>("puSummarySrc")),
    fMeanShifter(iConfig.getParameter<double>("shiftMeanAmount")),
    fUseSimulatedPileup(iConfig.getParameter<bool>("useSimulatedPileup")),
    fSummer11S4Mode(iConfig.getParameter<bool>("summer11S4Mode")),
    fEnabled(iConfig.getParameter<bool>("enabled")),
    fShiftMean(iConfig.getParameter<bool>("shiftMean"))
  {
    if(fShiftMean && (!fSummer11S4Mode || !fUseSimulatedPileup)) {
      throw cms::Exception("Configuration") << "shiftMean can be used only with the reweighting by simulated PU interactions (not reconstructed vertices), and with Summer11S4 samples" << std::endl;
    }

    if(fUseSimulatedPileup) {
      std::vector<double> mcDist = iConfig.getParameter<std::vector<double> >("mcDist");
      std::vector<double> dataDist = iConfig.getParameter<std::vector<double> >("dataDist");
      std::vector<float> mcDistF; mcDistF.reserve(mcDist.size());
      std::vector<float> dataDistF; dataDistF.reserve(dataDistF.size());
      std::copy(mcDist.begin(), mcDist.end(), std::back_inserter(mcDistF));
      std::copy(dataDist.begin(), dataDist.end(), std::back_inserter(dataDistF));

      // std::cout << "mcDistF.size() " << mcDistF.size() << " dataDistF.size() " << dataDistF.size() << std::endl;
      fLumiWeights = edm::LumiReWeighting(mcDistF, dataDistF);
    }
    else {
      fWeights = iConfig.getParameter<std::vector<double> >("weights");
    }
    edm::Service<TFileService> fs;
    hWeights = fs->make<TH1F>("pileupReweightWeights", "Reweighting weight distribution", 100, 0, 10);
  }
  VertexWeight::~VertexWeight() {}

  std::pair<double, size_t> VertexWeight::getWeightAndSize(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    edm::Handle<edm::View<reco::Vertex> > hvertex;
    iEvent.getByLabel(fVertexSrc, hvertex);

    size_t vertSize = hvertex->size();

    if(!fEnabled || iEvent.isRealData()) {
      hWeights->Fill(1.0);
      return std::make_pair(1.0, vertSize);
    }

    double weight = std::numeric_limits<double>::quiet_NaN();
    if(fUseSimulatedPileup) {
      // See https://twiki.cern.ch/twiki/bin/view/CMS/PileupMCReweightingUtilities
      edm::Handle<std::vector<PileupSummaryInfo> >  hpu;
      iEvent.getByLabel(fPuSummarySrc, hpu);
      int npv = -1;

      if(fSummer11S4Mode) {
        npv = 0;
        for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpu->begin(); iPV != hpu->end(); ++iPV) {
          npv += iPV->getPU_NumInteractions();
        }
        float ave_nvtx = npv/3.;

        weight = fLumiWeights.weight3BX( ave_nvtx );

        // See https://twiki.cern.ch/twiki/bin/view/CMS/PileupSystematicErrors
        if(fShiftMean) {
          weight = weight*fMeanShifter.ShiftWeight( ave_nvtx );
        }
      }
      else {
        for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpu->begin(); iPV != hpu->end(); ++iPV) {
          if(iPV->getBunchCrossing() == 0) {
            npv = iPV->getPU_NumInteractions();
            break;
          }
        }
        if(npv < 0) {
          throw cms::Exception("LogicError") << "Didn't find number of interactions for in-time BX" << std::endl;
        }
        weight = fLumiWeights.weight( npv );
      }
    }
    else {
      size_t n = vertSize;
      if(n >= fWeights.size())
        n = fWeights.size() - 1;
      weight = fWeights[n];
    }

    /// Return "Vertex Weight" according to the number of vertices found in Event
    hWeights->Fill(weight);
    return std::make_pair(weight, vertSize);
  }


  double VertexWeight::getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    return getWeightAndSize(iEvent, iSetup).first;
  }
}
