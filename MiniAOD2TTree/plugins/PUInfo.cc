#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"


#include "DataFormats/VertexReco/interface/Vertex.h"

#include "TFile.h"
#include "TH1F.h"

#include <iostream>
#include <vector>

/* Analyzer for dumping the MC PU distribution in a separate root file before skimming
   22102015/S.Lehti
*/
 
class PUInfo : public edm::EDAnalyzer {
    public:
	PUInfo(const edm::ParameterSet&);
	~PUInfo();

	void beginJob();
	void analyze( const edm::Event&, const edm::EventSetup&);
	void endJob();

    private:
        edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puSummaryToken;
        edm::EDGetTokenT<GenEventInfoProduct> eventInfoToken;
        edm::EDGetTokenT<std::vector<reco::Vertex> > pvToken;
        std::string filename;

	bool runOnData;

	TH1F* hPU;
};

PUInfo::PUInfo(const edm::ParameterSet& iConfig) :
  puSummaryToken(consumes<std::vector<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("PileupSummaryInfoSrc"))),
  eventInfoToken(consumes<GenEventInfoProduct>(edm::InputTag("generator"))),
  pvToken(consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("PileupSummaryInfoSrc"))),
  filename(iConfig.getParameter<std::string>("OutputFileName")),
  runOnData(iConfig.getUntrackedParameter<bool>("RunOnData",false))
{
  
  hPU = new TH1F("pileup","pileup",100,0,100);
}

PUInfo::~PUInfo() {}

void PUInfo::beginJob(){}
void PUInfo::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (!runOnData && iEvent.isRealData())
    return;
  std::cout << "check PUInfo::analyze" << std::endl;
  edm::Handle<GenEventInfoProduct> genEventInfoHandle;
  iEvent.getByToken(eventInfoToken, genEventInfoHandle);
  double w = 1.0;
  if (genEventInfoHandle.isValid()) {
    if (genEventInfoHandle->weight() < 0.0) {
      w = -1.0;
    }
  }
  edm::Handle<std::vector<PileupSummaryInfo> > hpileup;
    iEvent.getByToken(puSummaryToken, hpileup);
    if(hpileup.isValid()) {
std::cout << "check hpileup.isValid" << std::endl;
	short nPU = 0;
        for(std::vector<PileupSummaryInfo>::const_iterator iPV = hpileup->begin(); iPV != hpileup->end(); ++iPV) {
            if(iPV->getBunchCrossing() == 0) {
                nPU = iPV->getTrueNumInteractions();
                break;
            }
        }
	hPU->Fill(nPU, w);
    }
    edm::Handle<std::vector<reco::Vertex> > hPV2;
    iEvent.getByToken(pvToken, hPV2);
    if(hPV2.isValid()) {
        hPU->Fill(hPV2->size());
    }
}

void PUInfo::endJob(){
std::cout << "check PUInfo::endJob " << hPU->GetEntries() << std::endl;
  if(hPU->GetEntries() > 0){
    TFile* fOUT = TFile::Open(filename.c_str(),"RECREATE");
    fOUT->cd();
    hPU->Write();
    fOUT->Close();
  }
}

DEFINE_FWK_MODULE(PUInfo);
