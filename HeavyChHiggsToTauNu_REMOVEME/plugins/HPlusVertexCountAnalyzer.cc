#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include<vector>

#include<TH1F.h>

class HPlusVertexCountAnalyzer: public edm::EDAnalyzer {
 public:

  explicit HPlusVertexCountAnalyzer(const edm::ParameterSet&);
  ~HPlusVertexCountAnalyzer();

 private:
  virtual void beginJob();
  virtual void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  struct Histo {
    Histo(const edm::InputTag& src, TH1 *histo): src_(src), histo_(histo) {}

    edm::InputTag src_;
    TH1 *histo_;
  };

  std::vector<Histo> histos_;
  edm::InputTag weights_;
  bool usingWeights_;
};

HPlusVertexCountAnalyzer::HPlusVertexCountAnalyzer(const edm::ParameterSet& iConfig):
  weights_(iConfig.getUntrackedParameter<edm::InputTag>("weights", edm::InputTag("fake"))),
  usingWeights_(iConfig.exists("weights"))
{
  const std::vector<edm::InputTag>& tags = iConfig.getUntrackedParameter<std::vector<edm::InputTag> >("src");
  int nbins = iConfig.getUntrackedParameter<int>("nbins");
  double min = iConfig.getUntrackedParameter<double>("min");
  double max = iConfig.getUntrackedParameter<double>("max");

  edm::Service<TFileService> fs;

  histos_.reserve(tags.size());
  for(std::vector<edm::InputTag>::const_iterator iTag = tags.begin(); iTag != tags.end(); ++iTag) {
    std::string name = iTag->encode();
    TH1 *histo = fs->make<TH1F>(name.c_str(), name.c_str(), nbins, min, max);
    histo->Sumw2();
    histos_.push_back(Histo(*iTag, histo));
  }
  
}
HPlusVertexCountAnalyzer::~HPlusVertexCountAnalyzer() {}
void HPlusVertexCountAnalyzer::beginJob() {}

void HPlusVertexCountAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  double weight = 1.0;
  if(usingWeights_) {
    edm::Handle<double> hweight;
    iEvent.getByLabel(weights_, hweight);
    weight = *hweight;
  }

  edm::Handle<edm::View<reco::Vertex> > hvertices;
  for(std::vector<Histo>::iterator iHisto = histos_.begin(); iHisto != histos_.end(); ++iHisto) {
    iEvent.getByLabel(iHisto->src_, hvertices);
    iHisto->histo_->Fill(hvertices->size(), weight);
  }
}

void HPlusVertexCountAnalyzer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusVertexCountAnalyzer);
