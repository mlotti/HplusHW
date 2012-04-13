#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

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
    fEnabled(iConfig.getParameter<bool>("enabled"))
  {
    edm::Service<TFileService> fs;
    hWeights = fs->make<TH1F>("pileupReweightWeights", "Reweighting weight distribution", 100, 0, 10);

    if(!fEnabled)
      return;

    // Obtain data and mc distribution root files and labels
    // Both histograms are normalised to unit area (make sure they have same number of bins)
    edm::FileInPath myDataPUdistribution = iConfig.getParameter<edm::FileInPath>("dataPUdistribution");
    std::string myDataPUdistributionLabel = iConfig.getParameter<std::string>("dataPUdistributionLabel");
    edm::FileInPath myMCPUdistribution = iConfig.getParameter<edm::FileInPath>("mcPUdistribution");
    std::string myMCPUdistributionLabel = iConfig.getParameter<std::string>("mcPUdistributionLabel");
    
    fLumiWeights = edm::LumiReWeighting(myMCPUdistribution.fullPath(), myDataPUdistribution.fullPath(), myMCPUdistributionLabel, myDataPUdistributionLabel);
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

    //double weight = std::numeric_limits<double>::quiet_NaN();

    // See https://twiki.cern.ch/twiki/bin/view/CMS/PileupMCReweightingUtilities
    edm::Handle<std::vector<PileupSummaryInfo> >  hpu;
    iEvent.getByLabel(fPuSummarySrc, hpu);

    int n0 = -1;
    int nm1 = -1;
    int np1 = -1;
    for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpu->begin(); iPV != hpu->end(); ++iPV) {
      if(iPV->getBunchCrossing() == -1)
        nm1 = iPV->getTrueNumInteractions();
      else if(iPV->getBunchCrossing() == 0)
        n0 = iPV->getTrueNumInteractions();
      else if(iPV->getBunchCrossing() == 1)
        np1 = iPV->getTrueNumInteractions();
    }
    if(n0 < 0)
      throw cms::Exception("Assert") << "VertexWeight: Didn't find the number of interactions for BX 0" << std::endl;;

    // Obtain weight
    double weight = fLumiWeights.weight(n0);
    
    // Return "Vertex Weight" according to the number of vertices found in Event
    hWeights->Fill(weight);
    return std::make_pair(weight, vertSize);
  }


  double VertexWeight::getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    return getWeightAndSize(iEvent, iSetup).first;
  }
}
