#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/VertexReco/interface/Vertex.h"

#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include "TFile.h"

namespace HPlus {
  VertexWeight::VertexWeight(const edm::ParameterSet& iConfig, HPlus::HistoWrapper& histoWrapper):
    fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
    fPuSummarySrc(iConfig.getParameter<edm::InputTag>("puSummarySrc")),
    fEnabled(iConfig.getParameter<bool>("enabled")),
    fwEnabled(iConfig.getParameter<bool>("weightDistributionEnable"))
  {
    edm::Service<TFileService> fs;
    TFileDirectory dir = fs->mkdir("pileupReweight");

    // ATM not possible to change to HistoWrapper, as it is used to
    // hold the weights if fwEnabled is true
    hWeights = dir.make<TH1F>("pileupReweightWeights", "Reweighting weight distribution", 500, 0, 50);

    hTrueInteractionsMinus1 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, dir,
                                                        "trueNumberInteractionsBXminus1", "", 500, 0, 50);
    hTrueInteractions0 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, dir,
                                                   "trueNumberInteractionsBX0", "", 500, 0, 50);
    hTrueInteractionsPlus1 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, dir,
                                                       "trueNumberInteractionsBXplus1", "", 500, 0, 50);

    if(!fEnabled)
      return;

    if(fwEnabled){
      // Use edm::FileInPath to find the file, must do like this in
      // case fwEnabled is false and the file does not intentionally exist
      std::string filePath = iConfig.getParameter<std::string>("weightDistribution");
      edm::FileInPath myWeightPUdistribution = edm::FileInPath(filePath);
        std::string myWeightPUdistributionLabel = iConfig.getParameter<std::string>("weightDistributionLabel");

	TFile* fIN = TFile::Open(myWeightPUdistribution.fullPath().c_str(),"r");
	TH1F* weights = (TH1F*)fIN->Get(myWeightPUdistributionLabel.c_str());
	for(int i = 0; i < weights->GetNbinsX(); ++i){
	  hWeights->SetBinContent(i,weights->GetBinContent(i));
	}
	fIN->Close();
    }else{
    // Obtain data and mc distribution root files and labels
    // Both histograms are normalised to unit area (make sure they have same number of bins)
    edm::FileInPath myDataPUdistribution = iConfig.getParameter<edm::FileInPath>("dataPUdistribution");
    std::string myDataPUdistributionLabel = iConfig.getParameter<std::string>("dataPUdistributionLabel");
    edm::FileInPath myMCPUdistribution = iConfig.getParameter<edm::FileInPath>("mcPUdistribution");
    std::string myMCPUdistributionLabel = iConfig.getParameter<std::string>("mcPUdistributionLabel");
    
    fLumiWeights = edm::LumiReWeighting(myMCPUdistribution.fullPath(), myDataPUdistribution.fullPath(), myMCPUdistributionLabel, myDataPUdistributionLabel);
    }
  }
  VertexWeight::~VertexWeight() {
    //for(int i = 0; i < hWeights->GetNbinsX(); ++i){
    //  std::cout << "Weight " << i << " " << hWeights->GetBinCenter(i) << " " << hWeights->GetBinContent(i) << std::endl;
    //}
  }

  std::pair<double, size_t> VertexWeight::getWeightAndSize(const edm::Event& iEvent, const edm::EventSetup& iSetup, bool getSize) const {
    size_t vertSize = 0;
    if(getSize) {
      edm::Handle<edm::View<reco::Vertex> > hvertex;
      iEvent.getByLabel(fVertexSrc, hvertex);

      vertSize = hvertex->size();
    }

    if(!fEnabled || iEvent.isRealData()) {
      hWeights->Fill(1.0);
      return std::make_pair(1.0, vertSize);
    }

    //double weight = std::numeric_limits<double>::quiet_NaN();

    // See https://twiki.cern.ch/twiki/bin/view/CMS/PileupMCReweightingUtilities
    edm::Handle<std::vector<PileupSummaryInfo> >  hpu;
    iEvent.getByLabel(fPuSummarySrc, hpu);

    float n0 = -1;
    float nm1 = -1;
    float np1 = -1;
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

    hTrueInteractionsMinus1->Fill(nm1);
    hTrueInteractions0->Fill(n0);
    hTrueInteractionsPlus1->Fill(np1);

    // Obtain weight
    double weight = 0;
    if(fwEnabled){
	weight = myLumiWeights(n0);
    }else{
	weight = fLumiWeights.weight(n0);
        // Return "Vertex Weight" according to the number of vertices found in Event
        hWeights->Fill(weight);
    }
    return std::make_pair(weight, vertSize);
  }


  double VertexWeight::getWeight(const edm::Event& iEvent, const edm::EventSetup& iSetup) const {
    return getWeightAndSize(iEvent, iSetup, false).first;
  }

  double VertexWeight::myLumiWeights(float nvtx) const {
    if(nvtx < 0 || nvtx > hWeights->GetXaxis()->GetXmax()) return 0;
    return hWeights->GetBinContent(hWeights->FindFixBin(nvtx));
  }
}
