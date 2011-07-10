#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/VertexReco/interface/Vertex.h"

namespace HPlus {
  VertexWeight::VertexWeight(const edm::ParameterSet& iConfig):
    fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
    fUseSimulatedPileup(iConfig.getParameter<bool>("useSimulatedPileup")),
    fEnabled(iConfig.getParameter<bool>("enabled"))
  {
    if(fUseSimulatedPileup) {
      std::vector<double> mcDist = iConfig.getParameter<std::vector<double> >("mcDist");
      std::vector<double> dataDist = iConfig.getParameter<std::vector<double> >("dataDist");
      std::vector<float> mcDistF; mcDistF.reserve(mcDist.size());
      std::vector<float> dataDistF; dataDistF.reserve(dataDistF.size());
      std::copy(mcDist.begin(), mcDist.end(), std::back_inserter(mcDistF));
      std::copy(dataDist.begin(), dataDist.end(), std::back_inserter(dataDistF));

      std::cout << "mcDistF.size() " << mcDistF.size() << " dataDistF.size() " << dataDistF.size() << std::endl;
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

    size_t vertSize = 0;
    if(hvertex.isValid())
      vertSize = hvertex->size();

    if(!fEnabled || iEvent.isRealData()) {
      hWeights->Fill(1.0);
      return std::make_pair(1.0, vertSize);
    }

    double weight = std::numeric_limits<double>::quiet_NaN();
    if(fUseSimulatedPileup)
      // According to
      // https://twiki.cern.ch/twiki/bin/view/CMS/PileupMCReweightingUtilities
      // this checks from the provenance if the MC was generated with
      // faulty OOTPU, and gives correct weight for that
      weight = fLumiWeights.weightOOT(iEvent);
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
