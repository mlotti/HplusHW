#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 

namespace HPlus {
  VertexWeight::VertexWeight(const edm::ParameterSet& iConfig):
    fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
    fPileupSrc(iConfig.getParameter<edm::InputTag>("pileupSrc")),
    fWeights(iConfig.getParameter<std::vector<double> >("weights")),
    fUseSimulatedPileup(iConfig.getParameter<bool>("useSimulatedPileup")),
    fEnabled(iConfig.getParameter<bool>("enabled"))
  {}
  VertexWeight::~VertexWeight() {}

  std::pair<double, size_t> VertexWeight::getWeightAndSize(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    edm::Handle<edm::View<reco::Vertex> > hvertex;
    iEvent.getByLabel(fVertexSrc, hvertex);

    if(!fEnabled)
      return std::make_pair(1.0, hvertex->size());

    size_t n = 0;
    if(fUseSimulatedPileup) {
      edm::Handle<std::vector<PileupSummaryInfo> > hpileup;
      iEvent.getByLabel(fPileupSrc, hpileup);

      // https://twiki.cern.ch/twiki/bin/view/CMS/PileupInformation#Accessing_PileupSummaryInfo_AN1
      std::vector<PileupSummaryInfo>::const_iterator iBX = hpileup->begin();
      for(; iBX != hpileup->end(); ++iBX) {
        // Bunch crossing 0 is the in-time crossing
        if(iBX->getBunchCrossing() == 0) {
          n = iBX->getPU_NumInteractions();
        }
      }
      if(iBX == hpileup->end())
        throw cms::Exception("LogicError") << "Did not find bunch crossing 0 from the PileupSummaryInfo" << std::endl;
    }
    else
      n = hvertex->size();

    if(n >= fWeights.size())
      n = fWeights.size()-1;

    return std::make_pair(fWeights[n], hvertex->size());
  }


  double VertexWeight::getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    return getWeightAndSize(iEvent, iSetup).first;
  }
}
