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
    fMeanShifter(iConfig.getParameter<double>("shiftMeanAmount")),
    fUseSimulatedPileup(iConfig.getParameter<bool>("useSimulatedPileup")),
    fEnabled(iConfig.getParameter<bool>("enabled")),
    fShiftMean(iConfig.getParameter<bool>("shiftMean"))
  {
    edm::Service<TFileService> fs;
    hWeights = fs->make<TH1F>("pileupReweightWeights", "Reweighting weight distribution", 100, 0, 10);

    if(!fEnabled)
      return;

    if(fShiftMean && !fUseSimulatedPileup) {
      throw cms::Exception("Configuration") << "VertexWeight: shiftMean can be used only with the reweighting by simulated PU interactions (not reconstructed vertices)" << std::endl;
    }

    std::string method = iConfig.getParameter<std::string>("method");
    if(method == "intime")
      fMethod = kIntime;
    else if(method == "3D") {
      fMethod = k3D;
    }
    else
      throw cms::Exception("Configuration") << "VertexWeight: method can be only 'intime' or '3D'" << std::endl;

    if(fUseSimulatedPileup) {
      std::string mcDistName = "mcDistIntime";
      std::string dataDistName = "dataDistIntime";
      if(fMethod == k3D) {
        mcDistName = "mcDist3D";
        dataDistName = "dataDist3D";
      }

      std::vector<double> mcDist = iConfig.getParameter<std::vector<double> >(mcDistName);
      std::vector<double> dataDist = iConfig.getParameter<std::vector<double> >(dataDistName);
      std::vector<float> mcDistF; mcDistF.reserve(mcDist.size());
      std::vector<float> dataDistF; dataDistF.reserve(dataDistF.size());
      std::copy(mcDist.begin(), mcDist.end(), std::back_inserter(mcDistF));
      std::copy(dataDist.begin(), dataDist.end(), std::back_inserter(dataDistF));

      // std::cout << "mcDistF.size() " << mcDistF.size() << " dataDistF.size() " << dataDistF.size() << std::endl;
      fLumiWeights = edm::LumiReWeighting(mcDistF, dataDistF);

      if(fMethod == k3D) {
        std::string fileName = iConfig.getParameter<std::string>("weightFile3D");
        if(fileName.size() == 0) {
          fLumiWeights.weight3D_init();
          throw cms::Exception("Configuration") << "VwetexWeight: weightFile3D was empty, thus the file for 3D weights was then generated with a name 'Weight3D.root'" << std::endl;
        }
        edm::FileInPath fip(fileName);
        fLumiWeights.weight3D_init(fip.fullPath());
      }
    }
    else {
      fWeights = iConfig.getParameter<std::vector<double> >("weights");
    }
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

      int n0 = -1;
      int nm1 = -1;
      int np1 = -1;
      for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpu->begin(); iPV != hpu->end(); ++iPV) {
        if(iPV->getBunchCrossing() == -1)
          nm1 = iPV->getPU_NumInteractions();
        else if(iPV->getBunchCrossing() == 0)
          n0 = iPV->getPU_NumInteractions();
        else if(iPV->getBunchCrossing() == 1)
          np1 = iPV->getPU_NumInteractions();
      }
      if(n0 < 0)
        throw cms::Exception("Assert") << "VertexWeight: Didn't find the number of interactions for BX 0" << std::endl;;
      if(fMethod == kIntime) {
        weight = fLumiWeights.weight(n0);
      }
      else if(fMethod == k3D) {
        if(nm1 < 0)
          throw cms::Exception("Assert") << "VertexWeight: Didn't find the number of interactions for BX -1" << std::endl;;
        if(np1 < 0)
          throw cms::Exception("Assert") << "VertexWeight: Didn't find the number of interactions for BX +1" << std::endl;;

        weight = fLumiWeights.weight3D(nm1, n0, np1);
      }
      else {
        throw cms::Exception("Assert") << "This should never be reached at " << __FILE__ << ":" << __LINE__ << std::endl;
      }
      
      // See https://twiki.cern.ch/twiki/bin/view/CMS/PileupSystematicErrors
      if(fShiftMean) {
        weight = weight*fMeanShifter.ShiftWeight( n0 );
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
